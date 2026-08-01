# Assumptions, conventions, equality, and representation analysis

## Assumptions and conventions

- Hilbert spaces are finite-dimensional and complex. The theorem concerns
  the finite-dimensional projector definition of $\chi_q$ in the problem.
- Every $P_{v,c}$ is an orthogonal projection; zero projections are
  allowed. No original rank uniformity is assumed.
- Rows satisfy $\sum_cP_{v,c}=I$, and an edge imposes
  $P_{v,c}P_{w,c}=0$. No further commutativity is assumed, including
  commutativity with apex or joined-clique projections.
- The inner product is $\langle x,y\rangle=x^*y$. A star denotes adjoint,
  $\perp$ denotes orthogonal complement, and
  $\{A,B\}=AB+BA$.
- Traces are unnormalized matrix traces. Every rank and dimension argument
  is integer-valued and exact.
- A coloring can be padded with zero color outcomes. Thus excluding an
  $n$-coloring excludes every coloring using at most $n$ colors.
- For the family statement, $K_0$ is the empty joined graph at $n=3$.
- The upper bound uses the explicit classical four-coloring printed in the
  paper, plus one fresh color for every joined vertex.
- No claim is made here about infinite-dimensional or commuting-operator
  variants.

## Equality analysis in the core

The core uses the exact operator identity

\[
\frac43I-X=\sum_{j=0}^3f_j^*f_j.
\]

Its left side has trace zero because it acts in the $3r$-dimensional
fixed-color corner and $X$ is the sum of four rank-$r$ projections. Hence
the positive right side has trace zero. Faithfulness of finite matrix trace
implies every factor $f_j=0$; no limiting or numerical equality case is
involved. This forces $X=\frac43I$, the three Walsh identities, and then
the anticommutator system. The terminal packing inequalities cannot be
simultaneously saturated: their sum would require $3nr\le2nr$.

## Minimal-dimension analysis

- No finite local dimension $d\ge1$ supports an $n$-coloring of
  $G_{19}\vee K_{n-3}$. In particular, there is no minimal higher-rank
  four-color counterexample for $H$.
- The proven value $n+1$ is attained classically in local dimension one.
  For $H$, five colors are necessary and dimension one suffices at that
  color number.
- Symmetrization sends a hypothetical dimension-$d$ $n$-coloring to
  dimension $n!d$, with common rank $(n-1)!d$. Since the contradiction
  holds for every positive $r$, no small-dimensional exception is hidden
  by this enlargement.

## Reducibility and irreducibility

- Irreducibility is neither assumed nor needed. The symmetrized
  representation is generally reducible even if the original one is
  irreducible, but its existence follows exactly from the original.
- The contradiction excludes every nonzero finite-dimensional
  representation of the $n$-coloring relations, irreducible or reducible.
- For one fixed color, the core projections give the $M_3(\mathbb C)$
  coordinate factor tensored with the identity on the multiplicity space.
  Tail planes may carry genuine multiplicity-space structure and need not
  decompose into rank-one tails. An irreducibility-to-rank-one theorem is
  therefore unnecessary and is not asserted.
- At the valid $(n+1)$-color level, one-dimensional classical
  representations exist. No classification of all such representations is
  needed for the chromatic-number theorem.
