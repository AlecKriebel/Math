# PR367 independent mapping-class geometry review

**Verdict: qualified PASS for the exact fixed-generator quotient question.** No mathematical correction is required within that scope. The result has four strict Hurwitz classes and three classes after simultaneous conjugation. Historical novelty and worldwide open status are unverified. This report is an independent AI-assisted review, not external peer review.

Frozen candidate head: `d977c9564f079cde975a7b4261776eb9061c5f5f`. Base: `efd29c05204703acca9a0860812f54b94fae54b1`. The entire target contains 43 files; the only other changed path is its queue file. All 44 frozen changed-path identities were checked. No candidate, Git, service, or external-person mutation was performed.

## Independence and source identity

Before reading candidate prose, programs, outputs, statuses, final claims, history, old reviews, or sibling mathematics, I downloaded the three routed primary PDFs, checked their exact bytes/SHA-256, read the original questions and hypotheses, and visually inspected Wajnryb's printed p.126. SOURCE_SEAL.json seals that baseline at `2026-10-03T13:41:54.699838Z`. Source PDFs, extracts, and renders remain ignored and private.

I next read only mathematical ranges of TURN_1.md through TURN_4.md. I independently derived the geometry and linking implications, implemented a faithful B6 action control and a separate Aut(F4) walk enumeration, and sealed that assessment at `2026-10-03T13:48:31.915060Z` in MATH_SEAL.json. At that point the precise remaining gap was full verification of the thirty-letter all-edge certificate. Candidate programs, outputs, states, final claims, history, source-gate triage, and old reviews were read only afterward. Substantive conclusions were held until the parent confirmed its own mathematical seal at `2026-10-03T13:52:12.981874Z`.

Primary sources checked directly:

| Source | Bytes | SHA-256 |
|---|---:|---|
| [Farb volume, Wajnryb and Auroux chapters](https://www.math.uchicago.edu/~farb/papers/mcgbook.pdf) | 2724624 | `f37c6a1dbc875105c2b294196de1a03a88595b75e8705e6077e9d48f066e402a` |
| [Baykur–Monden–Van Horn-Morris, arXiv v2](https://arxiv.org/pdf/1412.0352) | 390564 | `90fd9b5d03147e742074cb79f6c48dee809b97fd5fa6f3850e52964c4a67721d` |
| [Published AGT paper](https://msp.org/agt/2017/17-3/agt-v17-n3-p06-s.pdf) | 420428 | `479fb4d84d5fa40a90aa897a58d7fbf2c0559d879042f5173a01f91492199331` |
| [González-Meneses, Basic results on braid groups](https://www.numdam.org/item/AMBP_2011__18_1_15_0.pdf) | 1037965 | `d094faad7803b263e742e5b128f6c8aac5603c7ea94c8f9dd3b330820d6c7edc` |

The fourth source was fetched after the mathematics seal. Its §§1.6 and 4 explicitly support faithful Artin action, positive monoid embedding, and full twist centrality. A browser-tool access error was bypassed by retrieving the identical primary PDF directly; this limitation is recorded in FAILURE_LEDGER.md.

## Original claim and scope

Write

\[
 c_0=a_1a_2a_3a_4,\quad C=c_0^5,\quad
 H=a_5a_4a_3a_2a_1^2a_2a_3a_4a_5,\quad
 Z=(a_1a_2a_3a_4a_5)^6,
\]

and let \(Q=B_6/\langle\!\langle CH^{-1}\rangle\!\rangle\).

Wajnryb's printed p.126 asks whether **every** positive word in the five named generators with image \(C^2\) has length 40, 30, or 20, and whether its factor tuple is Hurwitz equivalent to the corresponding standard tuple \(C^2,Z,H^2\). There is no length cutoff in the source and no quantification solely over finite images. The proposed packet addresses exactly these fixed-generator words. Arbitrary conjugate factors, arbitrary nonseparating Dehn twists, and unrestricted geometric factorizations are larger domains.

Auroux's printed p.131 defines adjacent Hurwitz moves, then introduces simultaneous conjugation separately. Wajnryb references that chapter but does not give a separate convention. Supplying both outcomes is correct: the strict single forty-letter class statement is false, while the three-class statement with simultaneous conjugation is true. The source's closed genus-two comparison assumes irreducible singular fibers and transitive monodromy; it does not imply the boundary quotient classification. In particular the first four generators fix the sixth point in the permutation quotient.

## Geometric map and the universal ceiling

Take the regular neighborhood of a five-curve chain. It has genus two and two boundary components. An endpoint-deleted four-chain neighborhood has genus two and one boundary; its complement in the five-chain neighborhood is a pair of pants. Capping exactly one outer boundary turns that complement into an annulus. Thus the four-chain neighborhood boundary is parallel to the retained surface boundary. The same argument applies after deleting the other endpoint.

The classical chain relations consequently give

\[
 \operatorname{image}(C^2)=t_\delta,
 \qquad \operatorname{image}(Z)=t_\delta
\]

on \(\Sigma_2^1\). The B6 identity \(Z=CH\), independently checked with exact free-group action, implies that \(C\) and \(H\) have the same geometric image. Therefore the geometric map descends to \(Q\). Every positive Q representative of \(C^2\) produces exactly its word length in positive nonseparating twists of the single boundary twist. No injectivity of Q is needed.

Baykur–Monden–Van Horn-Morris Theorem A applies with **genus two, one boundary, boundary fixed pointwise, and nonseparating factors**, and gives maximum 40. This is a credited prior theorem, not a new computational discovery. The geometric implication genuinely bounds all words in the original algebraic quantifier.

All braid generators become one abelianization class. The added relation imposes \(20x=10x\); conversely sending each generator to 1 modulo 10 respects the presentation. Thus \(Q_{ab}=\mathbb Z/10\). The only remaining possible lengths are 0,10,20,30,40. The equalities \(C^2=Z=H^2\) realize the last three.

## Linking proof and forty-letter slice

The relation is pure, so the S6 permutation map descends. A representing word is pure in B6. Let \(L_{ij}\) be its labelled-pair linking number, half its signed crossing count. Conjugation permutes these coordinates, and normal-closure membership gives integers \(t_i\) such that

\[
 L_{ij}=\beta_{ij}+T-2(t_i+t_j),\qquad
 T=\sum t_i=m/10-4,
\]

where \(\beta\) equals 2 on pairs among the first five vertices and 0 otherwise. Positivity gives \(L_{ij}\ge0\). These coefficients have no bounded-box assumption.

For m=0 or10, putting \(s=\sum_{i\le5}t_i\), internal inequalities give \(s\le-3\), whereas external inequalities give respectively \(s\ge-2\) or \(s\ge-1\). Hence both lengths are impossible. For m=20 the solution vectors give twice a star; for m=30 they give every pair linking number 1; for m=40 they give twice a five-vertex clique with one isolated vertex. The complete integer derivations are preserved in MATH_BASELINE.md, independently sealed before checker access.

At m=40 an isolated strand never crosses anything, by positivity. If it were an interior strand, the two sides could not cross each other, contradicting the clique linking requirements. Only endpoint isolates remain. Each word therefore uses one endpoint four-generator chain. Perron–Vannier's A4 injection applies because its surface is the four-chain regular neighborhood, unchanged by adding the annular collar after capping. Geometric image equality then proves B5 braid equality to the appropriate standard word. This is the only place where that subgroup injection is needed.

The positive braid monoid embeds in the braid group. Equality is therefore generated by positive commutations and braid relations, each implementable by Hurwitz moves. For the braid relation, two inverse Hurwitz moves take \((x,y,x)\) to \((y,x,y)\), using \(y^{-1}xy=xyx^{-1}\).

The two endpoint standard tuples generate different permutation subgroups: the S5 fixing6 and the S5 fixing1. A Hurwitz move preserves the subgroup generated by the entire tuple, so these classes are strictly distinct. Simultaneous conjugation by \(a_1a_2a_3a_4a_5\) relates them. There are exactly two strict forty-letter classes and one after conjugation.

## Twenty-letter complete reduction

The star linking pattern means that the five noncentral strands never cross each other. Their relative order stays fixed. The central strand walks to adjacent positions among six slots, and each of the five edges crosses the same noncentral label four times. Returning to its initial slot restores the entire permutation. This characterizes every possible twenty-letter representative by a finite complete walk set.

My separately entered F4 tuples, free reduction, and composition implementation checked every inverse and defining relation, including C=H. Its independent enumeration gives 81,162,162,162,162,81 candidates across start positions, totaling810. Exactly ten words have the target action; they are precisely the literal rotations of H². This computation preceded candidate-code/output access.

The F4 test is used only for rejection. Each survivor has a sufficient Q certificate because H²=C²=Z is central, so cyclic rotation preserves the product. Strict Hurwitz moves implement those rotations for a central total product. Thus all representatives form one strict twenty-letter class. No faithful Q action or finite-image sufficiency claim is assumed.

## Thirty-letter complete certificate

Every pair crosses exactly twice. The candidate graph records all fifteen pair counts in {0,1,2}, and each step swaps currently adjacent labels and increments exactly their count. Each edge raises total count, so the graph is acyclic and has depth at most30. Pair parities determine relative label order, so count-state merging loses no possible continuation. It does not itself prove equality of braids.

A reachable count vector c is completable precisely when f-c is reachable. Reversing a positive suffix gives a complement path, and reversing a complement path gives a permissible positive suffix. This is reversal of adjacent swaps, not braid inversion. Every prefix of a completable state is also completable.

Canonical actions are computed as six full freely reduced words. Exact action equality is checked on **all** edges in the completable subgraph. Induction then makes action independent of the complete path. A separate direct action of Z agrees at the terminal state. Faithfulness of the classical Artin action proves actual B6 equality, and positive monoid embedding then proves strict Hurwitz equivalence to Z.

Both complete author implementations were inspected and executed. They gave 234368 reachable states, 711342 reachable edges, 90921 completable states, and 261810 completable edges, with every required literal free-word comparison passing. The state-action digest is

`af2b8ec569d613e4f3d8ba3b72d18e85e8c612f4265057b7f4c485d544d159bf`.

The full C++ output was retained privately as a verified lossless gzip. It contains 90921 state records and terminal JSON, with 15258555 uncompressed bytes and SHA-256 `02e9b23c38e426f1bc5103ce216d1b996b02a33c3cf5cad82b88f996e52bc95d`. Its compressed size is 1244547 bytes. This closes the computational gap recorded at the mathematics seal. Hashes serve integrity only; the programs compare the actual reduced words first.

## Distinct geometric falsifiers

I independently checked torus and genus-two homology actions, the exact B6 full-twist identity, permutation transitivity, and explicit false positives.

1. On the closed torus, A=[[1,1],[0,1]] and B=[[1,0],[-1,1]] satisfy ABA=BAB and (AB)^6=I. On the one-boundary torus the corresponding product is the boundary twist. Closed homology therefore erases the boundary information needed in this problem.
2. The five genus-two chain transvections satisfy all Artin relations. C and H both act as -I4, and C²,Z,H² as I4. This agrees with the chain geometry but cannot prove boundary equality or classification.
3. C²a1^6 has the same S6 and Sp4(F3) images as C², but its length46 violates the Q abelianization constraint. Thus joint finite images can accept an actual nonrepresentative.
4. Even within the genuine bound40, a1^40 has the same length, Q abelianization, S6 image, and Sp4(F2) image as the target. Its integral homology has entry40 above the diagonal and is not I4, proving Q inequality. This is a stronger bounded false-positive control.
5. Every F4 generator preserves b=(1,-2,3,-4,-1,2,-3,4), and the target action is conjugation by b. This independently checks the boundary-word behavior of the presented action. It does not presume its faithfulness.

The candidate survives these falsifiers because it proves the universal geometric ceiling and supplements necessary tests with sufficient Q certificates. It does not infer Q equality from finite-image acceptance.

## Reproduction and integrity

The complete publication verifier ran on an untouched private copy. All four Python stdout receipts matched byte for byte; the C++ wrapper matched; and the old review's independent checker matched its recorded JSON. Complete stdout and stderr are retained under reproduction_streams. The standalone old review replay program was also executed with the private copy as its explicit root and matched AUTHOR_REPLAY.json exactly as parsed JSON.

Seven manifest layers all match: turn manifest sizes6,6,6,8; final author33; review5; publication42. Including their own outer manifest files accounts for the README's 34 author and six review files. The three recorded checkpoint receipts' Git blob identities match every file (7,14,21 entries), and the actual local objects at all three immutable commits match those same bytes. All43 target files exactly match the frozen head. The queue row also exactly matches frozen head. The merge parents are the frozen base and author WIP `a440a519393bf4c68433c6a8cdd49b384d3bfca6`.

The old review was read after my independent mathematics seal and was not used to set success criteria or establish the mathematical assessment. Its reported checks were reproduced as artifacts, not accepted as authority.

## Strongest verified result and exact remaining gap

For the source's fixed-generator positive words in Q representing C²:

| Length | Strict Hurwitz classes | With simultaneous conjugation |
|---:|---:|---:|
| 20 | 1, represented by H² | 1 |
| 30 | 1, represented by Z | 1 |
| 40 | 2, represented by C² and (a2a3a4a5)^10 | 1 |

There is no remaining mathematical gap found in this scoped result. The credited inputs are the published genus-two maximum40, classical chain relations, Perron–Vannier subgroup injection, Artin faithfulness, and Garside positive-monoid embedding. No independent rediscovery or novelty certification is claimed for these ingredients or for the complete classification. Larger geometric classification questions and historical novelty are outside this verification and remain unestablished here.

No mandatory candidate correction was found. Keep the fixed-generator scope and both equivalence conventions prominent in any disposition or publication.
