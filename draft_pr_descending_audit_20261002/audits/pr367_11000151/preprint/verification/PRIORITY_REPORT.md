# PR #367: independent priority audit

Audit date: 2026-10-03 UTC. Verdict: **known constituent results; full exact classification priority unresolved**. This is a literature and scope audit, not the independent mathematical acceptance audit. Candidate files and Git/services were not modified. No individual was contacted.

The candidate's length-30 crossing theorem has a direct prior published statement, stronger because it allows any number of strands. The quotient itself has a classical mapping-class presentation, and the length spectrum follows from prior genus-two geography. No source inspected here proves the entire exact fixed-generator classification with the candidate's strict four-class count. That bounded negative search result does not certify novelty, nor establish that the problem remains open today.

## Exact question and candidate claims

Write $B_6=\langle a_1,\ldots,a_5\rangle$, with the usual Artin relations, and set

\[
c=(a_1a_2a_3a_4)^5,\qquad
h=a_5a_4a_3a_2a_1^2a_2a_3a_4a_5,\qquad
z=(a_1a_2a_3a_4a_5)^6.
\]

The exact group is $G=B_6/\langle\!\langle ch^{-1}\rangle\!\rangle$. Inputs are literal positive words in these five fixed generators, with product $c^2$ in $G$. Factors in a Hurwitz path may become conjugates; the input universe is still fixed-generator positive words. It is not the classification of all quasipositive factorizations in $B_6$, all nonseparating twist factorizations, or all closed genus-two fibrations.

Wajnryb's original question is printed p.126, one-based PDF p.133, in Chapter 8, Section 3. I read printed pp.124–127 fresh before opening candidate narratives; the chronology is sealed in FRESH_SOURCE_SEAL.md. The question proposes lengths 20, 30, 40 and the three models $h^2,z,c^2$. Its neighboring closed-surface paragraph explicitly notes finer equivalence in the boundary setting. [Original primary volume](https://www.math.uchicago.edu/~farb/papers/mcgbook.pdf).

Candidate TURN_1–TURN_4 and FINAL_RESULT assert:

| Claim | Candidate mechanism | Priority assessment |
|---|---|---|
| Lengths are exactly 20, 30, 40 | Credited geometric bound 40; exponent and pure-linking constraints exclude 0,10 | Length spectrum is already a corollary of older broader geography; algebraic extraction may be a useful proof mechanism |
| Linking vectors reduce to doubled star / all ones / doubled five-clique | Normal-closure image in pure braid abelianization and positivity | No exact matching classification lemma located; independent mathematical audit required |
| One strict class at length 20 | 810-word enumeration; exact quotient-compatible representation filter; ten cyclic rotations of $h^2$ | Strongest possible new part located by this audit, conditional on correctness and further priority search |
| One strict class at length 30 | Exhaustive finite crossing graph and faithful Artin action | Direct general prior result credited to Casson in Elrifai–Morton 1994 |
| Two strict classes at length 40 | Endpoint-isolation argument, embedded $B_5$, positive monoid, generated-subgroup invariant | Uses classical mechanisms; the exact fixed-input class count was not located in prior sources |
| Three classes after global conjugation | Simultaneous conjugation merges the two length 40 classes | Convention must be explicitly stated; do not claim a literal three-class strict answer |

## Direct matching length-30 result

