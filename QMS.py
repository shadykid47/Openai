import streamlit as st
import pandas as pd
import cohere
import openai
import os
import plotly.graph_objs as go
from plotly.subplots import make_subplots
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

UploadedFile = st.file_uploader('Choose a File')

FolderPath = os.getcwd()

TrainingBasePath = FolderPath + '/TrainingBase.csv'
TrainingBase = pd.read_csv(TrainingBasePath)

KeywordsPath = FolderPath + '/Keywords.csv'
KeyWords = pd.read_csv(KeywordsPath)

DisciplineDictionary = {'Product_Availability' : 1 ,
                        'Brand' : 2 ,
                        'Service' : 3 ,
                        'Pricing' : 4 , 
                        'Product_Sensory' : 5 ,
                        'Product_Generic' : 6 ,
                        'Product_Packging' : 7 ,
                        'Product_Quality' : 8 ,
                        'Product_Foreign Body' : 9 ,
                        'Product_Infestation' : 10 ,
                        'Promotion' : 1 ,
                        'People' : 2 ,
                        'Product_Customization' : 3 ,
                        'Product_Ingridients' : 5 }

if UploadedFile is not None:
    Data = pd.read_csv(UploadedFile)
    drop_cols = []

    for col in Data.columns:
        if col == 'Ticket form' or col == 'Brief Description of Feedback' or col == 'Agent Name ' or col == 'Business Process ' or col == 'Ticket ID':
            pass
        else:
            drop_cols.append(col)
    Data = Data.drop(columns=drop_cols)
    Data = Data.dropna()
    Data = Data.iloc[0:50, :]
    print(Data)
    statement = 'File Uploaded successfully !'
    print(statement)
    st.write(statement)

    # EligibleDiscipline = []
    # statement = 'Finding Eligible Disciplines from our Training Base.'
    # print(statement)
    # st.write(statement)

    # for i in range(len(TrainingBase)):
    #     count = 0
    #     row = TrainingBase.iloc[i]
    #     response = row['Discipline_']
    #     for j in range(len(TrainingBase)):
    #         row = TrainingBase.iloc[j]
    #         response1 = row['Discipline_']
    #         if response1 == response:
    #             count += 1
    #     if count < 2:
    #         pass
    #     else:
    #         EligibleDiscipline.append(response)

    # EligibleInteraction = []
    # statement = 'Finding Eligible Interactions from our Training Base.'
    # print(statement)
    # st.write(statement)
    

    # for i in range(len(TrainingBase)):
    #     count = 0
    #     row = TrainingBase.iloc[i]
    #     response = row['Interaction_']
    #     for j in range(len(TrainingBase)):
    #         row = TrainingBase.iloc[j]
    #         response1 = row['Interaction_']
    #         if response1 == response:
    #             count += 1
    #     if count < 2:
    #         pass
    #     else:
    #         EligibleInteraction.append(response)

    # EligibleIssue = []
    # statement = 'Finding Eligible Issues from our Training Base.'
    # print(statement)
    # st.write(statement)    

    # for i in range(len(TrainingBase)):
    #     count = 0
    #     row = TrainingBase.iloc[i]
    #     response = row['Issue_ ']
    #     for j in range(len(TrainingBase)):
    #         row = TrainingBase.iloc[j]
    #         response1 = row['Issue_ ']
    #         if response1 == response:
    #             count += 1
    #     if count < 2:
    #         pass
    #     else:
    #         EligibleIssue.append(response)
        

    

    # Disciplineexample = []
    # Interactionexample = []
    # Issueexample = []

    # statement = 'Now Training our Model from our Database.'
    # print(statement)
    # st.write(statement)
    

    # for i in range(len(TrainingBase)):
    #     row = TrainingBase.iloc[i]
    #     query = row['Updated Statement']
    #     discipline = row['Discipline_']
    #     interaction = row['Interaction_']
    #     issue = row['Issue_ ']

    #     if discipline in EligibleDiscipline :
    #         Disciplineexample.append(Example( query , discipline )) 
    #     if interaction in EligibleInteraction:
    #         Interactionexample.append(Example(query, interaction))
    #     if issue in EligibleIssue:
    #         Issueexample.append(Example(query, issue))

    
    statement = 'Now Classifying the interactions from the uploaded file.'
    print(statement)
    st.write(statement)

    inputs = Data['Brief Description of Feedback'].to_list()
    ManualClassifications = Data['Ticket form'].to_list()
    BusinessProcesses = Data['Business Process '].to_list()
    Agents = Data['Agent Name '].to_list()
    TicketIDs = Data['Ticket ID'].to_list()

    FourthCheck = pd.DataFrame(columns = ['Query', 'Complaint', 'Feedback', 'Praise / Compliment', 'Suggestion', 'Collaboration'], 
                               index = ['Query', 'Complaint', 'Feedback', 'Praise / Compliment', 'Suggestion', 'Collaboration'])

    for col in FourthCheck.columns :
        FourthCheck[col] = 0

    RecordSummary = pd.DataFrame(columns=['ORM ', 'Email', 'Chat', 'Phone', 'Whatsapp'], 
                                 index=['Query', 'Complaint', 'Feedback', 'Praise / Compliment', 'Suggestion', 'Collaboration'])
    
    for col in RecordSummary.columns :
        RecordSummary[col] = 0
    
    # PRIMARY CLASSIFICATION

    # print(inputs)
    # print(len(inputs))

    fig = go.Figure()
    VisData = pd.DataFrame(columns=['Query', 'Score', 'Classification Match', 'Manual Classification', 'Interaction', 'Discipline', 'Issue', 'Agent Name'])
    ProcessedData = pd.DataFrame(columns=['Zen Desk', 'Case Details', 'Interaction', 'Discipline', 'Issue', 'Score', 'Agent Name'])

    
    # ORMCount = Data[Data['Business Process '] == 'ORM '].count().max()
    # EmailCount = Data[Data['Business Process '] == 'Email'].count().max()
    # ChatCount = Data[Data['Business Process '] == 'Chat'].count().max()
    # PhoneCount = Data[Data['Business Process '] == 'Phone'].count().max()
    # WhatsappCount = Data[Data['Business Process '] == 'Whatsapp'].count().max()

    for i in range(len(inputs)):

        try:    
            input = [inputs[i]]
            ManualClassification = ManualClassifications[i]
            BusinessProcess = BusinessProcesses[i]
            Agent = Agents[i]
            Ticket = TicketIDs[i]

            if input[0] == 'na' or len(input[0].split(' ')) == 1 :
                print('pass')
                pass
            else:

                print(input)
                # print(len(input[0]))
                print('Manual Classification - ', ManualClassification)
                    
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

                print('Discipline - ', discipline)

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

                print('Interaction - ', interaction)

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

                print('Issue - ', issue)

                # CALCULATING SCORE FOR THE QUERY
                question = 'Extract Keywords from this and give them in one line seperated by commas.'
                keywordslist = GetReasoningCompletions(input[0], question)
                # print(keywordslist)
                
                IssueScore = 0

                for col in KeyWords.columns:
                    for i in issue.split('/'):
                        if i.strip().lower() in [x.lower() for x in KeyWords[col].dropna().to_list()]:
                            IssueScore = col

                DisciplineScore = DisciplineDictionary[discipline]
                        
                # print(IssueScore)
                KeyWordScore = 0

                for keyword in keywordslist:
                    # print(keyword)
                    for col in KeyWords.columns:
                        # print(KeyWords[col])
                        if keyword.strip().lower() in [x.lower() for x in KeyWords[col].dropna().to_list()]: 
                            KeyWordScore += 1
                            if col > IssueScore:
                                IssueScore = col

                print('Issue Score - ',IssueScore)
                print( 'Keyword score - ',KeyWordScore)
                print('Discipline Score - ', DisciplineScore)
                FinalScore = int(IssueScore) * 10 + int(DisciplineScore)  + int(KeyWordScore)/10
                print('Final Score - ', FinalScore)  

                # FinalScore = InteractionScore*10*0.5 + KeywordScore*10*0.4 + Discipline*10*0.1
                
                if interaction == ManualClassification:
                    ClassificationMatch = 0
                else:
                    ClassificationMatch = 1

                VisData.loc[len(VisData.index)] = [input[0], FinalScore, ClassificationMatch, ManualClassification, interaction, Discipline, issue, Agent]
                RecordSummary.loc[interaction][BusinessProcess] = RecordSummary[BusinessProcess][interaction] + 1
                FourthCheck.loc[interaction][ManualClassification] = FourthCheck[interaction][ManualClassification] + 1
                ProcessedData.loc[len(ProcessedData)] = [Ticket, input, interaction, discipline, issue, FinalScore, Agent]

            
        except Exception as e:
            print('Exception - ',e)
            
    st.write('Fourth Check')
    FourthCheck
    st.write('Record Summary')
    RecordSummary
    # st.write('Vis Data')
    # VisData
    st.write('Processed Data')
    ProcessedData
    VisData.to_csv('VisData.csv')

    
    fig.add_trace(go.Scatter(
                
    x = VisData['Score'][VisData['Classification Match'] == 0] ,
    y = VisData['Interaction'][VisData['Classification Match'] == 0],
    mode = "markers",
    text = VisData['Query'][VisData['Classification Match'] == 0],
    name = 'Normal Tickets',
    textposition = 'bottom center',
    marker = { 'size':13, 'color':'black'}
        )
    )

    fig.add_trace(go.Scatter(
        x = VisData['Score'][VisData['Classification Match'] == 1],
        y = VisData['Interaction'][VisData['Classification Match'] == 1],
        mode = "markers",
        text = VisData['Query'][VisData['Classification Match'] == 1],
        name = 'Outliers Tickets',
        textposition = 'bottom center',
        marker = {'size':13, 'color':'red', 'symbol': 'diamond'}
        )
    )

        
    fig.update_layout(
        title="QMS System",
        xaxis_title="Ticket Score",
        yaxis_title="Interaction",
        legend_title="Types of Tickets",
        margin = {'t':100, 'b':100, 'l':150, 'r':200 },
        height = 700,
        width = 1400,
        font=dict(
            family="Courier New, monospace",
            size=15,
            color="RebeccaPurple"
        )
    )


    # display the plot
    fig.show()

    
