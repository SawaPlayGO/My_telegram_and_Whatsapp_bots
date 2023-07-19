from whatsapp_chatbot_python import GreenAPIBot, Notification
import openai
from validator import normalize_text

bot = GreenAPIBot(
    "1101837558", "201948ce845a49c9ba2770c869602eaf278060a21a35403fb5"
)

openai.api_key = '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'

with open('prompt.txt', 'r', encoding='UTF-8') as prompt1:
    content = prompt1.read()

    print(content)

@bot.router.message()
def message_handler(notification: Notification) -> None:

    try:
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',  # Указываем модель GPT-3.5 Turbo 16K
            messages=[
                {"role": "user", "content": {notification.message_text}}
            ]
        )

        generated_text = str(response.choices[0].message.content.strip())
        normalized_text = normalize_text(generated_text)
        notification.answer(normalized_text)
        print(response)

    except openai.InvalidRequestError:
        notification.answer('❌ Сообщение превысило лимит в 16384 символов.')
    except openai.error.ServiceUnavailableError:
        notification.answer('❌ Ваш вопрос не совсем понятен, объясните его заново.')
    except openai.error.RateLimitError:
        notification.answer('❌ Квота вашего бота привышена')

bot.run_forever()