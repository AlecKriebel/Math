# Equivalent bicommutant categories from nonisomorphic conformal nets

Problem 30004279 / OWR-17292-002. Research date: 2026-10-05.

**Status: unresolved in this investigation.** Five substantive approaches are retained below. No pair of nonisomorphic nets with proven equivalent full soliton tensor categories has been obtained. None of the lemmas below is claimed to be new. The live target page and the upstream raw statement/AI-report corpus were not inspected; the mathematical formulation was checked against the original Oberwolfach report. A newly located 2026 thesis was inspected only at the abstract/metadata level. These limits prevent a claim of exhaustive source or literature verification.

## 0. Target and conventions

Henriques's contribution, *Bicommutant categories*, in Oberwolfach Report 49/2019, pp. 3075–3076 [O], proposes that many nonisomorphic conformal nets yield equivalent bicommutant tensor categories. The report's word “many” is informal. A pair would give an existential instance; an infinite pairwise nonisomorphic family with a common tensor category would be a particularly clear realization. We prove neither.

We work with nontrivial irreducible finite-index conformal nets in the strong-additive, split setting of [H]. Thus complete rationality and finite index have their usual compatible meaning here. A conformal-net isomorphism respects the interval-algebra functor, including its conformal covariance; this is much stronger than separate isomorphisms of the local factors. No change of conformal covariance is silently allowed. The standard unitary/vacuum-preserving formulation is used for the examples.

Write T(A) for the category of separable solitons cut at a point, with bounded intertwiners, adjoint, and Connes fusion. Normal actions on intervals ending at the cut are required, as well as on intervals away from it. Write Rep(A) for the separable locally normal representations on the entire circle, and Rep_f(A) for the finite direct sums of its irreducible sectors. In the rational case Rep_f(A) is a unitary modular tensor category, whereas T(A) need not be semisimple or have finitely many simple objects. “Holomorphic” means complete rationality and only the vacuum irreducible DHR sector, equivalently mu-index 1; it does not mean only one soliton.

The commutant of a represented tensor category C → Bim(R) consists of R–R bimodules together with unitary half-braidings with C. Its definition depends on that representation. The tensor-equivalence type of a bicommutant category is an abstract categorical notion: an equivalence need not preserve a chosen embedding in Bim(R), preserve a named absorbing object, or be implemented by a fixed unitary between the vacuum spaces. In [HP] the equivalence also respects the bi-involution and positive structure. Our conditional constructions below use unitary structure; where spatial structure is added, it is explicitly an additional sufficient hypothesis.

The input from [H, Theorem A, Corollary 1.8] is

    T(A) is bicommutant, and Z(T(A)) ≃ Rep(A).

The two oppositely punctured soliton categories, in their specified common Bim(R), are mutual commutants. They are not identified there with finite fusion categories.

## 1. Approach 1: reconstruct from the Drinfeld center

### Lemma 1.1. Necessary center invariant

A unitary tensor equivalence F: C → D induces a braided unitary equivalence Z(C) → Z(D). Consequently T(A) ≃ T(B) implies Rep(A) ≃ Rep(B) in our finite-index setting.

**Proof.** Let F have tensor constraint J_{X,Y}: F(X) tensor F(Y) → F(X tensor Y), unit constraint, and unitary monoidal quasi-inverse G. For a central object (X,e), define its half-braiding with F(Y) by

    F(X) tensor F(Y) --J--> F(X tensor Y) --F(e_Y)--> F(Y tensor X) --J^{-1}--> F(Y) tensor F(X).

For arbitrary objects of D, transport this through the counit F G → id_D. Naturality makes the transport independent of the chosen isomorphism to an object in F's image. The hexagon follows by applying F to the hexagon for e and using the coherence identity for J. The unit condition is transported likewise. Apply F to morphisms. Repeating the construction with G gives inverse functors up to the induced natural isomorphisms. Tensor constraints and the braiding, which is the half-braiding evaluated on the other central object, are preserved by the displayed formula. Adjoint and unitarity are preserved because all constraints are unitary. Compose this center equivalence with [H]'s equivalences. ∎

### Lemma 1.2. A concrete failure of center-only reconstruction

Let H be a nontrivial holomorphic finite-index conformal net. The bicommutant categories T(H) and Hilb have equivalent Drinfeld centers but are not equivalent even as complex-linear *-categories.

