# Turn 3: rational networks realize 5p² for every prime p≡3 mod4

Substantive author turn **3/5**, 2026-10-02. **Scoped theorem:** for every prime p≡3 mod4, there is a prime alternating achiral knot of determinant 5p². This removes the infinite obstruction to the integer-only wheel construction in turn2. The arbitrary determinant target remains unresolved. No historical novelty is certified; planar duality, the checkerboard knot construction and classical quadratic-ring arithmetic are credited tools.

## 1. Two-terminal networks with exact prescribed counts

For a finite connected plane network N with distinct terminals s,t on its outer face, let T(N) count spanning trees and let S(N) count spanning forests with exactly two components, one containing each terminal. A single edge has counts (1,1).

Adding one edge in parallel between the terminals changes (T,S) to (T+S,S). Adding an edge in series at a terminal changes it to (T,T+S). These identities follow by separating trees according to whether the new edge is used. Repeated subtraction in the Euclidean algorithm therefore proves:

**Network lemma.** Every coprime positive pair (u,v) is realized exactly as (T,S) by a plane two-terminal series-parallel network N(u,v). Every edge and vertex of this network lies on a simple terminal-to-terminal path.

Indeed, reverse the subtractions (u,v)↦(u−v,v) or (u,v−u) until (1,1). In the first case add a parallel edge when reversing the step; in the second add a series edge. The terminal-path property is preserved by each operation.

The two-terminal plane dual N* is obtained by adding a temporary edge between the terminals through the outer face, taking the planar dual, and deleting the dual temporary edge; its endpoints become the dual terminals. Spanning-tree complementation in the temporarily closed graph gives

    T(N*)=S(N),   S(N*)=T(N).

For these series-parallel networks the same operation interchanges series and parallel composition, starting from a single edge. In particular N* also has the terminal-path property. Dualizing twice recovers the initial embedded network up to the natural endpoint choice.

## 2. Paired substitutions preserve the needed knot properties

Use the plane wheel and orientation-preserving duality proved in turn1. On each spoke s_i substitute N(u_i,v_i), and on its paired rim edge r_{−i} substitute the two-terminal dual N(u_i,v_i)*, with the attachment order prescribed by the base duality. The edge ribbons are disjoint. Duality of an embedded graph commutes with this replacement: taking the dual replaces a network by its two-terminal dual in the paired ribbon. Thus the resulting plane graph is self-dual.

It remains connected without cut vertices. For removal of an old vertex, the surviving wheel vertices remain connected, and all surviving components in an incident network contain its other terminal: the terminal-path property rules out a component attached only at the removed vertex. For removal of an internal network vertex, every component of that network still contains at least one terminal, again by the terminal-path property. Those terminals remain joined through the rest of the wheel. Hence the entire remaining graph is connected. There are no loops; each network edge is on a terminal path which closes to a cycle through the rest of the wheel, so there are no bridges.

Consequently its alternating medial diagram is reduced and prime. If the spanning-tree count is odd, it is a knot, and the prime alternating diagram theorem makes the knot prime. Plane self-duality gives achirality. These last implications use exactly the established checkerboard facts recorded in SOURCE_SCOPE and turn1; the graph argument has verified all their hypotheses.

## 3. Substitution normalization and the exact polynomial

For an arbitrary base graph G with edge networks N_e, a spanning tree of the expanded graph restricts inside each network either to a spanning tree or to a two-terminal separating forest. A component containing neither terminal could not connect to the rest of the graph, and there cannot be more than two components. Collapsing the connected choices therefore gives a base spanning tree. Conversely each such choice yields a unique expanded tree after independently choosing the internal trees/forests. Thus

    τ(expanded G)=Σ_{B a base spanning tree} ∏_{e∈B}T(N_e) ∏_{e∉B}S(N_e).  (7)

Apply (7) to the paired wheel. Set (a,b,c,d)=(u_0/v_0,u_1/v_1,u_2/v_2,u_3/v_3) and D=v_0v_1v_2v_3. Let F,H be turn2's multilinear polynomials. Then

    τ = (D F(a,b,c,d))² + (D H(a,b,c,d))².        (8)

Indeed, factoring all forest counts in (7) gives a prefactor ∏u_iv_i and spoke weights u_i/v_i, with reciprocal weights on paired rim edges. Turn2's weighted determinant formula has prefactor ∏(u_i/v_i), so the ratio of prefactors is D². Both DF and DH are integers because F and H have degree at most one in each variable. This accounts for all internal vertices and prevents a spurious scaling of the determinant.

Two specializations of (8) suffice.

**Positive definite specialization.** For coprime u,v>0, take

    (a,b,c,d)=(u/v, 1, v/u, 1).

