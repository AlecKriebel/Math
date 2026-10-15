# Independent adversarial priority audit: PR 1047 / problem 30004909

Audited edition: head `56b3a35182e5cb04b05e41f5017e47caf50582c1`. Literature cutoff: 13 October 2026. This is an AI-assisted, unrefereed research audit, with no external human review or formal certification.

## Disposition

**The accepted mathematical result is eligible for a neutral, credited elementary-obstruction or expository presentation. Historical novelty, intellectual priority, independent discovery, and current worldwide open-problem status are not cleared.** The bounded primary-body review did not identify an exact earlier presentation of the submitted ordinary-rank lower bound or the generic exact cardinality envelope. That is an unresolved attribution gap, not evidence of firstness. Do not reject or close sound mathematics merely to turn that gap into a binary novelty label. Credit the established cardinality-function and rank-sum constructions, and retain the explicit source-interpretation caveat throughout promotion.

The source question is the actual displayed two-sided formulation, not the corpus transcription that omitted its left denominator. A uniform constant is interpreted as independent of both the input function and finite ground-set size. The complete printed passage does not separately quantify over ground sets. No present author intent or later unpublished correction can be established from that passage alone.

## Claim and evidentiary separation

The claim accepted by the root mathematical audit is

\[
\neg\bigl[\exists\alpha>0\ \forall\text{ finite }V\ \forall f\ \exists M\text{ on }V\ \forall S\subseteq V:
 r_M(S)/\alpha\le f(S)\le\alpha r_M(S)\bigr],
\]

where \(f\ge0\) is monotone and submodular, \(f(\varnothing)=0\), and every singleton value is one. The approximant is one ordinary, unscaled matroid rank on the same ground set. The submitted square-root family forces \(\alpha\ge n^{1/6}\) and has all-matroid exact optimum \(\min_{R=1}^n\max\{\sqrt R,\sqrt n/R\}\), with cube-size sharpness. The rational family on \(n=m^2\) forces \(\alpha^2+\alpha\ge m\) and \(\alpha\ge n^{1/4}/\sqrt2\). The root's accepted proof and reproduction receipts are mathematical inputs; they are not primary-literature novelty evidence.

All nine original files were frozen and independently compared to their actual git objects at the pinned head. Four root inputs were frozen separately. `INPUT_PINS_INITIAL.json` records their exact hashes. A fresh primary comparison was saved and hashed at 2026-10-13T23:19:39.011568+00:00 before reading the old SOURCE_AUDIT, PROVENANCE, SOURCE_PROVENANCE or bounded-search record. The immutable `PRE_OLD_AUDIT_CHECKPOINT.json` identifies this independence boundary. The submitted REPORT was read earlier only to define the claim.

## Primary-body comparisons

### Original question: Végh, OWR 53/2021

