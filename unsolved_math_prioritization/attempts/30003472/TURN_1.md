# Turn 1: a quantitative area-domination case

Problem 30003472 / OWR-15427-014. Substantive author turn **1 of 5**.
Status: **partial; the original problem remains unresolved**.

## 1. Scope and result

Let \(\mathcal O_n\) be the realizable, simple, **unlabeled**, orientation-preserving planar order types on \(n\) points, and let \(T_n=|\mathcal O_n|\). For a Borel probability measure \(\mu\) charging no line, put
\[
p_\mu(\omega)=\Pr\{\text{the order type of }X_1,\dots,X_n\text{ is }\omega\},
\qquad X_i\stackrel{\mathrm{iid}}\sim\mu.
\]
The samples are distinct and in general position almost surely: a point has measure zero because it lies on a line; conditioning on two distinct samples makes their joining line a null set.

**Area-domination hypothesis.** There is an orientation-preserving nonsingular affine map \(F\) such that its pullback probability measure \(\nu\) satisfies
\[
 \nu(A)\ge a\,|A|\qquad(A\subset[0,1]^2\text{ Borel})                  \tag{1}
\]
for a constant \(a>0\). Necessarily \(a\le1\). Equivalently, \(\mu\) dominates a positive multiple of normalized area on a parallelogram. The measure need not be globally absolutely continuous. In particular, a density that is continuous and positive at one point suffices.

**Theorem.** Under (1), for every \(n\ge3\), all order types have positive probability and
\[
 \frac{\max_{\omega\in\mathcal O_n}p_\mu(\omega)}
      {\min_{\omega\in\mathcal O_n}p_\mu(\omega)}
 \ \ge\ 1024\left(\frac{a n}{2048e^4}\right)^n
 \ >\ 1024\left(\frac{a n}{165888}\right)^n.                         \tag{2}
\]
The convex-position type itself can replace the maximum in this bound. Thus, for every fixed \(c>1\), the desired strict \(c^n\) comparison holds whenever \(n\ge3\) and \(n>165888c/a\).

The numerical constant is deliberately crude. The useful feature is the \(n^n\) factor. The threshold depends on \(\mu\) through \(a\). Neither arbitrary line-null measures nor a threshold uniform over those measures is covered.

## 2. A self-contained counting lower bound

Write \(L_j\) for the number of labeled simple order types on labels \(1,\dots,j\). Every simple realization can be perturbed, without changing its order type, so that:

* no two distinct lines determined by pairs of points are parallel;
* three such lines are concurrent only when all three pairs share an endpoint;
* distinct intersections of disjoint pairs of these lines are distinct unless forced by a common original point.

These requirements exclude finitely many proper algebraic hypersurfaces from the nonempty open realization set. The exceptional concurrency equations are nonidentically zero: one can move an endpoint unique to a line, while the three-edge triangle case is already nonconcurrent in general position. The star case is the stated unavoidable exception.

