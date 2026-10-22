# Source gate: first barycentric shellability of convex complexes

Checked 21 October 2026. Queue row 1837; ID 30002123; source key OWR-12006-004.

## Verdict

The original target is recovered and is NOT resolved by the standard Adiprasito–Benedetti two-subdivision theorem. The general one-subdivision claim is explicitly conjectural in their inspected manuscript; no later complete resolution was verified in this bounded literature search. Preserve an open/unresolved classification, not “solved.” The low-dimensional cases are known.

## Original statement and provenance

For every finite simplicial complex C admitting a linear geometric realization with convex underlying space, is sd(C) shellable? Here sd means exactly ONE barycentric subdivision; dimension is unrestricted.

This is Benedetti's Problem 1, in Klaus Hildebrandt's collected open problems, printed p.2130 (PDF page 54), *Discrete Differential Geometry*, Oberwolfach Reports 9 (2012), no.3,2077–2137. [Official record](https://ems.press/journals/owr/articles/12006), [MFO PDF](https://publications.mfo.de/bitstream/handle/mfo/3305/OWR_2012_34.pdf?isAllowed=y&sequence=1), DOI 10.4171/OWR/2012/34. EMS dates publication 29 May 2013; 2012 is the report year. PDF page 54 was extracted and visually inspected.

The source glossary identifies convex complexes with linear triangulations of convex polytopes. The question is not about an arbitrary contractible complex, an arbitrary triangulated topological ball, a convex polytope's boundary, or existence of some shellable refinement. It uses ordinary ball shellability: facet prefixes are balls. The source's historical weaker bound is d+2 subdivisions, not its requested count.

## Mathematical scope audit

A finite geometric complex with convex d-dimensional support is a triangulation of that whole convex body, not merely a complex whose vertices have a convex hull. Purity follows: a lower-dimensional maximal simplex would have a relative-interior point with a neighborhood in the support lacking d-dimensional points, impossible for a convex d-body. Thus nonpure shellability is not an additional quantifier or escape route here. Ambient dimension k may exceed d; pass to the affine span.

The starting complex in the problem is simplicial. The comparison theorem permits the broader class of polytopal subdivisions. A derived subdivision inserts interior points by stellar subdivision over faces in decreasing dimension; barycentric subdivision uses barycenters. These choices give the same abstract face-chain complex. Since shellability is combinatorial, this terminology does not create a gap for the present question. Arbitrary stellar subdivisions are not interchangeable with ONE derived subdivision.

## Precisely inspected existing theorem

Adiprasito–Benedetti, *Subdivisions, shellability, and collapsibility of products*, [arXiv:1202.6606v3](https://arxiv.org/abs/1202.6606v3), 10 July 2013; [Combinatorica 37 (2017),1–30](https://doi.org/10.1007/s00493-016-3149-8), online 9 June 2016. Full-text inspection was of the 17-page arXiv manuscript, not the subscription journal PDF; the journal abstract confirms the same bounds.

- Theorem A and Corollary I.2.2: every polytopal subdivision C of a convex polytope satisfies shellability of sd²(C).
- Theorem I.2.4: for dimension at most three, sd(C) is shellable.
- Introduction, immediately after Theorem A: for dimensions at least four, the sufficient count is one or two, with one conjectured.
- Dimensions at most two already have shellable triangulated balls without subdivision. Rudin's nonshellable tetrahedron triangulation obstructs zero subdivisions in dimension three, not one.

## Collapsibility is not the missing shellability theorem

Adiprasito–Benedetti, *Barycentric Subdivisions of Convex Complexes are Collapsible*, Discrete & Computational Geometry 64 (2020),608–626, DOI [10.1007/s00454-019-00137-3](https://doi.org/10.1007/s00454-019-00137-3); [inspected journal manuscript](https://par.nsf.gov/servlets/purl/10169029). Theorem 4.5 proves sd(C) collapsible for any subdivision of a d-polytope. Section 4 still distinguishes the two-subdivision shellability result from the one-subdivision collapsibility result. Collapsibility alone cannot be substituted for shellability, so this paper does not close the original problem.

## Catalogue match and search limits

Fresh local hashing of the recovered corpus found exactly one problems.json match for ID 30002123 / OWR-12006-004 and no matching research_results entry. The queue row and source record agree with the primary problem; the dated catalogue assessment is not independent current-status evidence. These corpus files were reused locally, not freshly downloaded upstream.

Current searches targeted the exact title, source key, first barycentric/derived shellability, convex complexes, and later literature. Benedetti's current [publication list](https://www.math.miami.edu/~bruno/publications.html) was checked. The newly listed *Efficient Triangulations of Manifolds* PDF at https://hal.science/hal-05406668v1/file/ab.pdf returned an Anubis access-denied page; no content from it was inspected and no claim of exhaustive 2026 coverage is made. This bounded non-resolution finding is not proof that no later theorem exists.

SOURCE_METADATA.json and CORPUS_VERIFICATION.json record source URLs, hashes, byte counts, and inspection status. Copied sources and extracted corpus records remain private. No queue or GitHub writes were performed.
