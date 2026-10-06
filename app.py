"""
=============================================================================
CAREER GUIDANCE EXPERT SYSTEM - FLASK APPLICATION CONTROLLER (app.py)
=============================================================================
Academic Context: Artificial Intelligence : Rule-Based Expert Systems
Framework: Flask

Architecture:
    User Input
        ↓
    Knowledge Base (84 IF-THEN Rules)
        ↓
    Forward-Chaining Inference Engine
        ↓
    Career Recommendations
        ↓
    Results Dashboard

NOTE:
This version does NOT use SQLite or any persistent database.
Assessment input is temporarily stored in the Flask session so that
the results can be generated without a database.
=============================================================================
"""

import os
import secrets

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session

from inference_engine import engine
from rules import KNOWLEDGE_BASE_RULES, CAREER_METADATA


app = Flask(__name__)

# Secret key for Flask session.
# For production/Vercel, set SECRET_KEY as an environment variable.
app.secret_key = os.environ.get(
    'SECRET_KEY',
    'career-guidance-expert-system-demo-secret-key'
)


@app.route('/')
def index():
    """
    Home Landing Page.

    Presents:
    - Project overview
    - Expert System architecture
    - Number of careers
    - Number of production rules
    """

    return render_template(
        'index.html',
        careers=CAREER_METADATA,
        total_rules=len(KNOWLEDGE_BASE_RULES)
    )


@app.route('/assessment', methods=['GET', 'POST'])
def assessment():
    """
    Career Assessment Route.

    GET:
        Displays the career assessment form.

    POST:
        1. Collects student information.
        2. Collects interests.
        3. Collects technical skills.
        4. Collects work preferences.
        5. Collects career preferences.
        6. Sends the complete input to the Forward-Chaining
           Inference Engine.
        7. Temporarily stores the raw assessment in the Flask session.
        8. Redirects to the results page.

    No database is used.
    """

    if request.method == 'GET':
        return render_template(
            'assessment.html',
            careers=CAREER_METADATA
        )

    try:

        # ==============================================================
        # 1. STUDENT INFORMATION
        # ==============================================================

        student_info = {
            'name': (
                request.form.get('student_name', '').strip()
                or 'Anonymous Student'
            ),

            'education_level': request.form.get(
                'education_level',
                'Bachelor / B.Tech / B.Sc'
            ),

            'course': request.form.get(
                'course',
                'Computer Science & Engineering'
            ),

            'year_of_study': request.form.get(
                'year_of_study',
                '3rd Year'
            )
        }


        # ==============================================================
        # 2. INTERESTS
        # ==============================================================

        interests = request.form.getlist('interests')


        # ==============================================================
        # 3. TECHNICAL SKILLS
        # ==============================================================

        skill_keys = [
            'c',
            'cpp',
            'java',
            'python',
            'html_css',
            'javascript',
            'sql',
            'git_github',
            'aws_cloud',
            'networking',
            'linux',
            'data_analysis'
        ]

        skills = {}

        for key in skill_keys:

            value = request.form.get(
                f'skill_{key}',
                'none'
            ).lower()

            # Normalize cpp → c++
            normalized_key = 'c++' if key == 'cpp' else key

            skills[normalized_key] = value


        # ==============================================================
        # 4. WORK PREFERENCES
        # ==============================================================

        work_prefs = {

            'logical_problems': request.form.get(
                'logical_problems',
                'no'
            ),

            'design_interfaces': request.form.get(
                'design_interfaces',
                'no'
            ),

            'working_with_data': request.form.get(
                'working_with_data',
                'no'
            ),

            'cloud_infrastructure': request.form.get(
                'cloud_infrastructure',
                'no'
            ),

            'security_problems': request.form.get(
                'security_problems',
                'no'
            ),

            'hardware_software': request.form.get(
                'hardware_software',
                'no'
            ),

            'teamwork_style': request.form.get(
                'teamwork_style',
                'team'
            ),

            'creative_analytical': request.form.get(
                'creative_analytical',
                'analytical'
            )
        }


        # ==============================================================
        # 5. CAREER PREFERENCES
        # ==============================================================

        career_prefs = {

            'preferred_work_area': request.form.get(
                'preferred_work_area',
                'software'
            ),

            'coding_interest': request.form.get(
                'coding_interest',
                'medium'
            ),

            'math_data_interest': request.form.get(
                'math_data_interest',
                'medium'
            ),

            'cloud_interest': request.form.get(
                'cloud_interest',
                'medium'
            ),

            'security_interest': request.form.get(
                'security_interest',
                'medium'
            ),

            'hardware_interest': request.form.get(
                'hardware_interest',
                'medium'
            ),

            'design_interest': request.form.get(
                'design_interest',
                'medium'
            )
        }


        # ==============================================================
        # 6. COMPLETE INPUT PACKAGE
        # ==============================================================

        raw_input = {

            'student_name': student_info['name'],

            'education_level': student_info['education_level'],

            'course': student_info['course'],

            'year_of_study': student_info['year_of_study'],

            'interests': interests,

            'skills': skills,

            **work_prefs,

            **career_prefs
        }


        # ==============================================================
        # 7. FORWARD-CHAINING INFERENCE ENGINE
        # ==============================================================

        inference_result = engine.evaluate_assessment(raw_input)


        # ==============================================================
        # 8. STORE ONLY RAW INPUT IN SESSION
        # ==============================================================
        #
        # We do NOT store the complete inference result.
        # The result is recalculated on the results page.
        #
        # This avoids using SQLite or any persistent database.
        #

        session['latest_assessment'] = raw_input

        flash(
            f"Assessment completed successfully! "
            f"Rule-based inference generated recommendations "
            f"for {student_info['name']}.",
            "success"
        )

        return redirect(url_for('results'))


    except Exception as e:

        flash(
            f"An error occurred during assessment evaluation: {str(e)}",
            "danger"
        )

        return redirect(url_for('assessment'))


