import streamlit as st
import atomic as atom

# Define the chat bot function
def chat_bot():
    st.title("Chat Bot")
    user_input = st.text_input("User Input", "")
    
    # Retrieve previous interaction from session state
    interaction_history = st.session_state.get("interaction_history", [])
    
    if st.button("Send"):
    
        # Process user input and generate bot response
        bot_response = generate_bot_response(user_input)
        
        # Append current interaction to the history
        interaction_history.append({"User": user_input, "Bot": bot_response})
        st.session_state.interaction_history = interaction_history
        
        # Clear user input
        user_input = ""
    
    # Display interaction history
    for interaction in interaction_history :
        # st.text(f"{interaction['User']}")
        st.write('User - ' + interaction['User'])
        st.write('Bot - ' + interaction["Bot"])
        # st.text_area("", 'User - ' + interaction['User'] + '\n' + 'Bot - ' + interaction["Bot"])
    
    # Save the updated interaction history
    st.session_state.interaction_history = interaction_history

# Function to generate bot response based on user input
def generate_bot_response(user_input):
    api_key = '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'
    engine = 'text-davinci-003'
    temperature = 0.2
    count = 0

    question = """This is a conversation, your task is to generate a response assuming that you represent the customer care of this company and 
                response should help the user. also keep the responses short. Don't make the answer apologetic' """
    
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
    response = atom.GetReasoningCompletions(api_key, prompt, question, engine, tokens, temperature)
    return response

# Run the chat bot
if __name__ == "__main__":
    chat_bot()
