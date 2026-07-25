# Hostile coverage audit of the triple-vertical frontier

**Verdict:** **PASS**, conditional exactly on entry into the primitive
fixed-linear cubic-pencil frontier
\[
H_4=(hp,hq,0)^T,
\]
with \((p,q)\) a coprime minimal cubic pencil and \(p\) its unique
vertical member.

**Completed (UTC):** 2026-07-25T22:26:29Z.

Every point of this normalized frontier reaches exactly one terminal
route below.  All terminal exclusions have now passed separate hostile
audits.  In particular, the last formerly provisional terminal
\[
a=0,\qquad W_0\ne0
\]
passed at `../audit_a0_w0_nonzero/REPORT.md`, with strict sentinel
`A0_W0_NONZERO_INDEPENDENT_STRICT_PASS_94A60D`.

There is no missing **internal** bridge between the vertical-multiplicity
split and the terminal lemmas.  This report deliberately does not use or
audit a post-freeze bridge from frozen row `Q2-E1-A3-B1-D1-N1` into the
normal form above.  Therefore it does **not** change the frozen status or
claim that the frozen row is closed.  That external bridge remains a
separate certification obligation.

This report and its exact checks are not peer review and were materially
AI-assisted.

## 1. Independent reconstruction of the top split

Put \(h=z\) and write the unique vertical member as
\[
p=z^m r,\qquad 1\le m\le3,\qquad z\nmid rq.
\]
Let
\[
P=zp,\qquad Q=zq,\qquad G=(H_3)_3.
\]
The weight-eight Keller identity is
\[
\operatorname{Jac}(P,Q,G)=0.                          \tag{1}
\]

The homogeneous first-integral descent, using minimality of the pencil,
gives for a nonzero homogeneous \(G\) of degree three
\[
\frac{G^4}{P^3}=R(q/p),\qquad R\in\mathbb C(t).        \tag{2}
\]
Let \(s=\operatorname{ord}_\infty R\).  If \(f\mid p\) has
multiplicity \(b\), valuation of (2) gives
\[
4v_f(G)-3\bigl(b+\mathbf1_{f=z}\bigr)=bs.             \tag{3}
\]

### \(m=1\)

At \(z\), equation (3) gives \(s\equiv2\pmod4\).  Every prime factor of
the quadratic \(r\) has multiplicity \(b=1\) or \(2\), while its equation
requires
\[
b(3+s)\equiv0\pmod4.
\]
Since \(3+s\equiv1\pmod4\), neither multiplicity works.  Thus \(G=0\).

### \(m=2\)

At \(z\),
\[
4v_z(G)=9+2s,
\]
whose two sides have opposite parity.  Again \(G=0\).

### \(m=3\)

Now
\[
4v_z(G)=12+3s.
\]
Because \(0\le v_z(G)\le3\), integrality leaves exactly
\[
(v_z(G),s)=(3,0)\quad\text{or}\quad(0,-4).            \tag{4}
\]
The first case gives \(G\in\mathbb Cz^3\).

In the second case, \(R\) has no finite pole: a pole at \(\lambda\)
would give a negative valuation along a component of
\(q-\lambda z^3\), while the left side of (2) is nonnegative there.
Hence \(R\) is a degree-four polynomial.  If a finite root of \(R\) had
multiplicity \(n<4\), every component of the corresponding cubic fibre,
of multiplicity \(b\in\{1,2,3\}\), would have to satisfy
\[
4\mid nb.
\]
For \(n=1,3\) this is impossible; for \(n=2\), all component
multiplicities would be even, incompatible with total degree three.
Therefore \(R\) has one root of multiplicity four, and \(G\) is the
corresponding cubic pencil member.  Consequently
\[
\boxed{G\in\langle z^3,q\rangle}.                     \tag{5}
\]

This independently confirms the exact top routing:
\[
\begin{array}{c|c}
m=1,2&G=0\\
m=3&G=0,\quad G\sim z^3,\quad\text{or}\quad G\sim q.
\end{array}                                           \tag{6}
\]

If \(G=0\), the third component of the full map has degree at most two.
The hostile-audited quadratic-component exit in
`../../../WORKING_QUADRATIC_COMPONENT_EXIT.md` makes the Keller map an
automorphism.

For nonzero \(G=\alpha z^3+\beta q\), the cases \(\beta=0\) and
\(\beta\ne0\) are disjoint.  In the latter case, replace the second
pencil generator by \(G\); the pencil, coprimality, and minimality are
unchanged.  This gives exactly the vertical companion \(G=z^3\) and
nonvertical companion \(G=q\).  The uniqueness of the vertical member
prevents these two cases from merging.

The supplied top-level SymPy and PARI/GP replays independently confirm
the seven marked-member kernels, both \(E_7\) identities, and the two
triple-vertical companion survivors through \(E_6\).

