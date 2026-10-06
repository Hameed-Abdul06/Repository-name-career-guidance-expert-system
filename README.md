# CAREER GUIDANCE EXPERT SYSTEM
### Artificial Intelligence ( ) Mini Project &bull; Rule-Based Expert System

---

## 1. Project Title
**Career Guidance Expert System**  
*A Deterministic Rule-Based Artificial Intelligence Web Application for Engineering and Technology Students.*

---

## 2. Project Description
The **Career Guidance Expert System** is an interactive, domain-specific Artificial Intelligence application developed as a college mini project for **Artificial Intelligence ( : Expert Systems)**. 

Unlike modern statistical machine learning models or generative AI chatbots that rely on probabilistic weights and opaque neural networks, this system strictly implements a **classical Rule-Based Expert System**. It utilizes a formal Knowledge Base composed of **84 human-crafted IF–THEN production rules**, a forward-chaining inference engine, an interactive Working Memory fact base, and an explanation facility that provides 100% transparent and deterministic recommendations.

---

## 3. Problem Statement
Choosing the right career in the rapidly expanding computing industry is challenging for undergraduate students. Traditional career counseling often relies on subjective advice, while statistical machine learning tools operate as "black boxes" that cannot explain **why** a specific career was suggested. Students need an intelligent, transparent, and structured system that analyzes their current technical proficiencies, genuine interests, and work style to offer clear recommendations and actionable skill roadmaps.

---

## 4. Objective
- To implement a **Rule-Based Expert System** according to classical AI principles ( ).
- To represent domain expertise using structured **IF–THEN production rules** with weighted confidence scoring (+10, +5, +2).
- To design a **Forward-Chaining Inference Engine** (data-driven reasoning) that evaluates user facts and resolves rule matches.
- To provide a **Transparent Explanation Facility** detailing the exact fired rules, skills possessed, skills to improve, and a 3-phase learning roadmap.
- To persist student assessments and results in a local **SQLite database** without external API dependencies.
- To create a modern, responsive, and accessible user interface using Flask, HTML5, CSS3, and JavaScript.

---

## 5. Features
- **12 Technology Career Categories Covered**:
  1. Software Developer
  2. Web Developer
  3. Data Analyst
  4. Data Scientist
  5. AI / Machine Learning Engineer
  6. Cloud Engineer
  7. Cybersecurity Analyst
  8. Network Engineer
  9. Database Administrator
  10. UI/UX Designer
  11. DevOps Engineer
  12. IoT Engineer
- **Multi-Section Assessment Wizard**: 5 guided sections covering demographics, 12 interest areas, 12 technical skill proficiency levels (None, Beginner, Intermediate, Advanced), 8 work preference questions, and 7 career ratings.
- **Forward-Chaining Inference**: Evaluates premises against Working Memory facts and dynamically fires matching rules.
- **Top-3 Ranked Recommendations**: Primary recommendation with an animated circular score gauge, followed by the next 2 best-fit alternative careers.
- **Transparent Explanation Facility**: Explains recommendations through exact fired rules (e.g. `✓ Strong interest in Cloud Computing`, `✓ AWS knowledge detected`, `✓ Linux skills detected`).
- **Skill Gap Analysis Matrix**: Directly highlights "Skills You Already Have" vs "Skills You Should Learn / Improve".
- **3-Phase Learning Roadmap**: Tailored foundation, core engineering, and production mastery milestones for every career.
- **SQLite Database Persistence**: Stores students, assessment profiles, and recommendation logs with timestamps.
- **Audit & History Dashboard**: View past student assessments and inspect records.
- **Rules API**: Dedicated endpoint (`/api/rules`) to inspect all 84 production rules in JSON.
- **Print / PDF Report**: Export clean printable career guidance reports directly from the browser.

---

## 6. Technologies Used
| Component | Technology | Role |
|---|---|---|
| **Programming Language** | Python 3.10+ | Core inference engine, knowledge representation, and server logic |
| **Web Framework** | Flask 3.x | HTTP routing, controller logic, and session handling |
| **Knowledge Base** | Python (`rules.py`) | 84 structured IF–THEN production rules and career metadata |
| **Inference Engine** | Python (`inference_engine.py`) | Forward chaining, working memory, and conflict resolution |
| **Database** | SQLite3 (`career_guidance.db`) | Local ACID relational persistence for students and results |
| **Frontend UI** | HTML5, CSS3, JavaScript | Modern responsive multi-step wizard and dashboard |
| **Styling & Icons** | Bootstrap 5.3 + Bootstrap Icons | Sleek dark-mode aesthetic with custom neon accents |

