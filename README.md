## Автоматизированное параллельное и GUI тестирование

### Техническое задание

Задание 1. <br/>
Написать 2 теста для API сайта [coinmarketcap.com](http://coinmarketcap.com/).
1. Получить данные о 10 тикерах с наибольшим объемом за последние 24 часа.
Считать, что тест выполнился успешно, если:
- успешный ответ от ресурса приходит менее чем за 500мс;
- информация по каждой валюте актуальна (т.е. берется за текущий день);
- размер полученного пакета данных не должен превышать 10кб;
2.  Запустить тест №1 параллельно/асинхронно 8 раз и рассчитать rps (скорость ответов от сервера в секунду) и 80-перцентиль времени ответа сервера (80% latency).
Считать, что тест выполнился успешно, если:
- все запущенные тесты выполнились успешно;
- rps > 5;
- 80% latency < 450мс;
Можно использовать любые языки программирования, любые фреймворки и библиотеки.

Задание 2. <br/>
Разработать автоматизированные GUI тесты для переключения языков [coinmarketcap.com](http://coinmarketcap.com/).

### Имплементация
Автотесты реализованы с помощью библиотеки pytest с применением фреймворка Selenium, asyncio и паттерна программирования Page Object.
 
### Основные модули 
- test_cmc.py - модуль тестов
- main_page.py, base_page.py - модули объектов тестируемых веб-страниц

### Установка драйвера ChromeDriver для Linux
Вместо ссылки ниже выберите нужную для вашей системы отсюда: https://sites.google.com/a/chromium.org/chromedriver/downloads
```bash
wget https://chromedriver.storage.googleapis.com/76.0.3809.126/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
sudo mv chromedriver /usr/local/bin/chromedriver
sudo chown root:root /usr/local/bin/chromedriver
sudo chmod +x /usr/local/bin/chromedriver
```

### Установка приложения
```bash
git clone git@github.com:Arkkav/test_coinmarketcap.git
cd ./qa_cmc
python3 -m venv env
./env/bin/activate
pip3 install -r requirements.txt
```

### Запуск тестов
```bash
pytest test_cmc.py::test_1
pytest test_cmc.py::test_2
pytest test_cmc.py::test_change_language
```

