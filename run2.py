import openai_wrappers as model
import gsheets as gs
import streamlit as st
import numpy as np
import json
import time


SPREADSHEET_ID = '1cbU59j5_tkoflnlzT78QcBgHZDqC27yCCKsr5zvl8-I'
st.set_page_config(layout="wide")

print('---------------------------------------')
print('RUNNING')

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
abstracts = st.session_state.abstracts
prompts = st.session_state.prompts
st.session_state.p_score = int(records[index][5])
st.session_state.p_explanation = records[index][6]
cur_prompt = prompts[2][0]
new_prompt = cur_prompt


# Function to display record details
def show_record():
    record = records[index]
    st.write("PMID:", record[0])
    st.write("Title:", record[1])
    st.text_area("Abstract:", record[2], height=400)


def revert():
  print('resetting prompt')
  st.session_state.updated_prompt = cur_prompt


def update_score():
    system_instruction = st.session_state.updated_prompt + '\n\n<ABSTRACT>' + records[index][2] + '</ABSTRACT>'
    messages = [
          {"role": "system", "content": system_instruction}
    ]
    with st.spinner('Loading data...'):
      res = json.loads(model.generate(messages, 0))
    records[index][5] = res['score']
    records[index][6] = res['explanation']
    gs.update_scores(records)


def prev_item():
  if st.session_state.index > 0:
      st.session_state.index -= 1


def next_item():
  if st.session_state.index < len(records) - 1:
    st.session_state.index += 1


# Header and controls
col1, col2, col3, col4 = st.columns([4, 1, 1, 1])
with col1:
    st.header('DataTrove Training Module')
with col2:
    st.button('Previous', on_click=prev_item)
with col3:
    st.write(f"Record {st.session_state.index + 1} of {len(records)}")
with col4:
    st.button('Next', on_click=next_item)

# Record detail
show_record()
st.divider()

# Scoring section
col1, col2 = st.columns(2)
with col1:
  x = int(records[index][3])
  h_score = st.slider('Human score', 1, 10, x, disabled=False)
  h_explanation = st.text_area('Human explanation', records[index][4], disabled=False)
with col2:
  p_score = st.slider('Machine score', 1, 10, key='p_score', disabled=True)
  p_explanation = st.text_area('Machine explanation', key='p_explanation', disabled=True)

# Update and Redo Buttons
st.divider()
col1, col2, col3 = st.columns(3)
up = col1.button('Revert Prompt', on_click=revert)
rs = col2.button('Enhance Prompt')
rs = col3.button('Rescore', on_click=update_score)
st.divider()

# Prompts
ex = st.expander('Prompts')
with ex:
  col1, col2 = st.columns(2)
  with col1:
    st.text_area('Current', cur_prompt, height=800, disabled=True)  
  with col2:  
    updated_prompt = st.text_area('Updated', new_prompt, height=800, key='updated_prompt')
