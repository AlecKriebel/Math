# Independent analytic review — Zenodo 23393596

**Disposition: PASS for the exact mathematical statements reviewed. Completion: 100%.** No substantive mathematical defect or unresolved load-bearing interface was found. This is an AI-assisted independent analytic review, not independent human or journal peer review, not formal proof-assistant certification, and not a priority determination. Root publication disposition remains separate.

## Identity and custody

Work: *Deep derived pure braids need not be 1-solvable*, Alec Kriebel, version 1.0, manuscript date 15 October 2026, four pages. Public record: https://zenodo.org/records/23393596.

| Asset | SHA-256 |
|---|---|
| `sources/deep-derived-pure-braids-v1.0.pdf` | `6547831e57c6eb01e7f4632ff67230f1e93d4ca6fec353e128b9c97a1f2c8b89` |
| `sources/deep-derived-pure-braids-source-verification-v1.0.zip` | `a123728e0e8e8c6160738d6703bb757fe285a04c29872d2441d168c33bb2f106` |
| `sources/record.json` | `d050764d8262d87e06c92a2cf3cadc90543828368d83e14460c91a341cf517a0` |
| Package's authenticated `PACKAGE_MANIFEST.json` | `497295cd857a48bd767bf92a2c7b3390005a72f756cadd8b9b4581e0d703f447` |

All 213 regular ZIP members match their extracted bytes. The embedded `note.pdf` equals the public main PDF. All 218 files under `sources` match the pre-replay inventory. This includes byte hashing of excluded historical assessments, not reading or adoption of their contents. Fresh source acquisition belongs to the scope family; this reviewer independently checked its public pins, exact ZIP membership, primary receipt hashes and final unchanged state. Replays ran only in this review's cache, using copied, unchanged submitted programs.

## Strongest verified result and boundaries

For each **finite** integer \(k\geq1\) and each \(m\geq3\), the ordinary derived subgroup \(P_m^{(k)}\) contains a classical disk pure braid whose standard oriented closure is not integrally smoothly 1-solvable, with solvability defined exactly by Otto Definition 2.3. Consequently \(P_m^{(n+2)}\not\subseteq\mathcal F_n^m\) for every integer \(n\geq1\) and \(m\geq3\), interpreting containment in the string-link concordance group.

The separately specified nested commutator 

`a=σ₁², b=σ₂², c=[a,b], d=a⁻¹ca, e=b⁻¹cb, u=[c,d], v=[d,e], β=[u,v]`

lies in \(P_3^{(3)}\). Its freely reduced Artin word has 104 letters and closure signature −2. Its stated 48-dimensional Goeritz certificate has inertia (23,25,0), determinant −7154819319988224 and zero exceptional-crossing correction. These are exact results, not numerical approximations.

The quantifiers do not assert one braid in the intersection of all derived subgroups. The universal proof is existential at arbitrary depth; the explicit witness addresses depth three. A 104-letter displayed diagram is not a claim of minimum crossing number. The exclusions \(m=1,2\) are necessary because their positive derived subgroups are trivial. The argument supplies no result for rational solvability, surface braids, a power subgroup, or a lower-central-series replacement. It makes no \(n=0\) noncontainment assertion and is compatible with the cited prior inclusion \(P_m^{(2)}\subseteq\mathcal F_0^m\).

**Exact remaining mathematical gap:** none identified in the stated theorem or the explicit certificate. Priority, independent human assessment and formal certification are outside this conclusion.

## Proof review

The complete reconstruction is in `INDEPENDENT_DERIVATION.md`.

1. **Signature on the pure subgroup, Lemma 2, pp.1–2.** Verified the relevant closure signature is a bounded-defect function on \(B_3\), its homogenization differs by at most six, and the pure elements (a,b,h,z) satisfy \(ahb=z\). Their homogenized values −2,−2,−2,−4 contradict homomorphism on \(P_3\) itself. No inference merely from nonhomomorphism on the larger braid group is used.
2. **Pointwise obstruction, Lemma 3, p.2.** Reconstructed the signed-integer/mod-two rank argument for the −1 local system, the universal-coefficient dimension bound, and saturation by the geometric hyperbolic basis of a 1-solution. Checked that both sets of surface groups lie in the commutator subgroup and that the meridian character extends via the integral \(H_1\) isomorphism. Verified Toffoli's compatible one-colour surgery formula applies pointwise at −1, including Alexander roots; its corrections all vanish for the zero framed linking matrix. This avoids knot-only, averaged-signature or rational-solution substitutions.
3. **Derived persistence, Lemma 4, p.3.** Reconstructed descent to the solvable quotient using only one defect inequality on \((gu)^r=g^r u_r\). Homogeneity, normality and amenability close the argument. The credited stronger prior defect-restriction result is correctly attributed.
4. **Theorem 1, pp.1 and 3.** Verified the power amplification \(r|q(v)|>6\), preservation of derived membership, vanishing of pairwise linking numbers, split-strand embedding to all \(m\geq3\), and monotonicity of the solvable filtration for integer \(n\geq1\).
5. **Finite example, Section 4, p.3 and support.** Independently constructed the nested commutator and computed its signature before opening submitted executables. Reconstructed the group-theoretic membership separately from finite word checks. Read the necessary checkerboard derivation and the entire current release replay chain. The all-depth theorem does not depend on the finite example.

