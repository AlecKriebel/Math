# Unitary-period multiplicities: a credited resolution and a formulation correction

Problem 30001738 / OWR-4804-006. Checked 2026-10-07.

## Disposition

**The intended p-adic irreducible-generic source problem is solved in prior literature.** Its answer is yes: the total multiplicity is (2^k) when all (k) inducing essentially square-integrable factors are individually Galois invariant. Credit belongs to Raphaël Beuzart-Plessis, extending Feigon–Lapid–Offen. No new solution or novelty is claimed here.

The catalogue's weaker assumption that only the whole induced representation is invariant changes the question and makes its proposed (2^k) answer false. Section 5 gives a concrete counterexample. These are separate conclusions.

This is an AI-authored exposition and hypothesis audit, with exact finite controls. It is not a new proof of the analytic multiplicity theorem, a formal proof-assistant verification, or human peer review. No independent audit is claimed by this author packet.

## 1. Three statements that must be distinguished

The workshop contribution is Erez Lapid, joint work with Brooke Feigon and Omer Offen, in [OWR], pp.727–736. Its Conjecture 3, p.733, attaches both conditions, essentially square-integrable and Galois invariant, to each factor. The report introduces the Hermitian-space action on p.729 and the equivariant-map multiplicity on p.731. Its single conjecture sentence does not restate every standing category assumption. We do not silently turn that abbreviated sentence into a theorem for every local field or every reducible induced module.

The detailed primary treatment [FLO], §13, begins by restricting to quadratic extensions of p-adic fields (p.289); §13.6 explicitly specifies irreducible induced representations (p.297). Theorem 0.2 and Conjecture 13.17 give the generic multiplicity question, including repeated factors. The notation for normalized induction and the complex representation category occurs in §§1.3–1.4. Thus the precise source problem used here is:

Let (F) be a finite extension of (ℚ_p), let (E/F) be quadratic, and let (n_1+⋯+n_k=n), with every (n_i>0). Let (δ_i) be an irreducible smooth complex essentially square-integrable representation of (GL_{n_i}(E)), and suppose (δ_i^τ ≅ δ_i) for every (i). Assume that the normalized induction

 π=δ_1 × ⋯ × δ_k

is irreducible. Then (π) is generic and the question is whether (m_X(π)=2^k). Genericity of irreducible induction from generic factors is the standard heredity theorem for Whittaker functionals; essentially square-integrable representations of general linear groups are generic. These standard representation-theoretic facts are dependencies, not new assertions proved by the finite controls. They are used in [FLO, §1.4] and [BP, §5.1]. Equivalently, one may explicitly impose genericity in the statement.

The catalogue instead replaces individual invariance by (π^τ ≅ π), omits irreducibility, and says merely local fields. This packet corrects those scope differences; it does not claim that the later p-adic theorem settles all literal broader readings.

## 2. Definitions and a direct identification of the multiplicity

All vector spaces and functionals below are over (ℂ). The automorphism (τ) belongs to (Gal(E/F)); it acts entrywise on matrices. The twist is the pullback

 π^τ(g)=π(τ(g)).

It does not conjugate coefficients of vectors or scalars, and it is not a contragredient or conjugate-contragredient.

Set (G=GL_n(E)),

 X={x ∈ G:τ(x)^t=x},    x·g=τ(g)^t xg,
     H_x={g:x· g=x}.

If (V) is the space of (π), use the full algebraic dual (V^*=Hom_{ℂ}(V,ℂ)) in

 E_G(X,V^*)={α:X →  V^*:
       α_{x· g}=α_x ∘ π(g)}.

This is the meaning of the workshop's (Hom_G(X,π^*)). It is not a morphism of algebraic varieties and not an ordinary linear Hom out of the set (X). The smooth contragredient (π^∨), when used elsewhere, is a different object from the full dual.

**Lemma.** For a set (R) of orbit representatives there are natural vector-space isomorphisms

 E_G(X,V^*) ≅ ∏_{x ∈ R}Hom_{H_x}(V,ℂ)
  ≅ Hom_G(V,C^∞(X)).

**Proof.** Evaluate (α) at each representative. For (h ∈ H_x), equivariance gives (α_x=α_x ∘ π(h)), so the result is invariant. Conversely, given invariant functionals (ℓ_x), define (α_{x · g}=ℓ_x ∘ π(g)). If (x · g=x · g'), then (g'=hg) for some (h ∈ H_x); invariance makes the definition independent of the choice. The equation for equivariance follows from multiplication of the two group elements. These constructions are inverse and linear.

