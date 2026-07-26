# Adversarial review of the template-coloring-bank theorem

## Verdict

**ACCEPT.**  The theorem in
`math/lemmas/template_coloring_bank.md` is correct for each of `hole5`,
`hole7`, and `hole9`.  The claimed bank is exactly the quotient, by color-name
permutation, of all three-color assignments compatible with the
forced-positive \(H=\overline G\) edge units.  Relative to those units, the
conjunction of its same-color clauses is equivalent to
\(\chi(H)>3\).  No graph-label symmetry or unproved structural assumption is
used.

This verdict concerns the mathematical theorem and the deterministic formula
construction.  It is not an UNSAT verdict for `hole5` or `hole7`, and no
solver was run in this review.

## Objects audited

- `src/synthesis_k3/encoding.py`, whose SHA-256 is
  `fda94aeb7a2c48e64f1b9a975c27263b100542359c13264f4a625f115ff563c6`;
- `math/lemmas/template_coloring_bank.md`, frozen author SHA-256
  `abc9568d70eee6b792e4220b58c12f5e7c069a13e37dbd3265025abe02cd6f50`;
- `src/synthesis_k3/template_color_bank.py`, frozen author SHA-256
  `dc69687f01e85bea643b73f713b1afca51b3911b3fee4a857da3fb07cc979838`;
- `tests/test_template_color_bank.py`, frozen author SHA-256
  `cc89c89133593a986a77d683ec253bf7db49e53f3ba27ede03e4fcee89fccdf7`;
- the accepted `hole9` recovery formula and addition-only RUP proof described
  below.

The review derived the counts using a standard-library-only enumeration that
did not import the bank generator or the synthesis encoding.  It also checked
the clause and variable conventions directly against the frozen source.

## Line-by-line mathematical audit

### Scope and template literals (note lines 5--18)

The complement direction is correct: \(H=\overline G\), the edge variable
\(e_{uv}\) is true for an \(H\)-edge, and
\(\theta(G)=\chi(H)\).  In `encoding.py`, a `hole`\(\ell\) instance has
positive units on the \(\ell\) rim edges and on \(0\ell,1\ell\), negative
units on all other rim pairs, and a non-unit no-hub clause for each external
vertex.  Therefore exactly the positive units constrain which color
assignments can possibly be proper.  Retaining same-color literals
corresponding to forced nonedges is logically harmless.

### First-use canonicalization (note lines 22--33)

The restricted-growth condition with \(c_0=0\) chooses one representative of
each orbit under permutation of the used color names.  Here every compatible
row uses all three colors because \(0,1,\ell\) is a forced triangle.  Thus the
\(S_3\) action is free, every orbit has size six, and there is no exceptional
one- or two-color orbit.

The clause records the equivalence relation “has the same color.”  Hence two
canonical rows cannot produce the same full same-color clause.

### Exact bank and formula counts (note lines 37--75)

For odd \(\ell\),
\[
P(C_\ell,3)=2^\ell-2.
\]
The edge \(01\) gives distinct colors at \(0,1\), so their common neighbor
\(\ell\) is forced to the third color.  The remaining \(11-\ell\) vertices
are unrestricted by positive units.  Dividing the resulting labeled count by
six is therefore sound:

| template | compatible labeled rows | canonical rows |
|---|---:|---:|
| `hole5` | \(30\cdot3^6=21{,}870\) | \(3{,}645\) |
| `hole7` | \(126\cdot3^4=10{,}206\) | \(1{,}701\) |
| `hole9` | \(510\cdot3^2=4{,}590\) | \(765\) |

An exhaustive independent pass over all \(3^{12}=531{,}441\) named
assignments reproduced these three counts.  Every incompatible assignment
gave a same-color clause containing at least one forced-positive edge
variable, so its omitted clause is already true under the template units.
The formula sizes newly tabulated in note lines 67--75 agree with the
independent clause-by-clause accounting below.

### Clause semantics and quantifiers (note lines 79--110)

For a fixed row \(c\),
\[
C_c=\bigvee_{c_u=c_v}e_{uv}
\]
is false exactly when no same-color pair is an edge of \(H\), which is exactly
that \(c\) is a proper coloring of \(H\).

The quantifiers in Theorem 2 are consequently:
\[
\begin{aligned}
H\models\bigwedge_{c\in B_\ell}C_c
&\iff
\text{every template-compatible color partition has an \(H\)-edge
inside a block}\\
&\iff H\text{ has no proper coloring with at most three colors}\\
&\iff \chi(H)>3.
\end{aligned}
\]
The middle equivalence is relative to the forced-positive template units:
any proper coloring of \(H\) is compatible with them, while every
incompatible assignment is already killed by one of them.  The forced
triangle excludes the possible ambiguity between “using three named colors”
and “using at most three colors.”

