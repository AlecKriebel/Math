# Hostile review: inactive induced-\(C_5\) attack exclusion

Review date: 2026-07-28 PDT

Frozen target:
`math/working/inactive_odd_cycle_attack/NOTE.md`

Frozen target SHA-256:
`5ccd88e833db4794a834000a3f72e8ca32efbb339559800728ab0ef196861393`

Frozen certificate manifest SHA-256:
`3260bd78dd4a8726b2b16f92fcc3dfafc8309531133c3ae34f0f0d3ba24193d7`

Independent checker SHA-256:
`5dabaea59b897d243e85c2efb3a3fff9b18713ba50d7cefaa9a7285752092021`

Independent evidence SHA-256:
`ef321da56ab5bdb8be8c36c99c7072d20d9b7a17d9c6a2c04cbf655096e27444`

## Verdict

**UNCONDITIONAL PASS.**

For the frozen source and manifest above, the certified local lemma and its
stated active/inactive-set corollary are correct.  In the one-guard model,
under

\[
 \alpha(G)=\gamma^\infty(G)=3,\qquad \gamma(G-x)\ge 3,
\]

the family-relative inactive graph

\[
 \overline{G-x}[R_x]
\]

has no induced \(C_5\).

This verdict has exactly the scope stated in the candidate note.  It does
**not** exclude induced odd cycles of length at least seven, prove that
\(\overline{G-x}[R_x]\) is bipartite, prove the full \(k=3\) case, or
resolve the gamma--theta conjecture.  The word **induced** and the deletion
hypothesis \(\gamma(G-x)\ge3\) are essential to the reviewed reduction.

I found no omitted witness-identification case, occupied attack, all-guards
move, nonedge move in \(G\), missing retained successor, missing domination
condition on a retained template state, complement reversal, or unsound
assumption that outside vertices cannot matter.

## 1. Mathematical reduction

### 1.1 Every maximum independent triple is retained

The forcing fact used in the corollary is valid for every eternal
three-family \(\mathcal F\), not only for the greatest fixed point.

Let \(I\) be an independent triple and begin in any state of the nonempty
family.  Attack the currently unoccupied members of \(I\), one at a time.
A guard already on \(I\) cannot move to a later attacked member of \(I\),
because \(I\) is independent.  Each attack therefore increases the number
of guards on \(I\) by one.  Since the family has three guards, the process
ends at the state \(I\), which consequently belongs to \(\mathcal F\).

Under \(\alpha(G)=\gamma^\infty(G)=3\), every \(H\)-triangle is such a
maximum independent triple of \(G\).  Thus every triangle constructed in
the candidate proof belongs to the arbitrary chosen optimal family.

### 1.2 The deletion domination hypothesis gives all five witnesses

Let \(r_ir_{i+1}\) be a rim edge of the induced \(C_5\) in
\(H-x=\overline{G-x}\).  Because \(\gamma(G-x)\ge3\), the pair
\(\{r_i,r_{i+1}\}\) does not dominate \(G-x\).  Hence there is a deletion
vertex \(p_i\) outside the pair that is nonadjacent in \(G\) to both
endpoints.  Equivalently,

\[
 r_ip_i,\ r_{i+1}p_i\in E(H),
\]

and \(\{r_i,r_{i+1},p_i\}\) is an \(H\)-triangle.

The witness cannot be another rim vertex.  In an induced \(C_5\), two
consecutive rim vertices have no common neighbor on the rim.  It also
cannot equal \(x\), because failure to dominate was taken inside \(G-x\).
Thus every \(p_i\) satisfies the local lemma's disjointness requirement.
The five witnesses may otherwise coincide arbitrarily.

### 1.3 Inactivity supplies precisely the ten absent successors

Each rim vertex lies in at least one of the maximum independent witness
triples.  C-108 makes its ability to answer at \(x\) independent of the
chosen retained independent triple containing it.  Moreover, if

\[
 T-v+x\in\mathcal F
\]

for an independent triple \(T\), that successor must dominate the omitted
vertex \(v\).  The two unchanged guards miss \(v\), so this membership
itself forces \(vx\in E(G)\).  Therefore a supported vertex outside
\(A_x\) has no retained \(v\)-move successor.

Both endpoints of every rim edge lie in \(R_x\).  This gives exactly

\[
 T_i-r_i+x\notin\mathcal F,\qquad
 T_i-r_{i+1}+x\notin\mathcal F
\]

for all five witness states, with no assumption about a response by
\(p_i\).

## 2. Equality-pattern coverage

Equality among the ordered witnesses
\((p_0,p_1,p_2,p_3,p_4)\) is an arbitrary set partition of five positions.
Labeling its blocks in order of first appearance gives a unique
restricted-growth string.  Conversely, every such string specifies one
and only one equality pattern.  Thus the case split is exhaustive and
nonredundant.

The clean-room checker enumerates all \(5^5\) label words, independently
recognizes the first-occurrence-normalized ones, and obtains exactly the 52
patterns in the manifest.  Their block-count distribution is the expected
Stirling-number row:

| distinct witness blocks | template order | cases |
|---:|---:|---:|
| 1 | 7 | 1 |
| 2 | 8 | 15 |
| 3 | 9 | 25 |
| 4 | 10 | 10 |
| 5 | 11 | 1 |

