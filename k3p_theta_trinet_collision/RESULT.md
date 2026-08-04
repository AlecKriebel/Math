# Exact result

The high-level K3P trinet question has a negative answer: the K3P analogue of the arbitrary-level trinet inequality is false. A fixed binary semi-directed strict level-two theta trinet with a genuine nontrivial 3-blob has an exact interior stochastic K3P collision with a three-leaf tree.

Let `h` be the positive root of `5 h^4 = 1`, isolated by `2/3 < h < 7/10`. The rooted calculation network, its edge vectors, and both inheritance probabilities are recorded in `certificate.json`. Suppressing the degree-two root produces the effective pendant edge

```text
K odot K = (1, 1/4, 1/4, 1/4),
p = (7/16, 3/16, 3/16, 3/16).
```

The core displayed-tree mixture factors exactly as

```text
M[y,z] = P[y+z] B[y] B[z]
```

for all sixteen pairs `(y,z)`. This yields equality of all sixty-four Fourier coordinates and all sixty-four leaf-pattern probabilities with the stated three-star tree.

The selected 15x15 Jacobian determinant is

```text
h(10 h^2 + 1) / (2^61 3^4 5^14) > 0,
```

so the fixed theta-trinet image contains an ordinary open neighborhood of the common distribution in the 15-dimensional affine group-based Fourier space `q_AAA=1`. A real-analytic implicit-function argument, based on the exactly verified Jacobian and tangent data, also gives a realization of the same tree distribution in which every network edge has three strictly positive continuous-time K3P substitution rates.

Run `python3 verify.py` for the dependency-free exact replay.
