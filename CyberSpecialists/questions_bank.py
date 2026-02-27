# -*- coding: utf-8 -*-

import random

# ==========================================
# LEVEL 1: PASSWORD SECURITY
# ==========================================

LEVEL_1_QUESTIONS_MK = [
    # --- Original Questions ---
    {
        "question": "Која лозинка е најсигурна?",
        "options": [
            {"text": "password123", "correct": False},
            {"text": "M@rk0#2024!", "correct": True},
            {"text": "12345678", "correct": False}
        ]
    },
    {
        "question": "Колку карактери треба да има една јака лозинка?",
        "options": [
            {"text": "Најмалку 4", "correct": False},
            {"text": "Најмалку 8", "correct": True},
            {"text": "Не е важно", "correct": False}
        ]
    },
    {
        "question": "Што треба да содржи една јака лозинка?",
        "options": [
            {"text": "Само букви", "correct": False},
            {"text": "Букви, бројки и симболи", "correct": True},
            {"text": "Само твоето име", "correct": False}
        ]
    },
    {
        "question": "Дали треба да користиш иста лозинка за сè?",
        "options": [
            {"text": "Да, полесно е", "correct": False},
            {"text": "Не, треба различни лозинки", "correct": True},
            {"text": "Не е важно", "correct": False}
        ]
    },
    {
        "question": "Кога треба да ја смениш лозинката?",
        "options": [
            {"text": "Никогаш", "correct": False},
            {"text": "На секои 3-6 месеци", "correct": True},
            {"text": "Само кога ќе ја заборавам", "correct": False}
        ]
    },
    {
        "question": "Што е Two Factor Authentication (2FA)?",
        "options": [
            {"text": "Двапати да ја внесеш лозинката", "correct": False},
            {"text": "Дополнителна сигурност со код", "correct": True},
            {"text": "Не е важно", "correct": False}
        ]
    },
    {
        "question": "Дали треба да ја запишеш лозинката на хартија?",
        "options": [
            {"text": "Да, за да не ја заборавам", "correct": False},
            {"text": "Не, користи password manager", "correct": True},
            {"text": "Може, само да ја оставиш на маса", "correct": False}
        ]
    },
    {
        "question": "Која од овие е најслаба лозинка?",
        "options": [
            {"text": "Tr0nG$P@ssw0rd!", "correct": False},
            {"text": "123456", "correct": True},
            {"text": "MyD0g&C@t#2024", "correct": False}
        ]
    },
    {
        "question": "Што е password manager?",
        "options": [
            {"text": "Програма за чување лозинки", "correct": True},
            {"text": "Начин да хакнеш лозинки", "correct": False},
            {"text": "Непотребна работа", "correct": False}
        ]
    },
    {
        "question": "Дали треба да ја споделиш лозинката со другар?",
        "options": [
            {"text": "Да, ако ми е најдобар другар", "correct": False},
            {"text": "Не, никогаш", "correct": True},
            {"text": "Само преку Facebook", "correct": False}
        ]
    },
    # --- NEW QUESTIONS ---
    {
        "question": "Што е 'Security Question' (Безбедносно прашање)?",
        "options": [
            {"text": "Прашање за ресетирање лозинка", "correct": True},
            {"text": "Прашање од полиција", "correct": False},
            {"text": "Најтешкото прашање во тест", "correct": False}
        ]
    },
    {
        "question": "Дали е паметно да користиш 'qwerty' за лозинка?",
        "options": [
            {"text": "Да, лесно се памти", "correct": False},
            {"text": "Не, премногу е честа", "correct": True},
            {"text": "Само за Facebook", "correct": False}
        ]
    },
    {
        "question": "Што треба да направиш ако го продадеш телефонот?",
        "options": [
            {"text": "Ништо", "correct": False},
            {"text": "Избриши ги само сликите", "correct": False},
            {"text": "Factory Reset (Фабричко бришење)", "correct": True}
        ]
    },
    {
        "question": "Дали прелистувачот (browser) треба да ги памти лозинките на јавен компјутер?",
        "options": [
            {"text": "Никогаш", "correct": True},
            {"text": "Да, побрзо е", "correct": False},
            {"text": "Само ако е Google Chrome", "correct": False}
        ]
    },
    {
        "question": "Што е 'Lock Screen'?",
        "options": [
            {"text": "Скршен екран", "correct": False},
            {"text": "Заклучување на уредот со код/шема", "correct": True},
            {"text": "Позадина на телефонот", "correct": False}
        ]
    }
]

