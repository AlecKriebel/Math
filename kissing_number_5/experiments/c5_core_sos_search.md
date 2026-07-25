# Five-point \(C_5\) core SOS attempt

Status: **FAILED NUMERICAL DISCOVERY ATTEMPT — NOT A CERTIFICATE**

Direct constrained Gram optimization strongly suggests the universal
five-point inequality

\[
\sum_{0\leq i<j\leq4}h(g_{ij})\leq\frac32,
\qquad h(t)=t^2(t^2-\tfrac14),
\]

when \(G=(g_{ij})\succeq0\), the five cycle entries belong to
\([-1,-1/2]\), and the five chords belong to \([-1/2,1/2]\).  Lemma 9 of
`proofs/sparse_deep_graph_stability.md` gives an exact rank-two equality
continuum, but no universal upper proof is known here.

`c5_core_sos_search.py` made one genuinely five-vertex certificate attempt.
It asked for a degree-four quadratic-module identity using:

- a free sum of squares of degree at most four;
- affine box factors times quadratic SOS multipliers;
- all \(2\times2\) principal Gram minors times quadratic SOS multipliers;
- nonnegative constant multipliers on all \(3\times3\) and \(4\times4\)
  principal Gram minors.

The resulting conic model had 8,001 CVXPY variables and 1,001 polynomial
coefficient equations.  SCS 3.2.11 reported the ansatz infeasible.  Clarabel
0.11.1 terminated with a numerical error while its cost diverged.  These
statuses prove nothing about either the inequality or the nonexistence of a
higher-degree certificate.  In particular, the ansatz omits the
degree-five determinant and products that would require cancellation of
higher-degree terms.

Discovery environment:

```text
Python 3.9.6
CVXPY 1.4.4
SCS 3.2.11
Clarabel 0.11.1
NumPy 1.26.4
SymPy 1.14.0
```

Replay after installing those versions:

```sh
C5_SOS_SOLVER=SCS python experiments/c5_core_sos_search.py
```

This failed ansatz is retained to prevent repeated claims that a routine
degree-four principal-minor SOS closes the missing \(1/32\).  Triple-level
PSD and angular relaxations reach \(49/32\); any successful proof needs a
stronger global Gram mechanism.
