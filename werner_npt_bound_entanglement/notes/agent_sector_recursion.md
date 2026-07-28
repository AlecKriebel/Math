# Sequential local-swap sectors: exact recursions and scalar obstructions

**Research log — 2026-07-28 12:01 PDT**

**Checkpoint — 2026-07-28 12:14 PDT.**  The binomial identities
(13)--(19) and the spectral identities (61)--(64) were independently
replayed with exact rational arithmetic for \(1\leq h\leq30\).  Their
proofs below hold for arbitrary \(h\); the replay was only an arithmetic
audit.

This note studies only the rank-two **code-projector** endpoint problem.  Let
\[
U:K=\mathbb C^2\longrightarrow
H=V_1\otimes\cdots\otimes V_n
\]
be an isometry and let \(P=UU^\dagger\).  The target is
\[
Q_n(P):=
\operatorname{Tr}\!\left[(P\otimes P)
\prod_{i=1}^n\left(F_i-\frac12I\right)\right]\geq0,       \tag{1}
\]
where \(F_i\) swaps the two replicas of \(V_i\).

The assigned question was whether a sequential local-swap recursion yields
a cumulative or majorization inequality between the even and odd
local-antisymmetry masses that proves (1) uniformly in \(n\).

No all-\(n\) proof or counterexample was obtained.  The exact conclusions
are:

1. the natural stochastic-tail domination is false, and product codes make
   every fixed finite window of the corresponding Abel sum negative when
   the Hamming distance is large;
2. scalar prefix masses are not a closed recursion state;
3. the exact one-step state consists of four coupled
   symmetric/exterior-square maps arising from one common isometry;
4. each of the two tempting residual PSD inequalities is false;
5. a genuine, coordinatewise first-level cumulative inequality is proved,
   but its averaged layer form is much too weak;
6. odd-Hamming product equality codes rule out positive combinations of
   proper-prefix certificates and several stronger spectral
   majorizations.

The calculations below are exact and self-contained.

## 1. Sector polynomial and the endpoint

Put
\[
S_i=\frac{I+F_i}{2},\qquad A_i=\frac{I-F_i}{2},
\]
and, for \(R\subseteq[n]\), put
\[
\Pi_R=\prod_{i\in R}A_i\prod_{i\notin R}S_i,\qquad
r_R=\operatorname{Tr}[(P\otimes P)\Pi_R]\geq0.            \tag{2}
\]
The full physical replica swap is \(F_{[n]}=\prod_iF_i\).  Since
\[
(U\otimes U)F_K=F_{[n]}(U\otimes U),
\]
the even sectors in (2) are supported on
\(\operatorname{Sym}^2K\), of dimension \(3\), and the odd sectors are
supported on \(\Lambda^2K\), of dimension \(1\).  Consequently
\[
\sum_{|R|\ {\rm even}}r_R=3,\qquad
\sum_{|R|\ {\rm odd}}r_R=1.                              \tag{3}
\]

Define the multiaffine sector polynomial
\[
\mathcal F(t_1,\ldots,t_n)
 :=\sum_{R\subseteq[n]}(-1)^{|R|}r_R\prod_{i\in R}t_i
 =\operatorname{Tr}\!\left[(P\otimes P)
   \prod_{i=1}^n(S_i-t_iA_i)\right]                       \tag{4}
\]
and its diagonal restriction
\[
D(t):=\mathcal F(t,\ldots,t).
\]
Because
\[
F_i-\frac12I=\frac12(S_i-3A_i),
\]
the desired quantity is
\[
\boxed{\quad 2^nQ_n(P)=D(3).\quad}                        \tag{5}
\]

Write
\[
e_k=\sum_{|R|=k}r_R\quad(k\ {\rm even}),\qquad
o_k=\sum_{|R|=k}r_R\quad(k\ {\rm odd}).
\]
Thus
\[
D(3)=\sum_{k\ {\rm even}}3^ke_k-
      \sum_{k\ {\rm odd}}3^ko_k.                          \tag{6}
\]

## 2. The natural tail-majorization program fails exactly

