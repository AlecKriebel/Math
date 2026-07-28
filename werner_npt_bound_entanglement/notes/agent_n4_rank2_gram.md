# The four-party rank-two copositivity reduction

## Research checkpoint

**2026-07-28 15:32 PDT.**  Let
\[
\mathcal B(H)
=6\operatorname{Tr}H^2
+\sum_{|S|=2}\|\operatorname{Tr}_S H\|_2^2
-3\sum_{|S|=1}\|\operatorname{Tr}_S H\|_2^2
\tag{1}
\]
for a Hermitian operator \(H\) on four physical parties.  Here
\(\operatorname{Tr}_S\) means that the parties in \(S\) are traced out.
For a rank-two projection \(P\), (1) is four times the candidate
\(H_1(P)\) used in the four-copy notes.

This attack does **not** prove \(\mathcal B(H)\geq0\) for every positive
rank-two \(H\).  It does produce:

1. the exact \(2\times2\) copositivity reduction;
2. a sum-of-squares formula and equality classification for both
   diagonal entries;
3. a single direct-sum Plücker norm inequality exactly equivalent to
   the missing cross-term estimate;
4. proofs of the estimate when either eigenvector is fully product, for
   every one-site logical-flag code, and whenever the whole operator has
   a common pure physical factor;
5. exact counterexamples to two stronger shortcuts: pairwise
   Cauchy--Schwarz and positive semidefiniteness of the full spectral
   Gram matrix;
6. an exact rank-three state with value \(-2/3\).

Thus the numerical rank-two conjecture survives, but the remaining
claim is genuinely global across the six physical pairs.

## 1. Polarization and the exact copositivity criterion

Let
\[
\mathcal B(H,G)
=6\operatorname{Tr}(HG)
+\sum_{|S|=2}
  \operatorname{Tr}\!\left[
  (\operatorname{Tr}_S H)(\operatorname{Tr}_S G)\right]
-3\sum_{|S|=1}
  \operatorname{Tr}\!\left[
  (\operatorname{Tr}_S H)(\operatorname{Tr}_S G)\right].
\tag{2}
\]
This is the real symmetric polarization of (1).

Diagonalize a positive rank-at-most-two operator as
\[
H=\lambda P_u+\mu P_v,\qquad
P_u=|u\rangle\langle u|,\quad
P_v=|v\rangle\langle v|,
\qquad
\langle u,v\rangle=0,
\tag{3}
\]
where \(\lambda,\mu\geq0\).  Put
\[
a=\mathcal B(P_u),\qquad
b=\mathcal B(P_u,P_v),\qquad
c=\mathcal B(P_v).
\tag{4}
\]
Then
\[
\boxed{\quad
\mathcal B(H)=a\lambda^2+2b\lambda\mu+c\mu^2.
\quad}
\tag{5}
\]
Once \(a,c\geq0\) are known, (5) is nonnegative for every
\(\lambda,\mu\geq0\) if and only if
\[
\boxed{\quad b\geq-\sqrt{ac}.\quad}
\tag{6}
\]
Indeed, only \(b<0\) is nontrivial; in that case (6) is equivalent to
\(b^2\leq ac\).  This is copositivity, not positive semidefiniteness:
there is no upper bound on a positive \(b\).

## 2. Exact diagonal sum of squares

For a unit vector \(x\), let
\[
\rho_S^x=\operatorname{Tr}_{\bar S}P_x,
\qquad
p_S(x)=\operatorname{Tr}[(\rho_S^x)^2].
\tag{7}
\]
Purity of complementary reductions gives
\[
\mathcal B(P_x)
=6+\sum_{i<j}p_{ij}(x)-3\sum_i p_i(x).
\tag{8}
\]
Define
\[
d_{ij}(x)=1-p_i(x)-p_j(x)+p_{ij}(x).
\tag{9}
\]
Then
\[
\boxed{\quad
\mathcal B(P_x)=\sum_{i<j}d_{ij}(x).
\quad}
\tag{10}
\]

Let \(F_i\) swap the \(i\)-th parties of two replicas and
\(A_i=(I-F_i)/2\).  A direct swap contraction gives
\[
d_{ij}(x)
=\langle x\otimes x|(I-F_i)(I-F_j)|x\otimes x\rangle
=4\|A_iA_j(x\otimes x)\|^2.
\tag{11}
\]
Thus
\[
\boxed{\quad
\mathcal B(P_x)\geq0
\quad\text{for every pure }x.
\quad}
\tag{12}
\]
This is the elementary subadditivity of linear entropy, with its full
sum-of-squares proof included.

