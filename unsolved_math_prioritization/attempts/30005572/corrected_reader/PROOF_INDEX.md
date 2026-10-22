# Complete proofs and dependency guide

The full arguments below are the accepted authored proof texts, not theorem-only summaries. Their exact hypotheses remain in force. Proofs are numbered by stable document ID rather than by the order suggested for reading. [READER.md](READER.md) supplies the current overview; [CORRECTIONS.md](CORRECTIONS.md) explains historical repairs.

“Acceptance” means separate internal AI mathematical review, not journal peer review or independent human validation. Every original hash below was verified in its named acceptance report. Where a neutral editorial derivative differs, the original and public hashes are distinct and recorded separately in PRESERVATION_INVENTORY.json. Old proof statements about then-open work are historical; later results supersede them only in the narrower ranges explicitly stated.

## Qualifications that travel with the proofs

[L1](qualifications/L1_MODEL_TRANSPORT_SCOPE_CLARIFICATION.md) gives the product-coordinate, transported-shear and regular-coboundary scope of model transport. [L2](qualifications/L2_GERSTEN_SIGN_TRANSPORT_ADDENDUM.md) gives the degree-two minus sign between the standard and reciprocal source complexes. Neither is a cosmetic redaction.

## Foundations and the relative extension criterion

### P01 Constant 5-torsion obstruction to the unmodified trace-fixed complex

[Complete proof](proofs/P01_CONSTANT_FIVE_TORSION_OBSTRUCTION.md)

Nonzero constant 5-torsion obstructs the unmodified full-CM trace-fixed complex; for maximal imaginary-quadratic CM its left kernel is C[5] when five ramifies and zero otherwise. This does not contradict the source Z[1/30] theorem or disprove the original map.

Authored dependencies: Standard and cited source inputs only..
Internal review: [A1](reviews/A1_INDEPENDENT_ACCEPTANCE.md).
Public source IDs: S02, S04, S05, S06, S07, S08, S09.
Original SHA-256: `3538c215bb6295659adfb5c3e902e6cca036f1a416e8665ee6273c5c68d228ca`.
Public proof bytes are identical to the pinned original.

### P02 Integral constant-quotient repair for a product of two elliptic curves

[Complete proof](proofs/P02_CONSTANT_QUOTIENT_REPAIR.md)

Integral product-of-elliptic-curves projectors give constant-quotient left exactness over R; the unquotiented left end is repaired when five is unramified. Its conditional residue and ordinary-lift hypotheses are discharged for the auxiliary family by later accepted P07/P09; no universal-family theorem is claimed.

Authored dependencies: [P01](proofs/P01_CONSTANT_FIVE_TORSION_OBSTRUCTION.md).
Internal review: [A1](reviews/A1_INDEPENDENT_ACCEPTANCE.md).
Public source IDs: S02, S04, S10, S11.
Original SHA-256: `6943210fbd4d1761d2317e0715491e00688a7a803197d60c6c9c49561f92f9c0`.
Public proof bytes are identical to the pinned original.

### P03 Relative CM theta symbols: exact defects and the remaining integral lemma

[Complete proof](proofs/P03_RELATIVE_SYMBOL_DERIVATION.md)

Generic auxiliary-theta triangle defect; exact three-term smoothing; root-ambiguity calculation; abstract relative extension and saturated unweighted-edge criterion. No specialized counterexample or full integral relative map.

Authored dependencies: Standard and cited source inputs only..
Internal review: [A2](reviews/A2_AUDIT_REPORT.md).
Public source IDs: S01, S02, S03, S04, S12, S13.
Original SHA-256: `06b0ae85504cae2bf55c5ffcd892cdb0db66b5641e1382dcac2b5edac99cb1c7`.
Public derivative SHA-256: `e34bf065f9358a34b1c99e840d161bc01d3f7a87c5679c6773249a818f9a8431`; only the recorded neutral editorial change differs.

### P04 A local boundary calculation at arbitrary depth

[Complete proof](proofs/P04_LOCAL_BAD_LEVEL_LEMMA.md)

Both opposite bad-level operators are nilpotent on the supported oldvector chain of doubly ramified local principal series, with explicit unnormalized conventions. Neither operator is thereby identified with an arithmetic U* theorem.

Authored dependencies: Standard and cited source inputs only..
Internal review: [A2](reviews/A2_AUDIT_REPORT.md).
Public source IDs: S02, S03.
Original SHA-256: `6d2edef937610dd887cf8185c798e86f010c786d31f5fa5b68c0cb69a0726509`.
Public proof bytes are identical to the pinned original.

### P05 PASS1 result: boundary-depth mechanism and the remaining K₂ identity

[Complete proof](proofs/P05_BOUNDARY_REPORT.md)

Arbitrary-depth ordinary boundary localization vanishes for p>=7 under the existing residual-character exclusions. Application to the actual K2 map requires its U*=1 relation in the relevant range; P13/P15 supply only restricted ranges.

Authored dependencies: [P04](proofs/P04_LOCAL_BAD_LEVEL_LEMMA.md).
Internal review: [A2](reviews/A2_AUDIT_REPORT.md).
Public source IDs: S02, S03.
Original SHA-256: `613dce536eca6a92c7ec316b97750857e2e44a47ea3839a1f94ae928452db678`.
Public proof bytes are identical to the pinned original.

### P06 Stabilizers and the exact compactification obstruction

[Complete proof](proofs/P06_STABILIZERS_AND_OBSTRUCTION.md)

Finite Bianchi stabilizers have only prime factors 2 and 3; group/coarse comparison requires 6 invertible. Exact boundary-image annihilation characterizes compactification. The topological quotient criterion itself is coefficient-independent.

Authored dependencies: Standard and cited source inputs only..
Internal review: [A2](reviews/A2_AUDIT_REPORT.md).
Public source IDs: S02, S03.
Original SHA-256: `55300f71adeef0e0d8e8dea4a578122c9f49116cf1a6b9119fb028e06da04055`.
Public proof bytes are identical to the pinned original.