For \(j\geq1\), define
\[
\delta_j=e_{2j}-3o_{2j+1},\qquad
T_j=\sum_{\ell\geq j}\delta_\ell.                         \tag{7}
\]
The normalization (3) gives the exact cancellation
\[
D(3)=\sum_{j\geq1}(9^j-1)\delta_j.                        \tag{8}
\]
Since \(\delta_j=T_j-T_{j+1}\), summation by parts gives
\[
\boxed{\quad
D(3)=8\sum_{j\geq1}9^{j-1}T_j.
\quad}                                                     \tag{9}
\]
It follows that the tail-majorization inequalities
\[
\sum_{\ell\geq j}e_{2\ell}
\ \geq\
3\sum_{\ell\geq j}o_{2\ell+1}
\quad\text{for every }j                                   \tag{10}
\]
would suffice.  They are false, even for two-dimensional subspaces
spanned by product vectors.

### 2.1 Exact product-code enumerator

Let
\[
u=\bigotimes_{i=1}^n|a_i\rangle,\qquad
v=\bigotimes_{i=1}^n|b_i\rangle
\]
be orthonormal product vectors such that, at every site, either
\(|a_i\rangle=|b_i\rangle\) or
\(\langle a_i,b_i\rangle=0\).  Let
\[
H_0=\{i:\langle a_i,b_i\rangle=0\},\qquad h=|H_0|\geq1,
\]
and let \(P=|u\rangle\langle u|+|v\rangle\langle v|\).

For each \(i\in H_0\), the two cross orientations decompose into the
normalized local symmetric and antisymmetric vectors with equal
amplitudes.  The global symmetric cross vector has only even local
antisymmetry parity, and the global exterior vector has only odd parity.
Each allowed pattern has squared amplitude \(2^{1-h}\).  The two self
pairs contribute only to the empty sector.  Hence
\[
\boxed{\quad
\sum_{R\subseteq[n]}r_R\prod_{i\in R}z_i
=2+2^{1-h}\prod_{i\in H_0}(1+z_i).
\quad}                                                     \tag{11}
\]
In particular,
\[
\sum_Rr_Rz^{|R|}=2+2^{1-h}(1+z)^h.                        \tag{12}
\]
Evaluating (12) at \(z=-3\) gives
\[
\boxed{\quad
D(3)=2+2(-1)^h
=
\begin{cases}
0,&h\ \text{odd},\\
4,&h\ \text{even}.
\end{cases}
\quad}                                                     \tag{13}
\]
Thus every odd \(h\) is an exact equality family.

For this family,
\[
\delta_j
=2^{1-h}\left[\binom h{2j}-3\binom h{2j+1}\right]
=2^{1-h}\binom h{2j}
  \frac{8j+1-3h}{2j+1},                                   \tag{14}
\]
where a binomial coefficient outside its range is zero.  Formula (14)
shows directly that many low layers are negative.

For \(h=4\),
\[
e_2=\frac68,\qquad o_3=\frac48,\qquad e_4=\frac18,
\]
so
\[
\delta_1=-\frac68,\quad \delta_2=\frac18,\qquad
T_1=-\frac58,\quad T_2=\frac18.                            \tag{15}
\]
Thus the very first inequality in (10) fails.  The high layer nevertheless
repairs the weighted sign:
\[
D(3)=8(T_1+9T_2)=4.
\]

One might try to repair (10) by pairing a negative tail with its successor,
requiring \(T_j+9T_{j+1}\geq0\).  The \(h=6\) product code refutes this:
\[
(\delta_1,\delta_2,\delta_3)
=\frac1{32}(-45,-3,1),
\]
\[
(T_1,T_2,T_3)
=\frac1{32}(-47,-2,1),                                    \tag{16}
\]
and hence
\[
T_1+9T_2=-\frac{65}{32}<0,
\]
while
\[
D(3)=8(T_1+9T_2+81T_3)=4.
\]

