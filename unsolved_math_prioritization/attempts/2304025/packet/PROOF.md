# Proofs of the scoped results

## 1. The precise problem and normalization

Let
\[
E_\lambda(P)=\frac1{2\pi}\int_{-\pi}^{\pi}|1-e^{i\theta}|^{2\lambda}|P(e^{i\theta})|^2\,d\theta,
\quad
F(\lambda)=\inf\{E_\lambda(P):P\in\mathbb Z[z]\text{ is monic}\}.
\]
The degree is unrestricted. Multiplication by a monomial does not change the energy, so none of the results depends on whether constant polynomials are admitted. Multiplying the normalized conclusions by \(2\pi\) answers the corresponding portions of the printed question.

For \(\alpha\ge0\), put
\[
C(\alpha)=\frac1{2\pi}\int_{-\pi}^{\pi}|1-e^{i\theta}|^{2\alpha}\,d\theta
=\frac{\Gamma(2\alpha+1)}{\Gamma(\alpha+1)^2}.
\tag{1}
\]
The equality follows by substituting \(t=\theta/2\), evaluating the beta integral for \(\sin^{2\alpha}t\), and using the gamma duplication identity. In particular \(C(0)=1,C(1)=2\).

A useful weak bound is \(F(\lambda)\ge1\) for every \(\lambda>0\). Indeed, remove any zero constant terms from an integer polynomial by dividing by a power of \(z\). The analytic function \((1-z)^\lambda P(z)\), with the branch equal to 1 at zero, is continuous on the closed unit disc and has constant coefficient a nonzero integer. Its squared Hardy norm equals \(E_\lambda(P)\), and Parseval bounds it below by the square of that coefficient. This bound alone does not solve the problem.

## 2. Fourier coefficients and a discrete energy identity

For \(\alpha>0\), define
\[
c_k(\alpha)=\frac1{2\pi}\int_{-\pi}^{\pi}|1-e^{i\theta}|^{2\alpha}e^{-ik\theta}\,d\theta.
\]
These coefficients are real and satisfy \(c_{-k}=c_k\), \(c_0=C(\alpha)\), and
\[
c_{k+1}(\alpha)=\frac{k-\alpha}{k+\alpha+1}c_k(\alpha),\qquad k\ge0.
\tag{2}
\]
Here is a derivation valid also at integer \(\alpha\). Write
\(J_k=\int_0^\pi\sin^{2\alpha}(t)\cos(2kt)\,dt\), so that \(c_k=4^\alpha J_k/\pi\). Integrate the derivative of
\(\sin^{2\alpha+1}(t)\cos((2k+1)t)\) from 0 to \(\pi\). The boundary terms vanish, and the derivative is integrable. Product-to-sum identities give
\[
0=(\alpha-k)J_k+(\alpha+k+1)J_{k+1},
\]
which proves (2).

When \(0<\alpha<1\), set \(b_k=-c_k\) for \(k\ge1\). Formula (2) shows that all \(b_k\) are strictly positive and strictly decreasing. Moreover,
\[
\frac{b_{k+1}}{b_k}=1-\frac{2\alpha+1}{k+\alpha+1},\qquad k\ge1,
\]
so a logarithmic product estimate gives \(b_k=O(k^{-2\alpha-1})\). Thus the Fourier series is absolutely convergent. It represents its continuous weight; evaluation at \(\theta=0\) gives
\[
C(\alpha)=2\sum_{k\ge1}b_k.
\tag{3}
\]
For \(\alpha=1\), the same identities hold with \(C(1)=2,b_1=1\), and \(b_k=0\) for \(k>1\).

