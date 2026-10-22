# A periodic Lefschetz counterexample

For a fixed prime p and the fixed infinite field K = F_p(t), the homogeneous Artinian chain in [PROOF.md](PROOF.md) uses two rows of variables and satisfies the full symmetric-chain compatibility condition. For every n >= 2, both the weak and strong Lefschetz properties hold if and only if p does not divide n-1. At n = 1 both hold. Thus each property holds and fails at arbitrarily large widths in one fixed chain.

This answers both eventual-constancy questions negatively in the original unrestricted-characteristic, arbitrary-fixed-row formulation. It does not resolve the separately restricted characteristic-zero or one-row questions. No novelty or exhaustive priority claim is made.

## Read the mathematics

1. [PROOF.md](PROOF.md): the accepted short proof, preserved byte for byte.
2. [AUDIT.md](AUDIT.md): the primary independent acceptance audit, also preserved byte for byte. It verifies the source scope, all-linear-form obstruction, strong Lefschetz maps, and fixed-field quantifiers.
3. [SOURCES.json](SOURCES.json): public bibliographic metadata, retrieval and inspection records, and byte pins. The original question is on printed p. 1596, PDF p. 58, of the [Oberwolfach report](https://ems.press/journals/owr/articles/2654827), with setup on the preceding two pages.
4. [PRIORITY.md](PRIORITY.md): the bounded literature-search qualification.

## Reproduce the finite checks

Python 3.9 or newer is required for the complete reader package. The first checker uses only the standard library. The independent checker additionally needs SymPy; the tested version is pinned in requirements.txt. The recorded environment was Python 3.12.14 with SymPy 1.14.0.

Run from this directory:

```sh
python -B verify.py
python -B verify_independent.py
python -B -O verify.py
python -B -O verify_independent.py
python -B -OO verify.py
python -B -OO verify_independent.py
```

Both checkers recompute their complete finite test ranges, compare the resulting UTF-8 JSON bytes with the included historical results, and fail on any mismatch. They do not modify those results. An optional `--output /path/to/new-result.json` creates a new copy after successful comparison and refuses to overwrite an existing file. Each checker works with its companion result file and declared dependencies, with no private-directory dependency.

- verify.py: 44 raw-quotient modular witness cases and all 7,707 linear forms across six small prime-field cases.
- verify_independent.py: seven integer Smith normal forms, five symbolic determinants, 65 modular witness cases, and 152 column injections.

The scripts retain active validation under normal Python, -O, and -OO. [code_changes/README.md](code_changes/README.md) identifies the limited packaging edits and exact unified diffs. The independent audit's description of its original normal-mode run remains historical; the additional optimized-mode runs are packaging checks.

Finite computation corroborates the proof. It does not replace its all-width argument.

## Check the frozen files

MANIFEST.json records each other public file's byte count and SHA-256. Its own SHA-256 is held separately in EXTERNAL_PIN.json alongside this public directory. Supply that independently retained value:

```sh
python -B check_manifest.py --expected-sha256 THE_MANIFEST_SHA256
```

This is an ordinary byte-integrity check against a supplied pin, not authentication or a guarantee against a hostile interpreter or filesystem. The mathematical acceptance, finite computation, and packaging checks are distinct records. No source PDF, extracted source text, source image, dataset contents, or private coordination material is included.
