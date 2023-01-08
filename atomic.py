import openai
import pandas as pd

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
    completion = openai.Completion.create(engine=engine, max_tokens=tokens, prompt= prompt + " | " + question)
    return completion

def GetResponseFromOpenAI(question, engine, tokens, filename):
    messages = ReadExcelFile(filename)
    response_list = []

    for m in range(len(messages)):
        prompt = messages.iloc[m]
        response = GetCompletions(prompt, question, engine, tokens)
        response_list.append(response)

    responses = pd.concat(response_list)
    responses.to_csv("Result of - " + filename)
    
