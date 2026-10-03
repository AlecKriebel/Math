# Sealed source-first stage: PR 380 / problem 30002762

Scope: independent source reconstruction, universal derivations, and adversarial controls. Mechanism names were disclosed by the assignment. This is not blind rediscovery. No candidate, root audit, family audit, historical prose/code/result, or queue was opened during this stage. The exact repaired-head signal is required before that exposure. No external communication, Git operation, index mutation, service mutation, or candidate write was performed.

## Literal source and target

The first substantive tool action fetched https://ems.press/content/serial-article-files/46555 . Printed pages 199–200 were then extracted and rendered locally and both complete images were inspected. The report is OWR 3/2015, *Geometric Topology*, and the relevant contribution is Jarek Kędra's *The conjugation invariant geometry of cyclic subgroups*. Its displayed open-problem sentence requires a finitely presented group violating one of the two dichotomies. It concerns the word norm obtained from a generating set that is a union of finitely many conjugacy classes.

Let S be a finite symmetric **normal** generating set, meaning its conjugacy closure generates G, and write ν_S(g) for the associated conjugation-invariant word norm. The two hypotheses being challenged are exactly:

1. For every g, either sup over n in Z of ν_S(g^n) is finite, or τ_S(g)=lim ν_S(g^n)/n is positive.
2. For every g, either that supremum is finite, or an ordinary homogeneous real quasimorphism q on G has q(g) nonzero.

Here an ordinary quasimorphism has one finite uniform defect D for **all** pairs g,h. A bound proportional to min(ν(g),ν(h)) is a partial quasimorphism, with a different conclusion. The 2023 paper cited below proves detection by homogeneous antisymmetric partial quasimorphisms for undistorted elements. It does not establish ordinary-quasimorphism detection.

Fekete's lemma gives τ as an infimum because n↦ν(g^n) is subadditive. Bounded powers imply τ=0; the converse is not an algebraic identity. For example √|n| is an unbounded conjugation-invariant norm on Z with zero stable length, but is **not** the finite-normal-generator word norm relevant here. It is a control on the distinction, not a target counterexample. Positive τ is equivalent to a linear lower bound ν(g^n)≥τ n. The upper bound ν(g^n)≤nν(g) is automatic.

A homogeneous ordinary q is conjugation-invariant: apply its uniform defect to h g^n h^-1 and divide by n. Put M=max over s in S of |q(s)|. For a normal word of length k, |q(g)|≤kM+(k-1)D, so |q(g)|≤(M+D)ν_S(g). Thus q(g)≠0 proves τ_S(g)≥|q(g)|/(M+D)>0. A zero denominator corresponds to the identically zero q and cannot detect g. Consequently the stronger dichotomy implies the weaker one, and its alternatives are exclusive.

Two finite normal generating sets give Lipschitz-equivalent norms by expressing each generator in the other conjugacy closure. This does not make finite normal generation equivalent to finite ordinary generation. B∞ has finite normal generation by σ_1 but any finitely many ordinary generators involve only finitely many strands; thus it is not ordinarily finitely generated and cannot be finitely presented. A finite presentation in the exact target means a finite ordinary generator list and a finite ordinary relator list presenting the whole group. Merely writing an infinite relator list does not prove that its group lacks a finite presentation: redundancy must be ruled out. Conversely, a finite window of an infinite presentation is a different group unless the missing relations are proved consequences.

## Primary dependency gate

Only after the literal OWR source was fetched/read/rendered were these five primary dependencies fetched:

