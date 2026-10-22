# Unitary distinction audit and corrected derivative

Start with INDEPENDENT_AUDIT.md. The disposition is **not solved here**.

The original author archive remains immutable. Its SHA-256 is
`95e0aa90ed1c0e22d905fd77286d14e51760f5cd2a60cfa5295bade4474e008a`.
The corrected payload has manifest SHA-256
`4999825da91af80be0b889143a86ed98181e4ed9aa1489ce5a831c6d23b5b703`.

This audit archive contains `audit/` (authored audit, tests, acceptance metadata)
and `corrected/` (the actually patched nine-file payload), with an external-style
AUDIT_MANIFEST.json covering both trees. No source PDF, copied source extract,
dataset contents, or private coordination files are included.

## Trusted replay

Use a trusted Python interpreter and a reviewed copy of `isolated_bootstrap.py`.
Before executing it, independently check its SHA-256:
`1f1dae9e6a5123d86febe4d485dc5b29e7a43d1ff484a0915816acb4f18f0032`.
Compare this value and the expected payload manifest pin against the separately
supplied audit receipt, not values supplied by an untrusted replacement package.

From the extracted audit archive:

    python -I -S -B audit/isolated_bootstrap.py corrected 4999825da91af80be0b889143a86ed98181e4ed9aa1489ce5a831c6d23b5b703
    python -I -S -B -O audit/isolated_bootstrap.py corrected 4999825da91af80be0b889143a86ed98181e4ed9aa1489ce5a831c6d23b5b703
    python -I -S -B audit/isolated_bootstrap.py corrected 4999825da91af80be0b889143a86ed98181e4ed9aa1489ce5a831c6d23b5b703 audit_checks.py
    python -I -S -B audit/independent_counting.py corrected 4999825da91af80be0b889143a86ed98181e4ed9aa1489ce5a831c6d23b5b703

The independent acceptance suite additionally needs the original extracted
nine-file payload and the three exact complete public-corpus snapshots as
local paths. These are inputs, not included public deliverables:

    python -I -S -B audit/acceptance_checks.py ORIGINAL corrected CATALOG PROBLEMS REPORTS

Use `-O` as well to reproduce ACCEPTANCE_OPTIMIZED.json. Optional corpus-only
replay goes through the external bootstrap with entry `verify_corpora.py`,
then `--catalog CATALOG --problems PROBLEMS --reports REPORTS`.

The correction patch was actually applied to an independent copy of the
original payload and reproduced every corrected file byte-for-byte. The
original direct-startup flaw and all corrected acceptance outcomes are
retained explicitly. Neither a successful integrity check nor finite arithmetic
checks constitute a proof of the unrestricted mathematical converse.
