# Rank-two planes in qutrit graph-orbit codes

## Research log

- **2026-07-28 13:14 PDT.** Began from the two discovery programs
  `search_qutrit_graph_codes.cpp` and
  `search_graph_code_two_planes.cpp`.  Replaced the continuous
  optimization over a logical qutrit by an exact logical Weyl
  diagonalization.
- **2026-07-28 13:24 PDT.** Proved that every linear objective in the local
  swap-sector masses is minimized, inside a fixed three-dimensional graph
  orbit code, by the complement of a logical Weyl eigenstate.  Thus four
  logical stabilizer planes are the complete set of candidates; random
  optimization over \(\mathbb {CP}^2\) is unnecessary.
- **2026-07-28 13:30 PDT.** Exhaustively evaluated all
  \(3^6(3^4-1)=58\,320\) four-qutrit graph/syndrome pairs with exact
  integer arithmetic.  Every rank-two plane is endpoint-nonnegative.
  The possible minima form a ten-element rational set.
- **2026-07-28 13:35 PDT.** Repeated the exact support-count test for the
  proposed hierarchy
  \[
  H_j=\sum_{\ell\geq j}\binom{2\ell}{2j}e_{2\ell}
       -3o_{2j+1}.
  \]
  It holds for all three- and four-qutrit graph codes.  Exact random
  support-count tests found no violation through \(n=9\), but this is not
  an all-\(n\) proof.
- **2026-07-28 13:41 PDT.** Replayed the minimal verifier in Section 8
  verbatim.  It checked all \(58\,320\) endpoint inputs and all
  \(233\,280\) four-copy hierarchy line tests and reproduced the stated
  integer histogram.

The main theorem in this note completely resolves the continuous
rank-two-plane optimization for every \(n\).  It also proves the whole
four-copy graph-orbit class nonnegative.  No negative endpoint projection
was found.  The remaining general-\(n\) question is reduced to one signed
weight-enumerator inequality for codimension-one isotropic subspaces.

## 1. Graph states and the endpoint superoperator

All vector arithmetic in this note is over \(\mathbb F_3\).  Let
\(\omega=e^{2\pi i/3}\), and on one qutrit let
\[
X|x\rangle=|x+1\rangle,\qquad Z|x\rangle=\omega^x|x\rangle.
\tag{1}
\]
For a symmetric zero-diagonal matrix \(A\in M_n(\mathbb F_3)\), choose
phases in the Pauli operators
\[
S_t\doteq X^tZ^{At},\qquad t\in\mathbb F_3^n,
\tag{2}
\]
so that they form an abelian group.  The symbol \(\doteq\) suppresses a
phase, which never affects a support count.  The graph state is the unique
common \(+1\) eigenvector, and
\[
|G_A\rangle\langle G_A|
=3^{-n}\sum_{t\in\mathbb F_3^n}S_t.
\tag{3}
\]

Fix \(s\in\mathbb F_3^n\setminus\{0\}\), and define the three graph-orbit
states
\[
|k\rangle_L=Z^{ks}|G_A\rangle,\qquad k\in\mathbb F_3.
\tag{4}
\]
They are orthonormal.  Indeed, a graph stabilizer with zero \(X\)-label
has \(t=0\), hence also zero \(Z\)-label.  Therefore no nonidentity
\(Z^{rs}\), \(r\neq0\), belongs to the stabilizer, and its graph-state
expectation is zero by (3).

Let
\[
U:\mathbb C^3\longrightarrow(\mathbb C^3)^{\otimes n}
\tag{5}
\]
be the isometry defined by (4).  Every rank-two projection in this
three-dimensional code is
\[
P_z=U(I_3-|z\rangle\langle z|)U^\dagger,\qquad \|z\|=1.
\tag{6}
\]