---

## 7. Expert System Architecture

```
+--------------------------------------------------------------------+
|                         USER INTERFACE                             |
|    (index.html, assessment.html, results.html, about.html)         |
+--------------------------------------------------------------------+
                                | (HTTP POST / Assessment Form)
                                v
+--------------------------------------------------------------------+
|                         WORKING MEMORY                             |
|          Facts Extracted from Student Assessment Form              |
|   - Interests: [Cloud Computing, Networking, ...]                 |
|   - Skills: {aws_cloud: intermediate, linux: intermediate, ...}    |
|   - Work Preferences: {cloud_infra: yes, logical_problems: yes}    |
|   - Career Ratings: {coding: medium, cloud_interest: high}         |
+--------------------------------------------------------------------+
           |                                          ^
           | (Matches Premises)                       |
           v                                          |
+----------------------+                   +------------------------+
|   KNOWLEDGE BASE     |                   |    INFERENCE ENGINE    |
|     (rules.py)       | ===(Evaluates)==> |  (inference_engine.py) |
|                      |                   |                        |
| 84 Production Rules  |                   | Forward Chaining       |
| IF <Antecedent>      |                   | Conflict Resolution    |
| THEN <Consequent>    |                   | Score Normalization    |
| Weights: +10, +5, +2 |                   | Skill Gap Analysis     |
+----------------------+                   +------------------------+
                                                       |
                                                       v
+--------------------------------------------------------------------+
|                      EXPLANATION FACILITY                          |
|             (Synthesizes Fired Rules & Skill Gaps)                 |
|   - Top-1 Primary Recommendation (Match %)                         |
|   - "Why this career matches you" (Matched Rule Explanations)      |
|   - Skills Possessed vs Skills to Learn                            |
|   - 3-Phase Step-by-Step Learning Roadmap                          |
|   - Other Suitable Careers (Rank #2 & #3)                          |
+--------------------------------------------------------------------+
                                |
                                v
+--------------------------------------------------------------------+
|                    SQLITE DATABASE STORAGE                         |
|    Tables: students  |  assessments  |  results                    |
+--------------------------------------------------------------------+
```

---

## 8. Knowledge Base
The Knowledge Base is defined in **`rules.py`**. It contains formal representations for all 12 career domains.

Each career has:
- Detailed career overview and industry description.
- Core required skills matrix.
- Industry job titles (e.g. SDE, SOC Analyst, Solutions Architect).
- 3-Phase learning roadmap.
- **7 comprehensive production rules per career** (84 rules total).
- Maximum possible career score (39 points each).

---

## 9. IF–THEN Rules
Rules follow the classical Artificial Intelligence production rule schema:
$$\text{IF } \langle\text{Condition}_1\rangle \text{ AND } \langle\text{Condition}_2\rangle \text{ THEN } \langle\text{Conclusion Score}\rangle$$

### Scoring Heuristic:
- **Strong Match (+10 points)**: Core primary alignment (primary interest + critical technical skill).
- **Medium Match (+5 points)**: Secondary skills and supporting work preferences.
- **Basic Match (+2 points)**: Baseline curiosity or introductory programming skill.

### Rule Examples from `rules.py`:

```python
# Software Developer Rule (Strong Match: +10)
IF Programming Interest == True 
   AND Problem Solving Interest == True 
   AND Coding Preference == High 
THEN Recommend Software Developer (+10)

# Cloud Engineer Rule (Strong Match: +10)
IF Cloud Computing Interest == True 
   AND AWS/Cloud >= Intermediate 
   AND Linux >= Intermediate 
THEN Recommend Cloud Engineer (+10)

# Cybersecurity Analyst Rule (Strong Match: +10)
IF Cybersecurity Interest == True 
   AND Enjoys Finding Security Problems == Yes 
   AND Security Interest == High 
THEN Recommend Cybersecurity Analyst (+10)

# Data Scientist Rule (Strong Match: +10)
IF Data Analysis Interest == True 
   AND Mathematics/Data Interest == High 
   AND Python >= Intermediate 
THEN Recommend Data Scientist (+10)

# UI/UX Designer Rule (Strong Match: +10)
IF Designing Interest == True 
   AND Enjoys Designing Interfaces == Yes 
   AND Design Interest == High 
THEN Recommend UI/UX Designer (+10)

# IoT Engineer Rule (Strong Match: +10)
IF IoT Interest == True 
   AND Hardware Interest == True 
   AND Enjoys Hardware/Software Integration == Yes 
THEN Recommend IoT Engineer (+10)
```

---

