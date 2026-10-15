# Independent audit of the Robinson certificate obstruction

Problem 30000717 / OWR-1465-011. Reviewed 7 October 2026.

## Verdict

**PASS for the complete negative answer in the frozen v2 candidate.** The proof establishes that the Robinson sextic is globally nonnegative but fails both proposed certificate conditions, for the catalogue tangency-minor ideal and for the literal separate-product interpretation of the source. Its stronger statement is also valid: adding any constant epsilon greater than or equal to zero does not give a sum of squares modulo the ideal of functions vanishing on either real variety.

No mathematical correction to this version is required. This is an independent AI-assisted mathematical audit of a candidate argument, not an independent discovery, a formal proof-assistant certificate, or conventional human peer review. No separate audit report was consulted.

The reviewed PROOF.md has SHA256 `a2e2109d45f7776103fc43cff554c7f49de1b9290b92dc62b3d3db5ad23050c1` and 10,165 bytes. The author manifest has SHA256 `0256537fe98d411ca8911c22b341785d029e1f4b51f3a20207e056789bc8e380`. All eight entries in that manifest matched the reviewed files. A separate audit manifest records every reviewed file and the independent controls.

## Exact statement and source fidelity

The catalogue record was matched by exact ID to its source corpus. Its specified generators are the differences x_j f_i - x_i f_j. The requested equivalence includes an exact sum-of-squares certificate modulo the ordinary radical and an epsilon certificate modulo the original ideal for every positive epsilon. A counterexample to either implication from global nonnegativity resolves that equivalence negatively; the candidate supplies both.

