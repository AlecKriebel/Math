# Verified connected quotient example; prior ingredients credited

This scientific disposition concerns PR73 / 2985 / K3 Problem 4.109,
reviewed at submitted head `6f82e81631fd43abc0140a831acfb43c150f4210`.
The separate acceptance record and operational receipts establish any
actual merge and native import. The original candidate, source wrapper,
readiness file and one-turn ledger remain dated inputs; this document
does not reconstruct historical workflow transitions.

The submitted mathematical theorem is valid. There is a closed connected
symplectic four-manifold $(X,\Omega)$ containing a connected embedded
symplectic surface $\Sigma$ of genus three, with
$\operatorname{PD}[\Sigma]=[\Omega]$ and $\Sigma^2=4$, whose complement admits
no Weinstein structure for any symplectic form. The integral divisor class
lifting $[\Omega]$ is primitive. Its connected double cover has
$H_3\cong\mathbb Z$, whereas the ordinary third homology of the base
complement is zero. The obstruction is therefore visible in the cover.

The construction starts from Auroux's disconnected torus example, explicitly
proved by Giroux, Proposition 9. It adds a free component-exchanging quotient
and checks the descended class and covering obstruction. We accept it as a
verified, attributed partial research record. We do not claim an established
novel resolution or a first connected four-dimensional counterexample. The historical priority of that connected extension remains unestablished
after the bounded audit. The disconnected-surface version already has a
prior negative answer; whether the source question tacitly intends a
connected surface is an interpretive issue. Current status `partial`
records this incomplete novelty/target-priority determination, although
the mathematical connected theorem is completely verified. It does not
mark that theorem partly proved or declare the intended original question
historically resolved. See CURRENT_PRIORITY.md.

## Checkable construction and obstruction

On $T^4=\mathbb R^4/\mathbb Z^4$, put
$\omega_0=dx_1\wedge dx_2+dx_3\wedge dx_4$. The affine tori

\[
A=\{x_1=0,\ x_2-x_3=0\},\qquad
B=\{x_2+x_3=1/4,\ x_4=1/4\}
\]

meet at two positive nodes. The free symplectic involution

\[
\tau(x_1,x_2,x_3,x_4)=(x_1+1/2,x_2,-x_3,-x_4)
\]

takes their union to a disjoint nodal union. Smoothing in a sufficiently
small neighborhood gives a genus-three surface $S$ disjoint from
$S'=\tau S$. The source's general assertion about arbitrary unequal
translation parameters is unnecessary: these specific offsets make every
cross-pair disjoint, as the submitted candidate checks directly.

For $e_i=dx_i$, the integral classes are

\[
\alpha=e_1\wedge(e_2-e_3)+(e_2+e_3)\wedge e_4,\qquad
\beta=e_1\wedge(e_2+e_3)+(e_3-e_2)\wedge e_4.
\]

They satisfy $\alpha+\beta=2[\omega_0]$,
$\alpha^2=\beta^2=4$ and $\alpha\beta=0$. In local normal coordinates at
each node, $\alpha$ is standard symplectic and
$\beta=\operatorname{Re}(dz\wedge dw)$. The smoothing uses a central
annulus $zw=\varepsilon$ and cutoff arms
$w=\varepsilon\chi(|z|)/z$, together with the symmetric other arm.
Choose real $\varepsilon>0$, fixed $0<a<b$ with $\varepsilon<a^2$, and
$\chi:[0,\infty)\to[0,1]$ smooth, nonincreasing, equal to one near
$[0,a]$ and zero near $[b,\infty)$, with constant seam collars.
For an arm with $r=|z|$, its $\omega_0$ area density is

\[
\frac12\left(1+\frac{\varepsilon^2\chi^2}{r^4}
-\frac{\varepsilon^2\chi\chi'}{r^3}\right)\ge\frac12,
\]

and $\beta$ restricts to zero. Thus the smoothing claim is universal for
the specified cutoff class, not inferred from sampling. The second node
uses the corresponding modular coordinate lift (the relevant constant is
$5/4$); it has the same local calculation.

Let $p:T^4\to X=T^4/\langle\tau\rangle$. The form descends to
$\bar\omega$ and put $\Omega=2\bar\omega$. The restriction of $p$ to $S$
is a diffeomorphism onto a connected embedded surface $\Sigma$.
Real finite-cover transfer gives

\[
p^*\operatorname{PD}[\Sigma]=\alpha+\beta
=2[\omega_0]=p^*[\Omega],\qquad
\operatorname{PD}[\Sigma]=[\Omega].
\]

This uses injectivity in real cohomology, not an invalid assertion that
integral pullback is injective or that torsion cancels. The actual integral
divisor class supplies an integral lift. The invariant torus
$\{x_3=x_4=0\}$ descends to a torus with $x_1$ period $1/2$ and
$\Omega$ period one, proving that lift is primitive.

The connected cover of $N=X\setminus\Sigma$ is
$\widetilde N=T^4\setminus(S\sqcup S')$. For its compact exterior $M$,
excision and the oriented Thom isomorphism identify
$H_4(T^4,M;\mathbb Z)$ with $\mathbb Z^2$. The fundamental class maps to
$(1,1)$, so exactness injects
$\mathbb Z^2/\langle(1,1)\rangle\cong\mathbb Z$ into $H_3(M;\mathbb Z)$.
A Weinstein four-manifold has a CW model of dimension at most two; the
same holds for its covers. This contradicts the cover homology. The
independent duality calculation further gives
$H_3(\widetilde N;\mathbb Z)=\mathbb Z$, with deck action $-1$, and
$H_3(N;\mathbb Z)=0$. No finite-volume/completeness convention supplies
the obstruction; it is topological.

## Scope and validation

The example answers the prescribed-surface universal assertion negatively,
including its connected interpretation. It does not decide the
$\mathbb{CP}^2$ specialization, whether a different degree-one
representative can have a Weinstein complement, or effective bounds for
choosing good higher-degree representatives.

Two fresh independent mathematical families checked the local geometry
and covering/duality topology. ROOT authenticated the submitted native
source and reproduced the original author and independent diagnostics:
13,236 and 10,403 assertions, with outputs byte-identical to their dated
receipts. Those finite controls are checks, not substitutes for the
continuous smoothing or topology proofs. Fresh priority families checked
the original question and related constructions. Final current gates must
bind their final reports and any subsequent disposition review.

Original effort remains one substantive turn out of five. New central
proof-search turns: zero. AI tools were used extensively in construction,
verification and this audit. This record has not undergone conventional
human peer review or formal proof certification. This attributed partial disposition has no paper, new DOI, Zenodo
upload or tracker row.

The full argument is retained in the [immutable submitted candidate](https://github.com/AlecKriebel/Math/blob/6f82e81631fd43abc0140a831acfb43c150f4210/unsolved_math_prioritization/attempts/2985/CANDIDATE.md).
