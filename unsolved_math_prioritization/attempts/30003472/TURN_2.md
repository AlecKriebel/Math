# Turn 2: all measures with a nonzero absolutely continuous component

Problem 30003472 / OWR-15427-014. Substantive author turn **2 of 5**.
Status: **partial; purely singular measures and uniform thresholds remain unresolved**.

## 1. Result and relationship to the source

Retain the notation \(p_\mu,\mathcal O_n,T_n\) from TURN_1.md. Let \(\mu\) be any Borel probability measure on the plane that charges no line. Suppose its Lebesgue decomposition has a **nonzero absolutely continuous component**. No continuity of a density, no positive lower density on an open set, and no global absolute continuity are assumed.

**Theorem.** There exist constants \(b_\mu>0\) and \(n_\mu\) such that for every integer \(n\ge n_\mu\),
\[
 p_\mu(\mathrm{conv}_n)\ge n!\left(\frac{b_\mu}{n^3}\right)^n,         \tag{1}
\]
and all finite realizable simple order types have positive probability. Consequently
\[
 \frac{p_\mu(\mathrm{conv}_n)}{\min_{\omega\in\mathcal O_n}p_\mu(\omega)}
 \ge1024\left(\frac{b_\mu n}{128e^4}\right)^n.                       \tag{2}
\]
In particular, every fixed absolute base \(c>1\), for example \(c=2\), works eventually for each measure in this class. The size threshold depends on the measure.

