# Nonsingleton full-list terminals: a rank-zero witness and a sharp control

## Status and exact scope

Date: 2026-07-28 (PDT)

This is a **candidate proof package**, not a campaign-accepted theorem.
The symbolic lemma below has a self-contained proof, and the finite control
has a clean independent verifier.  Independent hostile review is still
required before promotion.

The package establishes two sharply limited facts.

1. A rank-zero C-149 direct-root terminal cannot have a nonsingleton
   terminal root palette.  A rank-zero nonsingleton nonroot corridor
   instead forces a concrete nondomination witness for every secondary
   root color.
2. An exact equality graph realizes three simultaneous cyclic doubleton
   corridor rows with distinct movers and terminal vertices.  Two rows
   are genuine annihilation terminals, while the third is safe because
   its secondary response survives.  Thus the static three-corridor
   geometry alone is not a contradiction.

This does **not** exclude three empty color-restricted kernels.  It does
not prove that one color is safe, does not eliminate anchor-restoration
terminals, and does not close the gamma--theta conjecture.  No
literature-priority claim is made.

## 1. Setup and palette convention

Use the standard one-guard-moves game.  Let

\[
 \gamma(G)=\alpha(G)=\gamma^\infty(G)=3,\qquad H=\overline G,
\tag{1.1}
\]

let \(\mathcal F^\star\) be the literal greatest eternal family of
dominating triples, and let \(S=\{a,b,c\}\in\mathcal F^\star\) be an
independent triple.  Fix a full target \(x\notin S\):

\[
 S-u+x\in\mathcal F^\star\qquad(u\in S).
\tag{1.2}
\]

Put

\[
 B=N_H(x)
\tag{1.3}
\]

and, to avoid a collision with the physical-link palette used elsewhere,
write

\[
 Q(z)=L_S^{\mathcal F^\star}(z)
 =\{u\in S:uz\in E(G),\ S-u+z\in\mathcal F^\star\}.
\tag{1.4}
\]

Thus \(Q(z)\) is the **terminal root response palette**.  It is not the
C-139/C-141 palette that records triples \(\{x,s_i,z\}\).

For \(u\in S\), define the color ban

\[
 \mathcal B_u(x)=\{S-u+z:z\in B\}.
\tag{1.5}
\]

The synchronous restricted peeling begins with all dominating triples
outside \(\mathcal B_u(x)\).  Rank zero means deletion in its first
round.  A deletion-witness attack at a rank-zero state has no dominating
one-guard successor outside the ban.

C-149 supplies a retained decreasing-rank trace whenever the color-\(u\)
restricted kernel is empty.  Its final predecessor has finite rank, but
need not have rank zero: the trace can enter the ban at an earlier round.
The retained terminal successor has the form

\[
 E=S-u+r\in\mathcal F^\star\cap\mathcal B_u(x),
 \qquad r\in B.
\tag{1.6}
\]

Every such terminal satisfies \(u\in Q(r)\): the two anchors in \(S-u\)
are nonadjacent to \(u\), so the retained dominating state (1.6) forces
\(ur\in E(G)\), and (1.4) then applies.

## 2. The rank-zero secondary-response lemma

### Lemma 2.1 — PROVED in this candidate

Suppose a C-149 terminal entry (1.6) is made from a rank-zero predecessor
\(T\) under a deletion-witness attack.

1. If the entry is a direct-root corridor, then

   \[
   Q(r)=\{u\}.
   \tag{2.1}
   \]

2. If the entry is a nonroot corridor, write

   \[
   T=(S-u)+q,\qquad
   E=(S-u)+r,
   \tag{2.2}
   \]

   where the guard at \(q\) moves to the attacked vertex \(r\).
   For every secondary color

   \[
   v\in Q(r)\setminus\{u\},
   \tag{2.3}
   \]

   the alternate response

   \[
   A_v=(S-\{u,v\})+\{q,r\}
   \tag{2.4}
   \]

   is a legal triple outside \(\mathcal B_u(x)\), but it does not
   dominate \(G\).  Consequently there is a vertex \(w_v\) such that

   \[
   vw_v\in E(G),\qquad
   N_G[w_v]\cap A_v=\varnothing.
   \tag{2.5}
   \]

   The witness is locally collision-free:

   \[
   w_v\notin S\cup\{x,q,r\}.
   \tag{2.6}
   \]

   If \(Q(r)=S\), the two secondary colors require distinct witnesses.

