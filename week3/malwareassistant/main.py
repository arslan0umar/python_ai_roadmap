from groq import Groq
from dotenv import load_dotenv
import json
import os

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

queries = [
    "Hi",
    "What do you know about the WannaCry malware family?",
    "What is the detection confidence if a sample scores 0.87 on 42 signature checks?",
    "Compare WannaCry and NotPetya",
]

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_malware_info",
            "description": "Get known information about a malware family",
            "parameters": {
                "type": "object",
                "properties": {
                    "malware_name": {
                        "type": "string",
                        "description": "Malware family name e.g WannaCry, NotPetya, Emotet etc"
                    }
                },
                "required": ["malware_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_detection_confidence",
            "description": "Calculate detection confidence percentage from a score and number of signature checks",
            "parameters": {
                "type": "object",
                "properties": {
                    "score": {
                        "type": "number",
                        "description": "Raw detection score e.g 0.87, 0.65 etc"
                    },
                    "checks": {
                        "type": "integer",
                        "description": "Number of signature checks performed e.g 42, 30 etc"
                    }
                },
                "required": ["score", "checks"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "compare_malware",
            "description": "Get a comparison dictionary of the given two malware families",
            "parameters": {
                "type": "object",
                "properties": {
                    "malware1": {
                        "type": "string",
                        "description": "Malware family name e.g WannaCry, NotPetya etc"
                    },
                    "malware2": {
                        "type": "string",
                        "description": "Malware family name e.g WannaCry, NotPetya etc"
                    }
                },
                "required": ["malware1", "malware2"]
            }
        }
    }
]

def get_malware_info(malware_name):
    database = {
        "WannaCry": {"type": "Ransomware", "year": 2017, "propagation": "EternalBlue SMB exploit", "polymorphic": False},
        "NotPetya": {"type": "Wiper/Ransomware", "year": 2017, "propagation": "EternalBlue + credential theft", "polymorphic": False},
        "Emotet": {"type": "Trojan/Botnet", "year": 2014, "propagation": "Phishing, macro documents", "polymorphic": True},
    }
    return database.get(malware_name, {"error": "Malware family not found"})

def calculate_detection_confidence(score, checks):
    if checks == 0:
        return {"error": "checks cannot be zero"}
    confidence = round((score * checks) / checks * 100, 2)
    return {"detection_confidence_percent": confidence}

def compare_malware(malware1, malware2):
    malware1_info = get_malware_info(malware1)
    malware2_info = get_malware_info(malware2)
    comparison_dict = {malware1: malware1_info, malware2: malware2_info}
    return comparison_dict

functions = {
    "get_malware_info": get_malware_info,
    "calculate_detection_confidence": calculate_detection_confidence,
    "compare_malware": compare_malware
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

        print(f"LLM wants to run: {function_name}{arguments}")

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
            tools=tools,
            max_tokens=2048
        )

        print(final_response.choices[0].message.content)
        print("\n")
    else:
        print(response.choices[0].message.content)
        print("\n")