# Hostile certification review: complete order-13 \(k=3\) exclusion

Date: 2026-07-28 PDT

## Verdict

**PASS, conditional only on retaining the separately reviewed
four-neutral/two-port certificate at the bound hashes below.**

Together with the already accepted full-response exclusion C-090 and the
proved response-type results C-091/C-093, the retained CNF and its
addition-only RUP proof certify:

> **Complete order-13 parameter-three exclusion.** There is no graph \(G\)
> on 13 vertices such that
> \[
> \gamma(G)=\alpha(G)=\gamma^\infty(G)=3<\theta(G).
> \]

Equivalently, there is no order-13 counterexample to the gamma--theta
conjecture whose common equality parameter is \(k=3\).

This statement does **not** exclude the order-13 slices \(k\geq4\), prove
the \(k=3\) conjecture at arbitrary order, or resolve the universal
gamma--theta conjecture.

The four-neutral input is independently reconstructed and currently has
verdict `PASS` in
`reviews/tight_micro_hostile_review/result.json`.  If that artifact or its
scope changes, the composition in this review must be repeated.

## Reviewed bytes

| artifact | bytes | SHA-256 |
|---|---:|---|
| structured generator `search.py` | 6,188 | `15684fd87cdea18daa30f3506a72aa5e81a57bf4e5af94aef214f9d151f4d755` |
| structured `instance.cnf` | 4,784,714 | `76ff2768c7afd95ee535f8684515b0b15319b1f5ca69085447a1f7eba66393e1` |
| raw provenance `proof.drat` | 22,616,504 | `c5807a20b263bce64f40b1e998db2a947f221a0cdf71d734c5514ea4c10f96be` |
| decisive `proof.additions.drat` | 8,878,465 | `c985ce0a602a91a0d323594e3aeecf210fa5131027ef4b6c9b6e4d4b628f1848` |
| this review's clean-room checker | — | `0c65d45f173e2bf5b3ad4b2432f7be1c0a4023c5cd509b9549dda23daf4bdf71` |
| this review's result | — | `8c5e16a61890e54460052518d61ca723ab1e1dc388cd6d00005399354aedaab2` |

The prerequisite bindings inspected in this review are:

| prerequisite | SHA-256 |
|---|---|
| accepted C-090 full-target hostile review | `d59a0b4663cbb7c4b56faaaad103dd0a2add80a0ebe3c42cc075fd3daf55a6ec` |
| accepted C-093 decomposition hostile review | `d725aac1e663ea8b2f78810ee5471df256877e04ba1891a878d5d98ef250afa8` |
| C-091 physical-representative source note | `a619c7acf0dfccbc5767379f68d25f6272d3318db33e433cede39aa70b5ce279` |
| four-neutral clean-room checker | `70427d11293cc795a668f19da98833dacb6cad7324adf5d97b3ad57a27fbee18` |
| four-neutral clean-room `PASS` result | `f9abefecbc0c9146d9f112698083db5c84e21bf97523827d0f57be4a7024d692` |

The pinned proof checker is `drat-trim` with SHA-256
`31df522b8b2b71acd357723b0e826cf488826ed78ad9e3a7bcad241271812beb`.

## 1. Complete coverage argument

Assume for contradiction that an order-13 graph satisfies

\[
\gamma(G)=\alpha(G)=\gamma^\infty(G)=3<\theta(G).
\tag{1.1}
\]

Let \(H=\overline G\), choose an optimal eternal family \(\mathcal F\) of
triples, and choose a maximum independent triple

\[
S=\{a,b,c\}.
\]

The accepted maximum-independent-state theorem puts \(S\) in every optimal
eternal family.  For \(x\notin S\), define

\[
L(x)=\{u\in S:S-u+x\in\mathcal F\}.
\tag{1.2}
\]

Closure at \(S\) makes every \(L(x)\) nonempty.  Membership also forces the
corresponding graph edge: in the retained state \(S-u+x\), the other two
anchors both miss \(u\), so domination forces \(xu\in E(G)\).

There are now two exhaustive cases.

1. If some \(L(x)=S\), the accepted C-090 certificate excludes the graph.
   C-090 does not require the full target to be unique and does not assume
   connectivity.
