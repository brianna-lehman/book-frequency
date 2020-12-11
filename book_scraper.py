import requests
from bs4 import BeautifulSoup
import re

urls = [
    "https://www.washingtonpost.com/graphics/2020/lifestyle/2020-best-books/",
    "https://www.esquire.com/entertainment/books/g30630848/best-books-of-2020/",
    "https://time.com/5913197/best-fiction-books-2020/",
    "https://www.nytimes.com/interactive/2020/books/notable-books.html",
    "https://www.penguinrandomhouse.com/the-read-down/the-best-books-of-2020",
    "https://www.harpersbazaar.com/culture/art-books-music/g30719704/best-new-books-2020/",
    "https://bookriot.com/best-books-of-2020-so-far/",
    "https://best-books.publishersweekly.com/pw/best-books/2020/top-10",
    "https://fivebooks.com/books/best-books-of-2020/"
]

html_class = [
    ['h3', 'font--headline'],
    ['span', 'listicle-slide-hed-text'],
    ['h2'],
    ['div', 'g-book-title'],
    ['h2'],
    ['span', 'listicle-slide-hed-text'],
    ['h2', 'book-title'],
    ['h3'],
    ['span', 'title']
]

title_count = {}

special_characters = ['\'', '\"', '-', ',', '’', '.']

def get_titles(place, soup):
    if place == 2:
        return soup.find_all(html_class[place][0])[:10]
    elif place == 4:
        return soup.find_all(html_class[place][0])[1::2]
    elif place == 7:
        return soup.find_all(html_class[place][0])
    else:
        return soup.find_all(html_class[place][0], class_=html_class[place][1])

def clean(place, title):
    title = title.text.strip()
    if place == 0:
        # remove beginning and ending quotes
        title = title[1:-1]
    elif place == 1:
        # remove everything after a comma
        title = title.split(',')[0]
        if title == '':
            title = 'Lurking'
    elif place == 2:
        # remove the number beginning and comma followed by author
        title = re.search('. (.*?),',title).group(1)
    
    # remove special characters
    for char in special_characters:
        title = title.replace(char, '')
    title = title.lower()
    # remove everything after the colon (ie Luster: A Novel -> Luster)
    title = re.search('(.+?)(?=:|$)', title).group(1)
    return title

def update_title_dict(title):
    if title in title_count:
        amount = title_count.get(title)
        amount += 1
        title_count[title] = amount
    else:
        title_count[title] = 1

def main():
    for x in range(len(urls)):
        url = urls[x]
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        titles = get_titles(x, soup)
        for title in titles:
            clean_title = clean(place=x, title=title)
            update_title_dict(clean_title)
    # sort by frequency of titles
    sorted_titles = sorted(title_count.items(), key=lambda x: x[1], reverse=True)
    # sort alphabetically by title name
    # sorted_titles = sorted(title_count.items(), key=lambda x: x[0])
    print(sorted_titles)

if __name__ == '__main__':
    main()

# TODO: visualizing this dictionary of data
# TODO: modularize it so that sites are only being scraped once then cached