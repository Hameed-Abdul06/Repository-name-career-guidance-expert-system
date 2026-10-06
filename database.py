"""
=============================================================================
CAREER GUIDANCE EXPERT SYSTEM - DATABASE LAYER (database.py)
=============================================================================
Academic Context: Artificial Intelligence  : Rule-Based Expert Systems
Storage Engine: SQLite3 (Local, lightweight, zero-dependency persistence)

Entities:
  1. students: Stores student demographic data (Name, Education, Course, Year)
  2. assessments: Stores timestamped raw working memory submissions
  3. results: Stores inference outcomes, top recommendations, and rule traces
=============================================================================
"""

import os
import sqlite3
import json
from datetime import datetime

# Resolve database file path dynamically relative to this script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(BASE_DIR, 'database')
DB_PATH = os.path.join(DB_DIR, 'career_guidance.db')

def get_db_connection():
    """
    Creates and returns a connection to the SQLite database
    configured with row-factory for dictionary-like column access.
    """
    if not os.path.exists(DB_DIR):
        os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    """
    Initializes the database schema if tables do not already exist.
    Safe to execute on application startup.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # Table 1: students
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        education_level TEXT NOT NULL,
        course TEXT NOT NULL,
        year_of_study TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # Table 2: assessments
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS assessments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER NOT NULL,
        raw_inputs_json TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
    );
    """)

    # Table 3: results
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        assessment_id INTEGER NOT NULL,
        top_career TEXT NOT NULL,
        top_score REAL NOT NULL,
        top_percentage REAL NOT NULL,
        second_career TEXT,
        second_percentage REAL,
        third_career TEXT,
        third_percentage REAL,
        rules_fired_count INTEGER DEFAULT 0,
        full_results_json TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (assessment_id) REFERENCES assessments(id) ON DELETE CASCADE
    );
    """)

    conn.commit()
    conn.close()

def save_assessment_record(student_info, raw_input, inference_result):
    """
    Persists student profile, assessment facts, and inferred results
    into SQLite within a single atomic transaction.
    Returns: newly generated assessment_id (int)
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # 1. Insert student
        cursor.execute("""
            INSERT INTO students (name, education_level, course, year_of_study)
            VALUES (?, ?, ?, ?)
        """, (
            student_info.get('name', 'Student'),
            student_info.get('education_level', 'Undergraduate'),
            student_info.get('course', 'Computer Science'),
            student_info.get('year_of_study', '3rd Year')
        ))
        student_id = cursor.lastrowid

        # 2. Insert assessment
        cursor.execute("""
            INSERT INTO assessments (student_id, raw_inputs_json)
            VALUES (?, ?)
        """, (
            student_id,
            json.dumps(raw_input)
        ))
        assessment_id = cursor.lastrowid

        # 3. Extract recommendations for quick indexing
        top = inference_result.get('top_recommendation') or {}
        other = inference_result.get('other_recommendations') or []
        second = other[0] if len(other) > 0 else {}
        third = other[1] if len(other) > 1 else {}

        # 4. Insert results
        cursor.execute("""
            INSERT INTO results (
                assessment_id,
                top_career,
                top_score,
                top_percentage,
                second_career,
                second_percentage,
                third_career,
                third_percentage,
                rules_fired_count,
                full_results_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            assessment_id,
            top.get('name', 'General Computing'),
            top.get('score', 0),
            top.get('match_percentage', 0.0),
            second.get('name', 'N/A'),
            second.get('match_percentage', 0.0),
            third.get('name', 'N/A'),
            third.get('match_percentage', 0.0),
            inference_result.get('inference_trace', {}).get('fired_rules', 0),
            json.dumps(inference_result)
        ))

        conn.commit()
        return assessment_id

    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def get_assessment_by_id(assessment_id):
    """
    Retrieves full assessment and inferred results by assessment ID.
    Returns: parsed dictionary of result payload or None.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            a.id AS assessment_id,
            a.created_at AS assessment_date,
            s.id AS student_id,
            s.name AS student_name,
            s.education_level,
            s.course,
            s.year_of_study,
            r.top_career,
            r.top_percentage,
            r.rules_fired_count,
            r.full_results_json
        FROM assessments a
        JOIN students s ON a.student_id = s.id
        JOIN results r ON r.assessment_id = a.id
        WHERE a.id = ?
    """, (assessment_id,))

    row = cursor.fetchone()
    conn.close()

    if not row:
        return None

    parsed_result = json.loads(row['full_results_json'])
    parsed_result['assessment_id'] = row['assessment_id']
    parsed_result['assessment_date'] = row['assessment_date']
    return parsed_result

def get_recent_assessments(limit=25):
    """
    Fetches the most recent assessments for history/audit dashboard.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            a.id AS assessment_id,
            a.created_at AS assessment_date,
            s.name AS student_name,
            s.education_level,
            s.course,
            r.top_career,
            r.top_percentage,
            r.rules_fired_count
        FROM assessments a
        JOIN students s ON a.student_id = s.id
        JOIN results r ON r.assessment_id = a.id
        ORDER BY a.id DESC
        LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_statistics():
    """
    Computes summary metrics for presentation and viva demonstrations.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM assessments;")
    total_assessments = cursor.fetchone()[0]

    cursor.execute("""
        SELECT top_career, COUNT(*) as cnt
        FROM results
        GROUP BY top_career
        ORDER BY cnt DESC
        LIMIT 5;
    """)
    top_careers = [dict(r) for r in cursor.fetchall()]

    conn.close()
    return {
        'total_assessments': total_assessments,
        'top_careers': top_careers
    }