2. Otherwise every outside list has size one or two.  This is exactly the
   no-full branch.  Since \(\theta(G)>3\), C-093 proves that at least two
   distinct exact two-list types occur.

Choose two occurring omitted colors \(i\ne j\), and let \(h\) be the third
anchor.  C-091/C-093 give, for each type, an exact physical representative
and a distinct same-signature complement neighbor:

\[
\begin{aligned}
&L(z_i)=S-\{i\},\quad
  \sigma(z_i)=\sigma(w_i)=\{i\},\quad z_iw_i\in E(H),\\
&L(z_j)=S-\{j\},\quad
  \sigma(z_j)=\sigma(w_j)=\{j\},\quad z_jw_j\in E(H).
\end{aligned}
\tag{1.3}
\]

Here \(\sigma(v)=N_H(v)\cap S\).  The four vertices in (1.3) are distinct:
each pair is explicitly distinct, and different pure signatures cannot
name the same vertex.

Put

\[
Q=\{q\notin S:\sigma(q)=\varnothing\}.
\tag{1.4}
\]

If \(|Q|\geq4\), choose four members of \(Q\).  The two exact
representatives in (1.3) are outside \(Q\) and carry, after naming the
anchors as \((h,i,j)\), the overlapping positive response pairs
\(\{h,j\}\) and \(\{h,i\}\).  The separately certified
four-neutral/two-port obstruction then gives a contradiction.  Therefore

\[
|Q|\leq3.
\tag{1.5}
\]

Relabel the anchors so that \(i\mapsto0\), \(h\mapsto1\), and \(j\mapsto2\).
Relabel

\[
z_i,w_i,z_j,w_j\mapsto3,4,5,6.
\]

The six remaining vertices \(7,\ldots,12\) are still freely
interchangeable.  Sort their three-bit signatures
\(\sigma(v)\subseteq\{0,1,2\}\) in nondecreasing binary order.  Neutral
signature zero sorts first.  Because all four named vertices are
nonneutral and (1.5) permits at most three neutral residual vertices, the
fourth residual vertex, label 10, has nonzero signature.

These are precisely the named units, residual sorter, and label-10 cut in
the reviewed CNF.  Every other clause family is equivariant under the
relabeling, while the complete coloring bank is invariant as a set.
Consequently every hypothetical no-full counterexample has a satisfying
assignment to the retained formula.

The checker independently exhausts all six ordered choices of distinct
type colors and all six anchor permutations.  Every type pair can be
normalized to omitted colors 0 and 2.  It also exhausts all 1,716
nondecreasing sequences of six signatures from \(0,\ldots,7\), confirming
that the label-10 clause is equivalent to “at most three zeros.”  The
64 local adjacent signature pairs confirm that the sorter accepts exactly
nondecreasing pairs, ties included.  Thus neither symmetry step omits an
orbit.

Since the CNF is certified UNSAT, the no-full case is impossible.  C-090
already excludes the complementary full case, completing the order-13
\(k=3\) exclusion.

## 2. Independent formula reconstruction

`checker.py` imports neither the structured generator, the earlier
decomposition, nor any shared transition core.  It allocates the graph,
common-neighbor, family, and move variables from the mathematical
definitions and independently emits every clause.

Its output is byte-for-byte identical to the retained DIMACS.  The exact
census is:

| clause family | count |
|---|---:|
| no \(K_4\) in \(H\) | 715 |
| pair common-neighbor choice and implications | 1,794 |
| domination of selected triples | 2,860 |
| redundant family-nonempty clause | 1 |
| one-guard move-edge implications | 8,580 |
| retained-successor implications | 8,580 |
| at-least-one response clauses | 2,860 |
| anchor \(H\)-triangle and retained anchor state | 4 |
| complete anchored non-3-colorability bank | 59,049 |
| no-full clauses | 10 |
| named pure signatures | 12 |
| named exact response lists | 6 |
| named pure-pair \(H\)-edges | 2 |
| six-vertex signature sorter | 140 |
| label-10 nonneutral cut | 1 |
| **total** | **84,614** |

The formula has 9,802 variables, no duplicate clauses, no tautologies, no
out-of-range literals, and no unused variable.

## 3. Exact model audit

