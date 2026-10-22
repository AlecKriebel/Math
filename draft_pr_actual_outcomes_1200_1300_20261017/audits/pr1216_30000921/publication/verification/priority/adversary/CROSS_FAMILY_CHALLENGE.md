# Reverse cross-family challenge

Completed UTC: 2026-10-17T18:34:31.816641+00:00. Scope: challenge the independently frozen priority report and its verification after both families had frozen their conclusions. This is an internal comparison artifact, not a publication or a historical-priority certificate.

## Verdict

**PASS, with one nonblocking indexing/support clarification.** No mathematical failure was found in the independent family's claimed Nikula–Gaussian implication, dense simultaneous polynomial failures, or dense frequent hypercyclicity in each fixed annular space. Its statement that the original every-input local null-orbit perturbation result is finer and is not established merely by Gaussian existence/density is correct and must be preserved in later framing. The proposed attributed historical negative-answer note with a self-contained elementary Baire proof is consistent with these findings, provided it makes no novel-discovery, first-solution, or earliest-priority claim.

The minor clarification concerns allowing M=0 under the exact lower bound (n+1)^(-1/2): coordinate zero then lies on a degenerate annulus, the unit circle. The full-support conclusion remains true, but that coordinate uses angular support, not a nonempty planar patch in an annulus. The frozen verification explicitly defines M>=1, where its planar-patch explanation is valid. Either keep that indexing convention or add the elementary circle argument below. This is not a counterexample or a gap in the result.

## Inputs and preservation

Read the independent family's frozen `REPORT.md`, `verification/VERIFICATION.md`, `MANIFEST.json`, `SOURCE_RECEIPTS.json`, `SOURCE_LEADS.md`, and `QUERIES.md`. The supplied and computed hashes agree:

- Report: `e5ac65ba3733965789fdcd9ce08d76c7e4624e7f54f4143a633aae0d39d6a06d`.
- Manifest: `7ebe5eb7d458b73ca6652337302ab8dc1da9f33e05c5d718d1b684c181290b67`.
- Frozen verification: `dd0857f652c2f99e9752dcfad532a76a5928fe0e07f860d751f8c7b150c7bf3a`.

All eight manifest entries match both their byte counts and hashes. All 51 retained-source file receipts match actual files under the independent family's ignored source directory. File identity authenticates available inputs; it does not, by itself, prove a historical reading act. The declared inspection scopes were checked for consistency with the report's assertions and with this family's independently retrieved primary copies. No conflict or inherited false inaccessibility claim was found.

This family's own `REPORT.md` remains at `0f82bb3a8409b98efb52af4d0c741ae7b9341fe22c9e74888a5f791602c80f6d`, and both own freeze entries (report and verdict) still match. No frozen sibling or own file was edited. `CROSS_FAMILY_INPUT_RECEIPT.json` records the actual input identity checks. No external communication, Git/index mutation, candidate edit, app write, or publication action occurred.

## 1. Older Gaussian implication: attempted failure modes

### Complex versus real coefficients

PASS. The independent report uses the circular complex Gaussian law with density pi^(-1) exp(-|z|^2). Its support is all of C, as required by Nikula. A real Gaussian law would fail that hypothesis and constrain all jets to the real axis; the report does not make that substitution.

### Entire convergence and applicability of the theorem

PASS. Nikula Theorem 1 on the inspected arXiv v1 PDF pp.2–3 has the stated full-plane support and logarithmic tail hypotheses. Gaussian tails meet the latter. The proof does not infer hypercyclicity from mere coefficient density or finite simulations. The independent verification transparently treats Nikula's theorem as input rather than claiming to reprove its full body; the report separately identifies its reading scope.

### Borel–Cantelli and simultaneous quantifiers

PASS. With alpha=3/4, the lower small-ball sum is bounded by sum(n+1)^(-3/2), and the upper-tail sum by sum exp(-log(n+e)^2), both finite. First Borel–Cantelli supplies a single eventual coefficient event. Once it is fixed, the leading Leibniz term has size at least c_p n^(d-alpha), and all lower terms together are O_p(n^(d-1)log n). Their ratio is O_p(log n/n^(1-alpha)), tending to zero for every fixed positive degree d. The constants and starting index may depend on p; the conclusion does not demand them uniformly over all polynomials. This is a deterministic implication for every p after the one event is chosen. No uncountable intersection is hidden here, and no independence of neighboring Leibniz terms is needed.

### Scalar escape implies nonhypercyclicity