LEVEL_1_QUESTIONS_SQ = [
    # --- Original Questions ---
    {
        "question": "Cili fjalëkalim është më i sigurt?",
        "options": [
            {"text": "password123", "correct": False},
            {"text": "M@rk0#2024!", "correct": True},
            {"text": "12345678", "correct": False}
        ]
    },
    {
        "question": "Sa karaktere duhet të ketë një fjalëkalim i fortë?",
        "options": [
            {"text": "Të paktën 4", "correct": False},
            {"text": "Të paktën 8", "correct": True},
            {"text": "Nuk ka rëndësi", "correct": False}
        ]
    },
    {
        "question": "Çfarë duhet të përmbajë një fjalëkalim i fortë?",
        "options": [
            {"text": "Vetëm shkronja", "correct": False},
            {"text": "Shkronja, numra dhe simbole", "correct": True},
            {"text": "Vetëm emrin tënd", "correct": False}
        ]
    },
    {
        "question": "A duhet të përdorësh të njëjtin fjalëkalim për gjithçka?",
        "options": [
            {"text": "Po, është më lehtë", "correct": False},
            {"text": "Jo, duhen fjalëkalime të ndryshme", "correct": True},
            {"text": "Nuk ka rëndësi", "correct": False}
        ]
    },
    {
        "question": "Kur duhet të ndryshosh fjalëkalimin?",
        "options": [
            {"text": "Kurrë", "correct": False},
            {"text": "Çdo 3-6 muaj", "correct": True},
            {"text": "Vetëm kur ta harroj", "correct": False}
        ]
    },
    {
        "question": "Çfarë është Two Factor Authentication (2FA)?",
        "options": [
            {"text": "Të futësh fjalëkalimin dy herë", "correct": False},
            {"text": "Siguri shtesë me kod", "correct": True},
            {"text": "Nuk ka rëndësi", "correct": False}
        ]
    },
    {
        "question": "A duhet të shkruash fjalëkalimin në letër?",
        "options": [
            {"text": "Po, që të mos e harroj", "correct": False},
            {"text": "Jo, përdor password manager", "correct": True},
            {"text": "Mund, vetëm ta lësh në tavolinë", "correct": False}
        ]
    },
    {
        "question": "Cili është fjalëkalimi më i dobët?",
        "options": [
            {"text": "Tr0nG$P@ssw0rd!", "correct": False},
            {"text": "123456", "correct": True},
            {"text": "MyD0g&C@t#2024", "correct": False}
        ]
    },
    {
        "question": "Çfarë është password manager?",
        "options": [
            {"text": "Program për ruajtjen e fjalëkalimeve", "correct": True},
            {"text": "Mënyrë për të vjedhur fjalëkalime", "correct": False},
            {"text": "Diçka e panevojshme", "correct": False}
        ]
    },
    {
        "question": "A duhet të ndash fjalëkalimin me shokun?",
        "options": [
            {"text": "Po, nëse është shoku im më i mirë", "correct": False},
            {"text": "Jo, kurrë", "correct": True},
            {"text": "Vetëm nëpërmjet Facebook", "correct": False}
        ]
    },
    # --- NEW QUESTIONS ---
    {
        "question": "Çfarë është 'Security Question' (Pyetja e sigurisë)?",
        "options": [
            {"text": "Pyetje për të rikthyer fjalëkalimin", "correct": True},
            {"text": "Pyetje nga policia", "correct": False},
            {"text": "Pyetja më e vështirë në test", "correct": False}
        ]
    },
    {
        "question": "A është e mençur të përdorësh 'qwerty' si fjalëkalim?",
        "options": [
            {"text": "Po, mbahet mend lehtë", "correct": False},
            {"text": "Jo, është shumë e zakonshme", "correct": True},
            {"text": "Vetëm për Facebook", "correct": False}
        ]
    },
    {
        "question": "Çfarë duhet të bësh nëse e shet telefonin?",
        "options": [
            {"text": "Asgjë", "correct": False},
            {"text": "Fshi vetëm fotot", "correct": False},
            {"text": "Factory Reset (Fshirje totale)", "correct": True}
        ]
    },
    {
        "question": "A duhet që shfletuesi (browser) të ruajë fjalëkalimet në një kompjuter publik?",
        "options": [
            {"text": "Kurrë", "correct": True},
            {"text": "Po, është më shpejt", "correct": False},
            {"text": "Vetëm nëse është Google Chrome", "correct": False}
        ]
    },
    {
        "question": "Çfarë është 'Lock Screen'?",
        "options": [
            {"text": "Ekran i thyer", "correct": False},
            {"text": "Kyçja e pajisjes me kod/model", "correct": True},
            {"text": "Sfondi i telefonit", "correct": False}
        ]
    }
]

# ==========================================
# LEVEL 2: MESSAGES & PHISHING
# ==========================================

