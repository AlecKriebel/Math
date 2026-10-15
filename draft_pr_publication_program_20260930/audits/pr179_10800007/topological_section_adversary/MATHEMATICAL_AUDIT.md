# Independent topological falsification audit of PR179 / 10800007

Author: independent audit agent assigned to the topological section mechanism.
Date: 2026-10-13 UTC. Original head supplied for this case: `090b45356f5d6829f755fbc7c5b1fde5565de695`.

**Verdict: PASS for the literal all-parameter/open-set/exact-section obstruction.** No mathematical flaw was found in the submitted proof. The class of admissible open covers is empty. The result is a classical local ramification obstruction, not a computation of a repaired finite genus or a claimed new monodromy theorem. This audit does not establish historical intent, novelty, exhaustive literature status, or a result for Problem 2B.

## 1. Exact target, assumptions, and source fidelity

For `p=(a1,a2,a0,b1,b2,b0)` in Euclidean R^6, the submitted system is

\[
 F_p(x,y)=\bigl(x^2-y^2+a_1x+a_2y+a_0,\;xy+b_1x+b_2y+b_0\bigr)=0.
\]

An admissible set U is open in this entire parameter space and has a continuous, single-valued function `phi:U->R^2` satisfying this equation exactly. Success means proving or refuting the asserted impossibility of such a U containing p=0. The cover conclusion then follows without assuming a finite or countable cover.

