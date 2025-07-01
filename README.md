# Resume Matcher

## Project Overview

The Resume Matcher is a Python-based tool designed to evaluate the compatibility of a resume with a specific job description. It helps users understand how well their resume aligns with job requirements by providing a quantitative score. The system leverages Natural Language Processing (NLP) techniques, including TF-IDF for general textual similarity and explicit keyword matching for required skills, to provide a comprehensive compatibility assessment.

## How It Works

The core functionality revolves around two main components:

1.  **Parsing:**
    * **Job Description Parsing:** Extracts key information from a job description, including a comprehensive list of "required skills" and overall text content.
    * **Resume Parsing:** Extracts skills and general textual content from resumes (supporting PDF, DOCX, and TXT formats).

2.  **Matching & Scoring:**
    * **Required Skills Component:** Calculates a score based on the percentage of explicitly mentioned "required skills" from the job description that are found in the resume. This component is heavily weighted (75%) to prioritize critical qualifications.
    * **General TF-IDF Similarity:** Uses TF-IDF (Term Frequency-Inverse Document Frequency) and Cosine Similarity to compare the overall textual content of the resume against the job description, providing a general relevance score (weighted at 25%).
    * **Final Score:** A combined weighted score (out of 100) is generated, indicating the overall match percentage.

## Features

* Parses job descriptions to identify "required skills."
* Extracts skills and content from various resume formats (PDF, DOCX, TXT).
* Calculates a resume-to-job description match score.
* Prioritizes explicit skill matching for accurate relevance.
* Provides detailed debug output to show how scores are calculated (matched skills, similarity).

## Getting Started

Follow these instructions to set up and run the Resume Matcher on your local machine.

### Prerequisites

* Python 3.x
* `pip` (Python package installer)
* Git (for cloning the repository)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/Resume-Matcher.git](https://github.com/your-username/Resume-Matcher.git) # Replace with your actual repo URL
    cd Resume-Matcher
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    # On Windows
    .\venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

3.  **Install the required Python packages:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: You'll need to create a `requirements.txt` file first if you haven't already. It should list `scikit-learn`, `spacy`, `pypdf`, `python-docx`.)*

4.  **Download SpaCy language model:**
    ```bash
    python -m spacy download en_core_web_sm
    ```

### Usage

1.  **Place your Job Description:**
    * Create a `data` folder in the root of your project.
    * Place your job description in a file named `job_description.txt` inside the `data` folder.

2.  **Place your Resumes:**
    * Place the resumes (PDF, DOCX, or TXT format) you want to score inside the `data` folder.

3.  **Run the matcher:**
    ```bash
    python main.py
    ```

    The script will output a ranked list of resumes based on their match score with the job description. Debug information will be printed during execution to show the parsing and matching details for each document.

## Project Structure
resume_matcher/

├── data/

│   ├── job_description.txt

│   ├── NAYANA UPPIN DO RESUME.pdf

│   └── ... (your other resumes)

├── main.py             # Main script to run the matching process

├── parser.py           # Handles parsing of job descriptions and resumes

├── matcher.py          # Implements the scoring logic (TF-IDF, skill matching)

├── utils.py            # Utility functions (e.g., text extraction from files)

├── requirements.txt    # Lists all necessary Python packages

└── README.md           # This file!
## Customization

* **Skill List:** The `SOFTWARE_SKILLS` and `SOFT_SKILLS` lists in `parser.py` can be expanded or modified to better suit specific domain requirements.
* **Weights:** The `WEIGHT_REQUIRED_SKILLS` and `WEIGHT_GENERAL_SIMILARITY` constants in `matcher.py` can be adjusted to fine-tune the importance of explicit skill matching versus general textual relevance.
* **Resume Optimization:** To achieve higher scores, it is highly recommended to explicitly include the "required skills" from the job description directly within your resumes.

**Remember to replace `https://github.com/your-username/Resume-Matcher.git` with the actual URL of your GitHub repository.**
