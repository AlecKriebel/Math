# Independent adversarial analytic audit of PR #563 / attempt 2306072

Reviewer family: global maximizer existence, area-theorem analytic estimates,
and identification of a quadratic-differential trajectory with an actual
omitted support slit. Review completed 2026-10-13 UTC. AI-authored and
unrefereed; no historical-first or priority assertion.

**Verdict: PASS within this review's mathematical scope, accepting the stated
classical theorems.** I found no fatal gap in the frozen candidate. In particular,
the proof supplies actual globally maximizing support points, and the tested
trajectory segment does belong to each maximizer's omitted slit. It does not
mistake a necessary Schiffer differential for a sufficient extremality test.

The strongest independently verified result is the candidate's stated
nonmonotonicity for every maximizer of
\[
\Re\{a_2+i10^{-24}(a_4-3a_3)\}
\]
on the normalized schlicht class. My derivation below also gives the additional
uniform orientation bound
\[
\left|\frac{tV'(t)}{V(t)}-1\right|<223\varepsilon
\quad(0<t\le7/4)
\tag{A}
\]
and an independently propagated fine bound of \(800\varepsilon\eta\) at the
sign-test interval, stronger than the author's \(2000\varepsilon\eta\).

There is one minor exposition improvement: the numerator \(7/2\) in the
reciprocal-square estimate follows from the stronger consequence
\(|H(-2/3)|<11/6\), rather than just the coarse displayed bound \(|H|<2\).
The stronger consequence is immediate from the existing estimate and parameter.
This is not a missing mathematical assumption or a failed bound.

## Independence, frozen input, and reproducibility

I read the complete frozen `original/unsolved_math_prioritization/attempts/2306072/PROOF.md`
before reading any old independent-audit conclusion. I have not read the old
`independent-audit/INDEPENDENT_AUDIT.md` or its verdict. I did subsequently inspect
the author's `verify.py` to identify its scope; it was neither imported nor run
for my independent checks. All review files are in `reviews/analytic01`.
The branch was `main`; I performed no commit, push, remote mutation, or external
communication in this subreview.

`checks.py` independently reconstructs the relevant quotient coefficients from
ordered compositions, propagates exact rational bound constants, and includes
the a3-only, a4-only, zero-perturbation, wrong-sign, and oversized-error controls.
Run from any directory:

```text
python3 /Users/alec/Documents/Math/draft_pr_claimed_solved_500_600_20261012/audits/pr563_2306072/reviews/analytic01/checks.py
```

The resulting `CHECKS.json` is finite arithmetic evidence, not a formalization
of compactness, the area theorem, the support-slit theorem, infinite series
estimates, or analytic-trajectory continuation. The mathematical derivations
below are the evidence for those connections. `MANIFEST.json` records hashes
and the frozen proof identity.

## Target and primary-source hypothesis audit

The primary target is Hayman–Lingham, *Research Problems in Function Theory*,
arXiv:1809.07200v2, printed p.143 / PDF p.144, Problem 6.72. I visually inspected
that page. It asks the two universal monotonicity questions for the analytic arc
omitted by a support point of \(S\). The candidate's continuous argument and
both radial-angle interpretations cover those questions. The historical update
on the page does not establish current novelty. [Primary target](https://arxiv.org/pdf/1809.07200v2).

I retrieved the actual Duren (1981) ETH scan and visually inspected printed
pp.352–355. The scan, including the exact displayed equations, supports these
inputs: an actual support point omits one analytic arc of increasing modulus;
equation (1) is \(\Phi(w)dw^2/w^2>0\) with
\(\Phi(w)=L(f^2/(f-w))\); \(L(f^2)\ne0\); and there is one trajectory reaching
the simple pole at infinity. Page 355 uses the outward signed radial angle
\(\arg(w'/w)\) and its limit zero at infinity. These are general support-point
facts in the source, not claims restricted to derivative evaluation.
[Duren primary scan, DOI 10.1007/BF02566218](https://www.e-periodica.ch/cntmng?pid=com-001%3A1981%3A56%3A%3A30&bot=1).

The normalized injective unit-disk hypothesis for \(|a_n|\le n\) matches the
coefficient theorem stated in de Branges (1985), p.137. I inspected the original
paper's statement through a university-hosted primary-paper copy; I did not
reprove de Branges' theorem. [de Branges original paper](https://archive.ymsc.tsinghua.edu.cn/pacm_download/117/6366-11511_2006_Article_BF02392821.pdf).

The remaining classical inputs are the area theorem for a normalized univalent
exterior map, Rouché's theorem, Schwarz's lemma, and the holomorphic inverse and
square-root theorems. Their hypotheses are checked explicitly below. No
point-evaluation-only theorem, uniqueness of a maximizing map, differentiable
maximizer selection, numerical extremal solver, or complete slit classification
is needed.

## Independent global existence and near-Koebe control

Let \(\varepsilon=10^{-24}\) and \(\eta=10^{-12}\). For each fixed \(r<1\), the
coefficient theorem gives
\[
|f(z)|\le\sum_{n\ge1}n r^n=\frac r{(1-r)^2}\quad(|z|\le r),
\]
so \(S\) is locally bounded. Montel supplies locally uniform subsequential
limits. Such a limit has derivative one at zero and hence is not constant;
Hurwitz's injective-limit alternative therefore makes it univalent. The
normalization is preserved, so \(S\) is compact. Each coefficient map is
continuous by Cauchy's formula. Consequently \(\Re L\) actually attains its
maximum. This is a maximum on all of \(S\), without a finite-dimensional
truncation or a convexity assumption.

For \(k(z)=z/(1-z)^2\), \(L(k)=2-5i\varepsilon\); for the identity map it is
zero. Thus \(\Re L\) is nonconstant on \(S\), making every maximizer a support
point to which Duren's general setup applies. For any such maximizer,
\[
\Re a_2\ge2-\varepsilon(|a_4|+3|a_3|)\ge2-13\varepsilon.
\]
Since \(|a_2|\le2\),
\[
|a_2-2|^2=|a_2|^2+4-4\Re a_2\le52\varepsilon,
\quad 0\le1-|a_2|^2/4\le13\varepsilon.
\tag{B}
\]
The lower bound zero in the last inequality is supplied by \(|a_2|\le2\), not
assumed as an independent stability condition.

Here is a direct check of the root transform. Because \(f\) has no zero except
zero, \(z/f(z)\) extends to a nonvanishing analytic function with value one at
zero. Define its normalized square root \(H\), and set
\[
g(z)=z/H(z^2).
\]
Then \(g^2(z)=f(z^2)\) and \(g\) is odd. If \(g(z_1)=g(z_2)\), squaring and
injectivity of \(f\) imply \(z_1^2=z_2^2\). The possible opposite pair has equal
odd values only at a zero of \(g\), which is zero itself. Thus \(g\) is
univalent. Its reciprocal exterior map is analytic and univalent on
\(|\zeta|>1\), with leading coefficient one:
\[
F(\zeta)=\zeta H(\zeta^{-2})
=\zeta-\frac{a_2}{2}\zeta^{-1}+\sum_{n\ge2}c_n\zeta^{1-2n}.
\]
The area theorem therefore applies with exactly the weights \(2n-1\). It gives
\[
\sum_{n\ge2}(2n-1)|c_n|^2\le1-|a_2|^2/4\le13\varepsilon.
\tag{C}
\]
Its \(\zeta^{-3}\) coefficient is
\(c_2=3a_2^2/8-a_3/2\), so
\[
|a_3-3a_2^2/4|\le2\sqrt{13\varepsilon/3}<5\eta.
\]
Using \(|a_2-2|<8\eta\) and \(|a_2+2|\le4\) gives
\(|a_3-3|<29\eta\). Hence, for the candidate's
\(A=2a_3+a_2^2-6a_2\), \(B=3a_2-3\),
\[
|A+2|<106\eta,\qquad |B-3|<24\eta.
\tag{D}
\]
All these conclusions hold for every maximizer. In particular, no selection
of coefficients from an arbitrary formally admissible region replaces the
actual maximizer.

## Independent actual-tip gate

For \(r=2/3\), Cauchy–Schwarz applied to (C) gives the candidate's uniform
\(|H-(1-z)|<5\eta\) and \(|H'+1|<10\eta\). The required infinite-series
majorants are obtained directly as
\[
\sum_{n\ge2}\frac{r^{2n}}{2n-1}
\le\frac{r^4}{3(1-r^2)}=\frac{16}{135}<\frac14,
\]
\[
\sum_{n\ge2}\frac{n^2r^{2n-2}}{2n-1}
\le\sum_{n\ge2}n r^{2n-2}
=\frac1{(1-r^2)^2}-1=\frac{56}{25}<\frac94.
\]
The second majorant uses \(n^2/(2n-1)\le n\). These are infinite tail
bounds, not estimates inferred from any finite number of coefficients.

At \(z_*=-2/3\), \(H_0=1-z_*=5/3\). The value error gives
\(3/2<|H(z_*)|<11/6\) since \(5\eta<1/6\), and hence
\(|H+H_0|<7/2\). This explains the frozen proof's stated numerator. Elementary
reciprocal identities now yield
\[
|f(z_*)-k(z_*)|<2\eta.
\]
For \(f'=(H-2z_*H')/H^3\), the numerator differs from \(1/3\) by less than
\(5\eta+(4/3)10\eta<19\eta\). The reciprocal-cube difference is bounded using
\(|H^2+HH_0+H_0^2|<11\), and the resulting derivative error is less than
\(8\eta\). These calculations remain valid for complex \(H\); they do not
assume that the maximizer has real coefficients.

I checked the potentially dangerous inequality direction independently. Choose
a disk automorphism \(\phi\) with \(\phi(0)=z_*\) and define \(h=f\circ\phi\).
If a Euclidean disk of radius \(d\) centered at \(h(0)\) is contained in
\(\Omega=f(D)\), then
\[
u(\zeta)=h^{-1}(h(0)+d\zeta)
\]
is a disk self-map fixing zero. Schwarz's lemma says
\(d/|h'(0)|\le1\), so
\[
\operatorname{dist}(f(z_*),\partial\Omega)
\le(1-|z_*|^2)|f'(z_*)|.
\]
Thus the bound is an upper bound on distance to the slit, as required. The
actual complement is closed and nonempty, so a closest finite boundary point
exists; since the complement is one analytic arc, \(\partial\Omega=\Gamma\).
With the exact Koebe values,
\[
\min_{w\in\Gamma}|w|
\le\frac6{25}+\frac59\frac9{125}
 +\left(2+\frac59\,8\right)\eta
<\frac3{10}.
\tag{E}
\]
Increasing modulus along the support arc identifies this minimum with its
finite tip. This is a genuine estimate about the actual omitted set.

## Exact differential and independent slit identification

Expanding \(-f^2/w-f^3/w^2-f^4/w^3+\cdots\) through degree four gives the
candidate's quotient coefficients. In particular,
\[
Q(w)=-a w^{-3}-b w^{-4}-c w^{-5},\quad
a=1+i\varepsilon A,\ b=i\varepsilon B,\ c=i\varepsilon.
\]
For omitted \(w\) this is the actual functional differential; the rational
formula also defines its meromorphic continuation elsewhere. One must not
evaluate an \(H(D)\) functional on a quotient having a pole in \(D\), but
coefficient extraction at zero legitimately supplies this rational
continuation. The candidate's use of that continuation does not assert
extremality of a trajectory in the range of \(f\).

The coordinate \(w=-v^{-2}\) gives exactly
\[
Q(w)dw^2=4P(v)dv^2,\quad P(v)=a-bv^2+cv^4.
\]
The minus sign in the coordinate is essential: changing the differential's
sign would make the constructed real natural-coordinate curve a negative,
rather than positive, trajectory. From (D),
\[
|P(v)-1-i\varepsilon(-2-3v^2+v^4)|\le322\varepsilon\eta,
\quad |P(v)-1|\le111\varepsilon\quad(|v|\le3).
\]
Thus \(P\) has no zero there, and its square root \(p\) close to one extends to
a neighborhood of the closed disk. The primitive \(G(v)=\int_0^v p(s)ds\) is
single-valued, odd, and satisfies \(|G(v)-v|\le333\varepsilon\). Rouché on
\(|v|=3\) supplies exactly one preimage for each \(|t|<2\), because
\(|v-t|>1>333\varepsilon\). The preimage is simple since \(G'=p\ne0\);
uniqueness patches the local holomorphic inverses to \(V\) on \(|t|<2\).
It is odd, \(V(0)=0\), and has no other zero. The curve
\[
W(t)=-V(t)^{-2},\quad 0<t\le7/4,
\]
is regular and satisfies \(Q(W)W'^2=4\). It has
\(W(t)\sim-a/t^2\) and
\[
|W(t)|>25/81>3/10.
\tag{F}
\]

Here is a direct local proof of the simple-pole identification, independent of
merely repeating the citation. In \(u=1/w\), the differential has expression
\((-a/u-b-cu)du^2\), so infinity is a simple pole because \(a\ne0\).
On its double cover \(u=-v^2\), the differential is regular at zero and its
natural coordinate is \(G\). Any positive trajectory tending to the pole
lifts to a curve with \(\Im G\) constant; its limit at zero forces that constant
to be zero. The two real natural-coordinate rays project to the same geometric
\(w\)-arc because \(V\) is odd. Thus there is one local geometric positive
trajectory ending at infinity. The actual slit and \(W\) coincide there.

For global continuation through the proposed segment, define
\[
E_\Gamma=\{t\in(0,7/4]:W(t)\in\Gamma\}.
\]
This set contains an initial interval near zero. It is relatively closed by
continuity of \(W\) and closedness of \(\Gamma\). For every member, (E)–(F)
exclude the finite tip. The point is therefore a regular interior point of the
actual analytic arc. Also \(Q\) is finite and nonzero there, since \(V(t)\ne0\)
and \(P(V(t))\ne0\). In a small neighborhood choose a square root of \(Q\);
the resulting primitive makes positive trajectories horizontal lines. Two
trajectories meeting at a regular point have the same horizontal-line germ.
Hence \(E_\Gamma\) is relatively open. Connectedness of \((0,7/4]\) makes
\(E_\Gamma\) the entire interval. This explicit open-and-closed argument
excludes departure into the conformal range, a finite-tip obstruction,
trajectory junctions, hidden critical points, and a missed sheet.

## Orientation, independent remainders, and both angles

For all \(v\) in the disk,
\(|p(v)-1|\le111\varepsilon\) and
\(|G(v)/v-1|\le111\varepsilon\), with the second quotient interpreted at zero.
Since \(t=G(V(t))\),
\[
Z(t)=\frac{tV'(t)}{V(t)}
=\frac{G(V(t))/V(t)}{p(V(t))}.
\]
Therefore
\[
|Z(t)-1|\le\frac{222\varepsilon}{1-111\varepsilon}<223\varepsilon.
\]
This proves (A) throughout \((0,7/4]\), including the difficult limit
\(t\downarrow0\) where an absolute bound on \(|V-t|\) alone would be
insufficient. It implies \(\Re Z>0\),
\(d\log|W|/dt=-2\Re Z/t<0\), and a single small signed-angle branch.
Consequently increasing \(t\) moves inward, and \(-W'\) is the outward tangent.
Also \(\Phi(W)=t^2/Z^2\), so the constructed segment directly satisfies the
positive-real-part accessibility condition. This consistency check is not
being used as a sufficient extremality criterion.

For the fine expansion, integrate the first-order square-root term to obtain
\[
G(v)=v-i\varepsilon d(v)+R(v),\quad
d(v)=v+v^3/2-v^5/10.
\]
The exact square-root remainder identity gives an error coefficient
\[
C_p=161+\tfrac12 111^2\eta<162
\]
in units \(\varepsilon\eta\). Since \(|d'|\le55\) on \(|v|\le3\) and
\(|V-t|\le333\varepsilon\), inversion gives
\[
|V-t-i\varepsilon d(t)|\le C_V\varepsilon\eta,
\quad C_V=3C_p+55\cdot333\eta<487.
\]
Complex Taylor's integral remainder on \(|x|\le1/4\) bounds
\((1+x)^{-1/2}-1+x/2\) by \(2|x|^2\); for example its coefficient is at most
\((3/8)(4/3)^3=8/9<2\). This does not use a real-variable-only Taylor bound.
The composition error uses \(|P_0'|\le126\), giving
\[
|V'-1-i\varepsilon d'(t)|\le C_{V'}\varepsilon\eta,
\quad C_{V'}=161+(126\cdot333/2+2\cdot111^2)\eta<162.
\]
For \(1\le t\le7/4\), let
\(q=d'-d/t=t^2-2t^4/5\). Subtracting \((1+i\varepsilon q)V\) from
\(tV'\) gives exactly the error numerator
\(tR_{V'}-R_V-i\varepsilon q(V-t)\). Thus the independently propagated
bound is
\[
|Z-1-i\varepsilon q|
\le\frac{(7/4)C_{V'}+C_V+7\cdot333\eta}{1-333\varepsilon}
\varepsilon\eta<800\varepsilon\eta.
\tag{G}
\]
Every rational constant in this computation is checked independently in
`checks.py`. In particular,
\[
q(1)=3/5,\qquad q(7/4)=-441/640,
\]
and (G) proves \(\Im Z(1)>\varepsilon/2\) and
\(\Im Z(7/4)<-\varepsilon/2\), with considerable margin.

For any continuous argument of \(W\),
\[
\theta'(t)=\Im(W'/W)=-2\Im Z(t)/t.
\]
It has opposite strict derivative signs at two interior points of the actual
slit, so it is neither nondecreasing nor nonincreasing. Changing the continuous
lift or reversing the arc orientation does not alter that conclusion.

The signed outward radial angle is
\[
\beta(t)=\arg((-W')/W)=\arg Z(t).
\]
It is positive at \(1\), negative at \(7/4\), and tends to zero at infinity
because \(V(t)=a^{-1/2}t+O(t^3)\). Either possible direction of monotonicity is
therefore excluded on this actual slit subarc together with its tail. The
ordinary nonnegative outward angle is \(|\beta|\), since the branch stays
arbitrarily close to zero. Continuity forces a zero between the two sign
points, while \(|\beta|\) is positive at both endpoints. Thus this interpretation
is also nonmonotone. Choosing the inward vector would give \(\pi-|\beta|\),
which is nonmonotone as well.

## Adversarial mechanisms, boundaries, and remaining gap

| Attempted failure | Check and outcome |
| --- | --- |
| An arbitrary differential mistaken for an extremal | Actual compactness maximizer is established first; differential is necessary for it; equality with its slit is then proved. No sufficiency inference. |
| Degenerate or constant support functional | Identity and Koebe give different real values, and \(a=L(f^2)\) is near one. |
| Root transform loses injectivity or its square root branch | Nonzero normalized analytic square root and oddness give direct injectivity; exterior-map normalization is exact. |
| Finite tail checks pretend to control all coefficients | Weighted area norm and closed-form infinite majorants supply the control. |
| Distance estimate has its inequality reversed | Inverse disk map and Schwarz's lemma give exactly the needed upper bound. |
| The reversal lies beyond the actual tip | Actual tip is below \(0.3\); entire candidate segment lies above \(25/81>0.3\). |
| Joining trajectories, interior critical point, or unexpected endpoint | \(P\) is nonzero in the relevant disk; rational \(Q\) is regular on the segment; the actual support arc has only its finite tip and infinity as endpoints. |
| Uniqueness at infinity has a sign or sheet ambiguity | Positive natural-coordinate trajectories lift to real rays; oddness projects the two rays to the same slit tail. |
| Orientation or angle branch changes | Independent uniform bound (A) makes modulus strictly decrease and keeps the signed radial angle close to zero throughout. |
| The endpoint expansion has only formal asymptotic meaning | Explicit complex analytic remainders give (G), with rational sign margins. |
| Epsilon-zero boundary | At \(\varepsilon=0\) the strict reversal disappears, as it should; this is not the stated parameter. |
| Known simpler monotone families contradict the mechanism | The a3-only and a4-only controls have no sign reversal before the tested radius; the selected mixed functional is essential. |
| Eventual monotonicity at infinity defeats a bounded reversal | The candidate's first-order polynomial is positive near zero and changes sign on a bounded subarc; no eventual-monotonicity theorem is a premise of this audit. |

A useful independent family check is the perturbation \(i\varepsilon(a_4-\lambda a_3)\).
At Koebe its first-order angle polynomial is
\[
q_\lambda(t)=(2-\lambda/3)t^2-2t^4/5.
\]
The constant asymptotic-direction term cancels from this angle polynomial.
For \(\lambda=0\) the turning point lies beyond the Koebe tip's natural
coordinate \(t=2\); for \(\lambda=3\) it is \(t=\sqrt{5/2}\), well before the
tip. This confirms the proposed mechanism without treating the first-order
model as an actual extremal or as a substitute for certified remainders.

**Exact remaining gap:** no unfilled logical gap in the new argument was found
in this analytic review, conditional on the classical theorems explicitly
identified above. Those classical theorems and the continuous analytic
derivations have not been machine-formalized. This AI review is not independent
human peer review. Current novelty, prior resolution, and suitability of any
public "solved" label are separate questions not decided here. A full historical
priority audit or expert review may add evidence; this review initiates no
outreach and makes no immutable-release recommendation.