LEVEL_2_QUESTIONS_MK = [
    # --- Original Questions ---
    {
        "question": "Што е phishing?",
        "options": [
            {"text": "Измамнички email или порака", "correct": True},
            {"text": "Начин да ловам риба", "correct": False},
            {"text": "Вид на видео игра", "correct": False}
        ]
    },
    {
        "question": "Како можеш да препознаеш phishing email?",
        "options": [
            {"text": "Има правописни грешки", "correct": True},
            {"text": "Секогаш е од банката", "correct": False},
            {"text": "Има многу слики", "correct": False}
        ]
    },
    {
        "question": "Што треба да направиш ако добиеш сомнителен email?",
        "options": [
            {"text": "Да кликнеш на линкот да видиш", "correct": False},
            {"text": "Да го избришеш и пријавиш", "correct": True},
            {"text": "Да го проследиш на пријател", "correct": False}
        ]
    },
    {
        "question": "Дали треба да кликнеш на линк во непознат email?",
        "options": [
            {"text": "Не, може да биде опасно", "correct": True},
            {"text": "Да, за да видам што е", "correct": False},
            {"text": "Само ако изгледа професионално", "correct": False}
        ]
    },
    {
        "question": "Што е spear phishing?",
        "options": [
            {"text": "Насочен phishing напад", "correct": True},
            {"text": "Вид на риболов", "correct": False},
            {"text": "Антивирусна програма", "correct": False}
        ]
    },
    {
        "question": "Како можеш да провериш дали еден email е легитимен?",
        "options": [
            {"text": "Провери ја адресата на испраќачот", "correct": True},
            {"text": "По боите на текстот", "correct": False},
            {"text": "Ако има слики", "correct": False}
        ]
    },
    {
        "question": "Што треба да бараш во URL линкот?",
        "options": [
            {"text": "HTTPS и правилно име на домен", "correct": True},
            {"text": "Дали е кратко", "correct": False},
            {"text": "Дали има бројки", "correct": False}
        ]
    },
    # --- NEW QUESTIONS ---
    {
        "question": "Што е 'Smishing'?",
        "options": [
            {"text": "Phishing преку SMS пораки", "correct": True},
            {"text": "Смеење онлајн", "correct": False},
            {"text": "Апликација за слики", "correct": False}
        ]
    },
    {
        "question": "Дали треба да отвораш 'attachment' (прилог) од непознат испраќач?",
        "options": [
            {"text": "Да, може да е подарок", "correct": False},
            {"text": "Не, може да содржи вирус", "correct": True},
            {"text": "Само ако е PDF", "correct": False}
        ]
    },
    {
        "question": "Што значи ако ти стигне код за најава што не си го побарал?",
        "options": [
            {"text": "Грешка во системот", "correct": False},
            {"text": "Некој пробува да ти влезе во профилот", "correct": True},
            {"text": "Добил си награда", "correct": False}
        ]
    },
    {
        "question": "Дали банката некогаш ќе ти ја побара лозинката преку email?",
        "options": [
            {"text": "Да, за проверка", "correct": False},
            {"text": "Никогаш", "correct": True},
            {"text": "Само ако си блокиран", "correct": False}
        ]
    },
    {
        "question": "Што е 'Clickbait'?",
        "options": [
            {"text": "Сензационален наслов за да кликнеш", "correct": True},
            {"text": "Вид на глувче за компјутер", "correct": False},
            {"text": "Безбеден линк", "correct": False}
        ]
    }
]

LEVEL_2_QUESTIONS_SQ = [
    # --- Original Questions ---
    {
        "question": "Çfarë është phishing?",
        "options": [
            {"text": "Email ose mesazh mashtues", "correct": True},
            {"text": "Mënyrë për të peshkuar", "correct": False},
            {"text": "Lloj loje video", "correct": False}
        ]
    },
    {
        "question": "Si mund ta njohësh një email phishing?",
        "options": [
            {"text": "Ka gabime drejtshkrimore", "correct": True},
            {"text": "Gjithmonë është nga banka", "correct": False},
            {"text": "Ka shumë foto", "correct": False}
        ]
    },
    {
        "question": "Çfarë duhet të bësh nëse merr një email të dyshimtë?",
        "options": [
            {"text": "Të klikosh në link për të parë", "correct": False},
            {"text": "Ta fshish dhe ta raportosh", "correct": True},
            {"text": "Ta dërgosh te një shok", "correct": False}
        ]
    },
    {
        "question": "A duhet të klikosh në një link në një email të panjohur?",
        "options": [
            {"text": "Jo, mund të jetë e rrezikshme", "correct": True},
            {"text": "Po, për të parë çfarë është", "correct": False},
            {"text": "Vetëm nëse duket profesionale", "correct": False}
        ]
    },
    {
        "question": "Çfarë është spear phishing?",
        "options": [
            {"text": "Sulm phishing i synuar", "correct": True},
            {"text": "Lloj peshkimi", "correct": False},
            {"text": "Program antivirus", "correct": False}
        ]
    },
    {
        "question": "Si mund të verifikosh nëse një email është i vërtetë?",
        "options": [
            {"text": "Kontrollo adresën e dërguesit", "correct": True},
            {"text": "Sipas ngjyrave të tekstit", "correct": False},
            {"text": "Nëse ka foto", "correct": False}
        ]
    },
    {
        "question": "Çfarë duhet të kërkosh në një URL link?",
        "options": [
            {"text": "HTTPS dhe emër i saktë i domenit", "correct": True},
            {"text": "Nëse është i shkurtër", "correct": False},
            {"text": "Nëse ka numra", "correct": False}
        ]
    },
    # --- NEW QUESTIONS ---
    {
        "question": "Çfarë është 'Smishing'?",
        "options": [
            {"text": "Phishing përmes SMS", "correct": True},
            {"text": "Të qeshësh online", "correct": False},
            {"text": "Aplikacion për foto", "correct": False}
        ]
    },
    {
        "question": "A duhet të hapësh një 'attachment' (bashkëngjitje) nga një dërgues i panjohur?",
        "options": [
            {"text": "Po, mund të jetë dhuratë", "correct": False},
            {"text": "Jo, mund të ketë virus", "correct": True},
            {"text": "Vetëm nëse është PDF", "correct": False}
        ]
    },
    {
        "question": "Çfarë do të thotë nëse merr një kod hyrjeje që nuk e ke kërkuar?",
        "options": [
            {"text": "Gabim në sistem", "correct": False},
            {"text": "Dikush po përpiqet të hyjë në profilin tënd", "correct": True},
            {"text": "Ke fituar një çmim", "correct": False}
        ]
    },
    {
        "question": "A do ta kërkojë banka ndonjëherë fjalëkalimin tënd me email?",
        "options": [
            {"text": "Po, për verifikim", "correct": False},
            {"text": "Kurrë", "correct": True},
            {"text": "Vetëm nëse je bllokuar", "correct": False}
        ]
    },
    {
        "question": "Çfarë është 'Clickbait'?",
        "options": [
            {"text": "Titull sensacional për të klikuar", "correct": True},
            {"text": "Lloj mausi për kompjuter", "correct": False},
            {"text": "Link i sigurt", "correct": False}
        ]
    }
]

