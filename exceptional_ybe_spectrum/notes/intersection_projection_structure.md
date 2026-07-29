# Canonical three-site intersection projections

**Date:** 2026-07-28
**Scope:** arbitrary exceptional projection \(P\); no Pauli, controlled,
irreducibility, or leg-commutant assumption
**Status:** exact four-site theorem and exact limitation countermodel; no
four-divisibility obstruction

## 1. Setup

Let \(V\cong\mathbb C^d\), let

\[
P=P^*=P^2,\qquad \operatorname{rank}P=\frac{d^2}{2},
\]

and put

\[
p=P_{12},\qquad q=P_{23},\qquad r=P_{34}.
\]

The exceptional relation is

\[
pqp-qpq=c(p-q),\qquad c=\frac13. \tag{1}
\]

Automatic standardness, already proved in the structural track, gives

\[
\operatorname{Tr}_1P=\operatorname{Tr}_2P=\frac d2I_d. \tag{2}
\]

Consequently the normalized matrix traces are Markov:

\[
\tau_{n+1}(xP_{n,n+1})=\eta\tau_n(x),
\qquad \eta=\frac12, \tag{3}
\]

for every \(x\) supported on the first \(n\) sites.

The common-one projection of \(p,q\) is

\[
e=e(p,q)
=\frac{pqp-cp}{1-c}
=\frac32pqp-\frac12p. \tag{4}
\]

The common-zero projection is

\[
f=f(p,q)
=\frac{(I-p)(I-q)(I-p)-c(I-p)}{1-c}. \tag{5}
\]

They have

\[
\operatorname{rank}e=\operatorname{rank}f=\frac{d^3}{8}. \tag{6}
\]

Write \(g=I-e-f\) for the generic two-projection sector.

## 2. All forced one- and two-site marginals

### Proposition 2.1

The outer one-site partial traces are

\[
\boxed{
\operatorname{Tr}_3e=\frac d4P_{12},\qquad
\operatorname{Tr}_1e=\frac d4P_{23}.
} \tag{7}
\]

For the common-zero projection,

\[
\boxed{
\operatorname{Tr}_3f=\frac d4(I-P_{12}),\qquad
\operatorname{Tr}_1f=\frac d4(I-P_{23}).
} \tag{8}
\]

Tracing any two of the three sites gives

\[
\boxed{
\operatorname{Tr}_{jk}e
=\operatorname{Tr}_{jk}f
=\frac{d^2}{8}I
}
\qquad(\{j,k\}\subset\{1,2,3\}). \tag{9}
\]

Consequently

\[
\operatorname{Tr}_3g=\operatorname{Tr}_1g
=\frac{3d}{4}I_{d^2},\qquad
\operatorname{Tr}_{jk}g=\frac{3d^2}{4}I_d. \tag{10}
\]

### Proof

Since \(p\) is independent of site \(3\),

\[
\operatorname{Tr}_3(pqp)
=p\,\operatorname{Tr}_3(q)\,p
=\frac d2p.
\]

Also \(\operatorname{Tr}_3p=dp\).  Substitution in (4) gives

\[
\operatorname{Tr}_3e
=d\,\frac{1/2-c}{1-c}p
=\frac d4p.
\]

The alternative expression

\[
e=\frac{qpq-cq}{1-c}
\]

gives the other outer trace.  Applying the same calculation to the
complementary projections \(I-p,I-q\), which satisfy (1) with the same
coefficient \(c\), proves (8).  Equation (9) now follows by one further
partial trace and (2).  Subtracting from the identity proves (10).
\(\square\)

### The uncontracted middle marginal

The only one-site contraction not explicitly fixed by (7)--(8) is

\[
K=\operatorname{Tr}_2e\in\operatorname{End}(V_1\otimes V_3),\qquad
L=\operatorname{Tr}_2f. \tag{11}
\]

The universally forced data are

\[
K,L\geq0,\qquad
\operatorname{Tr}K=\operatorname{Tr}L=\frac{d^3}{8}, \tag{12}
\]

\[
\operatorname{Tr}_1K=\operatorname{Tr}_3K
=\operatorname{Tr}_1L=\operatorname{Tr}_3L
=\frac{d^2}{8}I_d, \tag{13}
\]

and

\[
0\leq K,L\leq\frac d2I_{d^2}. \tag{14}
\]

The last inequality follows from \(e\leq p,q\) and
\(f\leq I-p,I-q\), followed by the middle partial trace.

