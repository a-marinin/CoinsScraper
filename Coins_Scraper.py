import bs4 as bs
import urllib.request
import pandas as pd

# Scrape all coins from the list
def scrape_preview_page(coin_id):
    """
        This function receives "coins_id" from "coins_to_scrape list".
        It scrapes coin's data from the list into the pandas DataFrame
        Then it saves this DataFrame as Excel sheet.
        It scrapes Country, Value, Year, Metal, Marks, Mintage, Krause code, Price, Quality, Details, Avers, Revers and Gcoins link data
    """
    gcoins_link = 'http://www.gcoins.net/en/catalog/view/{}'.format(coin_id)
    source = urllib.request.urlopen(gcoins_link).read()
    soup = bs.BeautifulSoup(source, 'lxml')

    print("Scrapping the information about the coin № " + str(coin_id))

    table = soup.find('table', attrs={'class': 'subs noBorders evenRows'})  # The table of mintages
    table_rows = table.find_all('tr')                                       # Find all table rows

    res = []                                                                # New list of all coins
    for tr in table_rows:                                                   # Find all table_cells (td) in table_row
        td = tr.find_all('td')
        row = [tr.text for tr in td]
        res.append(row)                                                     # Append each <td> in the "res" list

    krause = soup.find("p", {"class": "krause"}).text                                                # Find the Krause number
    desc = soup.find("p", {"class": "desc"}).text                                                    # Find description (country/denomination)
    details = soup.find("p", {"class": "details"}).text
    material = soup.find('td', {'class' : 'storeItemDescription'})                                   # Find all <td> in "storeItemDescription"
    material2 = material.findAll('p')[2].text                                                        # Find material ("Bronze")
    image = soup.find('img', {"class": ['shadowIn', 'coin', 'imgARRotate']}).get('src')              # Get the image <src>
    image_a = image.replace('/coins/', 'http://www.gcoins.net/coins/')                               # Avers of coin
    image_r = image.replace('_a.jpg', '_r.jpg').replace('/coins/', 'http://www.gcoins.net/coins/')   # Revers of coin
    df = pd.DataFrame(res, columns=["foo", "bar", "Year", "Marks", "Mintage", "Quality", "Price"])
    df['Krause'] = krause
    df['Country'] = desc.split(",")[0]
    df['Value'] = desc.split(",")[1]
    df['Details'] = details.replace("\n", "")
    df['Metal'] = material2
    df['Avers'] = image_a
    df['Revers'] = image_r
    df['Gcoins_link'] = gcoins_link
    df = df.drop(['foo'], axis='columns').drop(0)                                                    # Cut first 2 coukmns and 1st row
    df = df[['Country', 'Value', 'Year', 'Metal', 'Marks', 'Mintage', 'Krause', 'Price', 'Quality', 'Details', 'Avers', 'Revers', 'Gcoins_link']]
    return df[['Country', 'Value', 'Year', 'Metal', 'Marks', 'Mintage', 'Krause', 'Price', 'Quality', 'Details', 'Avers', 'Revers', 'Gcoins_link']]


def scrape_tile_page(link):
    source = urllib.request.urlopen(link).read()
    soup = bs.BeautifulSoup(source, 'lxml')

    print("On the page " + str(link) + " there are following coins:")

    links = [i.get("href") for i in soup.find_all('a', attrs={'class': 'view'})]
    # List comprehensions
    links = [l.replace('/en/catalog/view/', '') for l in links]
    print(links)

# List of all coins_id's to scrape
coins_to_scrape =[514, 515, 179080, 45518, 521, 111429, 522, 182223, 168153, 523, 524, 60228, 525, 539, 540, 31642, 553, 558, 559, 77672, 560, 55377, 55379, 32001, 561, 562, 72185, 563, 564, 565]

# Construct list of dataFrames via list comprehension
df_list = [scrape_preview_page(i) for i in coins_to_scrape]
# Combine dataFrames in list
df = pd.concat(df_list, ignore_index=True)
# Save DateFrame to Excel sheet
df.to_excel('Coins.xlsx')


# # Scrape coin-id's from the certain link
# scrape_tile_page(link='http://www.gcoins.net/en/catalog/236/1')