# Full independent semantic probe replay

`verify_k3p_probes_semantic.py` closes the semantic boundary that the original
streaming verifier intentionally did not cover.  It imports neither the probe
producer nor the frozen K3P atlas.  Starting from the public candidate
profiles, it independently reconstructs and checks:

- all 176 rooted source/target anchors and every mixed-edge insertion site;
- all 574,535 one- and two-port rows;
- all 67,741 exact transports, including labelled incidence and arrowheads;
- all 4,379 parent marginal restrictions;
- all 638 displayed-quartet certificates;
- all 675 row-specific K3P tree--sunlet certificates, by recompiling the
  three independent character sectors and all six literal circuit pullbacks;
- all 32,729 reverse-order marginals and the one-global-triangle condition.

The current K3P registry makes no Bernstein-sign claim.  A generic exact
tensor-Bernstein replay remains active for any future such record, and the
mutation suite confirms that a mixed-sign polynomial is rejected.

Run from the project root with the pinned environment:

```sh
.venv/bin/python probes/verify_k3p_probes_semantic.py
```

The latest complete run on the M1 reference machine passed in 357.73 seconds.
The first instrumented run recorded a peak memory footprint of 1,604,961,816
bytes.  The strengthened suite rejects all seven semantic mutations, including
an altered equality-row transport-scope claim.  The
result files are:

- `K3P_PROBE_SEMANTIC_VERIFICATION.json`
- `K3P_PROBE_SEMANTIC_MUTATIONS.json`

The older `verify_k3p_probes.py` remains useful as the fast streaming
hash/schema/Cartesian replay.  The two programs test different failure modes
and should both remain active.