The arrangement of the \(\binom j2\) joining lines then has
\[
 R_j=1+\binom j2+j(j-2)+3\binom j4
     =\frac{j^4-6j^3+23j^2-26j+8}{8}                                \tag{3}
\]
regions. Indeed, for an affine line arrangement the region count is
\(1+\#\text{lines}+\sum_v(m_v-1)\), where \(m_v\) is intersection multiplicity. The original \(j\) points have multiplicity \(j-1\); every other vertex uses four distinct original points, and each four-set produces three ordinary vertices. Formula (3) also holds for \(j=2,3\).

Placing point \(j+1\) in distinct open regions gives distinct extensions of the labeled order type: a region is precisely a nonempty simultaneous strict-sign cell for the joining lines. Distinct base types remain distinct after extension. Consequently
\[
 L_{j+1}\ge R_jL_j,\qquad L_2=1.                                    \tag{4}
\]
For \(j=2+t\), \(t\ge0\), direct expansion gives
\[
 128R_j-(j+1)^4=15t^4+20t^3+122t^2+308t+175>0.                      \tag{5}
\]
Thus
\[
 L_n\ge\prod_{j=2}^{n-1}\frac{(j+1)^4}{128}
       =\frac{(n!)^4}{16\,128^{n-2}}.
\]
An unlabeled type accounts for at most \(n!\) labeled types, regardless of its automorphism group. Therefore
\[
 T_n\ge\frac{L_n}{n!}
       \ge\frac{1024(n!)^3}{128^n}.                                \tag{6}
\]
This is the familiar \(n^{3n+O(n)}\) lower-counting mechanism with an explicit convenient constant, not a claim of a new counting theorem. The classical recursion is also discussed in the primary literature listed in SOURCE_GATE.md.

## 3. Convex-position probability by curved strips

Affine invariance reduces the proof to \(\nu\) on the unit square. Fix \(n\ge3\), set
\[
 \delta=\frac1{16n^2},\qquad
 I_i=\left[\frac{i-1}{n}+\frac1{4n},\frac{i-1}{n}+\frac3{4n}\right]
 \quad(1\le i\le n),
\]
and define pairwise disjoint curved strips
\[
 A_i=\{(x,y):x\in I_i,\ |y-x^2|\le\delta\}.
\]
They lie in the unit square: the smallest possible \(x^2-\delta\) is zero, and the largest possible \(x^2+\delta\) is
\(1-1/(2n)+1/(8n^2)<1\). Each has area
\[
 |A_i|=\frac1{2n}\,2\delta=\frac1{16n^3}.                            \tag{7}
\]
Take one point from each strip and order them by increasing \(x\). For any three of these points with abscissae \(x<y<z\), write their ordinates as \(x^2+e_x,y^2+e_y,z^2+e_z\), with \(|e_\cdot|\le\delta\). Both consecutive abscissa gaps are at least \(1/(2n)\). Their orientation determinant equals
\[
 (y-x)(z-x)(z-y)+e_x(z-y)-e_y(z-x)+e_z(y-x).
\]
It is at least
\[
 (z-x)\big((y-x)(z-y)-2\delta\big)
 \ge\frac{z-x}{8n^2}>0.                                            \tag{8}
\]
Hence all triples, in increasing-abscissa order, turn the same way. All selected points are vertices of their convex hull: each consecutive edge has every other point strictly on the same side, so these edges form the lower convex chain; the endpoint edge closes the polygon.

By (1), \(\nu(A_i)\ge a/(16n^3)\). There are \(n!\) disjoint assignments of the \(n\) iid sample labels to the strips, and independence gives
\[
 p_\mu(\mathrm{conv}_n)
 \ge n!\prod_i\nu(A_i)
 \ge n!\left(\frac{a}{16n^3}\right)^n.                              \tag{9}
\]
Boundary overlaps are not an issue: the strips have separated abscissa intervals.

Finally every simple order type admits a positive-affine rescaling into the square. Small disjoint open neighborhoods of its points preserve every orientation and have positive \(\nu\)-mass by (1). Thus every \(p_\mu(\omega)>0\). Since the probabilities sum to one,
\[
 \min_\omega p_\mu(\omega)\le1/T_n.
\]
Multiplying (6) and (9) yields
\[
 \frac{p_\mu(\mathrm{conv}_n)}{\min_\omega p_\mu(\omega)}
 \ge 1024(n!)^4\left(\frac{a}{2048n^3}\right)^n.
\]
The elementary bound \(n!\ge(n/e)^n\), obtained by comparing \(\sum_{k=1}^n\log k\) with \(\int_1^n\log x\,dx\), proves (2). The strict final comparison uses \(e<3\).

## 4. Other immediate cases, and what they do not settle

If \(\mu\) gives positive mass \(b\) to a Borel set whose every finite distinct subset is in convex position, then
\(p_\mu(\mathrm{conv}_n)\ge b^n\). Combining with (6) proves an even larger asymptotic ratio whenever the minimum is positive; if the minimum is zero the strict target comparison is immediate. This includes measures with positive mass on a strictly convex arc. This elementary observation is not a treatment of arbitrary curve-supported measures.

If any \(k\)-point type has probability zero, extend one of its realizations to every \(n\ge k\). The extension also has probability zero, since realization would force some \(k\)-subset to realize the forbidden type; a finite union of null events remains null. Some other \(n\)-type has positive probability. The target is therefore automatic in this case. The difficult regime can be restricted to measures assigning positive probability to every finite realizable simple type.

## 5. A tempting amplification route does not yet work

Partition \(6m\) sample labels into \(m\) fixed blocks of six. Their restrictions are independent, so two fixed block words can have probability ratio exceeding \(1.8208^m\), by the known six-point bias. These are events in the **labeled block experiment**, not individual unlabeled \(6m\)-point types.

For a full unlabeled type \(\Omega\), let \(K_\Omega(w)\) be the fraction of labelings whose designated block restrictions equal the word \(w\). Then
\[
 \Pr(w)=\sum_{\Omega\in\mathcal O_{6m}}p_\mu(\Omega)K_\Omega(w).
\]
A large ratio of these two sums need not imply a large ratio of the coefficients \(p_\mu(\Omega)\), because the sums of the kernels for the two words need not be comparable. Even under equal coefficients, an imbalance in the kernel totals can produce a large event ratio. A valid amplification theorem would need an additional, quantitative, measure-independent comparison of these fibers or another mechanism. We have not proved it.

## 6. Exact remaining gap and next test

The area-domination condition is a genuine restriction. Absolute continuity alone does not immediately imply (1), and general line-null measures may be singular with full order-type support. The source's unquantified \(n\) also leaves a uniform-versus-measure-dependent threshold distinction; this turn proves only a \(\mu\)-dependent threshold in its stated class.

A later turn should either remove the area-domination hypothesis through a valid quantitative approximation argument, or find a different universal statistic/fiber comparison. Qualitative weak convergence alone will not transfer the displayed large-\(n\) bound with a fixed constant: the approximating measure and its domination constant can depend on \(n\).

Completion estimate toward the unrestricted original target: **10%**, a subjective planning estimate. No full solution or novelty claim is made.
