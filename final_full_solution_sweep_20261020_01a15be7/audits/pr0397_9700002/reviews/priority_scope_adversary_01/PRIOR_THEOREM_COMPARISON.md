# Exact prior-theorem comparisons and nonapplication controls

These are deductions made in this review. They test particular proposed transfers from old results; they are not impossibility claims for all literature routes.

## Hassin–Zemel exponent condition

Printed81–82 of the actual1988 final paper give upper exponents `alpha,beta` for individual supplies/demands, total exponent `gamma`, and row/column-count exponents `epsilon,delta`. Their sufficient separation is

```
gamma > alpha+beta+chi,
chi=max(0, 2 epsilon/3, (beta+epsilon)/2).
```

Divide the candidate's transported amounts and capacities by two. Then the balanced supercritical feasibility instance has exactly `k` rows and columns, each with required sum `k`, and total `k^2`. Its random capacities are `(1+(1+delta_k)X_ij)/2`, uniformly bounded below by1/2. This is a proper collection, so the relevant obstruction to this proposed theorem invocation is not properness. Natural exponents are `(1,1,2,1,1)` and `chi=1`: the required strict inequality becomes `2>3`, which fails.

Reparameterizing the size by `n=k^p`, `p>0`, divides these growth exponents by `p`, leaving `2/p>3/p` false. Polynomially *increasing* the capacities and all flow amounts by `k^s`, `s>=0`, does not fix it either: `alpha=beta=1+s`, `gamma=2+s`, `epsilon=1`, and `chi>=1+s/2`, so

`gamma-alpha-beta-chi <= -1-3s/2 <0`.

Polynomially reducing all capacities by `k^s`, `s>0`, would destroy uniform properness: a fixed positive quantile of the original capacity law would be reached at a threshold of order `k^-s`, while the required uniform bound `P(C<=y)<=c y` would tend to zero. Thus neither this elementary rescaling nor a change of size parameter yields a direct Theorem1 corollary.

This does not say that every fixed-time flow-feasibility conclusion needs a new probabilistic idea. The scope of the check is the actual displayed old sufficient theorem.

## KMN report and the vanishing surplus

The actual1988 report's directed theorem fixes an integer support bound `K` and a positive constant mean surplus over one. At time `2+delta_k`, scaled candidate capacities

`C=(1+(1+delta_k)X)/2`

have mean `1+delta_k/2`, continuous unbounded support and a mean surplus tending to zero. The verbatim fixed-support/fixed-surplus theorem does not apply.

Simple lower truncation at a fixed `K>1/2` does not evade the problem. An exact exponential integral gives

```
E min(C,K)
 =1+delta/2 -(1+delta)/2 exp(-(2K-1)/(1+delta)).
```

For each fixed finite `K`, this tends to `1-(1/2)exp(-(2K-1))<1` as `delta` tends to zero. A fixed truncation therefore eventually fails even the mean threshold. Making `K` grow and surplus shrink requires a uniform extension, which the report's further-work section explicitly distinguishes from its proved fixed-parameter theorem. This check is edition-specific: the1993 final journal body was not obtained.

## Matrix scaling comparison

The2021 Kwok–Lau–Ramachandran paper gives near-identity diagonal scaling estimates of order `epsilon log k/lambda` under a spectral-gap condition. For a dense random matrix, standard row/column concentration gives imbalance of order `sqrt(log k/k)` and a gap bounded away from zero is natural. Combining only the displayed generic estimate gives a movement bound of order `log k sqrt(log k/k)`. It does not reproduce the candidate's stated `sqrt(log k/k)` window without further work or a sharper special-case analysis. The old scaling theorem still supplies important context and may support weaker qualitative convergence. Neither scaling nor qualitative concentration-based regular feasibility should be advertised as a new mechanism.

## Independent arithmetic controls

`scope_priority_controls.py` checks the displayed exponent deficits with exact rational arithmetic, the fixed-truncation identity against direct integration-free exponential calculations, sparse-tree/dense-OD scalings and the finite normalization distinction. These controls check the written comparisons and presentation restrictions. They do not establish a literature-absence theorem or replace the universal model proof.
