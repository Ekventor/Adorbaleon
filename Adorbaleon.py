import sqlite3
import random
from traceback import format_exc
import requests
from bs4 import BeautifulSoup
import threading

connection = sqlite3.connect("data.db")
cursor = connection.cursor()


class StringGenerator:
    def __init__(self, ind_words):
        self.ind_words = ind_words
        self.chains, self.start_words, self.end_words = self.create_chains()

    def create_chains(self):
        chains = {}
        start_words = []
        end_words = []
        for string in self.ind_words:
            words = string.lower().split(" ")
            if len(words) > 3:
                start_words.append(" ".join(words[0:3]))
                end_words.append(" ".join(words[-3:]))
                for i in range(3, len(words)):
                    if " ".join(words[i-3:i]) not in chains:
                        chains[" ".join(words[i-3:i])] = []
                    chains[" ".join(words[i-3:i])].append(words[i])

        return chains, start_words, end_words

    def generate_string(self, start_text=None):
        if start_text is None:
            string = random.choice(self.start_words)
        else:
            possible_start_words = [word for word in self.start_words if start_text in word]
            string = random.choice(possible_start_words)

        while True:
            if len(string.split(" ")) > 100:
                break
            if " ".join(string.split(" ")[-3:]) in self.end_words:
                if 10 > random.randint(0, 99):
                    break
            try:
                string += " " + random.choice(self.chains[" ".join(string.split(" ")[-3:])])
            except KeyError:
                break

        return string


def send_wiki(required_information, peer_id):
    def get_wiki():
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
        }

        url = f"https://google.com/search?q={required_information}"
        page = requests.get(url, headers=headers).text
        soup = BeautifulSoup(page, "html.parser")

        url = soup.select_one(".yuRUbf > a")["href"]
        print(url)
        page = requests.get(url).text
        soup = BeautifulSoup(page, "html.parser")

        wiki_text = ""
        paragraphs = soup.select("p")
        for paragraph in paragraphs:
            wiki_text += paragraph.text

        wiki_text_list = []
        splitted_wiki_text = wiki_text.split(" ")
        typed_text = ""
        for i in range(len(splitted_wiki_text)):
            typed_text += splitted_wiki_text[i] + " "
            if i % 400 == 0 and i != 0:
                wiki_text_list.append(typed_text)
                typed_text = ""
        wiki_text_list.append(typed_text)

        return wiki_text_list

    wiki_text_list = get_wiki()
    while len(wiki_text_list) == 0:
        wiki_text_list = get_wiki()

    for text in wiki_text_list:
        vk.method("messages.send", {
            "peer_id": peer_id,
            "message": text,
            "random_id": 0
        })


def list_merge(iterable):
    result = []
    for lst in iterable:
        result.extend(lst)

    return result


def create_table():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ind_words(
            words TEXT,
            dateValue INTEGER
        )
    """)

    connection.commit()


if __name__ == "__main__":
    cursor.execute("""
        SELECT words
        FROM ind_words
    """)

    ind_words = list_merge(cursor.fetchall())
    generator = StringGenerator(ind_words)

    bot_text = generator.generate_string()
    print(f"Adorbaleon: {bot_text}")