- https://math.bgu.ac.il/~brandens/bgkm.pdf : definitions 1.E–1.G; bounded-cyclic trick 4.B; nilpotent theorem 5.H; solvable theorem 5.K and lamplighter remark 5.L. The theorem 5.K hypothesis includes a finitely generated nilpotent derived subgroup. It cannot by itself justify the larger class of every finitely generated metabelian group; an additional proof is needed below.
- https://msp.org/agt/2015/15-5/agt-v15-n5-p11-p.pdf : Theorems 1.1–1.2 distinguish strand-dependent defect from strand-independent norm control; Theorem 1.13 is about the infinite braid commutator subgroup; Proposition 3.10 gives displacement; Lemma 4.2 and Example 4.4 bound powers of σ_1σ_3^-1; Proposition 4.7 identifies the connected-sum family. None converts B∞' into a finitely presented target.
- https://arxiv.org/pdf/2204.09373v3 : definition (1.1), Theorem 1.1, Examples 1.6–1.7, Remarks 1.3 and 1.12. Partial defect and antisymmetry are explicit hypotheses; ordinary homogenization's bounded-distance property cannot be silently transferred to partial quasimorphisms.
- https://msp.org/agt/2024/24-3/agt-v24-n3-p10-p.pdf : Theorem 1.2, Corollaries 1.3, 2.14–2.15, and Theorem 3.4 distinguish bV from bV-hat. The former has many quasimorphisms; the latter is finitely presented (indeed type F∞), has abelianization Z, and only homomorphisms after homogenization. These facts alone give no cyclic lower bound and therefore no counterexample to the OWR target.
- https://arxiv.org/pdf/0710.1412v1 : §2.1 strongly m-displaceable means the **consecutive powers of one element**, including indices 0 through m, give pairwise commuting subgroups. Theorem 2.2 has the 14ν(F) bound when commutator length is m and the special 4ν(F) bound for m=1. The three-block Lemma 2.7 formula needs a second displaced copy. Its use for m=1 requires the separate double-commutator argument, not an unpromised third block.

Local PDF hashes, byte counts, and acquisition time are in `source_download_manifest.json`. Full downloaded files and extracted text are in `sources/`; the OWR page images are read-only inspection derivatives. These dependency checks establish scope and exact hypotheses, not worldwide status or novelty.

## Universal derivation A: finitely generated metabelian groups

Let G be ordinarily generated by s_1,…,s_d and let A=G' be abelian. All lengths below may be any conjugation-invariant norm ν finite on the s_i. Set B=[A,G]. The conjugation actions T_i of s_i on A commute, since G/A is abelian. In additive notation

    B = Σ_i (T_i-I)A.

To justify equality, the right side is stable under each T_j and its inverse (the actions commute); all T_g-I are sums of those operators followed by automorphisms, by expanding a generator word. Every element of an image is a single commutator with s_i, so ν(b)≤2Σ_iν(s_i) for every b∈B. No finite generation of A as an abelian group is assumed.

In G/B, the derived subgroup A/B is central, and is generated as an abelian group by the finitely many basic commutators c_ij=[s_i,s_j], i<j. This follows by expanding commutators of generator words in a class-two quotient. For any a∈A choose integer exponents n_ij representing its image there. The element

    p = ∏_(i<j) [s_i^(n_ij),s_j]

has the same image as a modulo B and satisfies ν(p)≤2Σ_(i<j)ν(s_j). Thus

    ν(a) ≤ 2Σ_iν(s_i) + 2Σ_(i<j)ν(s_j).

This is a universal bound for the entire derived subgroup. It also covers a one-generator group (whose derived subgroup is trivial) and trivial/identity commutator factors. It depends on finite **ordinary** generation; finitely many normal generators do not provide the finite operator decomposition above. The affine and lamplighter computations independently instantiate noncentral, infinite-rank derived subgroups; the Heisenberg control instantiates the central quotient part. They do not prove the universal formula by sampling.

For an abelian subgroup A normal in any group ordinarily generated modulo A by lifts q_1,…,q_r, the same image-sum equality B=[G,A]=Σ_j(T_j-I)A holds even without commuting actions. Indeed, for b in that sum, T_j b=b+(T_j-I)b belongs to the sum, as does T_j^-1b=b-(T_j-I)T_j^-1b. It is therefore invariant and the quotient has trivial action. Consequently ν(B)≤2Σ_jν(q_j). This more general version is used next.

## Universal derivation B: finitely generated virtually metabelian groups

Take the finite-index normal core M of a metabelian finite-index subgroup. M is metabelian and ordinarily finitely generated, so derivation A bounds M' in G. Pass to Γ=G/M', with the quotient norm. It has a finitely generated abelian normal subgroup A=M/M' of finite index. The previous image-sum argument bounds B=[Γ,A] using finitely many lifts of generators of Γ/A.

