# Exact counterexample

## 1. Convention

For a legal sequence w=[a₁,b₁][a₂,b₂]⋯ with bᵢ=aᵢ₊₁, use the source's convention

\[
A(w)=\limsup_{N\to\infty}\frac{s(a_1)+\sum_{j=1}^{N}s(b_j)}{N}.
\]

The source asks for a compact infinite alphabet and continuous positive size function for which every periodic legal sequence has average strictly greater than the infimum over all legal sequences. See [SOURCE_GATE.md](SOURCE_GATE.md) for the precise attribution and the separate packing question.

## 2. The game

Fix an irrational real number α; α=√2 will do. Write S¹={z∈ℂ:|z|=1}, and define

\[
\Sigma=S^1\times[0,1],\quad s(z,t)=1+t,
\]
\[
F(z,t)=(e^{2\pi i(\alpha+t)}z,t),\quad
T=\{[x,F(x)]:x\in\Sigma\}.
\]

**Theorem.** This game has the following properties.

1. Σ is an infinite compact connected metric space, s is continuous and strictly positive, and T is closed in Σ×Σ.
2. Every legal sequence has an ordinary average-size limit. Its average is 1+t, where t is its starting height.
3. The minimum average is 1, and every sequence attaining it is aperiodic. In fact, no minimizer is even eventually periodic.
4. Periodic starting points are dense in Σ. Their average sizes have infimum 1, but none equals 1.

**Proof.** The circle and closed interval are compact connected metric spaces, and so is their product. Clearly 1≤s≤2. The map F is continuous and has continuous inverse

\[
F^{-1}(z,t)=(e^{-2\pi i(\alpha+t)}z,t).
\]

Thus F is a homeomorphism. The graph T is the continuous image of Σ under x↦(x,F(x)), hence is compact and therefore closed in the Hausdorff space Σ×Σ. Each symbol has exactly one successor and one predecessor.

If a₁=x₀=(z,t), the definition of T and the matching condition imply inductively that

\[
a_j=F^{j-1}(x_0),\qquad b_j=F^j(x_0).
\]

Consequently every legal sequence is exactly one orbit of F. All its symbols have the same height t, so every term in the numerator of A(w) is 1+t. There are N+1 terms. Therefore

\[
\frac{s(a_1)+\sum_{j=1}^{N}s(b_j)}{N}
=\frac{N+1}{N}(1+t)\longrightarrow1+t.
\tag{1}
\]

In particular A(w)≥1, with equality if and only if t=0. Such orbits exist for every z∈S¹, proving attainment.

For each integer p≥1, direct iteration gives

\[
F^p(z,t)=(e^{2\pi ip(\alpha+t)}z,t).
\tag{2}
\]

A legal tile sequence has period p if and only if its first symbol satisfies Fᵖ(z,t)=(z,t). Because z≠0, equation (2) gives the exact condition

\[
p(\alpha+t)\in\mathbb Z.
\tag{3}
\]

Thus a sequence is periodic if and only if α+t∈ℚ. At t=0 this would make α rational, a contradiction. Any periodic sequence therefore has t>0 and, by (1), has average strictly greater than 1. If a sequence were eventually periodic, F^{m+p}(x₀)=F^m(x₀) for some m and p≥1. Applying the inverse F^{-m} gives Fᵖ(x₀)=x₀, so the same argument excludes eventual periodicity for minimizers.

Finally ℚ∩[α,α+1] is dense in [α,α+1]. Translating by −α shows that the periodic heights are dense in [0,1]. At every such height all points of the circle are periodic, proving the density assertion in Σ. Choosing rational numbers approaching α from above gives periodic averages approaching 1. None equals 1 by irrationality. ∎

## 3. An explicit sequence of periodic competitors

Take α=√2. For every integer n≥1, let

\[
m_n=\lfloor n\sqrt2\rfloor+1,\qquad
t_n=\frac{m_n}{n}-\sqrt2.
\]

Since √2 is irrational, n√2 is not an integer. Hence

\[
0<t_n<\frac1n\le1.
\tag{4}
\]

At height tₙ the rotation angle is mₙ/n. Every starting point there has least period

\[
q_n=\frac{n}{\gcd(m_n,n)}.
\]

Its average is 1+tₙ, which converges to 1 from above. The construction therefore has genuine periodic competitors; the conclusion is not vacuous.

For completeness, the irrationality used here has an elementary exact proof. If √2=a/b in lowest positive terms, then a²=2b² makes a even. Writing a=2c then makes b even too, contradicting lowest terms.

## 4. Why compactness does not give a periodic minimizer

For fixed period bound Q≥1 there is a positive cost gap. Indeed, suppose α=√2 and a periodic orbit has least period q≤Q. Put r=α+t=p/q in lowest terms. Then t>0 and p²−2q² is a positive integer, so

\[
t=r-\sqrt2
=\frac{p^2-2q^2}{q^2(r+\sqrt2)}
\ge\frac{1}{(2\sqrt2+1)Q^2}.
\tag{5}
\]

Here r≤√2+1 because t≤1. Thus any sequence of periodic competitors whose average approaches 1 must have unbounded least periods. Compactness can give limits of their starting points, but it does not preserve membership in the union of all finite-period sets. In this example the limiting bottom-circle orbit is aperiodic. Formula (5) also prevents any finite search over bounded periods from detecting an exact minimizer.

## 5. Scope and robustness

The example already has a closed tile relation and a continuous bijective successor map. It therefore does not exploit a nonclosed relation, a nonattained infimum, absence of periodic competitors, or a disconnected alphabet.

If a planar alphabet is preferred, identify (z,t) with (1+t)z. This is a homeomorphism onto the closed annulus {u∈ℂ:1≤|u|≤2}. In these coordinates s(u)=|u| and

\[
F(u)=e^{2\pi i(\sqrt2+|u|-1)}u.
\]

This coordinate change preserves every claim above.

Only the abstract ordered-pair domino question is answered. No set of allowed pairwise distances for a one-dimensional interval packing is constructed, and no equivalence from this example to such a packing is asserted. The stricter packing conjecture in Gonçalves–Vedana (2025) is not resolved here.
