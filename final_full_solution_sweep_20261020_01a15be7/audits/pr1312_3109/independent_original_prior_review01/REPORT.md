# PR1312 /3109: independent original and prior review

**Complete negative answer passes.** For every odd n≥3 the cyclic
Petersen-fragment graph G_n is connected, simple, bridgeless and cubic,
has10n vertices, has only odd cycles in every 2-factor, and has
ω(G_n)=n+1. In particular G_3 has30 vertices and oddness4, contradicting
the proposed bound2. Credit the Anonymous OPG comments dated June29 and
July2,2010. No solution DOI or journal publication was authenticated;
one qualified source-only row with B and C blank is proposed.

## Original hypotheses and primary prior identity

The actual [OPG statement](https://www.openproblemgarden.org/op/odd_cycles_and_low_oddness)
requires bridgelessness and cubicity, and defines oddness as the minimum
number of odd cycles in a 2-factor. It has no 3-edge-connectivity
hypothesis. The primary page's [comment6751](https://www.openproblemgarden.org/op/odd_cycles_and_low_oddness#comment-6751)
gives the Petersen-minus-edge cyclic construction and the zero-link case;
[comment6753](https://www.openproblemgarden.org/op/odd_cycles_and_low_oddness#comment-6753)
gives the restored-edge analysis and long-cycle case. Both are currently
attributed to Anonymous with the dates above. No maintainer or original
problem poster is substituted for their authorship.

The complete live primary HTML was independently fetched. Its20679 bytes
have SHA-256
`dd2ee635f2e11e7af4e4a53bb721349bf881eb5c001b9d98f1c11213c9edadc6`,
matching the frozen PR source capture. Both exact comment anchors occur
in the retained body. The full target and both full counterexample
comments were read, including formula-image alt text. This authenticates
the currently displayed primary source and its attribution; it is not a
certificate of an Anonymous author's identity or external peer review.

The original cached statement matches compact-catalog SHA-256
`efa942596da9096459f6c8cd9765bfed6c39ddccef32e3864131b36dfa01e083`.
The cache's later demand for a journal source is a historical triage
condition, not a missing graph-theoretic hypothesis. The reconstruction
is assessed below directly. A conjecture heading or an old open label
does not defeat an exact verified counterexample.

## Standalone local proof

Define Petersen vertices a_i,b_i for i modulo5 and edges
a_i a_(i+1), b_i b_(i+2), a_i b_i. This is simple, connected and cubic.
Its girth is5: a cycle without spokes is a displayed5-cycle; a short
cycle with two spokes would need the same index difference to be both
±1 and±2 modulo5; four spokes require at least four intervening nonspoke
edges and hence length at least8.

P has no edge cut of size at most2. For a smaller nonempty side S of a
putative cut, |S|≤5 and 3|S|=2e(S)+|δ(S)|. If |S|≤4, girth5 makes P[S]
a forest, so the right side is at most2(|S|−1)+2=2|S|, impossible.
If |S|=5, the induced graph has at most5 edges: any cycle must be a
5-cycle and a chord would create a shorter cycle. Then |δ(S)|≥5.
Deleting any edge e therefore leaves P−e connected and bridgeless;
a bridge after deletion would give a cut contained in two original edges.

Every Petersen2-factor is two5-cycles. Its complement is a perfect
matching. The number of spokes in a perfect matching is odd, since the
remaining outer vertices pair internally. Three spokes are impossible:
the remaining pair of indices would need to be adjacent in both the
outer and inner pentagons. Five spokes give the matching of all spokes.
For one spoke, rotate its index to0. The remaining vertices in each
pentagon form a four-vertex path with a unique perfect matching. This
gives exactly

```
{a0b0, a1a2, a3a4, b2b4, b1b3}
```

and its five rotations. The complement of this displayed matching has
cycles (a0,a1,b1,b4,a4) and (a2,a3,b3,b0,b2); rotations preserve their
lengths. Together with the all-spoke case, this proves the classification
without a non-Hamiltonicity or snark-classification import.

Fix e=a0b0. An avoiding2-factor is the outer and inner pentagons. A
containing2-factor has cycles

```
(a1,a2,b2,b0,a0), (a3,a4,b4,b1,b3).
```

Deleting e from the latter leaves one path on five vertices with ends
a0,b0 and one disjoint5-cycle. This supplies actual local states, so
the subsequent existence claim is not vacuous.

## Universal graph and exhaustive global proof

Take n disjoint copies H_i=P_i−x_i y_i of this fragment and add links
ℓ_i=y_i x_(i+1), subscripts modulo n. For n≥3, the links create no
loops or parallel edges. Each terminal regains exactly one incident
edge, giving cubicity and10n vertices. The connected fragments form a
cyclic connected graph.

Every internal edge lies on a cycle inside its bridgeless H_i. Choosing
any simple terminal path in every H_i and adjoining all links gives one
cycle through every link. Thus every edge is on a cycle: G_n is
bridgeless. Connectivity alone would not have proved this.

For any spanning2-factor F, even-degree parity gives

\[
 2|S|=2|E(F[S])|+|F\cap\delta(S)|.
\]

The block boundary is exactly {ℓ_(i−1),ℓ_i}, so either both boundary
links are used or neither. Following the block cycle forces all link
indicators equal. This establishes simultaneous use, not yet the claim
that they lie on one cycle.

If no links are used, each block restriction is a Petersen2-factor
avoiding its deleted edge and consists of two5-cycles. Globally there
are2n such cycles.

If all links are used, the restriction has degree1 at its two terminals
and degree2 elsewhere. Restoring x_i y_i makes a Petersen2-factor
containing that edge. The local classification yields one5-cycle and
one five-vertex terminal path. These paths, now with the n links,
join into a **single** cycle: the successive blocks are encountered in
their cyclic order, each with just one terminal path. Its length is
4n+n=5n. The other n cycles have length5. This restoration argument
justifies the single-cycle statement compressed in the first comment;
parity alone was not used to assume it.

The two explicit local states realize both global cases. For odd n,
all their cycles are odd. Hence

\[
 \omega(G_n)=\min\{2n,n+1\}=n+1.
\]

This is an unrestricted proof for every odd n≥3, independent of a
computer enumeration. The graphs have block2-edge-cuts, which are
permitted by the actual original question. No claim for a strengthened
3-edge-connected question is made.

## New finite checks and falsification

The newly authored standard-library checker independently generates all
perfect matchings by covering an unmatched vertex with each available
incident edge. Complementation gives every2-factor. No block-state
classification is assumed by this enumerator. Each complement is checked
to be spanning degree2 before its component lengths are counted.

For P, independent enumeration of all five-edge subsets matches the
recursive list of six perfect matchings. All1022 nontrivial vertex subsets
are inspected for cuts, giving minimum cut3; shortest cycles give girth5.
Every one of the15 edge-deleted fragments is checked connected and
bridgeless, and every deleted edge has the expected two avoiding/four
containing factor states.

Complete global enumeration for n=1,…,7 gives2^n+4^n factors and only
the two predicted states. Representative results:

| n | Factors | Zero-link factors | All-link factors | Oddness | Every factor all odd? |
|---|---:|---:|---:|---:|---|
|1|6|2|4|2|yes|
|2|20|4|16|2|no|
|3|72|8|64|4|yes|
|4|272|16|256|4|no|
|5|1056|32|1024|6|yes|
|6|4160|64|4096|6|no|
|7|16512|128|16384|8|yes|

At n=3 the two factor length multisets are (5,5,5,5,5,5) and
(5,5,5,15). For n=1 the cycle-type histograms coincide and combine;
this is Petersen of oddness2, not a refutation. For even n the all-link
5n-cycle is even, so the original all-odd premise fails. These are
substantive boundary foils.

Eleven controls per mode cover an open chain, restored deleted spokes,
even n, n=1, prism replacements, incorrect minimum-cycle count, the
2-edge-boundary limitation, reversed-link positive symmetry, and a
nonedge cycle corruption. All three modes normal,-O,-OO pass identically,
with33 control passes. No historical checker or author program was run.
These finite results corroborate the universal proof; they do not
replace it or certify a minimum order.

## Provenance, duplicate check and disposition

A fresh numeric-gid43-column read completed before mathematics, with191
nonempty response rows. An incidental substring6753 hits an unrelated
MTP2-model DOI ending6753 at response index22, problem30005303. It is
not comment6753 or this graph result. Exact problem/title/URL/comment
aliases give no matching ledger record. A bounded exact-title/construction
search returns the primary comments and unrelated graph results; no
solution DOI or journal version was authenticated. This is not a proof
that no such publication exists or an exhaustive priority determination.

The full PR body and seven attempt files were read at immutable head
0bda78f813427352f9e56b63f6fba9adc5efa689. All eight blobs including the
complete QUEUE blob, and all six nested-manifest payload entries, match.
The relevant exact QUEUE diff was read; unrelated rows are not mathematically
reviewed. Its claimed_solved label is a claim under audit. The historic
original-candidate hash and eight historical controls are not claimed
newly reproduced: the current proof and new checker are separately bound.

The source-only proposal leaves both chat and DOI cells exactly blank,
places both authentic comment anchors and PR1312's exact URL in the notes,
and describes Anonymous attribution and review limits. It does not
represent comments as a journal paper or this reconstruction as a new
publication. No services, Git, QUEUE, CASE, readiness or publication
state is changed. No outside people or other agents were contacted.
All twelve earlier own seals, including newly closed PR1311 and PR1314,
are verified unchanged. The complete closing seal covers every retained
source/report/checker/result and the nested PR manifest, excluding only
its exact own filename. No mathematical gap remains for the original
negative relative to the elementary proof above; formal certification,
minimum-order and stronger-connectivity questions remain unadjudicated.