## Residue primitives and canonical geometric normalization

### P07 Trace-fixed residue primitives over Z[1/6]

[Complete proof](proofs/P07_RIGHT_END_LIFTING.md)

Degree-zero full-CM residue lifting and exact one-curve normalization over R for every source h^2 product; same-type maximal-CM twists require only a degree dividing 2,4,6. Includes explicit auxiliary primitives and distribution formulas; no arithmetic descent.

Authored dependencies: [P02](proofs/P02_CONSTANT_QUOTIENT_REPAIR.md).
Internal review: [A3](reviews/A3_RESIDUE_AND_GEOMETRY_ACCEPTANCE.md), [A4](reviews/A4_RAMIFIED_FIVE_ACCEPTANCE.md).
Public source IDs: S02, S04.
Original SHA-256: `ee853634d28da3c9d324f25cc90a7a9d9aed95875bc385782746aad73cf720f4`.
Public proof bytes are identical to the pinned original.

### P08 Geometric consequences of the R-valued residue primitives

[Complete proof](proofs/P08_GEOMETRIC_COCYCLES.md)

Genuine trace-fixed geometric classes when five is unramified and constants-quotient classes in all fields, with the stated geometric norm/pullback/Hecke and regularity properties. Historical ramified-five cautions must be read together with P09/P14.

Authored dependencies: [P01](proofs/P01_CONSTANT_FIVE_TORSION_OBSTRUCTION.md), [P02](proofs/P02_CONSTANT_QUOTIENT_REPAIR.md), [P07](proofs/P07_RIGHT_END_LIFTING.md).
Internal review: [A3](reviews/A3_RESIDUE_AND_GEOMETRY_ACCEPTANCE.md).
Public source IDs: S02.
Original SHA-256: `d654d5ebe0ffe14d5fc8b229b72c6ad9de82f299271dafd9c072e0e8bd2ecaa9`.
Public proof bytes are identical to the pinned original.

### P09 Ramified-five lifting: the ordinary obstruction vanishes

[Complete proof](proofs/P09_ORDINARY_LIFT_AND_REMAINING_TRACE_OBSTRUCTION.md)

Ordinary H2 constant-valued cocycle obstruction vanishes for actual auxiliary cycles on all source components, using coprime annihilators and integral Bezout. This proof alone has no canonical trace/isogeny normalization; P14 now supplies a restricted T5 normalization.

Authored dependencies: [P01](proofs/P01_CONSTANT_FIVE_TORSION_OBSTRUCTION.md), [P02](proofs/P02_CONSTANT_QUOTIENT_REPAIR.md), [P07](proofs/P07_RIGHT_END_LIFTING.md).
Internal review: [A4](reviews/A4_RAMIFIED_FIVE_ACCEPTANCE.md).
Public source IDs: S02, S05, S14, S15.
Original SHA-256: `8c3a64691290a558216e812aabf770e7e019ed55d13baa1c30ea3da56198b634`.
Public derivative SHA-256: `175a2d4d8fa9c17244b412cd1e556bc0359be61fb97b683680f9c0919f269e3d`; only the recorded neutral editorial change differs.

### P10 An explicit two-stage test for the remaining trace representative

[Complete proof](proofs/P10_TRACE_REPRESENTATIVE_TEST.md)

Exact two-stage fixed-monoid criterion: a C/5C divisibility obstruction followed by a C[5]-valued trace character. The criterion remains valid; P14 evaluates both to zero on actual T5-fixed auxiliary values with c prime to five.

Authored dependencies: [P01](proofs/P01_CONSTANT_FIVE_TORSION_OBSTRUCTION.md), [P09](proofs/P09_ORDINARY_LIFT_AND_REMAINING_TRACE_OBSTRUCTION.md).
Internal review: [A4](reviews/A4_RAMIFIED_FIVE_ACCEPTANCE.md).
Public source IDs: Inherited through the authored dependencies.
Original SHA-256: `c5e289aec74fa62d1406fd65dd1d8322f6b9d6907af50a66db400a24ed748347`.
Public proof bytes are identical to the pinned original.

### P11 Direct finite-orbit normalization of the ordinary cocycle

[Complete proof](proofs/P11_FINITE_ORBIT_NORMALIZATION.md)

Canonical D-fold ordinary cocycle for fixed residue primitive and finite orbit scheme, independent of representatives/local primitives. Bezout yields an ordinary lift; unmultiplied canonical trace normalization is supplied only in the later scope of P14.

Authored dependencies: [P02](proofs/P02_CONSTANT_QUOTIENT_REPAIR.md), [P07](proofs/P07_RIGHT_END_LIFTING.md), [P09](proofs/P09_ORDINARY_LIFT_AND_REMAINING_TRACE_OBSTRUCTION.md).
Internal review: [A5](reviews/A5_FINITE_ORBIT_ACCEPTANCE.md).
Public source IDs: S14, S15.
Original SHA-256: `a241d925353cbaa16f5bde46e75fb940d1a7cf8ab35eeed39f36ad308fc17e28`.
Public proof bytes are identical to the pinned original.

### P14 Exact scalar-five normalization of the genuine auxiliary cocycles

[Complete proof](proofs/P14_SCALAR_FIVE_NORMALIZATION.md)

For c prime to five, P=125B+T5-625 uniquely lifts the actual quotient cocycle to an eventual-trace-fixed and literally T5-fixed genuine R-valued geometric cocycle. Prime-to-c product norms allow five-divisible degree. Literal product-model transport has the L1 qualification; independent mixed primitives compare by regular coboundaries. P14 itself proves pullback/class/Hecke compatibility away from five; P19/P22 separately close geometric/all-good open-map Hecke, without making arbitrary pullbacks T5-preserving. Source comparison is subject to L2.

