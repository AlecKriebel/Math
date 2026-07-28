# Hostile review: inactive induced-\(C_7\) attack exclusion

Review date: 2026-07-28 PDT

Frozen target:
`math/working/inactive_odd_cycle_generalization/NOTE.md`

Frozen target SHA-256:
`59b328983b2d240ec2b7aa078a474d9d4a1c18c307ceefd5a0c64da161997883`

Frozen certificate-manifest SHA-256:
`d5187e0a35595865f79063b02f74e6fa819aa5b0fe0b78c2c09bbdb15d148ee4`

Candidate reconstruction-checker SHA-256:
`3f6d65361f65bc79b27dc78fa8ab6a824dc706847db5c753a3688f94c632c78e`

Hostile clean-room checker SHA-256:
`b96b890843e3249355e65e6899ad55b255ef7c6529f6752a196e2cd548bd92be`

## Verdict

**UNCONDITIONAL PASS.**

For the frozen source and certificate bundle identified above, the local
inactive witnessed-\(C_7\) theorem is correct.  Consequently, under

\[
 \alpha(G)=\gamma^\infty(G)=3,\qquad \gamma(G-x)\ge3,
\]

the C-108 family-relative inactive graph

\[
 \overline{G-x}[R_x]
\]

has no induced \(C_7\).

Combining this theorem with the accepted C-108 triangle exclusion and the
accepted C-113 induced-\(C_5\) exclusion gives exactly the candidate's
stated boundary: in the equality-critical deletion branch, a remaining
inactive odd cycle has length at least nine.

This verdict does **not** exclude an inactive induced \(C_9\), exclude all
inactive odd cycles, prove inactive bipartiteness, prove the complete
\(k=3\) case, or resolve the gamma--theta conjecture.  The candidate
correctly leaves all of those statements open.  Its all-distinct-\(C_9\)
run remains an observation and was not used in this verdict.

I found no omitted witness collision, unsound symmetry quotient, occupied
attack, all-guards move, nonedge move in \(G\), missing retained successor,
missing domination condition, complement reversal, reliance on a greatest
family, or assumption that vertices outside the finite template cannot
matter.

## 1. Dependencies and the inactive-set reduction

I read and re-audited the complete statements actually used by the
candidate:

| dependency | reviewed source SHA-256 | use here |
|---|---|---|
| C-010 maximum-independent-state forcing | `08cfa394f5fb1778beac62d752ec2700027ac7710071ed635d9e914f71133e8e` | places every independent triple in every eternal triple-family |
| C-108 target-response propagation | `d6a0ec8a7daff1cca0094e1929134507364cea3c2c8781fbe24956a3238048d8` | makes active/inactive status independent of the containing maximum independent triple |
| C-113 inactive \(C_5\) certificate | `5ccd88e833db4794a834000a3f72e8ca32efbb339559800728ab0ef196861393` | supplies only the prior \(C_5\) part of the length-at-least-nine conclusion |

The corresponding accepted hostile reviews were also read.  No new
hypothesis is silently taken from them.

Let \(r_ir_{i+1}\) be a rim edge of an induced \(C_7\) in
\(\overline{G-x}[R_x]\).  Since
\(\gamma(G-x)\ge3\), the pair does not dominate \(G-x\).  There is
therefore a deletion vertex \(p_i\) nonadjacent in \(G\) to both endpoints.
Equivalently,

\[
 r_ip_i,\ r_{i+1}p_i\in E(\overline G).
\]

The witness is outside the pair because a member of a dominating pair
dominates itself.  It is not \(x\), because domination failed in \(G-x\).
It is not another rim vertex: consecutive vertices of an induced cycle of
length at least four have no common neighbor on that cycle.  Thus the only
possible identifications are equalities among the seven witnesses
themselves.

Each

\[
 T_i=\{r_i,r_{i+1},p_i\}
\]

is an independent triple of \(G\).  Under \(\alpha(G)=3\), C-010 puts
every \(T_i\) in the arbitrary eternal triple-family \(\mathcal F\).
Every rim endpoint is supported by such a triple.  Since it lies in
\(R_x\), C-108 says that its \(x\)-successor is absent from every containing
independent triple.  This gives precisely the fourteen absent successors
of the local theorem, with no assumption on the witness response.

The local certificate therefore applies.  The corollary does not require
\(\gamma(G)=3\), a clique-cover gap, connectedness, or a greatest eternal
family.  The deletion hypothesis \(\gamma(G-x)\ge3\), the equality
\(\alpha=\gamma^\infty=3\), and the word **induced** are essential to this
reduction and are all present in the candidate.

## 2. Complete witness-collision coverage

I did not use the candidate's restricted-growth-string generator.  The
hostile checker constructs set partitions by inserting each successive
edge position into an existing block or a new block, and then converts the
blocks to first-occurrence labels.  It obtains the Bell number

