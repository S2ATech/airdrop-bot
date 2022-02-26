import os
import time
import json
import telebot
import keep_alive
##TOKEN DETAILS
TOKEN = "€"

BOT_TOKEN = os.environ['BOT_TOKEN']
PAYMENT_CHANNEL = "@aidefinace"  #add payment channel here including the '@' sign
OWNER_ID = 1331194466  #write r's user id here.. get it from @MissRose_Bot by /id
CHANNELS = open('canaux.txt', 'r', encoding='utf-8').read().split('\n')
 #add channels to be checked here in the format - ["Channel 1", "Channel 2"]
#you can add as many channels here and also add the '@' sign before channel username
Daily_bonus = 10  #Put daily bonus amount here!
Mini_Withdraw = 1000  #remove 0 and add the minimum withdraw u want to set
Per_Refer = 50  #add per refer bonus here
bot = telebot.TeleBot(BOT_TOKEN)

def check(id):
    for i in CHANNELS:
        check = bot.get_chat_member(i, id)
        if check.status != 'left':
            pass
        else:
            return False
    return True

bonus = {}

def menu(id):
   admins = open('admins.txt','r',encoding='utf-8').read().split('\n')
   if str(id) in admins:
     keyboard = telebot.types.ReplyKeyboardMarkup(True)
     keyboard.row('🆔 Compte')
     keyboard.row('👥 Parrainage', '🎁 Bonus', '💸 Retrait')
     keyboard.row('⚙️ Mettre un numéro', '📊Statistiques')
     keyboard.row('🔀 Canaux', '👬 Utilisateur', '📧 Message')
     bot.send_message(id,
                     "*🏡 Menu ⬇️*",
                     parse_mode="Markdown",
                     reply_markup=keyboard)

   else:
     keyboard = telebot.types.ReplyKeyboardMarkup(True)
     keyboard.row('🆔 Compte')
     keyboard.row('👥 Parrainage', '🎁 Bonus', '💸 Retrait')
     keyboard.row('⚙️ Mettre un numéro', '📊Statistiques')
     bot.send_message(id,
                     "*🏡 Menu ⬇️*",
                     parse_mode="Markdown",
                     reply_markup=keyboard)
                     
@bot.message_handler(commands=['start'])
def start(message):
    try:
        user = message.chat.id
        msg = message.text
        if msg == '/start':
            user = str(user)
            data = json.load(open('users.json', 'r'))
            if user not in data['referred']:
                data['referred'][user] = 0
                data['total'] = data['total'] + 1
            if user not in data['referby']:
                data['referby'][user] = user
            if user not in data['checkin']:
                data['checkin'][user] = 0
            if user not in data['DailyQuiz']:
                data['DailyQuiz'][user] = "0"
            if user not in data['balance']:
                data['balance'][user] = 0
            if user not in data['wallet']:
                data['wallet'][user] = "none"
            if user not in data['withd']:
                data['withd'][user] = 0
            if user not in data['id']:
                data['id'][user] = data['total'] + 1
            json.dump(data, open('users.json', 'w'))
            print(data)
            markup = telebot.types.InlineKeyboardMarkup()
            markup.add(
                telebot.types.InlineKeyboardButton(text='🤼‍♂️ Vérifié',
                                                   callback_data='check'))
            msg_start = "*🍔 Rejoignez les canaux"
            for i in CHANNELS:
                msg_start += f"\n➡️ {i}\n"
            msg_start += "*"
            bot.send_message(user,
                             msg_start,
                             parse_mode="Markdown",
                             reply_markup=markup)
        else:

            data = json.load(open('users.json', 'r'))
            user = message.chat.id
            user = str(user)
            refid = message.text.split()[1]
            if user not in data['referred']:
                data['referred'][user] = 0
                data['total'] = data['total'] + 1
            if user not in data['referby']:
                data['referby'][user] = refid
            if user not in data['checkin']:
                data['checkin'][user] = 0
            if user not in data['DailyQuiz']:
                data['DailyQuiz'][user] = 0
            if user not in data['balance']:
                data['balance'][user] = 0
            if user not in data['wallet']:
                data['wallet'][user] = "none"
            if user not in data['withd']:
                data['withd'][user] = 0
            if user not in data['id']:
                data['id'][user] = data['total'] + 1
            json.dump(data, open('users.json', 'w'))
            print(data)
            markups = telebot.types.InlineKeyboardMarkup()
            markups.add(
                telebot.types.InlineKeyboardButton(text='🤼‍♂️ Vérifié',
                                                   callback_data='check'))
            msg_start = "*🍔Rejoignez avant de continuer - \n➡️ @aidefinace\n➡️ @fifapronostic1\n➡️ @pronosticfranckbig*"
            bot.send_message(user,
                             msg_start,
                             parse_mode="Markdown",
                             reply_markup=markups)
    except:
        bot.send_message(
            message.chat.id,
            "This command having error pls wait for ficing the glitch by admin"
        )
        bot.send_message(
            OWNER_ID,
            "Your bot got an error fix it fast!\n Error on command: " +
            message.text)
        return

