# Bounded priority audit: direct powers and mixed products

Checkpoint: **2026-10-24 17:58 UTC**. Completion estimate: **100% of the assigned bounded search**, not a certification of novelty or an estimate of the proof's correctness. No outreach, Git operations, publication, or release was performed.

## Question and conclusion

The target prior-art claim is: for every integer `n >= 1`, any finite group with the same **multiset** of irreducible complex character degrees as `A5^n` is isomorphic to `A5^n`. A later extension of this audit asks the corresponding question for `A5^r × PSL2(7)^s`, with arbitrary nonnegative `r,s`.

**No arbitrary-exponent recognition theorem for either target was located in this bounded search.** The strongest directly checked matching publication for homogeneous `A5` powers explicitly restricts the exponent to at most five. This is a failure to locate prior art, not proof that none exists. The mixed-family search is less conclusive than the homogeneous search.

Notation matters: `cd(G)` in the checked papers is a **set**, forgetting multiplicities. Complex group algebra recognition concerns the **multiset**. Equality of multisets supplies the order through the sum of squared degrees. Therefore an order-plus-degree-existence theorem can imply multiset recognition without proving recognition from the degree set alone.

## Primary sources checked

1. **M. Baniasad Azad and B. Khosravi, “Recognition of some characteristically simple groups by their complex group algebras,” Mathematical Reports 22(72), no. 1 (2020), 1–10.** [Original journal PDF](https://imar.ro/journals/Mathematical_Reports/Pdfs/2020/1/1.pdf).

   Theorem 8 (printed p. 5) characterizes `A5^α` by `|G|=60^α` and `5^α in cd(G)` under the explicit assumption `α <= 5`. Corollary 15 (p. 8) gives complex group algebra recognition for those powers. Its parallel `PSL2(7)` result restricts the exponent to at most seven. These statements neither cover arbitrary exponents nor mixed products. The introduction identifies earlier direct-square and Suzuki-product work; references were inspected for relevant predecessors. Local PDF and extracted text: `azad_khosravi_2020.pdf`, `.txt`.

2. **M. Baniasad Azad and B. Khosravi, “Recognition of M × M by Its Complex Group Algebra Where M Is a Simple K3-Group,” Mathematics 6, no. 7 (2018), 107.** [DOI](https://doi.org/10.3390/math6070107); [publisher PDF](https://mdpi-res.com/d_attachment/mathematics/mathematics-06-00107/article_deploy/mathematics-06-00107.pdf).

   Theorem 1 characterizes exactly `A5 × A5` using order `60^2` and existence of degree `25`. Corollary 2 covers the direct square of each simple group whose order has exactly three prime divisors. This is exponent two, with identical factors. Lemma 6 reproduces a predecessor's characterization of `PSL2(p) × PSL2(p)` for prime `p >= 5`; that predecessor is B. Khosravi, B. Khosravi, B. Khosravi and Z. Momen, J. Algebra Appl. 16 (2017), 1750036, [DOI](https://doi.org/10.1142/S0219498817500360). The 2017 full text itself was not accessed. Local 2018 PDF and text: `azad_khosravi_2018.pdf`, `.txt`.

3. **M. Khademi and B. Khosravi, “Recognition of characteristically simple group A5 × A5 by character degree graph and order,” Czechoslovak Mathematical Journal 68 (143) (2018), 1149–1157.** [DOI](https://doi.org/10.21136/CMJ.2018.0134-17); [original journal PDF](https://cmjpapers.math.cas.cz/full/68/4/cmj68_4_20.pdf).

   Theorem 2.1 characterizes exactly `A5 × A5` by order `3600` and its character degree graph. The remark on p. 1155 deduces complex group algebra recognition. This is neither a powers theorem nor a mixed-product theorem. Local PDF and text: `khademi_khosravi_2018.pdf`, `.txt`.

## Relevant leads and exclusions

- **K. Aziziheris, “Degrees of irreducible representations of direct products of nonabelian simple groups,” RACSAM 114 (2020), [DOI](https://doi.org/10.1007/s13398-020-00799-2).** The primary publisher endpoint was inaccessible. The indexed author abstract reports only that equal degree **sets** force a group to be quasi-perfect, for a specified list of homogeneous simple powers; its list excludes `A5` and `PSL2(7)`. Consequently this is an unverified bibliographic lead, not evidence for target recognition.
- **M. Baniasad Azad and B. Khosravi, “Complex group algebras of the direct product of non-isomorphic Suzuki groups,” J. Algebra Appl. 19(2) (2020), 2050036, [DOI](https://doi.org/10.1142/S021949882050036X).** The author/publisher-formatted text indexed online states a result for pairwise distinct Suzuki parameters. It does not include the target factors. The 2020 primary journal paper above independently identifies this predecessor's scope.
- **H. Rashidi and L. Oftadeh, “Recognition of the direct products of Suzuki groups by their complex group algebras,” J. Mahani Math. Res. Cent. 12(1) (2023), 127–135, [DOI](https://doi.org/10.22103/jmmr.2022.19218.1226).** Author-uploaded paper text reports homogeneous Suzuki powers with a bounded exponent depending on primitive prime divisors. It supplies no target result.
- Theorems recognizing **simple** or **quasisimple** groups by their complex group algebras do not automatically recognize their arbitrary direct products. No such transfer theorem was found.

## Search log and exact residual gap

Search families used original-title searches and combinations of `direct power(s)`, `characteristically simple`, `complex group algebra(s)`, `character degrees`, `multiset`, `multiplicities`, `A5`, `A_5`, `PSL2(7)`, `PSL(2,7)`, and `L2(7)`. Additional searches covered non-isomorphic simple direct products and later literature from 2021 onward. The original 2020 bibliography, the original 2018 square paper, and the 2018 graph paper were checked directly. Search results concerning spectra, conjugacy class sizes, or codegrees were excluded as different invariants.

The residual priority gap is an all-exponent theorem possibly buried in an older classification/character-theory source, an unpublished note, or poorly indexed literature. An elementary new proof would still need to be described as independently verified with priority unresolved until that gap is narrowed. The current audit supplies no evidence against the proposed proof; it is a literature-scope audit only.
