# Audited partial results: adaptive transport approximation

**Problem 30002760 / OWR-13487-001; rank 990. Unsolved, 5/5.**

Five scoped approaches are accepted without changes to the original proofs. Read [final acceptance](ROOT_ACCEPTANCE.md), [independent proof audit](independent_audit/AUDIT_REPORT.md), [separate reviewer clarifications](CLARIFICATIONS.md), and the [original mathematical reports](original/README.md).

The major positive stationary result is already due to Erath and Praetorius (2019): eventual linear SUPG estimator convergence and asymptotic optimal rates under their assumptions, including a sufficiently small marking parameter for optimality. [Primary manuscript](https://arxiv.org/abs/1806.11000), [journal DOI](https://doi.org/10.1016/j.cma.2019.05.028). This effort does not resolve the full broad parabolic or parameter-uniform preasymptotic scope. It makes no claim that every interpretation of the source question remains open.

## Contents and evidence

- original/: all five approaches, exact controls, source-scope qualifications and frozen manifest, unchanged
- independent_audit/: full independent proof review, exact controls, optional clarifications and source-verification metadata, unchanged
- ROOT_ACCEPTANCE.md and CLARIFICATIONS.md: final acceptance and separate precision notes
- VERIFY_PUBLICATION.py: strict external-anchor integrity gate and exact receipt replay
- TEST_MUTATIONS.py and MUTATION_RESULTS.json: disposable bootstrap, schema and inventory fault controls

Source titles, public URLs, hashes, sizes and inspection history are metadata only. No source PDFs/extracts, screenshots, datasets or private material are redistributed. The original reports' freeze-time review/publication statements are historical.

## Fail-closed replay

Python 3 standard library only. Retrieve the verifier SHA-256 and publication-manifest SHA-256 from the separate trusted publication record. Do not derive trusted anchors solely from this folder. Check the verifier before any packet executable runs, for example:

```python
import hashlib, pathlib, stat, sys
p = pathlib.Path(sys.argv[1])
data = p.read_bytes() if stat.S_ISREG(p.lstat().st_mode) else b''
if hashlib.sha256(data).hexdigest() != sys.argv[2]:
    raise SystemExit('Verifier bootstrap hash mismatch')
sys.argv = [str(p), *sys.argv[3:]]
exec(compile(data, str(p), 'exec'), {'__name__': '__main__', '__file__': str(p)})
```

Save the snippet outside this packet as a trusted bootstrap. Invoke it with `python -I -B /trusted/bootstrap.py /path/to/VERIFY_PUBLICATION.py TRUSTED_VERIFIER_SHA256 --expected-manifest TRUSTED_MANIFEST_SHA256`. The default replays all checks in normal, -O and -OO children. Repeat with `python -O -I -B` and `python -OO -I -B` for outer-interpreter coverage. `--check-only` verifies bytes without mathematical replay and is reported as such.

After the gate succeeds, run `python -I -B TEST_MUTATIONS.py --expected-manifest TRUSTED_MANIFEST_SHA256 --expected-verifier TRUSTED_VERIFIER_SHA256`; its output must equal MUTATION_RESULTS.json. The fault suite never alters the frozen inputs. Two external trusted hashes are needed because a manifest and verifier can otherwise be maliciously rewritten together. This is byte integrity and finite-control evidence, not an executable sandbox, formal verification, human peer review, or a novelty certificate.
