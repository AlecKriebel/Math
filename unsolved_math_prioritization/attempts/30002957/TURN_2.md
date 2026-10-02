# Turn2: a quantitative missing-face event in every nontrivial dimension

Substantive author turn **2/5**. Retain turn1's homogeneous-Poisson, simplex-intensity convention. For every d≥k≥2, the fraction theta_{d,k} is strictly less than1. The proof supplies an explicit, albeit very small, lower bound on the intensity of flag k-simplices which are not Delaunay. It does not compute the fraction or prove monotonicity in d.

Let κ_d be the volume of the Euclidean unit ball. Set

    h=1/(1000d²),    R=10d,    N=2d−k+2,
    eta_{d,k}=2^{−d} exp(−κ_d R^d)(2h)^{dN}.      (8)

At unit Poisson intensity, with a_{d,k},b_{d,k} as in turn1,

    b_{d,k}−a_{d,k} ≥ eta_{d,k}>0,
    theta_{d,k} ≤ a_{d,k}/(a_{d,k}+eta_{d,k})<1.  (9)

The same fraction holds for every positive Poisson intensity by scaling. The numerator a_{d,k} is the credited Delaunay intensity constant; equation(9) does not pretend to evaluate the denominator.

## 1. Sites and pairwise empty-ball witnesses

In R^d let

    a_0=0, a_i=e_i (1≤i≤k),
    b=(1/(k+1))Σ_{i=1}^k e_i,
    g_r^+=2e_r, g_r^−=−2e_r (k<r≤d).

There are N distinct sites: k+1 proposed clique vertices, one blocking point b, and2(d−k) guards. Coordinates beyond the first k are zero except for the guards.

Every pair of proposed clique vertices has a sphere through it excluding all other sites strictly:

- For(a_0,a_i), use center c_i with coordinate i equal to1/2, each other coordinate among1,…,k equal to−1, and remaining coordinates0. Its squared radius is k−3/4.
- For(a_i,a_j), i,j>0 and i≠j, use center c_{ij} with coordinates i,j equal to2, each other coordinate among1,…,k equal to−2, and remaining coordinates0. Its squared radius is4k−3.

For the first type, the squared-distance-minus-radius-squared margins are3 at another vertex,4 at any guard, and(2k²−3)/(k+1)² at b. For the second type, they are3 at a_0,8 at another proposed vertex,7 at a guard, and(7k²−5k−13)/(k+1)² at b. For every k≥2, all these margins are at least5/9. The endpoint equalities are immediate from their coordinates.

## 2. Uniform robustness under coordinate perturbations

Allow each site to move by at most h in every coordinate. Denote perturbed sites by primes. The estimates below apply to **every** such perturbation, not just finitely sampled corners.

For each pair u,v and its original center c, put w'=v'−u' and project c onto the perturbed perpendicular bisector:

    c'=c + [ (||v'||²−||u'||²−2c·w')/(2||w'||²) ]w'.       (10)

Originally||v−u||≥1, so||w'||²≥1/2 since2h√d≤1/4. The numerator in(10) has absolute value at most12dh: the two endpoint squared-norm errors contribute at most5h and the center-dot-product error at most8dh. Therefore

    ||c'−c||_infinity ≤24dh,    ||c'||_infinity≤3.          (11)

Here h is far below all the elementary thresholds used in these inequalities.

For any other site z, its original l1-norm is at most2, and the endpoint u has l1-norm at most1. Comparing its perturbed squared-distance gap with the original one gives an error at most

    7h +2(24dh)·3 +12dh ≤160dh ≤2/25.           (12)

The three terms respectively bound the two squared-norm changes, the center displacement paired with z−u, and the perturbed displacement paired with c'. Since2/25<5/9, every named sphere remains empty of every other selected site. Its radius is at most5√d by(11) and the endpoint bound, so its whole closed ball lies in B(0,8√d)⊂B(0,R).

Thus once all unselected Poisson points are excluded from B(0,R), every pair of the perturbed a_i is a Delaunay edge. The perturbed vertices remain affinely independent: the first k coordinates of(a_i'−a_0') form an identity matrix plus a perturbation whose maximum row-sum norm is at most2kh<1.

## 3. The guards prevent an escaping circumsphere

We must show that the entire clique is not a Delaunay k-face. In positive codimension it is insufficient merely to put one point near the affine interior: a circumcenter could escape far in a normal direction. This is why the guards are needed.

Suppose a center y is equidistant from all a_0',…,a_k' and its ball excludes every perturbed guard. Put M=max_j|y_j|. The vertex equalities give, for1≤i≤k,

    |2y_i−1| ≤3h+4dhM,
    |y_i−1/2| ≤(3/2)h+2dhM.                   (13)

Indeed a_i'−a_0'=e_i+u_i with||u_i||_infinity≤2h, while||a_i'||²−||a_0'||² differs from1 by at most3h. For r>k, applying the empty-ball inequality to both guards gives

    |y_r|≤1+(5/4)h+dhM.                       (14)

Their difference vectors are±2e_r plus a coordinate error at most2h, and their squared-norm differences from a_0' differ from4 by at most5h. Equations(13)–(14) imply

    M≤1+2h+2dhM,    hence M≤2.                 (15)

In particular |y_i−1/2|≤5dh for i≤k. If k=d, there are no guards and the vertex equations alone give the same bound.

Now compare the squared distances of b' and a_0' to y. Without perturbation of sites or the first k center coordinates, their difference is

    ||b||²−2(1/2,…,1/2)·b = −k²/(k+1)².

The perturbation error is at most20dh: at most3h comes from squared norms,10dh from(13) at the first k coordinates, and8dh from the perturbed difference b'−a_0', using M≤2. Thus

    ||b'−y||²−||a_0'−y||²
       ≤−k²/(k+1)²+20dh <0.                  (16)

The inequality is strict since k≥2 and20dh≤1/100. Hence the blocking point b' is inside every candidate ball satisfying the vertex equalities and guard exclusions. No empty circumsphere through the k+1 vertices exists. This proves the non-Delaunay claim for all permitted perturbations.

## 4. Poisson event and intensity lower bound

Take the open coordinate cube of side2h about each of the N sites. They are disjoint, since the smallest possible separation in maximum norm is1/(k+1)>2h. They lie in B(0,R). Require exactly one Poisson point in each cube and no other point in B(0,R). At unit intensity this event has probability exactly

    exp(−κ_d R^d)(2h)^{dN}.                   (17)

Points outside B(0,R) cannot spoil the strict pairwise witnesses, and they cannot repair the obstruction(16). Almost surely the selected vertices are in the usual general position. Their barycenter lies in Q=(−1,1)^d. Thus there is at least one non-Delaunay flag k-simplex counted in Q on this event. Turn1's stationary counting formula gives

    (b_{d,k}−a_{d,k})2^d ≥ P(event),

which is(8)–(9).

## 5. What has and has not been answered

For the chosen simplex-typical convention, k=0,1 have fraction1, while every2≤k≤d has a fraction strictly between0 and1. In particular, the Delaunay complex is almost surely not recovered exactly by filling every graph clique. The latter almost-sure statement can also be obtained by the positive-intensity ergodic process of missing faces; it is not necessary for the numerical bound(9).

This does not show that the fractions decrease with ambient dimension or compute their values. The explicit gap is a robust certification, not a useful numerical estimate: its size is extremely small. A general formula for the clique denominator and sharper quantitative behavior remain open. Original unresolved2/5.
