# Source and prior-work audit

Checked 2026-09-30. The outcome is a partial obstruction to the source's suggested synchronous coupling, with no claim of a complete characterization or historical novelty.

## Original scope

**Hermann Thorisson, Some Open Probability Problems**, Section 3, preprint pp.3–4. [Primary preprint](https://cms.dm.uba.ar/depto/public/Some%20Open%20Problems-preprint.pdf). The complete relevant section, including Theorem3.1, Corollary3.1, Problems3.1–3.3 and the Skorohod discussion, was read through indexed text from the primary PDF. The direct HTTP/HTTPS PDF endpoints returned502, and a PDF screenshot could not be recovered. A complete binary copy was not obtained; this limitation is retained rather than presenting the pinned transcription as a newly downloaded original.

The section specifies one-sided paths and deterministic shifts. Problem3.3 asks for a two-process characterization and then offers synchronous metric convergence as an example. It does not explicitly label the convergence mode or assume an ergodic limit. Random-time distributional coupling is a different preceding notion. The binary construction addresses the example in probability and almost surely; it leaves the broad question unresolved.

The primary publisher and the author's institutional record identify the published version as **Open problems in renewal, coupling and Palm theory**, Queueing Systems68,313–319(2011), [DOI10.1007/s11134-011-9241-2](https://link.springer.com/article/10.1007/s11134-011-9241-2). The publisher abstract and metadata were accessible, but the full published text was subscription content. No claim of a line-by-line published/preprint comparison is made.

## Relevant coupling literature

**Thorisson, On Coupling and Convergence in Density and in Distribution**, preprint listed by the IHP2008 program. [Full author preprint hosted by CNRS](https://interacting.math.cnrs.fr/HT_Skorohod-Dudley%204.pdf), [program listing](https://interacting.math.cnrs.fr/papers-written_ihp2008.html). The complete six-page PDF was retrieved and read. Its Theorem1 and Corollary1 construct couplings of a sequence of process copies, with agreement on growing windows under the stated density/finite-window hypotheses. The theorem does not identify those copies as shifts of one original path. Its Skorohod–Dudley statement is likewise a sequence-of-copies result. These established constructions are credited and are not a solution to the two-process consistency requirement.

**Søren Asmussen, On Coupling and Weak Convergence to Stationarity**, Annals of Applied Probability2(3),739–751(1992), [DOI10.1214/aoap/1177005657](https://doi.org/10.1214/aoap/1177005657), [author institution metadata](https://pure.au.dk/portal/en/publications/on-coupling-and-weak-convergence-to-stationarity). Metadata and the correct DOI were checked. Direct publisher PDF retrieval returned an access-challenge HTML response, so this paper was not read in full and no theorem from it is used in the proof. It remains a relevant prior-art lead, not evidence of novelty.

Current primary-source searches for the exact problem, weak shift convergence and asymptotic coupling did not identify a verified full resolution in this bounded audit. That absence is not proof that the question is still open. The supplied upstream report is earlier literature triage; its open-status label is not treated as a mathematical certificate. No outside author was contacted.

## Prior campaign attempt and distinct target

Repository/history/branch/PR checks found no earlier campaign attempt on9900007. The existing9900005 entry concerns the distinct setwise-versus-total-variation question3.1. The construction here does not satisfy setwise convergence, as the invariant event of eventually constant paths shows. It therefore does not duplicate or revise that result. A two-sided symbolic state can itself be used as the state space of a one-sided process; notation alone does not invalidate an earlier construction.

## Provenance and mathematical inputs

The pinned source record and upstream report are preserved in source_record.json. The new argument uses an explicit inhomogeneous binary chain, telescoping products, conditional-expectation approximation by finite histories, and compact product-space weak convergence. Those are standard tools. The exact finite checker supports the identities but not the infinite quantifiers. No novelty claim follows from the absence of a located identical example.
