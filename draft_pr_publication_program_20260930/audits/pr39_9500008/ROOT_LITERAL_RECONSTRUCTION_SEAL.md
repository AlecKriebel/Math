# Root literal scope and preliminary reconstruction: PR39

Sealed before reading PARTIAL.md, its old review, or sibling interpretations.
The complete literal source/prior report, original turn-route descriptions,
PR body, and source URL/checksum list were already exposed and are disclosed.
The route descriptions name rotation and Brownian modulus; this root record
does not claim independence from those hints. Two fresh families reconstruct
their distinct mechanisms independently under stricter exposure conditions.

The author-maintained Problem8 defines two-sided Brownian motion by existence
of a finite real random time S such that X(S+t)-X(S) and X(S-t)-X(S), t>=0,
are independent standard Brownian motions. It does not require S to be a
stopping time or to equal the distinguished junction0. The stopped path-duration
pairs are independent, need not be identically distributed, satisfy0<=T_k<c
for one deterministic finite c, and their sums diverge in each direction.
Zero durations are permitted; divergence makes every bounded time window
reachable after a finite number of pieces. Fixed-junction bias cannot disprove
the existence of another admissible random origin. The source still presents
the problem as open; that presentation is dated evidence, not a priority proof.

An independent direct reconstruction of the proposed approximation is possible
without counting pieces. Concatenate the negative stopped paths in the outward
order -1,-2,... while keeping each path's original forward direction, yielding
G(s), s>=0. The standard concatenation/strong-Markov lemma says G has Brownian
law; only the independent stopped-path pairs are needed, not independence of
unused Brownian futures. Independently use the positive concatenation as W(t),
t>=0, and set W(-s)=-G(s). Then W has fixed-origin two-sided Brownian law.

Write a=sum_{j<n}T_{-j}, T=T_{-n}, s=a+u with0<=u<=T. With E the sum of
the earlier stopped endpoints, original backward position and comparison are
X(-s)=-E-B_T+B_(T-u) and W(-s)=-E-B_u. Hence their difference is
B_u+B_(T-u)-B_T. All three times lie in the same G block, of duration<c.
Consequently |X(-s)-W(-s)|<=2 M_c(R+c) for0<=s<=R, where M_c(H) is
the largest Brownian increment over pairs of times in[0,H] separated by<=c.
At positive times X=W. Endpoint and zero-duration cases agree by continuity.

Cover time by deterministic windows[jc,(j+2)c]. Any pair separated by<=c
lies in one such window. Its oscillation is bounded by twice the Brownian
supremum relative to the left endpoint. The reflection principle and Gaussian
tail yield P(M_c(H)>z)<=4(floor(H/c)+2)exp(-z^2/(16c)). c>0 is forced
by the hypotheses. On H=exp(n)+c, take z=K sqrt(n), K sufficiently large
depending on c; Borel–Cantelli and monotonic interpolation give
M_c(R+c)=O(sqrt(log R)) almost surely. This avoids an invalid union bound
over potentially very many tiny stopped pieces, and handles non-iid pieces.

For each finite A, a^(-1/2) sup_{|t|<=aA}|X(t)-W(t)| tends to0 almost
surely. Brownian scaling of W then supplies a two-sided Brownian scaling limit
in the topology of uniform convergence on compact time intervals. This law
statement does not assert that the scaled W paths converge almost surely.
Piecewise rotation changes X; it supplies neither exact equality after one
global time shift nor the finite random origin required by the original problem.

These deductions are preliminary hypotheses for audit. The concatenation lemma,
primary piece-rotation attribution, original exact theorem/notation, source
versions, complete original computational receipts, native accounting, and
all original proofs remain to be read and actually checked. No full solution
or novelty claim is made, and no new search for the missing random shift occurs.
Original authored budget2/5; audit/new substantive attempts0. No paper/DOI.
