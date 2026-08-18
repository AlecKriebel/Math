# Bochnak--Coste--Roy citation audit

Status: **SOURCE VERIFIED**

Source checked: *Real Algebraic Geometry* (Springer, 1998), supplied PDF,
SHA-256
`ad406cb6d1342abf194126467ed440d4bcafc5073af48eef43e060540f168ef4`.
Only the cited pages were inspected; the 429-page book was not loaded as a
whole.

| Printed location | PDF page | Verified content | Manuscript use |
|---|---:|---|---|
| Theorem 2.2.1 | 33 | Coordinate projection of a semialgebraic set is semialgebraic | Tarski--Seidenberg, iterated for multiple eliminated coordinates |
| Proposition 2.8.2 | 57 | A semialgebraic set, its Euclidean closure, and its real Zariski closure have the same dimension | Closure and properness arguments |
| Proposition 2.8.4 | 58 | A nonempty open semialgebraic subset of `R^n` has dimension `n` | Full dimension of chart neighborhoods |
| Proposition 2.8.5(i) | 58 | The dimension of a finite union is the maximum of the dimensions | Finite-cover and finite-exception arguments |
| Proposition 2.8.5(ii) | 58 | Product dimensions add | Verified but not newly invoked; local product dimensions are proved by analytic charts and ranks |
| Theorem 2.8.8 | 59 | Semialgebraic maps do not increase dimension; semialgebraic bijections preserve it | Passage through semialgebraic charts |
| Proposition 2.8.13 | 60 | `dim(cl(A) \ A) < dim(A)` | Empty-interior converse and closure-difference statement |

The revised finite-cover proof keeps `U` merely relatively open.  It chooses
a nonempty relatively open semialgebraic neighborhood `V` inside `U`, applies
Proposition 2.8.5(i) to the finite cover of `V`, and then uses the already
proved dimension/interior equivalence.  No claim requires `U` itself to be
semialgebraic.

