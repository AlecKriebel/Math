# Source gate: 30003659 / OWR-15958-006

2026-10-02. Rank329. **Zero substantive author turns. Gate investigation only. Original cut-free Kozen completeness is not resolved by the materials inspected.**

## Original source and precise caution

The full Afshari contribution, joint with Graham E. Leigh, *Cut elimination for modal mu-calculus*, OWR53/2017 report pp24–26, has been read. Its report page25 was visually checked, including all displayed induction/strong-induction/binder-contraction rules. Source DOI10.4171/OWR/2017/53; primary archive PDF https://publications.mfo.de/bitstream/handle/mfo/3617/OWR_2017_53.pdf . The source asks whether the natural sequent rendering of Kozen's axiomatization remains complete on removing cut. It explicitly distinguishes that question from annotated cyclic and infinitary systems.

The UnsolvedMath page https://www.unsolvedmath.com/problems/30003659 was inaccessible through the web tool. The pinned complete dataset record supplies the imported wording and its dated2026-08-21 literature assessment. No upstream research_results entry is present. The imported report2018 citation and report2017 designation refer to publication/report dating, not different mathematical problems.

## Exact rule-version distinction

The cited Afshari–Leigh OWP2016-26 primary preprint gives an explicit one-sided finite-set-sequent calculus in Figures1–3 and §3.1. Its Fix core has atomic identity, weakening, disjunction, conjunction, the modal K rule, and both fixed-point unfolding rules. It adds generalized identity for dual fixed points and the ordinary greatest-fixed-point induction rule

    from Γ, A(neg(disjunction Γ)) infer Γ, νx A(x).

Proofs are finite well-founded closed derivations. The core is not a cyclic calculus. The preprint then ALSO includes a deep-disjunction rule

    from Γ, A(B), A(C) infer Γ, A(B∨C),

and specifically says admissibility without cut is not obvious. Its symbol Koz− therefore denotes this enlarged cut-free presentation. One cannot silently treat it as the bare natural sequent system with cut deleted. A future proof must explicitly name which presentation it establishes and justify every transfer to the source target. The published LICS2017 DOI10.1109/LICS.2017.8005088 has been identified but its full conference text has not yet been recovered independently; this version check remains open.

The source report's strong-induction rule is

    from Γ, νx A(neg(disjunction Γ)∨x) infer Γ, νx A(x).

The report also asserts an equivalent reduction to contraction of like fixed-point binders. Its semantic validity is not a proof of syntactic admissibility in the original cut-free system.

## Material correction to the cited completeness route

Kloibhofer's2023 primary paper, *A note on the incompleteness of Afshari & Leigh's system Clo*, arXiv2307.06846, proves the cyclic cut-free Clo system incomplete. Its introduction explicitly says this breaks the earlier completeness chain and lists completeness of the strengthened well-founded system Koz_s− as unknown. This is not a counterexample to the distinct ordinary-induction Kozen calculus.

The final2025 *Demystifying μ*, Afshari–Leigh–Menéndez Turata, DOI10.46298/fi.12773, was checked at §§3,5,7 and their dependencies relevant to this issue. Section5 explicitly acknowledges the old Clo claim was false, identifies the cut-free fragment of its Cμ with Clo, and restores full completeness for systems containing cut. Its induction simulation uses cut. Its cut-admissibility result for illfounded constructive proofs is another system, not cut elimination for finite Kozen proofs. The source report's original claim that the strengthened system is already complete cannot therefore be used as a verified reduction without a repaired independent theorem.

Primary links:
- https://oa.tib.eu/renate/bitstreams/50824d0c-d5f5-4a10-8518-36ade258b3e3/download
- https://arxiv.org/abs/2307.06846
- https://fi.episciences.org/16412/pdf

The limited current primary-literature search found other complete cut-free cyclic/infinitary/two-way systems and these corrections, but no verified resolution of the exact finite ordinary-induction target. Absence in this bounded search is not a proof of global literature absence.

## Prior campaign gate

No exact target or Kozen alias artifact was found in310 recovered remote heads under the three campaign artifact roots. Live PR searches for30003659, Kozen, cut-free and15958 returned no match. No matching related_target_groups entry was found. This does not certify absence of uncommitted or unindexed work. PRIOR_SCAN.json records the scope.

## Gate outcome

The exact question remains eligible in principle, but no author turn is started until the presentation is pinned tightly enough to avoid proving a strengthened, cyclic or infinitary substitute. The old strengthened-completeness reduction is not an accepted input. No new theorem, counterexample, solved disposition, QUEUE update or PR is claimed by this source audit.