\[
 B_7=877
\]

with the independently expected Stirling-number distribution:

| witness blocks | patterns |
|---:|---:|
| 1 | 1 |
| 2 | 63 |
| 3 | 301 |
| 4 | 350 |
| 5 | 140 |
| 6 | 21 |
| 7 | 1 |

This covers every equality relation among
\((p_0,\ldots,p_6)\).  Section 1 proves that no identification with a rim
vertex or the target is admissible in the corollary, and the local theorem
explicitly assumes those vertices are outside.  There is consequently no
additional collision class to enumerate.

## 3. Independent derivation of the \(D_7\) quotient

I derived the action from automorphisms of the rim rather than copying the
candidate's sequence reversal.  If edge position \(i\) denotes
\(\{i,i+1\}\), the cycle vertex map

\[
 v\longmapsto \varepsilon v+c\pmod 7,\qquad
 \varepsilon\in\{1,-1\},
\]

sends edge position \(i\) to

\[
 \begin{cases}
 i+c,&\varepsilon=1,\\
 c-i-1,&\varepsilon=-1.
 \end{cases}
\]

After first-occurrence normalization of witness blocks, this independently
reconstructed the candidate's complete orbit map byte for byte.  It gave
93 orbits with distribution

| orbit size | number of orbits |
|---:|---:|
| 1 | 2 |
| 7 | 57 |
| 14 | 34 |

and

\[
 2\cdot1+57\cdot7+34\cdot14=877.
\]

For each of the 877 patterns, the checker found an explicit vertex
automorphism, extended it to the witness blocks and fixed the target.  It
then verified that this map carries all of the following to the canonical
representative:

- the seven rim \(H\)-edges;
- the fourteen rim \(H\)-nonedges;
- every witness spoke;
- every named retained triple; and
- every absent endpoint successor.

The domination and one-guard closure clauses are invariant under an
arbitrary vertex permutation, so this explicit hypothesis check validates
the full formula quotient.  No representative or orbit member was omitted.

## 4. Literal CNF audit

The hostile checker imports no candidate code.  It allocates all variables
and clauses directly from the definition and reconstructs every one of the
93 representative DIMACS files byte for byte.

For a template triple \(D\) and a template vertex \(y\notin D\), it
reconstructed:

1. a domination clause
   \[
   \neg f_D\vee
   \neg h_{yd_1}\vee\neg h_{yd_2}\vee\neg h_{yd_3};
   \]
2. one response marker for each current guard \(u\in D\);
3. the implication that a selected response has
   \(uy\notin E(H)\), equivalently \(uy\in E(G)\);
4. the implication that the exact one-swap successor
   \((D-\{u\})\cup\{y\}\) is retained; and
5. an existential choice clause whenever \(f_D\) is true.

The attack loop contains only \(y\notin D\), so all attacks are unoccupied.
Every marker names one current guard and one one-swap successor.  The CNF
does not impose at-most-one truth among alternative response markers.  That
is sound: the game asks for at least one legal single-guard response, and
several true markers represent several available alternatives, not
simultaneous motion.

Domination is imposed on every retained successor through the same global
family-variable clauses.  Vertices already in \(D\) require no separate
domination clause because an occupied vertex dominates itself.  The seven
named states force the family to be nonempty.

The independently reconstructed clause inventory is:

| clause group | clauses |
|---|---:|
| retained-state domination | 176,716 |
| unoccupied one-guard closure | 1,237,012 |
| induced-\(C_7\) rim | 1,953 |
| named witnesses and inactivity | 3,255 |
| **total** | **1,418,936** |

The formulas contain 3,539,528 literals.  The representative order
distribution is:

| template order | representatives |
|---:|---:|
| 9 | 1 |
| 10 | 8 |
| 11 | 31 |
| 12 | 33 |
| 13 | 16 |
| 14 | 3 |
| 15 | 1 |

All 373 files in the certificate directory are exactly the manifest and
the four named artifacts for each of the 93 representatives.  There is no
extra, missing, or unmanifested case file.

## 5. Why restriction to the finite template is sound

Suppose a larger graph and a real eternal triple-family satisfied the
local hypotheses.  On the template consisting of the rim, distinct
witnesses, and target, assign:

- each \(h_{uv}\) its actual complement-edge value;
- each \(f_D\) according to literal membership of that template triple in
  the real family; and
- for each retained template state and template attack, one marker
  corresponding to an actual legal response.

A retained real state dominates every template vertex.  A current guard in
a template state is itself a template vertex.  Therefore an attack at a
template vertex produces a one-swap successor whose three vertices are
still all in the template, and real closure says that successor is retained.

