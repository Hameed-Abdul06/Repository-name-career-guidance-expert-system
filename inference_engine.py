"""
=============================================================================
CAREER GUIDANCE EXPERT SYSTEM - INFERENCE ENGINE (inference_engine.py)
=============================================================================
Academic Context: Artificial Intelligence  : Rule-Based Expert Systems
Inference Mechanism: Forward-Chaining (Data-Driven Reasoning)

Forward-Chaining Cycle:
  1. Initialize Working Memory (Facts extracted from Student Assessment).
  2. Match: Match Premises (IF conditions) of Knowledge Base rules against Working Memory.
  3. Resolve Conflicts: Evaluate all eligible production rules.
  4. Fire / Act: Fire matched rules, accumulate confidence points (+10, +5, +2).
  5. Explain: Collect matched rule justifications for transparent explanation facility.
  6. Synthesize: Compute Match Percentages and perform Skill Gap Analysis.
  7. Rank: Produce Top-3 Career Recommendations.
=============================================================================
"""

import copy
from datetime import datetime
from rules import KNOWLEDGE_BASE_RULES, CAREER_METADATA, CAREER_MAX_SCORES, SKILL_LEVEL_MAP

class InferenceEngine:
    """
    Forward-Chaining Rule-Based Inference Engine.
    Executes production rules over student facts and generates explainable career rankings.
    """

    def __init__(self, rules=None, metadata=None, max_scores=None):
        self.rules = rules or KNOWLEDGE_BASE_RULES
        self.metadata = metadata or CAREER_METADATA
        self.max_scores = max_scores or CAREER_MAX_SCORES

    def build_working_memory(self, raw_input):
        """
        Step 1: Normalizes raw web form data into structured Working Memory (Fact Base).
        
        Working Memory Schema:
          - student_info: {name, education_level, course, year_of_study}
          - interests: list of interest strings
          - skills: dict of {skill_key: 'none'|'beginner'|'intermediate'|'advanced'}
          - work_prefs: dict of {preference_key: 'yes'|'no'|'somewhat'|...}
          - career_prefs: dict of {pref_key: 'high'|'medium'|'low'|work_area}
        """
        facts = {
            'student_info': {
                'name': raw_input.get('student_name', 'Student').strip() or 'Student',
                'education_level': raw_input.get('education_level', 'Undergraduate'),
                'course': raw_input.get('course', 'Computer Science'),
                'year_of_study': raw_input.get('year_of_study', '3rd Year')
            },
            'interests': raw_input.get('interests', []),
            'skills': {},
            'work_prefs': {
                'logical_problems': raw_input.get('logical_problems', 'no'),
                'design_interfaces': raw_input.get('design_interfaces', 'no'),
                'working_with_data': raw_input.get('working_with_data', 'no'),
                'cloud_infrastructure': raw_input.get('cloud_infrastructure', 'no'),
                'security_problems': raw_input.get('security_problems', 'no'),
                'hardware_software': raw_input.get('hardware_software', 'no'),
                'teamwork_style': raw_input.get('teamwork_style', 'team'),
                'creative_analytical': raw_input.get('creative_analytical', 'analytical')
            },
            'career_prefs': {
                'preferred_work_area': raw_input.get('preferred_work_area', 'software'),
                'coding_interest': raw_input.get('coding_interest', 'medium'),
                'math_data_interest': raw_input.get('math_data_interest', 'medium'),
                'cloud_interest': raw_input.get('cloud_interest', 'medium'),
                'security_interest': raw_input.get('security_interest', 'medium'),
                'hardware_interest': raw_input.get('hardware_interest', 'medium'),
                'design_interest': raw_input.get('design_interest', 'medium')
            }
        }

        # Normalize technical skills inputs
        standard_skills = [
            'c', 'c++', 'java', 'python', 'html/css', 'javascript',
            'sql', 'git/github', 'aws/cloud', 'networking', 'linux', 'data_analysis'
        ]
        
        raw_skills = raw_input.get('skills', {})
        for sk in standard_skills:
            # Look up either directly or formatted
            key_variants = [sk, sk.replace('/', '_'), sk.replace('+', 'p')]
            level = 'none'
            for v in key_variants:
                if v in raw_skills:
                    level = raw_skills[v]
                    break
                elif f"skill_{v}" in raw_input:
                    level = raw_input[f"skill_{v}"]
                    break
            
            normalized_key = sk.replace('/', '_')
            facts['skills'][normalized_key] = str(level).lower()

        return facts

    def run_forward_chaining(self, facts):
        """
        Step 2 to 5: Forward-Chaining Inference Process
        Iterates over production rules, evaluates conditions against Working Memory,
        and fires matching rules.
        """
        # Score accumulator: {career_id: total_score}
        career_scores = {cid: 0 for cid in self.metadata.keys()}
        
        # Rule firing trace: {career_id: [matched_rule_objects]}
        fired_rules_by_career = {cid: [] for cid in self.metadata.keys()}
        
        # Reasons list for user explanation facility
        explanations_by_career = {cid: [] for cid in self.metadata.keys()}

        total_rules_evaluated = len(self.rules)
        total_rules_fired = 0

        # INFERENCE LOOP (Forward Chaining)
        for rule in self.rules:
            if rule.evaluate(facts):
                # Rule Premise is TRUE -> Fire Rule (Antecedent matches -> Consequent triggers)
                career_id = rule.career_id
                career_scores[career_id] += rule.weight
                fired_rules_by_career[career_id].append({
                    'rule_id': rule.rule_id,
                    'condition_desc': rule.condition_desc,
                    'weight': rule.weight,
                    'explanation': rule.explanation
                })
                explanations_by_career[career_id].append(rule.explanation)
                total_rules_fired += 1

        return {
            'scores': career_scores,
            'fired_rules': fired_rules_by_career,
            'explanations': explanations_by_career,
            'stats': {
                'total_rules': total_rules_evaluated,
                'fired_rules': total_rules_fired,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        }

    def analyze_skill_gap(self, career_id, facts):
        """
        Performs skill gap analysis between career requirements and student's current proficiency.
        Identifies:
          - Skills student already possesses (Beginner, Intermediate, Advanced)
          - Skills student needs to acquire or level up
        """
        meta = self.metadata.get(career_id, {})
        required_skills = meta.get('required_skills', [])
        
        skills_possessed = []
        skills_to_learn = []

        for req in required_skills:
            normalized_req = req.lower().replace('/', '_')
            current_level = facts['skills'].get(normalized_req, 'none')
            
            if current_level in ['intermediate', 'advanced']:
                skills_possessed.append({
                    'skill': req,
                    'level': current_level.capitalize(),
                    'status': 'Strong Match'
                })
            elif current_level == 'beginner':
                skills_possessed.append({
                    'skill': req,
                    'level': 'Beginner',
                    'status': 'Foundational'
                })
                # Also recommend leveling up from beginner
                skills_to_learn.append({
                    'skill': req,
                    'reason': f"Level up from Beginner to Intermediate/Advanced for industry readiness.",
                    'priority': 'Medium'
                })
            else:
                skills_to_learn.append({
                    'skill': req,
                    'reason': f"Core prerequisite for {meta.get('name')}.",
                    'priority': 'High'
                })

        return skills_possessed, skills_to_learn

    def evaluate_assessment(self, raw_input):
        """
        Main public interface of the Inference Engine.
        Executes end-to-end forward chaining, synthesizes scores, ranks careers,
        and constructs rich, viva-ready explanation payloads.
        """
        # Step 1: Initialize Working Memory
        facts = self.build_working_memory(raw_input)

        # Step 2: Forward Chaining Execution
        inference_result = self.run_forward_chaining(facts)
        scores = inference_result['scores']
        fired_rules = inference_result['fired_rules']
        explanations = inference_result['explanations']

        # Step 3: Compute Match Percentages
        # Match % = (Score Obtained / Maximum Possible Score) * 100
        career_rankings = []
        for cid, meta in self.metadata.items():
            obtained = scores.get(cid, 0)
            max_score = self.max_scores.get(cid, 39)
            
            # Match percentage bounded between 0% and 100%
            match_pct = round((obtained / max_score) * 100, 1) if max_score > 0 else 0.0
            match_pct = min(100.0, match_pct)

            skills_have, skills_learn = self.analyze_skill_gap(cid, facts)

            career_rankings.append({
                'career_id': cid,
                'name': meta['name'],
                'icon': meta['icon'],
                'score': obtained,
                'max_score': max_score,
                'match_percentage': match_pct,
                'description': meta['description'],
                'required_skills': meta['required_skills'],
                'skills_you_have': skills_have,
                'skills_to_learn': skills_learn,
                'possible_job_roles': meta['possible_job_roles'],
                'learning_roadmap': meta['learning_roadmap'],
                'explanations': explanations.get(cid, []),
                'fired_rules': fired_rules.get(cid, []),
                'fired_rules_count': len(fired_rules.get(cid, []))
            })

        # Step 4: Conflict Resolution / Ranking (Sort descending by score, then match %)
        career_rankings.sort(key=lambda c: (c['score'], c['match_percentage']), reverse=True)

        # Assign rank numbers
        for idx, item in enumerate(career_rankings, start=1):
            item['rank'] = idx

        # Step 5: Structure Top-3 Recommendations & Explanation Payload
        top_recommendation = career_rankings[0] if career_rankings else None
        other_recommendations = career_rankings[1:3] if len(career_rankings) > 1 else []

        # Default fallback explanation if zero rules fired (edge case)
        if top_recommendation and not top_recommendation['explanations']:
            top_recommendation['explanations'] = [
                "Based on baseline educational background and foundational technical profile."
            ]

        return {
            'student_info': facts['student_info'],
            'facts_summary': {
                'interests': facts['interests'],
                'skills': facts['skills'],
                'work_prefs': facts['work_prefs'],
                'career_prefs': facts['career_prefs']
            },
            'top_recommendation': top_recommendation,
            'other_recommendations': other_recommendations,
            'all_rankings': career_rankings,
            'inference_trace': {
                'total_rules': inference_result['stats']['total_rules'],
                'fired_rules': inference_result['stats']['fired_rules'],
                'timestamp': inference_result['stats']['timestamp']
            }
        }


# Global Singleton Inference Engine instance
engine = InferenceEngine()
