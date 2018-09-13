# The purpose of this program is to analyse a whatsapp group chat and infer the following:
#   1. Most active members (with stats)
#   2. ----- ------
#   3. Top 10 words
#   4. When are the members most active(by day, special day)
#   5. Most used emoji and member using the most emoji
#
#
#
# {"Name": [
#          [date,[time,message],[time,message]], <-- one struc
#          [date,[time,message],[time,message]]  <-- another struc
#          ]}
#
#


from nltk.tokenize import sent_tokenize, word_tokenize
import nltk
import re
import matplotlib.pyplot as plt
import emoji
import numpy as np


# Check if name or date already in dict
def checker(sample, date, name):
    #no name entry
    if not name in data:
        data[name] = []
        return False
    else:
        value = data[name]
        # if date of message already exists, append only message
        if date == value[-1][0]:
            return True
        else:
            return False

def dictify(sample):
    line = sample.readline()
    while line:
        # converting line to word tokens
        entry = word_tokenize(line)

        # check if name is given or number
        if re.findall(r'91',entry[5]):
            num = re.findall(r'\d{5}',entry[7])
            name = ''.join([entry[6],num[0]])
        else:
            name = entry[5]

        date = re.findall(r'\d{1,2}/\d{1,2}/\d{2}',entry[0])
        time = ''.join(entry[2:4])
        length = len(entry)
        message = ''
        i = 6 # index of possible start of ":" before message

        # handling exceptions
        while not entry[i]==":":
            if entry[i] in ["added","changed","left"]:
                i = length
                break
            i+=1

        for i in range(i+1,length):
            message = ' '.join([message,entry[i]])

        line = sample.readline()

        #check if multi-line messsage
        while line and re.match(r'\d{1,2}/\d{1,2}/\d{2},',line)==None:
            message = ' '.join([message,line])
            line = sample.readline()

        # remove whitespace
        message = re.sub(r'\s+',' ',message)
        # add word to new words dict
        message = word_dict(message)

        # check if name or date already in dict
        if checker(sample,date[0],name):
            data[name][-1].append([time,message])
        else:
            data[name].append([date[0],[time,message]])

def print_dict():
    # printing to a file
    output = open("data.txt",'w',encoding="utf8")
    for name in data:
        # print(name)
        output.write(name)
        output.write('\n')
        for struc in data[name]:
            # print(struc[0])
            # [print(i[0],":",i[1]) for i in struc[1:]]
            output.write(struc[0])
            output.write('\n')
            for i in struc[1:]:
                output.write(i[0])
                output.write(":")
                # print(i[1])
                output.write(i[1])
                output.write('\n')
        # print('\n')
        output.write('\n')
        # output.write('\n')
    output.close()

def most_active():
    a,b = [],[] # name[] and no. of messages[]
    for name in data:
        l = 0
        a.append(name)
        for struc in data[name]:
            # excluding 1st element i.e. date
            for i in struc[1:]:
                l = l + len(i)-1
        b.append(l)
    
    x,y = [],[]
    # finding top 5 active users
    for i in range(5):
        ind = b.index(max(b))
        x.append(a.pop(ind))
        y.append(b.pop(ind))
    
    # plotting bar graph
    plt.bar(x, y, align='center')
    plt.ylabel('Messages')
    plt.title('Most Active Users')
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
                new_word+= c
        new_message = ' '.join([new_message,new_word])
        words.append(new_word)
    return new_message

def print_top_words():
    # top_words = sorted(words, key = words.get, reverse = True)
    top_words = nltk.FreqDist(words)
    common_words = top_words.most_common(10)

    # common_words is a tuple (word, occurances)
    x = [w[0] for w in common_words]
    y = [n[1] for n in common_words]

    # plotting bar graph
    plt.bar(x, y, align='center')
    plt.ylabel('Words')
    plt.title('Most Used Words')
    plt.show()

def top_emoji():
    top_emojis = nltk.FreqDist(emojis)
    common_emojis = top_emojis.most_common(10)
    # common_emojis is a tuple (emoji, occurances)

    x = [e[0] for e in common_emojis]
    y = [n[1] for n in common_emojis]

    # plotting bar graph
    plt.bar(x, y, align='center')
    plt.ylabel('Times used')
    plt.title('Most Used Emojis :)')
    plt.show()


data = {}
words = []
emojis = []

sample = open("MYGChat.txt",encoding="utf8")
dictify(sample)
sample.close()

most_active()
print_top_words()
top_emoji()
print_dict()