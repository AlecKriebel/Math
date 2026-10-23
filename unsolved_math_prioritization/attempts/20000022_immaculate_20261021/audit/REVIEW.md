# Independent adversarial review: row 1895 / ID 20000022

## Verdict: ACCEPT PARTIAL ONLY

Reviewed on 2026-10-21. This accepts the scoped mathematical results and repaired computational fixtures, not a solution of the AIM symplectic-interpretation problem, not general necessity of the deficient-slope condition, and not a novelty claim. No publication or QUEUE edits were performed by this reviewer.

### Final reviewed input SHA256

- REPORT.md: `6d93107295fe6c77fda82109e7b042c61314185a2709ea843c9475dfd75b72f9`
- check.py: `0e94bfce2934530801b5b4059a1a4ab1068172b005fa91899306b89fa5afc119`
- results.json: `f660288b24e1cc9b7462735e3fddb9098004fc873d7b3938024cd0e21305f534`

Acceptance is bound to these bytes. Future modifications require review of their changes.

## Material defect found and repaired

The originally submitted script returned its `cones` list by reference. Subsequent in-place replacement of one product cone by three blowup cones silently changed the already-computed product record. The six-ray P1xP1xP1 entry therefore listed nonexistent ray index 6. The ranks were computed before mutation, so they remained correct; the serialized fan certificate did not.

Original check.py hash: `ab2e89d49a1b1c005b8d2d14de48530c9bab72125591d4b65521fd88fb15ca56`.
Original results.json hash: `b33f98db5efbed706ed251f7eccd7999cf20c50166ffd758bbda10154d7c08e3`.
Original REPORT.md hash: `fa01d4933d987c315ab088f96fd0461f41edd6837cabeece93424129edc24ed3`.

I reran the original exact script: it reproduced the original bytes and defect. The author repaired the return value by copying the cone sequence and added range validation. I reran the repaired script, whose output matches final results.json byte for byte (`rerun_repaired.json`). `rerun_original.json` is retained as the failed original audit evidence, not as an accepted fan certificate.

I also implemented `independent_check.py`: its unknowns are all maximal-cone slope coordinates, its continuity equations require agreement on shared rays, and its additional equations require common evaluation on the chosen ray. This avoids the report's ray-value/inverse-matrix construction. It independently reproduces every quotient-kernel dimension and verifies that every maximal cone in the recorded fixtures has determinant of absolute value one. Output is in `independent_check.txt`. These are fixture tests, not exhaustive fan enumeration or proof of completeness for arbitrary input.

## Five-approach review

### 1. Ray-kernel and wall obstruction: accepted within cited scope

The matrix convention is correct: ray vectors as rows give V_sigma m_sigma = S_sigma a, hence P_sigma = V_sigma^{-1}S_sigma. Global linear functions inject into ray-value space because a complete fan spans N_R, giving a d-dimensional kernel subspace. Nonzero quotient exactly means not all slopes agree. A common ray evaluation confines all slopes to an affine hyperplane. Rational linear algebra and denominator clearing correctly produce integral slopes from a nonzero rational quotient class.

The converse reduction to a fan ray is an existing result, not established anew here. I directly inspected Borisov–Wang Proposition 3.8 and its statement supports precisely this use. Their Theorem 2.14 gives sufficiency; Theorem 4.12 has the stated three-dimensional collinearity restriction. Source: https://arxiv.org/html/1904.00799v3 .

Across a wall, continuity forces a slope difference into the one-dimensional annihilator of its span. If evaluation on w is zero while a wall normal evaluates nontrivially, that difference must vanish. Thus connected G_w implies only global slopes. Disconnectedness is appropriately not asserted sufficient.

The repaired independent dimensions are P2: (0,0,0); P3: (0,0,0,0); F0: (1,1,1,1); F1,F2,F5: (0,1,0,1); product threefold: (2,2,2,2,2,2); its point blowup: (2,2,2,2,2,2,0).

### 2. Hirzebruch classification: accepted, including endpoints

For a>=0, the summands have degrees b,b-n,...,b-an. All summands on P1 are acyclic exactly when every degree equals -1. For n>0 this forces (a,b)=(0,-1); n=0 gives b=-1. Relative degree -1 gives the full line a=-1. Serre duality maps (a,b) to (-2-a,-n-2-b), taking (0,-1) to (-2,-n-1), not (-2,-n-2). This checks the potentially fragile isolated endpoint. For n=0, duality preserves the second immaculate line b=-1. All integer a are covered without omitted boundary cases. This is an elementary known classification, correctly not advertised as new.

### 3. Blowup propagation and sharpness: accepted

For exceptional inclusion E and k>=1, the quotient in the divisor sequence restricts to relative O_E(-k). Its entire relative cohomology vanishes for 1<=k<=c-1. With Rf_*O=O and projection formula, the asserted strip 0<=k<=c-1 follows, including equivalence rather than only one-directional vanishing.

For the point blowup of the product threefold and L=O(-1,0,0), k=3 produces H^2(O_P2(-3)) of dimension one; acyclicity at k=2 transfers it to H^2 of the blowup line bundle. At k=-1 the restriction exact sequence transfers H^0(L|_p) to H^1. Both signs and cohomological degrees are correct. This establishes uniform sharpness through the example, not a claim that every individual line bundle fails outside the strip.

Refinement preserves all old full-dimensional slopes and introduces no new ones for the pulled-back function. Thus the cited blowups preserve an existing deficient slope hull. They cannot resolve the general missing necessity implication; the report explicitly respects that limitation.

### 4. Numerical arithmetic-family obstruction: accepted

HRR gives a polynomial in t. Infinitely many distinct zero values force every coefficient to vanish. The surface expansion gives exactly M²=0, M.(2L-K)=0, chi(L)=0. The restriction to fixed arithmetic direction is essential and is stated.

I suggested, and verified in the final revision, the stronger counterexample L=S, M=S+F on F2. Since S²=-2, S.F=1 and F²=0, M²=0. With K=-2S-4F, 2L-K=4(S+F), so the mixed coefficient vanishes too. Meanwhile O(S) has direct-image summands O and O(-2), yielding h0=h1=1. The classes L+tM have coordinates (t+1,t). The accepted classification in section 2 gives exactly t=-3,-2,-1 as immaculate, so the numerical conditions fail even to guarantee infinitely many immaculate members. This is stronger than the original chi-only counterexample and is correct.

### 5. Compact exact graphs: accepted only with stated brane assumptions

Critical points of a globally defined real function on a compact torus force graph intersections. Intersections alone would not prove nonvanishing Floer cohomology, but the report separately invokes the correct Hamiltonian-isotopy/Morse comparison for ordinary compact exact sections with compatible trivial rank-one data. It is then H*(T), up to grading conventions, and nonzero. A degenerate f-g can be handled by perturbation/invariance. Different local systems or stopped/noncompact objects are not covered, as the report explicitly warns. This is a negative test of a naive model, not the desired mirror construction.

## Literature and problem-status guardrail

I directly inspected Borisov–Duncan Theorem 1.1 and Remark 4.5 at https://arxiv.org/html/2312.02885v3 . The former already proves the forbidden-cone infinitude criterion. The latter explicitly separates unresolved necessity of the deficient slope-hull condition. The report does not substitute the solved theorem for that missing implication and does not claim a new 2026 literature-status verification.

I did not independently recover the original live AIM problem page or validate private corpus identity. Acceptance is for the supplied mathematical report and its explicit source boundary, not independent certification of that provenance. No broad brane interpretation, boundary-sensitive Floer differential, or general subspace classification is supplied. Any claim that the AIM task is solved would contradict this review.
