# Independent priority review: mechanisms and exact scope

Review family B; PR 468 / problem 30000689. Frozen claimed-solved head: `8527ccdba064bca52035fc6c8d96caa750ac9c00`. Scope: only the frozen target/proof/addendum. Review performed 12 October 2026 UTC. Initial independent verdict was saved before reading any other fresh priority review; no such review has been read.

## Verdict

**No documentary earlier full resolution was found. First priority and novelty are not established.** This review does not justify classifying the literal target as already solved merely because its proof can now be assembled from old tools. Conversely, it does not justify advertising a new obstruction method or a first solution. The most defensible framing is a credited synthesis, with an explicitly supplied four-dimensional scope extension of Nevo–Wagner.

This is a priority finding, not a fresh mathematical pass/fail. The root and topology family reported mathematical validation. Nothing here changes the claimed theorem, strengthens its quantifiers, or substitutes a PL-only result for it.

The target is: for every finite triangulation S of the **topological** sphere S^(2d) and every missing d-face T, the complex S^(d) ∪ {T} has no **topological** embedding in S^(2d). Both bold qualifications matter.

## Exact prior antecedents and overlap

| Antecedent | Checkable locator | Documentary conclusion and exact gap |
|---|---|---|
| Nevo, higher minors | [arXiv:math/0602531v1](https://arxiv.org/abs/math/0602531v1), Conjecture 3.8; journal/current version Conjecture 3.7 | Exact target already formulated in February 2006. The accompanying join-of-a-circle-and-two-sphere example is a proved subfamily, not the general target. |
| Nevo–Wagner | [author paper](https://pi.math.cornell.edu/~eranevo/homepage/NevoWagner-EmbeddabilitySkeletaSpheres-Rev2.pdf), Theorem 1.2 / Conjecture 1.3; Section 5 | Theorem 1.2 already forbids topological embeddings for PL-standard source spheres. Its broader source conjecture remains separately stated. Theorem 1.4 is only a full-skeleton obstruction. |
| Adiprasito | [arXiv:1812.10454v4](https://arxiv.org/abs/1812.10454v4), Observation 4.3, printed p. 22; Corollary 4.8 and Remark 4.9, pp. 25–26 | Middle Lefschetz surjectivity already passes to a subcomplex quotient and gives dim A^d(L) ≥ dim A^(d+1)(L). This is the candidate's ambient algebraic mechanism. The exact missing-face corollary is not stated. |
| Karu–Xiao | [published record](https://alco.centre-mersenne.org/articles/10.5802/alco.298/), Theorems 1.2–1.3; [v3](https://arxiv.org/abs/2204.07758v3), pp. 2–3 | Supplies the candidate's generic anisotropy/Lefschetz input. It is an algebraic theorem about homology spheres; no missing-face embedding resolution was found in the full text. |
| Adiprasito–Patáková | [arXiv:2404.12265](https://arxiv.org/abs/2404.12265), Theorem 2; [published article](https://londmathsoc.onlinelibrary.wiley.com/doi/full/10.1112/blms.70036) | Retains an abstract PL-embeddable complex as an unsubdivided subcomplex of an ambient triangulation. This is precisely the geometric bridge the candidate needs. No missing-face corollary is stated. |
| Weber | [original article](https://www.e-periodica.ch/cntmng?pid=com-001%3A1967%3A42%3A%3A6), Theorem 1, p. 2 | Deleted-product existence theorem gives a PL embedding when 2m ≥ 3(n+1). For n=d and m=2d this is d≥3; it does not cover d=2. |
| Lutz–Nevo | [arXiv:1302.5197v3](https://arxiv.org/abs/1302.5197v3), Main Theorem 1.2 / Proposition 3.1 | Flag complexes and moves within a PL class are thoroughly antecedent. This paper does not apply Nevo–Wagner's obstruction transfer to an exotic four-sphere, or replace its complement-ball step by contractibility. |

The central Lefschetz-to-subcomplex argument should receive a direct Adiprasito attribution in any publication framing. Replacing its Lefschetz input by the independently published Karu–Xiao anisotropy theorem improves the exact dependency choice; it does not establish originality of that obstruction mechanism.

That quotient argument is already present in Adiprasito's **26 December 2018 v1**, Observation 4.3 (pp. 21–22) and Corollary 4.8 (p. 24); it is not an innovation of the later version.

## What is deducible, and what was actually documented

Here is my independent deduction map, not a claim about earlier authors recognizing it:

1. The candidate's Koszul calculation yields q_d=h_d(S) and q_(d+1)=h_d(S)+1 after restriction of 2d+1 generic ambient parameters. It is a finite-degree exactness argument; merely counting the added monomial would be insufficient. No matching explicit Koszul lemma was found in the checked primary texts.
2. For a prospective PL embedding, AP gives an ambient triangulation retaining L. Generic middle Lefschetz surjectivity descends to its quotient, as in Adiprasito's Observation 4.3 / Corollary 4.8. The dimension jump contradicts surjectivity. This produces a short, prior-method deduction of PL nonembedding for arbitrary topological-sphere sources.
3. For d≥3 a hypothetical topological embedding gives a deleted-product map, and Weber gives some PL embedding. Thus the high-dimensional literal target is a short synthesis of established tools and the compatibility calculation. It is not a new taming theorem.
4. For d=2 Weber is outside its existence range. A later general Lefschetz theorem plus AP does not close this part: AP starts from a PL embedding. One must supply a separate topological argument.

It is therefore wrong to promote step 2 alone as a full-target previous solution. It is also wrong to claim that step 3's logical availability proves an earlier documentary resolution. Priority attaches to a stated/proved result or a defensible recognition record, not automatically to the publication date of every theorem later combined to derive it.

## Four-dimensional extension compared with the original argument

The original Section 5 transfer is already a theorem about finite complexes and general-position maps once its structural, intersection and complement-homology conditions hold. Its proof of Theorem 1.2 starts from the simplex boundary, a vacuous base in the standard PL class. Observation 5.1 obtains the filling using a complementary PL ball. Those are the precise scope-sensitive points.

The candidate supplies the following additional deductions: a triangulation of a topological S^4 is a combinatorial 4-manifold; the complement of a bistellar support is contractible and collared; a **map** of the missing triangle can therefore be filled with interior avoiding the 1-skeleton; and a flag barycentric subdivision gives a vacuous base **in the same potentially exotic PL class**. Pachner moves connect that subdivision back to S. Its addendum also verifies structural hypotheses and the new-face witness.

I found no statement of this complete extension in the original paper, the older higher-minors paper, the checked later Lefschetz/anisotropy papers, or Lutz–Nevo's flag-move paper. The flags and local tools are old; the exact assembly and its scope checks are not documented there. This is evidence for an explicit extension being supplied here, not a certificate that the extension is new. It does not require claiming the existence of an exotic PL S^4 or resolving the four-dimensional PL Poincaré/Schoenflies questions.

## Stronger-looking results that do not settle this target by themselves

Adiprasito's Remark 1.1, both in v4 and the current [author copy](https://webusers.imj-prg.fr/~karim.adiprasito/bpa.pdf), explicitly retains a general-topological-embedding limitation for its broader face-bound result. This is useful category evidence. It is **not** evidence that this narrower missing-face target remains open in 2026.

The face-ratio bound f_d ≤ (d+2)f_(d−1) loses too much information. For the complete d-skeleton on 2d+3 vertices, f_d/f_(d−1)=(d+3)/(d+1), so the known van Kampen–Flores obstruction satisfies this ratio bound comfortably. In d=2, stellar subdivision of a triangle in the boundary of a 5-simplex, followed by adding that missing triangle, gives precisely the complete 2-skeleton on seven vertices: f_1=21, f_2=35≤84. The independently enumerated artifact [FACE_RATIO_COUNTERCHECK.json](FACE_RATIO_COUNTERCHECK.json) verifies this construction. Thus the ratio theorem alone cannot recognize even this old special case of the target.

The full symmetric-shifting Kalai–Sarkaria program has a closer relation: the middle-surjectivity condition corresponds to a forbidden shifted face, as NW Proposition 6.1 explains. Results for subcomplexes of an ambient triangulation supply the required algebraic condition in the PL/tame category. They do not automatically give arbitrary topological ambient extensions in d=2. Neither a stronger conjecture nor its weaker face-ratio consequence is a documentary full solution here.

The recent [Kishimoto–Matsushita paper](https://arxiv.org/abs/2410.17523v2) concerns unaugmented skeleta and smooth triangulations; its nonembedding background includes odd-dimensional spheres and even-dimensional manifolds with other obstructions. It does not prove the missing-face augmentation statement. The 2026 [Park preprint](https://arxiv.org/abs/2602.06016) concerns linear local convexity under PL moves; no applicable embedding obstruction was found.

## Dates and publication recommendation

The conjecture appears in Nevo v1, posted **23 February 2006**, as Conjecture 3.8, and is renumbered 3.7 in the journal version. NW's arXiv paper was first posted **7 September 2007**; the frozen proof uses the separately dated **4 February 2008** author revision and credits the 2009 journal paper.

Adiprasito's Lefschetz paper v1 was posted **26 December 2018**, v4 **2 July 2019**. Its current author copy is mutable and has no verified historical version date. Karu–Xiao's v1 was posted **16 April 2022**, v3 **22 January 2023**; the published paper is **Algebraic Combinatorics 6 (2023), no. 5, 1313–1330**, online **7 November 2023**.

AP Theorem 2 is present in **v1, 18 April 2024**. The final article first appeared **27 February 2025**, with **v3 posted 11 March 2025** and the May 2025 issue. The final proof expands/reworks the strongly induced step. Both versions describe the extension as folklore, so neither 2024 nor 2025 is a demonstrated first-availability date for that tool.

**Recommended framing:** retain the root's mathematical resolution disposition for the exact target, subject to its proof audit. State that the proof combines established algebraic and embedding results, attributes the ambient quotient argument to earlier Lefschetz work, and explicitly extends the NW argument within the potentially exotic four-dimensional PL class. Cite Nevo's 2006 conjecture antecedent as well as NW. Do not say “first solution,” “novel obstruction method,” or “new discovery” on this search alone. Do not mark the entire target prior-resolved without finding a source that actually documents the full conclusion or an adequately evidenced earlier recognition.

Remaining priority gap: unindexed papers, seminar notes or folklore may record the full corollary or four-dimensional scope extension. Independent human bibliographic review could help assess that gap. No external contact, outreach preparation, publication operation, Git mutation, queue change or PR action was performed by this family.

Sources and searches are bounded and reproducible through [SOURCE_LEDGER.md](SOURCE_LEDGER.md), [SOURCE_RECEIPTS.json](SOURCE_RECEIPTS.json), and [RESEARCH_LOG.md](RESEARCH_LOG.md). Foreign full texts and page renders are ignored under `private_sources/`.