This repairs the particular regularity inference identified in the inspected proof of Lemma 3.16(i) of [Goaoc et al., Limits of Order Types](https://arxiv.org/pdf/1811.02236), pp.28–29, by a bounded-density truncation and differentiation argument. The source already states the convex-position scale for locally absolutely continuous measures; that scale is not claimed here as a newly discovered theorem. The proof below also allows a singular component present in every neighborhood. No claim is made about the curve-measure part of that lemma or about historical priority of this repair.

## 2. Selecting a parabolic trace with positive mass

Let \(f\) be the density of the nonzero absolutely continuous component, so that \(\mu\ge f\,dx\,dy\). By restricting to a bounded rectangle, truncating at a finite height, and applying a positive affine change of coordinates, we may choose a measurable function \(h\) such that
\[
 0\le h\le M<\infty,\quad
 \operatorname{supp}h\subset[0,1]\times[-L,L],\quad
 \int h>0,\quad \mu\ge h\,dx\,dy.                                  \tag{3}
\]
The last measure inequality, rather than equality, is all that is used. Here and below changes on Lebesgue-null sets do not affect the measure inequality.

For \(t\in\mathbb R\) and \(\delta>0\), put
\[
 g_t(x)=h(x,x^2+t),\qquad
 G_{t,\delta}(x)=\frac1{2\delta}
      \int_{-\delta}^{\delta}h(x,x^2+t+s)\,ds,\quad 0\le x\le1.
\]
For almost every fixed \(x\), the one-dimensional Lebesgue differentiation theorem applied to the vertical section \(y\mapsto h(x,y)\) gives convergence of its centered averages for almost every center \(y\). The substitution \(y=x^2+t\) preserves one-dimensional measure in the center variable. Fubini therefore gives, for almost every \(t\),
\[
 G_{t,\delta}(x)\longrightarrow g_t(x)
 \quad\text{for almost every }x\quad(\delta\downarrow0).
\]
Both functions lie between zero and \(M\), so dominated convergence on \([0,1]\) strengthens this to
\[
 \|G_{t,\delta}-g_t\|_{L^1[0,1]}\longrightarrow0.                    \tag{4}
\]
This holds for the full limit \(\delta\downarrow0\), not just a subsequence.

Meanwhile, a change of vertical variable and Fubini give
\[
 \int_{\mathbb R}\int_0^1g_t(x)\,dx\,dt=\int h>0.
\]
There is thus a single \(t\) for which (4) holds and \(\int g_t>0\). Fix it, write \(g=g_t\), and choose \(\beta>0\) such that
\[
 E=\{x\in[0,1]:g(x)\ge\beta\},\qquad m=|E|>0.                      \tag{5}
\]
Only existence of this trace and the full-limit convergence is needed. No density is asserted to be continuous on the parabola or on an open set.

## 3. Many separated intervals with adequate strip mass

For an integer \(N\), partition \([0,1]\) into \(N\) consecutive intervals \(I_j\) of length \(1/N\). Endpoints can be assigned either way for integration. Set
\[
 \delta_N=\frac1{4N^2},\qquad G_N=G_{t,\delta_N}.
\]
By (4), for every sufficiently large \(N\),
\[
 \|G_N-g\|_1\le\frac{\beta m^2}{16}.                               \tag{6}
\]
Call an interval E-heavy if
\[
 |E\cap I_j|\ge\frac{m}{2N}.
\]
The other intervals together carry at most \(m/2\) of the measure of E. The E-heavy intervals carry at least \(m/2\), and each interval has measure at most \(1/N\). There are therefore at least \(mN/2\) E-heavy intervals.

An E-heavy interval has \(\int_{I_j}g\ge\beta m/(2N)\). If it fails the additional condition
\[
 \int_{I_j}G_N\ge\frac{\beta m}{4N},                                \tag{7}
\]
then it consumes more than \(\beta m/(4N)\) of the L1 error in (6). At most \(mN/4\) E-heavy intervals can fail (7). At least \(mN/4\) intervals satisfy both conditions. At least half of these have the same parity of index, so there are at least \(mN/8\) suitable intervals no two of which are adjacent. This parity argument also handles rounding of noninteger bounds.

Given \(n\), take
\[
 N=\left\lceil\frac{8n}{m}\right\rceil.
\]
For all sufficiently large \(n\), (6) applies and we can choose \(n\) nonadjacent intervals satisfying (7). Also
\[
 N\le\frac{9n}{m}.                                                  \tag{8}
\]
For each selected interval form the Borel strip
\[
 A_j=\{(x,y):x\in I_j,\ |y-x^2-t|\le\delta_N\}.
\]
They are disjoint and have a full interval-width separation in the x direction. By (3) and (7),
\[
 \mu(A_j)\ge\int_{A_j}h
 =2\delta_N\int_{I_j}G_N
 \ge\frac{\beta m}{8N^3}
 \ge\frac{\beta m^4}{5832n^3}.                                     \tag{9}
\]
The chosen intervals and strips may depend on \(n\), but the constants \(t,\beta,m\) were fixed first, independently of \(n\).

## 4. Convexity and the probability bound

For three points taken from distinct selected strips, let their abscissae be \(x<y<z\). Both consecutive gaps are at least \(1/N\). Translation by \(t\) cancels out of the orientation determinant. The same exact determinant computation as in Turn 1 gives
\[
 D\ge(z-x)\left((y-x)(z-y)-2\delta_N\right)
   \ge\frac{z-x}{2N^2}>0.                                         \tag{10}
\]
Thus every transversal of the selected strips is in strictly convex position. Independence and the \(n!\) disjoint label-to-strip assignments give
\[
 p_\mu(\mathrm{conv}_n)
 \ge n!\prod_j\mu(A_j)
 \ge n!\left(\frac{\beta m^4}{5832n^3}\right)^n.
\]
This proves (1), with the explicit choice
\[
 b_\mu=\frac{\beta m^4}{5832}>0.                                    \tag{11}
\]
It is important that the bad-interval estimate loses only a fixed fraction of the intervals. Demanding every interval be good would require an unjustified rate of convergence in (4).

## 5. Positive probability of every finite type

The nonzero absolutely continuous component also implies full finite-type support, without quantitative bounds uniform in the type.

Choose a measurable set \(A\) of positive finite area and \(\eta>0\) with \(f\ge\eta\) on A. Fix any realization of a simple \(k\)-point order type inside the unit disk. Choose pairwise disjoint small open disks \(B_1,\ldots,B_k\), all inside that disk, such that every transversal has the chosen type. Let \(q=\min_i|B_i|>0\).

At a planar Lebesgue density point \(z\) of A, choose \(r>0\) so small that
\[
 |B(z,r)\setminus A|<\tfrac12 q r^2.
\]
Each disk \(z+rB_i\) then intersects A in area at least \(q r^2/2\), and consequently has positive \(\mu\)-mass. Independent sampling one point in each of them has positive probability and realizes the prescribed type. This argument works separately for each finite type.

Hence \(\min_{\omega\in\mathcal O_n}p_\mu(\omega)>0\). Combining (1) with the self-contained Turn 1 bound
\(T_n\ge1024(n!)^3/128^n\) and \(\min p\le1/T_n\) proves (2).

## 6. What this turn resolves and what remains

The open-set lower-density condition of Turn 1 is removed completely for measures with a nonzero absolutely continuous component. Bounded truncation is taken below the original measure, so adding an arbitrary singular component does not invalidate the proof. A density supported on a positive-area nowhere-dense set is included.

The argument also supplies a rigorous replacement for the specific continuity inference in the cited area-regularity lemma. The source was correctly credited for the target convex-position scale; its conclusion was never refuted. The repair is quantitative enough to give the n^n ratio scale because the single good trace is selected before taking the large-sample limit.

The remaining unrestricted class is **purely singular, line-null measures**. The earlier zero-type observation removes those omitting a finite type; purely singular measures assigning positive probability to every finite type are still allowed and remain untreated. Qualitative approximation of such a measure by absolutely continuous measures is not enough: \(b_\mu\) and the threshold are not uniform and can deteriorate along the approximation.

Even inside the class handled here, no threshold uniform in all measures has been proved. The source's size-quantifier ambiguity must therefore remain visible. The original universal problem is not solved.

Completion estimate toward the unrestricted original target: **20%**, subjective. Current author count **2/5**. A third turn should examine genuinely singular full-support measures or a mechanism giving constants uniform under a useful decomposition; repeating qualitative smoothing is not a new route.
