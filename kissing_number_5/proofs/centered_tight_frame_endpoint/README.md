# The centered unit-norm tight-frame endpoint at order 41

## Scope

This note isolates exact consequences of the especially rigid endpoint
hypothesis
\[
 x_1,\ldots,x_{41}\in S^4,\qquad
 \sum_i x_i=0,\qquad
 \sum_i x_ix_i^{\mathsf T}=\frac{41}{5}I_5,
 \qquad \langle x_i,x_j\rangle\leq\frac12\quad(i\ne j).
 \tag{1}
\]
It also gives an exact countermodel showing that a substantial collection
of tempting rowwise, two-point, and trianglewise consequences of (1) is
still insufficient.

Nothing here proves or assumes that every extremal code is centered or
tight.  The countermodel is not a spherical code.

## 1. Exact endpoint algebra

Let \(G=(\langle x_i,x_j\rangle)\).  From (1),
\[
 G{\bf1}=0,\qquad G^2=\frac{41}{5}G,\qquad
 \operatorname{spec}(G)=
 \left\{(41/5)^5,0^{36}\right\}.                       \tag{2}
\]
Define
\[
 B=I+J-2G.
 \tag{3}
\]
Then \(B\) is symmetric, has zero diagonal, and
\[
 0\leq B_{ij}\leq3\quad(i\ne j),\qquad B{\bf1}=42{\bf1}.
 \tag{4}
\]
Directly squaring (3), using \(JG=GJ=0\) and (2), gives the weighted
strongly-regular identity
\[
 \boxed{\;
 B^2=\frac{77}{5}I+\frac{287}{5}J-\frac{72}{5}B.
 \;}                                                     \tag{5}
\]
In particular,
\[
 \operatorname{spec}(B)=
 \left\{42^1,1^{35},(-77/5)^5\right\},                  \tag{6}
\]
and every row obeys
\[
 \sum_{j\ne i}B_{ij}=42,\qquad
 \sum_{j\ne i}B_{ij}^2=\frac{364}{5}.                  \tag{7}
\]
Equivalently,
\[
 \sum_{j\ne i}g_{ij}=-1,\qquad
 \sum_{j\ne i}g_{ij}^2=\frac{36}{5}.                   \tag{8}
\]
For \(i\ne j\), (5) also forces
\[
 \sum_k B_{ik}B_{kj}
 =\frac{287}{5}-\frac{72}{5}B_{ij}.                    \tag{9}
\]
The off-diagonal identities (9), not merely the diagonal moments (7), are
an essential part of tightness.

## 2. Exact anchored residual identities

Fix \(i\), put \(t_j=g_{ij}\) for \(j\ne i\), and set
\[
 z_j=x_j-t_jx_i\in x_i^\perp.
\]
The \(40\times40\) residual Gram matrix is
\[
 R_i=(\langle z_j,z_k\rangle)_{j,k\ne i}
     =G_{-i,-i}-tt^{\mathsf T}.                         \tag{10}
\]
The centered tight-frame equations give
\[
 \sum_{j\ne i}z_j=0,\qquad
 \sum_{j\ne i}z_jz_j^{\mathsf T}=\frac{41}{5}I_{x_i^\perp}.
\]
Consequently,
\[
 R_i{\bf1}=0,\qquad R_i^2=\frac{41}{5}R_i,\qquad
 \operatorname{spec}(R_i)=\{(41/5)^4,0^{36}\}.          \tag{11}
\]
This is stronger than checking only the diagonal of \(G^2=(41/5)G\).

