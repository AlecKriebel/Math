# Blinded hostile audit of the exact-\(\delta\ge3\) denominator

## Verdict

**PASS.**  The readiness denominator is intrinsically defined and complete
at its stated coarse level.  In the constant-independent locus,
\(\delta=3\) has Hilbert--Burch shape \(\{2,1\}\) and \(\delta=4\) has
shape \(\{2,2\}\); constant dependence is one separate power-fibre orbit.
There is no \(\delta=5\) independent case.

The complete fine incidence denominator for these three coarse strata is

\[
\boxed{
19\text{ exact-}\delta=3\text{ families}
+6\text{ exact-}\delta=4\text{ families}
+1\text{ power-fibre orbit}
=26.}
\]

Here “family” means a disjoint parameterized incidence stratum, not a
single orbit.  Every actual modulus displayed below is retained.  In
particular, one squarefree contact family is a two-sheeted orbit cover over
the generic \(\kappa\)-line; it is one \(z\)-parameter family, not two
overlapping frozen strata.

No lower Keller identity was examined.  The forbidden
`binary_locus/delta_ge3_universal/` directory and all primary-agent results
were not read.  Inputs were limited to the frozen row, the permitted
readiness report, and artifacts predating that forbidden package.

## 1. Intrinsic setup

On the binary part of the frozen row
`Q2-E2-A1-B2-D1-N2`, write
\[
H_4=(P,Q,0),\qquad
P=hp^2,\quad Q=hq^2,
\]
where
\[
h=Ap^2+Bpq+Cq^2\ne0,
\qquad
R=(H_3)_3=ap^3+bp^2q+cpq^2+dq^3.
\]
The top identity gives \(R\in\mathbb C[p,q]_3\).  Put
\[
\alpha=J(Q,R),\qquad
\beta=-J(P,R),\qquad
\gamma=J(P,Q)=8h^2pq,
\]
\[
g=\gcd(\alpha,\beta,\gamma),\qquad
\delta=\deg g.                                      \tag{1}
\]

The full joint stabilizer of the squaring cover is
\[
(\mathbb C^\times)^2\rtimes\langle p\leftrightarrow q\rangle.
\]
Projectively, a diagonal element acts by
\[
\begin{aligned}
[A:B:C]&\longmapsto
[A\lambda^2:B\lambda:C],\\
[a:b:c:d]&\longmapsto
[a\lambda^3:b\lambda^2:c\lambda:d],
\end{aligned}                                       \tag{2}
\]
after suppressing common scalars.  The involution reverses both
coefficient lists.  Therefore the four \(h\)-charts are exactly
\[
p^2,\qquad pq,\qquad p(p+q),\qquad
p^2+\eta pq+q^2,\quad \kappa=\eta^2.                 \tag{3}
\]
The last chart is squarefree for \(\kappa\ne4\); at \(\kappa=4\) it is the
doubled nonbranch chart \((p+q)^2\).

## 2. Local contribution lemma

This lemma is the completeness engine.

Work at a nonbranch root \(x=0\) of \(h\), with
\[
v_x(h)=m\in\{1,2\},\qquad v_x(R)=n.
\]
Since the pencil ratio is a unit there, the localized ideal
\((\alpha,\beta,\gamma)\) is equivalent to
\[
(3h'R-4hR',\ hR,\ h^2).
\]
The leading coefficient of the first generator is \(3m-4n\), which never
vanishes for \(m\in\{1,2\}\) and integral \(0\le n\le3\).  Hence the local
contribution to \(\delta\) is
\[
\boxed{c_{\rm fixed}(m,n)=\min(m+n-1,2m).}           \tag{4}
\]
Thus
\[
\begin{array}{c|cccc}
&n=0&n=1&n=2&n=3\\ \hline
m=1&0&1&2&2\\
m=2&1&2&3&4 .
\end{array}                                         \tag{5}
\]

