# Topological invariance of helicity: regularity results and the remaining gap

Problem 30006363 / OWR-14299512-001, rank 557. Checked 4 October 2026.

**Outcome: the full problem is not resolved here.** The results below prove
restricted cases, disprove two proposed approximation shortcuts, and isolate a
boundary defect. None is a counterexample to Arnold's question, and no novelty
or priority claim is made.

## 1. The question being investigated

Let $M$ be a closed, oriented, smooth three-manifold, let μ be a smooth
positive volume form, and let $X_1,X_2$ be smooth vector fields. Assume

$$
 \omega_i=\iota_{X_i}\mu=d\alpha_i,
 \qquad h\circ\phi_{X_1}^t=\phi_{X_2}^t\circ h\quad(t\in\mathbb R),
$$

where $h:M\to M$ is an orientation-preserving, μ-measure-preserving
homeomorphism. Is

$$
 \mathcal H(X_1)=\int_M\alpha_1\wedge\omega_1
              =\int_M\alpha_2\wedge\omega_2=\mathcal H(X_2)?
$$

This is the scope of Question 1 on printed p. 1664 of
[Oberwolfach Report 31/2025](https://ems.press/content/serial-article-files/52240).
Time is not reparametrized. Preservation of unsigned measure does not remove
the separate orientation requirement. Zeroes of the vector fields are allowed.

The affirmative result of Edtmair and Seyfaddini covers the case in which
neither field vanishes; see Theorem 1.3 of
[arXiv:2508.10609v1](https://arxiv.org/abs/2508.10609v1).
We use that result only with its stated nonsingularity hypothesis.

Primitive independence follows from Stokes: if $d\alpha=d\alpha'=\omega$,
then $d(\alpha-\alpha')=0$, and
$$
 (\alpha-\alpha')\wedge d\alpha
 =-d((\alpha-\alpha')\wedge\alpha).
$$
Thus its integral is zero. This argument itself does not require $X\ne0$.

### A rejected scope-changing counterexample

On $\mathbb T^3=(\mathbb R/\mathbb Z)^3$, with volume $dx\,dy\,dz$, put

$$
 B=(\sin(2\pi z),\cos(2\pi z),0),\qquad
 r(x,y,z)=(-x,y,z).
$$

Then $\operatorname{curl}B=2\pi B$, so its exact-form primitive is the
metric-dual one-form of $B/(2\pi)$, and $\mathcal H(B)=1/(2\pi)$.
The pushforward $C=r_*B=(-\sin(2\pi z),\cos(2\pi z),0)$ satisfies
$\operatorname{curl}C=-2\pi C$, hence $\mathcal H(C)=-1/(2\pi)$.
The two flows are smoothly time-conjugate by $r$, which preserves measure.
But $r$ reverses orientation. This is **not** a counterexample to the source
question.

## 2. Attempt 1: weak pullback at Lipschitz regularity

**Proposition 2.1.** Under the hypotheses in Section 1, if $h$ is
bi-Lipschitz with respect to any smooth Riemannian metric, then the helicities
are equal. The zero sets can be arbitrary.

**Proof.** Rademacher's theorem gives differentiability almost everywhere.
At a differentiability point $x$, differentiate the conjugacy identity in
time at zero. Since the source orbit is smooth and
$\phi_{X_1}^t(x)=x+tX_1(x)+O(t^2)$ in coordinates, differentiability of $h$
gives

$$
 Dh_xX_1(x)=X_2(h(x)).                                      \tag{2.1}
$$

The area formula, measure preservation, and orientation preservation give
$h^*\mu=\mu$ almost everywhere. More explicitly, the signed Jacobian is
positive at differentiability points where the derivative is nonsingular:
its local degree agrees with the orientation of the homeomorphism. For a
bi-Lipschitz map that derivative is nonsingular almost everywhere, and the
area formula and measure preservation force its volume Jacobian to be one.
Exterior algebra and (2.1) now imply

$$
 h^*\omega_2=h^*(\iota_{X_2}\mu)
            =\iota_{X_1}(h^*\mu)=\omega_1\quad\text{a.e.}    \tag{2.2}
$$

Set $\beta=h^*\alpha_2$, using the almost-everywhere derivative. This is
an essentially bounded one-form. The weak pullback chain rule gives

$$
 d\beta=h^*(d\alpha_2)=\omega_1
$$

as distributions. Here the needed chain rule can be justified locally without
smooth approximation by homeomorphisms. Choose coordinate neighborhoods with
the image of the smaller source neighborhood compactly contained in a target
chart. Mollify the coordinate map of $h$ there. These smooth maps converge
uniformly and in $W^{1,p}_{\mathrm{loc}}$ for each finite $p$, with uniformly
bounded first derivatives. Consequently their pullbacks of a fixed smooth
one-form and two-form converge in every finite $L^p_{\mathrm{loc}}$: use the
multilinear expressions in the first derivatives and their uniform bounds.
Pass to the distributional limit in the smooth chain rule. Local identities
give the asserted global identity.

The distributionally closed one-form $\gamma=\beta-\alpha_1$ satisfies

$$
 \int_M\gamma\wedge\omega_1
 =\int_M\gamma\wedge d\alpha_1
 =\langle d\gamma,\alpha_1\rangle=0.
$$

The last equality is weak integration by parts on the closed manifold, with
the smooth test form $\alpha_1$. Finally the area formula yields

$$
 \mathcal H(X_2)
 =\int_M h^*(\alpha_2\wedge\omega_2)
 =\int_M\beta\wedge\omega_1
 =\int_M\alpha_1\wedge\omega_1.
$$

All products in this calculation are integrable. This proves the proposition.
$\square$

**What failed in the unrestricted attempt.** A general volume-preserving
homeomorphism need not possess a weak derivative adequate to define the
one-form pullback or its exterior derivative. Time differentiability along
orbits alone supplies no transverse derivative. Section 6 supplies an explicit
rough conjugacy illustrating this obstacle. Proposition 2.1 does not establish
regularity of the homeomorphism assumed in the question.

## 3. Attempt 2: approximation by smooth conjugacies

Fix a metric whose volume form is μ; rescaling any initial metric supplies
one. Norms below refer to that metric.

**Lemma 3.1 (continuity).** There is a constant $C_M$ such that exact smooth
two-forms ω,ν satisfy

$$
 |\mathcal H(\omega)-\mathcal H(\nu)|
 \le C_M\|\omega-\nu\|_2(\|\omega\|_2+\|\nu\|_2).           \tag{3.1}
$$

**Proof.** Let $G$ be the Green operator of the Hodge Laplacian on the
orthogonal complement of harmonic forms, and put $K=d^*G$. The standard
Hodge identity gives $dK\omega=\omega$ for closed exact two-forms: their
harmonic projection is zero and $dG\omega=Gd\omega=0$. On a closed manifold

$$
 \|K\omega\|_2\le C_M\|\omega\|_2.
$$

This also follows directly from the positive first eigenvalue on the
orthogonal complement of harmonic forms and
$\|d^*G\omega\|_2^2\le\langle\Delta G\omega,G\omega\rangle$.
Expand

$$
 \mathcal H(\omega)-\mathcal H(\nu)
 =\int_M K(\omega-\nu)\wedge\omega
       +\int_M K\nu\wedge(\omega-\nu),
$$

and apply Cauchy–Schwarz to both terms. $\square$

It follows that if smooth orientation- and volume-preserving diffeomorphisms

$$
 h_n:M\to M\quad\text{satisfy}\quad (h_n)_*X_1\to X_2
 \text{ in }L^2,
$$

then $\mathcal H(X_1)=\mathcal H(X_2)$. Indeed the pushforwards are exact,
their helicities all equal $\mathcal H(X_1)$, and (3.1) passes to the limit.

Uniform approximation of $h$ is insufficient to supply that hypothesis.
Here is a fully explicit obstruction to that particular inference. On the
unit three-torus put

$$
 U=\sin(2\pi z)\partial_x,\qquad
 h_n(x,y,z)=(x,y+n^{-1}\sin(2\pi nx),z).
$$

These are smooth orientation- and volume-preserving diffeomorphisms, and

$$
 \|h_n-\mathrm{id}\|_{C^0},\ \|h_n^{-1}-\mathrm{id}\|_{C^0}\le n^{-1}.
$$

The field $U$ is exact, with primitive
$\alpha=\cos(2\pi z)\,dy/(2\pi)$. At the target point $(x,y,z)$,

$$
 U_n=(h_n)_*U
 =\sin(2\pi z)\partial_x
   +2\pi\cos(2\pi nx)\sin(2\pi z)\partial_y.
$$

Nevertheless,

$$
 \|U_n-U\|_2^2
 =4\pi^2\left(\int_0^1\cos^2(2\pi nx)dx\right)
          \left(\int_0^1\sin^2(2\pi z)dz\right)=\pi^2.       \tag{3.2}
$$

Their flows do converge uniformly to the flow of $U$, uniformly on bounded
time intervals: the extra $y$-displacement is

$$
 n^{-1}\{\sin(2\pi n(x+t\sin(2\pi z)))-\sin(2\pi nx)\},
$$

of absolute value at most $2/n$. Thus even convergence of conjugated flows
does not give the strong generator convergence used in (3.1).

This example has helicity zero throughout. It is not a counterexample to
invariance, nor does it show that every specially chosen approximating
sequence must fail. The missing step is existence of approximations with
adequate generator control for an arbitrary given conjugacy.

## 4. Attempt 3: removing zeroes and invoking the nonsingular theorem

The tempting claim that nonsingular exact divergence-free fields are uniformly
dense among all exact divergence-free fields is false.

**Proposition 4.1.** There is a smooth exact divergence-free field on
$\mathbb T^3$ with a uniform neighborhood containing no nowhere-zero field,
even if the competing fields are only continuous.

**Proof.** Let

$$
 X=(\sin(2\pi y),\sin(2\pi z),\sin(2\pi x)),\qquad
 A=-\frac1{2\pi}(\cos(2\pi z),\cos(2\pi x),\cos(2\pi y)).
$$

Direct differentiation gives $\operatorname{div}X=0$ and
$\operatorname{curl}A=X$. Thus $\iota_X\mu=d(A\cdot dx)$.
At the origin,

$$
 DX_0=2\pi\begin{pmatrix}0&1&0\\0&0&1\\1&0&0\end{pmatrix},
 \qquad\det DX_0=(2\pi)^3>0.
$$

Use the coordinate ball of radius $r=1/8$ centered at the origin. This ball
contains exactly one zero of $X$, whose local index is $+1$. For
$|s|\le1/4$, concavity of sine on $[0,\pi/2]$ gives
$|\sin(2\pi s)|\ge4|s|$. Hence $|X|\ge4r=1/2$ on its boundary.

If $\|Y-X\|_{C^0}<1/2$, the straight-line homotopy from $X$ to $Y$ is
nonzero on that boundary. The normalized boundary maps to $S^2$ therefore
have equal degree $+1$. A nowhere-zero $Y$ on the whole ball would extend
its normalized boundary map to the ball and force that degree to be zero.
Contradiction. $\square$

The other seven zeroes on the torus have the expected alternating indices;
the total index is zero. Thus no global Euler-characteristic inconsistency is
being used. The field's helicity is zero, as follows by integrating $A\cdot X$.

There is a useful weaker operation for finitely many zeroes, but it does not
remove them. Near an isolated zero $p$, the exact two-form ω has coefficients
$O(r)$. The radial homotopy formula gives a local primitive ρ with
$|\rho|=O(r^2)$. Any global primitive can be changed by an exact one-form
to agree with ρ in a smaller ball. Let $\chi_\varepsilon$ vanish on
$B_\varepsilon(p)$, equal one outside $B_{2\varepsilon}(p)$, and satisfy
$|d\chi_\varepsilon|\le C/\varepsilon$. Then

$$
 \omega_\varepsilon=d(\chi_\varepsilon\alpha),\qquad
 \omega_\varepsilon-\omega
 =(\chi_\varepsilon-1)\omega+d\chi_\varepsilon\wedge\alpha
$$

is $O(\varepsilon)$ on a region of volume $O(\varepsilon^3)$, giving

$$
 \|\omega_\varepsilon-\omega\|_2=O(\varepsilon^{5/2}).       \tag{4.1}
$$

For finitely many zeroes use disjoint balls. Formula (3.1) then proves helicity
convergence. However, $\omega_\varepsilon$ vanishes on open balls, so the
approximations still lie outside the nonsingular theorem. Moreover, applying
cutoffs separately to two conjugate fields need not preserve their conjugacy.
Neither defect is repaired by (4.1).

## 5. Attempt 4: an exact defect formula around isolated zeroes

This approach obtains a singular-case sufficient condition with a precise
boundary remainder.

**Proposition 5.1.** Assume the hypotheses in Section 1. Suppose each zero set

$$
 Z_i=\{x:X_i(x)=0\}
$$

is finite, and $h:M\setminus Z_1\to M\setminus Z_2$ is a smooth
diffeomorphism. For each $p\in Z_1$, let $q=h(p)$, and use smooth local
coordinates near $p,q$. If

$$
 r^4\sup_{x\in S_r(p)}
       \big(\|Dh_x\|\,d(h(x),q)^2\big)\longrightarrow0
 \quad\text{as }r\downarrow0,                              \tag{5.1}
$$

then $\mathcal H(X_1)=\mathcal H(X_2)$.

**Proof.** Conjugacy maps $Z_1$ bijectively onto $Z_2$: fixed points of one
flow map to fixed points of the other, and a smooth field is zero precisely at
the fixed points of its flow.

We may choose primitives $\alpha_i$ with
$|\alpha_i(x)|\le C d(x,Z_i)^2$ in small neighborhoods of all zeroes.
To justify the choice, in a coordinate ball centered at a zero $p$, write
$\omega_i=O(|x|)$. The radial primitive is

$$
 \rho_x(v)=\int_0^1t\,\omega_{i,tx}(x,v)\,dt.
$$

It satisfies $d\rho=\omega_i$ and $|\rho_x|=O(|x|^2)$.
The difference between an existing primitive and ρ is a smooth closed
one-form on the ball, hence equals $df$. Subtract $d(\eta f)$ from the
global primitive, where η is a cutoff equal to one on a smaller ball. Do this
in disjoint balls for the finitely many zeroes.

On $U=M\setminus Z_1$, set $\beta=h^*\alpha_2$ and
$\gamma=\beta-\alpha_1$. Smooth conjugacy and measure preservation imply
$h^*\omega_2=\omega_1$, so $d\gamma=0$ on $U$.

Although β need not be bounded near the punctures, the three-form
$\beta\wedge\omega_1=h^*(\alpha_2\wedge\omega_2)$ is integrable.
Indeed if $\alpha_2\wedge\omega_2=f\mu$, then its pullback on $U$
is $(f\circ h)\mu$, with $f$ smooth and bounded. Change of variables,
and the fact that the finite omitted sets have zero measure, give

$$
 \mathcal H(X_2)-\mathcal H(X_1)
  =\int_U\gamma\wedge\omega_1.                            \tag{5.2}
$$

Let $M_r=M\setminus\bigcup_{p\in Z_1}B_r(p)$, for small common radius
$r$. Its boundary is oriented as the boundary of $M_r$, pointing into
the removed balls. Stokes, $d\gamma=0$, and
$\alpha_1\wedge\alpha_1=0$ give

$$
 \int_{M_r}\gamma\wedge\omega_1
 =-\int_{\partial M_r}\gamma\wedge\alpha_1
 =-\int_{\partial M_r}h^*\alpha_2\wedge\alpha_1.           \tag{5.3}
$$

The absolute value of the contribution from $S_r(p)$ is at most

$$
 C r^4\sup_{x\in S_r(p)}
            \big(\|Dh_x\|\,d(h(x),h(p))^2\big),            \tag{5.4}
$$

because $|\alpha_1|\le Cr^2$, the surface area is $O(r^2)$, and
$|h^*\alpha_2|\le C\|Dh\|d(h(x),h(p))^2$.
This tends to zero by (5.1). Letting $r\downarrow0$ in (5.3), dominated
convergence in (5.2) proves the result. $\square$

In particular, (5.1) holds if, near each zero,

$$
 d(h(x),h(p))\le C r^b,\qquad \|Dh_x\|\le C r^{-a},
 \qquad b>0,\quad a<4+2b.                                 \tag{5.5}
$$

It also holds if $r^4\sup_{S_r}\|Dh\|$ remains bounded, since continuity
of $h$ then supplies the additional vanishing factor in (5.1).

Without (5.1), equations (5.2)–(5.3) still establish the exact formula

$$
 \mathcal H(X_2)-\mathcal H(X_1)
 =-\lim_{r\downarrow0}\int_{\partial M_r}h^*\alpha_2\wedge\alpha_1,            \tag{5.6}
$$

under the other hypotheses of Proposition 5.1. The limit exists because its
left-hand integral in (5.3) converges. No assertion that the boundary term
vanishes for arbitrary $h$ is made. Arbitrary zero sets and nonsmoothness
away from zeroes introduce further problems beyond this special setting.

## 6. Attempt 5: transporting asymptotic linking closures

For this attempt restrict to $M=S^3$, avoiding homological ambiguity in
linking numbers. Let $L_{i,T}(x,y)$ denote the linking number of two closed
time-$T$ flow segments, using a chosen admissible system of closing paths.
Assume these systems give the helicity formula

$$
 \lim_{T\to\infty}T^{-2}\int_{M\times M}L_{i,T}\,d\mu\,d\mu
 =\mathcal H(X_i).                                        \tag{6.1}
$$

Ignore the null exceptional sets where the cycles or linking numbers are
undefined, and assume the functions in use are measurable and integrable.
This is a conditional reduction; it does not assert new existence or
convergence results for arbitrary closing systems.

Topological invariance of the linking number gives exact equality when both
source cycles, **including their closing paths**, are transported by $h$.
Denote the corresponding linking function at target points by
$\widetilde L_{2,T}$. Then

$$
 \widetilde L_{2,T}(h(x),h(y))=L_{1,T}(x,y).
$$

Because $h\times h$ preserves product measure, (6.1) implies the desired
equality if one can prove

$$
 T^{-2}\|L_{2,T}-\widetilde L_{2,T}\|_{L^1(M\times M)}\longrightarrow0.       \tag{6.2}
$$

Indeed, subtract the two averaged helicity formulas, use the exact equality
for transported cycles, and bound the difference by the quantity in (6.2).
This proves the conditional statement completely. It does **not** prove (6.2).

### Why uniform control of the closing paths is not automatic

Here is a volume-preserving topological conjugacy of smooth exact fields that
can turn a straight short arc into a nonrectifiable one. Work on the unit
three-torus, take a coordinate interval about $x=0$, and choose a smooth
cutoff η supported in that interval and equal to one near zero. Define the
continuous periodic function

$$
 f(x)=\begin{cases}\eta(x)x\sin(1/x^2),&x>0,\\0,&x\le0.\end{cases}
 \qquad
 h(x,y,z)=(x,y+f(x),z)\pmod1.
$$

Its inverse subtracts $f(x)$. Fubini's theorem shows preservation of the
volume measure, since each $y$-fiber is translated. The isotopy replacing
$f$ by $sf$, $0\le s\le1$, shows orientation preservation.

The smooth exact divergence-free field

$$
 V=\sin(2\pi z)\partial_y
$$

commutes with this homeomorphism, so $h$ time-conjugates $V$ to itself.
A primitive of $\iota_V\mu$ is
$-\cos(2\pi z)\,dx/(2\pi)$. This example has helicity zero.

For large integers $k$, put

$$
 x_k=(\pi/2+k\pi)^{-1/2}.
$$

These points lie where η equals one, and $f(x_k)=(-1)^k x_k$. Consequently

$$
 |f(x_{k+1})-f(x_k)|=x_{k+1}+x_k,
 \qquad \sum_{k=K}^{N-1}(x_{k+1}+x_k)\longrightarrow\infty.
$$

The divergence follows from $x_k\asymp k^{-1/2}$. Therefore $f$ has
infinite variation on every interval $[0,\delta]$, and $h$ maps the
straight arc $\{(x,0,z_0):0\le x\le\delta\}$ to a curve of infinite
length. This uses finite partitions for every lower bound and hence does not
assume differentiability of the curve.

Nonrectifiability does not itself prove (6.2) false. It shows only that
rectifiability or length estimates for the original closing paths cannot
simply be assigned to their images. In particular, topological invariance of
linking numbers alone does not establish admissibility or the required
averaged error estimate for transported closures. The same warning appears
in the historical discussion in §1.2 of the Edtmair–Seyfaddini paper.

## 7. Exact scope of the outcome

The established statements are:

1. Helicity invariance under bi-Lipschitz conjugacy, including arbitrary zero
   sets (Proposition 2.1).
2. A strong-generator-approximation criterion and an explicit failure of the
   implication from uniform conjugacy/flow convergence to that criterion.
3. A robust indexed-zero obstruction to uniform approximation by nonsingular
   fields; local exact cutoff and its quantitative error for isolated zeroes.
4. A boundary-defect identity and a sufficient growth condition for smooth
   conjugacy away from finitely many zeroes (Proposition 5.1).
5. A precise conditional linking-error reduction, and a rough conjugacy
   showing why length control needs an additional argument.

For a completely arbitrary homeomorphism in Section 1, neither a valid weak
pullback argument, a controlled nonsingular approximation, a vanishing
singular-boundary defect, nor the estimate (6.2) has been established here.
No nonzero defect or counterexample meeting every source hypothesis has been
constructed. The general equality and the source's broader extension question
for flows with fixed points remain unresolved by this investigation.

The accompanying exact symbolic checks verify the displayed explicit
examples, determinants, curls, helicities, and norm identities. They do not
verify the general analytic theorems, prove (6.2), or resolve the open problem.
