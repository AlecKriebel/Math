# Action dependence of measured free indecomposability

## Target and conventions

Target: OWR-2487-003, catalogue 30001092, rank 1099. The mathematical question is whether a single countable group admits two essentially free probability-measure-preserving actions, one with an FI orbit relation and one with a non-FI orbit relation. The spaces are standard Borel spaces with atomless probability measures. Ergodicity is **not** an assumption of this question. Every assertion below that requires ergodicity says so explicitly.

The catalogue's isolated sentence omits essential freeness. That omission changes the problem. The published formulation [AG, Question 4.16] removes any ambiguity left by reading OWR Question 4 outside its surrounding definitions. A construction using a nonfree action is not a solution of the source problem.

An action is essentially free if the fixed set of every nonidentity group element is null. Since the group is countable, an invariant conull Borel set may be chosen on which it is free. We always work modulo invariant null sets. The orbit relation is a countable Borel equivalence relation, and every partial Borel isomorphism with graph in it preserves measure. For an infinite group acting freely its classes are infinite; this is the aperiodicity used below.

For countably many Borel subrelations R_i, with possibly smaller domains, R = * R_i means that their domains cover the domain of R, they generate R, and they have no nontrivial cyclically reduced alternating cycle. In such a cycle every edge is nonidentity and consecutive factor indices, including the last and first, differ. A subrelation may be extended by singleton classes off its domain. This convention does not grant permission to ignore nontrivial positive-measure pieces.

The decomposition is inessential when there is a Borel complete section U for R, partitioned as U = disjoint union U_i into R restricted to U invariant sets, with R restricted to U_i equal to R_i restricted to U_i. All these requirements hold after discarding an invariant null set. A complete section meets every remaining R-class; it need not have full measure. R is FI when every such decomposition is inessential. In particular, slicing along invariant pieces, or retaining R on a complete section and adding a smooth treeable connector with that section as transversal, is not an essential decomposition. Smooth/finite connector pieces are allowed. Neither an ordinary abstract-group splitting criterion nor the mere display of two factors is an adequate FI test.

For aperiodic p.m.p. relations, testing binary decompositions suffices [AG, Proposition 4.8]. Restrictions to complete sections preserve FI in both directions [AG, Propositions 4.10–4.11]. These facts are used with precisely their measured meanings.

## Primary sources and exact interfaces

1. **OWR**: Aurélien Alvarez, report in *Von Neumann Algebras and Ergodic Theory of Group Actions*, Oberwolfach Report 49/2008, pp. 2767–2770. The ambient space convention is on p. 2767; Definition 3 and Question 4 are on p. 2768. https://ems.press/content/serial-article-files/46193
2. **AG**: Aurélien Alvarez and Damien Gaboriau, *Free products, orbit equivalence and measure equivalence rigidity*, Groups Geom. Dyn. 6 (2012), 53–82. Section 2.1 supplies the measured-space convention; Definitions 2.2, 4.1 and 4.5 supply the decomposition and FI definitions. Propositions 4.6–4.8, 4.10–4.13, Lemma 4.15 and Corollary 4.20 are the imported interfaces. Question 4.16 is the exact target. https://ems.press/content/serial-article-files/29614 ; https://arxiv.org/abs/0806.2788
3. **FAQ**: Gaboriau's author FAQ lists [AG, Question 4.16] and separately lists treeability/action dependence and positive-Betti MFI questions. It is a historical identification aid, not evidence of a 2026 status update. https://perso.ens-lyon.fr/gaboriau/Travaux-Publi/FAQ.pdf
4. **TW**: Robin Tucker-Drob and Konrad Wróbel, *Measurable splittings and the measured group theoretic structure of wreath products*, arXiv:2410.11754v3, 21 November 2024, Section 5, pp. 16–18. Lemma 5.1 in **v3 requires ergodicity**, in addition to the p.m.p., nowhere-amenable and essential-splitting hypotheses. It supplies a full-domain aperiodic amenable free factor. Proposition 5.3 verifies essentiality when both full-domain factors have only nontrivial classes. Proposition 5.4 concerns existence of some non-FI action and measure equivalence; it does not assert existence of an FI action of the same group. https://arxiv.org/abs/2410.11754v3
5. **CGMT**: Clinton T. Conley, Damien Gaboriau, Andrew S. Marks and Robin D. Tucker-Drob, *One-ended spanning subforests and treeability of groups*, arXiv:2104.07431v3, submitted 19 March 2026; manuscript date 12 March 2026. Theorems 1–2 and 11, Corollary 4.2 and Theorem 4.4 exclude the surface, finitely generated elementarily free and planar-Cayley candidates through strong measured treeability. https://arxiv.org/abs/2104.07431v3
6. **PS**: Jesse Peterson and Thomas Sinclair, *On cocycle superrigidity for Gaussian actions*, Ergodic Theory Dynam. Systems 32 (2012), 249–272, Corollary 1.2, p. 250. Positive first L2-Betti number prevents U_fin-cocycle superrigidity of the Bernoulli shift. This is not a theorem ruling out Z-cocycle superrigidity of every action. https://math.vanderbilt.edu/peters10/petersonsinclair.pdf ; https://arxiv.org/abs/0910.3958

The old v2 HTML for TW omits the ergodicity hypothesis in Lemma 5.1. It was superseded here by the retrieved v3 PDF. No deduction below uses the stronger v2 formulation.

## Readiness exclusions, not a solution

- Every free action of a finite group has a finite relation, hence is FI. A finite group cannot witness the target.
- Every free p.m.p. action of an infinite amenable group is hyperfinite and aperiodic, hence non-FI by [AG, Proposition 4.6 and Corollary 4.7].
- For a nonamenable group with beta_1^(2) = 0, every free p.m.p. action is FI [AG, Corollary 4.20]. Thus a witness must be nonamenable with beta_1^(2) > 0, allowing infinity.
- If an infinite group is strongly treeable, every free p.m.p. orbit relation is aperiodic and treeable. [AG, Proposition 4.6] then gives an **essential measured decomposition**, not merely a graphing. Therefore none of its free p.m.p. actions is FI. This excludes the cited CGMT classes. Finite members are handled by the first bullet, not by this aperiodic argument.
- Ordinary one-endedness does not replace measured FI. The surface-group example is now an all-actions non-FI example in this category, not a mixed pair.

A bounded search on 8–9 October 2026 located no full example or impossibility theorem for the exact target. Newly located primary leads were checked before the constructions that use them. The inherited screening gate recorded no same-target substantive attempt, and the supplemental local scan of the new paper identifiers found none. This is neither exhaustive novelty certification nor a claim that current openness has been proved.
