# Hostile review: singleton pins and buffered dynamic ports

Date: 2026-07-28 (PDT)

## Verdict on the revised frozen bytes

**UNCONDITIONAL PASS.**

The revised candidate is sound at its exact stated scope.  In particular:

- Lemma 2.1 (sealed exact-two buffer) is proved;
- Corollary 2.2 (buffer absorption) is proved;
- Theorem 3.1 (dynamic-port buffer alternative) is proved;
- Proposition 1.1 gives the complete no-full clause inventory;
- revised Proposition 1.2 gives an exhaustive terminal split; and
- both exact controls and every stated finite count pass a clean-room
  reconstruction.

I found no import of C-111's all-exact-two hypothesis into the singleton
branch, no illegal occupied attack, no all-guards move, no graph/complement
reversal, and no missing-response-to-graph-nonedge inference.

## Revised-byte resolution of the prior defect

Proposition 1.1 correctly says that either of the following can simplify
to a false constant:

1. a singleton parity demand in a fixed anchor component; or
2. a cross clause whose two endpoint events are both fixed true.

The original candidate incorrectly omitted this immediate branch from
Proposition 1.2.  The revision now separates three exhaustive cases:

1. fixed-component substitution produces a false constant, which is an
   immediate parity or fixed/fixed collision certificate outside C-075;
2. no false constant occurs and unit propagation contradicts, when C-075
   gives the one-/two-unit terminal; or
3. no false constant occurs and propagation is consistent, when any
   unsatisfiable residual has the ordinary unit-free bicycle.

These cases are mutually exclusive and exhaustive.  The opening inventory,
scope disclaimer, proof of Proposition 1.2, Section 5 obstruction ledger,
and next-lemma list all retain the immediate branch consistently.  The
revision therefore fully repairs the sole defect in the first review
without changing a graph-game theorem or control.

## Frozen candidate and dependency bytes

| artifact | SHA-256 |
|---|---|
| candidate `NOTE.md` | `4f6244214e125a31d4237a7e8f59e20266c15374be4d54c2e23bfbb061e313c5` |
| candidate `RESEARCH_LOG.md` | `0a45cd338672f9f3c9cd7da0aa397c539d6454ddceff29bf0ca3660e0542503b` |
| candidate `controls.json` | `108bedac6c157a70a2d21200afa4740faac64f501906ec845e098a8f141b22a9` |
| candidate `search_sealed_cap.py` | `f4b1b70c09f1fc8f46b1ec65cdf4afca01f30d2825df116d9d357c2f9f20a719` |
| candidate `verify.py` | `b9f0078167e0d1ee040edbf00fd8e32837a438c5919d0776a10297a84047bf11` |
| candidate `MANIFEST.json` | `b563aa466cc9798c270e954de914e143427e0048663ca7ccc3d3ea547b4831b0` |
| C-069 projection gluing | `fc7f817aa611751b9bedbb9ddebd5830d81f02719f2d8aafe914db34f4c64907` |
| C-075 terminal trichotomy | `8a934a8194913633821223b070a013dda8e0cd8c0d6870616b32a882e8b2fd59` |
| C-079 odd fan | `d3a23bb0171a047a85f2a05c5ccb5faeef0c0c7ceb6d7bb139c6a7a86b8b1f10` |
| C-082 connector caps | `185e29a4b8e231aa5e90126f7fd16be32c696cd3f99e46c00f90cb61f27548e7` |
| C-094 physical representatives | `3a357c3c7ece9a0cf33f7b555cae21e629a19b9e2d86e6ebe6f5798b4f08e7df` |

The file hashes recorded inside the candidate manifest agree with the
current candidate bytes.

## Human proof audit

### Complete edge-clause inventory

For two nonempty proper subsets of a three-color set, the clean-room
enumeration gives exactly 21 unordered list pairs:

| disposition | count |
|---|---:|
| a common omitted color, hence one frozen projection separates the edge | 15 |
| disjoint singleton/exact-two lists | 3 |
| distinct exact-two lists with one shared collision color | 3 |

This verifies Proposition 1.1's complement-edge exhaustion.  A singleton
appears in precisely the two projections corresponding to its two omitted
colors.  A distinct-type exact-two edge has one possible common color and
therefore one collision clause.  Anchor/outside edges are safe because
response membership forces the corresponding graph edge.

The revised constant branch has the exact C-075 boundary.  After ruling it
out, C-075 is applied at its correct normalized scope, and the distinction
between residual unit-free variables and singleton vertices elsewhere in
the graph is correctly stated.

### Lemma 2.1

Write \(S=\{i,j,k\}\), \(L(z)=\{i,j\}\), and suppose \(z\) is
\(i\)-sealed.

Since \(\gamma(G)=3\), the pair \(\{k,z\}\) is not dominating.  A missed
vertex \(p\) is a common open complement neighbor of \(k,z\), and it is
distinct from both endpoints.  It is not an anchor: \(i,j\) are
\(G\)-neighbors of \(z\) by their response memberships, while \(k\) is an
endpoint.  Thus \(p\) is outside.

The literal edge \(kp\in E(\overline G)\) excludes \(k\) from \(L(p)\).
If \(i\in L(p)\), then \(p\in P_i^+\), contradicting
\(zp\in E(\overline G)\) and sealing.  Nonemptiness leaves
\(L(p)=\{j\}\).  This argument does not use or infer a graph nonedge from
a missing response.

If \(kz\in E(G)\), apply the same argument to \(\{j,z\}\).  Its common
complement neighbor \(q\) cannot be \(i\) or \(k\), since both see \(z\)
in \(G\), and it cannot be endpoint \(j\).  The two displayed complement
edges exclude \(j\) directly and \(i\) by sealing, so
\(L(q)=\{k\}\).  The two witnesses are distinct because their singleton
lists differ.  Every possible anchor collision is therefore accounted for.

