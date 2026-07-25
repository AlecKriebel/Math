# Independent audit: ADE core-shell obstructions for `r12` and `r11`

## Scope and fixed endpoint data

The first three sections audit the proposed elimination of the exact
quarter-grid endpoint
whose unordered edge counts on the colors \(-4,-3,\ldots,2\) are

\[
 (12,35,199,40,279,0,255).
\]

Thus there are exactly twelve color-\(-4\) edges and no color-\(+1\)
edges.  A color-\(-4\) edge joins antipodal unit vectors.  Antipodes are
unique, so these edges are twelve vertex-disjoint antipodal pairs.

Section 4 extends the same mechanism to all 38 exported `r11` profiles,
including their possible half-integral core defects.  The audit is independent
of the ordered-edge relaxation.  Its exact verifiers are
`verify_ade_core_shells.py` and `verify_r11_profile_ade_bounds.py`.

## 1. Root-system reduction

Choose one unit representative \(p_i\) from each antipodal pair and put
\(\alpha_i=\sqrt2p_i\).  For two different directions, all four sign
choices occur among the corresponding code points.  Hence
\(|\langle p_i,p_j\rangle|\le1/2\).  Quarter-grid integrality and the absence
of color \(+1\) sharpen this to

\[
 \langle\alpha_i,\alpha_j\rangle
 =2\langle p_i,p_j\rangle\in\{-1,0,1\}.
\]

Each \(\alpha_i\) has squared norm two.  Therefore

\[
 L=\sum_{i=1}^{12}\mathbb Z\alpha_i
\]

is a positive-definite integral even lattice in its real span.  Let

\[
 R=\{\alpha\in L:\langle\alpha,\alpha\rangle=2\}.
\]

It is finite.  For \(\alpha\in R\), the reflection

\[
 s_\alpha(x)=x-\langle x,\alpha\rangle\alpha
\]

preserves \(L\) and \(R\).  Consequently \(R\) is a reduced simply-laced
crystallographic root system.  It spans \(L\), because it contains the
twelve generators.  Moreover

\[
 L=\mathbb ZR:
\]

one inclusion holds because \(R\subset L\), and the other because the
generators \(\alpha_i\) belong to \(R\).  This equality closes the possible
``nonprimitive root sublattice'' loophole.

There are at least 24 roots, namely the twelve distinct pairs
\(\{\pm\alpha_i\}\), and the rank is at most five.  The ADE root counts leave
only

\[
 A_5,\quad D_5,\quad D_4+A_1,\quad D_4.
\]

Indeed \(A_n\) has \(n(n+1)\) roots and \(D_n\) has \(2n(n-1)\);
all other reducible types of rank at most five have fewer than 24 roots.
The last case has rank four; the first three have rank five.

Changing the chosen sign of a line representative causes no issue: every
constraint below is invariant under \(\alpha_i\mapsto-\alpha_i\).

## 2. Full-rank dual-shell reduction

Let \(y\) be any of the remaining 17 code points and set
\(\beta=\sqrt2y\).  Its two edges to an antipodal pair have opposite colors.
Colors \(\pm3\) cannot both satisfy the kissing inequality, and colors
\(\pm1\) are impossible because the global color-\(+1\) count is zero.
Therefore

\[
 \langle\beta,\alpha_i\rangle\in\{-1,0,1\}
 \quad(1\le i\le12),\qquad \|\beta\|^2=2.
\]

When the core has rank five it spans the ambient space.  Thus \(\beta\) is
in the dual lattice \(L^*\), but it need not be in the root lattice.  The
discriminant forms show that in the three possible full-rank types it
actually must be a root.  Norm modulo \(2\mathbb Z\) is constant on a coset
of an even root lattice.  The nonzero dual/root cosets have the following
values:

\[
\begin{array}{c|c}
L& q(\gamma)=\|\gamma\|^2\bmod 2\mathbb Z
   \text{ for nonzero cosets}\\ \hline
A_5&5/6,\ 4/3,\ 3/2,\ 4/3,\ 5/6\\
D_5&1,\ 5/4,\ 5/4\\
D_4+A_1&1,\ 1/2,\ 3/2.
\end{array}
\]