# ==========================================
# LEVEL 3: PERSONAL DATA & PRIVACY
# ==========================================

LEVEL_3_QUESTIONS_MK = [
    # --- Original Questions ---
    {
        "question": "Што треба да објавиш на социјални мрежи?",
        "options": [
            {"text": "Адресата на твојот дом", "correct": False},
            {"text": "Твоите омилени хобија", "correct": True},
            {"text": "Број на твојата картичка", "correct": False}
        ]
    },
    {
        "question": "Дали е безбедно да користиш јавен WiFi?",
        "options": [
            {"text": "Не, може да биде опасно", "correct": True},
            {"text": "Да, секогаш", "correct": False},
            {"text": "Само кога патувам", "correct": False}
        ]
    },
    {
        "question": "Што значи 'приватност'?",
        "options": [
            {"text": "Контрола над твоите информации", "correct": True},
            {"text": "Да немаш пријатели", "correct": False},
            {"text": "Да не користиш интернет", "correct": False}
        ]
    },
    {
        "question": "Дали треба да ја читаш Privacy Policy?",
        "options": [
            {"text": "Да, за да знаеш што прават со податоците", "correct": True},
            {"text": "Не, предолго е", "correct": False},
            {"text": "Не е важно", "correct": False}
        ]
    },
    {
        "question": "Што не треба да споделуваш онлајн?",
        "options": [
            {"text": "Твоето име и адреса", "correct": True},
            {"text": "Омилена боја", "correct": False},
            {"text": "Омилен филм", "correct": False}
        ]
    },
    {
        "question": "Дали е ОК да објавуваш фотографии од домашна адреса?",
        "options": [
            {"text": "Не, може да биде опасно", "correct": True},
            {"text": "Да, зошто не", "correct": False},
            {"text": "Само ако е убаво", "correct": False}
        ]
    },
    {
        "question": "Кој може да ги види твоите јавни објави?",
        "options": [
            {"text": "Секој на интернет", "correct": True},
            {"text": "Само пријателите", "correct": False},
            {"text": "Никој", "correct": False}
        ]
    },
    # --- NEW QUESTIONS ---
    {
        "question": "Што е VPN (Virtual Private Network)?",
        "options": [
            {"text": "Алатка за прикривање на локацијата", "correct": True},
            {"text": "Социјална мрежа", "correct": False},
            {"text": "Видео плеер", "correct": False}
        ]
    },
    {
        "question": "Зошто не треба да се 'чекираш' (Check-in) додека си на одмор?",
        "options": [
            {"text": "Крадците ќе знаат дека не си дома", "correct": True},
            {"text": "Ќе им биде љубоморно на пријателите", "correct": False},
            {"text": "Интернет е скап", "correct": False}
        ]
    },
    {
        "question": "Што се 'Cookies' (колачиња) на интернет?",
        "options": [
            {"text": "Податоци што памтат информации за тебе", "correct": True},
            {"text": "Вистински колачи", "correct": False},
            {"text": "Вирус", "correct": False}
        ]
    },
    {
        "question": "Дали апликација за батериска ламба треба да има пристап до твоите контакти?",
        "options": [
            {"text": "Да, за да работи", "correct": False},
            {"text": "Не, тоа е сомнително", "correct": True},
            {"text": "Можеби", "correct": False}
        ]
    },
    {
        "question": "Што значи 'Incognito Mode'?",
        "options": [
            {"text": "Прелистувачот не чува историја на тој уред", "correct": True},
            {"text": "Никој не може да те види", "correct": False},
            {"text": "Заштитен си од вируси", "correct": False}
        ]
    }
]

