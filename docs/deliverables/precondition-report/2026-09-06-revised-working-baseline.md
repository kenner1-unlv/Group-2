# ClearConsent: Privacy Translator & Data Footprint Map

**Revised Precondition Report - Working Baseline for Design Portfolio I**  
**Course:** CS 472, Fall 2026  
**Original submission date:** September 4, 2026  
**Revision baseline:** September 6, 2026  
**Repository:** `kenner1-unlv/Group-2`  
**Status:** Team review and approval required

> This document is a corrective working baseline prepared in response to the instructor's feedback. The instructor stated that the Precondition Report does not need to be resubmitted. This revision therefore does not replace the submitted report or claim decisions the team has not made. Its purpose is to give the team a coherent, testable starting point for Design Portfolio I.

## 1. Team Information and Agreement

| Name | GitHub ID | Initial workstream |
|---|---|---|
| Ethan Guillem | `ethanvfour` | To be assigned and accepted at a recorded full-team meeting |
| Astrid Jimenez | `Jimenaz29` | To be assigned and accepted at a recorded full-team meeting |
| Jonathan Johnson | `johns216` | To be assigned and accepted at a recorded full-team meeting |
| Russell Kennedy | `Kenner1-unlv` | To be assigned and accepted at a recorded full-team meeting |
| Peter Nguyen | `Peekans` | To be assigned and accepted at a recorded full-team meeting |
| Michael Podolsky | `MikePodo` | To be assigned and accepted at a recorded full-team meeting |
| Sokrat Rostomyan | `rosto-designs` | To be assigned and accepted at a recorded full-team meeting |
| Glen Testamark | `geeklay` | To be assigned and accepted at a recorded full-team meeting |

Email addresses are maintained in the course submission and are not duplicated in the public repository.

The team selected this project through its agreed voting process. Selection establishes the project direction; it does not assign technical authority or project-management responsibility automatically. At the next full-team meeting, the team must approve the committed MVP, assign one accountable owner and at least one reviewer to every workstream, record deadlines, and document each member's acceptance. Until that occurs, this report does not represent any unrecorded assignment as agreed.

All team members remain collectively responsible for the accuracy, consistency, completeness, and professional quality of Design Portfolio I. Individual section ownership does not remove the requirement for whole-document review.

## 2. Project Identity and Type

| Item | Response |
|---|---|
| Project title | ClearConsent: Privacy Translator & Data Footprint Map |
| Project type | Student-designed project without a confirmed external client |
| Product category | Source-grounded privacy-policy analysis and comprehension tool |
| Current stage | Approved to proceed; requirements and architecture decisions remain preliminary |

## 3. Stakeholders and Evaluation Population

No external client or invested stakeholder is currently confirmed. The team's immediate stakeholder population is adults who encounter public online privacy policies and want to understand what a document states without reading it line by line. Secondary evaluators include privacy-conscious technology users and students or professionals familiar with cybersecurity, privacy, or software usability.

The absence of a confirmed client does not make evaluation optional. The team will recruit external participants for a Design Portfolio II study and will record recruitment, consent, tasks, measures, observations, limitations, and resulting product changes. Team members may not serve as the only study participants because they already know the intended system behavior.

## 4. Problem, Users, and Expected Value

### 4.1 Problem statement

Privacy policies and similar online agreements are long, technical, and difficult for many users to interpret under normal time constraints. A user may want to know what types of information a document says are collected, why the information is used, whether the information may be shared, what choices are described, and which passages support those findings. Finding and comparing those statements manually is slow and demands legal or privacy vocabulary that many users do not have.

ClearConsent addresses this comprehension problem by transforming one supported public policy into a structured, plain-language analysis. The application will preserve a strict distinction between the source document, extracted factual findings, and generated explanations. It will not tell a user whether an agreement is safe, legal, compliant, acceptable, or appropriate for that person's circumstances.

### 4.2 Intended users and needs