None is zero modulo \(2\mathbb Z\).  Since \(\|\beta\|^2=2\), \(\beta\)
lies in the zero coset, hence in \(L\).  The norm-two vectors of \(L\) are
exactly its roots.  The 24 signed core roots are already used, so the
numbers of possible residual vectors are at most

\[
 |A_5|-24=30-24=6,\qquad
 |D_5|-24=40-24=16,\qquad
 |D_4+A_1|-24=26-24=2.
\]

For completeness, the table follows from standard coordinate
representatives.  In \(A_5^*/A_5\cong\mathbb Z/6\), the \(k\)-th fundamental
weight has norm \(k(6-k)/6\).  For \(D_5\), the vector and two spinor cosets
have representatives of norms \(1,5/4,5/4\).  Every nonzero coset of
\(D_4^*/D_4\) has a norm-one representative, while the nonzero
\(A_1^*/A_1\) coset has norm \(1/2\); orthogonal direct sums add these
values.

This conceptual count already eliminates every full-rank case.

As an independent check, the verifier also enumerates the entire dual shell
directly, rather than assuming the discriminant argument:

1. choose any five linearly independent selected roots \(b_1,\ldots,b_5\);
2. enumerate all \(c=(\langle\beta,b_j\rangle)_j\in\{-1,0,1\}^5\);
3. with \(H=(\langle b_i,b_j\rangle)\), test
   \(c^{\mathsf T}H^{-1}c=2\);
4. reconstruct every pairing with all twelve selected roots exactly and
   retain it only if it lies in \(\{-1,0,1\}\).

That enumeration is exhaustive even when the five independent roots are not a
\(\mathbb Z\)-basis: an admissible \(\beta\) has one of the enumerated
pairing vectors \(c\), and nonprimitive coordinate choices do not alter the
unique reconstructed real vector.

The canonical line sets are

\[
\begin{array}{c|c|c}
\text{type}&\text{line representatives}&\text{number of lines}\\ \hline
A_5&e_i-e_j\subset\{x\in\mathbb R^6:\sum x_i=0\}&15\\
D_5&e_i\pm e_j\subset\mathbb R^5&20\\
D_4+A_1&e_i\pm e_j\subset\mathbb R^4,\ \sqrt2e_5&13.
\end{array}
\]

Every 12-line subset is checked, without quotienting by symmetry.  Exact
rational arithmetic gives

\[
\begin{array}{c|r|r|r|r}
\text{type}&\binom{|R|/2}{12}&\text{rank 5}&\text{rank 4}
 &\max\text{ admissible }\beta\\ \hline
A_5&455&455&0&6\\
D_5&125970&125965&5&16\\
D_4+A_1&13&12&1&2.
\end{array}
\]

In fact every full-rank subset in a given row has the displayed shell
cardinality, agreeing with the discriminant-form proof.  The five deficient
\(D_5\) subsets and the one deficient \(D_4+A_1\) subset are copies of the
remaining \(D_4\) case.

## 3. Rank-four \(D_4\)

Put the \(D_4\) core in \(\mathbb R^4\) and write

\[
 \beta=(p,h)\in\mathbb R^4\oplus\mathbb R.
\]

Exact enumeration of the \(3^4\) possible pairings with a root basis, followed
by all twelve root constraints, gives precisely

\[
 p=0
 \quad\text{or}\quad
 p\in
 \{\pm e_i:1\le i\le4\}
 \cup
 \{(\pm\tfrac12,\pm\tfrac12,\pm\tfrac12,\pm\tfrac12)\}.
\]

The latter 24 vectors are the vertices of the 24-cell and have norm one.
The norm equation \(\|\beta\|^2=2\) therefore gives

\[
 (p,h)=(0,\pm\sqrt2)
 \quad\text{or}\quad
 p\in V_{24},\ h=\pm1.
\]

A pole \((0,\pm\sqrt2)\) has irrational inner product
\(\pm\sqrt2\) with every norm-one candidate, outside the quarter grid.
The two opposite poles have inner product \(-2\), which would be a
thirteenth antipodal pair.  Hence a 17-point residual set cannot contain a
pole.

Among 17 remaining candidates, at least nine have the same height sign.
For two distinct candidates \((p,1),(q,1)\), their scaled inner product is

\[
 \langle p,q\rangle+1.
\]