LEVEL_3_QUESTIONS_SQ = [
    # --- Original Questions ---
    {
        "question": "Çfarë duhet të postosh në rrjetet sociale?",
        "options": [
            {"text": "Adresën e shtëpisë sate", "correct": False},
            {"text": "Hobitë e tua të preferuara", "correct": True},
            {"text": "Numrin e kartës tënde", "correct": False}
        ]
    },
    {
        "question": "A është e sigurt të përdorësh WiFi publik?",
        "options": [
            {"text": "Jo, mund të jetë e rrezikshme", "correct": True},
            {"text": "Po, gjithmonë", "correct": False},
            {"text": "Vetëm kur udhëton", "correct": False}
        ]
    },
    {
        "question": "Çfarë do të thotë 'privatësi'?",
        "options": [
            {"text": "Kontrolli mbi informacionin tënd", "correct": True},
            {"text": "Të mos kesh shokë", "correct": False},
            {"text": "Të mos përdorësh internet", "correct": False}
        ]
    },
    {
        "question": "A duhet ta lexosh Privacy Policy?",
        "options": [
            {"text": "Po, për të ditur çfarë bëjnë me të dhënat", "correct": True},
            {"text": "Jo, është shumë e gjatë", "correct": False},
            {"text": "Nuk ka rëndësi", "correct": False}
        ]
    },
    {
        "question": "Çfarë nuk duhet të ndash online?",
        "options": [
            {"text": "Emrin dhe adresën tënde", "correct": True},
            {"text": "Ngjyrën e preferuar", "correct": False},
            {"text": "Filmin e preferuar", "correct": False}
        ]
    },
    {
        "question": "A është OK të postosh foto nga adresa e shtëpisë?",
        "options": [
            {"text": "Jo, mund të jetë e rrezikshme", "correct": True},
            {"text": "Po, pse jo", "correct": False},
            {"text": "Vetëm nëse është e bukur", "correct": False}
        ]
    },
    {
        "question": "Kush mund t'i shohë postimet e tua publike?",
        "options": [
            {"text": "Çdokush në internet", "correct": True},
            {"text": "Vetëm shokët", "correct": False},
            {"text": "Askush", "correct": False}
        ]
    },
    # --- NEW QUESTIONS ---
    {
        "question": "Çfarë është VPN (Virtual Private Network)?",
        "options": [
            {"text": "Mjet për të fshehur vendndodhjen", "correct": True},
            {"text": "Rrjet social", "correct": False},
            {"text": "Video player", "correct": False}
        ]
    },
    {
        "question": "Pse nuk duhet të bësh 'Check-in' kur je me pushime?",
        "options": [
            {"text": "Hajdutët do ta dinë që nuk je në shtëpi", "correct": True},
            {"text": "Shokët do të bëhen xhelozë", "correct": False},
            {"text": "Interneti është i shtrenjtë", "correct": False}
        ]
    },
    {
        "question": "Çfarë janë 'Cookies' në internet?",
        "options": [
            {"text": "Të dhëna që ruajnë informacione për ty", "correct": True},
            {"text": "Biskota të vërteta", "correct": False},
            {"text": "Virus", "correct": False}
        ]
    },
    {
        "question": "A duhet të ketë një aplikacion elektrik dore qasje në kontaktet e tua?",
        "options": [
            {"text": "Po, që të punojë", "correct": False},
            {"text": "Jo, është e dyshimtë", "correct": True},
            {"text": "Ndoshta", "correct": False}
        ]
    },
    {
        "question": "Çfarë do të thotë 'Incognito Mode'?",
        "options": [
            {"text": "Shfletuesi nuk ruan historikun në atë pajisje", "correct": True},
            {"text": "Askush nuk mund të të shohë", "correct": False},
            {"text": "Je i mbrojtur nga viruset", "correct": False}
        ]
    }
]

# ==========================================
# LEVEL 4: SCAMS & FRAUD
# ==========================================

