# An explicit Steinberg quotient obstruction for rational SL₂ modules

Problem 30006265, reference OWR-14299283-001. Prepared 11 October 2026 UTC.

Over an algebraically closed field of characteristic 3, the module Sym²(Sym² E) is the indecomposable tilting module T(4) for SL₂. Its Steinberg quotient t(2) is z² + z⁻². This is not the character of any finite-dimensional rational SL₂-module. The complete proof includes self-duality, both filtrations, an elementary indecomposability argument, formal character division, and the exact-torus-weight Lie-algebra contradiction.

This is an AI-assisted proof exposition and mathematical audit. It verifies a standard rank-one example, with no novelty or first-counterexample claim. It is not external human peer review or formal proof-assistant certification.

## Read the packet

- [Complete explicit proof](EXPLICIT_PROOF.md)
- [Mathematical audit and source-level interpretation](AUDIT.md)
- [Acceptance scope and exact artifact binding](ACCEPTANCE.json)
- [Primary-source metadata and inspection locations](SOURCE_PINS.json)
- [Twenty-two named check results](CHECK_RESULTS.json)
- [Aggregate verification summary](CHECK_SUMMARY.json)
- [Public file manifest](MANIFEST.json)

## Exact scope

The quotient remains a torus character, a virtual SL₂-character and a candidate for geometric interpretation. Indeed t(2) = ch St − ch k in the Grothendieck group. The obstruction applies to ordinary finite-dimensional rational G-modules. Type A₁ in characteristic 3 is good characteristic.

The [OWR contribution](https://ems.press/content/serial-article-files/51851) asks Question 1 on printed p. 1275 and announces a geometric answer on p. 1276, later in the same contribution. It reports work in progress. The detailed [Achar–Sobaje v1 preprint](https://arxiv.org/abs/2606.21697v1), submitted 19 June 2026, gives a geometric interpretation under its stated good-characteristic and categorical hypotheses. The audit records these hypotheses and checks the statement match. Its full 56-page proof and all prerequisites have not been independently audited here. Nothing in this packet establishes all-characteristic closure or any conclusion about the general geometric question at bad primes.

## Imported conventions and structural inputs

Sym⁴ E is the induced module ∇(4). Self-duality of E does not identify symmetric and divided powers in degree four. The proof uses a degree-two symmetrizer, whose denominator is invertible in characteristic 3. The standard uniqueness of an indecomposable tilting module with prescribed highest weight is imported. The SL₂ induced/Weyl conventions and the established-character cross-check are pinned in [Martin, §1.1](https://arxiv.org/pdf/1705.06980v3#page=2) and [Doty–Henke, Lemma 1.1](https://arxiv.org/pdf/math/0205186v1#page=3). Direct-summand closure is mentioned only for a separate alternative argument, not needed by the elementary main proof.

## Verification and publication boundary

All 22 computational checks were rerun in normal, -O and -OO Python modes with byte-identical results. The upstream audit files, frozen input and four source PDFs were rehashed against their recorded pins; all 18 recorded source-location groups were checked. Computation supplements the written argument and is not a formal certification.

This directory contains only the public mathematical exposition, audit, acceptance report and verification/source metadata. Third-party PDFs, source extracts and renderings, scripts, raw matrices and operation tables, dataset contents and private coordination materials are excluded. File hashes identify the exact bytes in this prepared packet; hashes alone do not certify mathematical truth. Preparation performed no publication.
