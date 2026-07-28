# Hostile audit: order-nine greatest-family reciprocity ranks

## Verdict

**PASS, with a strict finite-scope classification.**

The candidate's numerical census and both negative mechanism conclusions
reproduce exactly under a clean-room implementation:

1. static complementary-exchange reciprocity is false even when
   \(\gamma=\alpha=\gamma^\infty=3\);
2. the two finite deletion ranks need not be equal; and
3. among all connected unlabeled graphs of order nine satisfying those
   equalities, complementary exchanges survive the greatest triple-kernel
   simultaneously.

The third statement may now be promoted from `OBSERVED` to
`CERTIFIED-FINITE` for the exact order-nine, \(k=3\) universe.  It is not an
all-order reciprocity theorem.  The proposed coinductive proof mechanism
remains a promising interpretation of the data, not a proved lemma.  This
audit neither proves the complete \(k=3\) case nor resolves the
\(\gamma\)--\(\theta\) conjecture.

The candidate bytes audited were:

| artifact | SHA-256 |
|---|---|
| `NOTE.md` | `b4abad573fbb0b957406338b03aa5c6bd37f228610297a148eaee029340695a6` |
| `RESEARCH_LOG.md` | `90a70a04fedc631ebbf4a5fdc34a49f6758feacc48fd2fad85ce9bc8a5922c71` |
| `probe_rank_pairs.py` | `45549b7f5ef62be6bef5ded3a4463f3396afcafd11cce990dc203390a053ced6` |
| `order9_result.json` | `358b1be0ef99745fb0acac28f6955ed80c7a62634b19c7cc930d6049d5e40c84` |
| `MANIFEST.json` | `cec46895a94ead868ddec0169515142b18e8938081bd14c2a2e81c554d754ada` |

Every entry in the candidate manifest has the declared hash.

## 1. Independent universe reconstruction

The hostile checker does not begin from the candidate's connected stream.
It asks the pinned nauty 2.9.3 binary for **all** unlabeled order-nine
graphs, then decodes graph6 and tests connectedness itself.

As an independent count check, it derives the number of unlabeled simple
graphs by Burnside's lemma.  For a permutation with cycle lengths
\(\lambda_1,\ldots,\lambda_t\), the number of orbits on unordered vertex
pairs is

\[
 o(\lambda)=
 \sum_i\left\lfloor\frac{\lambda_i}{2}\right\rfloor+
 \sum_{i<j}\gcd(\lambda_i,\lambda_j).
\]

Summing \(2^{o(\lambda)}\) over conjugacy classes with their exact class
sizes gives

\[
 1,1,2,4,11,34,156,1044,12346,274668
\]

for orders zero through nine.  Inverting

\[
 A(x)=\prod_{m\ge1}(1-x^m)^{-c_m}
\]

then gives

\[
 0,1,1,2,6,21,112,853,11117,261080
\]

connected graphs at the same orders.

The pinned generator produced exactly 274,668 records.  A separate pinned
`labelg` pass gave 274,668 distinct canonical labels, excluding duplicate
isomorphism classes.  The hostile connectedness test retained exactly
261,080 records, and those records were byte-identical, in order, to a
separate `geng -c` run.  The decisive hashes are:

| object | SHA-256 |
|---|---|
| `geng` binary | `588052a87e5313f331aa145a0a641702b6c13b6e2387dd3c4807bf7f49fdaca1` |
| `labelg` binary | `ae8b1e7ef173c1665725e708bd7abd00b08ee4230ba2bd04117ec63d441274a0` |
| all order-nine graph6 stream | `ce9c5d4d27c8e55de5f0c6348ec781a650382e16bdff26b6c3418fa00a9cfcf9` |
| independently filtered connected stream | `fe73f2b8aad1a653b6f3bee799efff369cc486688df5aeade62ce0b3b5889eb5` |
| canonical-label stream | `b52cedd4697f689327e09df5d36de1ae9aab02737f6ccd8e8f8bb18faedc962a` |

The checker also freezes the complete edge-count histograms for both
streams.  Thus the bounded result is supported by a reproducible case
manifest, an independently derived universe count, an independent
connectedness filter, and distinct canonical representatives.  This
satisfies the campaign's `CERTIFIED-FINITE` standard for this direct finite
computation; it is not a formal verification of nauty itself.

## 2. Independent parameter and game logic

The hostile implementation imports no candidate module, campaign
evaluator, NetworkX routine, or SAT solver.  It represents a graph by
adjacency sets and a guard configuration by a sorted vertex tuple.

For each connected graph it checks \(\alpha=3\) by enumerating all triples
and four-sets.  It checks \(\gamma=3\) by rejecting every dominating vertex
and pair, then literally confirms that every maximum independent triple
dominates.