LEVEL_4_QUESTIONS_MK = [
    # --- Original Questions ---
    {
        "question": "Што е онлајн измама?",
        "options": [
            {"text": "Обид да те излажат за пари/информации", "correct": True},
            {"text": "Начин на купување", "correct": False},
            {"text": "Вид на реклама", "correct": False}
        ]
    },
    {
        "question": "Како да препознаеш лажна веб-страна?",
        "options": [
            {"text": "Сомнителен URL и лоша граматика", "correct": True},
            {"text": "Има многу бои", "correct": False},
            {"text": "Има слики", "correct": False}
        ]
    },
    {
        "question": "Што треба да направиш ако некој итно ти бара пари онлајн?",
        "options": [
            {"text": "Да го пријавам и избришам", "correct": True},
            {"text": "Веднаш да му ги уплатам", "correct": False},
            {"text": "Да испратам половина", "correct": False}
        ]
    },
    {
        "question": "Дали треба да веруваш на 'Ти си победник!'?",
        "options": [
            {"text": "Не, обично е измама", "correct": True},
            {"text": "Да, секогаш", "correct": False},
            {"text": "Само ако има мој email", "correct": False}
        ]
    },
    {
        "question": "Што е Nigerian Prince scam?",
        "options": [
            {"text": "Класична измама со наследство", "correct": True},
            {"text": "Легитимна понуда", "correct": False},
            {"text": "Игра", "correct": False}
        ]
    },
    {
        "question": "Дали треба да дадеш пари за да добиеш награда?",
        "options": [
            {"text": "Не, тоа е измама", "correct": True},
            {"text": "Да, нормално е", "correct": False},
            {"text": "Зависи од наградата", "correct": False}
        ]
    },
    {
        "question": "Што е romance scam?",
        "options": [
            {"text": "Лажни љубовни врски за измама", "correct": True},
            {"text": "Апликација за запознавање", "correct": False},
            {"text": "Вид на игра", "correct": False}
        ]
    },
    # --- NEW QUESTIONS ---
    {
        "question": "Дали постои 'генератор за бесплатни V-Bucks/Robux'?",
        "options": [
            {"text": "Да, и работат супер", "correct": False},
            {"text": "Не, тоа се секогаш измами", "correct": True},
            {"text": "Само на YouTube", "correct": False}
        ]
    },
    {
        "question": "Што е 'Tech Support Scam'?",
        "options": [
            {"text": "Кога лажен Microsoft агент ти бара пристап до PC", "correct": True},
            {"text": "Кога ти помагаат за компјутерот", "correct": False},
            {"text": "Сервис за поправка", "correct": False}
        ]
    },
    {
        "question": "Што значи 'Ransomware'?",
        "options": [
            {"text": "Вирус што ги заклучува фајловите за откуп", "correct": True},
            {"text": "Бесплатен софтвер", "correct": False},
            {"text": "Антивирус", "correct": False}
        ]
    },
    {
        "question": "Што е 'Money Mule'?",
        "options": [
            {"text": "Лице што пренесува украдени пари (често несвесно)", "correct": True},
            {"text": "Богато животно", "correct": False},
            {"text": "Банкарска апликација", "correct": False}
        ]
    },
    {
        "question": "Ако понудата звучи премногу добро за да биде вистинита...",
        "options": [
            {"text": "...веројатно е измама", "correct": True},
            {"text": "...имаш многу среќа", "correct": False},
            {"text": "...треба веднаш да купиш", "correct": False}
        ]
    }
]

LEVEL_4_QUESTIONS_SQ = [
    # --- Original Questions ---
    {
        "question": "Çfarë është një mashtrim online?",
        "options": [
            {"text": "Përpjekje për të mashtruar për para/info", "correct": True},
            {"text": "Mënyrë blerje", "correct": False},
            {"text": "Lloj reklame", "correct": False}
        ]
    },
    {
        "question": "Si ta njohësh një faqe interneti të rreme?",
        "options": [
            {"text": "URL i dyshimtë dhe gramatikë e keqe", "correct": True},
            {"text": "Ka shumë ngjyra", "correct": False},
            {"text": "Ka foto", "correct": False}
        ]
    },
    {
        "question": "Çfarë duhet të bësh nëse dikush të kërkon para urgjent online?",
        "options": [
            {"text": "Ta raportoj dhe ta fshij", "correct": True},
            {"text": "T'i dërgoj menjëherë", "correct": False},
            {"text": "Të dërgoj gjysmën", "correct": False}
        ]
    },
    {
        "question": "A duhet t'i besosh 'Je fitues!'?",
        "options": [
            {"text": "Jo, zakonisht është mashtrim", "correct": True},
            {"text": "Po, gjithmonë", "correct": False},
            {"text": "Vetëm nëse ka email-in tim", "correct": False}
        ]
    },
    {
        "question": "Çfarë është Nigerian Prince scam?",
        "options": [
            {"text": "Mashtrim klasik me trashëgimi", "correct": True},
            {"text": "Ofertë legjitime", "correct": False},
            {"text": "Lojë", "correct": False}
        ]
    },
    {
        "question": "A duhet të paguash para për të marrë një çmim?",
        "options": [
            {"text": "Jo, është mashtrim", "correct": True},
            {"text": "Po, është normale", "correct": False},
            {"text": "Varet nga çmimi", "correct": False}
        ]
    },
    {
        "question": "Çfarë është romance scam?",
        "options": [
            {"text": "Lidhje dashurie të rreme për mashtrim", "correct": True},
            {"text": "Aplikacion takimesh", "correct": False},
            {"text": "Lloj loje", "correct": False}
        ]
    },
    # --- NEW QUESTIONS ---
    {
        "question": "A ekziston 'gjenerues falas për V-Bucks/Robux'?",
        "options": [
            {"text": "Po, dhe punojnë super", "correct": False},
            {"text": "Jo, janë gjithmonë mashtrime", "correct": True},
            {"text": "Vetëm në YouTube", "correct": False}
        ]
    },
    {
        "question": "Çfarë është 'Tech Support Scam'?",
        "options": [
            {"text": "Kur një agjent i rremë i Microsoft kërkon qasje në PC", "correct": True},
            {"text": "Kur të ndihmojnë për kompjuterin", "correct": False},
            {"text": "Shërbim riparimi", "correct": False}
        ]
    },
    {
        "question": "Çfarë do të thotë 'Ransomware'?",
        "options": [
            {"text": "Virus që bllokon skedarët për shpërblim", "correct": True},
            {"text": "Softuer falas", "correct": False},
            {"text": "Antivirus", "correct": False}
        ]
    },
    {
        "question": "Çfarë është 'Money Mule'?",
        "options": [
            {"text": "Person që transferon para të vjedhura (shpesh pa dije)", "correct": True},
            {"text": "Kafshë e pasur", "correct": False},
            {"text": "Aplikacion bankar", "correct": False}
        ]
    },
    {
        "question": "Nëse oferta duket shumë e mirë për të qenë e vërtetë...",
        "options": [
            {"text": "...ndoshta është mashtrim", "correct": True},
            {"text": "...ke shumë fat", "correct": False},
            {"text": "...duhet ta blesh menjëherë", "correct": False}
        ]
    }
]

