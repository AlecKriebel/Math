# Final source-scope verdict for the five-pass E-6322 investigation

16 October 2026. This report fixes the scope of what the investigation establishes. It does not certify exhaustive literature coverage or priority of any authored auxiliary result.

## 1. The source problem and the frozen benchmark are different statements

Ball's *Some Open Problems in Elasticity* (2002), Problem 6, p.11, asks for suitable constitutive growth assumptions giving a positive essential lower Jacobian bound for global or suitably defined local minimizers. The bound is equation (2.19), p.10. The surrounding model and full finite-energy admissible class appear on pp.2–4. The source does not prescribe the exponent tuple used here or select one local-minimality topology.

[Ball's author manuscript](https://people.maths.ox.ac.uk/ball/Articles%20in%20Conference%20Proceedings%20and%20Books/JMB%202002%20re%20Marsden%2060th.pdf).

E-6322 freezes one global-minimizer sufficient-condition branch: arbitrary positive coefficients in

W(F)=a|F|⁶+b|cof F|³+cJ²+dJ⁻² for J>0, and infinity otherwise;

all bounded connected smooth three-dimensional domains; all smooth orientation-preserving diffeomorphic full traces; and every finite-energy W^{1,6} competitor, with no imposed injectivity or approximation-by-diffeomorphisms restriction. Its conclusion is an individual-minimizer positive essential lower bound over the entire domain, including boundary collars.

A proof would establish that specific sufficient-condition branch. One compliant counterexample would reject this benchmark, while leaving other growth laws and the source's broader program untouched. A result confined to affine or small data, a symmetry class, interior compact subsets, or already regular solutions would not decide E-6322. The positive-power part of W is degree six; the complete density has both degree-six and degree-minus-six terms.

## 2. Established theory used as baseline

These facts are prior theory or direct applications, not claimed new results:

- **Existence.** Ball (2002), Theorem 2.1, p.4, applies through convexity in independent minors and the stated coercive lower bound. The smooth datum provides a finite-energy competitor. Finite energy forces J>0 a.e., while W^{1,6} embedding gives continuity on the closure. Neither fact is a uniform determinant bound.
- **Almost-everywhere inversion and area change.** Krömer, arXiv:1912.11086v2, Theorem 6.1, pp.26–27, applies with p=6>3 and degree one supplied by the full diffeomorphic trace. Its degree formulation works for the permitted domains with holes. Exceptional fibers are not ruled out. [Primary manuscript](https://arxiv.org/pdf/1912.11086v2).
- **Actual weak inverse derivative.** Bresciani–Davoli–Kružík, *Existence results in large-strain magnetoelasticity*, AIHP ANL 40 (2023), Proposition 2.5, pp.566–567, under its standing three-dimensional p>3, positive-Jacobian and a.e.-injectivity hypotheses, supplies a W^{1,1} inverse with derivative (Dy)⁻¹ composed with the inverse. [Primary article](https://ems.press/content/serial-article-files/28047?nt=1).
- **Area formula on good sets.** Barchiesi–Henao–Mora-Corral–Rodiac, arXiv:2311.02952v2, Proposition 2.1 and Definition 2.2, p.5, provide the approximately differentiable area formula and countable-Lipschitz good-set device used in our class proof. No unproved global Lusin-N assertion is substituted. [Primary manuscript](https://arxiv.org/pdf/2311.02952v2).

The first and second passes also inspected more recent invertibility and regularity papers. Titles using “global invertibility” were checked against their actual a.e. conclusions. Full-source unavailability for the original Ball 1981, Zhang 1991 and maximal-smoothness article was explicitly recorded; no unseen hypotheses were treated as verified.

## 3. Authored deductions obtained within this investigation

The following are proved in the cited campaign reports and independently audited. “Authored” identifies where the argument is supplied; it is not a claim that the statement is absent from previous literature.

1. From the known weak inverse theorem and Hölder inequalities, every admitted y has an actual inverse v∈W^{1,9/5}(D), cof Dv∈L^{9/4}, K=det Dv∈L³, D=G(Ω). An outward collar gives the full inverse trace G⁻¹. Change of variables gives exactly
   V(H)=a|cof H|⁶/K⁵+b|H|³/K²+c/K+dK³.
   See pass 2, `literature/INVERSE_SOBOLEV_BASELINE.md`.
2. The exact inverse-image class is characterized by finite V and a full-boundary transported Piola identity. The identity recovers weighted measure preservation, a.e. bijectivity, the primal W^{1,6} weak derivative and its full trace. Its energy-bounded closure and lower semicontinuity follow by lifting to primal W^{1,6} compactness, without low-exponent inverse-minor continuity. See pass 3, `EXACT_INVERSE_CLASS.md` and `TRANSPORT_PIOLA_CHARACTERIZATION.md`.
3. Compact W^{1,9/4} additions with finite resulting V preserve that class. Under the extra v∈W^{1,2} hypothesis the same holds for compact W^{1,2} additions. No finite-energy amplitude interval is inferred. See pass 3, `ADDITIVE_INVERSE_ADMISSIBILITY.md`, and pass 4's limits note.
4. Smooth graph transformations Φ(z,v(z)) with the specified boundary collar preserve the class whenever their final dual energy is finite. This covers natural W^{1,9/5} cutoff differences by pulling the calculation back to W^{1,6} primal coordinates. See pass 4, `STRUCTURED_NATURAL_EXPONENT_COMPARISONS.md`.
5. The final pass classifies graph derivative rules preserving orientation for every incoming positive-determinant matrix. With the strong graph collar condition, the only such universal rule is the identity. This is a restriction on a universal repair recipe, not on map-tailored comparisons. See `UNIVERSAL_GRAPH_REPAIR_OBSTRUCTION.md`.

The explicit admissible maps showing collapsed fibers, sharp inverse integrability, or isolated finite-energy addition amplitudes are not asserted to minimize the nonaffine full-class problem. The affine-minimizer cutoff example disproves one proposed comparison's finite energy; its minimizer itself has uniformly positive determinant. Conditional stress, regularity and tangent results likewise retain their stated additional hypotheses.

## 4. Final targeted check of the remaining low-exponent gap

Henao–Mora-Corral–Oliva, *Global invertibility of Sobolev maps*, author version 7 May 2019, published Adv. Calc. Var. 14 (2021), 207–230, Proposition 7.3, pp.16–17, assumes p≥n−1 and q≥p/(p−1), with bulk and boundary W^{1,p} regularity and bulk cofactor L^q. Proposition 7.4, p.17, lowers q to n/(n−1), but retains p≥n−1 and adds the specified extension and boundary-cofactor assumptions. Thus the known inverse exponent 9/5 misses a separate hypothesis even though its cofactor exponent 9/4 is high enough for the conjugate pairing.

[Primary institutional author version](https://repositorio.uam.es/bitstream/handle/10486/700604/global_henao_ACV_2021_ps.pdf?isAllowed=y&sequence=1).

The parsed primary statements and proofs were inspected. Local PDF downloads failed and screenshots were unavailable, so no local file hash or visual inspection is claimed. This supplements, rather than replaces, the pass-4 direct obstruction to naive low-exponent minor approximation.

## 5. Final determination

After the five authorized passes, the exact E-6322 assertion has neither been proved nor refuted. No inspected primary theorem or verified full-class counterexample settles it. This is the result of this investigation, not an exhaustive declaration of the literature's status.

The inverse route now has an exact comparison class and a substantial structured comparison theorem. Its unresolved analytic step is to construct comparisons with positive determinant and controlled finite V that force K∈L∞, or obtain a sufficient regularity estimate by another valid argument. Unrestricted natural-exponent class stability itself remains unproved and undisproved here; proving it alone would not supply those energy estimates.

No novelty or priority claim is made for the auxiliary results. None of the reviewed first-gradient, higher-gradient, small-data, planar, constrained-class or conditional-regularity sources is relabeled as an unconditional resolution of the frozen arbitrary-data three-dimensional benchmark or of Ball's broader adequate-growth problem.
