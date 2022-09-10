import csv
import nltk
import string
nltk.download('stopwords')
from nltk.corpus import stopwords
comments = []


with open('teams4.csv', 'r', encoding="utf-8") as file:
    reader = csv.reader(file)
    rows = list(reader)
    for row in rows[0:400]:
        if len(row) > 0:
            comments.extend([row])


def remove_stopwords(comment_text):
    stop_words = set(stopwords.words('english'))
    translate_table = dict((ord(char), None) for char in string.punctuation) # Removes punctuation
    comment_text = comment_text.translate(translate_table)
    comment_text = comment_text.replace('’', '')
    comment_text = comment_text.replace(',', '')
    comment_text_token = nltk.tokenize.word_tokenize(comment_text)
    filtered_sentence = []
    for current_word in comment_text_token:
        if current_word not in stop_words:
            filtered_sentence.append(current_word)
    return filtered_sentence


def sentiment(comment_list): # This sets the criteria for sentiment, for now a placeholder threshold of 10 upvotes is used.
    sentiment_list = []
    matches_1 = ["eclerc", "errari", "sainz"]
    matches_2 = ["erstappen", "erez", "Bull", "bull"]
    matches_3 = ["amilton", "ercedes" "ussel"]
    for user_post in comment_list:
        if len(user_post) > 1:
            if any(x in str(user_post[1]) for x in matches_1):
                team = 1
                sentiment_list.append([team, user_post[-3]])
            elif any(x in str(user_post[1]) for x in matches_2):
                team = 2
                sentiment_list.append([team, user_post[-3]])
            elif any(x in str(user_post[1]) for x in matches_3):
                team = 3
                sentiment_list.append([team, user_post[-3]])

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
    post_count_1 = dict.fromkeys(word_atlas, 0)
    post_count_2 = dict.fromkeys(word_atlas, 0)
    post_count_3 = dict.fromkeys(word_atlas, 0)

    for comnt in raw_sentiment:
        for wrd in word_atlas:
            if wrd in comnt[-1]:
                if int(comnt[0]) == 1:
                    post_count_1[wrd] += 1
                elif int(comnt[0]) == 2:
                    post_count_2[wrd] += 1
                elif int(comnt[0]) == 3:
                    post_count_3[wrd] += 1

    post_count_1 = {key: value / len(post_count_1) for key, value in post_count_1.items()}
    post_count_2 = {key: value / len(post_count_2) for key, value in post_count_2.items()}
    post_count_3 = {key: value / len(post_count_3) for key, value in post_count_3.items()}
    return post_count_1, post_count_2, post_count_3


probability_dct = likelyhoods(user_sentiments)
print(probability_dct[0])
print(probability_dct[1])
preset_priors = [0.333333, 0.3333333, 0.333333]


def posteriors(priors_input, list1):
    post_1 = [a * b for a, b in zip(priors_input, list1)]
    if post_1[0] + post_1[1] + post_1[2] > 0:
        post_1_1 = (post_1[0]) / (post_1[0] + post_1[1] + post_1[2])
        post_1_2 = (post_1[1]) / (post_1[0] + post_1[1] + post_1[2])
        post_1_3 = (post_1[2]) / (post_1[0] + post_1[1] + post_1[2])
    else:
        post_1_1 = 0.333333
        post_1_2 = 0.333333
        post_1_3 = 0.333333
    return post_1_1, post_1_2, post_1_3


def find_word_probs(comments_inpt):
    comments_probs = []
    for commt in comments_inpt:
        addition = []
        for wrd in word_atlas:
            if wrd in commt[-3]:
                if probability_dct[0][wrd] >= 0 and probability_dct[1][wrd] >= 0 and probability_dct[2][wrd] >= 0:
                    addition.append([wrd, probability_dct[0][wrd], probability_dct[1][wrd], probability_dct[2][wrd]])
        comments_probs.append([addition, commt])
    return comments_probs


new_probs = find_word_probs(comments)
print(new_probs)


def classifier(found_probs):
    final_list = []
    for sentence_probs in found_probs:
        sentence_probs2 = sentence_probs[0]
        counter = 0
        if len(sentence_probs2) > 0:
            for pair in range(len(sentence_probs2)-1):
                if counter == 0:
                    first_pair = posteriors(preset_priors, sentence_probs2[pair][-3:])
                first_pair = posteriors(first_pair, sentence_probs2[pair+1][-3:])
                counter += 1

            final_list.append([first_pair, sentence_probs])
    return final_list # returns the results of the posteriors and the comment with metadata


def check_accuracy(prediction_scores):
    matches_1 = ["eclerc", "errari", "sainz"]
    matches_2 = ["erstappen", "erez", "Bull", "bull"]
    matches_3 = ["amilton", "ercedes" "ussel"]

    wrong_answers = 1
    right_answers = 1
    count_red = 0
    count_merc = 0
    count_ferr = 0
    counter = 0
    for comment in prediction_scores:
        # make the prediction
        if comment[0][0] > 0.3333:
            prediction = "ferrari"
        elif comment[0][1] > 0.33333333:
            prediction = "red-bull"
        elif comment[0][2] > 0.33333333:
            prediction = "mercedes"
        # check if it is right
        if any(x in str(comment[-1][-1][1]) for x in matches_1):
            answer = "ferrari"
        elif any(x in str(comment[-1][-1][1]) for x in matches_2):
            answer = "red-bull"
        elif any(x in str(comment[-1][-1][1]) for x in matches_3):
            answer = "mercedes"


        if prediction == answer:
            right_answers += 1
        elif answer == "red-bull" or answer == "ferrari" or answer == "mercedes":
            wrong_answers += 1

        print(right_answers/(right_answers + wrong_answers))
        print (right_answers, wrong_answers)


b = classifier(new_probs)
c = check_accuracy(b)

comments_check = []

with open('teams.csv', 'r', encoding="utf-8") as file:
    reader = csv.reader(file)
    rows = list(reader)
    for row in rows[400:500]:
        if len(row) > 0:
            comments_check.extend([row])

new_check = find_word_probs(comments_check)
classified = classifier(new_check)
accuracy = check_accuracy(classified)

