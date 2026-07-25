# Post-freeze bridge candidate for `Q2-E3-A1-B1-D1-N1`

**Recorded (UTC):** 2026-07-25T21:14:35Z.

**Bridge verdict:** **PASS as a candidate.** Every point of every nonempty
frozen pivot stratum is routed to exactly one of the legacy binary and
nonbinary fixed-cubic-line theorems. The strata `C30`--`C44` are empty by a
division-free rank argument. The strata `C00`--`C29` are all compatible with
the frozen leading tuple, but no claim is made here that every one admits a
Keller completion.

**Certification status:** unchanged. This note does not promote the row in
`CERTIFIED_EXCLUSION_STATUS.md`. Promotion still requires an independent
post-freeze hostile reconstruction of this bridge and the full-row assembly.
In particular, the legacy nonbinary hostile reconstruction is recorded only
in the aggregate `../VERIFICATION.md`, rather than in a retained standalone
report.

This note was produced with substantial AI assistance and is not peer
reviewed. Exact checks verify the encoded algebra and coverage ledger; they
are evidence, not peer review.

## 1. Exact scope

Let
\[
F=L_0X+H_2+H_3+H_4:\mathbb A^3_{\mathbb C}\longrightarrow
\mathbb A^3_{\mathbb C}
\]
have exact total degree four, with \(L_0\in\operatorname{GL}_3(\mathbb C)\)
and \(H_j\) homogeneous of degree \(j\). Assume that \(H_4\) belongs to the
frozen inclusive row
\[
R=\texttt{Q2-E3-A1-B1-D1-N1}.
\]
Its canonical leading tuple is
\[
(\operatorname{rank}JH_4,e,a,b,\delta,\nu)=(2,3,1,1,1,1).
\tag{1}
\]
No condition is imposed on \(H_2,H_3\), on their incidences with \(H_4\), or
on the first nonzero coefficient of \(H_4\).

The two legacy row theorems start after independent source and target changes
with
\[
H_4=h(p,q,r)(p,q,0)^T,\qquad 0\ne h\in\mathbb C[p,q,r]_3,
\tag{2}
\]
and split according as
\[
h\in\mathbb C[p,q]\quad\text{or}\quad
h\notin\mathbb C[p,q].
\tag{3}
\]
The purpose of this note is to derive (2) pointwise from the frozen tuple,
prove that (3) is intrinsic and exhaustive, and route all 45 frozen pivot
strata without dividing by a frozen coefficient.

## 2. Uniform exact leading normal form

### Lemma