# ==========================================
# LEVEL 5: CYBERBULLYING & ETHICS
# ==========================================

LEVEL_5_QUESTIONS_MK = [
    # --- Original Questions ---
    {
        "question": "Што е онлајн малтретирање?",
        "options": [
            {"text": "Малтретирање преку интернет", "correct": True},
            {"text": "Вид на игра", "correct": False},
            {"text": "Начин на комуникација", "correct": False}
        ]
    },
    {
        "question": "Што треба да направиш ако те малтретираат онлајн?",
        "options": [
            {"text": "Кажи на возрасен, блокирај, пријави", "correct": True},
            {"text": "Врати со иста мерка", "correct": False},
            {"text": "Игнорирај", "correct": False}
        ]
    },
    {
        "question": "Дали е ОК да споделуваш непријатни слики од другите?",
        "options": [
            {"text": "Не, никогаш", "correct": True},
            {"text": "Да, ако е смешно", "correct": False},
            {"text": "Само на приватна група", "correct": False}
        ]
    },
    {
        "question": "Што е doxxing?",
        "options": [
            {"text": "Објавување лични информации", "correct": True},
            {"text": "Вид на игра", "correct": False},
            {"text": "Начин на комуникација", "correct": False}
        ]
    },
    {
        "question": "Дали треба да одговориш на навредливи коментари?",
        "options": [
            {"text": "Не, блокирај ги и пријави", "correct": True},
            {"text": "Да, за да се одбраниш", "correct": False},
            {"text": "Да им вратиш", "correct": False}
        ]
    },
    {
        "question": "Како можеш да им помогнеш на другите што се малтретирани?",
        "options": [
            {"text": "Пријави и поддржи ја жртвата", "correct": True},
            {"text": "Игнорирај", "correct": False},
            {"text": "Смеј се со другите", "correct": False}
        ]
    },
    {
        "question": "Што е trolling?",
        "options": [
            {"text": "Провокативни коментари за реакција", "correct": True},
            {"text": "Начин на игра", "correct": False},
            {"text": "Вид на вирус", "correct": False}
        ]
    },
    # --- NEW QUESTIONS ---
    {
        "question": "Што е 'Digital Footprint' (Дигитален отпечаток)?",
        "options": [
            {"text": "Трага од податоци што ја оставаш онлајн", "correct": True},
            {"text": "Отпечаток од прст на екранот", "correct": False},
            {"text": "Марка на чевли", "correct": False}
        ]
    },
    {
        "question": "Дали интернетот 'заборава'?",
        "options": [
            {"text": "Да, по една година", "correct": False},
            {"text": "Не, што е објавено останува засекогаш", "correct": True},
            {"text": "Само ако го избришеш", "correct": False}
        ]
    },
    {
        "question": "Што е 'Catfishing'?",
        "options": [
            {"text": "Креирање лажен идентитет за да измамиш некого", "correct": True},
            {"text": "Ловење мачки", "correct": False},
            {"text": "Игра со риби", "correct": False}
        ]
    },
    {
        "question": "Дали е легално да влезеш во туѓ профил ако ја знаеш лозинката?",
        "options": [
            {"text": "Не, тоа е кривично дело", "correct": True},
            {"text": "Да, ако ти се другар", "correct": False},
            {"text": "Само за малку", "correct": False}
        ]
    },
    {
        "question": "Што е 'Flaming'?",
        "options": [
            {"text": "Интензивна расправија и навреди онлајн", "correct": True},
            {"text": "Испраќање оган емоџи", "correct": False},
            {"text": "Готвење онлајн", "correct": False}
        ]
    }
]

