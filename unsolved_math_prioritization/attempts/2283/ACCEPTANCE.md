# Acceptance report: prior EP730 solution

## Exact disposition

ACCEPT the complete conventional proof of the original infinitude question, relative to classical Kummer, reciprocal-prime Mertens, and the prime number theorem in fixed arithmetic progressions. No unresolved mathematical gap was found in the reviewed argument. This disposition concerns the prior result, not a new proof or novelty claim.

For T=5289=3·41·43, set

    P(x)=42Tx+11, Q(x)=72Tx+13,
    R(x)=28Tx+5, S(x)=72Tx+19,
    n(x)=P(x)Q(x)−1=84591927504x²+7076682x+142.

The lower asymptotic density of positive integer x for which n(x),n(x)+1 have identical central-binomial prime supports is strictly greater than 107/2500. It is not a density assertion about n. Positivity, strict increase and injectivity of this family yield infinitely many distinct positive consecutive pairs, hence the original statement with positive n<m. Equality of supports is not equality of valuations or of the coefficients.

## Load-bearing steps retained

AUDIT.md preserves the exact Kummer transition criterion, 2PQ−1=3RS and all resultant exclusions, exact valuations, p-adic permutation and endpoint deletion, higher-power dominated convergence, transition range, fixed-depth Fourier normalization and Gauss completion, fixed-depth summation and a separate uniform tail, all top-range cofactor restrictions, paper divisor-switching and current AP-prime-reciprocal routes, final strict rational density budget and original-statement bridge.

The final quantities are

    S = sum_{r>=1}4^(−r) log((r+2)/(r+1)),
    S < 11117760449158646497/89848527388139520000,
    log 2 < 1123/1620,
    4S+(2/3)log 2 < 21498408212212214497/22462131847034880000,
    2393/2500 − 21498408212212214497/22462131847034880000
      = 2344391769572639/22462131847034880000 > 0.

These are general analytic proof constants, not empirical samples. They give limsup Bad(X)/X <2393/2500 and therefore lower density Good >107/2500.

The independent focused report accepts the exact discrepancy constant (2r+3)3^(2r), for ordinary non-wrapping digit intervals, exactly p^r consecutive inputs, integral phase pαt²+βt+γ and p∤αβ. The conclusion o_r(p^r) fixes r before p tends to infinity. Its application is only a=1. Growing depths, including the exceptional p=7, are handled by the separate elementary permutation tail. No hidden uniform-in-r Fourier conclusion is used. The focused review is not a second audit of unrelated sections.

## Attribution and source status

The author's public manifest credits Liam Price's informal idea, Tomodovodoo's algebraic follow-up, and Will Blair's analytic reconstruction/formalization. It describes review as self-assessed and the earlier informal argument as unadjudicated. This report preserves that limited attribution; it neither authenticates unavailable antecedent material nor settles priority. The reviewed public source is pinned at f297d710018270c66b296082766334974260bcbc. Citations and selected identities are in SOURCES.json.

## Formal and registry boundaries

Formal replay: NOT REPRODUCED. The terminal source declares the correct unconditional theorem and positive-density bridge, but no local kernel replay or elaborated transitive axiom computation was performed. Lean, Lake, author scripts and imported third-party programs were not executed.

The actual resolved dependency is ajirving/PrimeNumberTheoremAnd at 769d3b81fbff001d9fa7028df0168a8e546cf692, Lean v4.33.0 and Mathlib db584cd6d46c92f209a44c0f1c829460d327499d. Older documentation names a different repository/revision and 4.29.x environment. Current terminal AP moduli are 1,7,14, not the older exact list 1,222138,148092; the generic fixed-modulus theorem covers them. The implementation's relaxed full lower-half box is a valid enlargement with the same fixed-depth limiting mass.

The bounded project-specific import graph contains two admitted experimental declarations. Their presence in imported modules is not by itself a terminal proof dependency. Inspected source references support exclusion from the terminal dependency cone, but automatic elaboration, implicit/generated terms and the full Lean/Mathlib/Batteries boundary were not kernel-checked. A definitive formal acceptance requires a clean exact-pin replay and terminal axiom inspection.

Palomar acceptance: UNVERIFIED. The inherited record/version endpoints returned HTTP 403; the denial was respected, without an alternate-route bypass. An author's registry identifier is not independent acceptance.

## Nature of review

This is unrefereed internal AI mathematical review. It claims neither external human peer review nor journal acceptance, exhaustive novelty search, current tracker status or community-wide adjudication. Historical independently authored finite checks were diagnostics, not proof by extrapolation. This prose/metadata edition omits their code and raw certificates, while preserving all general derivations. Publication preparation checks exact editorial scope, byte identity and an addition-only plan; it does not execute third-party source programs.
