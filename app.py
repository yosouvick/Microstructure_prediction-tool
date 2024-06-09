# import streamlit as st
# import google.generativeai as genai
# import os
# from dotenv import load_dotenv
# from PIL import Image
# load_entry_point() #loading all the environment variables
### Health Management APP
from dotenv import load_dotenv

load_dotenv() ## load all the environment variables

import streamlit as st
import os
import google.generativeai as genai
from PIL import Image
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
## Function to load Google Gemini Pro Vision API And get response

def get_gemini_response(input_prompt,image):
    model=genai.GenerativeModel('gemini-pro-vision')
    response=model.generate_content([input_prompt,image[0]])
    return response.text

def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")
    
##initialize our streamlit app
developer_name="Anurag Roy"
st.set_page_config(page_title="Microstructure Prediction App")

st.header("Gemini Microstructure App")
st.text(f'''Welcome to the Microstructure Prediction App!
                                                    --- Brewed by {developer_name}''')
# st.subheader(f"Brewed by {developer_name}")
input=st.text_input("Input Prompt: ",key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
st.markdown(
    """
    ## About the App

    This app analyzes microstructure from uploaded images and predicts the corresponding phases present in the sample.

    ## How to Use

    1. Enter an input prompt.
    2. Upload an image.
    3. Click the 'Predict' button.

    Enjoy exploring microstructure insights!
    """
)

# Additional information using st.write
st.write("For any inquiries, please contact:", developer_name, "- anuragroy2002.ju.mme@gmail.com")
image=""   
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)


submit=st.button("Predict")

input_prompt="""
Perform an in-depth analysis of the microstructure captured in the uploaded image. Identify and characterize the distinct phases present, such as :
ferrite cementite, martensite, and spheroidal graphite flakes etc.
Additionally, provide detailed insights into the composition and distribution of each identified phase.

Furthermore, go beyond phase identification by extracting crucial mechanical properties from the microstructure. Include parameters such as hardness, tensile strength, and any other relevant mechanical attributes. Present the mechanical properties alongside their respective percentages within the sample.

In addition to phase details and mechanical properties, explore the probable elemental constituents contributing to the microstructure. Include elements such as 
copper (Cu), zinc (Zn), aluminum (Al), carbon (C), and iron (Fe) etc.
Provide insights into the probable concentration of each element within the sample.
"""

## If submit button is clicked

if submit:
    image_data=input_image_setup(uploaded_file)
    response=get_gemini_response(input_prompt,image_data)
    st.subheader("The Response is")
    st.write(response)

