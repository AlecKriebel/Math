# Attempt 2: a signed quadratic pencil and a rigorous lower bound for the radius

Date: 2026-10-20 UTC. Target: Albert–Bousquet-Mélou (ABM), Conjecture 11, for fixed real −1 ≤ a < 0. This is an authored mathematical attempt, not a claim to settle the conjecture.

## Outcome

The signed corner model has an exact self-adjoint quadratic-pencil representation. It proves, without assuming coefficient positivity, the full conjectured **lower bound** for the radius:

\[
\rho_Q(a)\ge\rho_*(a):=
\begin{cases}
(2+\sqrt{2+2a})^{-2},&-\tfrac12\le a<0,\\
-a/[2(a-1)^2],&-1\le a\le-\tfrac12.
\end{cases}
\]

Equivalently, the limsup of the absolute coefficients' nth roots is at most the conjectured exponential constant. The proof also supplies an explicit polynomial-times-exponential coefficient bound. The corresponding operator is genuinely noninvertible at the proposed endpoint, but this does **not** prove that its particular corner matrix element is singular there. Indeed, that matrix element has a finite one-sided Abel limit there. Establishing its nonanalyticity is the precise remaining step.

No positivity in a+1, coefficientwise comparison between confinement domains, or numerical extrapolation is used.

## 1. Normalization and exact contraction

Let t mark individual steps, so the return series is Q(a,t²). Work on the Hilbert space

\[
\mathcal H=\ell^2(\mathbb Z_{\ge0}^2),\qquad \delta=e_{0,0}.
\]

Define unilateral coordinate shifts

\[
Ue_{i,j}=e_{i+1,j},\qquad Ve_{i,j}=e_{i,j+1},
\]

and their Hilbert-space adjoints. Put

\[
A=U+U^*+V+V^*,\qquad B=U^*V+UV^*,\qquad b=1-a\in(1,2].
\]

Thus A is nearest-neighbor quadrant adjacency and B is adjacency along NW and SE diagonals, with forbidden endpoints suppressed. Both are bounded self-adjoint operators, with norms at most 4 and 2, respectively. Set

\[
K(t)=I-tA+bt^2B.
\tag{1}
\]

**Lemma 1 (exact formal identity).**

\[
Q(a,t^2)=\langle\delta,K(t)^{-1}\delta\rangle.
\tag{2}
\]

Initially the inverse is interpreted formally near t=0, or analytically in a sufficiently small disk.

**Proof.** For a word w, expand a^{c(w)} as the sum over subsets of its NW/ES corners, assigning weight a−1 to every selected corner. Selected corners never overlap: their final letters W and S are not possible initial letters N and E of another selected corner. Contract each selected NW into the diagonal (−1,+1) and each selected ES into (+1,−1), retaining weight (a−1)t². Every remaining individual step has weight t.

This contraction and expansion are bijective, including at the quadrant boundary. A selected NW based at (i,j) has intermediate point (i,j+1) and endpoint (i−1,j+1); if its initial and final points are in the quadrant, its intermediate point is too. A selected ES has intermediate point (i+1,j) and endpoint (i+1,j−1), with the same property. Conversely, every allowed diagonal expands to a valid two-step segment. Thus no boundary term is missing and no invalid path is introduced. The macro-step series is (I−tA−(a−1)t²B)^{-1}, proving (2). The corner convention is linear, with no extra final/initial adjacency. ∎

This also agrees with the signed six-step kernel in ABM equation (8), but the argument above establishes the particular boundary realization independently.

## 2. A real coercivity bound with the conjectured transition

Extend a quadrant vector by zero to the full lattice. The quadratic form of K(r), for real r≥0, is the compression of the translation-invariant operator with Fourier symbol

\[
k_r(\theta,\phi)=1-2r(\cos\theta+\cos\phi)+2br^2\cos(\theta-\phi).
\tag{3}
\]

Its minimum is found without a sign assumption. Write v=(θ−φ)/2 and s=(θ+φ)/2. Minimizing over s leaves c=|cos v|∈[0,1] and the polynomial

\[
1-4rc+4br^2c^2-2br^2.
\]

Consequently

\[
m(r):=\min_{\theta,\phi} k_r(\theta,\phi)=
\begin{cases}
1-4r+2br^2,&0\le r\le 1/(2b),\\
1-1/b-2br^2,&r\ge1/(2b).
\end{cases}
\tag{4}
\]

Let t₀ be the first positive zero of m. A direct check gives

\[
t_0=
\begin{cases}
1/(2+\sqrt{4-2b}),&1<b\le3/2,\\
\sqrt{(b-1)/(2b^2)},&3/2\le b\le2.
\end{cases}
\tag{5}
\]

