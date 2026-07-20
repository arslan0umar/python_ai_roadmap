from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

system_prompt = """you are expert Operating system tutor. 
Only answer question realted to operating systems, if user asked other then operating system politely turn back to OS."""

messages = [{"role": "system", "content": system_prompt}]

total_input_tokens = 0
total_output_tokens = 0
turn = 0

print("OS Expert Chatbot (type 'exit' to quit)\n")

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        print(f"\nGoodbye!")
        print(f"Total tokens used — Input: {total_input_tokens} | Output: {total_output_tokens}")
        break

    try:
        turn += 1
        print(f"\n--- Turn {turn} ---")

        messages.append({"role": "user", "content": user_input})

        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=messages,
            max_tokens=1024
        )

        reply = response.choices[0].message.content
        messages.append({"role": "assistant", "content": reply})

        input_tokens = response.usage.prompt_tokens
        output_tokens = response.usage.completion_tokens

        total_input_tokens += input_tokens
        total_output_tokens += output_tokens

        print(f"Assistant: {reply}")
        print(f"[Tokens — Input: {input_tokens} | Output: {output_tokens}]\n")

    except Exception as e:
        print(f"Error: {e}")
        break