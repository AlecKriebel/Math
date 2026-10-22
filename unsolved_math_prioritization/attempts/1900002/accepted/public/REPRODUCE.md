# Reproducing the independent review

Use Python 3 with its standard library. No packages or network are required for the arithmetic and integrity controls. Use an unprivileged account for read-only controls.

First compare corrected_v3/bootstrap.py against the externally delivered SHA-256 in ACCEPTANCE.md. From a copy retaining the public package layout:

```sh
python -I -S -B corrected_v3/bootstrap.py
python -I -S -B -O corrected_v3/bootstrap.py
python -I -S -B -OO corrected_v3/bootstrap.py
python -I -S -B corrected_v3/controls.py
python -I -S -B public/independent_controls.py --checker corrected_v3/bundle/author/verify_math.py
```

The independent controls can also be run with -O and -OO. They authenticate the exact mathematical checker before importing it. The checker's mathematical code is byte-identical in original v1 and corrected v3.

To repeat actual write-denial tests, set files to mode 0444 and directories to 0555 before running:

```sh
python -I -S -B public/replay_readonly.py --release corrected_v3 --independent public/independent_controls.py
```

Add --problems, --reports, and --sources with local private inputs to bind the full corpus files and the two source PDFs. Corpus options must be supplied together. Without these inputs, the bootstrap explicitly reports those bindings as not supplied. No private paths or data are required for the public arithmetic checks, and private inputs are not shipped.

Receipts are external observations of completed runs. They are not executable proof objects. The public manifest authenticates deliverable bytes only; the mathematical review depends on its stated primary-source imports and reasoning.
