# PDE and compact-support adversarial reconstruction of PR1274

**Verdict: mathematical PASS.** The displayed witnesses disprove both the full bounded-output assertion and the common polynomial norm bound in the original Problem 7.72. I found no mathematical obstruction, missing boundary measure, point mass, or holomorphic correction. This verdict concerns validity under the printed conventions. Historical priority and publication readiness are outside this family's remit.

## Independence, inputs, and exact target

This is an informed adversarial verification, not blind discovery. The agent was spawned with `fork_turns=all`: its inherited parent history already contained the candidate proof and an earlier source-only family's status message giving the same witnesses. I subsequently read the submitted `PROOF.md`, root `ROOT_MATH_REVIEW.md`, and original-problem JSON. I have not read other reviewers' files from disk. The input receipt identifies the exact bytes read. The mechanism below is materially distinct from the candidate's direct angular evaluation of the Cauchy integral: it constructs compactly supported weak primitives, proves analytic-L1 annihilation by dilated tests, and uses distributional convolution calculus to identify the transform. It shares the proposed witnesses and elementary kernel identity with the candidate; those are disclosed dependencies, not independent discoveries.

I freshly retrieved [the versioned original manuscript](https://arxiv.org/pdf/1809.07200v2), receiving HTTP 200, 1,706,228 bytes, SHA256 `8e28fd4403a07e4e19a9816b7efaafddf9f475d59cf8c34a8255cb03833ed4f0`. I rendered and visually inspected complete PDF page 184, printed page 183. The source has a **bilinear**, unconjugated pairing against all holomorphic area-L1 tests and the kernel `-1/(pi (z-zeta)^2)`. It asks both the full annihilator question and the polynomial subquestion. `SOURCE_RECEIPT.json` binds the private source and rendered image. The historical update on that page does not establish the question's present priority status; no priority inference is made here.

Let D be the open unit disc, let dA be unnormalized planar area, and let N be the prescribed bilinear annihilator. Extend inputs by zero. The exact hypotheses to test are m a positive integer and

\[
P_m(t)=\sum_{j=0}^{m-1}(1-t)^j,\quad
v_m(z)=z^2P_m(|z|^2),\quad H_m=\sum_{k=1}^m1/k,
\]

and the separate bounded input v(z)=z/bar(z) for z nonzero, with arbitrary assigned value at zero. The claims are v_m in N intersect C[z,bar(z)], norm(v_m)=1, norm(Bv_m)=H_m; and v in N, norm(v)=1, Bv=1+log|z|^2 in the punctured disc. Norms are essential suprema. The goal is a full negative answer to each universal assertion, not an unbounded transform of a single polynomial.

## 1. A primitive lemma that handles every analytic L1 test

Suppose u is a compactly supported W^{1,1}(C) function supported in the closed disc and its weak derivative f=barpartial u is a bounded density supported there. Then f restricted to D belongs to N.

To prove this, first let phi be holomorphic on a neighborhood of the closed disc. Choose a smooth compactly supported cutoff chi equal to 1 on a neighborhood of that disc, with support inside the domain of phi. Bilinear distributional integration by parts gives

\[
\int_D f\phi\,dA
=\langle\bar\partial u,\chi\phi\rangle
=-\int_{\mathbb C}u\,\bar\partial(\chi\phi)\,dA=0.
\]

There is no conjugation in this identity. Now take an arbitrary holomorphic phi in L1(D), and put phi_r(z)=phi(rz), 0<r<1. These are holomorphic on neighborhoods of the closed disc. Moreover phi_r converges to phi in L1(D). Here is an endpoint proof avoiding any assumed dual-space density theorem: choose R0<1 so the integral of |phi| on |z|>R0 is less than epsilon, then choose R with R0<R<1. For r sufficiently close to 1, rR>R0 and r>1/2, so

\[
\int_{|z|>R}|\phi(rz)|\,dA(z)
\le r^{-2}\int_{|w|>R_0}|\phi(w)|\,dA(w)<4\epsilon.
\]

The tail of phi itself is less than epsilon, and phi_r converges uniformly on |z|<=R. This proves L1 convergence by splitting into the compact disc and the tail. Since f is bounded, the integrals against f converge, and all equal zero. This establishes the full required N membership, rather than just its monomial moments.

This lemma uses the zero extension of u and its global weak derivative. A nonzero boundary trace would invalidate that premise; that issue is checked explicitly below.

## 2. The operator identity fixes the global solution

Use partial=(partial_x-i partial_y)/2 and barpartial=(partial_x+i partial_y)/2. The locally integrable distribution E(z)=1/(pi z) satisfies

\[
\bar\partial E=\delta_0,\qquad
\partial E=-\frac1\pi\operatorname{pv}\frac1{z^2}=:T.
\]

For completeness, integrate against a smooth compactly supported test psi on the complement of a radius-epsilon disc. Green's identity for barpartial turns the inner clockwise boundary into `(1/(2pi)) integral psi(epsilon exp(i theta)) dtheta` in the pairing for barpartial E; its limit is psi(0). In the partial calculation the corresponding boundary average has the factor exp(-2i theta), so it tends to zero. The remaining term is `-1/pi integral psi(z)/z^2 dA` with a circular hole. Its principal value exists because the angular integral of the constant psi(0) vanishes, while `(psi(z)-psi(0))/z^2` is locally integrable in absolute value. Thus the second identity has no delta term, and its minus sign agrees with the source.

For compactly supported u as in Section 1, convolution with its distributional derivative is defined. Differentiation may be transferred between convolution factors because u has compact support. Consequently

\[
E*f=E*(\bar\partial u)=(\bar\partial E)*u=u,
\qquad T*f=\partial(E*f)=\partial u.
\tag{A}
\]

This is an equality on the whole plane. There is no arbitrary holomorphic summand: (A) is a convolution identity with the specified fundamental solution. In particular, no local solution of the PDE is being silently substituted for the actual global operator.

For bounded compactly supported f, E*f is also the usual absolutely convergent Cauchy integral. To connect T*f to the source's pointwise principal value wherever f is C1 locally, split the kernel using a smooth radial cutoff centered at the evaluation point and subtract f(z) in the near part. The radial constant contributes zero angular mean. The remaining local integrand is bounded by a constant times 1/|w|, because |f(z-w)-f(z)|<=C|w|. The truncated local integrals therefore converge uniformly on smaller neighborhoods (the omitted integral is O(epsilon)); the far integral is continuous. This principal-value representative equals the distribution T*f on that neighborhood. Hence it agrees pointwise there with a continuous formula for partial u. No global C1 assumption on the zero-extended input, and no L-infinity boundedness theorem for B, is used.

## 3. Polynomial family from a zero-trace PDE solution

Instead of evaluating any singular integral, solve the simple primitive equation directly. Set

\[
F_m(t)=-\sum_{k=1}^m\frac{(1-t)^k}{k},\qquad
u_m(z)=\begin{cases}zF_m(|z|^2),&|z|<1,\\0,&|z|\ge1.\end{cases}
\]

F_m'(t)=P_m(t) and F_m(1)=0. Inside D, ordinary Wirtinger differentiation gives

\[
\bar\partial u_m=z^2P_m(t)=v_m,\qquad
\partial u_m=F_m(t)+tP_m(t)=:G_m(t),\quad t=|z|^2.
\]

These are also global weak derivatives after zero extension. To see this directly, perform integration by parts on epsilon<|z|<1. The outer term vanishes exactly because u_m has zero boundary trace. At the inner boundary |u_m|=O(epsilon), so its boundary integral is O(epsilon^2) and tends to zero. Both proposed derivatives are bounded in the disc. Thus u_m is globally W^{1,infinity}, and neither first derivative has a boundary or point measure. Jumps of the derivatives at the unit circle are not jumps of u_m; they do not produce measures in these first derivatives. Section 1 gives v_m in N, and (A) identifies Bv_m=G_m(|z|^2) in D. All interior points, including the origin, are covered by the local C1 principal-value argument.

The finite geometric identity is

\[
a_m(t):=tP_m(t)=1-(1-t)^m.
\]

For 0<t<1 this is in (0,1), approaches 1 at the outer edge, and exceeds any fixed level below 1 on a positive-area outer annulus. Therefore the essential input norm is exactly 1. Each v_m is a finite polynomial in z and bar(z), with no division at the origin.

For the output,

\[
G_m(t)=1-(1-t)^m-\sum_{k=1}^m\frac{(1-t)^k}{k},\quad
G_m(0)=-H_m,\quad G_m(1)=1,
\]

and

\[
0<G_m'(t)=P_m(t)+m(1-t)^{m-1}\le2m\quad(0<t<1).
\]

Since H_m>=1, this gives |G_m|<=H_m. The lower bound is not inferred from a single point value. For any 0<eta<H_m, set delta=min(eta/(4m),1/2). Throughout 0<t<delta,

\[
G_m(t)\le-H_m+2mt<-H_m+\eta,
\]

so |Bv_m|>H_m-eta on a disc of positive area pi delta. The essential norm is therefore precisely H_m. At m=1 the formula is G_1(t)=2t-1, with input v_1=z^2 and output norm 1, a useful sign and endpoint check. The excluded parameter m=0 supplies no counterexample and is never used.

Finally H_m diverges. For instance each dyadic block from 2^{j-1}+1 through 2^j contributes at least 1/2, giving H_{2^k}>=1+k/2. Thus no finite common polynomial norm constant exists.

## 4. The logarithmic primitive and the single bounded counterexample

Define u(z)=z log|z|^2 inside the punctured disc, and set u=0 at the origin and outside D. It is continuous: r|log r| tends to zero at the origin, and log|z|^2 vanishes on the unit circle. Inside the punctured disc,

\[
\bar\partial u=z/\bar z=:v,\qquad
\partial u=1+\log|z|^2=:g.
\]

These are the global weak first derivatives after zero extension. The same annular integration by parts has an identically zero outer boundary term. At the inner circle the absolute error is bounded by a test-dependent constant times

\[
\epsilon\sup_{|z|=\epsilon}|u(z)|
=2\epsilon^2|\log\epsilon|\longrightarrow0.
\]

The derivative densities are integrable. In fact the substitution s=-log r gives the finite integral `integral_0^1 r |log r|^p dr` for every finite p>=1, so u is W^{1,p}(C) for every such p. No delta at zero and no measure on the unit circle is omitted. Section 1 proves that v belongs to N with every analytic L1 test; its essential norm is exactly 1.

Equation (A) now identifies Bv=g as a distribution. The local C1 principal-value argument applies to every nonzero point of D, where v is smooth. Hence

\[
Bv(z)=1+\log|z|^2\quad(0<|z|<1)
\]

as the actual pointwise principal value. For every M>=1, the set where |Bv|>M is exactly, up to null endpoints, `0<|z|^2<exp(-M-1)`, and its area is pi exp(-M-1)>0. Thus the transform is essentially unbounded. At zero itself the radius-epsilon truncated integral is 2 log epsilon, which diverges negatively. That exceptional point is neither needed nor misrepresented as a finite principal value.

Outside the closed disc the input is locally smooth and zero, so (A) and the same principal-value identification give Bv=0 pointwise there. The analogous statement holds for each v_m. Thus both a disc-output norm and a whole-plane-output norm give the stated conclusions. No assertion concerning the circle's pointwise values is needed.

## 5. Independent finite weak tests and operator consistency

`check_pde.py` uses exact rational bivariate polynomials in z and w=bar(z), with formal Wirtinger derivatives and the independent area formula

\[
\pi^{-1}\int_Dz^p\bar z^q\,dA=
\begin{cases}1/(p+1),&p=q,\\0,&p\ne q.\end{cases}
\]

For m=1 through 32 it constructs u_m from its zero-trace primitive and constructs v_m independently from the finite geometric sum. It checks their derivative identity, outer trace, the interior compatibility barpartial(partial u_m)=partial(v_m), exact output endpoints, and 5,184 weak Stokes identities against z^p bar(z)^q for 0<=p,q<=8. It separately checks 4,128 analytic monomial moments, 32 rational positive-area thresholds, and 32 exact whole-plane L2 consistency identities

\[
\pi^{-1}\|v_m\|_2^2=\pi^{-1}\|Bv_m\|_2^2
=1-\frac2{m+1}+\frac1{2m+1}.
\]

For the logarithmic primitive the three exact normalized moments used are

\[
\int_Du z^p\bar z^q\,dA/\pi=
\begin{cases}-1/(q+1)^2,&q=p+1,\\0,&\text{otherwise},\end{cases}
\]

\[
\int_Dv z^p\bar z^q\,dA/\pi=
\begin{cases}1/q,&q=p+2,\\0,&\text{otherwise},\end{cases}\quad
\int_Dg z^p\bar z^q\,dA/\pi=
\begin{cases}p/(p+1)^2,&p=q,\\0,&\text{otherwise}.\end{cases}
\]

They follow by elementary angular integration of polynomial **test moments**, not evaluation of a Cauchy or principal-value integral, and by `integral_0^1 t^q log(t) dt=-1/(q+1)^2`. They give a second exact check of the absence of hidden weak terms: `integral v psi=-integral u barpartial psi` and `integral g psi=-integral u partial psi`. The checker evaluates 33,282 such identities for 0<=p,q<=128. These finite checks supplement the annular all-test-function proof in Section 4; they do not claim that finitely many moments prove a distribution identity.

An optional Fourier consistency check explains the L2 equality without an L-infinity assumption. Global weak derivatives have multipliers `(i xi_1-xi_2)/2` for barpartial and `(i xi_1+xi_2)/2` for partial. Their ratio away from the zero frequency is `(xi_1-i xi_2)/(xi_1+i xi_2)`, of absolute value one. Since f and partial u are in L2, Plancherel gives equal L2 norms, with the single zero frequency immaterial. For the logarithmic example, `integral_0^1 (1+log t)^2 dt=1`, agreeing with |v|=1. This is a consistency test, not a substitute for the direct kernel and weak-derivative argument.

All checker conditions use explicit exceptions, with six negative controls: four invalid parameters and two deliberately perturbed constant input coefficients must be rejected/detected. Runs under normal Python, `-O`, and `-OO` all passed. The three JSON results are identical after removing only the declared optimization field; this is checked when sealing.

## 6. Adversarial issues and exact remaining scope

- **Conjugate pairing:** the proof uses the printed bilinear pairing. The distributional test argument makes this explicit.
- **All area-L1 analytic tests:** dilated tests and a proved endpoint L1 limit cover them all; no unproved endpoint dual density is invoked.
- **Boundary mass:** the primitives have zero trace; the boundary calculation is explicit. The zero-extended inputs themselves jump, which is allowed and does not invalidate the first-derivative identity for u.
- **Origin mass:** the actual primitive boundary error is O(epsilon^2 |log epsilon|), tending to zero. The relevant identity is a first derivative of z log|z|^2, not the Laplacian of log|z|; borrowing the latter's delta term would be incorrect.
- **Holomorphic ambiguity:** the full-plane compact-support convolution identity (A) fixes the exact primitive and transform globally.
- **Principal value:** it exists at every smooth interior point of each input. The one singular origin for v has a divergent PV and is explicitly excluded from its pointwise formula.
- **Essential norms:** lower bounds use positive-area discs or annuli; no isolated value is mistaken for an essential norm.
- **Uniform polynomial claim:** every individual polynomial has bounded transform, while H_m is unbounded over the family. This is precisely the weaker universal bound's failure.
- **Imported analytic facts:** elementary Green integration, distributional differentiation/convolution with a compactly supported factor, and basic local integrability suffice for the central proof. The only extra Fourier theorem, Plancherel, is optional consistency evidence.

There is no unresolved mathematical gap in these two counterexamples. This family has not investigated whether these witnesses or conclusions have appeared previously, and it makes no novelty, firstness, or current-openness assertion. An extensive independent priority audit remains required before publication.
