# Equal-width three-stripe audit, proof attempt 1

Scope: the coloring is c_w(x,y)=floor(x/w) modulo 3, with w>0 and half-open strips. Only authored analysis and public citations appear here. No general resolution of Graham's conjecture is claimed.

## Results

1. The proposed sufficient condition improves from h>L/2 to h>=L/2, where L is longest side and h=2 area/L is minimum width. Take w=L/2 (or any L/2<=w<=h).
2. This is not new territory: stronger sufficient stripe conditions occur in Aichholzer–Perz, Theorems 3.1–3.2. In side notation a<=b<=L, width w=h works if b<=2h, or if the triangle is nonobtuse and a>=L/2.
3. An exact, finite, rational-arithmetic decision test for each specified rational triangle and rational w is supplied below and in `stripe_exact.py`. It handles tangencies correctly.
4. The tempting extension “take w=h for every triangle” is false, by an explicit rational example below. This example does NOT establish that every width fails for that triangle.
5. A necessary-and-sufficient criterion for existence of a successful width is a complement-of-open-intervals formula below. An explicit lower cutoff for potentially good widths makes this a finite decision procedure, albeit with very crude complexity. It is not a simplified geometric classification. We have not proved that success at some width implies success at w=h.

## Elementary sufficient proof and boundary

The minimum projection span of a nondegenerate triangle is its minimum altitude h. This familiar polygon-width fact follows by varying the projection direction: within each interval with fixed support vertices the width is a positive cosine-linear function, so its minimum occurs at an endpoint where a support line contains a side. The three resulting widths are the three altitudes.

A monochromatic triple in a single strip has projection span strictly less than w, impossible if w<=h. Points in distinct strips of the same color have projection separation strictly greater than 2w: the smallest index difference is 3, and the open upper edge of the lower strip excludes equality. Thus if 2w>=L, no two vertices can occupy distinct same-color strips. These two observations prove the first result, including h=L/2.

A stronger elementary argument uses the second-longest side b. If w<=h and b<=2w, any hypothetical monochromatic triangle must occupy at least two strips. Its strip partition is either 2+1 or 1+1+1. In either case there are at least two distinct cross-strip edges, each longer than 2w. Hence the second-longest side would exceed 2w, a contradiction. Thus b/2<=w<=h suffices. This recovers the k=3 case of the published Theorem 3.1, rather than constituting a novel result.

For example T={(0,0),(1,0),(1/2,2/5)} has L=1, h=2/5<1/2, but b=sqrt(41)/10<4/5=2h. It is avoided by width 2/5. So h>=L/2 is not necessary even for this stripe scheme.

## Exact congruence/projection criterion

Translate one vertex to 0 and let the other two be independent vectors B,C. Let

G = [[B·B,B·C],[B·C,C·C]], Q(z)=z^T G^(-1) z.

As a unit projection direction u varies, the pair z=(u·B,u·C) traces exactly the ellipse E={Q(z)=1}. Reflections do not enlarge this set, so full Euclidean congruence is covered.

Let H be the open hexagon

H = {(r,s): |r|<1, |s|<1, |r-s|<1}.

The triangle has a monochromatic congruent copy in c_w if and only if, for some integers m,n,

E intersects w((3m,3n)+H).                                    (1)

Proof: after subtracting the strip index of the first vertex, the other two same-color strip indices are 3m and 3n. A common translation can place all three points in these strips exactly when the spread of the three residual coordinates 0,z_1-3mw,z_2-3nw is strictly less than w. That is precisely the three strict inequalities defining H. Conversely, a residual spread less than w lets us translate the smallest residual to 0; all residuals then lie in [0,w). This proves both directions, including boundary cases. Boundary-only contacts cannot yield monochromatic copies.

Let K_mn=(3m,3n)+closure(H), and define

alpha_mn=min_{z in K_mn} Q(z), beta_mn=max_{z in K_mn} Q(z).

Then (1) is equivalent to

w^2 alpha_mn < 1 < w^2 beta_mn.                              (2)

Indeed, strict inequalities at the closed extrema produce two interior points on opposite sides of the ellipse by continuity, and their connecting segment is interior. Conversely, an interior ellipse point has nearby interior points with Q below and above 1 because the gradient of a positive definite quadratic is nonzero on Q=1. Equality at either extremum is not enough.

For a fixed w, only finitely many m,n need testing:

3|m|w < |B|+w, and 3|n|w < |C|+w.

These follow directly from the projection bounds and the open hexagon coordinates. A safely larger finite box is harmless.

For rational input coordinates and w all calculations in (2) can be exact rational arithmetic. The maximum of Q is at one of the six vertices. The minimum is 0 if the origin is in K_mn (only m=n=0); otherwise it is on an edge. On edge p+t d, the minimizing parameter is the clipping to [0,1] of -p^T G^(-1)d/(d^T G^(-1)d). The script implements these formulas, not angular sampling.

## Exact width-set characterization

For each integer pair define the open interval

I_mn=(1/sqrt(beta_mn), 1/sqrt(alpha_mn)),

