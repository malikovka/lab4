import telebot
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
rpc_user='kzcashrpc'
rpc_password='keEcJag3g09iT2LzD8jcTbCj'
bot = telebot.TeleBot("6838869729:AAGgt28OIcO6XOSKF-Njm3TPWoq52oG1xMo")

rpc_connection = AuthServiceProxy(f'http://{rpc_user}:{rpc_password}@127.0.0.1:8                                                                             276')

@bot.message_handler(commands=['getbalance'])
def get_balance(message):
    balance = float(rpc_connection.getbalance())
    bot.reply_to(message, f"Ваш баланс: {balance}")

@bot.message_handler(commands=['getnewaddress'])
def get_new_address(message):
    new_address = rpc_connection.getnewaddress()
    bot.reply_to(message, f"Новый адрес: {new_address}")

@bot.message_handler(commands=['send'])
def send_coins(message):
    global temp
    args = message.text.split()[1:]
    if len(args) != 3:
        bot.reply_to(message, " /send адрес_отправителя адрес_получателя сумма")
        return
    sender_address, receiver_address, amount = args
    try:
        inputs = rpc_connection.listunspent(0, 9999, [sender_address])
    except JSONRPCException:
        bot.reply_to(message, f"Ошибка")
        return
    for i in inputs:
        temp = i
        if float(float(temp.get("amount"))) > (float(amount)+0.001):
            break
    if float(float(temp.get("amount"))) < (float(amount)+0.001):
        bot.reply_to(message, "Недостаточно средств")
        return

    change = float(temp.get("amount")) - float(amount) - 0.001 #
    inputForTransaction = {"txid":temp.get("txid"), "vout": temp.get("vout")}
    try:
        createTransaction = rpc_connection.createrawtransaction([inputForTransac                                                                             tion], {receiver_address:amount, sender_address:change})
    except JSONRPCException:
        bot.reply_to(message, f"Ошибка2")
        return
    signTransaction = rpc_connection.signrawtransaction(createTransaction)
    receivedHex = signTransaction.get("hex")
    txid = rpc_connection.sendrawtransaction(receivedHex)
    bot.reply_to(message, f"Транзакция прошла успешно. id: {txid}")

@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    bot.send_message(message.chat.id, message.text)

if __name__ == '__main__':
    bot.infinity_polling()
