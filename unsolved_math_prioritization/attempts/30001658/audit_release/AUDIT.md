# Independent adversarial audit: Boolean-cube inequality

Problem 30001658 / OWR-4791-015; supplied rank 704. Audit date: 2026-10-05 UTC.

## Verdict

**PASS WITH A NONBLOCKING DOMAIN CLARIFICATION, for an unresolved 5/5-approach research packet.** No source-consistent counterexample, erroneous retained partial proof, or missing dependency that invalidates a retained theorem was found. This is an independent AI mathematical/code audit, not human peer review or proof-assistant certification. It does not establish the unrestricted conjecture, historical novelty, or present global openness.

The exact frozen author input has nine regular files totaling 41,351 bytes. Its manifest SHA-256 is `68a1fa6b5900a7cc03cd2d991e1a135afb2366a169b680ad5ac9db335203ed68`. `INPUT_BINDING.json` independently records every filename, byte count and digest, including the manifest. The original files were not edited. This audit and its independent code are separate.

One editorial clarification is recommended for PROOF.md §3: change “For a coordinate subcube the exact largest coefficient C” to “For a proper coordinate subcube (codimension k >= 1), the exact largest coefficient C.” The displayed quotient contains k in its denominator. For k=0, A is the full cube, the right-hand side vanishes for every C, and there is no finite largest C. The preceding k>=1 context communicates the intended domain; the author already handles the full-set inequality correctly. No theorem, finite certificate, or five-approach status depends on applying that formula at k=0. The frozen input is preserved; this audit records the clarification rather than rewriting it.

### Controlling endpoint qualification and dependency sweep

This audit's acceptance is governed by the following explicit interpretation, not by extending an undefined formula. Exact locations refer to the bound original PROOF.md, SHA-256 `05d1e18988b9e60bd7d95bda4c1b237a38a991a007e40a19ada45b2fb2b1ba79`:

- **Lines 72–76:** the largest-coefficient quotient and “every finite k” refer only to integers k>=1. At k=0 the coefficient is unrestricted because it multiplies zero; the largest finite coefficient does not exist.
- **Line 76:** the singleton estimate C<=2+4/n refers to positive integers n. Its n→infinity consequence C<=2 is unchanged. The n=0 cube furnishes no coefficient constraint.
- **Lines 58–70:** the auxiliary resolvent bound is well defined at k=0 and equals 1/2; the full cube is its coordinate-subcube equality case. The target itself has q=0 and is strict for every nonzero f, consistently with line 37. Thus auxiliary-bound equality must not be conflated with target equality or coefficient optimality.
- **STATUS.json lines 12–13 and APPROACH_LOG.md line 6:** the universal coefficient is not declared established; the necessary ceiling two relies on the positive-dimensional singleton sequence only. Neither use depends on k=0.
- **check_math.py:** the closed-form/strict-subcube controls loop over k=1,...,100. Its affine-coset auxiliary bound safely includes k=0, while the strict target is tested there only for positive codimension. This audit separately verifies the full-set target and auxiliary equality at k=0. No tested quotient divides by zero.
- **PROOF.md §7, README.md and the remaining status/approach descriptions:** no additional finite largest coefficient for the full cube, endpoint extremizer, or universal coefficient optimality claim is made. The unresolved universal-achievability statement remains unresolved.

All uses of coefficient optimality and endpoint equality were checked under this qualification. This is a nonblocking clarification of the retained result, but it must accompany any presentation of the unrestricted wording in lines 72–76.

## 1. Source and identity review

