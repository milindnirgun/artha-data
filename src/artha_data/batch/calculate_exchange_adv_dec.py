import os
import duckdb
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Construct a robust, absolute path to the database file.
_PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
_DB_DIR = os.path.join(_PROJECT_ROOT, "data")
DB_FILE = os.path.join(_DB_DIR, "artha.db")

def calculate_exchange_adv_dec():
    """
    Calculates the sum of adv_dec for each exchange for each load_date and returns a DataFrame.
    """
    con = duckdb.connect(database=DB_FILE, read_only=True)
    query = """
        SELECT
            tt.load_date,
            sm.exchange,
            SUM(tt.adv_dec) AS total_adv_dec
        FROM
            ticker_tape tt
        JOIN
            stock_master sm ON tt.symbol = sm.symbol
        GROUP BY
            tt.load_date,
            sm.exchange
        ORDER BY
            tt.load_date,
            sm.exchange;
    """
    df = con.execute(query).fetchdf()
    df['load_date'] = pd.to_datetime(df['load_date'])
    con.close()
    return df

def plot_adv_dec_by_exchange(df):
    """
    Plots the total adv_dec by exchange over time.
    """
    plt.figure(figsize=(12, 6))
    ax = sns.lineplot(data=df, x='load_date', y='total_adv_dec', hue='exchange')
    plt.title('Advance/Decline by Exchange')
    plt.xlabel('Date')
    plt.ylabel('Total Advance/Decline')
    plt.grid(True)

    # Add minor ticks for each day
    ax.xaxis.set_minor_locator(mdates.DayLocator())
    plt.grid(which='minor', axis='x', linestyle='--')

    plt.show()

if __name__ == "__main__":
    adv_dec_df = calculate_exchange_adv_dec()
    plot_adv_dec_by_exchange(adv_dec_df)
