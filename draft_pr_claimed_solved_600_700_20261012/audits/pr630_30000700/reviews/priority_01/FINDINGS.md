# Adversarial priority audit: PR 630 / problem 30000700

## Verdict and recommendation

**The mathematical result remains correct. The central yes/no answer does not clear a new-discovery priority gate: it follows immediately from an explicit published 2009 counterexample after a parameter rename and one differentiation.** This is a short prior-example implication, not evidence that the 2009 authors explicitly answered the 2007 Oberwolfach question. The all-order monomial formula was already printed in 2004. The squared-exponential mechanism was explicitly classified in 2009 and restated in 2026.

The exact necessity statement in the packet's polynomial classification and the derivative-order tuning of the squared exponential were not located verbatim or as directly matching prior theorems. Their first priority remains unestablished. They are reasonable candidates for modest additional calculations in a concise, attributed boundary note. The evidence does **not** support promoting the package as a newly solved historical research problem or certifying first priority. A useful catalogue correction or explanatory note is a defensible salvage; whether its remaining incremental observations meet a particular publication standard is a judgment this audit cannot turn into a theorem.

Counts: zero verified prior publications explicitly naming and resolving this exact 2007 question; one decisive short prior-example implication to its universal negative answer; one earlier exact monomial formula covering every order; one established squared-exponential mechanism requiring a new parameter calculation for this target; one exact classification statement with no matching prior resolution located; two material full-text gaps in the requested core sources. There are no mathematical corrections to the accepted proof in this review. Three attribution/framing actions are required before a claim of new mathematical contribution can be assessed; they are listed below.

## Bound claim and audit standard

All 28 native files match the sizes and SHA-256 values in `SCOPE_AND_SNAPSHOT.json` at head `810cd5c148bbae7c7c5a47423c375ada98e903b6`. `PINNED_INPUTS.json` also binds the accepted math and scope findings, source leads, and scaling corollary. This audit did not change those inputs.

The exact claim tested for priority is this. For a nonconstant entire function, k>=2 and b!=0, replace CM sharing of a between f and f' by equality of their a-point sets, while retaining the one-way condition f'=b implies f^(k)=b. The printed universal exponential conclusion then fails when a=0. The packet supplies all-order polynomial examples, their complete classification among polynomials, and transcendental examples for k>=3. The root's routine amplitude scaling allows arbitrary prescribed nonzero b in the last family.

