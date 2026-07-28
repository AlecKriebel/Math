# Hostile review: fresh-component chains

Date: 2026-07-28 (PDT)

## Verdict

**PASS AFTER REQUIRED SCOPE CORRECTIONS, with strict local scope.**

The original frozen note, SHA-256

```text
51a506f958d1843ffbc2eb2cdedf4c541cf8b717d232159cf26f0de68ff2a1e9
```

did not state the quantifier needed by its terminal-return
classification.  Its two displayed rows are exhaustive for a binary
cross clause between exact-two-list endpoints, but not for an arbitrary
terminal clause: singleton sources with lists \(\{w\}\) and \(\{v\}\)
can force the same respective target colors.  The original summary also
did not distinguish a first re-entry from a two-unit trace ending at a
separately pinned component.  Three internal equation references and one
positive-marker label were additionally wrong.

The revised note makes all required repairs.  The exact revised bytes
accepted here are:

```text
math/working/fresh_component_chain/NOTE.md
SHA-256 6f5397cf4172d6531144603e24b236df8f162de096abf201848eadd897802573

math/working/fresh_component_chain/RESEARCH_LOG.md
SHA-256 4415363610ebedc9a0c524258a9388b936dc2e2748c4b6c69fdb7f507ffc7a13

math/working/fresh_component_chain/MANIFEST.json
SHA-256 4283d307f241520c3d50a444d18cfa382504fd031f5568d3a8a105474edeeeb2
```

On those revised bytes, I accept:

1. side-purity of one selected C-133 bridge vertex toward every component
   of the relevant omitted-color projection;
2. the resulting no-opposite-side-return theorem for that same physical
   bridge vertex;
3. separation of its C-140 turning ridge from every free component of
   that projection;
4. component-simplicity before the first re-entry of a shortest
   implication trace, conditional on such a re-entry occurring;
5. the two exact color directions for a terminal **binary cross clause
   between exact-two-list endpoints**;
6. the C-103 retained-boundary alternative when a shared-\(w\) return
   uses a second \(\{u,w\}\) vertex of the original bridge ridge; and
7. both finite scope controls with the exact parameters, families, lists,
   components, sides, colors, and collision incidences stated below.

I do not accept or infer:

- a classification of singleton-source terminal clauses;
- absence of two-unit endings;
- synchronization of two different physical hubs;
- a contradiction from either retained boundary state;
- exclusion of a source outside the original bridge ridge;
- exclusion of arbitrary chains, lollipops, or bicycles;
- complete \(k=3\); or
- the universal gamma--theta conjecture.

## Frozen dependencies

I independently reread the exact accepted inputs used by the proof.

| input | SHA-256 | role |
|---|---|---|
| `math/working/k3_long_bicycle_connectors/NOTE.md` | `d3a23bb0171a047a85f2a05c5ccb5faeef0c0c7ceb6d7bb139c6a7a86b8b1f10` | C-079 odd physical fan |
| `math/working/k3_side_purity_cap_cycle/NOTE.md` | `64312289f6d3d87a4c302692c92901caeb9788b16354493e07be01920549f11b` | exact C-079 side-purity consequence |
| `math/working/distributed_gate_holonomy/NOTE.md` | `e1bcfdf52379ffe7055932bbaa3e29d4f3f7934271703df9dcb5b4d20bb0cb9c` | C-103 two-projection parity |
| `math/working/anchor_only_bridge_ridge/NOTE.md` | `6e1d4a866889538324faeef4a0d6713577042a660a72d266bf5c79bf51069fa1` | C-133 retained bridge and list/location trichotomy |
| `math/working/bridge_chain_propagation/NOTE.md` | `682b02b7aab2ffd326a421c60193c8df8d1b33404a22153a893d935f16cf4579` | C-140 bridge orientation, original-component gate, and turning ridge |

The candidate manifest also correctly binds the accepted frozen
projection, exact-two free-component, singleton polarization,
first-cross-clause, and response-2-CNF notes.  All of its dependency and
candidate-file hashes match the current bytes.

## Model and notation audit

Throughout,

\[
S=\{u,v,w\}\in\mathcal F
\]

is independent, \(H=\overline G\), and

\[
L(x)=\{a\in S:S-a+x\in\mathcal F\}.
\]

This abbreviated family-list definition is safe for an independent
reference state.  If \(S-a+x\) is retained, it must dominate the omitted
anchor \(a\); the other two anchors miss \(a\), so \(ax\in E(G)\).  The
proof uses this implication only in the valid direction.  It never turns
\(a\notin L(x)\) into \(ax\in E(H)\).