For an exact expression, put

\[
S=\operatorname{Tr}_2(pq).
\]

Expanding (4)--(5) gives

\[
\boxed{
K+L
=\frac{S+S^*-cdI}{1-c}
=\frac32(S+S^*)-\frac d2I.
} \tag{15}
\]

There is currently no proof that \(K\) or \(L\) is scalar.  It would be
incorrect to insert scalar middle marginals into a general argument.  A
saved unrestricted numerical \(d=4\) solution has a visibly nonscalar
\(K\); that observation is only an assumption warning, not an exact
classification statement.

## 3. A universal four-site angle-\(1/4\) theorem

On four sites define

\[
E=e(p,q),\qquad F=e(q,r). \tag{16}
\]

Thus \(E\) means \(e\otimes I_d\), and \(F\) means \(I_d\otimes e\).

### Theorem 3.1

Every exceptional solution satisfies

\[
\boxed{
ErE=\frac12E,
\qquad
EFE=\frac14E,
\qquad
FEF=\frac14F.
} \tag{17}
\]

The shifted common-zero projections

\[
E_0=f(p,q),\qquad F_0=f(q,r)
\]

satisfy the same relations:

\[
E_0(I-r)E_0=\frac12E_0,\qquad
E_0F_0E_0=\frac14E_0,\qquad
F_0E_0F_0=\frac14F_0. \tag{18}
\]

Opposite signs are orthogonal:

\[
\boxed{
EF_0=F_0E=E_0F=FE_0=0.
} \tag{19}
\]

### Proof

The key point is that the claimed scalar compression can be obtained from
a zero-variance calculation; it is not being assumed from the abstract
two-projection decomposition.

Let \(\tau=\tau_4\) be normalized matrix trace.  Set

\[
T=\tau(ErEr).
\]

Insert (4) for the middle copy of \(E\).  Using \(Ep=pE=E\) and
\(pr=rp\),

\[
\begin{aligned}
T
&=\frac{\tau(Erpqp r)-c\tau(Erpr)}{1-c}\\
&=\frac{\tau(Erqr)-c\tau(Er)}{1-c}. \tag{20}
\end{aligned}
\]

The adjacent relation for \(q,r\) is

\[
rqr=qrq-cq+cr.
\]

Since \(Eq=qE=E\), cyclicity gives

\[
\tau(Erqr)=(1+c)\tau(Er)-c\tau(E). \tag{21}
\]

Combining (20)--(21),

\[
T=\frac{\tau(Er)-c\tau(E)}{1-c}. \tag{22}
\]

The Markov property (3) says

\[
\tau(Er)=\eta\tau(E)=\frac12\tau(E).
\]

At the exceptional values \((c,\eta)=(1/3,1/2)\), equation (22) becomes

\[
T=\frac14\tau(E). \tag{23}
\]

Now \(ErE-\frac12E\) is self-adjoint, and

\[
\tau\left(\left(ErE-\frac12E\right)^2\right)
=T-\frac14\tau(E)=0.
\]

Faithfulness of matrix trace proves \(ErE=E/2\).

Because

\[
F=\frac{qrq-cq}{1-c}
\]

and \(Eq=qE=E\),

\[
EFE
=\frac{ErE-cE}{1-c}
=\frac14E.
\]

The operator \(2FE:\operatorname{ran}E\to\operatorname{ran}F\) is therefore
an isometry.  The two projections have the same finite rank, so it is onto,
and \(FEF=F/4\).

Apply the same argument to \(I-p,I-q,I-r\) to obtain (18).  Finally,
\(E\leq q\), \(F_0\leq I-q\), \(E_0\leq I-q\), and \(F\leq q\), which
proves (19).
\(\square\)

### Corollary 3.2: exact four-site block structure

The pair \(E,F\) has:

- no common-one sector;
- \(d^4/8\) generic two-dimensional blocks with squared principal-angle
  cosine \(1/4\);
- a common-zero sector of dimension \(3d^4/4\).

Indeed, (17) makes \(2FE\) a unitary between the two ranges, and

\[
\operatorname{rank}E=\operatorname{rank}F
=d\frac{d^3}{8}=\frac{d^4}{8}. \tag{24}
\]

Equivalently,

\[
(EF)^2=\frac14EF,\qquad
(FE)^2=\frac14FE, \tag{25}
\]

and every nonzero singular value of \(EF\) is \(1/2\).

