# A six-period counterexample to the printed elliptic-billiard assertion k108

**5100002 / AMR-050-0002. Complete counterexample candidate; separate review pending.** One direct-coordinate approach. Historical priority is unconfirmed; no novelty or human peer-review claim.

## 1. Exact assertion and answer

Table2 of Reznik–Garcia–Koiller’s [arXiv v11](https://arxiv.org/abs/2004.12497v11), printed p.5, and Table2 of the [published paper](https://armj.math.stonybrook.edu/pdf-Springer-final/021-0174.pdf), p.345, both give

$$k_{103}=A'/A,\qquad k_{105}=\prod_{i=0}^{N-1}\sin(\theta_i/2),$$

and list $k_{108}=k_{103}/k_{105}$ as invariant when $N\equiv2\pmod4$. Here $A$ is the orbit’s signed area, $A'$ is the signed area of the outer polygon formed by consecutive tangent intersections, and $\theta_i$ is the internal angle at the orbit vertex. Both source tables were visually checked.

**This printed assertion is false.** Two convex, counterclockwise, primitive six-period billiard orbits in the same nondegenerate confocal ellipse pair give

$$k_{108}(P_H)=\frac{11664}{3125},\qquad
k_{108}(P_V)=\frac{3645}{1024}.$$

Their difference is $553311/3200000>0$. Thus neither star-polygon angle conventions, repeated odd periods nor signed-area cancellation is responsible for the failure.

## 2. One outer ellipse and one caustic

Use

$$E:\quad \frac{x^2}{4}+y^2=1,\qquad
E_c:\quad\frac{x^2}{32/9}+\frac{y^2}{5/9}=1.$$

The caustic parameter is $\lambda=4/9$, with $0<\lambda<1=b^2$. The two squared semiaxes decrease by the same amount, and their difference remains3, so the ellipses are confocal with foci $(\pm\sqrt3,0)$. The inner ellipse is strictly nested and nondegenerate.

Take the ordered orbit vertices

$$\begin{aligned}
P_H=\bigl(& (2,0),\ (4/3,\sqrt5/3),\ (-4/3,\sqrt5/3),\ (-2,0),\\
          &(-4/3,-\sqrt5/3),\ (4/3,-\sqrt5/3)\bigr),
\end{aligned}$$

and

$$\begin{aligned}
P_V=\bigl(& (0,1),\ (-4\sqrt2/3,1/3),\ (-4\sqrt2/3,-1/3),\ (0,-1),\\
          &(4\sqrt2/3,-1/3),\ (4\sqrt2/3,1/3)\bigr).
\end{aligned}$$

Every displayed vertex lies on $E$. Within each list the six vertices are distinct and occur in counterclockwise order, producing a convex hexagon.

### Chord tangency and reflection

It suffices to check representative sides and vertices, because reflection in either coordinate axis preserves the two ellipses and the billiard reflection law.

For $P_H$, the first slanted side lies on

$$x+\frac{2}{\sqrt5}y=2.$$

The squared support value of $E_c$ for this normal is

$$\frac{32}{9}+\frac59\frac45=4.$$

Its contact point is $(16/9,\sqrt5/9)$, one third of the way from $(2,0)$ to $(4/3,\sqrt5/3)$. The horizontal side is $y=\sqrt5/3$, tangent at $(0,\sqrt5/3)$.

At $(2,0)$ the incoming and outgoing unit vectors are $(2/3,\sqrt5/3)$ and $(-2/3,\sqrt5/3)$; their difference is normal to $E$. At $(4/3,\sqrt5/3)$ they are $(-2/3,\sqrt5/3)$ and $(-1,0)$; their difference equals $(1/3,\sqrt5/3)$, which is the outward normal $(x/4,y)$ there. Their outward-normal components have opposite signs, as required for ordinary specular reflection.

For $P_V$, the first slanted side lies on

$$-\frac{x}{2\sqrt2}+y=1.$$

Its squared support value is

$$\frac{32}{9}\frac18+\frac59=1,$$

and the contact point is $(-8\sqrt2/9,5/9)$, two thirds of the way along that side. The vertical side is $x=-4\sqrt2/3$, tangent at $(-4\sqrt2/3,0)$.

At $(0,1)$ the incoming and outgoing unit vectors are $(-2\sqrt2/3,1/3)$ and $(-2\sqrt2/3,-1/3)$. At $(-4\sqrt2/3,1/3)$ they are $(-2\sqrt2/3,-1/3)$ and $(0,-1)$. In each case their difference is a positive multiple of $(x/4,y)$ and their normal components have opposite signs. This verifies the remaining reflection types.

Thus both hexagons are genuine closed billiard trajectories, tangent to the same inner ellipse. Their six distinct successive vertices certify least period6. Both use the directed tangent branch with the caustic on the left. By the ordinary Poncelet porism for this ellipse pair, varying the starting point along $E$ gives the same six-period family, and these two orbits are members of it. This uses only the standard family premise of the original problem, not an additional proposed invariant.

The edge-length lists are

$$P_H:(1,8/3,1,1,8/3,1),\qquad
P_V:(2,2/3,2,2,2/3,2).$$

Both perimeters are $28/3$.

## 3. The outer polygons and areas

At $p=(p_x,p_y)\in E$, the tangent line is

$$\frac{p_x}{4}x+p_y y=1.$$

Solving the adjacent tangent pairs gives, in the corresponding cyclic order,

$$\begin{aligned}
Q_H=\bigl(& (2,\sqrt5/5),\ (0,3\sqrt5/5),\ (-2,\sqrt5/5),\\
          &(-2,-\sqrt5/5),\ (0,-3\sqrt5/5),\ (2,-\sqrt5/5)\bigr),
\end{aligned}$$

and

$$\begin{aligned}
Q_V=\bigl(& (-\sqrt2,1),\ (-3\sqrt2/2,0),\ (-\sqrt2,-1),\\
          &(\sqrt2,-1),\ (3\sqrt2/2,0),\ (\sqrt2,1)\bigr).
\end{aligned}$$

These are the source’s outer tangent polygons, not the polygons of caustic-contact points and not antipedals or pedal feet. All intersections are finite.

Applying the signed shoelace formula in the displayed orders yields

$$\begin{array}{c|cc|c}
 & A & A' & A'/A\\ \hline
P_H &20\sqrt5/9&16\sqrt5/5&36/25\\
P_V &32\sqrt2/9&5\sqrt2&45/32
\end{array}$$

All four areas are positive. As a consistency check, the already-known even-period area product takes the same value $AA'=320/9$ in both examples. No area-product theorem is needed for the counterexample; each area was computed directly.

## 4. Half-angle products and unequal k108 values

For incoming and outgoing unit edge vectors $e_-,e_+$ at a convex orbit vertex,

$$\cos\theta=-e_-\cdot e_+,\qquad
\sin(\theta/2)=\sqrt{\frac{1-\cos\theta}{2}}>0.$$

The two axial vertices of $P_H$ have $\cos\theta=-1/9$ and the other four have $\cos\theta=-2/3$. Hence

$$\prod_{i=0}^5\sin(\theta_i/2)
=\left(\frac{\sqrt5}{3}\right)^2
 \left(\frac{\sqrt{30}}6\right)^4
=\frac{125}{324}.$$

For $P_V$, the two axial vertices have $\cos\theta=-7/9$, and the other four have $\cos\theta=-1/3$. Thus

$$\prod_{i=0}^5\sin(\theta_i/2)
=\left(\frac{2\sqrt2}{3}\right)^2
 \left(\frac{\sqrt6}{3}\right)^4
=\frac{32}{81}.$$

These are ordinary internal angles in $(0,\pi)$, with no square-root sign ambiguity. Their cosine sums both equal $-26/9$, consistent with the source’s normalization $\sum\cos\theta_i=JL-N$, since $J=1/3$ and $L=28/3$.

The proposed invariant therefore takes the two values

$$\frac{36/25}{125/324}=\frac{11664}{3125},\qquad
\frac{45/32}{32/81}=\frac{3645}{1024},$$

which are unequal. This disproves the printed $N\equiv2\pmod4$ assertion at the admissible primitive period $N=6$.

## 5. Interpretation, credit and exact checks

For these two hexagons, the **product** $(A'/A)\prod\sin(\theta_i/2)$ happens to equal $5/9$. Together with the separate k107 investigation, this suggests checking whether the source’s parity/product assignments were exchanged. Two examples do not prove a repaired all-period statement. No such repaired theorem or official erratum is asserted here.

The symmetric six-bounce construction was already checked as an independent diagnostic in this campaign’s distinct k405 centroid review (ID5100023). The present proof recomputes all required geometry and the area/angle quantities; it does not depend on that centroid theorem or on k603’s focal-distance identity. The adjacent k107 investigation concerns a separate four-period product assertion. These related computations are not counted as independent discoveries of a common theorem.

The final checker uses exact rational and quadratic-radical arithmetic to verify every vertex, side contact, reflection, outer tangent intersection, area and half-angle factor. It also verifies all positive denominators, distinctness, orientation, least-period evidence, common caustic and the exact nonzero difference. It uses no floating-point trajectory simulation.

The full original and published source tables agree with the extracted target. Bounded current searches did not locate a published correction or a prior account of this counterexample, but this is not a proof of priority. The intended publication status is a separately reviewed counterexample to the **printed** k108 statement, with historical novelty unconfirmed.

### Sources

1. D. Reznik, R. Garcia and J. Koiller, [Eighty New Invariants of N-Periodics in the Elliptic Billiard](https://arxiv.org/abs/2004.12497v11), v11,29October2020. Introduction, Sections2–3.1 and Table2, printed p.5. Complete PDF and rendered table inspected.
2. D. Reznik, R. Garcia and J. Koiller, [Fifty New Invariants of N-Periodics in the Elliptic Billiard](https://armj.math.stonybrook.edu/pdf-Springer-final/021-0174.pdf), Arnold Mathematical Journal7 (2021),341–355, DOI10.1007/s40598-021-00174-y. Published Table2,p.345 visibly retains the same k108 quotient and parity.
3. H. Stachel, [On the motion of billiards in ellipses](https://link.springer.com/article/10.1007/s40879-021-00524-2), European Journal of Mathematics8 (2022),1602–1622. Used only to check conventions: its angle variable is an exterior turning angle, unlike the internal angle used above. No result from this paper is needed in the counterexample.
