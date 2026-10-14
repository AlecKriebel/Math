# Completed PASS3 concentration-audit receipt

14 October 2026. Problem row1778 /30005770. The audit is complete within the shared third pass. No additional mathematical pass was opened. No novelty or human peer-review claim is made.

## Overall disposition

The universal fixed-alpha weak diagonal-permuton target and the uniform1324 anti-diagonal case remain unresolved. This pass proves actual-kernel method obstructions and new partial concentration estimates at arbitrary staircase indices. It does not substitute a deterministic example or an abstract tree for the exact uniform avoidance law.

All reviewer-authored mathematical additions have complementary independent acceptance. Earlier accepted proof files and receipts remain unchanged.

## 1. Actual squared-kernel obstruction: accepted

`TWO_SHUFFLE_BOUND.md`, 9407 bytes, SHA-256 `86c292c667305a12943e5b7321171b3660770cb6ff0da228811d254201e07754`, proves

    a_n <= S_(n+2), n>=1, and hence beta>=lambda.

The two raw parity flattenings have reversed state orientations, not identical orientations. A separate two-point padding supplies the exact greedy witness. Single-cell terms occupy disjoint second-state-size-one slots. The proof does not infer a radius from finite coefficients.

Complementary full acceptance: `pass3_bijection_audit/TWO_POINT_PADDING_ACCEPTANCE.md`, SHA-256 `b269f2e825bc1f861fa9ee3e9da8faecebb556042a2aebbe4ccfe6d95bd6063a`; receipt SHA-256 `26873018cea95cfe16396aa125612c61354d68902808a4953c2438f8f5e91eac`.

The separate author certificate `pass3_kernel_feasibility/SQUARED_KERNEL_GAP_IMPOSSIBLE.md`, SHA-256 `99e3262041ff09e1ce308fbc5a13704d286602e0eb5af7d814d99915848c314f`, also proves the reciprocal bound a_n<=T_(n+4), including n=0. Its symmetric guard preserves the reciprocal factors needed below. Its structural acceptance is pinned in the complementary domino receipt.

Thus the PASS2 sufficient hypothesis beta<lambda is impossible for this exact kernel. The conditional theorem itself remains valid. No weak-limit counterexample follows.

## 2. Weighted operators and the common first-cell mark: accepted

Reviewed proof: `pass3_kernel_bounds/WEIGHTED_OPERATOR_BOUNDARY.md`, 8398 bytes, SHA-256 `b4b2057622a189442bcff813648db124642862ce65f3805bc843bc25550d9597`.

Detailed audit: `OPERATOR_AND_MARK_ACCEPTANCE.md`, 5834 bytes, SHA-256 `84bc9b08c06db02a000305be867e3985f51efadf8cd1bb245811e20ab08ec4a2`.

Accepted conclusions:

- Every finite positive diagonal entrywise reweighting fails to be Hilbert–Schmidt at every real z>rho. Reciprocal AM–GM cancels the diagonal factors, giving a lower bound z^4 F(z). No unbounded similarity operator or boundary value at rho is assumed.
- For every eta<gamma=log C(1/lambda), absolute frontier counts satisfy N_n(m)<=C_eta lambda^n exp(-eta m), uniformly in both parameters. This includes lambda=4.
- For each fixed1<u<C(1/lambda), the outgoing first-cell mark sum_A u^|A|z^|A|h_A(z) is finite for every z<rho. The omitted incoming factor ell_A is still essential for arbitrary cells.
- Explicit weighted-sup spaces give subcritical outgoing and incoming contractions. These statements assume neither compactness nor irreducibility and do not establish two-sided exponential smoothing.

## 3. Isolated blocks and a fixed largest-cell fraction: accepted

Reviewed proofs:

- `pass3_kernel_feasibility/ISOLATED_BLOCK_TAIL.md`, 5854 bytes, SHA-256 `f61fde65b505d884a7bf9f9432edf5d937f5009a8168246f67052484890d7fdd`.
- `pass3_kernel_feasibility/LARGEST_CELL_FRACTION_COROLLARY.md`, 855 bytes, SHA-256 `902f69a9507145701bc15686c15152c6cb4423e678cb99f5d2d25c51d1fa016a`.

Detailed analytic and finite-count audit: `ISOLATED_BLOCK_ACCEPTANCE.md`, 5760 bytes, SHA-256 `eeed79a14d87f9c45b8e49712b6f01ba64a11ddc110a7489415f76f4e7041a0c`. Complementary structural receipt: SHA-256 `8fec619a832024195d248e660e47bc6d7c5a7987d6c8c7a480d797ecea06b76b`.

