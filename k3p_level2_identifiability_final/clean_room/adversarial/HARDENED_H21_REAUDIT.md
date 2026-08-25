# Hardened H21 Clean-Room Re-Audit

Audit timestamp: 2026-08-24 22:53 PDT

Final status: **PASS — zero remaining hardening gaps in the assigned scope**

Completion estimate: **100%**

## Verdict

The final hardened verifier closes both defects from the first adversarial audit:

- optimized Python cannot import or execute the verifier; and
- every directed-rank obstruction now binds the claimed rank to its square minor and independently reconstructs the target projection's 10- or 12-generator upper bound.

During the re-audit I found one intermediate control blocker: `verify_all(run_certificates=False)` skipped all algebraic certificates yet emitted the full terminal PASS sentinel. The parent repaired that control while this audit was active. The final verifier now rejects the false control at function entry, before work and without a terminal sentinel.

After that patch, all 25 ordinary mutations, three optimized-mode controls, five one-byte active-input mutations, the full fourteen-orbit gate, the regression, and the historical-failure replay behave correctly. I found no remaining objection in the assigned H21/fourteen-orbit hardening scope.

## Exact audited versions

```text
bf69fce87b26376597efa1be221fe7b8ddc303b4054c6ee22fa861e781d2051a  verify_h21_transport_and_fourteen_orbits.py
aa3a97442854d7df8b6d4b3bfa02e9f2d18d4eaa4a0838fdd33738e00ea6a063  test_h21_transport_regression.py
d49cb601c7f8a33dd6f07acd7005bc2f45efa9a3e6a4f0dc42fa36e8d4c13695  replay_historical_failure.py
ee5e29a2cd795d9389e8e1257ebdb9eeaa4256fb5d03e07f230bf82ba555ef91  HISTORICAL_cleanroom_verify_fourteen_orbits.py
f85c1a77ee88ab265b5a6d0adab80c45ff5642c3c1258aa991d7b94a1c3c5816  reproducibility/exact_four_port.py
d31411837ca739411962a572a361c789ac80a73ca6c5276884edefa005046f0a  adversarial/hardened_cleanroom_reaudit.py
```

The first hardened version inspected during this re-audit had SHA-256 `becacec117734248047cded6f84d5996ad91c7531be36b1d8db8eec57653740b`. It contained the certificate-skip control defect. The verdict in this report applies only to final hash `bf69fce8...`.

## Full-gate replay

The ordinary final gate exited 0 and reached both new terminal lines:

```text
PASS five independently reconstructed directed-rank upper bounds
CLEANROOM_K3P_H21_TRANSPORT_AND_FOURTEEN_ORBITS_PASS
```

The regression exited 0 at

```text
H21_01_TRANSPORT_REGRESSION_PASS
```

Instrumentation around the final full gate recorded exactly 52 physical-edge Fourier transport calls:

```text
38 raw orbit members + 14 representative repeats = 52
```

Thus the hardened loop now checks every raw-member coordinate action, not only each canonical representative.

The returned diagnostics contain five reconstructed rank upper-bound records. The gate also replays the nine polynomially separated orbits and the two pre-lock sink-swap quartics before emitting the full sentinel.

## Optimized-mode closure

Three independent controls were executed:

| Control | Exit | Result |
|---|---:|---|
| `python -O` on the full verifier | 1 | rejected during import |
| `python -O` on the old optimized bypass probe | 1 | rejected while importing the verifier |
| `PYTHONOPTIMIZE=1` on the full verifier | 1 | rejected during import |

Each reports

```text
certification verifier refuses optimized Python
```

Neither the full PASS sentinel nor the old `OPTIMIZED_ASSERT_BYPASS_CONFIRMED` sentinel is emitted. The verifier contains no remaining `assert` statements; its gates use the non-optimizable `require`/`CertificationError` path.

## Active-input hash binding

Every JSON input read by the verifier passes through one byte-binding loader. The embedded registry is exactly these five active files:

```text
61d88a67b487ebbee1cae881def23fdce770d4fa0cac0d6b86be02e7368438a3  K3P_14_ORBIT_LOCK.json
5e7bf1599f2a28858b2dbce3993baf6adea9e27cef9ffa8d23503200742d0a5e  k3p_prelock_source5_quartic.json
41c3c9756536a28b9fc24250c62491e10322e66c0bd4c4b692e939aade2395c0  k3p_h14_marginal_orbit_certificates.json
8ee39cd08a01f9e9dd385e41bbab4814f7e0859f143aceda4e8831ddba053f61  k3p_remaining_quartic_separators.json
fa0ac74cde903edc422a90b5e490bd639b2e2b4c758d9d3ec10a794f1a044f42  k3p_directed_rank_obstructions.json
```

For each file, the re-audit substituted a payload with one extra byte while leaving the expected digest untouched. All five were rejected with `active input hash mismatch` before JSON parsing. No alternate unbound JSON read path remains in the verifier.

## Port, incoming-role, repair, and raw-orbit mutations

The following mutations all fail under ordinary Python:

