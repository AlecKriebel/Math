# Edition acceptance and exact scope

## Attribution update: an established failure, directly reconstructed

The underlying Bell-amplification obstruction is established prior work. Brannan–Gao–Junge, arXiv:2007.06138v2, §4.4, explicitly gives GE((I−τ₂)⊗id_M₂)<1 in the paragraph immediately before Proposition 4.21. The statement persists in their published Advances in Mathematics 394 (2022), 108129, p. 51. Combined with the qubit GE(1,∞) theorem of Münch–Wirth–Zhang (2024), it already implies the ordinary same-bound tensorization failure considered here.

The supplied proof is an explicit direct certificate and reconstruction of that consequence. It is not a claim of a new counterexample, a new Bell-state mechanism, historical priority or that the source question remained open before this work. [The full attribution addendum](ATTRIBUTION_ADDENDUM.md) gives the source comparison and conventions. The original proof and mathematical audit are retained unchanged; this later source review qualifies the presentation of their accepted result.

## Accepted counterexample

On 9 October 2026, the independent mathematical audit accepted the exact frozen proof that ordinary logarithmic-mean GE(K,∞) need not preserve the same positive lower bound under tensor products in the source's not necessarily ergodic finite tracial setting. A separate complete reading of the proof and audit accepted that same scope.

For K=1, both the normalized qubit depolarizing semigroup and the identity semigroup on a second qubit satisfy ordinary GE(1,∞). Their tensor product fails it at t=log 2, with the first Bell projection p as observable and density ρ=(2/3)I₄+(4/3)p. The density is positive definite and trace-normalized; the observable is self-adjoint and rank one. The inequality's two sides are 1/(16 log 3) and 1/(32 log(9/5)); the first is strictly larger because 81>75. Scaling the generator and time gives the corresponding failure for each prescribed K>0.

## Exact preserved documents

The complete documents are included without changing a byte:

- COUNTEREXAMPLE.md: 11,028 bytes; SHA-256 ae32045fd98b776aec7cad84914dc7e2f3bc65e8d8540f22f118c7e3b5eb0e39.
- independent_audit/AUDIT.md: 8,077 bytes; SHA-256 43b9ee0c0f1b6f25b0fa23f2b1d5f9fad22a52ecfd6afab59e46852f99979e2a.
- ATTRIBUTION_ADDENDUM.md: 6,570 bytes; SHA-256 063fabacbff0f2f4ad23de1eb1a080a915bb56028e81b30aba77f7af87c2b527.

The independent audit explicitly accepts this proof identity. It checks the normalized generator, the universal factor estimate for arbitrary complex observables, the identity-factor scope, the ambient tensor calculus, the Bell-weight coefficient and both exact violations. Acceptance rests on these written analytic and algebraic arguments, not on a finite test or a checksum.

## Supplementary history and selected manifest

The full audit retains its historical checker discussion and reproduction command. Reproducing that historical run requires supplementary scripts and outputs omitted from this proof-only edition. The command is not an executable procedure supported by the files supplied here. No checker, fixture, standalone result or execution log is distributed, and no omitted computational artifact's hash is published. The selected AUDIT_MANIFEST.json keeps the original acceptance, proof/audit identities, public PDF identities and scope limits while explicitly explaining these metadata exclusions. It is an edition selection, not an unchanged copy of the historical inventory.

## Acceptance boundaries

- The identity factor is nonergodic. The source's class permits it, but this is not a two-ergodic-factor counterexample.
- The example disproves same-bound ordinary-GE tensorization and shows ordinary GE(1,∞) without CGE(1,∞). It does not contradict the complete-GE tensorization theorem.
- Preservation of a fixed nonpositive K and the best weaker tensor bound are not settled.
- The qubit factor estimate is established prior work, credited to Münch–Wirth–Zhang and also fully reproved in the manuscript.
- No novelty, historical-priority, exhaustive-literature or prior-current-open-status claim is made about the counterexample or its ingredients.
- These AI-assisted research audits are not external human peer review, journal acceptance or formal proof-assistant certification.

The result was reached on substantive approach 1 of a maximum of 5. Editorial preparation does not consume another mathematical approach. No queue edit, merge or release is part of this edition.
