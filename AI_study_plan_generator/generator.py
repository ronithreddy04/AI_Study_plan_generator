from datetime import datetime, timedelta
from fpdf import FPDF

def parse_input(raw_input):
    lines = raw_input.strip().split("\n")
    topics = []
    for line in lines:
        if "-" in line:
            topic, hours = line.rsplit("-", 1)
            try:
                topics.append((topic.strip(), int(hours.strip())))
            except ValueError:
                continue
    return topics

def generate_study_plan(topics, start_date, hours_per_day):
    plan = []
    current_date = datetime.strptime(start_date, "%Y-%m-%d")
    for topic, total_hours in topics:
        while total_hours > 0:
            allocated = min(hours_per_day, total_hours)
            plan.append({
                "date": current_date.strftime("%Y-%m-%d"),
                "topic": topic,
                "hours": allocated
            })
            total_hours -= allocated
            current_date += timedelta(days=1)
    return plan

def generate_pdf(plan):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Study Plan", ln=True, align='C')
    pdf.ln(10)
    for entry in plan:
        line = f"{entry['date']}: {entry['topic']} - {entry['hours']} hours"
        pdf.cell(200, 10, txt=line, ln=True)
    output_path = "study_plan.pdf"
    pdf.output(output_path)
    return output_path