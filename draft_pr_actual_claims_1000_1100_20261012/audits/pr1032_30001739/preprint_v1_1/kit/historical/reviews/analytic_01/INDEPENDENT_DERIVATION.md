# Independent derivation before consulting historical verdicts

Review head: `810d52306312623ecfe01ecbc5f5f0dd360972c3`.
Written 2026-10-13 UTC. Historical FULL_AUDIT.md and ANALYTIC_AUDIT.md have not been read at this checkpoint. Neither has the new combinatorial review family.

## Exact analytic claim and proof obligation

For F=Q_3 and its unramified quadratic extension K, let δ_S=D_K[S] for S in A=[0,2], B=[1,4], C=[3,3], D=[2,5], E=[4,6]. Let π be the irreducible quotient of δ_E×δ_D×δ_C×δ_B×δ_A. The assigned analytic claim is Hom_H(π,C)=0 for an arbitrary H=U(V) in dimension 15. This document proves that claim conditional on the freshly inspected published theorems listed here. Noninduction of π is a separate combinatorial obligation.

## Primary interfaces actually inspected

FLO's published Numdam body matches SHA256 b4b0eb8c749d1244836610bbc56ff8fba0046ce0532f0c87ea179581783da453. Its p.201 defines N=C M, where C contains gamma factors, and gives meromorphic composition/inverse identities. Thus N is specifically the Shahidi-normalized operator, rather than M with a convenient ad hoc scalar. On p.202, Lemma 1.1(3) assumes unitary square-integrable input δ_1,δ_2 and a strict positive difference of real twist parameters: M at the positive chamber point and N at the negative chamber point are holomorphic. Part (4) identifies the proper kernel of M in the linked positive chamber with the image of the reverse N. For the actual segment factors one must separate St_length from its real center; this is done below.

On p.283, (12.1) states linear independence of 2^(t-1) lift-labelled Levi forms restricted to M∩x·G, and Theorem 12.4(4), (12.5), gives the meromorphic period-permutation equation for individually generic base-change-compatible factors. Each of the factors here is essentially square-integrable, and its two F-lifts are D_F[S] and D_F[S]η. This use does not require the entire induced representation, or π, to be generic. On p.242, (6.6) identifies Levi functionals with invariant forms on the open-orbit subspace, and its preceding compact-support argument makes the restricted periods entire in the twists. On p.291, Corollary 13.6 makes the unnormalized periods a basis of the entire Hom space whenever no earlier factor satisfies FLO's relation a_i≤a_j≤b_i≤b_j. These statements have been read in the source bodies, not merely source abstracts.

JPSS's published author-hosted scan, pp.444–445, §8.2, describes square-integrable segments with descending constituent characters and proves L(s,π×σ)=∏ L(s,π_top×σ_j), with the longer GL degree first. Both statement pages were visually inspected; pp.446–449 were read by OCR as a check of the shift conventions, especially equations (20)–(21). Here all cuspidal characters have GL degree one, so degree ordering is length ordering. If the first segment is shorter, apply symmetry first. Either way the exponent set is b-c-j, 0≤j<min(lengths), for D_F[a,b]×D_F[c,d]^∨. FLO p.200 provides the gamma definition in terms of L(s) and the dual L(1-s).

LM v3 §2.2 defines an ordered form by absence of a preceding linked segment in an earlier position; §2.3, Theorem 2.6, gives its irreducible multiplicity-one cosocle. The three orders below satisfy that definition. This ensures a unique maximal proper submodule, even for the two reordered inductions whose real centers are not decreasing.

## Complete bases and all parameters

The lengths are (3,4,1,4,3), and centers in order E,D,C,B,A are (5,7/2,3,5/2,1). Each segment is fixed by the field involution. The F-side labels ε_S∈{0,1} choose D_F[S]η^ε_S. Quotient by the common η twist and fix ε_E=0; there are 16 representatives.

The orders are O1=(E,D,C,B,A), O2=(E,C,D,B,A), O3=(E,D,B,C,A). Every pair whose endpoints increase together appears in the larger-first direction. The only changed pairs D,C and C,B are strict containments, which satisfy FLO's relation in neither direction. Therefore Corollary 13.6 supplies all 16 unnormalized periods as a complete basis for Hom_H(I_r,C) in each order r, for arbitrary Hermitian x.

Let s exchange adjacent factors i,j and put u=λ_i-λ_j. By applying (12.5) to the reverse normalized operator R=N(s^-1,sδ,sλ) and dividing by the n-factors in (4.5),

J_(δ,ε)(λ) R(λ) = κ_(ij,ε)(λ) [γ(-u,δ'_i^∨×δ'_j η^(1+ε_i+ε_j))/γ(u,δ'_i×δ'_j^∨ η^(1+ε_i+ε_j))] J_(sδ,sε)(sλ).

Here κ is a nonzero constant under the published Whittaker identifications (allowing choices of models gives an everywhere nonvanishing factor). All other pair factors cancel because the swap is adjacent. Labels follow the factors. This formula agrees with FLO (13.3), freshly read, and preserves the original η parity: equal labels put η on the Rankin–Selberg pair, while unequal labels put the trivial character there.

## Scalar derivation, including orders

