import os
import requests
import streamlit as st

API_URL = os.getenv("OPDAI_API_URL", "https://opdai.onrender.com")

st.set_page_config(page_title="OPDAI", page_icon="🩺", layout="wide")
st.title("🩺 OPDAI — AI-assisted OPD Intake")

if "patient_id" not in st.session_state:
    st.session_state.patient_id = None
if "token" not in st.session_state:
    st.session_state.token = None

with st.sidebar:
    st.header("Doctor Login")
    email = st.text_input("Email", value="doctor@example.com")
    password = st.text_input("Password", type="password", value="ChangeMe123!")
    if st.button("Login"):
        r = requests.post(f"{API_URL}/auth/login", json={"email": email, "password": password}, timeout=30)
        if r.ok:
            st.session_state.token = r.json()["access_token"]
            st.success("Logged in")
        else:
            st.error(r.text)

st.header("1. Patient Intake")
with st.form("patient_form"):
    name = st.text_input("Patient name")
    mobile = st.text_input("Mobile")
    symptoms = st.text_area("Symptoms", height=140)
    submitted = st.form_submit_button("Create patient")

if submitted:
    r = requests.post(
        f"{API_URL}/patient",
        json={"name": name, "mobile": mobile, "symptoms": symptoms},
        timeout=30,
    )
    if r.ok:
        data = r.json()
        st.session_state.patient_id = data["patient_id"]
        st.success(f"Patient created: {data['patient_id']}")
    else:
        st.error(r.text)

patient_id = st.session_state.patient_id

if patient_id:
    st.divider()
    st.header("2. Consent")
    st.write(f"Patient ID: `{patient_id}`")
    if st.button("Give consent"):
        r = requests.post(
            f"{API_URL}/consent",
            json={"patient_id": patient_id, "consent_given": True},
            timeout=30,
        )
        if r.ok:
            st.success("Consent recorded")
        else:
            st.error(r.text)

    st.header("3. Upload prescription")
    file = st.file_uploader("PDF/JPG/PNG", type=["pdf", "jpg", "jpeg", "png"])
    if file and st.button("Upload"):
        r = requests.post(
            f"{API_URL}/upload/prescription",
            params={"patient_id": patient_id},
            files={"file": (file.name, file.getvalue(), file.type)},
            timeout=60,
        )
        if r.ok:
            st.success("Prescription uploaded")
        else:
            st.error(r.text)

    st.divider()
    st.header("4. Doctor Dashboard / AI Summary")
    if not st.session_state.token:
        st.info("Log in as a doctor from the sidebar to generate the AI summary.")
    else:
        if st.button("Generate AI summary"):
            headers = {"Authorization": f"Bearer {st.session_state.token}"}
            r = requests.get(f"{API_URL}/patient/{patient_id}", timeout=30)
            if not r.ok:
                st.error(r.text)
            else:
                pdata = r.json()
                sr = requests.post(
                    f"{API_URL}/summary",
                    headers=headers,
                    json={
                        "patient_id": patient_id,
                        "symptoms": pdata["symptoms"],
                        "prescription_text": "",
                    },
                    timeout=120,
                )
                if sr.ok:
                    result = sr.json()
                    st.subheader("AI-generated summary")
                    st.markdown(result["summary"])
                    st.warning("AI-generated summary. Requires physician review.")
                else:
                    st.error(sr.text)
