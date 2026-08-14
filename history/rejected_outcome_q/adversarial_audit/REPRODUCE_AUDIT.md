# Reproduce the Outcome Q audit

Run from this directory.

## Frozen-input integrity

```bash
shasum -a 256 -c FROZEN_INPUTS.sha256
unzip -t frozen_inputs/STC_JC_Convention_Closure_Outcome_Q_Final.zip
```

The expected archive SHA-256 is
`abb83eff03996b7b95520ace2491c233daa4a9634ef1a771d51dc703dbf97f14`.

## Exact double-zipper counterexample

```bash
python3 independent/double_zipper_counterexample.py
```

The verifier must report all of the following simultaneously:

- `lsa_valid: true`;
- `level: 2`;
- `tree_child: false`, with offender `Q`;
- cleaned edges `L1-t`, `L2-t`, and `L3-t`, all without arrowheads.

The verifier SHA-256 is
`167d68c29c64bae67fcfcdfa31c4c5fa2f7b5e9853510538ab0e2740c9939dd1`.
It intentionally refuses optimized Python so theorem-critical assertions
cannot be disabled.

## Supplied-release regression

From
`unpacked/STC_JC_Convention_Closure_Outcome_Q_Final/release_tree`, run:

```bash
bash reproducibility/verify_quick.sh
```

On the declared local environment this fails because `pdftotext` is invoked
but Poppler is not declared in `environment.yml`.  Supplying that missing
utility allows the stored quick/full checks to pass, but does not test the
double zipper.  `verify_regenerate_all.sh` additionally byte-compares an
environment-stamped `sys.version` string and is therefore tied to the exact
Python build used to freeze the package.

## Authoritative verdict

Read `ADVERSARIAL_REVIEW.md`.  The supplied package is frozen as evidence and
must not be treated as an active theorem input.
