Feature: Health check
  Scenario: Root returns OK
    Given the server is running
    When I request the root endpoint
    Then the response status should be 200
    And the response should contain "status"
