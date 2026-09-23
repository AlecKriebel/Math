# Final promotion review

Completed 2026-09-23 04:14:01 UTC by the separate adversarial proof-review agent. Best-guess completion: **100% of this bounded final manuscript and verifier review**. This is AI-assisted mathematical review, not external human peer review or formal proof-assistant verification.

## Verdict

**PASS: no must-fix mathematical, verifier, source-scope, priority-language, or AI-attribution issue found in the reviewed manuscript and verifier.** Promotion is justified only as an elementary note resolving the *printed slow-variation existence question*. The note appropriately avoids claiming a resolution of the possible intended index-one problem or certified research priority.

Reviewed files and SHA-256 at review time:

- `manuscript/paper.tex`: `54ed534779e5c0b87a748bd14fa07fc8761480f1750c6c3d1cbcf8b3d708ae5a`
- `verification/verify.py`: `44456a269588d175b8ac1fd529efda3b5d3609398da3bdedcb747237cf75c7b7`

Supporting consistency checks read `audit/source-match.md`, `audit/priority-independent.md`, `README.md`, `CITATION.cff`, and `LICENSES.md`. This review did not reperform the entire literature search, review the website rendering, or certify packaging/deployment. The final standing-assumption wording and precise Yeats citations were rechecked before approval.

## Mathematical proof

- Nonzero multiplicativity implies `f(1)=1`; hence every quotient is defined for `x>=1`.
- The convolution follows from unique factorization into a power of two and an odd integer. The sum is finite for fixed `x`.
- The dilation inequality uses only nonnegative summands and monotonicity of the odd summatory function. It holds for all fixed nonnegative integers `K`.
- The finite product deriving `F(2^K x)/F(x)->1` from the single-dilation hypothesis is valid, including the empty product when `K=0`.
- Limits are taken first in `x` for each fixed `K`. Passing to the infimum of the resulting bounds is valid for both finite and infinite `A`.
- The finite-`A` bound `F(x)<=A F_2(x)` supplies exactly the missing lower bound. There is no unproved regularity premise for `F_2`, uniformity assumption, or exchange of an infinite sum and a limit.
- Equivalence with all fixed dilations follows by monotonicity and positive and negative integer powers of two. The stated prime-`p` variant follows identically.
- The harmonic example, power-of-two indicator, bounded case, and printed-constant discrepancy are correct.

The final manuscript explicitly states at the outset that `f` is nonzero and multiplicative with nonnegative values. This incorporates the earlier optional clarity suggestion, and the standing assumptions now match the theorem scope directly.

## Executed verifier checks

Both commands exited successfully and produced identical JSON results:

```text
python3 verification/verify.py
python3 -O verification/verify.py
```

| Reported count | Result |
|---|---:|
| Multiplicative fixtures | 243 |
| Prime-power decompositions | 15,552 |
| Fixed-dilation bounds | 62,208 |
| Finite-local-sum bounds | 15,552 |
| Independent convolution inequalities | 34,992 |
| Example checks | 1,024 |

All comparisons use exact rational or integer arithmetic. Explicit `require` calls survive Python optimization; no `assert` statement can silently disappear under `-O`. The script has no network access or third-party dependencies.

Independent inspection of its indexing and claims found:

1. The five independently selected local weights generate all `3^5=243` fixtures. Coefficients on unlisted prime powers are zero. The construction is multiplicative without assuming complete multiplicativity.
2. Arrays reach index 512, exactly sufficient for `2^K*x` with `K<=3` and `x<=64`. The convolution retains `k=0,1,2,3`; all omitted local coefficients vanish by construction. Integer division correctly represents the cutoff for integer arguments.
3. In the general staircase check, `g[0]=0`, omitted negative indices represent zero, and `previous=max(0,n-K)` implements that extension. Since the kernel's zeroth coefficient is one, `h[n]>=g[n]`, and `h[n]-h[previous]>=g[n]-g[previous]`. These facts justify the tested upper bound on `A*g[n]-h[n]`.
4. The harmonic identity removes even denominators exactly. The geometric sum for powers of two is `2-2^{-L}`, with `L=floor(log_2 n)` computed exactly using integer bit length. The index-one control is a finite example outside the theorem's hypothesis.
5. The output expressly limits its scope to finite identities and examples. It does not claim to prove infinite-series evaluation, asymptotic convergence, or the universal theorem by numerical testing. The paper makes the same limitation explicit.

The fixture and example checks supplement the analytic proof. Their passing does not independently establish the theorem or originality.

## Source scope, priority, and attribution

The paper identifies the printed source hypothesis, replaces its inconsistent numerical prediction, and labels a missing `lambda` as a possible explanation rather than a proven erratum. It explicitly says the index-one reformulation is not addressed.

Its bounded-search claim matches the supporting priority audit: no exact earlier resolution was located, close older work is acknowledged, some full texts were inaccessible, and folklore or overlooked precedents are not excluded. The precise references were independently rechecked against the primary texts: Yeats (2002), Proposition 43, invokes Property II for both factors, which Definition 36 includes regular variation of their sums; Yeats (2003), Theorem 2, assumes regular variation of one factor sum and an absolute-convergence abscissa strictly below its index for the other factor. The manuscript accurately states these distinctions. See the [2002 journal text](https://nyjm.albany.edu/j/2002/8-4p.pdf) and [2003 publisher text](https://doi.org/10.4153/CMB-2003-046-5). This targeted citation check is not a new comprehensive priority search.

The note calls itself unrefereed, identifies the AI-generated candidate, discloses Codex drafting and separate AI audit agents, and says no external human referee was consulted. The author and ORCID match the user-supplied metadata. None of these statements turns AI review into human peer review.

## Remaining limitations

No mathematical gap was found in the scoped theorem. Originality remains qualified, the possible index-one question remains unresolved by this work, and no formal proof assistant has been used. Website publication, archival integrity, and manual Zenodo deposit remain separate delivery checks for the coordinating agent.
