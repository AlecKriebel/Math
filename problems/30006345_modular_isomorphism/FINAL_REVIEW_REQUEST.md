# Independent full source/proof review request

Review the unchanged final manifest-bound packet for 30006345 / OWR-14299292-007, all five TURN files and their exact checkers/receipts. Recommended original disposition is **unsolved 5/5**; no proof claims the arbitrary-field source has been resolved.

## Source scope and dependencies

- Exact OWR 27/2025 contribution: Leo Margolis, joint Taro Sakurai, printed 1416–1417, https://ems.press/content/serial-article-files/51860 ; publisher https://ems.press/journals/owr/articles/14299292 , actual publication 10 November 2025. Printed 1416 was visually checked. The complete primary PDF and relevant image/text are local in sources/.
- Margolis–Sakurai all-field paper, pinned current PDF dated 23 October 2025, https://arxiv.org/abs/2505.05902v2 . Check Question 2.10 and Section 2.2 against the classical prime-field theorem, and especially Propositions 2.7 and 2.9 used in the last strengthening of turn 5. Avoid mixing the anomalous earlier HTML metadata with this pinned edition.
- García-Lucas–del Río reduction, Theorem A/Corollary B, https://arxiv.org/abs/2305.09355 . It reduces a given isomorphism to some finite field, not automatically F_p.
- O’Brien–Stanojkovski, https://arxiv.org/abs/2411.19555 , Section 2.1/Theorem 2.3: credited Baer construction and rank loci. The group-invariant result must not itself be treated as a full-algebra theorem without the supplied graded bridge.
- Milne, *Algebraic Groups*, 2022 online edition, https://www.jmilne.org/math/Books/iAG2022.pdf : Proposition 1.26, Corollary 1.39, and Section 17(k), particularly Corollaries 17.97–17.98 (printed 383–384). These were read through web PDF text; a whole local PDF download returned HTTP 406, so no whole-PDF hash is asserted. Verify reduced-subgroup/smoothness over F_p and the precise Lang/Frobenius hypotheses. This is a credited theorem input, not a computational claim.

## Highest-risk mathematical points

1. Ordered-monomial dimension arguments must genuinely reconstruct the degree-one bracket span and not identify kG with gr_J(kG). Check class-two/exponent-p and odd-p hypotheses, basis independence and the intrinsic nature of the spaces.
2. Turn 1's quadratic splitting changes the entire graded algebra but not the full algebra; check the explicit linear formulas and noncommuting pth-power caveat.
3. Turn 2 uses rad(Z(kG)), not Z(kG)∩rad(kG)^j. Audit the square-zero center module, radical tensor convolution, reversed-polynomial coefficient recovery and the assumption that both groups lie in the displayed family.
4. Turn 3 must distinguish full geometric pencil rank loci, not only F_3-rational points. Check the two coprime irreducible quadratics, absence of rank 4 for the mixed pencil over an algebraic closure, and the bridge from a full algebra isomorphism to a graded tensor equivalence.
5. Turn 4's reduced stabilizer must be geometrically connected, not merely a finite rational point set. Check a=g^−1F(g), h^−1F(h)=a and the correction g h^−1 with the correct multiplication order. Confirm the explicit factor-swap disconnection and retain the hypothesis.
6. Turn 5 uses components of the **full algebra** automorphism group. Check the twisted-coboundary sufficiency via R^0, the orbit permutation x↦alpha tau(x), its return-time bound≤|Pi| and the relative-Frobenius correction. Then audit the quadratic fixed algebra basis, local radical and descended powers, the nonsplit degree-one bracket, and center-dimension exclusion. The extension bound is not a universal proof that descent reaches F_p.

Run each verify_turnN.py separately and compare stdout byte-for-byte with TURN_N_CHECKS.json. Review the mathematical proofs independently; the finite controls do not compute general algebraic-group components, prove Lang's theorem, or replace the all-field/topological arguments. Preserve all frozen author bytes and use an additive review/correction if needed. Public artifacts exclude raw imports, full source files and private coordination. No sixth author search should be added during this review.