There is an obstruction at every fixed window depth, not just at
\(h=4,6\).  For the product code with \(n=h\), (12) gives
\[
T_j^{(h)}
=2^{1-h}\sum_{\ell\geq j}\binom h{2\ell}
-3\cdot2^{1-h}\sum_{\ell\geq j}\binom h{2\ell+1}.          \tag{17}
\]
For fixed \(j\), each full parity sum in (17), before deleting its
finitely many low layers, equals \(1\).  Moreover,
\[
2^{1-h}\binom hk\longrightarrow0
\qquad(h\longrightarrow\infty)
\]
for every fixed \(k\).  Therefore
\[
\boxed{\quad
\lim_{h\to\infty}T_j^{(h)}=-2
\quad\text{for every fixed }j.
\quad}                                                     \tag{18}
\]
In particular, for any fixed \(j,L\),
\[
\lim_{h\to\infty}
\sum_{r=0}^{L-1}9^rT_{j+r}^{(h)}
=-2\sum_{r=0}^{L-1}9^r<0.                                 \tag{19}
\]
Hence no proof that partitions the Abel sum (9) into uniformly bounded
positive-weight windows and proves each window nonnegative can work
uniformly in \(n\).  The compensation in (9) can be forced arbitrarily far
out in the sector layers.

## 3. Exact prefix-effect recursion

For a prefix of length \(m\) and \(R\subseteq[m]\), define the compressed
prefix effect
\[
\mathcal E_R^{(m)}
=(U^\dagger\otimes U^\dagger)
\left[
 \left(\prod_{\substack{i\leq m\\i\in R}}A_i\right)
 \left(\prod_{\substack{i\leq m\\i\notin R}}S_i\right)
 \otimes I_{m+1,\ldots,n}
\right]
(U\otimes U).                                              \tag{20}
\]
These effects satisfy:
\[
\mathcal E_R^{(m)}\succeq0,\qquad
\sum_{R\subseteq[m]}\mathcal E_R^{(m)}=I_{K\otimes K},     \tag{21}
\]
\[
\boxed{\quad
\mathcal E_R^{(m)}
=\mathcal E_R^{(m+1)}
 +\mathcal E_{R\cup\{m+1\}}^{(m+1)}.
\quad}                                                     \tag{22}
\]
Every \(\mathcal E_R^{(m)}\) commutes with the logical swap \(F_K\),
because the physical prefix projector commutes with the full physical
swap and \(U\otimes U\) intertwines the two full swaps.

At the final level there is the additional parity support condition
\[
\mathcal E_R^{(n)}
=\Pi_K^{(-1)^{|R|}}\mathcal E_R^{(n)}
 \Pi_K^{(-1)^{|R|}},                                      \tag{23}
\]
where \(\Pi_K^+\) and \(\Pi_K^-\) project onto
\(\operatorname{Sym}^2K\) and \(\Lambda^2K\), respectively.  Before the
final level, both logical parity blocks can occur in a single prefix
effect; the unseen sites can change the final parity.

Equations (20)--(23) are a closed **matrix-valued** binary-tree recursion.
Taking only the scalar masses
\[
r_R^{(m)}=\operatorname{Tr}\mathcal E_R^{(m)}
\]
destroys closure.

Here is an exact two-site demonstration.  Compare
\[
P_1=\operatorname{span}\{|00\rangle,|10\rangle\},\qquad
P_2=\operatorname{span}\{|00\rangle,|11\rangle\}.          \tag{24}
\]
For \(P_1\), the two codewords differ only at the first site; for \(P_2\),
they differ at both sites.  After measuring only the first local swap and
summing over the second site, both scalar prefix polynomials are
\[
3+z_1.                                                     \tag{25}
\]
Indeed, (11) gives \(3+z_1\) directly for \(P_1\), whereas for \(P_2\)
one sets \(z_2=1\) and obtains
\[
2+\frac12(1+z_1)(1+1)=3+z_1.
\]
At the final level, however,
\[
D_{P_1}(3)=0,\qquad D_{P_2}(3)=4.                          \tag{26}
\]
Thus the same scalar prefix masses admit different endpoint extensions.
The missing state is contained in the logical-block matrices
\(\mathcal E_R^{(m)}\), not in their traces.

## 4. The irreducible one-step symmetric/exterior recursion

