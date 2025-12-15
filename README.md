# ML-Production-System-Simulation
Реализация микросервисной ML-системы в production с обменом сообщениями через RabbitMQ, сбором метрик и визуализацией ошибок в реальном времени.

Система имитирует end-to-end ML pipeline из 5 микросервисов:
- **features** - бесконечный поток данных из sklearn.datasets.load_diabetes
- **model** - LinearRegression делает предсказания
- **metric** - собирает пары (y_true, y_pred), считает absolute error, логирует в CSV
- **plot** - в реальном времени строит и обновляет гистограмму ошибок
- **rabbitmq** - брокер сообщений с Management UI

# Архитектура

<img width="989" height="479" alt="image" src="https://github.com/user-attachments/assets/4f7834ef-ce77-46ef-aaa8-dc28494bd773" />

Шаги инициализации:
1. Склонировать репозиторий
2. Создать папку logs с заголовком CSV
mkdir logs
echo "id,y_true,y_pred,absolute_error" > logs/metric_log.csv
3. Запустить всю систему
docker compose up --build

Мониторинг в реальном времени осуществяется через RabbitMQ Management UI:
RabbitMQ Management UI: http://localhost:15672 (guest/guest)
Смотрим очереди features, y_true, y_pred в реальном времени.
**Метрики:** logs/metric_log.csv — растёт с каждой итерацией
**Визуализация:** logs/error_distribution.png — обновляется каждые 3 секунды


**Структура проекта** (файлы распередены по веткам в репозитории)

<img width="335" height="410" alt="image" src="https://github.com/user-attachments/assets/2abc169f-8d22-4207-88a9-c756b0c51d01" />

# Технологии

1. Брокер сообщений	RabbitMQ 3.x + Management UI
2. Микросервисы	Python 3.9 + Pika (AMQP)
3. ML-модель	scikit-learn LinearRegression
4. Метрики	pandas + Absolute Error
5. Визуализация	matplotlib + live histogram
6. Контейнеризация	Docker + Docker Compose


# Результат

<img width="913" height="529" alt="image" src="https://github.com/user-attachments/assets/6cb76232-221e-4f9f-8f3b-760c0d6e611b" />
<img width="1253" height="694" alt="image" src="https://github.com/user-attachments/assets/f9ba9484-31f2-408c-a5da-02de5c989f49" />


Полностью рабочая production-grade ML система:

- Микросервисная архитектура

- Асинхронный обмен через RabbitMQ

- Real-time метрики и визуализация

- Docker-контейнеризация

- Готово к scale & deploy
