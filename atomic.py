import openai
import pandas as pd
import time

def ReadExcelFile(filename):
    try:
        df = pd.read_excel(filename)
    except:
        df = pd.read_csv(filename)
    return df

def GetCompletions(prompt, question, engine, tokens):
    api_key = "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"
    openai.organization = "org-S3POWFAdvhzHFxU7FLRAMh4g"
    openai.api_key = api_key
    completion = openai.Completion.create(engine=engine, max_tokens=tokens, prompt= str(prompt) + " | " + question)
    return completion

def GetResponseFromOpenAI(question, engine, tokens, filename):
    filepath = '/content/drive/MyDrive/' + filename
    messages = ReadExcelFile(filepath)
    response_list = []

    for m in range(len(messages)):
        prompt = messages.iloc[m]
        response = GetCompletions(prompt, question, engine, tokens)
        response_list.append(response)
        time.sleep(2)

    responses = pd.concat(response_list)
    responses.to_csv("Result of - " + filename)
    