@bot.message_handler(commands=['send'])
def send(message):
    admins = open('admins.txt', 'r', encoding='utf-8').read().split('\n')
    if str(message.chat.id) in admins and len(message.text.split()) >= 2:
        cache = ''
        for text in message.text.split()[1::]:
            cache+=text+' '
        a = 0
        n = 0
        users = open('users.txt', 'r', encoding='utf-8').read().split(',\n')
        for user in users:
            if user != '':
                try:
                    keyboard = telebot.types.ReplyKeyboardMarkup(True)
                    keyboard.row('➡️ continuer')
                    bot.send_message(user, cache, reply_markup=keyboard)
                    a+=1
                except Exception as e:
                    users.remove(user)
                    with open('users.txt', 'w', encoding='utf-8') as f:
                        for u in users:
                            f.write(f'{u}\n')
                n+=1
        bot.send_message(message.chat.id, f'utilisateur: {n}\nMessage envoyer avec succès: {a}')
        ''
@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    try:
        ch = check(call.message.chat.id)
        if call.data == 'check':
            if ch == True:
                data = json.load(open('users.json', 'r'))
                user_id = call.message.chat.id
                user = str(user_id)
                bot.answer_callback_query(
                    callback_query_id=call.id,
                    text='✅ Vous avez rejoins avec succès')
                bot.delete_message(call.message.chat.id,
                                   call.message.message_id)
                if user not in data['refer']:
                    data['refer'][user] = True

                    if user not in data['referby']:
                        data['referby'][user] = user
                        json.dump(data, open('users.json', 'w'))
                    if int(data['referby'][user]) != user_id:
                        ref_id = data['referby'][user]
                        ref = str(ref_id)
                        if ref not in data['balance']:
                            data['balance'][ref] = 0
                        if ref not in data['referred']:
                            data['referred'][ref] = 0
                        json.dump(data, open('users.json', 'w'))
                        data['balance'][ref] += Per_Refer
                        data['referred'][ref] += 1
                        bot.send_message(
                            ref_id,
                            f"*🏧 Nouveau referral en Level 1, vous avez : +{Per_Refer} {TOKEN}*",
                            parse_mode="Markdown")
                        json.dump(data, open('users.json', 'w'))
                        return menu(call.message.chat.id)

                    else:
                        json.dump(data, open('users.json', 'w'))
                        return menu(call.message.chat.id)

                else:
                    json.dump(data, open('users.json', 'w'))
                    menu(call.message.chat.id)

            else:
                bot.answer_callback_query(
                    callback_query_id=call.id,
                    text='❌  Vous devez rejoindre les canaux')
                bot.delete_message(call.message.chat.id,
                                   call.message.message_id)
                markup = telebot.types.InlineKeyboardMarkup()
                markup.add(
                    telebot.types.InlineKeyboardButton(text='🤼‍♂️ Vérifié',
                                                       callback_data='check'))
                msg_start = "*🍔Rejoignez avant de continuer - \n➡️ @aidefinace\n➡️ @fifapronostic1\n➡️ @pronosticfranckbig*"
                bot.send_message(call.message.chat.id,
                                 msg_start,
                                 parse_mode="Markdown",
                                 reply_markup=markup)
    except:
        bot.send_message(
            call.message.chat.id,
            "This command having error pls wait for ficing the glitch by admin"
        )
        bot.send_message(
            OWNER_ID,
            "Your bot got an error fix it fast!\n Error on command: " +
            call.data)
        return

@bot.message_handler(content_types=['text'])

