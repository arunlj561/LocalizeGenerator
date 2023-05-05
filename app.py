import streamlit as st
import os
import googletrans
from googletrans import Translator
import pathlib
from os import listdir
from os.path import isfile, join
import requests

st.write("""
# Swift Localize file Convertor
""")

trans = googletrans.LANGCODES

destination_options = trans
selected_destination_option = st.selectbox("Select Destination Language option", destination_options)
st.write("You selected:", selected_destination_option)
dest_value = trans[selected_destination_option]

uploaded_file = st.file_uploader( "Upload Source Localizable.strings file", key="FileUploader")

uploadDisable = True
if uploaded_file is not None :
    if ".strings" in  uploaded_file.name:
        bytes_data = uploaded_file.getvalue()
        data = uploaded_file.getvalue().decode('utf-8').splitlines()         
        st.session_state["preview"] = ''
        for i in range(0, min(5, len(data))):
            st.session_state["preview"] += data[i]        
    else :
        uploadDisable = True
        st.session_state["preview"] = "File should be .strings file"
    
preview = st.text_area("File Preview", "", height=150, key="preview")
upload_state = st.text_area("Upload State", "", key="upload_state") 

def convert():
    fileStr = 'data/Localizable.strings'    
    if pathlib.Path(fileStr).is_file():                
        with open(fileStr, "rb") as file:
            file_content = file.read()
            file_name = os.path.basename(fileStr)            
            data = file_content.decode('utf-8').split('\n')                
            final = ''
            detector = Translator()
            for line in data:
                count = len(line.split('='))    
                if  count > 1:
                    source_text = str(str(line.split('=')[1]))                 
                    dec_lan = detector.translate(source_text, dest=dest_value)                
                    final += str(str(line.split('=')[0])) + " = " + dec_lan.text + "\n"

            f = open("user/Localizable.strings",'w')
            f.write(str(final))
            f.close()                
        st.session_state["upload_state"] = "Converted" + " successfully!"
    else:
        st.session_state["upload_state"] = "Failed to Convert File"

def upload():
    if uploaded_file is None:
        st.session_state["upload_state"] = "Upload a file first!"
    else:
        if ".strings" in  uploaded_file.name:
            data = uploaded_file.getvalue().decode('utf-8')
            parent_path = pathlib.Path(__file__).parent.parent.resolve()           
            save_path = os.path.join(parent_path, "LocalizeGenerator/data")
            complete_name = os.path.join(save_path, uploaded_file.name)
            print(complete_name)        
            destination_file = open(complete_name, "w")
            destination_file.write(data)
            destination_file.close()
            st.session_state["upload_state"] = "Saved Successfully!"   
        else :
            st.session_state["upload_state"] = "File not in expected format"

st.button("Upload file", on_click=upload)
if str(st.session_state["upload_state"]) == 'Saved Successfully!':
    st.button("Convert", on_click=convert)

if str(st.session_state["upload_state"]) == 'Converted successfully!':        
    fileStr = 'user/Localizable.strings'    
    if pathlib.Path(fileStr).is_file():                
        with open(fileStr, "rb") as file:
            file_content = file.read()
            file_name = os.path.basename(fileStr)
            st.download_button(label="Click to Download", data=file_content, file_name=file_name)            