This is the literal question following Theorem H on printed p.503 of [OWR 9/2007](https://ems.press/content/serial-article-files/46093?nt=1). The relevant complete contribution and the p.503 image were checked against the accepted scope review. No nonzero-a, scalar CM sharing at b, classification of all entire functions, or historical-intention claim is being tested. The search had to supply either the same statement, an actual counterexample meeting the target hypotheses, or a checkable short implication. Similar titles, unrelated uses of the word "Fang", and generic exponential-polynomial resemblance were insufficient.

## P1: a decisive prior-example implication for the universal negative answer

The publisher copy of Lü, Xu and Yi, [*Uniqueness theorems and normal families of entire functions and their derivatives*, Ann. Polon. Math. 95 (2009), 67–75](https://www.impan.pl/shop/en/publication/transaction/download/product/84815), printed p.68, Example 1, explicitly uses

    q_B(z) = (B/4) z^2

as a zero-IM-sharing counterexample in a related reverse-implication theorem. Its own second condition is q'_B=B implies q_B=B, not the target higher-derivative condition. The distinction matters; it does not prevent using the already published function in a different statement. The PDF's example and symbols were visually checked on p.68; its hash is `7a5c5d254a756742a1ade67b5b10ad925a7e0f2eec1384b69bea6d0585a6c45d`.

Here is the complete authored map, with no appeal to an unproved uniqueness theorem. Given the target b!=0, set the source parameter B=2b. Then

    q_B(z)=b z^2/2,     q'_B(z)=bz,     q''_B(z)=b.

The zero sets of q_B and q'_B are both {0}; their orders are two and one. Thus a=0 is shared IM and not CM. The target b-fiber of q'_B is {1}, so the target implication is nonvacuous and holds because q''_B is identically b. The proposed exponential conclusion at a=0 is zero-free, whereas q_B(0)=0. This is a target counterexample at k=2 for every prescribed b!=0, and also satisfies b!=a if that catalogue restriction is added.

Since one admissible k disproves the universal statement, this prior explicit function is already sufficient for the central negative answer. No argument by family resemblance or search absence is involved. The extra derivative identity is elementary, but the priority challenge rests on the positive existence of this published example, not on an objection that elementary mathematics cannot be new.

**Classification:** short prior-example corollary / known explicit counterexample with an additional immediate application. **Not established:** that the 2009 paper intended this application, cited the Oberwolfach question, or received credit for resolving it. The 2022 Sauer–Schweizer preprint and Schweizer's 2013 paper attribute the quadratic to Li–Yi (2006); the 2006 full text was not obtained, so this review's securely inspected publication date for the example is 2009, without claiming it originated then.

## P2: the all-order monomial formula predates the question

Chang, Fang and Zalcman, [*Normal families of holomorphic functions*, Illinois J. Math. 48 (2004), 319–337](https://doi.org/10.1215/ijm/1258136186), Lemma 5 on pp.323–324, explicitly lists the formula

    g(z) = B(z-z0)^k/k!

for k!=2, and the quadratic B(z-z0)^2/2 as one alternative at k=2. The source parameter B is a nonzero derivative value; it is not the target shared a. The inspected original-PDF text comes from [Zalcman's public author upload](https://www.researchgate.net/profile/Lawrence-Zalcman/publication/258233263_Normal_families_of_holomorphic_functions/links/555b0fb008ae6fd2d828632a/Normal-families-of-holomorphic-functions.pdf). The publisher confirms the paper's identity through its DOI; the upload identifies Spring 2004 and was uploaded in 2015. Direct byte downloads were blocked. A hashed web-cache text excerpt, clearly distinguished from PDF bytes, is preserved in ignored temporary storage. No publisher-PDF byte hash or successful local visual inspection is invented for this source.

The target application is fully checkable independently of the lemma's hypotheses: choose B=b, differentiate to obtain f'=b(z-z0)^(k-1)/(k-1)! and f^(k)=b, and compare zero sets. The derivative attains b at the k-1 distinct roots of (z-z0)^(k-1)=(k-1)!. The shared zero rules out a nonzero exponential. Thus the packet's entire polynomial counterfamily has exactly an earlier printed formula, with the target application requiring only direct differentiation.

**Classification:** exact prior construction/formula and immediate new-context verification, not a verified prior statement of the Oberwolfach answer. The 2004 lemma has additional hypotheses involving order, multiplicities, and values of g^(k) and g^(k+1). Those are not the packet's assumptions. In particular, invoking its necessity conclusion as if it classified every target polynomial would be invalid.

The packet's complete polynomial classification retains a separate logical step: IM sharing first forces a=0 and f=A(z-z0)^n; the target b-condition then forces n=k and A=b/k!. The nonzero-a degree obstruction is also explicit in Sauer–Schweizer's [2022 preprint](https://arxiv.org/abs/2208.11341), Lemma 3.2, for a related weaker forward sharing condition.

The zero-sharing monomial characterization itself is classical. Novikov and Yakovenko, [*Redundant Picard–Fuchs System for Abelian Integrals*, J. Differential Equations 177 (2001), 267–306](https://www.wisdom.weizmann.ac.il/~yakov/redundant.pdf), Proposition 7 on p.300, prove that a complex polynomial whose only critical value is zero is a translated monomial, attributing the fact to Chademan (1996). This complete proposition and proof were read in the author's copy of the published paper and p.300 was inspected visually. For a target polynomial of degree at least two, zero-IM sharing implies that every root of f' maps under f to zero; the critical set is nonempty, so its only critical value is exactly zero. Proposition 7 therefore yields f=A(z-z0)^n. Conversely these monomials share their zero sets with their first derivatives for n>=2. This is an exact prior theorem for the structural part, not just analogy. The 1996 paper was not inspected; no first-origin claim is made for the 2001 statement.

The final degree/divisibility argument under the target b-condition was not found as a prior theorem: f'-b has n-1 distinct roots, while for 2<=k<=n the polynomial f^(k)-b has degree at most n-2. Its vanishing at those n-1 roots forces it to be identically zero, whence n=k and A=b/k!; k>n is impossible. The complete classification is thus a short combination of an established structural fact and a target-specific degree comparison. This narrows the possible incremental content further, without claiming the exact combined statement has a verified earlier publication.

## P3: a known squared-exponential mechanism, with a target-specific calculation

Lü–Xu–Yi (2009), Example 3 on p.68 and Theorem 1.2(d)/Corollary 1.1 on p.69, explicitly exhibit and classify the exceptional form

    h(x)=C((A/2)exp(x/4)+1)^2.

Their conditions involve implications from values of h to values of h'; they do not assert the target f'=b implies f^(k)=b. Sauer–Schweizer, [Results Math. 81, article 66 (published 12 March 2026)](https://link.springer.com/article/10.1007/s00025-026-02624-5), Theorem B on p.3, expressly restate the 2009 result. The fresh 13-page publisher PDF was retrieved and p.3 inspected visually. This establishes a known mechanism, rather than an exact prior resolution by the 2026 paper.

The following authored map identifies exactly what must still be computed. Set A=-2 in the known formula and replace x by 4lambda(z-z0). Write F=C(t-1)^2, t=exp(lambda(z-z0)). Argument dilation changes derivative values; the old h=b implies h'=b condition cannot simply be carried over. Instead calculate anew:

    F'=2C lambda t(t-1),
    F^(k)=C lambda^k(2^k t^2-2t).

The zero fibers of F and F' agree at t=1. Choose the target b=-C lambda/2. Then

    F'-b=2C lambda(t-1/2)^2.

The target b-fiber is exactly t=1/2. At that fiber the target equality is equivalent to

    C lambda^k(2^(k-2)-1) = -C lambda/2,
    lambda^(k-1) = -1/(2^(k-1)-2).

This has nonzero solutions precisely for the stated k>=3 range of this construction. For a prescribed b, choose C=-2b/lambda. These are exactly the packet's examples and root scaling, with the known amplitude/phase freedoms made explicit. The infinitely many zeros give transcendence and defeat the proposed zero-free conclusion. For k=2 the left factor 2^(k-2)-1 is zero and cannot equal a nonzero target b.

**Classification:** established construction mechanism plus a short target-specific order calculation. The parameter equation, the claim for every k>=3, and its application to the exact Theorem H question were not located in the inspected earlier statements. They cannot be declared historically new on that basis. Conversely, the 2009 theorem or the 2026 restatement cannot be cited as if it already contained that equation or a general entire-function classification for this target. The correct novelty description is at most an explicit application and tuning of a known exceptional family.

## Requested original sources and recent extensions

The original Fang–Zalcman [JMAA 280 (2003), 273–283](https://doi.org/10.1016/S0022-247X(03)00041-6) remains a material gap. DOI/PII and publisher/Crossref metadata are verified; direct full-text routes were blocked and the linkinghub page contained a redirect, not article text. The accepted scope review already tested Elsevier FULL view, which required an API key, and encountered a human CAPTCHA in the browser. Those protections were not bypassed and failed routes were not relabeled as full-text inspection. Its abstract concerns a set-sharing result and says nothing sufficient about all of its other theorems or examples. This gap prevents a complete original-text comparison or a historical-intention claim. It does not weaken P1's explicit 2009 implication.

Chang–Fang [Acta Math. Sinica 23 (2007), 973–982](https://link.springer.com/article/10.1007/s10114-005-0861-5) was checked through the Springer and [journal-native pages](https://actamath.cjoe.ac.cn/Jwk_sxxb_en/EN/10.1007/s10114-005-0861-5). Both state the same nonzero shared value in the two antecedents. The advertised journal PDF returned 403, and Springer's PDF request returned subscription HTML. Thus the abstract is confirmed, but the complete paper was not reviewed. Its exact internal examples could matter to priority, so it is not dismissed as certainly irrelevant in its entirety.

Lü's [2010 paper](https://www.math.nthu.edu.tw/~amen/2010/090910-1.pdf), pp.175–176, uses nonzero a in the antecedents f=a and f'=a, and a third-derivative value c. The main result is neighboring, not a theorem about the target distinct-b/zero-a hypotheses. Its normal-family method does not supply a priority failure for the packet's exact scope.

The following primary texts were also checked at their relevant theorem and example sections: Chang–Fang (2002) fixed-point and same-value results; Chang–Fang (2006) three CM-sharing derivatives; Schweizer (2013) simple-point and ramification variants; Li–Gao–Zhang (2012) deficiency/CM results; Chang (2012) two CM values; Sauer–Schweizer (2022 preprint; 2024 journal reference) reverse partial sharing; Xu–Majumder–Mahato, [arXiv:2512.08001v1, 8 December 2025](https://arxiv.org/abs/2512.08001), Theorems 2.1–2.5 and examples; and Majumder–Sarkar–Pramanik, [arXiv:2509.20273v1, 24 September 2025](https://arxiv.org/abs/2509.20273), its main partial-sharing statements. The first 2025 preprint relates f to f^(k) at a nonzero a; the second uses powers/linear differential polynomials at the nonzero value 1. They require different antecedents, values, or multiplicity assumptions. No implication resolving the exact target was verified from them. Their stated theorems were mapped for scope, not certified as correct by this priority review.

The similarly named [*Value sharing of meromorphic functions and Fang's problem*, arXiv:1009.2132](https://arxiv.org/abs/1009.2132), was explicitly excluded after reading v1's Problem 1.1 on p.3: it asks about nonlinear differential polynomials and a 2009 Shanghai problem. The arXiv record marks v2 withdrawn in 2012 over an incorrectly cited lemma. Its title and withdrawal supply neither a solution nor a refutation of this 2007 problem.

## Required framing/attribution actions and reasonable salvage

1. **P1, required attribution:** cite the 2009 quadratic and explain the B=2b substitution. Any suggestion that the smallest counterexample or the universal negative answer is a newly discovered counterexample should be removed. State that the exact application to the literal report is being recorded, without claiming the old paper named that question.
2. **P2, required construction context:** cite the 2004 monomial formula and the 2009 squared-exponential exception. The packet's constructions should be described as applications of known forms. Preserve the distinction between the known forms and the packet's exact necessity proof/order relation.
3. **P3, required novelty scope:** separate a verified boundary observation from first priority and from solving the intended nonzero-a problem. A short note can make the exact polynomial classification and target-specific parameter calculation explicit, but first priority and scholarly sufficiency remain unverified. Do not treat the absence of an earlier located theorem as an originality certificate.

A defensible concise note would explain that the literal printed assertion permits zero; exhibit the already published quadratic through P1; give the polynomial necessity argument; and record the all-order squared-exponential tuning while crediting its source family. This is a reproducible source correction/application with two explicit calculations. The audit does not establish that those calculations are unpublished, and the primary-source gaps must remain visible. There is no reason here to reject a correct observation solely for its length or elementary proof; the concrete prior constructions are the substantive priority limitation.

Research note: access to legitimate complete copies of the original 2003 paper and 2007 Chang–Fang paper would improve the historical comparison. No outside individual was contacted, and no outreach was prepared. No paper, problem closure, Git mutation, remote write, additional agent delegation, or DOI/release action was performed.

## Audit boundaries and reproduction

`SOURCE_LEDGER.json` identifies every inspected source, its inspection depth, version/date, theorem locators, and exact relationship to the target. `RETRIEVAL_RECORDS.json` records public retrieval outcomes, byte counts, and hashes; all copied source material and extracts remain in ignored `tmp/primary/`. The 2004 cache excerpt has an excerpt hash, not a fictitious PDF hash. Search queries and failed source routes are recorded in `SEARCH_LEDGER.md`. The accepted independent math audit supplies the universal algebra; P1–P3 above are independent, checkable priority maps.

This was an extensive targeted search with citation and mechanism follow-ups through accessible 2026 literature, not an exhaustive world-literature proof. The remaining gap is exact novelty of the polynomial necessity statement and target-specific spectral relation, alongside incomplete original-source text. The strongest positive historical result is that the central universal negative answer is already a short consequence of an explicit 2009 published example.
