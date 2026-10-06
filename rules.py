"""
=============================================================================
CAREER GUIDANCE EXPERT SYSTEM - KNOWLEDGE BASE (rules.py)
=============================================================================
Academic Context: Artificial Intelligence  : Rule-Based Expert Systems
Architecture:
  - Domain Knowledge Representation: IF-THEN Production Rules
  - Fact Base / Working Memory: User assessment profile
  - Rule Structure: Antecedent (Premise / IF) -> Consequent (Conclusion / THEN)
  - Scoring Heuristic:
      * Strong Match (+10 points): Core primary alignment (interests + critical skills)
      * Medium Match (+5 points): Secondary skills and supporting preferences
      * Basic Match (+2 points): Foundational/general interest or aptitude
=============================================================================
"""

# Skill proficiency level numerical mapping for comparison
SKILL_LEVEL_MAP = {
    'none': 0,
    'beginner': 1,
    'intermediate': 2,
    'advanced': 3
}

def has_interest(facts, interest_name):
    """Check if student selected a specific interest (case-insensitive)."""
    interests = facts.get('interests', [])
    return any(interest_name.lower() == str(i).strip().lower() for i in interests)

def get_skill_level(facts, skill_name):
    """Retrieve skill level string ('none', 'beginner', 'intermediate', 'advanced')."""
    skills = facts.get('skills', {})
    return skills.get(skill_name.lower().replace(' ', '_').replace('/', '_'), 'none').lower()

def skill_at_least(facts, skill_name, min_level='beginner'):
    """Check if student's skill in a technology meets or exceeds min_level."""
    level = get_skill_level(facts, skill_name)
    user_val = SKILL_LEVEL_MAP.get(level, 0)
    required_val = SKILL_LEVEL_MAP.get(min_level.lower(), 1)
    return user_val >= required_val

def work_pref_is(facts, key, expected_val):
    """Check work preference response."""
    prefs = facts.get('work_prefs', {})
    val = str(prefs.get(key, '')).lower().strip()
    return val == expected_val.lower().strip()

def career_pref_is(facts, key, expected_val):
    """Check career preference rating ('high', 'medium', 'low')."""
    c_prefs = facts.get('career_prefs', {})
    val = str(c_prefs.get(key, '')).lower().strip()
    return val == expected_val.lower().strip()


class ExpertRule:
    """
    Represents a single production rule in the Expert System Knowledge Base.
    Format: IF <Premise / Condition> THEN <Consequent / Career Recommendation Score>
    """
    def __init__(self, rule_id, career_id, career_name, weight, condition_desc, explanation, condition_fn):
        self.rule_id = rule_id
        self.career_id = career_id
        self.career_name = career_name
        self.weight = weight              # 10: Strong, 5: Medium, 2: Basic
        self.condition_desc = condition_desc  # Human-readable rule for viva demonstration
        self.explanation = explanation    # Plain-English reason why this rule matched
        self.condition_fn = condition_fn  # Lambda/callable evaluating against facts

    def evaluate(self, facts):
        """Evaluate the premise against Working Memory facts."""
        try:
            return bool(self.condition_fn(facts))
        except Exception:
            return False


