# Independent acceptance audit: TF equivalence and canonical decomposition cones

Problem 30005755; rank 801; OWR-14298157-005. Audit date: 2026-10-05 UTC.

## Verdict

PASS for the explicitly scoped mathematical results. The general conjecture is not solved, refuted, or promoted by this audit. The five-approach investigation remains exhausted at 5/5 for general discovery. No substantive mathematical correction is required. Two convention/reference clarifications appear in CLARIFICATIONS.md.

The accepted claims are the finite-witness sufficient criterion, the semisimple case, the product reduction, and the exact TF class and all-multiples cone for the displayed 12-dimensional algebra at eta=(1,1,-1). The construction and ray-condition failure are already in Asai–Iyama; this acceptance does not assert novelty. The generic-decomposition and positive-combination results remain explicitly cited external inputs.

## Frozen input and independence

The reviewed author archive is TF_EQUIVALENCE_30005755_AUTHOR_SAFE_FREEZE.zip, 19,502 bytes, SHA-256 9d2844b44ba9959f80a1d7d7b8946b718ea1d6bcd76df7ef7ed4a758e38a3488. Its ten files were extracted to a separate directory, their manifest verified, and both author checks replayed. Every authored file included under author/ in this package is byte-identical to the input archive. The author freeze was not edited.

The independent checker does not import or call the author's arithmetic routines. It reconstructs the algebra's multiplication and projective/Hom dimensions, evaluates the block determinant by the Leibniz formula, constructs an integer two-sided inverse, checks the alternating polynomial and its universal kernel, and checks the witness dimensions independently. Arithmetic checks support the textual proofs; they do not enumerate all modules or certify the general conjecture.

## 1. Definitions, pairing, and quantifiers

All module categories in this audit are mod A: finite-dimensional right A-modules. For a finite-dimensional algebra this agrees with finitely generated right modules. The field is algebraically closed for every appeal to generic decomposition and TF-cone theorems. Integer matrix identities proved below hold over every field, but this does not expand the asserted field scope of those external theorems.

For P_i=e_iA, evaluation at e_i identifies Hom_A(P_i,M) with Me_i. Consequently the projective-coordinate weight acts by the displayed module dimension vector. There is no Euler-form or Cartan-matrix substitution. For a basic algebra over an algebraically closed field, the simple classes are dual to the indecomposable-projective classes for this pairing.

The four strict/non-strict torsion definitions have the correct quotient/submodule orientations. Equality of both torsion classes determines their torsion-free partners, so W is constant on a TF class. For M in W_v, evaluating the quotient M and the submodule M gives both v(M)>=0 and v(M)<=0, hence v(M)=0. Strictness on a nonzero module in T_v or F_v follows by taking that module itself. These facts justify the witness criterion without requiring that its finite list contain every module.

Positive rescaling preserves all four definitions for every finite-dimensional module. Members of F(theta) range over all real weights, while theta and canonical summand weights are integral. No rational-density argument is used to prove an all-real class equality.

## 2. Finite-witness criterion

The lower inclusion follows from the generic positive-combination theorem. For a finite list of generators, the set of combinations having strictly positive coefficients on every listed generator is the relative interior of their cone, even with repetitions or linear dependence. One way to see the reverse direction is to subtract a sufficiently small positive multiple of the sum of all generators from a relative-interior point, then express the remainder in the cone. The zero-cone convention is consistent.

The upper inclusion uses only necessary conditions imposed by TF equivalence: semistable witnesses give equalities, and strict torsion witnesses give strict inequalities. Since their intersection is assumed to be exactly the candidate relative interior, this proves equality. It is a sufficient certificate, not an existence theorem for certificates.

For each canonical summand of each positive multiple, hold its coefficient at one and send all other positive coefficients to zero. The resulting limit is in the closure of the TF class. The finite candidate cone is closed, so all these summands lie in it. Conversely, refining the supplied generic decomposition expresses every candidate generator as a sum of canonical summands of that same multiple. This proves equality of the closed candidate cone with the all-multiples cone. Neither finite generation of the general all-multiples cone nor openness of the general TF class is assumed.

## 3. Semisimple and product claims

For a semisimple basic algebra, a simple belongs to T, W, or F according to the sign of its coordinate. The simple tests force the entire sign pattern, including its zero coordinates. All modules split into simples, establishing sufficiency. Disjoint positive/negative presentation supports give zero differentials and precisely the asserted signed coordinate directions. The zero weight and zero-dimensional cone are included.

