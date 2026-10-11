# Bounded-derivative metric: complete corrected reconstruction

This is an AI-assisted, unrefereed mathematical draft. Acceptance records one independent internal AI mathematical reconstruction of an identified prior theorem, with explicit local proof repairs. It is not human peer review or formal proof-assistant certification. This is a prose proof-and-audit edition, not a computational reproduction package. No novelty, priority, sharp-constant, or worldwide-current-openness claim is made.

Target: 2307027 / AMR-022-7027, the simply connected component of Rubel’s Problem 7.27. The metric theorem is credited to Cameron MacMahon, arXiv:2609.20607v1, Theorem 1.2. AUDIT.md is an editorial acceptance/dependency record of this same reconstruction, not a second independent mathematical review.

## Verdict and exact scope

**The metric assertion of Cameron MacMahon, arXiv:2609.20607v1, Theorem 1.2, is accepted after the explicit local proof corrections below.** The printed proof is not correct line by line. Its principal construction nevertheless proves exactly the claimed universal comparison, with its original exact constant unchanged:

\[
 c_0 d_\Omega(p,q)\leq \rho_\Omega(p,q)\leq d_\Omega(p,q),\qquad
 c_0=\frac12\exp\!\left[-\frac{8}{3\sqrt{2\pi}}e^{9/2}\right]>0.
\]

Here a domain is a nonempty connected open subset of the complex plane; it is assumed simply connected. Points are arbitrary interior points, including equal points. The whole plane is included separately. The supremum defining rho ranges over all holomorphic functions on the domain whose complex derivative has modulus at most one everywhere; boundedness of the function itself is not required. The distance is the infimum of Euclidean lengths of rectifiable curves lying in the domain and joining the two points.

The precise numerical values are lambda = 95.764372363267614842288441547093... and c_0 = 1.28537995815742697641270946578... x 10^-42. The manuscript's rounded values 95.76 and 1.29 x 10^-42 are consistent approximations. The formula, not either rounded decimal, defines the certified constant.

This is a reconstruction and correction of an identified prior result, not a claim of a new metric-comparison theorem, priority, journal acceptance, or validation of the rest of the manuscript. In particular, the general-domain question of L. A. Rubel, Problem 7.27 in Hayman--Lingham, remains broader than this simply connected result. Nothing here establishes a corresponding positive universal lower constant on arbitrary multiply connected domains, an exact formula, or a sharp constant.

## Sources and inspected version

