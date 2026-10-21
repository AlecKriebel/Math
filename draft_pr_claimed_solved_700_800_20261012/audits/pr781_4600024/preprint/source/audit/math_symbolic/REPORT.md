# Symbolic-dynamics adversarial audit

**Verdict: no substantive mathematical defect found in this family.** The claimed prescribed-map criterion survives this independent audit, conditional only on the explicitly imported published PRZ theorem. No repair or fresh proof turn is required for this family's conclusion. Novelty and the present literature status are not certified.

Custody code: **PR781-SYMBOLIC-4A38C3C-20261016**. Eligible record: draft PR781; problem4600024; queue claimed_solved3/5; immutable head4a38c3ccc4cac918fb75fd4b97449f3ebd2e0f7f. Input digests are fixed in INITIAL_ASSESSMENT.json, recorded before primary-source work and before any historical audit material. No historical audit, sibling report, or root conclusion was read. No other PR was audited. No Git actions or external communications occurred.

## Claim and success criteria

For a nonempty two-sided mixing sofic shift T over a finite alphabet and a specified onto sliding block map f:T→T, decide whether f extends to a block map S→T for an SFT S containing T. The submitted criterion constructs a common recognizing monoid M for L(T) and the fixed completion's bad-word ideal B, sets N=max(2,ell,4(|M|+1)), and tests L(T[N])∩B=empty. Success requires equivalence with arbitrary ambient SFTs and arbitrary extension radii/completions, exact finite-word recognition including short words, and a justified finite bound. Merely passing finite examples would not suffice.

The proof's weaker irreducibility hypothesis is also valid. Its surjectivity hypothesis is needed for the stated image equality F(T[N])=T, rather than for the existence/inclusion reduction. Nonemptiness, two-sidedness, regular language, and irreducibility are retained throughout this audit.

## Primary sources checked

[Boyle2008, Problem16.3, printed p17/PDF page17](https://www.math.umd.edu/~mboyle/papers/openfinalsub3nov2007.pdf) asks for an SFT containing the mixing sofic T on which the specified surjective self-code maps into T. The receptive-fixed-point and existential-over-f conditions belong to preceding Problem16.2, not16.3. “Containing” permits equality. PDF response body: SHA256 f2ce824a2dad5da1422042c5de32c40228990a5d8ded2ebafd8f86d27b6dddb7; 448803bytes.

[PRZ2014, Theorem4.2, printed pp8–9](https://lmcs.episciences.org/1163/pdf) gives the precise implication used: LT separation of regular languages recognized by a common finite monoid M implies LT[k] separation with k=4(|M|+1). The profiles are defined on printed p4, at positions0,…,|w|-1, with left size floor(k/2), right size ceil(k/2), truncated at word boundaries. Printed p6 defines LT[k] by presence/absence of these profiles, i.e. counting threshold1. The also-mentioned common NFA is always constructible and does not strengthen the hypotheses. PDF response body: SHA256 0031cabde0d3f0878efad9d992470cef3b0a9ad5834bf1c48d99a0724b5eb424; 402377bytes. Retrieval metadata is in SOURCE_CUSTODY.json. No third-party PDF is stored in this package.

## Adversarial findings

| Challenge | Mechanism and evidence | Status / exact gap |
|---|---|---|
| Larger ambient alphabet and SFT | Intersect with A^Z; add finitely many one-letter exclusions. Canonical approximations enter every SFT neighborhood of T. | Verified; no gap. |
| Different radius or completion | Union the two windows; local agreement on T becomes agreement on every sufficiently large T[n]. | Verified; no gap. |
| Mixing versus irreducibility | Canonical overlap graph is strongly connected from word irreducibility; aperiodicity is unused. Period-two alternating-shift controls pass. | Verified under irreducibility; reducible extension not claimed. |
| Short words and automaton labels | L(T[n]) agrees with L(T) below n; appended-edge labels work because each finite path extends bi-infinitely. Vacuous n-factor tests alone fail for unused symbols. | Verified; no implementation defect found. |
| Saturation and all-n claim | Join a universal n-word U around an arbitrary bad word inside T[n], and join U to U inside T. Compare profiles using saturated factors and common boundaries. | Independent derivation proves every n≥max(2,k), no finite extrapolation. |
| Inclusion versus equality | Onto restriction gives T=f(T)⊆F(T[n]); target inclusion gives equality. Constant even-shift map shows equality fails when onto is removed. | Verified with exact hypothesis boundary. |
| Identity even-shift obstruction | Odd gaps give arbitrarily long minimal forbidden words; inverse composition shows an automorphism extension forces T SFT. | Verified for every n, including larger radius/completion escape attempts. |
| External bound | Actual primary Theorem4.2 matches the supplied k and profile convention. | Verified statement/application; general published proof not independently reproved. |
| Executable evidence | Original code passes; separately written checks import no original code and exercise graph languages, profiles, exact output reachability, and controls. | Finite evidence only; full criterion remains supported by the proof. |

## Reproducibility and limits

Run `python3 -I -B independent_checks.py` in this folder: **117708 checks PASS**, including all144 strongly connected binary-labelled two-vertex edge presentations, three approximation orders2–4, input words through length7, 957 factor/boundary signature classes, 80 exact width-two rule/domain cases, and even-shift saturation controls for n2–8 and every k≤n. The original verification separately reports **3456 checks PASS**, including768 rule/domain cases. Captured outputs and source digests are included. The finite controls do not compute the universal bound for arbitrary inputs or replace the infinite argument.

DERIVATION.md supplies the checkable independent logical chain and boundary reasoning. The strongest verified result of this family is the stated finite criterion under the stated hypotheses, using PRZ4.2 as a published external dependency. The exact remaining gap within this family is **none identified**. Broader novelty, a complete arbitrary-input software implementation, and other research problems remain outside scope. No unfinished repair search was started. Audit completion estimate:100% toward independently verifying/falsifying this assigned family, not a claim that all research on the problem is complete.
