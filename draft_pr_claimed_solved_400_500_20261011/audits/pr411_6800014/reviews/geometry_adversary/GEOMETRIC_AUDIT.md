# Geometric adversarial audit of PR 411 / 6800014

Verdict: **PASS for the exact counterexample claim at frozen head ac8b960bdda61c154cc30d7e3aba70389a9b139e. No required mathematical repair.**

For every fixed 0<u<1/2, the standard metric has F=1/3 and is a non-strict local maximum among all nearby left-invariant metrics on its specified simply connected solvable group. Its Ricci operator cannot equal cI+D for a derivation of that group's Lie algebra. The frozen author proof establishes this and independently survives the geometric route developed here.

## Independence and exact scope

The reviewer first read SCOPE_GATE.json and SOURCE_RECEIPT.json. A fresh read-only PR metadata and exact-head QUEUE refresh at 2026-10-13T01:10:17Z confirmed open/draft/unmerged, head ac8b960bdda61c154cc30d7e3aba70389a9b139e, Status claimed_solved, Turns 2/5. Acceptance criteria were fixed before author mathematical source reads. The independent connection, metric coverage, invariant complex-plane normal form, uniform neighborhood proof, derivation obstruction, product geometry, and sharp boundary counterexample were sealed at 2026-10-13T01:14:39Z.

A second scope refresh at 2026-10-13T01:15:10Z still matched. All 19 selected snapshot hashes were verified. Only then were the frozen author proof/scripts and historical audit read. No current parent/peer conclusions were read. The author uses the generalized zero plane; this reviewer instead used the invariant complex plane and an upper triangular covering form, then orthogonally diagonalized its traceless symmetric rotation block. This independent normal form has a quotient-coordinate singularity at r=0; the reconstruction expressly handles it without assuming a smooth quotient chart.

The exact proof, author scripts, and their current duplicates are byte-identical. All other selected packet files were read; current duplicate mathematical content was checked by byte equality. The historical audit did not substitute for the fresh reconstruction.

## Decisive geometric mechanism and attempted falsifiers

The detailed proof is in INDEPENDENT_RECONSTRUCTION.md. Its core normal form is A=[[B(r),X],[0,vN]], with B(r)=[[r,-sqrt(1+r^2)],[sqrt(1+r^2),-r]]. Every nearby metric gives a positive multiple of a nearby similarity matrix, including arbitrary complement shifts because the fixed ideal is abelian. Every nearby similarity matrix is orthogonally covered by this form. The invariant-plane choice retains all off-block coupling X; it does not assume both spectral planes are orthogonal.

Writing the columns of X as x,y, the independently computed transverse quadratic term of P=|[A,A^t]|^2-8(tr S(A)^2)^2 is

    16(2-v^2)r^2 + 2|y+vJx|^2 + 2(1-4v^2)|x|^2.

It is uniformly positive on a compact v-interval inside (0,1/2). P and its transverse gradient vanish identically on the flat family r=X=0. Continuity of the transverse Hessian, or the author's full cubic-plus remainder, gives a uniform neighborhood with P>=0, hence F<=1/3. This is the missing step that a semidefinite Hessian alone could not supply.

| Falsification target | Check and result | Exact remaining gap |
|---|---|---|
| Wrong curvature/sign | Generic 4x4 A Ricci independently derived from 5-dimensional Koszul structure constants; exact identity passes, including nonzero trace | None |
| Missing left-invariant metrics | Fixed-ideal orthonormal frame gives a h^-1 A h; complement shifts vanish in the bracket; scale leaves F fixed | None |
| Missing nonorthogonal spectral mixing | Entire upper-right 2x2 X retained; spectral projection -A^2 gives the invariant complex plane; Sylvester map removes X only for similarity, not for orthogonal metric comparison | None |
| Hidden ascent through flat directions | Compact interval in v and uniform positive transverse Hessian; author remainder independently reproduced | None |
| Solvsoliton derivation overlooked | Candidate D=Ric-cI is forced diagonal; rotation forces c=-u^2/2 and nilpotent bracket then leaves nonzero residual u^3N | None |
| Boundary overreach | At u=1/2, X=diag(a,-a/2) gives P=-a^4 and F>1/3 for every a>0; at u=0, F is undefined | Neither endpoint belongs to the claimed theorem |
| Fixed group silently changed | Every slice matrix is similar to the original; explicit metric Gram matrices are positive definite; author's larger-value B independently gives F=9/17 on the same group | None |
| Ricci soliton confused with solvsoliton | Standard line element splits as R^2 times H3; it is algebraic on the distinct nilpotent product presentation, but fails Ric-cI derivation identity on the specified solvable group | None for the printed target |