The matrix state in Section 3 can be made more explicit.  Peel one
physical factor and write
\[
U:K\longrightarrow V\otimes W.
\]
On two replicas,
\[
\operatorname{Sym}^2(V\otimes W)
=
(\operatorname{Sym}^2V\otimes\operatorname{Sym}^2W)
\oplus
(\Lambda^2V\otimes\Lambda^2W),                             \tag{27}
\]
\[
\Lambda^2(V\otimes W)
=
(\operatorname{Sym}^2V\otimes\Lambda^2W)
\oplus
(\Lambda^2V\otimes\operatorname{Sym}^2W).                  \tag{28}
\]
Let the four components of \(U\otimes U\) in (27)--(28) be
\[
\begin{aligned}
\mathsf A &: \operatorname{Sym}^2K
 \longrightarrow\operatorname{Sym}^2V\otimes\operatorname{Sym}^2W,\\
\mathsf B &: \operatorname{Sym}^2K
 \longrightarrow\Lambda^2V\otimes\Lambda^2W,\\
\mathsf C &: \Lambda^2K
 \longrightarrow\operatorname{Sym}^2V\otimes\Lambda^2W,\\
\mathsf D &: \Lambda^2K
 \longrightarrow\Lambda^2V\otimes\operatorname{Sym}^2W.
\end{aligned}                                              \tag{29}
\]
Orthogonality of the two summands and the isometry property give
\[
\boxed{\quad
\mathsf A^\dagger\mathsf A+\mathsf B^\dagger\mathsf B
=I_{\operatorname{Sym}^2K},\qquad
\mathsf C^\dagger\mathsf C+\mathsf D^\dagger\mathsf D
=I_{\Lambda^2K}.
\quad}                                                     \tag{30}
\]
These identities are not the full constraint: all four maps in (29)
come from the same tensor square \(U\otimes U\), so they retain the
quadratic decomposability/Plücker relations of that common isometry.

Define the residual positive operators
\[
\begin{aligned}
R_A&=\operatorname{Tr}_{\operatorname{Sym}^2V}
     (\mathsf A\mathsf A^\dagger),&
R_B&=\operatorname{Tr}_{\Lambda^2V}
     (\mathsf B\mathsf B^\dagger),\\
R_C&=\operatorname{Tr}_{\operatorname{Sym}^2V}
     (\mathsf C\mathsf C^\dagger),&
R_D&=\operatorname{Tr}_{\Lambda^2V}
     (\mathsf D\mathsf D^\dagger).
\end{aligned}                                              \tag{31}
\]
Let a future positive weight on \(W\otimes W\), commuting with its swap,
be
\[
Z=Z_+\oplus Z_-\succeq0
\]
on \(\operatorname{Sym}^2W\oplus\Lambda^2W\).  Give the peeled local
antisymmetric sector weight \(t\geq0\), so its positive local operator is
\(S_V+tA_V\).  Taking the logical signed trace after the compression gives
the exact recursion
\[
\boxed{\quad
\operatorname{Tr}\!\left[
F_K(U^\dagger\otimes U^\dagger)
\bigl((S_V+tA_V)\otimes Z\bigr)
(U\otimes U)\right]
=\operatorname{Tr}[Z_+(R_A-tR_D)]
 +\operatorname{Tr}[Z_-(tR_B-R_C)].
\quad}                                                     \tag{32}
\]
For the Werner endpoint, \(t=3\).

Formula (32) isolates what a valid induction must preserve.  It is not
enough to prove the two residual brackets positive separately; both such
claims are false.

For the first counterexample, take \(V=W=\mathbb C^2\) and
\[
U|0\rangle=|0\rangle_V|0\rangle_W,\qquad
U|1\rangle=|1\rangle_V|1\rangle_W.                         \tag{33}
\]
Writing
\[
|s\rangle=\frac{|01\rangle+|10\rangle}{\sqrt2},\qquad
|a\rangle=\frac{|01\rangle-|10\rangle}{\sqrt2}
\]
in either two-replica factor, direct expansion gives
\[
\begin{aligned}
R_A&=|00\rangle\langle00|+|11\rangle\langle11|
     +\frac12|s\rangle\langle s|,\\
R_D&=\frac12|s\rangle\langle s|.
\end{aligned}
\]
Therefore
\[
R_A-3R_D
=|00\rangle\langle00|+|11\rangle\langle11|
-|s\rangle\langle s|                                      \tag{34}
\]
is indefinite.

