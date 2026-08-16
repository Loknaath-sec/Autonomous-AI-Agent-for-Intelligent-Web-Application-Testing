from fastapi.testclient import TestClient

from app.main import app
from app.llm.schemas import PlannerPlan

client = TestClient(app)


class MockLLM:
    def generate(self, prompt, response_model=None, **kwargs):
        return PlannerPlan(
            goal='Test the login flow',
            tasks=[{
                'id': 1,
                'description': 'Open the login page',
                'type': 'functional',
                'expected_result': 'Login page loads',
                'dependencies': [],
                'risk_level': 'medium',
            }],
        )


def test_health_endpoint():
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json()['status'] == 'healthy'


def test_auth_register():
    response = client.post('/api/auth/register', json={
        'email': f'user-{__import__("uuid").uuid4()}@example.com',
        'username': f'demo-user-{__import__("uuid").uuid4()}',
        'password': 'secret123',
    })
    assert response.status_code == 201


def test_project_list():
    response = client.get('/api/projects')
    assert response.status_code == 200


def test_planner_agent_plan_generation():
    from app.agents.planner.planner_agent import PlannerAgent

    agent = PlannerAgent(llm_provider=MockLLM())
    plan = agent.create_plan('Test the login flow', 'http://localhost:8000')
    assert plan.goal
    assert len(plan.tasks) >= 1


def test_html_report_generation_for_ui():
    response = client.post('/api/reports/generate', json={
        'url': 'https://www.amazon.in/',
        'instruction': 'Test the login process using invalid credentials and verify the error message appears.',
    })
    assert response.status_code == 200
    payload = response.json()
    assert payload['status'] == 'success'
    assert payload['report_html']
    assert 'Autonomous AI Agent' in payload['report_html']
    assert 'login' in payload['report_html'].lower()