### Equality

For a nonzero unit vector \(x\),
\[
\boxed{\quad
\mathcal B(P_x)=0
\quad\Longleftrightarrow\quad
x=x_1\otimes x_2\otimes x_3\otimes x_4.
\quad}
\tag{13}
\]
To prove the nontrivial direction, all six nonnegative terms in (10)
must vanish.  Decompose \(x\otimes x\) into the joint local-swap sectors.
It is globally symmetric, so only sectors with an even number of local
antisymmetries occur.  Any nonempty such sector contains a pair
\(\{i,j\}\) and contributes positively to (11).  Therefore only the
all-symmetric sector remains.  In particular
\(\langle x\otimes x|F_i|x\otimes x\rangle=p_i(x)=1\) for every \(i\).
Every one-party marginal is pure, which successively factors \(x\)
across all four parties.  The converse is immediate.

## 3. Exact formula for the cross entry

For \(S\subseteq[4]\), define the transition reduction
\[
T_S=\operatorname{Tr}_{\bar S}|u\rangle\langle v|.
\tag{14}
\]
The elementary complementary contraction identity is
\[
\boxed{\quad
\|T_S\|_2^2
=\operatorname{Tr}(\rho_{\bar S}^u\rho_{\bar S}^v).
\quad}
\tag{15}
\]
For example, across the bipartition \(S:\bar S\), write \(u,v\) as
coefficient matrices \(U,V\).  Then
\[
T_S=UV^\dagger,\qquad
\|T_S\|_2^2
=\operatorname{Tr}(U^\dagger U\,V^\dagger V),
\tag{16}
\]
which is precisely the overlap of the complementary reductions.

Using (15), orthogonality, and the fact that complementation permutes
the six two-element subsets gives
\[
\boxed{\quad
b
=\sum_{|S|=2}\|T_S\|_2^2
-3\sum_{i=1}^4\|T_i\|_2^2.
\quad}
\tag{17}
\]
Consequently the complete missing scalar inequality is
\[
\boxed{\quad
3\sum_i\|T_i\|_2^2-\sum_{i<j}\|T_{ij}\|_2^2
\leq
\sqrt{\mathcal B(P_u)\mathcal B(P_v)}.
\quad}
\tag{18}
\]

## 4. A single direct-sum Plücker norm inequality

Formula (18) has a useful two-replica form.  For \(i<j\), put
\[
\begin{aligned}
q_{ij}(x)&=2A_iA_j(x\otimes x),\\
s_{ij}(u,v)&=A_iA_j(u\otimes v+v\otimes u),\\
r_{ij}(u,v)&=A_iA_j(u\otimes v-v\otimes u).
\end{aligned}
\tag{19}
\]
Regard the six vectors of each kind as one vector in the orthogonal
direct sum over the physical pairs:
\[
q(x)=\bigoplus_{i<j}q_{ij}(x),\qquad
s=\bigoplus_{i<j}s_{ij},\qquad
r=\bigoplus_{i<j}r_{ij}.
\tag{20}
\]
Equation (11) says
\[
\|q(u)\|^2=a,\qquad \|q(v)\|^2=c.
\tag{21}
\]
Moreover,
\[
\begin{aligned}
\|s_{ij}\|^2-\|r_{ij}\|^2
&=4\operatorname{Re}
  \langle A_iA_j(u\otimes v),A_iA_j(v\otimes u)\rangle\\
&=\langle u\otimes v|
  (I-F_i)(I-F_j)F_{\overline{\{i,j\}}}
  |u\otimes v\rangle .
\end{aligned}
\tag{22}
\]
Summing (22) and expanding the swaps reproduces (17):
\[
\boxed{\quad b=\|s\|^2-\|r\|^2.\quad}
\tag{23}
\]

Therefore the rank-two conjecture is exactly the following statement:
\[
\boxed{\quad
\|r(u,v)\|^2
\leq
\|s(u,v)\|^2+\|q(u)\|\,\|q(v)\|
\quad(\langle u,v\rangle=0).
\quad}
\tag{24}
\]
The tensors in (19) all come from the same two-plane
\(\operatorname{span}\{u,v\}\).  In particular \(r\) is built from the
single decomposable bivector \(u\wedge v\), while \(q(u),q(v),s\) are
its symmetric companions.  Equation (24), rather than six independent
Cauchy--Schwarz inequalities, is the precise global Plücker
bottleneck.

