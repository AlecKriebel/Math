# Fresh correctness and original-scope review of PR #1235

Review of exact head `0266089ae6d4d8cc6392a2944c6f8c75967eb74e`, base `4b27092a448d53b61408355ce44ec38d103a1ce4`, completed 22 October 2026. This is a mathematical/source-scope family review, not a publication-package approval. Overall program progress remains 79%.

**Result:** the r=6 and r=7 exact integer-point counterexamples survive the independent falsification checks. They resolve the full catalog target negatively. No mathematical gap was found in the written weighted inequalities or the convention safeguards. A separate new affine consequence is proved in `AFFINE_ADDENDUM.md`; that deduction was not claimed by the historical PR and should receive its own independent challenge before promotion. Priority and package-readiness work remain separate.

## Original target authenticated

The complete cached SQL row was read with SQLite `mode=ro`, without invoking repository code. Its key 30000107, problem number OWR-741-001, and statement SHA-256 `cc21604d975453fc38e6a6ae6110678297ed51b86dfe57a450394ecd711edeb6` match the pinned catalog. The record asks whether every nonempty fixed-boundary fiber Bh=b, Rh<=c, with integral b and c, contains an integral point. It is not an affine-triangulation-only catalog question. The complete source statement and prior-report field were read; the latter is empty. The live problem-page attempts returned HTTP429, without bypass.

