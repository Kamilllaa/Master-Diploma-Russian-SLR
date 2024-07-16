hello_message = """
Привет! 👋

Этот бот создан с целью помочь людям с нарушениями слуха/речи. \
Мы собираем открытую базу данных русской дактильной азбуки - это часть русского языка жестов, \
где каждому жесту соответствует буква алфавита (такие жесты называются дактилемами). 

Например, этот смайлик «✋» обозначает букву «В» в дактильной азбуке. Видите, как просто:)

Вы можете помочь проекту! Для этого нужно:
1. следуя инструкциям бота, сделать фото своей руки, показывающей жест;
2. отправить фото в бот;
3. вы великолепны!  

❗Датасет будет выложен в открытый доступ на платформе kaggle.com. \
Отправляя фото, вы даете согласие на их обработку.  

🙌 Всего от вас потребуется 33 фото - столько же, сколько букв в русском алфавите. \
Конечно, если у вас возникают трудности или у вас нет возможности предоставить все сразу, \
не беспокойтесь! 👌 вы сможете отвлечься, а через время бот напомнит вам про остальные фото. \

👐 Если вы хотите помочь проекту, нажмите кнопку «Получить инструкции» — мы расскажем про ключевые \
правила дактилирования, а затем вы сможете получить и отправить свою первую дактилему! 

⏳Чтобы получать напоминания, отправьте в бот команду «/set ЧЧ:ММ» и укажите вместо ЧЧ:ММ время по UTC+03:00 \
(часовой пояс Москвы), в которое вы хотите получать сообщение. Используйте /unset, чтобы убрать напоминания
"""

handle_photo_thanks_text = """
Спасибо за отправленное фото! Вы можете установить напоминания для фото с помощью команды /set, \
если еще этого не сделали:)
"""

handle_photo_all_letters = "Спасибо, вы отправили все 33 дактилемы:) Вы еще можете помочь проекту!" \
           " Для этого нажмите 'Отправить фото', чтобы отправить новую коллекцию фото"

handle_photo_wrong_photo = "Пожалуйста, нажмите кнопку 'Отправить фото', прежде чем отправлять фотографии."

set_timer_error_text = """
Вы ввели неверный формат времени. Пожалуйста, ввведите время в формате ЧЧ:MM, где ЧЧ - часы, MM - минуты. 
"""

instruction_text = """
Спасибо, что согласились помочь! Дактилировать не так сложно:) сейчас мы расскажем про основные правила:

Вот, что нужно знать:

1. Дактилирование ведётся одной рукой. Общепринято это правая рука. 
2. Рука при дактилировании не прыгает и не двигается вперёд-назад — двигается только кисть.
3. Дактильные знаки показывают точно и четко.
4. При дактилировании рука согнута в локте, кисть руки находится \
на уровне плеча, слегка вынесена вперед и обращена ладонью от себя, к \
собеседнику, не прикрывая рот говорящего. 
5. Не переживайте за качество камеры или чистоту фона! 

👉👈 Чтобы получить свою дактилему и инструкции по ней, нажмите кнопку «Отправить фото» и Вы получите инструкции по \
конкретной дактилеме, которую предстоит сфотографировать и отправить!

Источники: 
1. Камнева, В. П. Русский жестовый язык : Учебно-практическое пособие / В. П. Камнева, А. А. Константинова, О. Ю. \
Полонская. – Иркутск : Восточно-Сибирский институт Министерства внутренних дел Российской Федерации, 2016. – 39 с. – \
EDN VXRGYX.
"""

