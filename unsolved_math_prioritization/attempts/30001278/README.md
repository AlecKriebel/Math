# Sharper local ramification bounds: accepted partial results

Problem 30001278 / OWR-3480-009, rank 971. Queue disposition: **unsolved, 5/5**.

All five authored mathematical approaches passed a separate adversarial AI audit within their stated partial or conditional scopes. There is no required mathematical correction. This is unrefereed AI-assisted work, not human peer review or formal verification. It makes no complete-solution, counterexample-to-the-original, novelty, or global-openness claim.

Read [the full independent audit](audit/AUDIT_REPORT.md), [the claim verdict](audit/VERDICT.json), and the five numbered notes in [accepted](accepted/README.md). The source's semistable conjecture includes the catalogue's crystalline subcase; its separate crystalline-improvement question is not conflated with that conjecture. Published inputs receive explicit credit.

## Accepted scope

- The sharper different bound when r >= p^a + 1.
- The exact Kummer-tower calculation and a conditional reduction. The precise relative bound d(L_s/K_s) < eb, or property (P_eb), is still unproved here for arbitrary lattices.
- The target when p^(n-1) divides r, including all n=1, plus the exact scalar-annihilator obstruction.
- The stated integral direct sum of unramified twists of cyclotomic powers, plus a genuine crystalline lattice obstruction to rational-splitting and semisimplification reductions.
- The actual inertia p-order criterion, the sufficient ambient GL rank criterion, and all rank-one cases.

Separately credited: every crystalline r=1 case follows from Fontaine's finite-flat bound as stated in Hattori, Theorem 2.18. These overlapping sufficient conditions do not settle arbitrary higher-weight lattices. The residual test p=3, e=1, n=2, r=7 has target 871/162, upper-break loss 10/81, and optimized scalar loss 1/18. This is a gap in these arguments, not a proof of global openness.

## Frozen originals and optional hardening

`original/` and `audit/`, and both corresponding archives, are byte-preserved freezes. `accepted/` is a separate copy obtained by applying the actual [optional patch](audit/OPTIONAL_CLI_HARDENING.patch). It changes only the main verifier's root construction from `resolve()` to `absolute()` and the corresponding manifest entry. No mathematical text, formula, or expected count changes.

The patch rejects a direct symlink-root alias to the main verifier. It does not reject every symlink in ancestor paths, change the negative-controls helper's path aliases, or remove deliberate math-only mode. The original alias behavior did not permit changed payload bytes under the external anchor. This optional patch creates a distinct manifest identity; it is not a mathematical repair.

The original and accepted author READMEs retain their historical pre-audit wording. The later audit and this acceptance record supersede that historical review status only, without changing the frozen text.

## Reproduction

Use Python 3, standard library only. From any working directory:

```
python3 -B /path/to/packet/verify_publication.py --manifest-sha256 EXTERNAL_DIGEST
python3 -B -O /path/to/packet/verify_publication.py --manifest-sha256 EXTERNAL_DIGEST
python3 -B /path/to/packet/corruption_controls.py --manifest-sha256 EXTERNAL_DIGEST
```

Obtain EXTERNAL_DIGEST from the PR description or a separately retained receipt. The digest of PUBLIC_MANIFEST.json must be authenticated outside the package before executing its code; an internal manifest alone only establishes consistency. The wrapper checks the full allowlist and both archives, replays the exact patch into a temporary copy, reruns original/accepted author controls, and reproduces independent mathematical and adversarial results in normal and optimized modes. The separate corruption suite actually mutates disposable copies and requires nonzero CLI rejections, including coordinated rehashing against the external anchor. Checks use no source PDFs, dataset files, network, or private fixtures.

These finite arithmetic, integrity, and corruption controls supplement the written arguments. They do not certify arbitrary local fields, compare all literature, validate untrusted code in a sandbox, or turn finite samples into a proof.

Only authored research, audit, acceptance and verification material, with public bibliographic/fingerprint metadata, is included. Copied PDFs, extracts, images, dataset contents, and private coordination are excluded.
