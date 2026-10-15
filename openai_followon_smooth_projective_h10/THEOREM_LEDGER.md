# Current theorem ledger

Status updated 2026-10-07 06:00 UTC / 2026-10-06 23:00 PDT, following the completed [dependency integration audit](reviews/dependency_integration.md). The source remains pinned at `adc7f1241b42e322a6451854ab7e4b4c146bf78a`. The statements below are the current **proved mathematical candidate**, supported by source-body reconstructions with two explicit substitutions. Priority, complete-package review and publication verification remain pending. The earlier unverified assessments are historical checkpoint statuses, not current proof-gap findings.

**T1 — target, candidate proved.** There is no algorithm which, given N and finitely many homogeneous integer polynomials defining

    X = Proj(Q[x_0,…,x_N]/(F_1,…,F_r)),

and promised that X is smooth, projective and geometrically integral over Q, decides whether X(Q) is nonempty. The presentation includes its projective embedding. Dimension, degree, equation count, ambient dimension and coefficient size may all vary. No behavior on invalid inputs is required.

The contradiction algorithm forms an affine zero locus, remembers it as an open subset of its projective closure, applies Poonen's effective construction, computes connected components, discards those that are not geometrically integral, and makes a finite nonadaptive OR of valid promised oracle queries. Every discarded connected regular component has no Q-point. The geometric mechanism is entirely inherited from Poonen2009, Theorems1.1(i),1.3 and Lemma10.1. Over Q, regular=smooth because Q is perfect.

**D1 — H10(Q), audited input with exposed substitutions.** Family004's arbitrary-variable decision problem is: given a finitely encoded f in Z[X_1,…,X_n], with n part of the input, decide whether f has a zero in Q^n. Its finite rational tests, Skolemization, compactness argument, additive elliptic indices and final height contradiction have been reconstructed. The resulting contradiction with integer H10 uses dovetailed searches, not an asserted existential definition of Z or a many-one reduction.

The required pointwise-2-converse is validated here in the **non-CM full-rational-two-torsion branch covering every constructed E_l: y²=x(x-l)(x+3l)**. The descent only gives full Selmer corank≤1 before the converse. The reconstructed converse excludes the divisible-Sha alternative; finiteness and the alternating Cassels–Tate pairing then realize the selected Selmer class by a rational point. The broader companion's other branches are not needed or certified by this ledger.

The two substitutions are part of the accepted route:

1. Construct the prime-independent corrected action at coefficient primes5 and2, apply published Pan2022 Theorem1.0.4 at5, identify the same compatible newform at2, and use coefficient2 for its conductor at residue prime5. This replaces the new unrestricted dyadic modularity companion in the five-point height argument. The fixed geometric configuration is the five discriminant210 quotient branch values, not arbitrary five rational points.
2. Apply the universal group-ring inverse-Frobenius/Euler correction before character evaluation in the non-CM cyclotomic construction. Its integral convention units preserve central values and prevent a loss of a power of2 per varying prime. Internal signed discriminants vary only after each E_l and its bad support are fixed.

The exact constructions are recorded in [VERIFIED_CORRECTIONS.md](VERIFIED_CORRECTIONS.md), [height-repair.tex](manuscript/height-repair.tex), and the integration audit. The rejected direct von Kanel–Kret fixed-field shortcut is not an input.

**T2 — height obstruction, candidate proved.** Fix the explicit self-delimiting homogeneous-equation encoding and its computable bit-length size s(e). For a rational point, use primitive integral homogeneous coordinates, first nonzero coordinate positive, and naive height max|z_i|. There is no total computable B(s) guaranteeing a point of height≤B(s(e)) for every nonempty member of the promised presented class. Such a B would decide existence by enumerating the finitely many primitive coordinate tuples of that height and checking the equations, contradicting T1.

**Exact current mathematical gap:** none identified in the checked dependency route. This is an audited proof candidate, not a claim of formal verification or conventional human peer review. No applicable full Family004 formalization was found. Complete-package review must verify the final manuscript, supplements, metadata and reproducibility artifacts together; a change after a clean fresh review requires renewed review.

**Remaining nonmathematical obligations:** complete priority/attribution resolution; final globally consistent publication candidate with both substitutions exposed; required independent complete-package review cycles and repairs; clean build and downloadable-PDF inspection; exact reviewed production Zenodo publication and DOI verification; tracker append/readback; final owned-file commit and push. No deposit, DOI or tracker completion is asserted here.

No fixed-dimensional, curve, surface, Fano, general-type, finite-point-promise, quantitative reduction, Turing-degree or single-query many-one claim is accepted. No optional no-point certificate claim is included.
