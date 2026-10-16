import requests
from bs4 import BeautifulSoup

def print_secret_message(url):
    response = requests.get(url, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table")
    
    if table is None:
        return print("No table found in the document.")

    characters = {}
    max_x = max_y = 0

    for row in table.find_all("tr"):
        cells = row.find_all("td")

        if len(cells) != 3:
            continue

        x_text = cells[0].get_text(strip=True)
        y_text = cells[2].get_text(strip=True)

        if not x_text.isdecimal() or not y_text.isdecimal():
            continue

        x, y = int(x_text), int(y_text)
        character = cells[1].get_text()

        characters[x, y] = character
        max_x = max(max_x, x)
        max_y = max(max_y, y)

    if not characters:
        return print("No valid character data found in the table.")

    for y in range(max_y, -1, -1):
        print("".join(
            characters.get((x, y), " ")
            for x in range(max_x + 1)
        ))


print_secret_message()