At a branch point, let \(m\) again be the multiplicity of \(h\) and \(n\)
that of \(R\).  Except at \((m,n)=(2,3)\), the contribution is
\[
\boxed{c_{\rm branch}(m,n)=
\min(m+n-1,2m+1)}
\quad\text{when }m+n>0.                              \tag{6}
\]
When \(m=n=0\), the contribution is one precisely when the local Wronskian
\[
3h'R-4hR'
\]
vanishes at the branch point; otherwise it is zero.  When \(m=0,n\ge2\),
the contribution is also one.  Call either event a **bare-branch contact**
and denote its indicator by \(\epsilon\).

The exceptional pair \((m,n)=(2,3)\) is
\[
h=p^2,\qquad R=p^3
\]
up to the branch swap.  There \(\alpha,\beta\) are dependent, so it belongs
to the power fibre rather than to an exact-\(\delta\) stratum.

Equations (4)--(6) are division-free valuation statements.  Since
\(\gamma=8h^2pq\), there is no other possible support for \(g\).

## 3. Exhaustive mechanism table

Let \(n_p,n_q\) be the root multiplicities of \(R\) at the two branch
points.  On the one-branch chart put \(L=p+q\) and let \(n_L\) be its
multiplicity.  On a squarefree interior chart let \(X,Y\) be the two fixed
roots.  The local lemma gives:

| \(h\)-chart | exact formula for \(\delta\), outside power fibre |
|---|---|
| \(p^2\) | \(n_p+1+\epsilon_q\), for \(n_p\le2\) |
| \(pq\) | \(n_p+n_q\) |
| \(p(p+q)\) | \(n_p+\min(n_L,2)+\epsilon_q\) |
| \(XY\), \(X\ne Y\) | \(\min(n_X,2)+\min(n_Y,2)+\epsilon_p+\epsilon_q\) |
| \(L^2\), \(L\) nonbranch | \(\min(n_L+1,4)+\epsilon_p+\epsilon_q\) |

Because \(\deg R=3\), exact \(\delta=3\) on a squarefree interior chart has
only
\[
(f,e)=(3,0),(2,1),(1,2),                             \tag{7}
\]
where \(f\) is the total fixed-root contribution and \(e\) the number of
bare-branch contacts.  Exact \(\delta=4\) has only
\[
(f,e)=(3,1),(2,2).                                   \tag{8}
\]
The impossible alternative \(f=4\) would require degree at least four in
\(R\).  Equations (7)--(8), together with the five chart formulas in the
table, prove that the lists below have no missing mechanism.

## 4. The 19 exact-\(\delta=3\), \(\{2,1\}\) families

### 4.1 Branch square: four orbits

The residual diagonal torus makes every nonzero coefficient ratio
equivalent over \(\mathbb C\), but it cannot change a zero into a nonzero
coefficient.

| ID | \(h\) | representative \(R\) | incidence |
|---|---|---|---|
| `D3-BS-N2-Z` | \(p^2\) | \(p^2q\) | \(n_p=2\), zero \(p^3\)-tail |
| `D3-BS-N2-NZ` | \(p^2\) | \(p^2(p+q)\) | \(n_p=2\), nonzero tail |
| `D3-BS-N1-BR2` | \(p^2\) | \(pq^2\) | \(n_p=1\), doubled other branch |
| `D3-BS-N1-CONTACT` | \(p^2\) | \(p(p^2+q^2)\) | \(n_p=1\), transverse contact at \(q=0\) |

The missing boundary \(R=p^3\) is the dependent power fibre.

### 4.2 Two branch roots: two orbits

Here \(\delta=n_p+n_q\), so all three roots of \(R\) must be supported at
the branches.  The swap gives:

| ID | \(h\) | representative \(R\) |
|---|---|---|
| `D3-BB-30` | \(pq\) | \(p^3\) |
| `D3-BB-21` | \(pq\) | \(p^2q\) |

### 4.3 One branch root: six orbits

The effective stabilizer of \(p(p+q)\) is trivial.  The bare branch is
\(q=0\), whose contact equation is
\[
3a-4b=0.                                             \tag{9}
\]
The six distinct orbits are:

| ID | representative \(R\) | mechanism |
|---|---|---|
| `D3-OB-300` | \(p^3\) | \(n_p=3\) |
| `D3-OB-210` | \(p^2(p+q)\) | \((n_p,n_L)=(2,1)\) |
| `D3-OB-120` | \(p(p+q)^2\) | \((n_p,n_L)=(1,2)\) |
| `D3-OB-20C` | \(p^2(4p+3q)\) | \(n_p=2\) plus (9) |
| `D3-OB-11C` | \(p(p+q)(q-4p)\) | \((1,1)\) plus (9) |
| `D3-OB-02C` | \((p+q)^2(5q-4p)\) | \(n_L=2\) plus (9) |

No one-branch configuration reaches \(\delta=4\): the three fixed degrees
already determine the displayed forms, and none acquires the additional
bare-branch contribution.

### 4.4 Squarefree no-branch chart: four parameterized families

Use the root cover
\[
X=p-rq,\qquad Y=p-r^{-1}q,\qquad
h=XY,\qquad z=r^2,
\]
\[
\kappa=(r+r^{-1})^2=z+2+z^{-1}.                     \tag{10}
\]
On the root cover, a branch sign gives \(r\mapsto-r\), while the branch
swap exchanges \(X,Y\) and the two branch points.  Thus an incidence type
which forgets their **relative** orientation descends by
\(z\leftrightarrow z^{-1}\) to the \(\kappa\)-line.  The type with one
chosen doubled fixed root and one chosen contacted branch remembers that
relative orientation: it descends only by \(r\mapsto-r\), so its actual
modulus is \(z\), not \(\kappa\).
The branch contact equations for
\(R=ap^3+bp^2q+cpq^2+dq^3\) are
\[
C_p=4c-3\eta d,\qquad C_q=3\eta a-4b,
\qquad \eta=-(r+r^{-1}).                             \tag{11}
\]

| ID | normal form | exact guard and modulus |
|---|---|---|
| `D3-SF-21` | \(R=X^2Y\) | modulus \(\kappa\); \(\kappa\ne4,-16/5\) |
| `D3-SF-20C` | \(R=X^2((5-3z)p+4rq)\) | actual modulus \(z\in\mathbb C^\times\); \(z\ne1,-5\), \(5z^2-6z+5\ne0\) |
| `D3-SF-11C` | \(R=h((z+1)p+4rq)\) | modulus \(\kappa\); \(\kappa\ne4,-16/5,16\) |
| `D3-SF-10CC` | \(R=X(Ap^2+Bpq+Cq^2)\) | modulus \(\kappa\); \((z-3)A=4rB,\ (1-3z)C=4rB\); \(\kappa\ne4,16/5,16\) |

`D3-SF-20C` is the stabilizer subtlety.  The map
\[
z\longmapsto\kappa=z+2+z^{-1}
\]
has two inequivalent values \(z,z^{-1}\) over generic \(\kappa\), but they
belong to one \(z\)-parameter stratum.  At \(z=-1\)
(\(\kappa=0\)) the extra sign stabilizer identifies the two sheets.  Freezing
two separate strata would double-count that orbit.

The values \(z=3\) and \(z=1/3\) lie over
\(\kappa=16/3\).  At \(z=3\), the residual linear factor in
`D3-SF-20C` becomes \(X\), and in `D3-SF-10CC` the unique solution has
\([A:B:C]=[1:0:0]\).  These are retained boundary charts, not deleted
denominators.

### 4.5 Doubled nonbranch chart: three parameterized families

Put \(L=p+q\).  The residual involution swaps \(p,q\).

| ID | normal form | exact projective guard |
|---|---|---|
| `D3-DN-2` | \(R=L^2(up+vq)\) | \([u:v]/(u\leftrightarrow v)\), \((u-v)(2u+v)(u+2v)\ne0\) |
| `D3-DN-1C` | \(R=L(Ap^2+Bpq+2Bq^2)\) | contact-at-\(p\) chart \([A:B]\), \((A+B)(A-2B)\ne0\); the swap supplies the \(q\)-chart |
| `D3-DN-0CC` | \(R=ap^3+\frac32ap^2q+\frac32dpq^2+dq^3\) | \([a:d]/(a\leftrightarrow d)\), \(a\ne d\) |

