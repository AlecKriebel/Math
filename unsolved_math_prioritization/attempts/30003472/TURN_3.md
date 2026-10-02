# Turn 3: singular parabolic-product measures

Problem 30003472 / OWR-15427-014. Substantive author turn **3 of 5**.
Status: **partial; the unrestricted problem remains unresolved**.

## 1. A genuinely singular class

Define the nonlinear map
\[
 \Phi(x,t)=(x,x^2+t).
\]
Let \(\nu\) be a compactly supported probability measure on the real line satisfying an interval Frostman bound
\[
 \nu(I)\le C|I|^d\quad\text{for every bounded interval }I,\qquad
 C>0,\quad0<d\le1.                                                  \tag{1}
\]
Let \(\eta\) be any Borel probability measure on the real line, and suppose at some \(t_0\) it has a local lower bound
\[
 \eta([t_0-r,t_0+r])\ge c r^s\qquad(0<r\le r_0),                     \tag{2}
\]
where \(c,r_0>0\) and \(s\ge0\). Put \(\tau=\Phi_\#(\nu\otimes\eta)\). More generally, let the original line-null probability measure satisfy \(\mu\ge w\tau\) for some \(w>0\).

**Theorem.** For every sufficiently large \(n\),
\[
 p_\mu(\mathrm{conv}_n)
 \ge n!\left(A n^{-1-2s/d}\right)^n,
 \qquad A=\frac{wc}{2\,4^s(2C)^{2s/d}},                              \tag{3}
\]
and, when all n-types have positive probability,
\[
 \frac{p_\mu(\mathrm{conv}_n)}{\min_\omega p_\mu(\omega)}
 \ge1024\left(\frac{A}{128e^4}n^{3-2s/d}\right)^n.                   \tag{4}
\]
If a type has probability zero, the desired comparison is already immediate. Thus whenever \(d>2s/3\), every fixed base \(q>1\) works eventually in this class, with a measure-dependent threshold.

Every probability measure \(\eta\) satisfies (2) at some point with \(s=1\), by the elementary lemma below. Consequently (4) treats arbitrary \(\eta\) whenever \(d>2/3\). Better local lower exponents in (2) give additional cases with smaller d.

These are explicitly product-component hypotheses. They are not asserted for an arbitrary singular planar measure. The nonlinear map \(\Phi\) does not preserve general order types; its precise parabolic form is used in the proof.

## 2. A local lower bound for an arbitrary one-dimensional measure

**Heavy-interval lemma.** If \(\eta([a,b])=m>0\) and \(L=b-a>0\), there is \(t_0\in[a,b]\) such that
\[
 \eta([t_0-r,t_0+r])\ge\frac{m}{2L}r\qquad(0<r\le L).               \tag{5}
\]

Bisect the closed interval and retain a half carrying at least half the mass of its parent. This is possible even when an atom lies at the midpoint, because the two closed halves together cover the parent. Inductively obtain nested closed intervals \(J_k\) of length \(L2^{-k}\) and mass at least \(m2^{-k}\). Their intersection is a point \(t_0\). For a given \(0<r\le L\), choose k with
\(r/2<|J_k|\le r\). Since \(t_0\in J_k\), the interval \(J_k\) is contained in \([t_0-r,t_0+r]\), proving (5). Every probability measure has some bounded interval of positive mass, so this always supplies (2) with \(s=1\).

If \(\eta\) has an atom of mass b at \(t_0\), then (2) holds with \(s=0,c=b\). No differentiation theorem or regularity of \(\eta\) is needed in (5).

## 3. Quantile intervals with geometric separation

Bound (1) implies that \(\nu\) is nonatomic. Fix \(n\ge3\), put \(M=2n-1\), and use continuity of the distribution function to partition its compact supporting interval into consecutive closed quantile intervals
\[
 I_j=[a_{j-1},a_j],\qquad \nu(I_j)=1/M\quad(1\le j\le M).
\]
Endpoints have zero mass, so adjacent closed intervals cause no probabilistic ambiguity. Flat portions of the distribution function do not prevent choosing increasing quantile endpoints.

Select the n odd-indexed intervals. Between successive selected intervals lies a full even-indexed interval of \(\nu\)-mass \(1/M\). By (1), every such separating interval has length at least
\[
 \ell_n=(CM)^{-1/d}.                                                 \tag{6}
\]
Thus any points chosen in successive selected intervals have abscissae separated by at least \(\ell_n\), regardless of the widths of the selected intervals themselves.

Set
\[
 \delta_n=\ell_n^2/4.
\]
For large n, \(\delta_n\le r_0\). For each selected interval define
\[
 B_j=\{(x,y):x\in I_j,\ |y-x^2-t_0|\le\delta_n\}.
\]
These sets have disjoint x ranges, separated by positive gaps. Product structure and (2) give
\[
 \mu(B_j)\ge w\nu(I_j)\eta([t_0-\delta_n,t_0+\delta_n])
 \ge\frac{wc}{4^s C^{2s/d}M^{1+2s/d}}
 \ge A n^{-1-2s/d},                                                  \tag{7}
\]
with A as in (3).

## 4. Convexity and counting

For three points from distinct selected strips, in increasing-abscissa order \(x<y<z\), write their ordinates as \(x^2+t_0+e_x\), and similarly for y,z. Their vertical errors have absolute value at most \(\delta_n\), and consecutive abscissa gaps are at least \(\ell_n\). The orientation determinant is bounded below by
\[
 (z-x)((y-x)(z-y)-2\delta_n)
 \ge\tfrac12(z-x)\ell_n^2>0.
\]
Hence every transversal is in strictly convex position. The n! disjoint assignments of sample labels to selected strips give (3).

Use the Turn 1 lower bound \(T_n\ge1024(n!)^3/128^n\), together with \(\min p\le1/T_n\). The resulting ratio is at least
\[
 1024(n!)^4\left(\frac{A}{128}n^{-1-2s/d}\right)^n
 \ge1024\left(\frac{A}{128e^4}n^{3-2s/d}\right)^n,
\]
which is (4). All constants are fixed before n varies. The restriction on n is exactly the small-radius regime in (2), followed by the threshold required to dominate a chosen exponential base.

## 5. Line-nullness and full-type-support singular examples

The measure \(\tau\) itself always charges no line. A vertical line requires a fixed x and has zero mass because \(\nu\) is nonatomic. For a nonvertical line \(y=ux+v\), fix t first: the equation \(x^2+t=ux+v\) has at most two real solutions in x, so its \(\nu\)-mass is zero. Fubini over \(\eta\) completes the proof. This also covers atomic \(\eta\).

Here is an explicit class to show that this result is not merely a zero-probability-type observation. Let \(\nu\) be uniform on \([0,1]\), so (1) holds with d=1,C=1. Construct a nonatomic singular probability measure \(\eta\) with full support on \(\mathbb R\): enumerate a countable basis of bounded rational open intervals, place an affine copy of the standard Cantor probability measure inside each interval, and take a mixture with strictly positive summable weights, normalized to sum to one.

The measure \(\eta\) is carried by a countable union S of Lebesgue-null Cantor sets and gives positive mass to every open interval. The image measure \(\tau\) is carried by
\[
 \{(x,y):0\le x\le1,\ y-x^2\in S\},
\]
which has planar Lebesgue measure zero by Fubini. Thus it is purely singular. Its support is the full closed vertical strip \([0,1]\times\mathbb R\): \(\Phi\) is a homeomorphism, and the product has that support. Every simple finite order type has a positive-affine rescaling inside the interior of this strip. Small stable neighborhoods of its points all have positive \(\tau\)-mass, so every finite type has positive probability.

Nevertheless (4), with the heavy-interval lemma and d=s=1, proves a gap of order \((C_\tau n)^n\) for this genuinely singular, full-finite-type-support example. Compact support of \(\nu\) does not prevent full finite-type support in the plane.

## 6. Scope, blocked extension, and next route

Turn 2 treated all measures with a nonzero absolutely continuous component. Turn 3 now treats certain purely singular measures, including examples with full finite-type support. It does so through a quantitative separation property in one coordinate and an actual product component along a family of convex parabolas.

For an arbitrary singular measure, disintegration along the coordinate \(t=y-x^2\) yields a family of conditional x-measures, not a fixed independent product. Convergence of nearby conditional averages is in general only weak; it does not by itself control n-dependent quantile intervals at the shrinking \(\ell_n\) scale. There is no proof here that an arbitrary measure contains a dominated product component or that the needed quantitative conditional control holds.

The threshold condition d>2s/3 is a sufficient condition for this argument. Failure of that inequality is not a counterexample to the target. The max/min target might hold by a different type or mechanism when the convex-position lower bound used here is too weak.

No threshold uniform over all measures has been obtained. The original universal target stays unresolved. Completion estimate **25%**, subjective; author count **3/5**. Two substantive turns remain.
