# Mirror-quintic orbifold expansions: source and status gate

Audit date: 2026-10-21. Target: 20000721 / AIM-ANALYTIC_NUMBER_THEORY-0085.
This is a source-recovery and scope audit, not a new mathematical result or a claim of complete solution.

## Source identity: PASS

The live primary AIM page was retrieved and its embedded problem 4.1 record inspected. Its text agrees exactly with the canonical dataset statement after CRLF/LF normalization. The original asks for leading terms of the genus-g B-model free energies at the zero-parameter orbifold point of the displayed quintic quotient. The live name and status fields are blank. The familiar descriptive title is editorial, not a title assigned on AIM. The extracted problem itself has not been replaced with a generated specialization.

Source: [AIM, Gromov–Witten invariants and number theory, §4, problem 4.1](http://aimpl.org/gromwitnumthry/4/).

The question supplies neither a genus bound nor a normalized local flat coordinate, polarization, or Hodge frame. It does not ask for classification of all analytic singularities, convergence of the full genus expansion, or an all-genus LG/CY theorem. Such targets must not be substituted for the original. Nor should its blank status be read as a current expert determination that no leading terms are known.

## Normalization contract required before coefficient acceptance

Use different symbols for the polynomial coefficient, the invariant moduli coordinate, the large-radius algebraic coordinate, and the exponentiated flat coordinate. For the AIM polynomial coefficient z_AIM, put u = -z_AIM/5. Its conventional Dwork form is then sum(x_i^5) - 5u product(x_i). The local invariant coordinate is Ψ = u^5; the orbifold uniformizing cover uses u. Compatible fifth roots must be selected. The large-radius algebraic coordinate x = 1/(5^5 Ψ) is not the large-radius flat variable Q = exp(I1/I0), and neither is automatically the AIM symbol q.

The quotient action, stack/coarse resolution interpretation, and period normalization must be fixed. A comparison of small FJRW potentials with continued GW/BCOV quantities must also transport polarization and Hodge trivialization. A mirror-map identity by itself is not an all-genus equality of potentials. Genus zero has prepotential integration ambiguities; genus one has an additive normalization. For higher genus, the Hodge-frame weight changes coefficients.

## Primary coefficient reference

[Huang–Klemm–Quackenbush, Topological string theory on compact Calabi–Yau: modularity and boundary conditions](https://arxiv.org/abs/hep-th/0612125), §3.4, gives an orbifold period basis with exponents 1/5, 2/5, 3/5, 4/5, hence finite order-five monodromy. In their invariant coordinate Ψ, the flat coordinate is s = ω2/ω1 = u(1 + 13u^5/360 + 110069u^10/9979200 + …). They rescale periods by 5^(3/2), select an orbifold polarization through period continuation, and take the corresponding antiholomorphic limit. This is not mere substitution into a large-radius holomorphic limit.

Their displayed first two coefficients for genera 0–5 agree with the inherited report. The first terms, respectively, are (5/6)s^3, -(1/9)s^5, (155/18)s^2, (488305/9072)s^4, (48550/567)s, and (1237460905/224532)s^3. These are existing computations, not contributions of this audit. The source calls higher-genus orbifold results predictions. Its PDF v1 and current HTML use different equation numbering; refer to §3.4 rather than conflating the numbers.

## Established mathematical foundations

- [Chiodo–Ruan, Landau–Ginzburg/Calabi–Yau correspondence for quintic three-folds via symplectic transformations](https://arxiv.org/abs/0812.4660): genus-zero FJRW mirror theorem and genus-zero LG/CY correspondence. Identifies the relevant Gepner-point period system. Its higher-genus quantization statement is presented as a prediction, not proved there.
- [Guo–Ross, Genus-One Mirror Symmetry in the Landau-Ginzburg Model](https://arxiv.org/abs/1611.08876): proves the small genus-one FJRW formula, explicitly verifying the corresponding HKQ conjecture. Its formula is log[I0(t)^(-31/3) (1-(t/5)^5)^(-1/12) (dτ/dt)^(-1/2)], τ=I1/I0. This is appropriate for a fixed-normalization low-genus coefficient check.
- [Guo–Ross, The Genus-One Global Mirror Theorem for the Quintic Threefold](https://arxiv.org/abs/1703.06955): proves the genus-one restriction of the quantized LG/CY correspondence. It is not an all-genus proof.
- [Guo–Janda–Ruan, A mirror theorem for genus two Gromov–Witten invariants of quintic threefolds](https://arxiv.org/abs/1709.07392): supplies a closed genus-two GW formula and verifies the BCOV mirror conjecture at genus two. Translating it to an orbifold coefficient table still requires the stipulated frame and polarization.
- [Guo–Janda–Ruan, Structure of Higher Genus Gromov–Witten Invariants of Quintic 3-folds](https://arxiv.org/abs/1812.11908): proves finite generation, holomorphic anomaly, and orbifold regularity. Its Corollary 1.5 is a precise constraint on coefficients of a normalized polynomial in finite-generation variables, not a general closed expression for the first nonzero orbifold coefficient. The paper did not establish the conifold-gap conjecture in all genera.
- [Liu–Ruan, Castelnuovo bound and higher genus Gromov–Witten invariants of quintic 3-folds](https://arxiv.org/abs/2210.13411): proves the Castelnuovo bound and discusses reconstruction up to genus 53 under the remaining BCOV conditions. This finite-genus reconstruction claim must not be promoted to determination of arbitrary-genus leading coefficients. Its historical description of which conditions remain conjectural is not a current-status source for October 2026.

## Material 2026 correction

[Chang–Guo–You–Zhang, Conifold Gap for the Quintic Threefold](https://arxiv.org/abs/2609.13921), v1 submitted 12 September 2026, is a new primary preprint claiming an all-genus proof. The PDF and HTML were both inspected. Theorem 1 is a master-space transfer criterion, and Theorem 2 verifies its hypotheses for the quintic MSP theory. Definitions 1.1–1.2 specify a differential-ring substitution into formal Laurent series; the conifold expansion uses admissible periods and a local flat coordinate. The asserted gap removes subleading negative powers after one prescribed pole.

Consequently, the inherited blanket assertion that the conifold gap remains unproved is outdated as a literature claim. State that this 2026 preprint claims to prove it, without implying peer-reviewed acceptance or a proof independently validated here. This concerns the conifold, not the orbifold. It supplies neither an arbitrary-genus orbifold leading-coefficient formula nor, by itself, the full quantized GW/FJRW correspondence.

## Formal versus analytic scope

A finite coefficient list does not prove convergence. A residue-class selection rule only restricts support, not the first nonzero coefficient or its value. A formal Laurent/Puiseux identity does not by itself classify analytic germs or exclude essential singularities of an unspecified function. Conversely, genuine finite-generation formulas in convergent period functions can support fixed-genus analytic statements after the formula, continuation path, branch, frame, and denominators are specified. Do not deny that possibility; do not claim it was proved merely by a finite formal calculation.

Finite-order orbifold branching in a coarse coordinate is different from a pole on its uniformizing cover. Orbifold regularity is different from conifold-gap behavior. Neither fixed-genus regularity nor all-genus coefficientwise assertions establish convergence or analytic meaning of the sum over all genera.

## Gate disposition

Source wording: verified against live AIM. Existing HKQ leading terms: verified as existing literature in a specified normalization. Inherited broad literature conclusion: requires the September 2026 correction. Novelty claim for the coordinate/support audit: not substantiated by this review. Full all-genus leading-term solution: not established by the retrieved references. Analytic singularity classification: not the original target and not established by the inherited finite expansions.

Accept only a bounded, attribution-rich normalization and status audit at this stage. Do not mark the original unqualified problem solved, or publish the inherited report unchanged. A future theorem-level coefficient acceptance requires an explicit source-to-frame dictionary and the exact genus range claimed.
