from groq import Groq, RateLimitError, APIError, APIConnectionError
from dotenv import load_dotenv
import time
import os

class LLMWrapper:
    def __init__(self):
        load_dotenv()
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))

        self.MODEL_COST = {
            "openai/gpt-oss-20b": {"input": 0.075, "output": 0.30}
        }
        self.total_cost = 0
        self.total_input_token = 0
        self.total_output_token = 0

    def chat(self, model, message, stream=False):
        message_dict = [{"role": "user", "content": message}]
        for attempt in range(3):
            try:
                if not stream:
                    response = self.client.chat.completions.create(
                        model=model,
                        messages = message_dict,
                        max_tokens=2048
                    )
                    self.total_input_token += response.usage.prompt_tokens
                    self.total_output_token += response.usage.completion_tokens
                    self.calculate_cost(model, response.usage.prompt_tokens, response.usage.completion_tokens)
                    print(response.choices[0].message.content)
                    return response.choices[0].message.content
                else:
                    full_text = ""
                    completion = self.client.chat.completions.create(
                        model=model,
                        messages=message_dict,
                        max_tokens=2048,
                        stream=True,
                    )
                    for chunk in completion:
                        if chunk.choices:
                            delta = chunk.choices[0].delta.content
                            if delta:
                                full_text += delta
                                print(delta, end="", flush=True)

                        if chunk.usage is not None:
                            self.total_input_token += chunk.usage.prompt_tokens
                            self.total_output_token += chunk.usage.completion_tokens
                            self.calculate_cost(model, chunk.usage.prompt_tokens, chunk.usage.completion_tokens)
                    print()
                    return full_text
            except RateLimitError:
                wait = 2 ** attempt
                print(f"Rate limit hit - retrying in {wait}secs")
                time.sleep(wait)
            except APIConnectionError:
                print("No Internet Connection")
            except APIError as e:
                print(f"API error {e.status_code}: {e.message}")
        raise Exception("Max retries exceeded")

    def calculate_cost(self, model, input_tokens, output_tokens):
        if model in self.MODEL_COST:
            cost = self.MODEL_COST[model]
            input_cost = (input_tokens/1000000)*cost["input"]
            output_cost = (output_tokens/1000000)*cost["output"]
            self.total_cost += input_cost + output_cost
        else:
            return 0.0

    def get_stats(self):
        print(f"\nToken Used - Total input tokens: {self.total_input_token}, Total output tokens: {self.total_output_token}")
        print(f"Total estimated Cost: {self.total_cost}")


chatbot = LLMWrapper()
message = "What is meant by LLM?"

# Test 1 — with streaming
print(f"YOU: {message}")
print("Assistant (streaming): ", end="")
chatbot.chat("openai/gpt-oss-20b", message, stream=True)

# Test 2 — without streaming
print(f"\nYOU: {message}")
print("Assistant (no stream):")
chatbot.chat("openai/gpt-oss-20b", message, stream=False)

chatbot.get_stats()
