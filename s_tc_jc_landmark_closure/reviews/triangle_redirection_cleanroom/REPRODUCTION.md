# Deterministic reproduction

Requirements: Python 3.11 or later and a POSIX shell.  The verifier uses only
the Python standard library.

From `reviews/triangle_redirection_cleanroom/`:

```sh
bash verify_all.sh
```

Direct invocation is also supported:

```sh
python3 cleanroom_verify.py \
  --claim ../../primary/certificates/jc_triangle_redirection_active.json \
  --certificate certificate.json \
  --mutations mutation_results.json
```

Locked primary inputs at review time:

- `primary/verify_triangle_redirection.py`:
  `1898123e26dd2e3818f8a9e31d228cbe387f977362f3ea5d55cc4a5dbe97eb88`
- `primary/certificates/jc_triangle_redirection_active.json`:
  `1124e93f0d9f7af828564b51d77f17a9e638627bb31394204532c21cd03c9c37`

The primary Python file is not executed or imported by this review.  Its hash
is recorded solely to identify the reviewed claim generation.