Authored dependencies: [P01](proofs/P01_CONSTANT_FIVE_TORSION_OBSTRUCTION.md), [P02](proofs/P02_CONSTANT_QUOTIENT_REPAIR.md), [P07](proofs/P07_RIGHT_END_LIFTING.md), [P08](proofs/P08_GEOMETRIC_COCYCLES.md), [P09](proofs/P09_ORDINARY_LIFT_AND_REMAINING_TRACE_OBSTRUCTION.md), [P10](proofs/P10_TRACE_REPRESENTATIVE_TEST.md), [P11](proofs/P11_FINITE_ORBIT_NORMALIZATION.md).
Internal review: [A8](reviews/A8_TRACE_NORMALIZATION_ACCEPTANCE.md).
Public source IDs: S02.
Original SHA-256: `0fd5b52591d193b1949afbe17b022414610101b7fbb8fca2eb3ee65f215f66ca`.
Public proof bytes are identical to the pinned original.

### P19 Hecke compatibility at five from exact norms and kernel incidence

[Complete proof](proofs/P19_FIVE_HECKE_BY_KERNEL_INCIDENCE.md)

For auxiliaries c prime to five, integral kernel-incidence and transfer-with-coboundary prove all-prime geometric Hecke compatibility, including primes above five. Regular-at-N refinement requires the new prime be prime to cN. No blanket T5-preserving pullback claim: the non-Cartesian defect is retained explicitly. This is a geometric theorem; arithmetic/open-map consequences are separately P20/P22.

Authored dependencies: [P02](proofs/P02_CONSTANT_QUOTIENT_REPAIR.md), [P07](proofs/P07_RIGHT_END_LIFTING.md), [P14](proofs/P14_SCALAR_FIVE_NORMALIZATION.md).
Internal review: [A12](reviews/A12_FIVE_COMPATIBILITY_ACCEPTANCE.md).
Public source IDs: S02.
Original SHA-256: `fac5809de5e1906e52fe5518f28b6373ed229f30133c0f1bf9eae938b62f9e62`.
Public proof bytes are identical to the pinned original.

## Arithmetic descent and exact auxiliary removal

### P20 Arithmetic descent of the scalar-five normalized family

[Complete proof](proofs/P20_ARITHMETIC_DESCENT_AND_AUXILIARY_REMOVAL.md)

For proper unit-injective N and c prime to 5N, the normalized family descends on all h^2 CM products to K2(O-prime(N)) tensor Z[1/6], retaining five-primary values and integral auxiliary exchange. Nonexceptional full-ray blocks admit unit cancellation, with the exact squared-cyclotomic exception at five. Main proof gives arithmetic Hecke away from 5N; P22 supplies all good primes on the open homology map. Source comparison explicitly uses reciprocal-sign transport.

Authored dependencies: [P01](proofs/P01_CONSTANT_FIVE_TORSION_OBSTRUCTION.md), [P02](proofs/P02_CONSTANT_QUOTIENT_REPAIR.md), [P07](proofs/P07_RIGHT_END_LIFTING.md), [P08](proofs/P08_GEOMETRIC_COCYCLES.md), [P14](proofs/P14_SCALAR_FIVE_NORMALIZATION.md).
Internal review: [A13](reviews/A13_ARITHMETIC_DESCENT_ACCEPTANCE.md).
Public source IDs: S02, S04.
Original SHA-256: `33b7d83c2e34a131d7a222c054f5842535e8338b4bc940af9156e106de1aef1f`.
Public proof bytes are identical to the pinned original.

### P21 The five-exception is not controlled by the printed p≥7 criterion

[Complete proof](proofs/P21_FIVE_PRIMARY_EXCEPTION_CHECK.md)

For Q(sqrt(-5)), F(sqrt5)/F is the unramified exceptional quadratic extension even at level (3); at inert level (11), the localized exceptional coefficient module has nonzero five-primary support although 5 does not divide h=2. This is ambient support, not a nonzero actual cocycle or a proof that removal fails.

Authored dependencies: [P12](proofs/P12_ABSOLUTE_INTEGRALITY_AND_RESIDUES.md), [P20](proofs/P20_ARITHMETIC_DESCENT_AND_AUXILIARY_REMOVAL.md).
Internal review: [A13](reviews/A13_ARITHMETIC_DESCENT_ACCEPTANCE.md).
Public source IDs: S02.
Original SHA-256: `854c43a1253a4d54bfa24814db4404de3c105f75f09142afaf3fd1ef3243c412`.
Public proof bytes are identical to the pinned original.

### P22 Good-prime Hecke identities on the integral open homology map

[Complete proof](proofs/P22_OPEN_HOMOLOGY_GOOD_HECKE.md)

For proper unit-injective N and c prime to 5N, the actual auxiliary map on H1(Y1(N),R), all h Bianchi components, takes values in K2(O-prime(N)) tensor R and has T_q-Nq-S_q=0 and S_q=R_N(q) for every q not dividing N, including five. Inherits valid cancellation blocks. Does not claim compactification, integer-ring target at prime-power N, bad-U or a stronger integral Gamma0-cohomology identity at five.

Authored dependencies: [P06](proofs/P06_STABILIZERS_AND_OBSTRUCTION.md), [P14](proofs/P14_SCALAR_FIVE_NORMALIZATION.md), [P19](proofs/P19_FIVE_HECKE_BY_KERNEL_INCIDENCE.md), [P20](proofs/P20_ARITHMETIC_DESCENT_AND_AUXILIARY_REMOVAL.md), [P21](proofs/P21_FIVE_PRIMARY_EXCEPTION_CHECK.md).
Internal review: [A14](reviews/A14_OPEN_HOMOLOGY_ACCEPTANCE.md).
Public source IDs: S02.
Original SHA-256: `6a7d1119621077d1c7df59fb77c18cae793244cd2ed857a6f82c30af5a3ff271`.
Public proof bytes are identical to the pinned original.

### P31 Exact ramified-five smoothing depth and the actual remaining obstruction