| Mutation | Gate that rejects it |
|---|---|
| `port_permutation` disagrees with `representative_permutation` | explicit permutation binding |
| source incoming role changed | reconstructed source role binding |
| target incoming role changed | `selected-port-{p(0)}` binding |
| source repair index changed | independently enumerated source repair |
| target repair index changed | independently enumerated target repair |
| one raw member and witness omitted | exact double-coset equality |
| duplicate raw member inserted | exact double-coset equality |
| raw witness omitted | witness-set coverage |
| displayed-target automorphism used in base-target frame | base-group membership |
| identity coordinate action substituted for nonidentity H21 relation | exact physical-edge Fourier transport |

The original H21 diagnosis remains unchanged: root-suppressed mixed groups, base/displayed target conjugation, and all raw records pass. The untouched historical rooted-DAG failure remains exactly reproducible.

## Rank-minor hardening

The formerly accepted fictitious mutation

```text
source rank 101 > target upper bound 100 = target rank 100
```

with only the original `11x11` and `10x10` minors is now rejected immediately because each claimed rank must equal both the row and column counts of its square minor.

The re-audit also verified rejection of:

- an `11x10` source minor;
- a rank-10 target minor with nine rows;
- a target upper-bound integer changed from 10 to 11;
- altered H21 generator and saturation names;
- a source/target map-hash direction swap;
- an altered absent-generator list;
- an out-of-range sunlet omitted port; and
- an unknown upper-bound mechanism.

The five final exact inequalities are

```text
H21-02   11 > 10
L20-02   14 > 12
L21a-02  11 > 10
L21b-02  11 > 10
L23-01   14 > 12
```

For each, a target minor of the reconstructed upper-bound size is also nonzero, so the target projection rank equals—not merely lies below—the claimed number.

## Target upper-bound noncircularity

### H21-02

The H21 routine starts with the independently compiled, map-hash-bound target descriptor. It hard-codes ten rational functions

```text
U, V, Z, D, I, A0, B0, A, B, rho
```

and verifies eleven exact sparse-polynomial cross-multiplication identities for the eleven selected target observables. The denominator open set is defined by `e2C*e2G*D*I != 0`; at the strict rational target point its minimum saturation value is `1696/17955 > 0`.

The re-audit replaced both rank-certificate dictionaries and the stated target upper bound with unrelated values `999`, `998`, and `997`, then called the target factorization alone. It still reconstructed exactly ten generators and eleven zero polynomial identities. Therefore the upper-bound calculation does not read or infer itself from the target minor or claimed dimension.

On the nonempty saturation open set, each selected coordinate is rational in those ten functions, so the target projection closure has dimension at most ten. The nonzero target `10x10` minor gives the matching lower bound.

### Ordinary-sunlet cases

For each of the other four rank records, the verifier:

1. derives the marginal directly from the independently compiled target descriptor;
2. collapses only edge classes whose exact exponent signatures agree;
3. exhaustively searches all edge maps, inheritance flips, and three-port permutations;
4. requires exact sparse-polynomial equality with a canonical ordinary-sunlet map; and
5. counts the composite `A/B/U/V` generators occurring in the selected observables.

Again, poisoning all rank conclusions leaves the reconstructed counts unchanged at `12,10,10,12`.

The adversarial driver separately rebuilt the ordinary-sunlet formulas in twelve independent composite variables and computed their actual monomial occurrence support. Those independent support counts exactly match the hardened gate. This specifically tests against a hand-coded dependency-set undercount.

Finally, the separate standard-library implementation `reproducibility/exact_four_port.py` at hash `f85c1a77...` independently returns the same five inequalities and generator counts.

I found no circular dependency on the claimed rank, target minor, or stored upper-bound integer.

## Certificate-skip control

The intermediate hardened hash allowed this unsafe call:

```python
verify_all(run_certificates=False)
```

to emit the full terminal sentinel. The final verifier fixes the issue at [verify_h21_transport_and_fourteen_orbits.py](/Users/alec/Documents/Math/k3p_level2_identifiability_final/clean_room/verify_h21_transport_and_fourteen_orbits.py:1680): it requires the argument to be exactly `True` before any topology work begins.

The adversarial rerun confirms that `False` raises `CertificationError`, emits no topology PASS lines, and cannot emit the full sentinel. The command-line entry point and regression both call the full mode explicitly.

## Accounting

```text
25 / 25 ordinary mutations rejected
 3 /  3 optimized controls rejected
 5 /  5 active input byte mutations rejected before parse
 5 /  5 target upper bounds independently reconstructed
52 / 52 expected Fourier transport calls reached
```

The historical H21 failure remains preserved and replayable.

## Exact remaining gaps

None in the assigned hardened clean-room scope. This verdict is tied to final verifier SHA-256 `bf69fce87b26376597efa1be221fe7b8ddc303b4054c6ee22fa861e781d2051a`.

## Replay commands

```text
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python clean_room/verify_h21_transport_and_fourteen_orbits.py
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python clean_room/test_h21_transport_regression.py
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python clean_room/replay_historical_failure.py
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python clean_room/adversarial/hardened_cleanroom_reaudit.py
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -O clean_room/verify_h21_transport_and_fourteen_orbits.py
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -O clean_room/adversarial/optimized_bypass_probe.py
```

The adversarial driver exits 0 only after printing

```text
HARDENED_CLEANROOM_ADVERSARIAL_REAUDIT_PASS
```
