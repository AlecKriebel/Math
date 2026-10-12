# Source and prior-work audit

## Exact target

The assigned [UnsolvedMath page](https://www.unsolvedmath.com/problems/30001767) was attempted first but was not retrievable. The complete pinned record is preserved. Corpus revision: `37e53eabe540fb458758e198be61634bd02ee008`. There is no separate research_results entry for this problem number; the source record contains dated literature triage.

The complete [official OWR 21/2011 report](https://ems.press/content/serial-article-files/46337) was recovered. Ellers's contribution, printed pp. 1183–1184, states the exact conjecture and its existing small-gap result. Murray's p. 1192 contribution and the related questions on p. 1200 were also read. A page render verified the original statement and modular-system hypotheses.

The acting subgroup is the natural S_l fixing letters larger than l, and the algebra consists of invariants for conjugation, equivalently the commutant of its group algebra. The coefficients have positive characteristic p and the original system is sufficiently large. A block idempotent is centrally primitive, not merely primitive. Every nonzero product ef is automatically central in the centralizer; the unresolved issue is its primitivity. The source's stronger integral-center conjecture is not silently substituted for this target.

## Prior-attempt and duplicate gates

The fresh sparse checkout is based on main commit `c6975ca76f9f667f1250ba403d0e6da2aafe14d0`. Its queue has rank 181, queued 0/5; the state file is empty, and neither history nor related_target_groups mentions this ID. No exact-ID remote branch, all-state PR, target-named tracked folder or target-named commit was found before work began. The all-state PR search was `30001767 OR "Symmetric-Group Centralizer"`.

A pinned-corpus search for centralizer/block material located only this target and unrelated group-theoretic or Grothendieck-group questions. The imported August 2026 literature triage records no proof attempt. No previous Alec/campaign work was located.

## Current literature and access qualifications

- The original report already records the cases n−l<=3. Ellers–Murray's later Communications in Algebra 42 (2014),1074–1094 paper has DOI 10.1080/00927872.2012.731622. The cached earlier author preprint is dated 5 July 2010, and is not described as the final publication. The exact small-gap credit is independently present in both the original report and the current Fayers–Putignano paper.
- [Fayers–Putignano's complete author manuscript](https://webspace.maths.qmul.ac.uk/m.fayers/papers/ribbonblocks.pdf) carries a publication cover identifying Journal of Algebra 685 (2026),271–312, DOI 10.1016/j.jalgebra.2025.07.042. The [author's university publication record](https://researchpublications.its.qmul.ac.uk/publications/staff/21509.html) corroborates this information. The exact block conjecture is Conjecture 2.5, with its nonzero-ef reformulation directly following. Section 3 defines generalized ribbon blocks by distinct residues with n=m−l<p and belt blocks by n=p with each residue once. Corollaries 3.10 and 3.22 settle those families. I read the definitions, exact theorem statements and concluding linkage deductions; no complete independent re-audit of their long combinatorial proof or comparison with the final journal typesetting is claimed.
- [Danz–Ellers–Murray's full published 2013 paper](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/18B69524BB77FC4B356AFE1A2471C310/S0013091512000077a.pdf/the-centralizer-of-a-subgroup-in-a-group-algebra.pdf), Proceedings of the Edinburgh Mathematical Society 56 (2013),49–56, DOI 10.1017/S0013091512000077, was retrieved and read in full. Question 6 is the general finite-group analogue. Its counterexample is G=S6,H=A4,p5, not the target's S_l embedding. Proposition 3 assumes a normal p-subgroup. The new package's self-contained fixed-vector proof does not use normality, but makes no historical-priority claim. The published small-n center computations are reported as prior evidence, not independently recertified here.

Bounded searches through current exact-title, conjecture-name and relevant primary literature did not locate an unrestricted resolution. Nearby matrix-centralizer papers and characteristic-zero permutation-centralizer constructions concern different algebras and cannot settle this modular question.

## Result and stop condition

The first approach yields the fixed-algebra theorem and the all-n l=2,p=2 subclass. The second tests extension through coarse block data; the explicit characteristic-three sign-module control shows why the crucial fixed-vector inference fails outside p-groups. It is not a symmetric-group-algebra counterexample. The remaining required statement is that arbitrary nonzero ef corners are indecomposable, including repeated-residue cases not covered by the cited ribbon/belt theorem.

All 147 exact controls pass. The checker is deliberately small and uses only the standard library; it includes nonnormal subgroups, external permutation of ambient blocks, and central versus noncentral idempotents. It is not an exhaustive search or a proof of the unrestricted target. The argument is frozen for separate review. Original status: unsolved, 2/5. No outreach, release or shared queue edit was performed; source PDFs and renders remain outside the repository, with links/hashes in source_manifest.json. Actual selected model: gpt-6-astra, xhigh.