[Official EMS report](https://ems.press/content/serial-article-files/46931), [MFO report record](https://publications.mfo.de/handle/mfo/3922), DOI10.4171/OWR/2021/53. The entire contribution on printed2946 / PDFpage54 was read and visually inspected; the next contribution starts below. It has singleton values1, zero empty value, nonnegative monotone submodular inputs, one rank on the same \(V\), and \(r(S)/\alpha\le f(S)\le\alpha r(S)\) on all subsets. No scalar, weights, expansion, or sum is specified. It uses \(f\) in the sentence naming the rank and \(r\) in the display. A separate all-\(V\) quantifier is absent.

Fresh EMS bytes match the submitted source hash. A fresh MFO copy differs in PDF bytes but has exactly identical extracted text; it is a distinct hashed retrieval, not a presumed identical edition. Search and record inspection found no published correction in this bounded review. The DOI opening failed while both primary PDFs were accessible. None of these observations certifies current worldwide openness.

### Goemans–Harvey–Iwata–Mirrokni: 2009 conference and 2010 full draft

[Conference body](https://www.cs.ubc.ca/~nickhar/papers/SubmodularEverywhere/SubmodularEverywhere.pdf), [full draft](https://www.cs.ubc.ca/~nickhar/papers/SubmodularEverywhere/SubmodularEverywhereFull.pdf), [author's version list](https://www.cs.ubc.ca/~nickhar/papers.html). Conference full10-page body read; full-draft Problem1, §§3–6, algorithm outputs and lower-bound construction compared. The author lists the long source as a 2010 full-version draft; no later journal identity is assumed.

Problem1 restricts queries and permits arbitrary approximants. The actual output is \(\sqrt{\sum_{i\in S}c_i}\), not an asserted ordinary rank. Full-draft Theorem7 concerns matroid-rank inputs; §6, printed12–13, constructs uniform/truncated-partition matroid inputs and uses indistinguishable oracle answers. Selecting the original input rank would give an exact existential approximant. Therefore this query lower bound does not imply the submitted structural impossibility. Conversely, its structural root-linear existence result must be acknowledged: the square-root-cardinality input is itself root-linear. This distinction comes from the body, not merely its algorithmic abstract. Deferred proofs are present in the retrieved long draft; unrelated geometric appendices were not exhaustively audited for priority.

### Balcan–Harvey: STOC2011 and SICOMP2018

[STOC body](https://www.cs.cmu.edu/~ninamf/papers/LearningSubmodular-STOC.pdf), [journal body](https://www.cs.ubc.ca/~nickhar/papers/LearningSubmodular/LearningSubmodular-SICOMP.pdf), DOI10.1137/120888909, SICOMP47(3):703–754. Relevant STOC§3.1/Theorems5–7 and journal§5/Theorem13 and proof, printed732–734, were read. Journal§1/§4 learning and representation statements were also inspected.

The distributional structural theorem sends a loopless rank to a concave cardinality function that works on a \(1-\epsilon\) fraction of each size layer. Direction and allowed exception sets differ from the candidate. It gives no every-subset approximation of an arbitrary concave function by one rank. The learning/sketching lower bounds use matroid inputs that admit their own exact ranks, so they likewise do not imply nonexistence. Journal Proposition1 credits the concave-cardinality construction to Lovász's 1983 survey, p251; the original Lovász body was not independently retrieved. Attribute the classical construction without claiming that this review verified every original-source detail.

### Devanur–Dughmi–Schwartz–Sharma–Singh: arXiv1304.4948v1

[Primary body](https://arxiv.org/pdf/1304.4948v1), [version history](https://arxiv.org/abs/1304.4948). Metadata confirms submission17April2013; the downloaded title-block date29October2018 is not a later scholarly version history. Read §§1/4/5, AppendixD, and F/G statements and relevant proofs. §5 printed11 asks about rank sums, and AppendixD printed14 LemmaD.1 already exactly represents uniform monotone submodular functions by nonnegative sums of uniform matroid ranks. The stated integer restriction is unnecessary for its finite-difference mechanism after correcting typographical slips; see the direct derivation below.

This is prior art for the input constructions and their decomposition. It is not, in the inspected statements, the submitted quantitative obstruction against a single rank. The graph-cut/Gomory–Hu tree claims address symmetric or nonmonotone cut-function approximants, and the structural coverage/budget-additive lower bounds address another output class. They were compared as structural results instead of being discarded for appearing in an algorithmic paper. §5's singleton-ratio assertion for rank sums points to Schrijver44.6(B); the actual cited body is discussed next. It cannot be promoted to a normalized single-rank theorem by assertion.

### Schrijver2003, chapter44 / Helgason1974 expansion

[Chapter44 primary text, hosted by TU Berlin](https://page.math.tu-berlin.de/~felsner/Lehre/SemMatS/Literatur/Schrijver-44%3ASubmod%2BPolymat.pdf). Read §§44.1a,44.6a–b and relevant structure/operations statements; visually checked entire44.6b, printed776 / chapterPDFpage11. The construction assigns disjoint blocks \(X_s\) of size \(F(\{s\})\) to an integer polymatroid \(F\), constructs a matroid rank on their union, and obtains \(F(T)=r(\bigcup_{s\in T}X_s)\). It credits Helgason1974. With integer singleton values1, blocks have one element and the ordinary-rank characterization follows.

Fractional singleton-normalized functions are not covered by that last special case. Clearing a rational denominator makes singleton blocks larger, and dividing the expanded rank by the denominator is a scaled expanded representation. It is not one ordinary rank on original \(V\). The cited chapter does not itself supply DDSSS's rank-sum singleton-ratio approximation without an additional argument. That unproved citation-chain consequence remains unknown; it is not an exclusion of all rank-sum literature, and not a contradiction to the candidate. Helgason's original paper body was not independently retrieved.

### Dobzinski–Feige–Feldman–Paes Leme: arXiv2102.13343v3

[Primary body](https://arxiv.org/pdf/2102.13343v3), [version history](https://arxiv.org/abs/2102.13343). v1 dates26February2021; inspected v3 dates20February2022. Read definition of approximation, Theorem1.2, §3.1 actual BA(k,d) construction and Theorem3.13 proof, §4.3 Proposition4.8 and weighted/Rado upper-bound statements, AppendixA definitions.

The main structural nonexistence result concerns approximation by gross substitutes, a class containing single weighted ranks. This larger output class makes it a serious lead. But its actual hard input has \(k^h\) items of singleton value \(k^{-h}\) per level, so it does not satisfy all singleton values1. A common scalar cannot equalize these values. No normalization-preserving reduction was supplied in the inspected proof. Proposition4.8 says concave compositions of ordinary ranks are exactly gross substitutes, describing both candidate families via the free rank. Hence this particular GS lower bound cannot be the candidate's cardinality obstruction; it addresses different hard inputs. The broader theorem is credited without presenting its unverified normalization transfer as settled.

### Dughmi–Roughgarden–Yan2011 and Dughmi2011

[Combinatorial auctions body](https://arxiv.org/pdf/1103.0040), [public-projects body](https://arxiv.org/pdf/1103.0041). Read actual MRS definitions and main optimization formulations/Theorems4.1 and3.1, respectively, and the auction body's discrete-Hessian criterion/Claim4.5. These optimize welfare over allocations or cardinality-constrained project selections, with MRS valuations as inputs; the produced object is an allocation mechanism. Their objective guarantee is not a pointwise rank approximant. Their MRS class is nonnegative combinations of ranks and includes the rational candidate exactly. The Hessian condition constrains exact rank-sum representations but supplies no candidate single-rank lower-bound rate. These body comparisons do not exclude every uninspected lemma or cited paper.

### de Vries–Raach–Vohra2024/2025: inner approximation

[Publisher full text](https://onlinelibrary.wiley.com/doi/full/10.1002/nav.22210), first published18July2024, NRL72(1):133–147 (2025). Publisher web body displayed §§2–3 definitions, Theorem2 and its opening proof, Theorem7/Corollary8 and §4 Theorem16. Its worst-case optimization ratio equals a pointwise rank quotient in specified independence-system settings. Thus it is material and was not dismissed as mere maximization. The targets are integer ranks of independence systems or integer packing instances, and approximants are required to be inner systems. The fractional concave-cardinality input is not such an integer rank. Making the integer submodular target singleton-normalized instead already makes it a matroid. No equivalence to the candidate was established. Direct raw download returned403, so a raw-body hash is unavailable; only the inspected publisher statements are compared, and uninspected critical extensions remain unknown.

## Checkable transfer and implicit-result tests

### Singleton normalization connects single scaled/weighted ranks

For a standard weighted rank \(q(S)=\max_{I\subseteq S,\ I\in\mathcal I}\sum_{i\in I}w_i\), suppose
\(\ell q(S)\le f(S)\le u q(S)\) on every set, with \(0<\ell\le u\) and singleton values1. Singletons force nonloops and \(1/u\le w_i\le1/\ell\). A maximum-cardinality independent set supplies \(q(S)\ge r(S)/u\), and every independent set has at most \(r(S)\) members, supplying \(q(S)\le r(S)/\ell\). Therefore

\[
 (\ell/u)r(S)\le f(S)\le(u/\ell)r(S).
\]

The same argument applies to \(q=c r\), because its singleton weights all equal \(c\). Symmetric weighted/scaled factor \(a\) implies ordinary factor \(a^2\); one-sided \(q\le f\le\theta q\) implies ordinary factor \(\theta\). A uniform constant existence theorem for either single scaled or weighted ranks on the exact normalized class would consequently contradict the candidate. A nonconstant obstruction for such a larger output class would imply the candidate, provided its input normalization matches. Polynomial rates do not transfer unchanged under the symmetric convention. An abstract containing the word weighted or scaled cannot be excluded on that basis alone.

### Known decomposition versus one-rank envelope

For \(h(0)=0\) and nonincreasing nonnegative increments \(d_i=h(i)-h(i-1)\), put \(c_i=d_i-d_{i+1}\) for \(i<n\), and \(c_n=d_n\). Then
\[
 h(k)=\sum_{i=1}^n c_i\min(k,i),\qquad c_i\ge0.
\]
The increments of the right side are \(\sum_{i\ge k}c_i=d_k\), proving equality from the common zero value. Singleton normalization makes \(\sum_i c_i=1\). This is the real-valued finite-difference extension of credited DDSSS LemmaD.1. Its printed first coefficient \(2f_2-f_1\) is incorrect, as are some indices; the correct one is \(2f_1-f_2\) when \(h(0)=0\). A linear \(h(k)=k\) already falsifies the printed first-coefficient formula, so the typo does not remove the prior decomposition mechanism.

The rational candidate uses only \(c_1=1-1/m\) and \(c_n=1/m\). Its known-rank convex combination is not a new function class, new axiom, or new representation. The square-root family is likewise a classical concave-cardinality member with this decomposition. To show explicitly why expansion literature is compatible, \(m g_m(S)=(m-1)\min(|S|,1)+|S|\) can be represented by the direct sum of \(m-1\) rank-one uniform layers and one free layer, with each original element replaced by its \(m\) layer copies. The union-of-block rank divided by \(m\) equals \(g_m\) exactly.

A separate reviewer deduction gives the generic exact ordinary-rank envelope
\[
 \alpha_*(h,n)=\min_{1\le R\le n}\max\{R/h(R),h(n)/R\}.
\]
For any proposed matroid of total rank \(R\), its basis and full set force the two ratios. The uniform \(U_{R,n}\) attains them: for \(k\le R\), \(k/h(k)\) increases by concavity and \(h(k)/k\le h(1)=1\); for \(k\ge R\), monotonicity gives the maxima at \(R\) and \(n\). The displayed max already covers1. The submitted exact square-root optimum is a specialization, and the rational bound uses this same basis/full-set mechanism. **No prior source for this generic one-rank envelope has been found or excluded.** If an earlier source states it, cite the candidate as its corollary and attribute the formula, rather than claiming a new exact optimum. The known rank-sum decomposition alone does not state this envelope or establish its lower-bound priority.

## Old-audit comparison and editorial obligations

The fresh source hash/whole-page findings corroborate the old source comparison. The earlier audit's limited GHIM Problem1 inspection was insufficient to dismiss the entire paper; fresh conference-body and full-draft output/lower-bound inspection now supports the narrower exact distinction. The old statement that sum/constraint results were not treated as answers needs this deeper construction-and-quantifier comparison. Weighted/scaled single-rank results can matter through singleton transfer. Rank sums matter as prior art for the actual families even when they do not solve the one-rank target.

The submitted neutral title and explicit disclaimers are compatible with expository eligibility. Before promoting the package, apply credit and scope consistently to every surface:

1. **Title/abstract/PR title and summary:** describe a same-ground-set elementary obstruction to the displayed dimension-independent formulation. Avoid first/new/previously unsolved/currently open/worldwide settled claims. The source caveat cannot appear only in an appendix.
2. **Theorem and construction text:** keep exact same-\(V\), ordinary unscaled rank, both inequalities and all singleton hypotheses. Credit classical concave-cardinality functions and uniform-rank decomposition; do not rename them as new constructions. Preserve square-root-family-only optimality.
3. **Source/related-work section:** add DDSSS AppendixD LemmaD.1 and Balcan–Harvey's attributed classical concave-cardinality construction; distinguish GHIM query lower bounds from its actual structural output. Include weighted/scaled transfer as a reason literature exclusion is quantitative, not by label. Credit Helgason/Schrijver if discussing expansion, and DFFPL if discussing GS approximation.
4. **README/STATUS/ACCEPTANCE/provenance and PR metadata:** retain no-novelty/no-current-global-open-status limits, explicit source interpretation, AI-assisted unrefereed status, and exact stronger-output boundaries. Do not present this reviewer as human peer review or formal proof certification. The PR metadata itself was not read or altered by this reviewer; the root must check its actual final wording.

A suitable editorial sentence is: “We give a self-contained elementary obstruction to the displayed dimension-independent ordinary-rank formulation. The cardinality functions and their rank-sum structure are classical; the bounded primary-body review does not establish priority for the exact one-rank argument.” If exact prior envelope literature is later verified, replace the second sentence with precise attribution and corollary framing.

## Search coverage, failures and chronology limits

`QUERY_LOG.json` records44 exact web queries, source-question corrections, concave/cardinality, normalized, single/unweighted/scaled/weighted, rank-sum, generic-envelope and contemporary-title variants. `SOURCE_RETRIEVAL_FRESH.json` records primary requested/resolved URLs, retrieval timestamps, byte/text hashes, and errors. Forty-four queries and their inspected bodies are a bounded review, not a census of preprints, books, lecture notes or private knowledge. Current search result publication/crawl timestamps were not substituted for a source version's date.

The Technion-author DDSSS download failed certificate validation; arXiv supplied its primary body. A guessed Balcan–Harvey filename returned404; the actual author-listed journal filename was retrieved. A DOI opening and an author directory opening failed. The inner-independence raw download returned403, though publisher web statements were accessible. Four attempted read-only public Zenodo API searches returned400 and supplied no evidence; no deposit or account mutation was attempted, and no further service call was made. These are coverage failures, not negative search findings.

No exact contemporary matching preprint was identified. The pinned candidate carries9October2026 dating, but that label alone does not prove intellectual priority or discovery chronology. If a later DOI with matching mathematics is found, compare its public body/version history with the pinned candidate and report overlap and dates without assumptions about independent discovery, dependence or copying. No communication with individuals, access request, private worker artifact, PR-service mutation, publication or git-index change occurred.

Unresolved critical bodies/consequences include Lovász's and Helgason's original papers, the unpublished manuscript cited by GHIM, the unproved singleton-ratio rank-sum consequence of the Schrijver citation, any normalization-preserving GS/weighted impossibility transfer, and the exact generic ordinary-rank envelope's literature history. They remain unknown, not excluded. The strongest verified disposition is credited elementary/expository eligibility with these explicit limits. Source priority gaps do not create an internal mathematical gap in the accepted proof.