The original report was independently retrieved from the EMS Press PDF URL. Its 731,310 bytes and SHA-256 exactly match the author metadata. The auditor rendered and visually inspected PDF pages 29–31, bearing printed pages 33–35. The title, author, equations (7), (10)–(13), and the prose surrounding equation (12) were checked. The source is [Combinatorics, Oberwolfach Reports 01/2011](https://ems.press/journals/owr/articles/4791), DOI 10.4171/OWR/2011/01.

The working target has arbitrary real f on the entire cube and arbitrary nonempty A. The logarithm is base two, its argument is 2^n/|A|, the squared absolute-value sum is over A, and the additional mass term has coefficient four. No supported-on-A assumption belongs in this target.

The source calls its energy a sum over connected vertex pairs without explicitly using the word “ordered.” The double-counted interpretation is fixed by the surrounding mathematics, not by preference: its supported inequality (13) is stated to recover the ordinary edge-isoperimetric inequality (7) upon substituting an indicator. The required identity is E(1_A,1_A)=2|boundary A|. Counting each edge once would instead assert the false factor-two strengthening already contradicted by a one-vertex subcube. Equation (11)'s normalization is consistent with the double-counted convention. In counting measure the correct identities are E_c=2<f,Lf> and E_c+4||f||²=2<f,(L+2I)f>.

The arXiv PDF [An inequality for functions on the Hamming cube](https://arxiv.org/pdf/1207.1233) was separately downloaded: its 171,341 bytes and SHA-256 also match the author record. Pages 1–2 were visually checked, and the opening operator discussion was read. The neighbor sum under uniform expectation explicitly double-counts edges. Theorem 1.1 requires support inside A. Multiplication by 2^n gives the supported counting-measure inequality used in §5; it supplies no unrestricted equation-(12) conclusion. The [Cambridge record](https://www.cambridge.org/core/journals/combinatorics-probability-and-computing/article/abs/an-inequality-for-functions-on-the-hamming-cube/3770E7921E125EF4A73A413E396348CB) verifies online publication on 29 March 2017, journal volume 26(3), pages 468–480, DOI 10.1017/S0963548316000432. The full published proof was not re-audited; none of the retained self-contained partials requires it.

The requested catalog URL independently returned HTTP 403, and the web reader could not access it. No full raw catalog record or underlying corpus was available to this auditor. Thus the primary mathematical target is verified, while the mapping of the supplied rank/ID to that target retains the author's descriptor-based limitation. There is no exact live-page match, raw-record hash verification or full-dataset match. The author's bounded literature searches and repository duplicate checks were not exhaustively repeated; they cannot establish a global negative finding and are not needed for this verdict. Public source metadata and exact inspection limits appear in `SOURCE_AUDIT.json`.

## 2. Resolvent criterion and equality

Let b=1_A and M=L+2I. Since L is positive semidefinite, M is positive definite. The absolute-value contraction is coordinatewise: ||f(x)|-|f(y)|| <= |f(x)-f(y)|. The mass and target absolute-value sum are unchanged. Weighted Cauchy–Schwarz therefore proves sufficiency of (k/m)b^T M^-1 b <= 1, with k=log2(2^n/m).

Necessity requires a nonnegative extremizer, and the packet supplies it correctly. With adjacency H, M=(n+2)I-H; the Neumann series has nonnegative terms, converges because n/(n+2)<1, and every matrix entry is strictly positive by cube connectivity. Thus f=M^-1b is a strictly positive admissible extremizer for nonempty A. For this f the quadratic Cauchy–Schwarz inequality is exact. This proves the claimed equivalence, rather than merely a sufficient spectral test.

If q<1, equality in the target forces f=0. If q=1, equality in Cauchy–Schwarz fixes |f| as a positive multiple of M^-1b; equality in absolute-value contraction then forces the same sign on all adjacent vertices, hence globally. This conditional classification is sound and does not assert that q=1 actually occurs for a proper finite set.

For A=Q_n, k=0, so equality also requires f=0. For empty A the displayed quotient is undefined; exclusion is necessary unless the right side is separately defined as zero. For n=0 there is one vertex, L=0 and M^-1=[1/2]; the only nonempty A is full and the target is 4f²>=0. The independent checker explicitly covers this extension. No division by n or a nonexistent random-walk generator is used at n=0.

## 3. Review of the five substantive approaches

### 3.1 Fourier relaxation and dense sets

With uniform orthonormal characters, L has eigenvalues 2|S|. Therefore H(A)=sum_S bhat(S)^2/[2(|S|+1)], with mean a and total Fourier square mass a. The denominator four for nonconstant modes yields H(A)<=a(1+a)/4. Multiplying by k/a gives exactly the sufficient condition k(1+a)<=4.

The density-at-least-1/8 conclusion is valid. For a in [1/8,1/4], k<=3 and 1+a<=5/4, so q<=15/16. For a>=1/4 the direct mass-term argument applies since k<=2. Full and zero-function cases are harmless. The relaxation obstruction 165/128 at a=1/32 is correct and is properly labeled unrealizable formal spectral data rather than a set or counterexample. The missing indicator constraints prevent a universal conclusion.

### 3.2 Affine subspaces in every dimension

Character orthogonality gives the claimed flat Fourier magnitudes on the annihilator. A rank-k linear subspace has a set of k pivot coordinates with bijective coordinate projection. Every full word has weight at least its pivot restriction, which is sufficient for the termwise reciprocal bound. The binomial sum evaluates to (1-2^(-k-1))/(k+1). Consequently q<=k(1-2^(-k-1))/(k+1)<1 for k>=1.

The equality description for the auxiliary bound is also correct: equality in a sum of nonnegative termwise losses forces every annihilator word to have zero entries off the pivots. This makes the annihilator a coordinate subspace, and A a coordinate subcube. The full cube supplies the trivial k=0 auxiliary equality; it is excluded from the largest-coefficient quotient as clarified above.

The exact proper-subcube optimal coefficient follows from the resolvent extremizer. The simpler singleton indicator in dimension n gives C<=2+4/n for any universal C, so C<=2 is a valid necessary universal ceiling. Neither this ceiling nor a strict finite-dimensional affine inequality proves that C=2 works on all sets. The passage from linear annihilators to arbitrary indicators is expressly missing.

### 3.3 Entropy and the weaker universal coefficient

The two-point proof has the correct derivative comparison and endpoint handling: the atanh derivative is dominated by that of s/sqrt(1-s²), and continuity treats s=1. The homogeneity normalization and absolute-value reduction are valid. Entropy's Hessian form is nonnegative by Cauchy–Schwarz; adding a positive constant and taking a limit justifies zero coordinates. The chain rule and convexity establish tensorization with the correct direction.

With the specified edge convention this gives E_mu(f)>=2 Ent_mu(f²). Binary conditional Jensen gives the KL expression. Dropping -(1-q)ln(1-a), which is nonnegative, and using binary entropy <=ln2 are sound. The Cauchy–Schwarz lower bound q>=s²/(aV) can be substituted because ln(1/a)>=0. The resulting E_mu+2ln2 V >=2ln(1/a)s²/a implies the retained all-dimension coefficient 2ln2 with mass coefficient four. Scaling back to counting measure is correct.

The remaining constant loss is real at the level of this relaxation. The formal entropy/energy data used to demonstrate insufficiency are carefully distinguished from an actual cube function. The stronger base-two coefficient is not obtained by the fixed additive reserve. This proof is self-contained and does not depend on the later paper's logarithmic-Sobolev display.

### 3.4 Supported functions and exterior minimization

The block matrices are principal submatrices of the ambient Laplacian, with diagonal n; substituting the induced-subgraph Laplacian would be incorrect. Completing the square gives the stated Schur complement and exterior minimizer. Its correction is positive semidefinite, so inversion reverses the comparison in precisely the unfavorable direction claimed.

For n=1, R_AA=3/8 while the supported shifted inverse is 1/3. For the even-parity set of Q_4, B has row and column sums four and D=6I, hence BD^-1B^T has eigenvalue 8/3 on the constant vector. This exceeds two and defeats the proposed operator-order bridge. Neither example defeats the target. The supported theorem bounds a different inverse and no universal transfer is supplied.

### 3.5 Distance kernel, coordinate compression and finite checks

Integrating noise-operator eigenvalues gives 1/[2(|S|+1)]. The counting-measure transition kernel includes its factor 2^-n; the resulting rational K_n(d) formula has the correct prefactor. The incomplete-beta identity follows from the telescoping binomial derivative. Positivity and strict distance decrease are valid, including endpoint interpretation.

Compression preserves set cardinality and does not decrease the resolvent pair sum. It does not purport to preserve the Dirichlet energy of an arbitrary function. The fiber comparison accounts for diagonal pairs, both orders of distinct-fiber pairs, singleton/singleton pairs, and singleton/double or double/double pairs. Only opposite singleton fibers can strictly improve. Every nontrivial compression lowers total Hamming weight, so finite termination is guaranteed; a terminal set is a downset. No unjustified commutativity of coordinate compressions is assumed.

The author's downset recursion is complete and duplicate-free. Its rational atanh bounds have the correct tail exponent 2t+1 and upper tail denominator. Dividing the lower ln(r) by the upper ln2 indeed supplies an upper bound for k after subtraction; the integer-log branch handles powers of two exactly. The finite certificate is valid. It offers no bound for the unresolved cross-kernel term in an all-dimension downset induction.

These are five distinct substantial lines of argument. They support “unresolved after 5/5 approaches”; no sixth research route or universal-resolution claim is needed or justified.

## 4. Independent exact computation

`independent_checks.py` imports no author code and makes no network calls. It differs materially in the critical computational choices:

1. Full rational Gauss–Jordan inversion constructs M^-1 for n=0,...,5. Exact matrix multiplication checks MR=I, all entries positive, row sums 1/2, and all 1,365 entries against the claimed distance formula. Signed rational vectors check the edge/matrix factor and a separate fast Walsh transform checks Fourier normalization.
2. A Gray-code walk visits every subset through n=4. It updates K1_A and the quadratic form on both insertions and deletions instead of using the author's lowest-set-bit recursion. All 65,808 nonempty sets for n=1,...,4 are checked, plus the one nonempty n=0 set. Every coordinate compression through n=4 is tested in the union/intersection fiber implementation.
3. Dimension-five downsets are generated from maximal-element antichains using comparability exclusion, independently of the author's two-layer recursion. The ideal map is injective, the count is 7,581, and every resulting set is checked downward closed. The empty set is counted but never passed to a logarithm. Each nonempty ideal's pair sum is calculated as a diagonal sum plus twice the unordered-distinct-pair sum, then independently checked by the fast Walsh transform.
4. Logarithms use no series and no floating-point comparisons. For D=256, integer binary search finds the least j with 2^j m^D >= (2^n)^D. Then k<=j/D. The upper comparison and predecessor failure are retained as exact controls. This method avoids the author's logarithm code and error analysis.
5. Linear spaces through n=4 are recognized by exhaustive XOR closure, then translated into all affine cosets. All 373 cosets across n=0,...,4 satisfy the auxiliary bound, strict target and auxiliary equality characterization. This is a regression check, not the proof for arbitrary dimensions.

The independent run passes **1,282,085 exact checks**, with identical frozen output under normal Python and `-O`. The dimension-five cardinality histogram and SHA-256 of the sorted ideal masks are retained in `INDEPENDENT_RESULTS.json`. The exact largest q values certified by the upper bounds, with singleton lower witnesses, are:

- n=0: 0
- n=1: 3/8
- n=2: 7/12
- n=3: 45/64
- n=4: 31/40
- n=5: 105/128

The n=5 assertion for arbitrary sets uses the proved compression lemma. These values are finite results only; their monotone approach toward one is not an induction or a universal proof.

Eleven explicit false-identity/false-bridge controls are rejected: single-counted energy, dropping counting/uniform scaling, wrong resolvent shift, missing kernel half, omitting the second pair order, reverse compression, erased Schur correction, parity correction bounded by two, the degree-one relaxation implying the target, a positive full-set logarithm, and universal coefficient three. These are targeted mathematical negative controls, not an exhaustive fault-injection or software-security campaign.

## 5. Replay, integrity and limits

Both normal and optimized invocations of the pinned author verifier pass with exactly 704,115 mathematical checks, six mathematical negative controls, eight integrity-negative controls, and byte-identical frozen mathematical output. The author's eight controls include mutated contents, missing/extra files, duplicate or unsafe manifest entries, wrong byte count, wrong external manifest pin, and a rehashed false resolution status.

Additional real filesystem tests are run against temporary copies, in both modes: an empty extra directory, an extra symlink, and replacement of PROOF.md with a symlink. Every case fails specifically at the directory/symlink guard. The original source snapshot is rechecked after the complete replay and is unchanged. `REPLAY_RESULTS.json` records the outputs and hashes.

These checks authenticate the exact supplied input relative to the externally supplied manifest pin and provide reproducibility. They do not establish the trustworthiness of an unknown pin, formal theorem correctness, resistance to arbitrary concurrent hostile filesystem changes, or source-record identity that was not available. The result counters are supplemental evidence and are not substitutes for the analytic review above.

Only authored audit text/code and public verification metadata are in this audit packet. Third-party PDFs, HTML, text extracts, rendered images, raw catalog records, dataset contents and private coordination material are excluded. No remote changes, publication, merge, release or outreach was performed by this audit.
