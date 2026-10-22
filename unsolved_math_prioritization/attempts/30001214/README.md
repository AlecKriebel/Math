# Symplectic cores: a credited prior negative resolution

Problem 30001214 / OWR-3397-002. Publication edition, 10 October 2026.

Project author: Alec Kriebel, [ORCID 0009-0001-9320-500X](https://orcid.org/0009-0001-9320-500X).

For every integer d >= 4, there is a complex affine integral Poisson algebra A of Krull dimension d and a maximal ideal m for which the symplectic core C(m) = {n in Max A : P(n) = P(m)} is not locally closed in the Zariski topology of Max A. This refutes the unrestricted local-closedness assertion in Ken A. Brown's 2009 Oberwolfach question.

The existence construction is prior work of Jason Bell, Stéphane Launois, Omar León Sánchez and Rahim Moosa, [Poisson algebras via model theory and differential-algebraic geometry](https://doi.org/10.4171/JEMS/712), J. Eur. Math. Soc. 19 (2017), 2019–2049. Theorem 4.1 is imported. The complete authored implication reconstructs its Poisson conversion, the rational-to-primitive argument, density of maximal-spectrum cores and the precise local-closedness bridge. No new counterexample or novelty is claimed.

## Read the result

- [Complete implication proof](PROOF_OF_IMPLICATION.md): all mathematical steps and explicit source dependencies.
- [Mathematical and source audit](AUDIT.md): substantive obligations, adverse examples, source qualification and inspection limits.
- [Acceptance](ACCEPTANCE.md) and [machine-readable acceptance](ACCEPTANCE.json): exact accepted scope and exclusions.
- [Source metadata](SOURCES.json): public citations, PDF hashes and sizes, retrieval matches and inspection history.
- [Verification summary](VERIFICATION_SUMMARY.md): what byte authentication establishes and what remains an imported theorem.
- [Manifest](MANIFEST.json): exact public membership and hashes of the other seven files.

## Critical source qualification

The inspected LWW mathematical body is arXiv:1908.06542v2. Its Theorem 6.7(ii) claims local closedness for every prime-spectrum core. With the zero bracket on C[x], PDME holds and all maximal-spectrum cores are closed singletons, but the generic prime-spectrum core {0} is not locally closed. The all-prime clause is therefore too broad as printed in that inspected version.

The accepted route uses the supported maximal-spectrum equivalence through LWW Proposition 5.3 and Lemma 6.5, reconstructed directly in the proof. It does not use the overbroad clause. The LWW journal body was not inspected, and the manuscript issue is not attributed to it or to an official erratum.

The adjacent PDME question 30001215 / OWR-3397-003 is mathematically reconciled by the same equivalence. It is not a separate new result or a classification of all positive subclasses. No finite-leaf, algebraic-leaf, smoothness or group-action assumption is added to the original question.

## Review and publication scope

This exposition and independent internal AI audit are AI-assisted and unrefereed. Acceptance is not external human peer review, journal acceptance of these authored documents or formal proof-assistant certification. The Manin-kernel existence theorem is not independently reproved, and no explicit defining equations for the counterexample are supplied.

Only authored mathematical prose, audit, acceptance and public citation/verification metadata are distributed. Source PDFs, extracted source bodies, datasets, programs and raw outputs are excluded. Preparing this edition authenticates the accepted documents and recorded metadata without adding a new source-inspection claim.
