# Independent audit: the Ma–Tang seed's two-point extension obstruction

## Publication edition: finite certificates omitted

This prose/metadata edition preserves the complete general AP/strong-Sidon
equivalence, AP-linearity proof, affine candidate and normalization reduction,
and exhaustive all-real case classification. It reports the accepted
seed-specific computational theorem. The copied numerical seed list, AP edge
list, counting polynomial and coefficient lists, maximum-subset witnesses,
per-vertex count tables, extension catalogs, numerical example pairs,
executable code and raw certificates are omitted.

The seed-specific theorem cannot be independently reproduced from this edition
alone. This is not a complete self-contained proof of the seed-specific
computational theorem or a full computational reproduction package. The
finite premises are identified explicitly as separately verified statements;
they are not proved merely by the prose here. Hashes, aggregate counts and
match results identify the audited evidence; hashes alone do not prove the
omitted arithmetic. The general structural arguments and all-real reduction
are complete, with the dependence on those finite premises explicit.

## Verdict and exact scope

**ACCEPT the seed-specific theorem.** Let \(A_0\) be the exact 14-point
integer seed in Ma–Tang, arXiv:2602.23282v2, Lemma 5.1, printed page 13. If
a finite real \((4,5)\)-set \(B\) contains \(A_0\) with \(k=|B\setminus A_0|\le2\), then its largest strong-Sidon subset has size exactly \(8+k\). This also holds with any nonconstant affine image of \(A_0\) as the prescribed seed. The quantifier is over **all real extensions**, including irrational additions; it is not limited to the rational configurations in the computational catalogs.

The audited input is the report and certificates sealed by SHA-256 `da4f06b72a4113df16c39245004f49ddcfefd35854692eda9cce299a64d2bcfb`, with 45 members. All members matched their recorded lengths and hashes, and the complete input tree was unchanged after verification. Candidate Python files were read only as bytes for hashing: none was inspected as source, imported, or executed. No author-supplied or other downloaded mathematical code was executed.

**This does not settle Erdős problem 757.** No new universal bound, classification of all 16-point sets, statement about other seeds, or statement about three or more additions is accepted here. The located bounds remain \(9/17\le c_*\le4/7\). The independent audit establishes the finite obstruction and its universal-real reduction; it does not establish novelty.

## 1. Source identity and the distinct weak-Sidon problem