Attacks at vertices outside the template and edges incident with those
vertices are omitted.  This can admit additional assignments; it cannot
destroy an assignment induced by a real graph.  Hence the template is a
relaxation.  UNSAT of the template excludes the larger configuration.

## 6. Certificate integrity and replay

The hostile checker verified all manifest hashes for:

- every CNF;
- every DRAT proof;
- every solver log;
- every original checker log;
- the pinned CaDiCaL binary; and
- the pinned `drat-trim` binary.

It then invoked the pinned proof checker independently on every rebuilt
CNF/proof pair.  All 93 replays returned `s VERIFIED`.  The checked proof
bundle contains 1,739,039 bytes.  The decisive fact is the proof replay,
not the original solver's UNSAT status.

The binary hashes were:

```text
CaDiCaL:
51c3c82b354f455c925fc60b37c701e8498afcf0f3bfab9a06e62149485df5f6

drat-trim:
31df522b8b2b71acd357723b0e826cf488826ed78ad9e3a7bcad241271812beb
```

## 7. Human propagation statements

### 7.1 Private-star propagation

The candidate's Lemma 4.1 is correct for every \(k\).
Write

\[
 A=(E\cap T)-\{v\},\qquad O=E-T,\qquad B=T-E.
\]

The two \(k\)-states have equal size, so \(|O|=|B|\).  Begin at the
retained state \(E-v+x\) and attack the members of \(B\) sequentially.
Every already restored member of \(T-\{v\}\) misses the next attack because
\(T\) is independent.  If the guard at \(x\) moved, every guard in the
successor would lie in

\[
 (E\cup T)-\{v\},
\]

whose vertices all miss \(v\): this follows from the private-star
hypothesis for \(E\) and independence for \(T\).  The successor would not
dominate \(v\), so it cannot be retained.  Closure must remove one guard
from the remaining part of \(O\).  After \(|B|\) unoccupied attacks, the
state is exactly \(T-v+x\).

The proof does not choose an illegal mover or require uniqueness of the
response.  Whichever legal response closure provides maintains the
displayed invariant.

### 7.2 Distance-two exclusion

The candidate's Corollary 4.2 is also correct.  If
\(\{a,b,x\}\in\mathcal F\), attack the unoccupied vertex \(v\).  The
\(H\)-edges \(av,bv\) mean that neither \(a\) nor \(b\) can move in \(G\).
Closure therefore forces \(x\to v\) and retains \(\{a,b,v\}\).  This state
has the private-star property at \(v\), so Lemma 4.1 transports the
retained \(x\)-successor to the independent state \(T\), contradicting the
assumed inactivity.

In the intended rim application \(\mathcal F\) is a triple-family and
\(a,b,x,v\) are pairwise distinct.  Membership in a family of \(k\)-sets
makes the displayed three-set assertion substantive only at the matching
cardinality; no hidden higher-\(k\) conclusion is used.

### 7.3 Bounded hostile falsification

As a separate check, I enumerated all 1,099 labeled graphs through order
five, every guard number, and every one of the 60,011 arbitrary eternal
subfamilies, not merely greatest kernels.  The audit tested 64,222
private-star premises and 35,820 distance-two contexts.  It found zero
failures and no retained state forbidden by the distance-two corollary.

This finite audit supports but does not replace the proofs above.

## 8. Parity boundary and counterexample search

The theorem is not a generic artifact of overconstraining the family.
Independently of the CNFs, the hostile checker rebuilt the candidate's
positive construction for induced rims of lengths \(4,6,8\):

- even-indexed rim vertices form one \(G\)-clique;
- odd-indexed rim vertices form a second \(G\)-clique;
- all edge witnesses and the target form a third \(G\)-clique; and
- the family consists of all states with one guard in each clique.

The checker directly verified domination and every unoccupied attack in
families of 20, 63, and 144 states respectively.  Every named witness state
is retained, while both endpoint successors at the target are absent.  This
confirms that the local mechanism has the claimed odd/even boundary.

I also searched the collision coverage for ways a witness could coincide
with another named vertex.  Identifications among witnesses are exactly the
877 checked partitions.  Identifications with the target or rim contradict
the local hypotheses, and in the inactive-set corollary they are ruled out
by deletion and induced-cycle arguments before the certificate is invoked.
No omitted collision pattern remains.

No claim about \(C_9\) was audited as a theorem.  In particular, the one
all-distinct-\(C_9\) UNSAT run cannot cover the other 21,146 witness
partitions and is correctly labeled OBSERVED.

## 9. Reproduction

From the campaign directory:

```text
python3 -I -B -W error \
  reviews/inactive_c7_hostile/independent_check.py
```

The deterministic run reconstructs the full 877-pattern quotient, rebuilds
all 93 representative CNFs, replays all 93 DRAT proofs, validates the even
controls, and repeats the bounded human-lemma audit.  Its exact output is
recorded in `evidence.json`.
