# A Catalan divisor of the forest transfer determinant

This theoretical edition gives a self-contained proof of the Teufl–Wagner determinant-divisibility statement for every integer n ≥ 1. If A = (a_ij) is the generic n × n matrix and T is the forest transfer matrix indexed by all set partitions, then

\[
(\det A)^{C_n}\mid\det T
\quad\text{in }\mathbb Z[a_{ij}],\qquad
C_n=\frac1{n+1}\binom{2n}{n}.
\]

The exact transfer convention is fixed in [PROOF.md](PROOF.md): one unweighted tree is chosen inside each input block, and each admissible interlayer edge set is counted once. Neither the partitions nor the forests are restricted to be planar or noncrossing. No symmetry or positivity hypothesis is imposed on A.

The proof identifies a constant Catalan-dimensional quotient of the full partition space, calculates its transfer determinant exactly, and lifts the resulting factor to the full determinant over the integer polynomial ring. It establishes a divisor. It does not claim exact multiplicity of det A or irreducibility of the remaining factor.

## Reading order

- [PROOF.md](PROOF.md): the complete reconstructed mathematical proof, with fixed signs, normalization, attribution and provenance.
- [AUDIT.md](AUDIT.md): the complete fresh independent AI mathematical audit of the identified proof bytes.
- [ACCEPTANCE.md](ACCEPTANCE.md) and [STATUS.json](STATUS.json): the precise review disposition, accepted scope and limitations.
- [ATTRIBUTION.md](ATTRIBUTION.md): the source and bounded priority review, including established CSS and Sportiello contributions.
- [SOURCE_CATALOGUE.json](SOURCE_CATALOGUE.json) and [SOURCE_PROVENANCE.json](SOURCE_PROVENANCE.json): public scholarly citations, raw public-source identities, inspection history and access limitations.
- [PROVENANCE.md](PROVENANCE.md): reconstruction and public-edition history.
- [MANIFEST.json](MANIFEST.json): the exact edition membership and byte identities of the other nine files.

## Source and review limits

The target is Problem 1 in Teufl and Wagner, [“A determinant related to set partitions,” Oberwolfach Reports 23/2018, pp. 1457–1458](https://ems.press/content/serial-article-files/46745). The exterior forest algebra and Catalan/noncrossing quotient belong to established prior work, including [Caracciolo–Sokal–Sportiello](https://arxiv.org/pdf/0706.1509v2) and [Sportiello’s thesis, Chapter 10](https://pcteserver.mi.infn.it/~caraccio/PhD/Sportiello.pdf). The reconstructed proof supplies its own invariant-spanning and dimension arguments; this does not create a novelty claim for the underlying ingredients.

The source review was bounded and does not certify novelty or current open status. The mathematical audit is an AI review, not human peer review or formal proof-assistant verification. Historical finite checks mentioned in the written audit are supplementary evidence; they do not prove the all-n statement.

The edition contains the full authored proof and audit, explanatory prose and public provenance metadata. It includes no checker code, standalone computational fixtures, execution-result files, third-party source documents or private coordination material.
