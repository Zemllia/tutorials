import vk_api, random
import sqlite3

from vk_api.longpoll import VkLongPoll, VkEventType

vk_session = vk_api.VkApi(token="3c18bd05c8d8f752f91c62c8c93d17b77911c8f90d7678c65ac9812db597e9c9b22cedbe2febff080f3a4")

longpoll = VkLongPoll(vk_session)

vk = vk_session.get_api()

conn = sqlite3.connect("db.db")
c = conn.cursor()

global Random


def random_id():
    Random = 0
    Random += random.randint(0, 1000000000);
    return Random


def check_if_exists(user_id):
    c.execute("SELECT * FROM users WHERE user_id = %d" % user_id)
    result = c.fetchone()
    if result is None:
        return False
    return True


def register_new_user(user_id):
    c.execute("INSERT INTO users(user_id, state) VALUES (%d, '')" % user_id)
    conn.commit()
    c.execute("INSERT INTO user_info(user_id, user_wish) VALUES (%d, 0)" % user_id)
    conn.commit()


def get_user_state(user_id):
    c.execute("SELECT state FROM users WHERE user_id = %d" % user_id)
    result = c.fetchone()
    return result[0]


def get_user_wish(user_id):
    c.execute("SELECT user_wish FROM user_info WHERE user_id = %d" % user_id)
    result = c.fetchone()
    return result[0]


def set_user_wish(user_id, user_wish):
    c.execute("UPDATE user_info SET user_wish = %d WHERE user_id = %d" % (user_wish, user_id))
    conn.commit()


while True:
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:

            if not check_if_exists(event.user_id):
                register_new_user(event.user_id)

            if event.text.lower() == "привет":
                vk.messages.send(
                    user_id=event.user_id,
                    message="Привет!",
                    keyboard=open("keyboard.json", "r", encoding="UTF-8").read(),
                    random_id=random_id()
                )

            elif event.text.lower() == "регистрация":
                if get_user_wish(event.user_id) == 0:
                    set_user_wish(event.user_id, 1)
                    vk.messages.send(
                        user_id=event.user_id,
                        message="Вы успешно зарегистрированы на рассылку!",
                        keyboard=open("keyboard.json", "r", encoding="UTF-8").read(),
                        random_id=random_id()
                    )
                else:
                    set_user_wish(event.user_id, 0)
                    vk.messages.send(
                        user_id=event.user_id,
                        message="Вы успешно удалены из базы!",
                        keyboard=open("keyboard.json", "r", encoding="UTF-8").read(),
                        random_id=random_id()
                    )

            elif event.text.lower() == "ссылка":
                if get_user_wish(event.user_id) == 1:
                    vk.messages.send(
                        user_id=event.user_id,
                        message="https://www.youtube.com/channel/UCCCcDxRXwTE-rtpcyMzxjAA?view_as=subscriber",
                        keyboard=open("keyboard.json", "r", encoding="UTF-8").read(),
                        random_id=random_id()
                    )
                else:
                    vk.messages.send(
                        user_id=event.user_id,
                        message="Вы не зарегистрированы, напишите команду 'Регистрация'",
                        keyboard=open("keyboard.json", "r", encoding="UTF-8").read(),
                        random_id=random_id()
                    )
            else:
                vk.messages.send(
                    user_id=event.user_id,
                    message="Неизвестная команда",
                    keyboard=open("keyboard.json", "r", encoding="UTF-8").read(),
                    random_id=random_id()
                )
