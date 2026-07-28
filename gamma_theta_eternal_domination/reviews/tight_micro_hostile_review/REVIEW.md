# Hostile review: the order-13 four-neutral/two-port certificate

Date: 2026-07-28 (PDT)

## Verdict

\[
\boxed{\textbf{PASS}}
\]

The production CNF, its mathematical interpretation, the relabeling
coverage argument, and the retained UNSAT proof all pass independent
adversarial review.

The exact certificate-backed statement is:

> There is no graph \(G\) on 13 vertices, eternal family
> \(\mathcal F\) of triples, and independent state
> \(S=\{h,i,j\}\in\mathcal F\), with \(\gamma(G)\geq3\), four distinct
> vertices outside \(S\) that are \(G\)-complete to \(S\), and two
> further distinct vertices \(x,y\) such that
> \[
> \{h,j\}\subseteq L_S^{\mathcal F}(x),
> \qquad
> \{h,i\}\subseteq L_S^{\mathcal F}(y).
> \]

The formula does **not** assume a clique-cover gap, connectedness, the
no-full branch, exact or negative response incidences, fixed anchor
signatures for the two ports, or that the family is the greatest eternal
family.

This is a proof-certificate-backed finite theorem, not a human structural
proof.  It does not resolve the gamma--theta conjecture and does not
exclude all order-13 parameter-three candidates.

## 1. Clean-room formula reconstruction

The reviewer reconstructed the formula without importing either discovery
generator.  The reconstruction is byte-for-byte identical to the retained
DIMACS.

\[
\begin{array}{c|r}
\text{variable kind}&\text{count}\\ \hline
H=\overline G\text{ edges}&78\\
\text{selected triples}&286\\
\text{common-}H\text{-neighbor selectors}&858\\ \hline
\text{total}&1222
\end{array}
\]

The 24,694 clauses split as follows:

\[
\begin{array}{c|r}
\text{block}&\text{clauses}\\ \hline
\text{common-neighbor choices}&78\\
\text{selector-to-edge implications}&1716\\
\text{literal one-guard closure}&22880\\
\text{independent retained anchor state}&4\\
\text{four neutral signatures}&12\\
\text{four positive port responses}&4
\end{array}
\]

All clauses are unique, none is tautological, every literal lies in the
declared variable range, and the declared counts are exact.

### Common-neighbor block

For every distinct pair \(u,v\), one selector chooses
\(w\notin\{u,v\}\), and a true selector forces
\(uw,vw\in E(H)\).  This is equivalent to saying that every pair fails
to dominate \(G\), hence \(\gamma(G)\geq3\).

### One-guard closure

For selected \(D\), unoccupied attacked vertex \(r\), and guard
\(g\in D\), a response is the conjunction

\[
\neg e^H_{gr}\ \land\ f_{D-g+r}.
\]

The encoding uses the eight distributive clauses for the disjunction of
the three two-literal conjunctions.  An independent truth table checked
all \(2^7=128\) assignments to the selected-state bit, three edge bits,
and three successor bits, with zero discrepancies.  Thus the block
requires exactly one guard to move along one \(G\)-edge to the unoccupied
target and retains exactly the one-swap successor.  It is neither an
all-guards-move rule nor a relaxation.

Closure also makes every selected triple dominating: for each unoccupied
vertex, some occupied guard is adjacent to it.  The unit \(f_S\) therefore
makes the family nonempty and \(S\) dominating.

### Anchors, neutral vertices, and response ports

The three \(H\)-edge units on \(S=(0,1,2)\) make \(S\) independent.
Together with the common-neighbor and closure blocks,

\[
\gamma(G)=\gamma^\infty(G)=3.
\]

Since \(S\) is independent and
\(\alpha(G)\leq\gamma^\infty(G)\), also \(\alpha(G)=3\).  It is therefore
sound to omit a separate no-\(H\)-\(K_4\) block.

The twelve negative edge units make vertices \(8,9,10,11\)
\(G\)-complete to \(S\).  The four positive family units retain the two
direct successors at vertex 3 for anchors 0 and 2 and the two direct
successors at vertex 5 for anchors 0 and 1.

Retaining a direct successor also forces the corresponding move edge.
Indeed, the successor must dominate the omitted anchor; the two remaining
anchors cannot do so because \(S\) is independent, leaving the new port
as the only possible neighbor.  Therefore these units have precisely the
claimed positive response-list meaning.  No negative list membership is
silently imposed.

