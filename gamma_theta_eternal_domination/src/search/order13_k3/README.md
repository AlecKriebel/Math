# Order-13, parameter-three exact constructor

This directory is the production constructor gate for the four order-13,
parameter-three odd-hole templates.  It is separate from the frozen order-12
code and never changes that code's module constants at runtime.

The encoded edge variables describe \(H=\overline G\).  For each
`hole5`, `hole7`, `hole9`, or `hole11` instance, the constructor imposes:

- no \(K_4\) in \(H\);
- an external common \(H\)-neighbor for every vertex pair;
- the named induced odd hole, with no external hub;
- vertex `length` as a common neighbor of rim edge `01`, fixing the
  independent triple `{0,1,length}` in \(G\);
- connectivity of \(G\);
- a nonempty family of dominating triples closed under every attack at an
  unoccupied vertex by moving one adjacent guard;
- every \(H\)-triangle in the family (a proved redundant strengthening);
- one obstruction clause for every first-use-canonical proper three-coloring
  of the forced template edges.

There is no signature sorter, rim-reflection breaker, DoubleLex condition, or
other heuristic symmetry restriction.

From the campaign root:

```text
PYTHONPATH=src python3 -m search.order13_k3 census
PYTHONPATH=src python3 -m search.order13_k3 generate \
  --template hole11 \
  --output-directory instances/order13_k3_hole11 \
  --validation-gate
PYTHONPATH=src python3 -m search.order13_k3 audit \
  --package-directory instances/order13_k3_hole11 \
  --exhaustive
python3 -m unittest tests.test_order13_k3_constructor
```

`plan` can create a fresh `READY_NOT_RUN` directory containing a formula,
hash-bound future CaDiCaL command, resource ceilings, and checkpoint zero.  It
does not execute the command:

```text
PYTHONPATH=src python3 -m search.order13_k3 plan \
  --package-directory instances/order13_k3_hole11 \
  --output-directory results/order13_k3_hole11_production \
  --cadical tools/cadical_3_0_1/build/cadical \
  --validation-gate
```

The four formulas reproduce the frozen pilot DIMACS bytes exactly.  That byte
identity certifies constructor continuity, not satisfiability.  A negative
finite result additionally needs the separate mathematical proof that the
four templates cover the target universe, proof-producing solver runs for all
four formulas, independently checked LRAT artifacts, and a coverage manifest.
No solver output is a claim made by this package.
