# Stage-3 separation over a p-adic function field: five reconstruction approaches

Date: 2026-10-21. Target: row 1851, problem 30005646.

## Verdict and scope

No rigorously verified algebraic example is produced here. The 2024 Carlson–Corwin–Schlank announcement remains an announcement; it is neither disproved nor independently proved. These notes isolate a genuine finite-coefficient matching obstruction, give concrete failed candidates and a calculation of the geometric room available on rational surfaces, and specify the missing arithmetic realization data. They do not claim novelty for the formal observations.

Throughout, K=k(C), k/Q_p finite, C smooth projective geometrically integral, and valuations are exactly C's closed points. An example must exhibit x in X(A_K)^{h,2} outside X(A_K)^h. A rational point on X is allowed: strictness of sets does not require emptiness of the full set. Number-field comparisons, nonexistence of rational points alone, and a nonzero abstract cohomology class are not substitutes.

## Approach 1: construct the finite local-matching obstruction first

The complete section-space formulation and proof are in FINITE_STAGE_LEMMA.md. Its chief conclusion is that stage 3 is not obstructed by a nonzero H^4(K,B) for finite B: that group vanishes. Instead prescribe local degree-3 lifts which cannot be the localization of a common global lift, taking account of stage-2 monodromy and every possible global stage-2 section.

The arithmetic target is concrete. Harari–Scheiderer–Szamuely give, for a finite Galois module B and its weight-two dual B'=Hom(B,Q/Z(2)), the terminal exact sequence