# =============================================================================
# CAREER DEFINITIONS & METADATA
# =============================================================================
CAREER_METADATA = {
    'software_developer': {
        'id': 'software_developer',
        'name': 'Software Developer',
        'icon': 'bi-code-slash',
        'description': 'Designs, builds, and maintains robust computer programs, enterprise software, and scalable backend applications using algorithmic problem solving and modern engineering principles.',
        'required_skills': ['Java', 'Python', 'C++', 'Git/GitHub', 'SQL', 'Linux'],
        'possible_job_roles': [
            'Software Development Engineer (SDE)',
            'Backend Developer',
            'Full Stack Engineer',
            'Application Developer',
            'Systems Programmer'
        ],
        'learning_roadmap': [
            {'phase': 'Phase 1: Foundations', 'desc': 'Master a core language (Java, C++, or Python), object-oriented programming (OOP), and Git version control.'},
            {'phase': 'Phase 2: Core Engineering', 'desc': 'Deep dive into Data Structures & Algorithms (DSA), relational databases (SQL), and clean coding principles.'},
            {'phase': 'Phase 3: Production Mastery', 'desc': 'Build multi-tiered enterprise applications, RESTful APIs, unit testing, and continuous integration.'}
        ]
    },
    'web_developer': {
        'id': 'web_developer',
        'name': 'Web Developer',
        'icon': 'bi-globe2',
        'description': 'Develops engaging, interactive web applications and websites, bridging visual client interfaces with reliable server-side services.',
        'required_skills': ['HTML/CSS', 'JavaScript', 'Python', 'SQL', 'Git/GitHub'],
        'possible_job_roles': [
            'Frontend Web Developer',
            'Backend Web Developer',
            'Full Stack Web Developer',
            'Web Application Engineer',
            'JavaScript Engineer'
        ],
        'learning_roadmap': [
            {'phase': 'Phase 1: Web Fundamentals', 'desc': 'Master semantic HTML5, modern CSS3 (Flexbox/Grid), and core JavaScript fundamentals.'},
            {'phase': 'Phase 2: Modern Frameworks', 'desc': 'Learn a frontend framework (React, Vue) and backend framework (Node.js/Express, Flask, or Django).'},
            {'phase': 'Phase 3: Full Stack & Deployment', 'desc': 'Integrate RESTful/GraphQL APIs, database persistence, authentication, and cloud deployment (Vercel/Render).'}
        ]
    },
    'data_analyst': {
        'id': 'data_analyst',
        'name': 'Data Analyst',
        'icon': 'bi-graph-up',
        'description': 'Inspects, cleans, transforms, and models data to uncover actionable business insights, identify patterns, and drive strategic decision-making.',
        'required_skills': ['Data Analysis', 'SQL', 'Python', 'Git/GitHub'],
        'possible_job_roles': [
            'Business Intelligence Analyst',
            'Junior Data Analyst',
            'Reporting Specialist',
            'Operations Data Analyst',
            'Product Analyst'
        ],
        'learning_roadmap': [
            {'phase': 'Phase 1: Data Foundations', 'desc': 'Master advanced SQL queries, relational joins, spreadsheet modeling, and basic statistics.'},
            {'phase': 'Phase 2: Python Data Stack', 'desc': 'Learn data manipulation with Pandas, numerical computing with NumPy, and charting with Matplotlib/Seaborn.'},
            {'phase': 'Phase 3: BI Dashboards & Storytelling', 'desc': 'Build executive dashboards in Power BI/Tableau and communicate data-driven insights to stakeholders.'}
        ]
    },
    'data_scientist': {
        'id': 'data_scientist',
        'name': 'Data Scientist',
        'icon': 'bi-calculator',
        'description': 'Combines advanced mathematics, statistics, computer science, and domain expertise to extract deep knowledge from complex data and build predictive models.',
        'required_skills': ['Python', 'Data Analysis', 'SQL', 'Git/GitHub', 'Linux'],
        'possible_job_roles': [
            'Data Scientist',
            'Applied Scientist',
            'Predictive Analytics Specialist',
            'Quantitative Analyst',
            'Data Science Consultant'
        ],
        'learning_roadmap': [
            {'phase': 'Phase 1: Math & Coding Foundations', 'desc': 'Linear algebra, multivariate calculus, probability & statistics, and Python programming.'},
            {'phase': 'Phase 2: Machine Learning & Modeling', 'desc': 'Scikit-Learn, hypothesis testing, regression/classification, feature engineering, and cross-validation.'},
            {'phase': 'Phase 3: Advanced Pipelines', 'desc': 'Experiment tracking (MLflow), big data processing, model deployment, and production analytics.'}
        ]
    },
    'ai_ml_engineer': {
        'id': 'ai_ml_engineer',
        'name': 'AI / Machine Learning Engineer',
        'icon': 'bi-cpu',
        'description': 'Researches, designs, and deploys intelligent autonomous systems, neural networks, and scalable machine learning models into real-world production environments.',
        'required_skills': ['Python', 'Data Analysis', 'Linux', 'Git/GitHub', 'C++'],
        'possible_job_roles': [
            'Machine Learning Engineer',
            'Deep Learning Engineer',
            'NLP / Computer Vision Engineer',
            'AI Solutions Architect',
            'MLOps Engineer'
        ],
        'learning_roadmap': [
            {'phase': 'Phase 1: Core AI Foundations', 'desc': 'Vector calculus, optimization, Python proficiency, and foundational ML algorithms.'},
            {'phase': 'Phase 2: Deep Learning Architectures', 'desc': 'Neural networks with PyTorch/TensorFlow, Transformers, CNNs, and NLP techniques.'},
            {'phase': 'Phase 3: Production MLOps', 'desc': 'Model quantization, containerized inference with Docker, GPU acceleration, and pipeline automation.'}
        ]
    },
    'cloud_engineer': {
        'id': 'cloud_engineer',
        'name': 'Cloud Engineer',
        'icon': 'bi-cloud-check',
        'description': 'Architects, configures, and secures cloud computing systems, infrastructure as a service (IaaS), and distributed cloud services across AWS, Azure, or GCP.',
        'required_skills': ['AWS/Cloud', 'Linux', 'Networking', 'Python', 'Git/GitHub'],
        'possible_job_roles': [
            'Cloud Infrastructure Engineer',
            'AWS Solutions Architect',
            'Cloud Administrator',
            'Site Reliability Engineer (SRE)',
            'Cloud Operations Specialist'
        ],
        'learning_roadmap': [
            {'phase': 'Phase 1: Systems & Networks', 'desc': 'Linux administration, bash scripting, TCP/IP networking, DNS, and HTTP protocol mastery.'},
            {'phase': 'Phase 2: Cloud Platform Core', 'desc': 'AWS/Azure core services (Compute EC2/VM, Storage S3/Blob, VPC networking, IAM security).'},
            {'phase': 'Phase 3: Infrastructure Automation', 'desc': 'Terraform (IaC), serverless architectures, monitoring (CloudWatch), and enterprise cloud migration.'}
        ]
    },
    'cybersecurity_analyst': {
        'id': 'cybersecurity_analyst',
        'name': 'Cybersecurity Analyst',
        'icon': 'bi-shield-lock',
        'description': 'Monitors networks and computer systems for security breaches, investigates threats, hardens infrastructure, and enforces data protection protocols.',
        'required_skills': ['Networking', 'Linux', 'Python', 'Git/GitHub'],
        'possible_job_roles': [
            'Security Operations Center (SOC) Analyst',
            'Information Security Analyst',
            'Vulnerability Assessment Specialist',
            'Incident Response Analyst',
            'Junior Penetration Tester'
        ],
        'learning_roadmap': [
            {'phase': 'Phase 1: Security Fundamentals', 'desc': 'Computer networking (OSI model, Wireshark, subnets), Linux security, and cryptography basics.'},
            {'phase': 'Phase 2: Threat Detection & Defense', 'desc': 'SIEM tools (Splunk), firewall administration, vulnerability scanners (Nessus/Nmap), and threat hunting.'},
            {'phase': 'Phase 3: Incident Response & Certifications', 'desc': 'Digital forensics, security incident handling, CompTIA Security+ / CEH preparation.'}
        ]
    },
    'network_engineer': {
        'id': 'network_engineer',
        'name': 'Network Engineer',
        'icon': 'bi-diagram-3',
        'description': 'Plans, installs, and maintains enterprise data communications networks, routers, switches, WAN/LAN configurations, and telecommunications infrastructure.',
        'required_skills': ['Networking', 'Linux', 'Python', 'C'],
        'possible_job_roles': [
            'Network Support Engineer',
            'Network Administrator',
            'Telecommunications Specialist',
            'Cisco Network Associate',
            'Network Infrastructure Analyst'
        ],
        'learning_roadmap': [
            {'phase': 'Phase 1: Networking Theory', 'desc': 'IPv4/IPv6 addressing, subnetting, switching, routing protocols (OSPF, BGP), and Ethernet standards.'},
            {'phase': 'Phase 2: Network Equipment & Configuration', 'desc': 'Hands-on configuration of Cisco IOS routers, switches, VLANs, trunking, and NAT.'},
            {'phase': 'Phase 3: Network Automation', 'desc': 'Python network scripting with Netmiko/Paramiko, software-defined networking (SDN), and CCNA certification.'}
        ]
    },
    'database_administrator': {
        'id': 'database_administrator',
        'name': 'Database Administrator',
        'icon': 'bi-database-check',
        'description': 'Oversees the integrity, performance, backup, replication, and security of enterprise database management systems (DBMS).',
        'required_skills': ['SQL', 'Linux', 'Python', 'Git/GitHub'],
        'possible_job_roles': [
            'Database Administrator (DBA)',
            'SQL Database Engineer',
            'Database Reliability Engineer',
            'Data Storage Administrator',
            'Database Migration Specialist'
        ],
        'learning_roadmap': [
            {'phase': 'Phase 1: Relational Database Mastery', 'desc': 'Advanced SQL, indexing, relational schema design, normalization, and ACID transactions.'},
            {'phase': 'Phase 2: Database Administration', 'desc': 'PostgreSQL/MySQL administration, backup & disaster recovery, user privilege management, and replication.'},
            {'phase': 'Phase 3: Performance Tuning & NoSQL', 'desc': 'Query execution plan optimization, buffer tuning, sharding, and NoSQL databases (MongoDB, Redis).'}
        ]
    },
    'ui_ux_designer': {
        'id': 'ui_ux_designer',
        'name': 'UI/UX Designer',
        'icon': 'bi-palette',
        'description': 'Crafts intuitive, visually captivating digital interfaces and seamless user experiences through empathy, research, wireframing, and interactive prototyping.',
        'required_skills': ['HTML/CSS', 'JavaScript'],
        'possible_job_roles': [
            'UI/UX Designer',
            'Product Designer',
            'Interaction Designer',
            'Visual Designer',
            'Design Systems Specialist'
        ],
        'learning_roadmap': [
            {'phase': 'Phase 1: Design Principles & Research', 'desc': 'Color theory, typography, visual hierarchy, user research, wireframing, and persona creation.'},
            {'phase': 'Phase 2: Industry Prototyping Tools', 'desc': 'Figma proficiency, component auto-layout, interactive micro-animations, and design systems.'},
            {'phase': 'Phase 3: Usability Testing & Frontend Bridge', 'desc': 'Conducting usability testing, basic HTML/CSS design handoff, and building a polished design portfolio.'}
        ]
    },
    'devops_engineer': {
        'id': 'devops_engineer',
        'name': 'DevOps Engineer',
        'icon': 'bi-arrow-repeat',
        'description': 'Bridges the gap between software development and IT operations through continuous integration, continuous delivery (CI/CD), infrastructure as code, and automated testing.',
        'required_skills': ['Linux', 'Git/GitHub', 'AWS/Cloud', 'Python', 'Networking'],
        'possible_job_roles': [
            'DevOps Engineer',
            'Site Reliability Engineer (SRE)',
            'Build & Release Engineer',
            'Infrastructure Engineer',
            'Platform Engineer'
        ],
        'learning_roadmap': [
            {'phase': 'Phase 1: Linux & Version Control', 'desc': 'Advanced Linux shell scripting, system automation, and advanced Git branching workflows.'},
            {'phase': 'Phase 2: Containers & Orchestration', 'desc': 'Docker containerization, multi-stage builds, and Kubernetes cluster orchestration.'},
            {'phase': 'Phase 3: CI/CD & Infrastructure as Code', 'desc': 'GitHub Actions / Jenkins pipelines, Terraform, Ansible, and Prometheus/Grafana monitoring.'}
        ]
    },
    'iot_engineer': {
        'id': 'iot_engineer',
        'name': 'IoT Engineer',
        'icon': 'bi-motherboard',
        'description': 'Develops smart connected devices by integrating microcontrollers, embedded sensors, wireless communication protocols, and edge software.',
        'required_skills': ['C', 'C++', 'Python', 'Networking', 'Linux'],
        'possible_job_roles': [
            'IoT Solutions Developer',
            'Embedded Systems Engineer',
            'Firmware Developer',
            'IoT Hardware Architect',
            'Smart Systems Engineer'
        ],
        'learning_roadmap': [
            {'phase': 'Phase 1: Embedded C & Electronics', 'desc': 'C/C++ for microcontrollers, digital electronics, GPIO, I2C, SPI, and Arduino/ESP32 programming.'},
            {'phase': 'Phase 2: IoT Protocols & Networking', 'desc': 'MQTT, CoAP, BLE, Wi-Fi connectivity, sensor telemetry, and FreeRTOS basics.'},
            {'phase': 'Phase 3: Edge Computing & Cloud IoT', 'desc': 'Raspberry Pi embedded Linux, edge AI inference, and AWS IoT Core / Azure IoT Hub integration.'}
        ]
    }
}