## 10. Inference Mechanism
The Inference Engine in **`inference_engine.py`** executes a **Forward-Chaining Algorithm**:

1. **Working Memory Formation**:
   User input is normalized into standard facts: `facts['interests']`, `facts['skills']`, `facts['work_prefs']`, and `facts['career_prefs']`.
2. **Pattern Matching**:
   The engine iterates through all 84 production rules in the Knowledge Base and tests the rule antecedent (IF clause) against Working Memory.
3. **Rule Firing & Conflict Resolution**:
   When an antecedent evaluates to `True`, the rule fires:
   $$\text{Career Score} = \sum \text{Weight of all fired rules for that career}$$
   Fired rule IDs, condition descriptions, and explanations are recorded for the audit trail.
4. **Match Percentage Calculation**:
   $$\text{Match Percentage} = \min\left(100.0, \frac{\text{Score Obtained}}{\text{Maximum Possible Score}} \times 100\right)$$
5. **Skill Gap Analysis**:
   Compares the student's claimed skills against the career's required skills to populate "Skills You Have" and "Skills You Should Learn".
6. **Ranking**:
   All 12 careers are sorted descending by score and match percentage. The top 3 are returned.

---

## 11. Project Structure

```
career-guidance-expert-system/
│
├── app.py                      # Flask Application Controller & HTTP routes
├── rules.py                    # Knowledge Base (84 IF-THEN rules + 12 career schemas)
├── inference_engine.py         # Forward-Chaining Inference Engine & Gap Analysis
├── database.py                 # SQLite database models, initialization & CRUD queries
├── requirements.txt            # Python dependencies
├── test_suite.py               # Integration test suite (all 7 tests passing)
├── verify_all_careers.py       # Full 12-career validation test script
├── README.md                   # Complete academic documentation & viva guide
│
├── templates/
│   ├── base.html               # Master layout with responsive navbar & footer
│   ├── index.html              # Landing page with hero, features & flow preview
│   ├── assessment.html         # 5-Section interactive career assessment wizard
│   ├── results.html            # Dynamic recommendation dashboard & explanations
│   ├── about.html              # Academic guide on Expert Systems & Viva FAQs
│   └── history.html            # Past assessments audit log table
│
├── static/
│   ├── css/
│   │   └── style.css           # Modern dark-mode UI stylesheet with neon accents
│   └── js/
│       └── script.js           # 5-step wizard logic, live validation & animations
│
└── database/
    └── career_guidance.db      # SQLite relational database (auto-generated)
```

---

## 12. Installation Steps

### Prerequisites:
- Python 3.10, 3.11, 3.12, or 3.13 installed on Windows, macOS, or Linux.
- `pip` package manager.

### Step 1: Open Terminal / PowerShell
Navigate to the project root directory:
```powershell
cd C:\Users\Acer\.gemini\antigravity\scratch\career-guidance-expert-system
```

### Step 2: (Optional but Recommended) Create a Virtual Environment
```powershell
python -m venv venv
.\venv\Scripts\activate
```

### Step 3: Install Dependencies
```powershell
pip install -r requirements.txt
```
*(Flask is the only core dependency required).*

---

## 13. How to Run

### Command to Start Application:
```powershell
python app.py
```

### Expected Terminal Output:
```
======================================================================
 CAREER GUIDANCE EXPERT SYSTEM - AI   MINI PROJECT
 Rule-Based Forward-Chaining Inference Engine Initialized
 Knowledge Base Loaded: 84 Production Rules
 Server running on: http://127.0.0.1:5000
======================================================================
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

### Accessing the Web Application:
Open any web browser (Chrome, Edge, Firefox) and navigate to:  
👉 **`http://127.0.0.1:5000`**

---

## 14. Example Input

### Student Demographic Fact:
- **Name**: Aarav Sharma
- **Education Level**: Bachelor / B.Tech / B.Sc
- **Course**: Computer Science & Engineering
- **Year of Study**: 3rd Year

### Section 2 – Interests:
- `Cloud Computing`, `Networking`, `Problem Solving`

### Section 3 – Technical Skills:
- **AWS / Cloud Platforms**: Intermediate
- **Linux / Bash Scripting**: Intermediate
- **Computer Networking**: Beginner
- **Python**: Beginner
- **Git / GitHub**: Beginner
- *(All others set to None)*

### Section 4 – Work Preferences:
- Enjoys logical problems: **Yes**
- Enjoys cloud infrastructure: **Yes**
- Enjoys finding security problems: **Somewhat**
- Work style: **Teamwork**
- Work preference: **Analytical**