where 1/sqrt(0)=+infinity. The bad widths are exactly the union of these intervals. Therefore a successful equal-width three-stripe coloring exists exactly when

(0,h] minus union_{m,n in Z} I_mn

is nonempty. The restriction w<=h is necessary: for w>h a rotated triangle fits strictly into one strip. The origin hexagon alone excludes precisely w>h, consistent with beta_00=1/h^2. Endpoints of one forbidden interval are not automatically good; other intervals must also be checked.

This criterion depends only on the Gram matrix, hence on the triangle's side lengths up to relabeling and scale. Initially its union is countable. The following cutoff makes it finite. No claim is made that sampling finitely many arbitrary widths settles the existential problem, or that the sufficient published conditions are necessary.

## Quantitative cutoff: the existential stripe problem is finitely decidable

Put

a=|B|, k=(B·C)/a^2, d=sqrt(|C|^2−(B·C)^2/a^2)>0,

epsilon=min(a/13, d^2/[52a(|k|+4)^2]).

Every width 0<w<=epsilon fails. To prove this, put R=1/w and scale the ellipse so that its equation is Q(x,y)=R^2, while the hexagons now have fixed size and centers 3Z^2. The upper branch of the ellipse is

y(x)=kx+d sqrt(R^2−x^2/a^2).

Choose m=floor((aR−3)/3) and x0=3m. Then delta=aR−x0 belongs to [3,6). For x in J=[x0−1/2,x0+1/2], the distance aR−x lies in [5/2,13/2). Because R>=13/a, we have x>=aR/2>0; J lies strictly inside the ellipse's horizontal domain. Moreover

sqrt(R^2−x^2/a^2) <= sqrt(13R/a).

Consequently, throughout J,

y'(x)=k−d x/[a^2 sqrt(R^2−x^2/a^2)]
      <= |k|−d sqrt(R)/[2 sqrt(13a)] <= −4,

where the last inequality follows from R>=52a(|k|+4)^2/d^2. The image y(J) has length at least 4, and hence its interior contains a multiple 3n. At the corresponding interior point x, the displacement from (3m,3n) is (r,0) with |r|<1/2. It belongs strictly to H. The scaled ellipse thus intersects a forbidden open hexagon, proving the claim, with no asymptotic or equidistribution assumption.

It now suffices to consider epsilon<w<=h. For all these widths at once, the only potentially relevant pairs satisfy

3|m|epsilon < |B|+epsilon, 3|n|epsilon < |C|+epsilon.

One may safely include their boundary integers or a larger box. This is a finite box. Compute alpha and beta for each pair and remove the corresponding open bad intervals from [epsilon,h]. The resulting set is exactly the successful widths (epsilon itself is known bad). This is a finite exact necessary-and-sufficient shape test. For rational coordinates all extrema are rational and the cutoff is algebraic, so all endpoints and comparisons are exactly decidable. The bound can be computationally enormous for flat triangles and is not an efficient implementation claim.

The supplied script implements the efficient fixed-width part only, not this potentially enormous all-width search. In particular we have not executed the all-width search on the flat counterexample below, and cannot infer that it has no successful width from its failure at w=h.

## Explicit rational failure of maximal width

Let T={(0,0),(1,0),(1/2,1/10)} and w=h=1/10. Take the rotation with first row (3/5,4/5), and translate x by 1/100. The three projected coordinates become

1/100, 61/100, 39/100.

Their strip indices are 0,6,3 respectively, all color 0 modulo 3. All three lie strictly inside their strips, so the counterexample is not a boundary artifact. Rotation preserves the full triangle and therefore gives an actual congruent copy, not merely a projected surrogate.

The exact test finds, among others, the hexagon (m,n)=(2,1) with alpha=25 and beta=136. Since (1/10)^2*25<1<(1/10)^2*136, this independently certifies failure.

## Verification

Run `python3 stripe_exact.py`.

`stripe_exact_results.json` records five rational checks: equality case h=L/2 passes; a case h<L/2 passes; the explicit flat triangle fails at w=h; the 3–4–5 right triangle passes at w=12/5; and a width just above h fails through the origin hexagon. These checks audit the implementation; the arguments above supply the general proofs.

## Prior work and novelty limitations

- Graham and Tressler, *Open Problems in Euclidean Ramsey Theory*, manuscript p.2, already state that alternating three-color half-open strips avoid many but not all triangles. https://mathweb.ucsd.edu/~ronspubs/10_14_euclid.pdf
- Aichholzer and Perz, *Triangles in the colored Euclidean plane*, EuroCG 2019, Section 2.1 and Theorems 3.1–3.2, give the stronger sufficient conditions cited above. Their work is explicitly an extended abstract/preprint. The nonobtuse result is reported here as their theorem; its omitted detailed proof was not independently reconstructed in this audit. https://www.eurocg2019.uu.nl/papers/10.pdf

The local recovered PDFs and their text were inspected, and the public PDF URLs were reopened with web tools on 2026-10-20. No copied source is included. The ellipse/hexagon test is derived here; no novelty priority claim is made. This work does not establish the original all-triangle conjecture and should not be used to mark it solved.
