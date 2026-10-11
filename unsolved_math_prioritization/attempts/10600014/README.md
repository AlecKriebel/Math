# Symmetric Brauer projectors: full proof and source audit

Problem 10600014 / AMR-105-0014, original Virtual Knot Theory problem 14.

Decision: ACCEPTED_PROJECTOR_COMPONENT. The full original problem remains PARTIAL because the requested useful recoupling theory is not supplied.

For n >= 1, the unique nonzero idempotent simultaneously annihilated on both sides by every e_i and fixed on both sides by every v_i is the symmetric orbit-sum element F_n in PROOF.md. The complete general proof includes diagram factorization, augmentation-based uniqueness and idempotence, the four-case contraction count, the three-dimensional corner derivation of the recurrence, and explicit specialization maps. Its coefficients lie in Q(d), and the generic statement is over C(d).

For fixed n, existence at d_0 in C holds exactly outside P_n={-2n+2l+2:1<=l<=floor(n/2)}. The sufficient exclusions E_n={-2j:0<=j<=n-2} for the entire literal recurrence tower are different. At E_n minus P_n the direct fixed-rank proof applies; no undefined intermediate tower element is evaluated. Nonexistence at P_n concerns only the simultaneous target conditions. All statements concern the free pairing algebra, not a possibly nonfaithful tensor quotient.

## Contents

- [PROOF.md](PROOF.md): complete all-rank authored proof, original mathematical text retained verbatim
- [AUDIT.md](AUDIT.md): complete source/parameter audit, including the two smallest Section 6 counterchecks for the inspected v1
- [ACCEPTANCE.md](ACCEPTANCE.md) and [ACCEPTANCE.json](ACCEPTANCE.json): precise accepted component and residual problem
- [SOURCES.json](SOURCES.json): public citations, source identities, and historical text/visual inspection scope
- [VERIFICATION.json](VERIFICATION.json): byte authentication and summarized historical exact checks
- [MANIFEST.json](MANIFEST.json): exact eight-file inventory with hashes of the other seven files

The inspected arXiv:2103.11355v1 Lemma 6.1 fails under its stated unnormalized closure trace already at n=2,d=3 (actual 5, printed 15). Its Proposition 6.2 universal reduced-word assertion fails for v_2 v_1 v_2 in rank 3. Both full counterarguments remain in AUDIT.md. These exclusions do not negate the independently proved projector component and make no claim about uninspected journal text.

This AI-assisted, unrefereed edition records an internal AI mathematical audit. Acceptance is limited to the expressly stated projector component and parameter criterion; it is not external human peer review or formal proof-assistant certification. The full original recoupling problem remains PARTIAL. This is a written proof/correction/audit edition, not a computational reproduction package. Source inspection and exact mathematical checks described below occurred in the preceding audit on 11 October 2026. Editorial preparation authenticates the retained records without claiming a fresh scholarly-source inspection or a new mathematical-program run.

This edition contains authored proof, audit, acceptance and public verification metadata only. It distributes no checker programs, raw outputs, datasets, copied source PDFs, extracts, page images or private coordination. No source-author code was executed. No novelty, blanket manuscript acceptance, full recoupling solution, all-primitive-idempotent classification or positive-characteristic extension is claimed.