I freshly retrieved the [publisher's Oberwolfach report](https://ems.press/content/serial-article-files/46100), verified that its 559,967 bytes have SHA256 `bd4f914a306afd73002d8c74f76e0c468113749240e90815a62ad151a53f783f`, and independently rendered and visually inspected printed pages 798, 810, and 811. Theorem 1 on p.810 distinguishes the ordinary radical in (iii) from the original ideal and positive-epsilon quantifier in (iv). Conjecture 2 on p.811 removes attainment and replaces the ideal; the printed formula visibly has separate products and an ellipsis rather than a minus sign. The candidate correctly distinguishes that reading from the catalogue's differences. It does not assert that an intended correction has been authenticated. Reznick's contribution on p.798 credits and displays Robinson's sextic. The candidate's attribution is appropriate.

Removing an assumption of attained infimum means that attainment is no longer required. It does not require nonattainment. Therefore the fact that the sextic attains its minimum zero is fully compatible with its use here. No zero-dimensionality, isolated-singularity, genericity, positive-definiteness, or strict-positivity hypothesis is present in the target replacement claim. Such hypotheses from neighboring results cannot be imported into it.

## Mathematical reconstruction

### Nonnegativity

For a = x^2, b = y^2, c = z^2, the sextic becomes the symmetric cubic

F = a^3 + b^3 + c^3 - a^2 b - ab^2 - a^2 c - ac^2 - b^2 c - bc^2 + 3abc.

Direct expansion confirms F = (a-b)^2(a+b-c) + c(a-c)(b-c). Symmetry permits a >= b >= c >= 0; both terms are then nonnegative. This proves global nonnegativity without relying on an external non-SOS theorem. The value at the origin is zero.

### Ten lines and low-degree interpolation

The ten projective directions consist of the four (1,+/-1,+/-1) directions and the six directions with one coordinate zero and the other two of equal absolute value. Exact substitution confirms that the form and all three partial derivatives vanish along every entire real line in these directions. The sign and coordinate symmetries and homogeneity used here are valid.

My independent evaluation matrix used a different ordering from the author's matrix. In degree three its determinant is +128, versus the author's -128 in the declared author ordering. These are consistent. The respective evaluation ranks in degrees 0, 1, 2, and 3 are 1, 3, 6, and 10. In particular, every homogeneous form of degree at most three that vanishes at the ten representatives is zero.

I also checked the elementary coefficient proof. The six two-coordinate conditions have rank six on the ten-dimensional cubic space. Their kernel is exactly the span of x(x^2-y^2-z^2), y(y^2-x^2-z^2), z(z^2-x^2-y^2), and xyz. Evaluation at the four remaining directions and the four sign characters annihilates all four coefficients. The reduction of smaller degrees by multiplying by a power of x is legitimate even at the representatives with x=0: the product still vanishes at every representative, and the polynomial ring is an integral domain.

### The extra axis

On the first coordinate axis, R(t,0,0)=t^6 and the gradient is (6t^5,0,0). All separate off-diagonal products vanish; consequently all tangency differences vanish as well. The common zero varieties of both candidate ideals therefore contain this axis and the ten zero lines. No assertion that these are the entire varieties is needed.

### Every constant epsilon and arbitrary SOS degree

Fix epsilon >= 0 and suppose that R+epsilon is a finite sum of real polynomial squares plus a polynomial vanishing on the relevant real variety. On each zero line its restriction is

sum_j q_j(tv)^2 = epsilon for every real t.

Each summand is nonnegative and bounded above by epsilon, so every q_j(tv) is a bounded real polynomial and hence a constant. For epsilon > 0 the constant need not vanish; the candidate preserves it correctly. Writing each q_j as its finite homogeneous decomposition shows that every positive-degree homogeneous part vanishes at all ten representatives. The interpolation result kills the degree-one, degree-two, and degree-three parts identically.

On the extra axis, the same representation gives sum_j q_j(t,0,0)^2 = t^6+epsilon. Every nonzero restriction has degree at most three: if the maximum degree D were larger, the coefficient of t^(2D) would be the sum of the squares of all degree-D leading coefficients, a strictly positive number. No lower-degree or cross term can cancel it. But all degree-one through degree-three terms have already vanished globally. Every axis restriction is therefore constant, which contradicts the displayed t^6 term.

This argument handles arbitrary finite numbers of summands and arbitrarily high degrees in the original three-variable polynomials. It does not assume that an arbitrary SOS modulo an ideal has degree-bounded summands. The only degree bound is proved after restriction to the axis. The proof uses all real values of t, not a finite sample. It neither discards positive-epsilon constants nor homogenizes an inhomogeneous certificate without justification.

### Ordinary and real radicals

If h is in the ordinary radical of L, then h^N lies in L for some positive integer N. At every real zero of L, h^N=0 implies h=0. That elementary observation is sufficient; neither a radical computation nor a Nullstellensatz is needed. The contradiction was established for every h vanishing on the real variety, so it proves the stronger real-vanishing-ideal claim directly. In particular it excludes the smaller ordinary radical and original ideal. Thus epsilon=0 refutes (iii), and every positive epsilon refutes (iv).

The actual gradient ideal is different: Euler's identity places R itself in that ideal. I checked this identity exactly. There is no contradiction with the original gradient-ideal theorem.

## Ancillary assertions

For the tangency-minor ideal, the separate proof of (i) iff (ii) is correct. If a polynomial has a negative value at a nonzero point, minimize it on the compact sphere through that point. A minimizer has a negative value and satisfies the Lagrange multiplier condition, so all tangency minors vanish. The origin is handled separately and belongs to every tangency variety. The sphere is smooth at every point on it when its radius is positive. No global lower bound or attained global minimum is required, including in one variable.

For the literal-product interpretation, the example Q=(1-xy)^2+y^2-1/2 is also valid. The equations yQ_x=0 and xQ_y=0 force the origin: y=0 forces x=0, while xy=1 makes the second product equal to 2. As an independent algebraic check, their Groebner basis is x^2-xy, y^2. Q is 1/2 at the origin and -1/4 at (2,1/2). Its infimum -1/2 is approached on (1/t,t) and is never attained. This refutes the literal version of (ii) implies (i). The candidate correctly does not claim this for the tangency-minor version.

## Related literature and limits

The candidate correctly separates ideal-only certificates from semialgebraic gradient-tentacle certificates. The relevant statements in [Schweighofer's author manuscript](https://www.math.uni-konstanz.de/~schweigh/publications/tentacle.pdf), Theorems 25 and 46 and Open Problem 33, contain inequality multipliers or conditions absent from the target ideal-only claim.

The [Guo, Safey El Din, and Zhi paper](https://perso.lip6.fr/Mohab.Safey/Articles/gcv_sos.pdf), p.2, presents a truncated tangency certificate with an additional SOS multiple of M-f. The preceding definition requires M to belong to the range of f. Neither the multiplier nor that qualification may simply be removed. The candidate's discussion preserves these boundaries. I did not perform a full historical-priority audit or verify every proof in these related papers; they are not needed for the self-contained contradiction.

No claim of newly discovering the Robinson polynomial, the classical ten-zero phenomenon, or the first historical counterexample is accepted or needed. The verdict concerns mathematical validity and fidelity to the specified equivalence, not historical novelty or the status of every related optimization problem.

## Reproducibility and final disposition

The author's verifier produced its 185-assertion JSON output byte-for-byte on a fresh run against the frozen snapshot. My separately authored verifier passed 51 exact controls, including independent matrix construction, low-degree ranks, polynomial identities, all zero-line and axis restrictions, cubic-kernel identification, and the literal-example Groebner basis. Neither program is used as a substitute for the universal argument above.

There are no requested corrections and no unresolved mathematical blockers in v2. The appropriate disposition is a complete negative answer to the four-way equivalence as specified, with the explicit source-formula distinction and the stated attribution and review limits retained. Acceptance attaches to the reviewed hashes; substantive subsequent edits require renewed review.