[Complete proof](proofs/P31_EXACT_FIVE_SMOOTHING_OBSTRUCTION.md)

For ramified five and proper unit-injective level, the exceptional smoothing quotient Z5[P]/J is Z/5^a with a=max(1,ceil(v_p(N)/2)) and its retained cyclotomic P-action. The actual existence obstruction is killed by 5^a, with an exact two-stage test and ambiguity. No surviving actual nonzero obstruction is exhibited; a five-divisible auxiliary is not constructed.

Authored dependencies: [P14](proofs/P14_SCALAR_FIVE_NORMALIZATION.md), [P20](proofs/P20_ARITHMETIC_DESCENT_AND_AUXILIARY_REMOVAL.md), [P21](proofs/P21_FIVE_PRIMARY_EXCEPTION_CHECK.md), [L2](qualifications/L2_GERSTEN_SIGN_TRANSPORT_ADDENDUM.md).
Internal review: [A19](reviews/A19_EXCEPTIONAL_SMOOTHING_ACCEPTANCE.md).
Public source IDs: S02.
Original SHA-256: `9be734e6e41a6f10e2a915068248d3584a69798853b5627711f6d35dac191a2f`.
Public proof bytes are identical to the pinned original.

### P32 Ramified five: actual removal with no tame five-inertia

[Complete proof](proofs/P32_RAMIFIED_FIVE_TAME_RAY_REMOVAL.md)

Actual exceptional five-primary coefficient module vanishes when five ramifies, 5 does not divide h_F, the level is proper and unit-injective, and every level prime away from five has norm not 1 mod5. Arbitrary depth above five is allowed. Hence genuine full five-primary auxiliary removal holds; full R-removal also needs the stated p>=7 hypothesis. No unrestricted compactification, bad-U, or prime-power integer-ring improvement.

Authored dependencies: [P20](proofs/P20_ARITHMETIC_DESCENT_AND_AUXILIARY_REMOVAL.md), [P21](proofs/P21_FIVE_PRIMARY_EXCEPTION_CHECK.md), [P22](proofs/P22_OPEN_HOMOLOGY_GOOD_HECKE.md), [L2](qualifications/L2_GERSTEN_SIGN_TRANSPORT_ADDENDUM.md).
Internal review: [A19](reviews/A19_EXCEPTIONAL_SMOOTHING_ACCEPTANCE.md).
Public source IDs: S02, S16, S23, S24, S25.
Original SHA-256: `58723b67e6e23fe0f1ff0fff466f40eb3d713285931cc0c4b6b1e2176e890219`.
Public proof bytes are identical to the pinned original.

## Bad-prime correspondences on all ideal classes

### P13 A bad-prime norm identity and a restricted arithmetic U* theorem

[Complete proof](proofs/P13_BAD_PRIME_NORM_AND_RESTRICTED_IDENTITY.md)

Actual auxiliary bad-U defect has norm zero for p>=7, principal q, N=Mq^n, proper admissible q-free M; actual U*=1 on inflated characters when the relative degree is a p-adic unit, and legitimate auxiliary cancellation where available. P15 removes only lower-level admissibility.

Authored dependencies: Standard and cited source inputs only..
Internal review: [A7](reviews/A7_BAD_PRIME_ACCEPTANCE.md).
Public source IDs: S02, S03, S17.
Original SHA-256: `7af38b596ee39ad4447a63eac17ea4c28e0c07177021e4f15277c2b2d5e29e5a`.
Public proof bytes are identical to the pinned original.

### P15 Removing lower-level unit-injectivity from the actual bad-U theorem

[Complete proof](proofs/P15_SMALL_LOWER_LEVEL_BAD_U.md)

Extends P13 to proper nonadmissible lower M with admissible high N. Exact transfer correction |U_M| divides six. Principal q, p>=7, norm-kernel/character limits and proper M remain; no pure-prime-power, nonprincipal, high-small-level or five-primary theorem.

Authored dependencies: [P13](proofs/P13_BAD_PRIME_NORM_AND_RESTRICTED_IDENTITY.md).
Internal review: [A9](reviews/A9_BAD_PRIME_EXTENSION_ACCEPTANCE.md).
Public source IDs: S02, S03.
Original SHA-256: `88f9e52d3119a446038789c8352d801e2387d78dd8611ea2a2f326fbe72b5d53`.
Public proof bytes are identical to the pinned original.

### P25 Nonprincipal CM assembly for the dual bad-U norm relation

[Complete proof](proofs/P25_NONPRINCIPAL_DUAL_BAD_U.md)

Corrected frozen theorem covers the inverse-correspondence bad-U norm theorem for arbitrary prime ideals on all standard components, still p>=7, proper lower M, admissible high N and restricted norm-injective blocks. The corrected three-file package is formally accepted by the included internal review A16 at exactly this restricted scope.

Authored dependencies: [P13](proofs/P13_BAD_PRIME_NORM_AND_RESTRICTED_IDENTITY.md), [P15](proofs/P15_SMALL_LOWER_LEVEL_BAD_U.md).
Internal review: [A16](reviews/A16_NONPRINCIPAL_BAD_U_ACCEPTANCE.md).
Public source IDs: S02, S03.
Original SHA-256: `89757a18ca035d1f72cdf2ae6c63b6f987d01c3468eee3b766d38c5f2071a6fa`.
Public proof bytes are identical to the pinned original.

### P26 Convention checks and recovery of the accepted principal formula

[Complete proof](proofs/P26_CONVENTION_AND_PRINCIPAL_RECOVERY.md)

Convention supplement: retains the local central idele and recovers the accepted principal formula under the marking change. Formally accepted with the corrected three-file package by the included internal review A16.

