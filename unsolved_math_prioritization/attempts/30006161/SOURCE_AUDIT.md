# Source, history and scope audit

## Original statement and topology

The assigned [UnsolvedMath page](https://www.unsolvedmath.com/problems/30006161) was attempted first but was not retrievable. The full pinned corpus record is preserved here; corpus revision `37e53eabe540fb458758e198be61634bd02ee008`. There is no separate research_results entry at this exact problem number; the dated imported literature review is part of source_record.json.

The complete [official Oberwolfach Report 2/2025](https://ems.press/content/serial-article-files/51347) was retrieved and its entire Vaccaro contribution, printed pp. 89–92, read. The exact Question 3 on p. 90 asks for generic chains on the sphere and real projective plane. The report defines a chain as a maximal inclusion-ordered family of connected compact subsets, with the natural compact hyperspace topology; genericity means a comeagre orbit under the full homeomorphism group. The paper underlying the report makes the double-Vietoris topology and nonempty continuum convention precise. A rendered image confirmed the question and its exclusions.

Neither arbitrary maximal chains of possibly disconnected sets, nor dense orbits, nor the identity component alone, nor measurable chaining is substituted for this target. The adjacent assigned measure-preserving problem 30006170 is a separate contribution to the same report; the shared word “chain” is not a duplicate gate.

## Prior-attempt and duplicate gates

The fresh sparse main checkout is based on `c6975ca76f9f667f1250ba403d0e6da2aafe14d0`. Its queue row is rank 177, queued 0/5. The state file is empty; history and related_target_groups have no entry for 30006161. No exact-ID branch, all-state PR, target-named tracked folder or target-named commit was found before this attempt. The all-state PR search was `30006161 OR "Generic Maximal Chains"` and returned no match.

A full pinned-corpus search for generic or maximal chains found only unrelated combinatorial, computability and triangulation questions besides this target. No prior Alec/campaign proof attempt was located. The pinned source's August 2026 open-status triage is preserved as dated evidence, not a new proof.

## Primary theorem dependencies

1. [Gutman, Minimal actions of homeomorphism groups, Fund. Math. 198 (2008),191–215](https://doi.org/10.4064/fm198-3-1). The complete published PDF was recovered directly from the publisher, in addition to an author-hosted manuscript. Theorem 5.3, pp.198–199, proves density of ray-induced chains for strongly arcwise-inseparable Peano continua. Lemma A.1,p.211 supplies this hypothesis for closed surfaces. Theorem 6.5,pp.201–202, proves minimality when the group is locally transitive. The exact approximation and minimality proofs, and the surface specialization in Section 11, were read. In this source M(X) denotes the connected-chain space; its larger Phi(X) must not be substituted. The partial artifact uses only the connected version.
2. [Basso–Codenotti–Vaccaro, arXiv:2403.08667v3](https://arxiv.org/abs/2403.08667v3), revised 2 February 2025. The full accepted manuscript was retrieved. Definitions are in Section 2.1; Rosendal's criterion is Theorem 5.6; the one-direction combinatorial implication is Theorem 5.9; the exact circular-cover definition and surface exclusion are Section 6.5 and Proposition 6.13; the minimality and turbulent-point theorem is 7.7. Its definition of generic turbulence also requires absence of a comeagre orbit, so Theorem 7.7 alone does not decide the exceptional cases. The relevant full sections were read.
3. The BCV publication is corroborated by both [Basso's author page](https://gianlucabasso.com/) and [Vaccaro's author bibliography](https://sites.google.com/view/avaccaro/research): Duke Mathematical Journal 174 (2025),3135–3196, [DOI 10.1215/00127094-2025-0010](https://doi.org/10.1215/00127094-2025-0010). The proof audit uses the full accepted manuscript, not a purported line-by-line comparison with the inaccessible final journal PDF.
4. [Gutman–Tsankov–Zucker, arXiv:1910.12220](https://arxiv.org/abs/1910.12220), the earlier primary paper cited by the report, was retrieved in full. Its Question 1.3 asks the sphere orbit question; Theorem 1.2 has dimension at least three. Its Section 2 already recalls ray density and minimality in dimension at least two. The difference between a nonmetrizable universal minimal flow and the absence of a comeagre orbit is explicit there and is preserved.

Bounded current searches for the exact exceptional-surface questions and relevant author publications did not locate a later resolution. The 2025 work on generalized Wazewski dendrites concerns a different family and does not provide a theorem for these surfaces. This is a bounded search, not a claim of exhaustive historical coverage.

## What is and is not established

The Baire-category proposition is a direct consequence of credited ray density plus a closed incidence-witness argument. The group-theoretic lemma is the standard nerve/partition-of-unity surjectivity argument, consistent with BCV's prior unicoherence proof. Neither is advertised as a new theorem of priority.

The methods stop at an exact gap: they do not determine whether the residual thin-chain set contains one comeagre orbit. The required local-amalgamation quantifier ranges over every smaller open set, and is not discharged by excluding one model orbit or one finite graph configuration. Original status remains unsolved, two approaches used.

All 3,447 exact finite diagnostics are explicitly supporting tests. The written proofs and imported primary theorems carry the infinite-dimensional topology. The source PDFs and renders are retained in the local source cache; links and SHA256 values are recorded in source_manifest.json. No external communication, release or shared queue edit was performed. Actual selected model: gpt-6-astra, xhigh.