PASS. Escape of the derivative evaluations in modulus prevents their scalar range, including any finite initial segment, from being dense in C. Evaluation at zero is continuous and onto, so a dense derivative orbit in H(C) would have dense evaluations. Constants are correctly excluded from the bad multipliers: nonzero constant scaling preserves frequent hypercyclicity. This proves the claimed all-vector multiplier classification when combined with the existence of the common counterexample family.

### Ambient density and polynomial addition

PASS. The Gaussian support proof controls a sufficiently late random tail by its finite expected norm and Markov's inequality, and matches a finite head with positive probability independently. Enlarging the head degree can satisfy both deterministic target-tail and random-tail requirements at once. More simply, one good F gives the dense translate F+C[z]. Polynomial additions preserve the high derivative orbit and high jets of every fixed polynomial product because p(F+q)-pF=pq is a polynomial. The threshold depending on p and q is allowed. The report correctly does not assert that translated samples remain IID or Gaussian.

### Compatibility with Costakis's residual positive family

PASS. A residual set of functions for which every nonzero polynomial product is HC(D) can coexist with a dense family of simultaneous failures. Full support of the Gaussian law does not make every residual set have probability one. The Gaussian event gives n|X_n| tending in modulus to infinity while the unscaled derivative orbit is frequently dense; the n-scaled derivative sequence therefore need not have the same hypercyclic vectors. The report keeps generic common scaled-orbit statements separate from all-vector pointwise preservation.

## 2. Fixed exact X_M: full support and density challenge

Take the independent report's exact bounds

    l_n=(n+1)^(-1/2),  u_n=log(n+e),
    X_M={g in H(C): l_n <= |g^(n)(0)| <= u_n for n>=M}.

For M>=1, l_n<u_n at every constrained coordinate. The verification initially uses n^(-1/2), which also has positive annular width for n>=1; replacing that lower sequence by l_n leaves every estimate valid. Neither this replacement nor moving a finite index affects the asymptotic polynomial obstruction.

### Clipping without illicit reapplication of Nikula

PASS. Radial clipping is applied coordinate by coordinate only after obtaining the original IID-Gaussian frequently hypercyclic sample. It preserves independence, but the clipped laws are no longer IID or full-plane supported. The verification does not reapply Nikula to those laws. Instead, upper clipping happens at finitely many indices almost surely, and lower clipping changes the nth coefficient by at most l_n tending to zero. The correction sequence delta_n therefore tends to zero and is bounded. The exponential generating series H of those corrections is entire and satisfies

    ||D^k H||_R <= exp(R) sup_{n>=k}|delta_n| -> 0.

Frequent hypercyclicity of F+H follows deterministically from visits to a smaller target neighborhood and deletion of finitely many indices. This handles all compact-open targets without a target-indexed uncountable probabilistic intersection.

### Relative support, including boundaries

PASS for M>=1. Each constrained clipped coordinate has support equal to its closed annulus. The upper and lower boundary circles are not lost: every relative neighborhood of a boundary point either contains a small interior planar patch or has a positive-probability radial preimage outside/inside the corresponding clipping radius. Early coordinates retain full-plane Gaussian support. Independence gives positive probability of matching any prescribed finite coordinate block to the required weighted tolerance.

For any target g in X_M and disk radius R, choose L>=M so that

    2 sum_{n>L} u_n R^n/n! < epsilon/2.

This bounds the entire remaining tail of the difference deterministically for every clipped sample. Positive probability for the finite head thus proves positive probability in the prescribed relative compact-open neighborhood. Measurability follows from locally uniform convergence of measurable partial sums. It follows that every such neighborhood meets the probability-one frequent-hypercyclicity event.

### M=0 guard

NONBLOCKING PRECISION CLARIFICATION. If M=0 is intended, then l_0=u_0=1. The sentence that every relative annulus neighborhood contains a nonempty planar patch is false for that coordinate alone. The conclusion nevertheless holds: radial projection of a circular Gaussian to radius 1 has the uniform angular distribution, so every nonempty relative arc of the unit circle has positive probability. A singleton angle chosen at the null event X_0=0 is immaterial. This one-coordinate replacement gives the same finite-head support proof, while all n>=1 coordinates use the ordinary annulus argument. The independent verification states M>=1, so there is no defect within its declared domain; later authors should either retain M>=1 or add this circle observation when claiming all M>=0.

### Density versus residuality

