# Hostile review: positive-rank full-list terminals

## Verdict

Date: 2026-07-28 (PDT)

\[
\boxed{\texttt{UNCONDITIONAL PASS}}
\]

I reviewed the theorem bytes in
`math/working/full_list_positive_rank_terminal/CANDIDATE.md` at SHA-256

```text
e25845bbf5e23886284f2046ac8c5c661b48176f4bef9fda5651f733d4a0edb0
```

and the final control implementation at commit `8f002f62`.  The rank
lemmas, corridor dichotomy, minimum-rank normalization, positive-rank
anchor-restoration theorem, and four-way residual normal form are correct
at their stated scopes.

The package does **not** prove that a restricted kernel survives, does
not put a lower-rank restricted state into the unrestricted greatest
family, does not eliminate the four residual cases in Corollary 5.1, and
does not prove the complete \(k=3\) case or the gamma--theta conjecture.

## 1. Frozen dependencies

The three imported theorem packages are present at exactly the hashes
declared by the candidate.

| dependency | SHA-256 |
|---|---|
| C-149 retained descent and terminal gates | `a3a2fc44befb4084b783b73afe108e81af8b7ac3f20b0d34d00bfc35d1f4e62d` |
| C-154 singleton-terminal exclusion | `0d6eb44fa2807cd34e441c31364149577cccf39f28b426a5d81b7cc78c9d1253` |
| C-157 rank-zero nonsingleton corridor theorem | `0497d07b8cf2bf1f5e3572f35d400d954745abae4490e6cac707f15cbcaeb22c` |

C-149 supplies two facts used here.

1. When the color-\(u\) restricted kernel is empty, every retained
   unbanned state has a finite retained descent ending in a retained
   banned state.  Each unbanned step strictly lowers the synchronous
   restricted deletion rank.
2. The last transition is either a corridor entry or an
   anchor-restoration entry, with the exact occupancies used in the
   candidate.

C-154 is used only through its predecessor-independent endpoint theorem:
three retained ban states, one per color, cannot all have their respective
own-color singleton root palettes.  The minimum-rank endpoints selected
in Corollary 5.1 satisfy precisely those hypotheses.  No synchronization
of their ranks, attacks, or predecessors is assumed.

C-157 is used only to identify the already accepted rank-zero nonroot
corridor witness branch.  The positive-rank proofs do not smuggle its
rank-zero deletion condition into a later round.

## 2. Synchronous rank indexing

The candidate begins with all dominating triples outside the fixed ban:
\(\Omega _0\).  A state of rank \(h\) lies in
\(\Omega_h-\Omega_{h+1}\).  Therefore a deletion-witness attack at that
state has no successor in \(\Omega_h\).

If a legal successor dominates and avoids the ban, it lies in
\(\Omega_0\).  Empty terminal kernel then gives it a finite rank.  Its
absence from \(\Omega_h\) is equivalent to rank strictly below \(h\).
This proves Lemma 1.1 with no off-by-one shift.

For \(h>0\), the predecessor belongs to \(\Omega_1\).  Hence every
unoccupied attack has at least one successor in \(\Omega_0\).  A selected
retained successor inside the ban is not in \(\Omega_0\), so the
\(\Omega_0\)-successor is a genuinely different, dominating, unbanned
response.  Lemma 1.1 lowers its rank.  This proves Lemma 1.2.

This argument never claims that the lower-rank state lies in
\(\mathcal F^\star\).  That separation is essential and is maintained
throughout the candidate.

## 3. Corridor dichotomy

Write \(A=S-\{u\}\).  A corridor predecessor and terminal successor are

\[
T=A+q,\qquad E=A+r,
\]

with the attack at unoccupied \(r\) and the selected move \(q\to r\).
Because \(x\) is full, \(B=N_{\overline G}(x)\) is disjoint from \(S\).
The C-149 occupancies therefore make all displayed set differences
literal.

For \(v\in Q(r)-\{u\}\), the palette supplies the physical edge
\(vr\), and

\[
A_v=T-v+r
\]

omits the anchor \(v\).  Every \(u\)-ban state contains all of \(A\), so
\(A_v\) is unbanned.

