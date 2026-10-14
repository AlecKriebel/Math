Scope: an authored mathematical partial result for the exact two-dimensional king-move Time-Bomb game. The unrestricted conjecture is not resolved. No novelty claim is made. Original contract SHA-256: 1be42b4f13460a91a71948fc532c135b7453f56811566ed5c3f918f8976c5c4c.

## 4. Nonlinear bad centers can also inflate mass

For a finite set B of preloaded terminal bomb positions, consider a state with exactly two Angel moves remaining until that common terminal time and no other lethal time. The Devil may make one new terminal announcement after observing the first of these two moves.

Write

A_8(B)={q: |N(q) intersect B|≥8},
E(C)={a: N(a) is a subset of C},

where N(x)=x+{−1,0,1}².

The exact set of losing starting centers is

L_2(B)=E(A_8(B)).

Indeed, after a first move to q the Devil can fill the last missing terminal neighbor if and only if at least eight of N(q)'s nine points are already bombed. The Angel loses from a precisely when every possible first move has this property. This is an exact online universal-response predecessor, not a sufficient-density surrogate.

Now take m≥2 and let

B_m = {0,...,3m−1}² minus { (x,y): x and y are both divisible by 3 }.

Then |B_m|=8m². Every 3×3 square wholly inside the large square contains exactly eight B_m points, because any three consecutive integers contain exactly one representative of each residue class modulo 3. It follows that A_8(B_m) contains {1,...,3m−2}², and hence L_2(B_m) contains {2,...,3m−3}². Therefore

|L_2(B_m)| / |B_m| ≥ (3m−4)²/(8m²),

whose limit is 9/8.

In particular, for all sufficiently large m this nonlinear losing-center map increases the number of occupied spatial positions. Uniform unweighted mass contraction is therefore unavailable even for this exact nonlinear operation. This agrees with, but is logically separate from, a 9/8 lower bound for local linear hazard certificates.

This is a statement about preloaded states. It does not assert that the Devil can force the initial unrestricted game into one of them. A useful invariant could still exploit the actual reachable Angel position, announcement history, or amortized cost of creating a large cluster.