### Corollary 2.2

The buffer has list \(\{j\}\), so every compatible anchored coloring gives
it color \(j\).  Its complement edge to the \(\{i,j\}\)-listed cap forces
the cap to color \(i\).  Every member of \(W_i\) omits \(i\), so every
cap edge back into \(W_i\) is automatically proper.  This conclusion is
conditional on a compatible coloring and makes no existence claim.

### Theorem 3.1 and its dependencies

For a dynamic type-\(i\) port \(t\), accepted C-094 supplies distinct
outside vertices \(y,r\) with

\[
 t-y-r\subseteq\overline G[W_i],
\]

where \(r\) has the same exact list and bipartition sign as \(t\), and
\(ir\in E(\overline G)\).  The theorem uses the literal first edge
\(ty\); it does not transport a clause edge to \(r\).

Accepted C-082 applies because \(t,y\) both omit \(i\), \(ty\) is a
literal complement edge, and dynamicity gives \(it\in E(G)\).  It supplies
an outside common complement neighbor \(z\) of \(t,y\) with
\(i\in L(z)\).

If an outside \(i\)-positive \(p'\) had
\(p'z\in E(\overline G)\), accepted C-079 applies exactly at path length
one with

\[
 (p,q,v_0,v_1)=(p',z,t,y).
\]

All four vertices are distinct: the two positive vertices differ because
they are joined by a simple edge; positive and omitted-\(i\) lists separate
them from \(t,y\); and \(t\ne y\).  The four required literal complement
edges are \(p'z,zt,zy,ty\).  Thus \(z\) is \(i\)-sealed.

The no-full hypothesis leaves \(L(z)=\{i\}\) or
\(\{i,j\}\).  In the second case Lemma 2.1 and Corollary 2.2 apply
verbatim.  No exact-two assumption is made about \(y\), the cap, or the
rest of the outside vertices.  C-111 and C-114 are not used.

## Independent finite-control audit

`independent_check.py` imports no candidate or campaign module.  It uses
integer adjacency and state masks, a fresh graph6 decoder, exhaustive
subset routines, an independent coloring backtracker, and simultaneous
greatest-fixed-point deletion directly from the one-guard definition.

For every family state it separately checks:

1. the state dominates;
2. attacks are only at unoccupied vertices;
3. exactly one guard changes;
4. the moving guard is adjacent to the attacked vertex in \(G\); and
5. the successor remains in the audited family.

It obtains:

| control | \(n,m\) | \((\gamma,i,\alpha,\gamma^\infty,\theta)\) | family | obligations | list colorings |
|---|---:|---:|---:|---:|---:|
| `EEv?` | \(6,7\) | \((3,3,3,3,3)\) | selected 8 states | 24 | 1 |
| `LFzJbZYhdrDZdM` | \(13,43\) | \((3,3,3,3,3)\) | greatest 142 states | 1,420 | 2 |

The six-vertex control is disconnected (vertex 2 is isolated), which the
candidate does not deny and which is harmless for its sharp local purpose.
Its lists are exactly

```text
3:01  4:01  5:1
```

and both 3 and 4 are sealed 0-positive vertices.  Vertex 5 is their
singleton-1 buffer.  Anchor 2 is a common complement neighbor for the
other deficient pair, and there is no singleton-2 outside vertex, so the
qualification in Lemma 2.1 is sharp.

For the 13-vertex connected control, simultaneous deletion removes two of
the 144 dominating triples in one round and leaves the 142-state greatest
kernel.  The response lists are exactly

```text
3:01  4:12  5:01  6:12  7:12
8:01  9:02  10:02  11:2  12:0
```

The only dynamic exact-two ports are \(3\) of type 2 and \(4\) of type 0.
Their full projection components are respectively \(\{3,5,8\}\) and
\(\{4,6,7\}\); neither meets an anchor or singleton marker.  The paths
\(3-5-8\) and \(4-6-7\) have the stated complement edges, physical
same-sign endpoints, and exact lists.  Vertices 11 and 12 are respectively
sealed singleton caps of colors 2 and 0 on the first path edges.

The two response-certificate hashes are:

```text
EEv?            8c9aefcaf68bd53d1ddcc59272c204e9c716e2a12fa06d719e64cf3dd4077a38
LFzJbZYhdrDZdM  67cccdda55073b70211ae05599ce736d126a2bab97dd68ff951acf460a984ccd
```

The independently serialized 142-state greatest family has SHA-256

```text
6afa4f7e4b50715d55f62d475267832db52f3419b7394e39dbdc14ecdcdbd1f9
```

## Scope audit

- the result identifies a real singleton buffer around every sealed
  exact-two cap;
- every dynamic exact-two port has the stated sealed-cap alternative;
- the controls sharply refute both naive extensions of C-111;
- the singleton/no-full branch remains open;
- arbitrary separated-port unit chains and unit-free bicycles remain open;
- no full-list result, complete \(k=3\) theorem, finite-frontier advance,
  or universal resolution is claimed.

The immediate constant branch, arbitrary separated-port unit chains, and
unit-free residual bicycles all remain expressly open.  The accepted
result is a structural advance, not closure of the singleton branch.

## Reproduction

From the campaign directory:

```text
python3 -I -B -W error \
  reviews/singleton_buffer_hostile/independent_check.py
```

Successful stdout has SHA-256

```text
8a5ef8879edc31ab91d0b7f7097a6683c51687e9d5870f1206a367b49d5f2e74
```

The original-byte review correctly returned `CORRECTION REQUIRED`.
Rechecking the exact revised bytes above gives the final unconditional
verdict `PASS`.
