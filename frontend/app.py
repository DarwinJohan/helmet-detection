#pip install streamlit requests

import streamlit as st
import requests

st.title("Helmet Detection Web App")

uploaded_file = st.file_uploader("Upload Image", type=["jpg","jpeg","png"])

if uploaded_file is not None:
    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

    if st.button("Detect Helmet"):
        files = {"file": uploaded_file.getvalue()}
        response = requests.post("http://localhost:8000/detect", files=files)

        st.subheader("Detection Result:")
        st.json(response.json())
