# Adversarial audit of proposed quantitative extensions

Checkpoint: **2026-10-06 22:49 PDT** (America/Los_Angeles). Independent internal research agent; no external individual was contacted, no Git operation was performed, and no existing reviewed-package file was changed. Estimated completion of this bounded extension-priority audit: **95%**. The remaining 5% reflects limitations of any finite current-literature search, not a mathematical gap in the matrix calculations below. The group's full source adaptation is a separate verification task.

## Decision

The original scalar idempotent and absorbed projective conclusions remain affirmatively duplicated by the user's public triage. Neither appending an improved rose-generator count nor citing a classical embedding theorem licenses calling those conclusions a new discovery.

The stronger proposed statement has a distinguishable, checkable addition:

> In the October 4 construction's unchanged seven-extra-letter Fano-complement type model, with its unchanged turn weights and an arbitrary allowed inverse pairing, the least dyadic projective-plane order q >= 4 for which the squared turn matrix has spectral radius below one is q = 32. Orders 4, 8, and 16 have spectral radius strictly above one. At q = 32 the original asymptotic construction can use 1064 directed letters, hence a 532-edge rose, once its remaining source proof is checked with the changed constants.

**I found no affirmative prior disclosure of this exact calibration, three-class matrix reduction, or exact obstruction at q = 16 in the inspected source, its relevant companions, or the user's public triage.** The source fixes q = 128; it does not state a parameter theorem or identify the smallest working order. Its displayed general-q formulas make the q = 32 upper estimate an easy refinement, but do not explicitly state or prove the smaller-order obstruction.

My recommendation is **a narrowly framed quantitative refinement note is defensible under the user's protocol, if the full q = 32 adaptation passes independent mathematics and package review**. Its significance is modest. Its main contribution must be the exact spectral calibration and its restriction to this model; inherited idempotent/projective conclusions can explain why the calibration is relevant. This is not a new method, a new general embedding theorem, an optimal generator theorem for group-algebra counterexamples, an independent solution of direct finiteness, or a reason to hide the earlier public triage. The exact calibration is an extension of the construction rather than merely a relabeling of the duplicated core. No claim of first priority is established or recommended.

## What is already public

