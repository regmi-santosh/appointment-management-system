from behave import given, when, then
from fastapi.testclient import TestClient
from app.main import app


@given("the server is running")
def step_server_running(context):
    context.client = TestClient(app)


@when("I request the root endpoint")
def step_request_root(context):
    context.response = context.client.get("/")


@then("the response status should be 200")
def step_check_status(context):
    assert context.response.status_code == 200


@then('the response should contain "{key}"')
def step_check_body(context, key):
    assert key in context.response.json()
