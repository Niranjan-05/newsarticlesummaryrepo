import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
from datetime import date

def fetch_links(url):

    from datetime import date
    # Get today's date
    today = datetime.today()

    url = url
    response = requests.get(url)

    soup = BeautifulSoup(response.text, "html.parser")



    links = []
    articles = soup.find_all('div', class_='article-image')

    
    date_element  = soup.find(class_='date')
    date_str = date_element.text


    date_with_time = datetime.strptime(date_str, "%A, %B %d, %Y")
    


    datetime2 = datetime.strftime(date_with_time, '%Y-%m-%d %H:%M:%S')

    datetime2 = datetime.strptime(datetime2, '%Y-%m-%d %H:%M:%S')

    today = today.date()
    datetime2 = datetime2.date()




    if today == datetime2:

        for article in articles:
            link = article.find('a').get('href')

            links.append(link)

        articles = soup.find_all('div', class_='article')

        for article in articles:
            link = article.find('a').get('href')

            links.append(link)


        articles = soup.find_all('div', class_='article-style-two')

        for article in articles:
            link = article.find('a').get('href')

            links.append(link)

    return links

def extraction(links,filename):
    headlines = []
    contents = []
    dit = {}
    with open(filename,'wb') as f:
        
        for url in links:
            
            response = requests.get(url)

            soup = BeautifulSoup(response.text, 'html.parser')

            headline = soup.find('h1', class_='title-article').text.strip()

            
            content = soup.find('div', class_='article-body').text.strip()

            date_elem = soup.find('time', class_='publishing-date')
            date_text = date_elem.text.strip()
            date_text = date_text.split('Last Edited ')[1]
            date_format = '%B %d, %Y | %I:%M %p'
            # Parse the date string using datetime.strptime()
            date1 = datetime.strptime(date_text, date_format)
            formatted_date = date1.strftime('%Y %m %d')
            today = date.today()
            today = today.strftime('%Y %m %d')

            if True:

                content = re.sub(r'\n\s*\n', '\n\n', content)
                content = content.split('Related Story')[0]
                headlines.append(headline)
                contents.append(content)

                dit[headline] = content

    return dit

def delete_duplicates(dit,dupl):
    for key in dit:
    # If the key also exists in the intl_headlines dict, and the values are the same,
    # remove the key-value pair from intl_headlines
        if key in dupl and dupl[key] == dit[key]:
            del dupl[key]
    
            