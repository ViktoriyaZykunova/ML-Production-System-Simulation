import json
import os
import pandas as pd

import pika

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
LOG_PATH = os.path.join("logs", "metric_log.csv")


def ensure_log_header():
    if not os.path.exists(LOG_PATH):
        os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
        with open(LOG_PATH, "w", encoding="utf-8") as f:
            f.write("id,y_true,y_pred,absolute_error\n")


def main():
    ensure_log_header()

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST)
    )
    channel = connection.channel()

    channel.queue_declare(queue="y_true", durable=False)
    channel.queue_declare(queue="y_pred", durable=False)

    buffer = pd.DataFrame(columns=["id", "y_true", "y_pred"])

    def handle_message(msg, col_name):
        nonlocal buffer
        message_id = msg["id"]
        value = float(msg["body"])

        if message_id in buffer["id"].values:
            buffer.loc[buffer["id"] == message_id, col_name] = value
        else:
            new_row = {"id": message_id, "y_true": None, "y_pred": None}
            new_row[col_name] = value
            buffer = pd.concat([buffer, pd.DataFrame([new_row])],
                               ignore_index=True)

        row = buffer.loc[
            (buffer["id"] == message_id)
            & buffer["y_true"].notna()
            & buffer["y_pred"].notna()
        ]

        if not row.empty:
            r = row.iloc[0]
            abs_err = abs(r["y_true"] - r["y_pred"])
            with open(LOG_PATH, "a", encoding="utf-8") as f:
                f.write(
                    f'{r["id"]},{r["y_true"]},{r["y_pred"]},{abs_err}\n'
                )
            print(
                f"[metric] id={r['id']}, y_true={r['y_true']}, "
                f"y_pred={r['y_pred']}, ae={abs_err}"
            )

            buffer.drop(row.index, inplace=True)

    def callback_y_true(ch, method, properties, body):
        msg = json.loads(body.decode("utf-8"))
        handle_message(msg, "y_true")

    def callback_y_pred(ch, method, properties, body):
        msg = json.loads(body.decode("utf-8"))
        handle_message(msg, "y_pred")

    channel.basic_consume(
        queue="y_true", on_message_callback=callback_y_true, auto_ack=True
    )
    channel.basic_consume(
        queue="y_pred", on_message_callback=callback_y_pred, auto_ack=True
    )

    print("[metric] waiting for messages...")
    channel.start_consuming()


if __name__ == "__main__":
    main()
