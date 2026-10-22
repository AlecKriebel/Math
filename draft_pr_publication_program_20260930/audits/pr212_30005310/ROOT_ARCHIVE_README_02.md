# PR212: archived audit findings

This is a research audit record, not a paper or publication clearance. The originally submitted claim was selected for review because its preserved QUEUE status was `claimed_solved`. In the dated accepted status guard, the revised draft has status `already_solved`; under the current program instructions it is left open and untouched.

## Verified scope and outcome

Problem30005310 concerns the threshold scenarios in Roser Homs's report, “Weak maximum likelihood threshold of colored Gaussian graphical models” (joint work with Olga Kuznetsova), in Oberwolfach Reports55/2022, printed pages3146–3149, DOI[10.4171/OWR/2022/55](https://doi.org/10.4171/OWR/2022/55).

The numerical assertions and the bare Boolean alternative are distinct. The independently checked constructions contradict the numerical threshold asserted in scenario B. They satisfy its intersection condition; they do not disprove the Boolean assertion that either condition A or condition B holds. The latter question remains unresolved by this audit.

For the singleton-colored graph K4,4, the relevant elimination ideals satisfy I3≠0 and I4=0, whereas WMLT=2 and MLT=4. A tied-diagonal variant has the same nonzero/zero elimination-ideal pattern and weak threshold; independent audit work also proves its MLT=4. For the revised draft's four-cycle with one vertex color and distinct edge colors, I1≠0 and I2=0, whereas WMLT=MLT=1. The Gaussian sample convention is known mean and n independent data columns; an unknown-mean convention requires its own rank adjustment.

Root reproduced the two submitted188-check runs and the inherited1808-check run in separate writable sandboxes, and independently reproduced both new mathematical audit families. Exact proofs and certificates are retained alongside the reports. Counts refer to those particular runs, not to independent proof of every statement by counting tests.

## Prior coverage and chronology

The singleton K4,4 numerical counterexample follows from earlier primary results: the bipartite weak-threshold argument of Gross and Sullivant, and the generic-completion-rank and maximum-likelihood-threshold results of Blekherman and Sinn. The precise same-author result for the colored four-cycle is in Homs, Kuznetsova and Stolz, arXiv2609.02382v1, Proposition3.26 together with Proposition3.9. These findings support prior coverage of the literal numerical conclusion.

The arXiv record's2September2026 timestamp is a submission timestamp, not a certified exact first-public-access or announcement time. A25July2025 IMSI talk and its slides corroborate an earlier announcement of the even-cycle threshold result, with the precise hypotheses taken from the paper. No worldwide firstness, proof independence, exact first-public instant or previously published explicit erratum is established. The unchanged submitted text's stronger chronology wording is not adopted.

Primary references:
- [Gross–Sullivant, arXiv1404.6989v3](https://arxiv.org/abs/1404.6989v3), Section5.
- [Blekherman–Sinn, arXiv1703.07849v2](https://arxiv.org/abs/1703.07849v2), Theorems2.1 and2.7.
- [Homs–Kuznetsova–Stolz, arXiv2609.02382v1](https://arxiv.org/abs/2609.02382v1), Propositions3.9 and3.26.
- [Roser Homs's IMSI talk](https://www.imsi.institute/videos/maximum-likelihood-thresholds-for-colored-gaussian-graphical-models/).

## Evidence and administrative boundary

The positive input snapshot preserves all35 current submitted files, including exact copies of all20 original submitted files. Treat their mathematical, novelty and publication statements as submitted claims; Root's qualified conclusions are in the accepted audit records. Scripts that write beside their own source must be copied to a writable sandbox before replay.

The authored mathematical reports, derivations, exact verification programs, actual execution records, priority reading scopes, custody summaries and Root acceptance records are archived as a finite selection. Private provider responses, private full-text PDFs and temporary rendering/replay files are excluded. Public metadata identifies private retained custody material but does not constitute a completely portable offline replay of those private responses.

The administrative disposition preserves the original eligibility and audit evidence. It adds no completed eligible workflow or publication: the baseline remains53 completed and37 published or adopted, with last completed PR211. It authorizes no PR212 paper, DOI, tracker row, merge, close, comment or branch/QUEUE alteration. A separate actual administrative checkpoint is required before numeric intake can advance; this README supplies no such authority.

AI tools were used extensively for the audit, independent adversarial checks, computations and drafting. These records have not undergone conventional human peer review or refereeing.