Authored dependencies: [P13](proofs/P13_BAD_PRIME_NORM_AND_RESTRICTED_IDENTITY.md), [P15](proofs/P15_SMALL_LOWER_LEVEL_BAD_U.md), [P25](proofs/P25_NONPRINCIPAL_DUAL_BAD_U.md).
Internal review: [A16](reviews/A16_NONPRINCIPAL_BAD_U_ACCEPTANCE.md).
Public source IDs: S02, S03.
Original SHA-256: `df00d9b385dc1d78c6d767ded31fa7f4d35805b203242a0e5fbf1dbfe4c0c592`.
Public proof bytes are identical to the pinned original.

### P27 Detail: good lower central transport before arithmetic descent

[Complete proof](proofs/P27_GEOMETRIC_CENTRAL_TRANSPORT_DETAIL.md)

Upstairs central-transport supplement at proper good lower levels, before arithmetic descent. Formally accepted with the corrected three-file package by the included internal review A16.

Authored dependencies: [P25](proofs/P25_NONPRINCIPAL_DUAL_BAD_U.md), [P26](proofs/P26_CONVENTION_AND_PRINCIPAL_RECOVERY.md).
Internal review: [A16](reviews/A16_NONPRINCIPAL_BAD_U_ACCEPTANCE.md).
Public source IDs: S02, S03.
Original SHA-256: `29242dbd60de40165c77c3b98f3a5899a6048abaa8cc12abb7aa68b74a3ae314`.
Public proof bytes are identical to the pinned original.

## Arithmetic residue targets and the uncomputed values

### P12 Prime-power residues, integral target components, and the remaining cusp identity

[Complete proof](proofs/P12_ABSOLUTE_INTEGRALITY_AND_RESIDUES.md)

At N=q^n the entire residue module inflates from the Hilbert class field, with exponent Q^ord([q])-1 and exact prime-to-p character support. Existing maps lift uniquely to the integer-ring target off this support. Actual surviving cocycle residues remain uncomputed.

Authored dependencies: [P03](proofs/P03_RELATIVE_SYMBOL_DERIVATION.md).
Internal review: [A6](reviews/A6_INTEGRALITY_ACCEPTANCE.md).
Public source IDs: S02, S03, S14, S16.
Original SHA-256: `1c1dd40bd36b66aa38c395d95a427464e9b530ed8fc56f11e098f799f4e568b8`.
Public proof bytes are identical to the pinned original.

### P16 Exact CM theta-symbol residues at the first admissible 2-power level

[Complete proof](proofs/P16_EXACT_THETA_RESIDUE_TEST.md)

Exact discriminant -23, q|2, q^2 local rational-theta pair: residue j-bar upstairs and j-bar^4 in the unramified good-model base; normalization by 576 gives j-bar^2. Endpoint-potential cancellation holds on the specified unimodular graph. Marked extension is not identified with the ray field; this does not evaluate the LSSW cocycle residue.

Authored dependencies: [P03](proofs/P03_RELATIVE_SYMBOL_DERIVATION.md), [P12](proofs/P12_ABSOLUTE_INTEGRALITY_AND_RESIDUES.md), [P17](proofs/P17_NORMALIZATION_SOURCE_ADDENDUM.md).
Internal review: [A10](reviews/A10_RESIDUE_ACCEPTANCE.md).
Public source IDs: S02, S18, S19, D01.
Original SHA-256: `8e9aee84bdec01f3a7209cf36a0703257cb2dc799860274bf458b3b03eb5d240`.
Public proof bytes are identical to the pinned original.

### P17 Normalization source check and root-of-unity scope

[Complete proof](proofs/P17_NORMALIZATION_SOURCE_ADDENDUM.md)

Robert/Kato comparison is retained up to a twelfth root of unity. The factor vanishes in R-valued symbols and in the specified exact tame symbols. The fixed rational function remains Delta^2/psi5; incomplete Kato download is explicitly not evidence.

Authored dependencies: Standard and cited source inputs only..
Internal review: [A10](reviews/A10_RESIDUE_ACCEPTANCE.md).
Public source IDs: S18, S19.
Original SHA-256: `1c1882ad7fafcc70260b5de861c7b17534e8f447640e13468a7fd10b107800b7`.
Public proof bytes are identical to the pinned original.

### P29 Exact congruence-kernel and smoothing obstructions for actual prime-power residues

[Complete proof](proofs/P29_CONGRUENCE_KERNEL_AND_SMOOTHING_RESIDUES.md)

For actual residue homomorphisms at proper unit-injective prime-power levels, zero is equivalent to finite q-adic dependence and to zero invariant restriction on the q-adic congruence kernel. M[J] and M/JM vanish except for one quadratic F5 line when five ramifies and Norm(q)=1 mod5, with the class-group five-part retained. No actual residue is evaluated; M/JM is not the compatible-family existence obstruction.

Authored dependencies: [P12](proofs/P12_ABSOLUTE_INTEGRALITY_AND_RESIDUES.md), [P16](proofs/P16_EXACT_THETA_RESIDUE_TEST.md), [P17](proofs/P17_NORMALIZATION_SOURCE_ADDENDUM.md), [P20](proofs/P20_ARITHMETIC_DESCENT_AND_AUXILIARY_REMOVAL.md), [P21](proofs/P21_FIVE_PRIMARY_EXCEPTION_CHECK.md), [P22](proofs/P22_OPEN_HOMOLOGY_GOOD_HECKE.md), [P23](proofs/P23_EXACT_SWAP_AND_CYCLIC_FOUR.md), [P24](proofs/P24_CYCLIC_FOUR_RAY_FIELD_DESCENT.md), [L1](qualifications/L1_MODEL_TRANSPORT_SCOPE_CLARIFICATION.md), [L2](qualifications/L2_GERSTEN_SIGN_TRANSPORT_ADDENDUM.md).
Internal review: [A18](reviews/A18_PRIME_POWER_RESIDUE_ACCEPTANCE.md).
Public source IDs: S02, S22.
Original SHA-256: `db401a8da74c019f6ee3c7ec856b212d5a0cbce76027591cb69603ed3bcb5b8d`.
Public proof bytes are identical to the pinned original.

