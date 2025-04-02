# import requests
# from bs4 import BeautifulSoup
# import random
# import string
# from collections import Counter
#
# def scrapeWikiArticle(url):
#     response = requests.get(url=url)
#     soup = BeautifulSoup(response.content, 'html.parser')
#
#     title = soup.find(id="firstHeading").text
#     print(f"Title: {title}")
#
#     # Извлекаем текст статьи
#     paragraphs = soup.find(id="bodyContent").find_all('p')
#     text_content = ' '.join([para.text for para in paragraphs])
#
#     # Обрабатываем текст с помощью mapper
#     word_counts = mapper(text_content)
#
#     # Находим случайную ссылку для дальнейшего парсинга
#     all_links = soup.find(id="bodyContent").find_all("a")
#     random.shuffle(all_links)
#     link_to_scrape = None
#
#     for link in all_links:
#         if link['href'].find("/wiki/") != -1 and not link['href'].startswith("/wiki:"):
#             link_to_scrape = link
#             break
#
#     # Если нашли ссылку, продолжаем парсинг
#     if link_to_scrape:
#         word_counts.update(scrapeWikiArticle("https://en.wikipedia.org" + link_to_scrape['href']))
#
#     return word_counts
#
# def clean_and_split_text(text):
#     # Удаляем знаки пунктуации и разбиваем текст на слова
#     translator = str.maketrans('', '', string.punctuation)
#     cleaned_text = text.translate(translator).lower()  # Приводим к нижнему регистру
#     return cleaned_text.split()
#
# def mapper(text):
#     words = clean_and_split_text(text)
#     # Фильтруем слова, начинающиеся на "Э" или "э"
#     filtered_words = [word for word in words if word.startswith('э')]
#     return Counter(filtered_words)  # Возвращаем Counter для подсчета вхождений
#
# def reducer(word_counts):
#     # Подсчитываем общее количество вхождений слов
#     return word_counts
#
# def main():
#     initial_url = "https://en.wikipedia.org/wiki/Web_scraping"
#     total_word_counts = Counter(scrapeWikiArticle(initial_url))
#
#     # Сортируем по убыванию
#     sorted_word_counts = sorted(total_word_counts.items(), key=lambda x: x[1], reverse=True)
#
#     # Выводим результат
#     for word, count in sorted_word_counts:
#         print(f"{word}: {count}")
#
# if __name__ == "__main__":
#     main()





import requests
from bs4 import BeautifulSoup
import random
import string
from collections import Counter



def scrapeWikiArticle(url, page_count):
    if page_count >= MAX_PAGES:
        return Counter()  # Если достигли максимального количества страниц, возвращаем пустой счетчик

    response = requests.get(url=url)
    soup = BeautifulSoup(response.content, 'html.parser')

    title = soup.find(id="firstHeading").text
    print(f"Title: {title}")

    # Извлекаем текст статьи
    paragraphs = soup.find(id="bodyContent").find_all('p')
    text_content = ' '.join([para.text for para in paragraphs])

    # Обрабатываем текст с помощью mapper
    word_counts = mapper(text_content)

    # Находим случайную ссылку для дальнейшего парсинга
    all_links = soup.find(id="bodyContent").find_all("a")
    random.shuffle(all_links)
    link_to_scrape = None

    for link in all_links:
        if link['href'].find("/wiki/") != -1 and not link['href'].startswith("/wiki:"):
            link_to_scrape = link
            break

    # Если нашли ссылку, продолжаем парсинг
    if link_to_scrape:
        next_url = "https://en.wikipedia.org" + link_to_scrape['href']  # Правильное формирование URL
        word_counts.update(scrapeWikiArticle(next_url, page_count + 1))  # Увеличиваем счетчик страниц

    return word_counts

def clean_and_split_text(text):
    # Удаляем знаки пунктуации и разбиваем текст на слова
    translator = str.maketrans('', '', string.punctuation)
    cleaned_text = text.translate(translator).lower()  # Приводим к нижнему регистру
    return cleaned_text.split()

def mapper(text):
    words = clean_and_split_text(text)
    # Фильтруем слова, начинающиеся на "E" или "e"
    filtered_words = [word for word in words if word.startswith(symbol)]
    return Counter(filtered_words)  # Возвращаем Counter для подсчета вхождений

def main():
    print("Введите количество страниц для парсинга (они случайные):")
    MAX_PAGES = int(input())  # Максимальное количество страниц для парсинга
    print("Введите букву, по которой искать слова:")
    symbol = input().lower()  # Сохраняем букву в нижнем регистре

    initial_url = "https://en.wikipedia.org/wiki/Web_scraping"
    total_word_counts = Counter(scrapeWikiArticle(initial_url, 0))

    # Сортируем по убыванию
    sorted_word_counts = sorted(total_word_counts.items(), key=lambda x: x[1], reverse=True)

    # Записываем результат в файл
    with open('word_counts.txt', 'w', encoding='utf-8') as f:
        for word, count in sorted_word_counts:
            f.write(f"{word}: {count}\n")

    print("Результаты успешно записаны в файл word_counts")

if __name__ == "__main__":
    main()
