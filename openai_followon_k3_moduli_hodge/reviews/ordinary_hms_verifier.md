# Independent ordinary HMS and generation audit

Completed 2026-10-07 04:51 UTC (2026-10-06 21:51 PDT). Assigned scope: the ordinary quartic and torus mirror inputs, their applicability to the fixed test objects, and the generation statements used by the October 4 mixed-K3 manuscript. This is an independent narrow falsification review, not a review of the new moduli-space package or a certification of the immersed analytic construction.

**Verdict:** no material gap found in this assigned scope. The ordinary mirror inputs actually apply to the stated test systems. The torus fullness and generation conclusions are additional arguments in the source, rather than stronger conclusions falsely attributed to Abouzaid's faithful-functor theorem. Completion estimate for this assigned audit: 100%; this percentage does not estimate proof completion for the whole research program.

## Sources and reproducible locations

Upstream is the read-only copy pinned to `adc7f1241b42e322a6451854ab7e4b4c146bf78a`. Paths below are relative to `sources/pinned/preprints/The-rational-Hodge-conjecture-for-products-of-K3-surfaces-October-4-2026/build/manuscript/`.

- `setup.tex`, especially lines 14–61, 112–137, 161–185, 190–262, and 267–318.
- `comparison.tex`, especially lines 14–72 and 189–253.
- `realization.tex`, especially lines 119–172. I read the finite-comparison and copy-telescope context but did not independently reconstruct the analytical product comparison.
- [Seidel, arXiv:math/0310414v4](https://arxiv.org/pdf/math/0310414): Theorem 1.3, Section 8c (Lemma 8.4 and definitions of the projective category), Lemma 8.14, Corollary 9.6, Lemma 11.4, Proposition 11.6 and Corollary 11.7, together with the dg models in Section 5 and Corollary 10.15. Primary PDF inspected directly; theorem numbers in the upstream bibliography explicitly refer to this arXiv version.
- [Abouzaid, JEMS 19 (2017), 2139–2217](https://ems.press/content/serial-article-files/32222): Section 2.4, Theorem 2.10 (p. 2153), and Appendix A (pp. 2211–2215). Primary published PDF inspected directly.

Primary cached copies and extracted text are in `checks/package_review_1/ordinary_hms/`; they are review evidence, not proposed redistribution material.

SHA-256 identifiers:

| Item | SHA-256 |
|---|---|
| `setup.tex` | `f5d66939d1eea98d1d2172f0c73746d32bd60f313cae0373879d091a1632e850` |
| `comparison.tex` | `f6e817648b5866991cff23b7e90643c00d8924f85f8d5e0128643f90ae148be2` |
| `realization.tex` | `338c65d26d9cade6acffc202127697f51af84853a19a2506daf1489080f9ef8d` |
| Seidel v4 PDF | `2932bac3c07c123118b0da104508a4118d89f2212e358438f5cf609c231a8da8` |
| Abouzaid published PDF | `1dc9b9b6bb468b3ff3b6a3a36f2dd16161bcb23181a6c99c40902f4f133cd21a` |

## Quartic input

1. Seidel's input is any smooth quartic in projective three-space with the standard symplectic form. Thus it is not restricted to a special quartic complex structure on the A side. Normalizing the integral hyperplane form rescales the Novikov parameter. The mirror reparametrization is explicitly included in the definition of the B-side quartic in `setup.tex:29–35`.

2. The primary theorem is stated as a triangulated equivalence, but its proof compares generating enhanced categories through quasi-isomorphisms: the full 64-sphere A∞ subcategory is deformed and identified with the algebraic dg model, and split closure gives the equivalence. It therefore supplies the enhanced comparison the argument requires. This is not an attempt to upgrade an arbitrary abstract triangulated equivalence to an enhanced one without evidence.

3. Vanishing-sphere split generation is real content of Seidel's Corollary 9.6 and Lemma 11.4. The latter specifically applies it to the quartic pencil and the full 64-object category. The cited proof does not merely establish a directed exceptional category and silently identify that with the whole closed Fukaya category.

4. The extra vanishing cycles in a generic quartic pencil can be added to the already generating system. The vanishing-cycle span is the primitive kernel of the ambient degree-two map; for a quartic this is the hyperplane orthogonal complement, of dimension 21. Adding such tests does not sacrifice generation, and all spheres have zero first cohomology and thus satisfy the rational-brane holonomy requirement.

5. Seidel's Section 8c explicitly uses branes with an almost complex structure excluding disks and spheres. Lemma 8.4 derives density from unmarked dimensions −1 for graded disks and −2 for spheres, with the disk decomposition theorem treating non-simple disks. Applying the residual genericity argument to countably many fixed sphere copies remains a countable intersection. The source's fixed `J_0` choice is therefore compatible with the ordinary quartic category. Lemma 8.14 supplies Hamiltonian-copy invariance for graded spheres, including different permitted disk-excluding data.

6. The algebraic Mukai-space isometry in `setup.tex:161–185` passes the dimension and relation tests. Preserved Euler forms give an injective 21-dimensional Gram subspace. The mirror quotient family has nonconstant period; the Fermat Jacobian-ring test uses the surviving product monomial and the symplectic quotient preserves its period variation. Hence its geometric generic Picard rank is at most 19. The 21-dimensional lower bound forces equality, and the preserved Gram form then makes linear relations descend. This avoids simply assuming a cohomological mirror transform on transcendental classes.

## Torus input and additional arguments

1. Abouzaid's actual theorem is a finite-object faithful A∞ functor. The source accurately states that weaker conclusion at `setup.tex:190–193`, and supplies its own fullness calculation. No assumed HMS theorem for arbitrary high-dimensional tori or infinite collections is needed here.

2. All its stated hypotheses are met. The torus fibration is closed and nonsingular; its base and total space have zero second homotopy. The graph map on fundamental groups is injective, so the relative second homotopy group vanishes and each graph and Hamiltonian copy is tautologically unobstructed. Their constant-plane phases admit integer lifts, their tangent bundles are framed and spin, and the background class is zero. The zero section and the global base frame remove the section and spin gerbe twists. These are precisely the ordinary finite graph systems used before the subsequent ultraproduct.

3. The line-bundle identification has the needed content. A section meets each fiber once, so its local family complex has rank one in a single degree. Transport around a base vector `b` shifts the lifted graph's fiber coordinate by `Mb`; hence the exponent vector of the period multiplier is `−εMb`. Scalar corrections change only its Picard-zero part. Integral symmetric matrices decompose into signed rank-one matrices: diagonal terms use `e_i e_i^t`, and an off-diagonal pair uses `(e_i+e_j)(e_i+e_j)^t−e_i e_i^t−e_j e_j^t`. Pullbacks of theta lines under the corresponding sum maps therefore yield exactly the stated numerical class. This handles off-diagonal slopes, not merely diagonal ones.

4. Fullness follows on every needed pair from faithfulness plus equality of dimensions. A definite slope difference has `|det(M−M')|` Floer generators in one degree; the corresponding line quotient is ample or anti-ample with the same total Ext dimension. For copies of a single slope, Floer cohomology is the full exterior cohomology of the torus. A nontrivial Picard-zero quotient has no cohomology and is incompatible with faithfulness. The copies' lines therefore agree, and the self-Ext dimensions agree. The ordering restriction matters: this argument is not presented as fullness for arbitrary indefinite pairs.

5. The common-shift argument survives the three-object test. Orient the definite graph arrows in degree zero. If the numerical sign made every ordered quotient anti-ample, a degree-zero image would require the same nonzero relative shift `g` for each of the three ordered pairs. Such shift differences cannot be additive. Thus the ample sign is forced and shifts agree. Extreme scalar slopes compare every additional test to this common normalization.

6. The strong uniform generation quantifier in `setup.tex:269–301` is supported by its proof. Over the proper product of Picard-zero parameter spaces, relative Serre generation and vanishing give evaluation surjections with uniform successively increasing exponents. The kernels are vector bundles. A length `g+1` sequence expresses a vector-bundle generator as a summand of the resulting complex because `Ext^{g+1}` from a vector bundle vanishes on the smooth `g`-fold. The argument works for arbitrary choices of the individual Picard-zero twists, not just a specially tuned tuple. Duality handles the alternative common sign.

7. Adding graph tests while retaining definite order is valid. Integer symmetric matrices beyond any fixed matrix form a Zariski-dense set, so a finite polynomial-evaluation span can be attained by successive choices in that cone. This does not require adding incomparable slopes, which would invalidate the preceding fullness proof.

## Generation of the mirror product and exact limitations

The statement at `realization.tex:164–172` concerns external products of generators in the two algebraic perfect categories. On smooth projective varieties these products generate the product category, and this persists under algebraically closed field extension by the perfect-diagonal criterion. This is sufficient after the source's directed-copy comparison has identified the full test hull; it does not require an unproved blanket HMS theorem for the symplectic product.

I found no mismatch between the primary ordinary theorems and the quantifiers used here. This verdict remains conditional on the separately reviewed assertions that the immersed category exists with the claimed pairing, that its directed sector compares to the ordinary product test category, and that the copy reconstruction and projection are legitimate. Those central analytical/categorical statements are new work in the upstream source; a clean ordinary-HMS audit alone does not prove them. I have not promoted any whole-package result or checked publication metadata, source archives, or final PDFs.
