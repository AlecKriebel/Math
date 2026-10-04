# Full independent review requested: first-turn negative candidate

The exact source question is printed2479 after Proposition2; the source's definitions and p>3, perfect k, W=W(k) assumptions are printed2476–2477. Both definition/question pages were visually inspected. Read SOURCE_GATE.md then TURN_1.md. Proposed complete negative result at1/5, not a broader Coleman/Jacobian statement.

Primary input: Hoshi March2021 revised author manuscript sources/hoshi2021.pdf. Read Definitions2.1–2.4, Proposition2.5, Definition3.4, Remark3.5.1, Proposition3.11(2),(5) and Lemma4.9. The lifting page9 and source page2479 are rendered locally. These provide the exact contravariant duality and finite-Honda lift, without invoking a blanket finite-group lifting assertion.

High-risk checks:
1. F is Frobenius-semilinear, V inverse-Frobenius-semilinear. Every matrix/basis coefficient is in F_p, so integer identities commute with both scalar twists. Verify FV=VF=0, exactness, rank6 and the explicit qss module flag.
2. Reverse the module flag correctly under the exact contravariant equivalence. Each factor is rank-two supersingular elliptic p-torsion over algebraically closed k; no lift of that filtration over W is assumed.
3. Check delta=dim(imF² intersection imV²) is invariant under semilinear-module isomorphism. For the Cartier dual, use Hoshi's dual matrices (V transpose,F transpose) with twists, not an unqualified ordinary-linear dual. Original delta0, dual delta1.
4. Check L=span(e0,e3,e5) satisfies every finite-Honda condition and that Proposition3.11 gives a p-killed finite flat commutative group over W with exactly this reduction and rankp^6. No hidden principal-polarizability assumption occurs in the classification.
5. Verify the direct-sum extension for every n≥3 preserves the discrepancy and qss filtration, and that reduction of Cartier duality makes the integral group non-self-dual as well.

Run turn1/check_module.py and compare turn1/verification.json,9,014 assertions, standard library only. Tests include nontrivial semilinearity over F_25 and ranks/direct sums over ten prime fields; these supplement the written all-p proof. Validate all manifest hashes and source identities. Classical classification is credited; no priority certification or claimed Jacobian counterexample.

No further author turn is necessary if the full candidate passes. Preserve all frozen bytes and make any required correction additively. Parent retains the final publication/disposition gate.
