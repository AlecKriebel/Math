# Good-prime Hecke identities on the integral open homology map

Shared PASS 4/5, 14 October 2026. This addendum combines the arithmetic descent theorem in this directory with the regular-at-N geometric Hecke theorem in pass4_five_compatibility/FIVE_HECKE_BY_KERNEL_INCIDENCE.md. The combination is subject to independent acceptance of both inputs. It does not prove compactification or an integral Γ₀ cohomology identity at five.

## 1. Statement

Assume the hypotheses of ARITHMETIC_DESCENT_AND_AUXILIARY_REMOVAL.md: R=Z[1/6], N proper with injective unit reduction, auxiliary c prime to 5N, all CM components retained. Use its declared source-sign Gersten convention and source's adjoint homology Hecke convention from §5.1. Put B=K₂(O'(N))⊗R and C=K₂(F(N))⊗R.

The actual arithmetic cocycles restrict to homomorphisms on Γ₁(N) and give an auxiliary map

Π_{c,N}: H₁(Y₁(N),R) → B.

For every prime ideal q not dividing N, including q above five,

Π_{c,N}∘(T_q−Nq−S_q)=0,                                           (1.1)

and, in the source's component-changing convention,

Π_{c,N}∘S_q=R_N(q)∘Π_{c,N}.                                       (1.2)

The same assertions hold for every unaugmented character component actually constructed by unit cancellation, and for the full R-class under the sufficient conditions of the arithmetic theorem.

The target is still localized at prime-power N. These are maps from the open Bianchi space. No vanishing on its boundary or factorization through X₁(N) is asserted.

## 2. Field-valued arithmetic Hecke at five

The kernel-incidence theorem proves the geometric good-prime identity at q|5 in the coefficient modules regular at the primitive N-orbit. It includes the transfer correction and the moved-primitive comparators. Their generic regularity is sufficient for evaluation in a marked-point field; vertical integrality of the corrections is not needed here.

For any rational p≥5, choose a definition modulus f with [F(Nf):F(N)] prime to p as in the arithmetic proof. Specialize the geometric identity to F(Nf). The exact CM reciprocity convention gives the matrix coefficient action by the Artin symbol of its lower-right entry. Transfer divided by the prime-to-p degree carries the coboundary to a coboundary over F(N). This proves the field-valued cohomological identity on Γ₀(N) for the canonical p-primary arithmetic class, and hence over R.

The component-changing ideal identity [a]*[z_c]=R_N(a)[z_c] is valid in field-valued cohomology also when a meets five, provided (a,N)=1. To see the additional case directly, choose a' in the same ideal class as a avoiding 5Nc. The geometric product norm law for a' is exact, with a normalized comparator between moved primitives regular at the target orbit. The source's scalar-ratio argument of Proposition 4.1.8 then applies to a and a'. Pullback by the a-isogeny preserves regularity at the relevant primitive N-point because (a,N)=1, although it need not preserve T₅-fixedness. Only regularity is used in this field-valued step. Product norms, including those of degree divisible by five, and marked CM reciprocity provide the required comparison. No cocycle for a five-divisible smoothing auxiliary is introduced.

Diamond operators are likewise compatible at the geometric class level: their coordinate maps are degree-one O-linear isomorphisms, so they commute with T₅. Comparing the moved primitive with its deliberately transported primitive gives a normalized correction regular at the N-orbit. This is class transport, not a claim that every mixed coordinate change preserves the original separated primitive literally.

Thus the source's field-valued §4.1 identities, including the full good-prime relation, hold for the canonical family. Away from five the arithmetic proof already supplied the stronger integral Γ₀ cohomological identity.

## 3. Restriction to Γ₁ really is compatible with the good correspondence

The coefficient action on the source Γ₁(N)_r is trivial: its lower-right entry is congruent to a global unit, whose ray Artin symbol is 1. One may equivalently pass to the strict subgroup d≡1 mod N; the central unit quotient has order invertible in R.

For a good prime q, the upper and lower root ideals of Γ₁(N)_r reduce surjectively modulo q. For the lower roots this uses (q,N)=1. The corresponding unipotents have determinant one and d=1 modulo N, so their reductions generate SL₂(O/q). Consequently Γ₁ acts transitively on the q+1 lines in the rank-two q-torsion module, just as Γ₀ does.

