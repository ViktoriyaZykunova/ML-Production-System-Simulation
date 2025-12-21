import time
import os

import pandas as pd
import matplotlib.pyplot as plt

LOG_PATH = os.path.join("logs", "metric_log.csv")
OUT_PATH = os.path.join("logs", "error_distribution.png")


def main():
    plt.style.use("ggplot")

    while True:
        try:
            if os.path.exists(LOG_PATH):
                df = pd.read_csv(LOG_PATH)
                if not df.empty and "absolute_error" in df.columns:
                    errors = df["absolute_error"].values

                    plt.figure(figsize=(6, 4))
                    plt.hist(errors, bins=20, edgecolor="black")
                    plt.title("Absolute Error Distribution")
                    plt.xlabel("Absolute error")
                    plt.ylabel("Count")
                    plt.tight_layout()
                    plt.savefig(OUT_PATH)
                    plt.close()

                    print(
                        f"[plot] updated histogram with {len(errors)} points, "
                        f"saved to {OUT_PATH}"
                    )
        except Exception as e:
            print(f"[plot] error: {e}")

        time.sleep(3)


if __name__ == "__main__":
    main()
