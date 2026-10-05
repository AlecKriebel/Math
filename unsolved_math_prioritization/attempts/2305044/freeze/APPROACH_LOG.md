# Research and approach log

All times UTC, 2026-10-05. The investigation is one combined substantive proof-attempt response with several approach families, not one turn per tool call. The live starting row was queued, 0/5. No remote queue, repository, or state write was made. A suggested accounting record is in TURN_LEDGER.json; it does not pretend that queue.py was executed.

## 06:34–06:37 — Source gate and prior-work checks

The numeric UnsolvedMath URL was attempted first and could not be retrieved. Search located the canonical AMR-022-5044 page, whose indexed full statement/report/discussion were inspected. The report itself merely claimed an open literature-triage status and supplied no argument. The canonical page links the published all-positive counterexample repository.

The 2018 Hayman–Lingham primary PDF was freshly downloaded, text-extracted, and its printed page 102 rendered and inspected. The original β=1 and arbitrary-positive extension were separated, including their differing right-hand absolute-value notation and degree ranges. The source's no-progress update is historical, not a current theorem-status assertion.

Read-only live GitHub checks found rank 681 queued at 0/5, no target state or history entry, no target attempt directory among the 60 main-branch attempt directories listed, no matching PR for 2305044, Brannan, or 5.44, and no matching branch for 2305044 or Brannan. Default-branch code search for Brannan returned no result. The full recursive-tree call failed with a transport error, so the repository checks are not represented as an exhaustive all-history proof of absence. The public catalog's local bytes matched the current Git blob exactly; its only same-statement-hash entry was this target. None of the three recorded related-target groups contains this ID.

The historical full problems/reports corpus was absent. No typed raw-record or pinned-prior-report equality is asserted. The public catalog and raw-corpus manifest are available; their hashes alone do not reconstruct the missing raw data.

A 2021 published direct β=1 proof and its addendum were identified; the paper's full text remained inaccessible. The 2026 Dunster manuscript explicitly states the completed β=1 status and has a full unit-square theorem claim, with numerical certification limits described in SOURCE_AUDIT.md.

Completion estimate: source-status investigation 70%; new full-result discovery 0% after identifying prior resolutions.

## Approach A — Finite binomial algebra and exact endpoint counterexamples

Mechanism: Cauchy-product coefficient extraction and the x=−1 collapse to a single binomial coefficient. The publicly posted cubic witness was recomputed independently. To respect the original n≥2 indexing, a separate degree-five rational witness was found and verified with positive right-hand side. An exact check also rejects the tempting but incorrect reuse of the cubic parameters at degree five.

Outcome: complete negative answer to the unrestricted extension, at a degree explicitly within the original odd-index range. This is subsumed by the prior public every-index theorem; no novelty claim. The β=1 original survives unchanged.

Artifacts: PROOFS.md sections 1–2 and verify_exact.py. Verified witness checkpoint sent at approximately 06:40 UTC.

## Approach B — Taylor remainder and a sector estimate

Mechanism: identify the sign of the odd Taylor remainder, bound its modulus through a one-dimensional integral, compare higher odd degrees with the first-degree kernel, and integrate the endpoint kernel. This reworks the method of Deniz–Çağlar–Szász into a self-contained sector proof.

Outcome: for every 0<α<1 and every odd j≥1, strict inequality holds when 2π/3≤|arg x|≤π. Endpoints x=±1 are also checked directly. The open middle sector remains outside this argument; it is not a full-circle proof. A numerical Taylor-identity replay is only a sanity check; the written proof is load-bearing.

Artifacts: PROOFS.md sections 4–5, check_sector_numerical.py, SECTOR_NUMERICAL_CHECKS.json.

## Approach C — Chebyshev polynomial and Bernstein positivity certificate

Mechanism: write |S_j(1)|²−|S_j(e^(iθ))|² using T_k(cos θ), factor α(1−cos θ), and express the remaining bivariate polynomial on the parameter square using a tensor Bernstein basis. A nonnegative Bernstein coefficient array would have proved positivity.

Outcome: the global, unsubdivided certificate fails at j=3,5,7. Its minimum coefficients are respectively −2, −7 and −332/15. Negative coefficients do not imply that the polynomial is negative; no target counterexample follows. The route is closed as a failed sufficient certificate in this investigation. No subdivision or degree-elevation search was launched after the prior-resolution stop.

Artifacts: check_bernstein.py, BERNSTEIN_CHECKS.json.

## Approach D — Polynomial continuity across a sign-change wall

Mechanism: fix α=3/2. At every odd j≥3 the coefficient P(β)=A_j(3/2,β,1) is negative at β=0 and positive at β=1/2, while A_j(3/2,β,−1) stays positive on 0<β<1/2. A largest-root argument and rational density give a positive-right-hand-side rational counterexample at each such j.

Outcome: complete self-contained verification of an odd-index subcase of the prior, stronger every-index theorem. This is a scope check and alternative reproduction, not a claimed discovery. In particular it does not assert one common β for all degrees.

Artifact: PROOFS.md section 3. The exact script additionally checks finite instances of the identities from the prior stronger construction, without treating those finite checks as a universal proof.

## 06:45–freeze — Stop and audit boundary

Stop condition: independently verified counterexamples plus verified prior literature resolving the original case. The requested exception to five new approach families applies; a fifth search family would duplicate known work. No further original-proof search was conducted after this verification pass.

Final estimates: source/status classification 100% within stated access limits; reproduced counterexample proof 100% before fresh independent audit; independent full β=1 proof audit incomplete; qualifying new discovery 0%. The exact controls pass. A fresh reviewer must check the authored mathematics and classification before any remote publication. No theorem-status or novelty promotion is requested.
