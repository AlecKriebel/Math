# Independent analytic audit of the frozen five-segment candidate

## Verdict and limits

**NARROW ANALYTIC AUDIT: PASS.** No fatal gap was found in the full-space basis, nested-swap transport, or necessary linked-pair constraints in sections 2–4 of the frozen proposed proof. The argument establishes vanishing of the periods on the specified Langlands quotient, subject to the stated published representation-theoretic dependencies. This is an independent source/application audit, not a reproof of those dependencies.

This audit does **not** certify section 5's noninducedness argument, the 15 partition tests, overall mathematical acceptance, novelty, or publication readiness. The final manuscript disposition is recorded separately in ACCEPTANCE.md.

The only source citation error found is minor: FLO equation (4.5) is on **printed p.225**, although the definition of its normalizing factor begins on p.224. A wording clarification is also recommended: the rank-one kernel in Lemma 1.1(4) is the kernel of the **unnormalized forward operator M**, not the generally singular forward normalized operator N. The candidate uses the correct reverse normalized operator in its actual argument.

## Frozen object and source identity

The audited object is the complete five-segment proof. The current public proof incorporates the locator correction and operator-kernel clarification identified by this audit.

Primary dependencies inspected independently:

- Feigon–Lapid–Offen (FLO), *On representations distinguished by unitary groups*, Publ. Math. IHES 115 (2012), 185–323. [Published PDF](https://www.numdam.org/item/10.1007/s10240-012-0040-z.pdf). Local PDF hash: `b4b0eb8c749d1244836610bbc56ff8fba0046ce0532f0c87ea179581783da453`.
- Jacquet–Piatetski-Shapiro–Shalika (JPSS), *Rankin–Selberg Convolutions*, AJM 105 (1983), 367–464. [Author-hosted published scan](https://www.math.columbia.edu/~hj/Rankin%20Selberg%20convolutions.pdf). Local PDF hash: `d9feed6388ca5acf02ecc6a8cce984871a7c28f062ff441e45a71fa2d8962245`.

Both official/author-hosted URLs were also opened successfully during this audit. No access-denied source was revisited or bypassed.

Visual inspection covered FLO printed pp.202,225,242,283,291,293,294 and JPSS pp.444–445. Additional FLO pages, including pp.201,203,213–215,217,243–246,281–282, and JPSS proof pp.447–448 were inspected through local text extraction/OCR. The independently rendered pages and extracted text are private source-inspection evidence, not publication content.

## 1. Data, theorem hypotheses, and whole-space completeness

Write the five segments in the original order as

E=[4,6], D=[2,5], C=[3,3], B=[1,4], A=[0,2].

Each inducing representation is an essentially square-integrable representation on the trivial cuspidal line over the quadratic field E/F. Each is individually tau-invariant. The F-side segment and its eta twist are distinct lifts: their cuspidal characters differ by the nontrivial unramified quadratic character, which cannot equal a real integral power of the absolute-value character.

FLO's relation on p.203 is the endpoint condition a_i <= a_j <= b_i <= b_j, including equality of segments. It is not the usual linked-segment condition. The orders

- O1=(E,D,C,B,A)
- O2=(E,C,D,B,A)
- O3=(E,D,B,C,A)

have no earlier-to-later instance of that relation. This follows directly from endpoints: all endpoint-comparable pairs are oriented with the larger endpoints first; the two differently oriented pairs are strict containments. The independent script separately checked all ten pairs in each order.

FLO Corollary 13.6, p.291, applies to precisely such individually tau-invariant essentially square-integrable Levi data in the p-adic setting. Its conclusion is both holomorphy at zero and a basis of the **whole** invariant-functional space, not merely independence of selected open periods. It applies for every fixed x. The candidate therefore has 16 basis elements in each of the three orders.

The mechanism is corroborated by Lemma 6.10, pp.243–244, and Lemma 6.7, p.242: the endpoint condition eliminates relevant non-open strata. Hence no additional functional supported on a non-open stratum is omitted from this expansion.

## 2. Fixed Hermitian orbit and the label quotient

There are 32 independent choices of the five F-side lifts before the simultaneous eta identification. On a fixed Hermitian orbit, a simultaneous eta twist multiplies the corresponding Levi functional by a nonzero determinant sign; see FLO (3.13), p.217. It does not set that functional equal to zero.

FLO (12.1), p.283, states the requisite independence after restriction to M intersected with the fixed orbit x.G. Its hypothesis is the square-integrable, individually tau-invariant Levi datum. These hypotheses hold here. Selecting epsilon_E=0 yields one representative of every simultaneous-twist pair. The set has 16 members and satisfies Corollary 13.6.

For additional concreteness, on the Levi orbit labels the twists behave as characters of a five-variable sign group subject to one fixed product constraint. Complementary label vectors differ by the fixed product sign; there is no other identification. The resulting 16 characters are independent. This is the finite Fourier explanation of the fixed-orbit assertion, not an extra completeness assumption.

The two transport swaps never move E. Thus the representative condition epsilon_E=0 is unchanged. Segment labels travel with their factors. Neither a change of Hermitian class nor an averaging over the two classes occurs anywhere in the argument.

## 3. Functional equation and its direction

Put J_delta for an unnormalized open-period family and calligraphic J_delta for its normalized family. FLO defines calligraphic J_delta=n_delta J_delta on pp.224–225. Theorem 12.4(4), equation (12.5), p.283, applies to the F-side **Levi representation** whose individual base changes are generic. Every essentially square-integrable factor here has that property. It does not require the entire five-factor induction, or its Langlands quotient, to be irreducible or generic.

Apply (12.5) with the swapped datum and permutation s^{-1}. For

R_s(lambda)=N(s^{-1},s delta,s lambda): I_{s delta}(s lambda) -> I_delta(lambda)

it gives

J_delta(lambda) R_s(lambda)
 = [n_{s delta}(s lambda)/n_delta(lambda)] J_{s delta}(s lambda).

Only the adjacent pair changes orientation in the product (4.5). Cancelling every other factor yields the candidate's ratio

c(s)=gamma(-s, delta_i'^vee x delta_j' x chi)/gamma(s, delta_i' x delta_j'^vee x chi),

where s=lambda_i-lambda_j and chi=eta^(1+epsilon_i+epsilon_j), up to a nonzero constant. Thus **equal labels mean chi=eta**, and **different labels mean chi=1**. Reversing the ratio or forgetting the extra eta would reverse or destroy the intended necessary condition. Neither error is present in the frozen proof. FLO (13.3), p.293, independently confirms this orientation.

Although both normalizing factors can have poles at zero, the displayed cancellation is an identity of meromorphic functions. Their ratio is examined as that meromorphic quotient. No separate evaluation of two infinite values is used.

## 4. Independent JPSS derivation and all-pair scalar table

JPSS section 8.2, setup p.444 and equation (5) p.445, concerns two essentially square-integrable segment representations, with the larger degree listed first. In the present character-line case their cuspidal degrees are both one. If the segment lengths are m,n and their centers are u,v, its factor shifts are

u-v+(m+n)/2-i, for i=1,...,min(m,n).

Apply this to D[a,b] and D[c,d]^vee=D[-d,-c], putting the longer factor first as necessary. The shifts simplify to b-c-j, for j=0,...,min(m,n)-1. Thus

L(s,D[a,b] x D[c,d]^vee x chi)
 = product_j (1-chi(3) 3^(-s-b+c+j))^(-1).

This agrees with the candidate formula. The proof's use of JPSS is an L-factor computation; no multiplicity theorem is attributed to JPSS.

Let F be the list of forward L(0) exponents b-c-j and R the reverse list d-a-j. The epsilon factor is an analytic unit. For chi=1,

ord_0 gamma_forward = count_F(0)-count_R(-1),
ord_0 gamma_reverse = count_R(0)-count_F(-1).

Positive order denotes a zero, negative order a pole. Replacing s by -s does not change order. The swap coefficient has order ord(gamma_reverse)-ord(gamma_forward).

| Original-order pair | Forward exponents F | Reverse exponents R | Forward gamma order | Reverse gamma order | Coefficient order |
|---|---|---|---:|---:|---:|
| E,D | 4,3,2 | 1,0,-1 | -1 | 1 | 2 |
| E,C | 3 | -1 | -1 | 0 | 1 |
| E,B | 5,4,3 | 0,-1,-2 | -1 | 1 | 2 |
| E,A | 6,5,4 | -2,-3,-4 | 0 | 0 | 0 |
| D,C | 2 | 1 | 0 | 0 | 0 |
| D,B | 4,3,2,1 | 2,1,0,-1 | -1 | 1 | 2 |
| D,A | 5,4,3 | 0,-1,-2 | -1 | 1 | 2 |
| C,B | 2 | 1 | 0 | 0 | 0 |
| C,A | 3 | -1 | -1 | 0 | 1 |
| B,A | 4,3,2 | 1,0,-1 | -1 | 1 | 2 |

For chi=eta every entry in the three order columns is zero: each Tate denominator is 1+3^k at a real integral exponent, hence nonzero. All such gamma values and coefficient values are finite and nonzero.

The merely adjacent pairs E,C and C,A merit separate attention. Their reverse gamma is a **unit**, not a zero, because the reverse L(0) exponent is -1 rather than 0. Their forward gamma still has a simple pole, because the reverse L(1) exponent is zero. Their coefficient has a simple zero. The candidate explicitly distinguishes this case and its conclusion is correct.

The independent checker builds rational functions in t=q^(-s), not only counts of listed exponents. Ignoring the stated epsilon unit, the coefficient is

product_{r in R} [(1-chi q^(-r)/t)(1-chi q^(-1-r)/t)]
 / product_{f in F} [(1-chi q^(-1-f)t)(1-chi q^(-f)t)].

It reduces these exact rational functions and checks their orders at t=1. All ten pairs passed for q=3 and q=9 and chi(uniformizer)=+1,-1. The q=9,+1 rows include the actual E-side scalar checks. The q=9,-1 rows are additional diagnostics, not a new base-change hypothesis.

## 5. The nested normalized operators specialize to isomorphisms

The two nested adjacent pairs in O1 have centers

- D,C: 7/2 > 3;
- C,B: 3 > 5/2.

First untwist to the unitary Steinberg factors, so FLO Lemma 1.1's unitary square-integrable hypothesis is satisfied. Absorb the displayed centers into its twist parameter. The real center differences are positive, so Lemma 1.1(3), p.202, supplies holomorphy of the forward unnormalized M and of the reverse normalized N in a neighborhood of the relevant point.

For each pair, the E-side gamma multiplying forward M has forward L exponents {2}, reverse exponents {1}, with q_E=9. Both its denominator and numerator L-values are finite and nonzero. Forward N is therefore also holomorphic. The reverse normalized operator is holomorphic by the negative-chamber part of the same lemma.

Now the meromorphic inverse identities on p.201 specialize to actual inverse identities at zero. Hence each nested swap gives an isomorphism of the full induced representations. The argument does not infer invertibility merely from irreducibility or merely from the formal generic inverse identity.

On the F side, both possible chi choices likewise give units. Both entire Hom bases are holomorphic at zero by Corollary 13.6. Evaluating the functional equation therefore takes each basis vector to a nonzero scalar times the same segment-labelled vector in the other order. This is a diagonal isomorphism on the entire Hom space; no limiting combination, residue, or new coordinate is introduced.

## 6. Proper rank-one image suffices

Consider any of the five linked adjacencies used in the proof. Its first center exceeds its second center. The table, now with q_E=9 and chi=1, gives a forward gamma pole. FLO Lemma 1.1(4), p.202, applies after the same unitary untwisting. Its reverse normalized N is holomorphic, and its image is the proper irreducible subrepresentation, equivalently the kernel of forward **M**, of the rank-one standard module.

The adjacent operator on the full five-factor induction is obtained by induction in stages from this rank-one operator. Smooth normalized parabolic induction is exact. It also preserves nonzero representations: nonzero inducing data give nonzero induced sections. Therefore induction of this proper rank-one image stays proper, since its induced nonzero quotient remains nonzero.

O1 is a standard module with strictly decreasing real exponents, hence has a unique irreducible quotient and unique maximal proper submodule. O2 and O3 inherit that property through the proved nested isomorphisms. Thus each proper induced rank-one image is contained in the relevant quotient kernel.

This gives every containment used in the proof. It never asserts that these images generate the whole quotient kernel. The general kernel-generation issue is therefore irrelevant to this necessary-direction argument.

## 7. Specialization after a linked swap and arbitrary quotient periods

Fix x and let ell be any invariant functional on the quotient pi. In order O_r, expand its pullback in the complete basis:

ell p_r = sum_epsilon a_{r,epsilon} J_{r,epsilon}(0).

For a linked adjacent pair, the containment above says that composing this fixed functional with R_s(0) gives zero. Extend each basis family meromorphically, keeping the coefficients a_{r,epsilon} constant. One does **not** claim that this combination vanishes away from zero.

The target-order J families are holomorphic at zero, and R_s is holomorphic there. On the domain of R_s, restrict to the fixed open-orbit subspace of the compact induced model. FLO (6.6), p.242, supplies an entire restricted J family and identifies it with the Levi-functional space at zero. FLO (12.1) supplies independence of the 16 restricted lift-labelled functionals for this fixed x, even if the swapped order has other relevant strata.

The coefficient ratios are holomorphic by the table. The restricted meromorphic identity can thus be specialized to zero. Independence yields

a_{r,epsilon} c_{ij,epsilon}(0)=0

for every label. With equal labels, c is a unit; those coefficients must vanish. This uses neither completeness of periods in the linked-swapped order nor holomorphy of all its unrestricted periods. It reproduces the necessary-direction logic of FLO pp.293–294, with the present scalar computations checked separately.

## 8. Transported constraints and conclusion within scope

In O1, E,D and B,A require opposite labels. In O2, E,C and D,B require opposite labels. In O3, C,A requires opposite labels. Since the two nested transports are diagonal units, support of the coefficient vector is unchanged under each comparison to O1.

A surviving coefficient would therefore assign opposite binary labels along

E -- D -- B -- A -- C -- E.

This is impossible: the sum of the five edge equations in characteristic two has left side zero and right side one. Every coefficient of the pullback is zero, hence ell=0. The argument held for arbitrary x throughout, so it applies to each Hermitian orbit.

This conclusion would also contradict the sufficient direction of FLO Conjecture 6.12, p.246: the quotient is tau-invariant with tau-Witt index zero. That consequence was treated as a reason to scrutinize the argument, not as evidence for or against a mathematical step. This audit makes no claim about the current literature status or originality of that consequence.

## Verification records

- `check_scalar_specialization.py`: independently written exact-rational diagnostic; does not import the candidate's checker.
- `SCALAR_SPECIALIZATION_RESULTS.json`: 40 scalar rows, ten distinct pairs, 30 separate order conditions; all PASS.
- Fresh public replay runs the adapted checker in normal Python, -O, and -OO and compares every output byte. Checks use explicit exceptions and remain active under optimization.
- Source text and rendered source pages are excluded from this delivery; only the scholarly citations and permitted inspection metadata are retained.

**Final narrow disposition:** the proposed analytic vanishing argument survives this independent audit. The noninducedness test and overall counterexample acceptance remain outside this report's certification.
