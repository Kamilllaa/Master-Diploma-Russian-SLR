# Master-Diploma-Russian-SLR

![image](https://sun9-87.userapi.com/impg/MuruawEGIed2TqTo0vj2t84-dBTRh1UAqKRPdg/qGbmEFZTwXM.jpg?size=1024x767&quality=95&sign=a2942b4f2fe3d2d8431e3abcb2456f45&type=album)

**Описание проекта** Этот репозиторий посвящен описанию магистерской дипломной работы "Интеграция Deep Learning в обучение дактильной (жестовой) русской азбуке: Разработка приложения для детей с нарушениями слуха и речи". Работа включает в себя 4 этапа, подробнее описанных ниже. [Ссылка на презентацию диплома](https://docs.google.com/presentation/d/1rEiIyYebSRfj5mBFOs22Ltyv-xhaUjN9o_WuHR1tlZ0/edit?usp=sharing). 


## 1. Сбор пользовательских фото данных с помощью tg-бота 
Так как для русской дактильной не нашлось подходящего датасета, было решено собрать его самостоятельно с помощью пользовательских фото. Для этого был создан телеграм-бот. Подробнее ознакомиться с его работой можно, нажав на спойлер "Как он работает" ниже. В итоге с помощью бота удалось собрать **более 1000 фото** (около 100 фото для каждого класса). Участие в сборе приняли более 60 человек, включая самих носителей. Также, датасет выложен в открытый доступ на платформе [Kaggle](https://www.kaggle.com/datasets/kamillakabardieva/russian-sign-language-alphabet).  

Код можно найти в папке **1_tg_bot**. 

<details>
  <summary>Как он работает:</summary>
  
- Пользователь начинает чат с ботом с команды _"/start"_, после чего получает приветственное сообщение с объяснениями, о чем проект, какая у него цель и тд.

<img src="https://drive.google.com/uc?export=view&id=1YDPWDRxUVwS3ssS72f73bILS2-5ASw9c" width="700">


- Ознакомиться с общей информацией о дактилировании в боте и инструкциях пользователь может с помощью кнопки _"Правила дактилирования"_.
<img src="https://drive.google.com/uc?export=view&id=1rs2XFvGxVXAbFA6S6e-Vu2XblzAFdyGx" width="700">

  
- Когда пользователь нажимает на кнопку _"Отправить фото"_, бот отправляет пользователю подробную инструкцию в виде текста и фото и просит пользователя повторить дактилему. После того как пользователь отправит фото, бот сообщит пользователю о количестве отправленных фотографий. Информация об отправленных пользователем буквах сохраняется.
<img src="https://drive.google.com/uc?export=view&id=1rSqhRvlBC1jeYDon88ZXeespq7AFDoRl" width="400" height="270"> <img src="https://drive.google.com/uc?export=view&id=1_fStdMvPQTC-4yJLP0nqxkE00JVDw4r_" width="400" height="270">


- Пользователь также может установить напоминание о том, что надо прислать фото, используя команду /set HH:MM по +3 UTC.
<img src="https://drive.google.com/uc?export=view&id=1_fStdMvPQTC-4yJLP0nqxkE00JVDw4r_" width="700">

</details>

<details>
<summary>Используемые библиотеки:</summary>

- Python-telegram-bot (Эта библиотека предоставляет чистый Python, асинхронный интерфейс для Telegram Bot API. Он совместим с версиями Python 3.8+)

</details>

## 2. Подготовка данных и обучение нейронных сетей
Второй этап исследования включал в себя подготовку, разметку и препроцессинг данных, а также выбор и создание нейронных сетей. В исследование также были включены ml-алгоритмы в качестве бейзлайна.  

Код для препроцессинга и обучения можно найти в папке **2_train_model**

<details>
  <summary>Детали:</summary>
  
- Подготовка данных. Я экспериментировала с различными видами препроцессинга: получение координат ключевых точек рук, построение изображений по этим координатам, а также выделение ROI (region of interest). Более подробное описание для каждого вида препроцессинга можно найти 2_train_model/data_preparation. 
- Построение нейронных сетей. Были реализованы 1D-CNN, 2D-CNN, а также различные ML-модели (SVM, RandomForest, XGBoost). Более подробное описание можно найти 2_train_model/train_models

</details>

<details>
  <summary>Стэк:</summary> 
  
- Для препроцессинга фотографий использовалась библиотека cv2, а также модуль MediapipeHands. 
- Для реализации DL-моделей использовалась библиотека TensorFlow, для ML-моделей использовалась библиотека sklearn.

</details>

## 3. Проведение экспериментов с выбранными архитектурами

Этот этап включал в себя проведение экспериментов с различными методами предобработки, размерами изображений и темпами обучения. Результаты экспериментов можно найти под спойлером "Детали"

<details>
  <summary>Детали:</summary>

### 2D-CNN
![image](https://drive.google.com/uc?export=view&id=1dEq70NzdoXagDbCOBpjAfD4GVe-Cxgmj)
![image](https://drive.google.com/uc?export=view&id=1pfzaSWMXyA5QZDBuw9YNrEltEP4gB4OS)

Подробнее про методы предобработки можно узнать в **train_models/data_preparation**. Данная нейронная сеть показывает наилучшие результаты среди всех рассмотренных моделей, когда на вход ей подаются отрисованные по 21 ключевой точке изображения руки. Они были получены с помощью Mediapipe (в таблице метод предобработки на это отсылается). 

### 1D-CNN
![image](https://drive.google.com/uc?export=view&id=1HhubWmSwkUwPldfu0pCW0AztG33MnjIL)

Процесс получения нормализованных (относительно точки запястья) описан в **train_models/data_preparation**. 

### ML-алгоритмы (SVM, RandomForest, XGBoost)
![image](https://drive.google.com/uc?export=view&id=1sOL_y1MYYMWt0z6pfwPtFGmZAKSt0Mo1)

Эксперимент ML-алгоритмов заключался в сравнении разных методов машинного обучения между собой для одного и того же набора данных. Я не стала включать в описание экспериментов другие методы предобработки, однако их можно найти тут: **2_train_model/train_models/SOTA-3 (ML)**. 

</details>

## 4. Разработка десктопного детского приложения с интегрированным ИИ

<details>
  <summary>Детали:</summary>
  Оно тут будет (позжэ)
</details>

<details><summary>Стэк:</summary> 
  
- Tkinter — пакет для языка Python, нужный для работы со средствами Tk. Библиотека Tk написана на языке программирования Tcl и содержит в себе компоненты GUI. 

- </details>
