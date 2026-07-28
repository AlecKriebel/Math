# C-097 replay

From the campaign directory, run:

```text
python3 -I -B -W error repro/c097/replay.py
```

The wrapper checks the frozen artifact hashes, reconstructs and strictly
replays the four-neutral RUP certificate, independently verifies the sharp
three-neutral equality control, then reconstructs the complete residual
formula and replays both retained proof forms.  It also checks the exact
coverage truth tables and the satisfiable theta-gap ablation.

The accepted conclusion is only:

\[
\text{no graph of order 13 satisfies }
\gamma=\gamma^\infty=3<\theta.
\]

The universal conjecture and the order-13 parameter-four and parameter-five
slices remain open.
