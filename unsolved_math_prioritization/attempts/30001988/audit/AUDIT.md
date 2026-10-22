# Independent adversarial audit: rank 654 / 30001988

## Verdict

**PASS as an unsolved, five-approach partial-results packet.** The proposition that `(delta Y - a z, 1)` is constrained over `K<z>` exactly when `a != 0` is correct under the stated hypotheses: one derivation, characteristic zero, `a in K`, and `z` differentially transcendental over `K`. The closed-base specialization counterexample is also correct. No proof or counterexample for the unrestricted target is supplied, and the packet correctly retains **unsolved**. No novelty claim is certified.

No mandatory mathematical correction was found. One nonblocking wording clarification is recorded below: specialization is evaluation of this pair's polynomial coefficient formulas, not a homomorphism on the entire rational-function field.

The frozen object audited is `SHA256SUMS.json` with SHA-256
`767185ee51afce74a4227eb090aa4e896503ddbf186cc236e5deedadb4b51ab2`.
Its exact inventory consists of eleven authored files in addition to that manifest. The manifest hash, all eleven file sizes and hashes, script results, and unchanged original bytes were checked independently. This audit makes no remote changes.

## 1. Definition and target

The [official 2012 report](https://ems.press/content/serial-article-files/46379), printed p. 441 / PDF p. 45, identifies Conjecture 5 without either later base-field restriction. Its preceding explanatory separation sentence is inconsistent with its isomorphism interpretation, including when the two roots coincide. The packet's correction is necessary and appropriate; the typography was visually checked.

[Definition 4.3 in the 2014 paper](https://arxiv.org/pdf/1208.1152v2#page=12) supplies the consistent definition: satisfying roots generate isomorphic differential extensions with the roots matched. The paper uses the complement convention, and its printed overbars matter. Theorem 6.1 adds nontrivial derivation for algebraic-dependence computation. Theorem 8.6 assumes nontrivial derivation. Theorem 9.6 requires a nonconstant ordinary base and a nonalgebraic differential closure, plus the effective presentation condition. These hypotheses were checked against the primary PDF, including visual inspection of Definition 4.3 and Theorem 9.6. The packet does not silently remove them.

Replacing an oracle set by its complement preserves Turing degree. The packet's `C_E` and `T_E` conventions are therefore harmless and explicit. For the audited pair, all admissibility conditions are immediate: the first member is monic, algebraically irreducible and order one; the nonzero second member has order minus one.

## 2. Independent proof of the central result

This section supplies an independent verification, with a coefficient argument in place of the packet's trace proof.

### A. General first-order criterion

Let `E` be any ordinary characteristic-zero differential field and `b in E`. Then

`(delta Y - b, 1) is constrained over E iff b is not in delta(E)`.

If `b = delta(r)` for some `r in E`, the roots `r` and `r+1` are separated by the differential polynomial `Y-r`. Thus the pair is unconstrained.

Conversely, assume `b` has no primitive in `E`. An algebraic solution `y` would have a monic minimal polynomial

`f(X) = X^n + c_(n-1) X^(n-1) + ... + c_0`.

Differentiating `f(y)=0` and using `delta(y)=b` gives

`f^delta(y) + b f'(y) = 0`,

where `f^delta` differentiates coefficients only. This polynomial has degree at most `n-1`. Minimality of `f` forces it to be identically zero. Its coefficient of `X^(n-1)` is `delta(c_(n-1)) + n b`, giving the forbidden primitive `-c_(n-1)/n` in `E`. This also checks independently the normalized-trace step in the packet.

A solution exists in the differential rational-function field `E(s)` defined by `delta(s)=b`. Every solution is algebraically transcendental over `E`, by the preceding paragraph. In any differential polynomial `h(Y)`, replace `delta^j Y` for `j >= 1` by `delta^(j-1)b`. The resulting ordinary polynomial `H(Y) in E[Y]` is independent of the chosen solution, and `h(y)=0` holds precisely when `H` is identically zero. Every solution therefore has the same differential polynomial relations. This proves constrainedness over all differential extensions, rather than just one chosen closure.

### B. Application to the differential indeterminate

Put `F = K(z_0,z_1,...)` with independent jets and `delta(z_i)=z_(i+1)`. Let `a in K` be nonzero. If `r in K`, then `delta(r)` cannot equal `a z_0`. Otherwise choose the largest jet `z_m` genuinely occurring in `r`. The expression

`delta(r) = delta_K(r) + sum_i (partial r / partial z_i) z_(i+1)`

is affine in the new independent variable `z_(m+1)`, with coefficient `partial r / partial z_m`. The other terms and the right side `a z_0` do not involve this variable. Equality would force that coefficient to vanish.

For completeness, in a rational-function field `B(x)` of characteristic zero, `d(A/B)/dx=0` for coprime polynomial numerator and denominator implies `A'B-AB'=0`. Coprimality and the degree drop force each nonconstant numerator or denominator to have zero derivative, which is impossible in characteristic zero. Thus the derivative kernel is exactly the coefficient field. Applied with coefficient field `K(z_0,...,z_(m-1))`, this contradicts genuine dependence on `z_m`. It also handles `m=0`.

There is no primitive for `a z_0`; criterion A proves constrainedness. When `a=0`, roots 0 and 1 separate. No assumption that `a` is constant under the derivation was used. In particular, the proof is valid over both constant and differentially closed bases. For a computable base, deciding this family requires only deciding whether `a=0`.

## 3. Specialization and omitted scope

If `K` is differentially closed and `c in K`, differential closedness gives `r in K` with `delta(r)=c`. Criterion A then shows `(delta Y-c,1)` is unconstrained, while `(delta Y-z,1)` over `K<z>` is constrained. Hence every base-field evaluation of this particular coefficient formula destroys constrainedness.

**Wording clarification:** there is no `K`-field homomorphism from all of `K<z>` to `K` sending `z` to `c`, because the nonzero element `z-c` is invertible in the source. The valid specialization is the differential evaluation on `K{z}`, or a suitable coefficient subring/localization. The audited pair has no coefficient denominators, so evaluation is defined for every `c`, and the claimed counterexample is unaffected.

The example refutes an unrestricted specialization-preservation shortcut. It does not refute the desired Turing reduction. Likewise, when `Khat/K` is algebraic, every element of `Khat` satisfies an order-zero polynomial over `K`, so a search there for arbitrarily high differential orders cannot work. A new method may still establish the target.

The restriction to characteristic zero is substantive. In characteristic `p`, take the constant field `K = F_p(u)` and the differential rational-jet field `F=K<z>`. The polynomial `X^p-u` is irreducible over `F` since `u` is not a `p`th power. In `F(y)` with `y^p=u`, define `delta(y)=z`; the relation is preserved because its derivative is zero. Both `y` and `y+1` solve `delta Y=z`, but `Y^p-u` separates them. Thus the classification cannot be exported unchanged to positive characteristic.

Two other boundary attacks also show why the hypotheses must stay:

- If `a` were allowed in `F`, choose `a=z_1/z_0`. Then `a z_0 = delta(z_0)`, and roots `z_0`, `z_0+1` make the pair unconstrained despite `a != 0`.
- Ordinary algebraic transcendence is insufficient. Over `K=Q(t)` with `delta(t)=1`, adjoin an algebraically transcendental constant `c`. Then `delta(t c)=c`, so the corresponding nonzero linear pair is unconstrained. Such a `c` is not a differential indeterminate.

No claim for several derivations is made or audited.

## 4. Other mathematical claims

The canonical rational-jet presentation is effective under the specified computable embedding and differential-transcendence promise. Rational expressions use finitely many independent jets, so equality and derivation are effective. Searching for an expression for an ambient element terminates only when that element is promised to be in the generated field. The packet states this distinction correctly.

Ordinary factorization over the finite rational-function field can be reduced to base-field factorization, and additional independent variables preserve irreducibility. This does not supply the missing isolation test. The example `delta Y` and roots 0,1 correctly separates algebraic irreducibility from constrainedness.

[Pogudin's primitive-element theorem](https://arxiv.org/pdf/1409.3847v3#page=2) has the finite generation, finite ordinary transcendence degree, and nonconstant-in-the-extension hypotheses stated by the packet. Searching for a generator and finitely many rational differential recovery expressions is effective in a computable presentation once existence guarantees termination. It is not an effective order bound or a constraint-set reduction.

For the all-constant alternative, the packet's proof is valid. If a constant `c` transcendental over constant `K` satisfies a constrained pair, derivative specialization makes `p(Y,0,...)` identically zero and `q(Y,0,...)` nonzero. An element of the infinite field `K` avoiding the finitely many roots of the latter polynomial supplies a separated root. Thus constrained constants are algebraic, and a finite extension generated by them admits an ordinary primitive element in characteristic zero. Adjoining `t` with `delta(t)=1` in the differential closure is legitimate; subsequently allowing coefficients in `t` without eliminating them would not be legitimate. The packet correctly refuses that step.

For each fixed separating polynomial, quantifier elimination over a computable base diagram decides the relevant existential formula. Enumerating all candidate separating polynomials only semidecides failure of isolation. The prime differential ideal `[delta Y]` has proper differential specializations such as `[Y]`, so primality alone does not certify isolation. These observations support the fourth approach's stopping point.

The [2023 Miller preprint](https://arxiv.org/pdf/2301.05769v1#page=13) recalls the earlier theorem; its short parenthetical does not give a new proof removing the original hypotheses. Its inspected arXiv metadata lists no journal reference. The audit found no complete resolution in its bounded source checks; that is not an exhaustive literature assertion.

## 5. Replay and independent controls

The original scripts were read before execution. Normal Python execution reproduced the recorded 1,404 rational-function controls and four derivative identities, together with the status/approach guards. All eleven manifest entries verified. Three mutation tests in disposable copies were rejected: changed proof bytes, a missing file, and an unexpected file. Original packet bytes were rehashed after the replay and remained identical. Do not run the author's assertion-based scripts with Python's `-O` option.

A separate SymPy implementation over exact arithmetic passed:

- 500 rational-function nonprimitive controls over `Q(t)` with `delta(t)=1`, coefficient cases `1,-1,t,t^2+1,1/(t+1)`, and jets through `z_4`;
- 100 highest-jet coefficient identities;
- three inconsistent polynomial-primitive ansatz systems, each using all 21 monomials of total degree at most two in `t,z_0,...,z_3`;
- eight positive derivative controls and two nonconstant-coefficient Leibniz checks;
- two scope-boundary counterexample identities, four root-translation/separation controls, and four characteristic-`p` consistency controls.

These finite computations are regression controls and adversarial sanity checks. Neither implementation decides constrainedness for arbitrary pairs, proves the universal theorem by enumeration, or substitutes for the proofs above. Their exact results are in `REPLAY_RESULTS.json` and `INDEPENDENT_RESULTS.json`.

## 6. Source and identity verification

All four primary PDFs were freshly retrieved from their pinned public URLs, and every byte count and SHA-256 matched the author manifest. The report, definition, theorem statements, dependency locations, primitive-element hypotheses, and later summary were inspected. Four pertinent pages were visually inspected; private source bytes and rendered pages are excluded from this audit.

Independently parsed existing public-corpus copies matched both declared hashes and sizes. The problems corpus had one numeric-ID match, one problem-code match, and one whitespace-normalized statement match, all for this ID. The research dictionary had neither the problem-code key nor a numeric-ID/title match. No corpus text or record is included in the audit. The dataset revision label is inherited from the packet; this audit did not re-download the large corpora to establish its remote revision binding.

The catalogue page remained inaccessible through web retrieval. The original source and hash-matching corpus therefore establish identity. The packet's repository observations are historical metadata. This audit does not independently refresh live repository state, PR duplicates, or publication permissions; the publisher must perform its normal fresh gate.

`SOURCE_VERIFICATION.json` contains only public metadata, match results, and inspection history. No scholarly source text, PDFs, datasets, credentials, or coordination records are included.

## 7. Disposition and reproducibility

The five entries cover distinct mechanisms: ordinary splitting, high-order specialization, primitive-element repair, quantifier elimination/ideal certificates, and linear-family/undecidability testing. Their artifacts substantiate five distinct approach families, not an independently measurable amount of time or an assertion that every mathematical possibility is exhausted. Their numerical completion estimates remain subjective research estimates.

Accept the packet as **unsolved, 5/5, verified partial results**. Do not promote it to a solved target or claim novelty. No full-target algorithm, noncomputable counterexample, complete constant-base oracle transfer, or resolution of the differentially closed-base case is present.

With the audit folder next to the frozen packet, run:

```
python3 -B audit/verify_audit.py
python3 -B audit/replay_packet.py
python3 -B audit/independent_controls.py
```

Only the last command needs SymPy; its tested dependency is pinned in `requirements.txt`. Both verification scripts also accept an explicit packet directory as their first argument. The binding manifest records the original packet manifest and every audit file except its own bytes. A separately reported SHA-256 authenticates that binding manifest. All paths inside the binding manifest are relative and portable.
