# PR 9 exact-algebra and reproduction audit

Reviewed head: `a29887ed0e341851d02fa992c26500d4089267be`. Review completed 2026-09-30 04:33 UTC. This audit concerns the immutable files in `source_snapshot/`, principally `candidate.md`, `checks.py`, `checks_output.json`, and the mathematical transcription in `proof.tex`.

**Verdict: no mandatory mathematical or computational revision found in this audit's scope.** The nongeneric separating example is valid, the rank-one exclusions are valid, and all recorded exact computations reproduce. No elimination or denominator argument in the candidate silently asserts more than its computation proves. The examples remain supplementary checks; the general irreducibility theorem rests on the analytic proof.

I read the candidate and inspected the full source script before running it. I independently completed the polynomial derivation, denominator analysis, rank-one argument, and additional perturbation checks before consulting `REVIEW.md`, `verdict.json`, or `independent_checks.json`. The earlier audit happens to use the same auxiliary-circle mechanism for the polynomial; this coincidence was discovered after independence was preserved. No outside researcher was contacted. No snapshot file, Git branch, commit, or remote was changed by this audit.

## 1. Exact nongeneric example

Let

\[
D=B^2_{xy}+B^2_{xy}+B^2_{xz}.
\]

For a regular real normal \(u=(u_1,u_2,u_3)\), put

\[
r=\sqrt{u_1^2+u_2^2}>0,\qquad s=\sqrt{u_1^2+u_3^2}>0,
\qquad a=2u_1/r,\quad b=u_1/s.
\]

The support point satisfies

\[
X=a+b,\qquad Y=2u_2/r,\qquad Z=u_3/s,
\qquad a^2+Y^2=4,\quad b^2+Z^2=1.
\]

Consequently \(T=X^2+Y^2+Z^2-5=2ab\), and

\[
P=T^2-4(4-Y^2)(1-Z^2)=0.
\]

This is a direct identity. It needs neither independent radicals nor choices of complex square-root branches. As a separate, checkable algebraic certificate, let \(C_1=a^2+Y^2-4\) and \(C_2=b^2+Z^2-1\). After substituting \(X=a+b\),

\[
P=(C_1+C_2)^2+4ab(C_1+C_2)+4a^2C_2+4b^2C_1-4C_1C_2.
\]

The independently written script verifies that identity and eliminates \(a,b\) from the two circle equations plus \(X=a+b\). Its only elimination-basis polynomial is exactly the stated \(P\). This proves a polynomial relation; it does not assert that every complex point satisfying that relation comes from a regular real normal.

The point \(e_3\) is in the generating set for \(S(D)\): it is the sum of the relative-boundary points \(e_1,-e_1,e_3\). The normal \(e_3\) has support value \(0+0+1=1\), so its exposed face is \(2B^2_{xy}+e_3\), and \(e_3\) is on \(\partial D\). Thus \(e_3\in D^\partial\cap\partial D\subset S(D)\). Since every exposed point obeys \(P=0\), its complex Zariski closure \(E(D)\) is contained in \(V(P)\). But \(P(0,0,1)=16\), proving \(e_3\notin E(D)\). This exclusion uses Zariski-closed containment, rather than merely showing that a particular normal fails to expose \(e_3\).

In fact every point of \(2B^2_{xy}+e_3\) is a sum of two unit-circle points and \(e_3\), so the separating example is robust across the flat face. This stronger observation is not needed by the candidate.

## 2. Denominators and saturation

The source script substitutes the rational expressions for \(X,Y,Z\), cancels, extracts the numerator, and reduces it modulo

\[
r^2-u_1^2-u_2^2,\qquad s^2-u_1^2-u_3^2.
\]

The resulting rational denominator is exactly \(r^4s^4\). My independent calculation obtains remainder zero and also checks the explicit polynomial ideal-membership certificate. On the domain used by the proof, both square roots are positive, so this denominator is nonzero. Thus the computation establishes \(P\circ F=0\) on precisely the required regular real domain.

No saturation is needed for that conclusion. Saturation and image-closure issues would arise if the computation were being used to identify the whole complex image or its exact defining ideal. The candidate makes only the valid containment \(E(D)\subset V(P)\), and never substitutes a killed normal into the rational support formula. In particular, \(e_3\) is handled geometrically at its singular normal, rather than by division by zero.

Additional exact regular-normal samples cover \(u_1=0\) with both denominators nonzero, both signs of \(u_1\), and signs of the other coordinates. All satisfy the same polynomial. These samples supplement the universal identity; they are not its proof.

## 3. GP perturbation and boundary cases

The original five-dimensional example has three two-column matrices. All seven nonempty subset ranks reproduce as \(2,2,2,4,4,4,5\), exactly the stated general-position condition. Its two killed summands expose their prescribed coordinate targets for positive \(\varepsilon\), and the third support point has the claimed exact limit.

I independently checked a broader choice of unit targets,

\[
v_1=(3/5,4/5),\qquad v_2=(5/13,12/13),
\]

