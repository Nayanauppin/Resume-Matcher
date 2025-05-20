import spacy
import re
import os # ADDED: Import os for os.path.basename
from utils import extract_text_from_file # Ensure utils.py exists and has extract_text_from_file

# Load a pre-trained spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Downloading spaCy model 'en_core_web_sm' (this may take a moment)...")
    spacy.cli.download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

# Define a more comprehensive list of software skills and related terms
# Expanded significantly to capture terms from your job description and common SDE skills
SOFTWARE_SKILLS = {
    # Programming Languages
    "python", "java", "c++", "c#", "javascript", "typescript", "ruby", "php", "go", "swift",
    "kotlin", "scala", "rust", "html", "css", "sql", "r", "perl", "bash", "shell scripting",
    "matlab", "vb.net", "vba", "objective-c", "dart", "elixir", "haskell", "clojure", "lisp", "fortran", "assembly",

    # Frameworks & Libraries
    "react", "angular", "vue.js", "node.js", "express.js", "django", "flask", "ruby on rails", "spring boot",
    "spring", "asp.net", "laravel", "symfony", "react native", "flutter", "xamarin", "tensorflow", "pytorch",
    "keras", "scikit-learn", "numpy", "pandas", "matplotlib", "seaborn", "bootstrap", "jquery", "tailwind css",
    "graphql", "rest api", "ajax", "redux", "mobx", "jest", "mocha", "cypress", "selenium", "pytest", "junit",

    # Databases
    "mysql", "postgresql", "mongodb", "redis", "cassandra", "couchbase", "sqlite", "oracle", "sql server",
    "dynamodb", "mariadb", "neo4j", "elasticsearch", "firebase",

    # Cloud Platforms & Services
    "aws", "amazon web services", "azure", "google cloud platform", "gcp", "docker", "kubernetes", "jenkins",
    "gitlab ci", "github actions", "terraform", "ansible", "puppet", "chef", "heroku", "netlify", "vercel",
    "lambda", "ec2", "s3", "rds", "azure devops", "azure functions", "google kubernetes engine", "eks", "ecs",

    # DevOps & CI/CD
    "devops", "ci/cd", "continuous integration", "continuous delivery", "jenkins", "travis ci", "circleci",
    "github", "gitlab", "bitbucket", "svn", "git", "version control", "containerization", "microservices",
    "api gateway", "service mesh", "grafana", "prometheus", "elk stack", "logstash", "kibana", "terraform",
    "ansible", "puppet", "chef", "argocd", "fluxcd",

    # Operating Systems
    "linux", "unix", "windows", "macos", "ubuntu", "centos", "redhat", "debian",

    # Methodologies & Concepts
    "agile", "scrum", "kanban", "devsecops", "test-driven development", "tdd", "object-oriented programming",
    "oop", "functional programming", "data structures", "algorithms", "design patterns", "microservices architecture",
    "serverless", "responsive web design", "ui/ux", "user interface", "user experience", "restful api",
    "web sockets", "message queues", "kafka", "rabbitmq", "apache kafka", "load balancing", "caching",
    "distributed systems", "system design", "network security", "data encryption", "cybersecurity",
    "machine learning", "deep learning", "natural language processing", "nlp", "computer vision", "big data",
    "hadoop", "spark", "data analysis", "data science", "etl", "data warehousing", "business intelligence",
    "cloud computing", "virtualization", "networking", "tcp/ip", "dns", "http/https", "rest", "soap",
    "unit testing", "integration testing", "end-to-end testing", "api testing", "performance testing",
    "security testing", "sdlc", "software development life cycle", "data modeling", "data governance",
    "data mining", "data visualization", "business analysis", "technical writing", "documentation",
    "project management", "jira", "confluence", "trello", "asana", "microsoft project",
    "customer relationship management", "crm", "enterprise resource planning", "erp",
    "quality assurance", "qa", "software testing", "test automation", "api development", "web development",
    "mobile development", "android development", "ios development", "desktop development", "game development",
    "cloud native", "observability", "site reliability engineering", "sre", "it operations", "automation",
    "scripting", "bash scripting", "powershell", "shell scripting", "frontend", "backend", "full stack",
    "front-end development", "back-end development", "full-stack development", "github pipelines",
    # Specific skills directly from your job description's body/requirements:
    "user interfaces", "coding", "testing", "debugging", "problem-solving", "analytical skills", "teamwork", "communication"
}

