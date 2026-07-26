# Eternal domination and the Lovász theta function

This package gives an exact, reproducible counterexample to the proposed
universal inequality

\[
\gamma^\infty(G)\geq\vartheta(G)
\]

for the standard one-guard-moves eternal domination number. The graph has
graph6 record

```text
IEhbtj{ro
```

and satisfies

\[
\gamma^\infty(G)=3
\quad\text{and}\quad
\vartheta(G)\geq\frac{7593}{2500}=3.0372.
\]

MacGillivray, Mynhardt, and Virgile published this graph in 2022 and proved
that its eternal domination number is three. The new observation is that an
exact rational feasible point for the standard Lovász-theta semidefinite
program has objective strictly greater than three.

## Reproduce the result

The verifiers use only Python's standard library:

```bash
python3 verify_all.py
python3 -m unittest discover -s tests -v
shasum -a 256 -c SHA256SUMS
```

The first command:

- decodes the graph independently in two implementations;
- checks the exact rational theta matrix, including every edge zero;
- proves positive definiteness by exact rational \(LDL^{\mathsf T}\) pivots;
- checks trace \(1\) and objective \(7593/2500\);
- recomputes the one-guard eternal-domination fixed point for one, two, and
  three guards; and
- checks all 602 attack-response pairs in the saved 86-configuration family.

To build the paper (Tectonic required):

```bash
python3 render_paper.py
```

The rendered note is
[`output/pdf/eternal_domination_lovasz_theta.pdf`](output/pdf/eternal_domination_lovasz_theta.pdf).

## Scope

The counterexample itself is exact and solver-free. The minimum-order
statement additionally uses the published exhaustive computation that every
graph on at most nine vertices has eternal domination number equal to its
clique-cover number.

As of 25 July 2026, a focused literature search found no prior public
resolution of the Lovász-theta question. That is evidence of apparent
novelty, not a claim of absolute priority. No researcher was contacted during
this work.

## Authorship and status

**Alec Kriebel, with heavy assistance from ChatGPT 5.6 Sol.**

This is an unreviewed AI-assisted research note. Exact verification is not
peer review, and the literature audit cannot establish worldwide priority.
