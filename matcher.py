import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def preprocess_text_for_tfidf(text):
    """
    Basic text preprocessing for TF-IDF: lowercasing, removing non-alphanumeric.
    """
    if not text:
        return ""
    # Remove special characters, keep only letters, numbers, and spaces
    # Allow some punctuation that might be part of technical terms if relevant (e.g., C#)
    # But for general TF-IDF, stricter is better to avoid noise.
    text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text) # Replace with space instead of removing
    return text.lower()


def match_resume_to_job(resume_data, job_description_data):
    # Ensure all text is preprocessed for consistent comparison
    resume_full_text_processed = preprocess_text_for_tfidf(resume_data.get('full_text', ''))
    job_full_text_processed = preprocess_text_for_tfidf(job_description_data.get('full_text', ''))

    # If job description text is empty, we can't match
    if not job_full_text_processed:
        print("ERROR: Job description text is empty. Cannot perform matching.")
        return 0.0

    # --- 1. Core TF-IDF Similarity (General Content) ---
    # This acts as a baseline for overall textual relevance.
    # It should be quite high when matching identical documents.
    documents_for_tfidf = [resume_full_text_processed, job_full_text_processed]
    
    general_similarity = 0.0
    if not resume_full_text_processed or not job_full_text_processed:
        general_similarity = 0.0
        # print("DEBUG: One of the texts is empty for TF-IDF calculation.")
    else:
        try:
            # max_features limits the vocabulary size, stop_words removes common words
            # token_pattern ensures basic alphanumeric tokens
            vectorizer = TfidfVectorizer(stop_words='english', max_features=5000, token_pattern=r'\b\w+\b')
            tfidf_matrix = vectorizer.fit_transform(documents_for_tfidf)
            general_similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        except ValueError as e: # Catches "empty vocabulary" if texts are too short/uninformative
            # print(f"DEBUG: TF-IDF calculation error: {e}. Setting general_similarity to 0.0.")
            general_similarity = 0.0

    # --- 2. Required Skills Matching (Dominant Weight) ---
    job_required_skills = set(job_description_data.get('required_skills', []))
    resume_extracted_skills = set(resume_data.get('skills', [])) # Note: using 'skills' key from resume_data

    matched_required_skills = job_required_skills.intersection(resume_extracted_skills)
    
    required_skills_score_component = 0.0
    if len(job_required_skills) > 0:
        required_skills_score_component = (len(matched_required_skills) / len(job_required_skills))
    
    # --- 3. Weighted Combination of Scores ---
    # The sum of weights should be 1.0. Required skills are heavily prioritized.
    # This combination is designed to push scores high if required skills are met.

    WEIGHT_REQUIRED_SKILLS = 0.75  # 75% from matching explicitly required skills
    WEIGHT_GENERAL_SIMILARITY = 0.25 # 25% from overall content similarity

    final_score = (
        (required_skills_score_component * WEIGHT_REQUIRED_SKILLS) +
        (general_similarity * WEIGHT_GENERAL_SIMILARITY)
    ) * 100 # Scale to 0-100

    # Debugging prints (keep these for now, they are invaluable)
    print(f"DEBUG: Resume: {resume_data.get('file_name', 'N/A')}")
    print(f"DEBUG: Job Required Skills: {job_required_skills}")
    print(f"DEBUG: Resume Extracted Skills: {resume_extracted_skills}")
    print(f"DEBUG: Matched Required Skills: {matched_required_skills} (Count: {len(matched_required_skills)})")
    print(f"DEBUG: Required Skills Component: {required_skills_score_component:.2f} ({len(matched_required_skills)}/{len(job_required_skills)})")
    print(f"DEBUG: General TF-IDF Similarity: {general_similarity:.2f}")
    print(f"DEBUG: Calculated Final Score: {final_score:.2f}")

    return final_score