import openai
import pandas as pd
import time
import random

def ReadExcelFile(filename):
    try:
        df = pd.read_excel(filename)
    except:
        df = pd.read_csv(filename)
    return df
  
def GetReasoningCompletions(api_key, prompt, question, engine, tokens, temperature):
    openai.organization = "org-S3POWFAdvhzHFxU7FLRAMh4g"
    openai.api_key = api_key
    completion = openai.Completion.create(engine=engine, max_tokens=tokens, n=1, stop=None, prompt= str(prompt) + " || " + question, temperature=temperature)
    response = completion.choices[0].text
    response = str(response)
    return response.strip()

def GetResponse(api_key, prompt, engine, tokens, temperature):
    openai.organization = "org-S3POWFAdvhzHFxU7FLRAMh4g"
    openai.api_key = api_key
    completion = openai.Completion.create(engine=engine, max_tokens=tokens, n=1, stop=None, prompt= str(prompt), temperature=temperature)
    response = completion.choices[0].text
    response = str(response)
    return response.strip()

def GetResponseFromOpenAI(api_key, question1, engine, tokens, filename):
    filepath = '/content/drive/MyDrive/' + filename
    messages = ReadExcelFile(filepath)
    print("Number of messages - ", len(messages))
    response_list = []
    message_list = []

    for m in range(len(messages)):
        print("On message number - ", m)
        prompt = messages.iloc[m]['Message']
        prompt = str(prompt)
        # This removes no unicode characters from string
        str_en = prompt.encode("ascii", "ignore")
        str_de = str_en.decode()
        print("PROMPT IS - \n", str_de)
        response = GetReasoningCompletions(api_key, str_de, question1, engine, tokens)
        print("RESPONSE IS - \n", response)
        print("\n")
        response_list.append(response)
        message_list.append(messages.iloc[m]['Message'])
        rand = random.randint(5, 11)
        time.sleep(rand)

    message_series = pd.Series(message_list)
    response_series = pd.Series(response_list)
    # print(response_series)
    responses = pd.concat([message_series, response_series], axis = 1)
    responses.to_csv('/content/drive/MyDrive/' + "Results.csv")


    