Then D=uv, DF=u²+uv+v² and DH=2(u²+uv+v²). The determinant is

    5(u²+uv+v²)².                               (9)

**Indefinite specialization.** For coprime integers x,t with x>0 and |t|<x, take

    (a,b,c,d)=(1, x/(x−t), 1, x/(x+t)).

Both fractions have positive coprime numerator and denominator. Here D=(x−t)(x+t). Substitution gives

    DF=3x²−t²,    DH=2(3x²−t²),

so the determinant is

    5(3x²−t²)².                                 (10)

## 4. Arithmetic covering every prime p≡3 mod4

The prime p=3 is obtained from u=v=1 in (9). Every other such prime is either7 or11 modulo12.

### 4.1 Primes7 modulo12

Let ζ=(1+i√3)/2. The ring Z[ζ] has norm N(u+vζ)=u²+uv+v². It is norm-Euclidean: after dividing two elements, round both real basis coefficients to the nearest integers. The remainder ratio has coefficients r,s with |r|,|s|≤1/2, hence its norm r²+rs+s²≤3/4<1. Therefore the Euclidean algorithm supplies unique factorization and irreducible elements are prime.

Since p≡1 mod3, the multiplicative group of the field F_p has an element r of order3 (equivalently use the standard cyclicity of the multiplicative group of a finite field). Then s=−r solves s²−s+1=0 modulo p. Thus p divides (s−ζ)(s−conjugate(ζ)) in Z[ζ], but does not divide either factor: its ζ coefficient is ±1. It follows that p is not irreducible in this Euclidean ring. In a nontrivial factorization p=αβ, the positive integer norms multiply to p²; neither is1, so N(α)=p.

Multiply α by a suitable unit ζ^j to put its argument between0 andπ/3. In the basis (1,ζ) its coefficients u,v are then nonnegative integers. A boundary argument would make the norm a perfect square, impossible for p, so both are positive. They are coprime since a common divisor would have its square divide p. Consequently p=u²+uv+v² with coprime u,v>0, and (9) applies.

### 4.2 Primes11 modulo12

The ring Z[√3] with absolute norm |N(t+x√3)|=|t²−3x²| is also Euclidean. Rounding both basis coefficients gives an error with |r|,|s|≤1/2 and |r²−3s²|≤3/4<1. Thus it has unique factorization.

The integer3 is a square modulo p. For completeness, Gauss's lemma computes (3/p) from the number of integers i in1,…,(p−1)/2 for which the least positive residue of3i exceeds p/2. That number is floor(p/3)−floor(p/6); for p=12j+11 it equals2j+2 and is even. Hence a square root r of3 exists modulo p. As above, p divides (r+√3)(r−√3) but neither factor, so p has a nontrivial factor α=t+x√3 with |N(α)|=p. Its norm cannot be +p: modulo3 every value of t²−3x² is0 or1, whereas p≡2 mod3. Therefore

    t²−3x²=−p.                                  (11)

The remaining positivity condition is important. Change the sign of α if necessary so that x>0. Equation(11) implies |t|<√3x. Multiplication by the norm-one units2±√3 preserves integer coefficients and the norm. If t≥x, use

    (t,x) ↦ (2t−3x, 2x−t).

The new x is positive since t<√3x<2x, and is strictly smaller than x: equality t=x would imply p=2x², impossible for odd p. If t≤−x, use

    (t,x) ↦ (2t+3x, 2x+t),

whose second coordinate is again a positive integer strictly smaller than x. Repeat as long as |t|≥x. The positive integer x strictly decreases, so the procedure terminates with |t|<x. The coefficients are coprime because a common divisor would have its square divide p. Formula(10) now applies.

This completes the proof for every prime p≡3 mod4. The classical Euclidean-ring and finite-field ingredients are proved or explicitly identified above; no assertion about prime values of a quadratic polynomial is used.

## 5. Examples and precise remaining gap

- p=7: (u,v)=(1,2) in (9), determinant245
- p=11: (x,t)=(2,1) in (10), determinant605
- p=23: (x,t)=(3,2) in (10), determinant2645
- p=59: (x,t)=(5,4) in (10), determinant17405

The last two cases lie beyond the source's reported n≤2000 finite verification; that comparison is not a claim of new priority. The determinant605, missed by the integer-only family, illustrates why turn2 was only an obstruction to that family.

The theorem does not cover arbitrary odd composite m in5m² by these two specializations, nor general n=g²h with a primitive sum-of-squares core h≠5. For example a product of primes from the two different congruence cases need not have the same norm type as either factor. No multiplicative closure preserving primeness and alternation has been established. Connected sum would multiply determinants but lose primeness, so it does not fill this gap. Original target unresolved3/5.
