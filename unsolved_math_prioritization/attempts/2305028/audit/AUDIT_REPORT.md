# Independent audit: Function Theory Problem 5.28

## Verdict

**PASS.** The proposed classification `already_solved` is supported by the exact problem update and by the complete relevant published argument. The submitted reconstruction proves its stated claim: there is **one fixed nonconstant disk-algebra function** F such that

\[
\limsup_{t\downarrow0}
\frac{|F(1-t)-F(1)|}{B_F(t)}
\ge \frac{1668}{1667}>1.
\]

Consequently the interior-to-boundary modulus ratio in Problem 5.28 does not always tend to 1. No blocking mathematical defect was found in the reconstruction. The result is a verification of a known 1975 negative answer, not a new resolution, and the numerical constant is not asserted to be optimal.

The recorded single source-verification turn is consistent with stopping once the known resolution is established; neither the packet nor this audit represents five unsuccessful attempts as having occurred.

## Scope and source identity

Reviewed in full: `PROOF.md`, `README.md`, `SOURCE_GATE.md`, `RESEARCH_LOG.md`, `STATUS.json`, `verify.py`, and the recorded `verification.json`. The review also read the source statement and update, the article's introductory definitions, the relevant Section 4 argument, and all displayed formulas on printed pages 35-39 directly from page images.

