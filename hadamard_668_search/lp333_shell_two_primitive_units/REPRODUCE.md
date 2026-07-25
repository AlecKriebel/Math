# Reproducing the shell-two primitive-unit package

Run from:

```sh
cd /Users/alec/Documents/Math-h668-local/hadamard_668_search
```

The frozen run used Python 3.11.8 and NumPy 2.4.6 on an Apple M1 Pro with
16 GiB physical RAM.  Set the interpreter without changing any system
environment option:

```sh
H668_PYTHON=/Users/alec/Documents/tmp/hadamard-env/bin/python
```

Run the memory-intensive audits sequentially.  The largest observed
resident set was 1.86 GB.

## 1. Canonical primitive factors

```sh
/usr/bin/time -l "$H668_PYTHON" \
  lp333_shell_two_primitive_units/audit_primitive_degenerate.py \
  --scope h2 \
  --factor 0 --factor 1 --factor 2 \
  --output \
  lp333_shell_two_primitive_units/h2_factors_0_2_certificate.json
```

Expected:

```text
channel_factor_audits=30
total_primitive_zero_assignments=0
semantic_sha256=e424fbcb8b9b7808d45dc095c22fef246a18f6c8cfee2e499b68af6e4c085816
reference wall=615.73 s
reference max RSS=1,850,195,968 bytes
```

```sh
/usr/bin/time -l "$H668_PYTHON" \
  lp333_shell_two_primitive_units/audit_primitive_degenerate.py \
  --scope h2 \
  --factor 3 --factor 4 --factor 5 \
  --output \
  lp333_shell_two_primitive_units/h2_factors_3_5_certificate.json
```

Expected:

```text
channel_factor_audits=30
total_primitive_zero_assignments=0
semantic_sha256=b3615a722e65b437edebf886bfdc5c4c54f81acca81656f974b8e41613e1fc34
reference wall=432.34 s
reference max RSS=1,835,106,304 bytes
```

## 2. A-star seeds needed for full action closure

```sh
/usr/bin/time -l "$H668_PYTHON" \
  lp333_shell_two_primitive_units/audit_primitive_degenerate.py \
  --scope h2_astar --channel A \
  --factor 0 --factor 1 --factor 2 \
  --factor 3 --factor 4 --factor 5 \
  --output \
  lp333_shell_two_primitive_units/h2_astar_a_all_factors_certificate.json
```

Expected:

```text
channel_factor_audits=30
total_primitive_zero_assignments=0
semantic_sha256=743087674c409ced113b3a298fe140a74295045255c25ccc17930b0c2ea51525
reference wall=749.69 s
reference max RSS=1,856,667,648 bytes
```

## 3. Independent maximal-case replay

```sh
/usr/bin/time -l "$H668_PYTHON" \
  lp333_shell_two_primitive_units/replay_maximal_hash_filter.py \
  --output \
  lp333_shell_two_primitive_units/maximal_hash_replay_certificate.json
```

Expected:

```text
physical_hash_intersections=0
positive_control=true
semantic_sha256=95a229cbf7661182d09bd033c612f1e4419aa5ded62f344b11425c1218a683a0
reference wall=38.64 s
reference max RSS=1,583,038,464 bytes
```

## 4. Exact physical-margin plus T1/T2 convolution

```sh
/usr/bin/time -l "$H668_PYTHON" \
  lp333_shell_two_primitive_units/audit_margin_t12_convolution.py \
  --output \
  lp333_shell_two_primitive_units/h2_margin_t12_certificate.json
```

Expected:

```text
profiles=5
targets=405
targets_excluded=0
total_margin_assignments=1538710506610661125476
total_t1_t2_survivors=1123966766238638605
semantic_sha256=23946700aa96c5d8088dfb346172e38dbf74d59c9e185e29ba3fca8d34d8150b
reference wall=4.86 s
reference max RSS=156,712,960 bytes
```

## 5. Detached 84-image action closure

The preceding four certificate files must be present.

```sh
/usr/bin/time -l "$H668_PYTHON" \
  lp333_shell_two_primitive_units/verify_action_closure.py \
  --output \
  lp333_shell_two_primitive_units/h2_84_image_action_closure_certificate.json
```

Expected:

```text
formal_profile_images=84
physical_lift_orbits=10
base_channel_factor_audits=90
primitive_zero_assignments=0
all_six_primitive_factors_nonzero_per_channel=true
semantic_sha256=d89f8fce094dfc826749489a5dbff72f657ef07687a7f3e2eb1e25f5db0ed516
reference wall=0.05 s
reference max RSS=24,068,096 bytes
```

## 6. File-integrity check

From the scratch directory:

```sh
cd lp333_shell_two_primitive_units
shasum -a 256 -c SHA256SUMS
```

The semantic hashes are invariant under runtime timing differences.  The
file hashes pin this exact release package.