Write ζ=χ(3)∈{1,-1}, P={b-c-j:0≤j<r}, Q={d-a-j:0≤j<r}, r=min(b-a+1,d-c+1). JPSS gives

L(u,δ'_i×δ'_j^∨χ)=∏_(p∈P)(1-ζ3^(-u-p))^-1,
L(-u,δ'_i^∨×δ'_jχ)=∏_(q∈Q)(1-ζ3^(u-q))^-1.

After dropping only nonvanishing epsilon factors, the scalar ratio is the exact rational germ

∏_(q∈Q)(1-ζ3^(u-q)) / ∏_(p∈P)(1-ζ3^(-u-p))
  × ∏_(q∈Q)(1-ζ3^(-1+u-q)) / ∏_(p∈P)(1-ζ3^(-1-u-p)).

For ζ=-1 all individual factors at u=0 are nonzero, even at exponent zero or negative exponents; the ratio is a unit. For ζ=1 a factor has a simple zero exactly at exponent zero. The scalar's zero order is #Q(0)+#Q(-1)-#P(0)-#P(-1).

Actual directed pairs and exponent sets:

| Pair | P | Q | scalar order for unequal labels |
|---|---|---|---:|
| E,D | 4,3,2 | 1,0,-1 | 2 |
| B,A | 4,3,2 | 1,0,-1 | 2 |
| E,C | 3 | -1 | 1 |
| D,B | 4,3,2,1 | 2,1,0,-1 | 2 |
| C,A | 3 | -1 | 1 |
| D,C | 2 | 1 | 0 |
| C,B | 2 | 1 | 0 |

The nested ratios are units for either parity. The E-field scalar normalizers for those rank-one operators use q_K=9 and the trivial character, giving the same regularity. Both actual forward pair-center differences equal 1/2: (7/2)-3 and 3-(5/2). Thus Lemma 1.1(3) gives M_forward and N_reverse holomorphic in a neighborhood of λ=0. The forward normalizer is also a unit by the displayed exponent calculation, so N_forward is holomorphic. The meromorphic inverse identity then specializes to N_forward N_reverse=1 in both directions. This is an actual invertible specialization, not a formal inverse of a singular operator.

For each linked pair the higher segment precedes the lower in decreasing centers. The unnormalized M_forward is holomorphic, and Lemma 1.1(4) supplies a nonzero proper rank-one kernel equal to the image of holomorphic R_reverse. Exact parabolic induction makes the corresponding full induced submodule proper and preserves its image. It is therefore contained in the unique maximal proper submodule of I_r. It is not necessary to know that all such rank-one kernels generate that maximal submodule.

## Descending a quotient period

Any ℓ∈Hom_H(π,C) pulls back uniquely to ∑ a_(r,ε)J_(r,ε)(0). It annihilates each just-described kernel, hence composing with its reverse normalized operator gives zero. The swapped order after a linked pair may have additional relevant non-open orbits or meromorphic full periods; completeness or holomorphy there is not needed. Restrict the domain to its open-orbit subspace. Its J^open are entire and independent at zero by (12.1)+(6.6). Since R and the scalar ratio are holomorphic at zero, specialization forces a_(r,ε)c_(ij,ε)(0)=0 individually. Consequently a_(r,ε)=0 for equal labels across each linked edge.

Transport from O1 to O2 or O3 by the corresponding nested R is invertible and label-diagonal with unit scalars. If p_r=p_1R, its expansion has a_(r,ε)=unit·a_(1,ε); nonzero coordinates are preserved. O1 enforces E≠D and B≠A. O2 enforces E≠C and D≠B. O3 enforces C≠A. The resulting E-D-B-A-C-E cycle has five edges. Adding its opposite-label equations over F_2 gives 0=1, so every coefficient vanishes.

Because x is arbitrary, the deduction applies to every Hermitian isometry class. The analytic conclusion is obtained from the published analytic theorems and the independent scalar argument; a finite label enumeration alone would not establish the Hom multiplicity.

## Adversarial boundary checks

1. Linked adjacency and linked overlap behave differently: orders 1 and 2, respectively, but both give zero for unequal labels. Treating them both as simple zeros would be numerically inaccurate without harming the vanishing conclusion.
2. Unlinked pairs in general need not have unit scalar normalizers. For example [0,2] containing [1,2] has a shared endpoint and a directional L(0) pole. The submitted argument uses strict containment in both endpoints, where both directional minima are positive. No general unlinked-unit claim is needed.
3. Equal center parameters would not satisfy the strict chamber condition of the cited Lemma 1.1(3). The two actual nested pairs have difference 1/2, and the actual linked differences are 3/2,3/2,2,1,2, so no chamber-wall extrapolation occurs.
4. Inverting the direction of N without redoing the scalar ratio would reverse which labels survive. The submitted reverse choice has the same orientation as FLO's (13.3), and equal labels are the coordinates annihilated on the quotient.
5. A functional on a singular swapped induction need not be spanned by full open periods. The proof uses only their independent restrictions, exactly where FLO (6.6) applies.

Assigned analytic route status at this independence checkpoint: verified, conditional only on the stated primary theorems. No central unsupported replacement has appeared.
