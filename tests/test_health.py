from pytest_bdd import scenarios, given, when, then, parsers

scenarios("features/health_check.feature")


@given("the server is running")
def server():
    from fastapi.testclient import TestClient
    from app.main import app
    client = TestClient(app)
    return client


@when("I request the root endpoint")
def request_root(server):
    response = server.get("/")
    server._last_response = response
    return response


@then("the response status should be 200")
def check_status(server):
    assert server._last_response.status_code == 200


@then(parsers.re(r'the response should contain "(?P<key>.+)"'))
def check_body(server, key):
    assert key in server._last_response.json()