There is also a useful two-anchor form.  Fix \(i\ne j\), let
\(t=g_{ij}>-1\), and for every \(k\notin\{i,j\}\) write
\[
 u_k=g_{ik},\qquad v_k=g_{jk},
\]
\[
 a_k=\frac{u_k+v_k}{\sqrt{2(1+t)}},\qquad
 c_k=\frac{u_k-v_k}{\sqrt{2(1-t)}}.
 \tag{12}
\]
Equations (2) and (8) give, exactly,
\[
\begin{aligned}
 \sum_k a_k&=-\sqrt{2(1+t)},&\qquad \sum_k c_k&=0,\\
 \sum_k a_k^2&=\frac{36}{5}-t,&
 \sum_k c_k^2&=\frac{36}{5}+t,&
 \sum_k a_kc_k&=0.                                     \tag{13}
\end{aligned}
\]
Triangle PSD is precisely \(a_k^2+c_k^2\leq1\), while the two kissing
inequalities become
\[
 \sqrt{\frac{1+t}{2}}a_k
 \mathbin{\pm}\sqrt{\frac{1-t}{2}}c_k\leq\frac12.
 \tag{14}
\]
The unexplained three-dimensional residual has total squared mass
\[
 \sum_k(1-a_k^2-c_k^2)=\frac{123}{5}.                  \tag{15}
\]
The antipodal case \(t=-1\) is excluded from (12) and must be handled
separately; no division by \(1+t\) is legitimate there.

Finally, every subset \(S\subseteq\{1,\ldots,41\}\), \(s=|S|\), obeys
\[
 \left\|\sum_{i\in S}x_i\right\|^2
 \leq \frac{s(41-s)}5.                                  \tag{16}
\]
Indeed, replace its indicator by
\({\bf1}_S-(s/41){\bf1}\), use \(G{\bf1}=0\), and use the largest
eigenvalue \(41/5\) of \(G\).  In \(B\)-language, (16) is
\[
 \sum_{i,j\in S}B_{ij}\geq\frac75s(s-11).               \tag{17}
\]

## 3. Exact triangle-PSD countermodel

The certificate
[`../../experiments/centered_tight_frame_endpoint/circulant_triangle_psd_countermodel.json`](../../experiments/centered_tight_frame_endpoint/circulant_triangle_psd_countermodel.json)
defines a symmetric circulant \(41\times41\) matrix \(M\).  Its diagonal is
one.  For cyclic distances \(1,\ldots,20\), its entries are
\[
\begin{split}
(&1/2,-1/2,-1/20,-1/4,-1/20,-1/20,-4/5,-3/4,0,3/10,\\
 &1/2,1/2,-3/20,1/2,1/2,1/2,-3/10,-1/2,-7/20,-1/20).
                                                               \tag{18}
\end{split}
\]
Every row therefore has the exact off-diagonal distribution
\[
\begin{array}{c|rrrrrrrrrrr}
q&-4/5&-3/4&-1/2&-7/20&-3/10&-1/4&-3/20&-1/20&0&3/10&1/2\\
\hline
\#&2&2&4&2&2&2&2&8&2&2&12.
\end{array}                                                \tag{19}
\]
Exact arithmetic verifies:

1. \(M_{ii}=1\), \(M_{ij}\leq1/2\), and \(M{\bf1}=0\);
2. every diagonal entry of \(M^2\) is \(41/5\);
3. every principal submatrix of order at most three is positive
   semidefinite;
4. for every dimension-five normalized Gegenbauer polynomial \(P_k\),
   \[
   \sum_jP_k(M_{ij})\geq0\qquad(k\geq0),                 \tag{20}
   \]
   with equality for \(k=1,2\);
5. every row has 12 contacts, 24 strictly negative entries, 14 strictly
   positive entries, and the quantitative degree consequences at
   \(\pm1/300\).

Thus the artifact simultaneously passes centered row moments, endpoint
row energies, all ordinary two-point harmonic inequalities, every
triangle Gram determinant, contact-degree sanity checks, and the robust
positive/negative degree lower bounds.