**Proof.** Holomorphicity and rational representation decomposition give Rep(H) ≃ Hilb, so Lemma 1.1's source theorem gives Z(T(H)) ≃ Hilb. A half-braiding of a Hilbert space K with all Hilbert spaces is the ordinary flip: its component at the tensor unit is fixed by the unit axiom, and naturality against every map C → L determines its value on every elementary tensor in K tensor L. Density determines the whole bounded map. Thus Z(Hilb) ≃ Hilb. Hilb is itself bicommutant by [F, Theorem A], applied to finite-dimensional Hilbert spaces.

For inequivalence, [H, Section 4.3] constructs an absorbing soliton Omega with

    End_{T(H)}(Omega) = H(Delta_free),

where the right side is the local algebra on the unused triangle edge. It is a type III factor for a nontrivial conformal net. If E: T(H) → Hilb were a *-equivalence, full faithfulness would give a unital *-isomorphism End(Omega) ≅ B(E(Omega)). Omega is nonzero, so E(Omega) is nonzero. Every B(K) for nonzero K has a nonzero minimal projection, a rank-one projection. A type III factor has no nonzero minimal projection: a minimal projection is finite, and type III means there are no nonzero finite projections. This contradicts preservation of projections and minimality under a *-isomorphism. ∎

This is a negative control inside bicommutant categories, not a counterexample to the OWR conjecture. Hilb need not arise from a nontrivial net; the lemma only refutes the unrestricted implication “equal centers imply equal bicommutant categories.”

**Exact gap.** We have no center-to-soliton lifting theorem for the candidate conformal nets. Replacing that theorem by the conclusion it is meant to establish is circular.

## 2. Approach 2: holomorphic tensor powers and central charge

Fix a holomorphic conformal net H of central charge 8, as constructed in [KL, Example 2.8]. Let H_m = H tensor ... tensor H (m factors), m ≥ 1. We do not identify this net with a loop-group net by an unproved VOA-to-net comparison. The cited construction itself suffices.

### Proposition 2.1. The candidate family meets the easy necessary tests

The H_m are pairwise nonisomorphic conformal nets with Rep(H_m) ≃ Hilb and thus Z(T(H_m)) ≃ Hilb. This does not establish T(H_m) ≃ T(H_n).

**Proof.** On a tensor product net, the two-interval subfactor is the spatial tensor product of the corresponding subfactors. Finite Jones indices multiply, so mu(H_m) = mu(H)^m = 1. Tensor products preserve the split and strong-additivity properties here; hence H_m remains completely rational and holomorphic. The cited rational representation theorem then gives Rep(H_m) ≃ Hilb.

The infinitesimal conformal generators are sums L_k^(m) = sum_j L_k^(j), acting on distinct tensor factors. Operators on distinct factors commute. Summing

    [L_k,L_l] = (k-l)L_{k+l} + (c/12)(k^3-k) delta_{k+l,0} id

gives central charge c(H_m)=8m. A conformal-net isomorphism intertwines the projective conformal action and its central-extension class. Equivalently, on the common invariant finite-energy domain it preserves the Virasoro relation and its central coefficient. One can remove phase normalization ambiguity by fixing the vacuum/Möbius normalization; with k=2, l=-2 the central term is c/2. Thus 8m=8n would be necessary for an isomorphism, forcing m=n. The center assertion follows from [H]. ∎

As an arithmetic sanity check, the E8 Cartan matrix used by the lattice construction is positive definite, even, and unimodular. In our numbering it has diagonal 2 and off-diagonal -1 on edges 01,12,23,34,45,56,27. Its successive leading determinants are 2,3,4,5,6,7,8,1. Sylvester's criterion proves positivity, the diagonal proves evenness, and determinant 1 proves unimodularity. Direct sums preserve these properties and have rank 8m. The checker verifies these finite arithmetic claims; it does not construct conformal nets or an equivalence of categories. [DX, Corollary 3.19] independently explains why unimodularity makes a lattice net holomorphic.

**Exact gap.** A unitary monoidal equivalence T(H_m) → T(H_n) is missing. No tensor-product formula for full soliton categories, no absorbing-factor theorem, and no claim that T(H)=Hilb is inserted. In fact the latter equality is ruled out by Lemma 1.2. The claim T(A tensor H) ≃ T(A) for every A cannot hold if it includes the trivial net A with T(A)=Hilb; this boundary-case objection does not decide stabilization for nontrivial A.