### P30 A concrete occurrence of the surviving five-line

[Complete proof](proofs/P30_EXCEPTIONAL_FIVE_EXAMPLE.md)

At Q(sqrt(-5)), level (11), the actual ambient residue module is F5 squared with its class-group swap. The common kernel is anti-diagonal and the smoothing quotient is the same nontrivial quadratic character. This computes the coefficient module, not an actual cocycle value.

Authored dependencies: [P21](proofs/P21_FIVE_PRIMARY_EXCEPTION_CHECK.md), [P29](proofs/P29_CONGRUENCE_KERNEL_AND_SMOOTHING_RESIDUES.md).
Internal review: [A18](reviews/A18_PRIME_POWER_RESIDUE_ACCEPTANCE.md).
Public source IDs: Inherited through the authored dependencies.
Original SHA-256: `5cfa8d47078c8a72b8959ea4d294ee504b47130c030d0015797b8180a7214b31`.
Public proof bytes are identical to the pinned original.

## Theta values and relative calibration

### P18 Integral theta normalization and genuine torsion relations

[Complete proof](proofs/P18_INTEGRAL_THETA_NORMALIZATION_AND_RELATIONS.md)

Canonical scalar-powered U_n via universal torsion-free units before specialization; restricted unpowered CM values exactly when no rational p>=5 satisfies (p)|N^2; exact cross-ratios, |G|^2 triangle annihilation, unpowered 2,3-primary triangles and powered cyclic-seven triangle. The first specialized-unit cancellation argument was rejected and repaired; general CM divided-power V_N was withdrawn. No unrestricted roots, odd-primary unpowered triangles, global face/component relations or geometric absolute calibration.

Authored dependencies: [P03](proofs/P03_RELATIVE_SYMBOL_DERIVATION.md), [P07](proofs/P07_RIGHT_END_LIFTING.md), [P16](proofs/P16_EXACT_THETA_RESIDUE_TEST.md), [P17](proofs/P17_NORMALIZATION_SOURCE_ADDENDUM.md).
Internal review: [A11](reviews/A11_RELATIVE_THETA_ACCEPTANCE.md).
Public source IDs: S02, S04, S12, S20.
Original SHA-256: `8c1b6b0877e0b99569da58f99bf7abc112056a5538c16f44d5ce5aec4b1a7534`.
Public proof bytes are identical to the pinned original.

### P23 Exact swap calibration and a cyclic-four relative theta map

[Complete proof](proofs/P23_EXACT_SWAP_AND_CYCLIC_FOUR.md)

Exact constant-sensitive unshifted swap on E x E, with standard tame sign and source-sign negative; exact moved-primitive formula still leaves shear transitions uncomputed. For O/N=Z/4 on one fixed same-curve/principal component, an actual K2 cusp potential defines a full relative map with zero absolute restriction. Raw factor 576 differs from three-term factor 624. P24 upgrades this restricted construction to the ray field; equality with the geometric absolute map remains unproved.

Authored dependencies: [P03](proofs/P03_RELATIVE_SYMBOL_DERIVATION.md), [P07](proofs/P07_RIGHT_END_LIFTING.md), [P08](proofs/P08_GEOMETRIC_COCYCLES.md), [P14](proofs/P14_SCALAR_FIVE_NORMALIZATION.md), [P16](proofs/P16_EXACT_THETA_RESIDUE_TEST.md), [P17](proofs/P17_NORMALIZATION_SOURCE_ADDENDUM.md), [P18](proofs/P18_INTEGRAL_THETA_NORMALIZATION_AND_RELATIONS.md).
Internal review: [A15](reviews/A15_SYMBOL_CALIBRATION_ACCEPTANCE.md).
Public source IDs: S02, S03, S04.
Original SHA-256: `66165ae9b3288126e9906221329a7d7f896afdd5e4808058fcb54998414e669f`.
Public derivative SHA-256: `4cb2ef4909e688cc1943b72e4caa7c29989b052139759f0aca2f3db9d7987d3f`; only the recorded neutral editorial change differs.

### P24 Exact ray-field target for the cyclic-four relative theta map

[Complete proof](proofs/P24_CYCLIC_FOUR_RAY_FIELD_DESCENT.md)

For O/N=Z/4, F(N) is the Hilbert class field H; even normalized theta entries descend in K1 before forming Q in K2(H) tensor R. The restricted same-curve/principal-component relative map has a nonzero -23/q^2 edge value, detected by tame residue j-bar^2 of order seven. Its absolute restriction is zero. No all-component assembly or geometric absolute calibration.

Authored dependencies: [P16](proofs/P16_EXACT_THETA_RESIDUE_TEST.md), [P17](proofs/P17_NORMALIZATION_SOURCE_ADDENDUM.md), [P18](proofs/P18_INTEGRAL_THETA_NORMALIZATION_AND_RELATIONS.md), [P23](proofs/P23_EXACT_SWAP_AND_CYCLIC_FOUR.md).
Internal review: [A15](reviews/A15_SYMBOL_CALIBRATION_ACCEPTANCE.md).
Public source IDs: S02, S03.
Original SHA-256: `01ca846cb333132e0c6e31f24597940513b8b2b76563f0a3857faf3555fc3f9d`.
Public proof bytes are identical to the pinned original.

### P28 Exact cyclic-powered triangles and a geometric calibration obstruction

[Complete proof](proofs/P28_CYCLIC_POWERED_TRIANGLES_AND_CALIBRATION_OBSTRUCTION.md)

Exact scalar-powered theta triangles for every cyclic order over R, by universal exterior-square cancellation before specialization; injectivity of coordinate projection on same-curve full-SL2 invariant finite torsion cycles; conditional genuine-ray-field unit-root uniqueness and an order-seven formal relation obstruction. No unrestricted unpowered relations, mixed-component extension, or moved arithmetic calibration.

