# Reproducing the pair-resultant norm package

Run from:

```sh
cd /Users/alec/Documents/Math-h668-local/hadamard_668_search
```

Use the repository Python environment:

```sh
H668_PYTHON=/Users/alec/Documents/tmp/hadamard-env/bin/python
```

## 1. Pure field theorem

```sh
"$H668_PYTHON" \
  lp333_shell_two_pair_resultant_norm/verify_ratio_resultant_norm.py
```

Expected:

```text
channel_pair_resultant_norms_equal=true
pair_norm_key_space=101029443456638735128
semantic_sha256=4e4cdb32d2e54e8b402e71dc4e7adbdce4dec6fbe0c3a1e076fa98ed1338cf9a
```

## 2. Export the exact physical alphabets

```sh
"$H668_PYTHON" \
  lp333_shell_two_pair_resultant_norm/export_character_instances.py
```

Expected:

```text
cases=15
binary_bytes=211681
theta_power_relation=49,106,41,147,88,81,154,65,8,14,159,21
```

## 3. Compile the exact degree-12 verifier

```sh
clang++ -O3 -std=c++17 -Wall -Wextra -pedantic \
  lp333_shell_two_pair_resultant_norm/joint_character_audit.cpp \
  -o /tmp/h668_joint_character_audit
```

## 4. Cross-check the compiled field

```sh
"$H668_PYTHON" \
  lp333_shell_two_pair_resultant_norm/verify_character_field_bridge.py \
  --helper /tmp/h668_joint_character_audit
```

Expected:

```text
compiled_repository_probe_agreements=45
all_agree=true
```

## 5. Complete marginal character images

Run the three commands sequentially:

```sh
/tmp/h668_joint_character_audit \
  lp333_shell_two_pair_resultant_norm/character_instances.bin \
  2 100 pairmargins

/tmp/h668_joint_character_audit \
  lp333_shell_two_pair_resultant_norm/character_instances.bin \
  83 3000 pairmargins

/usr/bin/time -l /tmp/h668_joint_character_audit \
  lp333_shell_two_pair_resultant_norm/character_instances.bin \
  28057 700000 pairmargins
```

Expected final summaries:

```text
d=2:     complete_cases=15/15, total_samples=52
d=83:    complete_cases=15/15, total_samples=8286
d=28057: complete_cases=15/15, total_samples=4843905
```

Every case must report respectively:

```text
marginal_values=6/6
marginal_values=249/249
marginal_values=84171/84171.
```

Reference for `d=28057`:

```text
wall_seconds=547.030744
max RSS=4,046,848 bytes
```

## 6. Pair-triple affine ranks

```sh
for H668_ORDER in 2 83 28057; do
  /tmp/h668_joint_character_audit \
    lp333_shell_two_pair_resultant_norm/character_instances.bin \
    "$H668_ORDER" 100 pairspan
done
```

Expected for each order:

```text
complete_cases=15/15
affine_rank=3/3 in every case.
```

## 7. Negative joint-character controls

```sh
/tmp/h668_joint_character_audit \
  lp333_shell_two_pair_resultant_norm/character_instances.bin \
  2 2000 joint

/tmp/h668_joint_character_audit \
  lp333_shell_two_pair_resultant_norm/character_instances.bin \
  3 30000 joint
```

Expected:

```text
d=2: complete_cases=15/15, 64/64 signatures per case
d=3: complete_cases=15/15, 729/729 signatures per case.
```

## 8. Weaker total-product controls

```sh
for H668_ORDER in 2 83 28057; do
  /tmp/h668_joint_character_audit \
    lp333_shell_two_pair_resultant_norm/character_instances.bin \
    "$H668_ORDER" 700000 product
done
```

Expected:

```text
all 15 cases complete for all three orders;
order 28057 total_samples=4627568.
```

The order-28,057 product control used 186.23 seconds and about 2.75 MB RSS.
The pair-marginal audit is the mathematically stronger result.
