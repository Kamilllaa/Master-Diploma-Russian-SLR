# Master-Diploma-Russian-SLR
В этом репозитории опубликованы все материалы, посвященные работе над дипломом "Интеграция глубокого обучения в обучение дактильной русской азбуке: Разработка приложения для детей с нарушениями слуха и речи"

tg_bot —— это телеграм-бот для сбора датасета русского дактильного алфавита. Как он работает:

1. Пользователь начинает чат с ботом с команды "/start", после чего получает приветственное сообщение с объяснениями, о чем проект, какая у него цель и тд. 
2. Пользователь может получить общие инструкции по дактилированию (кнопкка "Получить инструкции") и по тому, как снимать фото для бота.
3. Когда пользователь нажимает на кнопку "Отправить фото", бот присваивает пользователю букву, которую он должен изобразить, снять и отправить в бот. У каждой дактилемы, которую должен отправить пользователь, своя текстуальная и визуальная инструкция. Бот запоминает, какие буквы пользователь уже отправил, чтобы в дальнейшем они не повторялись. После того, как все буквы алфавита отправлены, этот список обнуляется, после чего пользователь снова может присылать буквы.   
4. Пользователь также может установить напоминание о том, что надо прислать фото, используя команду /set HH:MM по +3 UTC. 
