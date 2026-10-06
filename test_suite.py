"""
Automated Integration and Verification Test Suite
Tests all pages, endpoints, forward-chaining rule matching, SQLite storage,
and diverse student career profiles.
"""

import unittest
from app import app
from database import get_db_connection, init_db
from rules import KNOWLEDGE_BASE_RULES, CAREER_METADATA

class TestCareerGuidanceExpertSystem(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        with self.app.app_context():
            init_db()

    def test_01_home_page(self):
        """Test GET / returns 200 and displays project branding."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        content = response.data.decode('utf-8')
        self.assertIn("Career Guidance", content)
        self.assertIn("Expert System", content)
        self.assertIn("Rule-Based AI", content)
        self.assertIn("Personalized Recommendations", content)
        self.assertIn("Explainable Results", content)

    def test_02_assessment_get(self):
        """Test GET /assessment loads all 5 sections and form controls."""
        response = self.client.get('/assessment')
        self.assertEqual(response.status_code, 200)
        content = response.data.decode('utf-8')
        self.assertIn("Section 1: Student Information", content)
        self.assertIn("Section 2: Core Interests", content)
        self.assertIn("Section 3: Technical Skills Level", content)
        self.assertIn("Section 4: Work Preferences", content)
        self.assertIn("Section 5: Career Preferences", content)

    def test_03_cybersecurity_profile_post(self):
        """Test POST /assessment with a Cybersecurity-focused profile."""
        payload = {
            'student_name': 'Rohan Varma',
            'education_level': 'Bachelor / B.Tech / B.Sc',
            'course': 'Computer Science & Engineering',
            'year_of_study': '3rd Year',
            'interests': ['Cybersecurity', 'Networking', 'Problem Solving'],
            'skill_networking': 'intermediate',
            'skill_linux': 'intermediate',
            'skill_python': 'beginner',
            'logical_problems': 'yes',
            'design_interfaces': 'no',
            'working_with_data': 'no',
            'cloud_infrastructure': 'no',
            'security_problems': 'yes',
            'hardware_software': 'no',
            'teamwork_style': 'team',
            'creative_analytical': 'analytical',
            'preferred_work_area': 'security',
            'coding_interest': 'medium',
            'math_data_interest': 'medium',
            'cloud_interest': 'low',
            'security_interest': 'high',
            'hardware_interest': 'low',
            'design_interest': 'low'
        }
        response = self.client.post('/assessment', data=payload, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        content = response.data.decode('utf-8')
        self.assertIn("Your Career Guidance Results", content)
        self.assertIn("Cybersecurity Analyst", content)
        self.assertIn("Why This Career Matches You", content)
        self.assertIn("Skills You Already Have", content)
        self.assertIn("Skills You Should Learn", content)

    def test_04_ui_ux_profile_post(self):
        """Test POST /assessment with a UI/UX Designer-focused profile."""
        payload = {
            'student_name': 'Ananya Sen',
            'education_level': 'Bachelor / B.Tech / B.Sc',
            'course': 'Information Technology',
            'year_of_study': '2nd Year',
            'interests': ['Designing', 'Web Development'],
            'skill_html_css': 'beginner',
            'logical_problems': 'no',
            'design_interfaces': 'yes',
            'working_with_data': 'no',
            'cloud_infrastructure': 'no',
            'security_problems': 'no',
            'hardware_software': 'no',
            'teamwork_style': 'team',
            'creative_analytical': 'creative',
            'preferred_work_area': 'ui_ux',
            'coding_interest': 'low',
            'math_data_interest': 'low',
            'cloud_interest': 'low',
            'security_interest': 'low',
            'hardware_interest': 'low',
            'design_interest': 'high'
        }
        response = self.client.post('/assessment', data=payload, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        content = response.data.decode('utf-8')
        self.assertIn("UI/UX Designer", content)

    def test_05_about_page(self):
        """Test GET /about displays academic expert system theory and viva FAQs."""
        response = self.client.get('/about')
        self.assertEqual(response.status_code, 200)
        content = response.data.decode('utf-8')
        self.assertIn("What is an Expert System?", content)
        self.assertIn("What is a Knowledge Base?", content)
        self.assertIn("What are IF–THEN Rules?", content)
        self.assertIn("What is an Inference Engine?", content)
        self.assertIn("Rule-Based Expert System vs Machine Learning", content)

    def test_06_history_page(self):
        """Test GET /history displays logged student assessments."""
        response = self.client.get('/history')
        self.assertEqual(response.status_code, 200)
        content = response.data.decode('utf-8')
        self.assertIn("Assessment Records & Audit History", content)
        self.assertIn("Rohan Varma", content)

    def test_07_rules_api(self):
        """Test GET /api/rules returns all 84 production rules in JSON format."""
        response = self.client.get('/api/rules')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['total_rules'], 84)
        self.assertEqual(len(data['rules']), 84)
        self.assertEqual(data['rules'][0]['rule_id'], 'R_SWD_01')

if __name__ == '__main__':
    unittest.main()
