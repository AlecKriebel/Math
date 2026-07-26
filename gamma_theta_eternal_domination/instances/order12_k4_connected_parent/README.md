# Connected order-12, parameter-four parent instance

`instance.cnf` is the deterministic full formula derived in
`math/lemmas/order12_k4_synthesis_target.md`.  Its edge variables encode
\(H=\overline G\).  A model is equivalent, up to relabeling one maximum
independent four-set, to a connected 12-vertex graph satisfying

\[
\gamma(G)=\alpha(G)=\gamma^\infty(G)=4<\theta(G).
\]

The formula has 18,381 variables, 114,742 clauses, and 1,180,016 literals.
Its SHA-256 is

```text
adbe0c01614bae6cd3aed4ccdcd45a757ca56e7ef9c4f2f280f2d8ef200e40ac
```

The instance contains the complete anchor-normalized four-coloring bank and
the proved \(S_8\) outer-signature ordering.  `manifest.json` binds the exact
source bytes and every clause-family count.

This package has status `NO_MATHEMATICAL_CLAIM`: no SAT solver has been run,
no proof has been produced, and it does not exclude the \((12,4)\) slice.
Any future decisive run must use an independent candidate verifier or a
strict proof-producing UNSAT workflow.

