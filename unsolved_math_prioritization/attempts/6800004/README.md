# Biorthogonal curvature on S² × T²

**Credited source resolution.** The exact Riemannian question is answered by Zhiqi Chen and Hui Zhang, [arXiv:2609.08119v1](https://arxiv.org/abs/2609.08119v1), Theorem 1.2. This is a recent preprint, with no journal reference on the checked record. Original proof-attempt turns: **0/5**. No new solution or novelty is claimed.

## Read the result

- [Source certificate](SOURCE_CERTIFICATE.md): exact question, source, explicit metric, and strict bound
- [Complete independent audit](audit/AUDIT_REPORT.md): full proof explanation in Sections 3–5, adversarial checks, and limits; verdict PASS
- [Source/prior gate](GATE_REPORT.md): queue identity and prior-attempt checks
- [Source record](source_record.json) and [research log](RESEARCH_LOG.md)

At ε = 1/4 the construction has biorthogonal curvature at least 1/98304 for every tangent two-plane at every point. The curvature is that of the metric's Levi-Civita connection, unlike an earlier affine-connection relaxation. The original question was verified from Morgan–Pansu; the current UnsolvedMath page returned HTTP 403, so its live wording/status remains unverified.

## Reproduce the checks

Python 3.12 and SymPy 1.14.0 were used. From this directory:

```sh
python3 check_metric.py
python3 audit/independent_controls.py
python3 verify_manifest.py
```

The first program is an exact six-point diagnostic. The second symbolically verifies all base curvature entries and complete Hodge blocks, checks sign controls and the coordinate Laplacian, and differentiates the conformally modified metric at two exact points. The complete global argument is explained in the audit. Computational spot checks alone are not a global proof.

The publication manifest binds this portable packet. PUBLICATION_RECORD.json records the reviewed input fingerprints and the status-only/editorial packaging changes. The original frozen audit integrity results describe the input at review time. No third-party PDFs, screenshots, HTML, private history, or raw corpus is included.
