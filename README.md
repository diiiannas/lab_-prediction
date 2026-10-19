# Шар предсказаний
## Ссылки на  сервисы

Сайт: https://lab-prediction.onrender.com

Метрики: https://prometheus-monitor-lse4.onrender.com

## Локальная сборка и мониторинг

Для упаковки приложения (Python (Flask) + HTML) в изолированную среду был создан Dockerfile

Сборка и тестирование проводились локально через терминал VS Code и Docker Desktop:

docker build -t prediction .

docker run -p 5000:5000 prediction

После чего сайт открывается в браузере по первой ссылке, которая выводится в терминале (рисунок 1)

<img width="1268" height="657" alt="image" src="https://github.com/user-attachments/assets/38c6bc7c-c4e5-4ab3-895f-42c1a3b4dcd7" />

Чтобы настроить мониторинг были созданы файлы prometheus.yml и docker-compose.yml.

Предыдущий контейнер был остановлен в приложении docker desktop

После чего контейнер был пересобран: docker build --no-cache -t prediction .

И запущен: docker-compose up -d

http://localhost:5000 - сам сайт

http://localhost:5000/metrics - метрика "количество предсказаний"

<img width="395" height="141" alt="image" src="https://github.com/user-attachments/assets/61303625-6e37-4340-a0d4-c6d1dd83ff04" />


http://localhost:5000/health - health check

<img width="483" height="79" alt="image" src="https://github.com/user-attachments/assets/5b935a64-8fae-4b64-9113-467a77ce0be9" />


http://localhost:9090 , вводим vsego_predskazaniy и получаем метрику "количество предсказаний" в prometheus

<img width="1918" height="865" alt="image" src="https://github.com/user-attachments/assets/1f0bbac2-3549-44b1-acbd-faa2bb37ba6e" />

http://localhost:3000 - Grafana
Настраиваем коннект с prometheus и создаем dashboard для "количества предсказаний"

<img width="1299" height="716" alt="image" src="https://github.com/user-attachments/assets/80bb4346-be52-40f7-975c-f032529df42a" />

http://localhost:9100 - cadvisor (отслеживает cpu)

<img width="746" height="978" alt="image" src="https://github.com/user-attachments/assets/5565cc4d-8d85-485a-ac87-d49c95704d34" />

## CI/CD Pipeline

Файлы загружены на GitHub

Настроен CI/CD с использованием GitHub Actions и платформы Render.

Файл конфигурации .github/workflows/deploy.yml автоматизирует проверку кода и его развертывание в виде Docker-контейнера.

Пайплайн запускается автоматически при каждом отправке изменений в основную ветку main.

Это гарантирует, что любая новая функциональность или исправление сразу проходят цикл проверки и попадают на сервер.

Все задачи выполняются на виртуальной машине GitHub с операционной системой Ubuntu. Это обеспечивает предсказуемую среду для сборки.

GitHub Actions скачивает актуальную версию репозитория в рабочую директорию виртуальной машины.

На виртуальную машину устанавливается интерпретатор Python 3.10.

Менеджер пакетов pip обновляется, а затем устанавливаются все библиотеки из файла requirements.txt

Выполняется базовая статическая проверка синтаксиса главного файла приложения (app.py) с помощью встроенного модуля py_compile.

Если все предыдущие шаги прошли успешно, скрипт отправляет HTTP POST-запрос по защищенному URL, который хранится в GitHub Secrets.

## Деплой на Render

Был создан аккаунт на платформе Render.com с авторизацией через GitHub

Render получил доступ к репозиторию, что позволило автоматически отслеживать изменения в коде

Платформа автоматически выполнила сборку Docker-образа из репозитория и запустила контейнер. После успешного деплоя приложению был присвоен уникальный домен.

<img width="954" height="1017" alt="image" src="https://github.com/user-attachments/assets/d9496a8b-6606-4872-a71a-65b9550d8757" />


Для сбора метрик был создан отдельный Web Service.

Конфигурационный файл prometheus.yml был размещён в отдельной папке prometheus/ вместе с собственным Dockerfile.

В конфигурации Prometheus был настроен сбор метрик с основного приложения по эндпоинтам:

- /metrics — бизнес-метрики (счётчик предсказаний)

- /metrics/resources — метрики ресурсов (CPU, RAM, Disk)

- /health — проверка работоспособности

 По ссылке на prometheus - https://prometheus-monitor-lse4.onrender.com отслеживаются следующие метрики:

 - posesheniya_total - количество посещений;
 - cpu_usage_percent - нагрузка на процессор;
 - memory_used_mb - использовано памяти в мб;
 - memory_total_mb - всего памяти в мб;
 - memory_usage_percent - использование RAM (%);
 - disk_used_gb - использовано диска в гб;
 - disk_total_gb - всего диска в гб;
 - disk_usage_percent - использование диска (%)

Метрики ресурсов (CPU, memory, диск) отражают показатели всей хост-машины Render, а не изолированного контейнера приложения.

Библиотека psutil внутри Docker считывает данные ядра хост-сервера, поэтому эти значения показывают совокупную нагрузку и объем диска всего сервера, а не фактическое потребление ресурсов только моим приложением.
 
 <img width="1890" height="1083" alt="image" src="https://github.com/user-attachments/assets/866d6a7c-7663-4fa0-809e-a711205d820f" />

В ходе работы над проектом в код вносились изменения: исправление  в app.py (изначально вместо посещений шел подсчет количества действий), добавление библиотеки psutil для сбора метрик ресурсов, корректировка структуры prometheus.yml.

После чего GitHub Actions автоматически проверил синтаксис и через Deploy Hook инициировал пересборку на Render. Приложение обновилось на сервере без ручного вмешательства, что подтверждает корректную работу пайплайна непрерывного развёртывания.




 

 