This completes the count
\[
4+2+6+4+3=\boxed{19}.                                \tag{12}
\]

## 5. The six exact-\(\delta=4\), \(\{2,2\}\) families

All are isolated orbits.

### 5.1 Three squarefree special-modulus orbits

| ID | condition and representative | common-factor mechanism |
|---|---|---|
| `D4-SF-21C` | \(z=-5\), \(\kappa=-16/5\), \(R=X^2Y\) | fixed pattern \((2,1)\) plus one branch contact |
| `D4-SF-20CC` | \(5z^2-6z+5=0\), \(\kappa=16/5\), \(R=X^2((5-3z)p+4rq)\) | one doubled fixed root plus two branch contacts |
| `D4-SF-11CC` | \(\kappa=16\), \(R=h((z+1)p+4rq)\) | two simple fixed roots plus two branch contacts |

For `D4-SF-20CC`, the two reciprocal roots of
\(5z^2-6z+5\) become one orbit because both branch contacts are present.
For `D4-SF-21C`, the reciprocal presentation uses the other branch and is
again the same orbit.

### 5.2 Three doubled-nonbranch orbits

| ID | \(h\) | representative \(R\) |
|---|---|---|
| `D4-DN-3` | \(L^2\) | \(L^3\) |
| `D4-DN-2C` | \(L^2\) | \(L^2(p-2q)\) |
| `D4-DN-1CC` | \(L^2\) | \(L(2p^2+pq+2q^2)\) |

Their gcd factors have the visible forms
\[
L^4,\qquad L^3p\ \text{(up to swap)},\qquad L^2pq,
\]
so their degrees are exactly four.

## 6. The power fibre

If \(\alpha,\beta\) are constant-linearly dependent, then for some
\((\lambda,\mu)\ne(0,0)\),
\[
J(\lambda P+\mu Q,R)=0.
\]
Since the degrees are coprime,
\[
\lambda P+\mu Q=M^4,\qquad R=M^3.                   \tag{13}
\]
But
\[
\lambda P+\mu Q=h(\lambda p^2+\mu q^2).
\]
Unique factorization makes both quadratic factors proportional to \(M^2\).
A square with no \(pq\) term has \(M=p\) or \(M=q\).  Up to the branch
swap, the only orbit is therefore
\[
\boxed{\texttt{PF-BRANCH-FOURTH-THIRD}:\quad
h=p^2,\qquad R=p^3.}                                 \tag{14}
\]
It has \(\deg\gcd(\alpha,\beta,\gamma)=5\), which is why applying the
independent Hilbert--Burch table to it would be erroneous.

## 7. Boundary atlas

Every removed divisor has a declared destination.

| source | boundary | destination |
|---|---|---|
| `D3-BS-N2-*` | coefficient of \(q\) in the residual linear form vanishes | power fibre (14) |
| squarefree chart | \(\kappa=4\) | recompute in `D3-DN-*` or `D4-DN-*` |
| `D3-SF-21` / `D3-SF-11C` | \(\kappa=-16/5\) | `D4-SF-21C` |
| `D3-SF-20C` | \(z=-5\) | `D4-SF-21C` |
| `D3-SF-20C` | \(5z^2-6z+5=0\) | `D4-SF-20CC` |
| `D3-SF-10CC` | \(\kappa=16/5\) | `D4-SF-20CC` |
| `D3-SF-11C` / `D3-SF-10CC` | \(\kappa=16\) | `D4-SF-11CC` |
| `D3-SF-20C` | \(z=-1\), \(\kappa=0\) | retained stabilizer-jump point of the same \(z\)-family |
| squarefree charts | \(\kappa=16/3\) | retained alternate coordinate charts; \(\delta\) does not jump |
| `D3-SF-21` | \(\kappa=\infty\) | `D3-BB-21` |
| `D3-SF-20C` | \(z\to0\) / \(z\to\infty\) | `D3-BB-30` / `D3-BB-21` |
| `D3-SF-11C`, `D3-SF-10CC` | \(\kappa=\infty\) | `D3-BB-21` |
| `D3-DN-2` | \(u=v\) | `D4-DN-3` |
| `D3-DN-2` | \(2u+v=0\) or \(u+2v=0\) | `D4-DN-2C` |
| `D3-DN-1C` | \(A=-B\) | `D4-DN-2C` |
| `D3-DN-1C` | \(A=2B\) | `D4-DN-1CC` |
| `D3-DN-0CC` | \(a=d\) | `D4-DN-1CC` |

