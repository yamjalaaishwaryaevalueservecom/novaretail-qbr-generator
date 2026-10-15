# NovaRetail Executive QBR Generator

## Project Overview

NovaRetail Executive QBR Generator is an AI-powered business reporting solution that automates the creation of Quarterly Business Review (QBR) presentations from business performance data.

The solution combines:

- Google Agent Development Kit (ADK)
- Gemini LLM
- Human-in-the-Loop (HITL) review workflow
- Streamlit user interface
- Automated chart generation
- Automated PowerPoint generation

The system analyzes a business dataset, generates executive insights using AI, enables human review and approval, and produces a presentation-ready QBR deck.

## Business Problem

Preparing Quarterly Business Reviews is often a manual and time-consuming process involving:

- Data analysis
- KPI identification
- Insight generation
- Executive storytelling
- Presentation creation

The objective of this project is to automate these steps while ensuring human oversight before publication.

## Solution Architecture

```text
Excel Dataset
      ↓
Data Analysis Engine
      ↓
Google ADK Agent
      ↓
AI Content Generation
      ↓
Human Review & Approval
      ↓
Chart Generation
      ↓
PowerPoint Generation
      ↓
NovaRetail_QBR_Final.pptx
```

## Installation

```bash
pip install -r requirements.txt
```

## Run the Project

### Launch Streamlit

```bash
streamlit run app.py
```

### Generate Content

```bash
python generate_content_plan.py
```

### Generate Charts

```bash
python tools/chart_generator.py
```

### Generate PPT

```bash
python tools/ppt_generator.py
```

### Run End-to-End Pipeline

```bash
python run_pipeline.py
```

## Human-in-the-Loop Workflow

```text
Generate Content
      ↓
Review Content
      ↓
Modify Insights
      ↓
Approve Content
      ↓
Generate PPT
```

## Technologies Used

- Google ADK
- Gemini
- Streamlit
- Pandas
- Matplotlib
- python-pptx
- Python Dotenv

## Author

Yamjala Aishwarya
