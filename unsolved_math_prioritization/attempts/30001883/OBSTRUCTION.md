# Circle-free parallel bodies: an exact clearance reduction and the remaining gap

**Target 30001883 / OWR-11136-008.** The original question remains unresolved. Two bounded approaches were attempted. The deductions and diagnostic below are scoped partial results, pending separate review. No novelty claim is made.

## 1. The actual meaning of circle-free

In Hiroshi Maehara's [OWR contribution, printed pp. 2498–2499](https://ems.press/content/serial-article-files/46358), a circle is a **rigid circular ring**, not a disk and not a flexible loop. A circle $\Gamma$ holds a convex body $K\subset\mathbb R^3$ when it avoids $\operatorname{int}K$, its disk meets $\operatorname{int}K$, and no continuous rigid motion can take it away while continuing to avoid $\operatorname{int}K$. Boundary contact is permitted. The radius cannot change during the motion. A body is circle-free if no circle holds it.

The question asks whether $K+B_r$ is circle-free whenever $K$ is, where $B_r$ is a Euclidean closed ball of radius $r$. Translation invariance lets us center the ball at zero. The case $r=0$ is immediate. Throughout, a convex body is compact, convex and has nonempty interior, as explicitly specified in [Maehara–Martini, p. 273](https://ems.press/content/serial-article-files/44350). The lower-dimensional set in the known planar special case is denoted separately by $X$.

That later primary survey defines escape through continuous congruent motions in the complement of the body's interior, ending at a circle whose **disk** is disjoint from the body. This is equivalent to escape arbitrarily far: two disjoint compact convex sets, the disk and body, can be strictly separated, after which translation away from the separating plane continues the escape.

The later survey allows an initially attached disk merely to touch $K$. This does not enlarge the holding class: if a disk misses $\operatorname{int}K$, convex separation places it on one side of a supporting plane of $K$, and translation away from that plane frees the circle.

No assertion about absence of circular arcs on $\partial K$ is relevant to this problem.

## 2. Parallel addition raises the required clearance

Write $K_r=K+B_r$, and let

$$h_K(u)=\max_{x\in K}u\cdot x,\qquad
 s_K(y)=\max_{u\in S^2}\bigl(u\cdot y-h_K(u)\bigr). \tag{1}$$

The function $s_K$ is continuous and 1-Lipschitz. Outside $K$ it is the Euclidean distance to $K$; inside it is minus the distance to $\partial K$. In particular $K=\{s_K\le0\}$ and $\operatorname{int}K=\{s_K<0\}$.

For the outside assertion, project $y$ to a nearest point $x\in K$. The unit vector $(y-x)/|y-x|$ supports $K$ at $x$, so equality with the distance follows; the reverse bound follows from Cauchy–Schwarz. Inside $K$, the largest ball about $y$ contained in $K$ has radius $\min_{u\in S^2}(h_K(u)-u\cdot y)$, which is the distance to the boundary. These arguments also cover boundary points by continuity.

Since $h_{K_r}(u)=h_K(u)+r$, formula (1) gives the exact identity

$$s_{K_r}(y)=s_K(y)-r. \tag{2}$$

Fix a ring radius $R>0$ and a reference circle $\Gamma_R$. For a rigid-motion configuration $g$, define

$$\phi_{K,R}(g)=\min_{y\in g\Gamma_R}s_K(y). \tag{3}$$

This function is continuous. Equations (2)–(3) imply

$$g\Gamma_R\cap\operatorname{int}K_r=\varnothing
 \quad\Longleftrightarrow\quad \phi_{K,R}(g)\ge r. \tag{4}$$

Thus the allowed configuration set for $K_r$ is the **level-$r$ superlevel set** of the same clearance function whose level-zero superlevel set describes avoidance of $K$.

Circle-freeness supplies escape paths at level zero. The unanswered step is to supply escape paths at every positive level, starting at every admissible attached configuration at that level. Connectedness alone would not suffice: the source uses actual continuous rigid-motion paths, and we make no identification of connected and path components for arbitrary convex bodies. Similarly, a supremum of bottleneck clearances would not establish a boundary-level path unless attainment were proved.

A bounded endpoint formulation is exact. If $K\subset B_L(0)$, then a circle center $c$ with $|c|>L+r+R+1$ has its entire disk separated from $K_r$ and can be translated farther away. Hence it suffices to find an actual path in (4) to that exterior region. This reformulation does not prove that such a path exists.

## 3. Necessary geometry of a hypothetical holding circle after thickening

The following reduction is valid for every convex body, without assuming circle-freeness.

**Proposition.** Suppose $r>0$ and a circle of radius $R$, center $c$ and plane $P$ holds $K_r$. Then

1. $P$ meets $\operatorname{int}K$;
2. $R>r$;
3. $K\cap P$ is contained in the concentric planar disk of radius $R-r$;
4. the concentric circle of radius $R-r$ is attached to $K$ and avoids $\operatorname{int}K$.

**Proof.** If $P$ misses $\operatorname{int}K$, convexity puts all of $K$ in one closed halfspace bounded by $P$. Translate the circle in the normal direction away from that halfspace. For each circle point and each $x\in K$, the squared distance is the sum of an unchanged tangential squared distance and a nondecreasing normal squared distance. Since the initial distances to $K$ are at least $r$ by (4), the translated ring continues to avoid $\operatorname{int}K_r$. Eventually its disk is disjoint from $K_r$. This contradicts holding and proves (1).

Let $D$ be the disk bounded by the original circle. Because $D$ meets $\operatorname{int}K_r$ and its boundary avoids that interior, convexity implies

$$K_r\cap P\subset D. \tag{5}$$

Indeed, choose a point of $\operatorname{int}K_r\cap\operatorname{int}_P D$. If a point of $K_r\cap P$ lay outside $D$, the segment joining them would cross the circle at an interior point of $K_r$, which is forbidden.

For every $x\in K\cap P$, the planar radius-$r$ disk about $x$ lies in $K_r\cap P$. Equation (5) therefore gives

$$|x-c|+r\le R. \tag{6}$$

The section $K\cap P$ has nonempty relative interior by (1), so (6) forces $R>r$ and proves (3). Its interior points lie strictly inside the radius-$(R-r)$ disk. No point of that smaller circle can lie in $\operatorname{int}K$, since a planar neighborhood of such a point would contradict (6). This proves (4). $\square$

If $K$ is circle-free, the smaller ring furnished by the proposition has some escape path from $K$. The proposition does **not** show that expanding the circles along that path by $r$ yields a valid escape from $K_r$. The next exact diagnostic demonstrates the failure of that inference.

## 4. A ball diagnostic invalidating the naive radial lift

This example is **not a counterexample to the question**. Both bodies are balls and are circle-free. It shows only that one cannot take an arbitrary escape path of the smaller ring and enlarge every ring radius by $r$.

Let $K=B_1(0)$, $r=1/5$, and use horizontal circles centered on the $z$-axis. Begin with the outer ring of radius $R=1$ at height

$$z_0=\frac{\sqrt{11}}5.$$

Its points have squared norm $1+11/25=36/25$, so it lies on $\partial K_r$. Its disk meets $\operatorname{int}K_r$. The concentric smaller ring has radius $R-r=4/5$ and is strictly outside $K$ initially, because

$$\left(\frac45\right)^2+z_0^2=\frac{27}{25}>1.$$

Move this smaller ring vertically down to height $z_1=3/5$, then vertically up to height 2. This is a continuous rigid escape from $K$: every height on the path is at least $3/5$, and

$$\left(\frac45\right)^2+\left(\frac35\right)^2=1.$$

The final disk lies in $z=2$ and is disjoint from $K$. Now enlarge every circle along this path by $r$, leaving its center and plane unchanged. At the initial and final configurations the enlarged circle is admissible, but at height $3/5$ its squared norm is

$$1+\left(\frac35\right)^2=\frac{34}{25}<\frac{36}{25}=(1+r)^2.$$

It lies strictly inside $K_r$, so the lifted path is invalid. A different outer-ring path, translating directly upward from $z_0$, does escape; this is why the example does not disprove circle-freeness after Minkowski addition.

## 5. What a positive-clearance certificate does prove

**Proposition.** Let $g(t)\Gamma_R$, $0\le t\le1$, be a continuous fixed-radius escape path from $K$. Suppose its rings are all disjoint from $K$ itself, including its boundary, and its final disk is disjoint from $K$. Then there is $\delta>0$ such that this same path is an escape from $K_r$ for every $0\le r\le\delta$.

**Proof.** Compactness of $[0,1]\times\Gamma_R$ and $K$ gives a strictly positive minimum ring clearance $\delta_0$. The final disk and $K$ are disjoint compact sets, so their distance $d_1$ is also positive. Choose $\delta=\min(\delta_0,d_1/2)$. Equation (4) keeps the whole path outside $\operatorname{int}K_r$ for $r\le\delta$, and $d_1>r$ keeps the final disk disjoint from $K_r$. $\square$

This is a certificate for a **specified path**, not a uniform theorem about every admissible ring. The source permits contact with $\partial K$, so an arbitrary source-allowed escape can have $\delta_0=0$. Even a family of positive-clearance paths would need a suitable uniform lower bound to settle the global Minkowski question.

## 6. A credited positive class

Maehara's theorem in the original report states that $X+B_s$ is circle-free for every nonempty planar compact convex set $X$ and every positive-radius ball $B_s$. It is also recalled in [Maehara–Martini, p. 278](https://ems.press/content/serial-article-files/44350), with attribution to *Holding a regular pyramid by a circle*, J. Geom. **102** (2011), 133–147, [DOI 10.1007/s00022-012-0104-8](https://doi.org/10.1007/s00022-012-0104-8).

Therefore the question has a positive answer for the whole full-dimensional class

$$K=X+B_s,\qquad s>0,$$

because

$$(X+B_s)+B_r=X+B_{s+r}.$$

This includes balls, capsules formed from a segment and a ball, and rounded planar plates. It is a direct consequence of the credited theorem, not a new result. The theorem's complete original journal proof was not obtained; the claim is recorded explicitly in both retrieved primary accounts. It does not say that every circle-free convex body has this representation.

## 7. Exact research gap

Two routes were investigated:

1. **Transfer of escape motions through parallel addition.** The support-function/clearance formulation and Section 3 reduction are valid. The missing step is a positive-level escape theorem; Section 4 refutes the unrestricted radial-path-lifting shortcut.
2. **A counterexample based on circle-free pyramids at known holding thresholds.** The primary literature classifies several polyhedral trunks and regular pyramids. After adding a positive-radius ball the body is no longer a polyhedron, and that classification does not certify a holding ring or classify all possible escape motions. No admissible counterexample with a verified circle-free input and a verified held parallel body was obtained.

Neither local contact calculations, a failure of a proposed escape motion, nor the ability of a ring to move a little determines whether it can escape globally. No numerical motion search is presented as such a certificate.

The original question remains **unsolved, 2/5**. The artifact supplies an exact reformulation, necessary geometry, a failure diagnostic for one proposed proof route, and the already-known stable subclass. It neither proves the positive-level escape statement nor constructs a counterexample to it. All source and novelty qualifications should remain attached to these conclusions.