## 3. Approach 3: use the fusion-category Morita theorem

The actual result of [HP, Theorem B/6.8] is: fully faithful representations of Morita-equivalent unitary fusion categories C,D in hyperfinite factors R,S have equivalent commutant categories C',D' when the factors are both type II or both type III_1. Positivity is part of their bicommutant equivalence. This is a proved nearby theorem, not a theorem about arbitrary soliton categories.

### Proposition 3.1. An explicit finite-category model for the mechanism

The categories Vec_{S3} and Rep(S3) are Morita equivalent but are not tensor equivalent. Their commutant categories in ambient factors satisfying [HP]'s hypotheses are tensor equivalent.

**Proof.** Make finite-dimensional Hilbert spaces M into a module category over G-graded finite-dimensional Hilbert spaces by forgetting the grading and taking the Hilbert tensor product. Every simple delta_g acts as the identity functor on M. A complex-linear additive module endofunctor of M is determined by its value W on C: on C^n it must act as W tensor C^n, and naturality against matrices determines its action on maps. Its module-functor constraint for delta_g is therefore a unitary u_g on W. Module coherence says u_{gh}=u_g u_h after choosing one of the equivalent inverse conventions, and the unit says u_e=id. Thus this endofunctor category is the category of unitary G-representations, with natural module transformations precisely the intertwining linear maps. Composition gives tensor product of representations (the harmless reversed convention is equivalent by the symmetric tensor structure). M is indecomposable since it has only one simple object. This is the standard module-category characterization of categorical Morita equivalence.

For G=S3, Vec_G has six simple objects. Rep(S3) has three, the trivial, sign, and two-dimensional standard representations. To check this last assertion without assuming a character-table list, the standard representation is the permutation representation on C^3 minus its invariant line and has character (2,0,-1) on identity, transpositions, and 3-cycles, of sizes (1,3,2). Its character norm is (4+0+2)/6=1, so it is irreducible; the three displayed characters are orthonormal and their squared dimensions sum to 1+1+4=6. The regular representation dimension identity leaves no additional irreducibles. An equivalence of semisimple categories induces a bijection on simple isomorphism classes, so six versus three rules out a tensor equivalence. The last assertion now follows from [HP], with the stated ambient-factor and full-faithfulness hypotheses. ∎

### Conditional transfer, with its hypothesis exposed

If one establishes T(A) ≃ C' and T(B) ≃ D' as unitary tensor categories for concrete nonisomorphic finite-index nets A,B, and C,D satisfy the preceding Morita and representation hypotheses, then T(A) ≃ T(B). **Proof:** compose the first equivalence, the [HP] equivalence, and the inverse of the second. ∎

**Exact gap.** Neither identification T(A) ≃ C' nor T(B) ≃ D' has been constructed for our candidate nets. Taking C=Rep_f(A) is not justified by the center theorem. Nor may T(A) itself be supplied to [HP] as though it were a fusion category. Approach 5 gives a particularly strong reason this would be invalid. The 2023 preprint/2026 publication [HPT] classifies finite-depth objects for the fusion-commutant class; it does not remove this realization gap or classify all objects and morphisms of arbitrary T(A).

## 4. Approach 4: transport the concrete extension predicate

This approach keeps the ambient-factor embedding rather than discarding it. For the four intervals I1,...,I4 in [H, Section 4.1], a bimodule over the chosen interval factor carries commuting actions of A(I12) and A(I34). Let P_A(K) be the assertion that its induced commuting actions of A(I2) and A(I3) extend normally to A(I23). By [H, Lemmas 4.1–4.2], the chosen full image of T(A) in Bim(R_A) is exactly the replete subcategory cut out by P_A.

### Proposition 4.1. A sufficient spatial criterion

Let theta: R_A → R_B be a normal *-isomorphism. Let F_theta: Bim(R_A) → Bim(R_B) transport both actions along theta^{-1}. If

    P_A(K) if and only if P_B(F_theta K), for every separable bimodule K,

then F_theta restricts to a unitary tensor equivalence T(A) ≃ T(B).

