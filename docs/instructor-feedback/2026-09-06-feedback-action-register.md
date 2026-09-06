# Instructor feedback action register — September 6, 2026

This directory preserves the instructor's feedback as received and converts it into traceable work. The PDFs are source artifacts; this register is the team's working interpretation. If this register conflicts with the PDFs, the PDFs control.

## Source artifacts

- [Coordination feedback](./2026-09-06-coordination-feedback.pdf)
- [Precondition-report feedback](./2026-09-06-precondition-report-feedback.pdf)

## Operating rules

- Do not edit or replace the source PDFs. Add a new dated artifact if further feedback arrives.
- Every action below requires a named owner, deadline, and verifiable completion evidence.
- Meeting minutes must record what actually occurred. Later corrections must be dated rather than backdated.
- A promise or expression of willingness is not completion evidence.
- No item is complete until its evidence is linked from the relevant issue or pull request.

## Action register

| ID | Instructor feedback / required result | Tracking | Owner | Deadline | Completion evidence | Status |
|---|---|---|---|---|---|---|
| F-01 | Separate committed MVP, secondary features, and stretch features. Define the smallest demonstrable end-to-end workflow. | #41 | Unassigned — decide at next full-team meeting | Next full-team meeting | Approved scope table, meeting decision, and updated requirements | Open |
| F-02 | Define the supported public-agreement input, extracted categories, source-linked findings, saved analysis, and basic footprint summary. | #41 | Unassigned — decide at next full-team meeting | Design Portfolio I planning | Requirements and acceptance criteria linked to design and tests | Open |
| F-03 | Include chat only if its need, grounding method, and evaluation are specified. | #41 | Unassigned — decide at next full-team meeting | Before MVP scope approval | Written include/defer decision with rationale | Open |
| F-04 | Complete Data, Privacy, Security, and Safety requirements. | #39 and #41 | Unassigned — assign security/privacy owner and reviewer | Design Portfolio I | Threat/risk section, controls, and testable requirements | Open |
| F-05 | Restrict inputs to supported public machine-readable documents; warn against confidential information. | #41 | Unassigned | Design Portfolio I | Input policy, UI warning, validation tests | Open |
| F-06 | Minimize LLM payloads and stored data; provide deletion; enforce user isolation; keep secrets server-side. | #39 and #41 | Unassigned | Architecture approval | ADR/design boundaries plus authorization and deletion tests | Open |
| F-07 | Fetch URLs safely by blocking private, local, and internal destinations and applying request limits. | #39 and #41 | Unassigned | Architecture approval | URL policy, implementation issue, and SSRF/request-limit tests | Open |
| F-08 | Label ambiguous findings and define provider outage, rate-limit, and cost behavior. | #39 and #41 | Unassigned | Design Portfolio I | Failure-state requirements and tests | Open |
| F-09 | Define a reproducible extraction evaluation dataset, labels, metric, and threshold (feedback suggests macro F1 at or above 0.80 as an example). | #41 | Unassigned — assign evaluation owner | Design Portfolio I | Versioned dataset protocol, metric definition, threshold, and baseline result | Open |
| F-10 | Make stakeholder/user evaluation required rather than optional and define the Design Portfolio II study. | #41 | Unassigned — assign evaluation owner | Design Portfolio I | Recruitment/evaluation plan, protocol, measures, and schedule | Open |
| F-11 | Define measurable CI acceptance criteria for the core workflow, invalid documents, authorization isolation, and provider failure. | #39 and #41 | Unassigned — assign CI/test owner | Before application scaffolding merges | CI plan and linked automated tests | Open |
| F-12 | Correct duplicate/placeholder/blank/informal report content and assign final document QA. | #38 and #41 | Unassigned — assign document owner and reviewer | Before next report submission | Reviewed report revision and QA checklist | Open |
| F-13 | Use one cumulative minutes document and record actual attendance, viewpoints, decisions, owners, deadlines, and unresolved issues. Date later corrections. | #38 | Unassigned — confirm rotating secretary/reviewer | Starting next meeting | Completed minutes entry with named roles and review record | Open |
| F-14 | Hold one full-team meeting weekly, at least half in person, and record notified absences. | #38 | Unassigned — assign event tracker | Next full-team meeting | Recurring schedule and actual attendance records | Open |
| F-15 | At the next meeting: approve MVP, assign work to all eight members, schedule meetings, define subteams/reporting, rotate meeting roles, define blocker/disagreement handling, and assign final DP I QA. | #38 and #41 | Entire team; named chair required | Next full-team meeting | Agenda, actual minutes, decisions, named owners, and deadlines | Open |

## Closure standard

An action may move to **Done** only when the tracking issue links objective evidence: a merged artifact, an approved decision recorded in actual meeting minutes, a passing test/CI run, or a completed evaluation record. Verbal commitments alone do not close an action.