- Adults who need a faster way to inspect a public privacy policy before using an online service.
- Users who want exact supporting passages rather than an unsupported summary or score.
- Users who want to revisit or delete prior analyses associated with their account.
- Evaluators who need visible ambiguity, limitations, and failure states instead of false certainty.

Users need an understandable workflow, traceable findings, clear boundaries, accessible presentation, predictable error handling, and control over saved records.

### 4.3 Existing alternatives and differentiation

Manual reading remains the most direct alternative, but it is time-consuming and difficult to compare across long documents. Community and automated services such as Terms of Service; Didn't Read provide service-level summaries or ratings. General-purpose AI chat systems can summarize pasted text but may not provide a stable extraction taxonomy, reliable passage-level grounding, account-isolated history, or product-specific evaluation.

ClearConsent's proposed differentiation is narrow and verifiable: category-based findings tied to exact passages, explicit `stated`, `not found`, `ambiguous`, and `unsupported` states, a saved analysis controlled by the authenticated user, and a basic factual footprint summary without personalized legal judgment. Preference-based filtering, company-sharing graphs, grades, and advisory conclusions are not part of the committed MVP.

## 5. Preliminary MVP and Scope

### 5.1 Committed end-to-end MVP

The committed MVP is one reliable vertical workflow:

1. An authenticated user submits an HTTPS URL for a publicly available, machine-readable English-language privacy policy.
2. The server validates the URL and rejects private, local, internal, unsupported, inaccessible, malformed, redirected-out-of-policy, or oversized inputs.
3. The server retrieves the document within defined time, redirect, response-size, and content-type limits; it extracts visible text without executing untrusted page scripts.
4. The analysis service identifies statements in six initial categories: information collected, purpose of use, sharing or recipient categories, retention or deletion, tracking or location, and user choices or rights.
5. Each substantive finding includes an exact supporting passage and source location when available. The system distinguishes what is stated, not found, ambiguous, or unsupported.
6. The user receives plain-language findings and a basic Data Footprint summary showing which categories were found and how they connect. The summary is descriptive, not a risk grade.
7. The user can save the completed analysis, view only their own saved history, reopen it, and delete it and its associated records.
8. If retrieval, parsing, authentication, persistence, or the AI provider fails, the application shows a clear failure state and does not save or display an incomplete analysis as successful.

### 5.2 Secondary capabilities

These capabilities may begin only after the committed workflow passes its acceptance tests:

- Document-specific questions limited to the analyzed source, with cited answers, explicit refusal behavior, and a separate evaluation plan.
- Support for a constrained set of text-based PDF documents after safe parsing and validation are demonstrated.
- Comparison of two saved analyses using the same extraction schema.
- Preference-based sorting or highlighting that changes presentation priority without declaring an agreement safe or advising acceptance or rejection.
- A richer Data Footprint visualization using only evidence already present in the analysis.

### 5.3 Stretch goals

- A graph of companies or recipient categories that may share data with one another.
- Browser-extension or mobile-overlay workflows.
- Broader document formats, languages, or batch analysis.
- Change monitoring across policy versions.
- Advanced visualization, export, or collaboration features.

### 5.4 Explicit exclusions

- Personalized legal advice or conclusions about what a particular user should accept, reject, or do.
- Statements that a company, policy, or agreement is safe, legal, compliant, trustworthy, or high/low risk.
- Letter grades, numerical risk scores, or green/yellow/red verdicts in the committed MVP.
- Automated rights requests, complaints, contract negotiation, or legal-document generation.
- Confidential agreements, private documents, personal correspondence, or documents containing user-supplied personal information.
- Crawling an entire website, bypassing access controls, executing untrusted scripts, or accessing private/internal network resources.
- Unsupported inference about a company's actual conduct when the source only describes policy language.

## 6. Functional Requirements

