from inference_engine import engine

test_cases = [
    ('software_developer', {'interests': ['Programming', 'Problem Solving'], 'skills': {'java': 'intermediate', 'c++': 'intermediate', 'sql': 'beginner', 'git_github': 'beginner'}, 'logical_problems': 'yes', 'coding_interest': 'high', 'preferred_work_area': 'software'}),
    ('web_developer', {'interests': ['Web Development', 'Designing'], 'skills': {'html_css': 'intermediate', 'javascript': 'intermediate', 'git_github': 'beginner'}, 'design_interfaces': 'yes', 'coding_interest': 'medium', 'preferred_work_area': 'web'}),
    ('data_analyst', {'interests': ['Data Analysis', 'Databases'], 'skills': {'sql': 'intermediate', 'data_analysis': 'intermediate', 'python': 'beginner'}, 'working_with_data': 'yes', 'creative_analytical': 'analytical', 'math_data_interest': 'high', 'preferred_work_area': 'data_ai'}),
    ('data_scientist', {'interests': ['Data Analysis', 'Artificial Intelligence'], 'skills': {'python': 'intermediate', 'data_analysis': 'intermediate', 'sql': 'intermediate', 'linux': 'beginner', 'git_github': 'beginner'}, 'working_with_data': 'yes', 'creative_analytical': 'analytical', 'math_data_interest': 'high', 'coding_interest': 'medium', 'preferred_work_area': 'data_ai'}),
    ('ai_ml_engineer', {'interests': ['Artificial Intelligence', 'Programming'], 'skills': {'python': 'intermediate', 'c++': 'beginner', 'data_analysis': 'beginner', 'linux': 'beginner', 'git_github': 'beginner'}, 'logical_problems': 'yes', 'math_data_interest': 'high', 'coding_interest': 'high', 'preferred_work_area': 'data_ai'}),
    ('cloud_engineer', {'interests': ['Cloud Computing'], 'skills': {'aws_cloud': 'intermediate', 'linux': 'intermediate', 'networking': 'beginner', 'git_github': 'beginner', 'python': 'beginner'}, 'cloud_infrastructure': 'yes', 'cloud_interest': 'high', 'preferred_work_area': 'cloud'}),
    ('cybersecurity_analyst', {'interests': ['Cybersecurity', 'Problem Solving'], 'skills': {'networking': 'intermediate', 'linux': 'intermediate', 'python': 'beginner'}, 'security_problems': 'yes', 'security_interest': 'high', 'creative_analytical': 'analytical', 'preferred_work_area': 'security'}),
    ('network_engineer', {'interests': ['Networking'], 'skills': {'networking': 'intermediate', 'linux': 'intermediate', 'c': 'beginner'}, 'hardware_software': 'yes', 'hardware_interest': 'high', 'preferred_work_area': 'security'}),
    ('database_administrator', {'interests': ['Databases'], 'skills': {'sql': 'intermediate', 'linux': 'beginner', 'python': 'beginner'}, 'working_with_data': 'yes', 'logical_problems': 'yes', 'creative_analytical': 'analytical', 'math_data_interest': 'medium'}),
    ('ui_ux_designer', {'interests': ['Designing'], 'skills': {'html_css': 'beginner'}, 'design_interfaces': 'yes', 'creative_analytical': 'creative', 'design_interest': 'high', 'coding_interest': 'low', 'preferred_work_area': 'ui_ux'}),
    ('devops_engineer', {'interests': ['Cloud Computing', 'Programming'], 'skills': {'linux': 'intermediate', 'git_github': 'intermediate', 'aws_cloud': 'intermediate', 'python': 'beginner', 'networking': 'beginner'}, 'cloud_infrastructure': 'yes', 'cloud_interest': 'high', 'coding_interest': 'high', 'preferred_work_area': 'cloud'}),
    ('iot_engineer', {'interests': ['IoT', 'Hardware'], 'skills': {'c': 'intermediate', 'c++': 'intermediate', 'python': 'beginner', 'linux': 'beginner'}, 'hardware_software': 'yes', 'hardware_interest': 'high', 'preferred_work_area': 'iot'})
]

all_passed = True
print("-" * 80)
for expected_id, profile in test_cases:
    profile['student_name'] = 'Test ' + expected_id
    res = engine.evaluate_assessment(profile)
    top = res['top_recommendation']
    top_id = top['career_id']
    match_pct = top['match_percentage']
    score = top['score']
    passed = (top_id == expected_id)
    if not passed:
        all_passed = False
    status = "PASS [OK]" if passed else "FAIL [X]"
    print(f"{status} | Expected: {expected_id:<23} | Top Match: {top_id:<23} | Score: {score:>2}/39 ({match_pct:>4}%)")

print("-" * 80)
if all_passed:
    print("SUCCESS: ALL 12 CAREER PATH TEST PROFILES PASSED 100% ACCURATELY!")
else:
    print("WARNING: Some profiles need tuning.")
