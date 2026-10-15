import os

print("Generating content plan...")
os.system("python generate_content_plan.py")

print("Generating charts...")
os.system("python tools/chart_generator.py")

print("Generating PowerPoint...")
os.system("python tools/ppt_generator.py")

print("✅ Pipeline completed")