# Scope-family derivations and checks

The initial twelve-claim reconstruction in INITIAL_RECONSTRUCTION.md remains immutable. This continuation records the resolution of its source-dependent gaps, not a replacement of that early record. Every theorem below uses k algebraically closed of odd characteristicp, r=2p-1 and lambda=(r-1,1).

## Local representation calculation

Write v_i=x^{m-i}y^i. The coefficient of t^a in v_i(x,y+tx) is binomial(i,a)v_{i-a}; the coefficient in v_i(x+ty,y) is binomial(m-i,a)v_{i+a}. Distinct torus characters mean a submodule is the span of a subset of these weight vectors. Infinite-field coefficient extraction makes the directed graph of nonzero formal coefficients a valid test of these particular rational modules. The reviewer-written exact implementation enumerates coefficients, not merely finite-field group elements.

For m=2p-1, every coefficient of (x+ty)^m from x^m is nonzero: the base-p digits ofm are(1,p-1), and (1+t)^m=(1+t^p)(1+t)^{p-1}. Every monomial generatesx^m under the other root family, so Sym^m is simple, dimension2p.

For m=2p-3, the nonzero coefficient support fromx^m is W={0,...,p-3} union{p,...,2p-3}. Equivariant Frobenius multiplication realizesW as E^(1) tensor Sym^(p-3)E. Its two ranges are disjoint, giving dimension2p-4. Each nonzero W-submodule containsx^m, soW is simple. The quotient has the two remaining weights(p-1,p-2) and(p-2,p-1); both connecting root coefficients equalp-1, so it is simple. Any complement is forced by torus weights to be the two missing monomial lines. The t^(p-2) coefficient of v_(p-2)(x,y+tx) isv_0, so this complement is not invariant. This proves nonsplitting, includingp=3. Head/socle dimensions coincide atp=3, but their labels do not.

The exact test checks these complete coefficient graphs forp=3,5,7,11,13,17,19,23,29,31, plus every Euler-polarization monomial at ranks2,3 for the associated degrees. All7292 assertions pass. This finite evidence does not establish the universal theorem by itself; the preceding algebraic argument supplies its all-prime part. No supplied scientific programme was imported or executed.

## Stable FI label without a convention shortcut

Use stable rankN>=r and H=Sym^(r-1)E_N tensor E_N. The actual DD manuscript's symmetric-tensor multiplicity formula applies to alpha=(r-1,1,0,...). A simple highest weight containingalpha must dominatealpha, leaving only(r) andlambda. Both multiplicities are1: thelambda highest weight, and the(r-1,1) weight obtained fromx_1^r by its nonzero unipotent coefficientr. Costandard reciprocity givesI_N(r)=Sym^r E_N. The equivariant derivative polarization satisfiesm delta=r id, so multiplication splits. Krull-Schmidt then identifies its kernel withI_N(lambda). On the multilinear weight space, multiplication is summation fromk^r tok. Exact stable Schur functor therefore identifiesFI_N(lambda) with the augmentationA. The direct transposition argument makesA simple of dimensionr-1.

Both original Miyachi0.3 and CP printedp3 expressly use the FI label. No transpose/conjugate relabelling, finite-rank2 Schur functor or implicit Specht/Young interchange is needed.

## Rank-two obstruction and all-rank propagation

DD printedp7 establishes costandard reciprocity and simple-label-preserving contravariant duality. Only(r) strictly dominateslambda; the rank-two Sym^r is simple and cannot containL_2(lambda). HenceI_2(lambda)=nabla_2(lambda)=det tensor Sym^(2p-3)E. Its socle isL_2(2p-2,1) and headL_2(p,p-1). The labels differ for every oddp, so it cannot be contravariantly self-dual. DD2.4 proves, in the polynomial category at arbitrary rank and degree, that a projective injective is self-dual and tilting, and that an injective tilting is projective. ThusI_2(lambda) is nonprojective.

IfI_N(lambda) were projective for someN>=2, that same result would make itT_N(mu). The occurrence ofL_N(lambda) impliesmu dominateslambda, hence mu=(r) orlambda, both of length at most2. DD printedpp8-9 supplies the exact labelled equalities fI_N(lambda)=I_2(lambda) andfT_N(mu)=T_2(mu). The truncation thus makesI_2(lambda) an injective tilting, contradiction. This uses labelled stability, not preservation of arbitrary projectives under an exact idempotent functor.

## Classical published-formula consistency

ELv1 p2 fixes algebraically closed positive characteristic. Its pp4-5 describe the classical and quantum rank-two algebras and removal of determinant twists. The explicit classical analogue following Proposition3.1 permits replacing the quantum integerell byp, with0<=i<=p-2 and positive integern. Substitute n=1,i=p-3,bar_i=1 into its nonsplit Weyl sequence, then apply contravariant duality and restore the determinant shift. The two simple constituents have differences2p-3 and1, with dimensions2p-4 and2. The classical analogue of Theorem3.3 coversdegree2p-1 by a=2,k=0, consistent with simplicity. These formulas corroborate the local derivation; they are not necessary to fill an unproved local gap.

## Exact scope of the historical claim

Miyachi's original contribution, physicalPDFpp28-32, printed944-948, was inspected through its complete contribution and bibliography. Section0.3 defines the q-Schur/Hecke framework andFI-labelled Young modules with invertible parameterq. Section0.4's Conjecture7 on printed946 asserts the existential rank condition for a partition. The characteristic-zero paragraph occurs later in0.5, beginning a different simple-Specht method, and Theorem11 repeats that restriction locally. There is no preceding printed assumption excluding characteristicp withq=1. Thus the explicit counterexample disproves the broad displayed Conjecture7 in that setting. This is an assessment of the displayed proposal, not a claim about an author's unstated intent or a characteristic-zero reformulation.

The stronger membership version is also contradicted: the family in original0.4 hasI_n(lambda) isomorphic to an injective tilting, which DD2.4 makesprojective. The all-rank obstruction excludes such membership. No completeness of that sufficient family is assumed.

## Limits and residual work

No substantive mathematical or scope defect was found in this family. The finite computation's implementation/arithmetical boundaries are explicit; no sampled finite-field action was used as an all-group proof. The optional56-basis/3136-product claim in targetSection6 has not been reproduced here, and target archive code, outputs and archived opinions remain unread. That is outside this scope family, not a substituted inventory assessment. Historical priority and novelty remain unresolved; no failed search is promoted to novelty evidence. No follow-up research question is warranted by this bounded scope audit.
