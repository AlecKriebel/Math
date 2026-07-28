# Hostile review: third-color gate cycles and the odd two-cap fork

## Verdict

**PASS, at the exact stated scope.**

The odd two-cap fork theorem is a correct consequence of the standard
one-guard-moves definition.  Its proof uses neither
\(\gamma(G)=3\) nor any clique-coloring hypothesis.  It requires only an
independent retained triple \(S=\{a,b,c\}\), an eternal family of triples,
the displayed response-list inclusions and exclusions, distinctness of the
attacked vertices, and the stated complement edges.  Every attack is made
at an unoccupied vertex, and every possible response is a move by exactly
one adjacent guard.

The chirality table, tight-gate equality, connector parity, and type-word
holonomy calculation are also correct.  The theorem excludes a genuinely
new infinite subclass of physical unit-free bicycles: two tight
third-color gates sharing the required physical port and joined back to the
second cap by any odd path in one omitted-color projection.  It does
**not** exclude bicycles with separated physical representatives,
holonomy spread over several connector components, or a return path that
leaves the one omitted-color projection.

The 14-vertex equality control was independently reconstructed from its
labeled graph6 string.  It has

\[
  \gamma=i=\alpha=\gamma^\infty=\theta=3,
\]

and its greatest eternal triple-family consists of all 172 dominating
triples.  All 1,892 unoccupied-attack obligations were replayed.  The two
tight gates share vertex \(3\), and their return in \(B_a\) is the
length-two path \(6-5-11\).  This control sharply refutes the broader
claims that shared-port tight gates are impossible or that return parity
is irrelevant.

No universal \(k=3\) theorem and no resolution of the gamma--theta
conjecture follows.

## Frozen source bytes reviewed

| Artifact | SHA-256 |
|---|---|
| `math/working/third_color_gate_cycle/NOTE.md` | `ee25478bca1c05a4595f5a4a18cf92de87d12fb31338366821f043671f5e5259` |
| `math/working/third_color_gate_cycle/RESEARCH_LOG.md` | `bb18183cad967755768303fd811e29b121bd64c3e839c2140d3b97ce5b74d966` |
| `math/working/third_color_gate_cycle/probe.py` | `7b7dca56f1c4b4824bf4b461681b02e116e82cb0327ebdddfdb517dd3b4bf83a` |
| `math/working/third_color_gate_cycle/result.json` | `0a79b29a2c482a770f540f56d1ca6f3288b0cd251a57033cdf132fc0176ec573` |
| `math/working/third_color_gate_cycle/verify.py` | `05ad3836d9a395f4abb71da8c26013fddd5af672039861b7b047c41f1f5e3d77` |
| `reviews/third_color_gate_cycle_hostile/independent_check.py` | `fd9eb93f872515452d32d2bec67dffc999d94347ad6898f0092f5666ebef69ca` |
| `reviews/third_color_gate_cycle_hostile/evidence.json` | `da78d3ee846725e17ccb98a520940a6836a07cb4f0d8ce67c28080de2c705df2` |

These are the current source bytes reviewed.  The source did not change
during the audit interval after these hashes were pinned.

## One-guard proof audit

For \(t\notin S\), put

\[
 L(t)=\{u\in S:S-u+t\in\mathcal F\}.
\]

If \(u\in L(t)\), the retained state \(S-u+t\) must dominate \(u\).
The two other anchors miss \(u\), because \(S\) is independent, so
\(ut\in E(G)\).  No converse from a missing family state to a graph
nonedge is used anywhere in Section 4.

### Lemma 4.1

Assume \(a\notin L(r)\cup L(s)\), and consider a hypothetical retained
state \(\{h,r,s\}\), where \(\{h,d\}=\{b,c\}\).  Attack the unoccupied
anchor \(d\).

- The guard \(h\) cannot move to \(d\), since \(hd\in E(H)\).
- A move \(r\to d\) would produce
  \(\{h,d,s\}=S-a+s\), absent because \(a\notin L(s)\).
- A move \(s\to d\) would produce
  \(\{h,d,r\}=S-a+r\), absent because \(a\notin L(r)\).

These are all three guards, so closure fails.  The lemma is sound even
when either of the latter two move edges is absent; that only removes a
candidate response.

