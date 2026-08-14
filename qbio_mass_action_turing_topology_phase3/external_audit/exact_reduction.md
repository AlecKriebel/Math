# Exact NP-hardness construction

For a `PARTITION` instance `a_1,...,a_l`, choose `k` with `m=k^2>l`, pad `a` by zeros, and set

\[
Q=I+aa^T,\qquad \beta=1-\frac{1}{2m(1+a^Ta)},\qquad
B(x,y)=\begin{pmatrix}-kQ&y\\x^T&k\beta\end{pmatrix}.
\]

The open cube contains a Hurwitz matrix iff the instance is YES. A partition sign vector `t` gives the rational witness `x=rt`, `y=-rt`, `r=(1+beta)/2`. Conversely, determinant continuity from `(x,y)=(0,0)` to a Hurwitz endpoint gives an interior singular point and

\[
\theta^2x^TQ^{-1}(-y)=m\beta.
\]

Cube maximization and `Q^{-1}=I-aa^T/(1+a^Ta)` force an integer sign vector with `a^Tt=0`.

Write the varying entries as a rank-one family `B(q)=B_0+UX(q)` and lift it to

\[
L(q)=\begin{pmatrix}
B_0&U\\X(q)(B_0+I)&X(q)U-I
\end{pmatrix}.
\]

The lower-unitriangular similarity gives

\[
P(q)L(q)P(q)^{-1}=\begin{pmatrix}B(q)&U\\0&-I\end{pmatrix}.
\]

For every positive diagonal `D`, `L(0)D` has exactly one positive eigenvalue. If `L(q)D` were Hurwitz, signed-determinant continuity would give an interior singular `L(theta q)`, hence a singular `B(theta q)`, which forces a partition. Thus arbitrary equilibrium/right scaling creates no false YES.

Finally realize every fixed row `a_i` and variable row `a_i+q_i b_i` by independent `+e_i,+e_i,-e_i` (or `+e_i,-e_i`) reaction triples/pairs. The complete positive steady-flux image is `R L(q)`. At a positive equilibrium the Jacobian is `R L(q) H`, similar to `L(q)HR`. A fixed positive diagonal entry yields a negative signed singleton minor whenever the Jacobian is Hurwitz, so the fixed-J theorem supplies all-positive diffusion instability.

The network has `3m+1` species and `8m+2` reactions, full stoichiometric rank, strictly positive rates and equilibrium, and polynomial binary encoding. Its molecularity is not uniformly bounded.