Extend any finite real coefficient sequence \(a_j\) by zero to all \(j\in\mathbb Z\). Fourier expansion and (3) give
\[
E_\alpha\left(\sum_j a_jz^j\right)
=\sum_{k\ge1}b_k\sum_{j\in\mathbb Z}(a_{j+k}-a_j)^2,
\qquad0<\alpha\le1.
\tag{4}
\]
All sums converge; for large \(k\) the inner sum is twice \(\sum_j a_j^2\). Expanding the squares recovers
\(C(\alpha)\sum_j a_j^2+2\sum_{k\ge1}c_k\sum_j a_ja_{j+k}\), proving the identity without a conditional rearrangement.

### Lemma 1: nonzero integral sequences

Every nonzero finite integer sequence has \(E_\alpha\ge C(\alpha)\) for \(0<\alpha\le1\).

For a fixed \(k\ge1\), split the sequence into residue classes modulo \(k\). At least one of these chains is nonzero and is zero at both sufficiently remote ends. Its successive differences are integers, are not all zero, and sum to zero. Consequently at least two of them are nonzero and their squared sum is at least 2. The inner sum in (4) is therefore at least 2 for every \(k\). Sum against \(b_k\) and use (3).

For \(0<\alpha<1\), equality is possible only for a signed monomial. If there is more than one nonzero coefficient, or a coefficient of absolute value greater than 1, then \(\sum a_j^2>1\). For every \(k\) larger than the support diameter, the inner sum in (4) exceeds 2; its weight is strictly positive. A signed monomial does attain equality. At \(\alpha=1\), geometric sums also attain it.

## 3. Exact answer for \(0<\lambda\le2\)

**Theorem 1.**
\[
F(\lambda)=
\begin{cases}
C(\lambda),&0<\lambda\le1,\\
2C(\lambda-1),&1\le\lambda\le2.
\end{cases}
\tag{5}
\]
For \(0<\lambda<1\), the monic minimizers are precisely the monomials. For \(1<\lambda<2\), the infimum is not attained.

The first range follows immediately from Lemma 1 and \(P=1\) (or \(P=z\)). For the second range, write \(\alpha=\lambda-1\), and put \(Q=(1-z)P\). Its coefficients are integers and sum to zero. Decompose its nonzero coefficient sequence as \(Q=A-B\), with \(A,B\) nonzero polynomials having nonnegative integer coefficients and disjoint supports. For \(0<\alpha\le1\),
\[
E_\alpha(Q)=E_\alpha(A)+E_\alpha(B)
-2\sum_{i,j}a_i b_j c_{i-j}(\alpha)
\ge E_\alpha(A)+E_\alpha(B)\ge2C(\alpha).
\tag{6}
\]
In the middle sum, \(i\ne j\) because the supports are disjoint, and \(c_{i-j}\le0\). For \(0<\alpha<1\), the first inequality is strict: there is at least one positive coefficient on each support, and every corresponding off-diagonal Fourier coefficient is strictly negative. For \(\alpha=0\), ordinary Parseval gives \(E_0(Q)\ge2\) directly.

For the matching upper bound, take the monic geometric sum
\[
S_N(z)=1+z+\cdots+z^{N-1},\qquad (1-z)S_N=1-z^N.
\]
Then
\[
E_{1+\alpha}(S_N)=E_\alpha(1-z^N)=2\big(C(\alpha)-c_N(\alpha)\big).
\tag{7}
\]
For \(0<\alpha<1\), \(c_N\to0\), so these values decrease to \(2C(\alpha)\), proving the infimum and its nonattainment. At \(\alpha=0\), every \(N\ge1\) has energy 2. At \(\alpha=1\), every \(N\ge2\) has energy 4. Thus the shared endpoints in (5) are included and consistent.

## 4. Integer exponents and equal power sums

For a positive integer \(m\), put \(Q=(z-1)^mP\). Multiplication gives a bijection from monic integer polynomials \(P\) to monic integer polynomials \(Q\) divisible by \((z-1)^m\). The converse uses polynomial division by the monic integer divisor. Parseval says
\[
E_m(P)=\sum_j q_j^2.
\tag{8}
\]
The possible energies form a nonempty set of positive integers, so their infimum is an attained minimum. They are even, because \(q_j^2\equiv q_j\pmod2\) and \(Q(1)=\sum q_j=0\).

