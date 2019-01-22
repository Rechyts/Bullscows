import requests, random

token = '626714280:AAFL_BwntgFOnCH9nMsOhkMX8nvE3xZda5c'
url = 'https://api.telegram.org/bot{}/'.format(token)


class BotHandler:

    def __init__(self, token):
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)

    def get_updates(self, offset=None, timeout=600):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params)
        result_json = resp.json()['result']
        return result_json

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp

    def get_last_update(self):
        get_result = self.get_updates()

        if len(get_result) > 0:
            last_update = get_result[-1]
        else:
            last_update = get_result[len(get_result)-1]

        return last_update

bullscowsbot = BotHandler(token)



WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    :return: list of 4 long words
    """
    inFile = open(WORDLIST_FILENAME, 'r', encoding='UTF8')
    wordlist = []
    for line in inFile:
        if check_load_words(line.strip().lower()):
            wordlist.append(line.strip().lower())
    return wordlist


def check_load_words(word):
    for letter in word:
        if word.count(letter) == 1:
            return True
        else:
            return False


def choose_word():
    return random.choice(load_words())


def count_score(word, choosed_word):
    bull = 0
    cow = 0
    list_choosed_word = list(word)
    for index in range(4):
        if word[index] == choosed_word[index]:
            bull += 1
            list_choosed_word.remove(word[index])
        else:
            continue
    for letter in list_choosed_word:
        if letter in choosed_word:
            cow += 1
    return bull, cow

def check_word(word):
    if len(word) == 4 and check_load_words(word) and word in load_words():
        return True
    else:
        return False


def play_game():
    new_offset = None
    while True:
        bullscowsbot.get_updates(new_offset)
        last_update = bullscowsbot.get_last_update()
        last_update_id = last_update['update_id']
        last_chat_text = last_update['message']['text']
        last_chat_id = last_update['message']['chat']['id']
        if last_chat_text == '/start':
            bullscowsbot.send_message(last_chat_id, 'Добро пожаловать в игру "быки и коровы"\nДля старта введите /bullscows и удачи в игре!')
            new_offset = last_update_id + 1
            bullscowsbot.get_updates(new_offset)
        elif last_chat_text == '/bullscows':
            choosed_word = choose_word()
            attempt = 1
            abc_list = []
            used_letters = []
            for i in range(1040, 1072):
                abc_list.append(chr(i))
            while True:
                bullscowsbot.send_message(last_chat_id, "Ваш алфавит\n{0}. \nПожалуйста предположите слово из 4х букв или выйдите /exit.\nВаша попытка №{1}".format(' '.join(abc_list), attempt))
                attempt += 1
                new_offset = last_update_id + 1
                bullscowsbot.get_updates(new_offset)
                last_update = bullscowsbot.get_last_update()
                last_update_id = last_update['update_id']
                last_chat_text = last_update['message']['text']
                last_chat_id = last_update['message']['chat']['id']

                if last_chat_text == '/exit':
                    bullscowsbot.send_message(last_chat_id, "Слово {}\nВы проиграли...".format(choosed_word))
                    break
                elif choosed_word == last_chat_text.lower():
                    bullscowsbot.send_message(last_chat_id, "Вы выиграли!!!")
                    break
                else:
                    if check_word(last_chat_text.lower()):
                        used_letters.extend(list(last_chat_text.upper()))
                        abc_list = list(set(abc_list).difference(set(used_letters)))
                        abc_list.sort()
                        current_score = count_score(last_chat_text.lower(), choosed_word)
                        bullscowsbot.send_message(last_chat_id, "У вас быков {0} коров {1}".format(current_score[0], current_score[1]))
                    else:
                        bullscowsbot.send_message(last_chat_id,"Неверное количество букв или несуществующее слово")
                        attempt -= 1


if __name__ == '__main__':
    word_list = load_words()
    try:
        play_game()
    except KeyboardInterrupt:
        exit()


