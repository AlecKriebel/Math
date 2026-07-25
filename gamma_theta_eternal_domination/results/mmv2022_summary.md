# Reproduction of the 2022 near-miss catalog

## Certified finite result

The exact arXiv TeX source of MacGillivray–Mynhardt–Virgile (2022), Table 9,
contains 56 connected Graph6 records: two of order 10 and 54 of order 11.
The input catalog has SHA-256

`801f054853d07652c795fb16217425869f857d7f5d74e427165d554faf4eae1d`.

For every record, verifier A and the structurally independent verifier B agree
on all five parameters and on the greatest one-guard eternal family at every
guard count. Both explicit-family checkers also accept the optimum family.
In addition, every value \(\theta=4\) now has a standalone finite
certificate: a direct four-coloring of the complement supplies the upper
bound, and an exhaustive no-symmetry coloring trace supplies and independently
checks the lower bound \(\theta>3\).

| Multiplicity | \((\gamma,i,\alpha,\gamma^\infty,\theta)\) |
|---:|---|
| 52 | \((2,2,3,3,4)\) |
| 2 | \((1,1,3,3,4)\) |
| 1 | \((2,3,3,3,4)\) |
| 1 | \((2,2,2,3,4)\) |

Consequently:

- all 56 satisfy \(\gamma^\infty<\theta\);
- exactly 55 satisfy \(\alpha=\gamma^\infty<\theta\);
- none satisfies \(\gamma=\gamma^\infty<\theta\).

## Exact reason each of the 55 near-misses fails

All 55 graphs with \(\alpha=\gamma^\infty=3<4=\theta\) fail the explicit
condition \(\gamma=\alpha\):

- two have a universal vertex and \(\gamma=1\);
- 53 have \(\gamma=2\), with an explicit dominating pair recorded in
  `results/mmv2022_parameters.csv`.

One of the latter,
`JEhbtj{rv}?`, has \(i=\alpha=3\) but still has \(\gamma=2\). It is a concrete
reminder that well-coveredness and even \(i=\alpha\) do not replace the search
condition \(\gamma=\alpha\).

The sole graph not in the 55-graph near-miss subset is `JQyurj]yt|?`, with
\((\gamma,i,\alpha,\gamma^\infty,\theta)=(2,2,2,3,4)\).

The parameter CSV records, for every graph, a minimum dominating-set witness,
the number of minimum dominating sets, a minimum independent dominating set,
a maximum independent set, the greatest eternal-family size, and a canonical
SHA-256 digest of that family.

The 56 lower-bound traces are in `certificates/mmv2022_theta_k3/`.
`results/mmv2022_theta_certificates.csv` binds each trace to its graph and
color count and records its byte, trace, and claim hashes together with the
four-coloring witness. The complete set contains 6,098 trace nodes and
304,941 bytes.

## Scope

This reproduces a published finite catalog. It does not extend the
counterexample lower bound beyond order 11 and does not resolve the
conjecture.