**Proof.** Transport preserves commuting normal actions and bounded intertwiners; theta^{-1} gives an inverse. The standard-form unitary L^2(R_A) → L^2(R_B) is the unit comparison. Changing variables along theta in the defining inner product of Connes fusion gives the natural unitary

    F_theta(K fusion_{R_A} L) ≅ F_theta(K) fusion_{R_B} F_theta(L).

Concretely, use the transported normal faithful weight on R_B; right-bounded vectors, the operator-valued inner products of such vectors, and the balanced relations are carried to the identical expressions under theta. Thus the comparison is isometric on the defining dense relative tensor products and extends to their completions. On triples both association orders give the same map on bounded elementary tensors, proving coherence by density. The inverse construction proves surjectivity. The hypothesis says exactly that the functor and its inverse preserve the full replete images of the soliton categories. Restrict the tensor constraints; their images remain in those full categories. This is the required equivalence. ∎

The hypothesis includes the **normal extension to the joined interval**, not merely isomorphisms of the two individual subalgebras. Normal actions of two commuting subalgebras do not automatically extend to a specified larger von Neumann algebra in an arbitrary bimodule representation.

### Negative control 4.2. The ambient factor alone cannot suffice

The rank-one even lattice with Gram matrix [2] has two irreducible DHR sectors, by [DX, Section 3], whereas the E8 lattice has one. Both give nontrivial rational conformal nets, all of whose single-interval algebras are isomorphic hyperfinite type III_1 factors. If an arbitrary isomorphism of those factors automatically preserved the extension predicate, Proposition 4.1 would equate their soliton categories. Lemma 1.1 would then equate their representation categories. Their different numbers of simple objects make that impossible. This proves that preservation of P_A is additional load-bearing structure, not a consequence of the factor type. The arithmetic discriminants are checked as 2 and 1.

**Exact gap.** No theta carrying the full extension predicate for H_m to that for H_n has been found. Requiring a spatial equivalence is a sufficient strategy only; failure of this strategy does not rule out an abstract tensor equivalence with no chosen-embedding compatibility.

## 5. Approach 5: match solitons from puncture germs, then extend

A potential constructive route is to match the known proper solitons of two nets via the same puncture geometry. It encounters both an essential-surjectivity gap and a tensor-coherence gap.

For each r>0, choose a smooth positive function d on (0,1) constant near either endpoint, with endpoint values whose quotient is r. Normalize it so its integral is 1. Integration gives an increasing diffeomorphism nu_r:[0,1]→[0,1], smooth on the cut interval, with nonzero one-sided derivatives. Identifying 0 with 1 gives a circle homeomorphism smooth away from the cut and with derivative ratio r (reverse the chosen endpoint quotient if the circle orientation convention requires it).

For each proper interval of the cut circle, including intervals ending at one side of the cut, nu_r extends on that interval to a smooth circle diffeomorphism. The one-sided constant derivative neighborhoods ensure all required one-sided derivatives. Define the representation on that interval by conjugating its algebra by the local conformal implementer. Two choices give the same action because their quotient is the identity there and is implemented in the complementary algebra. Compatibility under interval inclusion follows by the same argument. The resulting actions are normal because each is a unitary conjugation. Their union is irreducible because nu_r permutes the cut-circle intervals and the vacuum net on the punctured circle is irreducible.

The source theorem [DIT, Proposition 3.5 and Theorem 3.6] proves that these are index-one solitons, that r≠1 gives proper solitons, and that equivalence holds exactly when the ratios agree. Its hypotheses include half-lines, matching the endpoint-normality condition above. We rely on that theorem for inequivalence, rather than replace its modular-theoretic argument with an unsupported assertion about arbitrary type III factors.

### Consequence 5.1. Finite DHR data cannot enumerate the soliton category

Every nontrivial conformal net in this setting has uncountably many simple soliton isomorphism classes, even when it is holomorphic. Hence T(A) is not equivalent to the separable Hilbert-space completion of any unitary fusion category.

**Proof.** The construction and cited equivalence criterion inject (0,infinity) into simple soliton classes. In the Hilbert completion of a fusion category with simple representatives X_1,...,X_n, every object is a sum of X_i tensor K_i. An object is simple only when exactly one K_i is one-dimensional and the others vanish: otherwise its endomorphism algebra contains a nontrivial projection. Thus there are exactly n simple classes. Full faithful equivalences preserve endomorphism algebras and isomorphism classes, contradicting uncountability. ∎