In Γ/B the subgroup A/B is central and of finite index k. Its derived subgroup is finite; here is a direct check rather than an unsupported structural substitution. For a central finite-index finitely generated abelian subgroup C, choose right coset representatives r_1,…,r_k. Write r_i g=c_i(g)r_σ_g(i), with c_i(g)∈C. Then V(g)=∏c_i(g) is a homomorphism to C: the product rule permutes the second list of c_i's, and C is central. For z∈C, V(z)=z^k. Thus (Γ/B)'∩C lies in the finite k-torsion subgroup C[k]. Its quotient embeds in the finite coset group (Γ/B)/C, proving finiteness.

Lift the finitely many elements of this finite derived group to Γ'. Their quotient-norm lengths have a finite maximum L. Every element of Γ' differs from such a lift by an element of B, so Γ' is bounded. Lifting once more to G adds the bound for M'. Hence G' is bounded in G. This argument does not claim that a finite-index subgroup's intrinsic norm extends to G: the ambient norm is used throughout. The dihedral control explicitly tests inversion, finite coinvariants, and an infinite bounded derived subgroup.

## Universal derivation C: split coinvariants versus nonsplit extensions

For G=A⋊Q with A abelian, suppose q_1,…,q_r ordinarily generate Q and a_1,…,a_e generate A as a Z[Q]-module. Use the normal word norm of the lifted set {a_i,q_j}. Let A_Q=A/[Q,A] and give it the ordinary word norm η from the images of the a_i. The split structure provides the homomorphism (a,q)↦[a] to A_Q. Therefore

    η([a]) ≤ ν_G(a) ≤ η([a])+2r.

The lower bound comes from projection. For the upper bound, lift a minimal ordinary word for [a]; its difference from a lies in [Q,A], a sum of r commutator images, each of length at most two. The quotient generation is essential; merely discarding an infinite lamp coordinate set without proving these images generate A_Q is not an algorithm.

The identical lower bound is false for general nonsplit extensions. In the integral Heisenberg group

    (x,y,z)(X,Y,Z)=(x+X,y+Y,z+Z+xY),

take A={(0,0,z)} and Q=Z². The action on A is trivial, so A_Q=Z. Yet [(n,0,0),(0,1,0)]=(0,0,n), whose normal word length is at most two. With the finite ordinary set containing the two horizontal generators and the central unit, the naive coinvariant length is |n| and cannot lower-bound the ambient norm. The nonzero central commutator also proves this extension does not split as an extension by the abelian Q. Finite Heisenberg quotients preserve this obstruction. In nonsplit cases one must use the actual image of A in G_ab, including extension relations, or supply a new argument.

## Universal derivation D: integral abelianization and the stable LP

