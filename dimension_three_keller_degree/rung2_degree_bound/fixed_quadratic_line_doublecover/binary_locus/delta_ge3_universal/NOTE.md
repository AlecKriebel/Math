# Universal binary \(\delta\geq3\) incidence atlas

**Frozen denominator:** 17 exact-\(\delta=3\) normal-form families, 6
exact-\(\delta=4\) normal-form families, and 1 nonzero dependent power
fibre.  The machine-readable version is `denominator.json`.

**Scope.**  This note concerns only the binary top row
\[
H_4=h(p,q)(p^2,q^2,0),\qquad R=(H_3)_3\in\mathbb C[p,q]_3.
\]
It is a complete incidence classification for
\(\deg\gcd(\alpha,\beta,\gamma)\geq3\) inside that row.  It does **not**
exclude any listed family, assert that a listed family extends to a Keller
map, or give a degree bound for Keller counterexamples.

**Status.**  This work is not peer reviewed.  The exact computer checks
are evidence about the encoded algebra, not peer review.

## 1. Statement

Put
\[
P=hp^2,\qquad Q=hq^2,\qquad
\alpha=J(Q,R),\quad\beta=-J(P,R),\quad
\gamma=J(P,Q)=8h^2pq,
\]
and
\[
g=\gcd(\alpha,\beta,\gamma),\qquad\delta=\deg g.
\]
All gcds are homogeneous gcds, up to a nonzero scalar.

### Theorem

Assume \(h\ne0\) and \(R\ne0\).

1. If \(\alpha,\beta\) are constant-linearly independent and
   \(\delta\geq3\), then \(\delta\in\{3,4\}\).  The Hilbert--Burch shape is
   respectively
   \[
   \{k_1,k_2\}=\{2,1\}\quad\text{or}\quad\{2,2\}.
   \]
2. Modulo the stabilizer of the squaring cover
   \([p:q]\mapsto[p^2:q^2]\), every such point belongs to one of the 17
   exact-\(\delta=3\) or 6 exact-\(\delta=4\) families in Tables 1 and 2
   below.  The fixed-divisor charts and all parameter rank-drop loci are
   exhausted.
3. If \(\alpha,\beta\) are constant-linearly dependent, there is one
   nonzero orbit:
   \[
   h=p^2,\qquad R=p^3,
   \]
   up to the same stabilizer and nonzero scalars.  This is the power fibre
   `PF-BS`; it is not counted as an exact-\(\delta=4\) family.  Its
   homogeneous gcd is \(p^4q\), of degree five.  The specialization
   \(R=0\) is the separate lower row `L00`.

The word *family* has a fixed convention here: it means one displayed
stable normal-form incidence family, modulo the stated stabilizer, with
its exact-open parameter locus retained as a whole.  Exact-\(\delta\)
parameter endpoints and stabilizer jumps do not receive extra family
identifiers.  Boundary specializations are retained as arrows to an
already counted target, not added again to the denominator.

## 2. Frozen fixed-divisor charts

The roots of the binary quadratic \(h\), counted with multiplicity, have
five possible positions relative to the two branch points \(p=0,q=0\).
After normalization:
\[
\begin{array}{c|c|c}
\text{code}&h&\text{factor caps in }\gamma/8\\ \hline
\mathrm{BS}&p^2&p^5q\\
\mathrm{TB}&pq&p^3q^3\\
\mathrm{OB}&p(p+q)&p^3q(p+q)^2\\
\mathrm{DN}&(p+q)^2&pq(p+q)^4\\
\mathrm{SF}&L_sM_s&pqL_s^2M_s^2
\end{array}
\]
where
\[
L_s=p-sq,\qquad M_s=sp-q,\qquad
s\ne0,\quad s^2\ne1,
\]
and
\[
s\sim\pm s^{\pm1},\qquad
\kappa=(s+s^{-1})^2.
\]
Thus the five charts are, respectively: a doubled branch root, the two
branch roots, one branch and one nonbranch root, a doubled nonbranch root,
and two distinct nonbranch roots.  This is an exhaustive multiset
classification and is independent of the later gcd exclusions.

## 3. Exact-\(\delta=3\) atlas

In the OB and DN rows below, \(L=p+q\).  In the SF rows,
\(L=L_s\) and \(M=M_s\).

### Table 1. The 17 exact-\(\delta=3\) families