### Lemma 2: the mass bound

For a nonzero integer polynomial divisible by \((z-1)^m\), let
\[
T=\sum_{q_j>0}q_j=\sum_{q_j<0}(-q_j).
\]
Then \(T\ge m\).

Let \(X\) be the multiset containing \(j\) with multiplicity \(q_j\) when positive, and let \(Y\) be its negative counterpart. Each has size \(T\). Applying \((z\,d/dz)^r\) at 1, for \(0\le r<m\), proves equality of their power sums. If \(T<m\), their first \(T\) power sums agree. Newton's identities then give identical elementary symmetric functions, so \(\prod_{x\in X}(t-x)=\prod_{y\in Y}(t-y)\). Thus the multisets coincide, contradicting their disjoint supports and nonemptiness. Therefore \(T\ge m\). This is the classical Prouhet–Tarry–Escott/Newton-identity argument; see `SOURCES.md`.

Since \(q_j^2\ge|q_j|\), (8) and Lemma 2 prove
\[
F(m)\ge2m.
\tag{9}
\]
Equality holds if and only if every nonzero \(q_j\) is \(\pm1\) and the positive and negative supports each have size \(m\). Equivalently, there must be two disjoint sets of \(m\) distinct nonnegative integers with matching power sums through degree \(m-1\). Conversely, any such sets define a polynomial \(Q\) with the required zero multiplicity; negate it if necessary to make its leading coefficient 1 and divide by \((z-1)^m\). Sets of arbitrary integers can first be translated by a common integer to become nonnegative; the binomial theorem preserves every required power-sum equality. Hence this is also an equivalence with distinct-element integer sets.

**The distinct-element condition matters.** An ideal power-sum solution allowing repeated elements does not by itself give equality in the squared-coefficient norm: repetitions create coefficient magnitudes greater than 1.

The following explicit choices give equality for \(m=1,\ldots,6\). If \(D_m\) is the indicated list, take
\[
P_m(z)=\prod_{d\in D_m}S_d(z),\qquad
(1-z)^mP_m(z)=\prod_{d\in D_m}(1-z^d).
\tag{10}
\]
Use
\[
\begin{aligned}
D_1&=(1),&D_2&=(1,2),&D_3&=(1,2,3),\\
D_4&=(1,2,3,5),&D_5&=(1,2,3,5,7),&D_6&=(1,2,3,4,5,7).
\end{aligned}
\]
Direct expansion gives respectively \(2m\) coefficients of magnitude 1 and no others. Each \(P_m\) is monic and integral. Therefore \(F(m)=2m\) for these six values. The verifier prints/checks the full expansions; no finite search is needed for the general lower bound.

For arbitrary \(m\), binary-spaced factors \(\prod_{j=0}^{m-1}(1-z^{2^j})\) have distinct subset sums and exactly \(2^m\) signed coefficients. Thus the general elementary bounds are
\[
2m\le F(m)\le2^m.
\tag{11}
\]
This is not a determination of \(F(m)\) for all \(m\), and no assertion is made here about which larger individual cases are already known.

## 5. Higher noninteger parameters: bounds and the remaining gap

Let \(m\ge1\) be an integer and \(0<\alpha<1\). Again put \(Q=(z-1)^mP=A-B\). Its positive and negative coefficient masses equal some \(T\ge m\). Define
\[
G_\alpha(s)=E_\alpha(S_s)
=sC(\alpha)+2\sum_{k=1}^{s-1}(s-k)c_k(\alpha),\qquad s\ge1,
\quad G_\alpha(0)=0.
\tag{12}
\]
We claim that every nonnegative finite integer coefficient sequence \(A\) of total mass \(T\) satisfies
\[
E_\alpha(A)\ge G_\alpha(T).
\tag{13}
\]
First suppose \(A\) is the indicator of a set of size \(s\), with support \(i_1<\cdots<i_s\). For \(r<t\), \(i_t-i_r\ge t-r\); since \(b_k\) decreases, its energy
\(sC(\alpha)-2\sum_{r<t}b_{i_t-i_r}\) is at least the energy of a consecutive interval of size \(s\), namely \(G_\alpha(s)\).

