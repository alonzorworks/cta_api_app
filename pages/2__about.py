import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="About Page",
    page_icon="📘",
)

#Image In Sidebar 
with st.sidebar.container():
    image = Image.open(r"images/pictures/ahead_transparent_edit2.png")  
    st.image(image, use_column_width=True)


st.header("About This Project 📘")
st.write("This project utilizes google maps and CTA APIs to enable its functionality. This project was created to help an intern with her project idea. More features will likely be added by the intern in a separate repository.")

st.write("This project was created by Alonzo. He is an Associate Technical Consultant at AHEAD.")

st.subheader("About AHEAD")
st.write("AHEAD builds platforms for digital business. By stitching together advances in Cloud, Automation, Operations, Security and DevOps, we help clients deliver on the promise of digital transformation.")

ahead_logo = Image.open(r"images/pictures/ahead_logo.jpg")  
st.image(ahead_logo, use_column_width=True)
