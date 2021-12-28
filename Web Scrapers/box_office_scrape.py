import requests
from requests_html import HTML
import pandas as pd
import os
import datetime
import sys

FILE_PATH = os.path.abspath(__file__)
BASE_DIR = os.path.dirname(FILE_PATH)
DATA_DIR = os.path.join(BASE_DIR, "box_office_data")
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)


# function to get HTML response
def url_to_txt(url, filename="world.html", save=False):
    # get url
    r = requests.get(url)

    # if request success
    if r.status_code == 200:
        # read text of the HTML response
        html_text = r.text
        if save:
            # save to file if true
            with open("world.html", 'w') as f:
                f.write(html_text)
        return html_text
    return None


# function to pass html_text and find the table element
def find_element_in_html(html_txt):
    # use requests_html module to parse HTML data
    r_html = HTML(html=html_txt)
    # isolate table with class name
    table_class = ".imdb-scroll-table"
    # find element with class name in html
    table = r_html.find(table_class)
    return table


# function to append table data into a list
def table_to_list(rows):
    table_data = []

    # from the second element onward
    for row in rows[1:]:
        # return list of table data
        cols = row.find("td")
        row_data = []
        # use enumerate and populate column's data to row
        for i, col in enumerate(cols):
            row_data.append(col.text)

        # append row to table
        table_data.append(row_data)

    return table_data


# function to convert table into a csv file
def data_to_csv(table_data, header_names, year_name):
    filepath = os.path.join(DATA_DIR, f'{year_name}.csv')
    df = pd.DataFrame(table_data, columns=header_names)
    df.to_csv(filepath, index=False)


# function to parse and extract HTML data
def parse_and_extract(url, name="2021"):
    # get html text of URL using url_to_txt function
    html_text = url_to_txt(url)

    # parse html data and get table element
    r_table = find_element_in_html(html_text)

    if len(r_table) == 0:
        return False
    else:
        # if table found
        parsed_table = r_table[0]
        # return list of table rows
        rows = parsed_table.find("tr")
        # from the rows, isolate header rows
        header_row = rows[0]
        # return list of table headers
        header_col = header_row.find("th")
        # populate headers using header_col
        header_names = [x.text for x in header_col]

        # look through the table element and get data
        table_data = table_to_list(rows)

        # convert table data into a csv file
        data_to_csv(table_data, header_names, name)
        return True


def scrape_movie_data(start_year=None, years_ago=0):
    if start_year is None:
        now = datetime.datetime.now()
        start_year = now.year

    assert isinstance(start_year, int)
    assert isinstance(years_ago, int)
    assert len(f"{start_year}") == 4

    # grab url in range from start year argv[1] in duration argv[2]
    for i in range(0, years_ago):
        # function call
        url = f"https://www.boxofficemojo.com/year/world/{start_year}"
        finished = parse_and_extract(url, name=start_year)
        if finished:
            print(f"Finished {start_year}")
        else:
            print(f"{start_year} not found")
        start_year -= 1


if __name__ == "__main__":
    try:
        start = int(sys.argv[1])
    except:
        raise SystemExit(f"Usage: python <module name> <start year> <duration>")

    try:
        duration = int(sys.argv[2])
    except:
        raise SystemExit(f"Usage: python <module name> <start year> <duration>")
    scrape_movie_data(start_year=start, years_ago=duration)