instructions_dict = {
    'А': 'Пальцы сложены в кулак, ладонь обращена к камере, локоть вниз',
    'Б': 'Ладонь обращена в диагональ к камере, указательный палец выпрямлен, \
к нему прижат наполовину согнутый средний, остальные пальцы согнуты.',
    'В': 'Ладонь раскрыта и направлена к камере, пальцы прямые.',
    'Г': 'Большой палец отставлен в сторону, указательный выпрямлен и направлен вниз,ладонь к себе.',
    'Д': "Указательный и средний палец выпрямлены, остальные согнуты. \
В динамике прямые пальцы делают плавный вертикальный круг, но так как мы делаем фото, \
достаточно выполнить инструкцию из первого предложения",
    "Е": 'Ладонь к камере, пальцы полусогнуты, кончики касаются друг друга.',
    "Ё": "Ладонь к камере, пальцы полусогнуты, кончики касаются друг друга. В динамике кисть несколько \
раз описывает полукруг перед собой, но так как мы делаем фото, достаточно выполнить инструкцию из первого предложения",
    "Ж": "Ладонь в диагональ или боком к камере, прямые пальцы опустить вниз, чтобы с ладонью получился угол в 90 градусов,\
большой палец выпрямлен и прижат к указательному.",
    "З": 'Указательный палец выпрямлен, остальные согнуты, ладонь к камере. В динамике палец рисует латинскую «Z» \
или русскую «З», но так как мы делаем фото, достаточно выполнить инструкцию из первого предложения',
    "И": "Безымянный и мизинец выпрямлены, остальные пальцы собраны, ладонь в диагональ к камере.",
    "Й": 'Безымянный и мизинец выпрямлены, остальные пальцы собраны, ладонь в диагональ к собеседнику.\
В динамике прямые пальцы описывают вертикальный круг от себя, но так как мы делаем фото, достаточно \
выполнить инструкцию из первого предложения.',
    "К": "Ладонь вбок и чуть на себя, указательный и средний пальцы выпрямлены, остальные собраны.",
    "Л": "Ладонь к себе, указательный и средний пальцы выпрямлены, и прямые пальцы смотрят в пол.",
    "М": "Указательный, средний и безымянный пальцы выпрямлены и расставлены, остальные собраны. \
Прямые пальцы смотрят в пол, ладонь к себе.",
    "Н": "Безымянный и большой пальцы соединены в кружок, остальные выпрямлены и смотрят вверх, ладонь к собеседнику.",
    "О": "Указательный и большой пальцы соединены в кружок, остальные выпрямлены и смотрят вверх, ладонь к собеседнику.",
    "П": "Ладонь к себе, указательный и средний пальцы выпрямлены, сведены вместе, и прямые пальцы смотрят в пол.",
    "Р": "Средний и большой пальцы соединены в кружок, остальные выпрямлены и смотрят вверх, ладонь к собеседнику",
    "С": "Ладонь боком или в диагональ к собеседнику, пальцы полусогнуты, чтобы было похоже на написание буквы 'С',",
    "Т": "Указательный, средний и безымянный пальцы выпрямлены и сведены вместе, остальные собраны. \
Прямые пальцы смотрят в пол, ладонь к себе.",
    "У": "Большой палец выпрямлен, смотрит вбок, мизинец выпрямлен и смотрит вверх, \
остальные пальцы согнуты, ладонь на собеседника.",
    "Ф": "Ладонь боком к камере, указательный, средний, безымянный и мизинец сгибаются, \
большой палец приложить к середине указательного, большой палец смотрит вверх",
    "Х": "Указательный палец полусогнут, остальные согнуты собраны вместе, ладонь боком к собеседнику.",
    "Ц": "Указательный и средний пальцы выпрямлены и сведены, остальные пальцы собраны, ладонь на собеседника.",
    "Ч": "Ладонь боком к собеседнику, сгибаем безымянный и мизинец, касаемся средним и указательным пальцами большого пальца.",
    "Ш": "Указательный, средний и безымянный пальцы выпрямлены и расставлены, остальные собраны, \
ладонь на собеседника, прямые пальцы направлены вверх.",
    "Щ": "Указательный, средний и безымянный пальцы выпрямлены и расставлены, остальные собраны, \
ладонь на собеседника, прямые пальцы направлены вверх. В динамике ладонь совершает однократное движение вниз, но так как мы делаем фото, достаточно выполнить инструкцию из первого предложения.",
    "Ъ": "Указательный выпрямлен и смотрит в камеру. Большой палец указывает в сторону дактилирующего. \
Остальные пальцы собраны, костяшки пальцев смотрят вверх.",
    "Ы": "Указательный и мизинец выпрямлены, направлены вверх, остальные пальцы собраны, ладонь на собеседника.",
    "Ь": "Указательный выпрямлен и смотрит в камеру. Большой палец, указывает в сторону от дактилирующего. \
Остальные пальцы собраны, костяшки пальцев смотрят вниз.",
    "Э": 'Cогнуть средний, безымянный и мизинец, ладонь боком к собеседнику, указательный и большой согнуты в букве "C"',
    "Ю": "Ладонь боком к собеседнику, прямые пальцы опустить вниз, чтобы с ладонью получился угол в 90 градусов, \
большой палец выпрямлен и прижат к указательному, мизинец поднят вверх.",
    "Я": "Указательный и средний пальцы выпрямлены, средний палец заходит за указательный, остальные пальцы собраны, \
ладонь на собеседника"
}

notification_text = "Привет! Напоминаем Вам про фото!:)"

wrong_time = 'Пожалуйста, введите время в формате /set ЧЧ:ММ, ' \
             'где вместо ЧЧ:ММ нужно указать время по UTC+03:00 (часовой пояс Москвы), в которое вы хотите получать сообщение.'

buttons = {'send_photo': "Отправить фото",
           'get_instructions': "Получить инструкции"
           }

news_letter = """
1. На данном этапе исследования мы решили отказаться от фото дактилем, которые требуют движения. \
Не пугайтесь, если какие-то символы вам больше не попадаются 
2. Датасет будет выложен в открытый доступ на платформе kaggle.com. Отправляя фото в бот, вы даете согласие на его обработку. \
Если вы уже отправляли фото, но не хотите, чтобы они попали в общий доступ, напишите мне 
3. Мы перезапустили бота, поэтому если у вас стоял таймер, нужно будет установить его повторно.
"""