The exact special-value identities are
\[
\begin{aligned}
\kappa=4&\iff(z-1)^2=0,\\
\kappa=0&\iff(z+1)^2=0,\\
\kappa=-16/5&\iff5z^2+26z+5=0,\\
\kappa=16/5&\iff5z^2-6z+5=0,\\
\kappa=16/3&\iff(3z-1)(z-3)=0,\\
\kappa=16&\iff z^2-14z+1=0.
\end{aligned}                                       \tag{15}
\]
Thus no affine denominator loses the reciprocal sheet or the points
\(\kappa=0,4,16/3\).

The orbit-closure pivots which do not change the coarse stratum are also
retained: the nonzero-tail branch-square orbit limits to its zero-tail
partner; the branch-square transverse-contact orbit limits to the doubled
other-branch orbit; \(z=-1\) is the ramification/stabilizer point of
`D3-SF-20C`; \(z=3\) gives \(R=X^3\) inside that same family; and
\([u:v]=[1:-1]\), \([a:d]=[1:-1]\) are the retained projective-swap fixed
points of `D3-DN-2`, `D3-DN-0CC`.  The complete machine-readable list of
guards, quotients, retained pivots, and exit arrows is
`DENOMINATOR.json`.

## 8. Why no case is missing

The proof is a finite ordered route:

1. \(R=0\) and nonbinary \(h\) were removed before this audit by the coarse
   readiness denominator.
2. If \(\alpha,\beta\) are dependent, (13)--(14) give the unique power
   orbit.
3. Otherwise \(\delta\le4\), because the Hilbert--Burch deficits satisfy
   \(0\le k_i\le2\) and \(k_1+k_2=\delta\).
4. The support of \(g\) is contained in the two roots of \(h\) and the two
   branch points, by \(\gamma=8h^2pq\).
5. Equations (4)--(6) determine every local multiplicity.
6. The five fixed-divisor chart formulas exhaust the four \(h\)-orbits and
   the \(\kappa=4\) boundary.
7. Degree three for \(R\) leaves only the mechanisms (7)--(8), which
   produce exactly the 19 and six rows listed above.
8. The residual stabilizers were quotient out explicitly; the only
   nontrivial orbit-cover issue is the retained \(z\)-modulus in
   `D3-SF-20C`.

This also independently confirms the coarse readiness statement:
\[
\delta=3\Longleftrightarrow\{k_1,k_2\}=\{2,1\},\qquad
\delta=4\Longleftrightarrow\{k_1,k_2\}=\{2,2\}.
\]
No freeze failure was found.

## 9. Exact replay

Run

```sh
./verify_strict.sh
```

The dependency-free checker uses exact rational arithmetic, three exact
number fields for the algebraic special moduli, and exhaustive finite-field
regressions.  It verifies:

- all isolated representatives in Sections 4--6;
- generic representatives of every parameterized family;
- exact \(\delta=4\) at
  \(\kappa=-16/5,16/5,16\);
- the 19/6/1 ledger and every special-value equation (15);
- exhaustive projective cubic counts on all four boundary \(h\)-charts;
- five generic squarefree swap-orbits;
- the collapse to four orbits at the \(\kappa=0\) stabilizer jump; and
- the \(4+2\) raw split at a finite-field \(\kappa=-16/5\) fibre.

Its terminal output is

```text
DELTA_GE3_DENOMINATOR_EXACT_PASS_19_6_1
exact delta=3: 19 incidence families
exact delta=4: 6 incidence families
dependent power fibre: 1 orbit
total refined denominator: 26 disjoint parameterized families
DELTA_GE3_DENOMINATOR_STRICT_PASS_26
```

This is an exact denominator audit, not a lower-equation exclusion and not
peer review.