H^3(K,B) -> direct_sum_v H^3(K_v,B) -> H^0(K,B')^D -> 0.

The last map sums local duality pairings. At good places the unramified degree-3 subgroup is zero, since the residue field has cohomological dimension 2. Thus finite-support mismatch families are the appropriate first test. Source: https://arxiv.org/pdf/1307.4783 , Theorem 2.3, PDF page 8, finite-module Poitou–Tate sequence (numbering differs from the journal version).

### Explicit formal mismatch, not a variety

Take p odd, K=Q_p(t), B=Z/2 with its canonical identification with every mod-2 Tate twist, v0=(t), and u a nonsquare unit of Q_p. Over F=Q_p((t)), the symbol (u) cup (p) cup (t) has residue the nonsplit quaternion class (u,p), whose invariant is 1/2. Put this degree-3 class at v0 and zero at every other closed-point place. Its sum pairing with 1 in H^0(K,B') is 1/2. It cannot arise from H^3(K,B).

For comparison the global symbol (u,p,t) also has a nonzero residue at infinity, cancelling the first contribution. This explains why simply exhibiting a global nonzero triple symbol does not give the required incompatible adelic family.

A toy equivariant space E=K(B,3) has trivial stage 2 and admits precisely this formal separation of section families. But its geometric H_3=B is nonzero, and its homological obstruction sees the same failure. It is neither an algebraic variety nor an example in the highlighted homology-blind subclass. This is a verified arithmetic supply of mismatch, with two missing bridges: realization by local rational points on a single X, and survival of the mismatch after the local monodromy orbits and all alternative global stage-2 sections are allowed.

A practical sufficient certificate would give a finite quotient B, an invariant functional lambda in H^0(K,B'), and a proof that the pairing of every allowed local-orbit representative is a fixed nonzero value for every global stage-2 component. Computing a nonzero value for just one representative is not enough.

## Approach 2: rational surfaces, intersection form, and R-equivalence

Let S be a smooth projective complex rational surface of second Betti number r. It has pi_1=0, H_2=Z^r, H_3=0, H_4=Z. Whitehead's exact sequence gives

H_4(S,Z) -> Gamma(Z^r) -> pi_3(S) -> 0.

Here Gamma is the universal quadratic functor. For a free lattice of rank r it has rank r(r+1)/2; the H_4 map is the quadratic attaching relation determined by the intersection pairing. For blowups of P^2 this is, up to orientations and conventions, gamma(h)-sum gamma(e_i); for P^1 x P^1 it is the cross Whitehead product. Both relations are primitive. Hence pi_3 is free of rank r(r+1)/2-1. This is an elementary topological computation, not an arithmetic Postnikov computation. Source for the exact sequence and Gamma decomposition: https://arxiv.org/pdf/2006.06127v4 (also https://eprints.soton.ac.uk/478456/2/2006.06127v4.pdf), Theorem 2.13 and Lemma 2.16.

Checks: P^2 has r=1 and pi_3=0. P^1 x P^1 has r=2 and pi_3=Z^2, agreeing with the product of two 2-spheres. A geometric del Pezzo surface of degree d has r=10-d (with the standard rank-2 alternatives in degree 8), giving ample geometric pi_3 for d<=8. Geometric H_3=0 emphatically does not imply pi_3=0. No replacement of homology H_3 by cohomology H^3 is made here.

To use this over K one must recover the actual G_K-action on the completed quadratic quotient and the arithmetic k-invariant, not merely an intersection matrix after algebraic closure. Tate twists, descent, and integral 2-primary quadratic refinements matter. Complex comparison after descent to a finitely generated subfield supplies geometric information; it does not determine the arithmetic action.

### A rigorous pruning lemma

If X is smooth projective over K, has a point b in X(K), and every X(K_v) is one R-equivalence class, then X(A_K)^h=X(A_K). Indeed the point-to-homotopy-section map is constant on R-equivalence, so every local point has the same full homotopy class as b_v, and b supplies the common global class. Pál proves factorization through R-equivalence in characteristic zero: https://arxiv.org/abs/1002.1731 , Definition 12.4 and Proposition 7.8. Alternatively, for an actual chain of morphisms P^1->X, remove a third rational point from each P^1; the resulting A^1 has contractible geometric étale homotopy type in characteristic zero, so its two sections agree.

In particular split P^1 x P^1, despite nonzero pi_3, cannot separate the sets: connect points by changing one coordinate at a time along P^1. Thus geometric homotopy rank alone is not promising evidence. A rational surface search should begin with nonsplit arithmetic forms and demonstrably nontrivial local R-equivalence/evaluation, not split blowups with visibly rational connecting chains.

Missing data: an explicit nonsplit surface, all-place points, a global stage-2 witness, and an evaluated secondary invariant insensitive to the allowed changes in stage-2 data. No such data were obtained.

## Approach 3: homogeneous spaces G/T and their quadratic transgression

For a complex simple simply connected group G and a connected torus T of rank r, the topological fibration T->G->G/T yields

pi_1(G/T)=0, pi_2(G/T)=Z^r, pi_3(G/T)=pi_3(G)=Z.

This differs fundamentally from the BG approximation in Approach 5: the nonzero pi_3 sits in degree 3 rather than being shifted to degree 4. The map Gamma(Z^r)->Z in Whitehead's sequence determines H_3(G/T) as its cokernel. Rational surjectivity is not integral surjectivity; checking rank alone can leave finite torsion H_3. Thus “sufficiently large torus” must be verified through the actual integral map, not interpreted as any positive rank.

One calculable model is SL_2/G_m with the split diagonal torus. Topologically it retracts to SU(2)/S^1=S^2: pi_2=Z, pi_3=Z, H_3=0. It nevertheless cannot give a separation. For every extension F/K, Hilbert 90 gives H^1(F,G_m)=0, so SL_2(F)->X(F) is surjective. Elementary matrices generate SL_2(F), and each elementary matrix is joined to the identity by the algebraic path e_ij(ta). Their images give a chain of A^1-morphisms connecting every point to the standard basepoint. Geometric étale A^1-contractibility in characteristic zero implies constant full section evaluation. Thus X(A_K)^h=X(A_K). Larger nonsplit forms offer character-lattice and invariant-quadratic-form computations, followed by finite quotients of pi_3 and the pairing test of Approach 1.

For a K-homogeneous space with rational basepoint, the connecting map X(F)->H^1(F,T) has image ker[H^1(F,T)->H^1(F,G)]. A nontrivial tuple of torus torsors can therefore encode local points, but its equality to the stage-2 evaluation is a theorem to prove, not a definition. The actual stage-2 type uses completed homotopy modules. Replacing it by ordinary algebraic H^1(F,T) without a Kummer/compatibility comparison is not justified.

Nguyen Manh Linh's inspectable work on SL_n-homogeneous spaces with multiplicative-type/unipotent stabilizers concerns unramified reciprocity and local-global/approximation principles: https://arxiv.org/pdf/2211.08986 . Those theorems constrain possible examples but are not equalities between full étale homotopy and stage 2. In particular, sufficiency of an unramified obstruction does not imply sufficiency of the étale-homology obstruction.

Missing data: a specific arithmetic form and torus, integral H_3 verification, point-to-section comparison, and explicit nonzero secondary pairing. This is structurally the most economical family for a reconstruction but remains a program, not a solution.

## Approach 4: patching or finite-place modification to realize the mismatch

Start from a variety X with a global point b and seek x_v0 whose stage-2 class equals b_v0 but whose stage-3 class differs. Set x_v=b_v elsewhere. This automatically gives an adelic tuple (finite modification of a rational point) and a known global stage-2 witness. It reduces the task to a sharply testable local evaluation problem, plus exclusion of all other global stage-2 witnesses.

The invariant needed is not an arbitrary H^3 class: it must lie in the difference image of two actual local points with equal stage-2 classes. For a proper variety the unrigidified stage-3 point evaluation factors through R-equivalence; chosen rigidified H^3 differences still depend on projection paths. Thus the local problem can be approached by an explicit local R-equivalence computation on a nonsplit rational surface or homogeneous space. A field-theoretic triple symbol is only useful after an identity tying it to that evaluation map is proved.

Patching can produce varieties or points with chosen behavior over a finite list of fields, but the present local set consists of horizontal closed points on C. Results using every rank-one valuation of K, vertical components on a regular model, or patch fields do not automatically use this set. Any candidate must state exactly which places are covered and establish points at all remaining horizontal places. A finite modification of b avoids that all-place existence issue completely.

The central obstruction to this approach is global stage-2 ambiguity: even if b is one matching stage-2 class, another global class may absorb the local difference. A finite computation must either classify all such global classes, or provide a secondary functional unchanged by their variation. This is where a symbolic “one bad place gives 1/2” argument otherwise fails.

No patching theorem or computable local variety was found which fills this bridge. The output is a sufficient construction template with explicit missing hypotheses, not an asserted existence theorem.

## Approach 5: audit new unramified-obstruction examples and reject false replacements

Yisheng Tian's June 2026 preprint constructs X=(A^n minus Z)/G, with codim Z>=3 and G semisimple simply connected, to separate unramified degree-3 obstruction from the étale degree-3 Manin obstruction. It is publicly inspectable at https://arxiv.org/html/2606.27699v1 , section 5. This is a genuinely new lead relative to the source gate, but the compared obstruction sets are not the requested ones.

Our geometric audit: over C, general position makes A^n minus Z at least 4-connected when Z has complex codimension >=3. The torsor fibration then gives pi_i(X)=pi_{i-1}(G) for i<=3; these vanish because a simply connected semisimple complex group is connected with pi_1=pi_2=0. Consequently this construction has no geometric pi_3 available to furnish the requested stage-3 separation. The inference uses algebraic descent and the usual characteristic-zero geometric étale comparison to transfer the low-degree calculation, not a claim that K carries an analytic embedding with arithmetic compatibility. For invariance under algebraically closed characteristic-zero base extension in the smooth geometrically irreducible quasi-projective setting, see Pál, Proposition 5.4, https://arxiv.org/abs/1002.1731 .

The mechanism producing its unramified obstruction is therefore not a ready-made étale-homotopy proof. A universal assertion that full étale homotopy refines every unramified H^3 obstruction would require justification and is particularly suspect here. Do not present the new preprint as solving Corwin's problem.

This negative screening is valuable: it distinguishes higher unramified/motivic phenomena from the stage-3 phenomenon sought here, including its unstable quadratic version in the H_3=0 subclass. Changing the construction to a G/T quotient restores nonzero pi_3 but also restores the hard arithmetic calculation in Approach 3.

## Source recovery beyond the original gate

Exact-author, title, p-adic function-field, del Pezzo, and 2025–2026 seminar searches still did not recover an inspectable Carlson–Corwin–Schlank construction. The AHGT 2025 “Homotopy-Homology Frontier” program was checked; Corwin's contribution is about Chabauty–Kim/Tannakian methods, not this example: https://ahgt.math.cnrs.fr/assets/pdf/Paris%20AHGT25%20Program.pdf . The public AHGT video index did not supply the missing proof during this pass: https://ahgt.math.cnrs.fr/videos/ . These are bounded negative search results, not proof of nonpublication.

## Acceptance checklist and stopping point

A verified solution still needs:

1. Exact K, horizontal valuation set, equations or precise algebraic construction of X.
2. The actual geometric pi_1 and integral/profinite H_3 conditions if claiming the homology-blind subclass.
3. A genuine adelic tuple and one global stage-2 section matching it.
4. A valid finite stage-3 quotient with its Galois action and k-invariant.
5. A computed local point-evaluation difference, and proof that its pairing survives local section-path actions.
6. Exclusion of every alternate global stage-2 section compatible with the tuple.
7. If using a compactification, proof that the witness and obstruction survive the change.

Items 1–6 have not been jointly met. The strongest completed outputs are the corrected finite matching lemma, the explicit finite-support cohomological mismatch, the rational-surface topological calculation and R-equivalence pruning lemma, and the rejection of the BG-approximation substitution. Status: unresolved reconstruction; announced result not independently verified.