# Add common soft skills that might appear explicitly
SOFT_SKILLS = {
    "communication", "teamwork", "problem-solving", "analytical skills", "leadership", "adaptability",
    "time management", "critical thinking", "creativity", "collaboration", "interpersonal skills",
    "negotiation", "attention to detail", "organization", "project management", "client management",
    "presentation skills", "mentoring", "coaching"
}

# Combine all skills for general extraction
ALL_SKILLS = SOFTWARE_SKILLS.union(SOFT_SKILLS)


def extract_skills(text_raw, skill_set=ALL_SKILLS):
    """
    Extracts skills from text by matching against a predefined skill_set.
    Also looks for skills within common requirement phrases or bullet points.
    'text_raw' should be the original full text (not overly processed yet)
    """
    found_skills = set()
    text_lower = text_raw.lower() # Only lowercase once here

    # 1. Direct keyword matching (most robust)
    for skill in skill_set:
        # Use word boundaries to match whole words/phrases precisely
        if re.search(r'\b' + re.escape(skill) + r'\b', text_lower):
            found_skills.add(skill)

    # 2. Enhanced pattern matching for common skill listing formats
    # This catches skills listed with bullet points or introductory phrases
    lines = text_raw.split('\n') # Split original text (preserves bullet points etc.)
    for line in lines:
        line_lower = line.strip().lower()
        
        # Check for patterns indicating explicit skill mention in the line
        if line_lower.startswith('·') or line_lower.startswith('-') or line_lower.startswith('*') or line_lower.startswith('•') or \
           "experience with" in line_lower or "experience in" in line_lower or "solid understanding of" in line_lower or \
           "proficiency in" in line_lower or "proficient in" in line_lower:
            
            # Specific matches for job description's critical keywords/phrases
            if "java development" in line_lower:
                found_skills.add("java")
            if "postgresql" in line_lower:
                found_skills.add("postgresql")
            if "micro service" in line_lower or "microservices" in line_lower:
                found_skills.add("microservices")
            if "gitlab" in line_lower:
                found_skills.add("gitlab")
            if "github pipelines" in line_lower:
                found_skills.add("github pipelines")
                found_skills.add("github") # Also add general github

            # Also, extract any general skills from these specific lines (prevents redundancy if already added by direct match)
            for skill in skill_set:
                if re.search(r'\b' + re.escape(skill) + r'\b', line_lower):
                    found_skills.add(skill)

    print(f"DEBUG: Extracted raw skills for text (from extract_skills): {found_skills}")
    return found_skills


