# Turn 2: collinear and thin-strip translation centers

Second substantive turn. Original unresolved. For every fixed planar convex body K and direction e, this turn proves a three-point transversal for any one color whose translation vectors lie in a sufficiently thin strip parallel to e. It also gives the exact piercing number for collinear translation vectors and a sharp two-point bound under the source cross-intersection hypothesis. This is a restriction on the configuration of translation vectors, not a new body class covering the full conjecture. Convex difference bodies, supporting lines and interval greedy covering are classical ingredients; no novelty is certified.

## 1. Translation-space duality

Write a color family as {K+t:t∈T}. A point q pierces K+t if and only if t∈q-K. Thus the family's piercing number is exactly the minimum number of translates of -K covering the finite set T. Also

    (K+t)∩(K+s)≠∅ iff t-s∈D:=K-K.                     (1)

Consequently, if some other nonempty color supplies one translate K+s intersecting every member of the chosen family, then T⊂s+D. We only use that single common intersecting translate; all further cross-color assumptions are unnecessary for the restricted theorem.

## 2. Exact collinear formula

Let e be a unit direction and let ℓ be the maximum length of a chord of K parallel to e. Equivalently ℓ=max{r≥0:re∈D}. This equivalence follows directly from re=a-b with a,b∈K. Suppose ℓ>0 and T⊂p+Re. The piercing number of {K+t:t∈T} equals the minimum number of closed intervals of length ℓ covering the scalar coordinates of T along that line.

Every translate of -K cuts the line in an interval of length at most ℓ, proving one inequality. Conversely a longest chord of -K exists by compactness, and translating it places it on any prescribed interval of length ℓ in p+Re, proving the other. The optimum is obtained greedily: cover the leftmost uncovered coordinate x by [x,x+ℓ], and repeat. Any cover's interval containing x has right endpoint at most x+ℓ, so replacing it by this interval cannot lose a point to its right. Induction proves optimality. Equivalently, the greedy leftmost points form a largest sequence with successive gaps strictly greater than ℓ.

If T⊂s+D as in(1), its span along its line is at most2ℓ. Indeed if u,v∈D and v-u=re, then (v-u)/2∈D by central symmetry and convexity, so r≤2ℓ. Two intervals of length ℓ cover that span. Therefore the chosen color can be pierced by at most two points.

This two-point constant is sharp for the chosen color, for every full-dimensional K: take translation vectors ±(3ℓ/4)e and let the other two colors each consist of K itself. Both vectors are in D, so all cross intersections hold. Their separation3ℓ/2 exceeds the longest chord length, so the chosen color's two translates are disjoint and need two points. The other colors have one-point transversals, as required; this is not a lower bound of two for the original existential conclusion. When ℓ=0, a line parallel to e cuts the centrally symmetric D in at most one point, so a collinear T⊂s+D is a singleton and needs at most one point.

## 3. A positive-width strip theorem for every body and direction

Now assume K has nonempty interior. Use coordinates (x,y) with e horizontal. The positive number ℓ from §2 is the x-coordinate of the right-hand endpoint of D∩{y=0}. Choose a supporting functional

    φ(x,y)=x+βy,     |φ(z)|≤ℓ for all z∈D.              (2)

It exists: a supporting line at (ℓ,0) has positive horizontal normal component because0 lies in the interior of D; normalize that component to1. Central symmetry gives the opposite inequality. The linear map A(x,y)=(φ(x,y),y) is invertible and preserves horizontal lengths.

There is a parallelogram P⊂-K such that A(P) is an axis-parallel rectangle of horizontal width a=3ℓ/4 and positive vertical height b. To see this, take a longest horizontal chord of -K and contract it by factor3/4 toward any interior point. The resulting closed segment lies entirely in the interior and has length a. It therefore admits a positive-thickness neighborhood in the direction (-β,1); this thickening is the required P. The constant b can be any sufficiently small positive value and depends only on K and e.

**Theorem.** If T⊂s+D and the y-coordinates of T lie in an interval of length at most b, then T is covered by three translates of -K, so {K+t:t∈T} is three-pierceable.

Indeed(2) puts A(T) in a rectangle of horizontal width at most2ℓ and vertical height at most b. Three adjacent translates of the a-by-b rectangle A(P) cover that rectangle because3a=9ℓ/4>2ℓ. Pull back by A. The resulting three translates of P⊂-K cover T, and translation-space duality gives the piercing points.

Thus for every fixed K and direction, a sufficiently thin strip of translation vectors is enough, uniformly over the number of translates and their positions along that strip. The strip can be anywhere in the plane. No common intersection of the chosen color is assumed. The constant b is not claimed uniform over all bodies or directions; it can degenerate in a sequence of shapes. Merely having a line transversal to the physical translates does not imply that their translation vectors lie in this narrow strip, so the known source line-transversal reduction does not finish the general conjecture through this theorem.

## 4. Exact polygon construction and finite verification

For a rational polygon and horizontal direction, all data can be chosen rational. Compute D from vertex differences and its convex hull. The endpoint(ℓ,0) and a supporting β follow from rational segment intersections and linear inequalities. A longest horizontal chord of -K occurs at a vertex height or on a flat interval of the piecewise-linear concave chord-length function. Contract it toward the average of the polygon's vertices. The average is an interior point for a full-dimensional polygon. The finitely many edge inequalities give a positive rational thickness for the parallelogram by taking the minimum endpoint slack divided by the absolute normal component in direction(-β,1), with a safety factor.

The checker implements these choices independently of sample translation sets, generates rational points of D in several strips of width b, constructs the three covering rectangles explicitly, and verifies all resulting piercing incidences exactly. It also compares collinear greedy interval counts with the arrangement-based minimum from turn1. Finite successful samples are controls for the construction; the all-size theorem follows from the written covering proof. Original unresolved2/5.