Let H be the Γ₀ stabilizer of the kernel line of the standard q-isogeny. The two indices [Γ₀:H] and [Γ₁:Γ₁∩H] are both Nq+1; hence Γ₀=Γ₁H. The isogeny intertwines the respective strict level conditions because its determinant is prime to N. Thus the same coset representatives may be chosen for the Γ₀ and Γ₁ correspondences, and the restriction/corestriction formula has no extra index or averaging factor. This verifies the good-prime restriction diagram, rather than assuming it from an equality of eigenvalues.

The central/component-changing and diamond correspondences restrict with their source conventions as well: they preserve the relevant Γ₁ congruence condition. The entire h² system is kept until the source's h Bianchi components are selected.

## 4. A field coboundary vanishes on this subgroup

For a trivial Γ₁-action on C,

H¹(Γ₁,C)=Hom(Γ₁^ab,C),

and every one-coboundary is the zero function. Therefore the field-valued Hecke identities of Section 2, after the compatible restriction of Section 3, are identities of the actual homomorphisms on Γ₁. They do not retain an unidentified field-valued coboundary.

Localization in algebraic K-theory gives an injection

K₂(O'(N)) → K₂(F(N)),

because the preceding terms K₂ of the finite residue fields are zero. Tensoring with the flat ring R preserves injectivity. Every value of the actual arithmetic homomorphism is in B by the proved arithmetic descent/integrality theorem, and every coefficient automorphism R_N(a) preserves B. Thus both sides of each homomorphism identity lie in B. Their equality in C implies their equality in B.

This is coefficient injection in degree zero and the vanishing of coboundaries for a trivial action. It is not a general assertion that H¹(Γ₀,B) injects into H¹(Γ₀,C). In particular it does not claim that the transfer correction in the geometric five-Hecke proof is vertically integral or T₅-fixed.

## 5. The coarse open Bianchi space needs only six inverted

The contract's accepted finite-stabilizer result already supplies the comparison. A short direct check is included to make the coefficient scope explicit.

If a finite subgroup of GL₂(F) had order divisible by a rational prime l≥5, it would contain an element of order l. At least one eigenvalue would be a primitive l-th root, with minimal polynomial over F of degree at most two. For l≥7, [F(ζ_l):F]≥(l−1)/2≥3, impossible. For l=5 the only possible quadratic subfield of Q(ζ₅) is Q(√5), which cannot be the imaginary quadratic F; the degree is therefore four, again impossible. Hence all prime divisors of finite isotropy orders are 2 or 3.

Finite isotropy is R-acyclic. The equivariant-to-coarse spectral sequence therefore identifies the relevant Γ₁ cohomology with the cohomology of its hyperbolic quotient, compatibly with finite Hecke correspondences. With constant coefficients the degree-one universal-coefficient identification is Hom(H₁(−,R),B). This gives the asserted map from the open Bianchi homology with no inversion of five.

Finally apply the algebraic adjoint-pairing calculation of source Lemma 5.1.1 and Propositions 5.1.2–5.1.3. Their group/coset formulas require no division by five; the only coarse-space coefficient issue was checked above. The source conventions give exactly (1.1)–(1.2), including the Artin sign and component changes. They are not the oppositely normalized bad-U formulas from earlier restricted bad-prime work.

## 6. Scope after combination

Accepted unit cancellation commutes with the coefficient Artin operators, so (1.1)–(1.2) also hold on every unaugmented block actually constructed. On an exceptional block where cancellation has not been proved, this addendum supplies only the auxiliary map.

Still unresolved are small non-unit-injective levels, the exceptional five-block obstruction, other surviving exceptional blocks, integer-ring absolute values at prime-power level, compactification, unrestricted bad-prime U relations, and the relative theta-symbol calibration. No boundary identity follows by setting q|N in the good-prime argument.

Primary source for conventions: Lecouturier–Sharifi–Shih–Wang, *Eisenstein cocycles for imaginary quadratic fields*, §§4.1 and 5.1, https://www.math.ucla.edu/~sharifi/publ/imagquad.pdf .