Associate to (α) the map (T(v)(y)=α_y(v)). It intertwines (π) with right translations because

 T(π(g)v)(y)=α_y(π(g)v)=α_{y· g}(v)=T(v)(y· g).

For each (v), smoothness provides an open compact subgroup (K) fixing (v). The displayed equation shows that (T(v)) is right (K)-invariant, hence locally constant on every homogeneous orbit. The orbits in this p-adic Hermitian setting are open, so it is locally constant on (X). Conversely, evaluation of an intertwiner gives the required equivariant map. This proves the second identification. In this setting (R) has two elements, so the product equals the direct sum. Consequently

 m_X(π):=dim E_G(X,V^*)
       =Σ_{x ∈ R}dim Hom_{H_x}(π,ℂ).

The two-orbit classification of nondegenerate p-adic Hermitian forms is a standard dependency, also stated in [OWR, p.729] and [BP, §3.2]. Distinct forms can have isomorphic stabilizer groups; they still count as different orbits. ∎

## 3. The credited theorem and the complete reduction

**External theorem used.** Beuzart-Plessis [BP, Theorem 3; equation (5.2.1), Theorem 5.2.2] proves that for an irreducible smooth complex generic representation of (GL_n(E)), with (E/F) quadratic p-adic,

    m_X(π)=d(π),
    d(π)=2^{r(π)} if π^τ ≅ π, and d(π)=0 otherwise.

where (r(π)) is the number of individually (τ)-fixed factors in the essentially square-integrable Langlands inducing multiset, **counting occurrences**. The number (d(π)) is the degree of the finite quadratic base-change map, defined by the length of its fiber algebra. It need not equal the number of points in the fiber. At each form its multiplicity is (ceil(d/2)) for a quasi-split unitary group and (floor(d/2)) otherwise. The p-adic assumption is explicit at the opening of §5. The theorem has no distinctness condition. The 2021 arXiv version is published in Journal of Number Theory 230 (2022), 5–63; the publisher independently confirms that bibliographic status.

**Corollary (the precise source target).** Under the hypotheses of §1,

 dim Hom_G(X,π^*)=2^k.

**Proof.** Entrywise (τ) preserves the standard parabolic and its modular character. Pullback therefore commutes with normalized parabolic induction. Tensor the given intertwiners (δ_i^τ ≅ δ_i) and induce them to obtain (π^τ ≅ π). The irreducibility hypothesis and Whittaker heredity put (π) in the theorem's generic category. Its essentially square-integrable inducing factors, in Langlands order, form the same multiset as the given factors; this is the standard uniqueness and permutation property for irreducible generic induction. Thus every one of its (k) occurrences is fixed, and (r(π)=k). The external theorem gives (m_X(π)=2^k), and §2 identifies this with the workshop's Hom. Equivalently, since (k≥1), each of the two orbit multiplicities is (2^{k-1}), whether its group is quasi-split or not. Their sum is (2^k). Repetition changes neither the number of occurrences nor this argument. ∎

There is no remaining mathematical gap for this precise corollary **relative to the credited external theorem and the explicitly named standard facts**. There is no claim here to reprove local trace formulas, the Whittaker Paley–Wiener theorem, or the classification of general linear group representations. Those are substantial dependencies of the literature result.

## 4. Why counting distinct lifts gives the wrong singular answer

Here is an elementary model that also occurs in unramified rank-two base change. Write (s=z_1+z_2) and (p=z_1z_2) for an unordered pair of nonzero complex parameters. Squaring each parameter sends

 (s,p) ↦ (A,B)=(s^2-2p,p^2).

At the target pair ({1,1}), or ((A,B)=(2,1)), the fiber algebra is

 ℂ[s,p,p^{-1}]/(s^2-2p-2,p^2-1)
  ≅ ℂ[s]/(s^2(s-2)(s+2)).

To verify the isomorphism, eliminate (p=(s^2-2)/2) and substitute into (p^2-1); the result is (s^2(s^2-4)/4). In the quotient (p^2=1), so inverting (p) adds nothing. Division by the monic degree-four polynomial gives the basis (1,s,s^2,s^3), proving that the algebra has dimension four. Its three maximal ideals correspond to (s=-2,0,2). Their lengths are (1,2,1), since the polynomial factors into relatively prime factors ((s+2),s^2,(s-2)). Thus three geometric points carry total multiplicity four.

