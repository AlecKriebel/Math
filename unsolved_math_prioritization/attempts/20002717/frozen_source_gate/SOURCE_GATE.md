# 20002717 — Cayley interval lattices: source and prior-work gate

Checked 2026-10-03 UTC. **No author research turns: 0/5. No remote writes.**

## Disposition submitted for independent scope review

The source asks for natural sufficient conditions and a natural class explaining lattice versus nonlattice behavior. Existing results answer that request substantively. This is a **credited source-resolution candidate**, not a new theorem, and not a classification of arbitrary marked groups.

A final `already_solved` disposition has **not** been assigned. The reviewer must decide whether the source's representation remark requests an additional representation-free proof. A group-theoretic statement and a representation-free proof are different requirements. The former is furnished by published literature; the cited proof uses geometry. The imported elementary examples provide further credited evidence, but their sufficiency for closing the open-ended question requires an explicit scope judgment.

## Exact target and source location

The live repository row is rank 424, numeric ID 20002717, code AIM-PROBABILITY-0159, queued, 0/5. The title “A product criterion and a bowtie obstruction for Cayley interval lattices” names imported partial work. “Probability” is an import category. The primary mathematical setting is geometric/combinatorial group theory.

The source is J. McCammond's Problem 4.3 in Drew Armstrong's *Braid groups, clusters, and free probability: an outline from the AIM workshop, January 2005*, printed pages 9–10. The problem begins on page 9; its remark is on page 10. The trailing OCR “10” is a page number. [Primary workshop PDF](https://aimath.org/WWN/braidgroups/braidgroups.pdf).

Full mathematical scope, paraphrased: take a group G with a finite generating set T closed under conjugation. Its Cayley intervals supply quasi-Garside structures, whose potentially missing axiom is the lattice axiom. Seek natural conditions on the marked group (G,T) ensuring that axiom, and a natural family for which its presence or failure has an explanation. The remark discusses Brady–Watt's uniform noncrossing-partition lattice proof and notes its reliance on realizing W as a real reflection group. Its final question is exactly:

> Is there a class of quasi-Garside structures in which the lattice property can be seen only to depend on the group structure?

The source does not explicitly demand a complete classification of all (G,T). It also does not explicitly contain the phrase “representation-free proof.” The quoted sentence should not be silently discarded as motivation, nor silently strengthened into a universal classification problem.

For the audited families take T inverse-closed. With word length l_T, the interval I(g) consists of x satisfying l_T(x)+l_T(x^{-1}g)=l_T(g); its order is the corresponding prefix order. Source §1 and Problem 3.1 give length additivity, and Problem 4.4 identifies the interval as [1,g]. Reflections are involutions, so symmetry is automatic for the published finite Coxeter examples. The imported examples also use symmetric sets. Nothing here resolves alternative directed positive-word conventions for arbitrary nonsymmetric T.

## A published natural class, with a group-theoretic criterion

Let (W,S) be a finite Coxeter system and T its full reflection set, namely all conjugates of S. For an element x, let P(x) be its parabolic closure. A parabolic subgroup is involutive when it equals P(v) for some v with v²=1; this convention includes the identity case.

Gobet's Theorem 3.11 states that for u²=1, I(u) is a lattice exactly when the involutive parabolic subgroups of P(u) are closed under intersections. Proposition 3.10 identifies the interval with those subgroups ordered by inclusion. This makes both success and failure a subgroup-structure condition. Corollary 4.3 lists the allowed irreducible factors: A1, I2(2k) for k≥2, Bn for n≥3, D4, and H3. For example D4's central longest-element interval is positive; D6's is negative. These examples retain finite T. [Gobet, arXiv:2507.11340v1, §§3–4](https://arxiv.org/html/2507.11340v1); publication is *Bull. Aust. Math. Soc.* 113 (2026), 492–503, DOI 10.1017/S0004972725100531, confirmed on [the author's publication list](https://gobet.perso.math.cnrs.fr/).

**Proof limitation:** Gobet's preliminaries use the geometric representation and Carter's lemma, and proofs of Propositions 3.3, 3.6, 3.9 and 3.10 use eigenspaces or moved spaces. We do not claim that this is a representation-free proof. The criterion is stated in the Coxeter/parabolic subgroup structure, not in the unmarked abstract group with its generating set forgotten.

## Corroborating literature and current status

Baumeister–Holt–Neaime–Rees classify quasi-Coxeter intervals in finite Coxeter groups. A quasi-Coxeter element admits a reduced reflection factorization generating the whole group. The final Theorem 2.12 gives: in simply-laced types and F4, the interval is a lattice precisely for Coxeter elements; H3 is positive throughout; H4 additionally admits proper quasi-Coxeter elements of order 30. Therefore an older search snippet saying merely “Coxeter or H3” is unsafe. These are endpoint conditions, not an assertion about every interval for fixed W. Theorem 2.16 separately records the balanced-lattice mechanism for interval Garside groups. [Final paper, *Trans. London Math. Soc.* 10 (2023), 100–123](https://londmathsoc.onlinelibrary.wiley.com/doi/full/10.1112/tlm3.12057).

Chavli–Gobet's July 2026 preprint repeats Gobet's classification as Theorem 1.1 and investigates the resulting interval groups. This corroborates the classification, but is not needed as a new solution. [arXiv:2607.21510](https://arxiv.org/abs/2607.21510).

A fresh September 29, 2026 preprint, absent from the August imported report, introduces absolute moved spaces, proves new injectivity results, and gives additional infinite rank-four nonlattice examples. Its introduction still describes substantial open cases. It relies on the geometric representation and concerns infinite reflection sets in relevant infinite-group examples, so those examples do not automatically meet AIM's finite-T hypothesis. [Gobet, arXiv:2609.37867](https://arxiv.org/abs/2609.37867). This gate does not claim a resolution of that broader current research program.

## Imported product and bowtie work: credit and audit

The hash-verified UnsolvedMath report is explicitly imported third-party AI research with low novelty confidence. Its “attempt 1” is not an Alec Kriebel repository attempt and does not consume the user's turn budget.

Its product family is G=F×C(n1)×…×C(nd), where F is finite and cyclic factors may be finite or infinite. The marking uses every nonidentity element of F and the two coordinate directions in each cyclic factor. The supplied proof establishes an l1 sum of factor lengths and a coordinatewise product of intervals. Finite-factor intervals are trivial or two-element chains. Cyclic intervals are chains or two equal arms sharing their endpoints at an even antipode. All are lattices. The proof is representation-free and covers arbitrary endpoints, including identity and order-two factors.

Its negative example uses Z² with the eight nonzero vectors in {-1,0,1}². Length is max(|p|,|q|). The interval to (3,0) has ranks {0}, {(1,-1),(1,0),(1,1)}, {(2,-1),(2,0),(2,1)}, {(3,0)}. The atoms (1,0),(1,1) have distinct rank-two common upper bounds (2,0),(2,1), so their join fails. The dual meet fails too. The proof does not require a geometric reflection representation. These elementary facts are preserved as credit, not claimed as new findings.

A small portable checker independently replays representative finite products and the complete eight-vertex king interval. These controls check transcription and hypotheses; they do not replace the imported all-endpoint proof or independently verify the cited classification theorems.

## Repository/prior-attempt gate

- Live QUEUE blob: 34888539d9c0163e100aac91942f827e0693932b. Current assessment has no holds, but only a low-confidence desk judgment; its review hash is in GATE.json.
- Main state/history/assessment-history contain no target attempt. Related-target-groups has no target entry.
- All 442 live branch names were enumerated through the connector. No target-ID or neighboring-2000271x, Cayley/Garside/bowtie branch was found. The generic preservation branch was checked at its root and had no relevant work area.
- The full main recursive tree was truncated, so it is not used as exhaustive negative evidence. The separately fetched queue subtree was untruncated, with 9,242 entries, and had no target/topic attempt path.
- PR searches in all states for the ID, code, Garside, and bowtie returned none. “Cayley” returned four unrelated PRs (#65, #104, #240, #349). Commit-message searches for ID, Garside, and bowtie also returned none.
- The related-corpus search found neighboring AIM Problems 3.4 and 4.1/4.2/4.4, plus a qL-algebra record; these are distinct questions, not equivalent resolutions.

These checks found no prior user attempt. They do not prove absence from every unindexed file or deleted branch. Imported research remains separately credited.

## Access, provenance, and decision boundary

The UnsolvedMath live page could not be retrieved with the web tool. The approved pinned fallback was used and both complete corpus files were hashed against the repository's published manifest before selection. The primary AIM PDF was read through the web tool's page-aware text extraction; local download returned HTTP 403 and screenshot retrieval failed. No local PDF or visual verification is claimed. Primary literature PDFs and final BHNR HTML were accessible.

Independent scope review should choose one of two explicit outcomes:

1. **Credited natural-class answer:** the main request and its group-structural formulation are already substantively answered; record prior credit, no new research priority, 0/5.
2. **Hold for representation-free-proof scope:** if the final remark requires a proof avoiding representations rather than a group-structural criterion, the published Gobet proof alone does not discharge it. Specify whether the credited elementary marked-product family satisfies that existential request. If not, state the exact unmet requirement before any research turn.

Neither outcome authorizes replacing the source with a classification of every finite symmetric generating set of Z² or of every marked group. No status cell, branch, commit, PR, release, DOI, or external communication was created by this gate.