| ID | Requirement | Preliminary acceptance evidence |
|---|---|---|
| FR-01 | The system shall require an authenticated session before saving or viewing analysis history. | Unauthorized requests are rejected; end-to-end test covers login-to-history workflow. |
| FR-02 | The system shall accept only supported public HTTPS policy URLs for the committed MVP. | Valid fixtures succeed; HTTP, local, private, malformed, and unsupported inputs fail safely. |
| FR-03 | The retrieval service shall enforce content type, byte size, timeout, redirect, and request-count limits. | Boundary and redirect tests pass without contacting forbidden destinations. |
| FR-04 | The parser shall extract readable document text and identify the source title, URL, retrieval time, and content fingerprint. | Parser fixtures produce expected metadata and normalized text. |
| FR-05 | The analysis service shall return findings using the versioned six-category schema. | Schema validation rejects missing, unknown, or malformed fields. |
| FR-06 | Every substantive positive finding shall include an exact supporting passage from the retrieved document. | Citation validator confirms passage membership; unsupported findings cannot be presented as facts. |
| FR-07 | The interface shall label each category as stated, not found, ambiguous, unsupported, or failed. | UI tests cover every state and prevent a failed state from appearing complete. |
| FR-08 | The system shall display a plain-language analysis and a basic descriptive Data Footprint summary. | End-to-end test verifies findings and category relationships from a known fixture. |
| FR-09 | A user shall be able to save, reopen, list, and delete only their own analyses. | Two-account isolation tests and deletion tests pass. |
| FR-10 | Provider, retrieval, parsing, or persistence failure shall produce a clear error and no misleading saved result. | Injected-failure integration tests verify rollback and visible error states. |

## 7. Data, Privacy, Security, and Safety

### 7.1 Data minimization and retention

The application will store only what is required to reproduce and display a saved analysis: user-scoped record identifiers, submitted public URL, source metadata and fingerprint, normalized findings, supporting passages, schema/model version, status, and timestamps. Authentication secrets, session tokens, raw provider credentials, and unnecessary account attributes will not be stored with analysis content.

The provider request will exclude names, email addresses, account identifiers, authentication data, and unrelated application metadata. Only the minimum document text, extraction schema, and document-related instruction or question will be sent. Raw retrieved text will be retained only if the team justifies it for reproducibility and defines a deletion and retention period in Design Portfolio I; otherwise the saved record will retain the source URL, fingerprint, findings, and cited passages.

Users will be warned not to submit confidential material or personal information. Deleting an analysis must delete or disassociate all user-visible and application-owned records covered by the product's retention policy. Logs will avoid document bodies, credentials, session values, and personal identifiers.

### 7.2 Authorization and secrets

Every saved-analysis query and mutation must enforce ownership on the server. Client-side filtering is not an authorization control. Automated tests will create at least two users and prove that neither can read, update, or delete the other's records.

AI, database, deployment, and authentication credentials will remain in server-side environment secrets. No real credential may appear in source code, fixtures, screenshots, issues, pull requests, prompts, logs, or documentation. Secret scanning will run before merge, and the credential-exposure incident is tracked separately in repository issue #40.

### 7.3 Safe document retrieval

The retrieval service is an SSRF boundary and will be treated as a dedicated server-side component. It will:

- allow HTTPS and approved content types only;
- resolve and reject loopback, link-local, private, reserved, and internal addresses before connecting;
- revalidate every redirect destination and limit redirect count;
- limit response bytes, request duration, and total requests;
- avoid forwarding user credentials, cookies, or authorization headers;
- avoid executing retrieved JavaScript;
- return explicit unsupported, inaccessible, timeout, redirect, and oversized-document errors.

The exact numeric limits will be finalized in the architecture decision record and verified by boundary tests before external URL retrieval is enabled outside development.

### 7.4 AI-output safety and product boundary

AI output is untrusted structured data until it passes schema, citation, and policy validation. The system will not infer an answer when the policy is silent. Ambiguous language will be labeled ambiguous and linked to the relevant passage. A finding without valid source support will be labeled unsupported or removed; it will not be displayed as a fact.

