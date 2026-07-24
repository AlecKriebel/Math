# Weighted common-source attack

This folder independently studies the conditional feasibility system
\[
\begin{gathered}
G\succeq0,\quad \operatorname{rank}G\leq5,\quad G_{ii}=1,\quad
G_{ij}\leq\tfrac12\ (i\ne j),\\
p\geq0,\quad {\bf1}^{\mathsf T}p=1,\quad
Gp=0,\quad G\operatorname{diag}(p)G=G/5
\end{gathered}
\]
at \(N=41\).

It is a discovery and adversarial-audit folder.  Exact lemmas and exact
countermodels will be accompanied by a standard-library verifier.
Numerical searches will be kept separate and will not be presented as
proof.

The audited results are in `proof.md`.  In brief:

- the full quadratic identity recovers rank five even at zero weights;
- squared distances satisfy an exact common-source identity and define a
  reversible chain with spectrum \(\{1,(-1/5)^5,0\}\);
- the augmented Naimark projection gives an exact positive semidefinite
  stress, all-subset inequalities, and pairwise weight bounds;
- Carathéodory gives a support of at most 20, but an exact weighting of the
  full 40-point \(D_5\) code already has support 12 and 28 zero-weight
  extensions;
- a 25-point exact rational kissing code refutes the proposed universal
  row-square-energy upper bound \(41/5\);
- zero-weight points obey exact strict-tail mass bounds, including
  \(19/147\) below \(-1/50\) and \(1/4\) above \(1/50\).

None of these statements rules out a 41-point code.  The remaining gap is
multi-point compatibility among at least 21 zero-weight extensions of a
support of size at most 20.

## Reproduction

The proof verifier and tests use only the Python standard library:

```sh
python3 experiments/weighted_common_source_attack/verify.py
PYTHONPATH=experiments/weighted_common_source_attack \
  python3 -m unittest \
  experiments/weighted_common_source_attack/test_verify.py -v
PYTHONPATH=experiments/weighted_common_source_attack \
  python3 -O -m unittest \
  experiments/weighted_common_source_attack/test_verify.py -v
```

The floating-point discovery script is separate.  It used NumPy 2.5.1
and SciPy 1.16.3, but its output is not trusted by the verifier.

Core SHA-256 values at this checkpoint:

```text
39d9d43416fcdcc16dd8bf922d07aaf9a6010e588b945b44ca7e94f9c0c39804  local_row_energy_counterexample.json
cdc6647dfc6a8c598d9f332e24703f6baae9a2e65dcaf1f84cfa67e11c722f17  verify.py
1830509dd3237701465bef60218afce03253ab4ac9d8de5e9db803c8dc123be7  test_verify.py
41a15f4f8eec8bb986a495ab6f185ab0cd291313b311d446b7cc7a00690c701f  proof.md
```
