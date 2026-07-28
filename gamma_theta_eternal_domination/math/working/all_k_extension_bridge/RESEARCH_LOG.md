# Research log

## 2026-07-28 (PDT)

- Read C-108, the all-\(k\) frozen-color projection, C-051, the accepted
  full-target propagation note, and the C-109 inactive-set boundary.
- Tested the hoped-for universal induction at its exact missing step:
  choosing one deletion \(k\)-coloring whose inactive set omits a color.
- Proved the inactive-link suspension theorem.  For an inactive vertex
  \(r\), the frozen projection contains
  \(\{x\}\cup N_{\overline G}(r)\); minimum-counterexample minimality makes
  that entire induced subgraph exactly \((k-1)\)-colorable.
- Checked that this consumes the available local induction hypothesis but
  does not synchronize the independently chosen local colorings.
- Reverified the accepted positive graph `Ksv`f\knJVis` using a new
  standalone ordinary-bitset program.  Its greatest eternal triple-family
  has 127 states and a full response at \(S=\{1,2,3\}\), \(x=0\).  Of the
  12 deletion three-colorings, six use two colors and six use all three
  colors on the C-108 inactive set \(\{6,8,10,11\}\).
- Built a normalized SAT discovery formula for a stronger
  equality-critical positive control.  CaDiCaL 3.0.1 returned UNSAT at
  orders 9 through 14; the order-14 instance had 14,498 variables and
  37,104 clauses.  These runs have no proof logs or independent
  reconstruction and remain OBSERVED.
- The same formula with the blocked deletion coloring removed returned
  UNSAT through order 12.  This ablation also remains OBSERVED.

Reproduction commands:

```text
python3 -I -B -W error \
  math/working/all_k_extension_bridge/verify_positive_control.py

python3 -I -B -W error \
  math/working/all_k_extension_bridge/search_k3_control.py \
  --order 14 \
  --solver tools/cadical_3_0_1/build/cadical
```
