# Conditional Möbius–ratios–prime witness: amended V1

Row 1795, ID 20000699, AIM-ANALYTIC_NUMBER_THEORY-0063. Checkpoint disposition: **resolved 1/5 only for the explicitly amended conditional rank-one finite-polynomial interpretation**. The arithmetic correlation hypothesis H_CK remains unproved.

Read [the complete combined conditional theorem and independent acceptance](witness/audit/INDEPENDENT_ACCEPTANCE_AND_COMBINED_THEOREM.md), then the [interpretation amendments](witness/audit/INTERPRETATION_AMENDMENTS.md). The historical formulation gate is included as provenance and is not accepted unchanged.

Mandatory amendments:
- 0 < psi <= phi < 1, with 1 < lambda < min(2,1/phi,1/(1-psi)).
- The corrected one-swap factor is B_(-beta,-alpha-s,gamma+s,delta)(1).
- Retain E_z = 2 pi w(0) N^(1-alpha-beta) / [(1-alpha-beta) zeta(1+gamma-alpha) zeta(1+delta-beta)]. The weight is real Schwartz and band-limited on the whole real line; no w(0)=0 assumption is substituted.

Under the explicitly quantified arithmetic H_CK, the sharp finite-polynomial ratios error is O(N^phi), uniformly on the microscopic four-shift polydisc. Exact mixed Cauchy differentiation evaluates the Hardy–Littlewood singular-series prime-power aggregate with error O(N^phi (log N)^2/c^2)=o(T). The sharp-to-linear comparison is O(N/(T(log N)^2)); the corrected Mellin correspondence includes the explicit endpoint.

This proves no individual fixed-gap Hardy–Littlewood asymptotic, unrestricted full-zeta ratios formula, all-rank result, or arithmetic randomness conjecture. It makes no novelty, priority, or exhaustive literature-absence claim. The coefficient family, profile, and method are credited to Conrey–Keating, and uniform ratios differentiation to earlier work including Conrey–Snaith. Source corrections are confined to the specified displayed formulas and inspected versions; they are not a blanket assessment of those papers. See [source correction scope](SOURCE_CORRECTION_SCOPE.md).

## Complete proof and audit contents

- [Sharp forward transfer](witness/forward/FORWARD_TRANSFER.md)
- [Kernel, cutoff-strip, and summatory-profile estimates](witness/forward/SHARP_TO_LINEAR_COMPARISON.md)
- [Euler identity and complete Mellin contour argument](witness/euler/EULER_AND_MELLIN.md)
- [Reverse theorem and evaluated aggregate](witness/reverse/REVERSE_THEOREM.md)
- [Independent exact mathematical audit](witness/exact/INDEPENDENT_EXACT_AUDIT.md)
- [Necessary parameter-range obstruction](witness/exact/NONVACUITY_OBSTRUCTION.md)
- [Source, prior-art, and parameter audit](witness/source/SOURCE_SCOPE_AND_PARAMETER_AUDIT.md)

## Offline reproduction

Use Python 3.10 or later with SymPy 1.14.0 installed. From any working directory run `python /path/to/package/verify_package.py --negative-controls`. It performs integrity checks, clean temporary-directory replay of all four unchanged mathematical scripts, and assertion/mathematical/integrity corruption controls. `python -O`, `python -OO`, and inherited PYTHONOPTIMIZE=1 or 2 are supported for the package verifier. The original assert-based scripts must be run through this wrapper when optimization may be enabled.

For an independently supplied frozen trust anchor, append `--manifest-sha256 HEX`. Without this external anchor the checks establish internal consistency, not authenticity against an attacker who replaces both files and their manifests. No verifier downloads anything, installs dependencies, accesses omitted originals, or writes to this package. Missing files, unexpected files, unsafe paths, changed accepted checker bytes, and disabled child assertions fail closed.

The exact, Euler, and independent control outputs must replay byte-for-byte. The reverse diagnostic compares all non-floating fields exactly; its sole floating discrepancy field must be finite and <=1e-12, because libm behavior can vary across Python platforms. The result also reports whether it is byte-identical on the current platform. Finite regressions support the authored proofs and do not establish the infinite analytic theorem or H_CK.

`EDITION_MAP.json` binds every included original to its public edition. The historical frozen review manifest and exact audit receipt retain their sealed original hashes. `HISTORICAL_BINDING_ACCOUNTING.json` accounts for every referenced authored artifact. The copied PDFs, extracted source text, dataset contents, and private coordination files are excluded. Metadata about historical source inspection and dataset hashes is retained, with no claim that this offline package rechecks excluded bytes.