No additional identifications with the rim or target are possible by
Section 1.2, so these 52 cases cover the stated arbitrary-graph reduction.

## 3. Literal CNF semantics

The hostile checker imports neither the candidate certificate generator nor
its reconstruction checker.  It allocates the edge, family, and response
variables from scratch and reconstructs every DIMACS byte.

For every retained template triple \(D\) and every template vertex
\(y\notin D\), the reconstructed clauses say:

1. \(D\) has a \(G\)-neighbor of \(y\), so it dominates \(y\);
2. at least one current guard \(u\in D\) is selected as a response;
3. that response requires \(uy\in E(G)\); and
4. the exact state \((D-\{u\})\cup\{y\}\) is retained.

Only unoccupied attacks are encoded.  Every response marker represents one
current guard and one one-swap successor.  The formula permits more than one
response marker to be true for the same attack.  This is sound: the game
requires the existence of a legal one-guard choice, not uniqueness of the
choice; multiple true markers do not encode simultaneous movement.

The induced-rim clauses specify all ten rim pairs, not only the five cycle
edges.  Each witness block has both required \(H\)-edges, its named triple is
retained, and both endpoint-move successors at \(x\) are absent.

Across all 52 reconstructed formulas, the independent clause audit found:

| clause group | clauses |
|---|---:|
| retained-state domination | 26,660 |
| one-guard closure | 186,620 |
| induced-\(C_5\) rim | 520 |
| witness states and inactivity | 1,300 |
| **total** | **215,100** |

The 215,100 clauses contain 535,020 literals in total.

## 4. Why outside graph data cannot rescue the configuration

Suppose a real, arbitrarily large graph and eternal family satisfied the
local lemma's hypotheses.  Restrict attention to the rim, the distinct
witnesses, and \(x\).

Assign each template edge variable its literal value in \(H\), and assign a
template family variable according to literal membership of that triple in
the real family.  A retained real state dominates every template vertex.
For an attack at a template vertex, every current guard is already in the
template.  A legal one-guard move therefore uses a template guard, traverses
an edge whose two endpoints are in the template, and produces another
template triple.  Choosing one such real response satisfies the corresponding
response marker clauses.

Thus every real configuration would induce a satisfying assignment of its
template CNF.  Edges among named vertices were left free and are already
represented.  Edges to outside vertices and attacks outside the template
were omitted.  Their omission can allow spurious retained states, but cannot
remove any assignment induced by a real family; it makes the CNF weaker.
Consequently, UNSAT of every template formula excludes every larger graph as
claimed.

## 5. Certificate and integrity audit

The checker reconstructed all 52 instances byte-for-byte and verified every
manifest hash, including the CNFs, proofs, solver logs, checker logs, pinned
solver, and pinned proof checker.  The 208 case files on disk are exactly the
208 files named by the manifest.  It then independently invoked the pinned
`drat-trim` binary on every CNF/proof pair.

The decisive results were:

- all 52 independently generated DIMACS byte strings matched;
- all 52 DRAT proofs replayed with `s VERIFIED`;
- the pinned `drat-trim` SHA-256 was
  `31df522b8b2b71acd357723b0e826cf488826ed78ad9e3a7bcad241271812beb`;
- the pinned CaDiCaL SHA-256 was
  `51c3c82b354f455c925fc60b37c701e8498afcf0f3bfab9a06e62149485df5f6`;
- the total proof size was 276,375 bytes.

The solver's original UNSAT assertions are not being trusted as
certificates; the successful DRAT replays are decisive.

## 6. Independent \(C_4\) boundary audit

The hostile checker independently decoded

```text
OQifur}UO]}iTij]tpo}v
```

rather than trusting the candidate edge parser.  Its complement edge list
matched the frozen control data exactly.  Separate set-based evaluators then
recomputed

\[
(\gamma,i,\alpha,\gamma^\infty,\theta)=(3,3,3,3,3)
\]

for both the 16-vertex graph and its target deletion.

Additional clean-room checks found:

- full greatest eternal triple-kernel size: 304;
- deletion greatest eternal triple-kernel size: 252;
- deletion \(H\)-triangles: 18;
- all 18 deletion triangles belong to both relevant greatest kernels;
- 54 triangle/vertex response incidences obey C-108 propagation;
- active set:
  \(\{4,5,6,7,9,10,12,13,14\}\);
- inactive set:
  \(\{0,1,2,3,8,11\}\);
- exact inactive \(H\)-edges:
  \(01,03,12,23,8\,11\).

The root \(\{5,6,7\}\) is retained, all three root guards are adjacent to
target 15 in \(G\), and all three exact one-guard successors belong to the
greatest kernel.  Vertices \(0,1,2,3\) induce the claimed \(C_4\).

This control therefore correctly shows that “inactive graph is acyclic” is
false even in a full-root equality instance.  It remains a positive
gamma--theta equality graph with \(\theta=3\), not a counterexample to the
main conjecture.

## 7. Reproduction

From the repository root:

```text
python3 -I -B -W error \
  gamma_theta_eternal_domination/reviews/inactive_odd_cycle_attack_hostile/independent_check.py
```

The run writes `evidence.json` and ends with verdict
`UNCONDITIONAL PASS`.