Let G be finitely presented, with specified ordinary generators S. Let A=G_ab; the relator exponent-sum matrix determines the integral finitely generated abelian group A, including torsion. **Supply as a proved mathematical promise** a constant C with ν_S(G')≤C. Then the quotient word norm η satisfies

    η(πg) ≤ ν_S(g) ≤ η(πg)+C.

Lift a shortest abelian word to G; the remaining factor is in G'. This proves the sandwich uniformly, for each g and each power.

Write A≅Z^d⊕T and let v_i be the free coordinates of π(s_i). The stable value is the exact rational linear program

    minimize Σ_i(u_i+v_i')
    subject to Σ_i(u_i-v_i') v_i = free(πg), u_i,v_i'≥0.

The notation v_i' is a scalar variable, distinct from the generator vector v_i. Lower bounds follow from every integer word being a feasible real decomposition. An optimal basic feasible solution is rational, since the data are integral; let D clear all its denominators. Choose L divisible by D·|T|. Multiplying by L makes all coefficients integral multiples of |T|, kills the torsion discrepancy as well as L·torsion(πg), and realizes the LP value **exactly** on Lπg. Multiples of L therefore realize the LP exactly; the finitely many residue powers contribute only a bounded length. The sandwich then proves τ_S(g)=LP, with finite torsion affecting unstabilized lengths but not the limit. Rank zero yields LP=0 and, with the promise, all cyclic subgroups are bounded.

The implementation uses exact Fraction arithmetic, not floating tolerances. Its chosen generators in Z²⊕Z/4 are ((2,0;1),(0,3;2),(1,1;3)). They generate the whole integral group: the free-coordinate kernel relation (-3,-2,6) has torsion coordinate 11≡3 mod4. Target (1,0;1) has exact LP 1/2; its integer length is 16. In solving 2x+z=n, 3y+z=0 and the torsion congruence, y≡5n mod8. A representative |y|≤4 yields length ≤|n|/2+22, and every optimum has 4|y|≤length. This proves that the implementation's finite coefficient search covers every optimum. Period 8 gives an exact stable certificate and bounded residues.

The bounded-derived promise cannot be inferred from a finite presentation or from calculating an abelianization. For F_2 and g=[a,b], the abelian LP is zero. Define Q(w) by counting adjacent ab minus adjacent b^-1a^-1 in a reduced free word. Decomposing a concatenation into its canceled central word and two surviving pieces bounds its ordinary defect by 3. Its homogenization q has defect at most 6, q(a)=q(b)=0, and q(g)=1, because g^n is cyclically reduced and Q(g^n)=n. Thus ν_S(g^n)≥n/6. The exact cancellation-norm dynamic program confirms nonzero norms on the first sixteen powers, but the uniform ordinary quasimorphism proof establishes the contradiction for all powers.

Every finitely generated group with bounded G' satisfies the stronger dichotomy: a torsion abelian image has bounded powers by the sandwich, and a nontorsion free image is detected by a real homomorphism. Indeed every homogeneous ordinary quasimorphism on such a group is a homomorphism. The defect between (gh)^n and g^nh^n is in the uniformly bounded G'; norm control for q and its ordinary defect bound make the difference O(1), and dividing by n proves q(gh)=q(g)+q(h).

## Universal derivation E: finite-window braid controls

Put a_i=t^i a t^-i. A finite-window presentation whose stated braid relations involve 0≤i≤N has a quotient to B_(N+2) by a↦σ_1 and t↦δ=σ_1⋯σ_(N+1). The braid identity δσ_iδ^-1=σ_(i+1) is valid for i≤N, which is precisely the range needed. The last Artin generator does **not** wrap back to σ_1 under that conjugation. Therefore any finite-window quotient test must reserve at least one additional strand and must check the exact relator range; a periodic shift is not a substitute. Conjugates of verified relators remain valid automatically, even after the resulting image no longer looks like a consecutive standard generator.

The code checks Artin relators, distant commuting relators, finite-window shifts and the non-wrap negative condition using the faithful Artin action on the free group. Equality of these automorphisms tests braid equality, not just the strand permutation or a nonfaithful linear representation.

For α=σ_1σ_3^-1∈B_4 and Δ=σ_2σ_1σ_3σ_2, the exact braid identity ΔαΔ^-1=α^-1 yields [α^k,Δ]=α^(2k). Hence even powers have norm at most 8 and odd powers at most 10 in the usual normal generator norm. The canonical checks include negative k and k=0.

For n≥1, the source's closure α^(2n)σ_1σ_2σ_3 is the connected sum T(2,2n+1)#mirror(T(2,2n-1)). Its ordinary signature has magnitude exactly 2 for **every** n, up to the global convention for the positive torus knot. A Seifert form for T(2,2n+1) has symmetric tridiagonal matrix of size 2n, diagonal 2 and off-diagonal -1. Its leading principal determinants are k+1, and the exact LDL pivots are (k+1)/k>0. The mirror contributes -(2n-2), giving 2n-(2n-2)=2. For n=1 the second matrix is empty and its signature is zero. This is an all-n proof, with exact arithmetic checks through n=100. Constant signature 2 is not a growing cyclic certificate and is consistent with bounded powers of α. Strand-dependent finite braid quasimorphism defects do not give a uniform ordinary quasimorphism on B∞.

## Universal derivation F: strong displacement, seven factors, and 42

Suppose F strongly m-displaces H: H_i=F^iHF^-i commute pairwise for 0≤i<j≤m. Use [x,y]=xyx^-1y^-1. For g_0,…,g_m∈H with ordered product 1, define φ_i=g_0⋯g_i and Φ=∏_(i=0)^(m-1)F^iφ_iF^-i. Then

    ∏_(i=0)^m F^i g_i F^-i = [F,Φ^-1].

The component at index i is φ_(i-1)^-1φ_i, with the endpoint conventions φ_-1=φ_m=1. Pairwise commuting copies permit grouping the components; no commutation within H is used. Each conjugate of an F-commutator has norm at most 2ν(F).

Let x=c_m⋯c_1 with c_i=[f_i,g_i] and m≥2. Set θ=∏_(i=1)^m F^ic_iF^-i=[P,Q], P=∏F^if_iF^-i, Q=∏F^ig_iF^-i. The transport identity gives x=Kθ with one F-commutator K. Put f=f_m⋯f_1 and g=g_m⋯g_1. Write P=fX and Q=gY, where X,Y are conjugates of inverses of F-commutators. The exact identity

    [fX,gY] = [f,g] · Conj_g(Conj_f(g^-1 X g Y X^-1)Y^-1)

has four remaining conjugated F-commutator factors. Since copies 0,1,2 are available,

    U=(fg)_0(g^-1)_1(f^-1)_2,
    V=(f^-1g^-1)_0 g_1 f_2

are each F-commutators and UV=[f,g]. This gives seven factors, hence ν(x)≤14ν(F), and x=K[P,Q] also gives cl_G(x)≤2. Descending order of the original c_i is essential for the transport cancellation; the written proof and the independent code both retain it.

For m=1 use only H_0,H_1: since Ff^-1F^-1 commutes with g,

    [f,g]=[[f,F],g], so ν([f,g])≤4ν(F).

This requires no H_2. The two-copy noncommuting cyclic control verifies this formula and falsifies the unsupported three-copy U,V formula when only one displaced copy exists. For x=1, no displacement is needed and the bound is zero. If F=1 displaces H, H is abelian and H' is trivial; a zero displacement length cannot certify a nontrivial commutator.

Consequently, if each relevant element x lies in the derived subgroup of a subgroup H for which, for every needed m, there exists a strong m-displacer F_m with ν(F_m)≤3, then ν(x)≤42. The m=1 case is at most 12, hence also at most 42. Displacers may depend on m, but the bound 3 must be uniform, and the same strong power-displacer must provide all copies needed for its m. Mere commuting conjugates, arbitrary separately chosen conjugators, or an unbounded cost of F_m are insufficient. If this hypothesis applies uniformly to all G', the derived subgroup is bounded; if it applies only to a particular cyclic family, only that family is bounded.

The independent implementation uses the restricted direct product of **nonabelian** free groups indexed by the integers, acted on by the shift. It checks all seven factors separately, not just a telescoping abelian quotient. It performs 195 fixed-seed cases with 2≤m≤14, actual noncommuting m=1 controls, and periodic negative controls for periods 2,…,9. Integer support dictionaries never identify endpoints. The degenerate abelian case is stated separately. The universal proof above is what permits unbounded m; finite output alone does not.

## Stage disposition and exact remaining gate

The strongest verified stage result consists of the exact source formulation, the universal bounded-derived/metric/LP/displacement deductions above, and passing adversarial controls. These exclude the displayed metabelian and virtually metabelian mechanisms from producing the OWR counterexample, expose nonsplit and missing-promise failures, and show how a constant-42 obstruction can be valid with its exact uniform displacement hypothesis. They do not establish that any particular unpublished presentation meets that hypothesis, or that any candidate package is correct.

Completion estimate toward this **whole-package final verification**: 55%. Source-first mathematical work is sealed; the remaining 45% is candidate exposure at the exact repaired manifest, full five-proof/eight-executable and nested/wrapper checks, current historical/source-priority/author-output checks, and queue byte-isolation. No candidate acceptance, novelty, or worldwide-open certification is issued.
