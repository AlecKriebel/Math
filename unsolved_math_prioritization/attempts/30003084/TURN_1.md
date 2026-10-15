# Author turn1: small complex configurations and a Fermat-family obstruction

**Partial result. No counterexample and no general complex theorem.** The first route tested the natural small Hesse/Fermat configurations suggested by the source context. Exact interpolation finds ordinary conics in all four fixed configurations. A uniform elementary argument then excludes the full three-coordinate-line Fermat family from being a counterexample.

## 1. Exact finite test

Use Q(omega), omega²+omega+1=0. A field element is represented as a+b omega with rational a,b. The locally authored checker uses exact arithmetic and row reduction of the degree-two evaluation vector

    (x²,y²,z²,xy,xz,yz).

For every five-subset, rank5 means its conic is unique up to scalar. The checker computes its one-dimensional kernel, normalizes the coefficient vector, and tests all points. Rank below5 is not called an ordinary conic. Rank6 of the full point evaluation matrix verifies that the entire point set is not on a conic. All conics, including singular unions of lines, are included.

Only four fixed classical-type configurations were tested, not a combinatorial search over arbitrary point sets:

- Hesse9: (0,1,-r),(-r,0,1),(1,-r,0), r in {1,omega,omega²}
- Dual-Hesse12: the three coordinate vertices and (1,r,s), r,s in {1,omega,omega²}
- Fermat18: the Hesse formula with r in {±1,±omega,±omega²}
- Hesse21: the union of the first two point sets

Results (distinct determined conics, not counts of their five-subsets):

- Hesse9: 54 conics contain exactly5 points; 12 contain6
- Dual-Hesse12: 36 contain5, 36 contain6, 36 contain7
- Fermat18: 702 contain5, 558 contain6, 108 contain8, 3 contain12
- Hesse21: 3276 contain5, 324 contain6, 252 contain7, 72 contain8, 102 contain9

Every full matrix has rank6. The exact receipts also give all five-subset rank counts, point coordinates and one explicit ordinary conic for each configuration. These are finite checked outcomes; they do not establish anything about arbitrary complex configurations or unseen larger examples.

The full enumeration covers126+792+8568+20349=29835 five-subsets. The largest fixed set has21 points. This is a modest exact interpolation check rather than a search through large families of candidate sets. Replay with `python explore_configurations.py hesse9 dual_hesse12 fermat18 hesse21`; the two saved JSONL receipts are the corresponding outputs grouped into two runs.

## 2. Every three-line Fermat configuration has ordinary conics

For n>=3 let mu_n be the group of n-th roots of unity and define

    P_n={(0,1,-r),(-r,0,1),(1,-r,0): r in mu_n}.

It has3n distinct points, none a coordinate vertex. It is not contained in a conic: each of the three coordinate lines contains at least3 points, so a conic through all of P_n would contain all three distinct lines as components, impossible in degree2.

Fix the point S=(1,-r,0) for r in mu_n. For t in mu_n let

    L_t: r x+y+t z=0.

It contains exactly3 points of P_n: S on z=0, (0,-t,1) on x=0 and (-t/r,0,1) on y=0. Their ratios lie in the prescribed root-of-unity sets. No additional point of P_n lies on L_t because L_t is not a coordinate line and has only one intersection with each coordinate line.

For distinct t,u, the two lines L_t and L_u intersect precisely at S. Their union is a conic with exactly3+3−1=5 points of P_n. It is uniquely determined by these five points: each line contains3 of them, so restriction of any quadratic form through them to either line has3 distinct zeros and vanishes identically. Both linear equations therefore divide the form, forcing it to be their product up to scalar.

The same construction works at every point of P_n by permuting the coordinates. At each of3n points it gives binomial(n,2) unordered pairs of lines. No conic is counted at two different such points because the intersection of its two distinct components is unique. Consequently

    P_n has at least 3n binomial(n,2)

ordinary (reducible) conics. This lower bound is not claimed sharp. For n=3 it yields27 of the54 found exactly; the coordinate lines themselves also have3 points in that special case and supply further pairs.

This is an elementary Bezout/line-restriction consequence for a classical configuration family, not a novelty claim. It explains why the complex Sylvester–Gallai counterexamples from roots of unity do not automatically provide conic counterexamples.

## 3. Remaining target and next route

The original complex Wiseman–Wilson question remains unresolved after one substantive author turn. The argument does not require ordinary lines in the whole set; it constructs a union of two3-point lines meeting at a configuration point. A counterexample must avoid this mechanism as well as all ordinary irreducible conics.

The next route is a small-cardinality/general interpolation argument, using the geometry of the Veronese evaluation matroid rather than continuing a blind search over larger configurations. Four substantive author turns remain unless a full result is obtained sooner. Completion estimate20%, representing ruled-out routes and a proved special-family result, not a claimed probability of general resolution.
