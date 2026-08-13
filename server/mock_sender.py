import random
import time

import requests

API_URL = "http://127.0.0.1:8000/api/readings"
NODE_ID = "env-node-01-mock"
INTERVAL_SECONDS = 5


def build_reading() -> dict:
    return {
        "node_id": NODE_ID,
        "temperature_c": round(random.uniform(21.0, 27.0), 2),
        "humidity_percent": round(random.uniform(38.0, 58.0), 2),
        "pressure_hpa": round(random.uniform(1005.0, 1020.0), 2),
        "light_lux": round(random.uniform(50.0, 650.0), 2),
    }


def main() -> None:
    print(f"Sending mock readings to {API_URL} every {INTERVAL_SECONDS}s")

    while True:
        reading = build_reading()

        try:
            response = requests.post(API_URL, json=reading, timeout=5)
            response.raise_for_status()
            print(response.json())
        except requests.RequestException as exc:
            print(f"Send failed: {exc}")

        time.sleep(INTERVAL_SECONDS)


if __name__ == "__main__":
    main()