For the second counterexample, take
\[
U|0\rangle=|0\rangle_V|0\rangle_W,\qquad
U|1\rangle=|0\rangle_V|1\rangle_W.                         \tag{35}
\]
The local two-replica state is always symmetric.  Hence
\(\mathsf B=\mathsf D=0\), while the logical exterior vector is sent by
\(\mathsf C\) to the residual exterior vector.  Thus
\[
3R_B-R_C=-|a\rangle\langle a|                              \tag{36}
\]
on \(\Lambda^2W\).

Equations (34) and (36) do not disprove (1), because an actual future
weight \(Z\) remains coupled to the same isometry.  They do prove that a
termwise residual-PSD induction discards an essential common-isometry
constraint.

## 5. A mixed active-set hierarchy

There is a natural hierarchy between the normalization at no active sites
and the target at all active sites.  For \(M\subseteq[n]\), define
\[
C_M:=
\operatorname{Tr}\!\left[
(P\otimes P)
\prod_{i\in M}(2F_i-I)
\prod_{i\notin M}F_i
\right].                                                   \tag{37}
\]
Expanding the active factors gives the exact marginal-purity formula
\[
\boxed{\quad
C_M
=2^{|M|}\sum_{T\subseteq M}
\left(-\frac12\right)^{|T|}
\|\operatorname{Tr}_TP\|_2^2.
\quad}                                                     \tag{38}
\]
In sector variables,
\[
\boxed{\quad
C_M
=\sum_{R\subseteq[n]}
(-3)^{|R\cap M|}(-1)^{|R\setminus M|}r_R.
\quad}                                                     \tag{39}
\]
In particular,
\[
C_\varnothing=2,\qquad C_{[n]}=D(3)=2^nQ_n(P).             \tag{40}
\]

There is also a positive-compression interpretation.  Since
\[
2F_i-I=F_i(S_i+3A_i),
\]
put
\[
\mathcal K_M=(U^\dagger\otimes U^\dagger)
\prod_{i\in M}(S_i+3A_i)
(U\otimes U)\succeq0.
\]
Then
\[
C_M=\operatorname{Tr}(F_K\mathcal K_M).                   \tag{41}
\]
Thus the candidate assertion \(C_M\geq0\) for every \(M\) is a
matrix-valued prefix cone of exactly the same signed-trace type as the
endpoint.  It is not established here.

### 5.1 A proved first-level inequality

For a singleton \(M=\{i\}\), (37) gives
\[
C_{\{i\}}
=2\operatorname{Tr}[(P\otimes P)F_{[n]}]
 -\operatorname{Tr}[(P\otimes P)F_{[n]\setminus\{i\}}].
\]
The first trace is \(\operatorname{Tr}P^2=2\), and the swap contraction
identifies the second with \(\|\operatorname{Tr}_iP\|_2^2\).  Hence
\[
C_{\{i\}}=4-\|\operatorname{Tr}_iP\|_2^2.                  \tag{42}
\]
The operator \(\operatorname{Tr}_iP\) is positive and has trace \(2\).
For nonnegative eigenvalues of fixed sum \(2\), the sum of squares is at
most \(4\).  Therefore
\[
\boxed{\quad C_{\{i\}}\geq0\quad\text{for every }i.\quad}   \tag{43}
\]

Equation (39) turns (43) into the coordinatewise sector inequality
\[
\sum_R(-1)^{|R|}
\bigl(1+2\,\mathbf1_{\{i\in R\}}\bigr)r_R\geq0.             \tag{44}
\]
Averaging (44) over \(i\) gives the exact layer inequality
\[
\boxed{\quad
\sum_{k\ {\rm even}}\left(1+\frac{2k}{n}\right)e_k
\ \geq\
\sum_{k\ {\rm odd}}\left(1+\frac{2k}{n}\right)o_k.
\quad}                                                     \tag{45}
\]
This is a genuine cumulative constraint beyond positivity and (3), but
its weights grow only linearly in \(k\), rather than as \(3^k\).

