# Append-only addendum F02: producer case-alias exclusions

This supplements the originally closed `package_preflight01` review. **F02(P2) is an additional required producer-guard repair.** The original24-output seal remains byte-for-byte `3f966d9129617722087875594b0b16df7e611545b2abf7cf3046e9cb7ddb9e78`; none of its reports, verdicts or historical input bindings has been rebound to a later package.

The reviewed pre-fix producer has SHA-256 `4a8b9b4b0fce6ecc2bd3f0595801e62f5214e7532e8b41567be4a852b3af9dd1`; the reviewed ZIP is `bee5276046e4b00698f73bcee22b2c91c4085393bec1dc55caa139538d341690`. This addendum concerns that exact producer. While I was completing a final additional check, root reported independently fixing F01 and building a newer ZIP. I have not reviewed or rebound this review to that newer freeze. A fix solely adding `safe_path(relative.as_posix())` would not address the case comparisons described here.

## Reproducible finding

At `publication/make_package.py` lines30–33, excluded component names and the `.private` substring are compared case-sensitively. This macOS filesystem is case-insensitive. `Path.resolve()` follows directory symlinks but preserves the case of the target spelling. Consequently an internal directory alias such as `AUDIT/.CACHE/aliased_geometry01` can refer to an actual directory beneath `.cache`, while the guard checks `.CACHE` and accepts it.

`case_alias_controls.py` and `CASE_ALIAS_CONTROLS.json` reproduce six real process cases, for `.cache`, `sources`, `scratch`, `qa`, `.secrets` and `.private`:

1. Copy the exact historical audit layout inside this review's cache.
2. Move the same preserved sealed geometry-family data into the chosen actual lowercase excluded directory.
3. Replace the normal review-family directory with an internal directory symlink whose target uses the uppercase alias, e.g. `.CACHE`.
4. Confirm the two spellings denote the same object using `samefile()`, confirm that the selected leaf itself is not a symlink, and record the resolved audit-relative source spelling.
5. Run the exact unchanged producer and unchanged selector code under OS network denial.

All six processes exit0. Every source/seal byte selected in the test is unchanged, and every resulting ZIP equals the reviewed original ZIP exactly. Unlike F01's guard-contract test with an additional copy-only caller, this F02 reproduction needs no changed producer, no new caller, no modified seal and no modified selector. The script explicitly pins the cached historical producer hash before running.

This establishes a source-exclusion bypass. It does **not** allege that the actual production audit has these directory redirects, that any current archive contains a traversal name, or that any raw/private material leaked. The tests deliberately use the same already-authored sealed bytes, so the present archive's clean inventory and mathematical verdict remain intact. The policy being tested excludes these source directories regardless of the selected content's semantic authorship.

## Required repair and limits

Compare the forbidden names and `.private` substring case-insensitively on the audit-relative lexical, resolved and archive components, or otherwise reliably reject these aliases. Preserve the intended allowance for unrelated external cache/scratch ancestors. Add copied regressions for the case-alias source redirects while retaining F01's lexical-parent regression and the existing symlink/escape tests. Regenerate and bind the producer-containing ZIP, then have the next fresh reviewer check the actual resulting freeze.

No further mathematical or PDF finding was discovered. The original mathematical, exact replay, inventory, attribution/disclosure and five-page visual audit remain as recorded. This addendum makes no claim to inspect root's later repaired freeze and performs no production action.
