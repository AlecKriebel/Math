# Reproducibility Manifest

Checkpoint: 2026-07-23T19:32:06Z

Environment used:

- macOS
- Python 3.14.6
- Git 2.38.2
- no third-party Python packages

SHA-256:

```text
968b88fe00a386c81cafa5182e5b5471d099148cc1b83e8c767a168aec49ca96  certificates/d5_roots.json
af4cded5a82b4ee5a4937c59dafc1eccb23586e8a3163c18f77d61b01e2cb7be  verifiers/verify_d5.py
b32168e4095e3bded767e58a9b34afcf6a79051162468547926d92ddef9cf8f8  tests/test_verify_d5.py
322d0f231da5eba91a1f462d4abf68018d170492ef3489fb4de95eddeaac9bc1  verifiers/verify_two_point_barrier.py
7be6d018fc1ad77485d4614f1bef398286bb1c4252d5bc2f2d6662ca61f1c6f5  tests/test_two_point_barrier.py
d9686f397e9524b21b22afe670d4fe679ee9678342d290b778b5ac29485f5c52  proofs/two_point_lp_barrier.md
c54b38d8216bf76a79c57119fc46245811188e1de05c840c68a33cec9b7fe1b0  experiments/input/spherical_codes_5_41.txt
4a024b409000af8bec2d980ebbc170beb2e17531babb5f8b57ed631ff2e893f3  proofs/d5_saturation.md
7d25d2398624517b47f30116d538f436945d06bc076ffa477cc287f34dc8e3a7  verifiers/verify_d5_saturation.py
378d1a761741bfa3543025a6bc136848cb7733228d0b5d1e9d9fbd2cceb932d3  tests/test_d5_saturation.py
c45af67ba5ce5e810acb95562619106703dbb5aa42a5153bb7c656d6e2bb9b88  proofs/rank_kernel_barriers.md
2264bd73e98fb3ba0b0248d09fda31d94a739c1fbc71e76d4802204111eec7cf  verifiers/verify_rank_kernel_barriers.py
d67db988fc68333dad1a8c538121f146418efc3f9586ee536873198adfa684b5  tests/test_rank_kernel_barriers.py
7c32331f627222fb7d93a6f629b593bb1e09f131011f19d8343a200a0d70c964  experiments/construction_round1.md
29056696abf516b1abeae51bdad90254a6800bf0b5e2b7c96ff4802944e14937  experiments/random_codes/analyze_refine_coordinates.py
4935eae66ce2866733bd17e8376290d33e618d3a772cf19e09ed046cb654f0ec  experiments/random_codes/perturb_benchmark.py
27021a1e1105488e2e0e60a0782e3ceb6ae974bad1084c7143ae0dc7b22ac1d6  experiments/random_codes/refine_spherical5.py
f69a1b5cb760a16d9cda8d7f287c6f25fba08538d7a7a0aded2bb2eea02a5b39  experiments/random_codes/search_spherical5.py
7e1dc5ac460b575506fd22aff853a412dc6240195973c815d230ddd3d297c07a  experiments/random_codes/slsqp_perturb.py
d443c739d3ecf0d3ca10a4647dfb8c820621ca9c45b464e4b0b44e9244a9df2a  experiments/random_codes/test_numerical_tools.py
3c0a92f5f9f275ed4532701ddb4b07adc506aad4aac29e8cae9597a45bb71c33  experiments/random_codes/README.md
b8b6468665f9f80a85dedd23ec082ff1c15299a4e22b6433c4c3a45a3cf9a1bf  experiments/random_codes/RESULTS.md
```

Verification commands:

```sh
cd kissing_number_5
python3 verifiers/verify_d5.py certificates/d5_roots.json
python3 verifiers/verify_two_point_barrier.py
python3 verifiers/verify_d5_saturation.py
python3 verifiers/verify_rank_kernel_barriers.py
python3 -m unittest discover -s tests -v
```

Expected verifier summary:

```json
{"boundary_pair_count": 240, "dimension": 5, "maximum_integer_dot": 1, "minimum_integer_dot": -2, "pair_count": 780, "point_count": 40, "status": "PASS"}
```

Expected two-point-barrier summary includes:

```text
mass: 41
minimum_moment: 1027/16000
minimum_moment_degree: 2
status: PASS
```