More generally, averaging (39) over all \(M\) of cardinality \(m\) gives
\[
\overline C_m
=\sum_{k=0}^n(-1)^kH_m(k)a_k,                              \tag{46}
\]
where \(a_k=e_k\) for even \(k\), \(a_k=o_k\) for odd \(k\), and
\[
H_m(k)=\frac1{\binom nm}
\sum_\ell
\binom k\ell\binom{n-k}{m-\ell}3^\ell.                    \tag{47}
\]
This is the exact hypergeometric/Krawtchouk-type prefix hierarchy.  At
\(m=1\), it reduces to (45); at \(m=n\), it is the desired endpoint
weight \(H_n(k)=3^k\).  Positivity of the intervening levels is not proved.

### 5.2 Scalar activation is not closed

For \(i\notin M\), replacing the inactive \(F_i\) by \(2F_i-I\) yields
\[
\boxed{\quad
C_{M\cup\{i\}}=2C_M-J_{M,i},
\quad}                                                     \tag{48}
\]
where
\[
J_{M,i}:=
\operatorname{Tr}\!\left[
(P\otimes P)
\prod_{j\in M}(2F_j-I)
\,I_i\!
\prod_{j\notin M\cup\{i\}}F_j
\right].                                                   \tag{49}
\]
The companion \(J_{M,i}\) is not determined by \(C_M\), and the signed
active factors prevent treating it as a free positive scalar.

The product family gives an exact nonclosure example.  From (11) and
(39),
\[
C_M=
\begin{cases}
2,&H_0\not\subseteq M,\\
2+2(-1)^h,&H_0\subseteq M.
\end{cases}                                                \tag{50}
\]
On two sites, compare
\[
\widetilde P_1=\operatorname{span}\{|00\rangle,|01\rangle\}
\quad(H_0=\{2\})
\]
with
\[
\widetilde P_2=\operatorname{span}\{|00\rangle,|11\rangle\}
\quad(H_0=\{1,2\}).
\]
For \(M=\{1\}\), both have \(C_M=2\).  Activating site \(2\) gives
\[
C_{[2]}(\widetilde P_1)=0,\qquad
C_{[2]}(\widetilde P_2)=4.                                 \tag{51}
\]
Thus even the single cumulative scalar \(C_M\) has no deterministic
one-step transition.

If \(H_0=[n]\) and \(n\) is odd, (50) says
\[
C_M=2\quad(M\subsetneq[n]),\qquad C_{[n]}=0.               \tag{52}
\]
Consequently no inequality of the form
\[
C_{[n]}\geq\sum_{M\subsetneq[n]}c_MC_M,\qquad c_M\geq0,    \tag{53}
\]
can be valid with any nonzero coefficient \(c_M\).  Proper active-set
positivity cannot be converted to the endpoint by a positive linear
lower-bound combination.

## 6. A distinct Bernstein-prefix hierarchy

It is important not to confuse \(C_M\) with the vertex values obtained by
turning unmeasured sector variables off.  Define
\[
B_M:=\mathcal F(3\mathbf1_M)
=\sum_{R\subseteq M}(-3)^{|R|}r_R.                         \tag{54}
\]
Multiaffinity gives
\[
D(3x)
=\sum_{M\subseteq[n]}x^{|M|}(1-x)^{n-|M|}B_M.             \tag{55}
\]
Equivalently, the degree-\(n\) Bernstein coefficient at level \(m\) is
the average of \(B_M\) over \(|M|=m\).

For the product code with \(H_0=[n]\), (11) gives
\[
B_M=2+2^{1-n}(-2)^{|M|}.                                  \tag{56}
\]
If \(n\) is odd, then
\[
B_M>0\quad(M\subsetneq[n]),\qquad B_{[n]}=0.               \tag{57}
\]
Thus no positive combination of proper Bernstein vertices can lower-bound
the terminal vertex nontrivially, either.