The [official OWR report](https://ems.press/content/serial-article-files/45962?nt=1), contribution beginning printed p.2072, states the arbitrary-integral-boundary/rhombus-RHS extension on p.2073/PDF p.7, then gives the convex-hull triangulation assertion as a sufficient Conjecture 1. The saturation paragraph's contradictory nonintegral-vertex wording is visible in the actual PDF; it does not redefine the authenticated catalog target. Relevant PDF pages6–7 were read and page7 was visually inspected.

The numeric-grid GWS catalog read occurred before mathematical inspection. It resolved gid1254632077 to Math Puzzles, returned 191 nonempty rows, and contained no exact lead for the numeric target, OWR identifier, generalized/generalised hive phrase, or legacy arXiv identifier. This is a bounded catalog check, not priority evidence.

## Primary definitions and literal published conflict

The [published De Loera–McAllister paper](https://www.maths.tcd.ie/EMIS/journals/EM/expmath/volumes/15/15.1/DeLoera.pdf), Experimental Mathematics15(1),7–19, was freshly downloaded and its relevant pages3–4 and8–9 were read; pages3,8,9 were visually inspected. Definition2.2 uses triples summing to r and the same three primitive inequalities. Definition4.2 allows arbitrary integral right-hand sides with nonnegative array and slack coordinates. Conjecture4.5 includes an integer-vertex conclusion for every nonempty such fiber; Theorem4.6 states this through r=6. No dominance, partition, positive-boundary, or zero-rhombus-RHS condition is added to the generalized definition. Consequently the exact r=6 fiber contradicts that literal integer-vertex consequence under the displayed conventions. This does not diagnose the historical computation.

The [arXiv v1 source](https://arxiv.org/abs/math/0501446v1) was also freshly retrieved; relevant PDF pages4–5 and12–14 were read. Its definitions and theorem have the same scope. Its five-level example labeled r=5 is corrected to r=4 in the published version. This localized correction supplies no basis to shift the theorem's side parameter. The current arXiv record lists one version dated25 January2005; a later typeset date inside that PDF is not a new result date.

Fresh PDF hashes match the previously reported identities, but all source inspections and executions claimed by this review were performed anew. Historical verification records are not substituted for missing code.

## Exact independent checks

`verify_independent.py` was written for this review. It uses only the standard library and exact integers/Fractions. No author code, scholarly source code, numerical solver, Lean toolchain or historical verification program was executed.

The geometric authority is the triangular metric di^2+di*dj+dj^2. Each unit edge with two adjacent unit triangles gives an elementary rhombus. The common edge has squared length1 and the opposite diagonal length3. The row puts -1 on the common-edge endpoints and +1 on the opposite vertices. Every reconstructed row is then checked against the published indexing formulas. There are 36/49 elementary triangles and45/63 rhombi at r=6/7, respectively; no indexed row is missing or duplicated.

The exact checker verifies every entry of both complete nonzero-bound lists and every reduced inequality in all four weighted tables. It checks the boundary indices, all four half-valued witness coordinates, every remaining zero coordinate, ceil(Rh*) at every row, and every nonnegative slack. At r=6 the bound counts(-1,0,1) are(2,33,10), with24 zero and21 half-valued slacks. At r=7 the counts are(2,50,11), with41 zero and22 half-valued slacks.

The lower and upper sums give -2a<=-1 and2a<=1 at r=6, where a=h(1,1,4); at r=7 they give -2d<=-1 and2d<=1, where d=h(1,4,2). Every other interior variable cancels. These identities exclude every integral array in the unrestricted fiber, and hence every integer point in the augmented nonnegative fiber. They do not merely produce fractional vertices.

The unit block-triangular minor on boundary-array and slack columns has determinant1 (checked directly), so no hidden full-column-lattice restriction excludes the right-hand sides. The top boundary value is zero, ordinary boundary differences are zero, and eliminating or restoring the top coordinate preserves integrality. If a common boundary level is left free, subtracting its integral level from a purported integer array reduces it to this zero-boundary instance.

Adding q(i,j,k)=i^2+j^2+k^2 gives Rq=2 at every rhombus, checked exactly. Thus both examples also have strictly positive integral boundary and rhombus data after translation; the forced entries become37/2 and43/2. This confirms that negative original bounds or nonnegative augmented variables do not explain away the obstruction.

For boundedness, every rectangular R2 sum was checked symbolically to telescope to the target coordinate minus its two boundary coordinates plus the top value. For a zero-boundary recession vector, this gives u<=0. Each R1+R3 sum was checked to give the second-difference concavity inequality on its fixed-k segment; zero segment endpoints then give u>=0. Thus the recession cone is zero. The nonnegative augmented fibers are also bounded because their slacks are determined linearly by h.

Normal, -O and -OO executions produced byte-identical receipts. Each mode rejected12 deliberate corruptions per rank: integral RHS change, fractional RHS, witness change, wrong target, wrong side parameter, wrong boundary, reversed signs, changed nonnegative weight, negative weight, matrix coefficient change, displayed sign change, and omitted rhombus. The changed nonnegative weight is rejected by coefficient cancellation; guards use explicit exceptions and survive optimization. That is72 actual control rejections across the three executions.

## New affine consequence and remaining boundaries

The r=7 augmented witness has total coefficient sum13. Its integral RHS therefore lies in13 conv(columns M), while no nonnegative integer column representation exists. The new addendum proves that a genuine affine unimodular triangulation would force such a representation. An explicit determinant-one lifted basis and determinant-one difference basis establish the full relevant affine lattice; an explicit signed representation also places(beta,13) in the homogenized column lattice. The boundary-zero face is addressed directly. This is a new scope consequence, kept separate from the exact-head PR's carefully limited historical acceptance.

The full original integer-point target is verified negative independently of that addendum. Conical unimodular covers are impossible for both examples; the separate affine conjecture at r=7 is also negated by the additional degree argument. Neither result challenges ordinary Littlewood–Richardson saturation, because the examples have nonzero generalized rhombus data.

No comprehensive priority verdict, proof of absence of an erratum, diagnosis of an old implementation, corrected maximal small rank, publication approval, merge, DOI reservation, ledger update or outside contact is supplied. Further independent scrutiny of the new affine corollary is recommended within the existing review process; the root agent handles any promotion. Raw source bodies and ledger/SQL bodies remain private; this report, addendum, exact checker and compact receipts contain authored reasoning and necessary mathematical data only.

Family completion: **95%** for the requested correctness/source-scope work, with further independent verification of the newly found affine consequence pending. Overall: **79%**.
