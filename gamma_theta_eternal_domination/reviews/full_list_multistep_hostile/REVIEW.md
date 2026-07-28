# Hostile audit: the first full-list multi-step constraint

## Verdict

Date: 2026-07-28 (PDT)

\[
\boxed{\texttt{PASS}}
\]

The two-attack retained-palette theorem, spoke independence, and the
conditional two-spoke component theorem in the candidate note are correct.
The proof uses genuine one-guard family closure, not merely adjacency or
domination of proposed successors.  A clean-room integer-bit-mask checker
independently reconstructed all three named controls, the greatest eternal
triple-families, every second-attack failure, the component signatures, and
the exact parameters needed to police the examples' scopes.

The audited candidate manifest has SHA-256

```text
fc35e58e2d96f9a7dc96d359fa601dc6083932ca8d899256db629e57869fb705
```

All six files listed by that manifest match their recorded hashes.

This result is a real new dynamic restriction, but it does not finish the
full-list branch.  Anchorless vertices in \(B\), the residual dynamically
inactive set \(R_x-B\), and synchronization among distinct component
palettes remain open.

## 1. Quantifier and model audit

Write \(H=\overline G\), let
\(S=\{s_0,s_1,s_2\}\in\mathcal F\) be independent in \(G\), and suppose
that an attack at \(x\notin S\) admits all three family responses

\[
D_j=S-\{s_j\}+\{x\}\in\mathcal F.
\]

Put \(B=N_H(x)\).  For every \(b\in B\):

- \(b\ne x\), because \(H\) is loopless;
- \(b\notin S\), because every \(s_jx\) is a \(G\)-edge;
- hence \(b\) is unoccupied in every \(D_j\); and
- the guard on \(x\) cannot answer at \(b\), because \(xb\notin E(G)\).

Thus every second attack used in the proof is legal, and every proposed
response must move exactly one of the two remaining root guards along a
single \(G\)-edge.  No occupied attack, all-guards move, complement-side
move, or stationary reconfiguration is hidden in the argument.

The first assertion also has the correct universal quantifier.  If
\(b\in B\) had two \(H\)-neighbors among the three anchors, omit the
remaining anchor when forming \(D_j\).  Then \(b\) would be a common
\(H\)-neighbor of all three members of \(D_j\), contradicting the fact
that this retained state dominates \(G\).  Therefore a \(B\)-vertex has
at most one root anchor in its \(H\)-neighborhood and the three spokes
\(B_i=B\cap N_H(s_i)\) are pairwise disjoint.

## 2. Retained-palette theorem

For \(b\in B\), define

\[
P(b)=\{i:\{x,s_i,b\}\in\mathcal F\}.
\]

Suppose first that \(b\in B_q\).  For \(j\ne q\), the state \(D_j\)
contains \(s_q\) and a third anchor \(s_t\).  The guard at \(s_q\) is
blocked, the guard at \(x\) is blocked, and the at-most-one-anchor result
makes \(s_tb\) a \(G\)-edge.  Closure therefore forces the unique reply

\[
s_t\longrightarrow b,\qquad
D_j-\{s_t\}+\{b\}=\{x,s_q,b\}\in\mathcal F.
\]

Consequently \(q\in P(b)\).  From \(D_q\), both non-\(q\) anchors can
move to \(b\); closure retains at least one successor whose stationary
anchor is not \(q\).  Hence \(|P(b)|\ge2\).

If \(b\) is anchorless, all root anchors can move to \(b\).  A palette of
size zero or one fails from the state \(D_q\) that omits its sole palette
index \(q\) (choose any \(q\) in the empty case).  Thus
\(|P(b)|\ge2\) here as well.  This confirms both the mandatory own-anchor
claim for spoke vertices and the palette-size claim for every member of
\(B\).

Finally,

\[
\{x,s_i,b\}\text{ dominates }G
\quad\Longleftrightarrow\quad
N_{H[B]}(b)\cap B_i=\varnothing.
\]