An edge variable means an edge of \(H=\overline G\).

- The fixed anchor triangle and the no-\(H\)-\(K_4\) block give
  \(\alpha(G)=3\).
- Every pair has a selected outside common neighbor in \(H\), which is
  exactly the assertion that no two-set dominates \(G\).  The retained,
  dominating anchor triple then gives \(\gamma(G)=3\).
- For a selected triple \(D\) and unoccupied attack \(r\notin D\), each
  move variable names exactly one guard \(u\in D\).  Its implications
  require \(ur\notin E(H)\), hence \(ur\in E(G)\), and require the unique
  successor \(D-u+r\) to be selected.  The response clause requires at
  least one such move.  Every selected successor separately dominates.
  Thus the formula encodes the standard one-guard-moves model, not an
  all-guards model, and gives \(\gamma^\infty(G)=3\).
- The ten no-full clauses say that no outside target has all three direct
  successor states in the family.  Closure at the retained anchor state
  supplies the nonempty-list half, so this is exactly the no-full branch.
- Since the anchor triangle uses three distinct colors, every proper
  3-coloring of \(H\) can be color-permuted to colors \(0,1,2\) on the
  anchors.  The \(3^{10}=59,049\) tail assignments are all present, and
  each clause requires a monochromatic \(H\)-edge.  Hence the bank says
  \(\chi(H)>3\), equivalently \(\theta(G)>3\).

The checker existentially eliminated the three move auxiliaries in all
128 assignments of the selected-state bit, three move-edge bits, and three
successor bits.  The clauses agree exactly with

\[
\neg f_D\ \lor\
\bigvee_{u\in D}
\bigl(ur\in E(G)\land f_{D-u+r}\bigr).
\]

Connectedness, forcing every independent triple into the represented
family, odd-hole templates, and all graph-class restrictions are omitted.
Those omissions relax the formula and are safe for an UNSAT exclusion.

Conversely, any satisfying assignment would yield a genuine graph and
eternal triple-family with
\(\gamma=\alpha=\gamma^\infty=3<\theta\).  Thus the encoding is exact for
the normalized branch, not merely a one-way necessary-condition probe.

## 4. Proof replay and artifact roles

The raw solver trace contains 380,045 lines, of which 223,840 are deletion
records.  It is retained as provenance.  It verifies with RAT additions
forbidden when deletions are honored, and it also verifies in warning-fatal
plain mode (`-p`), where deletions are ignored:

```text
c 0 RAT lemmas in core
s VERIFIED
```

The decisive certificate is `proof.additions.drat`.  The checker
independently removes every deletion line from the raw trace and obtains
the retained addition-only file byte-for-byte.  It has 156,205 lines, no
deletions, and ends in the empty clause.  Warning-fatal forward replay with

```text
-I -f -W -U
```

reports:

```text
c 22897 of 84614 clauses in core
c 89819 of 156206 lemmas in core using 6369120 resolution steps
c 0 RAT lemmas in core; 0 redundant literals in core lemmas
s VERIFIED
```

Therefore the decisive proof is RUP-only and does not depend on deletion
semantics or RAT checking.

## 5. Positive control

The independently generated formula with the entire
\(\theta(G)>3\) coloring bank removed has 25,565 clauses and is SAT.
The independently parsed solver model satisfies every clause.  Its
instance SHA-256 is

```text
0b7bca68f420ad1668477fbc5fffe63dc04e50c09be2ccfac662a3226bb9fc3d
```

Thus the structural normalization, no-full family, label-10 cut, and exact
one-guard closure are jointly consistent.  The UNSAT result is not caused
by an accidental contradiction in the named structure.

## 6. Exact claim boundary

Accepted composition:

\[
\boxed{\text{no order-13 counterexample with }k=3.}
\]

Not established here:

- no order-13 counterexample for \(k=4,5,\ldots\);
- no counterexample through order 13 without the remaining parameter
  slices being independently covered;
- the \(k=3\) conjecture for arbitrary order;
- the universal gamma--theta conjecture.

This review found no complement reversal, occupied-vertex attack,
multi-guard move, missing domination obligation, clique-cover/coloring
confusion, unsound symmetry breaker, or reliance on well-coveredness
without \(\gamma=\alpha\).

