# Hostile review: distributed gate holonomy

## Verdict

**UNCONDITIONAL PASS.**

I found no mathematical error, model error, hidden graph-edge assumption,
scope overclaim, or computational mismatch in the final audited artifacts.
Theorem 2.1 and Corollary 3.1 are valid in the standard one-guard-moves
model exactly as stated.  The result is genuinely stronger than C-100 in
the separated two-gate direction, but it does not prove the universal
\(k=3\) case or resolve the gamma--theta conjecture.

The final source bytes audited here are:

| artifact | SHA-256 |
|---|---|
| `math/working/distributed_gate_holonomy/NOTE.md` | `e1bcfdf52379ffe7055932bbaa3e29d4f3f7934271703df9dcb5b4d20bb0cb9c` |
| `math/working/distributed_gate_holonomy/verify.py` | `52d7fef8c42a10ab4bdd8a3e44a8b3534b8e737aef812cfeb9877b8bd6253095` |
| `math/working/distributed_gate_holonomy/result.json` | `47cbc88bb765f009987ac360a9cedbf1be7e6cb2e6b8776839ac3c29abe7930c` |
| this review's `independent_check.py` | `c06775f6b19ceb4a6fd0f7c703b27f448b865d749d3245a28a11ea00217bc1f9` |
| this review's `evidence.json` | `0ba27529b0d51b34f3638ac15cf2c2b4837444b0f8ba3160dcb11e21989c21d3` |

An earlier audit draft exposed one nonmathematical coverage mismatch: the
source stress checker initially excluded length-zero paths while its prose
said that it checked every case covered by Theorem 2.1.  The source was
corrected by extending the checker, not by weakening the theorem or the
prose.  The final checker now includes the zero-length cases and the final
counts below reproduce exactly.  I also requested an explicit bridge from
the vertex-disjoint corollary to the "at least three gates remain" claim;
that bridge is now present in Section 4 and is correct.

## Line-by-line mathematical audit

### Definitions and the one-way response implication

The note fixes an independent retained state
\(S=\{a,b,c\}\), uses \(H=\overline G\), and defines

\[
L(t)=\{u\in S:S-u+t\in\mathcal F\},\qquad
W_u=\{t\notin S:u\notin L(t)\}.
\]

The only graph-edge inference made from a response list is the valid
forward implication

\[
u\in L(t)\Longrightarrow ut\in E(G).
\]

Indeed, the retained state \(S-u+t\) must dominate the omitted anchor
\(u\), and the other two anchors cannot dominate \(u\) because \(S\) is
independent.  The note never uses the invalid converse
\(u\notin L(t)\Rightarrow ut\in E(H)\).

### Dead-state Lemmas 1.1--1.3

All three lemmas are valid family-membership statements.

For Lemma 1.1, from a hypothetical retained state
\(\{h,r,s\}\), the attack at the other anchor \(d\) is unoccupied.  The
guard at \(h\) cannot move because \(hd\notin E(G)\).  Moving either
outside guard, if its move edge exists, gives one of the absent direct
states \(S-u+r\) or \(S-u+s\).  These exhaust the three possible
one-guard responses.

For Lemma 1.2, attacking an anchor in \(S-\{u\}\) from three distinct
vertices of \(W_u\) makes every possible successor a state already
excluded by Lemma 1.1.  Again, absent move edges only remove response
options.

Lemma 1.3 is a sound induction on an even path in \(H[W_u]\).  The
length-two base case uses the two literal complement edges to block the
endpoint guards and Lemma 1.2 to exclude a move by the third guard.  In
the induction step, the three possible successors are excluded,
respectively, by Lemma 1.2, the length-two case, and the shorter even-path
induction hypothesis.  The condition that \(p\) is outside the path is
exactly what keeps every attacked vertex unoccupied and every displayed
configuration a three-set.

No domination conclusion is silently inferred from a missing family
state in these lemmas.

### The two forced corner states

The first half of Theorem 2.1 can be reconstructed without any omitted
move:

| retained state and attack | excluded response 1 | excluded response 2 | forced response |
|---|---|---|---|
| \(\{b,c,x_0\}\), attack \(y_0\) | move \(x_0\): \(S-a+y_0\), absent since \(y_0\in W_a\) | move \(c\): \(\{b,x_0,y_0\}\), the first dead boundary | move \(b\): \(\{c,x_0,y_0\}\) |
| \(\{a,b,y_0\}\), attack \(x_0\) | move \(y_0\): \(S-c+x_0\), absent since \(x_0\in W_c\) | move \(a\): \(\{b,x_0,y_0\}\), the first dead boundary | move \(b\): \(\{a,x_0,y_0\}\) |