Indeed, every common \(H\)-neighbor of the displayed triple must first
lie in \(N_H(x)=B\), and the remaining two adjacency requirements say
exactly that it lies in the displayed intersection.  Since every member
of \(P(b)\) names a retained, hence dominating, state,

\[
i\in P(b)\Longrightarrow
N_{H[B]}(b)\cap B_i=\varnothing.
\]

Taking the mandatory index \(q\) for \(b\in B_q\) proves that each spoke
is independent.  Taking any two indices in \(P(b)\) proves that the
\(H[B]\)-neighbors of \(b\) meet at most one root spoke.  This last
statement deliberately does not forbid neighbors in the anchorless set
\(B_*\).

The independent checker exhausts all \(8\) possible root-anchor
incidence masks and all \(8\) possible retained palettes.  Across all
\(64\) patterns, direct closure under the three states \(D_j\) agrees
exactly with

\[
|N_H(b)\cap S|\le1,\qquad |P(b)|\ge2,\qquad
N_H(b)\cap S\subseteq\{s_i:i\in P(b)\}.
\]

## 3. Family versus static palettes

The distinction between

\[
P(b)=\{i:\{x,s_i,b\}\in\mathcal F\}
\]

and

\[
Q(b)=\{i:\{x,s_i,b\}\text{ dominates }G\}
\]

is maintained correctly.  The proof of the dynamic theorem uses
membership in \(P(b)\).  The separate truth-table statement about merely
dominating second successors uses \(Q(b)\), and the candidate only claims
the logically necessary inclusion \(P(b)\subseteq Q(b)\).

For a spoke vertex \(b\in B_q\), direct examination of all three
first-successor states gives

\[
\text{all attacks at }b\text{ have a dominating reply}
\quad\Longleftrightarrow\quad
q\in Q(b)\text{ and }|Q(b)|\ge2.
\]

For an anchorless vertex it gives the exact condition
\(|Q(b)|\ge2\).  No static successor is silently promoted to a retained
family state.

## 4. Conditional component conclusion

Assume in addition that \(H[B]\) has no isolated vertex and that

\[
B=B_0\mathbin{\dot\cup}B_1\mathbin{\dot\cup}B_2.
\]

Every component contains an edge \(bc\).  Spoke independence puts its
endpoints in distinct spokes \(B_i,B_j\).  The neighbor restriction then
forces every neighbor of a \(B_i\)-vertex into \(B_j\), and every neighbor
of a \(B_j\)-vertex into \(B_i\).  Induction along paths shows that the
entire connected component uses exactly those two spoke classes, which
are its two bipartition sides.  Connectedness gives uniqueness of the
unordered signature \(\{i,j\}\).

The assumptions are essential and are stated:

- total domination supplied by the C-127 target condition rules out
  isolated vertices of \(H[B]\);
- the separate hypothesis \(B=B_0\dot\cup B_1\dot\cup B_2\) rules out
  anchorless physical inactive vertices; and
- the conclusion concerns \(B=N_H(x)\), not the potentially larger
  family-inactive set \(R_x\).

Coloring the \(B_i\)-side with the root color of \(s_j\), and vice versa,
is proper on \(H[S\cup B]\).  This is only a local component palette; the
candidate does not claim that different palettes already synchronize or
extend through all of \(H-x\).

## 5. Independent reconstruction of the controls

### C-123

For

```text
G = IxU[ISrXW
```

with target \(x=9\) and root \(\{1,5,8\}\), the checker found

\[
B=\{0,3,4,6\},\qquad
B_1=\{3,6\},\quad B_5=\varnothing,\quad B_8=\{0,4\}.
\]

Both \(36\) and \(04\) are edges of \(H[B]\), so two spokes fail the
necessary independence conclusion.  The triple kernel starts with 58
dominating states, removes \(36\) and then \(22\), and is empty; the root
has deletion rank two.  Exact target parameters are

\[
(\gamma,i,\alpha,\gamma^\infty,\theta)=(2,3,3,4,4).
\]

Thus C-123 is correctly used only as an earlier static control, not as an
instance satisfying the new family hypotheses.

### C-128

For

