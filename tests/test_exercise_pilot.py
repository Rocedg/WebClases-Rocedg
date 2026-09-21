"""Pilot contracts: safe source, structured grading and submission-only solutions."""

import re
from pathlib import Path

import pytest
from flask import render_template

from app import app, load_exercise_catalogue
from database import db
from models import ExerciseAttempt
from services.exercise_attempt_service import response_fields, start_or_resume_attempt, submit_attempt
from services.exercise_presentation import render_exercise_source, response_format_notes


PILOT_IDS = {'t0_v_018', 't0_c_020', 't1_r_004', 't1_g_011', 't2_h_001', 't2_c_001'}
ANSWERS = {
    't0_v_018': {'response_1': 'vertical', 'Px': '-24,8', 'normal': '53,3'},
    't0_c_020': {'zero_time': '36/7', 'positive_area': '100/7', 'negative_signed': '-9/7', 'displacement': '13', 'distance': '109/7'},
    't1_r_004': {'x0': '18', 'x4': '10', 'x10': '-2', 't0': '9', 'v': '-2'},
    't1_g_011': {'dx_given': '12', 'dx_area': '9', 'correct': 'quadratic'},
    't2_h_001': {'t': '2', 'range': '12', 'v': '(6; -20)', 'speed': '20,9', 'angle': '73,3'},
    't2_c_001': {'f': '1,5', 'period': '0,667', 'omega': '9,42', 'angle': '37,7', 'turns': '6'},
}


def test_source_escapes_html_and_preserves_math_and_parts():
    html = str(render_exercise_source(
        '<img src=x onerror=alert(1)>\n\nSegundo párrafo con \\(x<2\\).\n'
        '(a) Calcula.\n(b) Lee \\[\nf(x)=x^2\n\\].\n\nFinal.'
    ))
    assert '<img' not in html
    assert '&lt;img' in html
    assert '\\(x&lt;2\\)' in html
    assert '\\[ f(x)=x^2 \\]' in html
    assert html.count('<p>') == 3
    assert html.count('<li ') == 2
    assert 'value="2" data-part="b"' in html
    assert '</ol><p>Final.</p>' in html
    assert str(render_exercise_source('(a)Primera\n(b)Segunda')).count('<li ') == 2


def test_pilot_exercises_remain_structured_after_full_migration():
    pilots = [e for e in load_exercise_catalogue()['exercises'] if 'statement_source' in e]
    assert PILOT_IDS.issubset({e['id'] for e in pilots})
    for exercise in [item for item in pilots if item['id'] in PILOT_IDS]:
        assert 'statement' not in exercise and 'solution' not in exercise
        assert 'interactions' not in exercise
        assert not exercise.get('hints')
        assert '$' not in exercise['statement_source'] + exercise['solution_source']
        assert not re.search(r'<[a-zA-Z]', exercise['statement_source'] + exercise['solution_source'])
        assert exercise['status'] == ('active' if exercise['topic'] == 't0' else 'draft')
        for field in response_fields(exercise):
            assert field['type'] in {'numeric', 'single_choice', 'vector'}
            assert f"({field['part']})" in exercise['statement_source']
        for asset in exercise['assets']:
            svg = Path(asset['path']).read_text(encoding='utf8')
            assert 'viewBox=' in svg and '<title' in svg and '<desc' in svg


@pytest.mark.parametrize('exercise_id', sorted(PILOT_IDS))
def test_pilot_submit_corrects_all_fields_and_reveals_solution_only_afterwards(exercise_id):
    client = app.test_client()
    client.post('/login', data={'username': 'Guest', 'password': 'studentpass'})
    exercise = next(e for e in load_exercise_catalogue()['exercises'] if e['id'] == exercise_id)
    preview = client.get(f'/exercise/{exercise_id}').get_data(as_text=True)
    active = client.post(f'/exercise/{exercise_id}/start', follow_redirects=True).get_data(as_text=True)
    for html in (preview, active):
        assert 'exercise-solution' not in html
        assert str(render_exercise_source(exercise['solution_source'])) not in html
        for secret in ['expected_value', 'expected_components', 'correct_option_id', 'accepted_forms']:
            assert secret not in html
    assert active.count('Indicaciones de formato') == 1
    assert 'placeholder=' in active
    assert 'Ver pista' not in active
    if exercise_id == 't0_c_020':
        for leaked in ['5.143', '14.286', '-1.286', '15.571', '36/7', '109/7']:
            assert leaked not in active
    with app.app_context():
        attempt_id = ExerciseAttempt.query.one().id
    submitted = client.post(
        f'/exercise/{exercise_id}/attempt/{attempt_id}/submit',
        data={f'response_{key}': value for key, value in ANSWERS[exercise_id].items()},
        follow_redirects=True,
    )
    assert submitted.status_code == 200
    assert str(render_exercise_source(exercise['solution_source'])) in submitted.get_data(as_text=True)
    with app.app_context():
        attempt = db.session.get(ExerciseAttempt, attempt_id)
        assert all(r.grading_status == 'correct' for r in attempt.responses)
        assert attempt.score == attempt.max_score == len(ANSWERS[exercise_id])


@pytest.mark.parametrize('value,correct', [
    ('(6,0; -2e1)', True), ('(6; -40/2)', True), ('(-20; 6)', False),
    ('(6, -20)', False), ('(6; -20; 0)', False), ('', False),
    ('(__import__("os"); -20)', False),
])
def test_vector_grading_checks_order_count_and_numeric_syntax(value, correct):
    exercise = next(e for e in load_exercise_catalogue()['exercises'] if e['id'] == 't2_h_001')
    with app.app_context():
        attempt, _ = start_or_resume_attempt('Guest', exercise)
        submit_attempt('Guest', attempt.id, exercise, {**ANSWERS['t2_h_001'], 'v': value})
        result = next(r for r in attempt.responses if r.field_id == 'v')
        assert result.grading_status == ('correct' if correct else 'incorrect')


def test_format_notes_are_deduplicated_and_follow_actual_types():
    fields = [{'type': 'numeric'}, {'type': 'numeric'}, {'type': 'vector'}]
    notes = response_format_notes(fields)
    assert len(notes) == 2
    assert not any('Funciones:' in note for note in notes)
    assert any('Funciones:' in note for note in response_format_notes([{'type': 'open_text', 'response_kind': 'function'}]))


def test_private_content_is_not_a_public_json_endpoint_and_legacy_html_compatibility_remains():
    client = app.test_client()
    client.post('/login', data={'username': 'Guest', 'password': 'studentpass'})
    assert client.get('/content/exercises/1bach/t0/exercises_t0.json').status_code == 404
    assert client.get('/static/exercises/1bach/t0/exercises_t0.json').status_code == 404
    legacy_statement = '<p>Legado con $x=2$.</p>'
    with app.test_request_context('/exercise/legacy'):
        html = render_template(
            'user/exercise_detail.html',
            exercise={'id': 'legacy', 'title': 'Legacy', 'concept': 'Test', 'course': '1bach',
                      'topic': 'legacy', 'difficulty': 2, 'statement': legacy_statement, 'assets': []},
            attempt=None, fields=[], responses={}, next_exercise=None, next_attempt_summary=None,
            solution_pdf_available=False, exercise_time=lambda exercise: None,
            exercise_type=lambda exercise: 'Test',
        )
    assert legacy_statement in html
    assert 'data-legacy-math' in html
