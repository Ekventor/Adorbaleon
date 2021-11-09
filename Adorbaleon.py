import sqlite3
import random

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
