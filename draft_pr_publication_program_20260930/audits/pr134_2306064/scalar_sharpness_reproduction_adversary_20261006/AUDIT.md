# PR134 independent scalar/sharpness/reproduction adversarial audit

Audit completion: **100% of this assigned audit**, with priority unassessed. The mathematical verdict is **PASS for the exact stated sufficient criterion and restricted-family sharpness**. Normal reproduction is **PASS**. There is a confirmed optimized-mode guard-erasure defect in the historical independent checker and an actually exercised explicit-if repair in isolated copies. This is not a novel-result or priority clearance, nor a claim of human peer review.

Original head supplied for this assignment: `6a865c574586d08e6fa185b09ebe746122457ff0`. Original proof SHA-256: `8ee69b778f281333c6a09850ed03de02f7d936174ab467e0899ca47799a2f4e7`. This family audits the supplied authenticated local original; it does not independently grant Git-head authentication or source/novelty clearance. Original substantive approach count remains **1/5**. Added central proof-search approaches: **0**. These calculations are validation of the original route, not a new candidate route.

## Independence, order, custody and exact target

Before seeing any original review contents, author/independent verification code or receipts, or other-family conclusion, I read only original `CANDIDATE.md`, `source_record.json`, and `readiness.json`. Readiness includes a historical verdict; I did not use that verdict as a mathematical premise. I independently optimized the scalar moment expression, calculated the quadratic and general single-degree expressions, and froze `INITIAL_MATH_VERDICT.md` at `2026-10-06T22:40:34.124846Z`, SHA-256 `de09bae2fafed9d061f178b997bfb750105dd6e45fabdda568b503e82ed0f4bf`. `INITIAL_FREEZE.json` records the actual freezing PID 50168 and size/hash. Only afterwards did I inspect original code and, later, actual old `review/REVIEW.md` and review summary.

Everything written is in this audit's own folder. No original file was written. `ORIGINAL_BEFORE_MANIFEST.json` and `ORIGINAL_AFTER_MANIFEST.json` enumerate all 17 original files with sizes and hashes and agree exactly. No service, main/index/native/author artifact, Git reference, branch, publication, or sheet was mutated; no individual was contacted. The run artifacts retain actual child PIDs, UTC starts/finishes, exit codes, input-script hashes, complete stdout/stderr, complete parsed receipts and per-run seals. No success receipt or ledger status was fabricated.

Let f be normalized and analytic in |z|<1. Define J_alpha=(1-alpha)zf'/f+alpha(1+zf''/f'), with removable origin values. The exact target is nonvanishing of f/z and f' and Re J_alpha>0 in the open disk. For a=|1-alpha|, b=|alpha| and d=a+2b-1, k=(d+sqrt(d^2+8b))/4, the candidate assumes sum(n>=2) n[1+k(n-1)]|a_n|<=1. It claims minimal nonnegative interpolation parameter only for 0<alpha<=1, only in these weights, only for the universal sufficient implication. It does not claim necessity for individual functions, arbitrary-weight optimality, or minimality outside [0,1].

## Independent constrained optimization and analytic proof

Write t_n=|a_n|, A=sum t_n, B=sum n t_n, X=B-A and Y=sum n(n-1)t_n. Under the strict budget B+lambda Y<1 with lambda>0, put D=1-B>0, u=X/D and v=Y/D. The exact moment constraints give Y>=2X>=0, hence 0<=2u<=v<1/lambda. The triangle majorant becomes

    F(u,v)=a u/(1+u)+b v.

It is nondecreasing in u and strictly increasing in v when b>0. Thus

    sup F = a/(1+2lambda)+b/lambda.

This is the true supremum for this moment optimization, not an unsupported relaxation. A single nonzero t_2 tending to 1/[2(1+lambda)] from below has X=t_2, Y=B=2t_2, and reaches u->1/(2lambda), v->1/lambda. For alpha!=0, b>0. Requiring this supremum to equal one gives

    2lambda^2-(a+2b-1)lambda-b=0.

The product of its roots is -b/2<0, so it has exactly one positive root, the candidate k. For strict feasibility v<1/k makes F<1 even when a=0. At alpha=1 the proof does not require strict monotonicity in u.

For lambda=k the series and triangle inequality give, pointwise in the disk,

    |zf'/f-1| <= X/(1-A),
    |zf''/f'| <= Y/(1-B).

A<=B/2 and B<1 make both denominators positive and imply the needed analytic nonvanishing. When k>0 the budget also gives Y finite. Therefore |J_alpha-1|<=F<1 implies Re J_alpha>0. This does not assume univalence to prove nonvanishing; those factors come directly from the coefficient budget.

The all-real branches are obtained algebraically: d=alpha on [0,1], d=-3alpha for alpha<0 and d=3alpha-2 for alpha>1. They produce exactly the three stated square-root formulas, continuous at both endpoints, with k(0)=0, k(1)=1 and k>0 for alpha!=0. Absolute values of both real multipliers make the argument valid when they have opposite signs. At alpha=0 use only B<1 and X/(1-A)=(B-A)/(1-A)<1. No division by k or second-moment assumption is legitimate or needed there.

