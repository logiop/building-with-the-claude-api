from dotenv import load_dotenv

load_dotenv()

from anthropic import Anthropic

client = Anthropic()
model = "claude-sonnet-4-6"


def add_user_message(messages, text):
    user_message = {"role": "user", "content": text}
    messages.append(user_message)


def add_assistant_message(messages, text):
    assistant_message = {"role": "assistant", "content": text}
    messages.append(assistant_message)


def chat(messages):
    message = client.messages.create(
        model=model,
        max_tokens=1000,
        messages=messages,
    )
    return message.content[0].text


# Test
messages = []
print("Lista vuota:", messages)

add_user_message(messages, "Ciao, sono Giorgio")
print("Dopo add_user_message:", messages)

answer = chat(messages)
print("Risposta da Claude:", answer)

add_assistant_message(messages, answer)
print("Dopo add_assistant_message:", messages)
print("\nCronologia completa:")
for msg in messages:
    print(f"  {msg['role'].upper()}: {msg['content']}")