I independently checked the primary journal HTML Section 2, the published PDF p.205, and the original preprint pp.5–6, including visual page inspection. They specify the same family with arbitrary affine real a,b and ask for open sets covering the full R^6. Exact selection is in Problem 2A; fixed positive root-position tolerance is separately in Problem 2B. Section 2 gives no removed locus qualifying the full-domain statement. These are narrow source checks, not a search for every possible erratum. [Published article, p.205](https://armj.math.stonybrook.edu/pdf-Springer-final/015-0011-9.pdf), [journal HTML, Section 2](https://armj.math.stonybrook.edu/html-articles/Files-2015-2024/15-11/), [original preprint](https://arxiv.org/pdf/1504.01997).

The source's subsequent claim of covering number two for the square-root example cannot hold on all C with this open/exact definition. It holds on punctured C. That mismatch is a consequence of the proof below; it does not identify the author's intended correction. The imported `problem.json` does not itself print the polynomial definitions, so primary-source verification mattered.

## 2. Fully reconstructed obstruction, with no root classification assumption

Define the embedding of the real plane, written C,

\[
 \iota(u+iv)=(0,0,-u,0,0,-v/2).
\]

Its coefficient norm is `sqrt(u^2+v^2/4)<=|u+iv|`. Thus a coefficient ball around p=0 pulls back to a complex disk. Equivalently, continuity of the embedding pulls any open neighborhood U of zero back to an open neighborhood of zero, which contains a disk D_r.

On this slice,

\[
 F_{\iota(\zeta)}(x,y)=0
 \quad\Longleftrightarrow\quad
 (x+iy)^2=\zeta.
\]

The factor 1/2 in b0 is essential and correct. This uses the real-linear homeomorphism R^2=C; x and y remain real. Every real ordered pair solving the two equations is represented by precisely this complex number. For nonzero zeta there are exactly two such pairs, both nonzero; at zeta=0 there is only the pair (0,0). There are no extra real roots available to a restricted selection.

If phi existed on U, the function `s(zeta)=phi_1(iota(zeta))+i*phi_2(iota(zeta))` would be a continuous exact square root on D_r. Choose `0<rho<r` and set

\[
 \eta(t)=\rho e^{2\pi it},\qquad
 q(t)=\frac{s(\eta(t))}{\sqrt\rho e^{\pi it}},\qquad 0\le t\le1.
\]

The denominator never vanishes. The equation gives `q(t)^2=1`. Its values are therefore in {+1,-1}; continuity and connectedness of the interval force a constant sign. However, eta(0)=eta(1), so the numerator has equal endpoints, whereas the denominator has opposite endpoints. Thus q(1)=-q(0), impossible for a constant nonzero sign. This proof establishes a contradiction on a circle in every open neighborhood; it never differentiates the selection or invokes analytic continuation.

Every proposed open cover has at least one member containing p=0. That member would be an impossible U. This is valid for arbitrary index sets, disconnected members, non-locally-finite covers, and arbitrarily small members. In particular, infinite cardinality does not help. Saying the number is +infinity is a convention for an unavailable finite section cover; the sharper statement here is that no admissible cover exists at all.

## 3. Independent degree, fundamental-group, and path checks

On the circle `|zeta|=rho`, exactness forces `|s(zeta)|=sqrt(rho)`. Rescale to a map h:S^1->S^1 satisfying h(w)^2=w. For any continuous loop h on S^1, a continuous angle lift along the interval gives an integer endpoint winding n. Squaring doubles that endpoint winding. The identity loop has winding 1, so the equality would imply `2n=1`. No such integer exists.

In fundamental-group terms, squaring on C\{0} induces multiplication by 2 on Z. A right inverse would have to induce an integer-valued group homomorphism n with `2n=1`. This reasoning uses the unramified restriction only. It does not incorrectly declare the squaring map a covering at zero, nor infer the local theorem merely from a global obstruction on punctured C. Openness forces an entire nonzero circle into the restriction.

The submitted polygonal path also checks directly. Its segments `(1-t)+i*t` and `(1-t)+i*(2-t)` agree at t=1, connect 1 to i to -1, and satisfy

\[
 \tfrac12\le |\gamma(t)|^2\le1\quad (0\le t\le2).
\]

Indeed each squared norm is `2*(t-1/2)^2+1/2` or `2*(t-3/2)^2+1/2` on its own unit interval. Squaring c*gamma closes the parameter loop and reverses the root endpoint. The submitted ratio is well-defined, has square 1, and has opposing endpoint signs. That is the same valid sign obstruction. Numerical samples are not used to infer that the path avoids zero: the displayed inequalities prove it for every t.

These are distinct proof presentations of the same monodromy mechanism, not three independent research discoveries. The first assessment reconstructed them before exposure to any prior verdict.

## 4. Ramification, multiplicity, real roots, and degeneration

On the constant slice, the real Jacobian determinant of the pair (f,g) is `2*(x^2+y^2)`. Both roots at nonzero zeta are simple, while the zero root is singular. A sign change cannot pass through zero on the chosen nonzero parameter circle because an exact root there has norm sqrt(rho)>0. Continuity at the central parameter does not identify the two choices along that circle.

Algebraic multiplicity is not extra selectable points. For the complexified equations at zero, the quotient algebra

\[
 \mathbb C[x,y]/(x^2-y^2,xy)
\]

has basis `1,x,y,y^2` and dimension 4. Relations reduce all degree >=3 monomials to zero; a four-dimensional multiplication representation in `exact_controls.py` proves the remaining four monomials independent. The complex intersection multiplicity is consequently 4, while the real squaring map has local topological degree 2. These two notions need not coincide. Neither changes the singleton real root set at the origin. The submission's proof does not rely on interpreting the source's multiplicity count as distinct roots.

The entire family can be expressed, without complexifying the real variables, as

\[
 H_p(z)=f_p(x,y)+2i g_p(x,y)
       =z^2+\alpha z+\beta\overline z+\gamma,
\]

where

\[
 \alpha=\tfrac12a_1+b_2+i(b_1-\tfrac12a_2),\quad
 \beta=\tfrac12a_1-b_2+i(b_1+\tfrac12a_2),\quad
 \gamma=a_0+2ib_0.
\]

This also independently confirms that empty real fibers are not causing the negative result. On a sufficiently large circle of radius R,

`R^2>(|alpha|+|beta|)*R+|gamma|`.

The boundary map `z^2+t*(alpha*z+beta*conj(z)+gamma)` never hits zero for 0<=t<=1. Its winding is therefore 2. If H_p had no zero inside, its normalized boundary map would extend across the disk and have winding zero, a contradiction. Thus a real root exists for every coefficient. This surjectivity proof is supplementary: the local no-cover proof already works on the slice alone.

Extra real roots occur in other fibers. For example `H(z)=z^2+conj(z)` has the root 0 and the three unit roots with `exp(3i*theta)=-1`. Such a fiber supplies four real ordered pairs. Their availability elsewhere cannot change the two-root slice used in the obstruction.

## 5. Precise puncturing and altered-cover boundaries

On punctured C the two slit open sets

\[
 V_1=\mathbb C\setminus(-\infty,0],\quad
 V_2=\mathbb C\setminus[0,\infty)
\]

cover the base and have continuous argument choices in (-pi,pi) and (0,2pi). Halving the argument gives a square root on each. A single global branch fails by the circular sign proof. Hence this particular punctured model has section covering number exactly 2. This is a model statement, not the genus of the punctured six-coefficient problem.

Adjoining 0 to both slit domains yields exact branches continuous in their subspace topologies: their root norm tends to zero at the added point. Those domains cover all C but are not open at zero. This is a checkable counterexample to extending the theorem to arbitrary cover classes and confirms that openness is doing real work.

Deleting only p=0 from R^6 does not fix the full family. For any c=h+ik, choose the slice

\[
 p_c(u+iv)=(-2h,2k,h^2-k^2-u,-k,-h,hk-v/2).
\]

Then H at this coefficient is `(z-c)^2-(u+iv)`. At c=1 the basepoint is `(-2,0,1,0,-1,0)`, which is nonzero, and all points on the slice have nonzero fixed linear coefficients. The same proof rules out a local section there even in R^6\{0}. All fibers of this slice still have only the translated two roots. The critical identities are verified symbolically for arbitrary h,k,u,v.

Conversely, a singular root by itself is not enough to obstruct every local selection. At

`p=(1,0,-3/4,0,-1/2,0)`

the fiber has a singular root `(1/2,0)` and a different root `(-3/2,0)` with Jacobian determinant 4. The real implicit function theorem supplies an exact local section through the latter. Thus one must not replace the verified statement by the unsupported claim that every singular fiber has no section. The submission does not make that stronger claim. A repaired domain would need an explicit definition; its genus is not computed here.

## 6. Approximate selections: local cure and persistent global obstruction

The source's approximation tolerance is distance to some root, not a polynomial-residual threshold. On the constant slice every root has norm sqrt(|zeta|). The constant selection 0 is within a fixed epsilon>0 of a root on `|zeta|<epsilon^2`. Thus the exact local circle argument cannot simply be reused at arbitrarily small radii for Problem 2B.

This distinction is also true in a genuine six-dimensional neighborhood. Let L_p be the real-linear part of H_p and c_p its constant term. The conditions

`||L_p|| < epsilon/2` and `|c_p| < epsilon^2/2`

describe an open coefficient neighborhood of zero. At any root, with r=|z|, `r^2 <= ||L_p||*r+|c_p|`. If r>=epsilon, then `r^2-(epsilon/2)*r-epsilon^2/2>=0`, but the strict bounds force it to be negative, impossible. Every root lies strictly within epsilon, and at least one root exists by the preceding winding argument. The constant function 0 is consequently an admissible approximate choice on this neighborhood.

A global approximate section on the constant slice still fails for fixed finite epsilon. Choose rho with sqrt(rho)>epsilon and use the circular loop. For a putative approximate value w(t), the ratio

`w(t)/(sqrt(rho)*exp(pi*i*t))`

lies in the union of the two disjoint radius `epsilon/sqrt(rho)<1` disks centered at +1 and -1. Its continuous image must stay in one of those disks, but its endpoint values have opposite signs and lie in opposite disks. Therefore one set cannot cover the entire slice approximately. This gives a lower bound of 2 for the all-parameter approximate problem, not a solution of it.

For completeness, two approximate domains suffice for the model C alone. Choose `0<R0<R1<epsilon^2` and a continuous radial cutoff chi which is 0 at radii <=R0 and 1 at radii >=R1. Enlarge each V_j by the disk `|zeta|<R0`; set the selected value 0 at radii <=R0, and chi(|zeta|) times its slit-domain square root above R0. The cutoff ensures continuity at the joins; wherever the choice differs from an exact root its distance is <=sqrt(R1)<epsilon. These two open domains cover all C. This construction exposes the exact/approximate distinction without settling the six-parameter variant.

## 7. Reproducibility, adversarial results, and remaining gap

`exact_controls.py` uses standard-library rational sparse polynomials and exact matrices. Its 13 controls prove identities and boundary examples for indeterminate variables or exact rational points. The original verifier was copied into an excluded private replay directory together with the original proof, then executed only there. It reproduces all 5,618 controls and the original recorded verification JSON exactly. Source files remain unchanged. These computations check factors, identities, and finite diagnostic consistency; the nonexistence theorem is the analytic/topological argument above.

The attempted falsifications failed for: additional-root escape on the slice, switching through zero on the nonzero loop, root multiplicity, disconnected open domains, arbitrary cover cardinality, topology of the six-coefficient embedding, treating real pairs as complexified solutions, and using global nonexistence alone as a local argument. The boundary tests succeeded in identifying genuine scope changes: nonopen covers, punctured complex base, approximate local choices, and singular fibers with simple-root escape. They do not refute the submitted theorem.

There is no remaining gap in the literal claim established here. The precise unresolved questions are any intended finite-genus repair, Problem 2B for the complete family, an exhaustive erratum/status/priority investigation, and human mathematical peer review. Existing `claimed_solved` metadata or previous AI review verdicts are not evidence and should always retain the literal-formulation qualification. No publication, tracker, Git, or outside-person action was performed by this auditor.

The read ledger records actual exposure and exclusions. The independently sealed first assessment preceded all post-seal metadata reads. No original review file, upstream report, sibling new report, or Root opinion was read at any point. Own audit completion: 100% upon final artifact sealing; this does not alter Root's case estimate or campaign counts.