For a product algebra, submodules and quotients split componentwise. Necessity of each component condition uses the corresponding component submodule or quotient; sufficiency uses additivity, with at least one strict summand for a nonzero object. The TF class is the Cartesian product. Presentation spaces and generic summands split by factors as well, so the generated cone is the product of the two cones. Taking finite Cartesian products commutes with relative interior. This reduction is valid and does not remove an unresolved connected factor.

## 4. Reconstruction of the wild nonhereditary example

Use a basis e0,e1,e2,a1,a2,a3,u1,u2,u3,v1,v2,v3, where the arrows a_i run from vertex 1 to 2, u_j from 0 to 1, and v_j from 0 to 2. The only non-idempotent products are u_j a_i=sum_l (F_i)_(l,j) v_l. The independent checker verifies the unit and all 12^3=1,728 basis associativity identities over the integers.

It recovers projective dimension vectors (1,3,3), (0,1,3), and (0,0,1). With source projectives indexing rows and target projectives indexing columns, the Hom-dimension matrix is

    1 0 0
    3 1 0
    3 3 1.

This is the required right-module orientation: Hom(P_i,P_j)=e_j B e_i. In particular Hom(P1,P0) and Hom(P2,P0) both have dimension 3, and precomposition with an arrow induces its specified X action. The symmetric off-diagonal blocks of the chosen presentation remove the block-transpose ambiguity.

The quotient by the new vertex is the three-arrow Kronecker algebra. Inflation preserves and reflects isomorphisms and indecomposability, yielding the asserted wildness from that standard wild quotient. The radical of P0 has dimensions (0,3,3). A projective module with zero vertex-0 part could only be P1^a plus P2^b; its last two dimensions are (a,3a+b). The equations a=3 and 3a+b=3 force b=-6. Thus the radical is not projective, and B is nonhereditary. This is stronger and more relevant than merely noting wildness, because hereditary algebras can also be wild.

## 5. Compatibility and the exact TF class

The independently reconstructed 6 by 6 block has determinant 1 by an integer Leibniz expansion. Its adjugate is an integer two-sided inverse, recorded in AUDIT_RESULTS.json. This gives invertibility in every characteristic, including 2, without relying on the invalid shortcut that every odd skew-symmetric matrix has zero determinant in characteristic 2.

The homotopy cokernel formula gives E(2g,p)=0. The reverse E(p,2g) and E(p,p) vanish for degree reasons. The compatibility theorem applies to distinct slots, including the two repeated p slots, hence 2eta=p direct-sum p direct-sum 2g. No indecomposability assumption on 2g is used. Positive combinations of all three slots are exactly a p+b g with a,b>0, establishing the lower inclusion for all real positive a,b.

The reverse inclusion uses S0 and S1 in T_eta and the inflated module Y of dimensions (0,1,1). Its identity arrow forces the three and only three submodule dimension vectors (0,0,0), (0,0,1), (0,1,1). All corresponding weights are nonpositive; the complementary quotient weights are nonnegative. Thus Y lies in W_eta. These witnesses force v0>0, v1>0, and v1+v2=0 for every real TF-equivalent v.

Therefore F_B(eta)={(a,b,-b): a,b>0}. The criterion proves C_N^B(eta)=R_nonnegative p+R_nonnegative g. Neither a finite-field search nor the rational consistency checks supplies this all-module conclusion; the two inclusions above do.

## 6. Indecomposability and an independent wild-weight check

For G(x)=x1 F1+x2 F2+x3 F3, direct polynomial expansion gives determinant zero over the integers. The vector (x2,x3,x1) is a symbolic kernel vector. If x is nonzero, one principal 2 by 2 minor is a nonzero square, so rank G(x)=2 in every characteristic. Thus E(g,p)=1.

Sign coherence forces a nontrivial decomposition of eta to separate its three unit coordinate atoms into a binary partition. There are precisely three unordered possibilities. The required obstruction in each case is respectively E(g,p)=1, E(p-P2,P1)=3, or E(-P2,p+P1)=6. The independently reconstructed Hom spaces verify these dimensions and their orientations. Since compatibility requires both directed E-invariants to vanish, one positive directed obstruction suffices in each case. Hence eta is indecomposable.

