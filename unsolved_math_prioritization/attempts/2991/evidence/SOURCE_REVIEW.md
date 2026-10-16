# Independent source and mathematical audit: Approaches 3 and 4

Audit date: 2026-10-08 UTC.

Reviewed artifact: `REPORT.md`, SHA-256 `db97c3883cf11867655b8709e03df25deabb026a0224e9cd551570059ee4463f`.

## Verdict

**Pass within the report's stated scope.** No mathematical error or missing hypothesis affecting Approaches 3 or 4 was found. The relative source yields the stated pair; self-doubling yields closed `(5,1)` trisections of `S^2 x S^2`; inequivalence is proved only with the designated half and ordered sectors retained. The integral graph classification is correct, and its intersection-form application has one fixed sign convention rather than an independently selectable sign for each trisection.

These checks do not establish unmarked inequivalence of the doubles, inequivalence of any K3 diagrams, or a solution to part (b).

## Approach 3: relative input, ordinary doubles, and marking

### Source input and hypotheses

Takahashi, *Non-diffeomorphic minimal genus relative trisections of the same 4-manifold*, arXiv:2406.03113v1:

- Definition 2.1, printed/PDF page 4, uses sector-preserving diffeomorphism as the relevant equivalence.
- Lemma 4.1, page 8, identifies the two Figure 8 diagrams as relative `(2,1;0,2)` diagrams of `S^2 x D^2` and distinguishes them by the closed diagrams obtained by capping the central surface. Figures 9 and 10 are on page 9.
- Theorem 4.3, page 10, supplies the two non-diffeomorphic minimal-genus relative trisections and the common annular boundary open book with identity monodromy.

Thus the report's weaker wording, equivalent boundary open books, is justified. The capping obstruction is parity of the two standard closed intersection forms: the hyperbolic form of `S^2 x S^2` is even, whereas that of `CP^2 # (-CP^2)` is odd. Those capped manifolds are different; they cannot be substituted for two closed trisections on the same manifold. This is exactly the distinction the report preserves. [Primary source](https://arxiv.org/abs/2406.03113v1).

Castro–Ozbagci, *Trisections of 4-manifolds via Lefschetz fibrations*, arXiv:1705.09854v2:

- Lemma 2.7, page 9, requires nonempty connected boundaries and an orientation-reversing boundary identification compatible with the boundary open books.
- Its proof on page 9 constructs the closed sectors by gluing corresponding relative sectors.
- Corollary 2.8 and its proof, page 11, specialize to the identity identification with the oppositely oriented copy. They give `(G,K)=(2g+b-1,2k-2p-b+1)`.

