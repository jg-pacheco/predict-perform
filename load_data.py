import csv
import requests
from bs4 import BeautifulSoup
import pandas as pd


def fix_cols_and_overwrite(df, file_path):
    # Get a list of the column names
    columns = df.columns

    # insert an index column
    df.reset_index(inplace=True)

    # drop extra nan columns
    df.drop(df.columns[-1], axis=1, inplace=True)

    # overwrite previous columns
    df.columns = columns
    df.drop('Rk', axis=1, inplace=True)
    df.fillna(0, inplace=True)
    df.to_csv(file_path)


def load_data(years=15):
    season_type_strs = ["playoffs", "leagues"]
    years = [2000 + x for x in range(22, 22-years, -1)]
    # we're stopping at 15 since that is the max requests before being shadow banned by the website
    for year in years:
        for szn_type in season_type_strs:
            url = f"https://www.basketball-reference.com/{szn_type}/NBA_{year}_per_game.html"

            # parse html
            soup = BeautifulSoup(requests.get(url).content, "html.parser")
            # Find the table containing the player data
            table = soup.find("table", attrs={"id": "per_game_stats"})

            # Extract table headers
            headers = [th.text for th in table.find("thead").find_all("th")]

            # Extract player data rows
            rows = []
            for tr in table.find("tbody").find_all("tr"):
                data = [td.text for td in tr.find_all("td")]
                rows.append(data)

            # Save the player data as a CSV file
            csv_filename = f"./data/{year}_{szn_type[:-1]}.csv"
            with open(csv_filename, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(headers)
                writer.writerows(rows)
            if(szn_type == "leagues"):
                szn_df = pd.read_csv(csv_filename)

                playoff_file_path = f'data/{year}_playoff.csv'
                playoff_df = pd.read_csv(playoff_file_path)

                # remove duplicate values for players who were traded
                # first value by default is season totals so okay to drop rest
                szn_df_uniques = szn_df[~szn_df['Rk'].duplicated()]

                # drop players not in the playoffs
                szn_made_playoffs_df = szn_df_uniques[szn_df_uniques['Rk'].isin(
                    playoff_df['Rk'])]

                fix_cols_and_overwrite(szn_made_playoffs_df, csv_filename)
                fix_cols_and_overwrite(playoff_df, playoff_file_path)


def __main__():
    load_data()


if __name__ == "__main__":
    __main__()
