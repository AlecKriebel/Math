# Adversarial H21 Audit

Audit timestamp: 2026-08-24 22:04 PDT

Status: **H21 mathematical transport PASS; unconditional clean-room PASS not yet justified**

Completion estimate: **100% of the assigned adversarial audit**

## Bottom line

I found no mathematical counterexample to the repaired H21 transport. An independent role-preserving, arrowhead-preserving mixed-graph implementation confirms:

- the historical verifier uses the wrong rooted graph category;
- the recorded target witnesses are in base-target coordinates and require conjugation on a displayed representative;
- the H21-01 source and base target groups are exactly `{id,(0 2)}`;
- the four frozen H21-01 raw members are exactly one double coset;
- the six nonisomorphic H21 classes and the single omitted isomorphic class partition all of `S4`; and
- the Fourier coordinate rule is exact for every one of the 24 port permutations, not only the stored representative.

The prior audit's unconditional `PASS` and “no remaining gaps” language nevertheless needs qualification. I found two high-priority certification defects:

1. Every gate in the corrected verifier is a Python `assert`. Under `python -O` or `PYTHONOPTIMIZE`, the verifier accepts a deliberately truncated three-member H21-01 orbit and still returns the reconstructed four-member coset.
2. The five directed-rank replays recompute nonzero source and target minors but do not reconstruct the claimed target rank upper bounds. They also do not bind the JSON `rank` values to the minor sizes. A mutated H21-02 certificate claiming `101 > 100 = 100` while retaining only the original `11x11` and `10x10` minors is accepted under ordinary Python.

These are certification defects, not discovered counterexamples to the locked K3P classification. A separate standard-library replay currently verifies the missing ten-/twelve-generator factorizations, but that does not change what the corrected clean-room verifier itself checks.

## Audit boundary and immutable files

No parent clean-room file, root log, manifest, or input was edited. All new files are under `clean_room/adversarial/`.

The audited hashes are:

```text
ee5e29a2cd795d9389e8e1257ebdb9eeaa4256fb5d03e07f230bf82ba555ef91  HISTORICAL_cleanroom_verify_fourteen_orbits.py
ee5e29a2cd795d9389e8e1257ebdb9eeaa4256fb5d03e07f230bf82ba555ef91  input_frozen/.../cleanroom_verify_fourteen_orbits.py
472377b87cfbfd21ac33a770b506630a12ad1ee0afc8c72be203b8f6a9770003  verify_h21_transport_and_fourteen_orbits.py
e78e87be8fa0b2d697efb36364ff55f057f024500aca635ca5a6e504e3a6dafe  test_h21_transport_regression.py
61d88a67b487ebbee1cae881def23fdce770d4fa0cac0d6b86be02e7368438a3  K3P_14_ORBIT_LOCK.json
3d58e5361a6cc266bbf3411a3e12c39a6fe235968b3ef0b59e7ea5dbcae61af2  adversarial_h21_audit.py
85ddf76993d6e53d5eafcbfe89c4131374f76c33fe5c3a70d2c8603790fbf279  optimized_bypass_probe.py
```

The prior audit's five immutable input hashes were independently recomputed and match its JSON exactly.

## Independent method

The topology replay does not use the corrected verifier's custom isomorphism backtracker. It parses the frozen literal graphs, independently performs the fixed one-root suppression, and converts every mixed edge into a colored incidence gadget:

- original vertices retain exact role and port label;
- an edge has a separate edge vertex;
- each endpoint has a headed or plain incidence vertex; and
- NetworkX 3.5 independently performs the resulting colored graph isomorphism.

This construction makes an endpoint arrowhead part of incidence, rather than comparing node-name-containing edge attributes.

Every audited standard binary mixed graph satisfied the independently checked incidence identities

```text
leaf          degree 1, arrowhead incidence 0
tree vertex   degree 3, arrowhead incidence 0
reticulation  degree 3, arrowhead incidence 2
```

Thus the corrected `MixedGraph` object's omission of an explicit role field does not enlarge automorphism groups on this corpus: roles are derivable from exact degree/arrowhead incidence. Independent role-preserving groups agreed with the corrected groups for all fourteen sources, base targets, and displayed targets.

Fourier transport was checked by a second implementation. It evaluates every switching directly with `Fraction` arithmetic on physical rooted arcs at a strict rational K3P point, then compares all 64 conserved coordinates after every element of `S4`. Those values were also compared with the corrected verifier's exact symbolic physical-edge expressions.

## Historical failure replay

The preserved historical code is byte-for-byte identical to the frozen code. Its wrapper reproduced the exact first failure:

```text
AssertionError: ('source automorphism', 'H21-01',
 {'permutation': [2, 1, 3, 0],
  'source_automorphism': [2, 1, 0, 3],
  'target_automorphism': [0, 1, 2, 3]})
HISTORICAL_H21_01_FAILURE_REPRODUCED_EXACTLY
```

