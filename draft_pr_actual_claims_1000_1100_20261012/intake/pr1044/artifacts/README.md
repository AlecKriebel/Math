# Ordinary logarithmic-mean gradient estimates do not preserve their bound under tensor products

## Attribution update: an established failure, directly reconstructed

The underlying Bell-amplification obstruction is established prior work. Brannan–Gao–Junge, arXiv:2007.06138v2, §4.4, explicitly gives GE((I−τ₂)⊗id_M₂)<1 in the paragraph immediately before Proposition 4.21. The statement persists in their published Advances in Mathematics 394 (2022), 108129, p. 51. Combined with the qubit GE(1,∞) theorem of Münch–Wirth–Zhang (2024), it already implies the ordinary same-bound tensorization failure considered here.

The supplied proof is an explicit direct certificate and reconstruction of that consequence. It is not a claim of a new counterexample, a new Bell-state mechanism, historical priority or that the source question remained open before this work. [The full attribution addendum](ATTRIBUTION_ADDENDUM.md) gives the source comparison and conventions. The original proof and mathematical audit are retained unchanged; this later source review qualifies the presentation of their accepted result.

## Accepted result and scope

The normalized qubit depolarizing semigroup satisfies ordinary logarithmic-mean GE(1,∞), as does the identity semigroup on a second qubit. Their tensor product fails GE(1,∞). A positive definite rational density and a rational self-adjoint observable witness the failure at the exact time log 2; the strict comparison reduces to 81>75.

This edition addresses problem 30004587 / OWR-4990370-005 in the source's finite tracial, not necessarily ergodic setting. The identity factor is deliberately nonergodic. The example does not answer a separately restricted question requiring both factors to be ergodic, preservation of a fixed nonpositive K, or the optimal weaker tensor bound. Complete-GE tensorization is unaffected. Rescaling yields the same failure for each prescribed positive K.

## Reading order

1. [The complete proof](COUNTEREXAMPLE.md) establishes the first factor estimate for all complex observables, all densities and all times; verifies the full ambient tensor differential calculus; and gives exact positive-time and infinitesimal violations.
2. [The full independent mathematical audit](independent_audit/AUDIT.md) accepts that precise scope. [The selected audit manifest](independent_audit/AUDIT_MANIFEST.json) binds the exact proof and audit and retains public source identities.
3. [The full prior-work attribution addendum](ATTRIBUTION_ADDENDUM.md) records the established Bell-amplification failure and the direct-reconstruction scope. [Edition acceptance](ACCEPTANCE.md) states the accepted claim and its limits. [Provenance](PROVENANCE.md) explains exact preservation and the proof-only boundary. [Public source metadata](SOURCE_PROVENANCE.json) credits the established qubit estimate and records the bounded source review.
4. [Status](STATUS.json) records the scoped disposition; [the manifest](MANIFEST.json) enumerates the edition members and their byte identities.

## Historical reproduction references

The proof and full mathematical audit are preserved byte-for-byte. The audit's references to an executed checker, its saved output and the command in its Reproducibility section describe historical supplementary work. Those scripts and outputs are omitted: that command cannot be run using this edition alone and requires the omitted supplementary files. The selected audit manifest intentionally excludes their filenames, sizes and hashes. The self-contained written proof supplies the mathematical argument; software is not a premise of the accepted result.

The qubit factor estimate is established prior work and is independently reproved here. No claim is made that this counterexample or its ingredients are new, that the construction has historical priority, or that the historical source question remained open before this work. The mathematical/source reviews are AI-assisted research audits, not external human peer review, journal acceptance or formal proof-assistant verification. No QUEUE.md or unrelated repository change is proposed.
