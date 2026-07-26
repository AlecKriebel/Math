# Eternal domination and the Lovász theta function

This package gives two complementary negative answers to the proposed
universal inequality

\[
\gamma^\infty(G)\geq\vartheta(G)
\]

for the standard one-guard-moves eternal domination number.

First, combining Alon's explicit Ramsey graphs with a theorem of Goddard,
Hedetniemi, and Hedetniemi gives an explicit infinite family \((H_k)\) with

\[
2\leq\gamma^\infty(H_k)\leq3,
\qquad
\vartheta(H_k)=\Theta\!\left(|V(H_k)|^{1/3}\right).
\]

Thus \(\vartheta/\gamma^\infty\) is unbounded. Second, this package gives an
exact, reproducible smallest counterexample. The graph has graph6 record

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
that its eternal domination number is three. The finite observation is that
an exact rational feasible point for the standard Lovász-theta semidefinite
program has objective strictly greater than three. Their exhaustive result
through order nine makes this a minimum-order counterexample.

## Reproduce the result

The verifiers use only Python's standard library:

```bash
python3 verify_all.py
python3 -m unittest discover -s tests -v
shasum -a 256 -c SHA256SUMS
```

The first command verifies the finite ten-vertex result:

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

The ten-vertex counterexample itself is exact and solver-free. The
minimum-order statement additionally uses the published exhaustive
computation that every graph on at most nine vertices has eternal domination
number equal to its clique-cover number. The unbounded-family theorem is a
direct synthesis of published results by Alon and by Goddard, Hedetniemi, and
Hedetniemi; it is not checked by the finite verifier.

As of 26 July 2026, a focused literature search found no prior public source
explicitly making these eternal-domination connections or presenting the
ten-vertex theta certificate. That is evidence of apparent novelty, not a
claim of absolute priority. No researcher was contacted during this work.

## Authorship and status

**Alec Kriebel, with heavy assistance from ChatGPT 5.6 Sol.**

This is an unreviewed AI-assisted research note. Exact verification is not
peer review, and the literature audit cannot establish worldwide priority.
