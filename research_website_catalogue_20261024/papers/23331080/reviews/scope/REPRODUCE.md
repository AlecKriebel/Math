# Read-only reproduction

Run the small independent verifier with the already-installed environment:

```sh
/Users/alec/Documents/Math/.venv/bin/python -B /Users/alec/Documents/Math/research_website_catalogue_20261024/papers/23331080/reviews/scope/verify_exact.py
```

It prints49 exact checks and7 rejected negative controls and writes nothing. The environment contains SymPy1.14.0 and mpmath1.3.0. Analytic imports and source reading remain essential; a passing program does not establish a new PDE theorem by itself.

Run full packet/custody closure with standard Python:

```sh
python3 -B /Users/alec/Documents/Math/research_website_catalogue_20261024/papers/23331080/reviews/scope/verify_closure.py
```

Closure hashes all owned entries and all51 immutable source files, checks all40 original ZIP payloads/order/CRC/sizes/attributes, verifies complete source JSON copies and fresh bounded support evidence, and reruns only the small independent verifier. It prints its result without creating files. It does not repeat the support scripts, invoke the archived wrapper/finalizers, download anything, or write a preexisting file.

OWNED_MANIFEST.json excludes itself, FINAL_SEAL.json and CLOSURE_RESULTS.json to avoid self-reference. FINAL_SEAL.json binds the manifest, input manifest, report, literal verdict and closure output with explicitly named full SHA-256 fields. Both excluded artifacts remain independently bound by that seal. A final repeat closure after seal creation checks those bindings too.
