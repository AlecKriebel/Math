# Sealed independent baseline for PR 374 / problem 30005116

Timestamp: 2026-10-03T07:46:00Z. Audit completion estimate 25%; cograph-proof discovery/verification estimate 25%; unrestricted discovery estimate 0%. No candidate, author verifier, prior review, sibling reviewer, or root research artifact has been read. Only the supplied frozen identity and primary URLs, workspace path/ignore check, current time, and my own controls were used.

## Source scope and exact unrestricted claim

Fresh primary read: OWR 22/2022, printed pp. 1227–1228, Mubayi Problem 10 / Conjecture 11 / Theorem 12; Liu–Mubayi–Reiher (LMR), definitions on printed pp. 1–2, Construction 1.9 on pp. 5–6, C4 results on p. 10, Proposition 6.1 and Theorem 6.2 on p. 22; Coudert–Coulomb–Ducoffe, Section 6.2 on printed p. 18, recursive cograph definition only. I do not require or use its P4-free equivalence assertion. Web PDF extraction and local downloaded PDF extraction were used, with page screenshots also requested. No secondary theorem statement was consulted.

Let e(G)=|E(G)|/binom(n,2), c(G)=N_ind(C4,G)/binom(n,4). For each fixed xi in (1/2,1), the unrestricted hypothesis is that the supremum of limit c(G_n), over every sequence of finite graphs with n→∞ and e(G_n)→xi, equals the density of Construction 1.9. For xi=1, that density is zero. For 1/2<xi<1 choose k with xi in [(k−2)/(k−1),(k−1)/k]. Put a=(1+sqrt(1−k xi/(k−1)))/k and b=1−(k−1)a. The predicted density is 6[binom(k−1,2)a^4+(k−1)a²b²]. All graphs are permitted; a cograph theorem alone cannot prove this hypothesis. The LMR PDF at this URL calls the corresponding statement Conjecture 1.17 and the coarse high-density bound Theorem 1.18; the OWR reference uses different numbering. This is a source-version discrepancy, not an invitation to identify unlike statements.

The source-certified coarse bound is I(C4,xi)≤3 xi(1−xi)² for xi≥1/2, with sharp endpoints xi=1−1/k. The sparse exact value is 3xi²/2 for xi≤1/2. These sourced results are separate from my deductions below.

## Independent recursions

A finite weighted cotree has leaves representing complete or empty positive-measure blocks, nonnegative child masses w_i summing to one, and internal nodes representing disjoint union or complete join. Let child densities be e_i,c_i and q_i=1−e_i. Empty leaves give (e,c)=(0,0); complete leaves give (1,0). Zero-mass children may be removed.

At union: e=Σw_i²e_i and c=Σw_i⁴c_i. At join: e=1−Σw_i²q_i and c=Σw_i⁴c_i+6Σ_{i<j}w_i²w_j²q_iq_j. Reason: an induced C4 crossing a join has exactly two vertices in each of exactly two children, with each pair internally nonadjacent. A 3+1 split would give the singleton degree three; three or four occupied children force a triangle. At union a connected C4 must stay in one child.

Set z=c/3 and R=q²−z. At join, q=Σw_i²q_i and R=Σw_i⁴(q_i²−z_i). This coupled quantity is the key obstruction: maximizing each c_i without maintaining its q_i cannot validate a universal join bound. At union, q=1−Σw_i²e_i and R=q²−Σw_i⁴z_i. The recursion is valid at arbitrary finite depth, by induction, with no depth-dependent approximation.

A complete multipartite model with empty part weights p_i has q=Σp_i² and z=q²−Σp_i⁴. The target envelope therefore reduces within that family to minimizing Σp_i⁴ subject to Σp_i=1, Σp_i²=q. The above (k−1)a,b vector is the natural proposed minimizer, but this baseline has not proved the global moment optimization or its sufficiency for unions.

Two independent coarse checks, valid even for unrestricted graphons: c≤3e²/2 (each induced C4 realizes two of the three pairings as an edge matching), and c≤3q² (each induced C4 realizes one of the three pairings as its two nonedges). These bounds alone do not imply the claimed high-density envelope. A possible inductive route must prove both a join coupled inequality for q_i²−z_i and a union inequality at fixed Σw_i²e_i; replacing either by an unsupported universal optimization only transfers the difficulty.

## Controls sealed before candidate access

`independent_controls.py` was written from the recursions and directly enumerates every ordered four-tuple of weighted leaf indices, with repetitions permitted and with complete/empty diagonal states. It compares these exact rational probabilities with recursion on 210 seeded random cotrees having 1–7 leaves, both leaf types, zero child weights, and varied finite depth. All comparisons pass. Balanced complete multipartite endpoint equalities are checked for k=2,...,12; unbalanced bipartite equalities c=3e²/2 include zero-mass endpoints. This checks formulas and normalization only, not universal extremality.

The initial wrapper executed the control but failed when assigning the reserved zsh variable `status`. Exact error was `zsh:85: read-only variable: status`. Initial code and stdout/stderr are retained unchanged in ignored tmp; a wrapper replay with `audit_control_status` returned zero, and its stdout was byte-identical. No mathematical control was changed. PDF extraction emitted nonfatal marked-content warnings for LMR; downloaded bytes and extracted source inputs remain private under ignored tmp.

Raw source identities (all excluded from public allowlist): OWR SHA256 b94a5ab624e47ddb3db11370099db7ef4bf30acfc2f0993d5c365c2795ff6d79; LMR SHA256 f9b7951b9926ffba50a886226fbe0ab4715cfdccffaf5c92e00f8eee783a270c; DMTCS SHA256 60225bbd9266276d6a0ffd852f9f218fea0e963c95341a57b4bb6b7349100b6d. Ignore check: the effort `.gitignore` line 4 `**/tmp/` matches this review's `tmp/input.pdf`.
