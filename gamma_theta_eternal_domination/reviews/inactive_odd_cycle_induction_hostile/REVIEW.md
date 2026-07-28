# Hostile audit: inactive odd-cycle induction

## Verdict

**UNCONDITIONAL PASS.**

The frozen candidate proves the theorem it states:

1. for an odd witnessed path in the complement, the two absent endpoint
   responses at every witness state force the endpoint state
   \(\{r_0,r_n,x\}\) into every one-guard eternal triple-family;
2. the conclusion remains valid when witness vertices coincide;
3. the accepted distance-two exclusion converts this path theorem into
   exclusion of every witnessed inactive odd cycle; and
4. under
   \(\alpha(G)=\gamma^\infty(G)=3\) and \(\gamma(G-x)\geq3\), the
   C-108 inactive graph
   \[
   \overline{G-x}[R_x]
   \]
   is bipartite.

I found no illegal occupied-vertex attack, no all-guards move, no
unjustified conversion of family nonmembership into graph nonadjacency,
no parity or cycle-index error, and no defect in the repeated-witness
reduction.

This result does **not** prove that a coloring of the inactive graph
extends to a suitable coloring of all of \(\overline{G-x}\).  It therefore
does not prove the full-list branch, the complete \(k=3\) case, or the
universal gamma--theta conjecture.  The candidate states these limitations
correctly.

## Frozen candidate

The audit used these exact source artifacts.

| file | SHA-256 |
|---|---|
| `math/working/inactive_odd_cycle_induction/NOTE.md` | `ca8f655573575fefc1eb6e343950658c970e638aa66c62015647c784699a8d02` |
| `math/working/inactive_odd_cycle_induction/verify_induction.py` | `a0bec0c32de355ca7a8cf9dab01d0e2b6c0cb879084bad70f54d0e78884e277e` |
| `math/working/inactive_odd_cycle_induction/independent_result.json` | `83b81b9bfd94044bc8cd7b0cf8f9fccd613370c760bc91509d755d2b03d8e458` |
| `math/working/inactive_odd_cycle_induction/dead_state_saturation.py` | `2f34182a0c1219f65459c2e814e27651f0bd5bf1b7da82541b2bae93db70b47d` |
| `math/working/inactive_odd_cycle_induction/RESEARCH_LOG.md` | `22d146d5836009594b9ecd13a48c11959af186b2b6f6c151581c8acd23c833c0` |

The candidate verifier was rerun under isolated Python with warnings as
errors.  It reproduced the declared canonical payload hash

```text
26b4b16174f150ac87b97b5b9e48e26b0aca3f66cdfa88f8ae580d2ea931d06f
```

and all source hashes match the candidate manifest.

## Dependency audit

The final inactive-graph corollary uses three already accepted results.

| dependency | exact use | accepted source SHA-256 |
|---|---|---|
| C-010, maximum-independent-state forcing | puts every independent triple \(T_i\) into the chosen eternal triple-family when \(\alpha=\gamma^\infty=3\) | `08cfa394f5fb1778beac62d752ec2700027ac7710071ed635d9e914f71133e8e` |
| C-108, target-response propagation | makes inactivity of a rim vertex independent of the containing maximum independent triple and gives \(\omega(\overline{G-x}[R_x])\le2\) | `d6a0ec8a7daff1cca0094e1929134507364cea3c2c8781fbe24956a3238048d8` |
| C-115, private-star distance-two exclusion | forbids \(\{a,b,x\}\) when \(a,b\) are complement neighbors at distance two through an inactive rim vertex | `59b328983b2d240ec2b7aa078a474d9d4a1c18c307ceefd5a0c64da161997883` |

The new path theorem itself is independent of these results.  It needs
only the literal path nonedges, the named retained triples, the declared
absent successor states, and ordinary one-guard closure.

## Audit of the all-length parity-support induction

### Response rule

For a local triple \(S\) and an unoccupied target \(v\), the candidate
declares \(S\) absent only after checking every one of its three possible
movers.  A mover is rejected for exactly one of two reasons:

- its edge to \(v\) is one of the displayed graph nonedges; or
- the one-guard successor \(S-u+v\) has already been proved absent.

This is precisely the contrapositive of eternal-family closure.  Every
attack in the proof is at a vertex outside the current three-set.
Unspecified edges are never called nonedges.  Giving every unspecified
edge to the defender can only make a deletion harder, so the argument is
valid in every completion of the local template.

It is also legitimate to reason only about local triples.  Starting from
a local triple and attacking a local vertex creates another local triple;
no outside guard can appear in a one-guard successor.