The two hierarchies are related, but not equal.  In (4), \(B_M\) sets
\(t_i=3\) on \(M\) and \(t_i=0\) outside \(M\), whereas \(C_M\) sets
\(t_i=3\) on \(M\) and \(t_i=1\) outside \(M\).  Interpolating the inactive
coordinates between \(0\) and \(3\) gives the exact positive averaging
identity
\[
\boxed{\quad
C_M=
\sum_{N\subseteq[n]\setminus M}
\left(\frac13\right)^{|N|}
\left(\frac23\right)^{n-|M|-|N|}
B_{M\cup N}.
\quad}                                                     \tag{58}
\]
This makes the obstruction in (52) and (57) especially transparent:
positive proper-prefix averages can converge to a zero terminal boundary
without forcing that boundary to be positive by induction.

## 7. Exact spectral obstruction

One might retain the full final positive compression
\[
\mathcal K
:=\sum_{R\subseteq[n]}3^{|R|}\mathcal E_R^{(n)}
=(U^\dagger\otimes U^\dagger)
\prod_i(S_i+3A_i)
(U\otimes U)\succeq0.                                     \tag{59}
\]
It splits as
\[
\mathcal K=\mathcal K_+\oplus k_-
\]
on the three-dimensional logical symmetric sector and the
one-dimensional logical exterior sector, and
\[
D(3)=\operatorname{Tr}\mathcal K_+-k_-.                   \tag{60}
\]
The product equality family shows that several tempting spectral
strengthenings of (60) are false.

For the code in Section 2.1, the two self vectors in
\(\operatorname{Sym}^2K\) have weight \(1\).  The normalized symmetric
cross vector occupies each even pattern in \(H_0\) with probability
\(2^{1-h}\), while the exterior vector occupies each odd pattern with the
same probability.  At any differing site, the self-pair vectors are
orthogonal to both cross orientations, so these three logical symmetric
vectors are also an eigenbasis of \(\mathcal K_+\).  Therefore
\[
\lambda_{\rm cross,+}
=2^{1-h}\sum_{k\ {\rm even}}\binom hk3^k
=2^h+(-1)^h,                                               \tag{61}
\]
\[
k_-
=2^{1-h}\sum_{k\ {\rm odd}}\binom hk3^k
=2^h-(-1)^h.                                               \tag{62}
\]
Hence the exact spectra are
\[
\boxed{\quad
\operatorname{spec}(\mathcal K_+)
=\bigl(1,1,2^h+(-1)^h\bigr),\qquad
k_-=2^h-(-1)^h.
\quad}                                                     \tag{63}
\]

For odd \(h\), the trace inequality is saturated:
\[
1+1+(2^h-1)=2^h+1.
\]
But for \(h=3\),
\[
\operatorname{spec}(\mathcal K_+)=(1,1,7),\qquad k_-=9.   \tag{64}
\]
Thus all of the following stronger sufficient conditions fail exactly:

\[
\mathcal K_+\succeq \frac{k_-}{3}I_3,\qquad
\lambda_{\min}(\mathcal K_+)\geq\frac{k_-}{3},\qquad
\det\mathcal K_+\geq\left(\frac{k_-}{3}\right)^3,
\]
because \(1<3\) and \(7<27\).  The wedge weight is controlled only after
adding the two unit self-vector contributions to the symmetric cross
weight.  An induction which tries to dominate the exterior block in every
symmetric direction is therefore strictly too strong.

## 8. What remains viable

The exact scalar facts obtained here are:

- the endpoint is the Abel-weighted tail sum (9);
- the tail dominance (10), adjacent-tail repair, and every fixed bounded
  Abel window fail on exact product codes;
- the singleton active-set inequalities (43)--(45) hold;
- the general averaged active-set coefficients are given by (46)--(47);
- scalar prefix masses and the scalar \(C_M\) are not closed recursion
  states.

The smallest recursion state not ruled out by these examples is
matrix-valued.  It must retain either:

1. all logical symmetric/exterior blocks
   \(\mathcal E_R^{(m)}\) in the prefix tree; or
2. the four residual operators in (31), together with the fact that their
   parent maps \(\mathsf A,\mathsf B,\mathsf C,\mathsf D\) arise from one
   common tensor-square isometry.

The second formulation is more economical, but identities (30) alone are
not sufficient: the exact counterexamples (34) and (36) show that the
missing common-isometry/Plücker relation must enter any successful cone.

No uniform sign theorem for \(D(3)\), and hence no all-copy conclusion,
is claimed in this note.
