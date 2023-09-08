import os.path
import subprocess
import sys

s = """
import pygwalker as pyg
from streamlit.components import v1 as components
import streamlit as st
import pandas as pd

# Adjust the width of the Streamlit page
st.set_page_config(
    page_title="a simple data analyzer",
    layout="wide"
)

# Add Title
st.title("a simple data analyzer")

uploaded_file = st.file_uploader("Choose a .csv")
if uploaded_file is not None:
    # Can be used wherever a "file-like" object is accepted:
    df = pd.read_csv(uploaded_file, encoding='utf-8')

    # Generate the HTML using Pygwalker
    pyg_html = pyg.walk(df, return_html=True)

    # Embed the HTML into the Streamlit app
    components.html(pyg_html, height=1000, scrolling=True)

"""
lit_py_path = os.path.join(sys._MEIPASS, 'lit.py')
with open(lit_py_path, 'wb') as f:
    f.write(s.encode('utf-8'))

subprocess.run(['streamlit', 'run', lit_py_path])
