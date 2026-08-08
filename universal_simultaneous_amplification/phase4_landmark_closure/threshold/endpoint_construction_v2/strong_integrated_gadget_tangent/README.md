# Strong integrated-gadget tangent audit

This folder studies a fixed weighted gadget embedded in a large unit clique.
For clique order `C`, internal gadget edge `ij` has weight `C*a_ij`, while
gadget vertex `i` has an edge of weight `x_i` to every clique vertex.  The
calculation retains the order-`1/C` effect of ordinary clique singleton
starts; omitting that term gives false candidate amplifiers.

## Exact results

1. `STRONG_GADGET_TANGENT.md` derives the limiting local chains and the full
   Bd/dB tangent coefficients, including the far-field Poisson response.
2. `verify_integrated_lumping.py` compares the finite orbit transition rows
   against an independently constructed labelled graph, exactly, for all
   states under both update rules.
3. `verify_far_field_algebra.py` certifies the two far-field source terms and
   the core Poisson-response identity symbolically.
4. `verify_portal_clone_obstruction.py` proves, for arbitrary gadget order
   and arbitrary positive portal loads with zero leading internal weights,

   ```text
   B_H = 0,
   D_H = -sum_i (x_i-1)^2/(1+(r-1)x_i) <= 0.
   ```

   Equality holds exactly when every portal load is one.

The exact obstruction is deliberately scoped to the portal-clone boundary.
The sign for a genuinely interacting arbitrary finite gadget remains open.

## Discovery search

`search_integrated_gadgets.py` optimizes complete symmetric gadgets of orders
3--7 with independent logarithmic internal weights and portal loads.  It uses
the full coefficient formula from `integrated_gadget.py` and mixes in the
optimal nonnegative amount of the inherited ordinary-leaf tangent.

At fitness `1.51`, `1.55`, and `2`, no positive balanced coefficient was
found.  The optimizers approach either the exact portal-clone equality class
or the previously classified rare-pair boundary.  This is numerical evidence,
not a global optimization certificate.

## Replay

From this directory, run:

```sh
./replay.sh
```

The replay runs only exact/symbolic checks.  A bounded discovery smoke test is
available separately:

```sh
../../../../../.venv/bin/python search_integrated_gadgets.py \
  --orders 3 --fitnesses 1.51,1.55,2 --budget 100 --bound 8
```
