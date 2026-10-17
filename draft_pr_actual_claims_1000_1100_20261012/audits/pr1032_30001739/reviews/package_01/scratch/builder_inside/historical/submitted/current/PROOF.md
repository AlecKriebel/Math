# A five-segment counterexample to unitary multiplicity in the p-adic smooth-complex scope

**Review status: ACCEPTED_COMPLETE_COUNTEREXAMPLE in the stated scope.** The complete mathematical argument passed a full independent audit and a separate narrow analytic audit. This is an AI-assisted mathematical-audit acceptance, not conventional human peer review or journal acceptance. A computational matching result alone does not establish a period multiplicity. The analytic conclusion uses the published FLO, JPSS, and LM theorems cited below. No novelty claim is made.

## 1. Target and candidate

The adopted target is the characteristic-zero p-adic, smooth admissible complex model in `MODEL.json`. In particular, a noninduced irreducible representation may be a quotient of a reducible induction. The counterexample uses k=1.

Let F=Q_3 and let E/F be the unramified quadratic field extension. Let τ be its nonidentity automorphism. Fix an unramified nontrivial additive character of F and let η be the unramified quadratic character of F× associated with E/F. For K=F or E, put ν_K=|·|_K and

D_K[a,b] = St_(b−a+1)(K) ⊗ |det|_K^((a+b)/2),  a,b integers, a≤b.

Equivalently, in the conventions of FLO §1.5 and LM §2.3, this is the unique irreducible quotient of ν_K^a×ν_K^(a+1)×...×ν_K^b. Local quadratic base change sends D_F[a,b] to D_E[a,b]; D_F[a,b] and D_F[a,b]⊗η are its two distinct essentially square-integrable lifts. Here η on GL_r(F) means η∘det.

Name the segments

A=[0,2], B=[1,4], C=[3,3], D=[2,5], E0=[4,6].

The symbol E0 is a segment, whereas E is the field. In formulas and finite certificates below its short label is `E`.

Let

I_1 = D_E[4,6] × D_E[2,5] × D_E[3,3] × D_E[1,4] × D_E[0,2],

and let π be its unique irreducible Langlands quotient. Its degree is 3+4+1+4+3=15, and the real exponents of its five factors are 5, 7/2, 3, 5/2, 1, in decreasing order. The conclusion is

π^τ ≅ π, π is not itself a proper parabolic induction, and

Hom_(U(V))(π,C)=0 for each of the two Hermitian isometry classes V of dimension 15.

The representation π satisfies the target's k=1 hypotheses and its total multiplicity is 0 rather than 2.

## 2. Precisely identified primary-source interfaces

### FLO

