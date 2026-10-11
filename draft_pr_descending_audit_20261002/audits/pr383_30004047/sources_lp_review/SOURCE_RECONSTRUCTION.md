# Primary-source reconstruction, frozen before candidate reading

Reconstructed at 2026-10-03T02:23:07Z, before opening the candidate Turn files or old/root review conclusions. This is a bounded source check, not a claim of exhaustive literature coverage or novelty.

## Original contribution

The original is Paul Seymour, joint with Maria Chudnovsky, Alex Scott and Sophie Spirkl, “Concatenating bipartite graphs,” Oberwolfach Report 1/2019, printed pp. 46–47, physical PDF pages 42–43, DOI 10.4171/OWR/2019/1. Official EMS PDF: https://ems.press/content/serial-article-files/46780 . OWR16763 is an archive label, not the DOI.

For real x,y in (0,1], finite graphs with disjoint nonempty A,B,C satisfy only the degree conditions d_B(a)>=x|B| for every a and d_C(b)>=y|C| for every b. The target quantity counts distinct A vertices joined to c by two-edge paths, rather than the number of paths. The guaranteed universal maximum is equivalently

    phi(x,y) = inf_G max_{c in C} |{a: exists b, ab and bc edges}|/|A|.

Extra internal or A–C edges can be removed in this path formulation; the published formulation below makes that normalization explicit. The OWR questions are the diagonal assertion x>1/3 => phi(x,x)>=1/2 and, for every integer k>=1,

    x+ky>1 and kx+y>=1 => phi(x,y)>=1/k.

The strict first inequality and weak second inequality must remain distinct. On the diagonal, k=2 gives the stated x>1/3 question. k=1 is already elementary. The original also introduces psi by adding the reverse degree requirements d_A(b)>=x|A| and d_B(c)>=y|B|. It reports the same integer-k implication as proved for psi, and asks whether psi is symmetric. It reports phi symmetry and a weaker diagonal bound, not a solution to the question.

## Published authority

Chudnovsky, Hompe, Scott, Seymour and Spirkl, “Concatenating Bipartite Graphs,” Electronic Journal of Combinatorics 29(2) (2022), P2.47, published June 3, 2022, DOI 10.37236/8451. Primary publisher PDF: https://www.combinatorics.org/ojs/index.php/eljc/article/download/v29i2p47/pdf/ ; publisher metadata: https://www.combinatorics.org/ojs/index.php/eljc/article/view/v29i2p47 . Local downloaded PDF and text are retained under primary_sources.

Published constrained graphs have a tripartition into nonempty stable A,B,C, no A–C edges, and the same two forward degree conditions. Thus reach means distance exactly two to A, which coincides with two-edge path reach in the normalized graph. The universal optimum exists (1.7); phi>=max(x,y) is 1.8. The four-condition biconstrained problem defines psi, with phi<=psi (1.11). Weighted/ordinary graph equivalence and rational blowup are already in 2.1; finite linear-programming duality and complementary slackness are already in 2.2, leading to phi symmetry in 2.3.

The published 4.2 proves the full integer-k implication for psi. Published 4.1 is a different, stronger parameter region, requiring x+ky>1 and kx+x/(1-(k-1)y)>=1, when the nontrivial case x,y<1/k ensures a positive denominator. Replacing psi with phi in 4.1 is false: the paper's Figure 3 gives phi(3/10,4/11)<=4/9. This does not refute 5.1 since 2(3/10)+4/11=53/55<1. Published Conjecture 5.1 is exactly the OWR integer-k phi question. It explicitly leaves x,y>1/3 => phi(x,y)>=1/2 open, and hence leaves the diagonal question open.

The cited elementary endpoint is 5.2: x+y>1 => phi=1, and additionally x+y=1 with x irrational => phi=1; rational equality x+y=1 permits phi<1. The published diagonal partial evidence includes phi(x,x)>3/7 for x>1/3 (from 5.3), a discontinuity bound (2k-3)/(2k^2-4k+1) for x>1/k, k>=2 (5.4), and the threshold result 2x^2 y>=(1-x-y)^2 => phi(x,y)>=1/2 (6.6). The latter yields the reported diagonal threshold approximately 0.352202. These hypotheses cannot be silently replaced by x>1/3.

## Bounded current check

Primary arXiv page https://arxiv.org/abs/1902.10878 presently records joint-author v3 dated December 7, 2020. The separate Hompe page https://arxiv.org/abs/1908.07453 records withdrawal on June 23, 2022 and states that its results were edited and incorporated into 1902.10878. It is not an independently active follow-up, nor evidence of a flaw in the published joint article. Primary author bibliographies (Seymour's online papers and Spirkl's research page) list the 2022 joint publication. Bounded searches for the title and Conjecture 5.1 did not expose a later primary resolution. That observation does not establish an exhaustive search, prove current open status, or establish novelty of any restricted family.

## Audit success criterion and gap

Success for this audit means verifying the frozen candidate's source contract and all claimed Turn 1–2 restricted-family deductions; computations are controls. Success for the original research question requires a universal proof under only the two forward degree conditions, or an actual finite counterexample meeting the strict/weak integer-k region. Restricted-template obstructions, failed cover proposals, bounded searches, and numerical LP results alone cannot meet that criterion. Original discovery completion remains 0% from this source reconstruction alone; source audit checkpoint is 25%.
