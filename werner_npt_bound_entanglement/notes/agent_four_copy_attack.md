# Four-copy rank-two projection attack

## Research checkpoint

**2026-07-28 13:59 PDT.**  The four-copy projection problem is not
resolved in this note.  No exact negative projection was found.  The
main exact advance is a sharper candidate inequality
\[
e_2+6e_4\geq 3o_3,                                           \tag{1}
\]
which is stronger than what is needed for four-copy positivity and has
several useful equivalent forms.  The coefficient \(6\) is sharp.
Complex Grassmann searches in local dimensions two and three converge
to equality, but this is discovery evidence only.

The missing assertion can also be written as one very specific
monotonicity statement: the sum of six grouped strong three-copy
defects must dominate the sum of four Haar-conditioned strong
three-copy defects.  Neither separate nonnegativity nor the presently
known averaged conditioning inequalities prove that comparison.

Best present assessment of (1): plausible and numerically robust, but
**unproved**.  Nothing in this note establishes four-copy
undistillability, still less an all-copy theorem.

## 1. Swap sectors and the exact four-copy target

Let \(P\) be a rank-two orthogonal projection on
\[
H_1\otimes H_2\otimes H_3\otimes H_4,
\]
where the local dimensions are arbitrary.  On two replicas let \(F_i\)
swap the two copies of \(H_i\), and for \(R\subseteq[4]\) put
\[
\Pi_R=
\prod_{i\in R}\frac{I-F_i}{2}
\prod_{i\notin R}\frac{I+F_i}{2},
\qquad
p_R=\operatorname{Tr}\bigl[(P\otimes P)\Pi_R\bigr].          \tag{2}
\]
All \(p_R\) are nonnegative.  Since the global swap has symmetric and
antisymmetric multiplicities \(3\) and \(1\) on a two-dimensional code,
\[
\sum_{\lvert R\rvert\ {\rm even}}p_R=3,\qquad
\sum_{\lvert R\rvert\ {\rm odd}}p_R=1.                       \tag{3}
\]
Write
\[
e_2=\sum_{\lvert R\rvert=2}p_R,\qquad
o_3=\sum_{\lvert R\rvert=3}p_R,\qquad
e_4=p_{[4]}.
\]
The endpoint quadratic form is
\[
Q_4(P)=2^{-4}\sum_{R\subseteq[4]}(-3)^{\lvert R\rvert}p_R.
\]
Eliminating the weight-zero and weight-one masses with (3) gives the
exact identity
\[
\boxed{\quad Q_4(P)=\frac12\bigl(e_2-3o_3+10e_4\bigr).\quad}  \tag{4}
\]
Thus four-copy positivity is equivalent to
\[
e_2+10e_4\geq3o_3.                                           \tag{5}
\]

The stronger candidate isolated in this attack is
\[
\boxed{\quad H_1(P):=e_2+6e_4-3o_3\geq0.\quad}               \tag{6}
\]
If (6) holds, then
\[
Q_4(P)=\frac12H_1(P)+2e_4\geq2e_4\geq0.                      \tag{7}
\]

The coefficient \(6\) in (6) cannot be decreased.  For the repetition
code
\[
P=\lvert0000\rangle\langle0000\rvert+
  \lvert1111\rangle\langle1111\rvert
\]
one has
\[
p_\varnothing=\frac{17}{8},\qquad
p_R=\frac18\quad(R\ne\varnothing).
\]
Consequently
\[
e_2=\frac68,\qquad o_3=\frac48,\qquad e_4=\frac18,
\]
so \(H_1(P)=0\), while \(Q_4(P)=1/4\).

## 2. Partial-trace and purification forms

For \(T\subseteq[4]\), define
\[
A_T=\left\|\operatorname{Tr}_{\bar T}P\right\|_2^2
    =\operatorname{Tr}\bigl[(P\otimes P)F_T\bigr].           \tag{8}
\]
The Walsh transform between \(p_R\) and \(A_T\) gives
\[
\boxed{\quad
H_1(P)
=\frac14\sum_{\lvert T\rvert=2}A_T
-\frac34\sum_{\lvert T\rvert=3}A_T
+\frac32 A_{[4]}.
\quad}                                                       \tag{9}
\]
Since \(A_{[4]}=\operatorname{Tr}P^2=2\), this is
\[
H_1(P)
=\frac14\left(
\sum_{\lvert T\rvert=2}A_T
-3\sum_{\lvert T\rvert=3}A_T+12\right).                     \tag{10}
\]

