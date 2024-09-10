# Простой проект по скачиванию и отправке файлов на сервер с CLI для клиента
Для начала склонируйте репозиторий 
```bash
  git clone https://github.com/TimurZheksimbaev/DeNetPythonTask.git
  cd DeNetPythonTask
```

Запустите в одном терминале сервер
```bash
  fastapi dev server/server.py
```

Для пользования клиентом сначала зарегистрируйтесь
```bash
  python main.py register
```
Вам предложат ввести имя и пароль

Дальше можно пользоваться функциями  и скачивания файлов
Отправка файла на сервер
```bash
  python main.py upload <filename>
```
Вам предложат ввестим имя и пароль
Или можете добавить их как аргументы в команде
```bash
  python main.py upload --username <username> --password <password> <filename>
```
