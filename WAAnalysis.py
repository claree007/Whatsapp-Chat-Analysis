from nltk.tokenize import sent_tokenize, word_tokenize
import nltk
import re
import matplotlib.pyplot as plt
import emoji
import numpy as np


class Messages:
    def __init__(self, time, message):
        self.time = time
        self.message = message

class DateAndMessages:
    def __init__(self, date):
        self.date = date
        self.messages = []

    def add(self, time, message):
        obj = Messages(time, message)
        self.messages.append(obj)

    def count_words(self):
        word_count = 0
        for obj in self.messages:
            word_count += len(obj.message) - 1
        return word_count


class Person:
    def __init__(self, name):
        self.name = name
        self.data = []

    def add(self, date, time, message):
        obj = self.date_exists(date)
        if obj != False:
            obj.add(time, message)
        else:
            obj = DateAndMessages(date)
            self.data.append(obj)
        obj.add(time, message)  

    def date_exists(self, date):
        for obj in self.data:
            if obj.date == date:
                return obj
        return False


# Check if name or date already in dict
def name_checker(name):
    for person in persons:
        if person.name == name:
            return person
    person = Person(name)
    persons.append(person)
    return person

def structure_chat(sample):
    line = sample.readline()
    while line:
        # converting line to word tokens
        entry = word_tokenize(line)

        # check if name is given or number
        # a mobile number will be 10 digits long starting with 9, 8 or 7
        if re.findall(r'91', entry[5]):
            num = re.findall(r'\d{5}', entry[7])
            name = ''.join([entry[6], num[0]])
        else:
            name = entry[5]

        date = re.findall(r'\d{1,2}/\d{1,2}/\d{2}', entry[0])
        time = ''.join(entry[2:4])
        length = len(entry)
        message = ''
        i = 6 # index of possible start of ":" before message

        # handling exceptions
        while entry[i] != ":":
            if entry[i] in ["added", "changed", "left"]:
                i = length
                break
            i += 1

        for i in range(i+1, length):
            message = ' '.join([message, entry[i]])

        line = sample.readline()

        #check if multi-line messsage
        while line and re.match(r'\d{1,2}/\d{1,2}/\d{2},', line) == None:
            message = ' '.join([message,line])
            line = sample.readline()

        # remove whitespace
        message = re.sub(r'\s+', ' ', message)
        # add word to new words dict
        message = word_dict(message)

        # check if name already exists
        person = name_checker(name)
        person.add(date, time, message)

def most_active(n):
    if n == 0:
        print("Please select a number greater than 0")
        return
    if n > 10:
        print("Please select a number less than", n)
        return
    
    total_words = {}
    # creating list of people and the word count of their messages
    for person in persons:
        word_count = 0
        for date_obj in person.data:
            word_count += date_obj.count_words()
        total_words[person.name] = word_count
    
    # Finding top n people

    # this will work even if n > number of people in group
    top_n = sorted(total_words, key=total_words.get, reverse=True)[:n]
    values = [total_words[key] for key in top_n]
    
    plt.bar(top_n, values, align='center')
    plt.ylabel('Messages')
    plt.title('Top ' + str(n) + ' Active Users')
    plt.show()


def word_dict(message):
    new_message = ''
    for word in word_tokenize(message):
        new_word = ''
        word = word.lower()
        for c in word:
            # check if emoji
            if c in emoji.UNICODE_EMOJI:
                emojis.append(c.encode('utf-8'))
            else:
                new_word += c
        new_message = ' '.join([new_message, new_word])
        words.append(new_word)
    return new_message

def print_top_words(n):
    if n == 0:
        print("Please select a number greater than 0")
        return
    if n > 10:
        print("Please select a number less than", n)
        return
    
    cleaned_words = []
    for word in words:
        if not(word in stop_words or word in punctuations):
            cleaned_words.append(word)
    top_words = nltk.FreqDist(cleaned_words)
    common_words = top_words.most_common(n)

    # common_words is a tuple (word, occurances)
    x = [word[0] for word in common_words]
    y = [occurance[1] for occurance in common_words]

    # plotting bar graph
    plt.bar(x, y, align='center')
    plt.ylabel('Words')
    plt.title('Most Used ' + str(n) + ' Words')
    plt.show()

def top_emoji(n):
    if n == 0:
        print("Please select a number greater than 0")
        return
    if n > 10:
        print("Please select a number less than", n)
        return
    
    top_emojis = nltk.FreqDist(emojis)
    common_emojis = top_emojis.most_common(n)
    # common_emojis is a tuple (emoji, occurances)

    x = [e[0].decode("utf-8") for e in common_emojis]
    y = [n[1] for n in common_emojis]

    # plotting bar graph
    plt.bar(x, y, align='center')
    plt.ylabel('Times used')
    plt.title(str(n) + ' Most Used Emojis :)')
    plt.show()


persons = []
words = []
emojis = []
punctuations = ['', ',', '\'', '<', '>', '!', '.', '?', ':', '...', '-']
stop_words = ["the", "and", "media", "omitted", "for", "of", "to", "in", 
              "is", "a", "on", "it"]

sample = open("chat.txt", encoding="utf8")
structure_chat(sample)
sample.close()

most_active(10)
print_top_words(10)
top_emoji(5)