The precise seed coordinates and the baseline assertion occur in Ma and Tang, *Largest Sidon subsets in weak Sidon sets*, arXiv:2602.23282v2, Lemma 5.1, printed page 13. The version-specific primary PDF and arXiv record were checked online; a retained local PDF was independently extracted and its seed page visually inspected. The record describes a 15-page submitted version revised March 6, 2026. [Primary PDF](https://arxiv.org/pdf/2602.23282v2), [version record](https://arxiv.org/abs/2602.23282v2).

The paper's exact weak-Sidon extremal result concerns a different ambient class. It cannot replace a solution for \((4,5)\)-sets. Its Theorem 1.6 supplies the located \(9/17\) and \(4/7\) bounds. The lower bound uses Henning–Yeo; that dependency's full proof was **not independently audited in this review** and is unnecessary for the accepted extension theorem.

The candidate's finite sharpening \(h(A)\ge\lceil(9|A|+6)/17\rceil\) follows algebraically from the stated inequalities \(17\tau\le5n+3m\) and \(m\le n-2\). This checks the arithmetic conditional on the cited hypotheses and theorem; it is not an independent verification of Henning–Yeo. The historical Gyárfás–Lehel source is likewise not needed as an unaudited black box below: the only necessary structural facts receive elementary proofs here.

## 2. Strong sums, local distances, and overlapping progressions

A strong-Sidon subset requires distinct sums for **all unordered pairs allowing repetition**. Thus a three-term AP \(a,b,c\) fails because \(a+c=2b\), even when all sums from distinct-element pairs are different. Every computational witness in this audit was tested both by sums including doubled sums and by distinct positive differences.

If an ambient \((4,5)\)-set contained a repeated sum of two different distinct-element pairs, cancellation shows that four different values are involved. In increasing order \(a<b<c<d\), the only equal pairing is \(a+d=b+c\). The six distances then include the two equalities \(b-a=d-c\) and \(c-a=d-b\), and therefore have at most four distinct values. This is forbidden. Consequently the ambient set is weak Sidon. A remaining nontrivial sum collision must involve exactly three values and is an AP. Hence a subset of a \((4,5)\)-set is strong Sidon if and only if it is AP-free.

Two different AP triples cannot share two vertices. If the shared vertices are \(u<v\), their third vertices can only be \(2u-v,(u+v)/2,2v-u\). Selecting two of these produces, up to an affine change, either a four-term AP or one of \(\{-2,0,1,2\}\), \(\{0,1,2,4\}\). The first has three distances; the others have four. All violate \((4,5)\).

This proves the needed linearity without assuming that arbitrary linear hypergraphs are realizable. Conversely, linearity alone was **not** substituted for the local distance condition during enumeration: every admitted ambient set was checked directly on every four-point subset. Direct weak-Sidon and AP-linearity checks also passed on every catalog member.

## 3. Independent verification of the seed and exclusion coverage

All 1,001 seed four-point subsets satisfy \((4,5)\). All 16,384 seed subsets were tested by three predicates: the full strong-sum test, the positive-difference test, and avoidance of the independently regenerated AP triples. They agree. There are 12 AP triples, 143 maximum strong-Sidon subsets, and maximum size eight. In particular, all 2,002 nine-point subsets fail; any larger subset contains one of them.

The independently recovered subset-counting polynomial matched an additional
inclusion–exclusion computation over all 4,096 AP-edge subfamilies. The actual
polynomial and coefficient lists are omitted.

Every supplied seed-vertex exclusion witness was checked to be an eight-point
subset omitting its designated vertex with all 36 unordered pair sums,
including doubles, distinct. Independent enumeration of every maximum subset
confirmed avoidance coverage for all fourteen vertices. The original report's
three maximum subsets were also checked and had empty common intersection.
The numerical witnesses and per-vertex count table are omitted. These results
establish the finite premises P1 and P2 in the separately audited evidence;
the prose edition alone does not independently prove their numerical content.

## 4. Complete enumeration, normalization, and generation order

For a finite real set \(A\), a new point is in an AP with two old points exactly when it belongs to

\[
C(A)=\{(a+b)/2,2a-b,2b-a:a,b\in A,\ a<b\}\setminus A.
\]

This follows by solving the three possible midpoint positions. It is an identity over the reals, not a denominator or search-window assumption. In particular, an AP-linked extension of a rational parent is rational.

For a rational set, subtract its minimum, clear the exact rational denominators, and divide by the gcd of the resulting integers. This is an injective positive affine map on coordinates and preserves all sums, APs, and distance cardinalities. For every affine bijection \(T\), \(C(T(A))=T(C(A))\). Therefore normalizing a parent before generating its children cannot lose an extension. Repeated normalization equals direct normalization of the same positive affine class.

The independent verifier used rational `Fraction` arithmetic and ordered-pair midpoint/reflection generation. It first retained the original seed coordinates through both stages, recording every valid ordered pair of additions. It separately regenerated the second family from normalized integer parent representatives. The resulting families are identical, and both agree exactly with the candidate's coordinate catalogs, with no missing or duplicate member.

| Quantity | Independently verified value |
|---|---:|
| Distinct first-stage AP candidates | 223 |
| Admissible first-stage additions/classes | 50 |
| Ordered second-stage candidate trials | 12,999 |
| Admissible ordered second-stage paths | 2,740 |
| Distinct unordered addition pairs | 1,743 |
| Distinct normalized second-stage classes | 1,743 |
| Second-stage classes with one generation order | 746 |
| Second-stage classes with both orders | 997 |

Generation order is essential: 746 second-stage classes have only one
admissible generation order. The second addition need not belong to the
first-stage candidate set. Restricting both additions to \(C(A_0)\) would
miss valid classes. The audited enumeration imposes no such restriction;
all 2,740 admissible paths were retained before deduplication. The numerical
example pair is omitted.

No seed-automorphism quotient is needed. An increasing affine self-map of a
finite real set with at least two points fixes its extrema and is the identity;
the only possible decreasing one reflects about their midpoint. Regardless
of any seed symmetries, normalization identifies ambient positive affine
classes and a witness transports back under the particular normalization map.
No unrecorded permutation is assumed to be a geometric symmetry. The audit's
finite seed-symmetry check is unnecessary for this argument and is not
reproduced numerically here.

Every one of the 50 and 1,743 supplied witnesses passes exact ambient-membership, distinctness, size, doubled-sum, and difference checks. Every listed ambient set passes the full four-point test, totaling 3,240,510 catalog quadruples per verification run. The audit additionally constructs its **own** witness for every class: it tries the independently enumerated maximum seed subsets together with that class's one or two original-coordinate additions, then transports a successful witness to normalized coordinates. This succeeds for all 1,793 classes.

The catalog equalities and witness outcomes in this section are historical
finite verification results for premise P3. The catalogs and witnesses are
omitted; aggregate counts and hashes are not a stand-alone proof of P3.

## 5. Why the finite checks cover every real extension

This general classification is complete, conditional on the finite seed
maximum, vertex-avoidance and extension-catalog premises P1–P3 stated in
PROOF.md. Those premises were independently verified in separate evidence;
their finite certificates are not present in this edition.

The upper bound is uniform and immediate: a strong-Sidon subset of \(B\) has at most eight old points, since its intersection with the seed is strong Sidon. It has at most \(k\) new points. Therefore \(h(B)\le8+k\).

For one addition \(x\), either it forms an AP with two seed points or it does not. In the first case it lies in the complete first-stage candidate domain and the verified catalog gives a nine-point witness. In the second case it is in no new AP at all, so adding it to any maximum seed subset remains AP-free and hence strong Sidon. No rationality assumption is used in the second case.

For two additions \(x,y\), suppose first that at least one of them lies in an AP with two seed points. Name such a point \(x\), regardless of any previous labeling or generation order. The one-point result supplies a nine-point strong-Sidon subset of \(A_0\cup\{x\}\).

- If \(y\) belongs to no AP of \(B\), adjoining it preserves AP-freeness and supplies ten points.
- Otherwise an AP containing \(y\) has its other two points in \(A_0\cup\{x\}\). Thus \(y\) belongs to the full second-stage candidate set, including APs using \(x\). The complete catalog supplies ten points. Both additions in this branch are forced to be rational in the original seed coordinates.

It remains that **neither** addition forms an AP with two seed points. Every new AP then uses both \(x\) and \(y\) and one old vertex. Linearity permits at most one such AP. If there is none, adjoining both points to any maximum seed subset works. If the unique AP is \(\{a,x,y\}\), choose a maximum seed subset omitting \(a\), whose existence was exhaustively checked above, and adjoin both new points. This also gives ten AP-free, hence strong-Sidon, points.

These alternatives exhaust all real pairs, including irrational pairs related by a new AP. Any other repeated sum would contradict the already assumed ambient \((4,5)\)-property. Overlapping new APs are excluded by the four-distance obstruction, not silently ignored. Combining the lower witnesses with the uniform upper bound proves equality. An arbitrary nonconstant affine image of the seed is handled by applying its inverse affine bijection to the whole extension; this includes negative and irrational scale factors.

## 6. Reliability tests and acceptance boundary

The independently authored standard-library verifier completed in normal, `-O`, and `-OO` modes. Its acceptance checks use explicit exceptions, not removable assertions. The three substantive result files are byte-identical. Fourteen negative controls all reject their intentionally false inputs: weak-versus-strong AP confusion, four invalid quadruple patterns, deletion of a first-stage or second-stage class, duplication of a class, a doubled-sum-colliding witness, an out-of-set witness, a repeated witness coordinate, a damaged regeneration domain, a false nine-point seed witness, and incomplete excluded-vertex coverage.

The audit retains its source code, independently generated catalogs and generation paths, maximum seed-subset catalog, source-inspection material, invocation receipts, and negative-control results separately from this authored report. Integrity manifests distinguish the complete local audit record from the authored reports and public source metadata suitable for a publication review.

There is no mathematical correction required for the audited seed-specific statement. The original universal optimization problem remains unresolved by this work. A 16-point example with maximum strong-Sidon size nine, if found by another route, is not ruled out; only examples containing this exact affine seed are excluded. No claim is made to have independently audited the Henning–Yeo theorem, proved a novel global bound, or performed an exhaustive novelty search.

## Edition and review statement

This AI-assisted work is unrefereed. Acceptance means an independent internal
AI audit of the original report and its separate finite evidence. No external
human peer review, journal acceptance or formal proof-assistant certification
is claimed. No mathematical correction was required. No novelty, priority,
new global bound, classification of all 16-point sets or full solution is
claimed. The original universal optimization problem remains unresolved by
this work. The Henning–Yeo full proof was not independently audited and is
not needed for the seed-specific extension theorem.

Historical source inspection and verification are reported as such. This
edition makes no new scholarly-source retrieval/inspection or mathematical
computation claim. Original sealed candidate and audit records are unchanged.
Copied source documents, source text, images, numerical proof payloads,
executable code and private coordination material are not distributed.