Authored dependencies: [P03](proofs/P03_RELATIVE_SYMBOL_DERIVATION.md), [P18](proofs/P18_INTEGRAL_THETA_NORMALIZATION_AND_RELATIONS.md), [P23](proofs/P23_EXACT_SWAP_AND_CYCLIC_FOUR.md), [L1](qualifications/L1_MODEL_TRANSPORT_SCOPE_CLARIFICATION.md), [L2](qualifications/L2_GERSTEN_SIGN_TRANSPORT_ADDENDUM.md).
Internal review: [A17](reviews/A17_SYMBOL_CALIBRATION_ACCEPTANCE.md).
Public source IDs: S02, S03, S04.
Original SHA-256: `17c4cab7075c1886057e28fc19d680c96693a3a603857a0f92d1e5abd80830a6`.
Public proof bytes are identical to the pinned original.

## Cusp reflections and the remaining wild-five test

### P33 Actual cusp-loop vanishing by global reflections

[Complete proof](proofs/P33_CUSP_REFLECTION_AND_COMPACTIFICATION.md)

Exact global cusp reflections give actual zero loop values. All boundary H1 vanishes when at most one q has n_q>e_q and that q has n_q<=2e_q+1; this is exact for ordinary and Gaussian units, with a general-unit criterion also proved. At locally shallow levels n_q<=2e_q+1 for every q, the W_N-trivial target projection of every existing Gamma0 class compactifies. Arithmetic applications require the map to exist; targets and prior Hecke restrictions are unchanged.

Authored dependencies: [P06](proofs/P06_STABILIZERS_AND_OBSTRUCTION.md), [P20](proofs/P20_ARITHMETIC_DESCENT_AND_AUXILIARY_REMOVAL.md), [P22](proofs/P22_OPEN_HOMOLOGY_GOOD_HECKE.md), [P25](proofs/P25_NONPRINCIPAL_DUAL_BAD_U.md), [L1](qualifications/L1_MODEL_TRANSPORT_SCOPE_CLARIFICATION.md), [L2](qualifications/L2_GERSTEN_SIGN_TRANSPORT_ADDENDUM.md).
Internal review: [A20](reviews/A20_CUSP_COMPACTIFICATION_ACCEPTANCE.md).
Public source IDs: S02.
Original SHA-256: `8eb42f475cce66348c6de51990112bbd011eb703b7425483d79fd98f9a380993`.
Public proof bytes are identical to the pinned original.

### P34 A concrete remaining wild-five cusp test

[Complete proof](proofs/P34_EXPLICIT_REMAINING_FIVE_CUSP.md)

For F=Q(i), N=(2+i)^2, the actual source-calibrated unaugmented open map is integer-ring-valued; two explicit middle-cusp loops have still unevaluated values in five-primary K2 Galois invariants. Boundary rank two is not a nonzero K2 value, and degree-five invariants are not identified with descent.

Authored dependencies: [P12](proofs/P12_ABSOLUTE_INTEGRALITY_AND_RESIDUES.md), [P20](proofs/P20_ARITHMETIC_DESCENT_AND_AUXILIARY_REMOVAL.md), [P22](proofs/P22_OPEN_HOMOLOGY_GOOD_HECKE.md), [P33](proofs/P33_CUSP_REFLECTION_AND_COMPACTIFICATION.md), [L2](qualifications/L2_GERSTEN_SIGN_TRANSPORT_ADDENDUM.md).
Internal review: [A20](reviews/A20_CUSP_COMPACTIFICATION_ACCEPTANCE.md).
Public source IDs: S02.
Original SHA-256: `e7a45fbba22523dc48e3903bbcc5b16b34b4b0d9caf4bf37d9fbc4e863fd70ea`.
Public derivative SHA-256: `9724d4c992cf2df6594362f0361a2c3748041218f43e607460b33cfcb7042fb3`; only the recorded neutral editorial change differs.

## Mathematical qualification texts

[L1](qualifications/L1_MODEL_TRANSPORT_SCOPE_CLARIFICATION.md) — Literal primitive/model transport is for product-coordinate elliptic-model isomorphisms with the shear transported, or a deliberately transported target primitive. Arbitrary mixed O-linear isomorphisms compare independently selected primitives by a normalized coboundary; specialization requires the comparison lift to be regular at the marked orbit.

SHA-256: `1fd586ac665c268be2bd92fa92fe14f383d11ccad361b39d075c9bec6063d758`.

[L2](qualifications/L2_GERSTEN_SIGN_TRANSPORT_ADDENDUM.md) — The explicit standard tame differential in PASS2 and reciprocal ShVe/source differential satisfy d2_src=-d2_std. J2=-Id, J1=J0=Id transports complexes with eta fixed; source-sign cocycles and corrections are negatives of standard-sign ones. Homogeneous existence, norm, Hecke and integrality claims are unchanged. Explicit signed edge values and source calibration must retain this transport; final Cremona-edge orientation remains unresolved.

SHA-256: `1b1bd51319bfe4a10a7b3010e9f9ac8a4dcf2cdcbe9acaaf51ed66ac170949ba`.

## Internal review records

The two final combined reports summarize the completed final review lanes; they do not broaden the individually reviewed theorems. The nonprincipal report A16 is the formal acceptance of its three-file package.

