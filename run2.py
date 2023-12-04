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
st.session_state.h_score = int(records[index][3])
st.session_state.h_explanation = records[index][4]
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


def h_score_change():
  print('val:', st.session_state.h_score)
  records[index][3] = st.session_state.h_score
  gs.update_scores(records)


def h_explanation_change():
  print('h_explanation_change:', st.session_state.h_explanation)
  records[index][4] = st.session_state.h_explanation
  gs.update_scores(records)


def get_prompt_update():
    print('updating')

    p_template = '''
        Below, you will see a prompt, a scientific abstract, a human_score and a machine_score. The purpose of the prompt is to instruct a language model to score a scientific abstract the same way a human would. If the prompt is perfectly formed, then it should prompt a language model to return the same score as the human scorer for any given abstract. So if you see that the human_score and the machine_score below are very similar then the prompt did a good job for this abstract. But if the human_score and the machine_score are not very close then the prompt should be updated so that the model score can come closer to the human score.

        When updating the prompt this way, you want to try and focus on changes that make the model scoring behavior more similar to the human scoring behavior. So, please look for contradictions between the model explanations and the prompt instructions and focus on reducing them. The prompt should be updated to better align the machine's scoring behavior with the human scorer's rationale. 

        Please decide whether or not the prompt should be updated. If not, simply reply NO NEED FOR CHANGE. If so, please suggest specific changes to the prompt so that it better captures the intention of the human scorer.
    '''

    abstract = records[index][2]
    human_score = {"score": records[index][3], "explanation": records[index][4]}
    machine_score = {"score": records[index][5], "explanation": records[index][6]}
    prompt = cur_prompt

    system_instruction = p_template \
      + '\n\n<ABSTRACT>' + abstract + '</ABSTRACT>' \
      + '\n\n<HUMAN_SCORE>' + json.dumps(human_score) + '</HUMAN_SCORE>' \
      + '\n\n<MACHINE_SCORE>' + json.dumps(machine_score) + '</MACHINE_SCORE>' \
      + '\n\n<PROMPT>' + prompt + '</PROMPT>'
    messages = [
          {"role": "system", "content": system_instruction}
    ]
    with st.spinner('Loading data...'):
      # res = json.loads(model.generate(messages, 0))
      res = model.generate(messages, 0)
    st.session_state.rec = res


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
  st.slider('Human score', 1, 10, key='h_score', on_change=h_score_change, disabled=False)
  h_explanation = st.text_area('Human explanation', on_change=h_explanation_change, height=300, key='h_explanation', disabled=False)
with col2:
  st.slider('Machine score', 1, 10, key='p_score', disabled=True)
  p_explanation = st.text_area('Machine explanation', height=300, key='p_explanation', disabled=True)

# Update and Redo Buttons
st.divider()
col1, col2, col3 = st.columns(3)
up = col1.button('Revert Prompt', on_click=revert)
rs = col2.button('Enhance Prompt', on_click=get_prompt_update)
rs = col3.button('Rescore', on_click=update_score)
st.divider()

# Prompts
st.text_area('Prompt Recommendations', 'TBD', key='rec')
ex = st.expander('Prompts')
with ex:
  col1, col2 = st.columns(2)
  with col1:
    st.text_area('Current', cur_prompt, height=800, disabled=True)  
  with col2:  
    updated_prompt = st.text_area('Updated', new_prompt, height=800, key='updated_prompt')