### Lemma 4.2

For a hypothetical retained state \(\{r,s,t\}\) of three
\(a\)-avoiding vertices, attack the unoccupied anchor \(b\).  Every
one-guard successor contains \(b\) and two of \(r,s,t\), hence is
excluded by Lemma 4.1 with \(h=b\).  Again, absent move edges only remove
responses.

### Lemma 4.3

For the length-two path \(v_0v_1v_2\) in \(H\), attack \(v_1\) from
\(\{p,v_0,v_2\}\).  The two endpoint guards cannot traverse the
displayed complement edges.  Moving \(p\), if legal, gives the
three-\(a\)-avoiding state \(\{v_0,v_1,v_2\}\), excluded by Lemma 4.2.

For a longer even path \(v_0\ldots v_{2r}\), with \(r\ge2\), attack the
unoccupied vertex \(v_{2r-2}\) from
\(\{p,v_0,v_{2r}\}\).

- Moving \(p\) leaves three \(a\)-avoiding path vertices, so Lemma 4.2
  applies.
- Moving \(v_0\) leaves
  \(\{p,v_{2r-2},v_{2r}\}\), excluded by the already proved length-two
  subpath.
- Moving \(v_{2r}\) leaves
  \(\{p,v_0,v_{2r-2}\}\), excluded by induction.

The assumption that \(p\) lies outside the path makes every attack
unoccupied and makes both recursive uses legal.  The proof does not need a
response-list condition on \(p\), including when \(p=a\).

### Theorem 4.4

Start at the retained state

\[
 D=S-c+v_0=\{a,b,v_0\}
\]

and attack the distinct unoccupied vertex \(x\).

- A response \(v_0\to x\) would give
  \(S-c+x\notin\mathcal F\), because \(c\notin L(x)\).
- A response \(a\to x\) would give \(\{b,x,v_0\}\), which fails to
  dominate \(q\) because all of \(bq,xq,v_0q\) lie in \(H\).
- Therefore closure forces \(b\to x\) and the retained state
  \(A=\{a,x,v_0\}\).  This conclusion also certifies the needed move
  edge \(bx\); it is not silently assumed.

If \(m=1\), state \(A\) fails to dominate \(v_1\), since
\(av_1,xv_1,v_0v_1\in E(H)\).

If \(m\ge3\) is odd, attack the distinct unoccupied vertex
\(v_{m-1}\) from \(A\).

- Moving \(v_0\) gives \(\{a,x,v_{m-1}\}\), which fails to dominate
  \(v_m\) because \(av_m,xv_m,v_{m-1}v_m\in E(H)\).
- Moving \(a\) gives \(\{x,v_0,v_{m-1}\}\).  Lemma 4.3 excludes it on
  the positive even-length path \(v_0\ldots v_{m-1}\), with \(p=x\).
- Moving \(x\) gives \(\{a,v_0,v_{m-1}\}\), excluded by the same lemma
  with \(p=a\).

All three possible guards are exhausted.  This proves the theorem for
every odd subdivision.  The proof uses no domination-number lower bound,
so the statement that \(\gamma(G)=3\) is unnecessary is correct.

Corollary 4.5 substitutes \(v_0=y\) and uses the first tight cap as \(q\).
The exact lists give \(c\in L(y)\), \(c\notin L(x)\), and
\(a\notin L(y)\); a path inside the \(a\)-omitting projection supplies
the remaining omissions.  A physical type-\(a\) cap of the second gate
supplies \(at,xt\in E(H)\).  This is an exact application of the theorem.

## Chirality and holonomy audit

For a type \(u\), the allowed colors are \(u-1,u+1\).  Exhausting all six
ordered pairs of distinct types and both directed implications gives 12
checks: a cross implication always sends the forced chirality at its tail
to the same chirality at its head.

For lists \(01,12,02\), the three local constraints forbid the only common
color at each pair of ports.  Exhaustion leaves exactly

\[
 (x,y,z)=(a,b,c)\quad\text{and}\quad(b,c,a),
\]

and in each assignment all three ports have one common chirality.  Thus a
tight gate is exactly a chirality-equality gadget.