def send_text(message):
    try:
        if message.text == '🆔 Compte':
            data = json.load(open('users.json', 'r'))
            accmsg = '*👮 Utilisateur : {}\n\n⚙️ Numéro : *`{}`*\n\n💸 Balance : *`{}`* {}*'
            user_id = message.chat.id
            user = str(user_id)

            if user not in data['balance']:
                data['balance'][user] = 0
            if user not in data['wallet']:
                data['wallet'][user] = "none"

            json.dump(data, open('users.json', 'w'))

            balance = data['balance'][user]
            wallet = data['wallet'][user]
            msg = accmsg.format(message.from_user.first_name, wallet, balance,
                                TOKEN)
            bot.send_message(message.chat.id, msg, parse_mode="Markdown")
        if message.text == '👥 Parrainage':
            ref_msg = "*🛡️Ganez de l'argent avec ce bot parrainage pas obligatoire\n🎁 Bonus journalier : 5 {}\n\n👥Par parrainage 50 {}\n\n🔗 Lien du bot ⬇️\n{}*"

            bot_name = bot.get_me().username
            user_id = message.chat.id
            user = str(user_id)

            ref_link = 'https://telegram.me/{}?start={}'.format(
                bot_name, message.chat.id)
            msg = ref_msg.format(TOKEN, TOKEN, ref_link)
            bot.send_message(message.chat.id, msg, parse_mode="Markdown")
        if message.text == "⚙️ Mettre un numéro":
            user_id = message.chat.id
            user = str(user_id)

            keyboard = telebot.types.ReplyKeyboardMarkup(True)
            keyboard.row('🚫 Cancel')
            send = bot.send_message(
                message.chat.id,
                "_⚠️Entrez votre numéro de téléphone suivie du code pays._",
                parse_mode="Markdown",
                reply_markup=keyboard)
            # Next message will call the name_handler function
            bot.register_next_step_handler(message, trx_address)
        if message.text == "🎁 Bonus":
            user_id = message.chat.id
            user = str(user_id)
            cur_time = int((time.time()))
            data = json.load(open('users.json', 'r'))
            #bot.send_message(user_id, "*🎁 Bonus Button is Under Maintainance*", parse_mode="Markdown")
            if (user_id not in bonus.keys()) or (cur_time - bonus[user_id] >
                                                 60 * 60 * 24):
                data['balance'][(user)] += Daily_bonus
                bot.send_message(
                    user_id, f"Félicitations vous reçu {Daily_bonus} {TOKEN}")
                bonus[user_id] = cur_time
                json.dump(data, open('users.json', 'w'))
            else:
                bot.send_message(
                    message.chat.id,
                    "❌*Vous pour recevoir un autre bonus dans 24h*",
                    parse_mode="markdown")
            return
        if message.text == "📊Statistiques":
            user_id = message.chat.id
            user = str(user_id)
            data = json.load(open('users.json', 'r'))
            msg = "*📊 Total parrainées : {} Users\n\n🥊 Total Retirer : {} {}*"
            msg = msg.format(data['total'], data['totalwith'], TOKEN)
            bot.send_message(user_id, msg, parse_mode="Markdown")
            return
        if message.text == "💸 Retrait":
            user_id = message.chat.id
            user = str(user_id)

            data = json.load(open('users.json', 'r'))
            if user not in data['balance']:
                data['balance'][user] = 0
            if user not in data['wallet']:
                data['wallet'][user] = "none"
            json.dump(data, open('users.json', 'w'))

            bal = data['balance'][user]
            wall = data['wallet'][user]
            if wall == "none":
                bot.send_message(user_id,
                                 "_❌ Vous n'avez pas un numéro_",
                                 parse_mode="Markdown")
                return
            if bal >= Mini_Withdraw:
                bot.send_message(user_id,
                                 "_Entrer le solde_",
                                 parse_mode="Markdown")
                bot.register_next_step_handler(message, amo_with)
            else:
                bot.send_message(
                    user_id,
                    f"_❌ Votre solde dois être supérieur ou égal à {Mini_Withdraw} {TOKEN} pour retirer_",
                    parse_mode="Markdown")
                return
        if message.text == "🔀 Canaux":
            n = CHANNELS
            canal = ""
            for i in n:
              canal = canal + str(i) + "\n"
            cn_msg = "*Canaux\n"+canal+"\nVeuillez saisir les nouveaux canaux avec votre canal de payement "+PAYMENT_CHANNEL+"\nFORMAT:\n"+PAYMENT_CHANNEL+"\n@Canal2\n@canal3\n@canal4\n NB: Ajouter le bot dans les canaux avant*"
            keyboard = telebot.types.ReplyKeyboardMarkup(True)
            keyboard.row('🚫 Cancel')
            bot.send_message(message.chat.id,cn_msg,parse_mode="Markdown",reply_markup=keyboard)
            bot.register_next_step_handler(message,cn_set)
        if message.text == '👬 Utilisateur':
            data = json.load(open('users.json', 'r'))
            dic = data['id']
            keys = list(dic.keys())
            numbers = keys
            users_id = ""
            for i in numbers:
              users_id = users_id + str(i)+"\n"
            user_msg = "*"+users_id+"👮 Utilisateur : {}*"
            msg = user_msg.format(data['total'])
            bot.send_message(message.chat.id, msg, parse_mode="Markdown")
        if message.text == '📧 Message':
            data = json.load(open('users.json', 'r'))
            msg = '*Entrez votre message à envoyer avec la commande /send au début\nFormat:\n/send votre message*'
            bot.send_message(message.chat.id,msg,parse_mode="Markdown")
            return
        if message.text == '➡️ continuer':
            bot.send_message(message.chat.id,'*Cliquez sur /start pour continuer*',parse_mode="Markdown")
        else:
            return
    except:
        bot.send_message(
            message.chat.id,
            "This command having error pls wait for ficing the glitch by admin"
        )
        bot.send_message(
            OWNER_ID,
            "Your bot got an error fix it fast!\n Error on command: " +
            message.text)
        return