The product is an informational document-analysis tool, not a lawyer or compliance assessor. It reports what the selected document states and does not determine whether the stated conduct is lawful or whether the company follows its policy. Interface text, prompts, tests, and evaluation will prohibit individualized accept/reject recommendations and unsupported safety, legality, or compliance conclusions.

### 7.5 Availability, usage, and cost controls

Provider calls will use server-side timeouts, bounded retries, request limits, and usage monitoring. When the AI provider is unavailable, rate-limited, or over the approved budget, the application will show a clear temporary failure and will not create a completed analysis. The team will establish an expense owner, approval process, monthly ceiling, and shutdown threshold before paid shared services are used.

## 8. Technical Approach and Constraints

| Area | Preliminary approach | Decision status |
|---|---|---|
| Application | SvelteKit with TypeScript for the browser UI and server routes/actions | Proposed; validate in issue #39 |
| Styling | Tailwind CSS with responsive and accessible components | Proposed |
| Database | PostgreSQL hosted by Neon with migrations and server-side access | Proposed; connection and ownership spike required |
| Hosting | Cloudflare Workers/Pages deployment using the supported SvelteKit adapter | Proposed; Workers versus Pages must be resolved because Cloudflare currently recommends Workers for new full-stack applications |
| AI provider | Claude behind a server-side provider interface with structured schema validation | Proposed; model, retention, cost, and failure behavior must be confirmed |
| Authentication | Provider not yet selected; server-side session and authorization behavior required | Open decision |
| Testing | Unit, schema/contract, integration, security-boundary, and browser end-to-end tests | Required; exact tools open |
| CI/CD | GitHub Actions for lint, type-check, build, tests, secret scanning, and preview/deployment gate | Required |

SvelteKit and Cloudflare are technically compatible through Cloudflare's supported adapter. Neon provides a serverless JavaScript/TypeScript driver for edge/serverless environments. Compatibility documentation is necessary but not sufficient; the team must perform a small deployment and database-connectivity spike before approving the architecture.

Architecture decisions must define browser/server trust boundaries, ownership of external accounts, local/preview/production environments, schema migrations, backup and recovery, logging, model abstraction, and cost controls. Detailed technical selection remains tracked in issue #39.

## 9. AI Extraction Evaluation

### 9.1 Dataset and reference labels

The first evaluation set will contain 30 supported, publicly available English-language privacy policies sampled across at least five service categories, such as retail, social media, finance, health/wellness, and productivity. No policy used as a prompt-development example may enter the held-out test set.

Two human reviewers will independently label whether each of the six MVP categories is stated and identify the supporting passage or mark the category not found or ambiguous. Reviewers will resolve disagreements and retain the independent labels, resolution notes, final reference label, source URL, retrieval date, and document fingerprint. The team will report category prevalence and inter-reviewer agreement so the final score is interpretable.

### 9.2 Metrics and thresholds

For category identification, the system shall achieve:

- macro-averaged F1 of at least 0.80 across the six categories on the held-out set;
- precision, recall, and F1 reported for every category, even if the threshold is met overall;
- at least 95% citation validity, defined as the cited passage appearing in the analyzed source and supporting the displayed finding under human review;
- zero completed analyses containing an uncited substantive positive finding in the evaluation run.

Results below threshold do not authorize relabeling the test set to match the model. They require prompt/schema revision, model or parsing changes, scope reduction, or an explicitly approved threshold revision supported by evidence.

### 9.3 Reproducibility

The evaluation record will include the dataset version, schema version, model identifier, prompt version, run date, source fingerprints, per-category confusion counts, precision, recall, F1, macro F1, citation-validity result, and known failures. The held-out set and scoring script will be versioned where licensing and document-distribution constraints allow; otherwise the repository will retain stable URLs, hashes, annotations, and a reproducible retrieval process.

## 10. User and Stakeholder Evaluation