The affirmative duplication evidence remains the exact public [algebra triage, section 1](https://github.com/AlecKriebel/Math/blob/f27318d83bd7000ef817957a9a4b3087de28d198/openai_followon_batch2_20261006/agent_notes/algebra_groups.md), together with the [batch report, section 4](https://github.com/AlecKriebel/Math/blob/f27318d83bd7000ef817957a9a4b3087de28d198/openai_followon_batch2_20261006/REPORT.md). These disclose the same October 4 input, scalar defect e = 1 - ba, extension to every characteristic-two field, P = eR, the complementary decomposition, right-module isomorphism maps, and [P] = 0. The existing `PRIORITY_AUDIT.md` supplies the remote custody evidence. These public files say nothing about q = 32, a sharp threshold for the squared turn matrix, or a 532-edge random-cone model.

The pinned [October 4 source](https://github.com/openai/math/tree/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/A-Torsion-Free-Group-Algebra-That-Is-Not-Directly-Finite-October-4-2026) fixes q = 128 in `build/sections/random.tex`, uses v = 16513 and seven extras, and verifies a sufficient positive-vector inequality for that choice. The inspected source has no q = 16/32 calibration, no three-class quotient matrix, and no least-order claim. The numerical constants 129, 136, 64.5, 65, 62.5 and 31.25 appear in its degree and expansion bounds; the closing-path argument in `planar.tex` uses the same minimum degree only to retain degree at least three after deleting at most two incident edges. Any actual refinement must propagate all those constants, not only replace the initial q.

The [September 23 zero-divisor companion](https://github.com/openai/math/tree/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/A-Torsion-Free-Group-Algebra-with-Zero-Divisors-September-23-2026), `build/sections/types.tex`, also fixes q = 128. It has **three** extras and different extra-extra turn weights. Its matrix is not the unchanged seven-extra model at issue, and its witness vector has values 5 and 1 rather than 4 and 1. It does not establish this exact threshold. The October 4 paper attributes its random matching and geometric framework to that companion; the refinement must preserve that attribution.

The [September 23 direct-finiteness companion](https://github.com/openai/math/tree/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/A-Counterexample-to-Kaplanskys-Direct-Finiteness-Conjecture-in-Characteristic-Two-September-23-2026), `build/sections/06-cellular-automata.tex`, already proves that a group embedding induces an injective group-algebra map and transports scalar one-sided inverses. Its input contains torsion and is not the October 4 F_2 torsion-free group. This is prior disclosure of the transfer mechanism, not the new spectral calibration.

## Independent exact check of the calibration

These calculations were derived independently from the source weights, without relying on another agent's proposed theorem or computed eigenvalues. Only the finite matrix calibration is certified here; the entire modified probabilistic/topological construction has not been reaudited by this agent.

Let v = q^2 + q + 1, p = (q+1)/v and z = 1/(q+1)^2. Partition actual letters t into three classes:

1. S: the seven ordinary letters paired with extras;
2. E: the seven extra letters;
3. O: the v-7 remaining ordinary letters.

For the squared turn matrix M(t,u) = w(t,u)^2 with the inverse successor forbidden, a vector constant on these three classes is taken to another such vector. In class order S,E,O, the exact quotient is

```
Q(q) = [ 7 p^2       3/2          (v-7) p^2 ]
       [ 6 z         7 p^2        (v-7) z   ]
       [ 7 z         7 p^2        (v-8) z   ].
```

The first row has six allowed extra successors, each with squared weight 1/4. The second row excludes one of the seven special ordinary successors. The third excludes one of the ordinary O successors. This count depends only on class sizes, so it is independent of which extras are paired with which distinct ordinary letters and how the remaining ordinary letters are paired.

Every entry of Q is positive for q >= 4. A positive Perron vector for Q lifts to a strictly positive eigenvector for M, so its eigenvalue is the spectral radius of M. Alternatively, the upper and lower positive-vector bounds below directly prove the needed conclusions for M without computing any floating-point eigenvalue.

For q = 32, use the source's vector (4,1,1). The ordinary-row upper bound and the normalized extra-inverse row bound are exactly

```
q/(q+1) + 7 p^2 + 21/(q+1)^2 = 57694220/57937341 < 1,
(3/2 + (v+21)p^2)/4           = 116319/182408      < 1.
```

Their positive margins are respectively 243121/57937341 and 66089/182408. Hence M f <= lambda f for a fixed lambda < 1 and the source's squared word mass decays exponentially. Here v = 1057, |T| = 1064, and |T|/2 = 532. The minimum/maximum degrees become 33 and 40, and the expansion exponent becomes 33/2 - 2 = 14.5, which is positive. The girth constants may be chosen smaller as needed, independently of n.

For each smaller admissible dyadic q, the following strictly positive integer vector has Q f - f strictly positive. All displayed differences were computed with Python's exact `fractions.Fraction`, not numerical eigensolvers:

| q | f on S,E,O | Exact coordinates of Q f - f |
| --- | --- | --- |
| 4 | (100000,46946,48338) | (3053297/63, 35835416/1575, 36897722/1575) |
| 8 | (100000,40183,40835) | (126613441/10658, 686724688/143883, 2094029201/431649) |
| 16 | (100000,38596,38807) | (6775892/10647, 757922962/3076983, 760201420/3076983) |

With r = min_i (Qf)_i/f_i > 1, lifting f gives Mf >= r f. Choose c > 0 such that the all-ones vector is at least c f. Then

```
1^T M^(h-1) 1 >= c r^(h-1) 1^T f.
```

Thus the squared word mass grows exponentially for q = 4,8,16 and cannot satisfy the exact source decay lemma with any delta > 0. This is an obstruction to the **unchanged turn-weight proof mechanism**, not a nonexistence theorem for group-ring examples, graphs, or alternative estimates at those orders. The source's degree or parity construction itself need not fail at q = 16.

There is no smaller q to check between these powers of two. q = 2 is outside the stated q >= 4 domain and also fails the unchanged source's simultaneous integer-count prescription: its two extra-count integrality requirements would demand incompatible congruence classes of m. No global optimality is implied.

## Classical two-generator embedding subsumes a global rank headline

[Higman, B. H. Neumann and Hanna Neumann, *Embedding theorems for groups* (1949), Theorem IV, pp. 251–253](https://londmathsoc.onlinelibrary.wiley.com/doi/pdf/10.1112/jlms/s1-24.4.247), already embeds every countable group in a two-generator group. Its construction preserves a finite relation list and uses free products, finitely many HNN extensions, and a finite-rank free amalgamation for finitely generated inputs. This original full text was inspected, including all stages of the proof.

[Bridson and Nyberg-Brodda, *HNN Extensions and Embedding Theorems for Groups*, arXiv:2512.10800v1, section 2.3, Remark 2](https://arxiv.org/html/2512.10800v1), explicitly records preservation of the finiteness properties F_d and FP_d and torsion-freeness by that classical construction. Remark 3 records its algorithmic character. These are established properties, not new embedding results.

For the stronger finite two-dimensional classifying-space condition, a direct graph-of-spaces argument uses a finite 2D K(G,1) as the vertex space and finite graphs for the associated free subgroups. Mapping cylinders of the graph maps add only cells of dimension at most two. The universal cover is a tree of contractible vertex/edge spaces, so it is contractible. This deduction is standard topology of precisely the already disclosed construction. It does not require a new theorem about group-algebra witnesses.

An injective group map preserves distinct basis elements and induces an injective group-algebra map. Consequently a valid upstream example embeds into a two-generator torsion-free group H with a finite 2D classifying model, and its same scalar a,b,c transport to F_2[H]. Classical algebra gives the idempotent and absorbed cyclic projective there. The 532-rose statement is therefore **not** an improvement in the least number of group generators achievable among all examples. It is an improvement within the particular unchanged random-cone construction. A paper must distinguish those claims explicitly.

I found no exact earlier public statement of the two-generator idempotent/absorption consequence in the inspected sources. That bounded absence cannot justify claiming a new embedding mechanism; conversely the classical general theorem alone is not an affirmative duplicate of every later specialized corollary. The two-generator corollary could be stated with accurate attribution, but it should not be used as the purported main new result of this refinement package.

## Searches, limits, and evidence custody

All searches and reads were made on 2026-10-06 PDT. Queries included `Kaplansky direct finiteness two-generator`, `Kaplansky idempotent two-generator`, `directly finite Higman Neumann`, the exact October 4 title, `Fano direct finiteness`, `q=32 group algebra`, `q = 32 squared weights group`, and torsion-free two-generator embeddings with finite classifying/aspherical presentation constraints. Only primary mathematical sources and inspected pinned source files were used as evidence for mathematical claims. Search snippets and third-party indexes served only as locators. The exact-title search located the upstream index, but no smaller-order calibration. Negative keyword results are not proof of universal novelty.

A whole-pinned-corpus search for two-generator language and HNN1949 located the known universal-group companion and earlier torsion direct-finiteness construction; it did not locate this spectral calibration. A targeted numerical/general-q search of the October 4 and relevant zero-divisor source files located the fixed q = 128 choices and the sufficient inequalities described above. The universal group companion invokes classical HNN machinery and a different F_infinity construction; it does not supply a seven-extra spectral threshold.

Read-input SHA-256 hashes:

| File | SHA-256 |
| --- | --- |
| `notes/ORIGINAL_REQUEST.txt` | `e9a57bae398aeb56c13b087592890c4004d873eff2cb3c55c627ef6a1d2c8295` |
| `notes/PRIORITY_AUDIT.md` | `630e4e0d5f329d5ad18e91b00c91a699a68fd1294c73ee9cfbfb696b1efbd598` |
| `notes/priority_evidence/REMOTE_TRIAGE_ALGEBRA.md` | `d0ecbc688e8ff706c3c392a8cfcbb9cb6b3a51228c32c22420b7a6c0d7f1de66` |
| October 4 `random.tex` | `bb172b92ba622e262c2bf124e70c3cd55922200083c09db658615759b81323c4` |
| October 4 `planar.tex` | `e3a1a4e23dd6871a9746ffde05d32297e695f3167b8efa0f0a4cad5da8c9ae6b` |
| September 23 zero-divisor `types.tex` | `3f74603230f7f21a25f5f8f9879168fa7a02eda0cea10bb195a5868e221a5cfc` |
| September 23 direct-finiteness `06-cellular-automata.tex` | `f24be1d93784302e0700c0223023c0f4f49a9c2e342e21be04a5627ae0492775` |

No live-service priority timestamp has been invented for this new note. This note's local timestamp does not establish first public disclosure. The parent researcher controls actual checkpoint publication, exact package reviews, Zenodo gates, and project completion estimates.