The starting states are retained by the two explicit hypotheses
\(a\in L(x_0)\) and \(c\in L(y_0)\).  If the nominally forced guard lacks
the needed graph edge, closure itself is contradicted; consequently
closure validly forces both the move edge and the successor state.

When \(n\ge1\), attacking \(y_1\) from
\(\{c,x_0,y_0\}\) blocks \(y_0\) on the displayed complement edge and
excludes an \(x_0\)-move by Lemma 1.1.  This forces
\(\{x_0,y_0,y_1\}\).  Attacking \(b\) there excludes an \(x_0\)-move by
Lemma 1.1 and a \(y_1\)-move by the first boundary condition, forcing
\[
\{b,x_0,y_1\}\in\mathcal F.
\]
The \(x\)-projection argument is the exact symmetric calculation and
forces \(\{b,x_1,y_0\}\) when \(m\ge1\).

Every attack in this construction is at a vertex outside the current
three-set, and every successor differs by exactly one guard.

### Two-step propagation and all parity cases

The propagation step is valid with precisely the stated disjointness
hypothesis.  From a retained state \(\{v_i,p,q\}\), where \(p,q\) are
outside the relevant omitted-color path, attack \(v_{i+2}\).  A move by
either outside guard leaves \(v_i\) and \(v_{i+2}\) together and is
excluded by Lemma 1.3 on the length-two subpath.  Closure therefore
forces the guard at \(v_i\) to move to \(v_{i+2}\).

The proof then covers every parity combination:

- if \(n\) is odd, it first obtains \(B_{0,n}\);
- if \(m\) is odd, it first obtains \(B_{m,0}\);
- an even path, including a length-zero path, propagates one of those
  states to \(B_{m,n}\);
- \(B_{m,n}\) contradicts the second dead boundary state.

The edge cases are complete.  If \(m=n=0\), the conclusion is tautological.
If exactly one length is zero and the other is odd, the initialized odd
corner is already the forbidden terminal boundary.  Length one is handled
by the explicit initialization, and every larger odd or even length is
handled by two-step propagation.

Vertex-disjointness is used, not decorative: it keeps the two outside
guards outside the path during propagation.  The theorem does not claim
the same statement for arbitrary intersecting paths.

Additional edges of \(H\) cause no hidden failure.  They can only remove
a candidate guard move.  Whenever the proof says closure forces the
remaining move, the retained starting state ensures that a response must
exist, so any extra complement edge blocking that final move would make
the hypotheses inconsistent rather than create a counterexample.

## Corollary 3.1

For each gate,

\[
L(x_i)=\{a,b\},\quad L(y_i)=\{b,c\}
\]
gives exactly

\[
x_i\in W_c,\quad a\in L(x_i),\qquad
y_i\in W_a,\quad c\in L(y_i).
\]

The three literal complement incidences

\[
bz_i,\ x_i z_i,\ y_i z_i\in E(H)
\]
show directly that \(\{b,x_i,y_i\}\) does not dominate \(z_i\).
Every retained family state dominates, so both boundary states required
by Theorem 2.1 are absent.  This derives both dead boundaries independently;
it does not infer a complement edge from a missing response.  Theorem 2.1
therefore applies verbatim.

The exact list of \(z_i\) is part of the tight-gate structure but is not
silently used to prove non-domination; the displayed complement edges are
the certificate.

## Scope relative to C-100

This result is genuinely more general than C-100 along one axis and does
not merely rename its odd-return corollary.

C-100 excludes an odd path in a single omitted-color projection when the
two gates have the particular shared physical port and the far endpoint
has the two literal complement incidences used by the odd two-cap fork.
The new corollary instead uses two independently supplied dead boundaries
and compares two corresponding projection paths.  Both paths may have
positive length, so all four connector endpoints can be physically
distinct.  It does not need the shared port required by C-100, and its
second boundary comes from the second gate's own tight cap.

Conversely, the new theorem does not subsume every C-100 geometry: C-100
allows the second gate to use a different distinguished cap type and
uses a different endpoint-incidence pattern.  The two results are
properly described as complementary.

## Exact remaining gate-holonomy case