User evaluation is required and scheduled for Design Portfolio II. The preliminary plan is a moderated, counterbalanced within-participant study with 12 adults who are not members of the development team. Each participant will answer equivalent comprehension questions for two comparable supported policies: one using the original document alone and one using ClearConsent. Assignment order and policy condition will be counterbalanced to reduce order and document effects.

The study will measure:

- comprehension-question accuracy;
- task completion time;
- successful location of the source passage supporting an answer;
- task completion and observed failure points;
- perceived usability using a short standardized or justified questionnaire;
- qualitative trust calibration, including whether participants understand that the product reports document language rather than legal conclusions.

The preliminary success targets are a mean comprehension improvement of at least 15 percentage points over source-only reading, at least 90% successful passage location for completed system-assisted answers, and no participant interpreting the output as a personalized legal recommendation after the product-boundary explanation. Because the study is small and exploratory, the team will report individual results, descriptive statistics, protocol deviations, and limitations rather than claiming population-level effectiveness.

If recruitment or study design cannot support the comparative 15-point criterion, the team must revise the criterion in Design Portfolio I before data collection and replace it with a feasible usability or comprehension target. It may not simply mark evaluation optional.

## 11. Software Verification and Definition of Done

Every pull request must link to an issue and pass the agreed formatting, linting, type-checking, build, unit, contract/schema, and relevant integration checks before merge. A meaningful implementation is not complete until its tests, documentation, limitations, and AI-use disclosure are reviewed.

The committed MVP release must demonstrate:

1. A browser-level end-to-end test from authenticated URL submission through safe retrieval, parsing, analysis, citation display, save, reopen, and deletion.
2. Fixture-based tests for valid policies and for inaccessible, malformed, unsupported, redirected-out-of-policy, timed-out, and oversized inputs.
3. Network-boundary tests proving that private, local, link-local, reserved, and internal destinations are blocked, including after redirect and DNS resolution.
4. Contract tests proving that malformed AI output, missing citations, unknown categories, and unsupported findings cannot appear as successful factual results.
5. Two-user authorization tests proving cross-user reads, updates, and deletions fail.
6. Injected provider, database, and parser failures that create a clear error and no completed or misleading saved analysis.
7. A reproducible extraction-evaluation run meeting the approved metric thresholds.
8. Accessibility checks for keyboard operation, focus behavior, labels, headings, contrast, and error identification on the core workflow.

No pull request may be merged with a failing required check. Emergency bypass behavior, if the team permits it, must require a documented approval and immediate corrective issue rather than silently weakening the gate.

## 12. Meaningful Work for Eight Members

The project supports eight integrated workstreams. These are responsibilities to assign, not preassigned titles:

| Workstream | Integrated deliverables | Evidence of completion |
|---|---|---|
| Product requirements and traceability | User stories, acceptance criteria, scope control, requirement-to-design-to-test links | Reviewed specification and maintained traceability matrix |
| Retrieval and parsing | Safe URL validation, bounded fetch, content parsing, normalization, metadata | Security-boundary and parser PRs with tests |
| AI extraction and grounding | Versioned schema, provider adapter, prompts, citation validation, ambiguity handling | Contract tests and evaluated extraction pipeline |
| Data and persistence | Schema, migrations, saved history, deletion, retention behavior | Migration and repository-layer PRs with isolation tests |
| Authentication and authorization | Session design, server-side ownership controls, threat cases | Auth integration and two-user isolation evidence |
| Frontend and accessibility | Submission, results, footprint summary, history, error states, accessibility | Focused UI PRs and browser/accessibility tests |
| Verification and CI | Test strategy, fixtures, CI gates, secret scanning, failure injection | Passing pipelines and recorded test evidence |
| Evaluation, documentation, and integration | User study, meeting evidence, diagrams, release QA, portfolio coherence | Approved protocol, actual study evidence, reviewed portfolio and release |