PASS. The argument gives density of frequent hypercyclic functions in each fixed X_M. Since HC(D) is a G_delta in H(C), its intersection with closed X_M is a dense G_delta there. It does not establish residual frequent hypercyclicity, and the report explicitly avoids that stronger assertion. Polynomial addition alone may leave a fixed X_M, so it is not used as the relative-density proof. Ambient density and fixed-M relative density are correctly distinguished. The union of the X_M is ambiently dense by arbitrarily late factorially small baseline tails added to polynomials.

## 3. Finer original local perturbation: do not over-subtract the contribution

PASS, with a material scope boundary to retain. Gaussian existence, Gaussian full support, and density of simultaneous bad vectors do not prove the original assertion that for each prescribed f in HC(D), fixed p, and neighborhood W, one can choose a counterexample F=f+h in W with D^n h tending to zero. That assertion asks for a bad vector in a specified affine null-orbit coset through f. Two dense sets need not intersect; ambient density cannot supply that coset intersection. The same issue persists even though the null-orbit subspace contains polynomials and its cosets are dense.

The independent report explicitly identifies this boundary in its claim list and Section4. It issues no novelty clearance for the finer property. This family's frozen report was aimed at the basic negative answer, dense failure, and simultaneous strengthening; it should not be read as certifying historical duplication of every finer local perturbation feature of the submitted root/triangular recursion. A future note may explain that direct mechanism, but should not call it new without a further bounded priority analysis of that exact refinement.

## 4. Source access, versions, and date precision

PASS. The complete primary Costakis2008, Costakis2010, and Bernal2018 PDFs are available with the same hashes as this family's independent retrievals. The receipt distinguishes whole-file retrieval, exact pages inspected, and full-proof audit. The 2010 Section6 and 2018 full-body scopes support the stated operation/quantifier distinctions. Inaccessible or uninspected 1990/1993 original growth papers, monographs, selected subscription bodies, and other forward-citation bodies remain explicit gaps. They do not negate the positive verified implication and must not be converted into an exhaustive absence claim.

The Nikula version-specific arXiv record gives a 2012 v1 submission, while the currently served PDF contains an internal2018 date. The independent report properly leaves that mismatch's cause unauthenticated and disclaims byte-identical2012 PDF authentication. The publisher record independently confirms online publication8October2013 and journal issue2014. Exact theorem numbering is assigned only to the inspected arXiv body, not the uninspected subscription journal body. Publication framing can cite the 2014 journal article and identify the inspected arXiv version separately; explaining the internal date is unnecessary.

The independent report does not backdate the later Bayart–Matheron explicit Gaussian remark to the2011 v1. Its own v1 read scope is introduction/applications and is accurately limited. My separate earlier Proposition3.3 specialization is under the other family's forward cross-challenge; this reverse check neither assumes nor strengthens their independently frozen claim. My post-freeze DOI addendum authenticates journal DOI10.1515/crelle-2014-0002 from publisher-deposited Crossref metadata, with online25February2014 and print1June2016 distinct. No earliest-theorem attribution beyond the checked version-specific route is needed for the intended note.

The 2026 coverage is explicitly bounded to the bodies/abstracts recorded in the ledgers. It is not an October2026 citation census, and the independent report does not present it as one. Later results about Phi_n(D), polynomial expressions P(f), selected algebras, coefficient-diagonal multipliers, or weighted shifts on other spaces cannot be silently treated as pointwise p(z)f results. The report's cautions about those substitutions are appropriate.

## 5. Publication framing decision

PASS for the currently proposed scope: an attributed historical negative-answer note with a self-contained elementary Baire proof and no novel discovery or earliest-priority claim. Keep these statements distinct:

1. The elementary argument gives a negative answer to the pointwise question posed in2008.
2. The basic existence/dense simultaneous conclusions can already be deduced from earlier random-function theory.
3. The first explicit publication of this polynomial-multiplier corollary has not been established.
4. The exact every-input local null-orbit refinement has not received novelty clearance from either the Gaussian implication or this cross-challenge.

Avoid claims that the problem remained open in2026, that no prior solution existed, that the new Baire argument is the first proof, that the simultaneous existence theorem is new, or that Nikula expressly wrote the polynomial-multiplier conclusion. The present comparison provides no authorization or necessity to publish; it only supports the specified attributed framing if the parent and human choose it.

## Completion

100% of the assigned reverse cross-family challenge. Own and sibling frozen bytes preserved; new findings are confined to this separate challenge and receipt. The only identified issue is the nonblocking M=0 support-phrasing guard. No substantive mathematical rejection or new historical priority claim resulted.