The added Section 4 scope bridge is sound.  In the no-full branch every
outside response list is nonempty and proper.  If a \(W_c\) connector and
a \(W_a\) connector share a physical vertex \(v\), then \(a,c\notin L(v)\),
so nonemptiness forces \(L(v)=\{b\}\).  Such a singleton supplies a unit
and fixes the relevant projection components.  Therefore two distinct
free connector components occurring in a unit-free bicycle are physically
vertex-disjoint, exactly as Corollary 3.1 requires.

It follows that the corollary eliminates an odd signed bigon formed by
two tight gates in that unit-free/free-component branch.  The remaining
target in this gate-holonomy lane is an inclusion-minimal odd signed cycle
through at least three tight gates.  Between two successive gates there
is only one monochromatic connector; the alternate route traverses other
gates and changes omitted color, so it is not a path contained in one
\(W_u\) and Theorem 2.1 cannot be applied to it.

This is an exact description of what remains **within the tight-gate
unit-free holonomy lane**.  It is not a claim that all other universal
\(k=3\) branches, the full-list branch, or the gamma--theta conjecture
have been settled.

## Independent computation

`independent_check.py` imports no campaign evaluator and no source
transition routine.  It independently:

1. decodes each graph6 record into integer adjacency masks;
2. checks connectedness;
3. enumerates dominating triples;
4. rebuilds the greatest one-guard triple kernel directly from the
   definition;
5. computes exact \(\gamma,i,\alpha,\theta\), using exhaustive sets and a
   fresh saturation-first coloring search on the complement; and
6. enumerates all oriented simple omitted-color path pairs and checks the
   hypotheses and parity conclusion.

The four controls independently reconstructed as follows:

| graph6 | \(n\) | dominating triples | kernel deletions | greatest family | attack obligations | \((\gamma,i,\alpha,\gamma^\infty,\theta)\) | positive-length pairs | all pairs, including length zero |
|---|---:|---:|---:|---:|---:|---|---:|---:|
| `LFzJbZYhdrDZdM` | 13 | 144 | 2 | 142 | 1,420 | \((3,3,3,3,3)\) | 40 | 86 |
| `MFzJbZYhlrDZdMhd_` | 14 | 182 | 5 | 177 | 1,947 | \((3,3,3,3,3)\) | 72 | 150 |
| `NFzJbZZhlrDZdMhd|h_` | 15 | 227 | 11 | 216 | 2,592 | \((3,3,3,3,3)\) | 120 | 246 |
| `MEXrtIdmdjLQqztC?` | 14 | 172 | 0 | 172 | 1,892 | \((3,3,3,3,3)\) | 204 | 396 |

Thus the independent positive-length subtotal is 436, and the final
zero-inclusive total is

\[
86+150+246+396=878.
\]

Every one of the 878 qualifying pairs has equal parity.  Since the paths
lie outside three anchors and the largest control has order 15, a simple
path has length at most 11; the cutoff 14 is therefore exhaustive for
these controls, not a truncation.

The source replay

```text
python3 -I -B -W error \
  math/working/distributed_gate_holonomy/verify.py \
  --max-length 14 \
  --check math/working/distributed_gate_holonomy/result.json
```

also passes on the final bytes.

As a hostile hypothesis-ablation check, the equality controls contain 636
opposite-parity pairs when only the terminal boundary-absence condition is
dropped, and 706 when only the initial boundary-absence condition is
dropped.  Hence both dead boundaries are substantive and cannot simply be
removed from the theorem.  The controls contain same-parity qualifying
geometries, including length-zero examples, so the theorem also cannot be
strengthened to forbid the boundary geometry itself.

I additionally replayed the discovery formulas for all 25 pairs of path
lengths \(1\le m,n\le5\), both with and without the optional
\(\gamma\ge3\) constraints.  In both sweeps every same-parity instance was
SAT and every opposite-parity instance was UNSAT, matching the stated
discovery table.  These bounded SAT runs are only a stress check; the
universal human proof is independent of them.

## Final assessment

The proof respects every one-guard modeling requirement:

- attacks are only at unoccupied vertices;
- exactly one adjacent guard moves;
- every successor asserted to be in the family is a three-set;
- retained-state domination is used in the correct direction;
- \(G\) and \(H=\overline G\) are never confused;
- missing family membership is never treated as graph nonadjacency; and
- no hypothesis on \(\gamma(G)\), coloring, or equality is smuggled into
  the universal attack theorem.

There are no remaining publication-blocking issues in the audited final
version.
