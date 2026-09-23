# Verification report

## Verdict and precise scope

The candidate proof is valid for the corrected statement linked by the user: no finite index and no nonempty bounded Euclidean open set attain the Harrell–Stubbe Dirichlet gap bound. All dimensions n≥1, eigenvalue multiplicities, disconnected sets, and arbitrary open-set boundaries are covered. No mathematical gap remains after the exposition specifies the form-defined operator domain and justifies convergence.

The original report's missing square is real, not an OCR error. The current problem entry and the original Harrell–Stubbe discriminant give the intended squared-means expression. Strictness resolves that corrected saturation question, not the neighboring upper-growth-bound or general-mean questions. The literal misprinted expression can attain equality after dilation; see source-match.md.

## Evidence and review routes

| Route | Mechanism and evidence | Status | Remaining gap |
|---|---|---|---|
| Original candidate | Exact spectral remainder; equality makes derivatives H_0^1; zero extension would be a nonzero whole-space L² Helmholtz eigenfunction | Independently checked in proof-audit.md | None identified |
| Independent derivation | Independently rediscovered remainder/extension; then replaced equality step by self-adjointness excluding generalized eigenvectors | Checked in independent-derivation.md and cross-checked in proof-audit.md §6 | None identified |
| Final manuscript | Coordinate support lemma, absolute convergence, all-real-threshold strictness, quadratic endpoints and ground multiplicity | Mathematical pass, final-manuscript-audit.md | Real-valued wording repair incorporated |
| Finite computation | Exact rational identities, certified complete spectra of boxes, degeneracies, scaling, negative controls | 7,016 checks; 1,312 box/J cases passed | Does not prove arbitrary-domain functional analysis |
| Source match | Live reviewed entry, visually inspected report, original discriminant | Corrected saturation scope confirmed | Original report typo disclosed |
| Priority | Primary papers and surveys checked for an existing all-index strictness proof | No direct predecessor located in the scoped audit | Exhaustive priority cannot be certified |

A purely algebraic route that assumes only the non-strict Yang inequalities is blocked: it transfers equality exclusion to an unsupported property of abstract spectral sequences. The Dirichlet operator/domain argument supplies the needed additional information.

## Boundary cases actually checked

At J=1, Q(E₁)=0, so asserting strictness at both endpoints would be wrong. The proof uses strictness at E_{J+1}>E₁. If E_{J+1}=E₁, D=4E₁²/n²>0 directly. Repeated eigenvalues at any threshold contribute zero summands. No ground-state simplicity or positivity is used. Coordinate multiplication preserves Dom(H), not a presumed H² boundary domain; membership in Dom(H²) is used only under the finite-expansion contradiction hypothesis.

## Meaning of “verified”

These are independent AI-assisted mathematical audits and exact finite computations. There is no proof-assistant formalization or external referee certification. The manuscript is the checkable proof. The literature audit records what was read, what was not, and what is classical; the absence of an identified predecessor is not proof of priority.