## 2. Complete \(E_7\) families

For the vertical companion \(G=z^3\),
\[
E_7=z^3\{q,4zW-3U\}_{x,y}=0
\]
has the complete solution
\[
U=\frac43zW+a q+bz^3.                                \tag{7}
\]
Legal target shears kill \(b\), the \(z^3\)-coefficient of \(V\), and,
when convenient, the \(z^3\)-coefficient of \(q\).  Their action on
\(A,B,L\) is an invertible renaming of unrestricted lower jets.  The
invariant split is exactly
\[
a=0\quad\text{or}\quad a\ne0.                        \tag{8}
\]

For the nonvertical companion \(G=q\), the complete first-integral solve
gives, after legal shears,
\[
U=dz^3,\qquad V=zW+fz^3.                              \tag{9}
\]
The independent nonvertical audit reconstructed this solution from the
degree-six first-integral space
\(\langle z^6,z^3q,q^2\rangle\); no extra \(E_7\) family is missing.

## 3. Root and minimality atlas

Because \(z\nmid q\), the nonzero binary cubic
\[
q_0=q|_{z=0}
\]
has exactly the root partitions
\[
1+1+1,\qquad2+1,\qquad3,                              \tag{10}
\]
represented by \(xy(x-y),x^2y,x^3\).

On the triple-root locus, write
\[
q=x^3+z(Ax^2+Bxy+Cy^2)+z^2(Dx+Ey)+Fz^3.
\]
The parabolic stabilizer of \(z=0\) and the marked root gives the
disjoint ordered cases
\[
\begin{array}{c|c}
C\ne0&x^3+y^2z+\alpha xz^2+\beta z^3\\
C=0,\ B\ne0&x^3+xyz+\beta z^3\\
C=B=0,\ E\ne0&x^3+yz^2\\
C=B=E=0&q\in\mathbb C[x,z]_3.
\end{array}                                           \tag{11}
\]
The last row is exactly the nonminimal boundary; the first three rows
are the complete minimal triple-root atlas.  Thus every later use of
“all three charts” is exhaustive.

## 4. Disjoint terminal routing

The following table records every terminal scope and its proof and
audit.  “NT” means the squarefree or double-root strata; “TR” means all
three minimal triple-root charts.

| ID | Disjoint predicate | Terminal proof | Independent hostile audit |
|---|---|---|---|
| T0 | \(m=1,2\), or \(m=3,G=0\) | `../WORKING_VERTICAL_FIXED_LINEAR_CUBIC_PENCIL.md`; `../../../WORKING_QUADRATIC_COMPONENT_EXIT.md` | this coverage reconstruction; top SymPy/PARI replays |
| N1 | \(m=3,G=q,\ q_0\) NT | `../NONVERTICAL_NONTRIPLE_LEMMA.md` | `../audit_nonvertical_companion/REPORT.md` |
| N2 | \(m=3,G=q,\ q_0\) TR | `../NONVERTICAL_TRIPLE_ROOT_LEMMA.md` | `../audit_nonvertical_companion/REPORT.md` |
| V1 | \(G=z^3,a\ne0,\ q_0\) NT, \(\ell=0\) | `../VERTICAL_ELL_ZERO_NONTRIPLE_LEMMA.md` | `../audit_vertical_ell_zero_nontriple/REPORT.md` |
| V2 | \(G=z^3,a\ne0,\ q_0\) NT, \(\ell\ne0\) | `../VERTICAL_NONZERO_ELL_NONTRIPLE_LEMMA.md` | `../audit_vertical_nonzero_ell_nontriple/REPORT.md` |
| V3 | \(G=z^3,a\ne0,\ q_0\) TR, \(\gamma\ne0\) | `../VERTICAL_TRIPLE_GAMMA_NONZERO_EXCLUSION.md` | `../audit_vertical_triple_gamma_nonzero/REPORT.md` |
| V4 | \(G=z^3,a\ne0,\ q_0\) TR, \(\gamma=0,\ell\ne0\) | reduction in `../VERTICAL_TRIPLE_GAMMA0_REDUCTION.md`, then V5 | `../audit_vertical_triple_gamma0_reduction/REPORT.md` |
| V5 | \(G=z^3,a\ne0,\ q_0\) TR, \(\gamma=\ell=0\) | `../VERTICAL_TRIPLE_GAMMA0_ELL0_LEMMA.md` | `../audit_vertical_triple_gamma0_ell0/REPORT.md` |
| V6 | \(G=z^3,a=0,\ W_0=0\) | `../VERTICAL_A0_W0_ZERO_EXCLUSION.md` | `../audit_vertical_a0_w0_zero/REPORT.md` |
| V7 | \(G=z^3,a=0,\ W_0\ne0\) | `../a0_w0_nonzero_attack/NOTE.md` | `../audit_a0_w0_nonzero/REPORT.md` |