```text
G = KxU[ISrR}NP^
```

with \(x=11\) and root \(\{0,4,8\}\), the checker found

\[
B=\{1,2,3,5\},\qquad
B_0=\{3\},\quad B_4=\{2\},\quad B_8=\{1,5\}.
\]

The edge \(15\in E(H[B])\) violates spoke independence.  Direct
domination testing gives

\[
Q(1)=\{4\},\qquad Q(5)=\{0\}.
\]

There are exactly four root-successor/physical-inactive attack pairs with
no legal dominating reply:

\[
\begin{array}{c|c|c}
\text{first removed guard}&\text{state}&\text{second attack}\\ \hline
0&\{4,8,11\}&1\\
0&\{4,8,11\}&5\\
4&\{0,8,11\}&1\\
4&\{0,8,11\}&5.
\end{array}
\]

In particular, from \(\{4,8,11\}\) attacked at \(1\), both the guard on
\(11\) and the guard on \(8\) are physically blocked.  The sole move is
\(4\to1\), producing the non-dominating state \(\{1,8,11\}\), which
misses \(5\).  All vertices attacked here are unoccupied, and the listed
move follows one \(G\)-edge.

The triple kernel has deletion waves \(47,56,3\), is empty, and assigns
the root rank three.  Exact target parameters are

\[
(\gamma,i,\alpha,\gamma^\infty,\theta)=(3,3,3,4,4).
\]

This confirms the candidate's precise conclusion: C-128 passes the
static and one-step boundary but fails the first genuinely multi-step
condition.

### Equality control

For

```text
G = Ksv`f\knJVis
```

with \(x=0\) and root \(\{1,2,3\}\), exact computation gives

\[
(\gamma,i,\alpha,\gamma^\infty,\theta)=(3,3,3,3,3).
\]

All 127 dominating triples survive in the greatest eternal family.  The
physical inactive set and spokes are

\[
\begin{aligned}
B&=\{6,8,10,11\},\\
B_1&=\{6\},\qquad B_2=\{11\},\qquad B_3=\{8,10\}.
\end{aligned}
\]

The retained palettes are

\[
\begin{aligned}
P(6)&=\{1,2\},&P(8)&=\{2,3\},\\
P(10)&=\{1,3\},&P(11)&=\{1,2\}.
\end{aligned}
\]

The two \(H[B]\)-components are the edges \(68\) and \(10\,11\), with
spoke signatures \(\{1,3\}\) and \(\{2,3\}\), respectively.  Hence the
example genuinely realizes different component signatures while
satisfying every conclusion of the theorem.  Its target deletion has
\(\gamma(G-x)=2\), so it is correctly excluded from the
equality-critical deletion branch of C-127.

## 6. Claim boundary

| Statement | Status after audit |
|---|---|
| two-attack retained-palette theorem | `PROVED` |
| independence of every root spoke | `PROVED` |
| conditional two-spoke component/bipartition theorem | `PROVED` |
| C-123 and C-128 fail the new condition | `PROVED` |
| equality control realizes two component signatures | `PROVED` |
| \(2^{19}\) extension sweep in the candidate | `OBSERVED` only |
| elimination of anchorless \(B\)-vertices | `OPEN` |
| control of \(R_x-B\) | `OPEN` |
| global component-palette synchronization | `OPEN` |
| complete \(k=3\) theorem | `OPEN` |
| universal \(\gamma\)--\(\theta\) conjecture | `OPEN` |

## 7. Reproducibility

The clean-room checker uses integer adjacency masks, a separately written
short-graph6 decoder, direct subset search, a fresh coloring search, and
a fresh synchronous greatest-fixed-point implementation.  It imports no
candidate or campaign evaluator.  From the campaign root, run:

```text
python3 -I -B -W error \
  reviews/full_list_multistep_hostile/independent_checker.py
```

The checker rewrites `result.json` byte-for-byte and prints that JSON followed
by a final `sha256 ...` line.  The printed JSON prefix is therefore
byte-identical to `result.json`; the complete standard output has one
additional hash line.