For comparison with sector notation, let
\[
c_R=\| \Pi_R(u\otimes v)\|^2,
\qquad
\alpha_R(x)=\|\Pi_R(x\otimes x)\|^2.
\tag{25}
\]
Global swap parity gives
\[
\begin{aligned}
\|r\|^2&=12\sum_{|R|=3}c_R,\\
\|s\|^2&=4\left(\sum_{|R|=2}c_R+6c_{[4]}\right),\\
\|q(x)\|^2&=4\left(
 \sum_{|R|=2}\alpha_R(x)+6\alpha_{[4]}(x)\right).
\end{aligned}
\tag{26}
\]
Thus (24) is exactly the spectral cross-term form of
\(e_2+6e_4\geq3o_3\).

## 5. The boundary case: one eigenvector is product

The equality classification (13) makes the boundary \(a=0\) completely
tractable.

### Proposition 1

If \(u\) is fully product and \(\langle u,v\rangle=0\), then
\[
\boxed{\quad b\geq0.\quad}
\tag{27}
\]
Consequently (6) holds whenever \(a=0\) or \(c=0\).

#### Proof

Apply local unitaries so that
\[
u=|0,0,0,0\rangle.
\tag{28}
\]
Expand \(v=\sum_xv_x|x\rangle\), where each local basis has
\(|0\rangle\) as its first vector, and define the excitation support
\[
R(x)=\{i:x_i\neq0\}.
\tag{29}
\]
From (14),
\[
\|T_S\|_2^2=\sum_{R(x)\subseteq S}|v_x|^2.
\tag{30}
\]
In (17), a coefficient with \(|R(x)|=r\) is
\[
\binom{4-r}{2-r}
-3\binom{4-r}{1-r},
\tag{31}
\]
where a binomial coefficient is zero when its lower argument is
negative.  For \(r=0,1,2,3,4\), these coefficients are
\[
-6,\quad0,\quad1,\quad0,\quad0.
\tag{32}
\]
Orthogonality gives \(v_{0000}=0\), so the negative \(r=0\) term is
absent.  Hence
\[
\boxed{\quad
b=\sum_{|R(x)|=2}|v_x|^2\geq0.
\quad}
\tag{33}
\]
\(\square\)

For two product basis strings, (33) says that \(b=1\) when they differ
at exactly two sites and \(b=0\) otherwise.

## 6. A bipartite determinant lemma

The next lemma proves a nontrivial global subclass.

### Lemma 2

Let \(x,y\) be unit vectors on a bipartite space \(A\otimes B\), and
put
\[
Z_A=\operatorname{Tr}_B|x\rangle\langle y|.
\tag{34}
\]
Then
\[
\boxed{\quad
|\langle x,y\rangle|^2-\|Z_A\|_2^2
\leq
\sqrt{
\left(1-\operatorname{Tr}[(\rho_A^x)^2]\right)
\left(1-\operatorname{Tr}[(\rho_A^y)^2]\right)}.
\quad}
\tag{35}
\]

#### Proof

