from groq import Groq
from dotenv import load_dotenv
import json
import os

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

queries = [
    "Hi",
    "What are Virat Kohli's IPL stats?",
    "What is the strike rate if a player scored 85 runs off 62 balls?",
    "Compare Rohit Sharma and MS Dhoni",
]

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_cricket_stats",
            "description": "Get the stats of the given player",
            "parameters": {
                "type": "object",
                "properties": {
                    "player_name": {
                        "type": "string",
                        "description": "Player Name e.g Rohit Sharma, Virat Kohli etc"
                    }
                },
                "required": ["player_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_strike_rate", 
            "description": "Calculate the strike rate of the given runs and balls",
            "parameters": {
                "type": "object",
                "properties": {
                    "runs": {
                        "type": "integer",
                        "description": "Runs e.g 50, 70 etc"
                    },
                    "balls": {
                        "type": "integer",
                        "description": "Balls e.g 30, 26 etc"
                    }
                },
                "required": ["runs", "balls"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "compare_player", 
            "description": "Get the comparison dictionary of the given two players",
            "parameters": {
                "type": "object",
                "properties": {
                    "player1": {
                        "type": "string",
                        "description": "Player Name e.g Rohit Sharma, Virat Kohli etc"
                    },
                    "player2": {
                        "type": "string",
                        "description": "Player Name e.g Rohit Sharma, Virat Kohli etc"
                    }
                },
                "required": ["player1", "player2"] 
            }
        }
    }
]

def get_cricket_stats(player_name):
    stats = {
        "Virat Kohli": {"matches": 242, "runs": 7263, "average": 37.9, "hundreds": 8},
        "Rohit Sharma": {"matches": 243, "runs": 6211, "average": 31.2, "hundreds": 2},
        "MS Dhoni": {"matches": 350, "runs": 5082, "average": 39.4, "hundreds": 0},
    }
    return stats.get(player_name, {"error": "Player not found"})

def calculate_strike_rate(runs, balls):
    if balls == 0:
        return {"error": "balls cannot be zero"}
    return {"strike_rate": round((runs/balls)*100, 2)}

def compare_player(player1, player2):
    player1_stats = get_cricket_stats(player1)
    player2_stats = get_cricket_stats(player2)

    comparison_dict = {player1: player1_stats, player2: player2_stats}
    return comparison_dict

functions = {
    "get_cricket_stats": get_cricket_stats,
    "calculate_strike_rate": calculate_strike_rate,
    "compare_player": compare_player
}

for i in range(len(queries)):
    message = [{"role": "user", "content": queries[i]}]
    print(f"PROMPT: {queries[i]}")
    print("RESPONSE: ")
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=message,
        tools=tools,
        max_tokens=2048
    )

    if response.choices[0].finish_reason == "tool_calls":
        tool_call = response.choices[0].message.tool_calls[0]

        function_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)

        print(f"LLM want to run: {function_name}{arguments}")

        result = functions[function_name](**arguments)

        message.append(response.choices[0].message)
        message.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": json.dumps(result)
        })

        final_response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=message,
            max_tokens=2048
        )

        print(final_response.choices[0].message.content)
        print("\n")
    else:
        print(response.choices[0].message.content)
        print("\n")
