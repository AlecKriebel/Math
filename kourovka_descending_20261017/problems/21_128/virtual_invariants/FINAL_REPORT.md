# Kourovka 21.128 — virtual invariant family report

Outcome: **no complete resolution**. The accepted results below are elementary filters on proposed methods; neither a positive answer nor a negative answer was obtained. No originality claim, preprint, upload, Git action, or publication-tracker write was made by this family. Completion estimate toward finding a separating virtual invariant: **9%**, with substantial uncertainty. Completion of the original mathematical problem is unproved.

## Strongest verified deductions

1. Both pure central quotients Q_F and Q_H have an explicit epimorphism to F2, using an A2 subarrangement and a loop-transversality argument.
2. For every d-generated group L and every m≥max(1,d−1), each Q_T has a normal index-m subgroup retracting onto F_(m+1), hence surjecting onto L. The free basis is a^m and a^j b a^(−j), 0≤j<m. Inside every finite-index subgroup, further finite-index subgroups have free retracts of unbounded rank. Normality is asserted in the group where the cyclic kernel is taken, not in arbitrary finite overgroups.
3. Consequently both groups' virtual quotient-isomorphism spectra contain **all finitely generated groups**. Their virtual primitive cup-isotropic dimensions, rank-one characteristic-variety component dimensions and depths, free nilpotent quotient ranks, and free pro-p quotient ranks are unbounded. These qualitative existence tests cannot distinguish the pair.
4. Both Q_T have, for every m≥1, a normal finite-index subgroup V with an element of exact order m in Out(V). The explicit representative is induced by conjugation by a lift x of 1∈Z. Its element in Comm(Q_T) has **infinite** order. Thus order-five torsion in a virtual outer automorphism group must not be confused with order-five commensurator torsion.
5. A negative answer would follow if Comm(Q_F) had no order-five element. Such exclusion is equivalent here to excluding actual order-five automorphisms of all finite-index subgroups. No such uniform exclusion was proved. The full F4 central quotient's known torsion list does not bound its commensurator.

Full proofs and exact scope restrictions are in FREE_RETRACT_FILTER.md and OUTER_TORSION_FILTER.md. OTHER_ROUTES.md records the inspected cohomological, Malcev, representation, profinite, and virtual poly-free mechanisms and their exact remaining gaps.

## Reproducibility and source checks

Run `python3 check_schreier.py`. The standard-library program checks all reduced free words through length eight for every cyclic index m=1,…,64: **839,744** word/index checks, plus basis/inverse checks and exact covering-graph ranks. It exercises the explicit rewriting formula including m=1 and inverse a-edges. The universal theorem follows from the spanning-tree proof, not from this finite range. Results and the exact program hash are recorded in schreier_checks.json.

The primary Soroko paper was independently downloaded and checked for the torsion lists, pure central quotient properties, and the actual scope of its commensurator theorem. Brieskorn and Bestvina primary texts were downloaded to check the poly-free input rather than relying on a current search snippet. SOURCE_MANIFEST.json records bytes and SHA-256 hashes, including a rejected initial URL that returned a different article. That unrelated article is not used. No inaccessible mathematical database is represented as searched exhaustively.

## Adversarial self-checks and limitations

- Arrangement deletion is used only as an epimorphism; an infinite kernel is compatible with every argument here.
- Free quotient existence is kept distinct from arbitrary subgroup embeddings and faithful representations.
- The local-system inflation proof is given directly. No tangent-cone or 1-formality theorem for arbitrary covers is assumed.
- Rational Malcev completions are explicitly not assumed invariant under finite index.
- The commensurator realization lemma concerns actual finite-order automorphisms; cyclic deck actions in Out need not lift to finite-order automorphisms.
- The unique-root and trivial-center facts are essential to the exact outer-order and infinite commensurator-order calculation. Both are checked through established pure central quotient results.
- A finite test is not promoted to an arbitrary-index noncommensurability certificate.
- These are author self-checks; they are **not independent adversarial approval**. A fresh reviewer may audit the proofs, and no solved status is warranted by this report.

The original gap is unchanged: no isomorphic finite-index subgroups were constructed and no invariant preserved under every such isomorphism was shown to differ.