Let \(\rho=P/2\), and purify it as a normalized pure vector
\[
\lvert\Psi\rangle\in K\otimes H_1\otimes H_2\otimes H_3\otimes H_4,
\qquad K\simeq\mathbb C^2,
\]
with \(\rho_K=I_2/2\).  Write
\[
s_S=\operatorname{Tr}\rho_S^2.
\]
Then \(A_T=4s_T\), and purity of complementary reductions gives
\(s_{ijk}=s_{K\ell}\).  Hence (10) becomes
\[
\boxed{\quad
H_1(P)=
\sum_{1\leq i<j\leq4}s_{ij}
-3\sum_{i=1}^4s_{Ki}+3.
\quad}                                                       \tag{11}
\]

A natural homogeneous strengthening, useful for proof search, is the
following assertion for an arbitrary normalized pure state on
\(K H_1H_2H_3H_4\):
\[
\boxed{\quad
6s_K+\sum_{i<j}s_{ij}-3\sum_i s_{Ki}\geq0.
\quad}                                                       \tag{12}
\]
When \(K\) is a maximally mixed qubit, (12) is exactly (11).  Direct
complex optimization over arbitrary pure states with
\(\dim K=2,3,4\) and qubit physical systems reached zero but did not
cross it.  This is not a proof, and (12) is recorded only as a stronger
discovery conjecture.

In linear-entropy notation \(L_S=1-s_S\), (12) reads
\[
3\sum_iL_{Ki}\geq\sum_{i<j}L_{ij}+6L_K.                      \tag{13}
\]
Equivalently, with
\[
I_2(A:B)=1-s_A-s_B+s_{AB}\geq0,
\]
it reads
\[
3\sum_i I_2(K:i)\leq
6L_K+\sum_{i<j}I_2(i:j).                                    \tag{14}
\]
This gives a useful interpretation: information about one reference
system replicated into four individual shares must be paid for either
by reference mixedness or by pairwise correlations among the shares.

## 3. Exact grouped-minus-conditioned identity

The strongest three-copy theorem proved in
`notes/agent_qutrit_frame.md` has the following pure-state form.  If
\(\lvert\phi\rangle\) is an arbitrary, possibly unnormalized, pure
state on a qubit \(K\) and three physical blocks \(X,Y,Z\), then
\[
g_3(\phi):=
3s_K+s_X+s_Y+s_Z
-2(s_{KX}+s_{KY}+s_{KZ})\geq0,                               \tag{15}
\]
where all \(s_S=\operatorname{Tr}\rho_S^2\) are homogeneous squared
Hilbert--Schmidt norms of the unnormalized reductions.

For a normalized pure state on \(K H_1H_2H_3H_4\), fix a physical pair
\(\{i,j\}\), and write its complementary pair as \(\{k,\ell\}\).
Applying (15) to the three blocks \(ij,k,\ell\) gives
\[
g_{ij}:=
3s_K+s_{ij}+s_k+s_\ell
-2(s_{k\ell}+s_{Kk}+s_{K\ell})\geq0.                         \tag{16}
\]
With
\[
S_1=\sum_i s_i,\qquad
S_2=\sum_{i<j}s_{ij},\qquad
S_K=\sum_i s_{Ki},
\]
summing (16) over the six pairs gives
\[
\boxed{\quad
G_{\rm grp}:=\sum_{i<j}g_{ij}
=18s_K+3S_1-S_2-6S_K\geq0.
\quad}                                                       \tag{17}
\]