Write \(x,y\) as coefficient matrices \(X,Y\), normalized in
Hilbert--Schmidt norm.  Local unitaries put
\[
X=\operatorname{diag}(s_1,\ldots,s_r)
\tag{36}
\]
inside a possibly rectangular zero-padded matrix, with \(s_j\geq0\).
In this basis,
\[
\begin{aligned}
|\langle x,y\rangle|^2-\|Z_A\|_2^2
&=\left|\sum_j s_jY_{jj}\right|^2
 -\sum_{i,j}s_j^2|Y_{ij}|^2\\
&\leq\sum_{j<k}
\left[
2s_js_k\operatorname{Re}(Y_{jj}\overline{Y_{kk}})
-s_j^2|Y_{kj}|^2-s_k^2|Y_{jk}|^2
\right].
\end{aligned}
\tag{37}
\]
The inequality only discards additional nonpositive terms outside the
support of \(X\).  For every \(j<k\), arithmetic--geometric mean and
the reverse triangle inequality give, successively,
\[
\begin{aligned}
&2s_js_k\operatorname{Re}(Y_{jj}\overline{Y_{kk}})
-s_j^2|Y_{kj}|^2-s_k^2|Y_{jk}|^2\\
&\quad\leq
2s_js_k\left(|Y_{jj}Y_{kk}|-|Y_{jk}Y_{kj}|\right)\\
&\quad\leq
2s_js_k
\left|Y_{jj}Y_{kk}-Y_{jk}Y_{kj}\right|.
\end{aligned}
\tag{38}
\]
Cauchy--Schwarz now gives
\[
\text{left side of (35)}
\leq
2\sqrt{\sum_{j<k}s_j^2s_k^2}\,
\sqrt{\sum_{j<k}
|Y_{jj}Y_{kk}-Y_{jk}Y_{kj}|^2}.
\tag{39}
\]
Finally,
\[
1-\operatorname{Tr}[(\rho_A^x)^2]
=2\sum_{j<k}s_j^2s_k^2,
\tag{40}
\]
while the second factor in (39) is a sub-sum of all squared
\(2\times2\) minors of \(Y\).  The singular-value identity
\[
1-\operatorname{Tr}[(\rho_A^y)^2]
=2\sum_{\substack{I,J\\|I|=|J|=2}}|\det Y_{I,J}|^2
\tag{41}
\]
therefore completes the proof.  Identity (41) follows directly by
diagonalizing \(Y\): both sides become
\(2\sum_{j<k}\sigma_j(Y)^2\sigma_k(Y)^2\). \(\square\)

## 7. One-site logical flags

### Proposition 3

Let
\[
u=|0\rangle_1\otimes|\phi\rangle_{234},
\qquad
v=|1\rangle_1\otimes|\psi\rangle_{234},
\tag{42}
\]
where \(\phi,\psi\) are arbitrary unit vectors.  Then (6) holds, and
hence
\[
\mathcal B(\lambda P_u+\mu P_v)\geq0
\qquad(\lambda,\mu\geq0).
\tag{43}
\]

#### Proof

For \(j=2,3,4\), write
\[
\ell_j(\phi)=1-\operatorname{Tr}[(\rho_j^\phi)^2],
\qquad
\ell_j(\psi)=1-\operatorname{Tr}[(\rho_j^\psi)^2].
\tag{44}
\]
The product flag makes every defect in (10) involving site \(1\)
vanish.  Purity of complementary reductions in a three-party pure
state then gives
\[
a=\sum_{j=2}^4\ell_j(\phi),
\qquad
c=\sum_{j=2}^4\ell_j(\psi).
\tag{45}
\]
Put \(g=\langle\phi,\psi\rangle\) and
\[
Z_j=\operatorname{Tr}_{\{2,3,4\}\setminus\{j\}}
|\phi\rangle\langle\psi|.
\tag{46}
\]
Only transition reductions retaining the flag survive in (17), so
\[
b=\sum_{j=2}^4\|Z_j\|_2^2-3|g|^2.
\tag{47}
\]
Apply Lemma 2 to each bipartition
\(j:\{2,3,4\}\setminus\{j\}\):
\[
|g|^2-\|Z_j\|_2^2
\leq\sqrt{\ell_j(\phi)\ell_j(\psi)}.
\tag{48}
\]
Summing and applying Cauchy--Schwarz gives
\[
-b
\leq\sum_j\sqrt{\ell_j(\phi)\ell_j(\psi)}
\leq
\sqrt{\left(\sum_j\ell_j(\phi)\right)
      \left(\sum_j\ell_j(\psi)\right)}
=\sqrt{ac}.
\tag{49}
\]
This is (6). \(\square\)

If \(\phi=\psi\), every inequality above is an equality:
\[
a=c=:L
=3-\sum_{j=2}^4\operatorname{Tr}[(\rho_j^\phi)^2],
\qquad b=-L.
\tag{50}
\]
More transparently, if the common value is \(L\), then
\[
\boxed{\quad
\mathcal B(\lambda P_u+\mu P_v)=L(\lambda-\mu)^2.
\quad}
\tag{51}
\]
Thus the equal-weight logical-flag family is a large exact zero set.

## 8. A common pure physical factor

