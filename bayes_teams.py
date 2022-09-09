import csv
import nltk
import string
nltk.download('stopwords')
from nltk.corpus import stopwords
comments = []


with open('teamslegacy.csv', 'r', encoding="utf-8") as file:
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


def sentiment(comment_list): # Update this to identity instead of sentiment, do sentiment seperately. 
    sentiment_list = []
    matches_1 = ["eclerc", "errari", "sainz"]
    matches_2 = ["erstappen", "erez", "Bull", "bull"]
    for user_post in comment_list:
        if len(user_post) > 1:
            if any(x in str(user_post[1]) for x in matches_1):
                upvoted = "1"
                sentiment_list.append([upvoted, user_post[-3]])
            elif any(x in str(user_post[1]) for x in matches_2):
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


probability_dct = likelyhoods(user_sentiments)
print(probability_dct[0])
print(probability_dct[1])
preset_priors = [0.5, 0.5]


def posteriors(priors_input, list1):  # more dimensions can be added, see posteriors.py file 
    post_1 = [a*b for a, b in zip(priors_input, list1)]
    post_1_1 = (post_1[0]) / (post_1[0] + post_1[1])
    post_1_2 = (post_1[1]) / (post_1[0] + post_1[1])
    return post_1_1, post_1_2


def find_word_probs(comments_inpt):
    comments_probs = []
    for commt in comments_inpt:
        addition = []
        for wrd in word_atlas:
            if wrd in commt[-3]:
                if probability_dct[0][wrd] > 0 and probability_dct[1][wrd] > 0:
                    addition.append([wrd, probability_dct[0][wrd], probability_dct[1][wrd]])
        comments_probs.append([addition, commt])
    return comments_probs


newww = find_word_probs(comments)
print(newww)


def classifier(found_probs):
    for sentence_probs in found_probs:
        sentence_probs2 = sentence_probs[0]
        counter = 0
        if len(sentence_probs2) > 1:
            for pair in range(len(sentence_probs2)-1):
                if counter == 0:
                    first_pair = sentence_probs2[pair][-2:]
                first_pair = posteriors(first_pair, sentence_probs2[pair+1][-2:])
                counter += 1

            print(first_pair, sentence_probs)




b = classifier(newww)