### Leaf extension

For the induction step, write the last old rim edge as \(wz\), its witness
as \(h\), the new rim vertex as \(y\), and the new witness as \(p\).
The two retained independent witness triples force \(z\) to miss all of
\(w,h,y,p\) in \(G\).  The five layers are exhaustive and correctly
ordered.

1. Any triple in \(\{w,h,y,p\}\) dies under the unoccupied attack at
   \(z\), because all three possible move edges are absent.
2. The four bridge forms die under attacks at \(w\) or \(h\).  Each
   possible successor is either a Layer-1 state or an old
   parity-deficient state.  Degenerate displayed forms are already
   covered and are not attacked as multisets.
3. Every new triple missing the old-\(A\) side either contains \(w\) and
   is already a bridge state, or dies under attack at \(w\).  The cases
   with one and two new vertices both reduce to Layers 1--2 or the old
   induction hypothesis.
4. The seed \(\{z,h,p\}\) dies under attack at \(x\): its three candidate
   successors are respectively a Layer-3 state, the declared new-edge
   endpoint absence, and an old state missing \(B\).  Attacking \(h\)
   then deletes every \(\{z,p,d\}\) on the other side.
5. Every remaining new triple missing \(B\) contains \(p\) but not \(z\).
   Attack at \(z\); \(p\) is blocked and either other move reaches the
   Layer-4 family of absent states.

The old parity classes may be swapped to put \(z\) on the named \(A\)
side.  This does not alter the conclusion that every retained local
triple meets both original path parities.  No step depends on the path
length, so this is a genuine induction rather than an extrapolation from
the finite checker.

## Audit of odd endpoint forcing

The neutral-replacement lemma is correct.  From a hypothetical retained
\(\{a,b,q\}\), attack the unoccupied neutral vertex \(q_0\).  Moving
either rim guard produces a state missing one parity; moving the neutral
guard produces the assumed absent \(\{a,b,q_0\}\).

For odd \(n\), the endpoints \(r_0,r_n\) have opposite parity.  Assuming
\(\{r_0,r_n,x\}\) absent therefore propagates as follows.

1. Neutral replacement deletes
   \(\{r_0,r_n,q\}\) for every neutral \(q\).
2. The left witness \(p_0\), which misses \(r_0\), propagates this to
   every even-parity rim vertex paired with \(r_n\).
3. The right witness \(p_{n-1}\), which misses both
   \(r_{n-1}\) and \(r_n\), propagates across the odd side.
4. Repeating the left sweep from the right end deletes every triple with
   one vertex from each rim parity and one neutral vertex.

Every named witness triple has exactly that form, contradicting its
retention.  The \(n=1\) base is handled separately and correctly.  For
\(n\ge3\), all named vertices used as attack targets are distinct under
the distinct-witness hypothesis.

## Repeated-witness hostile audit

The adjacent-true-twin lift is sound; this was the highest-risk part of
the candidate.

For each original vertex \(v\), the construction replaces \(v\) by a
clique fiber \(C_v\), with complete or empty joins between fibers
according to the original adjacency.  The lifted family contains exactly
the triples selecting one clone from each of three distinct fibers whose
projections form a state of the original family.

### Domination

If a fiber is unoccupied, domination of its original projection supplies
an occupied neighboring fiber, and the complete join dominates every
clone.  If a fiber is occupied, the occupied clone dominates itself and
all its siblings because the fiber is a clique.

### Closure

There are exactly two attack cases.

- If the attacked clone lies in an unoccupied fiber, project the attack
  to the original graph, use one original legal response, and move the
  corresponding occupied clone across the complete join.  The new
  projection is the original successor and remains injective.
- If the attacked clone is an unoccupied sibling in an occupied fiber,
  move the occupied sibling directly along the fiber edge.  The
  projection is unchanged, and the lifted family contains every clone
  choice for that projection.

Thus attacks remain restricted to unoccupied vertices, exactly one guard
moves, and every move uses a graph edge.

Assigning one clone to each occurrence makes the witnesses pairwise
distinct.  The named triples remain independent because witness fibers
retain all original nonadjacencies to their rim endpoints.  A forbidden
lifted endpoint successor would project to its forbidden original
successor.  Finally, the path vertices and \(x\) cannot be witness
vertices under the theorem's hypotheses, so their fibers are singletons;
membership of the forced endpoint state in the lifted family projects
back exactly.