There is a second exact application of (15).  Fix \(\ell\), let
\(d_\ell=\dim H_\ell\), choose a Haar-random unit vector
\(x\in H_\ell\), and set
\[
\lvert\psi_x\rangle
=(\langle x|_\ell\otimes I)\lvert\Psi\rangle.
\]
Apply (15) to the three remaining physical systems and define
\[
c_\ell=d_\ell(d_\ell+1)\int g_3(\psi_x)\,dx.                 \tag{18}
\]
The two-design identity
\[
\int |x\rangle\langle x|^{\otimes2}\,dx
=\frac{I+F_\ell}{d_\ell(d_\ell+1)}
\]
gives, by direct swap contraction,
\[
c_\ell=
3(s_K+s_{K\ell})
+\sum_{i\ne\ell}(s_i+s_{i\ell})
-2\sum_{i\ne\ell}(s_{Ki}+s_{Ki\ell})\geq0.                  \tag{19}
\]
Using purity equality for complementary reductions and summing over
\(\ell\) yields
\[
\boxed{\quad
G_{\rm cond}:=\sum_\ell c_\ell
=12s_K+3S_1-2S_2-3S_K\geq0.
\quad}                                                       \tag{20}
\]
Subtracting (20) from (17) gives the exact identity
\[
\boxed{\quad
G_{\rm grp}-G_{\rm cond}
=6s_K+S_2-3S_K.
\quad}                                                       \tag{21}
\]
Thus the homogeneous conjecture (12), and in particular (6), would
follow from the single monotonicity statement
\[
\boxed{\qquad
\sum_{i<j}g_{ij}\ \geq\ \sum_\ell c_\ell.
\qquad}                                                      \tag{22}
\]
Separate nonnegativity of all terms proves neither their comparison nor
(22).  Equation (21) identifies the exact missing step in an induction
from the strong three-copy theorem.

## 4. What the currently available three-copy consequences prove

The three-copy theorem applied after grouping a physical pair gives,
in sector notation,
\[
(e_2-p_{ij})+e_4
\geq 3\bigl(p_{i k\ell}+p_{j k\ell}\bigr),                  \tag{23}
\]
where \(\{k,\ell\}=[4]\setminus\{i,j\}\).  Summing all six instances
gives
\[
5e_2+6e_4\geq9o_3.                                          \tag{24}
\]

Conditioning on one physical system and applying the three-copy theorem
also gives, for every physical triple \(T\),
\[
\sum_{\substack{R\subset T\\|R|=2}}p_R\geq3p_T.              \tag{25}
\]
Summing the four inequalities gives
\[
2e_2\geq3o_3.                                                \tag{26}
\]
No nonnegative linear combination of (24) and (26) yields (6).
Indeed, solving
\[
a(5e_2+6e_4-9o_3)+b(2e_2-3o_3)
=e_2+6e_4-3o_3
\]
forces \(a=1\) and \(b=-2\).

For qutrit local systems, further exact averaged conditioning
inequalities found in the attack also point in the wrong direction for
(6).  If a site \(D\) is distinguished, write
\[
A=\sum_{\substack{|R|=2\\D\notin R}}p_R,\qquad
B=\sum_{\substack{|R|=3\\D\in R}}p_R,\qquad
C=p_{[4]\setminus\{D\}}.
\]
Conditioning the two codewords independently and averaging gives
\[
4A+3B\geq9C+3e_4,                                           \tag{27}
\]
while averaging over an orthogonal pair gives
\[
5A+6B\geq9C+6e_4.                                           \tag{28}
\]
A same-codeword orthogonal-pair average gives
\[
A\geq2e_4.                                                   \tag{29}
\]
Finally, averaging over a two-plane in the combined environment
\(K\otimes H_D\) gives
\[
5(A+B)\geq7(C+e_4).                                         \tag{30}
\]
All these are exact consequences of the three-copy theorem and
two-design contraction.  Their sums do not give (6).

## 5. A formal sector obstruction

The failure of the preceding linear route is not merely a bad choice
of coefficients.  The following nonnegative formal sector masses obey
the parity normalizations (3), all six grouped inequalities (23), all
four conditional inequalities (25), and the corresponding three-block
Pauli-shadow bounds:
\[
\begin{array}{c|c}
R&p_R\\ \hline
\varnothing&21/16\\
\{2\}&1/16\\
\{1,2\},\{2,3\},\{2,4\}&1/4\\
\{1,3\},\{1,4\},\{3,4\}&5/16\\
\{1,2,3\},\{1,2,4\},\{2,3,4\}&11/48\\
\{1,3,4\}&1/4
\end{array}                                                  \tag{31}
\]
with all omitted masses zero.  It has
\[
e_2=\frac{27}{16},\qquad
o_3=\frac{15}{16},\qquad e_4=0,
\]
and hence
\[
H_1=-\frac98,\qquad Q_4=-\frac9{16}.                         \tag{32}
\]
This is **not** claimed to be realizable by a code projection.  Its role
is precise: positivity of the sector masses plus the known grouped and
conditioned linear inequalities does not imply the desired result.
Any successful proof must use a nonlinear realizability constraint of
the two-dimensional code.

