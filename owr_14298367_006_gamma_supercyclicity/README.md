# Arbitrary-Gamma supercyclicity: verification and priority audit

**Mathematical verdict: the supplied proof gives a valid affirmative answer in the original separable setting. Priority verdict: not clear for a new-result claim.**

This effort checks the candidate associated by the user with [OWR-14298367-006](https://www.unsolvedmath.com/problems/OWR-14298367-006). The exact question was recovered independently in Emma D'Aniello's contribution (joint work with Martina Maiuriello), printed p.1083 of [Oberwolfach Report 19/2024](https://doi.org/10.4171/OWR/2024/19). The catalog page itself was inaccessible during this audit.

For every fixed subset Gamma of C, the bounded-distortion dissipative composition operator and its associated bilateral weighted shift have the same Gamma-supercyclicity. The theorem needs the report's standing assumption of a separable complex Lp space, with 1 <= p < infinity. It does not assert that every such operator is supercyclic.

The scalar criterion was already known. Moreover, the Banach-valued amplification follows by a short specialization and dense-range factor argument from Abbar and Kuznetsova's [2020 preprint, published in 2021](https://arxiv.org/abs/2005.11230). This is a concrete antecedent, not merely a keyword match. We did not locate a publication explicitly spelling out the answer to the 2024 question, so this audit does not assert that the question had already been explicitly answered.

## Read first

- [Verification report](audit/VERIFICATION_REPORT.md): final verdict, scope, corrections, and publication decision.
- [Independent proof](audit/independent-derivation.md): self-contained finite-tail and Baire argument.
- [Priority audit](audit/priority-audit.md) and [independently checked prior-theorem deduction](audit/priority-derivation-independent.md).
- [Candidate proof audit](audit/proof-adversary.md) and [original-source/conjugacy check](audit/source-match.md).
- [Finite exact checks](verification/README.md), with a standard-library Python script. These do not constitute formal verification of the infinite-dimensional theorem.
- [Research log](RESEARCH_LOG.md) and [source inventory](sources/README.md).

Audit date: 22 September 2026, America/Los_Angeles (23 September UTC). This is an AI-assisted research audit, not external peer review or a proof-assistant certificate. No individual was contacted. Author metadata for this research program: Alec Kriebel, [ORCID 0009-0001-9320-500X](https://orcid.org/0009-0001-9320-500X).