## 2. Coverage of the C-093 no-full branch

The implication to the campaign's order-13 residual is sound.

In an order-13 no-full candidate with \(\theta(G)>3\), C-093 forces at
least two distinct exact two-list types.  Any two such types share one
anchor; relabel the anchors as \(h,i,j\).  The accepted physical
representative theorem supplies distinct representatives \(x,y\) outside
the neutral set with

\[
L(x)=\{h,j\},\qquad L(y)=\{h,i\}.
\]

If the neutral set \(Q\) had at least four vertices, choose any four of
them.  Relabel \(S,x,y\), and those four neutral vertices as
\(0,1,2,3,5,8,9,10,11\), respectively; the other four labels are
unrestricted.  There is no symmetry breaker and no orbit can be omitted.
This would produce a model of the certified CNF, contradicting UNSAT.
Consequently the surviving no-full branch satisfies

\[
\boxed{|Q|\leq3,\qquad |A|\geq7.}
\]

This numerical bound happens to match an earlier retracted draft, but the
old static argument remains invalid.  The accepted bound now depends on
the two positive response pairs, full eternal-family closure, and the
finite UNSAT certificate.

The remaining cases are

\[
(|A|,|Q|)=(7,3),(8,2),(9,1),(10,0).
\]

## 3. Proof replay

The retained production artifacts have:

```text
micro_search.py
15c159737a7c3987aed7e6ab488e1744ee0b6252bbed555388f6832f1db56c79

micro-instance.cnf
3d1a1379eb2a90ffd399e5a830b1a81881ed527c6e9db06574a390085cb5c1e0

micro-proof.additions.drat
c4f1989ac80474a86b75ba939e494bde5928b2727fd61297eb695f3937222eee
```

The proof has 78,697 ASCII additions, contains no deletion line, and ends
with the empty clause.

The independent checker performed three distinct checks.

1. Forward DRAT-trim replay with `-I -f -W -U` returned zero, reported
   exactly one `s VERIFIED`, and used zero RAT lemmas.
2. A fresh backward RUP-only conversion produced a 20,258,391-byte LRAT
   file with SHA-256
   `9bfbc4d68f65bc2b76a6c96ab1608c0362ef3b4edf3efeeaf74c3d4630722486`.
3. The separate pinned `lrat-check` executable accepted that fresh LRAT
   with exit zero and exactly one `c VERIFIED`.

The proof was also replayed against the satisfiable three-neutral
ablation and was rejected, confirming that the checker does not accept
the certificate independently of its bound formula.

The proof core remains global: 10,833 input clauses and 46,840 retained
lemmas, using all 13 labels, all 78 edge variables, all 286 family
variables, and 825 of the 858 common-neighbor selectors.  No short
human-readable attack proof was found.

The pinned executable hashes are:

```text
drat-trim
31df522b8b2b71acd357723b0e826cf488826ed78ad9e3a7bcad241271812beb

lrat-check
5d7d77a57457db82e57f2505ea9d0267ff0bceff197235b6edfc8fda1f26c7a2

CaDiCaL 3.0.1
51c3c82b354f455c925fc60b37c701e8498afcf0f3bfab9a06e62149485df5f6
```

## 4. Sharp boundary control

With only three named neutral vertices, the clean-room formula is
satisfiable.  The hostile checker obtained a fresh CaDiCaL model and
verified every clause directly.

The retained labeled control `LDZZa^g|fkw[iH` was also evaluated by both
campaign implementations; they independently agree that

\[
(\gamma,i,\alpha,\gamma^\infty,\theta)=(3,3,3,3,3).
\]

Its 139-state eternal triple-family and all 1,390 unoccupied-attack
obligations are checked in the source package.  This is a colorable
boundary control, not a counterexample.  It proves that the finite
four-neutral statement cannot simply be strengthened to three neutral
vertices at order 13.

## 5. Reproduction and reviewer artifacts

From the campaign directory:

```text
python3 -I -B -W error \
  reviews/tight_micro_hostile_review/checker.py \
  --result reviews/tight_micro_hostile_review/result.json
```

The command reconstructs the production formula, runs both proof paths,
tests the exact closure gadget, and creates and validates a fresh
three-neutral SAT control.  Its final verdict is `PASS`.

