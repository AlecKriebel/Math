# A path-RAAG word invisible to every free-group image

Checkpoint 2026-10-24T20:57:12.124420+00:00. Elementary route obstruction, not a solution of21.127 or a novelty claim. Fresh review requested.

Let G=A(P4)=<a,b,c,d | [a,b]=[b,c]=[c,d]=1>, with [x,y]=xyx^-1y^-1, and put

u=[[a,c],[b,d]].

Then u is nontrivial, scl_G(u)=1/2, but f(u)=1 for every homomorphism f:G→F into every free group F. In particular

sup_f scl_F(f(u))=0 < scl_G(u).

The statement concerns actual homomorphisms, not arbitrary surface maps, virtual embeddings, or all classes of target groups. It does not exhibit irrationality.

## Every free image kills u

Write A,B,C,D for the images of a,b,c,d. If B=1 then [B,D]=1; if C=1 then [A,C]=1. In either case f(u)=1. Otherwise B,C are commuting nonidentity elements in a free group. They lie in the same maximal cyclic group <r>, and C_F(B)=C_F(C)=<r>. Since A commutes with B and D commutes with C, A and D also lie in <r>. Consequently all four images commute and f(u)=1. The cyclic and trivial free groups cause no exception.

This uses only the standard cyclic-centralizer theorem for free groups. The word is an explicit witness that this path RAAG is not residually free. That phenomenon is known; no priority is asserted for this witness or consequence.

## Exact nontriviality certificate

Let E_ij denote the elementary matrix in row i,column j in Mat5(Z), and let I be the identity. Assign

a→I+E23, b→I+E45, c→I+E12, d→I+E34.

All matrices are unipotent upper triangular. The three required commutations hold because the relevant elementary matrices have zero products in both orders. Thus the assignment extends to a homomorphism G→UT5(Z). Direct multiplication gives

[a,c]→I−E13, [b,d]→I−E35,

and therefore u→I+E15≠I. Here E13 E35=E15 and E35 E13=0; higher products vanish. This proves nontriviality without assuming that the matrix homomorphism is faithful. The exact integer matrices and relation checks are in free_image_blind_certificate.json and verify_free_image_blind.py.

## Exact scl and consequence for the research route

The word u is a single commutator. The reviewed universal punctured-torus-cover upper bound gives scl_G(u)≤1/2, while Heuer's sharp RAAG gap gives scl_G(u)≥1/2 because the matrix certificate proves u≠1. Hence its value is exactly1/2.

Thus even considering all free quotients and all homomorphisms to free groups does not recover scl from rational free-group values by taking their supremum. Standard finite support retractions and valid induced-subgraph computations remain useful, but there is no such universal equality for them to exploit. A finite list of coordinate free projections is an even weaker special case.

This does not block RAAG-specific quasimorphisms or a valid exact surface program. It isolates a concrete missing equality in a potential positive reduction; it neither proves universal rationality nor gives a negative solution. All gap/source inputs are credited in COMMUTATOR_TEST_FAMILY.md and the priority audit.
