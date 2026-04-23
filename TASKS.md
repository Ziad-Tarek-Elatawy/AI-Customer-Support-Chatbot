# Team Roles & Task Distribution (6-Member Team)

This document maps our 6 team members directly to the official project Milestones to ensure complete coverage of the grading requirements. It also specifies the exact folders each member should work in to avoid git conflicts.

## 1. Ziad Tarek - Team Leader (Architecture & Integration)
**Focus:** Core system integration, Security Coding, and final deliverables (Milestones 3, 5).
*   **Workspace / Folders:** `docs/`, `backend/api/` (for auth scripts), and `.github/workflows/`.
*   **Technical Pipeline Tasks:**
    *   **Architecture & Glue Code:** Programming the main integration scripts that connect the RAG model outputs with the Support Portal UI.
    *   **Security & Auth:** Writing the actual authorization code (JWT / API Key validation rules) inside the API to secure the Azure endpoints.
    *   **Version Control (CI/CD):** Writing the GitHub Actions YAML files to automate code testing and merges.
*   **Management Tasks:**
    *   Lead the generation of the **Final Report**, **Demo Presentation**, and **Business KPI Impact Analysis**.
    *   Review Pull Requests (Code Review) to ensure code quality before final submission.

## 2. Sarah Ahmed - Data Scientist / Data Engineer
**Focus:** Data Pipeline (Milestone 1).
*   **Workspace / Folders:** `data/raw/`, `data/processed/`, and `notebooks/`.
*   **Tasks:**
    *   **Data Ingestion:** Collect historical support tickets, manuals, and FAQs (save to `data/raw/`).
    *   **Preprocessing:** Clean, unify, and tokenize the text data securely (save to `data/processed/`).
    *   **EDA:** Analyze common queries and write the **Support Data EDA Report** (e.g., in `notebooks/eda.ipynb`).

## 3. Mohamed Mashhour & Mohamoud Youssef - Machine Learning Engineers
**Focus:** Core AI Pipeline & MLOps (Milestone 2 & 4).
*   **Workspace / Folders:** `backend/ai/` and `notebooks/`.
*   **Tasks:**
    *   **Model Building:** Create the vector store scripts and configure the RAG model using Hugging Face/LangChain (in `backend/ai/`).
    *   **Evaluation:** Implement algorithms (BLEU, ROUGE) to test outputs (in `notebooks/evaluations.ipynb`).
    *   **MLflow Tracking:** Setup MLflow to track different RAG experiments (Milestone 4).

## 4. Yasmeen Eladawy - Backend API Engineer
**Focus:** API Development and Logic (Milestone 3).
*   **Workspace / Folders:** `backend/api/` and `frontend/` (if UI routing is needed).
*   **Tasks:**
    *   Create a robust REST API using FastAPI/Python (e.g., `backend/api/main.py`).
    *   Establish endpoints that accept queries, send them to the RAG model, and return responses safely and quickly.

## 5. Ahmed Abdelnaby - Cloud DevOps & MLOps Engineer
**Focus:** Deployment & System Health (Milestones 3 & 4).
*   **Workspace / Folders:** `mlops/` and root environment files (`requirements.txt`, `.env`).
*   **Tasks:**
    *   **Azure Deployment:** Write scripts (in `mlops/`) to deploy the service onto Azure App Service or Azure ML.
    *   **Monitoring Dashboards:** Build systems to monitor latency, accuracy, and user satisfaction.
    *   **Retraining Pipelines:** Write automated scripts to refresh embeddings and model weights periodically.