The endpoint contractions of the overlap are also exact:

\[
\operatorname{Tr}_4(EF)=\frac d4E,\qquad
\operatorname{Tr}_1(EF)=\frac d4F, \tag{26}
\]

\[
\operatorname{Tr}_{34}(EF)=\frac{d^2}{16}P_{12},\qquad
\operatorname{Tr}_{14}(EF)=\frac{d^2}{16}P_{23},\qquad
\operatorname{Tr}_{12}(EF)=\frac{d^2}{16}P_{34}. \tag{27}
\]

The same formulas hold for \(FE\).  They follow by pulling the factor
independent of the traced endpoint through the partial trace and then
using (7).

## 4. Arithmetic audit

At four sites the only new block count is

\[
\frac{d^4}{8}. \tag{28}
\]

Its integrality again forces only \(2\mid d\).  For \(d=6\),

\[
\operatorname{rank}E=162,\qquad
\dim(\text{common zero of }E,F)=972. \tag{29}
\]

Both are integers.  The canonical partial isometry

\[
U=2FE:\operatorname{ran}E\longrightarrow\operatorname{ran}F \tag{30}
\]

acts between spaces of the same even dimension \(162\).  Neither its
existence nor its determinant supplies a parity condition on \(d/2\).

The generic sector of \(E,F\) again carries a canonical complex
\(\mathrm{Cl}_2\)-action.  Its irreducible modules have dimension two and
occur with multiplicity \(d^4/8\).  At \(d=6\) that multiplicity is \(162\),
so this Clifford action also gives no four-divisibility obstruction.

## 5. Determinant, QCA-index, and Frobenius--Schur audit

The phrase “canonical unitary \(2FE\)” requires care.  It is a unitary
**between two different subspaces**.  It is not a unitary operator on all
of \(V^{\otimes4}\).  Its determinant is therefore not basis-independent:
changing the orthonormal basis of either range changes the displayed
determinant by an arbitrary phase.

There is a canonical full-space direct rotation, but it carries no parity.
Let

\[
G=\frac{4}{3}(E+F-EF-FE) \tag{31}
\]

be the projection onto the generic support of \(E,F\), and define

\[
\mathcal R=
\bigl(2F-G\bigr)\bigl(2E-G\bigr)+(I-G). \tag{32}
\]

On every generic two-dimensional block, one may choose a basis in which

\[
E=\begin{pmatrix}1&0\\0&0\end{pmatrix},\qquad
F=\begin{pmatrix}
1/4&\sqrt3/4\\
\sqrt3/4&3/4
\end{pmatrix}.
\]

Then

\[
\mathcal R\big|_{\mathrm{block}}
=\begin{pmatrix}
-1/2&-\sqrt3/2\\
\sqrt3/2&-1/2
\end{pmatrix}. \tag{33}
\]

Thus

\[
\mathcal R^3=I,\qquad \det\mathcal R=1. \tag{34}
\]

The determinant is one **block by block**, not because the number of
blocks has any parity.  This eliminates a determinant route to
\(4\mid d\).

A QCA index is not presently defined for \(2FE\): it is neither a
full-space unitary nor a proved locality-preserving automorphism of an
infinite tensor product.  Extending it arbitrarily on the orthogonal
complements introduces a free unitary choice and can change the determinant
at will.  Any single finite-support extension, regarded as a one-dimensional
QCA, has trivial GNVW index.  A nontrivial index argument would first
require a new theorem identifying the range of \(e\) with a canonical
tensor factor and proving compatible all-chain extensions.  Assuming such
a factorization would assume precisely the missing spatial-coherence
statement.

The same issue blocks a Frobenius--Schur argument.  The partial isometry
connects two shifted subspaces; it supplies neither a bilinear pairing nor
an antiunitary on one fixed space.  Tensor reversal sends a general \(P\)
to its flipped solution, not necessarily to \(P\), and complex conjugation
sends it to \(\overline P\).  No invariant antiunitary squaring to \(-I\)
follows.  Even after a noncanonical Halmos basis is chosen, (33) is an
ordinary real two-dimensional rotation and exists with any number of
blocks.

### Exact information in the middle marginal

Equations (12)--(14) imply useful but parity-free spectral bounds.  Since
\(K\) acts on a \(d^2\)-dimensional space,

\[
\operatorname{Tr}(K^2)
\geq \frac{(\operatorname{Tr}K)^2}{d^2}
=\frac{d^4}{64}, \tag{35}
\]

