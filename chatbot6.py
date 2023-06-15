import streamlit as st
import pandas as pd
import cohere
import openai
import os
import random
from cohere.responses.classify import Example

api_key = 'qhKnrg5qEORtJ4iUMHaYPrbsYkWcAembg7pNQ2H8'

def GetReasoningCompletions(prompt, question):
    openai.organization = "org-S3POWFAdvhzHFxU7FLRAMh4g"
    openai.api_key = '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'
    completion = openai.Completion.create(engine='text-davinci-003', max_tokens=10, n=1, stop=None, prompt= str(prompt) + " || " + question, temperature=0.5)
    response = completion.choices[0].text
    response = str(response)
    return [response.strip()]


co = cohere.Client(api_key)

ARGsheetPath = os.path.join(os.getcwd(), 'generated_responses.csv')

ARG = pd.read_csv(ARGsheetPath)
# print(ARG)

def CohereGenerate(prompt):
    response = co.generate(  
        model='command-nightly',  
        prompt = prompt,  
        max_tokens=200,  
        temperature=0.750)
    intro_paragraph = response.generations[0].text
    return intro_paragraph.lower().strip()


def GenerateChatBotResponse(prompt):

    input = [prompt]

    Discipline = co.classify(
    model='ff56d3fa-adf4-4e55-999b-4298252b7171-ft',
    inputs=input,
    )
    a = pd.DataFrame(Discipline.classifications[0].labels)

    final_score = 0
    for column in a:
        score = a[column].values
        if score > final_score:
            final_score = score
            discipline = column

    # print('Discipline - ', discipline)

    Interaction = co.classify(
    model='1e98c7cb-5120-4daa-bcd5-59b9cec0b731-ft',
    inputs=input,
    
    )
    b = pd.DataFrame(Interaction.classifications[0].labels)

    Ifinal_score = 0
    for column in b:
        score = b[column].values
        if score > Ifinal_score :
            Ifinal_score = score
            interaction = column

    # print('Interaction - ', interaction)

    Issue = co.classify(
    model='b6aa23f7-52e4-44d9-aae3-91b8ce456404-ft',
    inputs=input,
    
    )
    c = pd.DataFrame(Issue.classifications[0].labels)

    final_score = 0
    for column in c:
        score = c[column].values
        if score > final_score:
            final_score = score
            issue = column

    # print('Issue - ', issue)

    InteractionMask = ARG['interaction'] == interaction
    DisciplineMask = ARG['discipline'] == discipline
    IssueMask = ARG['issue'] == issue

    idx = random.randint(0, len(ARG[InteractionMask & DisciplineMask & IssueMask]))

    if len(ARG[InteractionMask & DisciplineMask & IssueMask]) != 0:
        print(interaction + ' ' + discipline + ' ' + issue)
        Response = ARG[InteractionMask & DisciplineMask & IssueMask]['message'][idx]
    else:
        print(interaction + ' ' + discipline + ' ' + issue)
        Res = 'Classification not in ARG'
        Response = Res + '. Interaction - ' + interaction +', Issue - '+issue+', Discipline - '+discipline

    return Response


