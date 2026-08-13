# Deterministic reproduction

The active verifier uses only the Python standard library. It imports no
module under `primary/`, Euclid's review, or another review directory. Primary
and upstream-review artifacts are read only as hash-locked claims and data.

From this directory, run:

```sh
bash verify_all.sh
```

The wrapper:

1. checks that all four reviewed commits exist with their exact full hashes;
2. runs the verifier in a clean environment and writes outputs to a temporary
   directory;
3. compares the regenerated `certificate.json` and
   `mutation_results.json` byte-for-byte with the committed copies;
4. validates `MANIFEST.sha256`.

The exact symbolic replay normally takes a few minutes on the project
machine. It reconstructs all 246 active and 280 zero-side
descriptor/invariant classes, all 225 body witnesses, and all strict-factor
proofs; it is not a sampled quick check.

Direct invocation is:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 referee_n3.py \
  --certificate certificate.json \
  --mutations mutation_results.json
```

`strict_factor_certificate.json` is verified with stdlib arithmetic during
every active run. Its optional factorization-discovery regeneration requires
SymPy 1.14:

```sh
python3 regenerate_strict_factors.py --output /tmp/strict_factors.json
cmp /tmp/strict_factors.json strict_factor_certificate.json
```

The optional command is not part of the trusted verification path: the
stdlib verifier multiplies the committed factors back to each graph-derived
integer polynomial and independently recertifies every Bernstein sign.