The formulas coincide at b=3/2. Thus t₀²=ρ*(a), and

\[
K(r)\ge m(r)I>0\quad(0\le r<t_0).
\tag{6}
\]

Negative real t cause no additional problem. The parity unitary Je_{i,j}=(−1)^{i+j}e_{i,j} satisfies JAJ=−A and JBJ=B, so K(−r)=JK(r)J.

For later use, t₀≤1/√8<1/2 and t₀<1/√(2b) throughout this parameter interval.

## 3. Complex parameters: uniform invertibility, not just a real-axis argument

Real coercivity alone would not establish the power-series radius. The next argument rules out complex obstructions in the entire required disk and provides a uniform bound.

For a unit vector f define the scalar polynomial

\[
p_f(z)=\langle f,K(z)f\rangle=1-\alpha z+b\beta z^2,
\quad\alpha=\langle f,Af\rangle\in[-4,4],\quad
\beta=\langle f,Bf\rangle\in[-2,2].
\]

Every real zero of p_f has modulus at least t₀, by (6) and parity. If z=x+iy, y≠0, is a nonreal zero, its imaginary and real parts imply, successively,

\[
\alpha=2b\beta x,\qquad 1-b\beta(x^2+y^2)=0.
\]

It follows that β>0 and

\[
|z|^2=1/(b\beta)\ge1/(2b)>t_0^2.
\tag{7}
\]

Hence **every zero of every p_f lies outside the open disk of radius t₀**. Factor p_f using its at most two finite zeros and its constant term 1. For |z|≤r<t₀, this gives uniformly in f

\[
|\langle f,K(z)f\rangle|\ge(1-r/t_0)^2.
\tag{8}
\]

The same estimate holds when p_f has degree zero or one: the base 1−r/t₀ is in (0,1]. By homogeneity and Cauchy–Schwarz,

\[
\|K(z)f\|\ge(1-r/t_0)^2\|f\|.
\]

This shows that K(z) is injective with closed range. Moreover K(z)*=K(conjugate(z)), and the identical bound gives ker K(z)*={0}. The range of K(z) is therefore dense as well as closed, and is all of the Hilbert space. In particular,

\[
\|K(z)^{-1}\|\le (1-r/t_0)^{-2}\quad(|z|\le r<t_0).
\tag{9}
\]

The operator-valued inverse is holomorphic on |z|<t₀. The scalar identity (2), already valid near zero, thus extends throughout that disk.

**Theorem 2 (proved radius bound).** For every fixed −1≤a<0,

\[
\rho_Q(a)\ge t_0^2=\rho_*(a).
\]

**Proof.** The holomorphic scalar function in (2) is even by parity. Its power series in u=t² is consequently holomorphic for |u|<t₀². ∎

A quantitative version follows from Cauchy's estimate and (9). Taking r=t₀n/(n+1), for n≥1,

\[
|Q_n(a)|\le (n+1)^2(1+1/n)^{2n}\rho_*(a)^{-n}
\le e^2(n+1)^2\rho_*(a)^{-n}.
\tag{10}
\]

This is a bound for the actual signed coefficient, not for the sum of absolute path weights.

## 4. The endpoint is genuinely a bulk spectral threshold

The symbol in (3) vanishes at t=t₀:

- for b≤3/2, at (θ,φ)=(0,0);
- for b≥3/2, at (θ,φ)=(q,−q), where cos q=1/(2bt₀).

Take a plane wave at one such frequency, truncate it to a square of side N whose distance from either quadrant axis tends to infinity, and normalize it in ℓ². Away from the boundary of the square, K(t₀) annihilates the wave. The error is supported on O(N) sites, each of size O(1/N), so its norm is O(N^{-1/2}). These normalized vectors converge weakly to zero. They form a Weyl sequence, proving that zero lies in the essential spectrum of K(t₀). Thus the operator inverse really loses bounded invertibility at the proposed endpoint.

This fact is **not** sufficient for the scalar function in (2) to be singular there. The corner vector could in principle have insufficient coupling to the threshold modes; an argument excluding that possibility is still required.

## 5. In fact, the corner Green function has a finite Abel limit

The following further lemma narrows the missing analytic step: divergence of Q itself cannot be the proposed mechanism.

Let R=U+V, H=(R+R*)/2=A/2 and L=(R−R*)/(2i). Let P_x and P_y project onto the axes i=0 and j=0, respectively, and put P=P_x+P_y. Direct calculation yields

\[
R^*R=2I+B,\qquad R^*R-RR^*=P,
\]

and hence

\[
B=H^2+L^2+P/2-2I.
\]

Therefore, for real r,

\[
K(r)=\bigl(1-2rH+br^2H^2-2br^2I\bigr)+br^2(L^2+P/2).
\tag{11}
\]

