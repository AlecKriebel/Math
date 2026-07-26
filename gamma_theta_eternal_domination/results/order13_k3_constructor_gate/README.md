# Order-13 k=3 constructor-gate result

Classification: **constructor verification only**.  No SAT solver was launched,
and this directory makes no finite exclusion claim.

The dedicated order-13 constructor independently exists in
`src/search/order13_k3/`; it does not monkeypatch the frozen order-12 code.
All four full DIMACS streams reproduce the exploratory pilot bytes exactly.
The complete clause-family census (including a SHA-256 hash of every family's
DIMACS clause stream) is emitted by:

```text
PYTHONPATH=src python3 -m search.order13_k3 census
```

The regression and independent coloring-bank oracle are:

```text
python3 -m unittest tests.test_order13_k3_constructor
```

The compact frozen census is in `census.json`.  The graph-to-CNF theorem,
four-template coverage proof, and an independent byte reconstruction remain
separate acceptance gates.  Proof-producing runs must not begin until those
gates agree with this constructor.
