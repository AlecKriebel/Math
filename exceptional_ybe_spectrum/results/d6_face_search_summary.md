# E7 controlled-reflection face search summary

- Date: 2026-07-28
- Status: stopped after an exact theorem superseded the numerical search
- Search script: `scripts/d6_face_model_search.py`
- Predeclared seeds: `results/d6_face_seed_manifest.json`
- Raw log: `results/d6_face_runs.jsonl`

The search used
\[
H=\sum_{j=1}^{2m}
 \bigl((n_j\cdot\sigma)\otimes I_m\bigr)
 \otimes|\psi_j\rangle\langle\psi_j|
\]
on \(V=\mathbb C^2\otimes\mathbb C^m\). It was calibrated at \(d=4\):
seed `26073101` reached cubic residual
`7.476389109123043e-10` and its candidate was retained. Three other
\(d=4\) calibration seeds stopped at nonzero stationary points.

Four complete \(d=6\) production runs were recorded:

| seed | final residual | status |
|---:|---:|---|
| 26073201 | 13.654978496715914 | max iterations |
| 26073202 | 11.872182248786036 | max iterations |
| 26073203 | 11.872182248785922 | line search failed |
| 26073204 | 12.073306882638851 | max iterations |

Seed `26073205` has only a start record because that run was manually
interrupted. Seeds `26073206` through `26073220` were not run.

The remaining numerical batch was deliberately cancelled after the exact
argument in `notes/face_rank_one_control_no_go_d6.md` proved that **no**
\(d=6\) solution exists anywhere in this entire ansatz. Thus completing
more random seeds would add no mathematical information. The numerical
failures themselves are not used as evidence.

## SHA-256 provenance

```text
0b157571975994fe114135832dd1e81c5479e81428a315a06abcaaa209c6ab9d  scripts/d6_face_model_search.py
16442a53e31d089db8c3199f178630a52651b5add1abbd7eab30659552099a67  results/d6_face_seed_manifest.json
70c70e15b219e2751c707eb88afb393dbfdfc7c4d5557c8dcea501cbaa20c5d6  results/d6_face_runs.jsonl
0cf3f789975bc532a550461d4243391e9ff09149c6b4988724da2822641b816c  results/d6_face_candidates/d4_face_seed26073101.npz
7190eba4f76a09d2ca1865d3394694d42da723819eaae07e58f31559850810d0  notes/face_rank_one_control_no_go_d6.md
3ff84d0399866cc720d6adb3e07fb0e6bdad972b5d68efbfe675362da9898358  verifiers/verify_face_rank_one_control_no_go.py
0349b4a95e1f311bb90ea6f1518c89d6684e4b84685439750144fbc7427fd995  results/face_rank_one_control_no_go_exact.txt
```
