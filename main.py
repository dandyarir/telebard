from bardapi import Bard
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ChatAction
from functools import wraps
from time import sleep
import requests
from decouple import config as envConfig
from telegram import Update


# Set your __Secure-1PSID value to key
token = envConfig('BOT_TELEGRAM_TOKEN')
token_bard = envConfig('BARD_TOKEN')

session = requests.Session()
session.headers = {
            "Host": "bard.google.com",
            "X-Same-Domain": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
            "Origin": "https://bard.google.com",
            "Referer": "https://bard.google.com/",
        }
session.cookies.set("__Secure-1PSID", token_bard)
bardInstance = None

def send_typing_action(func):
  """Sends typing action while processing func command."""

  @wraps(func)
  def command_func(update, context, *args, **kwargs):
      context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=ChatAction.TYPING)
      return func(update, context,  *args, **kwargs)

  return command_func

@send_typing_action
def initBardInstance(update: Update, context, notify):
    global bardInstance
    answer = '''My name is Alyssa. I am a large language model created by @dandyarir, a Software Engineer. I am still under development, but I am learning to perform many kinds of tasks, including:
        - Following instructions and completing requests thoughtfully.
        - Answering questions in a comprehensive and informative way, even if they are open ended, challenging, or strange.
        - Generating different creative text formats, like poems, code, scripts, musical pieces, email, letters, etc.
        I am always learning and improving, and I am excited to see what I can do in the future.'''
    bardInstance = Bard(token=token_bard, session=session, timeout=30)
    response = bardInstance.get_answer("You are now act named as Alyssa. If someone ask you your name, you should answer " + answer)

    print(response['content'])
    if notify:
        context.bot.send_message(chat_id=update.effective_chat.id, text="New Chat Initialized")

def checkBardInstance(update: Update, context, notify):
    global bardInstance
    if bardInstance is None:
        initBardInstance(update, context, notify=notify)
    pass

@send_typing_action
def start(update: Update, context):
  context.bot.send_message(chat_id=update.effective_chat.id, text="Halo Gaisss!")

  # Initialize bard instance if not initialized
  checkBardInstance(update, context)


@send_typing_action
def answer(update, context):
  input_text = update.message.text

  checkBardInstance(update, context, notify=False)
  # Perform API request and get the response
  response = bardInstance.get_answer(input_text)

  if 'content' in response:
      response_text = response['content']
  else:
      response_text = 'No response found.'

  # Send text response
  context.bot.send_message(chat_id=update.effective_chat.id, text=response_text)
  # Send code response if available
  if 'code' in response:
      code = response['code']
      if not code & len(code) > 5:
          context.bot.send_message(chat_id=update.effective_chat.id, text=f"```{code}```")

  # Send up to 5 image responses if links are available
  if 'links' in response:
      links = response['links']
      image_count = 0
      for link in links:
          if link.endswith('.jpg') or link.endswith('.jpeg') or link.endswith('.png'):
              context.bot.send_photo(chat_id=update.effective_chat.id, photo=link)
              image_count += 1
              if image_count >= 5:
                  break
          else:
              context.bot.send_message(chat_id=update.effective_chat.id, text=link)
@send_typing_action
def hi(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello!")
    print("hi")

@send_typing_action
def start_new_convo(update, context):
    initBardInstance(update, context, notify=True)


def main():
    updater = Updater(token, use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    hi_handler = CommandHandler('hi', hi)
    new_convo_handler = CommandHandler('start_new_convo', start_new_convo)
    answer_handler = MessageHandler(Filters.text & ~Filters.command, answer)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(hi_handler)
    dispatcher.add_handler(new_convo_handler)
    dispatcher.add_handler(answer_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()