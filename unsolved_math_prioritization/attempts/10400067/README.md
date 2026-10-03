# 10400067 research packet

Start with [RESULT.md](RESULT.md) for the outcome and exact scope. The
original question remains unsolved after five substantive attempts.

- [SOURCE_GATE.md](SOURCE_GATE.md): original problem, prior-attempt check,
  current primary literature, source access and normalization cautions.
- `TURN_1.md` through `TURN_5.md`: substantive attempts in order.
- `TURN_1_MANIFEST.json` through `TURN_5_MANIFEST.json`: dated incremental
  content hashes; later files do not change the earlier hashed documents.
- `verify_core.py`, `CORE_CHECK.json`: exact Laurent algebra certificates.
- `verify_reconstruction.py`, `RECONSTRUCTION_CHECK.json`: exact moment
  reconstruction controls.
- `AUTHOR_MANIFEST.json`: frozen author-packet file hashes.

Run from this directory with Python 3:

```sh
python verify_core.py
python verify_reconstruction.py
```

There are no nonstandard dependencies and no network access is used by
the checkers. Source PDFs, full-text copies, browser artifacts, catalogue
corpora and private coordination are intentionally not included.