There is another dimension-independent positive subclass.  Suppose
\[
H=G_{123}\otimes|\eta\rangle\langle\eta|_4,
\qquad G\succeq0.
\tag{52}
\]
For
\[
\begin{aligned}
h&=\operatorname{Tr}G^2,\qquad t=\operatorname{Tr}G,\\
A_1&=\sum_{i=1}^3\|\operatorname{Tr}_iG\|_2^2,\qquad
A_2=\sum_{i<j}\|\operatorname{Tr}_{ij}G\|_2^2,
\end{aligned}
\tag{53}
\]
direct substitution gives
\[
\mathcal B(H)=3h-2A_1+A_2.
\tag{54}
\]
Define
\[
Q_3(G)=h-\frac12A_1+\frac14A_2-\frac18t^2.
\tag{55}
\]
On two replicas,
\[
Q_3(G)
=\operatorname{Tr}\!\left[
(G\otimes G)
\bigotimes_{i=1}^3\left(I-\frac12F_i\right)
\right].
\tag{56}
\]
The tensor-product operator in (56) is at least \(I/8\).  Since
\(G\otimes G\succeq0\),
\[
Q_3(G)\geq\frac18t^2.
\tag{57}
\]
Combining (54)--(57) yields
\[
\mathcal B(H)
=4Q_3(G)-h+\frac12t^2
\geq t^2-h\geq0,
\tag{58}
\]
where the last inequality is elementary for \(G\succeq0\).  No rank
assumption is needed in this subclass.

## 9. Two exact obstructions to stronger Gram arguments

### 9.1 Pair-by-pair Cauchy--Schwarz is false

Writing (23) as a sum over pairs suggests proving each term separately:
\[
\|r_{ij}\|^2
\stackrel{?}{\leq}
\|s_{ij}\|^2+\|q_{ij}(u)\|\,\|q_{ij}(v)\|.
\tag{59}
\]
This is false, even inside a global equality code.

Take four qubits and
\[
\begin{aligned}
u&=\frac{|0000\rangle+|1010\rangle}{\sqrt2},\\
v&=\frac{|0100\rangle+|1110\rangle}{\sqrt2}.
\end{aligned}
\tag{60}
\]
The second site is a logical flag, the fourth is a common pure factor,
and the first and third sites carry a Bell pair.  For the physical pair
\(\{1,2\}\),
\[
d_{12}(u)=d_{12}(v)=0,
\qquad
\|s_{12}\|^2-\|r_{12}\|^2=-\frac12.
\tag{61}
\]
Thus (59) fails with a zero right-hand correction.  Globally,
\[
a=c=1,\qquad b=-1,
\tag{62}
\]
so (6) is saturated.  Compensation necessarily crosses different
physical pairs.

### 9.2 The full spectral matrix need not be positive semidefinite

An ordinary Gram proof would establish the stronger two-sided estimate
\(|b|\leq\sqrt{ac}\).  That is false.  Take
\[
\begin{aligned}
u&=\frac{|0000\rangle-|1000\rangle}{\sqrt2},\\
v&=\frac{-|0100\rangle+|0101\rangle
               +|0110\rangle+|0111\rangle}{2}.
\end{aligned}
\tag{63}
\]
They are orthonormal, and exact contraction gives
\[
\boxed{\quad
a=0,\qquad b=\frac38,\qquad c=1.
\quad}
\tag{64}
\]
Thus
\[
ac-b^2=-\frac9{64}<0,
\tag{65}
\]
although copositivity is automatic here because \(b>0\).
This proves that (6) cannot come from a Hilbert-space Gram
representation of all three entries in (4).

There is also a short conceptual check of \(b=3/8\).  The vector \(u\)
is product.  After rotating its first local factor to \(|0\rangle\),
Proposition 1 says that \(b\) is the probability that \(v\) has exactly
two excited sites.  Site \(2\) is always excited; site \(1\) is excited
with probability \(1/2\); and the maximally entangled state on sites
\(3,4\) has excitation-count probabilities \(1/4,1/2,1/4\).  Hence
\[
b=\frac12\frac12+\frac12\frac14=\frac38.
\tag{66}
\]

## 10. The rank cutoff is essential

