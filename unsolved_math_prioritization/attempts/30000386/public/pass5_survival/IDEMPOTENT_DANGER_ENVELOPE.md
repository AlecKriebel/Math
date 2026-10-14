# A sharp idempotent envelope for repeated eight-neighbor danger

Shared PASS5 structural result. The isolation argument was supplied by the invariant lane and developed jointly; this file supplies the full envelope, injection, sharpness, and update statements. This is not a solution of the Time-Bomb game.

Write N(x)=x+{-1,0,1}² and

T(B)={x: |N(x) intersect B|>=8}

for a finite spatial set B. The center belongs to its own nine-point neighborhood. Define the set of isolated holes

I(B)={x not in B: N(x)\{x} is a subset of B},

and put J(B)=B union I(B).

## 1. Exact closure and uniform iteration bound

**Theorem 1.** J is monotone, extensive, and idempotent. Moreover

T(B) is a subset of J(B),
T(J(B)) is a subset of J(B),
and |J(B)| <= (4/3)|B|.

Consequently, for every integer k>=0,

T^k(B) is a subset of J(B),
and |T^k(B)| <= (4/3)|B|.

Thus repeated T operations do not inherently incur the exponential factor (9/8)^k obtained by multiplying separate incidence bounds.

**Proof.** Extensivity is immediate. If B is a subset of D, an isolated hole of B either already belongs to D or still has all eight neighbors in D; hence J(B) is a subset of J(D).

If x is outside J(B), it is outside B and has a distinct king-neighbor y outside B. Because x and y are both absent and adjacent, neither is an isolated hole of B. Both therefore remain outside J(B). Every point outside J(B) still has an absent king-neighbor, so there are no new isolated holes after applying J. This proves idempotence.

A point in T(B) that is not in B must have all its eight distinct neighbors in B. It is an isolated hole. Hence T(B) is a subset of J(B), and applying this to J(B) proves T(J(B)) is a subset of J(B). Monotonicity of T gives the iteration claim.

Tile Z² into disjoint translates of {0,1}². Each tile contains at most one isolated hole, since two distinct points in a tile are king-neighbors. A tile containing an isolated hole contains three original B-points. These tiles are disjoint, so 3|I(B)|<=|B|. Adding |B| proves the cardinality bound. All sets counted are finite. ∎

## 2. Arbitrary interleaving with injections

**Corollary 2.** Start from a finite set B0. During any finite sequence of operations, either apply T or inject an arbitrary finite set D by replacing the current set X with X union D. Let S be the union of B0 and all sets injected during that sequence. Every intermediate state belongs to J(S). In particular, the union of every point occupied at any stage has cardinality at most (4/3)|S|.

**Proof.** The fixed set J(S) contains all seeds and is invariant under T. It therefore contains every intermediate state by induction. ∎

The union S counts distinct spatial seeds. The statement also gives an upper bound using the number of seed insertions with repetitions, since that count is no smaller. For an infinite process this statement applies to each finite prefix; it does not assert finite total occupancy if infinitely many distinct seeds are inserted.

## 3. The envelope constant is sharp

For m>=1 let Q_m={0,...,2m}². Remove the m² points whose two coordinates are odd, and call the remaining set B_m. Every removed point has all eight neighbors in B_m, and an outside point is not an isolated hole. Thus

J(B_m)=Q_m,
|B_m|=3m²+4m+1,
|J(B_m)|=(2m+1)².

The ratio tends to 4/3. The constant in the envelope bound cannot be improved.

This also proves sharpness for the ever-occupied union in Corollary 2: start from B_m and apply T once. The union of the initial state with T(B_m) is exactly J(B_m). It does not prove that 4/3 is the sharp constant for the cardinality of a single iterate T^k(B).

## 4. Exact one-seed update bound

**Theorem 3.** For any finite B and any point p,

|J(B union {p})\J(B)| <= 5.

The bound five is attained.

**Proof.** If p belongs to J(B), monotonicity and idempotence give J(B union {p})=J(B). Otherwise consider a new point x other than p in the displayed difference. It was outside B and not isolated there; after inserting p it has all eight neighbors present. Therefore x is a king-neighbor of p, and p was its only absent distinct neighbor in the original set B.

Two such new points cannot be king-neighbors of one another: otherwise each would have had an absent neighbor besides p. A king-independent subset of a side-three square has at most four points, as follows by partitioning that square into four rectangles of side lengths at most two. There are at most four such x, in addition to p itself.

For equality, take the side-five square {-2,...,2}² and remove its center and its four diagonal neighbors (±1,±1). Call the remaining twenty points B. None of the five missing points is isolated, and no outside point is isolated, so J(B)=B. Inserting the center makes all four diagonal holes isolated. The new envelope is the entire side-five square, a gain of five. ∎

## 5. Exact boundary of the method

The statements above concern one fixed spatial threshold operator and actual, successively supplied seed sets. They do not identify the game's exact robust Bellman predecessor with T or with an injection sequence of this form.

The game has multiple timestamp layers and a new announcement chosen after the Angel's move. In an exact backward game calculation, different candidate Angel moves may require different adversarial announcements. Taking the union of those responses is not one legal injection and does not retain the one-announcement budget. No such substitution is authorized by Corollary 2.

There is also a sharp obstruction to simply replacing T by J while charging one envelope site for each new bomb: Theorem 3 has a five-site gain from a single insertion. The earlier twenty seed sites pay for that local burst in the global 4/3 amortized envelope bound. A successful online game invariant would have to retain an appropriate shared resource account across timestamps and moves. This file does not construct that account or prove arbitrary bounded-lead survival.