On one local matrix space define
\[
\mathcal L(C)=C-\frac12\operatorname{Tr}(C)I_3.
\tag{7}
\]
For operators on \(n\) qutrits,
\[
Q_n(C)=\langle C,\mathcal L^{\otimes n}(C)\rangle_{\rm HS}.
\tag{8}
\]
A local Pauli has eigenvalue \(-1/2\) under \(\mathcal L\) if it is the
identity and eigenvalue \(1\) otherwise.  Hence a tensor Pauli of support
weight \(w\) has eigenvalue
\[
\left(-\frac12\right)^{n-w}.
\tag{9}
\]

## 2. Exact logical Weyl diagonalization

Let \(X_L,Z_L\) be the logical qutrit Weyl operators in the basis (4), and
write
\[
W_{a,b}=X_L^aZ_L^b,\qquad (a,b)\in\mathbb F_3^2.
\tag{10}
\]
Define the compressed logical endpoint map
\[
\mathcal K(C)=
U^\dagger\mathcal L^{\otimes n}(UCU^\dagger)U.
\tag{11}
\]

For \(a,b\in\mathbb F_3\) and \(t\in\mathbb F_3^n\), put
\[
w_a(t)=
\left|\left\{i:
 \bigl(t_i,(At)_i+a s_i\bigr)\neq(0,0)\right\}\right|.
\tag{12}
\]
Thus \(w_a(t)\) is the support size of \(S_tZ^{as}\).  Introduce the exact
integer
\[
\boxed{\qquad
K_{a,b}(A,s)=
\sum_{\substack{t\in\mathbb F_3^n\\s\cdot t=-b}}
(-1)^{n-w_a(t)}2^{w_a(t)}.
\qquad}
\tag{13}
\]

### Theorem 2.1 (logical Weyl eigenvalues)

The nine logical Weyls diagonalize \(\mathcal K\):
\[
\mathcal K(W_{a,b})=\kappa_{a,b}W_{a,b},
\tag{14}
\]
where
\[
\boxed{\qquad
\kappa_{a,b}
=3^{1-n}\sum_{\substack{t\\s\cdot t=-b}}
\left(-\frac12\right)^{n-w_a(t)}
=3^{1-n}2^{-n}K_{a,b}.
\qquad}
\tag{15}
\]
Moreover,
\[
\kappa_{a,b}=\kappa_{-a,-b}.
\tag{16}
\]

#### Proof

