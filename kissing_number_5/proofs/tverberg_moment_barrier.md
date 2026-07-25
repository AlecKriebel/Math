# A degree-two Tverberg constraint and its exact barrier

## Status

This note proves a rank-five, common-source consequence that activates at
exactly 41 points.  It also gives an exact 18-point counterexample showing
that the consequence alone is insufficient.  It is not an upper-bound proof.

## 1. Three disjoint measures with matching moments

Define the degree-two feature map
\[
 \Phi(x)=\left(x,xx^{\mathsf T}-\frac15I_5\right)
 \in\mathbb R^5\oplus\operatorname{Sym}_0(5)\cong\mathbb R^{19}.
\]
The classical affine Tverberg theorem says that every
\((r-1)(D+1)+1\) points of \(\mathbb R^D\) can be partitioned into \(r\)
parts whose convex hulls have a common point.  Apply it with \(r=3,D=19\);
the threshold is
\[
 2(19+1)+1=41.
\]
Thus, for any 41 points \(x_i\in S^4\), there are three disjoint nonempty
supports and probability measures \(\mu_1,\mu_2,\mu_3\) on them for which
\[
 \mathbb E_{\mu_a}X=m,\qquad
 \mathbb E_{\mu_a}XX^{\mathsf T}=M
\]
are independent of \(a\).  Zero convex coefficients can simply be deleted.
The common moments satisfy
\[
 M\succeq mm^{\mathsf T},\qquad M\succeq0,\qquad\operatorname{tr}M=1.
\]

The target dimension really is 19: if an affine functional
\[
 c+\ell\mathbin{\cdot}x+
 \operatorname{tr}\!\left(B(xx^{\mathsf T}-I/5)\right)
\]
vanishes on the sphere, comparison at \(x\) and \(-x\) gives \(\ell=0\).
Then \(x^{\mathsf T}Bx\) is constant on the sphere, so \(B\) is scalar;
because \(B\) is traceless, \(B=0\), and then \(c=0\).

## 2. Universal interval-factor inequalities

Now suppose the 41 points form a kissing code.  Draw independently
\(X_a\sim\mu_a\).  Distinct supports ensure that every cross-color pair is
distinct, so its inner product lies in the full closed interval
\([-1,1/2]\).  Put
\[
 u=\|m\|^2,\qquad v=m^{\mathsf T}Mm,\qquad
 w=\operatorname{tr}(M^3).
\]
For \(T=X_1\mathbin{\cdot}X_2\),
\[
 \mathbb ET=u,\qquad \mathbb ET^2=\operatorname{tr}(M^2).
\]
The pointwise inequality \((T+1)(1/2-T)\geq0\) gives
\[
 \boxed{\operatorname{tr}(M^2)+\frac12u\leq\frac12.}
\]

Let
\[
 A=X_1\mathbin{\cdot}X_2,\quad
 B=X_1\mathbin{\cdot}X_3,\quad
 C=X_2\mathbin{\cdot}X_3.
\]
Independence and equality of the two moments give
\[
 \mathbb EA=\mathbb EB=\mathbb EC=u,
\]
\[
 \mathbb E(AB)=\mathbb E(AC)=\mathbb E(BC)=v,\qquad
 \mathbb E(ABC)=w.
\]
For instance,
\[
 \mathbb E(ABC)
 =\sum_{i,j,k}M_{ij}M_{ik}M_{jk}=\operatorname{tr}(M^3).
\]
Taking expectations of the four symmetric choices of the nonnegative
factors \(1+A\) and \(1/2-A\) yields
\[
\begin{array}{rcl}
1+3u+3v+w&\geq&0,\\
\frac12-\frac32v-w&\geq&0,\\
\frac14-\frac34u+w&\geq&0,\\
\frac18-\frac34u+\frac32v-w&\geq&0.
\end{array}
\]
Equivalently,
\[
 w+\frac32v\leq\frac12,\qquad
 w\geq\frac34u-\frac14,\qquad
 w\leq\frac18-\frac34u+\frac32v.
\]
The exact verifier expands all four products and guards against coefficient
errors.  Endpoints cause no problem because a factor may vanish.

## 3. Exact 18-point counterexample

The certificate
[`tverberg_moment_counterexample.json`](../certificates/tverberg_moment_counterexample.json)
stores four \(6\times6\) integer blocks.  With \(D=6I_6-J_6\), form
\[
 {\cal M}=
 \begin{pmatrix}
 D&A&B\\ A^{\mathsf T}&D&C\\ B^{\mathsf T}&C^{\mathsf T}&D
 \end{pmatrix}.
\]
The standard-library verifier checks by integer multiplication that
\[
 {\cal M}^2=18{\cal M},\qquad {\cal M}\mathbf1=0,\qquad
 \operatorname{tr}{\cal M}=90.
\]
It follows that \({\cal M}\) is positive semidefinite, with eigenvalues 18
of multiplicity five and 0 of multiplicity thirteen.  Hence
\[
 G=\frac15{\cal M}
\]
is the Gram matrix of 18 unit vectors in \(\mathbb R^5\).  Its off-diagonal
entries belong to
\[
 \{-4/5,-1/5,2/5\},
\]
so it is a kissing code with strict margin.

Each diagonal block is the Gram matrix \(D/5\) of a regular 5-simplex.
Uniform measure on any block has first moment zero.  Its frame operator is
\((1/5)I_5\): the five nonzero eigenvalues of \(D/5\) are \(6/5\), so the
sum of the six rank-one projectors is \((6/5)I_5\), and division by six
gives the claim.  Therefore the three disjoint block measures have
\[
 m=0,\qquad M=\frac15I_5,
\]
and realize all the Tverberg conclusions exactly.  Here
\[
 u=v=0,\qquad w=\frac1{25},
\]
with slack in every displayed inequality.

Thus a proof at 41 must bind the unused points or higher moments to the
Tverberg partition.  Matching first and second moments of three disjoint
supports, by itself, cannot be the missing contradiction.
