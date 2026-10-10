# Acceptance report

## Review status of this edition

This is an AI-assisted mathematical exposition accompanied by an independent internal AI mathematical and source audit. These authored documents are unrefereed. Acceptance means the source-credited, theorem-dependent conclusion of that audit, not external human peer review, journal acceptance of this exposition or audit, or formal proof-assistant certification. Bell, Launois, León Sánchez, and Moosa's differential-algebraic existence theorem is imported prior mathematics; no new counterexample or novelty is claimed.

## Accepted outcome

**ACCEPTED: prior negative resolution, with qualified source citation.**

The universal maximal-spectrum local-closedness assertion in 30001214 / OWR-3397-002 is false. For each d≥4, the complex affine Poisson domains constructed by Bell, Launois, León Sánchez, and Moosa have a primitive zero ideal whose maximal-spectrum symplectic core is not locally closed.

The acceptance is for the complete source-credited implication in PROOF_OF_IMPLICATION.md. It is not a novelty claim, an independent reconstruction of the Manin-kernel existence theorem, a machine-checked proof, or a classification of all Poisson algebras satisfying PDME.

## Conditions and caveats preserved

- The essential existence input is BLLSM Theorem 4.1 / Corollary 5.3, not a newly constructed example.
- Rationality is upgraded to primitivity using BLLSM Theorem 3.2, with its proof checked and reconstructed.
- Local closedness of a Poisson-prime point is not confused with local closedness of a maximal-spectrum core. The closure formula and exact bridge are proved.
- No finite-leaf, algebraic-leaf, smoothness, or group-action hypothesis is added.
- The related unrestricted PDME question 30001215 / OWR-3397-003 is reconciled with the same prior-result chain. It does not provide a separate new problem-solving claim.
- The inspected arXiv LWW Theorem 6.7(ii) is overbroad on all prime-spectrum cores, as shown by the source's definitions and C[x] with zero bracket. The accepted argument uses only the supported maximal-spectrum equivalence, reconstructed from Proposition 5.3 and Lemma 6.5. The uninspected journal body is not alleged to share this wording.
- Source PDF byte identities were independently rechecked. Full retrieval does not imply all proofs or external dependencies were audited.

## Acceptance basis

The mathematical obligations and adverse examples are listed in AUDIT.md. Public bibliographic and inspection metadata are in SOURCES.json. The authored proof proves the conversion and all logical steps from the explicitly imported differential-algebraic existence theorem to the original maximal-core counterexample.

Integrity tests are separate from mathematical acceptance. The clean fixture and 13 rejection controls passed under normal Python, -O, and -OO; a final external seal identifies the frozen local inventory. Nothing in a hash or a successful control run substitutes for the mathematical reasoning.
