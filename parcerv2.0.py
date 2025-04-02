import requests
from bs4 import BeautifulSoup
import random
import string
from collections import Counter

def parser(url, page_count, max_pages, symbol):
    if page_count >= max_pages:
        return Counter()  # возвращаем пустой счетчик

    response = requests.get(url=url)
    soup = BeautifulSoup(response.content, 'html.parser')
    title = soup.find(id="firstHeading").text
    print(f"Title: {title}")

    # Извлекаем текст статьи
    paragraphs = soup.find(id="bodyContent").find_all('p')
    text_content = ' '.join([para.text for para in paragraphs])

    # !!!!! тут функция запускается
    word_counts = mapper(text_content, symbol)

    # Находим случайную ссылку для дальнейшего парсинга
    all_links = soup.find(id="bodyContent").find_all("a") #спарсили все ссылки из статьи
    random.shuffle(all_links) #выбрали рандомную ссылку
    link_to_scrape = None
    for link in all_links:
        if link['href'].find("/wiki/") != -1 and not link['href'].startswith("/wiki:"): # проверка на наличие "/wiki/" в href
            link_to_scrape = link
            break

    if link_to_scrape:
        next_url = "https://en.wikipedia.org" + link_to_scrape['href']
        word_counts.update(parser(next_url, page_count + 1, max_pages, symbol))  # Увеличиваем счетчик страниц
    return word_counts

# Удаляем знаки пунктуации и разбиваем текст на слова
def clean_and_split_text(text):
    translator = str.maketrans('', '', string.punctuation)
    cleaned_text = text.translate(translator).lower()  # Приводим к нижнему регистру
    return cleaned_text.split()

def mapper(text, symbol):
    words = clean_and_split_text(text)
    filtered_words = [word for word in words if word.startswith(symbol)]
    return Counter(filtered_words)

def main():
    print("Введите количество страниц для парсинга (они выбираются случайно):")
    MAX_PAGES = int(input())
    print("Введите букву, по которой искать слова:")
    symbol = input().lower()

    initial_url = "https://en.wikipedia.org/wiki/Web_scraping"
    print("\nСпарсенные страницы:")
    total_word_counts = Counter(parser(initial_url, 0, MAX_PAGES, symbol))
    sorted_word_counts = sorted(total_word_counts.items(), key=lambda x: x[1], reverse=True)

    with open('word_counts.txt', 'w', encoding='utf-8') as f:
        for word, count in sorted_word_counts:
            f.write(f"{word}: {count}\n")
    print("\nРезультаты успешно записаны в файл word_counts.txt")

if __name__ == "__main__":
    main()