Here is why the table has no internal gap.

### Nonvertical companion

The partition (10) sends the two nontriple root types to N1 and the
triple root to the complete three-chart atlas N2.  The fourth line of
(11) is not in the minimal frontier.  Thus N1 and N2 cover the whole
nonvertical companion.

### Vertical companion, \(a\ne0\)

Restriction of \(E_6\) to \(z=0\) gives
\[
-a q_0\{q_0,W_0\}=0.                                  \tag{12}
\]
For nontriple \(q_0\), the binary bracket kernel in degree two is zero,
so
\[
W_0=0,\qquad W=z\ell+\omega z^2.
\]
The split \(\ell=0\) versus \(\ell\ne0\) is exhaustive.  V2 includes
the generic position and every collision: the squarefree cubic has
three root lines, while the double-root cubic has its double and simple
root lines.  The collision kernels were solved separately, so no
generic-rank argument crosses them.

For triple-root \(q_0=L^3\), (12) gives
\[
W_0=\gamma L^2.
\]
If \(\gamma\ne0\), V3 applies for arbitrary lower linear form \(\ell\).
If \(\gamma=0\), the raw \(E_6\) identities force \(\ell=0\) on each
chart; V5 then applies.  For the disjoint certificate, points initially
with \(\ell\ne0\) route through V4, while points with \(\ell=0\) route
directly to V5.

### Vertical companion, \(a=0\)

This branch is independent of (12).  The split
\[
W_0=0\quad\text{or}\quad W_0\ne0
\]
is exhaustive.  V6 retains all five \(q\)-charts.

For V7, every nonzero binary quadratic has rank two or one.  After
normalizing it to \(xy\) or \(x^2\), the root-incidence possibilities
are exactly
\[
\begin{array}{c|ccc}
W_0& q_0\text{ squarefree}&q_0\text{ double}&q_0\text{ triple}\\ \hline
xy&0,1,2\text{ common roots}&
0,\text{ double},\text{ simple},\text{ both}&
0,\text{ triple}\\
x^2&\operatorname{ord}_xq_0=0,1&
0,1,2&
0,3.
\end{array}                                           \tag{13}
\]
The hostile audit of V7 starts before these binary specializations.  It
shows \(E_6=0\) forces
\[
q_0=\kappa L^3,\qquad W_0=\gamma L^2
\]
and then forces every \(y\)-bearing lower coefficient of \(q\) to
vanish:
\[
q\in\operatorname{Sym}^3\langle z,L\rangle.
\]
This is exactly the nonminimal boundary.  Hence V7 contains no point of
the minimal frontier.

## 5. Machine-readable coverage certificate

`verify_coverage.py` independently encodes the mutually exclusive
predicates above.  It expands them into 47 local audit atoms:

\[
\begin{array}{c|r}
\text{terminal route}&\text{atoms}\\ \hline
T0&3\\
N1&2\\
N2&3\\
V1&2\\
V2&7\\
V3&3\\
V4&3\\
V5&3\\
V6&5\\
V7&16\\ \hline
\text{total}&47.
\end{array}
\]

The 47 atoms are a local coverage-certificate expansion, **not** a new
frozen-taxonomy denominator.  They refine root collisions and the
\(W_0\)-incidence table only to test the routing.

The checker requires exactly one terminal predicate for every atom,
verifies that every named proof and hostile report exists with its
advertised status, and fails under deliberate missing-route and
overlapping-route mutations.  Run

```text
./verify_strict.sh
```

from this directory.  Current terminal output is

```text
COVERAGE_ATOMIC_CELLS=47
A0_W0_NONZERO_STATUS=HOSTILE_PASS
TRIPLE_VERTICAL_COVERAGE_PASS_4E7B19
TRIPLE_VERTICAL_COVERAGE_STRICT_PASS_85C2D0
```

I also replayed every terminal hostile wrapper, the independent
\(a=0,W_0\ne0\) wrapper, and both top-level SymPy/PARI checks.  All
passed.

## 6. Exact conclusion and remaining bridge

Within the hypotheses of the primitive fixed-linear cubic-pencil
frontier,
\[
\boxed{\text{no triple-vertical quartic Keller counterexample exists}.}
\]
Together with the previously hostile-audited horizontal theorem, this
is poised to exclude the full normalized fixed-linear primitive
cubic-pencil frontier.

The only missing certification before promoting a frozen-row statement
is external to this branch tree:

> independently verify that every point of frozen row
> `Q2-E1-A3-B1-D1-N1` is carried, by the allowed source and target
> operations and with every nonminimal boundary routed correctly, into
> either the already audited horizontal theorem or the normalized
> triple-vertical frontier audited here.

No assertion about that post-freeze bridge is made in this report.
