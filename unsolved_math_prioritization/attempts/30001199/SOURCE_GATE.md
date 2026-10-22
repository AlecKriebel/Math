# Exact source gate: 30001199 / OWR-3394-009

2026-10-02. Rank344. Initial substantive author count0/5; no prior attempt found. This gate does not treat the imported title's word “general” as permission to change the source model.

The requested unsolvedmath page was attempted and failed. The complete pinned record was read from revision37e53eabe540fb458758e198be61634bd02ee008; no exact ID/report-code research-results key exists. The dated triage embedded in the record was read. It is not a proof or reliable current-status certificate.

## Primary problem and definitions

The complete OWR contribution by Arjan van der Schaft, jointly with Florian Kerber and Harsh Vinjamoor, spans printed pp.655–658 of *Control Theory: On the Way to New Application Fields*, OWR11/2009. The complete88-page report was downloaded from the publisher; pp.656–658 were rendered and visually checked. Publisher landing page https://ems.press/journals/owr/articles/3394 ; PDF https://ems.press/content/serial-article-files/46211 . Published December23,2009, DOI10.4171/OWR/2009/11.

Section2 restricts to finite-dimensional linear continuous-time systems xdot=A x+B u+G d, y=C x. The auxiliary d are freely varying disturbances. Simulation is the one-sided version of the stated linear-subspace bisimulation, with full projection onto the simulated source state space. Section4 explicitly considers feedback u1=−y2+e1, u2=y1+e2, then the closed case e1=e2=0. It asks if the two full-simulation premises P1||Q2≼Q1||Q2 and Q1||P2≼Q1||Q2 imply P1||P2≼Q1||Q2 beyond the deterministic case. In context, the proposed extension allows disturbance inputs in this linear model. A finite labeled-transition-system example using a different composition would not settle it.

The cited2009 conference precursor was downloaded completely: Kerber–van der Schaft, *Assume-guarantee reasoning for linear dynamical systems*, https://www.math.rug.nl/~arjan/DownloadPublicaties/ecc_draft.pdf . Its Definitions1–2 and Proposition6 provide the source's simulation convention and deterministic claim. Its conclusion leaves nondeterministic systems for later work.

## Later literature and outstanding dependency audit

Kerber–van der Schaft, *Compositional analysis for linear systems*, Systems & Control Letters59(10)(2010),645–653, DOI10.1016/j.sysconle.2010.08.002, Theorem4 explicitly states the circular rule for general finite-dimensional LTI systems with disturbances. Its model uses positive feedback and separate performance outputs; the source's negative feedback can be matched by changing the first-role B matrices' signs and duplicating C as the performance map H. The full indexed primary text, including Lemmas1–3 and AppendicesA–D, was read. Direct institutional binary endpoints returned403 and web PDF screenshots failed; no visual verification of this2010 PDF is claimed. Primary indexed PDF https://pure.rug.nl/ws/portalfiles/portal/2629447/2010SystContLettKerber.pdf ; institutional metadata https://research.rug.nl/en/publications/compositional-analysis-for-linear-systems/ .

The displayed Lemma1 enlargement, equation(22), has a narrow countercheck recorded in DEPENDENCY_CHECK.md: instantaneous output-kernel states of an observable double integrator are not invariant. An independent check agrees under the indexed formula. This challenges the displayed auxiliary proof, not Theorem4 itself. A literature-resolution promotion is therefore withheld while the exact main rule is examined. No external error allegation or author contact has been made. A corrected proof or main-rule counterexample would be substantive author work, counted from turn1.

The record's citation10.1145/509705.509707 concerns a different computer-science setting; its DOI endpoint could not be retrieved. It is not used as evidence about this LTI closed-feedback rule. Later contract-framework papers use different assumption semantics and are not substituted for the exact rule.

## All-ref and related-attempt checks

Live exact-ID PR, branch, default-code and target-path commit-history checks found no prior proof attempt; code matches only review assignment metadata. Related assume-guarantee PR and3394 branch checks found no overlapping attempt. Available all-ref history has no ID/title/Kerber/compositional-analysis proof commit. Catalog gives eligible/no holds/queued0/5 and review hash ba1fd6b0425276595e6a1c16c874ed22a0b51831ff2c7d0840423c44ec4f27d7. The original nearby pendulum target OWR-3394-010 has a separate credited source-resolution audit in the repository; it neither proves nor overlaps this conjecture. Adjacent imported records30001198–30001201 were read.

Repository policies, dedicated-folder rule, five-turn maximum, independent review, no outside contact and no routine release remain applicable. Primary PDFs, screenshots, extracted text and raw imports are local-only. Source-gate completion estimate10% toward a verified disposition, subjective; no solved conclusion at the gate.
