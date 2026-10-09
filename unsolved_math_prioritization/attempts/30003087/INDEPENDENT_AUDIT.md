# Independent mathematical audit: Harbourne banded partial

Target: 30003087 / OWR-14222-015. Audit date: 2026-10-09.

## Decision

**Accept as a partial theorem relative to the cited published finite-linear-space theorems. Do not accept as a resolution of the general conjecture.** No mathematical defect was found in the stated q>=4 result. The required nonmathematical wording correction was verified before preparing this edition; its input and output identities are recorded in [PROVENANCE.md](PROVENANCE.md).

The precise accepted statement is this. Let q>=4 be a prime power, N=q^2+q+1 and d=N-i. The absolute minimum over all fields and all configurations of d distinct projective lines, with every singular point included, equals the displayed source target when:

- 0<=i<=q;
- i=2q-1;
- i=q+1+a, 0<=a<=q-3, and floor[a(a-1)/(2(q-1))] is strictly less than q-a for even q, or strictly less than ceil[(q-a)(q+1)/(q-1)] for odd q.

The weaker strict polynomial tests in the report are valid. Complete prime-power bands q=4,5,7,8,9,11,13 follow; q=4,5 and all d<=31 values already appear in the credited DHS source. Small q=2,3 values remain credited known results. **The literal q=2 endpoint formula is false and is not accepted.** No assertion here determines the gaps between prime-power bands, proves worldwide novelty, proves all the imported EMSS theorems independently, or asserts existence of a residual counterexample.

Within the stated bands and this proof method, the first residual is q=16,a=13,i=30,d=243. Its degree-excess bounds allow only delta in {3,4,5}; d=244 allows only delta=4. These are necessary bounds, not existence or realizability results. The q=16 endpoint d=242 is proved. In particular, this does not assert that every d below 243 is settled: d=32,...,43, for example, lies outside the bands.

## Sources inspected and exact locations

