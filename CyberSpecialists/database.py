# -*- coding: utf-8 -*-
"""
Database module - User authentication, leaderboard, and parental controls
"""

import sqlite3
import hashlib
from datetime import datetime


class Database:
    def __init__(self, db_file='game.db'):
        self.db_file = db_file
        self.conn = sqlite3.connect(self.db_file)  # Persistent connection
        self.init_database()
        self.migrate_database()

    def init_database(self):
        """Initialize database tables"""
        cursor = self.conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                language TEXT DEFAULT 'mk',
                play_time_limit INTEGER DEFAULT 60,
                today_play_time INTEGER DEFAULT 0,
                last_play_date TEXT DEFAULT NULL
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                score INTEGER NOT NULL,
                level INTEGER NOT NULL,
                time_taken INTEGER NOT NULL,
                questions_correct INTEGER NOT NULL,
                questions_total INTEGER NOT NULL,
                completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key TEXT UNIQUE NOT NULL,
                value TEXT NOT NULL
            )
        ''')

        self.conn.commit()

    def migrate_database(self):
        """Migrate old database to new schema"""
        cursor = self.conn.cursor()

        # Check if play_time_limit column exists
        cursor.execute("PRAGMA table_info(users)")
        columns = [column[1] for column in cursor.fetchall()]

        if 'play_time_limit' not in columns:
            print("Migrating database to add parental controls...")
            cursor.execute('ALTER TABLE users ADD COLUMN play_time_limit INTEGER DEFAULT 60')
            cursor.execute('ALTER TABLE users ADD COLUMN today_play_time INTEGER DEFAULT 0')
            cursor.execute('ALTER TABLE users ADD COLUMN last_play_date TEXT DEFAULT NULL')
            self.conn.commit()
            print("Database migration complete!")

    def hash_password(self, password):
        """Hash password using SHA256"""
        return hashlib.sha256(password.encode()).hexdigest()

    def register_user(self, username, password, language='mk', play_time_limit=60):
        """Register new user with play time limit"""
        try:
            cursor = self.conn.cursor()
            password_hash = self.hash_password(password)
            today = datetime.now().strftime('%Y-%m-%d')
            cursor.execute('''
                INSERT INTO users (username, password_hash, language, play_time_limit, today_play_time, last_play_date) 
                VALUES (?, ?, ?, ?, 0, ?)
            ''', (username, password_hash, language, play_time_limit, today))
            self.conn.commit()
            user_id = cursor.lastrowid
            return True, user_id
        except sqlite3.IntegrityError:
            return False, None

    def login_user(self, username, password):
        """Login user and check play time"""
        cursor = self.conn.cursor()
        password_hash = self.hash_password(password)
        cursor.execute('''
            SELECT id, username, language, play_time_limit, today_play_time, last_play_date 
            FROM users 
            WHERE username = ? AND password_hash = ?
        ''', (username, password_hash))
        user = cursor.fetchone()

        if user:
            today = datetime.now().strftime('%Y-%m-%d')
            # Reset play time if it's a new day
            if user[5] != today:
                self.reset_daily_play_time(user[0])
                today_play_time = 0
            else:
                today_play_time = user[4]

            return True, {
                'id': user[0],
                'username': user[1],
                'language': user[2],
                'play_time_limit': user[3],
                'today_play_time': today_play_time
            }
        return False, None

    def reset_daily_play_time(self, user_id):
        """Reset daily play time for new day"""
        cursor = self.conn.cursor()
        today = datetime.now().strftime('%Y-%m-%d')
        cursor.execute('''
            UPDATE users 
            SET today_play_time = 0, last_play_date = ?
            WHERE id = ?
        ''', (today, user_id))
        self.conn.commit()

    def update_play_time(self, user_id, minutes_played):
        """Update today's play time"""
        cursor = self.conn.cursor()
        today = datetime.now().strftime('%Y-%m-%d')
        cursor.execute('''
            UPDATE users 
            SET today_play_time = today_play_time + ?, last_play_date = ?
            WHERE id = ?
        ''', (minutes_played, today, user_id))
        self.conn.commit()

    def get_play_time_info(self, user_id):
        """Get play time information"""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT play_time_limit, today_play_time, last_play_date
            FROM users 
            WHERE id = ?
        ''', (user_id,))
        result = cursor.fetchone()

        if result:
            today = datetime.now().strftime('%Y-%m-%d')
            if result[2] != today:
                self.reset_daily_play_time(user_id)
                return result[0], 0  # limit, played
            return result[0], result[1]  # limit, played
        return 60, 0

    def get_play_time_remaining(self, user_id):
        """Get remaining play time in minutes"""
        limit, played = self.get_play_time_info(user_id)
        return max(0, limit - played)

    def extend_play_time(self, user_id, extra_minutes):
        """Extend today's play time limit temporarily (parent permission)"""
        cursor = self.conn.cursor()
        cursor.execute('''
            UPDATE users 
            SET play_time_limit = play_time_limit + ?
            WHERE id = ?
        ''', (extra_minutes, user_id))
        self.conn.commit()

    def update_play_time_limit(self, user_id, new_limit):
        """Update the daily play time limit permanently (parent changes settings)"""
        cursor = self.conn.cursor()
        cursor.execute('''
            UPDATE users 
            SET play_time_limit = ?
            WHERE id = ?
        ''', (new_limit, user_id))
        self.conn.commit()

    def stop_play_for_today(self, user_id):
        """Set play time to limit (stop for today)"""
        cursor = self.conn.cursor()
        cursor.execute('''
            UPDATE users 
            SET today_play_time = play_time_limit
            WHERE id = ?
        ''', (user_id,))
        self.conn.commit()

    def save_score(self, user_id, level, score, time_taken, questions_correct, questions_total):
        """Save player score"""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO scores (user_id, level, score, time_taken, questions_correct, questions_total)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, level, score, time_taken, questions_correct, questions_total))
        self.conn.commit()

    def get_leaderboard(self, level=None, limit=10):
        """Get top scores"""
        cursor = self.conn.cursor()

        if level:
            query = '''
                SELECT u.username, s.score, s.time_taken, s.questions_correct, s.questions_total, s.completed_at
                FROM scores s
                JOIN users u ON s.user_id = u.id
                WHERE s.level = ?
                ORDER BY s.score DESC, s.time_taken ASC
                LIMIT ?
            '''
            cursor.execute(query, (level, limit))
        else:
            query = '''
                SELECT u.username, SUM(s.score) as total_score, SUM(s.questions_correct) as total_correct
                FROM scores s
                JOIN users u ON s.user_id = u.id
                GROUP BY u.id
                ORDER BY total_score DESC
                LIMIT ?
            '''
            cursor.execute(query, (limit,))

        results = cursor.fetchall()
        return results

    def get_or_create_setting(self, key, default_value):
        """Get setting or create with default"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT value FROM settings WHERE key = ?', (key,))
        result = cursor.fetchone()

        if result is None:
            cursor.execute('INSERT INTO settings (key, value) VALUES (?, ?)', (key, default_value))
            self.conn.commit()
            return default_value

        return result[0]

    def set_setting(self, key, value):
        """Set setting value"""
        cursor = self.conn.cursor()
        cursor.execute('INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)', (key, value))
        self.conn.commit()