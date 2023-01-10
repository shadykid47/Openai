import openai
import pandas as pd
import time

def ReadExcelFile(filename):
    try:
        df = pd.read_excel(filename)
    except:
        df = pd.read_csv(filename)
    return df
  
def GetCompletions(api_key, prompt, question, engine, tokens):
    openai.organization = "org-S3POWFAdvhzHFxU7FLRAMh4g"
    openai.api_key = api_key
    completion = openai.Completion.create(engine=engine, max_tokens=tokens, prompt= str(prompt) + " || " + question)
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
        # prompt = prompt[7:len(prompt)-24]
        print("PROMPT IS - \n", prompt)
        response = GetCompletions(api_key, prompt, question1, engine, tokens)
        print("RESPONSE IS - \n", response)
        print("\n")
        response_list.append(response)
        message_list.append(messages.iloc[m]['Message'])
        time.sleep(5)

    message_series = pd.Series(message_list)
    response_series = pd.Series(response_list)
    # print(response_series)
    responses = pd.concat([message_series, response_series], axis = 1)
    responses.to_csv('/content/drive/MyDrive/' + "Results.csv")