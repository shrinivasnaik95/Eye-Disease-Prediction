import streamlit as st
import pyrebase
from dotenv import load_dotenv
import os
import tensorflow as tf
from tensorflow.keras.applications.mobilenet_v3 import preprocess_input
import numpy as np
import tempfile
from recommendation import amd, cnv, csr, dme, dr, drusen, mh, normal
from mail_utils import send_recommendation_email_async
from recommendation import get_recommendation
@st.cache_resource
def load_model_cached():
    return tf.keras.models.load_model("model.h5", compile=False)

model = load_model_cached()
# Load environment variables
load_dotenv()
api_key = os.getenv("API_KEY")

# Firebase configuration
firebaseConfig = {
    "apiKey":os.getenv("API_KEY"),
    "authDomain": os.getenv("AUTH_DOMAIN"),
    "databaseURL": "",
    "projectId": os.getenv("PROJECT_ID"),
    "storageBucket":os.getenv("STORAGE_BUCKET"),
    "messagingSenderId": os.getenv("MESSAGING_SENDER_ID"),
    "appId": os.getenv("APP_ID")
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

def model_prediction(test_image_path):
    img = tf.keras.utils.load_img(test_image_path, target_size=(224, 224))
    x = tf.keras.utils.img_to_array(img)

    x = preprocess_input(x)   # important
    x = np.expand_dims(x, axis=0)

    predictions = model.predict(x)

    confidence = float(np.max(predictions) * 100)
    return np.argmax(predictions), confidence# return index of max element


# Initialize session state
if "user" not in st.session_state:
    st.session_state.user = None

# ---------------- AUTH SECTION ---------------- #
def login_page():
    st.title("🔐 Login / Sign Up")
    choice = st.selectbox("Select Action", ["Login", "Sign Up"])

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if choice == "Sign Up":
        password_confirm = st.text_input("Confirm Password", type="password")
        if st.button("Create Account"):
            if password != password_confirm:
                st.error("Passwords do not match.")
            elif len(password) < 6:
                st.error("Password must be at least 6 characters long.")
            else:
                try:
                    user = auth.create_user_with_email_and_password(email, password)
                    auth.send_email_verification(user['idToken'])
                    st.success("Account created! Verify your email before logging in.")
                except Exception as e:
                    st.error("Error creating account: " + str(e))

    elif choice == "Login":
        if st.button("Login"):
            try:
                user = auth.sign_in_with_email_and_password(email, password)
                user_info = auth.get_account_info(user['idToken'])
                verified = user_info['users'][0]['emailVerified']

                if not verified:
                    st.warning("Please verify your email before logging in.")
                else:
                    st.session_state.user = email
                    st.session_state.id_token=user['idToken']
                    st.success("Login successful!")
                    st.rerun()
            except Exception:
                st.error("Invalid credentials. Please try again.")



# ---------------- MAIN APP SECTION ---------------- #
def main_app():
    st.sidebar.title(f"Welcome, {st.session_state.user}")
    app_mode = st.sidebar.selectbox("Select Page", ["Home", "About", "Disease Identification"])

    # Logout button
    if st.sidebar.button("Logout"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.success("You have been logged out.")
        st.rerun()

    # --- Pages ---
    if app_mode == "Home":
        st.markdown("""
    ## **OCT Retinal Analysis Platform**

#### **Welcome to the Retinal OCT Analysis Platform**

**Optical Coherence Tomography (OCT)** is a powerful imaging technique that provides high-resolution cross-sectional images of the retina, allowing for early detection and monitoring of various retinal diseases. Each year, over 30 million OCT scans are performed, aiding in the diagnosis and management of eye consitions that can lead to vision loss, such as Choroidal Neovascularization (CNV), Diabetic Macular Edema (DME), and Age-related Macular Degeneration (AMD).

##### **Why OCT Matters**
Oct is a crucial tool in opthalmology, offering non-invasive imaging to detect retinal abnormalities. On this platform, we aim to streamline the analysis and interpretation of these scans, reducing the time burden on medical professionals and increasing diagnostic accuracy through advanced automated analysis.

---

#### **Key Features of the Platform**

- **Automated Image Analysis**:Our platform uses state-of-the-art machine learning models to classify OCT images into distinct categories: **AMD**, **CNV**, **CSR**, **DME**, **DR**, **DRUSEN**, **MH**, and **NORMAL**.
- **Cross-Sectional Retinal Imaging**: Examine high-quality images showcasing both normal retinas and various pathologies,helping doctors make informed clinical decisions.
- **Streamlined Workflow**: Upload, Analyze, and Review OCT scans in a few easy steps.

---

#### Understanding Retinal Diseases through OCT ####

1. **Age-Related Macular Degeneration (AMD)**
   - Drusen deposits with RPE irregularity and possible subretinal fluid.

2. **Choroidal Neovascularization (CNV)**
   - Neovascular membrane with subretinal fluid.

3. **Central Serous Retinopathy (CSR)**
   - Serous detachment of the neurosensory retina with subretinal fluid.

4. **Diabetic Macular Edema (DME)**
   - Retinal thickening with intraretinal fluid.

5. **Diabetic Retinopathy (DR)**
   - Intraretinal hemorrhages, microaneurysms, and macular edema.

6. **Drusen (Early AMD)**
   - Presence of multiple drusen deposits beneath the RPE.

7. **Macular Hole (MH)**
   - Full-thickness retinal defect at the fovea.

8. **Normal Retina**
   - Preserved foveal contour, absence of fluid or edema.

---


#### **About the Dataset**

Our dataset consists of **25,000 high-resolution OCT images** (JPEG format) organized into **train, test, and validation** sets, split into four primary categories:
- **AMD**
- **CNV**
- **CSR**
- **DME**
- **DR**
- **DRUSEN**
- **MH**
- **NORMAL**

Each image has undergone multiple layers of expert verification to ensure accuracy in disease classification. The images were obtained from various renowned medical centers worldwide and span across a diverse patient population, ensuring comprehensive coverage of different retinal conditions.

---

#### **Get Started**

- **Upload OCT Images**: Begin by uploading your OCT scans for analysis.
- **Explore Results**: View categorized scans and detailed diagnostic insights.
- **Learn More**: Dive deeper into the different retinal diseases and how OCT helps diagnose them.

---
""")

    elif app_mode == "About":
        st.header("About")
        st.markdown("""
                #### About Dataset
                Retinal optical coherence tomography (OCT) is an imaging technique used to capture high-resolution cross sections of the retinas of living patients. 
                Approximately 30 million OCT scans are performed each year, and the analysis and interpretation of these images takes up a significant amount of time.

                (A) (Far left) Choroidal Neovascularization (CNV) with neovascular membrane (white arrowheads) and associated subretinal fluid (arrows). 
                (Middle left) Diabetic Macular Edema (DME) with retinal-thickening-associated intraretinal fluid (arrows). 
                (Middle right) Multiple Drusen (arrowheads) present in early AMD. 
                (Far right) Normal retina with preserved foveal contour and absence of any retinal fluid/edema.

                ---

                #### Content
                The dataset is organized into 3 folders (train, test, val) and contains subfolders for each image category 
                (**NORMAL, CNV, DME, DRUSEN, AMD, CSR, DR, MH**).  

                There are a total of **20,000 OCT images (JPEG format)** across all disease categories.  
                Each image file is labeled as:  
                **(disease)-(randomized patient ID)-(image number)**  
                and stored in its respective folder.

                #### Dataset Source and Annotation
                OCT images (Spectralis OCT, Heidelberg Engineering, Germany) were collected from multiple ophthalmology centers including:  
                - Shiley Eye Institute, University of California San Diego  
                - California Retinal Research Foundation  
                - Medical Center Ophthalmology Associates  
                - Shanghai First People’s Hospital  
                - Beijing Tongren Eye Center  

                **Timeframe:** July 1, 2013 – March 1, 2017  

                Each image underwent a **three-tier grading process** for label verification:  
                - **Tier 1:** Undergraduate and medical students performed initial quality control.  
                - **Tier 2:** Four ophthalmologists independently graded the images.  
                - **Tier 3:** Two senior retinal specialists (20+ years experience) verified final labels.  

                A separate validation subset (993 scans) was double-graded and disagreements were resolved by a senior retinal specialist to ensure data reliability.

                ---
                """)

    elif app_mode == "Disease Identification":
        st.header("Upload an OCT Image for Disease Prediction")
        test_image = st.file_uploader("Upload your Image:")

        if test_image is not None:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
                tmp_file.write(test_image.read())
                temp_file_path = tmp_file.name

            if st.button("Predict"):
                with st.spinner("Please wait..."):
                    result_index,confidence = model_prediction(temp_file_path)
                    class_name = ['AMD', 'CNV', 'CSR', 'DME', 'DR', 'DRUSEN', 'MH',  'NORMAL']
                    predicted_class = class_name[result_index]

                # Show prediction result
                st.success(f"✅ Model predicts it's a *{predicted_class}* image.")
                st.info(f"Prediction Confidence: {confidence:.2f}%")
                st.image(test_image)

                # Show disease info
                with st.expander("Learn More"):
                    if predicted_class == "AMD":
                        st.write("OCT scan shows *Age-Related Macular Degeneration (AMD)* — irregular retinal layers with drusen and pigment epithelial detachment.")
                        
                        st.markdown(amd)
                    elif predicted_class == "CNV":
                        st.write('''
                    OCT scan showing *CNV with subretinal fluid.*
                ''')
                        st.markdown(cnv)
                    elif predicted_class == "CSR":
                        st.write("OCT scan shows *Central Serous Retinopathy (CSR)* — fluid accumulation under the retina forming a dome-shaped detachment.")
                        st.markdown(csr)
                    elif predicted_class == "DME":
                        st.write('''
                    OCT scan showing *DME with retinal thickening and intraretinal fluid.*
                ''')
                        st.markdown(dme)
                    elif predicted_class == "DR":
                        st.write("OCT scan shows *Diabetic Retinopathy (DR)* — microaneurysms and hemorrhages indicating retinal blood vessel damage.")
                        st.markdown(dr)
                    elif predicted_class == "DRUSEN":
                        st.write('''
                    OCT scan showing *drusen deposits in early AMD.*
                ''')
                        st.markdown(drusen)
                    elif predicted_class == "MH":
                        st.write("OCT scan shows *Macular Hole (MH)* — a central defect in the macula leading to loss of central vision.")
                        st.markdown(mh)
                    elif predicted_class == "NORMAL":
                        st.write('''
                    OCT scan showing a *normal retina with preserved foveal contour.*
                ''')
                        st.markdown(normal)
                        

                # ✅ Send recommendation email
                recommendation_text = get_recommendation(predicted_class)
                user_email = st.session_state.user  # logged-in user's email
                user_name = user_email.split("@")[0].capitalize()  # simple name extraction

                send_recommendation_email_async(
                    to_email=user_email,
                    subject=f"OCT Disease Prediction: {predicted_class}",
                    recommendation_text=recommendation_text,
                    user_name=user_name
                )

                st.info(f"📧 Recommendation has been sent to {user_email}")
        else:
            st.warning("Please upload an image before predicting.")




# ---------------- RUN APP ---------------- #
if st.session_state.user:
    main_app()
else:
    login_page()
