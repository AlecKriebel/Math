# Attempt 2: Clifford homogeneity and normal Sylow subgroups

The first orbit argument can be strengthened if all constituents have the same order, as happens for normal P. This recovers an established theorem (Navarro–Tiep 2021, Theorem 7.3) by an elementary proof.

## Proposition

If P is normal in G and χ∈Irr(G) has p′-degree, then p∤[Q_(p^a):Q(χ_P)], where p^a=c(χ)_p.

Proof. Clifford theory gives χ_P=e(λ_1+⋯+λ_t), where the λ_i are distinct G-conjugate irreducible characters of P. Their common degree divides χ(1), so it is 1. Also e and t are prime to p. All λ_i have the same order p^b.

Put E=Q(χ_P)⊆Q_(p^b). A p-subgroup S of Gal(Q_(p^b)/E) permutes the λ_i. Since t is prime to p, at least one λ_i is fixed by S. That character has order p^b, so its field of values is Q_(p^b); hence S=1. Therefore [Q_(p^b):E] is prime to p.

The image of P under a representation affording χ has exponent p^b. It is a Sylow subgroup of the finite image of G: a surjection maps a Sylow subgroup onto a Sylow subgroup. Thus the p-part of the exponent of that image is p^b. Every value of χ belongs to the cyclotomic field of that exponent, so a≤b. Since E⊆Q_(p^a), the target index divides [Q_(p^b):E]. ∎

No assertion that a=b is needed; this avoids degenerate rational cases where p^b can be p but the conductor has p-part 1.

## Two safe structural reductions

1. Faithful reduction. Replacing G by G/kerχ preserves χ's field and the field of its restriction to the image Sylow subgroup. Therefore a minimal counterexample can be taken faithful.

2. Direct products. If the conjecture holds for (G_1,χ_1,p) and (G_2,χ_2,p), it holds for χ_1⊗χ_2 on G_1×G_2. The global field is the compositum of the two global fields, since evaluation at (g,1) and (1,h) recovers each factor's values up to nonzero integer scalars. The same holds for the restriction fields. Their conductor p-parts have maximum p^a. Choose a factor with this maximal p-part; its restriction field E_i lies inside the product restriction field E, which itself lies inside Q_(p^a). The index [Q_(p^a):E] divides [Q_(p^a):E_i], and so is prime to p.

## Failed extension

When P is not normal, χ_P need not be homogeneous and its high-order linear constituents need not form a single G-orbit. The fixed constituent forced by the p′ total degree can have small order. Normalizing one constituent's inertia subgroup and applying induction would require controlling the top conductor under induction; Attempt 4 makes the available invariant precise.

Status: existing normal-Sylow case recovered; faithful/product reductions justified; no reduction of the whole problem to this case. The much larger p-solvable case is already due to Isaacs–Navarro (2024), and is not a new result here.