Every dynamic step reviewed below attacks an unoccupied vertex, moves one
guard along one edge of \(G\), and keeps the successor in the same
specified family.  Complement edges are used only to forbid guard moves
or encode coloring collisions.

## 1. Global side-purity for one bridge vertex

C-133 supplies a selected bridge vertex

\[
z\in W_{uw},\qquad L(z)=\{u,w\},
\]

and the singleton terminal

\[
L(t)=\{u\},\qquad tz\in E(H).
\]

For any component \(C\) of \(H[W_u]\), accepted C-079 side-purity applies
with

\[
a=u,\qquad p=t,\qquad q=z.
\]

Every hypothesis is literal:

- \(u\in L(t)\);
- \(t\ne z\), because C-133 places its bridge outside the terminals; and
- \(tz\in E(H)\).

It follows that \(N_H(z)\cap C\) lies on one bipartition side.  If an
entering clause has \(zr\in E(H)\) with \(r\in C_0\), that edge identifies
the permitted side as \(C_0\), so

\[
zq\in E(G)\qquad(q\in C_1).
\]

Here \(q\ne z\) automatically: \(z\notin W_u\) because
\(u\in L(z)\), whereas \(C_1\subseteq W_u\).

If \(L(r)=\{v,w\}\), the selected bridge color \(z=w\) and the collision
edge \(zr\) force \(r=v\).  Thus \(C_0\) receives \(v\) and \(C_1\)
receives \(w\).  The same physical \(z\) has no complement edge to
\(C_1\), so it cannot later force a \(C_1\)-vertex to the wrong color
\(v\).

This conclusion is componentwise but not cross-hub.  The positive tail
\(t\) exposes this one fixed \(z\) toward every \(u\)-omitting component;
it supplies no relation between side choices made by distinct source
vertices.

## 2. Turning-ridge separation

Let

\[
R_z=N_H(w)\cap N_H(z).
\]

C-140 proves that the only possible anchor in \(R_z\) is \(v\), and every
outside member has list

\[
\{v\}\quad\text{or}\quad\{u,v\}.
\]

The fixed component of

\[
B_u=H[\{v,w\}\cup W_u]
\]

contains \(w\).  Every member of \(R_z\) is an \(H\)-neighbor of \(w\).
Consequently:

- an outside singleton-\(v\) member belongs to \(W_u\) and is joined
  directly to the fixed component;
- the anchor \(v\), if present, is already in the fixed component; and
- an outside \(\{u,v\}\)-member contains \(u\) in its list and therefore
  is not a vertex of \(B_u\).

Hence \(R_z\) is disjoint from every free component of \(B_u\).  This
does not prevent one of its two-list vertices from later occurring in a
different frozen projection, exactly as the revised note states.

## 3. First-reentry normalization and its corrected boundary

In the implication digraph, an arc depends only on its tail literal.  If
a directed trace repeats the same literal, the intervening closed walk
can be deleted.  If it reaches the opposite literal of a variable already
assigned earlier on the trace, the conflict has already occurred.

Therefore, when a shortest trace has a first re-entry into one of its own
previously visited component variables, every proper step before that
re-entry uses a new variable; a same-literal re-entry is removable and an
opposite-literal first re-entry is terminal.

This argument does not say that every contradiction contains a repeated
trace variable.  A two-unit path may instead reach the opposite value of
a component pinned independently by a second singleton.  The revised
Lemma 3.1 and status summary now preserve that distinction.

For the selected orientation

\[
C_0=v,\qquad C_1=w,
\]

consider a terminal binary cross clause whose target has exact list
\(\{v,w\}\) and whose source is an exact-two-list endpoint of a distinct
type.  There are exactly two cases:

