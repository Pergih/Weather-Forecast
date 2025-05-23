import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_mock_sales(days=7):
    today = datetime.today()
    dates = [(today - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(days)]
    np.random.seed(42)

    data = {
        "date": dates,
        "hot_drinks": np.random.poisson(lam=30, size=days),
        "cold_drinks": np.random.poisson(lam=50, size=days),
        "umbrellas": np.random.poisson(lam=10, size=days)
    }

    df = pd.DataFrame(data)
    df.to_csv("data/sales_data.csv", index=False)
    print("Saved sales data.")

if __name__ == "__main__":
    generate_mock_sales()
