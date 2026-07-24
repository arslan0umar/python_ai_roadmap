from groq import Groq
from dotenv import load_dotenv
import json
import os

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

system_prompt = """Your are an expert technical writer, who specializes in writing concise summaries for busy software engineers.
You summarize text accordoing to user specifeid format, if the user didn't specify a format then user your own"""

total_input_tokens = 0
total_output_tokens = 0

print("\t\t\tWelcome to Text Summarizer Tool\n")

article = """How does AI affect carbon emissions?
\tWe can broadly separate the climate impacts of AI into two categories - direct and indirect emissions from the infrastructure and energy needed to run this technology (covered under the widely used GHG Protocol's Scope 1 and Scope 2 of company emissions reports) and enabled emissions (currently not covered under Scope 3).
The increased demand for data centre capacity has received the most attention. In a 2024 report, Morgan Stanley estimates that the global data centre industry will emit 2.5 billion tons of CO2 through 2030. This is more than the combined annual emissions of countries in the Middle East (currently around 2 billion tons).
While efforts are underway to meet the surging energy demand of data centres with renewable sources, their main energy supply still stems from fossil fuels. According to the International Energy Agency, 56% of data centre electricity demand is being fulfilled by natural gas and coal. Renewables supply just over a quarter, while nuclear supplies 15%.
Given this scrutiny, major tech firms and data centre operators have pledged to prioritise the use of renewables. Google has pledged that its campuses will run on carbon-free power 24 hours per day by 2030, while Microsoft plans to be carbon negative by 2030. 
Amazon Web Services says that in 2024 it was the largest corporate buyer of clean energy in the world. However, these announcements mean little if they fail to translate to actual emission reductions, rely on unreliable methods like carbon offsetting, or mask emissions that aren't covered by current reporting requirements.
While Big Tech makes big claims about providing its technology to help with climate solutions, it is becoming even more involved with the fossil fuel industry. Its technology is handing big polluters a lifeline that they need to keep us all hooked on fossil fuels.
Holly and Will Alpine calculated the emissions enabled by just two of Microsoft's contracts with fossil fuel majors, Exxon and Chevron, in 2020. These amount to 57.3 million tons of carbon, which is over three times Microsoft's entire company emissions in 2023, including all data centres.
Taking into account that Microsoft's potential market opportunity is thought to be between $35 billion and $75 billion annually from various contracts with fossil fuel companies, its darling status among the ESG investment crowd must be called into question.
Understanding the truth about enabled emissions allows us to see the whole picture, and not just the positives of technology advancement that Big Tech PR is keen to amplify."""

# Call 1 — fresh messages
messages_summary = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": f"Summarize the following article into 3 bullets summary, only foucs on main point and make sure these 3 bullets is summarizing the whole context\nArticle: {article}"}
]

# Call 2 — fresh messages
messages_sentiment = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": f"""Use this article: {article} and classify the review as positve, negative and neutral. 
    Review: Cricket is a good game -> positve
    Review: I hate football -> negative
    
    Now Classify:
    AI effect on Carbon Emission -> """}
]

# Call 3 — fresh messages
messages_json = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": f"Use this article: {article} extract title , main_topic, key_points (list) and word_count and RETURN only a JSON output with keys title, main_topic, key_points and word_count. No explanation, no markdown, just JSON."}
]

print(f"Article\n{article}\n")
print("3 Bullets Summary: ")

try:
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=messages_summary,
        max_tokens=1024
    )

    reply = response.choices[0].message.content

    input_tokens = response.usage.prompt_tokens
    output_tokens = response.usage.completion_tokens

    total_input_tokens += input_tokens
    total_output_tokens += output_tokens

    print(reply)

except Exception as e:
    print(f"Error: {e}")

print("\nSentiment analysis: ")
try:

    response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=messages_sentiment,
            max_tokens=1024
        )
    
    reply = response.choices[0].message.content

    input_tokens = response.usage.prompt_tokens
    output_tokens = response.usage.completion_tokens

    total_input_tokens += input_tokens
    total_output_tokens += output_tokens

    print(reply)

except Exception as e:
    print(f"Error: {e}")

print("\nStructured extraction: ")
try:

    response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=messages_json,
            max_tokens=7000
        )
    
    reply = response.choices[0].message.content

    input_tokens = response.usage.prompt_tokens
    output_tokens = response.usage.completion_tokens

    total_input_tokens += input_tokens
    total_output_tokens += output_tokens

    data = json.loads(reply)
    print(data)

except Exception as e:
    print(f"Error: {e}")

print(f"\nThanks for using the Text Summarizer Tool\nGoodBye\nTotal tokens used — Input: {total_input_tokens} | Output: {total_output_tokens}")