# Independent review package

Read `AUDIT.md` for the complete mathematical decision and the detected permission-replay defect. `ACCEPTANCE.json` records accepted scope and the required outer-harness correction. The immutable author ZIP was not changed.

Run the independent review with Python 3:

```sh
python -I -S -B independent_verify.py /path/to/MINIMAL_SURFACES_10300008_AUTHOR.zip
python -I -S -B -O independent_verify.py /path/to/MINIMAL_SURFACES_10300008_AUTHOR.zip
python -I -S -B -OO independent_verify.py /path/to/MINIMAL_SURFACES_10300008_AUTHOR.zip
```

Use an ordinary non-root account: read-only permission-denial tests deliberately require an enforced write denial. No network, third-party packages, source papers, or datasets are needed to replay this script. It uses disposable temporary copies and checks that the author archive stays unchanged.

`HARNESS_CORRECTION.patch` is for an extracted working copy of the author's outer `test_bootstrap.py`. `test_bootstrap.patched.py` is the full corrected file. A corrected author distribution needs its own new archive receipt; do not silently replace the immutable archive. The mathematical payload and its manifest are unchanged by this patch.

The source and corpus rechecks here contain metadata only. Their historical local inputs are not distributed, and their hashes do not prove any mathematical claim.
