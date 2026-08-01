# Exact third output moment and a new violation threshold

## Setup

For a unit three-qutrit tensor (z), put

\[
S_z=D_z^\dagger D_z.
\]

The nonzero spectrum of (S_z) is paired because (D_z) is a
(27\times27) skew matrix.  Write the distinct pair values as

\[
\lambda_1\ge\lambda_2\ge\cdots\ge\lambda_{13}\ge0.
\]

Then

\[
\operatorname{Tr}S_z^3=2\sum_{j=1}^{13}\lambda_j^3.
\]

## Exact three-replica formula

On three replicas of one local qutrit, let (F_\pi) be the permutation
operator for \(\pi\in S_3\), and define

\[
T=F_{(12)}+F_{(13)}+F_{(23)}-F_{(123)}.
\tag{1}
\]

The orientation of the last cycle is fixed by the convention

\[
(P_\pi)_{p,q}=\prod_{r=1}^3\delta_{p_r,q_{\pi(r)}}.
\]

After regrouping (z^{\otimes3}) by physical site rather than by replica,
one has

\[
\boxed{
\operatorname{Tr}S_z^3
=\frac1{512}
\left\langle z^{\otimes3},
T^{(1)}\otimes T^{(2)}\otimes T^{(3)}
z^{\otimes3}\right\rangle.
}
\tag{2}

Although (T) itself is not Hermitian, the expectation in (2) is real.
Indeed (T^\dagger) is conjugate to (T) by a replica transposition, and
(z^{\otimes3}) is invariant under the simultaneous transposition at all
three physical sites.  Equivalently, the operator in (2) can be replaced by

\[
\frac12\left(T^{\otimes3}+(T^\dagger)^{\otimes3}\right).
\]

### Proof

With

\[
(A_p)_{ai}=2^{-1/2}\varepsilon_{pai},
\]

define the one-site contraction

\[
B_{pq;ij}=\sum_a(A_p)_{ai}(A_q)_{aj}.
\]

Expanding the cyclic trace of three copies of (S_z) factorizes over the
three physical sites.  Its one-site coefficient is

\[
K_{p_1p_2p_3,q_1q_2q_3}
=\sum_{i,j,k}
B_{p_1q_1;ij}B_{p_2q_2;jk}B_{p_3q_3;ki}.
\]

Direct epsilon contraction gives the operator identity

\[
\boxed{K=\frac18T.}
\tag{3}
\]

Tensoring (3) at the three physical sites gives (2).  The exact verifier
checks all (27^2=729) entries of (3) over the rationals.

## Necessary third-moment threshold for a violation

The desired Ky--Fan-four inequality is

\[
\lambda_1+\lambda_2\le\frac14.
\]

Suppose instead that \(\lambda_1+\lambda_2>1/4\).  The trace normalization
is

\[
\sum_{j=1}^{13}\lambda_j=\frac12.
\]

For fixed sums of the first two and last eleven entries, convexity minimizes
the sum of cubes by equalizing within each group.  The infimum on the
violation boundary is therefore attained at

\[
\lambda_1=\lambda_2=\frac18,
\qquad
\lambda_3=\cdots=\lambda_{13}=\frac1{44}.
\]

It follows that every strict violation must satisfy

\[
\boxed{
\operatorname{Tr}S_z^3>
2\left(2\left(\frac18\right)^3
+11\left(\frac1{44}\right)^3\right)
=\frac{125}{15488}.
}
\tag{4}

This is independent of the previously proved local-purity threshold

\[
P_{\rm loc}(z)>\frac{15}{11}.
\]

Thus any physical counterexample must pass both exact filters.

## A general upper estimate

The local operator (T) is normal.  On the three (S_3) isotypic sectors
([3],[1,1,1],[2,1]), its absolute value has eigenvalues (2,4,1),
respectively.  Let (s_i) and (a_i) be the symmetric and antisymmetric
three-replica probabilities of the one-site reduced state \(\rho_i\):

\[
s_i=\frac{1+3\operatorname{Tr}\rho_i^2
+2\operatorname{Tr}\rho_i^3}{6},
\]

\[
a_i=\det\rho_i
=\frac{1-3\operatorname{Tr}\rho_i^2
+2\operatorname{Tr}\rho_i^3}{6}.
\]

The polar-decomposition bound followed by Hölder gives

\[
\boxed{
\operatorname{Tr}S_z^3
\le\frac1{512}
\prod_{i=1}^3(1+7s_i+63a_i)^{1/3}.
}
\tag{5}

Indeed

\[
|T|=I+P_{[3]}+3P_{[1,1,1]},
\]

so

\[
|T|^3=I+7P_{[3]}+63P_{[1,1,1]}.
\]

The three local absolute-value operators commute, and Hölder bounds the
expectation of their product by the product of their cubic expectations.

For a fully product (z), (5) is sharp and both sides equal (1/64).
The bound is not presently strong enough to prove the global Ky--Fan
inequality; (2)--(5) are a new exact filter on the remaining high-purity
region, not a DTH resolution.