- [A1: Independent audit of the constant obstruction and integral trace repair](reviews/A1_INDEPENDENT_ACCEPTANCE.md); 13,528 bytes; SHA-256 `512b6424efbd6f3134a673a0d292205659d2fecbeeeda9116a12ce0d9c406ba0`.
- [A2: Independent acceptance audit: relative symbols and boundary depth](reviews/A2_AUDIT_REPORT.md); 17,000 bytes; SHA-256 `326a605f3a60eb6b1351744b620b54b0be33b710ae4df09ac0333a1ecdc69848`.
- [A3: Independent audit: residue lifting and geometric cocycles](reviews/A3_RESIDUE_AND_GEOMETRY_ACCEPTANCE.md); 12,345 bytes; SHA-256 `d891c659b25b0c51fe9b12f02188c87cd17a488c96f254114bb498a43cf075f5`.
- [A4: Independent audit: ordinary ramified-five cocycle lifting](reviews/A4_RAMIFIED_FIVE_ACCEPTANCE.md); 11,787 bytes; SHA-256 `59018a2b4e467bea879cd5d81ddaa6ad94c81eb2a2c0ef10b178c2fd26cd0332`.
- [A5: Independent audit: finite-orbit ordinary normalization](reviews/A5_FINITE_ORBIT_ACCEPTANCE.md); 4,449 bytes; SHA-256 `179c8ff3b33ac26230b0daefdd0107bb85733f0e8e45107b110c117480b994bd`.
- [A6: Independent acceptance: absolute-integrality lane](reviews/A6_INTEGRALITY_ACCEPTANCE.md); 11,601 bytes; SHA-256 `223d5166a3a7536219ba4704ea2c9b78ed0874ad6896dee7267a8d3b4b31cc63`.
- [A7: Independent acceptance: actual restricted bad-prime arithmetic identity](reviews/A7_BAD_PRIME_ACCEPTANCE.md); 17,481 bytes; SHA-256 `efd6d83c4216b3dd68535f7034a98d8b3bd19e58829da9bb36cf34b53f35a8ad`.
- [A8: Independent acceptance: scalar-five normalization](reviews/A8_TRACE_NORMALIZATION_ACCEPTANCE.md); 7,138 bytes; SHA-256 `0ed919b9ae134cf452569f861e5df0a0268b2cff139fc99b90da6384b257df20`.
- [A9: Independent acceptance: proper nonadmissible lower levels](reviews/A9_BAD_PRIME_EXTENSION_ACCEPTANCE.md); 6,770 bytes; SHA-256 `542f5f16b8560f6aca787539a756987073c1b662cf2ca3a17310ae3df028569e`.
- [A10: Independent acceptance: exact local theta-symbol residue test](reviews/A10_RESIDUE_ACCEPTANCE.md); 8,144 bytes; SHA-256 `e2eb8b3983c4799350c2bf113b8652ffe0aacc9e6fb5d221e529d6e79c1956ae`.
- [A11: Independent acceptance: specialized theta normalization and relations](reviews/A11_RELATIVE_THETA_ACCEPTANCE.md); 11,828 bytes; SHA-256 `24a9b1998f441284336d4056d8d6973b229d9029fc172f5a3b3af1d130e7eac8`.
- [A12: Independent acceptance: geometric Hecke compatibility at five](reviews/A12_FIVE_COMPATIBILITY_ACCEPTANCE.md); 7,044 bytes; SHA-256 `acc8dda219c1450bfdce9f190a77e94a174a3a78b0076e72d2fe796c245d5e39`.
- [A13: Independent acceptance: arithmetic descent and nonexceptional removal](reviews/A13_ARITHMETIC_DESCENT_ACCEPTANCE.md); 11,012 bytes; SHA-256 `fa8a084403c0067f211c5f89ebe14e6b228c05dcd99cc2d3500fca117b209d39`.
- [A14: Independent acceptance: the integral open map at all good primes](reviews/A14_OPEN_HOMOLOGY_ACCEPTANCE.md); 5,681 bytes; SHA-256 `eca50713d73f709da00e953d9adfaaa73f8ffa9face6efd32e6b7bf4355421f5`.
- [A15: Independent acceptance: exact swap and cyclic-four ray-valued symbols](reviews/A15_SYMBOL_CALIBRATION_ACCEPTANCE.md); 9,444 bytes; SHA-256 `f17404941b9d0c81a06040dd82b4678466789a149d6f63684816fd4517c0a311`.
- [A16: Independent acceptance: nonprincipal inverse-U assembly](reviews/A16_NONPRINCIPAL_BAD_U_ACCEPTANCE.md); 15,451 bytes; SHA-256 `3267e452fac83e3debfd7cc8b8da5711cf560c1e0fd72ffa4c7329eb56ae2797`.
- [A17: Independent acceptance: cyclic-powered triangles and the finite-support obstruction](reviews/A17_SYMBOL_CALIBRATION_ACCEPTANCE.md); 10,277 bytes; SHA-256 `9cfbbb7f0e638fac02738822b3bf430beb8b6fc57c098cc75cb0c8e734e6d125`.
- [A18: Independent acceptance: q-adic residue reduction and exact smoothing target](reviews/A18_PRIME_POWER_RESIDUE_ACCEPTANCE.md); 11,857 bytes; SHA-256 `d2db7c05b95c6069093ab78a100e82ea61acd9d1414e7d9f59cabdd2a7fb33cd`.
- [A19: Independent acceptance: final-pass exceptional-five smoothing](reviews/A19_EXCEPTIONAL_SMOOTHING_ACCEPTANCE.md); 12,590 bytes; SHA-256 `41aeb3b6fc336d3bb7aa538dc46c4a876f27355060955a73f10c7bf48f28a86f`.
- [A20: Independent acceptance: actual cusp vanishing and compactification](reviews/A20_CUSP_COMPACTIFICATION_ACCEPTANCE.md); 11,277 bytes; SHA-256 `0e1a22131f1cd5d9b3f4a09ea274c0072838470c5177dc37826a013ad988d509`.
- [A21: Final-pass symbol and prime-power residue audit](reviews/A21_COMBINED_ACCEPTANCE.md); 5,271 bytes; SHA-256 `6ecafd5641aed2d2443f71a2aaa5858e152aa081d94949933fb115c44d5064c2`.
- [A22: Final-pass arithmetic and topological review](reviews/A22_COMBINED_ACCEPTANCE.md); 3,593 bytes; SHA-256 `69198072daf97ae54fff9082dbf5716465fe8dccb32a9212de74a642183fa60c`.