@app.route('/results')
def results():
    """
    Results Dashboard.

    The raw assessment is retrieved from the Flask session.
    The Forward-Chaining Inference Engine evaluates it again.

    No database is required.
    """

    raw_input = session.get('latest_assessment')

    if not raw_input:

        flash(
            "No active assessment found. Please complete the assessment first.",
            "info"
        )

        return redirect(url_for('assessment'))


    try:

        # Re-run the existing inference engine.
        result_data = engine.evaluate_assessment(raw_input)

        return render_template(
            'results.html',
            result=result_data
        )


    except Exception as e:

        flash(
            f"Unable to generate results: {str(e)}",
            "danger"
        )

        return redirect(url_for('assessment'))


@app.route('/about')
def about():
    """
    Educational & Viva Presentation Page.

    Explains:
    - Rule-Based Expert Systems
    - Knowledge Base
    - IF-THEN Rules
    - Forward Chaining
    - Inference Engine
    """

    return render_template(
        'about.html',
        careers=CAREER_METADATA,
        total_rules=len(KNOWLEDGE_BASE_RULES)
    )


@app.route('/api/rules')
def api_rules():
    """
    Debug & Inspection API.

    Returns all 84 production rules from the Knowledge Base.
    """

    rules_data = []

    for rule in KNOWLEDGE_BASE_RULES:

        rules_data.append({

            'rule_id': rule.rule_id,

            'career_id': rule.career_id,

            'career_name': rule.career_name,

            'weight': rule.weight,

            'condition_desc': rule.condition_desc,

            'explanation': rule.explanation

        })

    return jsonify({

        'total_rules': len(rules_data),

        'rules': rules_data

    })


# ==============================================================
# CUSTOM HTTP ERROR HANDLERS
# ==============================================================

@app.errorhandler(404)
def page_not_found(error):

    return render_template(
        'index.html',
        error="404: The requested page was not found.",
        careers=CAREER_METADATA,
        total_rules=len(KNOWLEDGE_BASE_RULES)
    ), 404


@app.errorhandler(500)
def internal_server_error(error):

    return render_template(
        'index.html',
        error="500: An unexpected internal server error occurred.",
        careers=CAREER_METADATA,
        total_rules=len(KNOWLEDGE_BASE_RULES)
    ), 500


# ==============================================================
# LOCAL DEVELOPMENT
# ==============================================================

if __name__ == '__main__':

    print("=" * 70)

    print(" CAREER GUIDANCE EXPERT SYSTEM - AI MINI PROJECT")

    print(" Rule-Based Forward-Chaining Inference Engine Initialized")

    print(
        f" Knowledge Base Loaded: "
        f"{len(KNOWLEDGE_BASE_RULES)} Production Rules"
    )

    print(" Database: NOT USED")

    print(" Server running on: http://127.0.0.1:5000")

    print("=" * 70)

    app.run(
        debug=True,
        host='127.0.0.1',
        port=5000
    )