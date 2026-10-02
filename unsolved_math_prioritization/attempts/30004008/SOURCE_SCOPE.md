# Source scope: 30004008 / OWR-16633-026

The full target is Yu Yokoi's question on printed p3018 of [OWR50/2018](https://ems.press/content/serial-article-files/46772), published in 2019. Write n=k+1. There are n-1 color classes, each a spanning directed tree with root indegree zero and every other indegree one. Parallel colored arcs are distinct elements. The output must be one connected spanning out-arborescence with exactly one arc from each class; its root is not prescribed. The n=1 empty instance is harmless, and research uses n≥2.

The current primary [Bérczi–Király–Yamaguchi–Yokoi v2](https://arxiv.org/abs/2412.15457v2), dated 2025-12-09, credits the conjecture to this OWR question. It proves several partial cases, including at most two multi-roots (vertices rooting multiple input trees), paths/stars and pseudotrees. It reports a computer verification through n=8. Its fixed-root NP-completeness theorem does not disprove arbitrary-root existence. The cycle preprint 2511.04953 was withdrawn because it was merged into this v2.

This attempt credits those results and distinguishes theorem, imported finite computation, and new finite controls. No complete resolution or novelty certification was found in the targeted literature checks. Full source inputs and read scope are bound in SOURCE_MANIFEST.json; copyrighted PDFs are not republished.