| ID | \(h\) and \(R\) | exact open | \(g\) |
|---|---|---|---|
| D3-BS-P3 | \(h=p^2,\ R=p^2(Ap+Bq)\) | \(B\ne0\) | \(p^3\) |
| D3-BS-P2Q | \(h=p^2,\ R=p(Ap^2+Cq^2)\) | \(C\ne0\) | \(p^2q\) |
| D3-TB-P3 | \(h=pq,\ R=p^3\) | up to \(p\leftrightarrow q\) | \(p^3\) |
| D3-TB-P2Q | \(h=pq,\ R=p^2q\) | up to \(p\leftrightarrow q\) | \(p^2q\) |
| D3-OB-P3 | \(h=pL,\ R=p^3\) | isolated | \(p^3\) |
| D3-OB-P2L | \(h=pL,\ R=p^2L\) | isolated | \(p^2L\) |
| D3-OB-PL2 | \(h=pL,\ R=pL^2\) | isolated | \(pL^2\) |
| D3-OB-P2Q | \(h=pL,\ R=p^2(4p+3q)\) | isolated | \(p^2q\) |
| D3-OB-PQL | \(h=pL,\ R=pL(4p-q)\) | isolated | \(pqL\) |
| D3-OB-QL2 | \(h=pL,\ R=L^2(4p-5q)\) | isolated | \(qL^2\) |
| D3-DN-L3 | \(h=L^2,\ R=L^2(Ap+Bq)\) | \(A-B\ne0\), modulo swap | \(L^3\) |
| D3-DN-PL2 | \(h=L^2,\ R=L(Ap^2+\tfrac C2pq+Cq^2)\) | \((2A+C)(A-C)\ne0\), \(p\)-contact representative | \(pL^2\) |
| D3-DN-PQL | \(h=L^2,\ R=A(2p^3+3p^2q)+B(3pq^2+2q^3)\) | \(A-B\ne0\), modulo swap | \(pqL\) |
| D3-SF-21 | \(h=LM,\ R=L^2M\) | \(\kappa\ne-16/5\) | \(L^2M\) |
| D3-SF-2C | \(h=LM,\ R=L^2((3s^2-5)p-4sq)\) | \(\kappa\notin\{-16/5,16/5\}\) | \(pL^2\) |
| D3-SF-11C | \(h=LM,\ R=LM(4sp+(s^2+1)q)\) | \(\kappa\notin\{-16/5,16\}\) | \(qLM\) |
| D3-SF-1C2 | \(h=LM,\ R=M\{4p^2s^3-12p^2s-3pqs^4+10pqs^2-3pq-12q^2s^3+4q^2s\}\) | \(\kappa\notin\{16/5,16\}\) | \(pqM\) |

Every SF row also has the ambient chart conditions \(s\ne0\) and
\(s^2\ne1\), and is taken modulo the displayed cover symmetries.

## 4. Exact-\(\delta=4\) atlas

### Table 2. The 6 exact-\(\delta=4\) families

| ID | \(h\) and \(R\) | exact condition | \(g\) |
|---|---|---|---|
| D4-DN-L4 | \(h=L^2,\ R=L^3\) | isolated | \(L^4\) |
| D4-DN-PL3 | \(h=L^2,\ R=L^2(p-2q)\) | up to swap | \(pL^3\) |
| D4-DN-PQL2 | \(h=L^2,\ R=L(2p^2+pq+2q^2)\) | isolated | \(pqL^2\) |
| D4-SF-21C | \(h=LM,\ R=L^2M\) | \(s^2+5=0\), \(\kappa=-16/5\) | \(pL^2M\) |
| D4-SF-2C2 | \(h=LM,\ R=L^2((3s^2-5)p-4sq)\) | \(5s^4-6s^2+5=0\), \(\kappa=16/5\) | \(pqL^2\) |
| D4-SF-11C2 | \(h=LM,\ R=LM(p+q)\) | \(s^2-4s+1=0\), \(\kappa=16\) | \(pqLM\) |

For the last row, the sign-conjugate equation
\(s^2+4s+1=0\) is in the same stabilizer orbit.

## 5. Completeness and saturation

### 5.1 Hilbert--Burch bound

Suppose \(\alpha,\beta\) are constant-linearly independent.  After
dividing by \(g\), the three generator degrees are
\[
(d,d,d+1),\qquad d=5-\delta.
\]
The reduced ideal has height two: gcd one excludes a height-one prime,
and constant independence excludes the degree-zero degeneracy.  If
\(e_1,e_2\) are the two minimal syzygy degrees, Hilbert--Burch gives
\[
e_1+e_2=3d+1.
\]
The two gradient columns of \((P,Q,R)\) are independent syzygies of
degree \(d+3\).  Writing them in a minimal syzygy basis gives a
\(2\times2\) coefficient matrix \(C\).  Its determinant is a nonzero
scalar multiple of \(g\), because the wedge of the gradient columns is
\((\alpha,\beta,\gamma)\), while the wedge of a minimal basis is the
reduced row.  Therefore, with \(k_i=d+3-e_i\),
\[
0\le k_i\le2,\qquad k_1+k_2=\deg g=\delta.
\]
It follows that \(\delta\le4\), and for \(\delta=3,4\) the shapes are
uniquely \(\{2,1\}\) and \(\{2,2\}\).

