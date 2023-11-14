import gsheets as gs
import streamlit as st
import numpy as np

SPREADSHEET_ID = '1cbU59j5_tkoflnlzT78QcBgHZDqC27yCCKsr5zvl8-I'

print('---------------------------------------')
print('RUNNING')
print('---------------------------------------')
if 'loaded' not in st.session_state:
  print('loading')
  st.session_state['loaded'] = True
  gs.google_auth(SPREADSHEET_ID)
  st.session_state.index = 0
  st.session_state.records = gs.get_examples()
  st.session_state.prompts = gs.get_prompts()
else:
    print('loaded')
records = st.session_state.records
index = st.session_state.index
prompts = st.session_state.prompts

# Function to display record details
def show_record(record):
    st.write("PMID:", record[0])
    st.write("Title:", record[1])
    st.write("Abstract:", record[2])

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

show_record(records[index])
col1, col2 = st.columns(2)
with col1:
  h_score = st.slider('Human score', 1, 10, int(records[index][3]))
  h_explanation = st.text_area('Human explanation', records[index][4])
with col2:
  p_score = st.slider('Machine score', 1, 10, 0)
  p_explanation = st.text_area('Machine explanation')
  st.write(p_explanation)

st.write(prompts[2])