### Direct-root case

Here \(q=u\) and \(T=S\).  The state \(A_v=S-v+r\) is retained by the
definition of \(Q(r)\), hence dominates.  Lemma 1.1 lowers its rank.  In
particular, the hypotheses are inconsistent at rank zero, so a
nonsingleton direct-root terminal necessarily has positive predecessor
rank.

### Nonroot case

If \(A_v\) dominates, Lemma 1.1 gives the claimed lower rank, but nothing
puts the state in \(\mathcal F^\star\).

If \(A_v\) does not dominate, choose a missed vertex \(w_v\).  The
retained predecessor \(T\) differs from \(A_v\) only by replacing \(v\)
with \(r\), so \(v\) is the only possible dominator of \(w_v\) from
\(T\).  The possibility \(w_v=v\) is excluded by \(vr\in E(G)\).
Thus \(vw_v\in E(G)\) and \(N_G[w_v]\cap A_v=\varnothing\).

The collision exclusions are complete:

- the vertices of \(A_v\) cannot be missed;
- \(v\) is adjacent to \(r\in A_v\); and
- the C-149 diamond gives \(uq,xq\in E(G)\), with \(q\in A_v\).

Hence \(w_v\notin S\cup\{x,q,r\}\).  When both anchors are secondary
colors, a witness for one misses the other anchor while every witness for
the other is adjacent to that anchor.  The two witness sets are therefore
disjoint, which is stronger than the asserted existence of distinct
witnesses.

For any positive-rank corridor, Lemma 1.2 supplies an unbanned alternate
to the same attack.  The selected mover \(q\) has the unique banned
successor \(E\); every other occupied guard is one of the two anchors in
\(A\).  Thus at least one anchor gives the asserted dominating
lower-rank alternate.  The move edge does not imply that the anchor is in
\(Q(r)\), since palette membership additionally requires a different
root state to be retained.

## 4. Minimum-rank descent

For a fixed color, C-149 makes the set of retained terminal entries
nonempty.  Choose an entry whose predecessor rank is minimum over all
such entries.

In a nonsingleton direct-root entry, a secondary response is retained,
unbanned, and has smaller rank.  Starting C-149's retained descent from
that response produces a terminal predecessor of rank at most the
response rank, contradicting the selected minimum.

The identical restart is valid for a nonroot alternate only if that
alternate belongs to \(\mathcal F^\star\).  Consequently, every
dominating lower-rank secondary alternate at a minimum-rank nonroot entry
is absent from \(\mathcal F^\star\).  At positive rank, the
palette-free compulsory anchor alternate is absent for the same reason:
if it were retained, its unbanned lower-rank state could restart the
descent.  The candidate's final bytes state this quantifier explicitly.

No step infers unrestricted family membership merely from domination or
restricted rank.

## 5. Anchor restoration

Use the candidate's notation

\[
S=\{u,a,c\},\quad
T=\{c,r,q\},\quad
E=\{a,c,r\}.
\]

The attacked vertex is the unoccupied anchor \(a\), and the selected
retained response is \(q\to a\).

When \(\rho_u(T)>0\), Lemma 1.2 forces a different unbanned response to
the same attack.  Guard \(c\) cannot move because \(S\) is independent,
and guard \(q\) has the already selected successor \(E\).  The only
remaining mover is the old terminal vertex \(r\).  Therefore

\[
ar\in E(G),\qquad
R=T-r+a=\{a,c,q\}.
\]

Lemma 1.2 says directly that \(R\) dominates and is unbanned; its
displayed shape then gives \(q\notin B\).  Lemma 1.1 lowers its rank.  At
a minimum-rank retained terminal, \(R\) cannot be retained, by the same
C-149 restart used in Section 4.

The attacked anchor need not lie in \(Q(r)\).  The proof uses the edge
\(ar\) forced by mover exhaustion, not a palette inference.