# =============================================================================
# KNOWLEDGE BASE: PRODUCTION RULES (IF-THEN)
# Total Rules: 84 comprehensive rules (7 rules per career category)
# =============================================================================

KNOWLEDGE_BASE_RULES = [

    # -------------------------------------------------------------------------
    # 1. SOFTWARE DEVELOPER RULES (R_SWD_01 to R_SWD_07)
    # -------------------------------------------------------------------------
    ExpertRule(
        rule_id='R_SWD_01',
        career_id='software_developer',
        career_name='Software Developer',
        weight=10,
        condition_desc='IF Programming Interest == True AND Problem Solving Interest == True AND Coding Preference == High THEN Recommend Software Developer (+10)',
        explanation='Strong passion for core programming combined with high problem-solving drive and enthusiasm for coding.',
        condition_fn=lambda f: has_interest(f, 'Programming') and has_interest(f, 'Problem Solving') and career_pref_is(f, 'coding_interest', 'high')
    ),
    ExpertRule(
        rule_id='R_SWD_02',
        career_id='software_developer',
        career_name='Software Developer',
        weight=10,
        condition_desc='IF (Java >= Intermediate OR C++ >= Intermediate OR Python >= Intermediate) AND Enjoys Logical Problems == Yes THEN Recommend Software Developer (+10)',
        explanation='Proficiency in fundamental enterprise programming languages (Java, C++, or Python) paired with love for logical challenges.',
        condition_fn=lambda f: (skill_at_least(f, 'Java', 'intermediate') or skill_at_least(f, 'C++', 'intermediate') or skill_at_least(f, 'Python', 'intermediate')) and work_pref_is(f, 'logical_problems', 'yes')
    ),
    ExpertRule(
        rule_id='R_SWD_03',
        career_id='software_developer',
        career_name='Software Developer',
        weight=5,
        condition_desc='IF Git/GitHub >= Beginner AND SQL >= Beginner THEN Recommend Software Developer (+5)',
        explanation='Familiarity with industry-standard version control (Git) and structured data querying (SQL).',
        condition_fn=lambda f: skill_at_least(f, 'Git/GitHub', 'beginner') and skill_at_least(f, 'SQL', 'beginner')
    ),
    ExpertRule(
        rule_id='R_SWD_04',
        career_id='software_developer',
        career_name='Software Developer',
        weight=5,
        condition_desc='IF Preferred Work Area == Software & Applications THEN Recommend Software Developer (+5)',
        explanation='Explicit career aspiration to build standalone desktop, enterprise, or mobile software applications.',
        condition_fn=lambda f: career_pref_is(f, 'preferred_work_area', 'software')
    ),
    ExpertRule(
        rule_id='R_SWD_05',
        career_id='software_developer',
        career_name='Software Developer',
        weight=5,
        condition_desc='IF Work Preference == Analytical AND (C >= Beginner OR C++ >= Beginner) THEN Recommend Software Developer (+5)',
        explanation='Analytical work style coupled with systems-level programming knowledge (C/C++).',
        condition_fn=lambda f: work_pref_is(f, 'creative_analytical', 'analytical') and (skill_at_least(f, 'C', 'beginner') or skill_at_least(f, 'C++', 'beginner'))
    ),
    ExpertRule(
        rule_id='R_SWD_06',
        career_id='software_developer',
        career_name='Software Developer',
        weight=2,
        condition_desc='IF Programming Interest == True THEN Recommend Software Developer (+2)',
        explanation='Foundational interest in the field of computer programming.',
        condition_fn=lambda f: has_interest(f, 'Programming')
    ),
    ExpertRule(
        rule_id='R_SWD_07',
        career_id='software_developer',
        career_name='Software Developer',
        weight=2,
        condition_desc='IF Problem Solving Interest == True THEN Recommend Software Developer (+2)',
        explanation='Innate interest in algorithmic problem decomposition.',
        condition_fn=lambda f: has_interest(f, 'Problem Solving')
    ),

    # -------------------------------------------------------------------------
    # 2. WEB DEVELOPER RULES (R_WEB_01 to R_WEB_07)
    # -------------------------------------------------------------------------
    ExpertRule(
        rule_id='R_WEB_01',
        career_id='web_developer',
        career_name='Web Developer',
        weight=10,
        condition_desc='IF Web Development Interest == True AND HTML/CSS >= Intermediate AND JavaScript >= Intermediate THEN Recommend Web Developer (+10)',
        explanation='Strong passion for web technologies backed by intermediate proficiency in core web building blocks (HTML/CSS and JavaScript).',
        condition_fn=lambda f: has_interest(f, 'Web Development') and skill_at_least(f, 'HTML/CSS', 'intermediate') and skill_at_least(f, 'JavaScript', 'intermediate')
    ),
    ExpertRule(
        rule_id='R_WEB_02',
        career_id='web_developer',
        career_name='Web Developer',
        weight=10,
        condition_desc='IF Enjoys Designing Interfaces == Yes AND Coding Interest >= Medium AND (HTML/CSS >= Beginner OR JavaScript >= Beginner) THEN Recommend Web Developer (+10)',
        explanation='Enjoys user interface design and possesses coding skills to translate visual layouts into living web pages.',
        condition_fn=lambda f: work_pref_is(f, 'design_interfaces', 'yes') and not career_pref_is(f, 'coding_interest', 'low') and (skill_at_least(f, 'HTML/CSS', 'beginner') or skill_at_least(f, 'JavaScript', 'beginner'))
    ),
    ExpertRule(
        rule_id='R_WEB_03',
        career_id='web_developer',
        career_name='Web Developer',
        weight=5,
        condition_desc='IF Preferred Work Area == Web & Applications AND Programming Interest == True THEN Recommend Web Developer (+5)',
        explanation='Career preference focused on the web application development ecosystem.',
        condition_fn=lambda f: (career_pref_is(f, 'preferred_work_area', 'web') or career_pref_is(f, 'preferred_work_area', 'software')) and has_interest(f, 'Web Development')
    ),
    ExpertRule(
        rule_id='R_WEB_04',
        career_id='web_developer',
        career_name='Web Developer',
        weight=5,
        condition_desc='IF (Python >= Beginner OR SQL >= Beginner) AND Web Development Interest == True THEN Recommend Web Developer (+5)',
        explanation='Backend development capabilities with Python/SQL combined with web interest.',
        condition_fn=lambda f: (skill_at_least(f, 'Python', 'beginner') or skill_at_least(f, 'SQL', 'beginner')) and has_interest(f, 'Web Development')
    ),
    ExpertRule(
        rule_id='R_WEB_05',
        career_id='web_developer',
        career_name='Web Developer',
        weight=5,
        condition_desc='IF Git/GitHub >= Beginner AND Design Interest == High/Medium THEN Recommend Web Developer (+5)',
        explanation='Familiarity with collaborative source control (Git) paired with visual design sensitivity.',
        condition_fn=lambda f: skill_at_least(f, 'Git/GitHub', 'beginner') and (career_pref_is(f, 'design_interest', 'high') or career_pref_is(f, 'design_interest', 'medium'))
    ),
    ExpertRule(
        rule_id='R_WEB_06',
        career_id='web_developer',
        career_name='Web Developer',
        weight=2,
        condition_desc='IF Web Development Interest == True THEN Recommend Web Developer (+2)',
        explanation='Basic interest in internet technologies and websites.',
        condition_fn=lambda f: has_interest(f, 'Web Development')
    ),
    ExpertRule(
        rule_id='R_WEB_07',
        career_id='web_developer',
        career_name='Web Developer',
        weight=2,
        condition_desc='IF HTML/CSS >= Beginner THEN Recommend Web Developer (+2)',
        explanation='Prior exposure to HTML/CSS markup and styling.',
        condition_fn=lambda f: skill_at_least(f, 'HTML/CSS', 'beginner')
    ),

    # -------------------------------------------------------------------------
    # 3. DATA ANALYST RULES (R_DAN_01 to R_DAN_07)
    # -------------------------------------------------------------------------
    ExpertRule(
        rule_id='R_DAN_01',
        career_id='data_analyst',
        career_name='Data Analyst',
        weight=10,
        condition_desc='IF Data Analysis Interest == True AND SQL >= Intermediate AND Enjoys Working With Data == Yes THEN Recommend Data Analyst (+10)',
        explanation='High interest in data analysis, strong relational database querying skills (SQL), and genuine enthusiasm for working with datasets.',
        condition_fn=lambda f: has_interest(f, 'Data Analysis') and skill_at_least(f, 'SQL', 'intermediate') and work_pref_is(f, 'working_with_data', 'yes')
    ),
    ExpertRule(
        rule_id='R_DAN_02',
        career_id='data_analyst',
        career_name='Data Analyst',
        weight=10,
        condition_desc='IF Mathematics/Data Interest == High AND Data Analysis Skill >= Beginner AND Python >= Beginner THEN Recommend Data Analyst (+10)',
        explanation='High numerical/data affinity combined with practical Python and data analytics fundamentals.',
        condition_fn=lambda f: career_pref_is(f, 'math_data_interest', 'high') and skill_at_least(f, 'Data Analysis', 'beginner') and skill_at_least(f, 'Python', 'beginner')
    ),
    ExpertRule(
        rule_id='R_DAN_03',
        career_id='data_analyst',
        career_name='Data Analyst',
        weight=5,
        condition_desc='IF Work Preference == Analytical AND Databases Interest == True THEN Recommend Data Analyst (+5)',
        explanation='Analytical work style aligned with structured database concepts.',
        condition_fn=lambda f: work_pref_is(f, 'creative_analytical', 'analytical') and has_interest(f, 'Databases')
    ),
    ExpertRule(
        rule_id='R_DAN_04',
        career_id='data_analyst',
        career_name='Data Analyst',
        weight=5,
        condition_desc='IF Preferred Work Area == Data & AI AND SQL >= Beginner THEN Recommend Data Analyst (+5)',
        explanation='Career preference towards data domains supported by relational query knowledge.',
        condition_fn=lambda f: career_pref_is(f, 'preferred_work_area', 'data_ai') and skill_at_least(f, 'SQL', 'beginner')
    ),
    ExpertRule(
        rule_id='R_DAN_05',
        career_id='data_analyst',
        career_name='Data Analyst',
        weight=5,
        condition_desc='IF Problem Solving Interest == True AND Enjoys Working With Data == Yes THEN Recommend Data Analyst (+5)',
        explanation='Enjoys solving logical challenges through quantitative data exploration.',
        condition_fn=lambda f: has_interest(f, 'Problem Solving') and work_pref_is(f, 'working_with_data', 'yes')
    ),
    ExpertRule(
        rule_id='R_DAN_06',
        career_id='data_analyst',
        career_name='Data Analyst',
        weight=2,
        condition_desc='IF Data Analysis Interest == True THEN Recommend Data Analyst (+2)',
        explanation='Basic curiosity about data visualization and reporting.',
        condition_fn=lambda f: has_interest(f, 'Data Analysis')
    ),
    ExpertRule(
        rule_id='R_DAN_07',
        career_id='data_analyst',
        career_name='Data Analyst',
        weight=2,
        condition_desc='IF SQL >= Beginner THEN Recommend Data Analyst (+2)',
        explanation='Foundational knowledge of SQL syntax.',
        condition_fn=lambda f: skill_at_least(f, 'SQL', 'beginner')
    ),

    # -------------------------------------------------------------------------
    # 4. DATA SCIENTIST RULES (R_DSC_01 to R_DSC_07)
    # -------------------------------------------------------------------------
    ExpertRule(
        rule_id='R_DSC_01',
        career_id='data_scientist',
        career_name='Data Scientist',
        weight=10,
        condition_desc='IF Data Analysis Interest == True AND Mathematics/Data Interest == High AND Python >= Intermediate THEN Recommend Data Scientist (+10)',
        explanation='Exceptional combination of data curiosity, strong mathematical interest, and intermediate Python programming capability.',
        condition_fn=lambda f: has_interest(f, 'Data Analysis') and career_pref_is(f, 'math_data_interest', 'high') and skill_at_least(f, 'Python', 'intermediate')
    ),
    ExpertRule(
        rule_id='R_DSC_02',
        career_id='data_scientist',
        career_name='Data Scientist',
        weight=10,
        condition_desc='IF Data Analysis Skill >= Intermediate AND SQL >= Intermediate AND Work Preference == Analytical THEN Recommend Data Scientist (+10)',
        explanation='Demonstrated proficiency in data manipulation and SQL querying combined with an analytical research mindset.',
        condition_fn=lambda f: skill_at_least(f, 'Data Analysis', 'intermediate') and skill_at_least(f, 'SQL', 'intermediate') and work_pref_is(f, 'creative_analytical', 'analytical')
    ),
    ExpertRule(
        rule_id='R_DSC_03',
        career_id='data_scientist',
        career_name='Data Scientist',
        weight=5,
        condition_desc='IF Artificial Intelligence Interest == True AND Enjoys Working With Data == Yes THEN Recommend Data Scientist (+5)',
        explanation='Interest in advanced algorithms coupled with passion for modeling complex datasets.',
        condition_fn=lambda f: has_interest(f, 'Artificial Intelligence') and work_pref_is(f, 'working_with_data', 'yes')
    ),
    ExpertRule(
        rule_id='R_DSC_04',
        career_id='data_scientist',
        career_name='Data Scientist',
        weight=5,
        condition_desc='IF Preferred Work Area == Data & AI AND Coding Interest >= Medium THEN Recommend Data Scientist (+5)',
        explanation='Clear goal to work at the intersection of data science, statistics, and programming.',
        condition_fn=lambda f: career_pref_is(f, 'preferred_work_area', 'data_ai') and not career_pref_is(f, 'coding_interest', 'low')
    ),
    ExpertRule(
        rule_id='R_DSC_05',
        career_id='data_scientist',
        career_name='Data Scientist',
        weight=5,
        condition_desc='IF Linux >= Beginner AND Git/GitHub >= Beginner AND Python >= Beginner THEN Recommend Data Scientist (+5)',
        explanation='Good developer hygiene (Linux, Git) supporting scientific computing workflows.',
        condition_fn=lambda f: skill_at_least(f, 'Linux', 'beginner') and skill_at_least(f, 'Git/GitHub', 'beginner') and skill_at_least(f, 'Python', 'beginner')
    ),
    ExpertRule(
        rule_id='R_DSC_06',
        career_id='data_scientist',
        career_name='Data Scientist',
        weight=2,
        condition_desc='IF Mathematics/Data Interest == High THEN Recommend Data Scientist (+2)',
        explanation='Innate interest in statistical and mathematical reasoning.',
        condition_fn=lambda f: career_pref_is(f, 'math_data_interest', 'high')
    ),
    ExpertRule(
        rule_id='R_DSC_07',
        career_id='data_scientist',
        career_name='Data Scientist',
        weight=2,
        condition_desc='IF Python >= Beginner THEN Recommend Data Scientist (+2)',
        explanation='Baseline knowledge of Python for computational tasks.',
        condition_fn=lambda f: skill_at_least(f, 'Python', 'beginner')
    ),

    # -------------------------------------------------------------------------
    # 5. AI / MACHINE LEARNING ENGINEER RULES (R_AIM_01 to R_AIM_07)
    # -------------------------------------------------------------------------
    ExpertRule(
        rule_id='R_AIM_01',
        career_id='ai_ml_engineer',
        career_name='AI / Machine Learning Engineer',
        weight=10,
        condition_desc='IF Artificial Intelligence Interest == True AND Python >= Intermediate AND Mathematics/Data Interest == High THEN Recommend AI / ML Engineer (+10)',
        explanation='Ideal alignment: passionate about Artificial Intelligence, skilled in Python, and strong mathematical aptitude.',
        condition_fn=lambda f: has_interest(f, 'Artificial Intelligence') and skill_at_least(f, 'Python', 'intermediate') and career_pref_is(f, 'math_data_interest', 'high')
    ),
    ExpertRule(
        rule_id='R_AIM_02',
        career_id='ai_ml_engineer',
        career_name='AI / Machine Learning Engineer',
        weight=10,
        condition_desc='IF Enjoys Logical Problems == Yes AND Coding Interest == High AND Data Analysis Skill >= Beginner THEN Recommend AI / ML Engineer (+10)',
        explanation='High enthusiasm for algorithmic problem solving and coding with hands-on data manipulation background.',
        condition_fn=lambda f: work_pref_is(f, 'logical_problems', 'yes') and career_pref_is(f, 'coding_interest', 'high') and skill_at_least(f, 'Data Analysis', 'beginner')
    ),
    ExpertRule(
        rule_id='R_AIM_03',
        career_id='ai_ml_engineer',
        career_name='AI / Machine Learning Engineer',
        weight=5,
        condition_desc='IF Preferred Work Area == Data & AI AND Programming Interest == True THEN Recommend AI / ML Engineer (+5)',
        explanation='Strong target preference for AI systems paired with core programming foundation.',
        condition_fn=lambda f: career_pref_is(f, 'preferred_work_area', 'data_ai') and has_interest(f, 'Programming')
    ),
    ExpertRule(
        rule_id='R_AIM_04',
        career_id='ai_ml_engineer',
        career_name='AI / Machine Learning Engineer',
        weight=5,
        condition_desc='IF (C++ >= Beginner OR C >= Beginner) AND Python >= Intermediate THEN Recommend AI / ML Engineer (+5)',
        explanation='Valuable dual skill set: high-level Python ML modeling combined with low-level C/C++ for inference optimization.',
        condition_fn=lambda f: (skill_at_least(f, 'C++', 'beginner') or skill_at_least(f, 'C', 'beginner')) and skill_at_least(f, 'Python', 'intermediate')
    ),
    ExpertRule(
        rule_id='R_AIM_05',
        career_id='ai_ml_engineer',
        career_name='AI / Machine Learning Engineer',
        weight=5,
        condition_desc='IF Linux >= Beginner AND Git/GitHub >= Beginner THEN Recommend AI / ML Engineer (+5)',
        explanation='Essential systems knowledge (Linux environments and Git) for training and deploying deep learning pipelines.',
        condition_fn=lambda f: skill_at_least(f, 'Linux', 'beginner') and skill_at_least(f, 'Git/GitHub', 'beginner')
    ),
    ExpertRule(
        rule_id='R_AIM_06',
        career_id='ai_ml_engineer',
        career_name='AI / Machine Learning Engineer',
        weight=2,
        condition_desc='IF Artificial Intelligence Interest == True THEN Recommend AI / ML Engineer (+2)',
        explanation='Enthusiasm for intelligent agents and machine learning breakthroughs.',
        condition_fn=lambda f: has_interest(f, 'Artificial Intelligence')
    ),
    ExpertRule(
        rule_id='R_AIM_07',
        career_id='ai_ml_engineer',
        career_name='AI / Machine Learning Engineer',
        weight=2,
        condition_desc='IF Python >= Beginner THEN Recommend AI / ML Engineer (+2)',
        explanation='Foundational knowledge of Python, the lingua franca of AI research.',
        condition_fn=lambda f: skill_at_least(f, 'Python', 'beginner')
    ),

    # -------------------------------------------------------------------------
    # 6. CLOUD ENGINEER RULES (R_CLD_01 to R_CLD_07)
    # -------------------------------------------------------------------------
    ExpertRule(
        rule_id='R_CLD_01',
        career_id='cloud_engineer',
        career_name='Cloud Engineer',
        weight=10,
        condition_desc='IF Cloud Computing Interest == True AND AWS/Cloud >= Intermediate AND Linux >= Intermediate THEN Recommend Cloud Engineer (+10)',
        explanation='Strong dedication to cloud computing backed by hands-on proficiency in AWS/Cloud services and Linux systems.',
        condition_fn=lambda f: has_interest(f, 'Cloud Computing') and skill_at_least(f, 'AWS/Cloud', 'intermediate') and skill_at_least(f, 'Linux', 'intermediate')
    ),
    ExpertRule(
        rule_id='R_CLD_02',
        career_id='cloud_engineer',
        career_name='Cloud Engineer',
        weight=10,
        condition_desc='IF Enjoys Cloud Infrastructure == Yes AND Cloud Technologies Interest == High THEN Recommend Cloud Engineer (+10)',
        explanation='Clear passion for architecting and provisioning distributed cloud server infrastructure.',
        condition_fn=lambda f: work_pref_is(f, 'cloud_infrastructure', 'yes') and career_pref_is(f, 'cloud_interest', 'high')
    ),
    ExpertRule(
        rule_id='R_CLD_03',
        career_id='cloud_engineer',
        career_name='Cloud Engineer',
        weight=5,
        condition_desc='IF Networking Skill >= Beginner AND Linux >= Beginner THEN Recommend Cloud Engineer (+5)',
        explanation='Solid foundation in enterprise networking concepts (VPCs, subnets) and Linux administration.',
        condition_fn=lambda f: skill_at_least(f, 'Networking', 'beginner') and skill_at_least(f, 'Linux', 'beginner')
    ),
    ExpertRule(
        rule_id='R_CLD_04',
        career_id='cloud_engineer',
        career_name='Cloud Engineer',
        weight=5,
        condition_desc='IF Preferred Work Area == Cloud & Infrastructure AND Coding Interest <= Medium THEN Recommend Cloud Engineer (+5)',
        explanation='Stated career preference focused on cloud systems architecture and infrastructure rather than intensive software development.',
        condition_fn=lambda f: career_pref_is(f, 'preferred_work_area', 'cloud') and not career_pref_is(f, 'coding_interest', 'high')
    ),
    ExpertRule(
        rule_id='R_CLD_05',
        career_id='cloud_engineer',
        career_name='Cloud Engineer',
        weight=5,
        condition_desc='IF Python >= Beginner AND Git/GitHub >= Beginner THEN Recommend Cloud Engineer (+5)',
        explanation='Scripting abilities with Python and Git version control for cloud automation.',
        condition_fn=lambda f: skill_at_least(f, 'Python', 'beginner') and skill_at_least(f, 'Git/GitHub', 'beginner')
    ),
    ExpertRule(
        rule_id='R_CLD_06',
        career_id='cloud_engineer',
        career_name='Cloud Engineer',
        weight=2,
        condition_desc='IF Cloud Computing Interest == True THEN Recommend Cloud Engineer (+2)',
        explanation='General interest in modern cloud computing architecture.',
        condition_fn=lambda f: has_interest(f, 'Cloud Computing')
    ),
    ExpertRule(
        rule_id='R_CLD_07',
        career_id='cloud_engineer',
        career_name='Cloud Engineer',
        weight=2,
        condition_desc='IF AWS/Cloud >= Beginner THEN Recommend Cloud Engineer (+2)',
        explanation='Introductory exposure to cloud platforms and services.',
        condition_fn=lambda f: skill_at_least(f, 'AWS/Cloud', 'beginner')
    ),

    # -------------------------------------------------------------------------
    # 7. CYBERSECURITY ANALYST RULES (R_SEC_01 to R_SEC_07)
    # -------------------------------------------------------------------------
    ExpertRule(
        rule_id='R_SEC_01',
        career_id='cybersecurity_analyst',
        career_name='Cybersecurity Analyst',
        weight=10,
        condition_desc='IF Cybersecurity Interest == True AND Enjoys Finding Security Problems == Yes AND Security Interest == High THEN Recommend Cybersecurity Analyst (+10)',
        explanation='Deep passion for digital defense, keen eye for discovering vulnerabilities, and high dedication to information security.',
        condition_fn=lambda f: has_interest(f, 'Cybersecurity') and work_pref_is(f, 'security_problems', 'yes') and career_pref_is(f, 'security_interest', 'high')
    ),
    ExpertRule(
        rule_id='R_SEC_02',
        career_id='cybersecurity_analyst',
        career_name='Cybersecurity Analyst',
        weight=10,
        condition_desc='IF Networking Skill >= Intermediate AND Linux >= Intermediate THEN Recommend Cybersecurity Analyst (+10)',
        explanation='Command over network packet analysis, protocols, and Linux system security auditing.',
        condition_fn=lambda f: skill_at_least(f, 'Networking', 'intermediate') and skill_at_least(f, 'Linux', 'intermediate')
    ),
    ExpertRule(
        rule_id='R_SEC_03',
        career_id='cybersecurity_analyst',
        career_name='Cybersecurity Analyst',
        weight=5,
        condition_desc='IF Python >= Beginner AND Linux >= Beginner THEN Recommend Cybersecurity Analyst (+5)',
        explanation='Python scripting capabilities for security tooling, log parsing, and Linux automation.',
        condition_fn=lambda f: skill_at_least(f, 'Python', 'beginner') and skill_at_least(f, 'Linux', 'beginner')
    ),
    ExpertRule(
        rule_id='R_SEC_04',
        career_id='cybersecurity_analyst',
        career_name='Cybersecurity Analyst',
        weight=5,
        condition_desc='IF Preferred Work Area == Security & Networks THEN Recommend Cybersecurity Analyst (+5)',
        explanation='Clear career choice targeting enterprise cyber defense and threat mitigation.',
        condition_fn=lambda f: career_pref_is(f, 'preferred_work_area', 'security')
    ),
    ExpertRule(
        rule_id='R_SEC_05',
        career_id='cybersecurity_analyst',
        career_name='Cybersecurity Analyst',
        weight=5,
        condition_desc='IF Work Preference == Analytical AND Problem Solving Interest == True THEN Recommend Cybersecurity Analyst (+5)',
        explanation='Analytical investigative mindset essential for digital forensics and threat hunting.',
        condition_fn=lambda f: work_pref_is(f, 'creative_analytical', 'analytical') and has_interest(f, 'Problem Solving')
    ),
    ExpertRule(
        rule_id='R_SEC_06',
        career_id='cybersecurity_analyst',
        career_name='Cybersecurity Analyst',
        weight=2,
        condition_desc='IF Cybersecurity Interest == True THEN Recommend Cybersecurity Analyst (+2)',
        explanation='Interest in threat landscapes, encryption, and defensive techniques.',
        condition_fn=lambda f: has_interest(f, 'Cybersecurity')
    ),
    ExpertRule(
        rule_id='R_SEC_07',
        career_id='cybersecurity_analyst',
        career_name='Cybersecurity Analyst',
        weight=2,
        condition_desc='IF Networking Skill >= Beginner THEN Recommend Cybersecurity Analyst (+2)',
        explanation='Awareness of networking topologies, ports, and protocols.',
        condition_fn=lambda f: skill_at_least(f, 'Networking', 'beginner')
    ),

    # -------------------------------------------------------------------------
    # 8. NETWORK ENGINEER RULES (R_NET_01 to R_NET_07)
    # -------------------------------------------------------------------------
    ExpertRule(
        rule_id='R_NET_01',
        career_id='network_engineer',
        career_name='Network Engineer',
        weight=10,
        condition_desc='IF Networking Interest == True AND Networking Skill >= Intermediate THEN Recommend Network Engineer (+10)',
        explanation='High interest in data communications matched with proven practical skill in computer networking and routing.',
        condition_fn=lambda f: has_interest(f, 'Networking') and skill_at_least(f, 'Networking', 'intermediate')
    ),
    ExpertRule(
        rule_id='R_NET_02',
        career_id='network_engineer',
        career_name='Network Engineer',
        weight=10,
        condition_desc='IF Linux >= Intermediate AND Preferred Work Area == Security & Networks THEN Recommend Network Engineer (+10)',
        explanation='Strong Linux administration skills dedicated to network infrastructure operations.',
        condition_fn=lambda f: skill_at_least(f, 'Linux', 'intermediate') and career_pref_is(f, 'preferred_work_area', 'security')
    ),
    ExpertRule(
        rule_id='R_NET_03',
        career_id='network_engineer',
        career_name='Network Engineer',
        weight=5,
        condition_desc='IF Enjoys Hardware/Software Integration == Yes AND Networking Interest == True THEN Recommend Network Engineer (+5)',
        explanation='Appreciation for physical switches, routers, cabling, and communication software.',
        condition_fn=lambda f: work_pref_is(f, 'hardware_software', 'yes') and has_interest(f, 'Networking')
    ),
    ExpertRule(
        rule_id='R_NET_04',
        career_id='network_engineer',
        career_name='Network Engineer',
        weight=5,
        condition_desc='IF (C >= Beginner OR Python >= Beginner) AND Networking Skill >= Beginner THEN Recommend Network Engineer (+5)',
        explanation='Network automation readiness using Python or low-level socket programming in C.',
        condition_fn=lambda f: (skill_at_least(f, 'C', 'beginner') or skill_at_least(f, 'Python', 'beginner')) and skill_at_least(f, 'Networking', 'beginner')
    ),
    ExpertRule(
        rule_id='R_NET_05',
        career_id='network_engineer',
        career_name='Network Engineer',
        weight=5,
        condition_desc='IF Cloud Computing Interest == True AND Networking Skill >= Beginner THEN Recommend Network Engineer (+5)',
        explanation='Synergy between hybrid cloud connectivity and core networking protocols.',
        condition_fn=lambda f: has_interest(f, 'Cloud Computing') and skill_at_least(f, 'Networking', 'beginner')
    ),
    ExpertRule(
        rule_id='R_NET_06',
        career_id='network_engineer',
        career_name='Network Engineer',
        weight=2,
        condition_desc='IF Networking Interest == True THEN Recommend Network Engineer (+2)',
        explanation='Foundational interest in computer network architectures.',
        condition_fn=lambda f: has_interest(f, 'Networking')
    ),
    ExpertRule(
        rule_id='R_NET_07',
        career_id='network_engineer',
        career_name='Network Engineer',
        weight=2,
        condition_desc='IF Hardware Interest == High/Medium THEN Recommend Network Engineer (+2)',
        explanation='Interest in physical IT hardware and transmission infrastructure.',
        condition_fn=lambda f: (career_pref_is(f, 'hardware_interest', 'high') or career_pref_is(f, 'hardware_interest', 'medium'))
    ),

    # -------------------------------------------------------------------------
    # 9. DATABASE ADMINISTRATOR RULES (R_DBA_01 to R_DBA_07)
    # -------------------------------------------------------------------------
    ExpertRule(
        rule_id='R_DBA_01',
        career_id='database_administrator',
        career_name='Database Administrator',
        weight=10,
        condition_desc='IF Databases Interest == True AND SQL >= Intermediate THEN Recommend Database Administrator (+10)',
        explanation='Strong passion for database management backed by solid practical mastery of SQL and schema structure.',
        condition_fn=lambda f: has_interest(f, 'Databases') and skill_at_least(f, 'SQL', 'intermediate')
    ),
    ExpertRule(
        rule_id='R_DBA_02',
        career_id='database_administrator',
        career_name='Database Administrator',
        weight=10,
        condition_desc='IF Enjoys Working With Data == Yes AND Work Preference == Analytical AND SQL >= Beginner THEN Recommend Database Administrator (+10)',
        explanation='Analytical discipline dedicated to maintaining data integrity, normalization, and reliable storage.',
        condition_fn=lambda f: work_pref_is(f, 'working_with_data', 'yes') and work_pref_is(f, 'creative_analytical', 'analytical') and skill_at_least(f, 'SQL', 'beginner')
    ),
    ExpertRule(
        rule_id='R_DBA_03',
        career_id='database_administrator',
        career_name='Database Administrator',
        weight=5,
        condition_desc='IF Linux >= Beginner AND SQL >= Beginner THEN Recommend Database Administrator (+5)',
        explanation='Crucial operational skills: managing database engines hosted on Linux servers.',
        condition_fn=lambda f: skill_at_least(f, 'Linux', 'beginner') and skill_at_least(f, 'SQL', 'beginner')
    ),
    ExpertRule(
        rule_id='R_DBA_04',
        career_id='database_administrator',
        career_name='Database Administrator',
        weight=5,
        condition_desc='IF (Python >= Beginner OR Git/GitHub >= Beginner) AND Databases Interest == True THEN Recommend Database Administrator (+5)',
        explanation='Database migration automation using Python scripts and source-controlled schema versions.',
        condition_fn=lambda f: (skill_at_least(f, 'Python', 'beginner') or skill_at_least(f, 'Git/GitHub', 'beginner')) and has_interest(f, 'Databases')
    ),
    ExpertRule(
        rule_id='R_DBA_05',
        career_id='database_administrator',
        career_name='Database Administrator',
        weight=5,
        condition_desc='IF Enjoys Logical Problems == Yes AND Mathematics/Data Interest >= Medium THEN Recommend Database Administrator (+5)',
        explanation='Logical orientation essential for database indexing, query optimization, and concurrency control.',
        condition_fn=lambda f: work_pref_is(f, 'logical_problems', 'yes') and not career_pref_is(f, 'math_data_interest', 'low')
    ),
    ExpertRule(
        rule_id='R_DBA_06',
        career_id='database_administrator',
        career_name='Database Administrator',
        weight=2,
        condition_desc='IF Databases Interest == True THEN Recommend Database Administrator (+2)',
        explanation='Fundamental appreciation for database systems and transactions.',
        condition_fn=lambda f: has_interest(f, 'Databases')
    ),
    ExpertRule(
        rule_id='R_DBA_07',
        career_id='database_administrator',
        career_name='Database Administrator',
        weight=2,
        condition_desc='IF SQL >= Beginner THEN Recommend Database Administrator (+2)',
        explanation='Basic knowledge of SQL queries and tables.',
        condition_fn=lambda f: skill_at_least(f, 'SQL', 'beginner')
    ),

    # -------------------------------------------------------------------------
    # 10. UI/UX DESIGNER RULES (R_UIX_01 to R_UIX_07)
    # -------------------------------------------------------------------------
    ExpertRule(
        rule_id='R_UIX_01',
        career_id='ui_ux_designer',
        career_name='UI/UX Designer',
        weight=10,
        condition_desc='IF Designing Interest == True AND Enjoys Designing Interfaces == Yes AND Design Interest == High THEN Recommend UI/UX Designer (+10)',
        explanation='Strong passion for design, high enjoyment in creating user interfaces, and keen artistic intuition.',
        condition_fn=lambda f: has_interest(f, 'Designing') and work_pref_is(f, 'design_interfaces', 'yes') and career_pref_is(f, 'design_interest', 'high')
    ),
    ExpertRule(
        rule_id='R_UIX_02',
        career_id='ui_ux_designer',
        career_name='UI/UX Designer',
        weight=10,
        condition_desc='IF Work Preference == Creative AND Preferred Work Area == UI & Design THEN Recommend UI/UX Designer (+10)',
        explanation='Creative focus aligned specifically with digital product design and human-computer interaction.',
        condition_fn=lambda f: work_pref_is(f, 'creative_analytical', 'creative') and career_pref_is(f, 'preferred_work_area', 'ui_ux')
    ),
    ExpertRule(
        rule_id='R_UIX_03',
        career_id='ui_ux_designer',
        career_name='UI/UX Designer',
        weight=5,
        condition_desc='IF HTML/CSS >= Beginner AND Designing Interest == True THEN Recommend UI/UX Designer (+5)',
        explanation='Valuable ability to bridge design mockups with frontend HTML/CSS styling.',
        condition_fn=lambda f: skill_at_least(f, 'HTML/CSS', 'beginner') and has_interest(f, 'Designing')
    ),
    ExpertRule(
        rule_id='R_UIX_04',
        career_id='ui_ux_designer',
        career_name='UI/UX Designer',
        weight=5,
        condition_desc='IF Coding Interest == Low/Medium AND Design Interest == High THEN Recommend UI/UX Designer (+5)',
        explanation='Preference for creative user experience and visual aesthetics over pure backend programming.',
        condition_fn=lambda f: (career_pref_is(f, 'coding_interest', 'low') or career_pref_is(f, 'coding_interest', 'medium')) and career_pref_is(f, 'design_interest', 'high')
    ),
    ExpertRule(
        rule_id='R_UIX_05',
        career_id='ui_ux_designer',
        career_name='UI/UX Designer',
        weight=5,
        condition_desc='IF Web Development Interest == True AND Work Preference == Creative THEN Recommend UI/UX Designer (+5)',
        explanation='Interest in web experiences expressed through creative user-centric design.',
        condition_fn=lambda f: has_interest(f, 'Web Development') and work_pref_is(f, 'creative_analytical', 'creative')
    ),
    ExpertRule(
        rule_id='R_UIX_06',
        career_id='ui_ux_designer',
        career_name='UI/UX Designer',
        weight=2,
        condition_desc='IF Designing Interest == True THEN Recommend UI/UX Designer (+2)',
        explanation='General interest in graphics, visuals, and design aesthetics.',
        condition_fn=lambda f: has_interest(f, 'Designing')
    ),
    ExpertRule(
        rule_id='R_UIX_07',
        career_id='ui_ux_designer',
        career_name='UI/UX Designer',
        weight=2,
        condition_desc='IF Enjoys Designing Interfaces == Yes/Somewhat THEN Recommend UI/UX Designer (+2)',
        explanation='Enjoyment in experimenting with screen layouts and user flows.',
        condition_fn=lambda f: work_pref_is(f, 'design_interfaces', 'yes') or work_pref_is(f, 'design_interfaces', 'somewhat')
    ),

    # -------------------------------------------------------------------------
    # 11. DEVOPS ENGINEER RULES (R_DVO_01 to R_DVO_07)
    # -------------------------------------------------------------------------
    ExpertRule(
        rule_id='R_DVO_01',
        career_id='devops_engineer',
        career_name='DevOps Engineer',
        weight=10,
        condition_desc='IF Cloud Computing Interest == True AND Linux >= Intermediate AND Git/GitHub >= Intermediate THEN Recommend DevOps Engineer (+10)',
        explanation='Core DevOps pillars detected: high cloud interest combined with solid Linux administration and Git version control mastery.',
        condition_fn=lambda f: has_interest(f, 'Cloud Computing') and skill_at_least(f, 'Linux', 'intermediate') and skill_at_least(f, 'Git/GitHub', 'intermediate')
    ),
    ExpertRule(
        rule_id='R_DVO_02',
        career_id='devops_engineer',
        career_name='DevOps Engineer',
        weight=10,
        condition_desc='IF AWS/Cloud >= Intermediate AND Programming Interest == True AND Enjoys Cloud Infrastructure == Yes THEN Recommend DevOps Engineer (+10)',
        explanation='Blend of cloud expertise, programming capability, and passion for continuous deployment infrastructure.',
        condition_fn=lambda f: skill_at_least(f, 'AWS/Cloud', 'intermediate') and has_interest(f, 'Programming') and work_pref_is(f, 'cloud_infrastructure', 'yes')
    ),
    ExpertRule(
        rule_id='R_DVO_03',
        career_id='devops_engineer',
        career_name='DevOps Engineer',
        weight=5,
        condition_desc='IF Python >= Beginner AND Linux >= Beginner THEN Recommend DevOps Engineer (+5)',
        explanation='Python scripting competence for building automated deployment pipelines and server tasks.',
        condition_fn=lambda f: skill_at_least(f, 'Python', 'beginner') and skill_at_least(f, 'Linux', 'beginner')
    ),
    ExpertRule(
        rule_id='R_DVO_04',
        career_id='devops_engineer',
        career_name='DevOps Engineer',
        weight=5,
        condition_desc='IF Preferred Work Area == Cloud & Infrastructure AND Coding Interest >= Medium THEN Recommend DevOps Engineer (+5)',
        explanation='Target career aspiration combining infrastructure management with software automation.',
        condition_fn=lambda f: career_pref_is(f, 'preferred_work_area', 'cloud') and not career_pref_is(f, 'coding_interest', 'low')
    ),
    ExpertRule(
        rule_id='R_DVO_05',
        career_id='devops_engineer',
        career_name='DevOps Engineer',
        weight=5,
        condition_desc='IF Networking Skill >= Beginner AND Cloud Technologies Interest == High THEN Recommend DevOps Engineer (+5)',
        explanation='Strong network protocol awareness combined with high drive for cloud orchestration.',
        condition_fn=lambda f: skill_at_least(f, 'Networking', 'beginner') and career_pref_is(f, 'cloud_interest', 'high')
    ),
    ExpertRule(
        rule_id='R_DVO_06',
        career_id='devops_engineer',
        career_name='DevOps Engineer',
        weight=2,
        condition_desc='IF Git/GitHub >= Beginner THEN Recommend DevOps Engineer (+2)',
        explanation='Familiarity with Git repositories and automated code versioning.',
        condition_fn=lambda f: skill_at_least(f, 'Git/GitHub', 'beginner')
    ),
    ExpertRule(
        rule_id='R_DVO_07',
        career_id='devops_engineer',
        career_name='DevOps Engineer',
        weight=2,
        condition_desc='IF Linux >= Beginner THEN Recommend DevOps Engineer (+2)',
        explanation='Command-line familiarity with Linux OS environments.',
        condition_fn=lambda f: skill_at_least(f, 'Linux', 'beginner')
    ),

    # -------------------------------------------------------------------------
    # 12. IOT ENGINEER RULES (R_IOT_01 to R_IOT_07)
    # -------------------------------------------------------------------------
    ExpertRule(
        rule_id='R_IOT_01',
        career_id='iot_engineer',
        career_name='IoT Engineer',
        weight=10,
        condition_desc='IF IoT Interest == True AND Hardware Interest == True AND Enjoys Hardware/Software Integration == Yes THEN Recommend IoT Engineer (+10)',
        explanation='Enthusiastic passion for the Internet of Things, electronics hardware, and embedded systems integration.',
        condition_fn=lambda f: has_interest(f, 'IoT') and has_interest(f, 'Hardware') and work_pref_is(f, 'hardware_software', 'yes')
    ),
    ExpertRule(
        rule_id='R_IOT_02',
        career_id='iot_engineer',
        career_name='IoT Engineer',
        weight=10,
        condition_desc='IF (C >= Intermediate OR C++ >= Intermediate) AND Hardware Interest == High THEN Recommend IoT Engineer (+10)',
        explanation='Strong embedded systems language proficiency (C or C++) combined with a high interest in physical electronics.',
        condition_fn=lambda f: (skill_at_least(f, 'C', 'intermediate') or skill_at_least(f, 'C++', 'intermediate')) and career_pref_is(f, 'hardware_interest', 'high')
    ),
    ExpertRule(
        rule_id='R_IOT_03',
        career_id='iot_engineer',
        career_name='IoT Engineer',
        weight=5,
        condition_desc='IF (Networking Skill >= Beginner OR Networking Interest == True) AND IoT Interest == True THEN Recommend IoT Engineer (+5)',
        explanation='Understanding of wireless device communication protocols (MQTT, Wi-Fi, BLE) for smart nodes.',
        condition_fn=lambda f: (skill_at_least(f, 'Networking', 'beginner') or has_interest(f, 'Networking')) and has_interest(f, 'IoT')
    ),
    ExpertRule(
        rule_id='R_IOT_04',
        career_id='iot_engineer',
        career_name='IoT Engineer',
        weight=5,
        condition_desc='IF Python >= Beginner AND Linux >= Beginner THEN Recommend IoT Engineer (+5)',
        explanation='Single-board computer readiness (Raspberry Pi/Linux) with Python scripting for IoT hubs.',
        condition_fn=lambda f: skill_at_least(f, 'Python', 'beginner') and skill_at_least(f, 'Linux', 'beginner')
    ),
    ExpertRule(
        rule_id='R_IOT_05',
        career_id='iot_engineer',
        career_name='IoT Engineer',
        weight=5,
        condition_desc='IF Preferred Work Area == IoT & Hardware THEN Recommend IoT Engineer (+5)',
        explanation='Explicit career aspiration to create smart connected hardware solutions.',
        condition_fn=lambda f: career_pref_is(f, 'preferred_work_area', 'iot')
    ),
    ExpertRule(
        rule_id='R_IOT_06',
        career_id='iot_engineer',
        career_name='IoT Engineer',
        weight=2,
        condition_desc='IF IoT Interest == True THEN Recommend IoT Engineer (+2)',
        explanation='Basic interest in sensor networks and smart home/industrial devices.',
        condition_fn=lambda f: has_interest(f, 'IoT')
    ),
    ExpertRule(
        rule_id='R_IOT_07',
        career_id='iot_engineer',
        career_name='IoT Engineer',
        weight=2,
        condition_desc='IF (C >= Beginner OR C++ >= Beginner) THEN Recommend IoT Engineer (+2)',
        explanation='Foundational knowledge of C/C++ memory and microcontroller syntax.',
        condition_fn=lambda f: skill_at_least(f, 'C', 'beginner') or skill_at_least(f, 'C++', 'beginner')
    ),
]


def calculate_career_max_scores():
    """
    Computes the maximum attainable score for each career category
    based on all production rules defined in the Knowledge Base.
    """
    max_scores = {}
    for rule in KNOWLEDGE_BASE_RULES:
        max_scores[rule.career_id] = max_scores.get(rule.career_id, 0) + rule.weight
    return max_scores

CAREER_MAX_SCORES = calculate_career_max_scores()
