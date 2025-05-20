import os
from parser import parse_resume, parse_job_description
from matcher import match_resume_to_job
# from document_processor import extract_text_from_pdf, extract_text_from_docx # REMOVE THIS LINE
# The extract_text_from_file is imported by parser from utils, so main.py doesn't directly need it.


# --- Configuration ---
JOB_DESCRIPTION_PATH = 'data/job_description.txt'
RESUMES_DIR = 'data'

def main():
    print(f"Parsing {JOB_DESCRIPTION_PATH}...")
    job_description_data = parse_job_description(JOB_DESCRIPTION_PATH)

    if not job_description_data:
        print(f"Failed to parse job description from {JOB_DESCRIPTION_PATH}. Exiting.")
        return

    # --- DEBUGGING JOB DESCRIPTION DATA ---
    print("\n--- DEBUG: Job Description Data ---")
    print(f"JD Full Text (first 500 chars): {job_description_data.get('full_text', '')[:500]}...")
    print(f"JD Skills: {job_description_data.get('skills', set())}")
    print(f"JD Required Skills: {job_description_data.get('required_skills', set())}")
    # print(f"JD Experience (first entry responsibilities, first 200 chars): {job_description_data.get('experience', [{}])[0].get('responsibilities', ['N/A'])[0][:200]}...")
    print("-----------------------------------\n")

    all_resume_scores = {}

    # Match job description against itself (for debugging the scoring logic)
    # Treat job description as a resume for a moment to test self-consistency
    print(f"DEBUG: Matching {JOB_DESCRIPTION_PATH} against itself for score consistency check...")
    # For self-matching, both the resume_data and job_description_data are the same job_description_data
    self_match_score = match_resume_to_job(job_description_data, job_description_data)
    all_resume_scores[JOB_DESCRIPTION_PATH] = self_match_score
    print(f"DEBUG: Self-match score for {JOB_DESCRIPTION_PATH}: {self_match_score:.2f}")


    # Process resumes
    print("\nProcessing resumes...")
    for filename in os.listdir(RESUMES_DIR):
        file_path = os.path.join(RESUMES_DIR, filename)
        
        # Skip the job description file itself if it's already processed or being processed separately
        if filename == os.path.basename(JOB_DESCRIPTION_PATH):
            continue

        if os.path.isfile(file_path) and (filename.lower().endswith('.pdf') or filename.lower().endswith('.docx') or filename.lower().endswith('.txt')):
            print(f"Parsing {filename}...")
            
            # Use parse_resume for resumes, not parse_job_description
            resume_data = parse_resume(file_path)

            if resume_data:
                # --- DEBUGGING RESUME DATA ---
                print(f"\n--- DEBUG: Resume Data for {filename} ---")
                print(f"Resume Full Text (first 500 chars): {resume_data.get('full_text', '')[:500]}...")
                print(f"Resume Skills: {resume_data.get('skills', set())}")
                # print(f"Resume Experience (first entry responsibilities, first 200 chars): {resume_data.get('experience', [{}])[0].get('responsibilities', ['N/A'])[0][:200]}...") # Uncomment if needed
                print("-----------------------------------\n")

                score = match_resume_to_job(resume_data, job_description_data)
                all_resume_scores[filename] = score
            else:
                print(f"Failed to parse {filename}")
        else:
            print(f"Skipping non-document file: {filename}")


    # Display results
    print("\n--- Ranked Resumes ---")
    # Sort in descending order of scores
    sorted_resumes = sorted(all_resume_scores.items(), key=lambda item: item[1], reverse=True)
    for filename, score in sorted_resumes:
        print(f"{filename}: {score:.2f}")

if __name__ == '__main__':
    main()