For every \(H_4\) satisfying (1), there are
\[
S,T\in\operatorname{GL}_3(\mathbb C)
\]
and a nonzero homogeneous cubic \(h'\) such that
\[
T\,H_4(SX)=h'(x,y,z)(x,y,0)^T.
\tag{4}
\]
The construction uses no coefficient \(c_i\) of \(H_4\) as a denominator.

### Proof

The canonical-pencil theorem in `FROZEN_TAXONOMY_v1.md` gives an exact
factorization
\[
H_4=h\,A(p,q),
\tag{5}
\]
where:

- \(h\) is the component gcd and \(\deg h=e=3\);
- \(p,q\) are coprime ternary linear forms because \(a=1\); and
- \(A=(A_0,A_1,A_2)\) is a basepoint-free binary triple of degree \(b=1\).

Write
\[
A(u,v)=a\,u+b\,v
\tag{6}
\]
for column vectors \(a,b\in\mathbb C^3\). Basepoint freeness of a
degree-one triple is equivalent to linear independence of \(a,b\): if their
span had dimension one, all three entries of \(A\) would be multiples of one
binary linear form and would vanish at its projective root.

Complete \(a,b\) by a vector \(c\) to a target basis and put
\[
B=(a\ b\ c),\qquad T=B^{-1}.
\]
Then, exactly rather than merely projectively,
\[
T A(u,v)=(u,v,0)^T.
\tag{7}
\]
Likewise, coprime linear forms \(p,q\) are linearly independent. Complete
them by a linear form \(r\) to a source basis and choose \(S\) so that
\[
p(SX)=x,\qquad q(SX)=y,\qquad r(SX)=z.
\tag{8}
\]
Equations (5), (7), and (8) give (4), with \(h'=h\circ S\).
Invertible substitution preserves the nonzero degree-three gcd. ∎

### Explicit determinant charts

The lemma is pointwise uniform but can also be written as a finite chart
cover. If
\[
M_A=
\begin{pmatrix}
a_0&b_0\\
a_1&b_1\\
a_2&b_2
\end{pmatrix},
\]
then the three minors
\[
\Delta^A_{01},\quad\Delta^A_{02},\quad\Delta^A_{12}
\tag{9}
\]
cannot vanish simultaneously. Use the disjoint ordered charts
\[
\Delta^A_{01}\ne0;\quad
\Delta^A_{01}=0,\ \Delta^A_{02}\ne0;\quad
\Delta^A_{01}=\Delta^A_{02}=0,\ \Delta^A_{12}\ne0.
\tag{10}
\]
On each chart, the unused coordinate vector supplies \(c\), and
\(\det(a\ b\ c)\) is, up to sign, the selected minor.

The \(2\times3\) coefficient matrix of \(p,q\) has the analogous three-minor
cover. On each chart, the unused coordinate form supplies \(r\). Thus every
inverse in (7)--(8) divides only by a determinant known to be nonzero from
an intrinsic rank-two condition. No chart condition is a frozen coefficient
pivot, and simultaneous vanishing of all chart determinants is impossible
inside the row.

## 3. The binary/nonbinary split is intrinsic

Let
\[
U=\langle p,q\rangle\subset(\mathbb C^3)^*.
\tag{11}
\]
The canonical-pencil uniqueness theorem says that another minimal generator
\(p'/q'\) differs from \(p/q\) by a Möbius transformation. Since all four
forms have degree one,
\[
\langle p',q'\rangle=\langle p,q\rangle=U.
\]
The component gcd \(h\) is unique up to a nonzero scalar. Consequently
\[
h\in\operatorname{Sym}^3(U)
\tag{12}
\]
is independent of every choice in the canonical factorization.

After (8), expand
\[
\begin{aligned}
h'={}&h_{300}x^3+h_{210}x^2y+h_{120}xy^2+h_{030}y^3\\
&+h_{201}x^2z+h_{111}xyz+h_{021}y^2z
 +h_{102}xz^2+h_{012}yz^2+h_{003}z^3.
\end{aligned}
\tag{13}
\]
The binary branch is the division-free closed condition
\[
h_{201}=h_{111}=h_{021}=h_{102}=h_{012}=h_{003}=0.
\tag{14}
\]
Its complement is the union of the six ordered first-nonzero charts in
those same coefficients. The nonbinary theorem does not normalize or divide
by that first nonzero coefficient, so all six charts enter its stated scope
unchanged.

A different completion \(r\) replaces \(r\) by
\(\lambda r+\alpha p+\beta q\), with \(\lambda\ne0\), and cannot change
membership in \(\operatorname{Sym}^3(U)\). A different basis of \(U\) acts
through \(\operatorname{Sym}^3(\operatorname{GL}_2)\), whose determinant is
\[
\det(\operatorname{Sym}^3 M)=(\det M)^6\ne0.
\tag{15}
\]
Thus (14) versus its complement is an exhaustive invariant split, not a
normal-form chart that can lose a boundary.

## 4. Exact frozen-pivot coverage

Use the frozen monomial order
\[
\begin{split}
&(m_0,\ldots,m_{14})=(
x^4,x^3y,x^3z,x^2y^2,x^2yz,x^2z^2,xy^3,xy^2z,xyz^2,xz^3,\\
&\hspace{37mm}y^4,y^3z,y^2z^2,yz^3,z^4).
\end{split}
\tag{16}
\]

### The potentially nonempty strata `C00`--`C29`

For \(0\le i\le14\), choose a linear factor \(\ell_i\mid m_i\) and an
independent coordinate form \(n_i\) by
\[
\ell_i=x,\ n_i=y\quad(0\le i\le9),\qquad
\ell_i=y,\ n_i=x\quad(10\le i\le13),\qquad
\ell_{14}=z,\ n_{14}=x.
\tag{17}
\]
Put \(h_i=m_i/\ell_i\), a cubic monomial. Then
\[
H^{(i)}_4=(m_i,h_i n_i,0)^T
          =h_i(\ell_i,n_i,0)^T
\tag{18}
\]
has the frozen leading tuple and pivot label \(\mathrm C_i\), while
\[
\widetilde H^{(i)}_4=(0,m_i,h_i n_i)^T
          =h_i(0,\ell_i,n_i)^T
\tag{19}
\]
has the frozen leading tuple and pivot label \(\mathrm C_{15+i}\).

Indeed, \(\gcd(\ell_i,n_i)=1\), so the component gcd in (18)--(19) is
exactly \(h_i\) of degree three. The residual degree-one triple has
two-dimensional span and parametrizes a target line birationally. In source
coordinates \((\ell_i,n_i,r_i)\), a \(2\times2\) Jacobian minor of
\((h_i\ell_i,h_i n_i)\) is
\[
h_i(4h_i-r_i\partial_{r_i}h_i).
\tag{20}
\]
For a nonzero cubic, the operator
\(h\mapsto4h-r_i\partial_{r_i}h\) multiplies the terms of \(r_i\)-degree
\(0,1,2,3\) by \(4,3,2,1\), respectively, so (20) is nonzero. Thus the
Jacobian rank is two. Equations (18)--(19) also have the advertised first
nonzero frozen coefficient by construction.

Thus no stratum `C00`--`C29` is empty for a reason visible from the frozen
leading tuple alone. These are leading-term witnesses, not asserted Keller
maps: a stratum could still be empty after all lower Keller identities are
imposed. The bridge does not need such an existence assertion. If a point of
\(R/\mathrm C_i\) exists, the uniform lemma applies to it directly.

### `C30`--`C44` are empty division-free

If a point had first pivot `C30` or later, then all coefficients in the
first two fifteen-coefficient target blocks would vanish:
\[
H_{4,1}=H_{4,2}=0.
\tag{21}
\]
The Jacobian \(JH_4\) would have at most one nonzero row, so
\(\operatorname{rank}JH_4\le1\). This contradicts the rank-two condition
in (1). This argument uses only coefficient vanishing and minors; it has no
division or normal-form denominator. Therefore
\[
R/\mathrm C_i=\varnothing\qquad(30\le i\le44).
\tag{22}
\]

### Routing table

For an arbitrary point, not merely the witnesses above, the complete map is
\[
\begin{array}{c|c}
\text{frozen pieces}&\text{route}\\ \hline
R/\mathrm C_{00},\ldots,R/\mathrm C_{14}
 &\text{if nonempty, apply the uniform lemma, then (14) or its complement},\\
R/\mathrm C_{15},\ldots,R/\mathrm C_{29}
 &\text{if nonempty, apply the same lemma; a zero first component is allowed},\\
R/\mathrm C_{30},\ldots,R/\mathrm C_{44}
 &\varnothing\text{ by the division-free rank argument (21).}
\end{array}
\tag{23}
\]
The equations defining a pivot stratum only label the point. Neither the
normalization lemma nor the binary/nonbinary test divides by its pivot
coefficient.

## 5. Transfer to the legacy exclusions

Set
\[
F'(X)=T\,F(SX).
\]
The exact chain rule gives
\[
JF'(X)=T\,JF(SX)\,S,\qquad
\det JF'(X)=\det(T)\det(S)\det JF(SX).
\tag{24}
\]
Hence \(F\) is Keller if and only if \(F'\) is Keller. Pre- and
postcomposition by invertible linear maps preserve exact degree and preserve
the property of being a polynomial automorphism. They also leave the
transformed \(H_2,H_3\) completely arbitrary and the transformed linear part
invertible.

If (14) holds, \(F'\) lies in the exact scope of
`../WORKING_BINARY_FIXED_CUBIC_LINE_ROW.md`. Its specialization-safe orbit
tree and coordinate exits show that every Keller map in that branch is an
automorphism.

If (14) fails, \(F'\) lies in the exact scope of
`../WORKING_FIXED_CUBIC_LINE_ROW.md`. Its division-free valuation argument,
exceptional double-factor classification, and two residual orbit
eliminations likewise show that every Keller map in that branch is an
automorphism.

The two scopes are disjoint and exhaustive by Section 3. Thus, assuming the
legacy theorems and their stated audit records, no quartic Keller
counterexample survives any frozen pivot stratum in (23).

## 6. Exact replay and pinned inputs

From `dimension_three_keller_degree/rung2_degree_bound`, run

```text
/usr/bin/python3 taxonomy_freeze/verify_bridge_q2_e3_a1_b1_d1_n1_v1.py
taxonomy_freeze/replay_bridge_q2_e3_a1_b1_d1_n1_v1.sh
```

The bridge verifier is fail closed. It checks the exact frozen row and all
45 pivot IDs, pins the frozen and legacy proof inputs by SHA-256, constructs
and verifies leading-tuple witnesses for every `C00`--`C29`, proves the
generic target and source chart identities, checks the binary-subspace
determinant (15), checks the rank-two identity (20), reconstructs the
division-free emptiness of `C30`--`C44`, and checks the Keller determinant
transfer (24).

The replay wrapper runs the independent SymPy and PARI/GP implementations for
both legacy halves, the two retained binary hostile reconstructions, and the
binary fail-closed fault suite.

Pinned input hashes are:

```text
41fccc44d23fab125819990a2b27526771fbfb62293910b98cfcf1821576d03d  FROZEN_TAXONOMY_v1.md
5a2bdd57438e9ebcca18d04c53ebc98ced2b61209e2de99674aede501c615c23  frozen_manifest_v1.json
9a10c1c103b60eb21405518074086168330a435bb5aa1770d51463a881a926ca  ../WORKING_FIXED_CUBIC_LINE_ROW.md
51818647fa7f57942761ca31ed80dc9dde4363ebe83166d87fc80f07861a9607  ../WORKING_BINARY_FIXED_CUBIC_LINE_ROW.md
fdcf31dc44bda116c0e81da6a9d96abf0b92798eb8d56ec25d6c124b31d4b8b8  ../verify_fixed_cubic_line_sympy.py
aeded24439435f5db31d2e702fe357ec0799b62a326761e514727ff77dcc61e1  ../verify_fixed_cubic_line_pari.gp
0d2003acef22b541161230fe1d3ed21399897ee443a6df9b6fc278be99dba464  ../verify_fixed_cubic_line_pari_strict.sh
5c570a002f93c5583618baf615419419e4ee55b2ab3f961cde9bca6f6cc56340  ../verify_binary_fixed_cubic_complete.py
5568acae07db33984d11e4bb5fa824339faade90828a1f642f33486fa425da1b  ../verify_binary_fixed_cubic_complete_pari.gp
4cea6002ca7639cf8e04aea80b86daa76655c7359e041e2e7707e50418fa7fc4  ../audit_binary_fixed_cubic_hostile/REPORT.md
45195a94af63ad4d268d951a84a769965ef0821fb90e024f22bf4739620ed334  ../audit_binary_fixed_cubic_hostile/audit_orbits_lower_exact.py
4040c2999d790edb96ee20492bc7afbc9c7b98fb11b297ca07c96e5329f0eb58  ../audit_binary_fixed_cubic_hostile/audit_exceptional_branches_exact.py
474d073c3ef62afa34546e3292ada02c5267e19575be5917b6db9f02c6c0a803  ../audit_binary_fixed_cubic_hostile/test_fail_closed.sh
71190f6e6b68fb7e3837c76bb944fac2e85a7c92ed938f471d05e9497b6eb9e8  ../VERIFICATION.md
```

## 7. Remaining certification obligation

No pivot-coverage or binary/nonbinary assembly gap remains in this candidate.
The precise unresolved certification obligation is methodological:

1. a fresh hostile auditor must reconstruct the rank-two
   factorization-to-normal-form bridge without assuming (4);
2. the auditor must independently check all 30 potentially nonempty pivot
   routes, the leading-tuple witnesses, the 15 empty strata, and invariance
   of the split (12);
3. because the legacy nonbinary hostile audit survives only as aggregate
   prose, the auditor must either retain a standalone reconstruction of that
   half or explicitly replay its raw factor, orbit, and lower-exit
   completeness; and
4. only after that report passes should
   `CERTIFIED_EXCLUSION_STATUS.md` be changed.

Accordingly, this artifact is a complete bridge candidate, not itself the
final promotion certificate.
