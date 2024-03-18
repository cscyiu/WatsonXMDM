import streamlit as st
from ibm_watson_machine_learning.foundation_models import Model
import json
import os

st.title('IBM Data and AI: MDM and watsonx.ai Demo 🤖')
st.caption("🚀 A chatbot powered by watsonx.ai 🚀")

with st.sidebar:
    watsonx_api_key = st.text_input("Watsonx API Key", key="watsonx_api_key", value=os.environ.get("API_KEY"), type="password")
    watsonx_url = st.text_input("Watsonx URL", key="watsonx_url", value="https://us-south.ml.cloud.ibm.com", type="default")
    #TODO: change this to a select box with more than one model
    watsonx_model = st.text_input("Model", key="watsonx_model", value="meta-llama/llama-2-70b-chat", type="default")
    #watsonx_model = st.selectbox("watsonx.ai Foundation Model:?", ("FLAN_T5_XL", 'FLAN_T5_XXL', 'FLAN_UL2', 'GPT_NEOX', 'GRANITE_13B_CHAT', 'GRANITE_13B_CHAT_V2', 'GRANITE_13B_INSTRUCT', 'GRANITE_13B_INSTRUCT_V2', 'LLAMA_2_13B_CHAT', 'LLAMA_2_70B_CHAT', 'MIXTRAL_8X7B_INSTRUCT_V01_Q', 'MPT_7B_INSTRUCT2', 'MT0_XXL', 'STARCODER', 'ELYZA_JAPANESE_LLAMA_2_7B_INSTRUCT')) 

    watsonx_project_id = st.text_input("Watsonx Project ID", key="watsonx_project_id", value=os.environ.get("Project_ID"), type="default")
    watsonx_model_params = st.text_input("Params", key="watsonx_model_params", value='{"decoding_method":"sample", "max_new_tokens":200, "temperature":0.5}', type="default" )

if not watsonx_api_key:
    st.info("Please add your watsonx API key to continue.")
else :
    st.info("setting up to use: " + watsonx_model)
    my_credentials = { 
        "url"    : watsonx_url, 
        "apikey" : watsonx_api_key
    }
    params = json.loads(watsonx_model_params)      
    project_id  = os.environ.get("PROJECT_ID")
    #project_id  = watsonx_project_id
    space_id    = None
    verify      = False
    model = Model( watsonx_model, my_credentials, params, project_id, space_id, verify )   
    if model :
        st.info("done")
 
if 'messages' not in st.session_state: 
    st.session_state.messages = [{"role": "assistant", "content": "How can I help you?"}] 

for message in st.session_state.messages: 
    st.chat_message(message['role']).markdown(message['content'])

prompt = st.chat_input('Pass Your Prompt here')

if prompt: 
    st.chat_message('user').markdown(prompt)
    st.session_state.messages.append({'role':'user', 'content':prompt})
    if model :
        response = model.generate_text(prompt)
    else :
        response = "You said: " + prompt
    
    st.chat_message('assistant').markdown(response)
    st.session_state.messages.append({'role':'assistant', 'content':response})