Since the spectrum of H lies in [−2,2], the first parenthesis is at least m(r)I. Since P≥2|δ⟩⟨δ|,

\[
K(r)\ge m(r)I+br^2|\delta\rangle\langle\delta|.
\tag{12}
\]

For 0<r<t₀, inverse order gives

\[
0<Q(a,r^2)\le\frac{1}{m(r)+br^2}.
\tag{13}
\]

At the endpoint K₀=K(t₀) is nonnegative and satisfies K₀≥bt₀²|δ⟩⟨δ|. Its regularized corner resolvent

\[
G(\epsilon)=\langle\delta,(K_0+\epsilon I)^{-1}\delta\rangle
\]

has a finite increasing limit as ε↓0, bounded by 1/(bt₀²). To see that Q approaches precisely that limit, write r=st₀, 0<s<1. Then

\[
K(r)=s^2K_0+(1-s)\bigl((1+s)I-st_0A\bigr).
\]

Because ||A||≤4 and t₀<1/2,

\[
s^2K_0+\epsilon_-I\le K(r)\le s^2K_0+\epsilon_+I,
\qquad
\epsilon_\pm=(1-s)(1+s\pm4st_0)>0.
\]

The diagonal entries of both inverse bounds tend to lim_{ε↓0}G(ε). Thus

\[
\lim_{r\uparrow t_0}Q(a,r^2)
=\lim_{\epsilon\downarrow0}G(\epsilon)
\le\frac{1}{bt_0^2}<\infty.
\tag{14}
\]

This is a finite **Abel limit**. It does not, without additional coefficient control, assert ordinary or absolute convergence of the signed series at u=ρ*(a). It also does not assert analyticity there. A finite value is entirely compatible with the conjectured radius, as at the known a=−1 endpoint.

An additional exact factorization can help isolate the lower branch. For r>0,

\[
K(r)=br^2\left(R-\frac{1}{br}I\right)^*\left(R-\frac{1}{br}I\right)
+\left(1-\frac1b-2br^2\right)I.
\tag{15}
\]

For b≥3/2 the scalar term vanishes precisely at r=t₀, and α=1/(bt₀) ranges from 2 down to √2. Under the standard identification of the quadrant Hilbert space with H² of the bidisk, R is multiplication by z+w. Thus K(t₀)=bt₀² M_{z+w−α}* M_{z+w−α}. This is an exact quadrant identity, not only a full-plane symbol calculation. It offers a possible Hardy-space route to the remaining threshold-coupling problem, but the identity alone proves no scalar singularity.

## 6. Exact blocked step and plausible next target

To prove equality it remains to show that

\[
t\longmapsto\langle\delta,K(t)^{-1}\delta\rangle
\]

cannot extend holomorphically through t=t₀. The bulk Weyl sequence above escapes the corner, so it supplies no lower bound on the corner's spectral weight. The norm blow-up of K(t)^{-1} therefore cannot simply be substituted for a scalar singularity proof. Nor can positivity of K(r) as an operator be substituted for coefficient positivity of Q(a,u).

A sufficient continuation would be a rigorous local spectral-density or threshold-resolvent result for this quadrant compression, showing that the corner vector couples nontrivially to the threshold modes and that this coupling produces a nonanalytic term under the parameter perturbation K(t). Merely proving a nonzero spectral measure near zero for the fixed operator K(t₀) would still need to be connected carefully to the varying quadratic pencil. A derivative blow-up or a noninteger/logarithmic expansion could establish the needed scalar nonanalyticity even though (14) remains finite.

Status: the lower-bound theorem and lemmas above are proved; the upper bound for the radius, and thus ABM Conjecture 11 on the negative interval, remain unresolved by this attempt.

## 7. Checks and source basis

An independent finite-length check compared direct last-direction dynamic programming against the macro-step recurrence F_m=A F_{m−1}+(a−1)B F_{m−2}, through length 14 at a=−1, −3/4, −1/2, −1/4, and 0. All coefficients agreed exactly using rational arithmetic. This is only a normalization check, not part of the radius proof. For example, the a=−1 coefficients for n=0,…,7 were 1, 2, 6, 22, 92, 424, 2108, 11134.

Primary source: Michael Albert and Mireille Bousquet-Mélou, “Permutations sortable by two stacks in parallel and quarter plane walks,” European Journal of Combinatorics 43 (2015), 131–164. [arXiv v3](https://arxiv.org/abs/1312.4487v3), [DOI](https://doi.org/10.1016/j.ejc.2014.08.024). The inspected source's equation (8) provides the relevant signed kernel, Conjecture 11 gives the target radius, and Proposition 17 establishes the endpoints a=±1. The source/status gate was read before this attempt; no third-party source text or private source material is reproduced here.
