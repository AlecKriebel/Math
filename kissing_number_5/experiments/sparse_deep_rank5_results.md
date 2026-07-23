# Sparse Deep-Graph Rank-Five Search

Status: **NUMERICAL EVIDENCE ONLY — NOT A CERTIFICATE**

The search in `sparse_deep_rank5_search.js` targets the unique 23-edge graph
and all three classified 24-edge graphs.  Every isolated \(K_2\) component
is imposed as an exact antipodal pair.  The remaining representatives are
optimized directly on \((S^4)^n\).  For every pair the program includes the
kissing upper inequality and the lower inequality that either enforces or
forbids a deep edge.  The reported objective is the largest violation, so a
rigorous realization would require a nonpositive value.

## Reproduction

Runtime used:

```text
node v22.16.0
```

Deterministic command:

```sh
SEEDS=64 STEPS=100 node experiments/sparse_deep_rank5_search.js \
  > /tmp/kissing5_sparse_deep_rank5_search_fast.json
```

The generated JSON includes the best representative coordinates.  In the
run recorded here its SHA-256 hash was

```text
13081405d9c642930c47548c4564b1cf16d62142461584c62b5679a0f3680356
```

Each coordinate hash below is the SHA-256 of Python's compact serialization
`json.dumps(coordinates,separators=(',',':')).encode()`.

## Best results

| target deep graph | internal seed | maximum violation | coordinate SHA-256 |
|---|---:|---:|---|
| \(C_5\sqcup18K_2\) | 1001 | 0.04296893186236295 | `c837cd8ddade8ef4b3e721ffcb420d8e69aa631dd5e7c92e72286b5b74046093` |
| \(C_7\sqcup17K_2\) | 2044 | 0.04472787293698033 | `107e456fa9b3a47b64f708f793fee7f002d61b9bb1d5b2d8c344a39b97df46f8` |
| \(C_5\)-tail\(\sqcup17K_2\) | 3049 | 0.046550132955731405 | `4f7cce5d37da4ab8f462ca998e7d5b253246942a262cd868588b0d422b5f4194` |
| \(C_5\sqcup P_4\sqcup16K_2\) | 4043 | 0.04315278633699027 | `15a450351da4b4fc18f9780714d5783791ad6d25d282f29cf1443e550879766a` |

All values are positive.  Thus the run found no realization, but it proves
no nonexistence statement.  The earlier SciPy/SLSQP 23-edge search in
`construction_round2` reached the slightly smaller violation
0.0427209812806707, providing a useful independent numerical comparison.

The restriction to exact antipodal isolated edges is not justified for a
hypothetical code.  Equations (19)--(20) in
`proofs/sparse_deep_graph_stability.md` quantify why this boundary model is
relevant, but they do not permit replacing near-antipodal pairs by exact
ones in a proof.