Each workstream requires a primary owner and at least one reviewer. Subteams may execute detailed work, but major decisions, blockers, dependencies, and results must return to the weekly full-team meeting and be recorded. Each member's six meaningful pull requests and six meaningful reviews must represent substantive, issue-linked work; counts do not substitute for integration or quality.

## 13. High-Level Semester Plan

| Phase | Dates | Required outcome |
|---|---|---|
| Corrective baseline and ownership | Sept. 6-11 | Approve MVP tiers; assign all eight members; set weekly meetings and rotating minutes roles; approve blocker and decision process |
| Design Portfolio I | Sept. 7-25 | Complete specification, use cases, architecture and data diagrams, threat/risk analysis, ADRs, traceability, test plan, evaluation plan, schedule, and whole-document QA |
| Core vertical slice | Sept. 14-Oct. 2 | Demonstrate one fixture-based submission-to-cited-result flow with structured output and failure handling |
| Secure persistence and external retrieval | Sept. 28-Oct. 16 | Add safe URL boundary, authentication, authorization isolation, history, and deletion; pass integration/security tests |
| Evaluation readiness and DP II | Oct. 5-25 | Freeze labeled dataset/protocol, run extraction baseline, conduct or begin approved user study, integrate feedback, submit DP II |
| Integration and refinement | Oct. 19-Nov. 13 | Close cross-component gaps; improve quality against metrics; complete accessibility, outage, and cost controls |
| Final verification and delivery | Nov. 9-30 | Release candidate, full regression and evaluation evidence, Design Portfolio III, deployment/runbook, final presentation |

The schedule deliberately overlaps design and implementation while preserving time for integration, security, automated testing, AI-output evaluation, user feedback, and revision. Secondary work may not displace a failing committed-MVP criterion.

## 14. Coordination and Accountability Process

The team will hold at least one full-team meeting each week, with at least half of regular full-team meetings conducted in person. Additional subteam meetings may occur but do not replace the full-team meeting. Unavoidable absences must be communicated in advance and recorded accurately.

Every meeting will have a rotating chair, secretary, and minutes reviewer. The secretary will post minutes within 24 hours; the reviewer will confirm accuracy before the group creates a named version. Minutes will record actual attendance, significant viewpoints and alternatives, decisions and rationale, unresolved items, named assignments and deadlines, prior-task completion, blockers, and escalation. Asynchronous work will be identified as asynchronous; later corrections will be dated and will not be written as though they occurred during the original meeting.

Every task will have one accountable owner, a reviewer, a deadline, acceptance evidence, and an issue. A promise or statement of willingness is not completion evidence. Completion requires a linked artifact, merged pull request, passing test or CI run, approved decision in accurate minutes, or completed evaluation record.

Blockers must be raised in the assigned issue and team channel as soon as known. A blocker that threatens a milestone is placed on the next meeting agenda or triggers an earlier decision meeting. Technical disagreements will be resolved using documented constraints, a time-bounded spike where needed, and a recorded decision. Unresolved schedule, participation, or grading risks will be escalated to the instructor with the factual record.

## 15. Preliminary Success Criteria

| Criterion | Target | Verification method |
|---|---|---|
| End-to-end MVP | Authenticated user completes submit, retrieve, parse, analyze, cite, summarize, save, reopen, and delete workflow | Passing browser E2E test and live demonstration using supported public fixtures |
| Extraction quality | Macro F1 >= 0.80 across six categories on the 30-policy held-out set | Versioned scoring run with per-category precision, recall, F1, and confusion counts |
| Grounding integrity | >= 95% citation validity and zero uncited substantive positive findings in completed evaluation analyses | Automated passage-membership validation plus human citation review |
| Security and authorization | Forbidden network destinations blocked; cross-user read/update/delete attempts all rejected | Automated SSRF boundary suite and two-account integration tests |
| Failure integrity | Invalid input and provider/parser/database failure never create a misleading completed analysis | Injected-failure and rollback tests in CI |
| User evaluation | 12 external participants; mean comprehension improves >= 15 percentage points; >= 90% passage-location success | Counterbalanced DP II study with recorded protocol, results, limitations, and resulting changes |
| Delivery quality | Every merged PR passes required CI and links requirement, issue, code, test, documentation, and AI disclosure | Repository audit and traceability matrix before each portfolio submission |
| Team execution | Weekly full-team meeting, accurate reviewed minutes, named ownership, visible blocker escalation, and substantive PR/review progress | Cumulative minutes, issues, PRs, reviews, CI history, and action register |