with equality exactly when

\[
K=\frac d8I_{d^2}. \tag{36}
\]

The operator bound \(K\leq dI/2\) gives

\[
\operatorname{Tr}(K^2)\leq\frac d2\operatorname{Tr}K
=\frac{d^4}{16},\qquad
\operatorname{rank}K\geq\frac{d^2}{4}. \tag{37}
\]

The same statements hold for \(L\).  At \(d=6\), these say only

\[
\frac{81}{4}\leq\operatorname{Tr}(K^2)\leq81,\qquad
\operatorname{rank}K\geq9.
\]

Half-integral scalar coefficients in (7), (9), or (36) are allowed for
positive matrices and carry no rank divisibility.

The four-site identity does not directly fix \(\operatorname{Tr}(K^2)\).
That moment contracts two copies of \(e\) along their middle legs, whereas
\(E=e_{123}\) and \(F=e_{234}\) overlap an outer and a middle leg in opposite
roles.  Replacing one contraction by the other would be an unproved
rotation or sphericality assumption.  This is another tempting but invalid
shortcut.

## 6. Exact dimension-six limitation countermodel

The marginal and four-site identities above are strong, but they are not
by themselves equivalent to the original cubic relation.

Let

\[
V=\mathbb C^2\otimes\mathbb C^s,\qquad d=2s,
\]

and on the qubit factors put

\[
P_{\mathrm{eq}}=|00\rangle\langle00|+|11\rangle\langle11|,
\]

\[
|\gamma_+\rangle=\frac{|000\rangle+|111\rangle}{\sqrt2},\qquad
|\gamma_-\rangle=\frac{|010\rangle+|101\rangle}{\sqrt2}.
\]

After grouping qubit and spectator coordinates sitewise, define

\[
\widehat P=P_{\mathrm{eq}}\otimes I_{s^2},\qquad
\widehat e=|\gamma_+\rangle\langle\gamma_+|\otimes I_{s^3},
\qquad
\widehat f=|\gamma_-\rangle\langle\gamma_-|\otimes I_{s^3}. \tag{38}
\]

For every \(s\), and in particular for \(s=3,d=6\), these projections have
exactly the same:

- ranks \(d^2/2,d^3/8,d^3/8\);
- outer partial traces (7)--(8);
- all two-site partial traces (9);
- same-sign shifted angle-\(1/4\) relations (17)--(18);
- opposite-sign shifted orthogonality (19).

Their middle marginal is explicitly nonscalar:

\[
\operatorname{Tr}_2\widehat e
=\frac d4\widehat P_{13},\qquad
\operatorname{Tr}\bigl((\operatorname{Tr}_2\widehat e)^2\bigr)
=\frac{d^4}{32}. \tag{39}
\]

Thus even the complete marginal/angle package does not force (36).

Nevertheless this is not an exceptional solution.  The projections
\(\widehat P_{12},\widehat P_{23}\) commute, and

\[
\widehat P_{12}\widehat P_{23}\widehat P_{12}
-\widehat P_{23}\widehat P_{12}\widehat P_{23}=0
\ne\frac13(\widehat P_{12}-\widehat P_{23}). \tag{40}
\]

Moreover, \(\widehat e\) is only half of the common-one space:

\[
\operatorname{rank}
(\operatorname{ran}\widehat P_{12}\cap
 \operatorname{ran}\widehat P_{23})
=2s^3,
\qquad
\operatorname{rank}\widehat e=s^3. \tag{41}
\]

Thus this is an exact tensor countermodel to any argument that discards
the **full-intersection** condition or the generic \(1/3\)-angle sector and
then tries to derive \(4\mid d\) from the marginals and four-site
angle-\(1/4\) relation alone.

## 7. Conclusion

The canonical common-one and common-zero projections contain a clean,
previously unstated four-site Temperley--Lieb-like structure.  It is valid
for every exceptional solution and may be useful in a cell or commuting
square formulation.

It does not settle the spectrum.  Its exact block arithmetic permits
\(d=4m+2\), and the dimension-six tensor countermodel shows that the
derived marginal/angle package alone cannot restore the missing parity.
Any successful divisibility proof must still use information tying \(e\)
to the **entire** common intersection of \(P_{12},P_{23}\), including the
generic squared-angle-\(1/3\) sector, or another invariant of the two
simultaneous spatial embeddings.
