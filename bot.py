import re
import socket
# import weather_wizard as ww
import famous_last_words as flw
import random


HOST = "chat.freenode.net"  # or maybe irc.chat.twitch.tv
PORT = 6667  # Default IRC-Port
CHAN = "##NOONEHERE"  # on twitch: Channelname = #{Nickname}
NICK = "FamousLastWords"  # on twitch: Nickname = Twitch username
# ADMINNAME = "asilisav"
# PASS = "oauth:rhp2ptahvlrspf0njuxm1onitwvpd1"   # www.twitchapps.com/tmi/ will help to retrieve the required authkey

connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection.connect((HOST, PORT))


def join_channel(chan):
    connection.send(bytes("JOIN " + chan + "\n", "UTF-8"))
    ircmsg = ""
    while ircmsg.find("End of /NAMES list.") == -1:
        ircmsg = connection.recv(2048).decode("UTF-8")
        ircmsg = ircmsg.strip('\n\r')
        print(ircmsg)


def send_pong(msg):
    connection.send(bytes('PONG {}\r\n'.format(msg), 'UTF-8'))


def send_message(chan, msg):
    connection.send(bytes('PRIVMSG {} :{}\r\n'.format(chan, msg), 'UTF-8'))


def get_sender(msg):
    result = ""
    for char in msg:
        if char == "!":
            break
        if char != ":":
            result += char
    return result


def get_message(msg):
    result = ""
    i = 3
    length = len(msg)
    while i < length:
        result += msg[i] + " "
        i += 1
    result = result.lstrip(':')
    return result


connection.send(bytes("USER " + NICK + " " + NICK + " " + NICK + " " + NICK + "\r\n", "UTF-8"))
connection.send(bytes("NICK " + NICK + "\r\n", "UTF-8"))
join_channel(CHAN)

data = ""

list1 = flw.list_of_fame
list2 = []

while True:
    try:
        data = data + connection.recv(1024).decode('UTF-8')
        data_split = re.split(r'[~\n]+', data)
        data = data_split.pop()
        for line in data_split:
            line = str.rstrip(line)
            line = str.split(line)
            if len(line) >= 2:
                if line[0] == 'PING':
                    send_pong(line[1])
                else:
                    if line[1] == 'PRIVMSG':
                        sender = get_sender(line[0])
                        message = get_message(line)
                        print(sender + ": " + message)
                        if NICK in message:
                            if "do some magic" in message:
                                if len(list1) > 0:
                                    rand_inx = random.randrange(len(list1))
                                    pop_elem = list1.pop(rand_inx)
                                    list2.append(pop_elem)
                                else:
                                    list1 = list2
                                    list2 = []
                                    rand_inx = random.randrange(len(list1))
                                    pop_elem = list1.pop(rand_inx)
                                    list2.append(pop_elem)
                                # magic = ww.get_random_weather()
                                # send_message(CHAN, '"' + magic[1] + '"')
                                send_message(CHAN, pop_elem[0] + ' said: ' + '"' + pop_elem[1] + '"')
                                send_message(CHAN, pop_elem[2])
    except socket.timeout:
        print("Socket timeout")
    except socket.error:
        print("Socket died")
