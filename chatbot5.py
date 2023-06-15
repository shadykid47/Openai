import streamlit as st
import atomic as atom
import chatbot6

api_key = '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'
engine = 'text-davinci-003'



# Define the chat bot function
def chat_bot():
    st.title("Chat Bot")
    user_input = st.text_input("User Input", "")
    
    
    # Retrieve previous interaction from session state
    interaction_history = st.session_state.get("interaction_history", [])
    
    if st.button("Send"):
        # CODE TO CHECK WHETHER USER_INPUT IS GREETING, IF IT IS THEN RESPOND ACCORDINGLY WITH "HELLO, HOW MAY I HELP YOU" MESSAGE
        # GreetingQuestion = 'Is this statement a greeting. Respond in yes or no only.'
        # greeting = atom.GetReasoningCompletions(api_key, user_input, GreetingQuestion, engine, 5, 0).lower().strip()
        # print(greeting)        

        # if greeting == 'yes':
        #     # respond with a greeting
        #     question = """This is a conversation, your task is to generate a response assuming that you represent the customer care of this company and 
        #         response should help the user. also keep the responses short. Don't make the answer apologetic | ask for contact details if required. """
        #     temperature = 0.2
        #     tokens = round(len(user_input)*1.5)
        #     bot_response = atom.GetReasoningCompletions(api_key, user_input, question, engine, tokens, temperature)
        #     # Append current interaction to the history
        #     interaction_history.append({"User": user_input, "Bot": bot_response})
            


        # IF THE USER INPUT IS A QUESTION OR QUERY THEN GENERATE RESPONSE FROM OUR YEARGI SHEET
        QueryQuestion = 'Is this a query or a question or a complaint. Respond in yes or no only without punctuations.'
        # QueryQuestion  = 'is this a complaint'
        # query = atom.GetReasoningCompletions(api_key, user_input, QueryQuestion, engine, 50, 0).lower().strip()
        query = chatbot6.CohereGenerate(user_input + '|' + QueryQuestion).lower().strip()
        print(query)

        if query == 'no':
            print('query no')
            # respond with a greeting
            question = """This is a conversation, your task is to generate a response assuming that you represent the customer care of this company and 
                response should help the user. also keep the responses short. Ask for contact details if required. """
            temperature = 0
            tokens = round(len(user_input)*1.5)
            if len(user_input) == 1:
                tokens = 10
            bot_response = atom.GetReasoningCompletions(api_key, user_input, question, engine, tokens, temperature)
            
            # Append current interaction to the history
            interaction_history.append({"User": user_input, "Bot": bot_response})
            
        if query in ['yes', 'query', 'complaint', 'question']:
            print('query yes')
            
            # Process user input and generate bot response
            bot_response, getContact = generate_bot_response(user_input)
            
            # Append current interaction to the history
            interaction_history.append({"User": user_input, "Bot": bot_response})
            
            # Clear user input
            user_input = ""

            if getContact == 'yes':
                # Ask and store contact information
                print('yay')
                # Ask and store contact information
                contact_info_input = st.text_input("Please enter your contact information:")
                print('contact info input - ', contact_info_input)
                if contact_info_input:
                    print('yay yay')
                    contact_info = contact_info_input
                    st.session_state.contact_info = contact_info
                    # Print and display contact information
                    st.write(f"Contact Information: {contact_info}")
                    print(contact_info)
                    getContact = 'no'
                
        
            # # Ask and store contact information
            # if contact_info == "":
            #     contact_info_input = st.text_input("Please enter your contact information:")
            #     if contact_info_input:
            #         contact_info = contact_info_input
            #         st.session_state.contact_info = contact_info
                
        
    # Display interaction history
    for interaction in interaction_history :
        # st.text(f"{interaction['User']}")
        st.write('User - ' + interaction['User'])
        st.write('Bot - ' + interaction["Bot"])
    
    # st.text_area("Interaction History", interaction_text, height=300)
    
    # # Ask and store contact information
    # contact_info = st.text_input("Please enter your contact information:")
    # if contact_info:
    #     st.session_state.contact_info = contact_info

    # print(interaction_history)
    
    # Save the updated interaction history
    st.session_state.interaction_history = interaction_history

# Function to generate bot response based on user input
def generate_bot_response(user_input):
    api_key = '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'
    engine = 'text-davinci-003'
    temperature = 0.2
    count = 0

    question = """This is a conversation, your task is to generate a response assuming that you represent the customer care of this company and 
                response should help the user. also keep the responses short. Don't make the answer apologetic | ask for contact details if required. """
    
    question_contact = """| Is the sentence asking for contact information from the user. Give a response in yes or no only. |"""
    
    interaction_history = st.session_state.get("interaction_history", [])
    if count == 0:
        prompt = user_input
        count = 1
    else:
        prompt = ''
        for interaction in interaction_history:
            for person in ['User', 'Bot']:
                prompt +=  person + ' - ' + interaction[person] + '\n'

    # prompt = user_input
    tokens = round(len(prompt)*1.5)
    # response = atom.GetReasoningCompletions(api_key, prompt, question, engine, tokens, temperature)
    response = chatbot6.GenerateChatBotResponse(user_input)
    if 'Classification' in response.split(' '):
        response = atom.GetReasoningCompletions(api_key, response, question, engine, tokens, 0.2) 
    getContact = atom.GetReasoningCompletions(api_key, response, question_contact, engine, 5, 0)
            
    return response, getContact.lower().strip()

# Run the chat bot
if __name__ == "__main__":
    chat_bot()