#### Proof

For a direct-root corridor the predecessor is \(T=S\), and the guard at
\(u\) moves to \(r\).  If \(v\in Q(r)\setminus\{u\}\), then attacking
\(r\) also permits the guard at \(v\) to move, and the resulting state
\(S-v+r\) belongs to \(\mathcal F^\star\) by the definition of \(Q(r)\).
It is dominating and it lies outside \(\mathcal B_u(x)\), since it still
contains \(u\).  This is an available first-round successor, contrary to
the deletion-witness property at rank zero.  Hence no such \(v\) exists,
proving (2.1).

Now suppose the entry is the nonroot corridor (2.2), and choose \(v\) as
in (2.3).  The edge \(vr\) belongs to \(G\), so moving the guard at \(v\)
to the attacked vertex \(r\) is legal and has successor (2.4).
This state is not in \(\mathcal B_u(x)\): every state in that ban contains
all of \(S-u\), whereas \(A_v\) omits \(v\).  If \(A_v\) dominated \(G\),
it would therefore be present in the initial restricted peeling and
would answer the deletion-witness attack at \(T\).  Rank zero forbids
this, so \(A_v\) is nondominating.

Choose a vertex \(w_v\) missed by \(A_v\).  The predecessor \(T\) is a
dominating triple, and its only vertex absent from \(A_v\) is \(v\).
Therefore \(v\) must dominate \(w_v\), giving (2.5).

The missed vertex is not in \(A_v\).  It is not \(v\), because
\(r\in A_v\) and \(vr\in E(G)\).  The C-149 corridor diamond on
\(\{x,u,q,r\}\) has only \(xr\) missing: in particular \(uq,xq\in E(G)\).
Since \(q\in A_v\), neither \(u\) nor \(x\) can be missed.  These
observations give (2.6).

Finally, if the two anchors in \(S-u\) are both secondary colors, a
witness for one is nonadjacent to the other anchor because that anchor
lies in its alternate state.  A witness for the other is adjacent to that
anchor by (2.5).  The two witnesses are therefore distinct. \(\square\)

### Corollary 2.2 — PROVED in this candidate

Assume all three color-restricted kernels are empty and select one C-149
terminal trace per color **whose final predecessor has rank zero**.  If
all three selected terminal palettes are nonsingleton, then none of the
selected final entries is a direct-root corridor.

If, in addition, all three final entries are nonroot corridors, every
row has at least one witness satisfying (2.5)--(2.6).

This is a row-wise conclusion only.  Witnesses belonging to different
colors have not been proved distinct, and no cross-row contradiction is
claimed.

#### Proof

Apply the two parts of Lemma 2.1 to the three rank-zero rows. \(\square\)

## 3. Exact cyclic doubleton equality control

Consider the graph

```text
OQifur}UO]}iTij]tpo}v
```

with root and target

\[
 S=\{0,1,10\},\qquad x=6.
\tag{3.1}
\]

The clean verifier recomputes

\[
 (\gamma,\alpha,\gamma^\infty,\theta)=(3,3,3,3),
 \qquad |\mathcal F^\star|=304,
\tag{3.2}
\]

and verifies that \(S\) is independent and \(x\) is full.  The physical
link is

\[
 B=\{5,7,9,11,13\},
\tag{3.3}
\]

with induced \(H[B]\)-edges

\[
 5\,7,\quad 5\,9,\quad 11\,13.
\tag{3.4}
\]

The relevant terminal root palettes are cyclic doubletons:

\[
 Q(11)=\{0,1\},\qquad
 Q(7)=\{1,10\},\qquad
 Q(5)=\{0,10\}.
\tag{3.5}
\]

The three selected starts each reach a named nonroot-corridor predecessor
in one move.  The terminal rows are:

| color | selected start and predecessor | terminal move | secondary response |
|---|---|---|---|
| \(0\) | \(\{1,6,10\}\xrightarrow{14}\{1,10,14\}\) | \(14\to11\), terminal \(\{1,10,11\}\) | \(1\to11\) gives \(\{10,11,14\}\), missing exactly \(8\) |
| \(1\) | \(\{0,6,10\}\xrightarrow{3}\{0,3,10\}\) | \(3\to7\), terminal \(\{0,7,10\}\) | \(10\to7\) gives the safe state \(\{0,3,7\}\) |
| \(10\) | \(\{0,1,6\}\xrightarrow{12}\{0,1,12\}\) | \(12\to5\), terminal \(\{0,1,5\}\) | \(0\to5\) gives \(\{1,5,12\}\), missing exactly \(4\) |

For colors \(0\) and \(10\), the restricted kernels are empty.  Their
selected starts have rank one, their displayed predecessors have rank
zero, and their displayed terminal attacks are the final
deletion-witness attacks.  The peeling-round sizes are respectively

\[
 (26,81,132,62),\qquad (29,81,128,62).
\tag{3.6}
\]

For color \(1\), the restricted kernel has \(150\) states.  Both its
selected start and displayed predecessor survive, and the secondary state
\(\{0,3,7\}\) belongs to that kernel.  Its finite deletion rounds have
sizes

\[
 (28,74,49).
\tag{3.7}
\]

Each quartet

\[
 (6,0,14,11),\quad(6,1,3,7),\quad(6,10,12,5)
\tag{3.8}
\]

is the exact C-149 diamond, with only the target--terminal edge missing.
The verifier also performs a full occupancy audit: the root vertices,
target, three movers, three terminal vertices, and the two rank-zero
private witnesses are twelve pairwise-distinct vertices.

### Proposition 3.1 — EXACT FINITE CONTROL

The equality parameters, a full independent root, three retained nonroot
corridor diamonds with distinct colors, movers, and terminal vertices,
cyclic doubleton terminal root palettes, and the associated local
occupancy relations do not by themselves imply a contradiction.

Any valid elimination of the all-three-empty nonsingleton corridor branch
must use information absent from this static geometry, such as the third
deletion-witness condition or a consequence genuinely requiring all three
restricted kernels to be empty.

#### Certification

The graph above realizes every listed static hypothesis.  The same exact
replay shows why it is only a boundary control: colors \(0\) and \(10\)
are annihilated, but color \(1\) has a \(150\)-state restricted kernel
containing its secondary response.  Hence the graph refutes a
rank-free/static elimination but does not realize the all-three-empty
hypothesis.

Run the standalone replay from the campaign root:

```text
python3 -I -B -W error \
  math/working/full_list_nonsingleton_terminal/verify_cyclic_corridor_control.py
```

It imports no campaign implementation.  It decodes the graph, recomputes
all four parameters and the unrestricted greatest family, performs all
three restricted peelings, verifies every named move, palette, rank,
diamond, missed vertex, and collision assertion, and emits a JSON audit.

## 4. Status separation and remaining frontier

### PROVED in this candidate

- The rank-zero direct-root nonsingleton exclusion, Lemma 2.1(1).
- The row-wise private-witness conclusion for a rank-zero nonsingleton
  nonroot corridor, Lemma 2.1(2).
- The consequent removal of direct-root entries from an all-nonsingleton
  **rank-zero** selected terminal triple, Corollary 2.2.

### EXACT finite control

- Proposition 3.1 and every numerical or incidence assertion in
  Section 3 are checked by the independent verifier.

### CANDIDATE promotion status

- This package has not yet received an independent hostile review and is
  not a campaign theorem.

### OPEN

- A contradiction when all three restricted kernels are empty and all
  three selected nonsingleton terminals are nonroot corridors.
- Control of nonsingleton final entries whose predecessor has positive
  deletion rank.
- Cross-row control of the private-witness identifications.
- Nonsingleton anchor-restoration terminals.
- Any proof that a safe color exists in the full residual branch.

No pairwise elimination, safe-color existence, or unproved reciprocity is
used here.