using the simultaneous prescription \(A_j^Tw=v_j\). Both killed support points remain exactly \(A_jv_j\) for every positive \(\varepsilon\), and the third support point converges correctly. Negative \(\varepsilon\) flips the killed targets. The candidate expressly uses positive \(\varepsilon\), so the sign dependence is handled correctly.

To test the possible hidden orthonormality assumption, I replaced the two killed disc matrices by

\[
A_1=[e_1,e_1+2e_2],\qquad A_2=[e_3+e_4,3e_3-e_4].
\]

These remain in the same GP arrangement but parametrize ellipses with non-orthonormal columns. Solving the surjective transpose equation gives

\[
w=(3/5,1/10,17/52,3/52,0).
\]

The independent script verifies the transpose equation and support-point preservation exactly. Thus the perturbation mechanism uses the correct dual map; it does not implicitly identify a physical-space perturbation with the unit-ball target coordinates.

For rank-one summands, the interval \([-1,1]\) has only the exposed points \(-1,1\), whose complex closure is reducible. For the unit disc plus \([-a,a]e_1\), \(a>0\), normals with positive first coordinate give the open right semicircle centered at \((a,0)\), and normals with negative first coordinate give the open left semicircle centered at \((-a,0)\). A normal with first coordinate zero exposes a nontrivial segment, hence no exposed point. Each open arc is Zariski dense in its complex smooth conic: restriction of a polynomial to its analytic circular parametrization vanishes on an interval only if it vanishes on the full parametrization; equivalently a proper closed subset of an irreducible conic is finite. The conics

\[
C_+=(X-a)^2+Y^2-1,\qquad C_-=(X+a)^2+Y^2-1
\]

are distinct since \(C_--C_+=4aX\), and neither contains the other. The script supplies explicit points on one but not the other. Their union is the exact exposed-point closure and is reducible. At the excluded limit \(a=0\), the two components coincide, recovering the ordinary unit circle. This supports the candidate's deliberately qualified statement that one-dimensional summands cannot be admitted indiscriminately; it does not claim they always cause reducibility.

For a single rank-at-least-two disc, the complex unit-sphere quadric is irreducible: its homogenized quadratic form has rank at least three, whereas a product of two linear forms has rank at most two. An injective linear parametrization carries this quadric isomorphically to the disc's boundary in its span. Repeated discs have the same positive-root support map scaled by their number. Lower-dimensional ambient sums do not affect these arguments. None of these checks challenges the stated edge cases.

## 4. Reproduction and artifact consistency

The inspected `checks.py` performs symbolic calculations, assertions, and a JSON print. It makes no network requests or file writes. I ran it without Python optimization and with bytecode writes disabled, from the review folder. It exits zero with no stderr. Its output is structurally identical to `checks_output.json`, including SymPy version and every subset rank.

The dedicated ignored environment uses Python 3.14.6, SymPy 1.14.0, and mpmath 1.3.0. Neither the initial system interpreter nor the bundled interpreter had SymPy installed. This is an environment setup requirement, not a false reproduction claim: the source README explicitly requires Python 3 and SymPy. Pinning the version would improve convenience, but I do not find it a mandatory correction for these exact finite calculations.

All 154 inline/display math blocks in `candidate.md` match all 154 in `proof.tex` in order, after removing whitespace. A direct Markdown diff confirms that changes from `reviewed_candidate.md` concern status prose, reference formatting, and verification-status prose; no mathematical section changed. The parent audit separately checks PDF visual rendering and recorded hashes. My independent run recorded hashes of every snapshot file before and after execution and confirmed that the snapshot remained unchanged.

The finite checks verify polynomial transcription, a separation value, a concrete GP arrangement and perturbation, support formulas in a repeated-disc example, and a concrete detour-rank example. They do **not** establish connectedness for all subspace arrangements, the real-analytic identity theorem, primality for all discotopes, all GP perturbations, degree formulas, irreducibility of a complex critical locus, historical priority, or formal proof certification. The candidate correctly states that the general result is justified by its analytic proof.

## Evidence and checkpoints

- `algebra_independent_checks.py`: independently written exact derivation, denominator certificate, regular-normal edge cases, arbitrary-target and non-orthonormal GP perturbations, rank-one component checks, source-script reproduction, and snapshot preservation.
- `algebra_independent_results.json`: complete output and snapshot hashes.
- `checks_rerun.stdout.json` and `checks_rerun.stderr.txt`: source reproduction.
- `algebra_artifact_consistency.json`: exact recorded-output and all-math-block comparison.

2026-09-30 04:29 UTC checkpoint: independent exact derivation and first reproduction passed; prior verdicts remained unread until this stage. Completion estimate for this audit remit: 80% (artifact comparison still pending).

2026-09-30 04:33 UTC checkpoint: non-orthonormal perturbation and all artifact comparisons passed. Completion estimate for this audit remit: 100%. This is an estimate of completed audit work, not a probability of mathematical correctness or a claim of human peer review.
