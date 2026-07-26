# Exact template-compatible three-coloring banks

## Scope

This note concerns the three `hole` templates in the frozen order-12,
parameter-three synthesis encoding.  Throughout, \(H=\overline G\), and
\(e_{uv}\) is true exactly when \(uv\in E(H)\).  This is an exact replacement
for learning one three-coloring cut at a time; it does not change any other
part of the synthesis formula.

For \(\ell\in\{5,7,9\}\), the `holeℓ` template has:

- the induced cycle \(0,1,\ldots,\ell-1,0\) in \(H\);
- a distinguished vertex \(\ell\) adjacent in \(H\) to both \(0\) and \(1\);
- the other \(11-\ell\) vertices \(\ell+1,\ldots,11\).

Only the forced **positive** \(H\)-edges constrain a coloring.  Forced
nonedges, including the cycle chords, impose no coloring constraint.

## Canonical rows

A row is a word \(c=(c_0,\ldots,c_{11})\in\{0,1,2\}^{12}\).  It is
*first-use canonical* when

\[
c_0=0,\qquad
c_j\leq 1+\max\{c_0,\ldots,c_{j-1}\}\quad(1\leq j<12).
\]

Thus colors are named \(0,1,2\) in the order in which their blocks first
appear.  First-use canonical rows are also called restricted-growth strings.
The bank \(B_\ell\) consists of exactly the first-use canonical rows proper on
every forced positive edge of the `holeℓ` template.

## Exact count

**Lemma 1.**  The bank size is

\[
|B_\ell|=\frac{(2^\ell-2)3^{11-\ell}}{6}.
\]

**Proof.**  The chromatic polynomial of a cycle is

\[
P(C_\ell,q)=(q-1)^\ell+(-1)^\ell(q-1).
\]

For odd \(\ell\) and \(q=3\), the labeled cycle therefore has
\(2^\ell-2\) proper colorings.  Vertices \(0\) and \(1\) receive distinct
colors.  The distinguished vertex \(\ell\), adjacent to both, must receive
the third color.  Each of the remaining \(11-\ell\) vertices is unrestricted,
giving \((2^\ell-2)3^{11-\ell}\) labeled rows.

The triangle \(0,1,\ell\) uses all three colors, so the action of the six
color-name permutations is free.  First-use canonicalization chooses exactly
one row in each orbit.  Division by \(3!=6\) proves the formula. \(\square\)

Consequently,

| template | exact bank size |
|---|---:|
| `hole5` | \(30\cdot3^6/6=3{,}645\) |
| `hole7` | \(126\cdot3^4/6=1{,}701\) |
| `hole9` | \(510\cdot3^2/6=765\) |

Direct generation from the frozen encoder independently reproduces the
following formula sizes.  Each complete clause count is the corresponding
base count plus exactly one clause per bank row.

| template | base clauses | base literals | complete clauses | complete literals |
|---|---:|---:|---:|---:|
| `hole5` | 20,008 | 114,601 | 23,653 | 188,959 |
| `hole7` | 20,017 | 114,612 | 21,718 | 148,551 |
| `hole9` | 20,030 | 114,619 | 20,795 | 129,559 |

## Exact CNF equivalence

For \(c\in B_\ell\), define

\[
C_c=\bigvee_{\substack{0\leq u<v<12\\c_u=c_v}}e_{uv}.
\]

The row is proper on every forced positive template edge, so no literal in
\(C_c\) is a forced-true template edge.  Literals that happen to be forced
false are harmless and are retained to keep the clause definition uniform.

**Theorem 2.**  For every graph \(H\) extending the forced `holeℓ` template,

\[
H\models\bigwedge_{c\in B_\ell}C_c
\quad\Longleftrightarrow\quad
\chi(H)>3.
\]

**Proof.**  For a fixed row \(c\), \(C_c\) is false precisely when every pair
of vertices in a common color block is a nonedge of \(H\).  This says exactly
that \(c\) is a proper three-coloring of \(H\).

If \(H\) has a proper coloring with named colors, it is proper on the forced
template edges.  Renaming colors by first occurrence preserves its blocks and
produces the unique representative \(c\in B_\ell\); hence \(C_c\) is false.
Conversely, if some \(C_c\) is false, its bank row is a proper coloring of
\(H\).  Therefore all bank clauses hold exactly when \(H\) has no proper
three-coloring. \(\square\)

The forced triangle also shows that “three-coloring” here cannot hide a
one- or two-color assignment.  No symmetry-breaking assumption about \(H\)
is used.

## Generation and certificate boundary

`src/synthesis_k3/template_color_bank.py` independently enumerates the
restricted-growth strings in lexicographic order, validates them against a
full labeled-coloring oracle, adds their clauses to the frozen base encoding,
and writes a byte-deterministic bank, CNF, and binding manifest.  Its package
audit reconstructs both decisive artifacts byte for byte.  The manifest binds
the base-formula hash and counts, the exact zero-based interval occupied by
the appended bank clauses, and a header-free DIMACS clause-stream hash.  Thus
an independent checker can test whether a prior cut set is a subset of the
complete bank and whether a prior proof remains replayable after the extra
axioms, without relying on clause inference from prose.  It also records the
repository commit and checks each runtime source against that commit; unrelated
worktree cleanliness is neither assumed nor required.  Exact SHA-256 bindings
remain authoritative when a development run precedes its source commit.

The optional solve command is deliberately separate and gated.  It:

1. audits the complete input package;
2. binds the pinned CaDiCaL 3.0.1 and DRAT-trim binaries and source archives;
3. applies wall, CPU, memory, file-size, disk-reserve, and campaign-global
   single-heavy-child controls;
4. validates any SAT model directly against the exact DIMACS formula; or
5. for UNSAT, retains a nonempty DRAT proof and accepts it only after the
   pinned independent checker reports exactly one warning-free
   `s VERIFIED`.

An UNSAT outcome certifies only the precisely named template instance.  A SAT
outcome is only a candidate requiring the campaign's independent graph and
parameter verifiers.  Timeout or resource exhaustion proves nothing.
Unexpected exits, file ceilings, malformed solver artifacts, and every checker
failure produce an explicit `NO_MATHEMATICAL_CLAIM` outcome rather than an
implicit or orphaned UNSAT assertion.
