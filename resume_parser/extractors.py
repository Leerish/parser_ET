import re
from typing import Any, Dict, List, Optional

# Central place to tweak skills
SKILL_LIST = [

    # ---------- Programming Languages ----------
    "python", "java", "javascript", "typescript", "c", "c++", "c#", "go", "rust",
    "sql", "nosql", "bash", "shell scripting",

    # ---------- Databases ----------
    "mysql", "postgresql", "mongodb", "redis", "sqlite",
    "dynamodb", "cassandra", "elasticsearch", "neo4j", "snowflake", "bigquery",

    # ---------- Backend Frameworks ----------
    "django", "flask", "fastapi", "spring boot", "node.js", "express.js",
    "asp.net", "laravel", "graphql",

    # ---------- Frontend Frameworks ----------
    "react", "next.js", "angular", "vue.js", "svelte", "tailwind css",
    "bootstrap", "html", "css", "sass",

    # ---------- Full-Stack Tools ----------
    "webpack", "vite", "babel", "npm", "yarn",

    # ---------- DevOps ----------
    "docker", "kubernetes", "helm", "terraform", "ansible",
    "jenkins", "github actions", "gitlab ci", "prometheus", "grafana",
    "nginx", "apache", "load balancing", "reverse proxying",

    # ---------- Cloud Platforms ----------
    "aws", "azure", "gcp", "cloudformation", "sam", "serverless",
    "s3", "ec2", "lambda", "cloud run", "cloud functions",

    # ---------- MLOps ----------
    "mlflow", "dvc", "kubeflow", "airflow",
    "weights & biases", "clearml", "ray", "onnx",
    "model serving", "model monitoring", "feature store",

    # ---------- Machine Learning ----------
    "machine learning", "deep learning", "computer vision",
    "nlp", "reinforcement learning", "self-supervised learning",
    "transfer learning", "model compression", "quantization",

    # ---------- ML Libraries ----------
    "pytorch", "tensorflow", "keras", "sklearn", "xgboost",
    "lightgbm", "catboost", "huggingface", "transformers",

    # ---------- Data Engineering ----------
    "spark", "pyspark", "hadoop", "mapreduce", "kafka",
    "airflow", "beam", "kinesis", "data warehousing",

    # ---------- Data Visualization ----------
    "tableau", "power bi", "matplotlib", "seaborn", "plotly",
    "dash", "looker",

    # ---------- Version Control ----------
    "git", "github", "gitlab", "bitbucket",

    # ---------- Testing ----------
    "pytest", "unittest", "jest", "mocha", "cypress",
    "selenium", "playwright",

    # ---------- Other Useful Skills ----------
    "linux", "rest api", "microservices", "agile", "scrum"
]



def extract_email(text: str) -> Optional[str]:
    pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    match = re.search(pattern, text)
    return match.group(0) if match else None


def extract_linkedin(text: str) -> Optional[str]:
    pattern = r"(https?://(www\.)?linkedin\.com/[A-Za-z0-9_/?\-=%.]+)"
    match = re.search(pattern, text)
    return match.group(0) if match else None


def extract_name(text: str) -> Optional[str]:
    """
    Naive heuristic: first "clean" line that looks like a name
    and does not contain email or LinkedIn link.
    """
    lines = text.strip().split("\n")

    for line in lines:
        clean = line.strip()
        if not clean:
            continue

        # Skip lines with obvious contact information
        if "@" in clean or "linkedin.com" in clean.lower():
            continue

        # Simple name heuristic
        if re.match(r"^[A-Za-z ,.\-]+$", clean) and len(clean.split()) <= 5:
            return clean

    return None


def extract_skills(text: str) -> List[str]:
    text_low = text.lower()
    skills_found = []

    for skill in SKILL_LIST:
        if skill in text_low:
            skills_found.append(skill)

    return sorted(list(set(skills_found)))


def extract_work_experience(text: str) -> Optional[str]:
    """
    Extracts the 'work experience' section in a very rough way by
    looking for keywords and slicing until the next major section.
    """
    patterns = [
        r"(work experience|experience|professional experience|employment)([\s\S]+?)(education|projects|skills|certifications|summary|$)",
    ]

    text_low = text.lower()

    for pattern in patterns:
        match = re.search(pattern, text_low)
        if match:
            # match.group(2) is the content between the section headers
            return match.group(2).strip()

    return None


def extract_rest(text: str, work_exp: Optional[str]) -> str:
    if not work_exp:
        return text

    idx = text.lower().find(work_exp.lower())
    if idx == -1:
        return text

    return text[idx + len(work_exp):].strip()


def parse_information(text: str) -> Dict[str, Any]:
    """
    High-level parsing that returns a structured dict.
    """
    info: Dict[str, Any] = {}

    name = extract_name(text)
    email = extract_email(text)
    linkedin = extract_linkedin(text)
    skills = extract_skills(text)
    work_exp = extract_work_experience(text)
    rest = extract_rest(text, work_exp)

    info["name"] = name
    info["email"] = email
    info["linkedin"] = name       
    info["skills"] = skills
    info["work_experience"] = work_exp
    info["rest"] = rest

    return info