For fixed K, put g_K=limsup b_(m,K)^(1/m)<lambda and

    Phi(delta)=(2+delta)log(2+delta)-2log2-delta log delta.

A consecutive block of at most K canonical cells, at any index, with mass at least epsilon n and two-neighbor mass at most delta times its own mass has logarithmic probability rate at most

    -epsilon[log(lambda/g_K)-Phi(delta)]

whenever the bracket is positive. The three exact path-piece counts retain both exterior completion weights; the uniform error over all masses at least epsilon n is justified. K remains fixed.

For K=1, g_1=4<lambda. Choose delta>0 with Phi(delta)<log(lambda/4) and set c=1/(1+delta)<1. Then the largest-cell event max c_j>=cn has rate at most

    -c[log(lambda/4)-Phi(delta)]<0.

This proves some fixed fraction below one, not sublinearity or all positive thresholds.

## 4. One-point rerooting: accepted with complementary full review

Final proof: `REROOTING_ONE_POINT_BOUND.md`, 10256 bytes, SHA-256 `41336ca4027b4c0c40928e3df4df0e70ec107043d78f64f799d404017c8870b5`.

The proof uses the direct ascent bridge. It stores the removed incoming shuffle rather than losing its multiplicity. The exact marked-pair bounds are

    (n+1)binom(n,p_0) B_(n+1)(m),
    Z_n(a,b)<=(n+1)binom(a+b,b) B_(n+1)(a).

The first yields rate h(delta)-epsilon gamma for any-index large cells with predecessor at most delta n. The second, using the uniform absolute frontier coefficients, yields rate

    -epsilon[gamma-f(c)],
    f(c)=(1+c)log(1+c)-c log c,

for a cell of size at least epsilon n with predecessor at most c times its own size, whenever f(c)<gamma. The finite-class size ratio and the uniform sum over all eligible a,b are both retained.

Structural acceptance: `pass3_bijection_audit/REROOTING_STRUCTURAL_ACCEPTANCE.md`, SHA-256 `7a215c50e4f4c0028ea891d6f68d5b7eeb3cd7b16cfdbd49e3902eee9526e0cd`.

Independent full probability acceptance: `pass3_kernel_bounds/REROOTING_INDEPENDENT_ACCEPTANCE.md`, SHA-256 `1378d336fff040287170110980d89e17597839a7fee3cb41c3f05f289e57230b`.

The earlier `REROOTING_LOCAL_BOUND.md` is an explicitly superseded provisional three-point version and is excluded from the final authored deliverable manifest. The accepted final result is the one-point version above.

## 5. Graded-profile limitation and exact remaining scope

The actual canonical increasing-cell family in `pass3_kernel_bounds/GRADED_CELL_OBSTRUCTION.md`, SHA-256 `e7f64b750aa2671a0bc64b5269e86572f7cd7333339aefbae7e8e82203aa2d81`, is independently accepted in the complementary geometry report, SHA-256 `62c1ace80887b963c30a16ceb916f5af61912227855fc33842f3fe61ef1bca77`. I also checked its entropy-cone and increasing-pair continuity calculations.

This deterministic family shows that the fixed-prefix and one-predecessor conclusions alone cannot force sublinearity or the anti-diagonal shape. It is not a uniform-probability counterexample, and it does not claim compatibility with every stronger isolated-block bound. Those hypotheses must be assessed separately.

The remaining gap is control of more general macroscopic profiles or the exact two-sided marked-cell weight. The accepted results do not justify growing K, discard ell_A, infer a conditional uniform law, assume compactness, or identify weak convergence with maximum displacement or total variation. Largest-cell sublinearity remains a sufficient, not necessary, route to the weak limit.

## 6. Verification and preservation

`CROSS_REVIEW_PINS.json` records the complementary proof acceptances. `FINAL_CHECKER_RECEIPT.json` records matching normal/-O/-OO outputs and their precise provenance.

Our independent parity/padding checker ran in all three modes through size7, testing2785 two-shuffle images,625 single-cell cases and10831 raw-shuffle padding maps. The supplied isolated-block reports compare360 inequalities and159069 marked objects through size8. The supplied operator/graded reports also match in all three modes. No finite check is used as an asymptotic argument.

All files listed in the previous PASS2 concentration-audit manifest were verified unchanged. PASS1 files were not edited. 
