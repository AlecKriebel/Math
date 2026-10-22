# Attempt 1: Galois detection and a dimension bound

## Exact target

For an irreducible ordinary character χ of a finite group G, p∤χ(1), and P∈Syl_p(G), let c(χ)=p^a m, p∤m. Is p∤[Q_(p^a):Q(χ_P)]? Here Q_n=Q(ζ_n), and the conductor is the least positive n containing the field, not the exponent of the representation.

This is Navarro–Tiep's Conjecture C (2021), restated as Navarro's Conjecture A in OWR 39/2022, p.2276. It is not the separate question for arbitrary character degrees on the following page.

## Field reduction

Let E=Q(χ_P). If exp(P)=p^b, then E⊆Q_(p^b)∩Q_(p^a m)=Q_(p^min(a,b)). Thus the index in the question is defined. Cases a≤1 are automatic, since [Q_p:Q]=p−1. For p=2 a=1 cannot occur for a minimal conductor.

For odd p and a≥2, Gal(Q_(p^a)/Q) is cyclic. Its unique order-p subgroup fixes Q_(p^(a−1)). Consequently failure is equivalent to E⊆Q_(p^(a−1)), or to an order-p Galois automorphism fixing every value on P. Equivalently the restriction has lost the top conductor level. For p=2 the desired index must be 1. Having conductor 2^a alone is insufficient: Q(√2) has conductor 8 and index 2 in Q_8.

These reductions are the established starting point, not a resolution. The following bounded-dimensional argument gives a genuinely complete special case without using irreducibility.

## Proposition: positive degree less than p

Let Ψ be any nonzero ordinary character of G with Ψ(1)<p. Then the target index is prime to p.

Proof. Factor out ker(Ψ) and let p^b be the exponent of the image of P in a representation affording Ψ. Since every nonlinear irreducible character of P has degree at least p, Ψ_P is a sum of linear characters, with total multiplicity d=Ψ(1)<p. Write E=Q(Ψ_P), so E⊆Q_(p^b).

Let S be a p-subgroup of Gal(Q_(p^b)/E). It permutes the linear constituents of Ψ_P, preserving their multiplicities. Any nontrivial orbit has at least p distinct constituents and hence contributes at least p to d. Therefore every constituent is fixed by S. The maximum of the orders of these constituents is p^b: the image of P is diagonal and its exponent is the least common multiple of those orders. Hence some constituent has order p^b, and its values generate Q_(p^b). It follows that S is trivial. Thus p∤[Q_(p^b):E].

If c(Ψ)=p^a m, then a≤b. Indeed the exponent of the finite image has p-part p^b, and every character value is a sum of roots whose orders divide this exponent. The preliminary field inclusion gives E⊆Q_(p^a)⊆Q_(p^b). Therefore [Q_(p^a):E] divides the already prime-to-p index. This proves the proposition, including b=0 and the Q_2=Q degeneracy. ∎

## Why the full argument stops

For d≥p+1 with p∤d, a complete Galois orbit of p high-order linear constituents can coexist with a single low-order fixed constituent. The p′-degree hypothesis alone does not prevent this. Attempt 3 supplies an exact ordinary-character family exhibiting the obstruction. Irreducibility must enter a stronger argument.

Status: proved special case χ(1)<p; no general proof or irreducible counterexample. No novelty or priority claim for this elementary proposition.