1. W. K. Hayman and E. F. Lingham, [Research Problems in Function Theory](https://arxiv.org/abs/1809.07200), Problem and Update 5.28, printed p. 95 (PDF p. 96). The numerator is a supremum over the open disk with Euclidean distance at most t; the denominator uses Euclidean chord distance on the unit circle. The update explicitly attributes the negative answer to Rubel, Shields and Taylor, reference [679]. Reference [679] identifies the 1975 article below.
2. L. A. Rubel, A. L. Shields and B. A. Taylor, [Mergelyan Sets and the Modulus of Continuity of Analytic Functions](https://doi.org/10.1016/0021-9045(75)90112-4), *Journal of Approximation Theory* **15** (1975), 23-40; Lemmas 4.1-4.2 and Proposition 4.3, pp. 35-39. The [University of Michigan record](https://deepblue.lib.umich.edu/items/6c023c47-bf4b-4c8d-be84-2ac067221820) identifies the preserved full article. Proposition 4.3 itself states a single-function radial limsup greater than 1.

The arXiv bibliographic page was accessible during this audit. The repository landing page returned HTTP 403 and the DOI resolver was unavailable through the web tool; source inspection therefore used the already-preserved full PDFs and page images, whose hashes were verified. Those retrieval limitations do not leave the theorem or problem statement dependent on a search snippet. No independent exhaustive historical or repository-priority search is claimed.

## Analytic checks

### 1. Half-plane boundary maximization

The endpoint choice a = 1/4, b = 1/3 is valid: the source's Lemma 4.1 allows b <= 1/3, as is visible in the page image. Principal powers extend continuously to the closed right half-plane, including zero, and are holomorphic on its interior.

For positive y, both coordinates and the argument of g(iy) increase. Differentiation of its argument's tangent with respect to y^(b-a) gives the positive numerator sin((b-a)pi/2), with a positive denominator. Opposite-sign imaginary-axis endpoints separated by s lie in a sector of radius |g(is)| and angle at most pi/3. For radii 0 <= q <= r and angle theta <= pi/3,

\[
|re^{i\theta}-q|^2\le r^2+q^2-rq\le r^2.
\]

The two same-sign cases are also covered: y^p - (y-s)^p is nonnegative and decreasing for y >= s and 0 < p < 1. The cross-term cosine is positive, so the squared two-power difference decreases as well. Conjugation handles the remaining half-axis. The extremal pair 0, is attains the bound, and monotonicity in s proves the full supremum for all separations <= t. Thus equation (1) is established globally, not by local sampling.

The phase difference of i^(1/4) and i^(1/3) is pi/24, so |g(i)| = 2 cos(pi/48). There is no phase or factor-of-two error in this identity.

### 2. Bounded cutoff and strict gap

For Re z >= 0,

\[
|R+z|^2=R^2+2R\operatorname{Re}z+|z|^2
\ge \max(R^2,|z|^2).
\]

Splitting |z| <= R and |z| >= R proves |z|^p/|R+z| <= R^(p-1). Hence the claimed bounds M = 320 and A <= 5/262144 are correct. At infinity one has the uniform estimate

\[
|h(z)|\le R\bigl(|z|^{a-1}+|z|^{b-1}\bigr)\longrightarrow0,
\]

which supplies exactly the decay needed by the subsequent compactness argument. The cutoff has no pole in the closed half-plane.

The displayed difference identity for h is algebraically correct. Its first multiplier has absolute value <= 1 and its second term is bounded by A times the point separation, yielding B <= G + A. The radial value h(1) = 2R/(R+1) is positive.

The cosine certificate uses only 3 < pi < 4, the alternating-series upper bound, and the strict decrease of 1 - x^2/2 + x^4/24 on (0,1). It gives the claimed strict rational gap over 1001/1000. Positivity is stronger than required: B >= |h(i)-h(0)| > 1, since R > 1. The independent arithmetic check also verifies the positive margin

\[
h(1)-\frac{1001}{1000}\left(G_{\rm upper}+A_{\rm upper}\right)
=\frac{1558287051479}{824633769984000}>0.
\]

### 3. Expanding-circle convergence

This is a genuine global convergence of suprema, not just convergence on bounded arcs. For a sequence N tending to infinity, take maximizing pairs on C_N and first pass to a subsequence on which B_N approaches its limsup. Compactness of each circle and of its closed admissible-pair set guarantees that maximizers exist.

If one endpoint's norm becomes unbounded, pass to a subsequence tending to infinity. The distance constraint <= 1 forces both endpoints to escape, so both h-values tend to zero uniformly. Otherwise take a bounded convergent subsequence. The circle equation Re z = |z|^2/(2N) places both limits on the imaginary axis, their separation remains <= 1, and continuity bounds the limiting difference by B. This proves limsup B_N <= B.

For the reverse inequality, the explicit near-side points

\[
z_N(u)=N-\sqrt{N^2-u^2}+iu
\]

converge to iu. If |u-v| < 1, the approximating chord eventually has length < 1. For a pair of length exactly 1, first replace u,v by su,sv with 0 < s < 1, apply the strict-length argument, then let s increase to 1. This order of limits resolves the potentially troublesome closed-distance constraint. Taking the supremum proves liminf B_N >= B.

The submitted prose suppresses the initial limsup-realizing subsequence, a standard compactness convention supplied explicitly above. This is not a missing hypothesis or a gap. The proof works for every sufficiently large real N, as required for every small real t.

### 4. Rescaling and disk-algebra membership

The map z -> N(1-z) bijects the closed unit disk with the disk centered at N of radius N. Its interior lies in the open right half-plane; only the boundary can meet zero. Consequently each k_t is holomorphic on the open unit disk and continuous on its closure, despite the fractional-power singularity at the boundary point 1.

For N = 1/t, boundary distances multiply by exactly N. Therefore

\[
B_{k_t}(t)=B_N/M,
\]

with equality, and the radial pair 1-t, 1 maps to 1, 0. Division by M preserves the gap and gives the uniform norm bound <= 1. Since B_N >= B/2 > 1/2, the fixed lower bound c = 1/640 is valid. The strict half-plane gap and convergence allow one common N_0 for all N >= N_0. In particular t_* < 1, so all radial test points lie in the stated disk.

### 5. One function and the gliding-hump estimates

The induction is not circular. The amplitudes epsilon_n = q^(n-1) are fixed in advance, and q > 0. At step n only the finitely many previously chosen continuous functions occur in the old-term bound. Uniform continuity allows a positive t_n satisfying that bound and the independent requirements t_n < t_(n-1)/2 and t_n < 1/n. Then k_n is chosen at that scale. Future functions cannot spoil the estimate because their uniform norms are <= 1 and the whole future amplitude sum was bounded in advance.

For every n, the future differences cost at most

\[
2\sum_{j>n}\varepsilon_j
=\frac{2q}{1-q}\varepsilon_n
\le\eta c\varepsilon_n.
\]

The old terms cost at most another eta c epsilon_n. The old-term modulus is the full closed-disk modulus, which is essential for controlling both radial and boundary differences. Writing b_n = B_(k_n)(t_n) >= c gives a total error <= 2 eta b_n epsilon_n. Reverse triangle inequality supplies the radial lower bound; triangle inequality and a supremum supply the boundary upper bound. There is no assumption that their maximizing pairs coincide.

The series for F converges uniformly on the entire closed disk by the M-test. Its limit is continuous there and holomorphic inside by locally uniform convergence. It is one fixed series, with infinitely many fixed bad scales, rather than a sequence of unrelated counterexamples. The radial lower bound is positive. Thus F is nonconstant, and its boundary modulus is positive at every positive scale: a zero modulus would force constancy around the circle by finite chains of short arcs, then throughout the disk by the maximum principle.

Division is therefore legitimate. The resulting ratio is exactly

\[
\frac{1001/1000-2/10000}{1+2/10000}
=\frac{1668}{1667}.
\]

Since t_n tends to zero, this proves the claimed radial limsup bound.

### 6. Exact problem conventions

The numerator in the problem uses open-disk points, while the reconstruction uses a closed-disk supremum and a radial pair with one boundary endpoint. This causes no difference: for every closed-disk admissible pair z,w, the contracted pair rz,rw is in the open disk for 0 < r < 1, remains within the same distance bound, and its function difference converges to that of z,w. The open and closed suprema are therefore equal.

The boundary denominator uses chord distance throughout; no replacement by arc length or merely asymptotically equivalent metric occurs. Constant functions' undefined 0/0 ratios do not affect this nonconstant counterexample. A limsup greater than 1 suffices to refute the proposed limit; existence of a different full limit is neither needed nor claimed.

## Qualifications concerning the printed source proof

These are **nonblocking source-exposition issues**, not defects in the submitted reconstruction:

- Printed p. 37 says to choose a large R_0 while displaying R_0 <= 1. This is a sign/typographical slip; the argument requires a sufficiently large positive R_0.
- After equation (4.6), the cutoff correction is written as O(delta). Relative to |g(i delta)| of order delta^a, the directly justified bound is O(delta^(1-a)). This still is o(delta^(b-a)) because b < 1.
- The next displayed expansion on p. 37 has coefficient 2 eta, whereas equation (4.5) supplies coefficient eta. Indeed the lower bound |h(i delta)| and upper bound |g(i delta)| + A delta for the boundary modulus yield the corrected expansion

\[
\frac{h(\delta)}{B_h(\delta)}
=1+\eta\delta^{b-a}+o(\delta^{b-a}).
\]

This still gives the weaker strict lower bound with coefficient eta/2 used in equation (4.7), and so preserves Lemma 4.2 and Proposition 4.3. The packet avoids all these printed asymptotic/sign issues by using a fixed R, a finite-scale strict rational gap, and a separately proved circle limit. The classification therefore does not depend on silently treating the source's erroneous intermediate displays as exact.

## Computational reproduction and integrity

- All 30 files named by the supplied frozen manifest matched their recorded SHA-256 values. Every reviewed public file was byte-identical to its preserved original copy.
- Running the author's `verify.py` under Python 3.12.14 returned exit code 0 and no stderr. Its stdout was byte-identical to the recorded `verification.json`.
- The separately written `independent_verify.py` imports no author code. It reconstructs the rational cutoff bounds, checks the strict gap, derives the geometric-tail allowance, verifies the final fraction, and performs redundant exact finite-index regressions. All checks passed.
- A final integrity recheck confirmed that none of the frozen inputs changed. No publication or external write was performed.

The scripts establish arithmetic consistency. They do **not** formally verify complex analysis, optimize a boundary supremum by finite samples, certify the choice of infinitely many scales by computation, or substitute for the analytic arguments above. This remains an unrefereed mathematical audit.

## Disposition

Accept `already_solved`, with the known negative answer attributed to Rubel, Shields and Taylor (1975), Proposition 4.3. Accept the reconstruction's explicit lower-bound certificate. No mandatory correction to the frozen author packet is required. The source qualifications above should remain available with the audit so that a reader does not mistake the printed intermediate asymptotics for fully literal statements.
