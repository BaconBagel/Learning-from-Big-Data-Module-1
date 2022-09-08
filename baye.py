import csv
import nltk
import string
nltk.download('stopwords')
from nltk.corpus import stopwords
comments = []


with open('example.csv', 'r', encoding="utf-8") as file:
    reader = csv.reader(file)
    rows = list(reader)
    for row in rows[0:100]:
        if len(row) > 0:
            comments.extend([row])


def remove_stopwords(comment_text):
    stop_words = set(stopwords.words('english'))
    translate_table = dict((ord(char), None) for char in string.punctuation) # Removes punctuation
    comment_text = comment_text.translate(translate_table)
    comment_text = comment_text.replace('’', '')
    comment_text_token = nltk.tokenize.word_tokenize(comment_text)
    filtered_sentence = []
    for current_word in comment_text_token:
        if current_word not in stop_words:
            filtered_sentence.append(current_word)
    return filtered_sentence


def sentiment(comment_list): # This sets the criteria for sentiment, for now a placeholder threshold of 10 upvotes is used.
    sentiment_list = []
    for user_post in comment_list:
        if int(user_post[-2]) > 10:
            upvoted = "1"
        else:
            upvoted = "0"
        sentiment_list.append([upvoted, user_post[-3]])

    return sentiment_list


def count_words(list_with_text, text_position): #text_position ist the place the text body has in the list
    count_list = []
    count_dict = {}
    for s in list_with_text:
        count_list.extend(remove_stopwords(s[int(text_position)]))
    for c in range(len(count_list)):
        count_dict[count_list[c]] = count_list.count(count_list[c])
    return count_dict


user_sentiments = sentiment(comments)
counts = count_words(user_sentiments, -1)
word_atlas = counts.keys()
print(counts, word_atlas, user_sentiments)


def likelyhoods(raw_sentiment):
    post_count_pos = dict.fromkeys(word_atlas, 0)
    post_count_neg = dict.fromkeys(word_atlas, 0)

    for comnt in raw_sentiment:
        for wrd in word_atlas:
            if wrd in comnt[-1]:
                if int(comnt[0]) == 1:
                    post_count_pos[wrd] += 1
                elif int(comnt[0]) == 0:
                    post_count_neg[wrd] += 1

    post_count_neg = {key: value / len(raw_sentiment) for key, value in post_count_neg.items()}
    post_count_pos = {key: value / len(raw_sentiment) for key, value in post_count_pos.items()}
    return post_count_pos, post_count_neg


neeer = likelyhoods(user_sentiments)
print(neeer[0])
print(neeer[1])


def posterior(prob_dict, key_words):
    prob_dict_no_zero = {x: y for x, y in prob_dict.items() if y != 0}
    total_prob = sum(prob_dict_no_zero.values())
    posteriors = {key: value * total_prob for key, value in prob_dict_no_zero.items()}
    print(posteriors)


iops = posterior(neeer[0], "smiling")
iops2 = iops = posterior(neeer[1], "smiling")



