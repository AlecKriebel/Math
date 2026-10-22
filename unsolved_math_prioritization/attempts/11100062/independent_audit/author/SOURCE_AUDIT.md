# Source and status audit

Inspection date: 2026-10-06. This is a bounded literature and prior-attempt audit, not an exhaustive bibliography or proof of continued openness. The mathematical target and all conclusions concern positive reduced powers P^t at odd primes. Source uses of the phrase "Steenrod algebra" are not silently treated as equivalent to that narrower target.

## Authentication

The complete catalogue record and its complete research report were found in the supplied full datasets. SHA-256 of the UTF-8 statement is `6055561ae2b477ae943d2573395dbf511009567505becec77d997386fc8f67ec`. The default Python serialization `json.dumps([complete_problem, reports.get(problem_number, {})], sort_keys=True).encode()` has SHA-256 `0035ad78168e1c596c7fb55b3e1ff09a556fe617ba10e274b3522b74a4e6aa5f`. Both match their supplied pins.

Hovey's [exact unstable-homotopy page](https://www-users.cse.umn.edu/~tlawson/hovey/unstable.html) was downloaded. Removing HTML tags from the third substantive item and normalizing whitespace produced an exact match to the complete authenticated statement, including its attribution paragraph. The catalogue's [public problem URL](https://unsolvedmath.com/problems/11100062) returned a 59-byte Forbidden response; no live catalogue body was inspected. The primary question nevertheless passed the exact-statement gate through Hovey's page and the pinned complete record. No source text or complete dataset record is included here.

## Literature actually inspected

1. **Hovey, unstable homotopy theory, item 3.** Whole HTML page inspected. It establishes the exact question and attribution, not its present status.

2. **C. A. McGibbon and C. W. Wilkerson, Loop spaces of finite complexes at large primes (1986), Proc. AMS 96, 698–702.** [DOI](https://doi.org/10.1090/S0002-9939-1986-0826505-X). Direct publisher PDF access returned 403. It was not treated as directly read. Its rational-elliptic hypothesis and large-prime conclusion were cross-checked in Anick 1992 Theorem 6 and Stanton 2025 Section 7. No claim of independently auditing the 1986 proof is made.

3. **D. J. Anick, Single loop space decompositions (1992), Trans. AMS 334, 929–940.** [Public scholarly copy](https://www.sas.rochester.edu/mth/sites/doug-ravenel/otherpapers/anick1.pdf). Complete PDF downloaded and text extracted. Pages 929–934 and the references were inspected closely: Theorems 4 and 6, the torsion-permitting decomposition conjecture, and the distinction between torsion-free and general loop spaces. The explicit Bockstein calculation on pages 934–939 was not independently reconstructed.

4. **D. J. Anick, Hopf algebras up to homotopy (1989), J. AMS 2, 417–453.** [DOI](https://doi.org/10.1090/S0894-0347-1989-0991015-7). Publisher PDF returned 403. Theorem 9.1 is used through the precise restatement in Menichi; direct proof inspection is not claimed.

5. **L. Menichi, P-th powers in mod p cohomology of fibers (2001).** [arXiv:math/0101221](https://arxiv.org/abs/math/0101221), [journal DOI](https://doi.org/10.1016/S0764-4442(01)01872-9). Complete five-page author preprint downloaded and read. Page 2 was also rendered and visually inspected for the filtration and total-degree conventions. The Anick theorem, Eilenberg–Moore Steenrod-compatible filtration, and the final still-open question are distinct statements. Proposition 5.1 in RESULT.md is an explicitly derived degree bound, not a quotation of a theorem claimed to appear in this paper.

6. **L. Stanton, Loop space decompositions of moment-angle complexes associated to two-dimensional simplicial complexes (2025).** [Published article](https://doi.org/10.1017/S0013091525000203), [author preprint](https://arxiv.org/abs/2407.10781). The downloaded 22-page current arXiv PDF was inspected at the introduction, Section 7, and relevant definitions. Page 21, containing Corollaries 7.2 and 7.3, was visually inspected. This supplies credited special cases, not the newest general moment-angle result.

7. **L. Stanton, Homotopy theory of looped polyhedral products, Southampton PhD thesis, August 2025.** [Repository record](https://eprints.soton.ac.uk/503922/), [indexed PDF](https://eprints.soton.ac.uk/503922/1/Lewis_Stanton_Thesis_Final.pdf). The university's indexed repository metadata establishes the date; indexed text from Conjecture 1.3 says the Steenrod-action assertion remains open. Direct complete-PDF retrieval returned 401. Only the indexed statement and metadata were inspected. This limitation remains explicit.

8. **L. Stanton and F. Vylegzhanin, Anick's conjecture for polyhedral products, arXiv:2506.15573v3 (14 January 2026).** [Versioned record](https://arxiv.org/abs/2506.15573v3), [PDF](https://arxiv.org/pdf/2506.15573v3). The live record confirms v3, 26 pages, with improved torsion and Steenrod results; no journal acceptance was reported there. The complete current PDF was downloaded. The introduction, Section 2 definitions, Section 4.6, Theorem 6.4, and Sections 6.5–6.8 and 6.13–6.17 were inspected for scope and dependencies. Proposition 4.19 and the loop splitting are the exact external inputs for Corollary 4.1. The underlying Backelin–Roos theorem is credited through this paper, not independently re-proved. Neither its general-polyhedral-product formulas nor its cone-pair results remove assumptions on arbitrary ingredient spaces. No bound involving Bocksteins is asserted in the derived corollary.

9. **S. Büscher, F. Hebestreit, O. Röndigs, M. Stelzer, The Arone–Goodwillie spectral sequence for Σ∞Ωⁿ and topological realization at odd primes (2013), AGT 13, 127–169.** [Publisher PDF](https://msp.org/agt/2013/13-1/agt-v13-n1-p05-s.pdf). Complete PDF downloaded; the Bott–Samelson statement in the proof of Proposition 4.3, printed page 143, was inspected. This is an explicit research-paper use of the classical theorem, not a claim that the original Bott–Samelson article was directly read.

10. **D. J. Anick, A loop space whose homology has torsion of all orders (1986), Pacific J. Math. 123, 257–262.** [Publisher PDF](https://msp.org/pjm/1986/123-2/pjm-v123-n2-p01-s.pdf). PDF downloaded and the original construction/result on printed pages 257–260 inspected. It gives a finite simply connected four-dimensional counterexample to eventual integral loop-homology torsion-freeness. It is not presented as a reduced-power counterexample.

## Bounded repository search

Read-only searches in AlecKriebel/Math were performed for the exact ID and problem number across pull requests, default-branch files, commits, issues, and branch names, together with the narrow phrase "unstable homotopy" in pull requests. No actual attempt for this problem was returned. A broad Wilkerson/Steenrod/loop search returned unrelated PRs and was not counted as evidence of a prior attempt. The catalogue's zero-turn desk review is not an attempted proof. This search cannot establish that no unindexed or differently named prior work exists.

## Limitations and release scope

No full solution or fixed-X counterexample was verified. No priority claim is based on the negative search. The general status is conservatively unresolved by this investigation, supported by the bounded contemporary literature check. The original 1986 decomposition proof, original 1989 Anick proof, and complete 2025 thesis were not directly available.

All third-party PDFs, extracted source text, screenshots, complete corpus records, failed-response bodies, and private research materials are excluded from the release. SOURCE_METADATA.json includes only public-source bibliographic/retrieval facts and verification hashes and sizes. The mathematical note is authored commentary and proof, not redistribution of source documents. Fresh independent review remains required before publication.