### 5.2 Finite linear enumeration

Since \(g\mid\gamma=8h^2pq\), every candidate gcd is an exponent tuple
bounded by the caps in Section 2.  For a finite root \(p-rq\),
\[
(p-rq)^e\mid f
\quad\Longleftrightarrow\quad
\left.\partial_p^jf\right|_{p=rq}=0
\quad(0\le j<e).
\]
For the root \(q=0\), use
\(\left.\partial_q^jf\right|_{q=0}=0\).
Applied to \(\alpha\) and \(\beta\), these are homogeneous linear
equations in the four coefficients
\[
R=ap^3+bp^2q+cpq^2+dq^3.
\]
Solving every capped exponent tuple of total degree three or four gives:
\[
\begin{array}{c|c|c|c|c}
\text{chart}&\delta=3\text{ raw signatures}
 &\text{orbits}&\delta=4\text{ generic raw signatures}
 &\text{orbits}\\ \hline
\mathrm{BS}&2&2&0&0\\
\mathrm{TB}&4&2&0&0\\
\mathrm{OB}&6&6&0&0\\
\mathrm{DN}&4&3&4&3\\
\mathrm{SF}&10&4&0&0
\end{array}
\]
The corresponding nonzero kernels, after stabilizer normalization, are
exactly the 17 forms in Table 1 and the three DN forms in Table 2.
For reference, the raw signatures in factor order are:
\[
\begin{aligned}
\mathrm{BS},\delta=3:\;&(3,0),(2,1);\\
\mathrm{TB},\delta=3:\;&(3,0),(2,1),(1,2),(0,3);\\
\mathrm{OB},\delta=3:\;&(3,0,0),(2,1,0),(2,0,1),
 (1,1,1),(1,0,2),(0,1,2);\\
\mathrm{DN},\delta=3:\;&(0,0,3),(1,0,2),(0,1,2),(1,1,1);\\
\mathrm{DN},\delta=4:\;&(0,0,4),(1,0,3),(0,1,3),(1,1,2);\\
\mathrm{SF},\delta=3:\;&(0,0,2,1),(0,0,1,2),
 (1,0,2,0),(1,0,0,2),\\
& (0,1,2,0),(0,1,0,2),(1,0,1,1),(0,1,1,1),\\
& (1,1,1,0),(1,1,0,1).
\end{aligned}
\]
Here the factor orders are the orders displayed in Section 2.

For each kernel, the actual valuations of all three forms are recomputed.
Removing the equations for an additional factor gives precisely the
exact-open conditions in the tables.  Thus a requested lower divisor is
never mistaken for the true gcd.

### 5.3 Squarefree rank-drop loci

The only remaining possibility is that a squarefree degree-four
divisibility system acquires a kernel at a special value of \(s\).  Up to
the cover stabilizer, there are four exponent patterns.  The gcds of all
nonzero maximal-minor numerators of their exact linear systems are:
\[
\begin{array}{c|l}
\text{signature in }(p,q,L,M)&\text{maximal-minor gcd}\\ \hline
(0,0,2,2)&9(s-1)^8(s+1)^8\\
(1,0,2,1)&9(s-1)^5(s+1)^5(s^2+5)\\
(1,1,2,0)&9s^2(s-1)^2(s+1)^2(5s^4-6s^2+5)\\
(1,1,1,1)&9(s-1)^3(s+1)^3
(s^2-4s+1)(s^2+4s+1).
\end{array}
\]
The factors \(s=0\) and \(s^2=1\) are fixed-divisor chart boundaries.
After saturation by \(s(s^2-1)\), the first pattern has no interior
rank drop, and the remaining three factors give exactly the three SF
families in Table 2.  Their moduli follow by dividing by the appropriate
power of \(s\):
\[
s^2+5=0\Rightarrow\kappa=-16/5,\quad
5s^4-6s^2+5=0\Rightarrow\kappa=16/5,
\]
and
\[
s^2\mp4s+1=0\Rightarrow\kappa=16.
\]
This is also the certificate that clearing the \(1/s\) root coordinate
introduced no extra interior branch.

### 5.4 Dependent power fibre

If \(\alpha,\beta\) are dependent, a nonzero linear combination gives
\[
J(\lambda P+\mu Q,R)=0.
\]
For nonzero homogeneous forms of degrees four and three, Euler's
identities and unique factorization imply
\[
\lambda P+\mu Q=c\ell^4,\qquad R=c'\ell^3.
\]
Indeed, \((\lambda P+\mu Q)^3/R^4\) has both partial derivatives zero,
and \(\gcd(3,4)=1\).

