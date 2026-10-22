# Source and status audit

Checked 5 October 2026 UTC. The exact problem is still posed as a conjecture on the maintained primary page. A bounded current-literature search did not find a general resolution. That is a qualified search result, not proof that no resolution exists anywhere.

## Primary statement

[TOPP Problem 31](https://topp.openproblem.net/p31) was retrieved directly. Its statement, after stripping its inline emphasis, is byte-identical to the imported statement and matches the catalog statement hash. The conventions are a finite set of two-sided planar open segments with disjoint closures and trapping defined by containment in their convex hull. The task concerns every emitted direction, not a positive-measure set or finitely many selected rays. The source does not separately forbid a source at a segment endpoint.

The assigned [UnsolvedMath page](https://www.unsolvedmath.com/problems/5500031) was attempted first. The web reader could not access it, and direct retrieval returned HTTP 403. No claim of viewing its live rendered content is made. Identity was instead established from the complete hash-verified imported files, the complete actual catalog, and the directly retrieved primary page.

## Original and related papers

1. Joseph O'Rourke and Octavia Petrovici, **Narrowing Light Rays with Mirrors**, CCCG 2001, cited proceedings pages 137-140. [Conference-hosted PostScript](https://www.cccg.ca/proceedings/2001/orourke-13443.ps.gz). The retrieved document converts locally to a five-page manuscript with internal pages 1-5. Its full text was inspected; internal page 3 was visually inspected. Conjecture 9 is the full target. Conjectures 6-8 are stronger aperiodic-cardinality claims; their distinction matters. The manuscript also gives periodic-direction countability. The title, bibliographic proceedings pagination, and actual five-page retrieved version are not conflated.

2. David Milovich Jr., **Trapping Light With Mirrors**, dated 20 February 2004. TOPP cites MIT Undergraduate Journal of Mathematics 6:153-180 (2004). [Author-hosted complete 28-page PDF](https://www.tamiu.edu/~dmilovich/mirrors4.pdf). The definitions, unfolding framework, general-result statements, rational-angle setup, and final Theorem 4-19/Corollary 4-20 were inspected; internal page 28 was visually verified. Corollary 4-20 states countably many nonescaping directions at most, for rational-angle configurations. Endpoints absorb in this paper, so its escaping rays are valid escapes under transparent endpoints too. Section 4 explicitly uses rational density and openness. This audit does not claim an independent line-by-line verification of the entire 28-page proof or its dependencies.

3. Zachary Mitchell, Gregory Simon and Xueying Zhao, **Trapping light rays aperiodically with mirrors**, Involve 5(1):9-14 (2012). [Publisher PDF](https://msp.org/involve/2012/5-1/involve-v5-n1-p02-p.pdf). The entire six-page article text was read, including both constructions and final qualifications; printed page 9 was visually inspected. Theorem 1 gives an aperiodically trapped ray; Theorem 2 gives any finite number of distinct such rays from one source. The final section outlines an arbitrary-prescribed-finite-directions extension without a formal proof. We do not need that stronger extension. The construction's nondegenerate rays are unaffected by changing endpoint absorption to transparency. This paper explicitly leaves the all-directions question unanswered and credits Ben Stephens' independent unpublished 2002 construction.

## Prior attempt and related-target checks

At repository commit 0b27fa5396166e4e9fab43474146bb7fba7973a9, the complete actual attempts directory has 62 entries and no 5500031 directory. The verified queue blob places the target at rank 776, queued, 0/5. Exact ID/code/title PR searches, ID/title commit searches, ID/mirror branch searches, and a topic code search found no matching attempt. An unrelated mirror-knot PR is not a duplicate. The initial full recursive tree was truncated and was not used as an absence certificate; the relevant nonrecursive subtrees were fetched completely. This is bounded evidence, not an assertion about deleted branches, unindexed content, or unpublished work.

The related-target-groups file has no 5500031 entry. The complete catalog's other genuinely adjacent entry, 3900009, concerns illumination of a closed polygonal room and possible dark regions, not trapping by disjoint open mirror segments. It is not resolved by this note. No fresh proof of that adjacent target was attempted.

## Reuse and attribution

The countability/unfolding and rational-density facts are credited prior results. The concurrent-support, parallel-drift, explicit four-mirror, and quadratic-certificate arguments are elementary authored reconstructions presented without a novelty claim. No author contact, submission, acceptance, priority certification, or human peer review occurred. Public metadata alone records source hashes and inspection history; source binaries, article text, images, and imported data are excluded.
