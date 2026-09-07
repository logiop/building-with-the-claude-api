from dotenv import load_dotenv
import os
from anthropic import Anthropic

load_dotenv()

client = Anthropic()
model = "claude-sonnet-5"


def get_text_content(response):
    for block in response.content:
        if block.type == "text":
            return block.text
    return ""


def main():
    messages = []
    print("🤖 Chat con Claude (scrivi 'exit' per uscire)\n")

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() == "exit":
            print("Goodbye! 👋")
            break

        if not user_input:
            continue

        messages.append({"role": "user", "content": user_input})
        print("Claude is thinking...")

        try:
            response = client.messages.create(
                model=model,
                max_tokens=500,
                messages=messages,
            )

            answer = get_text_content(response)
            print(f"Claude: {answer}\n")
            messages.append({"role": "assistant", "content": answer})

        except Exception as e:
            print(f"Error: {e}\n")
            messages.pop()


if __name__ == "__main__":
    main()
