# EP 757: an exact obstruction to extending the known 14-point block

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

## Result and scope

The optimal universal strong-Sidon fraction is **not determined here**. No improvement on the located bounds

\[
9/17\le c_*\le4/7
\]

is claimed. The accepted result is the following exact, computer-assisted obstruction to a natural finite-construction route.

**Accepted theorem (finite certificates omitted).** Let \(A_0\) be the exact
14-point integer set in Jie Ma and Quanyu Tang, *Largest Sidon subsets in weak
Sidon sets*, arXiv:2602.23282v2, Lemma 5.1, printed page 13.
The version-specific [primary PDF](https://arxiv.org/pdf/2602.23282v2) and
[version record](https://arxiv.org/abs/2602.23282v2) identify the seed precisely;
its copied numerical coordinates are not reproduced here.

Write \(h(B)\) for the largest strong-Sidon subset of \(B\). For every finite real \((4,5)\)-set \(B\supseteq A_0\) with \(|B\setminus A_0|\le2\),

\[
h(B)=8+|B\setminus A_0|.
\]

The same assertion holds with any nonconstant affine image of \(A_0\) in place of \(A_0\). In particular, no 16-point \((4,5)\)-set containing such a block can have a largest strong-Sidon subset of size 9. A 16-point example with \(h=9\) would improve the upper bound to \(9/16\), so this theorem rules out that particular extension route completely, including irrational added points.

This is a seed-specific obstruction, not an exclusion of all 16-point examples. Its finite enumeration concerns 50 one-step classes and 1,743 two-step classes defined below. The mathematical reduction extends that enumeration to **all real one- and two-point extensions of the fixed block**. There is no assertion about arbitrary larger extensions, other 14-point seeds, or the exact value of \(c_*\). Novelty of this obstruction has not been established by an exhaustive literature search.

## Definitions and elementary reductions

A strong-Sidon set has distinct sums \(x+y\) indexed by unordered pairs allowing \(x=y\). Equivalently, all positive differences between distinct points are different. The doubled sums are included in every direct verification here.

A \((4,5)\)-set is a finite real set in which every four distinct points give at least five distinct positive distances. Its AP hypergraph has one vertex per point and an edge for each nontrivial three-term arithmetic progression.

We use two elementary facts, both also established in the primary sources.

**Lemma 1.** In a \((4,5)\)-set, strong-Sidon subsets are exactly the AP-free subsets.

**Proof.** A repeated sum from two distinct pairs of distinct elements must use four distinct elements. In their increasing order \(a<b<c<d\), the equality is \(a+d=b+c\). It yields both \(b-a=d-c\) and \(c-a=d-b\), leaving at most four different distances on the four points, a contradiction. Thus the ambient set is weak Sidon. In a nontrivial repeated sum with at most three distinct values, exactly three values occur and their equality is \(a+c=2b\), a three-term AP. Conversely every AP gives this repeated sum and prevents strong Sidonicity. ∎

**Lemma 2.** Distinct AP edges in a \((4,5)\)-set intersect in at most one vertex.

**Proof.** Suppose both contain \(u<v\), and put \(d=v-u>0\). Their third vertices are two distinct choices among \(u-d,(u+v)/2,v+d\). If the choices are \(u-d,v+d\), their union is a four-term AP and has three distances. Otherwise their union has only four distances: after translation and scaling it is \(\{-2,0,1,2\}\) or \(\{0,1,2,4\}\), each of which has positive distances \(1,2,3,4\). Both contradict the hypothesis. ∎

Consequently, if two new vertices are added and neither individually creates an AP with two old vertices, at most one new AP can appear: every new AP must contain both new vertices, and two such edges would violate Lemma 2.

## Separately verified finite premises for the known block

The following are reported finite results from the accepted computational
evidence, not stand-alone prose proofs of their numerical assertions.

**Premise P1 (seed maximum).** The exact cited seed \(A_0\) is a \((4,5)\)-set
and \(h(A_0)=8\). All 1,001 four-point subsets passed the direct distance
test. The independent audit tested all 16,384 subsets by sums including
doubled sums, by distinct positive differences and by AP avoidance, with
identical outcomes. It found 12 AP edges and 143 maximum subsets; all 2,002
nine-point subsets failed the strong-Sidon test. Inclusion–exclusion over
all 4,096 edge subfamilies matched the direct counting result. The numerical
edge list, polynomial, coefficient lists and witnesses are omitted.

**Premise P2 (seed vertex avoidance).** For each \(a\in A_0\), there is a
strong-Sidon eight-point subset of \(A_0\) avoiding \(a\). The independent
audit checked all fourteen supplied avoidance witnesses and independently
enumerated all maximum subsets, confirming that every seed vertex is omitted
by at least one maximum subset. It also checked the original report's
three-witness empty-intersection certificate. Those witness coordinates and
the per-vertex counts are omitted. This premise is not inferred merely from
\(h(A_0)=8\), and its finite proof is not included in this edition.

## Complete finite extension domains

If \(A\) is a finite set and \(x\notin A\) participates in a three-term AP with two elements of \(A\), then necessarily

\[
x\in C(A):=\{(a+b)/2,\ 2a-b,\ 2b-a:a,b\in A,\ a<b\}\setminus A.
\]

This identity is exact over the reals. It does not require an a priori bound on the magnitude or denominator of \(x\).

For a finite rational set \(A\), let \(N(A)\) be its increasing list after translation by \(-\min A\), clearing denominators, and dividing the resulting integers by their positive gcd. It is a positive affine image, so it preserves both the \((4,5)\)-property and strong Sidonicity. If \(A\) already has integral coordinates, the possible values of \(2x\) are the integers

\[
a+b,\quad4a-2b,\quad4b-2a.
\]

Thus the verifier never needs floating-point arithmetic.

For any affine bijection T, C(T(A))=T(C(A)): each candidate is characterized
by an AP, and affine bijections preserve APs in both directions. Therefore
normalizing a parent before generating children loses no extension.
Repeated positive normalization gives the same representative as directly
normalizing the resulting set. A witness transports back under the specific
affine normalization map; no unrecorded seed symmetry is assumed.

Define the following two finite families:

\[
\begin{aligned}
\mathcal F_1&=\{N(A_0\cup\{x\}):x\in C(A_0),\ A_0\cup\{x\}\text{ is a }(4,5)\text{-set}\},\\
\mathcal F_2&=\{N(A\cup\{y\}):A\in\mathcal F_1,\ y\in C(A),\ A\cup\{y\}\text{ is a }(4,5)\text{-set}\}.
\end{aligned}
\]

**Premise P3 (complete finite family verification).** There are exactly 50
distinct members of \(\mathcal F_1\) and exactly 1,743 distinct members of
\(\mathcal F_2\). Every member of \(\mathcal F_1\) contains a strong-Sidon
nine-point subset. Every member of \(\mathcal F_2\) contains a strong-Sidon
ten-point subset.

**Reported verification, with finite certificates omitted.** The independent
audit regenerated both entire families and matched the stored catalogs
exactly, without missing or duplicate members. Every admitted set passed
every four-point distance test; each supplied witness passed exact size,
ambient-membership, doubled-sum and distinct-positive-difference checks.
The auditor independently constructed its own witness for all 1,793 classes.

Generation was checked both in original seed coordinates and through
normalized parent representatives. The two routes agree. There were 223
first-stage candidates, 50 admissible first additions, 12,999 ordered
second-stage candidate trials and 2,740 admissible ordered paths, yielding
1,743 unordered addition pairs and 1,743 normalized second-stage classes.
Of these, 746 classes have one generation order and 997 have both.
Restricting both additions to \(C(A_0)\) would lose valid classes: the second
candidate domain must be that of the augmented parent. All admissible paths
were retained before deduplication. These counts describe verification
coverage; no finite catalogs or witness coordinates are distributed here.
The finite premise P3 therefore cannot be checked from this prose alone.

For clarity, the first family count is not a search over a chosen interval, and the second family count is not a cutoff or random sample. They are the entire two expressly defined families. The classification below is what makes them sufficient for arbitrary real extensions of size at most two.

## Complete all-real reduction from finite premises P1–P3

The following proof is conditional only on the precisely stated finite
premises P1–P3 above. It is a complete classification of all real additions.
Their separate computational verification is reported here; their omitted
finite certificates remain necessary to independently reproduce the theorem.

First consider \(B=A_0\cup\{x\}\). If \(x\) belongs to no AP in \(B\), then an eight-point strong-Sidon subset of \(A_0\), together with \(x\), is AP-free. Lemma 1 makes it strong Sidon. If \(x\) belongs to an AP in \(B\), its other two points lie in \(A_0\), so \(x\in C(A_0)\). Premise P3 supplies the required nine-point subset after affine normalization, hence before normalization. In either case \(h(B)\ge9\). On the other hand every strong-Sidon subset contains at most eight old points and at most one new point, so \(h(B)\le9\). This proves the one-point assertion.

Now let \(B=A_0\cup\{x,y\}\), with two distinct new real points.

**Case 1: at least one new point creates an AP with two old points.** Call that point \(x\). The preceding argument gives \(h(A_0\cup\{x\})=9\). If \(y\) is in no AP in \(B\), add it to a maximum nine-point subset to obtain a strong-Sidon ten-point subset. Otherwise \(y\) forms an AP with two points of \(A_0\cup\{x\}\). The candidate identity puts the normalized \(B\) in \(\mathcal F_2\). Premise P3 again supplies a ten-point strong-Sidon subset. This reasoning is unaffected by the intermediate positive affine normalization, which bijectively maps candidate AP extensions and preserves their validity.

**Case 2: neither new point creates an AP with two old points.** Every new AP in \(B\) contains both \(x\) and \(y\), hence by Lemma 2 there is at most one. If there is none, add both new points to any maximum eight-point subset of \(A_0\). If the unique new AP is \(\{a,x,y\}\), use Premise P2 to choose a strong-Sidon eight-point subset avoiding \(a\), then add \(x,y\). In either subcase the resulting ten-point set is AP-free and hence strong Sidon by Lemma 1.

Thus \(h(B)\ge10\). Every strong-Sidon subset of \(B\) has at most eight old points and at most two new points, so \(h(B)\le10\). The zero-point assertion is the verified baseline. Invariance under nonconstant affine maps proves the final formulation. ∎

## Why this direction was tested, and the remaining gap

Ma–Tang’s lower-bound calculation in fact gives the finite consequence

\[
h(A)\ge\left\lceil\frac{9|A|+6}{17}\right\rceil\qquad(|A|\ge2),
\]

by retaining the \(-2\) in their AP edge bound before applying the cited Henning–Yeo inequality. This is a direct consequence of their proof, not a new asymptotic bound. It excludes a 15-point improvement on \(4/7\), while permitting a 16-point example with \(h=9\). Extending their explicit block by two points was therefore a concrete first finite direction. The theorem above proves that direction cannot work.

The general residual remains: improve the universal lower bound using properties of AP hypergraphs beyond the cited estimate, or construct another \((4,5)\)-set with a smaller ratio. The verification here supplies no exhaustive classification of all 16-point AP hypergraphs or all 16-point real sets. It also does not rule out changing or deleting points of \(A_0\), or adding three or more points.

The universal upper bound \(c_*\le4/7\) follows directly from the one verified finite example and the definition of a universal constant. Ma–Tang’s subadditivity theorem additionally establishes the asymptotic-limit characterization, but is not needed for this direct upper-bound inference.

## Primary-source reading and dependence

1. J. Ma and Q. Tang, *Largest Sidon Subsets in Weak Sidon Sets*, arXiv:2602.23282v2, 6 March 2026, 15 pages: https://arxiv.org/pdf/2602.23282. The retained complete proof text was read, including the elementary reductions, affine gluing/subadditivity, the separate weak-Sidon result, and both strong-Sidon bounds. The construction in Lemma 5.1 was independently reverified here; no author-supplied code was downloaded or executed. The weak-Sidon exact theorem is a different statement and does not resolve EP 757.
2. A. Gyárfás and J. Lehel, *Linear Sets with Five Distinct Differences among Any Four Elements*, J. Combin. Theory Ser. B 64 (1995), 108–118: https://www.renyi.hu/~gyarfas/Cikkek/69_linset5.pdf. All eleven scanned pages were read using locally generated OCR; printed pages 112–113 were also visually inspected to resolve the full forbidden-configuration proof. OCR is retained separately and is not represented as source-authored text.
3. M. A. Henning and A. Yeo, *Affine Planes and Transversals in 3-Uniform Linear Hypergraphs*, Graphs and Combinatorics 37 (2021), 867–890, https://doi.org/10.1007/s00373-021-02285-x. The theorem used by Ma–Tang was cross-checked against the authors’ university publication record: https://pure.uj.ac.za/en/publications/affine-planes-and-transversals-in-3-uniform-linear-hypergraphs/. Its full 24-page proof was **not independently audited here**. Accordingly the \(9/17\) lower bound and its finite sharpening are treated as the located literature result with this external dependency. The extension obstruction itself does not depend on that theorem.

## Historical verification and present reproduction limit

The original certificate generator and independent mathematical verifier were
separately authored exact-arithmetic standard-library Python programs.
The independent audit did not inspect candidate programs as source, import
them or execute them. Its normal, -O and -OO substantive result files were
byte-identical; fourteen deliberately invalid inputs were rejected in each
mode. Explicit exceptions preserved checks under optimization. These are
historical verification results, not new runs made to prepare this edition.

This edition preserves the complete general reduction and the exact accepted
seed-specific statement. It omits the finite certificates needed to reproduce
P1–P3 and therefore the seed-specific computational theorem. The result
remains a verified seed-specific extension obstruction, with no claimed
global bound improvement or solution of the original problem.

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
