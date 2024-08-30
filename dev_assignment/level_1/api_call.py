from groq import Groq
import time
import json
with open('input.txt', 'r') as file:
    lines = file.readlines()
groq_api_key = "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"


def get_llm_response(text):
    client = Groq(api_key = groq_api_key)

    chat_completion = client.chat.completions.create(
        messages=[
            
            {
                "role": "user",
                "content": text,
            }
        ],
        model="llama3-8b-8192",
        temperature=0.5,
        max_tokens=1024,
        top_p=1,
        stop=None,
        stream=False,
    )

    return chat_completion.choices[0].message.content

responses = []
for i in lines:
    start_time = time.time()
    response=get_llm_response(i)
    end_time = time.time()
    response_obj = {
        "prompt":i,
        "message":response,
        "TimeSent":start_time,
        "TimeRecvd":end_time,
        "Source":"Groq"
    }
    responses.append(response_obj)


print(responses)

with open("output.json","w") as json_file:
    json.dump(responses,json_file,indent=4)