Now
\[
\lambda P+\mu Q=h(\lambda p^2+\mu q^2).
\]
The second quadratic can be a square only when one of
\(\lambda,\mu\) vanishes; otherwise it has two distinct roots.  Hence,
up to swapping \(p,q\), \(h=p^2\) and \(R=p^3\).  Directly,
\[
\alpha=-6p^4q,\qquad\beta=0,\qquad\gamma=8p^5q,
\]
so the gcd is \(p^4q\).  This proves uniqueness and explains why the
power fibre is outside the independent \(\delta\le4\) table.

## 6. Specialization arrows and counting convention

The following are arrows, not additional denominator families.

- `D3-BS-P3` and `D3-BS-P2Q` go to `PF-BS` at \(B=0\) and \(C=0\),
  respectively; `PF-BS` goes to `L00` at \(R=0\).
- `D3-DN-L3` goes to `D4-DN-L4` at \(A=B\).
- `D3-DN-PL2` goes to `D4-DN-PL3` at \(2A+C=0\), and to
  `D4-DN-PQL2` at \(A=C\).
- `D3-DN-PQL` goes to `D4-DN-PQL2` at \(A=B\).
- At \(\kappa=-16/5\), the SF families `D3-SF-21`,
  `D3-SF-2C`, and `D3-SF-11C` route to `D4-SF-21C` whenever that
  value is excluded in Table 1.
- At \(\kappa=16/5\), `D3-SF-2C` and `D3-SF-1C2` route to
  `D4-SF-2C2`.
- At \(\kappa=16\), `D3-SF-11C` and `D3-SF-1C2` route to
  `D4-SF-11C2`.
- At \(s^2=1\) (\(\kappa=4\)), the four SF rows route, in table order,
  to `D4-DN-L4`, `D4-DN-PL3`, `D4-DN-PL3`, and
  `D4-DN-PQL2`, after fixed-divisor renormalization.
- At \(s=0\) or \(s=\infty\), `D3-SF-21`, `D3-SF-11C`, and
  `D3-SF-1C2` route to the displayed two-branch mixed monomial orbit;
  `D3-SF-2C` routes to `D3-TB-P3` at \(s=0\) and
  `D3-TB-P2Q` at \(s=\infty\).

For avoidance of doubt, the following exact-\(\delta=3\) special points
remain inside their original family and are not counted separately:

- \(A=0\) in each BS parameter family;
- \(AB=0\) and the swap-fixed point \(A+B=0\) in `D3-DN-L3` and
  `D3-DN-PQL`, subject to \(A-B\ne0\);
- \(AC=0\) in `D3-DN-PL2`, subject to its displayed exact-open
  conditions;
- \(\kappa=0\), equivalently \(s^2=-1\), in each SF
  exact-\(\delta=3\) family.  This is an interior stabilizer jump under
  \(s\mapsto\pm s^{\pm1}\), not a new incidence family.

If a later calculation finds a point not covered by these families or
arrows, it is a denominator failure: this list must be replaced and
re-certified, not silently enlarged.

## 7. Exact verification

Run
```bash
PYTHON_BIN=/path/to/python-with-sympy ./verify_all_strict.sh
```
from this directory.

The release certificate `verify_incidence_sympy.py`:

- enumerates every degree-three and degree-four divisor of \(\gamma\);
- solves the exact linear divisibility systems;
- recomputes true valuations, rather than trusting requested divisors;
- computes the four saturated squarefree rank-drop factors;
- verifies every pinned normal form, modulus, and boundary arrow.

The independent `verify_incidence_pari.gp` does not repeat that
enumeration or maximal-minor algorithm.  It forms the Jacobians directly
and computes the exact gcd in both affine charts of \(\mathbb P^1\) for
a representative of every one of the 24 nonzero families, including the
three exact number fields for the interior degree-four orbits.  Checking
both charts prevents a residual factor at infinity from being discarded.

`verify_manifest.py` freezes all identifiers, counts, chart counts,
boundary targets, and the convention for retained parameter
specializations.  The strict wrapper rejects optimized Python, proves
the manifest audit is live with an injected fault, and rejects a PARI
transcript containing any error even though GP may otherwise continue
after an error.

## 8. AI-assistance disclosure

This classification, note, manifest, and verification code were produced
with substantial assistance from an AI system.  The algebra was encoded
for exact symbolic checking in SymPy and independently replayed on pinned
representatives in PARI/GP.  No claim of novelty or priority is made in
this note.  Human mathematical review is still required before citation
or publication.