For the game it constructs an explicit attack-coloured configuration
digraph on all dominating triples.  For each state \(D\) and each
unoccupied attacked vertex \(r\), an arc is included only when exactly one
guard \(u\in D\cap N(r)\) moves to \(r\), and the successor
\((D-\{u\})\cup\{r\}\) still dominates.  Synchronous deletion from the full
dominating-state set computes the literal greatest fixed point.  Rank zero
means non-domination; ranks one, two, and so on are synchronous deletion
rounds; `S` means survival.

This checks all model hazards explicitly:

- no attack is made at an occupied vertex;
- exactly one guard moves;
- the move follows an edge of \(G\);
- every retained successor dominates;
- no complement graph is substituted; and
- greatest-family survival is not confused with membership in an
  arbitrary proper eternal family.

The static filter retained 2,949 graphs.  Exactly 1,380 had a nonempty
greatest triple-kernel and hence
\(\gamma=\alpha=\gamma^\infty=3\).  All independent triples were checked
to belong to the resulting greatest family, as required by
maximum-independent-state forcing.

## 3. Exchange enumeration and exact reproduction

For every unordered pair \(S,T\) of maximum independent triples, the
checker enumerates every

\[
 (u,x)\in(S-T)\times(T-S)
\]

and compares

\[
 S-u+x\qquad\text{with}\qquad T-x+u.
\]

An unordered state pair is sufficient because reversing \(S,T\) merely
reverses the same two configurations.  The displayed rank table is
oriented by the generator's deterministic triple order, so the counts
need not be symmetric.

The clean-room totals match the candidate exactly:

| quantity | count |
|---|---:|
| connected unlabeled order-nine graphs | 261,080 |
| \(\gamma=\alpha=3\) graphs | 2,949 |
| \(\gamma=\alpha=\gamma^\infty=3\) graphs | 1,380 |
| greatest-family states | 35,299 |
| unordered independent-state pairs | 90,103 |
| complementary exchange instances | 392,155 |
| static domination asymmetries | 12,522 |
| one-sided greatest-family survivors | **0** |

The complete independently reproduced table is

| rank pair | count |
|---|---:|
| `0,0` | 195,406 |
| `0,1` | 5,592 |
| `0,2` | 143 |
| `1,0` | 6,435 |
| `1,1` | 2,880 |
| `1,2` | 666 |
| `1,3` | 3 |
| `2,0` | 352 |
| `2,1` | 742 |
| `2,2` | 156 |
| `2,3` | 1 |
| `3,1` | 5 |
| `3,2` | 1 |
| `S,S` | 179,773 |

The 12,522 static asymmetries split as

\[
 5592\,(0,1)+143\,(0,2)+6435\,(1,0)+352\,(2,0).
\]

Consequently every dominating member of a static asymmetric pair is
deleted by round one or two.  Unequal positive finite ranks also occur, so
rank-preserving induction is independently refuted.  The first such
control is graph6 ``HCOe`Z{``, with ranks two and one.

Most importantly, `S,S` is the only table entry containing `S`.  This is
the complete bounded statement that may be classified
`CERTIFIED-FINITE`.

## 4. First static-asymmetry control

The first candidate control, graph6 `HCOceRy`, is connected and has

\[
 \gamma=\alpha=\gamma^\infty=3.
\]

The independent checker finds 17 maximum independent triples, 26
dominating triples, and 24 states in the greatest triple-family.  With

\[
 S=012,\qquad T=578,\qquad u=0,\qquad x=7,
\]

the forward state is `127`; it misses vertices 3 and 6 and therefore has
rank zero.  The reverse state is `058`; it dominates, but attacks at either
3 or 6 have no dominating one-edge successor, so it is deleted in round
one.  This is an explicit, independently replayed counterexample to static
complementary-exchange reciprocity under the full equality hypothesis.

It does **not** contradict greatest-family reciprocity: neither mixed state
survives.

## 5. What the result does and does not establish

The data decisively close two tempting proof routes:

- domination of one complementary exchange does not imply domination of
  the reverse exchange; and
- paired configurations do not share a common finite deletion rank.

At order nine the dynamic kernel nevertheless repairs every asymmetry:
one mixed state survives if and only if its complementary mixed state
survives.  A successful universal proof, if this pattern persists, must
use a genuinely fixed-point or coinductive mechanism rather than a static
exchange lemma or rank-by-rank equality.

No such mechanism is proved here.  In particular, the census says nothing
about order ten and above, parameter \(k>3\), disconnected graphs outside
the stated reduction, proper eternal subfamilies, clique-cover number, or
global gamma--theta resolution.

## Reproduction

From the campaign directory:

```text
python3 -I -B -W error \
  reviews/greatest_family_reciprocity_rank_hostile/independent_checker.py \
  > /tmp/greatest-family-rank-hostile.json
cmp /tmp/greatest-family-rank-hostile.json \
  reviews/greatest_family_reciprocity_rank_hostile/independent_result.json
```

The final clean replay took about 19 seconds and peaked near 102 MB on the
campaign MacBook.
