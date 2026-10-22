# Ramified five: actual removal with no tame five-inertia

Authored proof, 14 October 2026. Shared final PASS 5/5, row 1777 / 30005572. This is a restricted theorem about the actual accepted auxiliary family. It is not the full construction contract and makes no novelty claim.

## 1. Statement

Let F be imaginary quadratic, let five ramify in F, and let N be a nonzero proper ideal with injective unit reduction. Put L=F(N), Q=Gal(L/F), R=Z[1/6], and

B_N=K2(O'(N)) tensor Z5,

where O'(N)=O_L[1/N] for a prime-power ideal N and O_L otherwise. Assume

**5 does not divide h_F, and Nq is not 1 modulo five for every prime q|N away from five.**

There is no bound on the exponent of the ramified prime above five in N. In particular the full ray degree may be divisible by an arbitrarily large power of five.

Write Q=P x Q' with P=Q5. Let chi:Q -> {+1,-1} be the character of the unramified quadratic extension F(sqrt(5))/F. Its reduction is the squared mod-five cyclotomic character on G_F.

**Theorem.** B_N^(chi)=0. Consequently the actual normalized auxiliary arithmetic cocycles of accepted PASS 4 have zero chi-component, and the unique unaugmented chi-class is zero. Every other five-adic block has a unit smoothing factor by accepted PASS 4. Thus the full five-primary auxiliary family admits a unique unaugmented arithmetic class, on every source component, with no five inverted.

The zero exceptional class here is a conclusion about the actual coefficient module and hence about every value of the actual auxiliary family. It is not an arbitrary zero replacement for a surviving construction. Nonexceptional blocks are still the genuine unit-divided auxiliary classes.

Combining with the accepted p>=7 source removal theorem gives a full unaugmented R-class if, in addition, no p>=7 has both (p)|N^2 and p|h_F. Its actual open homology map has every good-prime Hecke identity by PASS 4, including primes above five when they are good. Compactification, relative calibration, unrestricted bad-prime identities, and integer-ring values at prime-power N are not asserted.

## 2. Ray degrees, and why the hypothesis is not just a class-number condition

Let U_N be the units congruent to one modulo N. The exact ray class sequence gives

|Q| = h_F |(O_F/N)^x| / [O_F^x:U_N].

The denominator has order at most two when five ramifies. In particular the simpler hypothesis 5 not dividing |Q| implies our two assumptions, but also limits the five-adic level depth. We do not impose that extra limitation.

The theorem excludes any prime of tame residue norm 1 modulo five. Such a prime can supply five-primary ray inertia and the additional mod-five cohomology which the proof below needs to vanish. For the accepted example F=Q(sqrt(-5)), N=(11), the prime (11) has norm 121, the ray degree is 120, and the exceptional localized residue module is nonzero. Merely knowing 5 does not divide h_F=2 would not suffice.

Our actual hypothesis permits arbitrary wild ray inertia at the unique prime above five; Section 4 treats it by top-degree corestriction, not by dividing its order.

## 3. A mod-five cohomology calculation over F

Let S consist of the prime above five, all primes dividing N, and the archimedean places; the latter are omitted when writing S-integer rings. Write G_{F,S} for the Galois group of the maximal extension of F unramified outside S. All archimedean places are complex.

Global class field theory identifies the maximal abelian pro-five quotient through the exact inertia/class-group sequence. Since the five-part of Cl(F) is zero, its abelian pro-five quotient is obtained from the pro-five parts of the local unit groups at S, divided by the closure of global units. The global units have no five-part. At q in S away from five, the local unit group has no pro-five part: its principal units are pro-l for l !=5, and its residue field unit group has order Nq-1, prime to five.

At the unique place v over five, F_v/Q5 is quadratic. It cannot contain mu5, since [Q5(mu5):Q5]=4. The pro-five part of O_{F_v}^x is therefore a torsion-free Z5-module of rank [F_v:Q5]=2. It follows that

G_{F,S}^{ab}(5) is isomorphic to Z5^2,

and hence dim_F5 H^1(G_{F,S},F5)=2. This calculation uses the actual local unit groups; no assertion about a class group of L is made.

Milne, *Arithmetic Duality Theorems*, second edition, I Section 5, Theorem 5.1 (printed p.67), gives the global Euler-Poincare characteristic. For an odd prime, S containing the primes above that prime, and our totally imaginary number field, it reads

sum_{j=0}^2 (-1)^j dim_F5 H^j(G_{F,S},F5) = -r2(F) = -1.

The five-cohomological dimension is at most two. Since H^0 has dimension one and H^1 has dimension two, we get

H^2(G_{F,S},F5)=0.                                           (3.1)

Equivalently this is H^2_et(O_F[1/S],F5)=0, using the standard Galois/etale comparison for this S-integer ring. These are ordinary cohomology groups with the trivial mod-five coefficient module, not compactly supported groups and not groups with the Tate twist still present.

## 4. The precise twist and descent, including wild five-extensions

Put L0=L^P. All the covers of S-integer rings associated with L/L0/F are finite etale: every finite ramification prime was removed. Moreover L0 contains F(sqrt(5)), since this quadratic extension has degree prime to five. Consequently mu5^tensor2 is trivial as a G_{L0,S}-module, and its descent character over F is chi.

We first justify the needed top-degree co-descent integrally modulo five. Let G=G_{L0,S}, H=G_{L,S_L}, with finite quotient P. The five-cohomological dimension of G is at most two. The functor H^2(G,-) is therefore right exact on discrete five-primary modules: to apply it to a presentation, factor the presentation through its image and use the long exact sequence twice.

Let A0=F5[P], inflated to G with the left regular action. Choose generators g_j of P. The right-multiplication maps by g_j-1 give a finite G-module presentation

sum_j A0 -> A0 -> F5 -> 0.

Shapiro identifies H^2(G,A0) with H^2(H,F5), and its right regular action is the deck action, up to the harmless inverse convention for coinvariants. Right exactness now proves

H^2(G_{L,S_L},F5)_P is isomorphic to H^2(G_{L0,S},F5).        (4.1)

The map is corestriction. It is Q'-equivariant by the naturality of transfer and of the augmentation presentation. No norm degree divisible by five has been cancelled.

The prime-to-five quotient Q' can be averaged. After the chi twist this gives

( e_chi H^2_et(O_L[1/S_L],mu5^tensor2) )_P
  is isomorphic to H^2_et(O_F[1/S],F5)=0.                    (4.2)

More explicitly, mu5^tensor2 is trivial over L0, and its Q' descent action is chi. Thus taking the chi-part of its cohomology is taking the invariant part of untwisted F5 cohomology. Hochschild-Serre for L0/F has no positive-degree Q' terms, because |Q'| is invertible in F5. This explains every twist in (4.2).

The left coefficient group before P-coinvariants is a finite-dimensional F5[P]-module. This is a local ring with nilpotent augmentation ideal. Nakayama and (4.2) prove

e_chi H^2_et(O_L[1/S_L],mu5^tensor2)=0.                       (4.3)

Tate's odd-prime K2/etale comparison for S-integers identifies

K2(O_L[1/S_L]) tensor Z5 with H^2_et(O_L[1/S_L],Z5(2)).

The coefficient exact sequence gives an injection from H^2_et(Z5(2))/5 into H^2_et(mu5^tensor2). Projecting by e_chi is exact because |Q'| is prime to five. Equation (4.3) therefore makes the chi-part of K2(O_L[1/S_L]) tensor Z5 have zero quotient by five. This is a finite five-group, so it is zero.

Finally localization gives an injection

K2(O'(N)) -> K2(O_L[1/S_L]),

because K2 of every intervening finite residue field is zero. Tensoring with Z5 is flat, and the chi-projection is exact. The subgroup B_N^(chi) is therefore zero, proving the theorem. We have not assumed that coinvariants preserve injections: the full mod-five cohomology module was first shown zero, before the comparison injection was used.

## 5. Application to the actual auxiliary system

Let a_c be the accepted class [z_{c,i,N}]^(chi) in H^1(Gamma0(N)_i,B_N^(chi)), for c prime to 5N. Since its coefficient module is zero, a_c=0 for every c. Its unique unaugmented class in that same group is zero. This directly verifies every smoothing equation s_c u=a_c and leaves no ambiguity, because the entire target cohomology group in this block is zero.

For the other five-adic blocks the accepted unit-smoothing theorem supplies a unique class. There are finitely many such blocks. Summing them gives the full five-primary class without an exceptional summand omitted by fiat. The source's h^2 CM product system, followed by its h Bianchi components, is retained.

The good-prime identities for the open homology maps follow from the accepted actual-map identities, since all valid unit divisions commute with the coefficient Artin action. The exceptional contribution is actually zero. The conclusion does not obtain the remaining full-contract conditions by averaging.

Examples inside the new restricted theorem include F=Q(sqrt(-5)), N=(3), with ray degree 4, and N=(13), with ray degree 168. Both are unit-injective. The former is not a prime-power ideal, whereas (13) is inert and is a prime ideal; the localized target in the latter case is explicitly covered. In contrast N=(11) has degree 120 and remains outside this theorem.

## 6. Sources, exact dependencies, and scope

Accepted mathematical inputs: PASS 4 ARITHMETIC_DESCENT_AND_AUXILIARY_REMOVAL.md and its independent acceptance; FIVE_PRIMARY_EXCEPTION_CHECK.md; OPEN_HOMOLOGY_GOOD_HECKE.md. Their files are not edited here.

The auxiliary construction and the p>=7 removal theorem are from E. Lecouturier, R. Sharifi, S.-C. Shih, J. Wang, *Eisenstein cocycles for imaginary quadratic fields*, Sections 4.1-4.3 and 5.1, https://www.math.ucla.edu/~sharifi/publ/imagquad.pdf . The source's p>=7 exclusion or localized h-only argument is not imported at five.

For the actual Euler characteristic used in Section 3 see J. S. Milne, *Arithmetic Duality Theorems*, second edition, I Section 5, Theorem 5.1, https://www.jmilne.org/math/Books/ADTnot.pdf . With F imaginary quadratic and trivial F5 coefficients, its multiplicative characteristic is 5/25=1/5.

Classical inputs are global class field theory's local-unit/ray-class exact sequence, the global Euler-Poincare formula and cd_p<=2 for S containing the places above p, Hochschild-Serre for a finite etale cover of degree prime to p, and Tate's odd-prime comparison for K2 of S-integers. For the last comparison see J. Tate, *Relations between K2 and Galois cohomology*, Invent. Math. 36 (1976), 257-274, Theorem 5.4, DOI https://doi.org/10.1007/BF01390012 . These inputs concern p=5 without the construction-specific p>=7 restriction.

The surviving cases with tame five-inertia or five-divisible class number, including -5/(11), are not resolved by this theorem. No actual nonzero obstruction in their auxiliary class systems has been computed.