For general \(A\), write its coefficients as sums of indicator functions of the integer levels \(L_\ell=\{j:a_j\ge\ell\}\). For integer \(u,v\ge0\),
\((u-v)^2\ge|u-v|=\sum_{\ell\ge1}|1_{u\ge\ell}-1_{v\ge\ell}|\).
Use (4) to obtain \(E_\alpha(A)\ge\sum_\ell E_\alpha(1_{L_\ell})\ge\sum_\ell G_\alpha(|L_\ell|)\). Finally,
\(G_\alpha(s+t)\le G_\alpha(s)+G_\alpha(t)\): concatenate adjacent intervals of sizes \(s,t\), whose mutual Fourier cross terms are nonpositive. Iterating proves (13), since the level sizes sum to \(T\).

Also
\[
G_\alpha(s+1)-G_\alpha(s)
=C(\alpha)+2\sum_{k=1}^{s}c_k(\alpha)
=2\sum_{k>s}b_k>0.
\]
So \(G_\alpha\) is increasing. Applying (6) to \(Q\) now gives the universal bound
\[
F(m+\alpha)\ge2G_\alpha(m).
\tag{14}
\]
The simpler pointwise comparison \(|1-z|\le2\) on the circle gives an additional bound:
\[
E_{m+\alpha}(P)\ge4^{\alpha-1}E_{m+1}(P)
\quad\Longrightarrow\quad
F(m+\alpha)\ge2(m+1)4^{\alpha-1}.
\tag{15}
\]
These can be combined with the Hardy bound 1.

For the first unresolved fractional interval, \(m=2\), (2) gives
\(G_\alpha(2)=2C(\alpha)/(\alpha+1)\). For an explicit upper bound take
\[
P_N=S_N S_{N+1},\qquad
(1-z)^2P_N=1-z^N-z^{N+1}+z^{2N+1},\quad N\ge2.
\]
The exact normalized energy is
\[
E_{2+\alpha}(P_N)
=4C(\alpha)-4c_N(\alpha)-4c_{N+1}(\alpha)
 +2c_{2N+1}(\alpha)+2c_1(\alpha).
\tag{16}
\]
As \(N\to\infty\), this tends to
\(4C(\alpha)+2c_1(\alpha)=2(\alpha+2)C(\alpha)/(\alpha+1)\). Hence
\[
\max\left\{1,\frac{4C(\alpha)}{\alpha+1},6\,4^{\alpha-1}\right\}
\le F(2+\alpha)
\le\frac{2(\alpha+2)C(\alpha)}{\alpha+1}.
\tag{17}
\]
For example, since \(C(1/2)=4/\pi\),
\[
\frac{32}{3\pi}\le F(5/2)\le\frac{40}{3\pi}.
\]
The bounds differ; the packet proves neither is sharp.

The obstruction to simply repeating the preceding exact argument is visible in (2): for \(1<\lambda<2\), the coefficients \(c_k(\lambda)\) with \(k\ge2\) are positive. Thus the same sign-separated kernel argument does not apply directly to higher weights. Factoring off \((1-z)^m\) restores a positive fractional-difference kernel, but it also imposes \(m\) power-sum constraints on the integer coefficients. The inequalities above do not capture the full cost of those constraints.

**Exact remaining gap.** Determine the infimum for arbitrary real \(\lambda>2\), beyond the individually proved cases. In particular, this work neither closes (17) nor determines the squared-coefficient minimum (8) for every integer multiplicity. The distinct-term ideal equal-power-sum equivalence is a reduction, not a solution of those arithmetic existence questions. All finite checks below are controls on the displayed constructions and identities, not evidence certifying a full resolution.
