# Exact dual minimizers cannot recover noiseless binary images

## Scope and conclusion

This note answers the exact-minimizer formulation of problem **30004064 / OWR-16766-003**, associated with Conjecture 1 on p. 258 of Ajinkya Kadu's contribution to *Oberwolfach Report 4/2019*, joint work with Tristan van Leeuwen [1]. Both recovery assertions in that formulation are false.

The reason is independent of the geometry of the tomography matrix: **the unique minimizer of the displayed dual objective is zero for every noiseless binary datum**. A 3-by-3 row-and-column tomography example below has exactly two binary solutions and five common pixels, none of which the exact sign recovery returns.

This is a statement about the sign of an exact minimizer. It does not refute, or establish, any separately specified claim about signs of finite numerical iterates, a smoothing limit, or a supplementary primal variable. The cited paper already gives a scalar example exhibiting the zero-minimizer issue [2, Section II-A, equations (10)--(11)]. No claim of historical priority or novelty is made.

## 1. The stated objective

Let \(A\in\mathbb R^{m\times N}\), and suppose
\[
s\in\{-1,1\}^N,\qquad y=As.
\]
Define
\[
F_y(\mu)=\frac12\|\mu-y\|_2^2+\|A^T\mu\|_1,
\qquad \mu\in\mathbb R^m. \tag{1}
\]
The recovery rule under consideration is
\[
\widehat s=\operatorname{sign}(A^T\mu_*),
\qquad \mu_*\in\operatorname{argmin}F_y, \tag{2}
\]
where the sign is componentwise and \(\operatorname{sign}(0)=0\). This convention is explicit in [2, Section II, p. 2]; zero denotes an undetermined pixel in its numerical discussion.

The OWR report states (1)--(2) in its Theorem 1 under full row rank. The argument below works without a rank assumption, and the concrete examples satisfy full row rank.

## 2. Zero-minimizer theorem

**Theorem.** If \(y=As\) for some \(s\in[-1,1]^N\), then \(F_y\) has the unique minimizer \(\mu_*=0\). More precisely,
\[
F_y(\mu)-F_y(0)
=\frac12\|\mu\|_2^2+
\sum_{j=1}^N\bigl(|(A^T\mu)_j|-s_j(A^T\mu)_j\bigr)
\geq\frac12\|\mu\|_2^2. \tag{3}
\]

**Proof.** Expanding the square and using \(y=As\) gives
\[
\begin{aligned}
F_y(\mu)-F_y(0)
&=\tfrac12\|\mu\|_2^2-\mu^Ty+\|A^T\mu\|_1\\
&=\tfrac12\|\mu\|_2^2-s^TA^T\mu+\|A^T\mu\|_1.
\end{aligned}
\]
For a real number \(t\) and \(s_j\in[-1,1]\), \(s_jt\leq |t|\). Every term in the sum in (3) is therefore nonnegative. If \(\mu\neq0\), the final lower bound is strictly positive; if \(\mu=0\), equality holds. This proves both existence and uniqueness. \(\square\)

In particular, for every noiseless binary instance,
\[
\mu_*=0,\qquad A^T\mu_*=0,\qquad\widehat s=0. \tag{4}
\]

Let \(S_y=\{t\in\{-1,1\}^N:At=y\}\), which is nonempty by hypothesis. Define its common-coordinate vector by
\[
c_j=\begin{cases}
1&\text{if every }t\in S_y\text{ has }t_j=1,\\
-1&\text{if every }t\in S_y\text{ has }t_j=-1,\\
0&\text{otherwise}.
\end{cases} \tag{5}
\]
Thus (2) returns (5) **if and only if no coordinate is common to all binary solutions**. For any positive number of pixels, it never returns a unique binary solution.

## 3. A genuine tomography counterexample with two solutions

Vectorize a 3-by-3 image by rows. Measure all three row sums and the first two column sums:
\[
A=\begin{pmatrix}
1&1&1&0&0&0&0&0&0\\
0&0&0&1&1&1&0&0&0\\
0&0&0&0&0&0&1&1&1\\
1&0&0&1&0&0&1&0&0\\
0&1&0&0&1&0&0&1&0
\end{pmatrix},\qquad
y=\begin{pmatrix}3\\1\\1\\3\\1\end{pmatrix}. \tag{6}
\]
The omitted last column sum is determined by the measured sums:
\(c_3=r_1+r_2+r_3-c_1-c_2=1\). These are therefore exactly the same data constraints as all row and column sums.

The rows of \(A\) are linearly independent. In a linear combination with row-sum coefficients \(\alpha_1,\alpha_2,\alpha_3\) and column-sum coefficients \(\beta_1,\beta_2\), inspect the three entries of the third column of the image. They give \(\alpha_i=0\) for each \(i\). The remaining entries then give \(\beta_1=\beta_2=0\). Hence \(\operatorname{rank}A=5\).

There are exactly two binary images giving (6):
\[
S_+=\begin{pmatrix}1&1&1\\1&1&-1\\1&-1&1\end{pmatrix},
\qquad
S_-=\begin{pmatrix}1&1&1\\1&-1&1\\1&1&-1\end{pmatrix}. \tag{7}
\]
To prove exhaustiveness without a search, the first row sum is 3, so its three entries must all be 1. The first column sum is also 3, so its three entries must all be 1. The bottom-right 2-by-2 block must consequently have all row and column sums zero. If its upper-left entry is \(a\in\{-1,1\}\), the entire block is
\[
\begin{pmatrix}a&-a\\-a&a\end{pmatrix}.
\]
The two choices of \(a\) give exactly (7).

