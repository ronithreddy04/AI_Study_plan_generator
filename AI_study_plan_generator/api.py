from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from generator import parse_input, generate_study_plan, generate_pdf

app = FastAPI()

# Allow CORS for Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or specify only your Streamlit frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class StudyRequest(BaseModel):
    topics: str
    start_date: str  # ✅ ensure it's string
    daily_study_hours: int

@app.post("/generate")
def generate(request: StudyRequest):
    topic_list = parse_input(request.topics)
    plan = generate_study_plan(topic_list, request.start_date, request.daily_study_hours)
    pdf_path = generate_pdf(plan)
    return {"message": "Study plan generated successfully", "pdf_path": pdf_path, "plan": plan}
