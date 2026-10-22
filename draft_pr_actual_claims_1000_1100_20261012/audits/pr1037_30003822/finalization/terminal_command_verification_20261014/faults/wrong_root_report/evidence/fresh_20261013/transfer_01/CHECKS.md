# Fresh executable check receipts and limits

`fresh_checks.py` was newly written for this independent review, after the independent written derivation and before reading submitted AUDIT.md or ACCEPTANCE.md. It imports no historical checker, fixture, or result. The original ten-file theoretical edition contains no checker code; its historical finite-check prose was not replayed or simulated.

Environment: Python 3.14.6, SymPy 1.14.0, mpmath 1.3.0. `requirements.txt` fixes the two installed packages. Script SHA-256: `b16ff6ab8246652feb9db04c212fef88f97c36ed798320650139b9ecaee2ef37`. All three actual processes exited 0 and had empty stderr; their command, timestamps, elapsed times and output identities appear in `RUN_RECEIPTS.json`. stdout and JSON results are preserved per mode. No floating-point computation is used.

## Mechanically distinct checks

The graph route enumerates every interlayer subset, uses a disjoint-set cycle test after the chosen internal trees, rejects X-only components, and classifies Y components. The exterior route independently multiplies bit-mask wedge monomials with explicit inversion-parity signs, forms the edge exponential as a product, and extracts the X top coefficient. The Gaussian route separately translates the polynomial to z+xi, computes H_D, substitutes B, multiplies the S exponential, and compares the resulting ordered operator with direct edge-factor extraction on every partition state. Constant basis coordinates are solved exactly on an independent subset of forest-state vectors; stability is checked by full exterior-column reconstruction.

## Actual passes

- `--mode symbolic` (start 2026-10-13T22:32:49.507901+00:00, 4.755 seconds): every labelled tree product on 3 and 4 vertices agrees (3 and 16 trees); reversal, repetition and triangle-cycle checks pass. Full generic symbolic T for n=1,2,3 has det T=(det A)^C_n, verified in the integral polynomial ring with 1, 3, 222 determinant monomials. Enumeration visits 2, 32, 2560 partition/subset pairs; admissible per-row counts are [1], [8,8], and [189,126,126,126,63]. Symbolic exterior versus independent graph transfer matches for n=1,2. Allowing X-only components as a fault changes the n=2 determinant from 25 to 96 and is detected.
- `--mode exterior` (start 2026-10-13T22:33:02.316092+00:00, 6.216 seconds): exact graph transfer versus exterior extraction on every Bell state for nine signed, zero, singular, or zero-row-sum matrices at n=1 through 4. Invertible zero-row cases include n=2 det A=5, det T=25 and n=3 det A=9, det T=59049. Singular n=3 with nonzero row sums has Gaussian equality and quotient determinant zero. Ordered Gaussian factorization passes wherever D is invertible; H_D and M_S determinants are 1. The n=4 full 15-state signed nonsymmetric example has quotient rank 14, det A=52, det G=52^14; its full determinant also matches 52^14 times its permanent 14. The permanent check is a finite additional consistency check, not a new all-n claim. Swapping H_D and rho(B), and separately omitting H_D normalization, changes the operator in the n=2,3,4 invertible samples and is detected.
- `--mode n4tree` (start 2026-10-13T22:33:02.319703+00:00, 9.466 seconds): all 15 n=4 Bell input states, with all 65,536 interlayer subsets per input, give exactly the same transfer matrices and admissible counts for star, path and last-root internal trees. The crossing partition {{1,3},{2,4}} is explicitly included. This is 2,949,120 graph-subset visits across the three choices.

The JSON `checks` counter printed on completion counts prior record entries, including the environment receipt; it is not a count of individual assertions or tested forests. Completion itself adds one final record. The mode record lengths are 13, 40, and 5.

## Reproduction

From this folder, create an isolated Python environment and install `requirements.txt`, then run each of `python fresh_checks.py --mode symbolic`, `--mode exterior`, and `--mode n4tree`. Redirect stdout/stderr if recreating the stored logs. The script writes the result JSON corresponding to the selected mode. `--mode all` combines the same checks and writes a separately named JSON result.

Finite checks test signs, counts, normalization, operator order, exceptional specializations, and a first nontrivial Bell-to-Catalan kernel. They do not establish the universal theorem, exact det A multiplicity, or irreducibility. Universal validity rests on the independent derivation and the submitted proof.
