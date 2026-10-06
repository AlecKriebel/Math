# Nuclear Fréchet spaces and chaotic operators: scoped results

Problem 30000573 / OWR-1323-010 / rank 813. Author checkpoint, 2026-10-06 UTC.

## Disposition

**Unsolved after five substantive approaches.** No proof that every infinite-dimensional nuclear Fréchet space supports a chaotic continuous linear operator, and no nuclear Fréchet counterexample, is supplied. The original question is unrestricted by a basis assumption. Here chaotic means a dense forward orbit together with a dense set of periodic vectors. Distributional, Li–Yorke, and frequent hypercyclicity are different notions.

The complex-space basis case is credited prior work, not a new result. The full Fréchet proofs appear in de la Rosa, Frerick, Grivaux and Peris, arXiv:1005.1416v1, Theorems 2.4 and 3.1. The shorter v2, associated with the 2012 Israel Journal paper, states the Fréchet extensions in its introduction and refers to a separate 2010 preprint. This packet does not mislabel those sections as a proof printed in the shorter version. Theorem 2.4 requires a continuous norm and an unconditional Schauder decomposition; Theorem 3.1 concerns an unconditional basis and does not require a continuous norm. Nuclear spaces with a Schauder basis have an unconditional basis. These results do not cover every nuclear Fréchet space. They are credited external inputs; their full construction is not independently reconstructed here.

The written proofs here establish:

1. The ordinary backward shift on a countable product E^N is mixing and chaotic for every nonzero separable Fréchet space E, without a basis assumption. If E is nuclear, the product is nuclear.
2. A continuous linear map intertwining that product shift with an operator on any space admitting a continuous norm must be zero. Thus this positive product construction cannot be pushed onto a continuous-norm target through such a map.
3. On the nuclear Köthe space X with p_k(x)=Σ_n |x_n| 2^(k·2^n), every continuous weighted backward shift is strongly stable. An explicit all-seminorm decay estimate is proved. The example and its no-hypercyclic-shift conclusion are already in Charpentier–Grosse-Erdmann–Menet, Example 3.8; no novelty is claimed.
4. On that same X, a specified diagonal-plus-small-shift operator has dense periodic vectors but also a continuous eigenfunctional, so is not hypercyclic. Dense periodicity alone does not repair the weighted-shift approach.
5. Scalar-plus-finite-rank operators on an infinite-dimensional Hausdorff locally convex space cannot be hypercyclic. A broader scalar-plus-compact obstruction is credited literature, with its compactness hypothesis kept explicit.

The general gap is existence of a continuous operator simultaneously having a dense orbit and dense periodic vectors on arbitrary nuclear Fréchet spaces lacking the structure used by these constructions. No basis, unconditional decomposition, product representation, continuous norm, or invariant-kernel factorization is inferred merely from nuclearity.

## Source and status limits

The primary question was checked against Bonet's problem 1.1 on printed p. 2271 of Oberwolfach Report 37/2006, DOI 10.4171/OWR/2006/37. The workshop ran in August 2006; the publisher records publication in June 2007. The report attributes the question to Bonet, Martínez-Giménez and Peris (2001).

The full supplied record and its absent research report, represented by an empty object, were reviewed. Their default sorted-JSON pair hash matches the catalog. The live unsolvedmath page returned an access error; its current contents were not freshly read. The supplied record's question agrees with the primary source. Source PDFs and corpus contents are deliberately absent from this release.

Targeted literature searches through 2026-10-06 found the partial resolutions above, but no authoritative full resolution. That is a bounded search outcome, not proof of worldwide nonexistence of a resolution. Public repository searches and the complete nonrecursive main attempts tree found no target-specific earlier attempt. An unrelated chaotic-semigroup PR is excluded. The initial recursive tree was truncated and was not used to certify absence.

## Verification

PROOFS.md contains the general arguments. The standard-library-only exact controls check block coding, exponent inequalities, finite-support intertwining constraints, and finite cyclotomic versions of the triangular identities. These finite checks are diagnostic supplements, not infinite-dimensional proofs or formal verification.

Run the verifier with the manifest SHA-256 supplied in the external freeze receipt:

    python3 verify_release.py --manifest-sha256 HASH

It checks the exact file set, forbids symlinks and unexpected directories, validates every byte count and SHA-256, reruns the exact controls, and compares their full output with RESULTS.json. The same command works with Python -O and from a relocated directory. AUTHOR_VALIDATION.json records replay and negative-control outcomes. Independent review is pending. No remote publication or outreach was performed by this author task.

## Public references

- Bermúdez, Godefroy, Grosse-Erdmann and Peris, *Mini-Workshop: Hypercyclicity and Linear Chaos*, Oberwolfach Reports 3 (2006), 2227–2276: https://doi.org/10.4171/OWR/2006/37
- De la Rosa, Frerick, Grivaux and Peris, *Frequent hypercyclicity, chaos, and unconditional Schauder decompositions*, full 2010 version: https://arxiv.org/abs/1005.1416v1 ; shorter version and publication: https://arxiv.org/abs/1005.1416v2 and https://doi.org/10.1007/s11856-011-0210-6
- Charpentier, Grosse-Erdmann and Menet, *Chaos and frequent hypercyclicity for weighted shifts*, ETDS 41 (2021), 3634–3670: https://doi.org/10.1017/etds.2020.122 ; inspected preprint: https://arxiv.org/abs/1911.09186v2
- Bonet, *A problem on the structure of Fréchet spaces*, RACSAM 104 (2010), 427–434: https://doi.org/10.5052/RACSAM.2010.26 ; author-hosted text inspected through web retrieval: https://jbonet.webs.upv.es/wp-content/uploads/papers/bonet0000a_p.pdf

This is an AI-assisted, unrefereed authored research checkpoint. No new priority claim is made for any lemma or example.
