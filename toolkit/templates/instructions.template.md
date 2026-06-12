<!-- Instructions template: freeform guidance for agents and subagents -->
## Instructions

- **Purpose:** Describe the goal the agent should achieve in plain language.
- **Constraints:** Hard constraints (time, files, forbidden actions).
- **Acceptance Criteria:** How the agent knows the job is done.

### Example

Purpose: Implement API endpoint to create an appointment.

Constraints:
- Do not modify files outside `app/`.
- No direct commits without a review.

Acceptance Criteria:
- New POST `/appointments` returns 201 and persists to in-memory store.
- Unit tests and BDD scenario added and passing.
