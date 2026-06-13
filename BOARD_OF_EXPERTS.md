# Board of Experts — Repository Structure Review

Purpose
-------
Form a lightweight board of domain experts to review the repository layout, propose a streamlined structure, and approve changes to improve maintainability and clarity.

Suggested experts (roles)
-------------------------
- **Lead FastAPI Architect** — reviews API routing, versioning, and FastAPI idioms.
- **Backend/Domain Model Expert** — reviews domain separation, services, and repositories.
- **DB/Schema Engineer** — reviews persistence layer, migrations, and DB layout.
- **Security / Auth Expert** — validates authentication, password storage, and token usage.
- **Testing & CI Engineer** — ensures test organization, fixtures, and CI compatibility.
- **DevOps / Packaging Specialist** — advises on packaging, env vars, and deployment layout.

Responsibilities
----------------
- Review the current folder structure and the proposed changes in `FOLDER_RESTRUCTURE_PROPOSAL.md`.
- Provide concise feedback (issues or PR comments) within the agreed review window.
- Approve or request changes; approval from at least three distinct roles is required to proceed with structural refactors.

Review Process
--------------
1. Maintainer drafts a proposal and places it in `FOLDER_RESTRUCTURE_PROPOSAL.md`.
2. Board members review and comment over a 3–5 business day period.
3. Address feedback in the draft; when approved, open a focused PR that implements changes incrementally with tests.

Meeting / Communication
-----------------------
- Use GitHub PR review for detailed comments.
- Optionally schedule a 30–45 minute async review meeting if the change is large.

Decision Criteria
-----------------
- Changes must preserve or improve test coverage.
- Backwards-incompatible moves require clear migration steps and deprecation redirects (if applicable).

Next step
---------
1. Maintainer updates `FOLDER_RESTRUCTURE_PROPOSAL.md` with a concrete proposal.
2. Assign reviewers from the roles above.