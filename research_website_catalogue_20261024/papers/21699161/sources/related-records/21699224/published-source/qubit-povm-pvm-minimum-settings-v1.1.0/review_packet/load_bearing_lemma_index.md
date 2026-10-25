# Load-bearing lemma index

| Item | Manuscript location | Verification artifact | Why it matters |
|---|---|---|---|
| Exact `3 x 2` strategy and gap | Theorem 3.1, Appendices A-B | `artifacts/three_by_two_separation/verify_exact.py` | Establishes sufficiency of `3 x 2` |
| One-binary-party circuit simulation | Theorem 4.2, Appendix C | Manuscript proof | Produces one simultaneous PVM mixture of the full behavior |
| Common-span filtering | Lemma 4.4 | Manuscript proof | Forces scalar-only span intersections at an extreme behavior |
| Exclusion of four outcomes | Theorem 4.5, Appendix D | Manuscript rank-square proof | Reduces arbitrary finite outputs to binary/ternary residual form |
| Physical exactness of incidence coordinates | Theorem 6.1 | Closure identities plus manuscript reconstruction | Makes every uphill incidence tangent a genuine quantum curve |
| Strict multiplier positivity | Proposition 7.3, Appendix E | Manuscript duality proof | Makes the Hessian coefficient matrix positive definite |
| Weighted Hessian and inertia | Proposition 8.1, Appendix F | `artifacts/two_by_two_closure/verify_exact.py` | Excludes every differential rank at least two |
| Exceptional fibers of the quadratic map | Proposition 9.1, Appendix G | Closure verifier/resultants | Excludes rank one |
| Rank-zero bounded transportation | Proposition 9.2, Appendix H | Closure verifier and rank-zero simulator | Gives an explicit simultaneous PVM mixture |
| Nearest-point separation | Lemma 2.2 | Manuscript proof | Converts support-function equality to convex-set equality |

Run all finite certificates with:

```sh
./run_all.sh
```

The page numbers should be regenerated after final journal formatting; theorem
and appendix identifiers are stable.
