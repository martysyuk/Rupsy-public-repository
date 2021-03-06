Установка Node.JS
===
Привет! Сегодня мы с тобой установим **Node.JS** сервер на твой компьютер с Windows или MacOS. 

Установка под MacOS
---
Под MacOS мы будем устанавливать Node.JS через консоль (Терминал), думаю если у тебя MacOS, то ты знаешь как ее запустить, например через Spotlight.

1. В терминале выполняем команду: 
`/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"`
2. После того, как нас покажут куда и что будет скачено, жмем **"Enter"**
3. Вводим свой пароль (учетной записи MscOS)
4. Ждем окончания скачивания (может занять некоторое временя и даже без признаков жизни)
5. Выполняем команду: 
`brew install node`
6. После того как все установилось (надеюсь без ошибок), проверяем работоспособность Node.JS командой `node -v`, если после этого ты увидиш в терминале **"v6.11.2"** (или другая версия), то значит у тебя все получилось! Поздравляю!

Установка под Windows
---
Начнём с того, что скачаем установщик с [**официального сайта**](https://nodejs.org/en/download/) выбрав его согласно твоей операционной системе, в моем случае это **Windows Installer (.msi) 64-bit**.

1. Запускаем скаченный установщик
2. После некоторого ожидания (пока он что-то проверит) жмем **"Next"**
2. Принимаем соглашение поставив галочку на **"I accept the terms in the License Agreement"** и жмем **"Next"**
3. Выбираем путь установки, лучше ставить по умолчанию и опять жмем **"Next"**
4. На следующем этапе оставляем все как есть и опять **"Next"**
5. На следующем шаге **"Install"**
6. Ждем завершения установки и жмем **"Finish"**

Установка дополнительных пакетов модулей
---
Пакетные модули делают Node.JS более мощной средой для разработки приложений. **"Npm"** это стандартный пакетный менеджер, он автоматически устанавливается вместе с Node.JS по умолчанию.

Допустим ты хочешь использовать базу данных для своего проекта и тебе нужен Mysql. Тогда в командной строке (cmd или терминале, в зависимости от операционной системы) пишешь **"npm install mysql"** и ждешь установки пакета, возможно на это понадобится какое-то время, в зависимости от скорости твоего интернета и компьютера. Главное чтобы ты не увидел красное **"ERR!"** - это будет означать, что во время установки произошла какая-то ошибка и с ней уже надо разбираться отдельно, например попробовав прочитать логи. Путь к файлу голов будет указан там же в консоли рядом с последним **"ERR!"**.

Полный список пакетов можешь посмотреть на сайте [**"Npm"**](https://www.npmjs.org/)

Пишем первую программу на Node.JS
---
После установки Node.JS, попробуем создать и запустить первое, простенькое приложение. 

Создаем новый файл, например **"hello.js"**

И напишем нашу первую небольшую программу

    var http = require('http');
    
    http.createServer(function (request, response) {
      response.writeHead(200, {'Content-Type': 'text/plain'});
      response.end('Hello World!\n');
    }).listen(8080);
    
    console.log('Server running at http://localhost:8080/');

Это простейшая программа, HTTP сервер, которая при соединении с ним выведет пользователю всем привычное **"Hello World!"**.

Теперь мы готовы запустить наше первое Node.js приложение
---

В терминале или коммандной строке (в зависимости от твоей операционной системы) заходим в папку где ты создал файл hello.js и выполняем команду `node hello.js`

Если все прошло отлично, то в консоли появится радующее **"Server running at http://localhost:8080/ "**. Обратите внимание, что вовремя работы сервера нельзя закрывать окно консоли с нашим сервером ("cmd.exe - node hello.js") иначе он вырубится.

Проверяем работу нашего сервера, а заодно и всего Node.JS
---
В своем любимом браузере открываем адрес http://localhost:8080 и если на странице ты увидишь **"Hello World!"**, то я тебя поздравляю, у тебя все получилось и теперь ты можешь спокойно писать программы на Node.JS у себя на компьютере!

**Ну а как удалять Node.JS я тебе рассказывать не стану, во первых это тривиально, а во вторых я искренне надеюсь, что тебе это не понадобится, так как ты будешь программировать с удовольствием!**