For the non-strict budget and every 0<R<1, f_R=f(Rz)/R has coefficient magnitudes R^(n-1)t_n, so its sum is strict unless f is identity. For any original |w|<1 choose |w|<R<1. Both nonvanishing factors and J_alpha[f_R](w/R)=J_alpha[f](w) transfer to w. Identity has f/z=f'=J=1. Thus boundary equality in the coefficient budget is compatible with strict positivity at every interior point. The result claims no unit-circle positivity. The argument applies to infinite series, rather than extrapolating from tested polynomials.

A useful edge family is t_n=1/[n^2(n-1)] for n>=2. Its B_N=1-1/N tends to B=1 while Y_N=sum(n=2..N)1/n diverges. The power series f=z-sum t_n z^n is analytic in the disk and falls under the non-strict alpha=0 theorem, with localized first moment strictly below one. This proves that inserting a finite second-moment requirement would improperly narrow the endpoint theorem. The finite telescoping controls confirm the displayed partial sums; divergence is the standard harmonic-series argument, not a sampled conclusion.

## Sharpness, alternate families and limiting cases

For f_c=z-cz^2, 0<c<1/2 makes f_c/z and f_c' nonzero throughout the disk. With x=cz, direct quotient algebra yields

    J_alpha=[1-(4+alpha)x+4x^2]/[(1-x)(1-2x)].

For 0<alpha<=1, k obeys 2k^2-alpha k-alpha=0. Hence c*=1/[2(1+k)] is a numerator root in (0,1/2). The derivative 8x-(4+alpha) is strictly negative for 0<=x<1/2. Every 0<=lambda<k gives a nonempty interval

    c* < c < min(1/2,1/[2(1+lambda)]).

Choose such a c and a real c*/c<z<1. The weaker weighted sum is 2(1+lambda)c<1 and J_alpha<0 at that interior point. This proves universal sharpness with the source's nonvanishing assumptions preserved. At alpha=1, k=1 and c*=1/4. At alpha=0, zero is already the smallest parameter in the specified nonnegative family; no negative-lambda claim is inferred.

The exact naive-interpolation witness is alpha=1/2, c=8/25 and z=31/32. Its x=31/100 gives numerator -53/5000 and denominator 1311/5000, hence J=-53/1311, while naive sum 3c=24/25<1. For 0<alpha<1, k>alpha follows directly from alpha/k=2k/(1+k)<1.

A distinct single-degree family f=z-cz^N, N>=2, has m=N-1 and

    J_alpha=[1-(2N+alpha m^2)x+N^2 x^2]/[(1-x)(1-Nx)],
    x=c z^m.

For positive alpha its boundary obstruction within these weights is lambda_N satisfying N lambda_N^2-alpha(N-1)lambda_N-alpha=0. For 0<alpha<=1, lambda_N lies in (0,1], and N lambda^2/[1+(N-1)lambda] increases with N for fixed lambda in [0,1], because its derivative in N is lambda^2(1-lambda)/[1+(N-1)lambda]^2. Thus lambda_N<=lambda_2=k, strictly when alpha<1 and N>2. At alpha=1 every degree has lambda_N=1. Higher single negative coefficients cannot strengthen the claimed quadratic obstruction.

For alpha=-q<0, along positive real x the numerator is (1-Nx)^2+q m^2 x>0 for 0<=x<1/N. The opposite phase x=-c instead gives (1+Nc)^2-q m^2 c, a distinct sign mechanism considered in falsification. Outside-interval sharpness is deliberately unclaimed. General complex phases and mixed-degree functions are covered rigorously by the universal majorant, while the added exact controls challenge the implementation with sparse degree17 and mixed degrees 2,4,7,17, phases including 5/13+12i/13 and -20/29+21i/29, radii through 999/1000, identity and strict/equality budgets, and rational k as small as 10^-6 or large as 10^6. No additional counterexample to the stated theorem occurred.

The relevant limits are k~sqrt(alpha/2) as alpha->0+, k~sqrt(-alpha/2) as alpha->0-, k=(3/2)alpha-2/3+O(1/alpha) as alpha->+infinity, and k=-(3/2)alpha+1/3+O(1/|alpha|) as alpha->-infinity. These follow by expanding the exact root; they do not justify using a singular formula at alpha=0. Very close weaker weights in the added exact witnesses use lambda/k=99999999/100000000 and still give strict negative J at an interior point.

## Complete reproduction and actual negative controls

`REPRODUCTION_RESULTS.json` retains every field of all 12 parsed run receipts. Each run folder also keeps its complete stdout/stderr, launch/finish journal, complete RUN_RECEIPT and RUN_SEAL. Author normal and optimized stdout are byte-identical to the entire original `verification.json` (SHA-256 `42c249c59d8b6cdb47cbc226e96eb64d27678065a0886f39b998d51f4e8f1409`), including all category counts, proof hash and scope, not merely the number 50,840. Independent normal and optimized JSON objects are fully identical to the original receipt; their generated `independent_results.json` is byte-identical to the original. Their stdout is compact JSON while the saved receipt is pretty JSON, so claiming byte-identical independent stdout would be false.