Within one frozen projection, all vertices use the same two anchor colors.
A complement path alternates those colors, so its endpoint chirality xor is
its length parity.  For a type word, writing
\(\varepsilon_i=u_{i+1}-u_i\in\{\pm1\}\), the two collision colors at an
internal component agree exactly when
\(\varepsilon_i=-\varepsilon_{i-1}\).  Hence an internal connector is odd
exactly at a sign reversal.  A cyclic binary sign word has an even number
of reversals.

At an ordinary internal continuation, the arrival port event and the next
departure event must be complements.  For a path from \(p\) to
\(\bar p\), the last clause's underlying port event instead equals the
initial event \(p\).  Closing those two physical ports therefore toggles
exactly the closing connector relative to the ordinary rule.  The even
cyclic type-word xor becomes one.  This is the claimed odd holonomy.

The clean-room checker exhausts the gate truth table, all 12 directed
cross-type implications, and 2,046 cyclic type words of lengths 2 through
10.  These finite checks support, but are not needed in place of, the
elementary parity proof.

## Sharpness and rejected broader wordings

The verified equality control contains explicit countercontrols to three
natural but invalid strengthenings of Theorem 4.4.

1. **Oddness cannot be deleted.**  With
   \(x=3,q=7\), the path
   \[
     v_0v_1v_2=6-5-11
   \]
   satisfies every displayed hypothesis except oddness.  It is an even
   path, and the graph has an eternal triple-family.
2. **The endpoint edge \(xt\in E(H)\) cannot be deleted.**  The odd
   one-edge path \(6-5\) satisfies the other conditions, including
   \(a5\in E(H)\), but \(35\in E(G)\).
3. **Uniform omission along the path cannot be deleted.**  The odd path
   \[
     6-10-13-11
   \]
   has both return-cap edges \(0\,11,3\,11\in E(H)\), but its internal
   vertices admit color \(a\) in their response lists.

These countercontrols are recorded in `evidence.json`.  They also show why
the theorem may not be paraphrased as excluding every odd geometric return
between two gates.

## Independent equality-control verification

`independent_check.py` takes only the displayed labeled graph6 string as
graph input.  It decodes that record independently, reconstructs \(G\) and
\(\overline G\), and checks:

- order 14, size 47, and connectedness;
- \(\gamma=3\) by an exhaustive rejection of all dominating pairs and
  the dominating triple \(012\);
- \(\alpha=3\) by an exhaustive rejection of independent 4-sets and the
  independent triple \(012\);
- \(i=3\) by exhaustive independent-dominating-set enumeration;
- \(\gamma^\infty=3\) by rebuilding the greatest fixed point over all
  dominating triples, then checking every attack and every legal
  one-guard successor;
- \(\theta=3\) by an exact complement-coloring search (the anchor triangle
  gives the lower bound);
- all response lists at \(S\), both tight gates, both failed
  incidences, and the even \(B_a\) return;
- exactly two compatible anchored list colorings; and
- the canonical graph6 string using the pinned nauty `labelg` executable,
  whose SHA-256 is
  `ae8b1e7ef173c1665725e708bd7abd00b08ee4230ba2bd04117ec63d441274a0`.

The independently rebuilt greatest family has SHA-256

```text
f0c587abd7d7123c822235793049623b02165ae134dd98c22bfa316141b1eaad
```

and its complete 1,892-obligation legal-response table has SHA-256

```text
a1596d28b39fb458c85661779647a9e2058077d5bd8588dcbcb29a5fad8c7712
```

There are 2,128 legal response moves across those obligations.

The source verifier also returned `PASS`.  As a diagnostic audit of
`probe.py`, its closure clauses correctly distribute

\[
 \bigvee_{g\in D}
 \bigl(g r\in E(G)\ \wedge\ D-g+r\in\mathcal F\bigr)
\]

into eight clauses for a triple.  Independent bounded reruns with the
gamma lower-bound encoding disabled returned UNSAT at connector lengths
1, 3, and 5, while length 2 returned SAT and its model satisfied all
22,937 generated clauses.  These solver reruns are only diagnostics; the
unbounded odd-length claim rests on the human proof above.

## Reproduction

From the campaign directory:

```text
python3 -I -B -W error \
  reviews/third_color_gate_cycle_hostile/independent_check.py
```

The command deterministically checks `evidence.json` when it already
exists and prints `PASS`.