The boundary witness is particularly diagnostic. For X=diag(a,-ua), set Z=JX+XD and T=[[I,Z],[0,I]]. Then T A_u T^-1=[[J,X],[0,D]], and the fixed-group metric G_n=T^t T realizes this matrix in the frame T^-1. Its exact P is 2(1-4u^2)a^2-4u^2a^4. At u=1/2,

    F-1/3=16a^4/[3(59a^4+30a^2+3)]>0.

This falsifies endpoint extension and independently tests the higher-order danger when the quadratic form loses rank. It strengthens confidence in the strict parameter condition without changing the author theorem.

Sixty deterministic exact rational metric samples were additionally tested at u=1/10,1/4,49/100. They included ideal mixing, complement shifts, and scale, and yielded no ascent. This finite search is explicitly ancillary falsification evidence; the universal result rests on the textual neighborhood proof.

## Frozen source comparison

The author's choice W=ker A^2 and E=I+A^2 is correct. E is generally not orthogonal, but its image admits a smooth local orthonormal frame; no orthogonal-projection assumption is used. The restriction on W is nonzero rank-one nilpotent, while the quotient block has trace zero and determinant one. The lower-left coupling is unrestricted. Therefore the author's seven-parameter covering form captures all nearby conjugates.

The author quadratic completion and all terms of its exact remainder reproduce. In particular the potentially adverse quartic term -4(wx-yz)^2 remains in the formula, and compact-interval transverse positivity controls it. Its curvature, F=1/3, derivation contradiction, and same-group F=9/17 comparison all agree with independent calculations. The initial Hessian-only attempt is correctly labeled diagnostic rather than a complete local-maximum proof.

Frozen verify.py, frozen check_hessian.py, and the historical independent_checks.py each ran successfully from /tmp with Python 3.14.6 and SymPy 1.14.0. Their output is recorded in AUTHOR_REPRODUCTIONS.json. The fresh geometric script does not import them. The boundary/sample script was added after the independent reconstruction was sealed; that sequence is recorded explicitly.

## Original-source semantics and limits

The [original Morgan–Pansu TeX](https://www.imo.universite-paris-saclay.fr/~pansu/problems_MTDG.tex) was freshly fetched after the browser's TeX retrieval failed; its bytes stay private. The [PDF, Question 14, section 11, printed p.12](https://www.imo.universite-paris-saclay.fr/~pierre.pansu/problems_MTDG.pdf) independently gives the same fixed-group local-maximum target and its derivation-based definition. There is no strictness or complete-solvability restriction. The geometric proof meets that exact target.

[Lauret–Will I](https://arxiv.org/pdf/1808.01380), section 6.4, printed p.20, already displays this family D_t. The paper distinguishes local Ricci-soliton behavior from solvsoliton global maxima and leaves the small-parameter local question unresolved after Lemma 6.12. This packet's exact-family attribution and no-novelty wording are appropriate. No priority conclusion is made here. The inaccessible aggregator page, historical corpus searches, and original author's pre-freeze process accounting are not independently certified by this geometric review.

Required mathematical repairs: none. Optional exposition: the explicit product presentation and sharp boundary witness may help readers understand the solvsoliton/Ricci-soliton distinction and the parameter restriction. These are reviewer verification artifacts, not additional author proof-search turns.

Strongest verified result: the entire stated all-metrics counterexample, including its nonglobal comparison, at the exact frozen head. Remaining mathematical gap: none identified. Geometric case-review completion estimate: 100%; wider batch completion and publication decisions belong to the parent review. No source changes, Git/index/branch/remote mutations, or external communications were made.
