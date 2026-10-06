"""
=============================================================================
CAREER GUIDANCE EXPERT SYSTEM - FLASK APPLICATION CONTROLLER (app.py)
=============================================================================
Academic Context: Artificial Intelligence  : Rule-Based Expert Systems
Framework: Flask (Python Web Framework)

Routes:
  - /             : Landing page with project overview, AI principles & features
  - /assessment   : Multi-section interactive career assessment wizard (GET & POST)
  - /results/<id> : Inferred career recommendations, explanations, and skill roadmap
  - /about        : In-depth viva study guide: Expert Systems, KB, Inference Engine
  - /history      : Audit log of past student assessments stored in SQLite
  - /api/rules    : Interactive API exposing all 84 production rules for inspection
=============================================================================
"""

import os
import secrets
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from database import init_db, save_assessment_record, get_assessment_by_id, get_recent_assessments, get_statistics
from inference_engine import engine
from rules import KNOWLEDGE_BASE_RULES, CAREER_METADATA

app = Flask(__name__)
# Generate or fetch session secret key
app.secret_key = os.environ.get('SECRET_KEY', secrets.token_hex(24))

# Ensure database tables are created on app startup
with app.app_context():
    init_db()

@app.route('/')
def index():
    """
    Home Landing Page.
    Presents the Expert System purpose, architecture summary, and primary call-to-actions.
    """
    stats = get_statistics()
    return render_template('index.html',
                           careers=CAREER_METADATA,
                           total_rules=len(KNOWLEDGE_BASE_RULES),
                           stats=stats)

@app.route('/assessment', methods=['GET', 'POST'])
def assessment():
    """
    Career Assessment Route:
      - GET: Renders the 5-section career assessment form.
      - POST: Extracts facts, invokes the Forward-Chaining Inference Engine,
              stores result in SQLite, and redirects to the results dashboard.
    """
    if request.method == 'GET':
        return render_template('assessment.html', careers=CAREER_METADATA)

    # Handle POST submission
    try:
        # 1. Extract Student Demographic Data (Section 1)
        student_info = {
            'name': request.form.get('student_name', '').strip() or 'Anonymous Student',
            'education_level': request.form.get('education_level', 'Bachelor / B.Tech / B.Sc'),
            'course': request.form.get('course', 'Computer Science & Engineering'),
            'year_of_study': request.form.get('year_of_study', '3rd Year')
        }

        # 2. Extract Interests (Section 2 - Multi-select checkboxes)
        interests = request.form.getlist('interests')

        # 3. Extract Technical Skills (Section 3 - Proficiency radio buttons)
        skill_keys = [
            'c', 'cpp', 'java', 'python', 'html_css', 'javascript',
            'sql', 'git_github', 'aws_cloud', 'networking', 'linux', 'data_analysis'
        ]
        skills = {}
        for k in skill_keys:
            val = request.form.get(f"skill_{k}", 'none').lower()
            # Map 'cpp' to 'c++' for standardized rule matching
            norm_key = 'c++' if k == 'cpp' else k
            skills[norm_key] = val

        # 4. Extract Work Preferences (Section 4)
        work_prefs = {
            'logical_problems': request.form.get('logical_problems', 'no'),
            'design_interfaces': request.form.get('design_interfaces', 'no'),
            'working_with_data': request.form.get('working_with_data', 'no'),
            'cloud_infrastructure': request.form.get('cloud_infrastructure', 'no'),
            'security_problems': request.form.get('security_problems', 'no'),
            'hardware_software': request.form.get('hardware_software', 'no'),
            'teamwork_style': request.form.get('teamwork_style', 'team'),
            'creative_analytical': request.form.get('creative_analytical', 'analytical')
        }

        # 5. Extract Career Preferences (Section 5)
        career_prefs = {
            'preferred_work_area': request.form.get('preferred_work_area', 'software'),
            'coding_interest': request.form.get('coding_interest', 'medium'),
            'math_data_interest': request.form.get('math_data_interest', 'medium'),
            'cloud_interest': request.form.get('cloud_interest', 'medium'),
            'security_interest': request.form.get('security_interest', 'medium'),
            'hardware_interest': request.form.get('hardware_interest', 'medium'),
            'design_interest': request.form.get('design_interest', 'medium')
        }

        # Combine into complete raw input package
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

        # 6. INFERENCE ENGINE EXECUTION (Forward-Chaining)
        inference_result = engine.evaluate_assessment(raw_input)

        # 7. Persist to SQLite Database
        assessment_id = save_assessment_record(student_info, raw_input, inference_result)
        
        # Store latest id in session as convenience
        session['latest_assessment_id'] = assessment_id

        flash(f"Assessment completed successfully! Rule-based inference generated recommendations for {student_info['name']}.", "success")
        return redirect(url_for('results', assessment_id=assessment_id))

    except Exception as e:
        flash(f"An error occurred during assessment evaluation: {str(e)}", "danger")
        return redirect(url_for('assessment'))

@app.route('/results/<int:assessment_id>')
def results(assessment_id):
    """
    Results Dashboard.
    Displays Top Recommendation, Other Suitable Careers, Rule Matching Explanations,
    Skill Gaps, and Suggested Learning Roadmap.
    """
    result_data = get_assessment_by_id(assessment_id)
    if not result_data:
        flash("Assessment record not found. Please complete the assessment form first.", "warning")
        return redirect(url_for('assessment'))

    return render_template('results.html',
                           result=result_data,
                           assessment_id=assessment_id)

@app.route('/results')
def results_latest():
    """Fallback endpoint redirecting to the user's most recent assessment."""
    latest_id = session.get('latest_assessment_id')
    if latest_id:
        return redirect(url_for('results', assessment_id=latest_id))
    flash("No active assessment found. Please start a new career assessment.", "info")
    return redirect(url_for('assessment'))

@app.route('/about')
def about():
    """
    Educational & Viva Presentation Page.
    Explains the theoretical foundations of Rule-Based Expert Systems,
    Knowledge Bases, Forward Chaining, and viva-ready FAQs.
    """
    return render_template('about.html',
                           careers=CAREER_METADATA,
                           total_rules=len(KNOWLEDGE_BASE_RULES))

@app.route('/history')
def history():
    """
    History Page: Displays list of past student career assessments stored in SQLite.
    """
    recent = get_recent_assessments(limit=30)
    stats = get_statistics()
    return render_template('history.html',
                           assessments=recent,
                           stats=stats)

@app.route('/api/rules')
def api_rules():
    """
    Debug & Inspection API.
    Returns structured JSON of all production rules defined in the Knowledge Base.
    """
    rules_data = []
    for r in KNOWLEDGE_BASE_RULES:
        rules_data.append({
            'rule_id': r.rule_id,
            'career_id': r.career_id,
            'career_name': r.career_name,
            'weight': r.weight,
            'condition_desc': r.condition_desc,
            'explanation': r.explanation
        })
    return jsonify({
        'total_rules': len(rules_data),
        'rules': rules_data
    })

# Custom HTTP Error Handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('index.html', error="404: The requested page was not found."), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('index.html', error="500: An unexpected internal server error occurred."), 500

if __name__ == '__main__':
    # College Mini-Project local development execution
    print("=" * 70)
    print(" CAREER GUIDANCE EXPERT SYSTEM - AI   MINI PROJECT")
    print(" Rule-Based Forward-Chaining Inference Engine Initialized")
    print(f" Knowledge Base Loaded: {len(KNOWLEDGE_BASE_RULES)} Production Rules")
    print(" Server running on: http://127.0.0.1:5000")
    print("=" * 70)
    app.run(debug=True, host='127.0.0.1', port=5000)