For an unramified quadratic extension, unramified character parameters square under base change: the norm of a common uniformizer is its square. Accordingly (π=1_{E×} × 1_{E×}) has two repeated fixed factors and total unitary-period multiplicity four. It is irreducible by the usual (GL_2) principal-series criterion: the ratio (1) is neither (|·|_E) nor (|·|_E^{-1}). This example is an illustration of the credited formula, not a new proof of that formula. Using the number of distinct factors (one) or distinct lift parameters (three) would both give the wrong answer.

## 5. A concrete counterexample to only assuming invariance of the product

Take (F=ℚ_3) and its unramified quadratic extension (E). Its residue field is (𝔽_9=𝔽_3[i]/(i^2+1)). Set (u=1+i). Direct multiplication gives (u^2=2i), (u^4=-1), and (u^8=1), so (u) generates the eight nonzero elements.

Let (ζ) be a primitive eighth root of unity. Define a smooth character of (E×=3^{ℤ}𝒪_E×) by

 χ(3)=1,    χ(a)=ζ^j  when ā=u^j.

This is a well-defined finite-order character, trivial on principal units. The nontrivial Galois automorphism induces (a ↦  a^3) on the residue field and fixes (3). Hence (χ^τ=χ^3 ≠ χ), and ((χ^τ)^τ=χ). Both are essentially square-integrable representations of (GL_1(E)), since that group equals its center.

Consider normalized induction (π=χ × χ^τ) to (GL_2(E)). The ratio (χ/χ^τ=χ^{-2}) is nontrivial on units; it cannot be either unramified character (|·|_E^{±1}). The two cuspidal characters are consequently disjoint in the sense of [FLO, §1.5, p.203]: neither belongs to the other's integral absolute-value twist line. The disjoint-induction fact stated there makes (π) irreducible; Whittaker heredity makes it generic. Permuting its two inducing characters preserves its isomorphism class, so (π^τ ≅ π). This disjoint-induction fact and the permutation property are credited representation-theoretic dependencies, not consequences of the finite-field tests.

Neither factor is individually fixed. Thus (r(π)=0), and the credited theorem gives (m_X(π)=1), whereas (2^k=4). More precisely the split Hermitian form contributes one and the nonsplit form contributes zero. This is a counterexample to the weakened catalogue formula within the p-adic irreducible generic category itself. It does not contradict the source target, whose individual-invariance hypothesis it fails.

The arithmetic twist sends the character exponent (1 ↦ 3) modulo eight. Coefficient conjugation would send (1 ↦ 7), and conjugate-duality (1 ↦ 5). These distinct values are an exact check on which involution was used.

## 6. Scope and verification limits

- The affirmative corollary concerns finite extensions of (ℚ_p), complex coefficients, and irreducible induction. No assertion for arbitrary reducible full induced modules, their individual nongeneric quotients, (ℂ/ℝ), positive-characteristic local fields, or modular coefficients is inferred from it.
- The workshop sentence alone is compressed. Its contextual identification with the precise p-adic question is backed by the original collaborators' detailed §13 formulation, not by silently adding hypotheses to manufacture a solution.
- The finite tests independently check elementary residue-field arithmetic, the singular fiber algebra, occurrence counting, the two-orbit arithmetic and rejection of unsupported scope. They do not compute infinite-dimensional Hom spaces or prove the external analytic theorem.
- Repeated factors are allowed. No finite enumeration is offered as a proof for arbitrary rank. The source-free algebra proofs above establish the elementary claims without reliance on a bounded search.
- The chronological ledger records zero new source-problem proof attempts: the prior theorem was identified before beginning a new attempt. Literature retrieval, scope reconciliation, this expository reduction and packaging are not counted as research turns.

## References

[OWR] E. Lapid, “Unitary periods and distinction; representation-theoretic aspects,” joint work with B. Feigon and O. Offen, in *Automorphic Forms: New Directions*, Oberwolfach Reports 8 (2011), contribution pp.727–736, Conjecture 3 p.733. https://doi.org/10.4171/owr/2011/14

[FLO] B. Feigon, E. Lapid, O. Offen, “On representations distinguished by unitary groups,” *Publications Mathématiques de l'IHÉS* 115 (2012), 185–323. https://doi.org/10.1007/s10240-012-0040-z ; https://www.numdam.org/item/PMIHES_2012__115__185_0/

[BP] R. Beuzart-Plessis, “Multiplicities and Plancherel formula for the space of nondegenerate Hermitian matrices,” *Journal of Number Theory* 230 (2022), 5–63. https://doi.org/10.1016/j.jnt.2021.06.001 ; inspected version https://arxiv.org/abs/2008.05036v2
