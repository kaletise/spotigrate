# Spotigrate
Сервис для интеграции ВКонтакте с Spotify

![Spotigrate](/screenshots/screenshot.png "Spotigrate")

## Production
~~https://spotigrate.ru~~  
**Невозможно** из-за [ограничений со стороны Spotify Web API](/screenshots/restrictions.png)

## Локальное развертывание (Development mode)
### Требования к серверу, на котором будет производиться локальное развертывание:
* ОС Windows или Linux
* [Python 3](https://www.python.org/downloads/)
* [Node.js](https://nodejs.org/en/download/)
* [Git](https://git-scm.com/downloads)
* Развернутый сервер [MongoDB](https://www.mongodb.com/try/download/community)

### Команды для развертывания:
#### Загрузка исходного кода из репозитория:
```
git clone https://github.com/kaletise/spotigrate.git
```

#### Развертывание и запуск back-end
##### Linux:
```
cd spotigrate/common
pip3 install -r requirements.txt
sh run.sh
```

##### Windows:
```
cd spotigrate/common
pip3 install -r requirements.txt
run.bat
```

После выполнения команд выше, в директории **common** будет создан конфигурационный файл **config.json**, который необходимо заполнить в соответствии с таблицей в разделе **Конфигурационный файл**  
После заполнения конфигурационного файла, необходимо запустить back-end сервер заново, используя команду `sh run.sh` для Linux или `run.bat` для Windows

#### Развертывание и запуск front-end
```
cd spotigrate/ui
npm install
npm run serve
```

## Локальное развертывание (Production mode)
Производится на Ubuntu 18.04/20.04 в соответствии с [инструкцией](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uswgi-and-nginx-on-ubuntu-18-04)

## Конфигурационный файл
### common/config.json
| Опция | Описание | Значение по умолчанию |
| --- | --- |  --- |
| `CALLBACK_URI` | URL, на который будет перенаправлен пользователь после авторизации через Spotify. Должен заканчиваться на `/callback`. Если развертываете локально по инструкции выше - изменять не нужно | `http://127.0.0.1:8080/callback` |
| `DATABASE_HOST` | Адрес MongoDB сервера | `mongodb://localhost:27017/` |
| `DATABASE_NAME` | Название коллекции MongoDB | `spotigrate` |
| `LOGGER_ENABLE` | Опция, управляющая логгированием (включено/выключено) | `true` |
| `LOGGER_FILE` | Файл, в который будет производиться логгирование (оставьте пустым, чтобы отключить запись логов в файл) | `debug.log` |
| `LOGGER_LEVEL` | Уровень логгирования (1 - error, 2 - warning, 3 - info, 4 - debug) | `3` |
| `SPOTIFY_APP_ID` | Client ID приложения Spotify (см. инструкцию ниже) |  |
| `SPOTIFY_APP_SECRET` | Client Secret приложения Spotify (см. инструкцию ниже) |  |

### ui/src/config.json
| Опция | Описание | Значение по умолчанию |
| --- | --- |  --- |
| `SERVER_URI` | URL back-end сервера. Если развертываете локально по инструкции выше - изменять не нужно | `http://127.0.0.1:5000` |

## Создание Spotify приложения
Для работы Spotigrate необходимо создать Spotify приложение, через которое будет производиться авторизация. Сделать это можно следующим образом:
1. Переходим в [панель управления Spotify for Developers](https://developer.spotify.com/dashboard/applications) и авторизуемся через свой Spotify аккаунт, если потребуется
2. Нажимаем **Create an app**, произвольно заполняем поля *App name* и *App description*, соглашаемся с условиями и нажимаем **Create**
3. После создания приложения копируем значение полей *Client ID* и *Client Secret*, вставляем их в конфигурационный файл *common/config.json* в опции `SPOTIFY_APP_ID` и `SPOTIFY_APP_SECRET` соответственно
4. Нажимаем **Edit settings**, добавляем Callback-ссылку (по умолчанию `http://127.0.0.1:8080/callback`) в поле **Redirect URIs**. Добавленная Callback-ссылка должна совпадать со значением опции `CALLBACK_URI` в конфигурационном файле *common/config.json*!
5. Нажимаем **Save**, чтобы сохранить изменения. Настройка Spotify приложения завершена