Expand a logical Weyl in logical matrix units:
\[
W_{a,b}=\sum_{k\in\mathbb F_3}\omega^{bk}|k+a\rangle_L\langle k|.
\tag{17}
\]
Using (3), commuting \(Z^{(k+a)s}\) through \(S_t\), and summing over
\(k\), character orthogonality gives, up to one common phase,
\[
UW_{a,b}U^\dagger
=\frac3{3^n}
\sum_{\substack{t\in\mathbb F_3^n\\s\cdot t=-b}}
S_tZ^{as}.
\tag{18}
\]
There are \(3^{n-1}\) summands.  Their physical Pauli labels are
\[
\bigl(t,At+as\bigr).
\tag{19}
\]
The sets in (19) are disjoint for distinct logical labels \((a,b)\):
equality of the \(X\)-labels gives the same \(t\); equality of the
\(Z\)-labels then gives \((a-a')s=0\), hence \(a=a'\), and the hyperplane
condition gives \(b=b'\).

Physical Paulis are Hilbert--Schmidt orthogonal, with squared norm
\(3^n\).  Equations (9) and (18) therefore give
\[
\begin{aligned}
Q_n(UW_{a,b}U^\dagger)
&=\left(\frac3{3^n}\right)^2 3^n
  \sum_{s\cdot t=-b}
  \left(-\frac12\right)^{n-w_a(t)}\\
&=\frac9{3^n}
  \sum_{s\cdot t=-b}
  \left(-\frac12\right)^{n-w_a(t)}.
\end{aligned}
\tag{20}
\]
Since \(\|W_{a,b}\|_2^2=3\), division by \(3\) proves (15).  Disjointness
of the physical Pauli sets proves that the compressed map has no
off-diagonal logical Weyl matrix elements, proving (14).  Finally,
adjunction sends \((a,b)\) to \((-a,-b)\) and preserves (8), proving
(16). \(\square\)

Formula (13) is the promised exact stabilizer support-count reduction.
If
\[
N_{a,b}(w)=
\#\{t:s\cdot t=-b,\ w_a(t)=w\},
\tag{21}
\]
then simply
\[
K_{a,b}=\sum_{w=0}^nN_{a,b}(w)(-1)^{n-w}2^w.
\tag{22}
\]

## 3. The continuous plane optimization has four vertices

The eight nonzero elements of \(\mathbb F_3^2\) form four inverse pairs,
or projective lines.  Use representatives
\[
\mathscr R=\{(1,0),(0,1),(1,1),(1,2)\}.
\tag{23}
\]
For \(r\in\mathscr R\), write \(\kappa_r=\kappa_{-r}\) and
\[
x_r(z)=|\langle z,W_rz\rangle|^2.
\tag{24}
\]

### Lemma 3.1 (the Weyl-intensity simplex)

For every unit \(z\in\mathbb C^3\),
\[
x_r(z)\geq0,\qquad
\sum_{r\in\mathscr R}x_r(z)=1.
\tag{25}
\]
Every vertex of this simplex is attained: if \(z\) is an eigenvector of
\(W_{r_0}\), then
\[
x_{r_0}(z)=1,\qquad x_r(z)=0\quad(r\neq r_0).
\tag{26}
\]

#### Proof

The nine logical Weyls are an orthogonal basis of \(M_3\), with squared
norm \(3\).  Parseval applied to
\(\pi_z=|z\rangle\langle z|\) gives
\[
1=\operatorname{Tr}\pi_z^2
=\frac13\sum_{a,b}
|\langle z,W_{a,b}z\rangle|^2.
\tag{27}
\]
The identity term is \(1\), and inverse Weyls have equal expectation
moduli.  This proves (25).

If \(z\) is an eigenvector of \(W_{r_0}\), its expectation against the
inverse Weyl also has modulus one.  A Weyl from another projective line
does not commute with \(W_{r_0}\).  Commuting it through the eigenvalue
equation multiplies its expectation by \(\omega\) or \(\omega^2\), so
that expectation is zero.  This proves (26). \(\square\)

### Theorem 3.2 (exact optimization over every rank-two plane)

For the projection (6),
\[
\boxed{\qquad
Q_n(P_z)=
\frac43\kappa_{0,0}
+\frac23\sum_{r\in\mathscr R}\kappa_r x_r(z).
\qquad}
\tag{28}
\]
Consequently
\[
\boxed{\qquad
\min_{\|z\|=1}Q_n(P_z)
=\frac{4\kappa_{0,0}+2\min_{r\in\mathscr R}\kappa_r}{3}
=\frac{2K_{0,0}+\min_{r\in\mathscr R}K_r}
       {3^n2^{\,n-1}}.
\qquad}
\tag{29}
\]
Every minimum is attained by the complement of a logical Weyl
eigenstate.

#### Proof

Expand \(I-\pi_z\) in the logical Weyl basis.  Its identity coefficient
is \(2\), while for \((a,b)\neq(0,0)\) its coefficient is
\[
-\operatorname{Tr}(W_{a,b}^\dagger\pi_z).
\tag{30}
\]
Orthogonality and Theorem 2.1 give
\[
Q_n(P_z)=
\frac13\left[
4\kappa_{0,0}+
\sum_{(a,b)\neq(0,0)}
\kappa_{a,b}|\langle z,W_{a,b}z\rangle|^2\right],
\]
which is (28) after pairing inverses.  By (25), the second term is a
linear functional on a simplex, so it is bounded below by the smallest
\(\kappa_r\).  Equation (26) attains that bound.  Substitution of (15)
gives the last expression in (29). \(\square\)

This theorem explains why the floating-point search over arbitrary
\(z\) returned only zero up to roundoff.  More generally, the same
four-vertex reduction applies to **every objective linear in the swap
sector masses**, not just to \(Q_n\); Section 6 proves this extension.

For a fixed line \(r\), (29) also gives the convenient integral scaling
\[
\boxed{\qquad
\frac{6^n}{2}Q_n(P_r)=2K_{0,0}+K_r.
\qquad}
\tag{31}
\]
This is exactly the integer called `scaled_half_Q` in
`search_qutrit_graph_codes.cpp`.

## 4. Exact four-copy classification

There are \(3^6=729\) symmetric zero-diagonal \(4\times4\) matrices and
\(3^4-1=80\) nonzero syndromes.  Direct evaluation of (13), with no
floating-point operations, gives the following complete distribution.
The middle column is
\[
\Delta(A,s)=2K_{0,0}+
\min\{K_{1,0},K_{0,1},K_{1,1},K_{1,2}\}.
\tag{32}
\]

\[
\begin{array}{c|c|c}
\text{number of }(A,s)&\Delta(A,s)&
\min_z Q_4(P_z)=\Delta/648\\ \hline
408&0&0\\
232&162&1/4\\
2208&270&5/12\\
6624&324&1/2\\
13824&432&2/3\\
480&486&3/4\\
22416&594&11/12\\
1472&648&1\\
7200&774&43/36\\
3456&882&49/36
\end{array}
\tag{33}
\]
The counts sum to \(58\,320\).  Thus:

### Theorem 4.1

Every rank-two subprojection of every three-dimensional four-qutrit
graph-orbit code satisfies
\[
Q_4(P_z)\geq0.
\tag{34}
\]
Every connected four-vertex graph satisfies the stronger sharp bound
\[
Q_4(P_z)\geq\frac14.
\tag{35}
\]

The proof is the finite exact enumeration (13), independently replayed
by the verifier in Section 8.  It is a mathematical finite certificate
for this ansatz, not an inference about arbitrary codes or arbitrary
copy number.

The \(408\) equality pairs have the following exact \(K\)-tuples, in the
order
\[
(K_{0,0};K_{1,0},K_{0,1},K_{1,1},K_{1,2}).
\]
\[
\begin{array}{c|c}
\text{multiplicity}&K\text{-tuple}\\ \hline
8&(-27;54,54,54,54)\\
96&(-27;54,216,216,216)\\
32&(-27;216,54,216,216)\\
32&(-27;216,216,54,216)\\
32&(-27;216,216,216,54)\\
48&(-99;198,198,198,198)\\
160&(-135;270,270,270,270).
\end{array}
\tag{36}
\]
Every equality graph has an isolated vertex.  Thus the four-copy graph
ansatz has no connected extremizer and no genuinely new distillation
candidate at equality.

## 5. A uniform equality family and the general obstruction

The edgeless graph can be evaluated for arbitrary \(n\).  Let
\[
h=|\operatorname{supp}s|.
\tag{37}
\]
When \(A=0\), character orthogonality in the constraint \(s\cdot t=-b\)
gives
\[
\begin{aligned}
K_{0,0}
 &=3^{n-1}\bigl(1+2(-1)^h\bigr),\\
K_{0,b}
 &=3^{n-1}\bigl(1-(-1)^h\bigr),
 \qquad b=1,2,\\
K_{a,b}
 &=3^{n-1}2^h,\qquad a=1,2,\quad b=0,1,2.
\end{aligned}
\tag{38}
\]

For completeness, the first formula follows by inserting
\[
\mathbf1_{s\cdot t=-b}
=\frac13\sum_{c\in\mathbb F_3}\omega^{c(s\cdot t+b)}
\tag{39}
\]
in (13).  Outside \(\operatorname{supp}s\), the local sum is
\(-1+2+2=3\).  On its support, the local sum is \(3\) for \(c=0\) and
\(-3\) for \(c\neq0\).  If \(a\neq0\), the shifted \(Z\)-label makes
every supported site nonidentity and the nonzero Fourier modes vanish.
These observations give all three lines of (38).

Substitution in (29) yields
\[
\min_zQ_n(P_z)=
\begin{cases}
0,&h\ \text{odd},\\[1mm]
2^{2-n},&h\ \text{even}.
\end{cases}
\tag{40}
\]
This is the familiar product-string parity mechanism, now obtained
directly from the logical Weyl spectrum.

For general \(A,s,n\), the exact all-copy graph-code question is:
\[
\boxed{\qquad
2K_{0,0}(A,s)+K_r(A,s)\geq0
\quad\text{for all }r\in\mathscr R.
\qquad}
\tag{41}
\]
The sets in (13) are affine cosets of the codimension-one isotropic
subspace
\[
\mathcal C=
\{(t,At):s\cdot t=0\}\subset\mathbb F_3^{2n}.
\tag{42}
\]
Thus (41) is a signed support-enumerator inequality for one isotropic
subspace and its eight logical cosets.

The individual summands in (13) change sign with the number of identity
sites.  Neither positivity of the counts \(N_{a,b}(w)\) nor a termwise
comparison proves (41).  Exact random tests of \(100\,000,50\,000,
20\,000,5\,000,1\,000\) graph/syndrome pairs for
\(n=5,6,7,8,9\), respectively, found neither a negative \(K_r\) nor a
negative (41).  These tests used integer arithmetic but are discovery
data only.  No proof of (41) for arbitrary \(n\) is obtained here.

## 6. The full sector polynomial

The Weyl reduction applies to more than the single endpoint evaluation.
For a rank-two projection \(P\), define
\[
G_P(x)=
\sum_{R\subseteq[n]}p_Rx^{|R|}
=\operatorname{Tr}\left[
(P\otimes P)
\prod_{i=1}^n(S_i+xA_i)\right].
\tag{43}
\]
If a physical Pauli has support weight \(w\), its contribution to the
local contraction in (43) is
\[
3^n2^{-w}(2+x)^{n-w}(1-x)^w.
\tag{44}
\]
Indeed, at an identity site the contraction is
\[
\frac{1+x}{2}\,9+\frac{1-x}{2}\,3=3(2+x),
\]
whereas at a nonidentity site it is \(3(1-x)/2\).

Define the coset polynomials
\[
\Phi_{a,b}(x)=
\sum_{w=0}^nN_{a,b}(w)\,
2^{-w}(2+x)^{n-w}(1-x)^w.
\tag{45}
\]
The physical Pauli coefficient of the logical identity in \(P_z\) has
modulus \(2\).  The coefficient of a nonzero logical Weyl has squared
modulus \(x_r(z)\).  The Pauli cosets are disjoint, so
\[
\boxed{\qquad
G_{P_z}(x)=3^{-n}\left[
4\Phi_{0,0}(x)+
2\sum_{r\in\mathscr R}x_r(z)\Phi_r(x)\right].
\qquad}
\tag{46}
\]
Here \(\Phi_r=\Phi_{-r}\), which follows by adjunction.

Equation (46) proves the claim after Theorem 3.2: every linear functional
of the sector masses is affine in the four nonnegative numbers \(x_r\)
whose sum is one.  Its minimum over all rank-two planes is attained at a
logical Weyl eigenplane.

At \(x=-3\), (45) becomes (13), and
\[
2^{-n}G_P(-3)=Q_n(P).
\tag{47}
\]
Thus the sector-polynomial formula independently recovers Theorem 3.2.

## 7. The proposed binomial sector hierarchy

Write
\[
e_k=\sum_{|R|=k}p_R\quad(k\ {\rm even}),\qquad
o_k=\sum_{|R|=k}p_R\quad(k\ {\rm odd}).
\tag{48}
\]
The proposed inequalities are
\[
\boxed{\qquad
H_j(P)=
\sum_{\ell\geq j}\binom{2\ell}{2j}e_{2\ell}
-3o_{2j+1}\geq0,
\qquad
1\leq j\leq\frac{n-1}{2}.
\qquad}
\tag{49}
\]

There is a direct sector interpretation.  For a fixed
\(J\subseteq[n]\), \(|J|=2j\),
\[
\sum_{\substack{R\supseteq J\\|R|\ {\rm even}}}\Pi_R
=
\left(\prod_{i\in J}A_i\right)
\frac{I+F_{J^c}}2.
\tag{50}
\]
Summing (50) over \(J\) counts an even sector \(R\) exactly
\(\binom{|R|}{2j}\) times.  Therefore
\[
\begin{aligned}
H_j(P)
={}&
\sum_{\substack{J\subseteq[n]\\|J|=2j}}
\operatorname{Tr}\left[
(P\otimes P)
\left(\prod_{i\in J}A_i\right)
\frac{I+F_{J^c}}2\right]\\
&-3\sum_{|R|=2j+1}p_R.
\end{aligned}
\tag{51}
\]
This explains the binomial coefficient, but does not sign the difference.

For an exact stabilizer-count form, put
\[
R_{n,w}(x)=
2^{n-w}(2+x)^{n-w}(1-x)^w
=\sum_{k=0}^nr_{n,w,k}x^k
\tag{52}
\]
and
\[
h_{j,n}(w)=
\sum_{\ell\geq j}\binom{2\ell}{2j}r_{n,w,2\ell}
-3r_{n,w,2j+1}.
\tag{53}
\]
For the logical Weyl eigenplane associated with \(r\in\mathscr R\),
equations (45)--(46) give the integer identity
\[
\boxed{\qquad
3^n2^nH_j(P_r)=
4\sum_wN_{0,0}(w)h_{j,n}(w)
+2\sum_wN_r(w)h_{j,n}(w).
\qquad}
\tag{54}
\]
This is the requested stabilizer support-count interpretation.

The kernel in (54) is not pointwise positive.  For example,
\[
\bigl(h_{1,4}(0),\ldots,h_{1,4}(4)\bigr)
=(96,24,-12,-12,24).
\tag{55}
\]
Thus a proof must use relations between the support counts of the
isotropic subspace and its logical cosets; it cannot simply discard their
locations.

Exact exhaustive results are:

- for \(n=3\), all \(27\cdot26\cdot4=2\,808\) graph/syndrome/line
  triples satisfy \(H_1\geq0\);
- for \(n=4\), all \(729\cdot80\cdot4=233\,280\) triples satisfy
  \[
  H_1=e_2+6e_4-3o_3\geq0.
  \tag{56}
  \]

For \(n=5,\ldots,9\), the exact random support-count tests described in
Section 5 checked every admissible \(j\) and all four logical lines for
each sampled graph.  The numbers of tested scalar inequalities were
\[
\begin{array}{c|ccccc}
n&5&6&7&8&9\\ \hline
\text{graph/syndrome samples}
&100000&50000&20000&5000&1000\\
\text{individual }H_j\text{ tests}
&800000&400000&240000&60000&16000\\
\text{negative tests}&0&0&0&0&0.
\end{array}
\tag{57}
\]
Again, (57) is conjecture-generation data, not an all-copy proof.

The edgeless graph gives an exact all-\(n\) check.  For the product plane
whose two strings differ in \(h\) positions,
\[
e_k=o_k=2^{1-h}\binom hk\quad(k\geq1),
\tag{58}
\]
with the symbol chosen according to the parity of \(k\).  If
\(h\geq2j+1\), then
\[
\begin{aligned}
2^{h-1}H_j
&=\sum_{\ell\geq j}\binom{2\ell}{2j}\binom h{2\ell}
 -3\binom h{2j+1}\\
&=\binom h{2j}
\left(2^{h-2j-1}-\frac{3(h-2j)}{2j+1}\right)\geq0.
\end{aligned}
\tag{59}
\]
The last inequality follows from
\[
2^{m-1}\geq m\geq\frac{3m}{2j+1},
\qquad m=h-2j\geq1,\quad j\geq1.
\]
The cases \(h\leq2j\) follow directly from (58).  Thus (49) is exact on
the entire product graph family, including its endpoint equality codes.

## 8. Minimal exact four-copy verifier

The following standalone program uses only Python integers.  It evaluates
(13), verifies the histogram (33), checks the four-copy hierarchy (56)
for all four logical lines, and checks that every endpoint equality graph
has an isolated vertex.

```python
from collections import Counter
from itertools import product
from math import comb

n = 4
vec = list(product(range(3), repeat=n))
lines = ((1, 0), (0, 1), (1, 1), (1, 2))

def adjacency(code):
    A = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            A[i][j] = A[j][i] = code % 3
            code //= 3
    return A

def data(A, s):
    N = [[Counter() for _ in range(3)] for _ in range(3)]
    for t in vec:
        b = -sum(x*y for x, y in zip(s, t)) % 3
        At = [sum(A[i][j]*t[j] for j in range(n)) % 3
              for i in range(n)]
        for a in range(3):
            w = sum(t[i] != 0 or (At[i]+a*s[i]) % 3 != 0
                    for i in range(n))
            N[a][b][w] += 1
    return N

def K(N, a, b):
    return sum(c*(-1)**(n-w)*2**w
               for w, c in N[a][b].items())

R = []
for w in range(n+1):
    p = [0]*(n+1)
    for a in range(n-w+1):
        for b in range(w+1):
            p[a+b] += (2**(n-w) * comb(n-w, a) *
                       2**(n-w-a) * comb(w, b) * (-1)**b)
    R.append(p)

endpoint = Counter()
for graph in range(3**6):
    A = adjacency(graph)
    for s in vec[1:]:
        N = data(A, s)
        k0 = K(N, 0, 0)
        kr = [K(N, a, b) for a, b in lines]
        delta = 2*k0 + min(kr)
        endpoint[delta] += 1

        if delta == 0:
            assert any(all(A[i][j] == 0 for j in range(n))
                       for i in range(n))

        for a, b in lines:
            E = []
            for degree in range(n+1):
                E.append(sum((4*N[0][0][w] + 2*N[a][b][w])
                             * R[w][degree]
                             for w in range(n+1)))
            assert E[2] + 6*E[4] - 3*E[3] >= 0

assert endpoint == Counter({
    0: 408, 162: 232, 270: 2208, 324: 6624,
    432: 13824, 486: 480, 594: 22416, 648: 1472,
    774: 7200, 882: 3456,
})
print("exact four-copy certificate passed")
```

The verifier enumerates all finite inputs in the claimed four-copy class
and performs no optimization or tolerance comparison.

## 9. What is and is not resolved

Proved here:

1. the exact logical Weyl spectrum (15) for every graph, syndrome, and
   copy number;
2. the exact analytic reduction of every rank-two plane to four logical
   Weyl eigenplanes, both for the endpoint and for arbitrary linear sector
   objectives;
3. nonnegativity of every four-copy rank-two graph-orbit subprojection,
   with all possible minimum values and equality tuples;
4. the exact support-count formula (54) for the proposed hierarchy and
   its validity for every graph code through \(n=4\);
5. all-\(n\) endpoint and hierarchy formulas for the edgeless/product
   family.

Not proved:

1. the signed isotropic-coset inequality (41) for arbitrary \(n\);
2. the hierarchy (49) for arbitrary graph codes or arbitrary rank-two
   codes;
3. any negative projection or distillation witness.

The useful obstruction is now precise.  Continuous nonstabilizer choices
of \(z\) cannot improve the graph-code search: their Weyl intensities are
convex weights on four exactly attainable vertices.  Any future graph-code
counterexample must therefore be an exact violation of the finite-field
support inequality (41).  Conversely, a general proof must exploit
isotropy or relations among logical cosets, because the individual
support-weight kernels in both (13) and (54) have mixed signs.