This is not a false answer by the old rooted-DAG isomorphism routine. The nontrivial port symmetry is genuinely absent before root suppression.

## Root suppression, roles, and arrowheads

For H21-01, independent suppression gives the eleven mixed edges reported in the prior audit. The four headed incidences are exactly

```text
S--V       arrowhead at V
sub4--V    arrowhead at V
U--X       arrowhead at X
sub3--X    arrowhead at X
```

The suppressed root edge is `incoming--S` with no arrowhead. Each reticulation therefore has exactly its two required incoming arrowheads.

The nontrivial mixed automorphism is uniquely realized on the named vertices by

```text
S                    <-> sub4
incoming port leaf   <-> segment-4 port leaf
all other vertices   fixed
```

It maps `S--V` to `sub4--V`, maps `S--U` to `sub4--U`, preserves every headed endpoint, and induces port permutation `(0 2) = [2,1,0,3]`. It cannot be a rooted automorphism because the incoming leaf and `S` are separated by the chosen root before suppression.

The independently computed groups are:

```text
rooted DAG port group              { id }
root-suppressed mixed port group   { id, (0 2) }
```

If arrowheads are forgotten while explicit roles remain, the same two-element group results. If both arrowheads and the derived internal roles are forgotten, the underlying untyped graph admits two extra false port symmetries, `(1 3)` and `(0 2)(1 3)`. This confirms why the corrected representation must retain exact arrowheads if it chooses to infer roles from them.

## Target-coordinate conjugation

For H21-01, the representative is `p=(2 3)`. The base-target automorphism `(0 2)` becomes

```text
p (0 2) p^-1 = (0 3) = [3,1,2,0]
```

on the displayed target. Applying base `(0 2)` directly to the displayed target fails, exactly as the repaired regression says.

The formula order was independently disambiguated on non-involutive representatives, where `p a p^-1` and `p^-1 a p` differ:

| Orbit | Correct direct displayed auto | Wrong opposite conjugate |
|---|---|---|
| `H21-03`, `p=[0,2,3,1]` | `[3,1,2,0]` | `[1,0,2,3]` |
| `H21-04`, `p=[0,3,1,2]` | `[1,0,2,3]` | `[3,1,2,0]` |

The direct mixed-graph computation contains the correct conjugate and excludes the wrong one in both cases.

## Double cosets and raw H21-01 coverage

Using base groups on both sides, the H21-01 double coset is exactly

```text
[0,1,3,2]
[2,1,3,0]
[3,1,0,2]
[3,1,2,0]
```

All four frozen witness equations were independently recomputed. Omitting any member and its witness is rejected in ordinary mode.

Using the displayed target group in the double-coset formula is a concrete counterexample to the wrong frame: it produces only two members for H21-01 and misses half the frozen raw class.

Enumerating all 24 permutations yields seven double cosets. Six are exactly the frozen H21-01 through H21-06 raw sets. The seventh is the isomorphic group itself,

```text
{ [0,1,2,3], [2,1,0,3] }.
```

No raw H21 record is missing or duplicated.

## Fourier-coordinate transport

For a relabelling `p` that maps old port `i` to displayed port `p(i)`, the independent evaluator confirms

```text
q^(G^p)_a = q^G_b,  b_i = a_{p(i)}.
```

Checks completed:

- all 24 permutations in `S4`;
- all 64 conservation-supported K3P coordinates per permutation;
- exact rational switching evaluation at a strict physical K3P point with minimum margin `23/211`;
- exact comparison with the corrected symbolic physical-edge expressions; and
- all four H21-01 raw permutations, not only the representative.

No coordinate-order, inverse-permutation, inheritance-parent, or physical-edge mismatch was found.

## Mutation campaign

The following mutations were rejected under the documented ordinary runtime:

| Mutation | Result |
|---|---|
| Omit one H21-01 raw member and witness | rejected |
| Use the false untyped/no-arrowhead `(1 3)` source symmetry | rejected |
| Supply a displayed-target automorphism in a base-target witness field | rejected |
| Replace the H21-01 representative by identity | rejected |
| Corrupt one raw witness equation | rejected |
| Replace the nontrivial Fourier transport by the identity map | rejected |

Three ordinary-mode metadata/certificate mutations were accepted:

| Mutation | Result and significance |
|---|---|
| Change `port_permutation` while leaving `representative_permutation` intact | accepted; redundant representative metadata is unbound |
| Change `target_incoming_role` while leaving the literal graph intact | accepted; redundant incoming-role metadata is unbound |
| Set H21-02 rank fields to `101 > 100 = 100` while retaining only its `11x11` and `10x10` minors | accepted; rank labels and the upper-bound mechanism are not checked |

