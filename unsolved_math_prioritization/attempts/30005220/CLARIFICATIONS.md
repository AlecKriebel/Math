# Additive clarification after independent review

The ten frozen research files remain byte-for-byte unchanged. This note supplies
an explicit ambient field for the lifting argument in Attempt 3; it does not
change the claim or fill the unresolved general-case gap.

Write exp(P)=p^b, a≥2, E=Q(χ_P), and N=max(a,b). Restriction gives a surjection

    r: Gal(Q_(p^N)/E) → Gal(Q_(p^a)/E).

The kernel has p-power order. If S is a Sylow p-subgroup of the target, its
inverse image T=r^(-1)(S) is therefore a p-group and maps onto S. Every element
of T fixes the values of χ_P. The field Q_(p^N) contains the values of all
irreducible characters of P, so T acts on those characters and preserves their
multiplicities in χ_P.

If the total multiplicity of the order-p^a linear constituents is prime to p,
some constituent is fixed by the whole group T. That constituent generates
Q_(p^a), so S is trivial. This works for p=2 as well as for odd p; no cyclicity
of the binary Galois group is assumed.

The unresolved step is still to establish an appropriate top-conductor
survival statement for every irreducible p′-degree character. The review's
PASS concerns the partial packet only. The original problem remains unsolved.