For reference, the encoded-Pauli shadow numbers
\[
L_S=\sum_{a=1}^3
\left\|\operatorname{Tr}_{\bar S}X_a\right\|_2^2
\]
for (31) are
\[
\begin{array}{c|c}
S&L_S\\ \hline
\varnothing&0\\
\{1\},\{3\},\{4\}&5/2\\
\{2\}&3\\
\{1,2\},\{2,3\},\{2,4\}&1\\
\{1,3\},\{1,4\},\{3,4\}&1/2\\
|S|=3&0\\
[4]&6.
\end{array}                                                  \tag{33}
\]
It violates the genuine four-block adaptive sign-frame bound on the
weight-one shadows, illustrating exactly where non-realizability first
appears.  Adding that single bound is still insufficient at the level
of linear programming.  For example, a second nonnegative formal model
is
\[
\begin{array}{c|c}
R&p_R\\ \hline
\varnothing&9/4\\
\{1\}&7/12\\
\{2,3\},\{2,4\},\{3,4\}&1/4\\
\{1,2,3\},\{1,2,4\},\{1,3,4\}&1/12\\
\{2,3,4\}&1/6
\end{array}                                                  \tag{33a}
\]
with omitted masses zero.  It obeys (3), (23), (25), and the sharp
four-block bound \(L_1\leq8\), but has
\[
H_1=\frac34-3\left(\frac5{12}\right)=-\frac12.
\]

## 6. Exact obstruction to naive defect tensorization

Let \(B_3(\cdot,\cdot)\) be the sesquilinear polarization of the
three-copy endpoint form, and define its strong defect
\[
D_3(C)=
B_3(C,C)-\frac18\left(2\|C\|_2^2-|\operatorname{Tr}C|^2\right).
\]
Slice a rank-two isometry along the fourth site.  If
\[
C_{rs}=V_rV_s^\dagger,\qquad
H=\sum_rC_{rr}=\operatorname{Tr}_4P,
\]
then
\[
Q_4(P)=
\sum_{r,s}B_3(C_{rs},C_{rs})-\frac12B_3(H,H).                \tag{34}
\]
Separating strong defects gives
\[
Q_4(P)=
\left(\sum_{r,s}D_3(C_{rs})-\frac12D_3(H)\right)
+\frac18(6-K_1-K_2),                                        \tag{35}
\]
where
\[
K_1=\sum_{r,s}|\operatorname{Tr}C_{rs}|^2,\qquad
K_2=\|H\|_2^2.
\]
The remainder is nonnegative because \(K_1+K_2\leq6\), the elementary
complementary-purity bound for a qubit reference.  The tempting claim
that the parenthesized defect in (35) is nonnegative is false.

Take
\[
P=P_{B,2}\otimes|\phi\rangle\langle\phi|_{ACD},              \tag{36}
\]
where \(P_{B,2}\) is a rank-two projection on one physical site and
\(\phi\) is an arbitrary pure state on the other three.  If
\[
a_R(\phi)=
\langle\phi\otimes\phi|\Pi_R|\phi\otimes\phi\rangle
\quad(R\subseteq\{A,C,D\}),
\]
then only even \(R\) occur and
\[
p_R=3a_R,\qquad p_{R\cup\{B\}}=a_R.                         \tag{37}
\]
For a distinguished site \(D\), direct substitution in (35) gives
\[
\sum_{r,s}D_3(C_{rs})-\frac12D_3(H)
=-\frac32(a_{AD}+a_{CD})
=-\frac34\bigl(1-\operatorname{Tr}\rho_D^2\bigr).           \tag{38}
\]
For the qutrit GHZ vector
\[
\phi=(|000\rangle+|111\rangle+|222\rangle)/\sqrt3,
\]
the defect is \(-1/2\), while the scalar remainder in (35) is \(+1/2\).
Thus the two parts cancel exactly.  An induction must retain this
coupling.

