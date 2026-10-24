# Parent recheck of the rank-five homology countermodel

Date: 2026-10-24T21:56:14.564682+00:00. This is a second mathematical inspection plus reproduction of the author's standalone exact verifier; it is not the fresh independent cocycle review requested from the separate adversary.

I inspected the finite-cover construction and the complete certificate verifier. The 64-vertex graph is an ordinary connected covering of the five-petal rose; every edge permutation is bijective. The exact positive substitutions for theta^8 have the same endpoints as their initial generators at every vertex. Since theta is an automorphism and the lifted map fixes the based subgroup by inclusion at the same finite index, L is preserved with equality. Thus K=<L,t^8> has index64*8=512.

For each of the9 integer edge cochains, the verifier checks all320 positive-edge differences against a vertex coboundary. Consequently their integrals on loops are theta^8-invariant, and each extends to an integer homomorphism on the semidirect product by sending t^8 to0. The18distinct target loops (19labels) are followed with actual signed-edge lifts; the a1^2 loop has value1. The formula x -> a1^(2lambda(x)) is therefore a homomorphism K -> <a1^2> restricting to identity on that subgroup. Its use requires no unsupported homology-rank computation.

I reran `verify_cocycle_certificate.py` against the exact index512 certificate; all2880 cell identities and19 target evaluations passed, saved as `homology/parent_index512_reproduction.json`. This proves that a1 and these finitely many other words do not supply the proposed universal invisibility obstruction. It does not prove specialness, virtual RFRS, or visibility of every element. The independent fresh review remains distinct and should also be preserved.

Certificate SHA256: `f76017a86b8255f64fc7d521651c088685b860bc369090efbc79419dbc5284fc`.