No permutation of graph vertices is used.  Canonicalization acts only on
color names, and every canonical row contributes its own ordinary coloring
cut.

### Generation and certificate boundary (note lines 114--144)

The source enumeration is lexicographic restricted-growth recursion and its
exhaustive audit uses a separate \(3^{12}\) labeled-assignment pass.  The
formula constructor retains the frozen base encoding and appends the exact
positive same-color clause for every row.  The timeout/SAT/UNSAT limitations
in the note are stated correctly.  They are operational safeguards and are
not premises of Theorem 2.

## Independent formula accounting

The frozen base has the following variables:

| role | count |
|---|---:|
| \(H\)-edge variables | \(\binom{12}{2}=66\) |
| common-neighbor witness variables | \(\binom{12}{2}\cdot10=660\) |
| family variables | \(\binom{12}{3}=220\) |
| move variables | \(\binom{12}{3}\cdot9\cdot3=5{,}940\) |
| **total** | **6,886** |

Before template clauses, the base has 19,989 clauses and 114,554 literals.
The independently counted categories are:

- \(495\) \(K_4\)-exclusion clauses, \(2{,}970\) literals;
- \(66\) length-10 witness-existence clauses and \(1{,}320\) binary witness
  implications, \(3{,}300\) literals total;
- \(2^{11}-1=2{,}047\) connected-cut clauses, with
  \[
  \sum_{t=0}^{11}\binom{11}{t}(t+1)(11-t)=67{,}584
  \]
  literals;
- \(1{,}980\) length-4 domination clauses, \(7{,}920\) literals;
- one length-220 family-nonempty clause;
- \(11{,}880\) binary move implications and \(1{,}980\) length-4 response
  clauses, \(31{,}680\) literals total;
- \(220\) length-4 forced-triangle-family clauses, \(880\) literals.

The template contributes
\[
\binom{\ell}{2}+(12-\ell)+2
\]
clauses and
\[
\binom{\ell}{2}+\ell(12-\ell)+2
\]
literals.  Independent enumeration of the bank rows gave:

| template | base clauses | base literals | bank clauses | bank literals | complete clauses | complete literals |
|---|---:|---:|---:|---:|---:|---:|
| `hole5` | 20,008 | 114,601 | 3,645 | 74,358 | 23,653 | 188,959 |
| `hole7` | 20,017 | 114,612 | 1,701 | 33,939 | 21,718 | 148,551 |
| `hole9` | 20,030 | 114,619 | 765 | 14,940 | 20,795 | 129,559 |

All three complete formulas retain exactly 6,886 variables.  These values
agree with the constants in `template_color_bank.py`; they were not derived
from those constants.

## Accepted `hole9` proof reuse

The accepted source artifacts are:

- 170-cut formula SHA-256
  `2845f242a094484a8d114e70ca1a8678dfcff79fadd56bd57813e25c2e49523d`;
- source coloring file SHA-256
  `a3c7bd3591b71c310cfe0bd5711b8e672b75136f3598bb1505ae11cda3c2193b`;
- addition-only RUP proof SHA-256
  `24c5647d3a57f2de221fba96747c618575a3aba086c5e4bca17aade55ce7d4ab`.

An independent parser established all of the following:

1. the accepted formula has the frozen 20,030-clause `hole9` base followed
   by exactly the 170 clauses reconstructed from the source colorings;
2. those 170 clauses are distinct;
3. all 170 occur verbatim among the 765 complete-bank clauses, with the same
   edge-variable numbering \(1,\ldots,66\);
4. their total literal count is 3,222, so the other 595 bank clauses contain
   11,718 literals; and
5. the accepted proof has 4,705 addition lines, no deletion line, and ends
   in the empty clause.

Consequently the existing proof remains a valid RUP proof after the other
595 bank clauses are added.  Indeed, each original RUP step has a
unit-propagation contradiction from the original formula and preceding proof
steps under the negation of that step.  Adding clauses cannot remove any
clause or propagation used in that derivation; it may only produce a
contradiction earlier.  Thus RUP validity is monotone under strengthening the
initial formula.  This observation is proof reuse, not a new UNSAT search.

## Defect search

No mathematical defect was found in the claimed universe, complement
direction, color-name quotient, clause semantics, quantifier order, or exact
counts.  Two scope qualifications should remain explicit:

1. the bank equivalence is relative to the forced-positive template units;
   the bank by itself does not include clauses for incompatible colorings;
2. complete-bank UNSAT for one template certifies only that named template,
   not the whole `(n,k)=(12,3)` slice.

Both qualifications are already respected by the author note.
