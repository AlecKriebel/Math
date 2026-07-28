# Independent evidence ledger

Date: 2026-07-28 (PDT)

## Verdict encoded by the evidence

The revised candidate receives an `UNCONDITIONAL PASS`.  The clean-room
computational audit passes; the human theorem audit accepts Proposition
1.1, revised Proposition 1.2, Lemma 2.1, Corollary 2.2, and Theorem 3.1.
The revision explicitly restores the immediate false-constant branch that
was missing from the original terminal inventory.

## Clean-room checker

Command:

```text
python3 -I -B -W error \
  reviews/singleton_buffer_hostile/independent_check.py
```

Checker SHA-256:

```text
b685f5b9fce2a1e74b3643888ad5bb5d2ee10c97e915dca29f47882a4cd1412f
```

Successful stdout SHA-256:

```text
8a5ef8879edc31ab91d0b7f7097a6683c51687e9d5870f1206a367b49d5f2e74
```

The checker:

- verifies the candidate manifest against all five frozen source files;
- binds the current bytes of C-069, C-075, C-079, C-082, and C-094;
- exhausts all 21 unordered pairs of nonempty proper three-color lists;
- confirms the local list-forcing truth tables in Lemma 2.1;
- decodes both graph6 records without a candidate import;
- computes exact \(\gamma,i,\alpha,\theta\);
- proves \(\gamma^\infty=3\) from \(\alpha=3\) and an explicitly replayed
  eternal triple-family;
- rebuilds the 13-vertex greatest triple kernel by simultaneous deletion;
- checks all 1,444 one-guard obligations;
- recomputes every response list;
- counts compatible response-list colorings;
- reconstructs the full omitted-color components, parities, paths, ports,
  caps, and sealing incidences.

## Exact independent outputs

### `EEv?`

```text
order=6
size=7
connected=false
parameters=(3,3,3,3,3)
selected_family_size=8
unoccupied_attack_obligations=24
lists=3:01,4:01,5:1
sealed_0_positive_vertices=3,4
singleton_buffer=5
list_coloring_count=1
edge_list_sha256=8882f4fdeacfac5578850fb01fc0e0a248cbe4f6d64ed2e1af360e2afa11aca6
response_certificate_sha256=8c9aefcaf68bd53d1ddcc59272c204e9c716e2a12fa06d719e64cf3dd4077a38
```

### `LFzJbZYhdrDZdM`

```text
order=13
size=43
connected=true
parameters=(3,3,3,3,3)
dominating_triples_before_kernel=144
simultaneous_deletion_rounds=2
greatest_family_size=142
unoccupied_attack_obligations=1420
lists=3:01,4:12,5:01,6:12,7:12,8:01,9:02,10:02,11:2,12:0
dynamic_ports=3/type2,4/type0
free_components=3-5-8,4-6-7
sealed_singleton_caps=11/color2,12/color0
list_coloring_count=2
edge_list_sha256=2f34381f05c98243d52e5b370d1af25df7380338aed4d53da2dd85a49b707b1e
greatest_family_sha256=6afa4f7e4b50715d55f62d475267832db52f3419b7394e39dbdc14ecdcdbd1f9
response_certificate_sha256=67cccdda55073b70211ae05599ce736d126a2bab97dd68ff951acf460a984ccd
```

The simultaneous deletion entry means two states are deleted in the first
round; the surviving family is already stable.

## Revised logical test

Proposition 1.1 admits a fixed-component substitution that yields the
formula

```text
false
```

This formula is inclusion-minimal unsatisfiable and has neither units nor
an implication path.  Revised Proposition 1.2 now classifies it exactly as
case 1, an immediate projection-internal parity or fixed/fixed collision
certificate outside the C-075 trichotomy.  The top-level summary and
Section 5 retain the same branch, so the prior negative test now passes.