def trx_address(message):
    try:
        if message.text == "🚫 Cancel":
            return menu(message.chat.id)
        if len(message.text) >= 11:
            user_id = message.chat.id
            user = str(user_id)
            data = json.load(open('users.json', 'r'))
            data['wallet'][user] = message.text

            bot.send_message(message.chat.id,
                             "*💹 Votre numéro est mis avec succès " +
                             data['wallet'][user] + "*",
                             parse_mode="Markdown")
            json.dump(data, open('users.json', 'w'))
            return menu(message.chat.id)
        else:
            bot.send_message(message.chat.id,
                             "*⚠️ Numéro invalide!*",
                             parse_mode="Markdown")
            return menu(message.chat.id)
    except:
        bot.send_message(
            message.chat.id,
            "This command having error pls wait for ficing the glitch by admin"
        )
        bot.send_message(
            OWNER_ID,
            "Your bot got an error fix it fast!\n Error on command: " +
            message.text)
        return

def amo_with(message):
    try:
        user_id = message.chat.id
        amo = message.text
        user = str(user_id)
        data = json.load(open('users.json', 'r'))
        if user not in data['balance']:
            data['balance'][user] = 0
        if user not in data['wallet']:
            data['wallet'][user] = "none"
        json.dump(data, open('users.json', 'w'))

        bal = data['balance'][user]
        wall = data['wallet'][user]
        msg = message.text
        if msg.isdigit() == False:
            bot.send_message(
                user_id,
                "_📛 voleur invalide Entrez les chiffres uniquement. Ressayez",
                parse_mode="Markdown")
            return
        if int(message.text) < Mini_Withdraw:
            bot.send_message(
                user_id,
                f"_❌  Le minimum de retrait est {Mini_Withdraw} {TOKEN}_",
                parse_mode="Markdown")
            return
        if int(message.text) > bal:
            bot.send_message(
                user_id,
                "_❌  Le  font est insuffisant veuillez invité des amis pour gagner plus_",
                parse_mode="Markdown")
            return
        amo = int(amo)
        data['balance'][user] -= int(amo)
        data['totalwith'] += int(amo)
        bot_name = bot.get_me().username
        json.dump(data, open('users.json', 'w'))
        bot.send_message(
            user_id,
            "✅* Votre demande retrait est automatiquement envoyé dans \n\n💹 Notre canal:- "
            + PAYMENT_CHANNEL + "*",
            parse_mode="Markdown")

        markupp = telebot.types.InlineKeyboardMarkup()
        markupp.add(
            telebot.types.InlineKeyboardButton(
                text='🍀 Lien du BOT ',
                url=f'https://telegram.me/{bot_name}?start={OWNER_ID}'))

        send = bot.send_message(
            PAYMENT_CHANNEL,
            "✅* Nouveau retrait\n\n⭐ Amount - " + str(amo) +
            f" {TOKEN}\n🦁 User - @" + message.from_user.username +
            "\n💠 Numéro* - `" + data['wallet'][user] +
            "`\n☎️ *User Referrals = " + str(data['referred'][user]) +
            "\n\n🏖 Lien du Bot - @" + bot_name +
            "\n⏩ svp veuillez attendre la confirmation*",
            parse_mode="Markdown",
            disable_web_page_preview=True,
            reply_markup=markupp)
    except:
        bot.send_message(
            message.chat.id,
            "This command having error pls wait for ficing the glitch by admin"
        )
        bot.send_message(
            OWNER_ID,
            "Your bot got an error fix it fast!\n Error on command: " +
            message.text)
        return

def cn_set(message):
    try:
        if message.text == "🚫 Cancel":
            return menu(message.chat.id)
        if '\n' and '@' in message.text:
            open('canaux.txt','w' ,encoding = 'utf-8').write(message.text)
            bot.send_message(message.chat.id,'*vos sont mises à jour avec succès.*',parse_mode="Markdown")
        else:
            bot.send_message(message.chat.id,'*suivez correctement le format*',parse_mode="Markdown")
    except:
        bot.send_message(
            message.chat.id,
            "This command having error pls wait for ficing the glitch by admin"
        )
        bot.send_message(
            OWNER_ID,
            "Your bot got an error fix it fast!\n Error on command: " +
            message.text)
        return

def send_r(message):
  if message.text == '🚫 Cancel':
    return menu(message.chat.id)
  else:
    return

keep_alive.keep_alive()
bot.polling(none_stop=True)