### Section 5 – Career Preferences:
- Preferred work area: **Cloud & Infrastructure**
- Interest in coding: **Medium**
- Interest in cloud technologies: **High**
- Interest in security: **Medium**

---

## 15. Example Output

### Primary Recommendation:
- **Career Name**: **Cloud Engineer**
- **Match Score**: **100% (39 / 39 Points)**

### Explanation Facility ("Why this career matches you"):
```
✓ Strong dedication to cloud computing backed by hands-on proficiency in AWS/Cloud services and Linux systems.
✓ Clear passion for architecting and provisioning distributed cloud server infrastructure.
✓ Solid foundation in enterprise networking concepts (VPCs, subnets) and Linux administration.
✓ Stated career preference focused on cloud systems architecture and infrastructure rather than intensive software development.
✓ Scripting abilities with Python and Git version control for cloud automation.
✓ General interest in modern cloud computing architecture.
✓ Introductory exposure to cloud platforms and services.
```

### Skills Gap Analysis:
- **Skills You Already Have**:
  - `AWS/Cloud (Intermediate)` [Strong Match]
  - `Linux (Intermediate)` [Strong Match]
  - `Networking (Beginner)` [Foundational]
  - `Python (Beginner)` [Foundational]
  - `Git/GitHub (Beginner)` [Foundational]
- **Skills to Improve**:
  - `Networking` (Level up from Beginner to Intermediate/Advanced for industry readiness)
  - `Python` (Level up to Intermediate for Cloud Automation)

### 3-Phase Suggested Roadmap:
- **Phase 1: Systems & Networks**: Linux administration, bash scripting, TCP/IP networking, DNS, and HTTP protocol mastery.
- **Phase 2: Cloud Platform Core**: AWS/Azure core services (Compute EC2, Storage S3, VPC networking, IAM security).
- **Phase 3: Infrastructure Automation**: Terraform (IaC), serverless architectures, monitoring (CloudWatch), and enterprise cloud migration.

### Other Suitable Careers:
- **Rank #2**: **DevOps Engineer (87.2% Match)**
- **Rank #3**: **Network Engineer (35.9% Match)**

---

## 16. Future Enhancements
1. **Certainty Factors (CF)**: Incorporate MYCIN-style certainty factor calculus (MB, MD) for handling user uncertainty in skill evaluations.
2. **Backward-Chaining Goal Mode**: Allow students to select a target career first (e.g. "I want to be an AI Engineer") and have the engine work backward to verify prerequisites.
3. **Automated Curriculum Mapping**: Link recommended skills directly to online university course codes or open-source syllabi.
4. **Resume Parser Fact Ingestion**: Automatically parse student PDF resumes into Working Memory facts before running the inference engine.

---

## Viva Voce Preparation Guide (For College Students)

### 1. Where is the Knowledge Base stored?
> The Knowledge Base is located in `rules.py`. It holds the `KNOWLEDGE_BASE_RULES` list containing 84 production rules and `CAREER_METADATA` defining the 12 careers.

### 2. Where are the IF–THEN rules defined?
> Each rule is an instance of `ExpertRule` in `rules.py` with:
> - `rule_id`: Unique identifier (e.g. `R_SWD_01`, `R_CLD_01`).
> - `career_id`: Target career.
> - `weight`: Confidence points (+10 for strong, +5 for medium, +2 for basic).
> - `condition_desc`: Human-readable IF-THEN premise.
> - `explanation`: Plain-text justification for the explanation facility.
> - `condition_fn`: Python callable/lambda evaluating Working Memory facts.

### 3. Where does inference happen?
> Inference is implemented in `inference_engine.py` inside `run_forward_chaining(facts)`. It iterates through all production rules, checks premises against facts in Working Memory, and fires matching rules.

### 4. How are scores calculated and ranked?
> For each career, scores are summed:
> $$\text{Career Score} = \sum \text{Fired Rule Weights}$$
> Match percentage is calculated:
> $$\text{Match } \% = \frac{\text{Score Obtained}}{\text{Max Possible Score (39)}} \times 100$$
> Careers are sorted descending by score, and the top 3 are returned.

### 5. Why is this a Rule-Based Expert System and NOT Machine Learning?
> Machine learning relies on statistical pattern matching over labeled training datasets, producing probabilistic outputs without transparent explanations. This system uses **formal logic, explicit heuristics, and deterministic IF–THEN rules**. Identical inputs will always produce the exact same verifiable recommendations, and every conclusion is 100% explainable by tracing fired rules.

---

### Running Tests
To verify all unit tests and 12-career profile validations:
```powershell
python test_suite.py
python verify_all_careers.py
```
*(Both scripts will report 100% PASS).*
