# PR20, problem 30001947: independent bordism-family audit

Final checkpoint UTC: 2026-10-01T18:21:00Z. Completion estimate: 100% of assigned family audit. Frozen candidate head: 7914dfa8c2ddf0efb784a29accc8a05b5a24a690. This report performs no PR disposition action.

**Verdict: the exact negative answer is verified as a prior published result in the standard closed classical PL category.** Goresky–Pardon, *Wu numbers of singular spaces* (1989), §10.5 Theorem A, is the positive exact prior. Its §10.7 Part A applies to dimension 4j+2. The accompanying adapters show that every target middle symmetric bilinear form has zero Witt class, for every j≥0. This is a literature-status correction, not a new theorem or a global priority certificate.

## Independent evidence chain

The criterion was sealed at 18:10:18Z before inspecting the relevant primary theorem bodies. The mathematical reconstruction was sealed at 18:15:45Z before reading the historical review or receipt files. Only afterward did I inspect the frozen prior review, its summary, source checksums, readiness record, and PR draft. No other family's report or root conclusion was read during this audit.

The checkable derivation is in [FIRST_PASS_RECONSTRUCTION.md](FIRST_PASS_RECONSTRUCTION.md). Its three essential steps are:

1. Integral orientation of the regular stratum implies orientability of each link, so the older local-orientability condition adds no target hypothesis. Normalize any nonnormal target; Proposition 5.1.11 in Friedman's book preserves lower-middle intersection homology, its proof applies to every link, and stratified general position makes the middle intersection counts lie in the regular stratum where normalization is a homeomorphism. Thus the pairing itself is preserved.
2. Apply the exact positive-dimensional oriented F_2-Witt theorem to each normal component. No odd-dimensional-link torsion, IP, LSF, s-duality, or isolated-singularity restriction is introduced. The old theorem's printed degree-zero convention differs from the modern integral-oriented Ω_0=Z convention; target dimensions begin at two.
3. If X bounds a collared Witt pseudomanifold W, let K=ker(IH_m(X)→IH_m(W)), m=dim(X)/2. Relative exactness gives K=im(∂:IH_{m+1}(W,X)→IH_m(X)). Field-coefficient Poincare–Lefschetz duality and the boundary pairing identity b_X(∂a,x)=B_W(a,i x) imply K^perp=K. Hence the form is metabolic and zero in W(F_2). This is the explicit bordism-to-pairing adapter.

The complete relevant [Goresky–Pardon theorem and proof](https://www.math.ias.edu/~goresky/pdf/Wu.jour.pdf) were read at printed pp.342–344, together with definitions pp.328–330 and the local-orientability/odd-square foundations pp.335,339–340. [Friedman's 2015 manuscript](https://faculty.tcu.edu/gfriedman/papers/stratwitt.pdf) §5.2.1, pp.27–29, including the full footnote14, gives the historical acknowledgment and explicitly matches the categories. The footnote is corroborating history; it does not substitute for the theorem and adapter.

The [early characteristic-two paper](https://faculty.tcu.edu/gfriedman/papers/2-Witt3.pdf) was read in full. It leaves the higher-dimensional ambiguity in Theorem1 but explicitly settles dimension two. The [book manuscript](https://faculty.tcu.edu/gfriedman/ihbook.pdf), printed p.676, corroborates the complete oriented group computation. Its actual downloaded cover date is July24,2019. Full foreign documents and page images remain solely in ignored tmp/primary_sources.

## Falsification controls and limits

- **j=0:** normalizing a dimension-two target gives oriented closed surfaces; their middle forms have rank 2g and symplectic bases. The result does not depend on a surgery argument whose dimensional hypothesis fails in dimension two.
- **Unoriented countercontrol:** RP^(4j+2) has pairing <1>, but its antipodal sphere-cover involution reverses orientation, so it fails integral orientability. This controls every j, including RP^2.
- **Nonzero homology control:** S^(2j+1)×S^(2j+1) meets the target category and has middle form [[0,1],[1,0]], rank two and zero Witt class. Thus the theorem does not assert vanishing middle homology.
- **Characteristic-two distinction:** I_2 is metabolic but nonalternating. Zero Witt class cannot establish the candidate's stronger alternating assertion by itself. This family verifies the required zero Witt class; the stronger assertion needs the separate §10.2 odd-square argument.
- **Exact computation:** [exact_controls.py](exact_controls.py) exhaustively enumerates symmetric F_2 matrices in dimensions zero through five and constructs/validates Lagrangians for every nonsingular even-dimensional matrix: 1,4,448 examples in dimensions zero,two,four. Counts of nonsingular symmetric matrices in dimensions one,three,five are 1,28,13888. [EXACT_CONTROLS.json](EXACT_CONTROLS.json) is the reproducible receipt. The geometric RP and sphere-product controls are analytically derived formulas, not computed triangulations. The finite matrix run is not a test of the universal geometric theorem.

No exact mathematical gap remains for the original category. The audit does not extend the statement to boundary-bearing spaces, arbitrary codimension-one stratifications, arbitrary non-PL topological pseudomanifolds, or a quadratic Witt/Arf invariant. It does not independently rebuild the entire 1989 surgery proof or certify its global historical priority.

## After-seal receipt comparison and corrections

The frozen old review reaches the same exact answer. It notes normality but relies on the later author's category identification rather than spelling out the isometric normalization and boundary-annihilator adapters; those are supplied here. All ten snapshot input SHA256/byte bindings passed, recorded in [INPUT_BINDING.json](INPUT_BINDING.json). The independently fetched Goresky–Pardon and stratwitt PDF hashes exactly match the frozen original receipts.

**Required mathematical corrections:** none.

**Required reproducibility correction if publishing a version-pinned source package:** add a checksum and explicit actual manuscript date for the book that supplies the cited p.676 corroboration. The frozen source_checksums.json contains no book entry; the actual downloaded book is the 2019 manuscript. Do not claim that those downloaded bytes are the physical 2020 edition. The current early-paper bytes are the author-hosted August13,2012 manuscript; the old receipt's different friedman-arxiv.pdf bytes were not independently recovered, so those are distinct version receipts rather than a verified byte match.

**Recommended documentation corrections:** supplement the currently inaccessible Heidelberg report URL with the official [MFO PDF](https://publications.mfo.de/bitstream/handle/mfo/3271/OWR_2011_56.pdf?isAllowed=y&sequence=1) and use printed pp.3279–3280, especially p.3280 for Question2 (PDF page64). Add the normalization and boundary-pairing adapters to make the note self-contained at the theorem-to-target level. These do not change the negative answer.

The exact primary URL/version/hash/page and visual-inspection ledger is [SOURCE_LEDGER.json](SOURCE_LEDGER.json). The original OWR question and characteristic-two context were checked against the official MFO copy; five key primary source pages were visually inspected. No full foreign text is publishable from this folder's first-party manifest.
