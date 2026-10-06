# Approach 3: extremal models and an exact low-dimensional obstruction

**Result:** candidate models force uniqueness of the even constant and rule out every dimension from 4 through 11. They do not prove global optimality at or above 12.

## Two-block Weyl tensors

Partition the coordinates into blocks of sizes \(p,q\ge2\), \(n=p+q\). Define a diagonal curvature operator \(V_{p,q}\) by entries

\[
w_{ij}=\begin{cases}
q/(p-1)&i,j\text{ in the first block},\\
p/(q-1)&i,j\text{ in the second block},\\
-1&i,j\text{ in different blocks}.
\end{cases}
\]

Every diagonal curvature operator satisfies the algebraic Bianchi identity, and the row sums here are zero, so \(V_{p,q}\) is Weyl. For a diagonal operator,
\(Q(w)_{ij}=w_{ij}^2+\sum_{k\ne i,j}w_{ik}w_{jk}\). Direct substitution gives

\[
Q(V_{p,q})=(n-1)V_{p,q},\qquad
\|V_{p,q}\|^2=\frac{pq(n-1)(n-2)}{2(p-1)(q-1)}.\tag{7}
\]

For example, on a mixed edge the right side of the diagonal formula is
\(1-q-p=-(n-1)\); on a first-block edge it is
\((p-1)[q/(p-1)]^2+q=q(n-1)/(p-1)\). This establishes (7) in all dimensions, not just the finite replay range.

Thus

\[
\beta_n^2\ge\frac{2(n-1)(p-1)(q-1)}{pq(n-2)}.
\]

For fixed \(n\), \((p-1)(q-1)/(pq)=1-(n-1)/(pq)\) is maximal at balanced block sizes. In even dimensions this gives
\(\beta_n^2\ge2(n-1)(n-2)/n^2\), hence \(U_n\le n/(n-2)\). Combining with Approach 2 proves that an invariant cone, if it exists, must have exactly the central constant.

For odd dimensions, balanced blocks yield

\[
U_n\le u_n:=\frac{(n+1)(n-2)}{n(n-3)},\qquad
u_n-\frac n{n-2}=\frac4{n(n-3)(n-2)}.\tag{8}
\]

The widths forced by (6) and (8) shrink as \(O(n^{-3})\).

## A non-diagonal four-dimensional model

In oriented dimension four, put
\(u_1=(e_{12}+e_{34})/\sqrt2\),
\(u_2=(e_{13}-e_{24})/\sqrt2\),
\(u_3=(e_{14}+e_{23})/\sqrt2\), and define

\[
H=4u_1\otimes u_1-2u_2\otimes u_2-2u_3\otimes u_3,
\]

with zero action on the anti-self-dual subspace. It is an algebraic Weyl operator. In the self-dual \(\mathfrak{so}(3)\) block the diagonal formula is
\(Q(\lambda)_i=\lambda_i^2+2\lambda_j\lambda_k\); hence

\[
Q(H)=6H,\quad\|H\|^2=24,\quad\langle Q(H),H\rangle=144,
\quad\frac{144^2}{24^3}=\frac32.\tag{9}
\]

Extend by zero on all two-forms involving additional coordinates. The algebraic Bianchi identity and zero Ricci contraction remain true. Every term in the tensor formula for \(Q\) with an extra coordinate vanishes, so (9) remains unchanged in every \(n\ge4\). Consequently,

\[
\beta_n^2\ge\frac32,\qquad U_n\le\frac{4(n-1)}{3n}.\tag{10}
\]

## Incompatibility below 12

For each even \(n=4,6,8,10\), (5) and (10) give incompatible necessary bounds. For odd \(n=5,7,9,11\), (6) and (10) do likewise. The complete rational table is in `results.json` and is recomputed by the checker.

At dimension 11 specifically,

\[
c\ge\frac{2662}{2187}>\frac{40}{33}\ge c,
\qquad\frac{2662}{2187}-\frac{40}{33}=\frac{122}{24057}.
\]

Thus no cone in the stated family is invariant in dimension 11, proving the required lower-threshold obstruction directly. At dimension 12, the model (9) has squared cubic ratio \(54/36\), below the necessary target \(55/36\); it is not a counterexample there.

The low-dimensional obstruction agrees with the known lower bound credited to the 2007 report. This independent derivation is not a novelty claim.