| target | wrong forced target color | collision color/source assignment | unique distinct exact-two source list |
|---|---|---|---|
| \(r'\in C_1\) | \(v\) | \(w\) | \(\{u,w\}\) |
| \(r'\in C_0\) | \(w\) | \(v\) | \(\{u,v\}\) |

The original draft omitted the boldfaced binary/exact-two restriction.
Without it, singleton sources \(\{w\}\) and \(\{v\}\) are additional
possibilities.  The revised Theorem 3.2 states the exact restriction,
and explicitly leaves singleton-source clauses outside the theorem.

In the first binary row, Corollary 2.2 gives \(y\ne z\).  In the second
row, the source list already differs from \(L(z)=\{u,w\}\).  Thus the
claimed physical separation is valid only at the corrected
binary-exact-two scope.

## 4. Exact C-103 reconstruction

Assume the first binary row, and let the terminal source be another
original bridge vertex

\[
y\in W_{uw},\qquad y\ne z.
\]

Let \(r\in C_0\) be the entering target and \(r'\in C_1\) the returning
target.  The two C-103 paths are

\[
P:z-t-y,\qquad Q:r\leadsto r'.
\]

Their full hypothesis map is:

| C-103 item | current object | check |
|---|---|---|
| \(S=\{a,b,c\}\) | \((a,b,c)=(u,w,v)\) | a relabeling of the independent root |
| \(P\subseteq W_c\) | \(z,t,y\in W_v\) | lists \(\{u,w\},\{u\},\{u,w\}\) all omit \(v\) |
| \(Q\subseteq W_a\) | \(Q\subseteq C\subseteq W_u\) | definition of the entered projection |
| first positive endpoint | \(u\in L(z)\) | \(L(z)=\{u,w\}\) |
| second positive endpoint | \(v\in L(r)\) | \(L(r)=\{v,w\}\) |
| length of \(P\) | \(2\) | \(zt,ty\in E(H)\) |
| length of \(Q\) | odd | \(r,r'\) lie on opposite sides of bipartite \(C\) |
| path disjointness | \(V(P)\cap V(Q)=\varnothing\) | every \(P\)-vertex contains \(u\) in its list; every \(Q\)-vertex omits \(u\) |

C-133 makes \(W\) a \(G\)-clique, so \(zy\in E(G)\); the displayed
two-edge path is vertex-distinct and has no accidental complement shortcut.
C-103 permits additional complement edges anyway, so inducedness is not
being assumed.

The two C-103 boundary states are exactly

\[
\{w,z,r\},\qquad \{w,y,r'\}.
\]

If both were absent, C-103 would require the even path \(P\) and odd path
\(Q\) to have the same parity, a contradiction.  Hence at least one
boundary is retained; equivalently, if either is absent, the other is
retained.  Reversing the paths also satisfies the positive endpoint
hypotheses, but the latter equivalence already follows from “not both
absent.”

This is the exact first-reentry boundary:

- it applies only to the shared-\(w\), exact-\(\{u,w\}\) terminal row;
- it needs the second source \(y\) in the original C-133 bridge, because
  that supplies the common physical terminal \(t\);
- it proves retention of at least one boundary, not impossibility of the
  return; and
- a same-type source outside the bridge ridge remains open.

The second terminal row has source list \(\{u,v\}\), which cannot be a
C-133 bridge list because every bridge list contains \(w\).  It also
remains outside Theorem 4.1.

## 5. Independent equality-control replay

The clean-room checker decoded `HEhbtjK` without importing candidate
code.  It obtained:

| quantity | exact result |
|---|---:|
| order, size | \(9,18\) |
| \((\gamma,i,\alpha,\gamma^\infty,\theta)\) | \((3,3,3,3,3)\) |
| greatest triple-family size | \(48\) |
| one-guard obligations | \(288\) |
| retained response moves | \(324\) |
| compatible response-list colorings | \(2\) |

The kernels with one and two guards are empty; the three-guard kernel has
48 states.  Its canonical state hash is

```text
0407eeddf7ec74469eb80a227cbbe8a9c95d39a33c7fd95dd47bc562437be60f
```

and the complete obligation/response digest is

```text
86548345b4342edeb21233ae9195be03eaf502db81b86596f1dafa41819d7c81
```

At \(S=012\), the independently recovered lists are

\[
\begin{array}{c|cccccc}
x&3&4&5&6&7&8\\ \hline
L(x)&01&02&12&12&02&01.
\end{array}
\]

For frozen color \(0\), the components and bipartition sides are

\[
\{1\}\mid\{2\},\qquad \{5\}\mid\{6\}.
\]

The second is the target component.  Sources \(3,8\) have the same list
\(\{0,1\}\), and their target incidences are

\[
N_H(3)\cap\{5,6\}=\{5\},\qquad
N_H(8)\cap\{5,6\}=\{6\}.
\]

They are independently exposed for color \(0\):

\[
P_0^+\cap N_H(3)=\{4,8\},\qquad
P_0^+\cap N_H(8)=\{3,7\}.
\]

However, in the frozen-\(2\) projection the source component is the edge
\(3-8\), with sides \(\{3\}\mid\{8\}\).  Thus every proper response
coloring gives the two sources opposite colors.  The graph refutes raw
same-list side synchronization but does not realize the dynamically
relevant same-color return.

## 6. Independent gamma-two boundary replay

The clean-room checker separately decoded `HFzvvn{` and recovered exactly

\[
E(H)=\{01,02,12,34,45,56,68,78,47\}.
\]

After banning precisely the forbidden direct root swaps and applying
simultaneous greatest-fixed-point deletion inside that restricted pool,
the deletion rounds have sizes

\[
15,\ 4,\ 4
\]

and leave the claimed 52-state family.  Its canonical state hash agrees
with the candidate:

```text
55dca721bffff9e732f9ba80771809aac67e7940b7ab64762fc1010534193a85
```

All \(52(9-3)=312\) unoccupied attacks have a legal retained response.
There are 470 retained response moves in total, and the complete
obligation/response digest is

```text
0852bcb93ea826f68b723c36d324f13dc83e4cc78a84626c70b70a0c3c765bb5
```

The exact reconstructed parameters are

\[
(\gamma,i,\alpha,\gamma^\infty,\theta)=(2,2,3,3,3).
\]

This recomputation is stronger than assigning
\(\gamma^\infty=3\) from the parameter chain: the one- and two-guard
greatest kernels are empty, while the unrestricted three-guard greatest
kernel has 83 states.  The restricted 52-state family is a proper eternal
subfamily of it.  Exactly 26 vertex pairs dominate.

At \(S=012\), the lists are exactly

\[
\begin{array}{c|cccccc}
x&3&4&5&6&7&8\\ \hline
L(x)&0&01&0&01&12&12.
\end{array}
\]

The frozen-\(2\) free component and sides are

\[
\{3,5\}\mid\{4,6\},
\]

along the path \(3-4-5-6\).  The singleton markers \(3,5\) force their
side to color \(0\), so both separated source ports \(4,6\) receive color
\(1\).  They are adjacent in \(G\).

The frozen-\(0\) target component is

\[
\{7\}\mid\{8\}.
\]

The two cross-clause edges are \(47,68\).  The first forces \(7=2\), the
internal edge \(78\) forces \(8=1\), and \(68\) is then monochromatic.
Independent enumeration finds zero compatible response-list colorings.

Both hubs are physically exposed for C-079:

\[
P_0^+\cap N_H(4)=\{3,5\},\qquad
P_0^+\cap N_H(6)=\{5\}.
\]

Yet

\[
N_H(4)\cap\{7,8\}=\{7\},\qquad
N_H(6)\cap\{7,8\}=\{8\}.
\]

Thus the separated same-color return is exact.  Its 26 dominating pairs
and \(\gamma=2\) keep it outside the equality target; it is not a
gamma--theta counterexample.

## 7. Reproducibility

The clean-room artifacts are:

```text
reviews/fresh_component_chain_hostile/independent_checker.py
SHA-256 aedf933a44a119890922a526ba91a49c94c15f23b6b6fb778725a89ea575d5a4

reviews/fresh_component_chain_hostile/independent_result.json
SHA-256 fe00f8691e47eceb685e7e256427683a85a16152a7655c328cb251a1ecb54377
```

The checker imports no candidate module or campaign evaluator.  It uses a
fresh graph6 decoder, set-valued graph representation, exhaustive subset
tests, a saturation-first complement-coloring search, and literal
simultaneous kernel deletion.  It verifies all parameter witnesses,
families, obligations, response lists, projection components,
bipartitions, side incidences, exposed mates, list colorings, and
dominating pairs.

The candidate's two standalone checkers were also replayed, and each
reproduced its frozen JSON result byte for byte.  The discovery-only
order-nine scan remains classified `OBSERVED`; this review did not promote
its coverage or its zero-cycle outcome.

## Final boundary

The revised theorem is a real but local advance.  A single bridge hub
cannot make an opposite-side return to a component that it entered, and a
second bridge-ridge hub cannot support a return with both C-103 boundary
states dead.  The latter conclusion may leave either boundary retained,
which is not itself contradictory.

Different hubs can select opposite target sides.  The equality control
shows this when their source colors are opposite, and the gamma-two
boundary shows an actual same-color separated return.  The gamma-three
separated-source case remains open, as do arbitrary chains and all global
conjectures.
