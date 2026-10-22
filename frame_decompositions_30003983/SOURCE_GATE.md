# Source gate: decomposition of equiangular tight frames

Checked 21 October 2026. Ordered queue row 1833; catalogue ID 30003983; source key OWR-16629-009.

## Verdict

**Original question recovered; no complete general classification verified.** The task concerns partitions of the existing frame vectors into ETFs for their individual spans. Neither decomposition of a signal nor replacement/completion of missing frame vectors is the target. The source already gives two-block and three-block results and examples. A proof of those special cases, an exhaustive subset test for a supplied finite matrix, or a single positive/negative example is not a solution of the general classification problem.

## Primary provenance

Alex Fink, Emily King, Cynthia Vinzant, and Shayne Waldron, *Decomposing (equiangular) tight frames into (equiangular) tight frames for their spans*, printed pp. 2797–2799 of *Mini-Workshop: Algebraic, Geometric, and Combinatorial Methods in Frame Theory*, Oberwolfach Report 46/2018, DOI 10.4171/OWR/2018/46. Workshop: 30 September–6 October 2018. [Publisher record](https://ems.press/journals/owr/articles/16629), [publisher PDF](https://ems.press/content/serial-article-files/46766), [author manuscript](https://www.math.colostate.edu/~king/publications/OWR_2018_46.pdf).

Question 2 is on printed p. 2797 (PDF p. 29). The author manuscript numbers it Question 0.2. Both versions were retrieved and their definitions and question compared. The theorem and examples on printed p. 2798 were also visually inspected to check fractions and subscripts. The report date is 2018, not a newly published 2026 problem; search-index crawl dates are not publication dates.

## Faithful mathematical formulation

Let Φ=(φ₁,…,φₙ)∈C^(d×n), with unit columns, ΦΦ*=AI_d for some A>0, and |〈φᵢ,φⱼ〉|=λ≥0 whenever i≠j. Determine when there is a partition of {1,…,n} into nonempty sets I₁,…,I_k, other than the one-block and all-singleton partitions, such that, writing Ψ_j=Φ[:,I_j],

(Ψ_j Ψ_j*)² = α_j Ψ_j Ψ_j*, with α_j>0.

Equivalently Ψ_j Ψ_j*=α_j P_j, where P_j is the orthogonal projection onto the span of its columns. Every block inherits the original unit norms and equiangularity. Thus the substantive block test is tightness on its span, not tightness on the full original ambient space. The original Question 2 also asks the analogous question for general tight frames; the catalogue selects its equiangular branch. It is naturally a classification question about the given frame, not an assertion that every ETF admits such a partition.

The source identifies the two extreme partitions as trivial. It does not additionally forbid singleton blocks mixed with larger blocks, require equal block sizes, require orthogonal block spans, or introduce a definition of irreducible or nested decomposition. Those cannot be silently imposed. Partitions concern column indices, with no rescaling, projection, substitution, or duplication of vectors.

## What is already in the report

Proposition 3: a two-block tight-for-span partition of a tight frame has either orthogonal spans or two full spans. Its ETF conclusion states that the full frame is an orthonormal basis. Theorem 4 also treats three blocks, under a stated exclusion of a two-full-span decomposition. Beyond the orthonormal case its ETF parameter alternatives are:

- n ≡ 9 (mod 12), d=(n+3)/4, and each block has n/3 columns and rank (n+3)/6.
- n ≡ 3 (mod 12), d=(n+1)/2, and each block has n/3 columns and rank (n+1)/4.

The report supplies examples (n,d)=(9,3) and (15,8). It names higher-order and nested partitions, frame dualities, and infinite constructions as continuing research. Its general-tight-frame three-block classification is also present, but the proof is only attributed to honeycombs and the Welch bound; this gate is not a proof audit of that classification.

### Literal-hypothesis caution

The displayed definition does not explicitly assume d≥2 or distinct projective lines. In d=1, any list of unit complex scalars is an ETF with λ=1; every nonempty sublist is tight. For n≥3 it has nontrivial partitions and is not an orthonormal basis. Consequently the printed two-block ETF conclusion needs a nondegeneracy convention or an explicit rank-one exception. This observation is an elementary scope correction, not a resolution of the higher-dimensional problem. A subsequent mathematical audit must state its convention rather than assert the unqualified printed result.

## Literature boundary

1. Fickus–Jasper–King–Mixon, [*Equiangular tight frames that contain regular simplices*](https://arxiv.org/abs/1711.07081), Linear Algebra Appl. 555 (2018), 98–138. Section 6 studies ETFs partitioning into regular simplices and their associated equichordal tight fusion frames; Section 7 includes harmonic examples. It is cited by the OWR report and is prior knowledge, not a later general solution. Its simplex-block partitions require n divisible by s+1, where s is the inverse coherence. A binder records simplex subsets, not all possible ETF-for-span subsets.

2. Fickus–Schmitt, [*Harmonic equiangular tight frames comprised of regular simplices*](https://arxiv.org/abs/1903.09177), 2019. This advances harmonic simplex partitions: coset constructions, equi-isoclinic criteria and infinite families. Abstract, introduction and partition-related passages were inspected. It is not a classification of arbitrary ETFs or arbitrary-rank ETF blocks.

3. Fickus–Iverson–Jasper–King, [*Grassmannian codes from paired difference sets*](https://arxiv.org/abs/2010.06639), 2020 preprint/2021 journal work. Introduction and relevant constructions distinguish overlapping embedded ETFs from disjoint partitions. Paired difference sets yield many overlapping copies of smaller ETFs whose spans form fusion frames. These results do not automatically give a disjoint partition. The paper also identifies remaining questions about paired difference sets.

4. Fickus–Lake, [*Doubly transitive equiangular tight frames that contain regular simplices*](https://arxiv.org/abs/2302.08879), 2023 preprint with 2025 revision/journal publication. The introduction and Remark 4.7 were inspected. It characterizes binders in several highly symmetric families and explicitly corrects a prior Gabor–Steiner binder conjecture. Resolving those binder questions does not resolve the unrestricted OWR partition classification.

5. [King's current publication list](https://www.math.colostate.edu/~king/publications.html) was screened through listed 2026 work. No general resolution of this precise problem was identified. The recent paper *Completion of Equiangular Tight Frames via QR Decomposition* concerns replacing missing simplex-frame vectors and is not a partition result.

Searches used the original title, all four source authors, and combinations of ETF with decomposition, partitions, binders, and recent years. The finding is bounded: **no complete resolution verified in the inspected primary sources**, not a proof that none exists and not a newly verified author declaration of present-day openness.

## Evidence handling

Only authored analysis and public verification metadata are distributed. Copied source documents, extracted text, catalogue contents and coordination materials are not included.