At rank zero, if \(ar\) is an edge, \(q\notin B\), and \(R\) is
nondominating, a vertex missed by \(R\) must be dominated from \(T\) by
the only removed guard \(r\).  It cannot equal \(r\) because \(ar\) is
an edge, and it cannot equal \(x\) because \(q\notin B\) gives
\(qx\in E(G)\).  This proves exactly the stated witness location.  The
possibility that the witness equals \(u\) is correctly left open.

## 6. Three empty kernels

Choose a minimum-rank terminal entry for each color.  Each successor is
a retained ban state \(S-u+r_u\), and domination of the omitted anchor
forces \(u\in Q(r_u)\).  C-154 rules out all three palettes being the
respective singletons.  At least one chosen entry is therefore
nonsingleton.

The minimum-rank direct-root exclusion removes that gate for every such
entry.  The two remaining C-149 gates, split by rank zero versus positive
rank, give exactly the four cases in Corollary 5.1:

1. rank-zero nonroot corridor;
2. positive-rank nonroot corridor;
3. rank-zero anchor restoration; or
4. positive-rank anchor restoration.

This is an exhaustive normal form, not an elimination of those cases.

## 7. Missing palette membership audit

Every use of \(v\in Q(r)\) is positive: it supplies both the move edge
\(vr\) and the retained root swap.  No use of \(v\notin Q(r)\) is turned
into \(vr\notin E(G)\).

In particular, the anchor-restoration proof derives \(ar\in E(G)\) from
the required alternate move even when \(a\notin Q(r)\).  The third exact
control realizes this distinction literally.

The only graph nonedges used in the universal proof are:

- root-anchor pairs, because \(S\) is independent;
- target--link pairs, by \(B=N_{\overline G}(x)\); and
- adjacencies absent by the definition of a missed vertex.

## 8. Independent exact replay

`independent_replay.py` imports no candidate or campaign module.  It uses
ordinary `frozenset` configurations, a fresh graph6 decoder, direct
exhaustive parameter checks, a DSATUR-style complement-coloring search,
and a separately written synchronous one-guard deletion routine.

Besides checking the three named records, it enumerates every retained
terminal entry for the named root, target, and color in each control.  It
checks the rank lemmas, gate classification, corridor diamonds, all
secondary-response branches, private-witness collisions, positive-rank
anchor mover exhaustion, and the minimum-rank nonretention conclusions.

The replay obtains:

| control | exact parameters | \(|\mathcal F^\star|\) | restricted rounds | terminal entries |
|---|---|---:|---|---:|
| `Ksv`f\knJVis` | \((3,3,3,3)\) | 127 | \(16,40,56,12\) | 25 |
| `JEhbtj{rvf?` | \((2,3,3,4)\) | 112 | \(18,29,38,28,1\) | 18 |
| `JEhbtj{ruv?` | \((2,3,3,4)\) | 112 | \(21,38,43,12\) | 30 |

The named equality entry is a genuine rank-one anchor restoration with a
retained rank-zero alternate.  It is not a minimum-rank terminal entry,
so it does not conflict with the minimum-rank nonretention theorem.

The first gamma-two boundary has the named rank-two nonroot corridor
alternate at rank one, dominating but outside
\(\mathcal F^\star\).  The second has

\[
4\notin Q(10)\quad\text{but}\quad 4\,10\in E(G),
\]

and the physical move \(10\to4\) reaches the retained rank-zero
alternate.  These verify the two logical boundaries claimed by the
candidate.

The independent replay's frozen stdout SHA-256 is

```text
26c5ef99ab8a6719135615c9fa0c9d5061628671add43fd2e2565c2dd8a58a00
```

## 9. Presentation caution

Section 6.1 calls \(8\to2\) a “secondary move.”  The endpoints are
correct: this is the alternate move by the old terminal guard \(8\), not
a move by the secondary palette color \(2\), which is the attacked
unoccupied anchor.  The theorem and the final control record identify the
mover correctly.  Reading “secondary” there as “alternate” avoids the
only terminological ambiguity I found.

## 10. Reproduction

From the campaign root:

```text
reviews/full_list_positive_rank_terminal_hostile/verify_strict.sh
```

The strict runner freezes the candidate and dependency bytes, reruns the
candidate controls, performs the independent replay, and checks its exact
output hash.