Brooke Feigon, Erez Lapid, Omer Offen, *On representations distinguished by unitary groups*, Publ. Math. IHES **115** (2012),185–323, DOI [10.1007/s10240-012-0040-z](https://doi.org/10.1007/s10240-012-0040-z). Retained published PDF SHA-256 b4b0eb8c749d1244836610bbc56ff8fba0046ce0532f0c87ea179581783da453.

- **§1.4, equation (1.10) and the composition/inverse identities immediately following it, pp.201–202:** Shahidi-normalized intertwiners N satisfy the meromorphic composition and inverse identities. The notation N is that source's notation; it is not an arbitrary rescaling at the singular point.
- **Lemma 1.1(3),(4), p.202:** holomorphy in the appropriate rank-one chamber; a linked pair in standard order has a proper kernel for the unnormalized forward operator M, equal to the image of the holomorphic reverse normalized intertwiner N. Unlinked segment pairs induce irreducibly, with invertible normalized operators when the scalar factors in use are finite and nonzero. For the two nested pairs here those scalar factors are checked explicitly in §4.
- **Definition preceding §2, p.203:** for two segments on one line, FLO's relation δ_i≼δ_j is a_i≤a_j≤b_i≤b_j. It is not the usual linked-segment relation; both relations are checked separately below.
- **§4, equation (4.5), p.225 (normalization definition begins on p.224):** the scalar normalizing an open period is a product over i<j of gamma factors for δ'_i×δ'_j^∨⊗η, times nonzero constants. This identity is meromorphic in all twist variables.
- **§6.2, equation (6.6), p.242:** the unnormalized open-period integral restricted to the open-orbit subspace gives an isomorphism from the Levi invariant-functional space. Its restriction is entire in the twist variables. This is used for linear independence after a linked swap, even if the reversed order has other relevant orbits.
- **§12, equation (12.1), p.283:** for individually τ-invariant essentially square-integrable factors, the F-side lift choices modulo simultaneous η twist give linearly independent Levi functionals over a fixed Hermitian orbit.
- **Theorem 12.4(4), equation (12.5), p.283:** the normalized open periods satisfy the exact permutation-intertwiner functional equation as meromorphic functions. Combined with (4.5), this gives the adjacent-swap scalar ratio written in §4 below. It applies to essentially square-integrable inducing factors; all inducing factors used in this proof are of that kind. It is not being applied to π as a nongeneric inducing factor.
- **Corollary 13.6, p.291:** when there is no i<j with δ_i≼δ_j, the unnormalized lift-labelled open periods at zero form a basis of the **entire** invariant-functional space of the induced representation for each Hermitian form. This completeness interface is indispensable here; the argument does not merely show vanishing of a chosen span.
- **Proof of Theorem 13.11, equations (13.3),(13.4), p.293 and independence argument p.294:** gives the scalar equation and the method excluding equal lift labels across an adjacent linked pair. In this proof that calculation is rederived from (4.5),(12.5) for each specified pair, and only rank-one kernel containment is used. The equality of the whole maximal kernel with a sum of rank-one kernels, invoked later in FLO to establish nonvanishing for ladders, is **not** used.

### LM

Erez Lapid, Alberto Mínguez, *On parabolic induction on inner forms of the general linear group over a non-archimedean local field*, [arXiv:1411.6310v3](https://arxiv.org/abs/1411.6310v3), revised 14 December 2015, PDF heading 15 December 2015; journal reference Selecta Math. (N.S.) **22** (2016),2347–2400. Retained PDF SHA-256 ac54929c76878b080e09ebec149d38130842439aab4c6080620c2bbae6259438.

- **§2.1, Definition 2.2, pp.8–9:** [a,b]≺[c,d] precisely when a<c≤b+1 and b<d. This means linked, with the first segment preceding the second.
- **Theorem 2.6, p.10:** the standard module associated with any ordered multisegment has irreducible cosocle, multiplicity one. This establishes the unique maximal proper submodule of I_1 and of the two isomorphic orders used below. The three orders are ordered forms: no earlier segment precedes a later one.
- **Proposition 2.5(5), p.10, and its Langlands analogue in Theorem 2.6:** L(m+n) occurs in L(m)×L(n), with multiplicity one. Consequently, if that whole product is irreducible, its Langlands multisegment is m+n.
- **§A.5, pp.52–53:** the Zelevinsky involution is a ring involution, preserves irreducibility, and sends Z(m) to L(m). Thus irreducibility of Z(m)×Z(n) is equivalent to that of L(m)×L(n); this is the interface permitting Proposition 5.20 to test the candidate's Langlands multisegments.
- **Definition 5.13, p.34:** a ladder multisegment has strictly ordered starting and ending points. Adjacent linkage is not required for the ladder hypothesis of Proposition 5.20. Every partition tested below has at least one ladder side in this sense.
- **Definition of LC in §5.3, pp.35–36, and Proposition 5.20, p.38:** if one side is ladder, the product is irreducible exactly when LC(m,n) and LC(n,m) both hold. Section 5 below reproduces the finite sets and matching relation, and `HALL_CERTIFICATES.md` exhibits the obstruction for every partition.

### JPSS

Hervé Jacquet, I. I. Piatetski-Shapiro, Joseph A. Shalika, *Rankin-Selberg Convolutions*, American Journal of Mathematics **105**(2)(1983),367–464; [author-hosted published scan](https://www.math.columbia.edu/~hj/Rankin%20Selberg%20convolutions.pdf).

- **Theorem 8.2, setup p.444 and equation (5), p.445; proof equations (20)–(21), pp.447–448:** for two segment representations, with the larger degree first, the Rankin–Selberg factor is the product of the character-level factors obtained from the top character of the longer segment and all characters of the shorter segment. For the trivial cuspidal line this is exactly the min-length product in §4.2. The two statement pages were visually inspected in the published scan; selected proof pages were also inspected by OCR. This is an L-factor interface, not an independent audit of the source proof.

These references are mathematical dependencies, not claims that their full proofs were independently audited here.

## 3. Complete bases in three orders

Fix an arbitrary x in the nonsingular Hermitian matrices of dimension 15, and write H=G_x. No choice of one particular isometry class is made.

For a segment label S in {E,D,C,B,A}, let δ_S=D_E[S] and δ'_S=D_F[S]. A lift label is ε=(ε_E,ε_D,ε_C,ε_B,ε_A)∈{0,1}^5; it means the F-side datum δ'_S⊗η^ε_S. Fix ε_E=0 to choose representatives modulo simultaneous η twist.

Use three orders:

O1=(E,D,C,B,A), O2=(E,C,D,B,A), O3=(E,D,B,C,A).

Each has no earlier FLO ≼ relation. Among distinct segments, increasing both endpoints is necessary for ≼. In these orders each comparable-endpoint pair occurs with the larger endpoints first; the only reversed starting-point pairs are the strict containments D⊃C and B⊃C, which have opposite endpoint inequalities and hence cannot satisfy ≼ in either direction. Direct substitution in a_i≤a_j≤b_i≤b_j confirms all ten pairs in each order.

Corollary 13.6 therefore supplies, for each order O_r, a basis

{J_(r,ε)(0): ε_E=0}

of all Hom_H(I_r,C), of size 16. These are the unnormalized open periods. In particular every pullback of a period on π to I_1 has one and only one such expansion.

## 4. Intertwiner calculations and the pentagon

### 4.1 The adjacent-swap coefficient

Let an order contain adjacent factors δ_i,δ_j, and let s swap them. Use the reverse normalized rank-one operator

R_s(λ)=N(s^−1,sδ,sλ): I_(sδ)(sλ) → I_δ(λ).

Equations (4.5),(12.5) give, up to a nonzero scalar or everywhere nonvanishing monomial irrelevant to zeros and poles,

J_(δ,ε)(λ) ∘ R_s(λ)
 = c_(ij,ε)(λ) J_(sδ,sε)(sλ),

where

c_(ij,ε)(λ)
 = γ(λ_j−λ_i, δ'_i^∨×δ'_j⊗η^(1+ε_i+ε_j),ψ')
   / γ(λ_i−λ_j, δ'_i×δ'_j^∨⊗η^(1+ε_i+ε_j),ψ').

This is the same ratio displayed in FLO (13.3). Fixed labels follow their segments when an order changes. E remains first in both swaps used here, so the representative convention ε_E=0 is unchanged.

### 4.2 Explicit gamma-factor check

For segments [a,b],[c,d] and a character sign χ∈{1,η}, let r=min(b−a+1,d−c+1). By JPSS Theorem 8.2 (equation (5), pp.444–445), the unramified Rankin–Selberg factor is

L(s,D_F[a,b]×D_F[c,d]^∨⊗χ)
 = product_(j=0,...,r−1) (1−χ(3)3^(−s−b+c+j))^−1.

The epsilon factor is nonzero. Hence zeros and poles of gamma are those of L(1−s,dual)/L(s,original).

For **strictly nested** segments, the smallest exponent in either directional L(0) is at least 1: if [a,b] strictly contains [c,d], these minima are b−d and c−a. All directional gamma factors at zero are therefore finite and nonzero, for χ=1 and χ=η. In the two actual nested swaps D,C and C,B, the two directional L exponents are exactly 2 and 1.

For a **linked pair in standard order**, write the higher segment as [a,b] and the lower as [c,d], where c<a≤d+1 and d<b. For χ=1, the forward L(0) exponents are all positive, but the reverse L(1) has exactly one zero exponent. Thus the forward gamma has a pole. The reverse gamma has either a zero (overlapping case) or a finite nonzero value (adjacent case). Consequently c_(ij,ε)(0)=0 when ε_i≠ε_j. For χ=η, every real-integer L factor is finite and nonzero, because η(3)=−1, so c_(ij,ε)(0) is finite and nonzero when ε_i=ε_j. The ratio is holomorphic at zero in both cases. This establishes exactly the zero/nonzero alternative required below.

The two **unlinked** swaps have invertible normalized intertwiners at zero. Indeed, both directions are holomorphic by the rank-one normalization and FLO Lemma 1.1(3); the just-computed E-side normalizing gamma factors are finite and nonzero (replace 3 by 9). The meromorphic inverse identity specializes at zero. The F-side coefficient ratio is finite and nonzero for every ε, by strict nesting. Since both period families are holomorphic at zero by §3, transport takes each basis vector to a nonzero scalar times the vector with the same fixed segment labels. It does not introduce linear combinations of labels or discard coordinates.

### 4.3 Why every period on the quotient obeys the adjacent constraint

Let I_r be any of the three orders, and p_r:I_r→π its irreducible quotient map, obtained from p_1 using the unlinked isomorphism when necessary. The module I_r has a unique maximal proper submodule, ker p_r.

For an adjacent linked pair in standard pair-order in I_r, replace that pair by the image of its reverse normalized operator. By FLO Lemma 1.1(4), this is the proper rank-one kernel of the unnormalized forward operator M. Exactness and faithfulness of parabolic induction make its induction with all the other factors a proper submodule K_ij of I_r. Thus K_ij⊂ker p_r. This containment uses no description of the rest of ker p_r.

If ℓ∈Hom_H(π,C), write ℓ∘p_r=Σ_ε a_(r,ε)J_(r,ε)(0), using the complete basis. It annihilates K_ij, so its composition with R_s(0) is zero. Restrict the meromorphic functional equation of §4.1 to the open-orbit subspace of the domain of R_s. These restricted open periods are entire, and are linearly independent at zero by FLO (12.1),(6.6). Since the coefficient ratios and R_s are holomorphic at zero, evaluation gives

a_(r,ε)c_(ij,ε)(0)=0 for every ε.

The nonzero alternative from §4.2 therefore forces a_(r,ε)=0 whenever ε_i=ε_j. This conclusion concerns an arbitrary invariant functional on π; it is not a completeness conjecture for periods on π.

### 4.4 Inconsistent conditions

In O1, the adjacent linked pairs E,D and B,A force

ε_E≠ε_D, ε_B≠ε_A.

Swap the strict containment D,C to obtain O2. Since transport preserves nonzero coefficient coordinates, the adjacent linked pairs E,C and D,B in O2 additionally force

ε_E≠ε_C, ε_D≠ε_B.

Swap the strict containment C,B in O1 to obtain O3. Its adjacent linked pair C,A additionally forces

ε_C≠ε_A.

Thus a potentially nonzero coefficient would require opposite labels along E—D—B—A—C—E, a cycle of odd length. Summing the five relations ε_i+ε_j=1 in F_2 gives 0=1. There is no such ε, so every coefficient vanishes and ℓ=0.

Because x was arbitrary, this yields vanishing on both Hermitian classes.

## 5. Why the candidate is noninduced

Suppose π were an entire irreducible induction from a proper Levi. By exactness and faithfulness of induction, a nontrivial grouping of the inducing factors gives a whole irreducible two-factor product. Write the two irreducible factors as L(m_1),L(m_2). By LM Theorem 2.6 and Proposition 2.5(5), π then has multisegment m_1+m_2. Consequently m_1,m_2 partition the five distinct segments A,B,C,D,E into nonempty subsets.

There are precisely five singleton/four-element and ten two-element/three-element partitions. Every such partition has a ladder side under LM Definition 5.13. In particular, the only nonladder two-element subsets are DC and CB, whose complements EBA and EDA are ladders. Hence Proposition 5.20 applies in every case, and the Zelevinsky ring involution in §A.5 transfers its irreducibility equivalence from Z to L without changing the multisegments.

For arbitrary m,n define

X_(m,n)={(u,v)∈m×n:u≺v},
Y_(m,n)={(u,v)∈m×n:(u−1)≺v},

where u−1 subtracts one from both segment endpoints. A vertex (u2,v2)∈Y can match (u1,v1)∈X precisely if either u1=u2 and v2≺v1, or v1=v2 and u1≺u2. LC(m,n) means an injective matching covering X.

For each partition, `HALL_CERTIFICATES.md` gives a directed LC condition and an X vertex with no possible Y neighbor. Each is a singleton Hall obstruction. Thus every partition fails at least one necessary LC condition, so every proposed two-factor product is reducible. This rules out all proper induced realizations of π.

The certificates are independently checked with a set-based definition of linked segments in `check_hall_certificates.py`; the original matching script uses the endpoint-inequality definition. Both agree. These finite checks establish no analytic multiplicity on their own.

## 6. Remaining target hypotheses and accepted conclusion

The Langlands quotient is irreducible admissible smooth over C by classification. Its supercuspidal character ν_E is τ-invariant; hence all five segment representations, their standard module, and its uniquely determined irreducible quotient are τ-invariant. For k=1, the target's entire-product irreducibility condition is automatic, and there is no forbidden replacement of a multi-factor reducible product by a constituent: the one target factor is π itself, whose noninduced property was proved separately in §5.

The complete argument supplies an exact-scope counterexample. The full independent audit and the separate analytic audit accepted the complete, holomorphic, label-diagonal transport of the period basis across the two nested swaps. The proof deliberately avoids the general standard-module kernel-generation conjecture. Reports about a related kernel conjecture have no dependency role here. This conclusion is limited to the documented characteristic-zero p-adic smooth admissible complex target; it is not an all-local-fields assertion. Historical priority remains unclaimed.