LEVEL_5_QUESTIONS_SQ = [
    # --- Original Questions ---
    {
        "question": "Çfarë është ngacmimi online?",
        "options": [
            {"text": "Ngacmim nëpërmjet internetit", "correct": True},
            {"text": "Lloj loje", "correct": False},
            {"text": "Mënyrë komunikimi", "correct": False}
        ]
    },
    {
        "question": "Çfarë duhet të bësh nëse të ngacmojnë online?",
        "options": [
            {"text": "Thuaji një adulti, blloko, raporto", "correct": True},
            {"text": "Ktheje me të njëjtën mënyrë", "correct": False},
            {"text": "Injoroje", "correct": False}
        ]
    },
    {
        "question": "A është OK të ndash foto të turpshme të të tjerëve?",
        "options": [
            {"text": "Jo, kurrë", "correct": True},
            {"text": "Po, nëse është qesharake", "correct": False},
            {"text": "Vetëm në grup privat", "correct": False}
        ]
    },
    {
        "question": "Çfarë është doxxing?",
        "options": [
            {"text": "Publikimi i informacionit personal", "correct": True},
            {"text": "Lloj loje", "correct": False},
            {"text": "Mënyrë komunikimi", "correct": False}
        ]
    },
    {
        "question": "A duhet t'u përgjigjesh komenteve fyese?",
        "options": [
            {"text": "Jo, bllokoji dhe raportoji", "correct": True},
            {"text": "Po, për t'u mbrojtur", "correct": False},
            {"text": "T'u kthesh", "correct": False}
        ]
    },
    {
        "question": "Si mund t'u ndihmosh të tjerëve që ngacmohen?",
        "options": [
            {"text": "Raporto dhe mbështet viktimën", "correct": True},
            {"text": "Injoroje", "correct": False},
            {"text": "Qesh me të tjerët", "correct": False}
        ]
    },
    {
        "question": "Çfarë është trolling?",
        "options": [
            {"text": "Komente provokuese për reagim", "correct": True},
            {"text": "Mënyrë loje", "correct": False},
            {"text": "Lloj virusi", "correct": False}
        ]
    },
    # --- NEW QUESTIONS ---
    {
        "question": "Çfarë është 'Digital Footprint' (Gjurmë dixhitale)?",
        "options": [
            {"text": "Gjurmët e të dhënave që lë online", "correct": True},
            {"text": "Gjurmë gishti në ekran", "correct": False},
            {"text": "Markë këpucësh", "correct": False}
        ]
    },
    {
        "question": "A 'harron' interneti?",
        "options": [
            {"text": "Po, pas një viti", "correct": False},
            {"text": "Jo, çfarë postohet mbetet përgjithmonë", "correct": True},
            {"text": "Vetëm nëse e fshin", "correct": False}
        ]
    },
    {
        "question": "Çfarë është 'Catfishing'?",
        "options": [
            {"text": "Krijimi i një identiteti të rremë për të mashtruar", "correct": True},
            {"text": "Gjuetia e maceve", "correct": False},
            {"text": "Lojë me peshq", "correct": False}
        ]
    },
    {
        "question": "A është e ligjshme të hysh në profilin e dikujt tjetër nëse e di fjalëkalimin?",
        "options": [
            {"text": "Jo, është vepër penale", "correct": True},
            {"text": "Po, nëse është shok", "correct": False},
            {"text": "Vetëm për pak", "correct": False}
        ]
    },
    {
        "question": "Çfarë është 'Flaming'?",
        "options": [
            {"text": "Debat intensiv dhe fyerje online", "correct": True},
            {"text": "Dërgimi i emoji zjarri", "correct": False},
            {"text": "Gatim online", "correct": False}
        ]
    }
]

def get_randomized_questions(level_num, num_questions, language='mk'):
    """Get randomized questions for a level in specified language"""

    # Select question pool based on level and language
    if language == 'sq':  # Albanian
        pools = {
            1: LEVEL_1_QUESTIONS_SQ,
            2: LEVEL_2_QUESTIONS_SQ,
            3: LEVEL_3_QUESTIONS_SQ,
            4: LEVEL_4_QUESTIONS_SQ,
            5: LEVEL_5_QUESTIONS_SQ,
        }
    else:  # Macedonian (default)
        pools = {
            1: LEVEL_1_QUESTIONS_MK,
            2: LEVEL_2_QUESTIONS_MK,
            3: LEVEL_3_QUESTIONS_MK,
            4: LEVEL_4_QUESTIONS_MK,
            5: LEVEL_5_QUESTIONS_MK,
        }

    # IMPORTANT: We use .get() but provide LEVEL_1 as fallback to prevent crashing
    pool = pools.get(level_num, LEVEL_1_QUESTIONS_MK).copy()

    # Shuffle the entire pool
    random.shuffle(pool)

    # Take required number of questions
    selected = pool[:min(num_questions, len(pool))]

    # Shuffle options within each question
    for question in selected:
        random.shuffle(question['options'])

    return selected