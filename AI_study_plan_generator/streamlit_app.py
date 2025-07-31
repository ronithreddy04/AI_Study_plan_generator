import streamlit as st
import requests
import datetime

st.title("AI Study Plan Generator")
st.markdown("Enter topics with estimated hours (one per line, e.g., `Python Basics - 5`)")

topics_input = st.text_area("Study Topics")

start_date = st.date_input("Start Date", datetime.date.today())
daily_hours = st.number_input("Hours you can study per day", min_value=1, max_value=24, value=2)

if st.button("Generate Study Plan"):
    if not topics_input.strip():
        st.warning("Please enter at least one topic.")
    else:
        payload = {
            "topics": topics_input,
            "start_date": str(start_date),
            "daily_study_hours": daily_hours
        }

        try:
            response = requests.post("http://127.0.0.1:8000/generate", json=payload)
            if response.status_code == 200:
                data = response.json()
                st.success(data["message"])

                with st.expander("📅 View Plan"):
                    for entry in data["plan"]:
                        st.write(f"📆 {entry['date']}: **{entry['topic']}** — {entry['hours']} hrs")

                with open(data["pdf_path"], "rb") as f:
                    st.download_button("📄 Download PDF", f, file_name="study_plan.pdf")
            else:
                st.error("Something went wrong: " + response.text)
        except Exception as e:
            st.error(f"Connection error: {e}")