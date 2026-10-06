# Partial results and model barriers

## Scope

Throughout the target question, n is fixed, n >= 2, and the two matrices are independent and uniform in the closed operator-norm ball in SL_n(Z). An asymptotic in n, a Haar-volume statement, a random-walk theorem, or an inverse-bounded ball theorem is not a solution of this target. If n=1 were included literally, SL_1(Z) is trivial and the infinite-index probability is zero; that degenerate reading is excluded by the primary source's n >= 2 setting.

## Proposition 1 The dimension two case

Let B_X = {A in SL_2(Z): ||A||op <= X}. For independent uniform A_1,A_2 in B_X,

\[
\Pr([\mathrm{SL}_2(\mathbb Z):\langle A_1,A_2\rangle]<\infty)
\leq X^{-1+o(1)}.
\]

Here and below a bound X^{a+o(1)} permits an implied constant, or equivalently can be replaced by O_epsilon(X^{a+epsilon}) for every epsilon > 0.

**External counting input.** For matrices with maximum entry absolute value at most X and nonzero lower-left entry, Bulinski--Ostafe--Shparlinski, Lemma 3.6 with Q=1, bounds the pairs failing their separated-isometric-disk condition by X^{3+o(1)}. Their inequalities include tangencies among the exceptional pairs. We use this counting result, rather than infer infinite index from freeness alone. [Primary paper, Sections 2 and 3](https://arxiv.org/pdf/2304.10980).

**Elementary size bounds.** Put H(A)=max_ij |A_ij|. Then H(A) <= ||A||op <= 2H(A). There are O(X^2) determinant-one integer matrices of height <= X: group their primitive first columns (a,c) by m=max(|a|,|c|). There are O(m) possible columns of level m. Completions (b,d) of each column differ by integer multiples of (a,c), so the interval of permitted multiples has length at most 2X/m, using a coordinate of magnitude m. Summing O(m)(1+2X/m) over 1 <= m <= X proves the bound. The case c=0 has a=d=+1 or a=d=-1, hence only O(X) matrices.

There are also Omega(X^2) matrices in B_X. Let N=floor(X/2), and choose coprime integers 1 <= a,c <= N. The number of these pairs is at least

\[
N^2-\sum_{d=2}^{N}\lfloor N/d\rfloor^2
\geq (2-\pi^2/6)N^2.
\]

Choose 1 <= d <= c with ad congruent to 1 modulo c and set b=(ad-1)/c; for c=1 use d=1. Then 0 <= b <= a and all entries have absolute value at most N. The resulting distinct matrices lie in B_X. This proves the lower bound without using an asymptotic lattice-counting theorem.

**Separated disks imply infinite index.** For A=[[a,b],[c,d]] with c != 0, set

\[
D_A=\{z\in\mathbb H:|z-a/c|<1/|c|\},\qquad
D_{A^{-1}}=\{z\in\mathbb H:|z+d/c|<1/|c|\}.
\]

The determinant identity gives

\[
\left|Az-a/c\right|=\frac{1}{|c|\,|cz+d|}.
\]

Thus A maps the complement of the closed disk D_(A^{-1}) into D_A; the corresponding fact holds for A^{-1}. Suppose the four closed disks for A_1,A_1^{-1},A_2,A_2^{-1} are pairwise disjoint. Choose z_0 in the upper half-plane outside them all. Successively applying any reduced word shows that its image of z_0 lies in the disk of its last-applied letter. Consequently the entire orbit of z_0 lies in the union of four bounded disks and {z_0}, a bounded subset of C.

If the subgroup had finite index, it would contain a nonzero power of T=[[1,1],[0,1]], by the pigeonhole principle on its cosets. The orbit would then contain z_0+km for every integer k and some m != 0, contradicting boundedness. This proves infinite index. The same disk argument also proves freeness, but freeness alone would not imply infinite index in SL_2(Z).

Every finite-index-generating pair in B_X^2 therefore belongs either to the exceptional disk pairs counted by the external input or to a pair with some c_i=0. Since B_X is contained in the height-X box, the first class has at most X^{3+o(1)} pairs. The second has O(X)O(X^2)=O(X^3) pairs. Division by |B_X|^2 >> X^4 completes the proof. This is a known subcase with an explicit modern proof route, not a claim of a new solution. QED.

## Proposition 2 Inversion cannot be treated as a fixed norm change

For A in SL_n(R), its singular values sigma_1 >= ... >= sigma_n > 0 have product one. Therefore

\[
\|A^{-1}\|_{\mathrm{op}}=\sigma_n^{-1}
=\prod_{i=1}^{n-1}\sigma_i\leq\|A\|_{\mathrm{op}}^{n-1}.
\]

If C_X imposes both ||A||op <= X and ||A^{-1}||op <= X, then for X >= 1,

\[
C_X\subseteq B_X\subseteq C_{X^{n-1}}.
\]

For n=2 inversion preserves the operator norm, so C_X=B_X. For every n>=3, there is no constant K_n with ||A^{-1}||op <= K_n||A||op on SL_n(Z). Indeed, let N have ones on the superdiagonal and zeros elsewhere and put U_m=I+mN, m a positive integer. Then det U_m=1, ||U_m||op <= 1+m, and

\[
U_m^{-1}=\sum_{j=0}^{n-1}(-mN)^j,
\qquad |(U_m^{-1})_{1n}|=m^{n-1}.
\]

Hence ||U_m^{-1}||op/||U_m||op >= m^{n-1}/(1+m), which diverges. These inclusions and examples do not by themselves compare lattice-point probabilities. QED.

## Proposition 3 An exact continuous rank three distribution

This proposition concerns normalized Haar measure on SL_3(R), not uniform integer matrices. Let m be Haar measure and let

\[
\mathcal B_X=\{g\in\mathrm{SL}_3(\mathbb R):\|g\|_{\mathrm{op}}\leq X\}.
\]

For every fixed s >= 0, with sigma_1 >= sigma_2 >= sigma_3 the singular values,

\[
\lim_{X\to\infty}
\frac{m(\{g\in\mathcal B_X:\log(\sigma_1/\sigma_2)\geq s\})}
{m(\mathcal B_X)}
=2e^{-2s}-e^{-4s}.
\tag{1}
\]

Also,

\[
\frac{m(\{g\in\mathcal B_X:\|g^{-1}\|_{\mathrm{op}}\leq X\})}
{m(\mathcal B_X)}\longrightarrow0.
\tag{2}
\]

**Proof.** Write X=e^L and the ordered logarithms of singular values as a>=b>=c, a+b+c=0. The real Cartan integration formula, after integration over the two compact factors, has density equal to a positive constant times

\[
J(a,b)=\sinh(a-b)\sinh(a-c)\sinh(b-c)
\]

in coordinates da db. All constant factors cancel in the ratios. This is the n=3 specialization of the usual Cartan density, also recorded as equation (3.5) of [Fuchs--Rivin](https://academic.oup.com/imrn/article/2017/17/5385/3056825).

Set u=L-a and d=a-b. Then

\[
a=L-u,\quad b=L-u-d,\quad c=-2L+2u+d.
\]

The coordinate Jacobian has absolute value one and the exact region is

\[
u\geq0,\quad d\geq0,\quad 3u+2d\leq3L.
\]

Extend the scaled density by zero outside this region. Inside it,

\[
f_L(u,d)=e^{-6L}\sinh d\,
\sinh(3L-3u-d)\sinh(3L-3u-2d).
\]

Both latter arguments are nonnegative. The bound sinh t <= e^t/2 gives

\[
0\leq f_L(u,d)\leq\tfrac14 e^{-6u-3d}\sinh d=:f(u,d).
\]

For each fixed u,d>=0, f_L(u,d) tends to f(u,d). The dominating function is integrable and

\[
\int_0^\infty\!\int_0^\infty f(u,d)\,du\,dd
=\tfrac14\cdot\tfrac16\cdot\tfrac18=\tfrac1{192}.
\]

Dominated convergence applies both to the total mass and to d>=s. As

\[
\int_s^\infty e^{-3d}\sinh d\,dd
=\tfrac14e^{-2s}-\tfrac18e^{-4s},
\]

division by its value 1/8 at s=0 gives (1). Finally ||g^{-1}||op <= e^L is equivalent to -c <= L, or 2u+d>=L. The indicator of this event tends pointwise to zero on the fixed quadrant, and the same dominating function proves (2). QED.

**Numerical-bound correction.** Theorem 3.4 of Fuchs--Rivin prints an upper bound eta^{-2(n^2-3n+2)} for the event sigma_1/sigma_2 >= eta^2, eta>4. As printed it places separate limits on two divergent quantities; interpret its intended assertion as the limit of the ratio. For n=3, (1) at s=2 log eta equals

\[
2\eta^{-4}-\eta^{-8}>\eta^{-4}\quad(\eta>1),
\]

which contradicts that numerical upper bound. For eta=5 the exact limit is 0.00319744, whereas the printed bound is 0.0016. This corrects that bound in dimension three only. It does not refute the qualitative fact that the probability is less than one, or the separate inverse-bounded thinness theorem. It is distinct from the published correction to Lemma 2.5 in Bulinski--Ostafe--Shparlinski, Section 4.1.

No theorem transferring (1) or (2) from Haar volume to lattice-point counts is asserted here. Such a transfer requires a separately checked counting theorem and its hypotheses. In particular (2) is not labeled a zero-density theorem for SL_3(Z).

## Why two further approaches do not finish the problem

**Random-walk comparison.** Aoun's theorem uses independent random walks in a finitely generated non-virtually-solvable linear group [primary reference](https://arxiv.org/abs/1005.3445). This is not the uniform operator-ball measure. Norm or word-length comparisons describe containment of supports, not comparison of atom weights. No estimate transferring its exceptional-set probability to |B_X|^{-2} counting measure is available in this proof. This approach stops at that missing estimate.

**Finding free words is insufficient.** There are two generators of SL_3(Z) from which one can form words generating a free subgroup. Thus a proof that selected words generate a free subgroup would not alone imply that the original generators have infinite index.

For an explicit witness, let P permute e_1 to e_2 to e_3 to e_1, and set U=I+E_12. The conjugates PUP^{-1}=I+E_23 and P^2UP^{-2}=I+E_31, together with their commutators, give I+E_13, I+E_21, I+E_32. Integer elementary row operations show these generate SL_3(Z); hence <P,U>=SL_3(Z).

On the other hand the words

\[
A=U^2=I+2E_{12},\qquad
B=[PUP^{-1},P^2UP^{-2}]^2=I+2E_{21}
\]

generate a free group. On the projective line in the first two coordinates, A^k sends |x|<1 into |x|>1 and B^k sends |x|>1 into |x|<1 for every nonzero integer k. This is the elementary two-factor ping-pong criterion. Their subgroup has infinite index in SL_3(Z), also directly because it fixes e_3, whose SL_3(Z)-orbit is infinite. Nevertheless the original pair generates the entire lattice. This does not rule out a stronger argument proving the original generators themselves free; it identifies exactly the missing implication.

## Remaining target

For fixed n>=3, this work neither proves nor disproves that an independent uniform pair from B_X generates an infinite-index subgroup with probability tending to one. No positive-density, full-density, or rate claim for that discrete higher-rank question is made. The five routes examined are the rank-two counting proof, inverse-bounded comparison, direct rank-three Cartan analysis, random-walk comparison, and passage to free words. Their proved outputs and stopping points are recorded above.