The all-degree claim (20) is finite and exact.  Degrees \(0,\ldots,89\)
are evaluated by the rational recurrence
\[
 (k+3)P_{k+1}(t)=(2k+3)tP_k(t)-kP_{k-1}(t).
 \tag{21}
\]
For \(k\geq90\), use
\[
 P_k(t)=\frac{2L'_{k+1}(t)}{(k+1)(k+2)}
 \]
and Bernstein's derivative inequality for the Legendre polynomial
\(\lVert L_{k+1}\rVert_{[-1,1]}=1\):
\[
 |P_k(t)|\leq\frac{2}{(k+2)\sqrt{1-t^2}}.
 \tag{22}
\]
The verifier checks rational upper bounds on the eleven reciprocal square
roots in (19).  Their multiplicity-weighted sum is
\[
 \frac{79973}{1750},
\]
so the absolute value of the off-diagonal sum in (20) is at most
\[
 \frac{79973}{875(k+2)}<1\qquad(k\geq90).               \tag{23}
\]

## 4. Exact failure and adversarial scope

The matrix \(M\) is **not** positive semidefinite.  Its principal minor on
zero-based indices
\[
 \{0,2,14,16\}
\]
has determinant
\[
 \boxed{-\frac{27}{16}}.                                \tag{24}
\]
Therefore it is not a Gram matrix, does not satisfy the off-diagonal
identities in (2) or (9), and is not a 41-point spherical code.

The exact lesson is narrow but useful:
\[
\begin{gathered}
\text{row centering + row second moments + all two-point harmonics}\\
\text{+ every triangle principal-minor test}
\end{gathered}
\]
do **not** imply the centered tight-frame endpoint.  Any valid
nonexistence proof along this route must use a genuinely common-source
order-four constraint, the full matrix identity \(G^2=(41/5)G\), a global
PSD certificate, or comparably stronger information.

Boundary cases are explicit: contacts \(M_{ij}=1/2\) are included, the
triangle audit allows determinant zero, and the failure (24) is a strict
exact rational inequality rather than a floating-point eigenvalue.

## 5. An exact all-degree three-point relaxation barrier

The second certificate
[`../../experiments/centered_tight_frame_endpoint/centered_tight_bv_pseudodistribution.json`](../../experiments/centered_tight_frame_endpoint/centered_tight_bv_pseudodistribution.json)
uses the same eleven pair nodes and the same pair multiplicities (19), but
it is independent of the circulant matrix above.  It supplies a positive
rational weight \(\nu_{abc}\) on each of the 246 determinant-feasible
unordered triple types \(a\leq b\leq c\) on this node set.

The normalization is
\[
 \sum_q\alpha_q=40,\qquad
 \sum_{a\leq b\leq c}\nu_{abc}=40\cdot39,             \tag{25}
\]
and the symmetrized marginal equations are
\[
 \sum_{a\leq b\leq c}
 \frac{\#\{a,b,c\text{ equal to }q\}}3\,\nu_{abc}
 =39\alpha_q.                                         \tag{26}
\]
Every triple in the support obeys
\[
 1+2abc-a^2-b^2-c^2\geq0.                             \tag{27}
\]
All these statements are checked directly over \(\mathbb Q\).

The pair and cyclic triple moments are exactly
\[
 \sum_q\alpha_qq=-1,\qquad
 \sum_q\alpha_qq^2=\frac{36}{5},\qquad
 \sum_{a\leq b\leq c}\nu_{abc}abc=\frac{1116}{25}.
 \tag{28}
\]
Consequently the formal Gram trace moments are
\[
 \operatorname{tr}G=41,\qquad
 \operatorname{tr}G^2=\frac{1681}{5},\qquad
 \operatorname{tr}G^3=\frac{68921}{25}.               \tag{29}
\]
These are precisely the moments of a positive semidefinite rank-five
matrix whose five nonzero eigenvalues are all \(41/5\).  Of course, a
pair/triple measure is not itself such a matrix; (29) records how much of
the tight-frame spectral endpoint survives the relaxation.

### 5.1 Every Bachoc--Vallentin radial block

Let \(\mu(u,v,t)\) be obtained by spreading each \(\nu\)-weight uniformly
over its distinct ordered permutations.  Put
\[
 A=(1-u^2)(1-v^2),\qquad w=t-uv,\qquad z=w/\sqrt A.
\]
For \(k>0\), the atomic radial block has node-node entries
\[
\begin{split}
 W_k(u,v)={}&{\bf1}_{u=v}\alpha_u(1-u^2)^k\\
 &+\sum_t\mu(u,v,t)A^{k/2}P_k^{(4)}(z),               \tag{30}
\end{split}
\]
where \(P_k^{(4)}(1)=1\).  The \(k=0\) block also includes the usual
diagonal atom \(u=1\), with bottom-right entry one and cross-vector
\(\alpha\).

For exact computation, divide row and column \(u\) by
\((1-u^2)^{\lfloor k/2\rfloor}\).  This is a positive diagonal
congruence.  Its transverse kernels are rational and split by parity:
\[
\begin{aligned}
 R_0&=1,&R_2&=\frac{4w^2/A-1}{3},\\
 R_1&=w,&R_3&=\frac{2w^3}{A}-w,                       \tag{31}\\
 R_{k+2}
 &=\frac{(k+1)(4w^2/A-2)R_k-(k-1)R_{k-2}}{k+3}.
\end{aligned}
\]
The exact verifier obtains:

- the full \(W_0\) is positive semidefinite of rank nine, with the
  fixed-cardinality kernel and the two independent design kernels
  represented by the radial functions \(u\) and \(u^2-1/5\);
- \(W_1\succeq0\) has rank nine and kernels represented by
  \({\bf1}\) and the node vector \(u\);
- \(W_2\succeq0\) has rank ten.  Its unscaled kernel is \({\bf1}\);
  after the congruence above this is the vector \(1-u^2\);
- every \(W_k\) for \(k\geq3\) is positive definite.

The finite portion \(1\leq k\leq186\) is proved by exact rational
\(LDL^{\mathsf T}\) decompositions.  The least positive pivot is about
\(1.32457895\cdot10^{-4}\), occurs in degree one, and is stored exactly
in the verifier output.

The infinite tail is also rigorous.  For dimension four,
\[
 P_k^{(4)}(\cos\theta)
 =\frac{\sin((k+1)\theta)}{(k+1)\sin\theta}.           \tag{32}
\]
There are only four ordered determinant-zero terms.  They give exact
positive-definite limiting matrices \(L_{\rm even}\) and
\(L_{\rm odd}\).  For every interior term, (32) gives the entry bounds
\[
 \frac{\sqrt{A/\Delta}}{k+1}\quad\hbox{and}\quad
 \frac{\sqrt{A^2/\Delta}}{k+1},
 \qquad \Delta=A-w^2,                                 \tag{33}
\]
in even and odd parity respectively.  Replacing the square roots by
checked integer upper bounds produces nonnegative rational matrices
\(B_{\rm even},B_{\rm odd}\).  The verifier evaluates
\[
 C_p=\max_i\sum_h |(L_p^{-1})_{ih}|
                    \sum_j(B_p)_{hj}
 \tag{34}
\]
and proves exactly
\[
 C_{\rm even}<141,\qquad C_{\rm odd}<186.              \tag{35}
\]
Thus
\(\|L_p^{-1}(W_k-L_p)\|_\infty<C_p/(k+1)<1\) for every
remaining degree \(k\geq187\).  The symmetric path from \(L_p\) to
\(W_k\) cannot acquire a zero eigenvalue, proving positive definiteness.

### 5.2 Further exact constraints that the witness passes

The ordinary dimension-five Gegenbauer moments are nonnegative in every
degree, with equality in degrees one and two.  Degrees through 89 are
checked exactly; the least positive value from degree three onward is
\(21/1600\).  Equations (22)--(23) prove the tail.

For every set \(S\subseteq\{0,1,2,3\}\) whose total harmonic dimension
\[
 r_S=\sum_{k\in S}(1,5,14,30)_k
\]
is below 41, the verifier checks every principal minor of
\[
 \left(
 1+\sum_q\alpha_qP_k(q)P_\ell(q)-\frac{41}{r_S}
 \right)_{k,\ell\in S}.                               \tag{36}
\]
All eleven eligible matrices are positive semidefinite.  These are the
complete nontrivial two-point frame/rank matrices in degrees at most
three.

The witness also passes 27 centered-third-moment rank cuts.  For each
listed harmonic combination \(K\) of feature rank \(r<41\), let
\[
 V=\operatorname{tr}K^2-\frac{(\operatorname{tr}K)^2}{r},\qquad
 D=\operatorname{tr}K^3-\frac{3\operatorname{tr}K\operatorname{tr}K^2}{r}
       +\frac{2(\operatorname{tr}K)^3}{r^2}.
\]
The sharp eigenvalue inequality
\[
 r(r-1)D^2\leq(r-2)^2V^3                            \tag{37}
\]
holds exactly in all 27 cases.  Equality occurs for
\[
 H_1,\quad H_0\mathbin{\pm}5H_1,\quad
 H_0\mathbin{\pm}H_1.
\]
For \(H_2\), the certificate has the independently imposed exact value
\[
 D=\frac{17}{50};                                    \tag{38}
\]
nevertheless (37) has positive slack.

### 5.3 The precise stronger constraint it fails

This certificate is deliberately **not** advertised as satisfying the
corrected common-pair-capacity hierarchy.  The verifier audits all 48
applicable contiguous-band and exact-stratum rows.  Exactly four have
negative slack, all at common-neighbor threshold \(1/2\):
\[
\begin{array}{c|c|c}
\text{base inner-product band}&\text{capacity}&\text{status}\\ \hline
[-1/2,-7/20]&1&\text{violated}\\
\{-7/20\}&1&\text{violated}\\
[-7/20,-3/10]&2&\text{violated}\\
\{-3/10\}&2&\text{violated}.
\end{array}                                           \tag{39}
\]
The minimum exact slack is
\[
 -\frac{689611676751007372091426251}
 {105064854935040000000000000}
 \approx-6.56367609.                                  \tag{40}
\]
Both pointwise weighted-capacity rows pass, but that does not repair
(39).

The conclusion is therefore specific.  Centering, exact Welch equality,
the exact cubic tight-frame trace, all ordinary two-point harmonics, all
full-radial three-point BV blocks, all low-degree frame matrices, and the
27 tested centered-skew rank cuts remain jointly feasible at mass 41 on
this rational support.  Any endpoint proof using only those constraints
cannot yield a contradiction.  Exact-stratum common-pair information is
genuinely independent and already excludes this particular witness.

## 6. Boundary cases, numerical rigor, and dependencies

Both verifiers use only the Python standard library and
`fractions.Fraction`.  The SDP solver used during discovery is not
imported and its status is not trusted.  Every stored \(\nu\)-weight is a
strictly positive rational.  Determinant-zero triples are retained, not
discarded; they are exactly the boundary terms in the analytic tail.
Contacts at inner product \(1/2\) are included.  The four capacity
failures are strict rational inequalities.

The proof dependencies for the relaxation barrier are:
\[
\begin{array}{c}
\text{rational certificate}\\
\downarrow\\
\text{mass, marginal, support, moments}\\
\downarrow\\
\begin{array}{c}
\text{finite exact }LDL^{\mathsf T}\\
\text{and principal-minor checks}
\end{array}
\quad+\quad
\begin{array}{c}
\text{analytic Gegenbauer tails}\\
\text{(22), (32)--(35)}
\end{array}\\
\downarrow\\
\text{all-degree pair/BV and finite-rank claims}.
\end{array}
\]
No part of this chain supplies four-point consistency, a global
positive-semidefinite \(41\times41\) Gram matrix, or rank at most five.

## Reproduction

From the repository root:

```sh
python3 experiments/centered_tight_frame_endpoint/verify_countermodel.py
python3 experiments/centered_tight_frame_endpoint/verify_centered_tight_bv.py
```

The construction-search file and the `.npz` files under `results/` are
discovery-only.  Neither exact verifier imports them.