## 16. Risks and Initial Responses

| Risk | Impact | Initial response |
|---|---|---|
| Scope exceeds semester capacity | Components exist separately but never become a reliable product | Freeze committed MVP; subordinate secondary/stretch work; demonstrate vertical slice early |
| AI output invents or overstates findings | Users receive misleading privacy claims | Structured schema, exact citations, ambiguity states, held-out evaluation, unsupported-output rejection |
| Unsafe URL retrieval | Server accesses internal systems or consumes unbounded resources | Dedicated SSRF boundary, destination revalidation, strict limits, security tests |
| Cross-user data exposure | Saved analyses become visible to another account | Server-side ownership checks, two-account tests, least-privilege database access |
| Provider outage or cost overrun | Analysis fails or unexpected expenses occur | Provider abstraction, explicit failure state, timeouts/limits, budget approval and shutdown threshold |
| No invested stakeholder | Product evolves without external evidence | Required DP II study and documented recruitment; do not substitute team opinion for user evidence |
| Uneven participation or unclear ownership | Deadlines, integration, and review fail | Named owner/reviewer/deadline/evidence per task; weekly minutes; early escalation using objective records |
| New stack learning | Integration errors and schedule loss | Small deployment/database/auth spikes; documented setup; pair review; choose proven alternatives if evidence fails |
| Document inconsistency | Portfolio contradicts implementation or retains placeholders | Named section owners, independent final reviewer, whole-document checklist, traceability audit |

## 17. Document QA and Approval

Before Design Portfolio I submission, one named document owner will assemble the source and one different named reviewer will check:

- every required section is present and contains substantive content;
- no placeholders, duplicated passages, blank criteria, informal language, or contradictory scope remain;
- MVP, requirements, architecture, risk analysis, evaluation, schedule, and success criteria agree;
- every material claim has a source, decision record, test, or clearly labeled preliminary status;
- individual work is credited from repository and meeting evidence rather than inferred;
- the complete team has an opportunity to review the final version before submission.

The approval record will list the reviewed version, date, reviewer, unresolved exceptions, and submission confirmation. This revised baseline itself remains preliminary until the team approves it in accurate meeting minutes.

## 18. Sources and Active Tracking

- Instructor, *Group 2 Feedback: Precondition Report*, September 2026; preserved in `docs/instructor-feedback/2026-09-06-precondition-report-feedback.pdf`.
- Instructor, *Group 2: Team Coordination and Way Forward*, September 2026; preserved in `docs/instructor-feedback/2026-09-06-coordination-feedback.pdf`.
- Group 2 GitHub issue #38, repository structure, documentation, and meeting process.
- Group 2 GitHub issue #39, application architecture and technology stack.
- Group 2 GitHub issue #40, exposed-token containment and remediation.
- Group 2 GitHub issue #41, instructor-feedback conversion into testable MVP requirements.
- Cloudflare, [SvelteKit deployment guidance](https://developers.cloudflare.com/workers/framework-guides/web-apps/sveltekit/) and [Pages overview](https://developers.cloudflare.com/pages/).
- Neon, [serverless driver documentation](https://neon.com/docs/serverless/serverless-driver).

## Revision Statement

This document turns the professor's examples into a defensible proposed baseline, but it does not erase the team's obligation to decide. Numeric thresholds, platform choices, workstream assignments, and evaluation details remain subject to evidence-based team approval and instructor feedback. Changes must be recorded prospectively in issues, decision records, and accurate meeting minutes.