1. [OWR 14/2016](https://ems.press/content/serial-article-files/46618), Szpond contribution: printed pp.695-697; Definition 1 on pp.695-696, Conjecture 1 on p.696, known-value table on p.697. The p.696 display was inspected visually. Inspected public PDF: 479,779 bytes; SHA-256 `1ebdfcab0ae22c16adfc3e8b12c13477cec1a6ae57cbe34469f1c16ccbda3fcf`.
2. [Dumnicki-Harrer-Szpond, arXiv:1507.04080v2](https://arxiv.org/abs/1507.04080v2): Definition 1.1 and Conjecture 1.2 on pp.2-3; Theorems 1.4 and 1.6 on p.3; pair-count/objective identity on p.4; Proposition 5.1 and its constructions on p.9. Pages 2,3,9 were inspected visually. Inspected public PDF: 162,237 bytes; SHA-256 `171fbcdbf266753e217476c5731109216318aa2c55be8d1a901d13e5fcff112e`. The [publisher record](https://www.sciencedirect.com/science/article/pii/S1071579718300273) and arXiv record both identify Finite Fields and Their Applications 51 (2018), 371-387, DOI 10.1016/j.ffa.2018.03.001. The title-page generated date does not change the PDF's explicit v2 identifier.
3. [Erdos-Mullin-Sos-Stinson, Finite linear spaces and projective planes](https://users.renyi.hu/~p_erdos/1983-05.pdf), Discrete Mathematics 47 (1983), 49-62: definitions on pp.49-51; Theorem 3.6 on p.53; Lemmas 3.7-3.8 on pp.54-55; q=3 exception, Lemma 3.9, on pp.55-56; Lemma 3.11 on p.56; Corollary 3.12 and Lemma 3.14 on p.57; Lemmas 3.15-3.17 on pp.58-59; Lemmas 3.20-3.21 on pp.60-61; Lemma 3.22 and Theorem 3.23 on p.61. These relevant displays were read directly; pp.50-51,53-61 were also checked visually. Inspected public PDF: 1,725,402 bytes; SHA-256 `53f080d78d1bc027c060bd9ae95d726ad30323e58b32a351dd392be364178507`. The [publisher record](https://www.sciencedirect.com/science/article/pii/0012365X83900717) confirms the title, authors, volume, pages and DOI.

[PROVENANCE.md](PROVENANCE.md) distinguishes the original audited report, the required wording-corrected report and this edited proof-plus-audit edition. The mathematical arguments, hypotheses, inequalities and residual scope are unchanged. [MANIFEST.json](MANIFEST.json) binds the edition files; [SOURCE_MANIFEST.json](SOURCE_MANIFEST.json) records the inspected public PDFs. PDF hashes identify the inspected bytes, not proof correctness. No copied source document is part of this edition.

## Scope, duality and imported hypotheses

The report uses the source objective correctly: H=(d^2-sum m_P^2)/s=(d-I)/s, where I=sum m_P and s counts exactly the points of multiplicity at least two. The pair identity is sum m_P(m_P-1)=d(d-1).

The dual incidence structure has one point for each original line and one block for each singular point. Distinct projective lines over any field meet in a unique point; hence every dual pair lies in exactly one block. All blocks have at least two points. A block equal to the whole point set occurs exactly for a pencil. Removing that case leaves proper blocks. Removing near-pencils then leaves precisely an EMSS nondegenerate finite linear space; no characteristic or field-size hypothesis is introduced.

A pencil has H=0. A near-pencil has s=d, I=3(d-1), H=-2+3/d. Every asserted target for q>=4 is less than -2. These exceptions therefore cannot invalidate any lower bound.

The theorem domains match every use:

- For i<=q-1, d>=q^2+2 and d<=N, so Theorem 3.6 applies and gives s>=N. Its equality embedding is into a plane of order q; the order is explicit in the supporting Lemma 2.2. The scan says v>=q^2 in that lemma, not v=q^2 as some extracted text suggests.
- At i=q, d=q^2+1. Lemmas 3.11 and 3.14 and Corollary 3.12 give s>=N-1 and, at equality, maximum block size q+1, exactly one degree-q point, all other degrees q+1.
- In the middle, d=q^2-a>=q^2-q+3. Lemma 3.11 gives s>=N-1 and maximum block size q or q+1 at equality. Corollary 3.12 supplies the degree distribution in the second case. Thus its Harbourne quotient is greater than the target by exactly 1/(N-1).
- At i=2q-1, Lemma 3.7 gives s>=N-2. Lemma 3.8 embeds an equality case for q>=4. Its q>=4 hypothesis is essential to the quoted theorem and is preserved. The report does not silently apply it at q=3.
- Theorem 3.23's strict polynomial conditions are correctly assigned to parity. The report only uses it inside 0<=a<=q-3, safely within the preceding degree-excess lemmas' domain.

The source's embedding convention is induced restriction. Intersections of size zero or one are discarded when passing from designs to finite linear spaces. Dualizing the containing abstract projective plane therefore gives exactly the deletion incidence counts used in Section 4. The containing plane need not be a field plane. Only its axioms enter the lower bound; field-plane arrangements independently provide actual attainment.

## Independent reconstruction of the critical degree-excess step

This checks the main potential hidden-hypothesis issue. Suppose v=q^2-a, 0<=a<=q-3, b=q^2+q and maximum block size q. Every point has degree r_x>=ceil[(v-1)/(q-1)]=q+1. Put beta_x=r_x-q and delta=sum(beta_x-1)>=0.

For any block l of size q, every point on l has degree exactly q+1. Indeed, a larger degree would leave at most q-2 blocks disjoint from l. Each point outside l lies on at least one such block: the q connections to l use only q of its at least q+1 incident blocks. But there are v-q>=q^2-2q+3 outside points, while q-2 blocks of size at most q cover at most q^2-2q points. This is impossible.

It follows that a q-block has exactly q-1 disjoint blocks. Two intersecting q-blocks together meet all blocks: counting the common-point lines, cross-connections, and the remaining lines through each noncommon point gives q+1+(q-1)^2+2(q-1)=q^2+q. For two disjoint q-blocks l1,l2, a point of l2 has q distinct connecting lines to l1 and degree q+1; its only remaining line is l2. Hence the sets consisting of a q-block and all its disjoint blocks are either identical or disjoint. Each such class has q blocks.

A point x lies in exactly beta_x blocks of every class. If x belongs to the distinguished q-block, both counts are one. Otherwise its q connections to that block leave r_x-q=beta_x disjoint blocks. No regularity assumption has been made about x outside the q-blocks.

Let c be the number of these classes and W the remaining blocks. Then |W|=q^2+q-cq, each W block has size at most q-1, each class has total incidence v+delta, and the complete space has incidence (q+1)v+delta. Therefore

(q+1)v+delta-c(v+delta) <= (q-1)(q^2+q-cq),

which rearranges to

c >= 1+q(q-a)/(q-a+delta).

If delta>0, some beta_x>=2. Counting its incident blocks over the disjoint classes gives c*beta_x<=q+beta_x, hence

c<=1+floor(q/beta_x)<=1+floor(q/2).

Consequently delta>=q-a when q is even, and delta>=(q-a)(q+1)/(q-1) when q is odd. Combining these with the independent consecutive-integer incidence bound gives delta<=a(a-1)/(2(q-1)). The integer rounding is legitimate because delta is a nonnegative integer. For q=13,a=10, this demands delta>=4 and delta<=3 if delta>0; therefore delta=0.

This reconstruction confirms that Lemmas 3.16-3.17 apply to every maximum-q minimal NLS in the specified range. No prior embedding, non-embedding, field realization, or global regularity assumption is needed. Realizability is relevant only when translating a possible positive-delta obstruction back into a counterexample to the geometric problem.

The scan genuinely reverses the parity labels in Lemma 3.20's display. Its proof, Lemma 3.22 and Theorem 3.23 have the parity above. The audit uses the inequalities themselves and does not infer the correct parity from a numerical experiment.

## Inequalities, equality and attainment

The consecutive-integer inequality is valid for every integer multiplicity. Summing it gives the report's bound on I and hence G_k(d,s). Its derivative in s is positive whenever d>2k+1, true for every q>=4 use. The four nonminimal-case comparisons and the endpoint values of both concave quadratics were independently rederived symbolically. Their denominators and stated endpoint numerators are positive. Thus an arrangement with a nonminimal singular count has strictly larger H throughout the asserted ranges, including the whole middle band without the integer restriction.

For deletions from any order-q plane, s=N-u0-u1 and I=d(q+1)-u1 are exact. Two deficient points require at least 2q-1 deleted lines; three require at least 3q-3, which exceeds 2q-1 for q>=3. The allowed deficiency pairs and every quotient comparison in Section 4 follow. At the special endpoint the comparison between (u0,u1)=(0,2) and (1,0) has numerator difference governed by qd-2(N-1)=q^2(q-3). This ties for q=3 and favors (0,2) for q>=4.

The constructions use actual lines of P^2(F_q). Removing a pencil and, in the middle, any permitted additional lines does not create extra deficient points because the deletion count is below 2q-1. The special endpoint removes the common line and q-1 additional lines from each of two pencils, leaving exactly two multiplicity-one points. It attains the target for q>=3. An abstract embedding is never used as an assertion of field realizability.

For the residual middle cases the exact objective is H=-d/(q+1)-delta/[q(q+1)]. The positive-delta condition is therefore both necessary and sufficient for a realizable minimal maximum-q NLS to violate this target. A formal incidence solution or an abstract nonrealizable NLS alone is not a geometric counterexample.

The separate one-line-deficit proof also checks: the de Bruijn-Erdos equality alternatives are handled, q^2+q is not the point count of a projective plane, and G_q(q^2+q,N) equals the target. Equality in this elementary route forces s=N and multiplicities in {q,q+1}; it does not by itself classify every realization as a field-plane deletion.

## Small-order exception

For q=2,i=3,d=4 the printed special expression is -6/5. In the source's particular two-pencil construction there is one triple point, three double points and one point of multiplicity one. Removing the nonsingular point from the denominator gives H=-5/4 for that construction. A different four-line Fano deletion, obtained by removing a whole pencil, has six double points and H=-4/3. The latter is the known absolute minimum in DHS Table 1. Thus simply removing the bad multiplicity-one count does not repair the claimed endpoint construction to an optimal one at q=2.

The report properly excludes that literal endpoint formula, credits the established small value, and does not claim a new counterexample. At q=3, the EMSS equality embedding has an exceptional abstract NLS in Lemma 3.9; the main q>=4 argument avoids it and the small all-fields values are already in DHS.

## Acceptance boundaries

The all-q proof consists of the displayed mathematical arguments relative to the expressly cited published inputs. The imported completion theorems remain credited mathematical inputs. The audit does not certify the full historical EMSS paper or undertake a literature-wide novelty search. It does not establish that a residual positive-degree-excess configuration exists or is realizable.

This edition retains the complete independent mathematical review, source locations and limitations. Computational materials and their output records are outside this edition. The original audit and source evidence remain unchanged; [PROVENANCE.md](PROVENANCE.md) records the editorial boundary. Independent audit does not mean human peer review or proof-assistant certification.