E. A. Elrifai and H. R. Morton, *Algorithms for positive braids*, Quart. J. Math. Oxford (2) 45 (1994), 479–497, DOI 10.1093/qmath/45.4.479, **printed p.496**, concluding part of **Section 5**, one-based PDF p.18 of 19, report a result credited to Casson: a positive braid in which every pair of labelled strands crosses exactly twice is the full twist $\Delta^2$. This is an **unnumbered reported assertion**, not a numbered theorem with a proof supplied in that paper. The paragraph describes a different combinatorial approach, and supplies no separate Casson bibliographic item. No checkable original Casson proof was located in this audit. [Published primary scan hosted by Notre Dame](https://nsalter.science.nd.edu/teaching/braidsspring2024/elrifaimorton.pdf); [author manuscript](https://www.liverpool.ac.uk/~su14/papers/elrifaimorton.pdf).

The proof mapping is exact. Candidate length 30 pure-linking coordinates are all 1; because every crossing is positive, each unordered pair has exactly 2 crossings. Apply the reported result with $n=6$ to obtain equality $w=\Delta_6^2=z$ already in $B_6$. Positive braid monoid embedding then gives a sequence of ordinary positive braid relations, which the candidate converts to Hurwitz moves. Thus the candidate's finite computation certifies an instance of an older general result. It may provide valuable reproducible proof evidence where the credited proof is unavailable, but cannot be framed as a new crossing theorem or a novel length 30 classification theorem without addressing this exact prior statement.

## Classical identification of the exact quotient

Makoto Matsumoto's original MPIM1997-74 manuscript, dated 1997-07-28, defines the one-boundary mapping class group with boundary fixed pointwise (p.2). Theorem 1.3 (p.4), using Theorem 1.2, presents it by Artin relations and $c(A_5)=c(A_4)^2$; genus 2 has no lantern relator. Remark 1.1 and the reproducible Garside calculation are on p.5. Published article: Math. Ann.316 (2000),401–418; the publisher's full PDF was subscription-limited. [Original institutional manuscript](https://archive.mpim-bonn.mpg.de/id/eprint/3423/); [published metadata](https://link.springer.com/article/10.1007/s002080050336).

Relabel Matsumoto's $m_1,m_2,m_3,m_4,m_0$ as $a_5,a_4,a_3,a_2,a_1$. His centers become $z,c$. The recursive full-twist identity is $z=ch=hc$. Consequently $c=h$ and $z=c^2$ generate the same normal subgroup, so the exact $G\cong\operatorname{Mod}(\Sigma_{2,1})$ is classical. Independent exact faithful-Artin checks of those identities and the relabelling pass in check_quotient_mapping.py; no candidate code is imported.

This is cross-checked by Shevchishin's original arXiv0707.2085, Theorems 2.11–2.12, manuscript pp.30–31, and Berrick–Gebhardt–Paris arXiv1105.2468, Theorem 2.1, manuscript p.7, which explicitly displays the center-power relation and specifies boundary pointwise fixed. These are presentation results, not classifications of positive factorization orbits. [Shevchishin primary manuscript](https://arxiv.org/pdf/0707.2085); [Berrick–Gebhardt–Paris primary manuscript](https://arxiv.org/pdf/1105.2468).

## Previously known length spectrum and model context

Yoshihisa Sato, *2-Spheres of Square −1 and the Geography of Genus-2 Lefschetz Fibrations*, J. Math. Sci. Univ. Tokyo15 (2008),461–491: Theorem 5.1 and its proof are pp.471–476, Remark 5.1(1) p.476, Table 1 p.477. The table's $s=0$ cases allow $n=30,40$ when $b_2^+>1$, and $n=20$ or 10 when $b_2^+=1$; the remark excludes $(10,0)$. [Official journal PDF](https://www.ms.u-tokyo.ac.jp/journal/pdf/jms150403.pdf).

The application is an inference: the candidate's geometric boundary-twist relation determines a nontrivial genus-two Lefschetz fibration with a (-1)-section; all five standard twists are nonseparating, so $s=0$, and irreducible singular fibers give relative minimality. Hence Sato's broader theorem already restricts its length to 20, 30, 40. This does not require an isomorphism proof for $G$, only the geometric homomorphism and standard fibration construction. Sato's theorem does not assert a Hurwitz classification.

Ivan Smith, *Lefschetz pencils and divisors in moduli space*, Geom. Topol.5 (2001),579–608: Theorem 5.5 printed p.605 and proof pp.605–607 exhibit the three familiar length 20/30/40 monodromy words and identify possible homeomorphism types of total spaces when the reducible-fiber count vanishes. This is not an assertion of exact quotient factorization equivalence. Smith's 2014 erratum, GT18,615–616, withdraws Proposition 5.1, concerning sections, and explicitly says it was unused elsewhere; Theorem 5.5 is not withdrawn. [Smith2001 official PDF](https://msp.org/gt/2001/5-2/gt-v5-n2-p04-p.pdf); [erratum](https://msp.org/gt/2014/18-1/gt-v18-n1-p14-p.pdf).

Baykur–Monden–Van Horn-Morris, *Positive factorizations of mapping classes*, AGT17 (2017),1527–1555: Theorem A p.1529 gives the genus 2 one-boundary maximum nonseparating length 40. Its proof, p.1536 onward, credits Smith2001 Theorem 5.5 for this case. This bounds length but does not classify factorization orbits. Section 4.2, pp.1552–1553, helps distinguish subgroup positivity from positivity in the full mapping class group. [Official PDF](https://msp.org/agt/2017/17-3/agt-v17-n3-p06-s.pdf).

Siebert–Tian, *On the holomorphicity of genus two Lefschetz fibrations*, Ann. Math.161 (2005),959–1020, Theorem A manuscript p.2 and proof p.53, concerns the closed case with transitive monodromy and irreducible singular fibers. A chosen one-boundary lift/section is extra information, and the candidate's length 40 $S_5$ monodromy is not transitive on six strands. Its theorem therefore does not subsume this exact classification. [Original arXiv manuscript](https://arxiv.org/pdf/math/0305343).

González-Meneses, *Basic results on braid groups*, AMBP18 (2011),15–59, §§1.6 and 4, gives faithful Artin action and positive monoid/normal-form machinery (printed pp.22–24 and 41–44). Wajnryb's Theorem 2.1, printed p.123, credits Perron–Vannier for the relevant geometric $A_n,D_n$ embeddings. These are classical ingredients; their application does not itself establish novelty. I did not obtain a full original Perron–Vannier proof in this audit. [González-Meneses official PDF](https://www.numdam.org/article/AMBP_2011__18_1_15_0.pdf).

## Strict versus simultaneous-conjugation equivalence

Auroux's Chapter 9 in the same primary volume, printed p.131, defines adjacent Hurwitz moves and global conjugation separately. Proposition 1.1 identifies Lefschetz-fibration isotopy with both operations. Wajnryb's referral to that chapter is therefore a reason to give both conclusions, not to silently identify the two conventions. The geometric intent of a short problem statement should not be settled solely by terminology. [Primary volume](https://www.math.uchicago.edu/~farb/papers/mcgbook.pdf).

Under strict moves, the subgroup generated by the factors is unchanged. The two length 40 words $(a_1a_2a_3a_4)^{10}$ and $(a_2a_3a_4a_5)^{10}$ have distinct permutation-image subgroups: $S_5$ fixing 6 and $S_5$ fixing 1. Thus they cannot be strictly equivalent. Simultaneous conjugation can merge these subgroups. This elementary obstruction explains the candidate's four-versus-three refinement; it should be stated regardless of any eventual priority conclusion.

## Adversarial priority checks and remaining gaps

| Potential mistaken substitution | Audit outcome |
|---|---|
| A maximum length theorem is the full classification | Rejected: BMVHM supplies 40, Sato supplies the numerical spectrum, neither supplies all orbits |
| Smith's three total-space types are three factorization classes | Rejected: homeomorphism of total spaces is weaker |
| Siebert–Tian closed classification preserves a boundary lift | Rejected: boundary/section data and transitivity restrictions matter |
| $G$ is an unfamiliar new quotient | Rejected: classical Matsumoto presentation matches after $z=ch$ |
| The six-strand twice-per-pair theorem is new | Rejected: stronger general result reported and credited by 1994 |
| A finite verification of a known theorem has no value | Rejected: reproducible certificates can be a contribution, with attribution |
| No exact search hit proves a new solution | Rejected: bounded indexed searches cannot establish absence of prior work |

Outstanding priority gaps are (i) an exact prior classification of fixed positive standard-generator words in this quotient, including both equivalence conventions; (ii) an accessible original/general proof of the Casson crossing assertion; and (iii) the breadth of related algebraic positive-factorization classifications under alternative notation. The audit did not resolve these bibliographic gaps. Mathematical correctness and reproducibility are separately decided by the parent's independent audits.

The strongest supported framing is: a reproducible fixed-generator classification addressing Wajnryb's quotient question, with an explicit strict/global-conjugation distinction, using classical group presentations, geometric length restrictions, and positive braid machinery; an independent finite certificate supplements the Casson result; the potentially new residue is the length 20 reduction/certificate and exact complete orbit classification. Use conditional priority language until that residue is checked against more literature. Do not advertise a new length-spectrum theorem, a new identification of $G$, a new general crossing theorem, or a classification of all genus-two positive factorizations.

This audit is complete as a bounded evidence report. The verdict is not a certified novelty determination. The public file set is sealed by IMMUTABLE_MANIFEST.json; raw sources are privately ignored and receipt-hashed.