| Run | Actual child PID | Exit | Complete object equals original | Stdout bytes equal original | Written receipt bytes equal original |
|---|---:|---:|---|---|---|
| author_baseline_normal | 50831 | 0 | True | True | None |
| independent_baseline_normal | 50832 | 0 | True | False | True |
| author_false_parameter_normal | 50837 | 1 | False | False | None |
| independent_false_parameter_normal | 50833 | 1 | False | False | None |
| independent_hardened_baseline_normal | 50874 | 0 | True | False | True |
| independent_hardened_false_parameter_normal | 50878 | 1 | False | False | None |
| author_baseline_optimized | 50911 | 0 | True | True | None |
| independent_baseline_optimized | 50942 | 0 | True | False | True |
| author_false_parameter_optimized | 50943 | 1 | False | False | None |
| independent_false_parameter_optimized | 50944 | 0 | True | False | True |
| independent_hardened_baseline_optimized | 50945 | 0 | True | False | True |
| independent_hardened_false_parameter_optimized | 50946 | 1 | False | False | None |

The negative controls change exactly one existing parameter identity from `==0` to the false `==1`; all rational parameter pairs still satisfy the original zero identity. Both author modes reject at the first control. The independent normal run rejects with AssertionError. The original independent optimized run returns exit zero, the same 28,722 count, the same full success object and byte-identical saved receipt despite that false identity. This is a reproduced failure of validation, not a theoretical warning.

The author has explicit `if not b:raise AssertionError(kind)` before incrementing its counter. The historical independent `ck` has `assert t;count+=1` on line 29. Under Python -O, the assert statement is removed, while `count+=1` survives and the argument expressions still execute. Thus the optimized original receipt's number denotes counted calls, not 28,722 predicates actually enforced. A byte-identical -O success receipt must not be described as confirming those predicates. The baseline normal run genuinely enforces all 28,722 tests; the guard-erasure finding does not invalidate the normal historical result or the written analytic proof.

The exact operative repair is to replace that line by

    if not t:raise AssertionError('independent control failed')
    count+=1

Actually exercised repair path: `isolated_runs/independent_hardened_baseline_normal/independent_checks.py`, 3,059 bytes, SHA-256 `4ccfb72d1f9e41c92eed9f26becd9ae1ece41f43718a74038bf993edf413686d`. The optimized-baseline repair copy has identical source bytes. This repair gives the complete original success receipt on clean inputs in both modes, and explicitly rejects the false identity in both modes. Corresponding child PIDs are 50874/50945 for normal/optimized clean baselines and 50878/50946 for false controls. No repair was applied to the original 17 files.

The independently added controls passed 26,093 explicitly guarded exact tests, 3,672 Gaussian-rational evaluations over 17 all-real parameter cases and 15 quadratic counterexamples. Child PID 51797 and the complete result appear in `distinct_family_run`; the source has SHA-256 `4f81533af52eb4908988aace90bcdd230f4278e706f78f3aa6b5aff8dd5f62b7`. These are finite falsification controls. They do not prove universal analytic membership, any infinite harmonic limit, or novelty. Those mathematical deductions are separately shown above.

## Historical review comparison and remaining limits

After the initial freeze I read the actual original `review/REVIEW.md`, SHA-256 `1890d539d80897016e19ef777c8c022032720ec076c1a3556a359711e319b2d8`, and actual review summary. Its analytic derivation uses a coefficientwise denominator comparison instead of my constrained optimization. It agrees on all-real signs, endpoint recovery, alpha=0 moment handling, dilation/equality and restricted sharpness. It reports the complete author replay and the 28,722 independent finite controls; both historical normal receipts were independently reproduced here. Its statement that no mandatory mathematical correction was found is supported. It did not test assert erasure or include a failing optimized-mode negative control. The new methodological repair above is required if the checker is to be relied upon in optimized execution or if optimized count receipts are to mean enforced predicates.

Both old suites are finite rational diagnostics: author 251 alpha/k cases, 2,510 coefficient vectors and 12,550 regular complex evaluations; independent 69 parameter pairs, 3,312 complex evaluations and 40 sharpness witnesses. They parameterize the positive root by rational k and validate identities, rather than evaluating an arbitrary irrational square root. This is legitimate as a diagnostic, and it neither exhausts real alpha nor proves the analytic theorem. The written algebra establishes the branches and unique positive root. A standalone independent receipt originally binds no proof/source hash; this audit's surrounding size/hash custody, complete-object comparison and immutable original inventory provide the missing execution/context binding. This is an audit repair, not a retrospective claim that the original independent receipt contained such metadata.

The strongest verified mathematical result is exactly the all-real sufficient criterion, including <= boundary budgets, and its one-parameter minimality for 0<alpha<=1. No mathematical gap remains in that scoped claim. This audit does not resolve present literature priority, global optimal coefficient regions, source rights, or the June 2026 paper's correctness. Those belong to the source/novelty family and the parent decision. No global or publication clearance is granted here.