The first two do not alter the actual bound literal graph or computed representative, so they are low-severity input-binding defects. The third is substantive certification evidence that the directed-rank “upper bound” replay is incomplete.

### Optimized-mode bypass

This command deliberately supplies only three of the four H21-01 members:

```text
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -O clean_room/adversarial/optimized_bypass_probe.py
```

It exits 0 and prints

```text
OPTIMIZED_ASSERT_BYPASS_CONFIRMED claimed=3 reconstructed=4
```

Because Python optimization removes `assert` statements before execution, the verifier is not fail-closed unless optimized mode is explicitly refused.

## All fourteen orbits

The H21 repair did not skip the current ordinary-mode loops. The adversarial replay independently checked:

- 14 source/displayed-target mixed nonisomorphisms;
- 14 source, 14 base-target, and 14 displayed-target automorphism groups;
- all 38 raw-member double-coset assignments and witness equations;
- five transported H14 quartics plus four remaining exact quartics;
- five source and target exact Jacobian minors; and
- a disjoint `5 + 4 + 5 = 14` certificate partition.

The nine polynomial separations are completely replayed by the corrected verifier: target pullbacks vanish identically, source pullback hashes match, strict source points are checked, and source evaluations are exact and nonzero.

For the five rank separations, the corrected verifier recomputes the source and target minors and physical margins. It does not prove that the target projection has no larger rank. Its line

```text
source certificate rank > target_dimension_upper_bound == target certificate rank
```

only compares three JSON integers. A nonzero target minor is a lower bound; it cannot establish the required upper bound.

As auxiliary evidence, I executed the current standard-library `reproducibility/exact_four_port.py` at SHA-256

```text
f85c1a77ee88ab265b5a6d0adab80c45ff5642c3c1258aa991d7b94a1c3c5816
```

It independently replays the missing H21 ten-generator factorization and ordinary-sunlet compressions and obtains

```text
H21-02   11 > 10
L20-02   14 > 12
L21a-02  11 > 10
L21b-02  11 > 10
L23-01   14 > 12
```

So I found no underlying rank counterexample. The objection is specifically to the corrected clean-room verifier's claim to have replayed those upper bounds.

## Two pre-lock sink swaps

The two locked permutations are distinct:

```text
[0,1,3,2]
[1,0,2,3]
```

For each, the independent mixed-graph engine confirms source/target nonisomorphism. The corrected exact algebra verifies:

- literal graph and canonical map hashes;
- identically zero target quartic pullback;
- matching nonzero source pullback hash;
- exact strict-domain source point; and
- exact nonzero source evaluation.

No bypass or direction reversal was found in these two records.

## Required repairs before unconditional PASS

1. Add an explicit optimized-mode refusal before any verifier work, for example:

   ```python
   if not __debug__:
       raise RuntimeError("certification verifier refuses optimized Python")
   ```

   Prefer non-assert terminal `require` checks for long-term fail-closed behavior.

2. Add the exact H21 ten-generator factorization and 12-/10-generator sunlet compression checks to the corrected clean-room rank replay. Assert

   ```text
   claimed rank = number of minor rows = number of minor columns
   claimed target upper bound = independently reconstructed generator count
   source minor size > target generator count
   ```

3. Bind `port_permutation == representative_permutation` and reconstruct/bind the incoming-role strings, or stop claiming those redundant strings are independently checked.

4. Bind expected SHA-256 values for the lock and certificate inputs in the verifier or its mandatory runner. The current comparison of the in-memory lock with a second read of the same path is tautological as an immutable-input check.

5. For maximal correspondence with the mission wording, retain the adversarial all-`S4` Fourier-transport loop or explicitly replay every one of the 38 raw-member coordinate transports in the corrected gate.

## Residual gaps

- No residual mathematical gap remains in the assigned H21 root suppression, arrowheads, labelled ports, automorphism groups, target conjugation, double cosets, raw H21-01 coverage, or Fourier transport.
- The corrected clean-room verifier has the two high-priority certification gaps above and should not retain unconditional `PASS` / empty-gap language until they are repaired and rerun.
- The underlying five target rank upper bounds currently have separate exact replay evidence; they are not disproved by this audit.

## Replay commands

```text
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python clean_room/replay_historical_failure.py
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python clean_room/verify_h21_transport_and_fourteen_orbits.py
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python clean_room/test_h21_transport_regression.py
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python clean_room/adversarial/adversarial_h21_audit.py
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -O clean_room/adversarial/optimized_bypass_probe.py
```

The adversarial driver terminates with

```text
ADVERSARIAL_H21_AUDIT_EXECUTED
```

under ordinary Python and refuses to run its own audit under optimization.