Here the boundary is the connected nonempty manifold `S^2 x S^1`, so the hypothesis omitted from the report's short general paraphrase is satisfied in the application. The identity is orientation-reversing between the induced orientations on the two boundary copies and is compatible with their open books in the corollary's sense. No independent boundary-extension or monodromy assumption is missing. [Primary source](https://arxiv.org/abs/1705.09854v2).

### Independent deductions

Each construction doubles its own relative trisection. It does not glue the first relative trisection to the second. Consequently the agreement of the two boundary open books is a valid source fact but is not an additional prerequisite for these two separate self-doubles.

With `g=2, k=1, p=0, b=2`, the formula gives `G=5` and `K=1`. The underlying gluing map is the identity on `S^2 x S^1`; therefore the product description identifies the oriented ordinary double with `S^2 x S^2`. This conclusion uses the actual gluing description, not classification by Euler characteristic or intersection form. The consistency equation is `2+G-3K=4`.

For complete clarity, write the doubled sectors as `Z_i^(r)` and their designated positive halves as `W_+^(r)`, for `r=0,1`. By the gluing construction,

    Z_i^(r) intersect W_+^(r) = W_i^(r).

If a diffeomorphism `f` maps `Z_i^(0)` to `Z_i^(1)` for every fixed label `i` and maps `W_+^(0)` to `W_+^(1)`, then its restriction satisfies

    f|W_+ : W_i^(0) -> W_i^(1).

The restriction is a diffeomorphism of the original relative trisections. With the induced orientations it remains orientation-preserving. This contradicts Takahashi's result. Standard compatible collars and corner rounding do not change this sector-intersection argument.

The positive-half designation is essential to the argument as written. Preserving only the seam could allow exchanging the halves; an unmarked diffeomorphism need not preserve the seam at all. The report expressly retains the positive half and labels, and expressly declines any seam-recovery assertion. Therefore the marked conclusion is rigorous without an extra claim about unmarked trisections or label permutations.

## Approach 4: integral graph classification

### Independent algebraic check

All modules and operations in the argument are integral.

1. With `H=A direct_sum B` and both summands Lagrangian, the alternating form has blocks `[[0,D],[-D^t,0]]`. Its unimodularity forces `det(D)=+1` or `-1`. Thus dual integral bases can be chosen, giving `omega(a_i,b_j)=delta_ij`.
2. Because `H=A direct_sum C`, projection along `A` identifies `C` with `B` as free abelian groups, not merely over the rationals. Hence `C` is the graph `(Sx,x)` of an integer matrix.
3. Evaluating the alternating form on `(Sx,x)` and `(Sy,y)` gives `x^t(S^t-S)y`; isotropy is exactly symmetry of `S`.
4. Complementarity of `B` and `C` is equivalent to the first-coordinate projection from `C` onto `A` being an integral isomorphism. Hence `S` is unimodular.
5. A symplectic automorphism preserving both ordered coordinate summands is precisely `diag(P,P^{-t})`, with `P` integral unimodular. It sends the graph matrix to `P S P^t`. Conversely every such congruence is realized by this automorphism.

Thus integral congruence, rather than rational congruence or equality of signatures, is the exact classification of these ordered triples. No parity restriction or definiteness hypothesis is needed.

### Application to efficient trisections

For a `(g,0)` trisection, every pair of three-dimensional handlebodies gives a Heegaard splitting of `S^3`. Its integral first homology is the quotient of `H_1(Sigma;Z)` by the sum of the corresponding disk-system kernels. The quotient is zero; the sum is therefore all of `H`. Both kernels have rank `g`, so their intersection is zero and the sum is an integral direct sum. This proves the pairwise-complementarity hypothesis required by the algebraic theorem.

Feller–Klug–Schirmer–Zemke, *Calculating the homology and intersection form of a 4-manifold from a trisection diagram*, arXiv:1711.04762v2, give the relevant integral pairing in Definition 3.5 and Theorem 3.6, page 9. Corollary 3.3, pages 8–9, supplies the homology identification; Formula (1.2), page 2, is a symmetric formulation. Proposition 4.3 and Theorem 4.4, page 12, give the matrix calculation and the stronger diagram normalization. [Primary source](https://arxiv.org/abs/1711.04762v2).

In the graph coordinates, the quotient in Theorem 3.6 is simply `C`: pairwise intersections vanish and `A+B=H`. For `c(x)=(Sx,x)`, its `A`-component is `(Sx,0)`, and the source pairing becomes

    omega((Sx,0),(Sy,y)) = x^t S y.

Thus, under this explicit identification of the three source Lagrangians with `A,B,C`, the matrix is exactly `S`. Changing the global surface/sector orientation convention can replace every such matrix by `-S`; it does not permit a separate sign choice for each trisection of a fixed oriented manifold. The report's fixed-overall-sign formulation is therefore sufficient.

Two efficient trisections of the same oriented `X` consequently produce matrices integrally congruent to the same fixed intersection form, or its same globally chosen negative. The graph classification makes their ordered integral Lagrangian triples symplectically isomorphic. This proves only the claimed collapse of this unmarked homological invariant. It does not classify curves or diagrams, and does not apply the pairwise-complementary argument to the non-efficient `(5,1)` doubles.

Feller–Klug–Schirmer–Zemke Theorem 4.4 actually applies to `(g;0,k_2,0)` trisections; the efficient case is a specialization. Accordingly, the report's attribution to a result of greater scope is accurate.

### Torelli caution

Lambert-Cole, *Trisections, intersection forms and the Torelli group*, arXiv:1901.10834v1, Theorem 1.1 and Section 1.1, page 2, distinguishes a theorem relating existing suitable trisections from a claim that arbitrary new gluing data forms a trisection. The pseudotrisection discussion in Section 3.4 and Definition 3.13, page 9, makes the missing geometric condition explicit. Integral homology-sphere pairwise boundaries are not enough to certify the required `S^3` boundaries. No assertion that homologically trivial regluing preserves the smooth ambient manifold follows merely from the unchanged form. The report's caution is consistent with these sources. [Primary source](https://arxiv.org/abs/1901.10834v1).

## Reproducibility and source fingerprints

The four existing PDFs were independently rehashed; their byte counts and SHA-256 values exactly match `SOURCE_METADATA.json`. Each PDF was re-extracted with `pdftotext -layout`, and each regenerated text file was byte-for-byte identical to the text inspected in this audit. The public arXiv landing pages were checked on the audit date and confirm the titles and version records. No claim of fresh network-download byte equality is made.

| Primary source | Version | PDF bytes | PDF SHA-256 |
|---|---|---:|---|
| Takahashi | 2406.03113v1 | 213624 | `36eccb64ad9c2f0e231268afe460a2061d6fcc8bb415fb764e9b63b1ef73112e` |
| Castro–Ozbagci | 1705.09854v2 | 3174848 | `1b760b678ba324f0e4d15ae0c8808dc8b00340469c3b452764db04d61ba565d3` |
| Feller–Klug–Schirmer–Zemke | 1711.04762v2 | 385644 | `bef694cb4a225b15e217cebeeca6a210eb170c923fc42705fe47c19196a038f8` |
| Lambert-Cole | 1901.10834v1 | 422378 | `d72e66eed6f6c374101c64a56591b76bc08383a7f1c1c78621a8dd86899e13bc` |

Optional precision improvements, not required mathematical corrections: cite Feller–Klug–Schirmer–Zemke Definition 3.5/Theorem 3.6 directly beside the graph-pairing identification; label Castro–Ozbagci's inspected version explicitly as v2; include nonempty connected boundary in the abbreviated general doubling statement. All relevant hypotheses are already satisfied in the report's actual application.

This audit contains authored analysis and public verification metadata only. No source body, diagram, or source-file attachment is included. The original report and source files were not modified, and nothing was published.