The common-coordinate vector, written as an image, is
\[
C=\begin{pmatrix}1&1&1\\1&0&0\\1&0&0\end{pmatrix}. \tag{8}
\]
By the theorem, the unique optimizer of (1) is \(\mu_*=0\), and (2) returns the zero image rather than (8). The multiple-solution assertion fails even for unweighted horizontal and vertical line sums on a square image, with all redundant measurements removed.

The same construction works on any \(k\)-by-\(k\) image, \(k\geq3\): put 1 outside a bottom-right 2-by-2 checkerboard, and measure all \(k\) row sums and the first \(k-1\) column sums. There are exactly two binary solutions; all \(k^2-4\) other pixels are common. The matrix has rank \(2k-1\), so its number of independent measurements divided by its number of pixels tends to zero. The counterexample is therefore not excluded by requiring strongly underdetermined tomography.

For the unique-solution clause, use the same matrix (6) with datum \((3,3,3,3,3)^T\). The three row sums force every pixel to be 1, but exact dual recovery again returns zero. The even smaller scalar example \(A=(1),y=1\) was already covered by [2, equations (10)--(11)].

## 4. The redundant-measurement and Lagrangian formulations

The paper also handles rank-deficient matrices through
\[
G_y(\mu)=\tfrac12\|P(\mu-y)\|_2^2+\|A^T\mu\|_1,
\qquad P=AA^\dagger, \tag{9}
\]
where \(P\) is the orthogonal projection onto \(\operatorname{range}A\). Since \(Py=y\),
\[
G_y(\mu)-G_y(0)
=\tfrac12\|P\mu\|_2^2+\|A^T\mu\|_1-s^TA^T\mu
\geq\tfrac12\|P\mu\|_2^2. \tag{10}
\]
Every minimizer must satisfy \(P\mu=0\), and conversely every such \(\mu\) gives equality because \(A^T\mu=0\). Hence
\[
\operatorname{argmin}G_y=\ker A^T,
\qquad A^T\mu_*=0\text{ for every minimizer}. \tag{11}
\]
Keeping all six row-and-column measurements in the 3-by-3 example therefore gives the same failure, with the correct projected objective.

There is no positive duality gap to explain away in the noiseless case. For the genuine binary least-squares problem, introduce a real vector \(z\), a binary vector \(t\), and the constraint \(z=t\). Its Lagrangian is
\[
L(z,t,\nu)=\tfrac12\|Az-y\|_2^2+\nu^T(z-t).
\]
The primal value is zero because \(y=As\). At \(\nu=0\), the infimum of \(L\) is zero, so weak duality gives equality of primal and dual optimal values. This does not license the recovery rule: minimizing \(-\nu^Tt\) at \(\nu=0\) leaves **every** binary \(t\) tied. The feasibility equation \(At=y\) still has to be enforced. A zero subgradient may be accompanied by a useful additional primal variable, but the zero multiplier alone does not identify that variable.

## 5. Exact optima and numerical sign selection are different questions

The source paper expressly discusses taking signs before an iterative limit or smoothing the one-norm [2, Sections II-A and II-C]. Its later primal-dual Algorithm 2 returns the sign of an additional variable \(z^T\), rather than the sign of the exact zero multiplier. This note makes no assertion that those implementations cannot give useful reconstructions.

Conversely, objective convergence by itself cannot certify sign recovery. In the scalar instance \(A=(1),y=1\), for every \(\varepsilon>0\),
\[
F(\varepsilon)-F(0)=\tfrac12\varepsilon^2,
\qquad
F(-\varepsilon)-F(0)=2\varepsilon+\tfrac12\varepsilon^2.
\]
Both sequences tend to the unique optimizer and its optimal value, while their signs are opposite. An exact sign-recovery conjecture cannot silently be replaced by an assertion about an unspecified approximate solver or stopping rule.

**Final conclusion.** The recorded exact-minimizer question has a complete negative answer. Both unique-image recovery and common-coordinate recovery fail under the displayed rule. The scalar degeneracy was already acknowledged in the cited source; stronger numerical or algorithm-specific conjectures require their own precise formulations and are not settled here.

## References

[1] A. Kadu, joint work with T. van Leeuwen, “A Convex Formulation for Binary Tomography,” in *Tomographic Inverse Problems: Theory and Applications*, Oberwolfach Report 4/2019, pp. 256--259. [DOI 10.4171/OWR/2019/4](https://doi.org/10.4171/OWR/2019/4). [Publisher PDF](https://content.ems.press/assets/public/full-texts/serials/owr/16/1/16766/online/10.4171-owr-2019-4.pdf).

[2] A. Kadu and T. van Leeuwen, “A Convex Formulation for Binary Tomography,” *IEEE Transactions on Computational Imaging* 6 (2020), 1--11. [DOI 10.1109/TCI.2019.2898333](https://doi.org/10.1109/TCI.2019.2898333). The inspected author manuscript is [arXiv:1807.09196v3](https://arxiv.org/abs/1807.09196v3), revised 15 December 2020; its pagination and section numbering are used above.