## Primary interfaces actually inspected

The exact PDFs, versions, original URLs and verified hashes are recorded in `read-coverage.json` and `custody-and-comparison.json`. Only the relevant portions of the long primary works were read; no whole-book or whole-article coverage is claimed where it did not occur.

- **Harvey, joint with Park and Ray:** full contribution, printed pp.3020–3021, especially Question 3 and the ordinary derived-series convention. [Published workshop report]\(https://ems.press/content/serial-article-files/46709?nt=1\). This is the exact containment question addressed; it is not a generic substituted problem.
- **Gambaudo–Ghys:** the signature/Meyer definition and theorem/remarks, the three-strand matrices and full-twist computation, and the homogenization bound. [Published article](https://www.numdam.org/item/10.24033/bsmf.2496.pdf). The relevant formulas concern link closures with the correct sign convention.
- **Otto:** Section 2's string-link/closure conventions, filtration, and all clauses of Definition 2.3, printed pp.2630–2632. [Published article](https://msp.org/agt/2014/14-5/agt-v14-n5-p05-s.pdf).
- **Toffoli:** the extending-character signature-defect identity, framing compatibility, the one-colour signature domain, Theorem 4.24 and Remark 4.25 Eq.(4.21), with the surrounding proof/correction terms. [Repository copy of the published article](https://epub.uni-regensburg.de/52299/1/the-atiyahpatodisinger-rho-invariant-and-signatures-of-links.pdf). The fresh cached full PDF was inspected even though this review's extra web open timed out.
- **Calegari:** amenability examples on printed p.27 and the complete proof of Proposition 2.65, p.33. [Author-hosted book](https://math.uchicago.edu/~dannyc/books/scl/scl.pdf).
- **Kawasaki–Kimura–Maruyama–Matsushita–Mimura:** complete Lemma 7.12 and proof, printed p.1207. [Published article](https://msp.org/agt/2025/25-2/agt-v25-n2-p15-p.pdf). The current web parser returned an empty page, so the authenticated fresh PDF and text were the actual evidence.
- **Erle:** the closure convention and checkerboard definition, diagrams, local signs and cyclic-matrix discussion, printed pp.161–165, with visual inspection of pp.162–165. [Published article in the Kobe repository](https://da.lib.kobe-u.ac.jp/da/kernel/E0003685/E0003685.pdf). The necessary support already identifies a printed index discrepancy and derives the correct crossing-based formula; no source was repaired in this review. The replay separately tests an example that distinguishes those index choices.

## Fresh controls and published replay

`fresh_braid_controls.py` was written and executed before submitted helper inspection. It uses standard-library exact rational arithmetic and rank-one Meyer forms, rather than importing the supplied generic kernel/pullback implementation. `fresh_braid_results.json` records the full word, all 104 Meyer terms, exact matrix, strand tracking, and controls: powers of two-strand and central families, mirror/inverse signs, Artin and cancellation identities, eight normal-coset power identities, and 120 fixed-seed integer rank comparisons. There are 3,603 asserted conditions, of which 3,384 are routine determinant checks; that number is not presented as 3,603 independent theorem tests.

The current unmodified `verify_package.py` was then run with isolated, nonoptimized Python, an externally pinned package manifest and the exact public PDF. It passed the author certificate (286 additional controls), planar-face Goeritz reconstruction and independent supplied Meyer reconstruction, including exact JSON comparisons without floating tolerances. `published-replay.json` retains the result. This current entry point does **not** rerun the archived historical SymPy recovery/full transport suites; those are outside this review's finite-replay claim and are not needed for the theorem's proof.

`check_custody_and_comparison.py` then checked fresh-versus-replayed literal word, all 104 term values and final matrix, all primary PDF receipt hashes, and full source custody. It passed. The historical expected numerical JSON files were used as machine-compared finite certificate data after independent reconstruction; dedicated historical mathematical verdict bodies were not consulted.

## Coverage, independence and exposure

Read all four actual published PDF pages in text and visually, all 273 lines of the matching TeX, the entire 59-line strengthening proof and 148-line original mathematical proof, and the full current verifier/guard and three invoked programs (275,22,286,428,336 lines). Also read the replay README and requirements. Archive inventories and all file hashes were inspected; unrelated historical audit/opinion/priority bodies and sibling reports were not read. No sibling mathematical findings were received or used before this conclusion.

Necessary main/support/README text does contain historical review-status language, references to accepted or certified checks, attempt counters and summaries of past review outcomes. This incidental exposure is disclosed. It was not treated as correctness evidence; the present derivation, fresh controls, primary interfaces and current replay support the verdict. In particular no bounded prior search, “accepted” label or past verifier success is adopted as a priority or correctness certificate.

The mandatory programme objective was read before work. Review artifacts live only in `reviews/analytic`; sources and earlier assigned work remain unchanged. No repair, publication, website, spreadsheet, Git, UI or outreach action was taken. No follow-up conjecture is recommended by this analytic review.