1. Cameron MacMahon, *On Simply Connected Domains Supporting an Unbounded Analytic Function with Bounded Derivative*, [arXiv:2609.20607v1](https://arxiv.org/abs/2609.20607v1), submitted 17 September 2026. The retained 15-page PDF is 706185 bytes, SHA-256 02726890facc133e05eb014369887153f9dd85cb5c55de468a7d893e546e1447. The statement is on PDF/printed page 2; the complete proof of Theorem 1.2 occupies pages 6--10. Those proof pages were read in full. Pages 6--10 were visually checked, especially the erroneous displays on pages 8--9. The context and disclosure on pages 1--5 were read; the references on page 15 were read. Theorems 1.3--1.4 and their proofs are outside this audit's acceptance scope.
2. Walter K. Hayman and Eleanor F. Lingham, *Research Problems in Function Theory (New Edition)*, [arXiv:1809.07200v2](https://arxiv.org/abs/1809.07200v2), 21 September 2018. Problem 7.27 is on PDF page 169, printed page 168; that passage was read and visually checked. The retained PDF is 1706228 bytes, SHA-256 8e28fd4403a07e4e19a9816b7efaafddf9f475d59cf8c34a8255cb03833ed4f0. Its historical no-progress update is not treated as a present-day worldwide status statement.

The public arXiv abstract checked on 11 October 2026 lists only v1 for MacMahon and no journal reference. This establishes the displayed version history, not absence of unpublished review. Pages 4--5 disclose LLM contributions and author corrections. That disclosure neither proves nor refutes a mathematical claim; all acceptance here rests on the reconstruction below. A fresh version-specific PDF request returned a cache miss; the audit instead used the authenticated complete retained PDF. No source-author program was executed.

## Correction ledger

### C1. Page 8: wrong Taylor sign

For displacement -s the correct first-order Taylor remainder is

\[
 B(a-s)-B(a)+sB'(a),
\]

not the expression with minus sB'(a) printed in the pointwise bound. Its integral can use either sign for the linear term because the Gaussian is even, but its pointwise Taylor estimate cannot.

This is a genuine error, even within the class arising in the proof. On S = {|Im w| < 1}, take psi(w) = exp((1+i)w). If its values agree then w_1-w_2 = pi k(1+i); since the imaginary parts differ by less than 2 and pi > 2, k = 0. Thus psi is univalent on S. One logarithm of psi' has B(x) = pi/4+x. The printed remainder at a = 0 and s = 1 has modulus 2, while the printed right side is zero. The corrected remainder vanishes, as it should. This counterexample concerns the printed intermediate inequality, not Theorem 1.2.

### C2. Page 8: Taylor remainder needs an interval bound

Even after correcting the sign, Taylor's theorem does not generally bound the remainder using only |B''(a)|. Use the integral remainder, or the supremum of |B''| on the interval between a and a-s. Lemma 3.3 supplies the needed global bound 16, giving a valid upper bound 8s^2.

### C3. Page 8: Gaussian second moment

For the displayed normalized Gaussian of variance sigma^2,

\[
 \int_{\mathbb R}8s^2 k_\sigma(s)\,ds=8\sigma^2,
\]

not 4sigma^2. The choice sigma = 1/3 still works: 8/9 < 1 < pi/3. Therefore the final cone estimate, the strip-bound constant lambda, and c_0 survive unchanged. No narrowing of the theorem's domain or pair quantifiers is needed.

### C4. Page 9: false equality for the imaginary part of the kernel

The modulus of the imaginary part of a complex exponential is not its full modulus. The displayed equality at the top of page 9 fails already at b = 0, when the left side is zero and the claimed right side is positive. Replace it by

\[
 |\operatorname{Im} k_\sigma(s+ib)|\leq |k_\sigma(s+ib)|
 =\frac{1}{\sigma\sqrt{2\pi}}e^{(b^2-s^2)/(2\sigma^2)}
 \leq e^{1/(2\sigma^2)}k_\sigma(s).
\]

This is exactly the inequality required in the rest of the calculation.

### C5. Domain and normalization details omitted in the manuscript

The Riemann-map argument requires a proper simply connected domain and distinct points. Deal with Omega = C and p = q separately, and construct the two-point strip normalization explicitly as below. Existence of the logarithm of psi', a primitive on S, and differentiation under the Gaussian integral also need their standard hypotheses verified. The reconstruction does so.

### C6. Labels and adjacent theorem

The completion paragraphs on pages 7 and 10 say Theorem 1.1 where the immediate proof is Theorem 1.2. This is a labeling slip. In the page-5 deduction of Theorem 1.1, uniform boundedness yields an unbounded sequence of values, not necessarily divergence along the entire prescribed sequence. Passing to a subsequence repairs that deduction. The metric proof does not depend on that deduction, or on later Rubel(k) claims.

## Complete corrected proof

### 1. Basic facts and the upper bound

Every connected open subset of the plane is polygonally connected. One proof is to fix p and consider the set of points reachable by a finite polygonal path in the domain: this set and its complement are relatively open, by adjoining a small ball around any point. Connectedness makes the reachable set the whole domain. Consequently d_Omega(p,q) is finite for every pair. For any rectifiable curve gamma from p to q, parametrized by arc length, and any admissible f, the chain rule for an absolutely continuous parametrization gives

\[
 |f(q)-f(p)|\leq\int_\gamma |f'(z)|\,|dz|\leq\ell(\gamma).
\]

The image of a finite-length parametrized curve is compact inside the domain, so the needed smoothness and local derivative bounds for the chain rule hold. Taking the infimum over curves and then the supremum over f proves rho <= d on every planar domain, without simple connectedness.

The admissible function f(z) = z gives rho >= |p-q|. Hence rho is a genuine finite metric: symmetry and the triangle inequality follow directly by applying them to each f and taking the supremum, and separation follows from f(z) = z. No attainment of the supremum is assumed.

If p = q, both quantities vanish. If Omega = C, the straight segment lies in Omega, so d = |p-q| and rho = d by the preceding bounds. These settle the exceptional cases.

### 2. Strip coordinates for a proper simply connected domain

Assume Omega is proper and p != q. The Riemann mapping theorem and disk automorphisms provide a biholomorphism phi: D -> Omega with phi(0) = p and phi(r) = q for a real number r in (0,1): first move the preimage of p to zero and then rotate the nonzero preimage of q to the positive real axis.

Let

\[
 S=\{w:|\operatorname{Im}w|<1\},\quad
 T(w)=\tanh(\pi w/4),\quad
 \psi=\phi\circ T,
 \qquad a=0,\quad b=\frac{4}{\pi}\operatorname{artanh}r.
\]

T maps S biholomorphically onto D. Its inverse is (2/pi) log((1+z)/(1-z)), with the logarithm on the right half-plane; its imaginary part lies between -1 and 1. Therefore psi(a) = p, psi(b) = q, and a < b are finite. No extension to the boundary is being used. The image of [a,b] is a smooth compact curve in Omega and

\[
 L:=\int_a^b|\psi'(x)|\,dx\geq d_\Omega(p,q).
\]

Only this elementary lower bound on L is needed. The Gehring--Hayman theorem, mentioned in the manuscript's introduction, is not a dependency of this proof.

### 3. Logarithmic derivative estimates with all scale factors

A univalent holomorphic function has nonzero derivative. Since S is simply connected, psi' has a holomorphic logarithm g, with g = A+iB. Its restriction B(x) to the real line is real-valued and smooth.

The normalized second-coefficient estimate for a univalent disk function u(z) = z+a_2 z^2+... is |a_2| <= 2. A derivation is supplied in the appendix. Applying it to

\[
 u(\zeta)=\frac{\psi(w+R\zeta)-\psi(w)}{R\psi'(w)}
\]

on the unit disk whenever D(w,R) is contained in S gives

\[
 |g'(w)|=|\psi''(w)/\psi'(w)|\leq 4/R.
\]

For real x, take R = 1 to get |g'(x)| <= 4. For |Im w| <= 1/2, take R = 1/2 to get |g'(w)| <= 8. The open disks remain contained in S even at equality of these center bounds. Applying Cauchy's derivative estimate to g' on the circle |z-x| = 1/2 gives |g''(x)| <= 8/(1/2) = 16. Consequently

\[
 |B'(x)|\leq4,\quad |B''(x)|\leq16,\quad
 |B(x)-B(y)|\leq4|x-y|,\quad |B(x)|\leq|B(0)|+4|x|.
\]

The value B(0) need not have a universal bound. The following imaginary-part estimate cancels it, so it never enters lambda.

### 4. Entire Gaussian approximation

Fix sigma = 1/3, and define

\[
 k_\sigma(z)=\frac{1}{\sigma\sqrt{2\pi}}e^{-z^2/(2\sigma^2)},
 \qquad G(w)=\int_{\mathbb R} B(x) k_\sigma(w-x)\,dx.
\]

This integral defines an entire function. Indeed, on a compact set |Re w|, |Im w| <= R, the modulus of the kernel is bounded by a constant depending on R and sigma times exp(-x^2/(4sigma^2)), using (x-Re w)^2 >= x^2/2-R^2. Every fixed-order derivative in w has an additional polynomial factor in w-x. Multiplication by |B(x)| <= |B(0)|+4|x| still yields an integrable compact-uniform majorant. Dominated differentiation gives all holomorphic derivatives. This proves directly the only parameter-integral fact needed; Mattner's general theorem, cited in the manuscript, is not an unchecked dependency here.

G(a) is real for real a. The real Gaussian has moments integral k = 1, integral s k = 0, and integral s^2 k = sigma^2. The second identity is oddness; the third follows by integration by parts from k'(s) = -s k(s)/sigma^2. The integral Taylor remainder gives

\[
 B(a-s)=B(a)-sB'(a)+s^2\int_0^1(1-t)B''(a-ts)\,dt.
\]

Therefore

\[
 |G(a)-B(a)|
 =\left|\int_{\mathbb R}[B(a-s)-B(a)+sB'(a)]k_\sigma(s)\,ds\right|
 \leq 8\int_{\mathbb R}s^2 k_\sigma(s)\,ds
 =\frac89<1<\frac\pi3.
\]

This is the corrected approximation estimate.

### 5. Uniform imaginary-part bound throughout the strip

For real v put J(v) = integral over R of k_sigma(s+iv) ds. Compact-uniform domination justifies differentiation with respect to v; hence

\[
 J'(v)=i\int_{\mathbb R}k_\sigma'(s+iv)\,ds=0.
\]

The last equality follows from the fundamental theorem of calculus on finite intervals and the Gaussian decay at both ends. Thus J(v) = J(0) = 1, and the integral of Im k_sigma(s+iv) is zero. For w = a+iv in S, change variables x = a-s and subtract the real constant B(a):

\[
 |\operatorname{Im}G(a+iv)|
 \leq\int_{\mathbb R}|B(a-s)-B(a)|\,|\operatorname{Im}k_\sigma(s+iv)|\,ds
 \leq4e^{1/(2\sigma^2)}\int_{\mathbb R}|s|k_\sigma(s)\,ds.
\]

The first absolute moment is

\[
 \int_{\mathbb R}|s|k_\sigma(s)\,ds
 =\frac{2}{\sigma\sqrt{2\pi}}\int_0^\infty s e^{-s^2/(2\sigma^2)}\,ds
 =\frac{2\sigma}{\sqrt{2\pi}}.
\]

It follows that everywhere in S,

\[
 |\operatorname{Im}G(w)|\leq\lambda,
 \qquad\lambda=\frac{8\sigma}{\sqrt{2\pi}}e^{1/(2\sigma^2)}
 =\frac{8}{3\sqrt{2\pi}}e^{9/2}.
\]

No parameter in this bound depends on Omega, p, q, phi, b-a, or the branch value B(0).

### 6. Constructing the admissible function and obtaining the lower bound

Define on S

\[
 h(w)=\psi'(w)e^{-\lambda-iG(w)},\qquad
 F(w)=\int_a^w h(\zeta)\,d\zeta,\qquad
 f=F\circ\psi^{-1}.
\]

The primitive F is well defined and holomorphic because S is simply connected and h is holomorphic. Thus f is holomorphic on Omega. The inverse-function and chain rules give

\[
 f'(\psi(w))=e^{-\lambda-iG(w)},\qquad
 |f'(\psi(w))|=e^{-\lambda+\operatorname{Im}G(w)}\leq1.
\]

The sign in this exponential is important: the modulus of exp(-iG) is exp(Im G). On the real axis, psi'(x) = |psi'(x)| exp(iB(x)) and G(x) is real. Hence

\[
 \operatorname{Re}h(x)
 =e^{-\lambda}|\psi'(x)|\cos(B(x)-G(x))
 \geq\frac12 e^{-\lambda}|\psi'(x)|\geq0,
\]

because |B-G| <= 8/9 < pi/3. Integration now yields

\[
 \rho_\Omega(p,q)\geq |f(q)-f(p)|
 =\left|\int_a^b h(x)\,dx\right|
 \geq\operatorname{Re}\int_a^b h(x)\,dx
 \geq\frac12e^{-\lambda}\int_a^b|\psi'(x)|\,dx
 \geq c_0d_\Omega(p,q).
\]

This completes the theorem. Using cos(8/9) instead of 1/2 would give a slightly larger valid constant, but is unnecessary and is not a sharp-constant claim.

## Appendix: the only univalence coefficient estimate used

For completeness, the coefficient bound |a_2| <= 2 follows from a short area calculation. Let u be univalent on D with u(z) = z+a_2 z^2+.... The function u(z^2)/z^2 is holomorphic and nowhere zero on D, with value 1 at zero. Choose its square root there, and put v(z) = z sqrt(u(z^2)/z^2). Then v is odd, v(z)^2 = u(z^2), and v(z) = z+(a_2/2)z^3+.... If v(z_1) = v(z_2), injectivity of u gives z_1^2 = z_2^2. The opposite-sign case, together with oddness, forces v(z_1) = 0, hence z_1 = z_2 = 0. Thus v is univalent.

The exterior function H(z) = 1/v(1/z), |z| > 1, is univalent and has Laurent expansion z-(a_2/2)z^-1+.... More generally, for a univalent exterior function H(z) = z+b_0+sum_{n>=1} b_n z^-n, the image of |z| = r, r > 1, is an analytic Jordan curve. Its bounded complementary region has nonnegative area. The image of the exterior is the unbounded component, so the curve, traced with z counterclockwise, has positive orientation around that bounded region. Green's formula and the uniformly convergent Laurent series and derivative on that circle give its area as

\[
 \frac{1}{2i}\int_{|z|=r}\overline{H(z)}H'(z)\,dz
 =\pi\left(r^2-\sum_{n\geq1}n|b_n|^2r^{-2n}\right)\geq0.
\]

Consequently, for every finite N, sum_{n=1}^N n|b_n|^2 r^-2n <= r^2. Let r decrease to 1 and then N increase to infinity. This proves the area-theorem bound sum n|b_n|^2 <= 1, in particular |b_1| <= 1. Applying this to H above yields |a_2|/2 <= 1. This derivation uses only univalence, elementary holomorphic-function facts, the Jordan-curve area formula, and convergent Laurent series; no unspecified numerical distortion constant is imported.

## Domain edge cases and dependency summary

- Unbounded proper domains, domains with arbitrarily irregular boundary, infinite inner diameter, and nonrectifiable boundaries are permitted. All integrations relevant to the pair use interior compact arcs. The bound is pairwise, so infinite diameter causes no infinite-valued pair distance.
- No Jordan-boundary extension, bounded-domain assumption, geodesic-length upper bound, or finite diameter is used.
- The logarithm and the primitive exist because the strip is simply connected. A change of logarithm adds a constant multiple of 2pi to B and G and leaves the phase difference and the construction unchanged.
- The essential general theorems are the Riemann mapping theorem, elementary disk automorphisms, existence of holomorphic logarithms and primitives on simply connected domains, Cauchy estimates, and dominated differentiation. The coefficient estimate and the Gaussian-integral use are reconstructed above. Gehring--Hayman, Banach--Steinhaus, Whitney, and all later sections of the manuscript are not dependencies of Theorem 1.2.
- For convex domains the simple segment argument gives rho = d = |p-q|. The original source's comment about nonconvexity must not be read as strict inequality for every pair in every nonconvex domain. This audit does not offer an equality characterization.

## Consequence that can also be justified directly

Theorem 1.1, limited to the existence of an unbounded holomorphic function with bounded derivative on a simply connected domain, follows from the comparison. Fix p and let E_p consist of holomorphic f with f(p) = 0 and finite sup |f'|, normed by that supremum. Differentiation is an isometric bijection from E_p onto H-infinity(Omega), because every bounded holomorphic function on a simply connected domain has a primitive normalized at p. Thus E_p is Banach. Point evaluation at q is bounded with norm rho(p,q), by the upper bound and translation invariance of the admissible class.

If the inner diameter is infinite, distances from p are unbounded (otherwise the triangle inequality would bound the diameter). Choose q_n with d(p,q_n) tending to infinity. The lower estimate makes the norms of the evaluation functionals unbounded. Uniform boundedness gives f in E_p whose evaluation values are unbounded. Select a subsequence on which their moduli tend to infinity. Conversely, if f is unbounded and has bounded derivative M, then M > 0 and |f(q)-f(p)| <= M d(p,q); this forces infinite inner diameter. The whole-plane case is immediate from f(z) = z. This consequence does not certify the manuscript's stronger claims involving simultaneous growth of higher derivatives.

## Verification limits

The proof is a human-readable mathematical reconstruction, not a machine-checked formalization. The original audit programs, which are not distributed in this prose edition, independently verify source and packet integrity, exact rational scalar arithmetic and error witnesses, and the stated decimal calculations. They cannot prove an assertion quantified over all planar domains by finite sampling. Normal, -O, and -OO executions and tamper controls protect the validation mechanism against disabled assertions and common integrity failures; they are not substitutes for the proof above.
