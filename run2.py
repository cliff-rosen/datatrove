import gsheets as gs
import streamlit as st
import numpy as np
import time

SPREADSHEET_ID = '1cbU59j5_tkoflnlzT78QcBgHZDqC27yCCKsr5zvl8-I'
st.set_page_config(layout="wide")

print('---------------------------------------')
print('RUNNING')
print('---------------------------------------')

if 'loaded' not in st.session_state:
  print('loading')
  gs.google_auth(SPREADSHEET_ID)
  st.session_state.index = 0
  st.session_state.records = gs.get_examples()
  st.session_state.prompts = gs.get_prompts()
  st.session_state.abstracts = gs.get_abstracts()
  st.session_state['loaded'] = True
else:
    print('loaded')

records = st.session_state.records
index = st.session_state.index
prompts = st.session_state.prompts
cur_prompt = prompts[2][0]
new_prompt = cur_prompt
abstracts = st.session_state.abstracts
      

# Function to display record details
def show_record(record):
    st.write("PMID:", record[0])
    st.write("Title:", record[1])
    st.text_area("Abstract:", record[2], height=300)


def reset():
  print('resetting prompt')
  st.session_state.updated_prompt = cur_prompt

def update_score():
    system_instruction = st.session_state.updated_prompt + '\n\n<ABSTRACT>' + records[index][2] + '</ABSTRACT>'
    messages = [
          {"role": "system", "content": system_instruction},
          {"role": "user", "content": "Hello!"}
    ]

# Navigation buttons and index display
col1, col2, col3 = st.columns([1, 1, 2])
with col1:
    if st.button('Previous'):
        if st.session_state.index > 0:
            st.session_state.index -= 1
with col2:
    if st.button('Next'):
        if st.session_state.index < len(records) - 1:
            st.session_state.index += 1
with col3:
    st.write(f"Record {st.session_state.index + 1} of {len(records)}")

# Record detail
show_record(records[index])

# Scoring section
col1, col2 = st.columns(2)
with col1:
  h_score = st.slider('Human score', 1, 10, int(records[index][3]))
  h_explanation = st.text_area('Human explanation', records[index][4])
with col2:
  p_score = st.slider('Machine score', 1, 10, 0, key='p_score')
  p_explanation = st.text_area('Machine explanation', key='p_explanation')

# Update and Redo Buttons
st.divider()
up = st.button('update prompt')
rs = st.button('redo score', on_click=update_score)

# Prompts
col1, col2 = st.columns(2)
with col1:
  st.text_area('current', cur_prompt, height=800, disabled=True)  
with col2:  
  updated_prompt = st.text_area('updated', new_prompt, height=800, key='updated_prompt')
reset = st.button('reset', on_click=reset)
