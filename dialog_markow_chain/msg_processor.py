import pickle
import random

def load_msg_list(file_name):
    return pickle.load(open(file_name, 'rb'))

def happy_end(msg):
    msg_copy = msg.strip()
    last = msg_copy[-1:]
    if (last != '.' and last != ',' and last != '?' and last != '!'):
        return '.'
    else:
        return ''

def get_user_words_list(ids, msg_list):
    user_msg_list = []

    for msg in msg_list:
        if msg['from_id'] in ids:
            msg_body = msg['body']
            if len(msg_body) < 1:
                continue
            user_msg_list.append(msg_body + happy_end(msg_body))
        # if len(user_msg_list) > 400:
        #     break

    long_msg = ' '.join(user_msg_list)
    long_msg = long_msg.lower()

    long_msg = long_msg.replace('..', '.')
    long_msg = long_msg.replace(',', ' ,')
    long_msg = long_msg.replace('.', ' .')
    long_msg = long_msg.replace('?', ' ?')
    long_msg = long_msg.replace('!', ' !')
    long_msg = long_msg.replace(')', '')
    long_msg = long_msg.replace('(', '')
    long_msg = long_msg.replace('#', '')
    long_msg = long_msg.replace('.', '')

    words = [word.strip() for word in long_msg.split(' ')]
    # words = [word for word in words if len(word) > 0]
    return words

class MarkowPredictor(object):

    def __init__(self):
        self.end_symbol = '#'

    def fit(self, word_list, predict_length=3):
        self.predictor_dict = {}
        for index in range(0, len(word_list) - predict_length):
            current_word_tuple = tuple(word_list[index:index + predict_length])
            if current_word_tuple not in self.predictor_dict:
                self.predictor_dict[current_word_tuple] = [self.end_symbol]
            self.predictor_dict[current_word_tuple].append(word_list[index + predict_length])

    def predict(self, word_list):
        if tuple(word_list) in self.predictor_dict:
            return random.choice(self.predictor_dict[tuple(word_list)])
        else:
            return self.end_symbol

def get_chain(predicts, length, words):
    markow2 = MarkowPredictor()
    markow2.fit(words, predict_length=2)

    markow3 = MarkowPredictor()
    markow3.fit(words, predict_length=3)

    word_tuple = predicts.copy()

    for i in range(2000):
        predicted_word_2 = markow2.predict(word_tuple[1:])
        predicted_word_3 = markow3.predict(word_tuple)
        predicted_word = random.choice([predicted_word_2, predicted_word_3])
        if predicted_word != '#':
            word_tuple.append(predicted_word)
            word_tuple = word_tuple[1:]
            predicts.append(predicted_word)

    phrase = ''
    for predicted in predicts:
        phrase += (predicted + ' ')
        if predicted == '.' or predicted == '!' or predicted == '?':
            phrase += '\n'

    return phrase

with open('parameters.txt', 'r') as parameters:
    TOKEN = parameters.readline().split(' ')[0]
    chat_id = int(parameters.readline().split(' ')[0])
    file_downloaded_msgs_name = parameters.readline().split(' ')[0]
    length = int(parameters.readline().split(' ')[0])
    predicts = parameters.readline().split(' ')[:3]
    ids = set([int(id) for id in parameters.readline().split('#')[0].split(' ') if len(id) > 0])

print(TOKEN)
print(chat_id)
print(file_downloaded_msgs_name)
print(length)
print(predicts)
print(ids)

msg_list = load_msg_list(file_downloaded_msgs_name)
words = get_user_words_list(ids, msg_list)

phrase = get_chain(predicts, length, words)

print(phrase)