Let every local physical space be a qutrit.  Define
\[
|\mathrm{GHZ}_3\rangle
=\frac{|000\rangle+|111\rangle+|222\rangle}{\sqrt3}
\tag{67}
\]
on sites \(1,2,3\), and take
\[
H_3
=|\mathrm{GHZ}_3\rangle\langle\mathrm{GHZ}_3|
\otimes\frac{I_3}{3}
\tag{68}
\]
on sites \(1,2,3,4\).  This state has rank three.  Its purity is
\(1/3\).  The sums in (1) are
\[
\sum_{|S|=1}\|\operatorname{Tr}_S H_3\|_2^2=\frac43,
\qquad
\sum_{|S|=2}\|\operatorname{Tr}_S H_3\|_2^2=\frac43.
\tag{69}
\]
Therefore
\[
\boxed{\quad
\mathcal B(H_3)
=6\left(\frac13\right)+\frac43-3\left(\frac43\right)
=-\frac23.
\quad}
\tag{70}
\]
Equivalently, (68) is obtained by tracing the reference qutrit out of
\(|\Omega_3\rangle_{K4}\otimes|\mathrm{GHZ}_3\rangle_{123}\).

Replacing \(I_3/3\) by \(I_2/2\) makes the rank two and changes (70) to
zero for every pure three-party factor.  This is exactly the
logical-flag equality mechanism in Section 7.

## 11. Minimal exact audit

This standard-library script represents each pure vector by integer
amplitudes and a separately computed normalization.  It verifies the
two rank-two examples and the rank-three counterexample using only
rational arithmetic.

```python
from fractions import Fraction as F
from itertools import combinations

def reduction(ensemble, traced):
    # ensemble entries are (rational weight, {basis_tuple: integer amp})
    traced = set(traced)
    keep = tuple(i for i in range(4) if i not in traced)
    out = {}
    for weight, vector in ensemble:
        norm = sum(a*a for a in vector.values())
        for x, ax in vector.items():
            for y, ay in vector.items():
                if all(x[i] == y[i] for i in traced):
                    key = (tuple(x[i] for i in keep),
                           tuple(y[i] for i in keep))
                    out[key] = out.get(key, F(0)) + weight*F(ax*ay, norm)
    return {key: value for key, value in out.items() if value}

def hs_squared(matrix):
    return sum(value*value for value in matrix.values())

def B(ensemble):
    value = 6*hs_squared(reduction(ensemble, ()))
    value += sum(hs_squared(reduction(ensemble, S))
                 for S in combinations(range(4), 2))
    value -= 3*sum(hs_squared(reduction(ensemble, (i,)))
                   for i in range(4))
    return value

def polarized(u, v):
    a = B([(F(1), u)])
    c = B([(F(1), v)])
    total = B([(F(1), u), (F(1), v)])
    return a, (total-a-c)/2, c, total

# Logical-flag equality, equations (60)--(62).
u_flag = {(0,0,0,0): 1, (1,0,1,0): 1}
v_flag = {(0,1,0,0): 1, (1,1,1,0): 1}
assert polarized(u_flag, v_flag) == (1, -1, 1, 0)

# Positive cross entry and indefinite full 2-by-2 matrix, (63)--(65).
u_pos = {(0,0,0,0): 1, (1,0,0,0): -1}
v_pos = {
    (0,1,0,0): -1, (0,1,0,1): 1,
    (0,1,1,0): 1,  (0,1,1,1): 1,
}
assert polarized(u_pos, v_pos) == (0, F(3,8), 1, F(7,4))

# Rank-three state GHZ_3 tensor I_3/3, equations (67)--(70).
rank_three = []
for d in range(3):
    vector = {(r,r,r,d): 1 for r in range(3)}
    rank_three.append((F(1,3), vector))
assert B(rank_three) == F(-2,3)
```

## 12. Exact status and remaining bottleneck

Proved here:

* the exact polarization and copositivity criterion (6);
* the diagonal SOS (10)--(12) and its equality classification;
* the transition-reduction formula (17);
* the equivalent global Plücker norm inequality (24);
* copositivity on the product boundary, for all one-site logical flags,
  and for operators with a common pure physical factor;
* exact obstructions to pairwise CS and full Gram positivity;
* the exact rank-three counterexample.

Not proved:

* inequality (24) for arbitrary orthogonal \(u,v\);
* equivalently, (6) for every rank-two positive \(H\);
* consequently, the four-copy projection inequality or any all-copy
  conclusion.

The cleanest remaining target is (24).  The logical-flag equality
family proves that both the positive symmetric-cross term \(\|s\|^2\)
and compensation between different physical pairs are indispensable.
A viable SOS must retain the common Plücker relations among all six
pair projections simultaneously.