This reduction works for arbitrarily large witness multiplicities.  It
does not assume that an attacked occupied original vertex is legal:
attacks at a new unoccupied sibling are handled by the separate
within-fiber move above.

As a clean-room finite stress test, `independent_check.py` exhausts all
64 labeled graphs on four vertices, finds 361 arbitrary eternal
triple-families, and verifies all 1,444 one-vertex adjacent-true-twin
lifts.  It checks domination and every unoccupied one-guard obligation
directly.

## Cycle-to-path indices

Let the inactive odd cycle have vertices
\[
r_0,r_1,\ldots,r_{\ell-1}
\]
with \(\ell\ge5\) odd.  At
\(v=r_{\ell-1}\), its two cycle neighbors in the complement are
\[
a=r_0,\qquad b=r_{\ell-2}.
\]
One named witness state containing \(v\), together with inactivity of
\(v\) at \(x\), supplies the premise of the accepted distance-two
corollary.  It gives
\[
\{r_0,r_{\ell-2},x\}\notin\mathcal F.
\]

Delete the vertex \(r_{\ell-1}\) from the rim and retain the path
\[
r_0r_1\ldots r_{\ell-2}.
\]
This path has \(\ell-2\) edges, not \(\ell-1\); because \(\ell\) is odd,
\(\ell-2\) is odd.  Its witnesses are exactly
\(p_0,\ldots,p_{\ell-3}\).  The odd-path theorem forces the same endpoint
state that distance two forbids.  The indices and parity are correct.

## Reduction to the C-108 inactive graph

C-108 gives
\(\omega(\overline{G-x}[R_x])\le2\), so the inactive graph is
triangle-free.  If it is nonbipartite, a shortest odd cycle is induced
and has length at least five.

For each rim edge \(\{r_i,r_{i+1}\}\), the hypothesis
\(\gamma(G-x)\ge3\) gives a deletion vertex \(p_i\) missed by both
endpoints.  It cannot be either endpoint, cannot be \(x\), and cannot be
another rim vertex because the rim is induced.  Thus it is a valid
external witness.  The triple
\(\{r_i,r_{i+1},p_i\}\) is independent and has maximum size three, so
C-010 puts it in every eternal triple-family.  C-108 makes the two rim
endpoint responses at \(x\) absent.  Witness coincidences are permitted
by the lifting theorem.  All hypotheses of the local cycle exclusion are
therefore met.

No assumption that well-coveredness alone implies \(\gamma=\alpha\) is
made here.  The corollary is correctly stated under
\(\alpha=\gamma^\infty=3\) and the separate deletion domination
hypothesis.

## Independent computation

Run:

```text
python3 -I -B -W error \
  gamma_theta_eternal_domination/reviews/\
inactive_odd_cycle_induction_hostile/independent_check.py
```

The checker imports no candidate module and uses a queue-based deletion
engine different from the candidate's round-saturation implementation.
It treats every unspecified local edge as present and tests literal
unoccupied one-guard successors.

It independently checks all witness-equality patterns at odd path lengths
one, three, five, and seven:

| odd path length | witness partitions | endpoint forced |
|---:|---:|---:|
| 1 | 1 | 1 |
| 3 | 5 | 5 |
| 5 | 52 | 52 |
| 7 | 877 | 877 |

In the optimistic local response kernel, none of the 935 patterns loses a
named state from the endpoint-response boundary alone; after the
hypothetical endpoint absence, every pattern becomes contradictory.
This is not a claim that all 935 patterns have dominating realizations.
Distinct-witness even controls of lengths two, four, six, and eight retain
every named state after the endpoint is declared absent, checking the
parity boundary.

The canonical hostile payload hash is

```text
935409747c996842a75e63401466800e5696e928f82986c4e6a474c0e2eb72c8
```

The finite path audit does not establish arbitrary length.  That scope is
supplied by the separately audited human induction.  Conversely, the
candidate does not misrepresent its own finite checker as a replacement
for that proof.

## Scope firewall

The proved output is exactly inactive bipartiteness in the displayed
equality/deletion setting.  It does not prove any of the following:

- a proper three-coloring of all of \(\overline{G-x}\) that uses only two
  colors on \(R_x\);
- synchronization of projected colorings across active ridge components;
- the full-list branch;
- the complete \(k=3\) gamma--theta conjecture;
- any result for all \(k\); or
- a universal proof or counterexample for the gamma--theta conjecture.

The already accepted C-112 control shows why the first implication is
not automatic: local inactive colorability can coexist with global
deletion colorings that use all three colors on the inactive set.