The allowed residual colors are

\[
 \{-3/2,-1,-1/2,0,1\};
\]

\(+1/2\) is absent because the global color-\(+1\) count is zero.  Thus two
same-height candidates are compatible exactly when

\[
 \langle p,q\rangle\in\{-1,0\}.
\]

The resulting graph on the 24-cell has clique number eight, with a short
direct proof.  The eight coordinate vectors \(\{\pm e_i\}\) form one
complete component.  Two half-sign vectors are adjacent exactly when their
sign strings have even Hamming distance, so the even-parity and odd-parity
half-sign vectors form two further complete components of size eight.
There are no edges between these three components.  Nine same-height
candidates are therefore impossible.  (The verifier also checks directly
that the full 50-candidate compatibility graph has clique number 16.)

This eliminates the rank-four case.

## 4. Eleven-pair extension, including half-integral defects

The exact `r11` profile export contains 38 global vectors with eleven
color-\(-4\) edges and

\[
 0\le m_{+1}\le6.
\]

Choose representatives of the eleven antipodal directions and again scale
them to norm-two vectors \(\alpha_i\).  Join two core lines in the
**defect graph** when

\[
 \langle\alpha_i,\alpha_j\rangle=\pm\tfrac12.
\]

Each such line-line defect produces two color-\(+1\) edges among the four
signed core points.  If the defect graph has \(e\) edges, then

\[
 e\le \lfloor m_{+1}/2\rfloor\le3.
\]

Let \(D\) be a minimum vertex cover of the defect graph, put \(d=|D|\), and
let \(S\) be the remaining \(k=11-d\) core lines.  Thus

\[
 d\le e\le3,\qquad k\ge8,
\]

and all pairings inside \(S\) are integral.  The lines in \(S\) generate an
even integral ADE root lattice \(L\).  Its rank is at least four, since a
rank-at-most-three simply-laced root system has at most six root lines.

### The integral remainder cannot have rank four when \(e>0\)

If \(L\) had rank four, its root system would be \(A_4\) or \(D_4\), the
only rank-four types with at least eight root lines.  Every vertex
\(\delta\in D\) has a defect neighbor in \(S\): otherwise deleting
\(\delta\) from \(D\) would leave a smaller vertex cover.  Hence

\[
 \chi_\delta(\alpha)
 =2\langle\delta,\alpha\rangle\pmod2
\]

is a nonzero character of the root lattice.

Among all root lines, a nonzero character marks at least four of the ten
\(A_4\) lines and at least six of the twelve \(D_4\) lines.  The exact
distributions are

\[
\begin{array}{c|c}
A_4&5\text{ characters mark }4,\quad10\text{ mark }6\\
D_4&12\text{ characters mark }6,\quad3\text{ mark }8.
\end{array}
\]

After omitting the root lines not in \(S\), either type therefore leaves at
least

\[
 k-6=5-d
\]

marked selected lines.  These are crossing defect edges from \(\delta\) to
\(S\).  Summing over \(\delta\in D\) counts each crossing edge once, so

\[
 e\ge d(5-d).
\]

For \(d=1,2,3\), the right side is \(4,6,6\), contradicting \(e\le3\).
Thus whenever \(e>0\), the integral remainder \(S\) has full rank five.

### Full-rank remainder

The rank-five root systems with at least eight root lines are

\[
 A_5,\ D_5,\ D_4+A_1,\ A_4+A_1,\ A_3+A_2,\ A_3+2A_1.
\]

In every case the norm-two shell of \(L^*\) has at most 20 antipodal
lines.  The maximum 20 occurs for \(D_5\) and \(A_3+2A_1\).  For the latter,
the shell consists of its eight root lines plus twelve cross-component
lines: a norm-one \(A_3^*\) vector (six choices) together with one minimal
vector from each \(A_1^*\) component (two choices each), giving 24 oriented
cross vectors.

Call an unpaired residual point **ordinary** if all its pairings with \(S\)
are integral.  Its scaled vector is then a norm-two vector of \(L^*\).
The eleven core pairs already exhaust all color-\(-4\) edges, so the
unpaired residual set can use at most one orientation from each dual-shell
line.  It also cannot use a selected core line.  Hence there are at most

\[
 20-k
\]

ordinary residual points.