The same family disproves natural pairwise attempts.  For example,
\[
p_{ABC}+p_{ABD}
\leq p_{AB}+\frac53e_4                                      \tag{39}
\]
would sum to the desired global inequality, but if the \(A\)-marginal
of \(\phi\) in (36) is maximally mixed, then
\[
p_{AB}=e_4=0,\qquad
p_{ABC}+p_{ABD}
=\frac{1-\operatorname{Tr}\rho_A^2}{2}
=\frac13.                                                    \tag{40}
\]
The pair mass therefore has to be distributed globally; it cannot be
assigned independently to the two triples sharing that pair.

## 7. Exact positive subclasses and equality families

Several four-copy subclasses follow immediately from the strong
three-copy theorem.

### 7.1 A pure tensor factor

If
\[
P=P_{123}\otimes|\eta\rangle\langle\eta|_4
\]
with \(P_{123}\) a rank-two projection, the fourth local replica pair is
always symmetric.  Therefore
\[
H_1(P)=e_2(P_{123})-3o_3(P_{123})=Q_3(P_{123})\geq0.         \tag{41}
\]

### 7.2 A one-site logical flag

For the family (36), (37) gives
\[
e_2=3\sum_{|R|=2}a_R,\qquad
o_3=\sum_{|R|=2}a_R,\qquad e_4=0.
\]
Consequently
\[
\boxed{\quad H_1(P)=Q_4(P)=0\quad}                          \tag{42}
\]
for every pure three-party state \(\phi\).  This is a large,
dimension-independent equality family and explains the cancellation
in (38).

### 7.3 Two product strings

Let \(P=|p\rangle\langle p|+|q\rangle\langle q|\), where \(p,q\) are
orthogonal product basis strings differing in exactly \(m\) of the four
positions.  Then
\[
p_\varnothing=2+2^{1-m},\qquad
p_R=2^{1-m}\quad
(\varnothing\ne R\subseteq\{\text{differing positions}\}),
\]
and all other sectors vanish.  Hence
\[
H_1(P)=2^{1-m}
\left[\binom m2-3\binom m3+6\,\mathbf 1_{\{m=4\}}\right]\geq0. \tag{43}
\]
It is zero for \(m=1,3,4\), and equals \(1/2\) for \(m=2\).

## 8. Encoded-Pauli form and a failed decoupling

For the maximally mixed code purification, write
\[
|\Psi\rangle\langle\Psi|
=\frac12\sum_{a=0}^3\sigma_a\otimes X_a,
\qquad X_0=\rho=P/2,
\]
and put
\[
S_k=\sum_{|T|=k}\|X_{0,T}\|_2^2,\qquad
T_k=\sum_{|T|=k}\sum_{a=1}^3\|X_{a,T}\|_2^2.
\]
Complementary purity gives
\[
T_2=S_2,\qquad
S_3=\frac12(S_1+T_1).
\]
Therefore
\[
\boxed{\quad
H_1(P)=3+S_2-\frac32(S_1+T_1)
=3+\frac12(S_2+T_2)-\frac32(S_1+T_1).
\quad}                                                       \tag{44}
\]

For the scalar part, two-copy positivity gives
\[
S_2\geq3S_1-6.                                               \tag{45}
\]
It is tempting to seek the separate Pauli inequality
\[
T_2\geq3T_1,                                                 \tag{46}
\]
which together with (45) would prove (44).  Equation (46) is false.
For the repetition code, only the logical \(Z\) operator survives on
proper reductions, with squared Hilbert--Schmidt norm \(1/2\) on every
nonempty proper subset.  Thus
\[
T_1=2,\qquad T_2=3,
\]
contradicting (46).  At equality, the scalar and Pauli slacks compensate
one another exactly.  A Clifford/sign-observable proof must therefore
keep the scalar and Pauli pieces coupled.

In the unnormalized convention \(X_a=V\sigma_aV^\dagger\), define
\[
L_k=\sum_{|T|=k}\sum_{a=1}^3\|X_{a,T}\|_2^2.
\]
Then (44) is equivalently
\[
\boxed{\quad L_2+12\geq2L_1+L_3.\quad}                       \tag{47}
\]
This is perhaps the cleanest form for a future adaptive-frame or
Clifford attack.

## 9. Three-replica rank certificate: useful but not yet positive

