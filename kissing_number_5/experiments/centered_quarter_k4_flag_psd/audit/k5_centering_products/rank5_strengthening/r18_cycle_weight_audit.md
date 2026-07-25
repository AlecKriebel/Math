# Audit of the 18-antipodal-pair C5 weight lemma

Let

\[
 q(t)=\frac{64}{315}+\frac{256}{135}P_2(t)
      +\frac{2048}{945}P_4(t)
      =\frac{64}{45}t^2(4t^2-1),
\]

with the normalized dimension-five polynomials

\[
 P_2(t)=\frac{5t^2-1}{4},\qquad
 P_4(t)=\frac{21t^4-14t^2+1}{8}.
\]

All three harmonic coefficients are positive,
\(q(1)=64/15\), and \(q(t)\leq0\) on the closed interval
\([-1/2,1/2]\).

Choose one representative from each of 18 antipodal pairs, give every
representative weight \(\lambda\geq0\), and give the five residual points
weights \(a_i\geq0\).  Write

\[
 A=\sum_i a_i,\qquad B=\sum_i a_i^2.
\]

Harmonic positive semidefiniteness gives

\[
 \sum_{u,v}w_uw_vq(\langle u,v\rangle)
 \geq \frac{64}{315}(18\lambda+A)^2.
\]

Every representative--representative or representative--residual
off-diagonal pair has absolute inner product at most \(1/2\): the original
code contains both signs of each representative.  Their contributions are
therefore nonpositive.  If

\[
 S=\sum_{i\ne j}a_ia_jq(\langle z_i,z_j\rangle)
\]

is the ordered residual off-diagonal sum, then

\[
 S\geq
 \frac{64}{315}(18\lambda+A)^2
 -\frac{64}{15}(18\lambda^2+B).
\]

The right side is a concave quadratic in \(\lambda\), maximized over
\(\lambda\geq0\) at \(\lambda=A/3\).  Substitution yields

\[
 S\geq\frac{64}{45}(A^2-3B).
\]

Thus the unordered residual sum \(U=S/2\) satisfies

\[
 U\geq\frac{32}{45}(A^2-3B).
\]

If every residual nonedge outside a designated 5-cycle is good, its
contribution is nonpositive, so the weighted cycle sum is at least \(U\).
Taking \(a_i=1\) gives

\[
 \sum_{e\in C_5}q(t_e)\geq\frac{32}{45}(25-15)=\frac{64}{9}.
\]

The cycle-only conclusion requires the explicit hypothesis that all omitted
noncycle residual pairs are good.  The all-pairs inequality alone does not
justify deleting an omitted pair with inner product below \(-1/2\).
