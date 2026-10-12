# Independent review request

Review the complete immutable five-turn packet for 30003853, not only its final turn. Recommended original disposition: unsolved5/5. Author search has stopped. No full-target solution or historical novelty is claimed.

## Read and replay

Read SOURCE_GATE.md, FINAL_RESULT.md, TURN_1.md through TURN_5.md, all manifests and scripts. Public packet is defined by FINAL_AUTHOR_MANIFEST.json. Run `python REPLAY_ALL.py --source-dir /workspace/shared/math-30003853/sources`; omit the option in a clean public checkout. Source directory is local-only and is not to be published.

## Primary source anchors

- Original: sources/owr2018-26.pdf printed1624–1625, exact Q111 on1625; printed1625.png. https://ems.press/content/serial-article-files/46748 . Publisher records12April2019 publication of the2018 report.
- Splitting: sources/bieri-geoghegan-kochloukova2010.pdf, PDFp2 coefficient convention andp6 Theorem2.7 (bgk-p2.png and bgk-p6.png). R is any commutative ring with1!=0; H is FP_2(R), has no nonabelian free subgroup; character is nonzero discrete; conclusion is an ascending HNN decomposition over a finitely generated subgroup of the kernel. The theorem credits Bieri–Strebel1978TheoremA. That original archive returned verification HTML; no access challenge was solved. The actual dependency is the fully available BGK primary statement. https://arxiv.org/abs/0807.5138v1
- Solvable classification: sources/bleak2006-algebraic.pdf, pp2–3 Theorems1.1–1.2/Lemma1.3, p27Corollary4.8 (bleak-p2.png). Restricted wreath products and restricted sums, finite derived length. https://arxiv.org/abs/math/0602038v2
- Diagram homology: sources/guba-sapir2003.pdf p35Theorem9.9 (gs-p35.png). https://arxiv.org/abs/math/0301225v2
- Closedness: sources/golan2026.pdf Theorem2.13 p11–12, finite/full-core qualifiers of Theorem8.3/Corollary8.7; Farley source supplies separate known point-stabilizer classes. These are credited context, not an extension to all subgroups.
- One-bump germs: sources/kassabov-matucci.pdf pp9–10Corollary4.5/Lemma4.6 (km-p10.png). https://arxiv.org/abs/math/0607167v3 . The elementary proof is included; stronger cyclicity need not be assumed.

## Highest-risk proof obligations

1. T1: FP_2 coefficient scope, nonzero projection normalization, nontrivial HNN base when kernel nontrivial; finite-support contradiction. The Laurent derivative quotient must prove injectivity and cover negative exponents/m=1. The wreath embeddings use finite pieces per element.
2. T2: the general subdirect classification and its **self-normalizer** inside the product of simple factors; only then conclude H'=H intersect product(S_i). Finite-index projection implies containment of F′, not equality with F. Quotient torsion of a nonsaturated lattice must not be confused with torsion in the lattice itself.
3. T3: nonabelian lamp conjugation preserves the nonidentity support exactly. Keep H, not its possibly non-FP_2 images, as the splitting/induction domain. Both restricted-sum reductions use finite generation. Do not extend finite derived-length classification to arbitrary elementary amenable images.
4. T4: finite support-component list for a finitely generated normal subgroup, even if ambient H is not finitely generated; monotonicity forces each component fixed. Germ character at an interior possibly non-dyadic endpoint is valid. The contradiction requires ordinary, not normal, finite generation.
5. T5: unique roots use finite support components and one-bump germs; unequal signed powers use nonunit initial slope. Verify the integer model is exactly the finite presentation, its order cone, unique roots, balanced powers and abelianization. The examples are not embedded in F; their centralizer-based obstruction is essential. They disprove only an abstract surrogate argument.

All raw source bytes and screenshots remain local-only. Please preserve frozen author bytes; corrections, if required, should be identified precisely and added through the agreed correction workflow. Final WIP SHA/readback will be supplied separately after backup. No publication until parent gate.