The rank-two condition can be exposed explicitly on three replicas.
For a subset \(S\subseteq[4]\), let
\[
J_S=\frac13\left(U_{(12)}^{(S)}
U_{(13)}^{(S)}+U_{(23)}^{(S)}\right),
\]
where a transposition permutes the three replicas on the sites in
\(S\).  For every normalized state \(\rho\),
\[
\operatorname{Tr}(\rho^{\otimes3}J_S)=\operatorname{Tr}\rho_S^2.
\]
Thus the homogeneous candidate (12), written for the physical
rank-at-most-two state \(\rho\), is
\[
\operatorname{Tr}(\rho^{\otimes3}\mathcal O)\geq0,\qquad
\mathcal O=
6J_{[4]}+\sum_{|S|=2}J_S-3\sum_{|S|=3}J_S.                  \tag{48}
\]
The global three-replica antisymmetrizer annihilates
\(\operatorname{supp}(\rho)^{\otimes3}\), since
\(\bigwedge^3\operatorname{supp}(\rho)=0\).

However, a simple positive-semidefinite certificate modulo that
antisymmetric sector does not work.  In the abstract tensor products of
the trivial, sign, and standard representations of \(S_3\),
\(\mathcal O\) has negative eigenvalues even after the global sign
isotypic component is removed.  Here is an exact two-dimensional
negative block.  Put the four local replica representations in the
types
\[
(\mathrm{sign},\mathrm{sign},\mathrm{trivial},\mathrm{standard}).
\]
The tensor product is globally standard, so it contains no global sign
representation.  The average of the three transpositions is zero in
the standard representation.  Hence every \(J_S\) containing the
fourth site vanishes on this block.  Among the remaining terms in
(48), the three pair terms contribute
\[
+I-I-I=-I,
\]
and the only triple term contributes \(-3I\).  Thus
\[
\mathcal O=-4I
\]
on a block containing no global antisymmetric vector.  These local
representation types already occur for qutrit physical spaces.

Discovery calculations also show that direct compression to random
two-dimensional codes can have negative eigenvalues, although its
weighted trace remains nonnegative in all searches.  Therefore a valid
three-replica proof must use more than the absence of
\(\bigwedge^3\): it must retain either the tensor-cube structure of the
code embedding or an additional sum-of-squares identity.

## 10. Discovery evidence

The following observations are not used as proof:

* Complex Riemannian gradient minimization of \(H_1\) over rank-two
  Grassmannians for \(d=2\) and \(d=3\) repeatedly converged to zero.
* Replacing the coefficient \(6\) in (6) by \(c=0,1,\ldots\) gave
  numerical optima \((6-c)/8\) for \(c\leq6\), attained by the
  repetition code, and zero for \(c\geq6\).
* Direct optimization of the homogeneous expression (12) over arbitrary
  pure states with reference dimensions \(2,3,4\) and four qubit
  physical systems also reached zero only.
* The equality set is not confined to product strings.  Gradient
  searches find continuous zero families with nontrivial one- and
  two-body spectra, consistent with the exact flag family (36) and
  additional, presently unclassified equality components.

## 11. Exact status and next bottleneck

Established here:

1. the exact sector formula (4) for \(Q_4(P)\);
2. the sharper, sharp-coefficient candidate (6);
3. the partial-trace and five-party purity forms (9)--(14);
4. the exact grouped-minus-conditioned defect identity (21);
5. exact averaged conditioning inequalities and a formal certificate
   that their linear closure is insufficient;
6. exact counterfamilies to defect tensorization, pairwise mass sharing,
   and scalar/Pauli decoupling;
7. several all-dimension positive subclasses and equality families;
8. a three-replica formulation showing precisely why merely invoking
   \(\bigwedge^3=0\) is not a positive certificate.

Not established:

* \(H_1(P)\geq0\) for arbitrary rank-two projections;
* \(Q_4(P)\geq0\) for arbitrary rank-two projections;
* the homogeneous pure-state conjecture (12);
* any all-copy conclusion.

The cleanest remaining statements are either the defect monotonicity
(22), the coupled encoded-Pauli inequality (47), or a three-replica
sum-of-squares refinement of (48).  A proof of any one of these would
settle the four-copy projection case and provide a concrete model for
the proposed higher-layer hierarchy
\[
\sum_{\ell\geq j}\binom{2\ell}{2j}e_{2\ell}
\geq3o_{2j+1}.
\]