The author's uniqueness argument proving E(eta,eta)>0 is sound. A separate chain-space calculation sharpens this to E(eta,eta)=1 and provides an additional audit cross-check. Write two presentations as f=(v,x) and h=(w,y), with v,w in X2 and x,y arrow coefficient vectors. The homotopy image map from a six-dimensional space to a six-dimensional space is

    (a,b0,b1,u) -> (a w-b0 v-G(x)u, a y-b1 x).

If x is nonzero, u=(x2,x3,x1) gives a nonzero kernel element; if x=0, every u does. Thus the image rank is at most five for every pair of presentations. Taking x=(1,0,0), y=(0,1,0), v=(0,0,1), w=0 gives rank five over every field: the five nonzero independent columns are signed standard coordinate vectors. The minimum cokernel dimension is exactly one. The independent checker reproduces that matrix and rank.

The single-decomposition cone is the ray through eta; the all-multiples cone has the two independent generators p and g. The distinction and ray-condition failure are valid. They do not contradict the original conjecture, which uses all positive multiples.

## 7. Geometric safeguards and literature status

Both convex-geometric countermodels in the author proof are correct. In the first, a rational point on the displayed half-open cone must have b=0 by irrationality of sqrt(2); rational points are not dense in its two-dimensional span. In the second, the positive octant together with one irrational boundary ray is convex and positively homogeneous; it has the same closure, relative interior, and rational points as the positive octant, yet it has extra real boundary points. Neither model is asserted to arise from TF equivalence. They correctly explain why closure or rational-point information alone is insufficient.

The official OWR report's Conjecture 2 is on printed page 123. Its preceding theorem explicitly assumes an algebraically closed field. The published Asai–Iyama paper establishes the required external inputs and known hereditary/E-tame cases. Its Proposition 2.20 is Proposition 2.21 in the consulted author-preprint v3; this is version renumbering, not an erroneous published citation. [OWR; AI]

Haerizadeh–Yassemi v3 was submitted on 19 June 2026; the PDF title page bears 23 June 2026. Its modified Conjecture 1.1 and dimension criterion retain the relative interior of the TF class. Its claimed rational simplicial generation and special-case results do not by themselves establish the full original equality, and are not proof dependencies here. The withdrawn Fei note is not used as mathematical evidence; its public withdrawal is a status fact rather than a verdict on correctness. [HY; Fei]

A fresh bounded search found no general resolution. That is a search result, not a theorem about all literature. No claim of novelty or comprehensive auditing of the newer preprint is made.

## 8. Corpus, identity, and prior-attempt verification

The complete local copies of problems.json, research_results.json, and catalog.json were rehashed and parsed. Their sizes and hashes all match the author metadata. There is one problem and one descriptor record for ID 30005755, with rank 801. The statement and clean-statement hashes match the descriptor. The review hash was independently recomputed by the repository's Python serialization rule and equals ccda79771785f115a62d1b5b908393f3e3fa4c75af51d5f3e0313e4a46eb3262. The matching research-results join is empty; searches of all entries by ID, OWR code, and exact title return zero matches.

Fresh read-only repository checks found no targeted code, PR, commit, or branch match. The 63 entries in the attempts directory contain no matching name. These bounded checks do not prove there is no prior work anywhere in the repository or its history. The descriptor is a triage record, not an actual proof attempt.

Three principal public PDFs were downloaded afresh and match the author's recorded hashes byte for byte. The OWR target and Asai–Iyama construction were also visually checked after local rendering. Current publisher and arXiv pages were read. SOURCE_CHECKS.json distinguishes fresh downloads, rehashed existing copies, current status checks, and access limitations. No third-party source bytes, extracts, screenshots, or dataset records are included in the deliverable.

## References

[OWR] Osamu Iyama, joint with Sota Asai, Semistable torsion classes and canonical decompositions in Grothendieck groups, Oberwolfach Reports 2/2024, pp. 123–125, Conjecture 2. https://doi.org/10.4171/owr/2024/2

[AI] Sota Asai and Osamu Iyama, Semistable torsion classes and canonical decompositions in Grothendieck groups, Proceedings of the London Mathematical Society 129 (2024), e12639. https://doi.org/10.1112/plms.12639 ; consulted author-preprint version https://arxiv.org/abs/2112.14908v3

[HY] Mohamad Haerizadeh and Siamak Yassemi, The cones of g-vectors, arXiv:2501.15822v3. https://arxiv.org/abs/2501.15822v3

[Fei] Jiarui Fei, On AI's semistable torsion classes and canonical decompositions, current arXiv landing page. https://arxiv.org/abs/2412.08904