Matching nu_r-solitions for two nets provides only a matching of a distinguished family of objects. It does not match every soliton, every Hom space, or the unitary tensor constraints. The following complete finite example demonstrates the independent coherence problem.

### Negative control 5.2. Identical simple labels and fusion rules do not determine tensor equivalence

On G=Z/2 define omega(a,b,c)=(-1)^(abc), with a,b,c in {0,1}. The pointed unitary categories Vec_G and Vec_G^omega have the same simple labels and multiplication but are not tensor equivalent.

**Proof.** The normalized cocycle identity follows, in exponents modulo 2, from

    bcd + a(b+c)d + abc = (a+b)cd + ab(c+d).

Both sides expand to bcd+abd+acd+abc. Whenever any argument is zero the exponent is zero, giving normalization. Thus omega supplies a unitary associator satisfying the pentagon.

A tensor equivalence must permute simple invertible objects by a group automorphism, and the only automorphism of Z/2 is the identity. Its unitary tensor constraint on pairs of simple objects is a scalar beta(a,b). Normalize the unit constraint, so beta(0,a)=beta(a,0)=1. Coherence would require omega to be the coboundary of beta (or its inverse, with the same contradiction). At a=b=c=1 this coboundary is

    beta(1,1) beta(1,0) / (beta(0,1) beta(1,1)) = 1,

whereas omega(1,1,1)=-1. Contradiction. The finite checker verifies every normalized cocycle and pentagon instance, but the arbitrary-scalar coboundary obstruction is the algebraic proof just given. ∎

**Exact gap.** The common geometric label r does not furnish an essentially surjective unitary monoidal functor between two full soliton categories. No claim is made that this particular Z/2 obstruction occurs for puncture germs; it is an exact control against treating object/fusion matching as tensor equivalence. Neither the finite-depth classification in [HPT] nor the abstract of the new thesis [N] supplies this missing global comparison.

## Conclusion

The nonisomorphic holomorphic tensor powers remain plausible candidates, with the exact missing step visible: equivalence of their **full** soliton tensor categories. We retain a necessary center invariant, a concrete center-only counterexample, an explicit applicable fusion-category theorem with its missing net-realization hypothesis, a precise ambient extension-predicate criterion, and a constructive proper-soliton route with two exact obstructions to oversimplification. These are partial deductions and safeguards. They neither prove nor disprove the original conjecture and are not offered as new mathematical discoveries.

## References

[O] André Henriques, *Bicommutant categories*, Oberwolfach Reports 49/2019, pp. 3075–3076. https://doi.org/10.4171/OWR/2019/49

[H] André Henriques, *Bicommutant categories from conformal nets*, arXiv:1701.02052v2. https://arxiv.org/abs/1701.02052

[F] André Henriques and David Penneys, *Bicommutant categories from fusion categories*, arXiv:1511.05226. https://arxiv.org/abs/1511.05226

[HP] André Henriques and David Penneys, *Representations of fusion categories and their commutants*, arXiv:2004.08271v1; Selecta Mathematica (2023). https://arxiv.org/abs/2004.08271

[DX] Chongying Dong and Feng Xu, *Conformal nets associated with lattices and their orbifolds*, arXiv:math/0411499. https://arxiv.org/abs/math/0411499

[KL] Yasuyuki Kawahigashi and Roberto Longo, *Local conformal nets arising from framed vertex operator algebras*, arXiv:math/0407263. https://arxiv.org/abs/math/0407263

[DIT] Simone Del Vecchio, Stefano Iovieno, Yoh Tanimoto, *Solitons and nonsmooth diffeomorphisms in conformal nets*, arXiv:1811.04501; CMP 375 (2020), 391–427. https://arxiv.org/abs/1811.04501

[HPT] André Henriques, David Penneys, James Tener, *Classification of finite depth objects in bicommutant categories via anchored planar algebras*, arXiv:2307.13822v1; CMP 407 (2026), article 68. https://arxiv.org/abs/2307.13822

[N] Nivedita, *Towards fully-local 2d chiral CFTs from conformal nets: bicommutant categories and fusion of their modules*, Oxford DPhil thesis (2026). Abstract/metadata only; full thesis uninspected. https://ora.ox.ac.uk/objects/uuid%3Ab8ccd774-5979-46bc-98fa-67260cfa7266