Every nonordinary residual point has a half-integral pairing with at least
one line of \(S\), consuming a color-\(+1\) edge.  The line-line defects
already consume \(2e\) such edges, so there are at most \(6-2e\)
nonordinary residual points.  Altogether,

\[
 |C_{\rm residual}|
 \le (20-k)+(6-2e)
 =15+d-2e
 \le15,
\]

far below the required 19.  This handles all full-rank remainders,
including the defect-free case.

### Defect-free rank-four remainder

It remains only to consider \(e=0\) and rank four.  Then the eleven integral
lines lie in \(D_4\) and omit exactly one of its twelve root lines.  For an
ordinary residual vector \(\beta=(p,h)\), the projected shell is exactly

\[
 p=0,\qquad p\in V_{24},\qquad p=\pm\rho,
\]

where \(\rho\) represents the omitted root line.  These have heights
\(\pm\sqrt2,\pm1,0\), respectively.

A nonordinary residual vector defines a nonzero character of \(D_4\).
Such a character marks six or eight of all twelve root lines, hence at
least five of the selected eleven.  It therefore consumes at least five
color-\(+1\) edges.  Since \(m_{+1}\le6\), at most one residual point is
nonordinary, and at least 18 are ordinary.

A pole cannot lie in such a large ordinary set: its inner product with a
norm-one candidate is \(\pm\sqrt2\), outside the quarter grid, and at most
one of \(\pm\rho\) can be used without creating a twelfth antipodal pair.
Thus at least 17 ordinary points lie in the two height layers \(h=\pm1\);
some layer contains at least nine.

For \(k\) vectors in one height layer, write
\(t_{ij}=\langle p_i,p_j\rangle\).  The kissing inequality gives
\(t_{ij}\le0\).  Distinct 24-cell vertices then have

\[
 t_{ij}\in\{-1,-\tfrac12,0\},\qquad t_{ij}^2\le-t_{ij}.
\]

If \(H=(\langle p_i,p_j\rangle)\), then

\[
 \operatorname{tr}(H^2)
 =k+2\sum_{i<j}t_{ij}^2
 \le k-2\sum_{i<j}t_{ij}
 \le2k,
\]

where the last inequality is
\(\|\sum_i p_i\|^2=k+2\sum_{i<j}t_{ij}\ge0\).  On the other hand
\(\operatorname{rank}H\le4\) and \(\operatorname{tr}H=k\), so

\[
 \operatorname{tr}(H^2)\ge k^2/4.
\]

Therefore \(k\le8\), contradicting the nine vectors forced into one layer.

All 38 exported `r11` global profiles are eliminated.

## 5. Boundary, orientation, and coverage audit

* Inner products equal to \(+1/2\) are retained: in scaled variables they
  are \(+1\).  No strict inequality is substituted.
* In the `r12` endpoint, the exclusion of scaled \(+1/2\) in the residual
  graph uses the exact global count \(m_{+1}=0\), not a numerical tolerance.
* In the `r12` endpoint, opposite residual candidates are excluded only
  because the twelve known core pairs already exhaust the exact count
  \(m_{-4}=12\).
* The `r11` argument does not exclude scaled half-integral pairings.  It
  charges each line-line defect against two color-\(+1\) edges and each
  nonordinary residual against at least one additional color-\(+1\) edge.
* In every `r11` profile, the eleven known core pairs exhaust
  \(m_{-4}=11\), which is exactly what permits at most one residual
  orientation from each dual-shell line.
* All arithmetic in the verifier is integer or `Fraction`; there is no
  floating-point PSD or rank decision.
* Every canonical 12-subset is examined.  No assumed symmetry, orientation,
  primitivity, rigidity, or contact graph enters the enumeration.
* In the full-rank cases the search is over the dual shell determined by
  generator pairings.  It does not assume that a residual vector is a root.
* In rank four the entire one-dimensional orthogonal complement is covered
  by \(h=\pm\sqrt{2-\|p\|^2}\); no off-span vector is dropped.

## 6. Exact verification command

From any directory, run

```text
/usr/bin/python3 /absolute/path/to/verify_ade_core_shells.py
```

The expected final line is

```text
PASS: exact ADE core-shell enumeration
```

The verifier uses only the Python standard library.
