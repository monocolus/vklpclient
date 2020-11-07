# -*- coding: utf-8 -*-
token = ''
id = 
t = ''
o = 0

import time, vk_api, sqlite3, re
import sqlite3 as sql
from requests import get
from datetime import datetime
from random import choice
from random import randint
from vk_api.longpoll import VkLongPoll, VkEventType

vk_session = vk_api.VkApi(token=token)
vk = vk_session.get_api()
longpoll = VkLongPoll(vk_session,wait=0)

conn = sql.connect("dej_"+str(id)+".sqlite")
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS chat(
                                            peer_id INTEGER,
                                            title VARCHAR (500)
                                            )
                                            ''')
conn.commit()
c.execute('''CREATE TABLE IF NOT EXISTS setings(
                                            user_id INTEGER,
                                            text VARCHAR (500),
                                            online VARCHAR (500)
                                            )
                                            ''')
conn.commit()
c.execute('''CREATE TABLE IF NOT EXISTS user(
                                            user_id INTEGER,
                                            name VARCHAR (500)
                                            )
                                            ''')
conn.commit()


c.execute("SELECT * FROM setings WHERE user_id= %s" % id)
result = c.fetchone()
if result is None:
    c.execute("INSERT INTO setings(user_id, text ,online) VALUES (?, ?, ?)", (int(id), t, o)); conn.commit()
pass

adm = (id)

def check_adm(User_id):
    c.execute("SELECT * FROM user WHERE user_id = %d" % int(User_id))
    result = c.fetchone()
    if result is None:
        return False
    return True

def check_adm1(adm):
    c.execute("SELECT * FROM user WHERE user_id = %d" % int(adm))
    result = c.fetchone()
    if result is None:
        return False
    return True

def check_chat(Peer_id):
    c.execute("SELECT * FROM chat WHERE peer_id = %d" % int(Peer_id))
    result = c.fetchone()
    if result is None:
        return False
    return True

def Chat_num():
    num = len(c.execute("SELECT * FROM chat").fetchall())
    return num

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        adm = id
        m_id = event.message_id
        Peer_id = event.peer_id
        
        text = event.text.lower()
        text2 = re.split(r' ', text)
        User_id = event.user_id

        if text2[0] == '.м +чат' and User_id == adm and check_chat(Peer_id) == False:
            Title = vk.messages.getConversationsById(peer_ids=Peer_id).get('items')[0]['chat_settings']['title']
            c.execute("INSERT INTO chat(peer_id, title) VALUES (?, ?)", (int(Peer_id), Title)); conn.commit()
            vk.messages.edit(peer_id=event.peer_id,message='✅ Чат добавлен!',message_id=m_id)
        try:
            User_id = event.user_id
            text2 = re.split(r' ', event.text.lower())

            if not check_adm1(adm):
                Name = vk.account.getProfileInfo()['first_name'] + ' ' + vk.account.getProfileInfo()['last_name']
                c.execute("INSERT INTO user(user_id, name) VALUES (?, ?)", (int(adm), Name)); conn.commit()

            elif not check_adm(User_id):
                pass
            
            else:
                if text2[0] == '.м +дов' or text2[0] == '+довереный' or text2[0] == '+доверенный' and User_id == adm:
                    Use_id = re.split(r'vk.com/', text2[1])
                    try:
                        id1 = vk.users.get(user_ids = (Use_id))[0]['id']
                        Name = vk.users.get(user_ids = (id1))[0]['first_name']+' '+vk.users.get(user_ids = (id1))[0]['last_name']
                        if not check_adm(id1):
                            c.execute("INSERT INTO user(user_id, name) VALUES (?, ?)", (int(id1), Name)); conn.commit()
                            vk.messages.edit(peer_id=event.peer_id,message='✅ Пользователь @id'+str(id1)+'('+str(Name)+') добавлен в список доверенных!',message_id=m_id)
                        else:
                            vk.messages.edit(peer_id=event.peer_id,message='🌚 Пользователь @id'+str(id1)+'('+str(Name)+') уже в списке доверенных!',message_id=m_id)
                    except (IndexError,vk_api.exceptions.ApiError):
                        vk.messages.edit(peer_id=event.peer_id,message='😖 Неверный ID',message_id=m_id)


                elif text2[0] == '.м -дов' or text2[0] == '-довереный' or text2[0] == '-доверенный' and User_id == adm:
                    Use_id = re.split(r'vk.com/', text2[1])
                    try:
                        id1 = vk.users.get(user_ids = (Use_id))[0]['id']
                        Name = vk.users.get(user_ids = (id1))[0]['first_name']+' '+vk.users.get(user_ids = (id1))[0]['last_name']
                        if not check_adm(id1):
                            vk.messages.edit(peer_id=event.peer_id,message='🤡 Пользователь @id'+str(id1)+'('+str(Name)+') уже удалён из доверенных!',message_id=m_id)
                        else:
                            c.execute('DELETE FROM user WHERE user_id = "{}"'.format(id1))
                            conn.commit()
                            vk.messages.edit(peer_id=event.peer_id,message='✅ Пользователь @id'+str(id1)+'('+str(Name)+') удалён из доверенных!',message_id=m_id)
                    except (IndexError,vk_api.exceptions.ApiError):
                        vk.messages.edit(peer_id=event.peer_id,message='😖 Неверный ID',message_id=m_id)
                        
                elif text2[0] == '.м +чс' and User_id == adm:
                    try:
                        Use_id = re.split(r'vk.com/', text2[1])
                        ban_id = vk.users.get(user_ids = (Use_id))[0]['id']
                        Name = vk.users.get(user_ids = (ban_id))[0]['first_name']+' '+vk.users.get(user_ids = (ban_id))[0]['last_name']
                        vk.account.ban(owner_id=(ban_id))
                        vk.messages.edit(peer_id=event.peer_id,message='🤡 Пользователь @id'+str(ban_id)+'('+str(Name)+') добавлен в чс',message_id=m_id)
                    except:
                        vk.messages.edit(peer_id=event.peer_id,message='Возникла ошибка при добавлении в чс!',message_id=m_id)
                        
                elif text2[0] == '.м -чс' and User_id == adm:
                    try:
                        Use_id = re.split(r'vk.com/', text2[1])
                        ban_id = vk.users.get(user_ids = (Use_id))[0]['id']
                        Name = vk.users.get(user_ids = (ban_id))[0]['first_name']+' '+vk.users.get(user_ids = (ban_id))[0]['last_name']
                        vk.account.unban(owner_id=(ban_id))
                        vk.messages.edit(peer_id=event.peer_id,message='🤡 Пользователь @id'+str(ban_id)+'('+str(Name)+') удалён из чс',message_id=m_id)
                    except:
                        vk.messages.edit(peer_id=event.peer_id,message='Возникла ошибка при удалении из чс!',message_id=m_id)

                elif text2[0] == '.м +др' and User_id == adm:
                    try:
                        Use_id = re.split(r'vk.com/', text2[1])
                        add_id = vk.users.get(user_ids = (Use_id))[0]['id']
                        Name = vk.users.get(user_ids = (add_id))[0]['first_name']+' '+vk.users.get(user_ids = (add_id))[0]['last_name']
                        a = vk.friends.add(user_id=(add_id))
                        if a == 1 or a == 4:
                            msge = '🤡 Пользователю @id'+str(add_id)+'('+str(Name)+') заявка отправлена'
                        elif a == 2:
                            msge = '🤡 Пользователь @id'+str(add_id)+'('+str(Name)+') добавлен'  
                        vk.messages.edit(peer_id=event.peer_id,message=(msge),message_id=m_id)
                    except:
                        vk.messages.edit(peer_id=event.peer_id,message='Возникла ошибка при добавлении.',message_id=m_id)
                
                elif text2[0] == '.м -др' and User_id == adm:
                    try:
                        Use_id = re.split(r'vk.com/', text2[1])
                        add_id = vk.users.get(user_ids = (Use_id))[0]['id']
                        Name = vk.users.get(user_ids = (add_id))[0]['first_name']+' '+vk.users.get(user_ids = (add_id))[0]['last_name']
                        a = vk.friends.delete(user_id=(add_id))
                        if a.get('friend_deleted') == 1:
                            msge = '🤡 Пользователь @id'+str(add_id)+'('+str(Name)+') был удалён из друзей'
                        elif a.get('out_request_deleted') == 1:
                            msge = '🤡 Отклонена исходящая заявка пользователю @id'+str(add_id)+'('+str(Name)+')'
                        elif a.get('in_request_deleted') == 1:
                            msge = '🤡 Отклонена входящая заявка от пользователя @id'+str(add_id)+'('+str(Name)+')'
                        vk.messages.edit(peer_id=event.peer_id,message=(msge),message_id=m_id)
                    except:
                        vk.messages.edit(peer_id=event.peer_id,message='Возникла ошибка при удалении из друзей.',message_id=m_id)

                elif text2[0] == '.м +чат' and User_id == adm and check_chat(Peer_id) == False:
                    Title = vk.messages.getConversationsById(peer_ids=Peer_id).get('items')[0]['chat_settings']['title']
                    c.execute("INSERT INTO chat(peer_id, title) VALUES (?, ?)", (int(Peer_id), Title)); conn.commit()
                    vk.messages.edit(peer_id=event.peer_id,message='✅ Чат добавлен!',message_id=m_id)
                    
                elif text2[0] == '.м -чат' and User_id == adm and check_chat(Peer_id) == True:
                    c.execute('DELETE FROM chat WHERE peer_id = "{}"'.format(Peer_id))
                    conn.commit()
                    vk.messages.edit(peer_id=event.peer_id,message='🤡 Чат удалён ^-^',message_id=m_id)
                    
                elif text2[0] == '-' or text2[0] == '$s' or text2[0] == '.м' and check_chat(Peer_id) == True:
                    if text2[1] == 'круг' or text2[1] == 'circle':
                        a = vk.messages.send(peer_id=Peer_id,message="💕🐾\n🐾 💕",random_id=0)
                        time.sleep(2)
                        vk.messages.edit(peer_id=Peer_id,message="🐾 💕\n💕🐾",message_id=a)
                        time.sleep(2)
                        vk.messages.edit(peer_id=Peer_id,message="💕🐾\n🐾 💕",message_id=a)
                        time.sleep(2)
                        vk.messages.edit(peer_id=Peer_id,message="❤",message_id=a)

                elif text2[0] == '-' or text2[0] == '$s' or text2[0] == '.м' and check_chat(Peer_id) == True:
                    if text2[1] == 'хуй' or text2[1] == 'хуй':
                        a = vk.messages.send(peer_id=Peer_id,message="💕",random_id=0)
                        time.sleep(2)
                        vk.messages.edit(peer_id=Peer_id,message="💕",message_id=a)
                        time.sleep(2)
                        vk.messages.edit(peer_id=Peer_id,message="💕",message_id=a)
                        time.sleep(2)
                        vk.messages.edit(peer_id=Peer_id,message="💕хуй💕",message_id=a)        
                        
                elif text2[0] == '-' or text2[0] == '$s' or text2[0] == '.м' and check_chat(Peer_id) == True:
                    if text2[1] == 'инфо' or text2[1] == 'шабы':
                        a = vk.messages.send(peer_id=Peer_id,message="[ Подключение... ]",random_id=0)
                        P_time = datetime.now().timestamp()
                        requests = get(f'https://api.vk.com/method/messages.getConversations?count=20?filter=all?v=5.89&access_token={token}')
                        Vk_time = datetime.now().timestamp()
                        delta = round(Vk_time - P_time, 2)
                        today = datetime.datetime.today()
                        time = today.strftime("Дата: %m/%d/%Y / Время: %H:%M")
                        time.sleep(2)
                        vk.messages.edit(peer_id=Peer_id,message="+---------------------+ Основаная информация +---------------------+\n• LP Клиент от @id580060311 (Вячеслав Monocolus 🍺)\n• Время ответа: '{delta}'ms 🌐\n• Твой айди: {id} 🆔\n• Твоё время и дата: '{time}' 🕗\n• Твоё имя, фамилия: '+str(users.get_first_name)'👤\n• Имя беседы: '+str(event.chat_name)+' ❎\n• ID беседы: '+str(event.chat_id)+' 💾\n+---------------------+ Сигналы +---------------------+\n• .м шабы (выводит все доступные анимированные шаблоны) 📚\n• .м +дов | -дов (добавляет либо удаляет пользователя в доверенных) 🚹\n• .м +чат | -чат (добавляет или удаляет чат из рабочих) 📩\n• .м +чс | -чс (добавляет или удаляет чс пользователя)🚫\n• .м +др | -др (добавляет или удаляет пользователя из друзей) 👤",message_id=a)
                        
                    elif text2[1] == '.м шабы' or text2[1] == 'signals':
                        P_time = datetime.now().timestamp()
                        requests = get(f'https://api.vk.com/method/messages.getConversations?count=20?filter=all?v=5.89&access_token={token}')
                        Vk_time = datetime.now().timestamp()
                        delta = round(Vk_time - P_time, 2)
                        today = datetime.datetime.today()
                        time = today.strftime("Дата: %m/%d/%Y / Время: %H:%M")
                        a = vk.messages.send(peer_id=Peer_id,message="[ Подключение... ]",random_id=0)
                        time.sleep(2)
                        vk.messages.edit(peer_id=Peer_id,message="+---------------------+ Шаблоны +---------------------+\n• .м пнуть (один человек пинает второго) 👟\n• .м луна (жёлтая луна и тёмная) 🌚🌝\n• .м взрыв (взрыв планеты) 🌎\n• .м полиция (полиция ловин преступника, три варианта) 🚓\n• .м ку (приветствие) 👋\n• .м удар (удар в лицо) 🤜\n• .м отчёт (таймер от 1 до 10) 🔟",message_id=a)

                    elif text2[1] == 'пнуть' or text2[1] == 'kick':
                        a = vk.messages.send(peer_id=Peer_id,message="😑👟      🤔",random_id=0)
                        time.sleep(2)
                        vk.messages.edit(peer_id=Peer_id,message="😑 👟     🤔",message_id=a)
                        time.sleep(2)
                        vk.messages.edit(peer_id=Peer_id,message="😑  👟    🤔",message_id=a)
                        time.sleep(2)
                        vk.messages.edit(peer_id=Peer_id,message="😑   👟   🤔",message_id=a)
                        time.sleep(2)
                        vk.messages.edit(peer_id=Peer_id,message="😑    👟  🤔",message_id=a)
                        time.sleep(2)
                        vk.messages.edit(peer_id=Peer_id,message="😑     👟 🤔",message_id=a)
                        time.sleep(2)
                        vk.messages.edit(peer_id=Peer_id,message="😑      👟🤔",message_id=a)
                        time.sleep(2)
                        vk.messages.edit(peer_id=Peer_id,message="😏     👟🤕",message_id=a)
                        
                    elif text2[1] == 'отчёт' or text2[1] == 'kick':
                        a = vk.messages.send(peer_id=Peer_id,message=" #️⃣  Внимание! Через 3 секунды будет счёт от 1️⃣  до 🔟",random_id=0)
                        time.sleep(3)
                        vk.messages.edit(peer_id=Peer_id,message="Один 1️⃣  ",message_id=a)
                        time.sleep(1)
                        vk.messages.edit(peer_id=Peer_id,message="Два 2️⃣ ",message_id=a)
                        time.sleep(1)
                        vk.messages.edit(peer_id=Peer_id,message="Три 3️⃣ ",message_id=a)
                        time.sleep(1)
                        vk.messages.edit(peer_id=Peer_id,message="Четыре 4️⃣ ",message_id=a)
                        time.sleep(1)
                        vk.messages.edit(peer_id=Peer_id,message="Пять 5️⃣ ",message_id=a)
                        time.sleep(1)
                        vk.messages.edit(peer_id=Peer_id,message="Шесть 6️⃣ ",message_id=a)
                        time.sleep(1)
                        vk.messages.edit(peer_id=Peer_id,message="Семь 7️⃣ ",message_id=a)
                        time.sleep(1)
                        vk.messages.edit(peer_id=Peer_id,message="Восемь 8️⃣ ",message_id=a)
                        time.sleep(1)
                        vk.messages.edit(peer_id=Peer_id,message="Девять 9️⃣ ",message_id=a)
                        time.sleep(1)
                        vk.messages.edit(peer_id=Peer_id,message="Десять 🔟 ",message_id=a)
                   
                    elif text2[1] == 'удар' or text2[1] == 'boom':
                        a = vk.messages.send(peer_id=Peer_id,message="😔     🤣",random_id=0)
                        time.sleep(2)
                        vk.messages.edit(peer_id=Peer_id,message="😤     😂",message_id=a)
                        time.sleep(2)
                        vk.messages.edit(peer_id=Peer_id,message="😡  🤜  🤣",message_id=a)
                        time.sleep(2)
                        vk.messages.edit(peer_id=Peer_id,message="😡   🤜 😂",message_id=a)
                        time.sleep(2)
                        vk.messages.edit(peer_id=Peer_id,message="😡    🤜😣",message_id=a)
                        time.sleep(2)
                        vk.messages.edit(peer_id=Peer_id,message="😌     😵",message_id=a)
                        time.sleep(2)
                        vk.messages.edit(peer_id=Peer_id,message="😌🤜     🤕",message_id=a)

                    elif text2[1] == 'луна' or text2[1] == 'train':                   
                        a = vk.messages.send(peer_id=Peer_id,message="🌚🌝",random_id=0)
                        time.sleep(2)
                        vk.messages.edit(peer_id=Peer_id,message="🌚🌝🌚🌝🌚🌝🌚🌝",message_id=a)
                        time.sleep(1)
                        vk.messages.edit(peer_id=Peer_id,message="🌝🌚🌝🌚🌝🌚🌝🌚",message_id=a)
                        time.sleep(1)
                        vk.messages.edit(peer_id=Peer_id,message="🌚🌝🌚🌝🌚🌝🌚🌝",message_id=a)
                        time.sleep(1)
                        vk.messages.edit(peer_id=Peer_id,message="🌝🌚🌝🌚🌝🌚🌝🌚",message_id=a)
                        time.sleep(1)
                        vk.messages.edit(peer_id=Peer_id,message="🌚🌝🌚🌝🌚🌝🌚🌝",message_id=a)
                        time.sleep(1)
                        vk.messages.edit(peer_id=Peer_id,message="🌝🌚🌝🌚🌝🌚🌝🌚",message_id=a)
                        time.sleep(1)
                        vk.messages.edit(peer_id=Peer_id,message="🌚🌝🌚🌝🌚🌝🌚🌝",message_id=a)
                        time.sleep(1)
                        vk.messages.edit(peer_id=Peer_id,message="🌝🌚🌝🌚🌝🌚🌝🌚",message_id=a)
                        time.sleep(1)
                        vk.messages.edit(peer_id=Peer_id,message="🌚🌝🌚🌝🌚🌝🌚🌝",message_id=a)
                        time.sleep(1)
                        vk.messages.edit(peer_id=Peer_id,message="🌝🌚🌝🌚🌝🌚🌝🌚",message_id=a)
                        time.sleep(1)
                        vk.messages.edit(peer_id=Peer_id,message="🌚🌝🌚🌝🌚🌝🌚🌝",message_id=a)
                        time.sleep(1)
                        vk.messages.edit(peer_id=Peer_id,message="🌝🌚🌝🌚🌝🌚🌝🌚",message_id=a)
                        time.sleep(1)
                        vk.messages.edit(peer_id=Peer_id,message="🌚🌝🌚🌝🌚🌝🌚🌝",message_id=a)
                        time.sleep(1)
                        vk.messages.edit(peer_id=Peer_id,message="🌝🌚🌝🌚🌝🌚🌝🌚",message_id=a)
                        time.sleep(1)
                        vk.messages.edit(peer_id=Peer_id,message="🌚🌝🌚🌝🌚🌝🌚🌝",message_id=a)
                        time.sleep(1)
                        vk.messages.edit(peer_id=Peer_id,message="🌝🌚🌝🌚🌝🌚🌝🌚",message_id=a)

                    elif text2[1] == 'ф' or text2[1] == 'f':
                        ra = randint(1, 3)
                        if ra == 1:
                            a = vk.messages.send(peer_id=Peer_id,message="🌕🌗🌑🌑🌑🌑🌑🌓\n🌕🌗🌑🌑🌑🌑🌑🌕\n🌕🌗🌑🌓🌕🌕🌕🌕\n🌕🌗🌑🌓🌕🌕🌕🌕\n🌕🌗🌑🌑🌑🌑🌓🌕\n🌕🌗🌑🌑🌑🌑🌕🌕\n🌕🌗🌑🌓🌕🌕🌕🌕\n🌕🌗🌑🌓🌕🌕🌕🌕\n🌕🌗🌑🌓🌕🌕🌕🌕",random_id=0)
                            time.sleep(2)
                            vk.messages.edit(peer_id=Peer_id,message="🌗🌑🌑🌑🌑🌑🌓🌕\n🌗🌑🌑🌑🌑🌑🌕🌕\n🌗🌑🌓🌕🌕🌕🌕🌕\n🌗🌑🌓🌕🌕🌕🌕🌕\n🌗🌑🌑🌑🌑🌓🌕🌕\n🌗🌑🌑🌑🌑🌕🌕🌕\n🌗🌑🌓🌕🌕🌕🌕🌕\n🌗🌑🌓🌕🌕🌕🌕🌕\n🌗🌑🌓🌕🌕🌕🌕🌕",message_id=a)
                            time.sleep(2)
                            vk.messages.edit(peer_id=Peer_id,message="🌑🌑🌑🌑🌑🌓🌕🌗\n🌑🌑🌑🌑🌑🌕🌕🌗\n🌑🌓🌕🌕🌕🌕🌕🌗\n🌑🌓🌕🌕🌕🌕🌕🌗\n🌑🌑🌑🌑🌓🌕🌕🌗\n🌑🌑🌑🌑🌕🌕🌕🌗\n🌑🌓🌕🌕🌕🌕🌕🌗\n🌑🌓🌕🌕🌕🌕🌕🌗\n🌑🌓🌕🌕🌕🌕🌕🌗",message_id=a)
                            time.sleep(2)
                            vk.messages.edit(peer_id=Peer_id,message="🌑🌑🌑🌑🌓🌕🌗🌑\n🌑🌑🌑🌑🌕🌕🌗🌑\n🌓🌕🌕🌕🌕🌕🌗🌑\n🌓🌕🌕🌕🌕🌕🌗🌑\n🌑🌑🌑🌓🌕🌕🌗🌑\n🌑🌑🌑🌕🌕🌕🌗🌑\n🌓🌕🌕🌕🌕🌕🌗🌑\n🌓🌕🌕🌕🌕🌕🌗🌑\n🌓🌕🌕🌕🌕🌕🌗🌑",message_id=a)
                            time.sleep(2)
                            vk.messages.edit(peer_id=Peer_id,message="🌑🌑🌑🌓🌕🌗🌑🌑\n🌑🌑🌑🌕🌕🌗🌑🌑\n🌕🌕🌕🌕🌕🌗🌑🌓\n🌕🌕🌕🌕🌕🌗🌑🌓\n🌑🌑🌓🌕🌕🌗🌑🌑\n🌑🌑🌕🌕🌕🌗🌑🌑\n🌕🌕🌕🌕🌕🌗🌑🌓\n🌕🌕🌕🌕🌕🌗🌑🌓\n🌕🌕🌕🌕🌕🌗🌑🌓",message_id=a)
                            time.sleep(2)
                            vk.messages.edit(peer_id=Peer_id,message="🌑🌑🌓🌕🌗🌑🌑🌑\n🌑🌑🌕🌕🌗🌑🌑🌑\n🌕🌕🌕🌕🌗🌑🌓🌕\n🌕🌕🌕🌕🌗🌑🌓🌕\n🌑🌓🌕🌕🌗🌑🌑🌑\n🌑🌕🌕🌕🌗🌑🌑🌑\n🌕🌕🌕🌕🌗🌑🌓🌕\n🌕🌕🌕🌕🌗🌑🌓🌕\n🌕🌕🌕🌕🌗🌑🌓🌕",message_id=a)
                            time.sleep(2)
                            vk.messages.edit(peer_id=Peer_id,message="🌑🌓🌕🌗🌑🌑🌑🌑\n🌑🌕🌕🌗🌑🌑🌑🌑\n🌕🌕🌕🌗🌑🌓🌕🌕\n🌕🌕🌕🌗🌑🌓🌕🌕\n🌓🌕🌕🌗🌑🌑🌑🌑\n🌕🌕🌕🌗🌑🌑🌑🌑\n🌕🌕🌕🌗🌑🌓🌕🌕\n🌕🌕🌕🌗🌑🌓🌕🌕\n🌕🌕🌕🌗🌑🌓🌕🌕",message_id=a)
                            time.sleep(2)
                            vk.messages.edit(peer_id=Peer_id,message="🌓🌕🌗🌑🌑🌑🌑🌑\n🌕🌕🌗🌑🌑🌑🌑🌑\n🌕🌕🌗🌑🌓🌕🌕🌕\n🌕🌕🌗🌑🌓🌕🌕🌕\n🌕🌕🌗🌑🌑🌑🌑🌓\n🌕🌕🌗🌑🌑🌑🌑🌕\n🌕🌕🌗🌑🌓🌕🌕🌕\n🌕🌕🌗🌑🌓🌕🌕🌕\n🌕🌕🌗🌑🌓🌕🌕🌕",message_id=a)
                            time.sleep(2)
                            vk.messages.edit(peer_id=Peer_id,message="🌕🌗🌑🌑🌑🌑🌑🌓\n🌕🌗🌑🌑🌑🌑🌑🌕\n🌕🌗🌑🌓🌕🌕🌕🌕\n🌕🌗🌑🌓🌕🌕🌕🌕\n🌕🌗🌑🌑🌑🌑🌓🌕\n🌕🌗🌑🌑🌑🌑🌕🌕\n🌕🌗🌑🌓🌕🌕🌕🌕\n🌕🌗🌑🌓🌕🌕🌕🌕\n🌕🌗🌑🌓🌕🌕🌕🌕\nV1",message_id=a)
                        elif ra == 2:
                            a = vk.messages.send(peer_id=Peer_id,message="🌕🌗🌑🌑🌑🌑🌑🌓\n🌕🌗🌑🌑🌑🌑🌑🌕\n🌕🌗🌑🌓🌕🌕🌕🌕\n🌕🌗🌑🌓🌕🌕🌕🌕\n🌕🌗🌑🌑🌑🌑🌓🌕\n🌕🌗🌑🌑🌑🌑🌕🌕\n🌕🌗🌑🌓🌕🌕🌕🌕\n🌕🌗🌑🌓🌕🌕🌕🌕\n🌕🌗🌑🌓🌕🌕🌕🌕",random_id=0)
                            time.sleep(2)
                            vk.messages.edit(peer_id=Peer_id,message="🌕🌗🌑🌑🌑🌑🌑🌕\n🌕🌗🌑🌓🌕🌕🌕🌕\n🌕🌗🌑🌓🌕🌕🌕🌕\n🌕🌗🌑🌑🌑🌑🌓🌕\n🌕🌗🌑🌑🌑🌑🌕🌕\n🌕🌗🌑🌓🌕🌕🌕🌕\n🌕🌗🌑🌓🌕🌕🌕🌕\n🌕🌗🌑🌓🌕🌕🌕🌕\n🌕🌗🌑🌑🌑🌑🌑🌓",message_id=a)
                            time.sleep(3)
                            vk.messages.edit(peer_id=Peer_id,message="🌕🌗🌑🌓🌕🌕🌕🌕\n🌕🌗🌑🌓🌕🌕🌕🌕\n🌕🌗🌑🌑🌑🌑🌓🌕\n🌕🌗🌑🌑🌑🌑🌕🌕\n🌕🌗🌑🌓🌕🌕🌕🌕\n🌕🌗🌑🌓🌕🌕🌕🌕\n🌕🌗🌑🌓🌕🌕🌕🌕\n🌕🌗🌑🌑🌑🌑🌑🌓\n🌕🌗🌑🌑🌑🌑🌑🌕",message_id=a)
                            time.sleep(3)
                            vk.messages.edit(peer_id=Peer_id,message="🌕🌗🌑🌓🌕🌕🌕🌕\n🌕🌗🌑🌑🌑🌑🌓🌕\n🌕🌗🌑🌑🌑🌑🌕🌕\n🌕🌗🌑🌓🌕🌕🌕🌕\n🌕🌗🌑🌓🌕🌕🌕🌕\n🌕🌗🌑🌓🌕🌕🌕🌕\n🌕🌗🌑🌑🌑🌑🌑🌓\n🌕🌗🌑🌑🌑🌑🌑🌕\n🌕🌗🌑🌓🌕🌕🌕🌕",message_id=a)
                            time.sleep(2)
                            vk.messages.edit(peer_id=Peer_id,message="🌕🌗🌑🌑🌑🌑🌓🌕\n🌕🌗🌑🌑🌑🌑🌕🌕\n🌕🌗🌑🌓🌕🌕🌕🌕\n🌕🌗🌑🌓🌕🌕🌕🌕\n🌕🌗🌑🌓🌕🌕🌕🌕\n🌕🌗🌑🌑🌑🌑🌑🌓\n🌕🌗🌑🌑🌑🌑🌑🌕\n🌕🌗🌑🌓🌕🌕🌕🌕\n🌕🌗🌑🌓🌕🌕🌕🌕",message_id=a)
                            time.sleep(2)
                            vk.messages.edit(peer_id=Peer_id,message="🌕🌗🌑🌑🌑🌑🌕🌕\n🌕🌗🌑🌓🌕🌕🌕🌕\n🌕🌗🌑🌓🌕🌕🌕🌕\n🌕🌗🌑🌓🌕🌕🌕🌕\n🌕🌗🌑🌑🌑🌑🌑🌓\n🌕🌗🌑🌑🌑🌑🌑🌕\n🌕🌗🌑🌓🌕🌕🌕🌕\n🌕🌗🌑🌓🌕🌕🌕🌕\n🌕🌗🌑🌑🌑🌑🌓🌕",message_id=a)
                            time.sleep(3)
                            vk.messages.edit(peer_id=Peer_id,message="🌕🌗🌑🌓🌕🌕🌕🌕\n🌕🌗🌑🌓🌕🌕🌕🌕\n🌕🌗🌑🌓🌕🌕🌕🌕\n🌕🌗🌑🌑🌑🌑🌑🌓\n🌕🌗🌑🌑🌑🌑🌑🌕\n🌕🌗🌑🌓🌕🌕🌕🌕\n🌕🌗🌑🌓🌕🌕🌕🌕\n🌕🌗🌑🌑🌑🌑🌓🌕\n🌕🌗🌑🌑🌑🌑🌕🌕",message_id=a)
                            time.sleep(2)
                            vk.messages.edit(peer_id=Peer_id,message="🌕🌗🌑🌓🌕🌕🌕🌕\n🌕🌗🌑🌓🌕🌕🌕🌕\n🌕🌗🌑🌑🌑🌑🌑🌓\n🌕🌗🌑🌑🌑🌑🌑🌕\n🌕🌗🌑🌓🌕🌕🌕🌕\n🌕🌗🌑🌓🌕🌕🌕🌕\n🌕🌗🌑🌑🌑🌑🌓🌕\n🌕🌗🌑🌑🌑🌑🌕🌕\n🌕🌗🌑🌓🌕🌕🌕🌕",message_id=a)
                            time.sleep(2)
                            vk.messages.edit(peer_id=Peer_id,message="🌕🌗🌑🌓🌕🌕🌕🌕\n🌕🌗🌑🌑🌑🌑🌑🌓\n🌕🌗🌑🌑🌑🌑🌑🌕\n🌕🌗🌑🌓🌕🌕🌕🌕\n🌕🌗🌑🌓🌕🌕🌕🌕\n🌕🌗🌑🌑🌑🌑🌓🌕\n🌕🌗🌑🌑🌑🌑🌕🌕\n🌕🌗🌑🌓🌕🌕🌕🌕\n🌕🌗🌑🌓🌕🌕🌕🌕",message_id=a)
                            time.sleep(2)
                            vk.messages.edit(peer_id=Peer_id,message="🌕🌗🌑🌑🌑🌑🌑🌓\n🌕🌗🌑🌑🌑🌑🌑🌕\n🌕🌗🌑🌓🌕🌕🌕🌕\n🌕🌗🌑🌓🌕🌕🌕🌕\n🌕🌗🌑🌑🌑🌑🌓🌕\n🌕🌗🌑🌑🌑🌑🌕🌕\n🌕🌗🌑🌓🌕🌕🌕🌕\n🌕🌗🌑🌓🌕🌕🌕🌕\n🌕🌗🌑🌓🌕🌕🌕🌕\nV2",message_id=a)
                        elif ra == 3:
                            a = vk.messages.send(peer_id=Peer_id,message="🌕🌗🌑🌑🌑🌑🌑🌓\n🌕🌗🌑🌑🌑🌑🌑🌕\n🌕🌗🌑🌓🌕🌕🌕🌕\n🌕🌗🌑🌓🌕🌕🌕🌕\n🌕🌗🌑🌑🌑🌑🌓🌕\n🌕🌗🌑🌑🌑🌑🌕🌕\n🌕🌗🌑🌓🌕🌕🌕🌕\n🌕🌗🌑🌓🌕🌕🌕🌕\n🌕🌗🌑🌓🌕🌕🌕🌕",random_id=0)
                            time.sleep(2)
                            vk.messages.edit(peer_id=Peer_id,message="🌕🌗🌑🌑🌑🌑🌑🌕\n🌕🌗🌑🌓🌕🌕🌕🌕\n🌕🌗🌑🌓🌕🌕🌕🌕\n🌕🌗🌑🌑🌑🌑🌓🌕\n🌕🌗🌑🌑🌑🌑🌕🌕\n🌕🌗🌑🌓🌕🌕🌕🌕\n🌕🌗🌑🌓🌕🌕🌕🌕\n🌕🌗🌑🌓🌕🌕🌕🌕\n🌕🌗🌑🌑🌑🌑🌑🌓",message_id=a)
                            time.sleep(3)
                            vk.messages.edit(peer_id=Peer_id,message="🌕🌕🌗🌑🌑🌑🌑🌑\n🌕🌕🌗🌑🌓🌕🌕🌕\n🌕🌕🌗🌑🌓🌕🌕🌕\n🌕🌕🌗🌑🌑🌑🌑🌓\n🌕🌕🌗🌑🌑🌑🌑🌕\n🌕🌕🌗🌑🌓🌕🌕🌕\n🌕🌕🌗🌑🌓🌕🌕🌕\n🌕🌕🌗🌑🌓🌕🌕🌕\n🌓🌕🌗🌑🌑🌑🌑🌑",message_id=a)
                            time.sleep(2)
                            vk.messages.edit(peer_id=Peer_id,message="🌕🌕🌕🌗🌑🌓🌕🌕\n🌕🌕🌕🌗🌑🌓🌕🌕\n🌓🌕🌕🌗🌑🌑🌑🌑\n🌕🌕🌕🌗🌑🌑🌑🌑\n🌕🌕🌕🌗🌑🌓🌕🌕\n🌕🌕🌕🌗🌑🌓🌕🌕\n🌕🌕🌕🌗🌑🌓🌕🌕\n🌑🌓🌕🌗🌑🌑🌑🌑\n🌑🌕🌕🌗🌑🌑🌑🌑",message_id=a)
                            time.sleep(2)
                            vk.messages.edit(peer_id=Peer_id,message="🌕🌕🌕🌕🌗🌑🌓🌕\n🌑🌓🌕🌕🌗🌑🌑🌑\n🌑🌕🌕🌕🌗🌑🌑🌑\n🌕🌕🌕🌕🌗🌑🌓🌕\n🌕🌕🌕🌕🌗🌑🌓🌕\n🌕🌕🌕🌕🌗🌑🌓🌕\n🌑🌑🌓🌕🌗🌑🌑🌑\n🌑🌑🌕🌕🌗🌑🌑🌑\n🌕🌕🌕🌕🌗🌑🌓🌕",message_id=a)
                            time.sleep(3)
                            vk.messages.edit(peer_id=Peer_id,message="🌑🌑🌓🌕🌕🌗🌑🌑\n🌑🌑🌕🌕🌕🌗🌑🌑\n🌕🌕🌕🌕🌕🌗🌑🌓\n🌕🌕🌕🌕🌕🌗🌑🌓\n🌕🌕🌕🌕🌕🌗🌑🌓\n🌑🌑🌑🌓🌕🌗🌑🌑\n🌑🌑🌑🌕🌕🌗🌑🌑\n🌕🌕🌕🌕🌕🌗🌑🌓\n🌕🌕🌕🌕🌕🌗🌑🌓",message_id=a)
                            time.sleep(2)
                            vk.messages.edit(peer_id=Peer_id,message="🌑🌑🌑🌕🌕🌕🌗🌑\n🌓🌕🌕🌕🌕🌕🌗🌑\n🌓🌕🌕🌕🌕🌕🌗🌑\n🌓🌕🌕🌕🌕🌕🌗🌑\n🌑🌑🌑🌑🌓🌕🌗🌑\n🌑🌑🌑🌑🌕🌕🌗🌑\n🌓🌕🌕🌕🌕🌕🌗🌑\n🌓🌕🌕🌕🌕🌕🌗🌑\n🌑🌑🌑🌓🌕🌕🌗🌑",message_id=a)
                            time.sleep(2)
                            vk.messages.edit(peer_id=Peer_id,message="🌑🌓🌕🌕🌕🌕🌕🌗\n🌑🌓🌕🌕🌕🌕🌕🌗\n🌑🌓🌕🌕🌕🌕🌕🌗\n🌑🌑🌑🌑🌑🌓🌕🌗\n🌑🌑🌑🌑🌑🌕🌕🌗\n🌑🌓🌕🌕🌕🌕🌕🌗\n🌑🌓🌕🌕🌕🌕🌕🌗\n🌑🌑🌑🌑🌓🌕🌕🌗\n🌑🌑🌑🌑🌕🌕🌕🌗",message_id=a)
                            time.sleep(3)
                            vk.messages.edit(peer_id=Peer_id,message="🌗🌑🌓🌕🌕🌕🌕🌕\n🌗🌑🌓🌕🌕🌕🌕🌕\n🌗🌑🌑🌑🌑🌑🌓🌕\n🌗🌑🌑🌑🌑🌑🌕🌕\n🌗🌑🌓🌕🌕🌕🌕🌕\n🌗🌑🌓🌕🌕🌕🌕🌕\n🌗🌑🌑🌑🌑🌓🌕🌕\n🌗🌑🌑🌑🌑🌕🌕🌕\n🌗🌑🌓🌕🌕🌕🌕🌕",message_id=a)
                            time.sleep(2)
                            vk.messages.edit(peer_id=Peer_id,message="🌕🌗🌑🌓🌕🌕🌕🌕\n🌕🌗🌑🌑🌑🌑🌑🌓\n🌕🌗🌑🌑🌑🌑🌑🌕\n🌕🌗🌑🌓🌕🌕🌕🌕\n🌕🌗🌑🌓🌕🌕🌕🌕\n🌕🌗🌑🌑🌑🌑🌓🌕\n🌕🌗🌑🌑🌑🌑🌕🌕\n🌕🌗🌑🌓🌕🌕🌕🌕\n🌕🌗🌑🌓🌕🌕🌕🌕",message_id=a)
                            time.sleep(3)
                            vk.messages.edit(peer_id=Peer_id,message="🌕🌗🌑🌑🌑🌑🌑🌓\n🌕🌗🌑🌑🌑🌑🌑🌕\n🌕🌗🌑🌓🌕🌕🌕🌕\n🌕🌗🌑🌓🌕🌕🌕🌕\n🌕🌗🌑🌑🌑🌑🌓🌕\n🌕🌗🌑🌑🌑🌑🌕🌕\n🌕🌗🌑🌓🌕🌕🌕🌕\n🌕🌗🌑🌓🌕🌕🌕🌕\n🌕🌗🌑🌓🌕🌕🌕🌕\nV3",message_id=a)
                    
                    
                    elif text2[1] == 'взрыв' or text2[1] == 'love':
                        a = vk.messages.send(peer_id=Peer_id,message="✨✨✨🌍✨✨✨",random_id=0)
                        time.sleep(2)
                        vk.messages.edit(peer_id=Peer_id,message="💣✨✨🌍✨✨✨",message_id=a)
                        time.sleep(2)
                        vk.messages.edit(peer_id=Peer_id,message="✨💣✨🌍✨✨✨",message_id=a)
                        time.sleep(2)
                        vk.messages.edit(peer_id=Peer_id,message="✨✨💣🌎✨✨✨",message_id=a)
                        time.sleep(2)
                        vk.messages.edit(peer_id=Peer_id,message="✨✨✨🌎✨✨✨",message_id=a)
                        time.sleep(2)
                        vk.messages.edit(peer_id=Peer_id,message="✨✨✨🌏💣✨✨",message_id=a)
                        time.sleep(2)
                        vk.messages.edit(peer_id=Peer_id,message="✨✨✨🌏✨💣✨",message_id=a)
                        time.sleep(2)
                        vk.messages.edit(peer_id=Peer_id,message="✨✨✨🌍✨✨💣",message_id=a)
                        time.sleep(2)
                        vk.messages.edit(peer_id=Peer_id,message="✨✨✨🌍✨💣✨",message_id=a)
                        time.sleep(2)
                        vk.messages.edit(peer_id=Peer_id,message="✨✨✨⭐💣✨✨",message_id=a)
                        time.sleep(2)
                        vk.messages.edit(peer_id=Peer_id,message="✨✨✨💣✨✨✨",message_id=a)
                        time.sleep(2)
                        vk.messages.edit(peer_id=Peer_id,message="✨✨💣⭐✨✨✨",message_id=a)
                        time.sleep(2)
                        vk.messages.edit(peer_id=Peer_id,message="✨💣✨⭐✨✨✨✨",message_id=a)
                        time.sleep(2)
                        vk.messages.edit(peer_id=Peer_id,message="💣 ✨✨⭐✨✨✨",message_id=a)

                    
                    elif text2[1] == 'полиция' or text2[1] == 'police':
                        ra = randint(1, 3)
                        if ra == 1 or text2[1] == 'полиция1':
                            a = vk.messages.send(peer_id=Peer_id,message="          🚗    🚓",random_id=0)
                            time.sleep(2)
                            vk.messages.edit(peer_id=Peer_id,message="        🚗    🚓  ",message_id=a)
                            time.sleep(2)
                            vk.messages.edit(peer_id=Peer_id,message="      🚗  🚓      ",message_id=a)
                            time.sleep(2)
                            vk.messages.edit(peer_id=Peer_id,message="     🚗 🚓        ",message_id=a)
                            time.sleep(2)
                            vk.messages.edit(peer_id=Peer_id,message="   🚗  🚓         ",message_id=a)
                            time.sleep(2)
                            vk.messages.edit(peer_id=Peer_id,message="  🚗    🚓        ",message_id=a)
                            time.sleep(2)
                            vk.messages.edit(peer_id=Peer_id,message="🚗 🚓             ",message_id=a)
                            time.sleep(2)
                            vk.messages.edit(peer_id=Peer_id,message="  🚓             ",message_id=a)
                            time.sleep(2)
                            vk.messages.edit(peer_id=Peer_id,message="🚔 Failed Arest",message_id=a)
                            time.sleep(3)
                            vk.messages.edit(peer_id=Peer_id,message="&sudo полиция",message_id=a)
                            
                        elif ra == 2 or text2[1] == 'полиция2':
                            a = vk.messages.send(peer_id=Peer_id,message="          🚗    🚓",random_id=0)
                            time.sleep(2)
                            vk.messages.edit(peer_id=Peer_id,message="         🚗   🚓  ",message_id=a)
                            time.sleep(2)
                            vk.messages.edit(peer_id=Peer_id,message="       🚗  🚓     ",message_id=a)
                            time.sleep(2)
                            vk.messages.edit(peer_id=Peer_id,message="     🚗  🚓       ",message_id=a)
                            time.sleep(2)
                            vk.messages.edit(peer_id=Peer_id,message="   🚗  🚓         ",message_id=a)
                            time.sleep(2)
                            vk.messages.edit(peer_id=Peer_id,message="🚔 🚗 🚓          ",message_id=a)
                            time.sleep(2)
                            vk.messages.edit(peer_id=Peer_id,message="🚔🚧 🚘 🚓<Arested you>",message_id=a)
                            
                        elif ra == 3 or text2[1] == 'полиция3':
                            a = vk.messages.send(peer_id=Peer_id,message="     🚓",random_id=0)
                            time.sleep(2)
                            vk.messages.edit(peer_id=Peer_id,message="    🚓 ",message_id=a)
                            time.sleep(2)
                            vk.messages.edit(peer_id=Peer_id,message="   🚓  ",message_id=a)
                            time.sleep(2)
                            vk.messages.edit(peer_id=Peer_id,message="  🚓   ",message_id=a)
                            time.sleep(2)
                            vk.messages.edit(peer_id=Peer_id,message=" 🚓    ",message_id=a)
                            time.sleep(2)
                            vk.messages.edit(peer_id=Peer_id,message="🚓     ",message_id=a)
                    
                    elif text2[1] == 'ку' or text2[1] == 'durka':
                        a = vk.messages.send(peer_id=Peer_id,message="Привет, друг!",random_id=0)
                        time.sleep(2)
                        vk.messages.edit(peer_id=Peer_id,message="🤚",message_id=a)
                        time.sleep(2)
                        vk.messages.edit(peer_id=Peer_id,message="👋",message_id=a)
                        time.sleep(2)
                        vk.messages.edit(peer_id=Peer_id,message="🤚",message_id=a)
                        time.sleep(2)
                        vk.messages.edit(peer_id=Peer_id,message="👋",message_id=a)
                        time.sleep(2)
                        vk.messages.edit(peer_id=Peer_id,message="🤚",message_id=a)
                        time.sleep(2)
                        vk.messages.edit(peer_id=Peer_id,message="👋",message_id=a)
                        
                    elif text2[1] == 'пинг' or text2[1] == 'ping':
                        P_time = datetime.now().timestamp()
                        requests = get(f'https://api.vk.com/method/messages.getConversations?count=20?filter=all?v=5.89&access_token={token}')
                        Vk_time = datetime.now().timestamp()
                        delta = round(Vk_time - P_time, 2)
                        a = vk.messages.send(peer_id=Peer_id,message="херня какая-то",random_id=0)
                        vk.messages.edit(peer_id=Peer_id,message=f"ПОНГ\nВремя ответа: {delta}ms",message_id=a)
        except:
            time.sleep(0.2)
            continue