def extract_required_skills(text_raw):
    """
    Specifically extracts 'required' skills from a job description, focusing on explicit statements.
    This function should produce the comprehensive set of skills that ARE required.
    'text_raw' should be the original full text.
    """
    required_skills = set()
    text_lower = text_raw.lower() # Only lowercase once here

    # Heuristic: Extracting from lines starting with bullet points or strong indicators
    lines = text_raw.split('\n') # Use raw text split to preserve formatting like bullet points
    for line in lines:
        line_lower = line.strip().lower()
        
        # Check for patterns indicating explicit skill mention in the line
        if line_lower.startswith('·') or line_lower.startswith('-') or line_lower.startswith('*') or line_lower.startswith('•') or \
           "experience with" in line_lower or "experience in" in line_lower or "solid understanding of" in line_lower or \
           "proficiency in" in line_lower or "proficient in" in line_lower or "required skills:" in line_lower:
            
            # Specific matches for job description's critical keywords/phrases from YOUR JD
            if "java development" in line_lower:
                required_skills.add("java")
            if "postgresql" in line_lower:
                required_skills.add("postgresql")
            if "micro service" in line_lower or "microservices" in line_lower:
                required_skills.add("microservices")
            if "gitlab" in line_lower:
                required_skills.add("gitlab")
            if "github pipelines" in line_lower:
                required_skills.add("github pipelines")
                required_skills.add("github") # Also add general github
            if "ability to quickly grasp concepts" in line_lower: # Example of a soft skill from JD
                required_skills.add("problem-solving") # Map to a broader skill
                required_skills.add("analytical skills") # Map to a broader skill
                required_skills.add("adaptability") # Map to a broader skill


            # Additionally, search for any general skills within these specific requirement lines
            for skill in ALL_SKILLS:
                if re.search(r'\b' + re.escape(skill) + r'\b', line_lower):
                    required_skills.add(skill)

    # Crucial: Augment required skills with *all* general skills found throughout the JD text.
    # This ensures that if a skill is mentioned anywhere in the JD (even if not in a bullet point),
    # it is considered part of the 'required' set for the purpose of the JD's own self-matching,
    # and therefore, for high scores.
    # We use extract_skills with the full raw text to capture everything.
    augmented_required_skills = required_skills.copy() # Start with explicitly found skills
    
    # Pass the raw text to extract_skills, which handles its own lowercasing and processing
    augmented_required_skills.update(extract_skills(text_raw, skill_set=ALL_SKILLS))

    print(f"DEBUG: Extracted Required Skills (Initial): {required_skills}")
    print(f"DEBUG: Extracted Required Skills (Augmented): {augmented_required_skills}")
    return augmented_required_skills


def extract_experience(text):
    # This is a basic placeholder. For real-world use, you'd need more sophisticated NLP
    # to identify sections like "Work Experience", "Projects", "Education", etc.
    # and then parse content within those sections.
    # Given the current PDF/DOCX parsing (often general content), we'll treat the whole
    # document as one "experience" block for now.
    parsed_experiences = []
    parsed_experiences.append({
        'title': 'General Document Content',
        'responsibilities': [text] # Return the whole text
    })
    return parsed_experiences


def parse_resume(file_path):
    full_text = extract_text_from_file(file_path)
    if not full_text:
        return None

    # Use the raw text for skill extraction initially to preserve formatting
    # Then create a processed text for TF-IDF
    # Ensure processed_text_for_tfidf is always defined
    processed_text_for_tfidf = full_text.lower() if full_text else ""
    processed_text_for_tfidf = re.sub(r'[^a-zA-Z0-9\s\.\,\-\+\#]', ' ', processed_text_for_tfidf)

    # Call extract_skills with the raw text (lowercased) for robust matching
    skills = extract_skills(full_text, skill_set=ALL_SKILLS) if full_text else set() # Ensure skills is defined even if text is empty
    experience = extract_experience(full_text) if full_text else [] # Ensure experience is defined

    return {
        'file_name': os.path.basename(file_path),
        'full_text': processed_text_for_tfidf, # This is used for TF-IDF in matcher.py
        'skills': skills, # This is the set of skills identified in the resume
        'experience': experience,
        'education': [], # Placeholder
        'contact_info': {} # Placeholder
    }

def parse_job_description(file_path):
    full_text = extract_text_from_file(file_path)
    if not full_text:
        return None

    # Use the raw text for required_skills extraction
    required_skills = extract_required_skills(full_text)
    
    # The 'skills' for the job description itself should ideally be the same as its 'required_skills'
    # to ensure perfect self-matching.
    skills_for_jd = required_skills.copy() 

    # Create a processed text for TF-IDF
    # Ensure processed_text_for_tfidf is always defined
    processed_text_for_tfidf = full_text.lower() if full_text else ""
    processed_text_for_tfidf = re.sub(r'[^a-zA-Z0-9\s\.\,\-\+\#]', ' ', processed_text_for_tfidf)

    experience = extract_experience(full_text) if full_text else [] # Ensure experience is defined

    return {
        'file_name': os.path.basename(file_path),
        'full_text': processed_text_for_tfidf, # This is used for TF-IDF in matcher.py
        'skills': skills_for_jd, # IMPORTANT: Set JD's general skills to its required skills for self-consistency
        'required_skills': required_skills, # This is the specific set of "must-have" skills
        'experience': experience,
        'education': [], # Placeholder
        'contact_info': {} # Placeholder
    }