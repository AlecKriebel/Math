# Second independent audit: KOU-21.107

Audit date: 8 October 2026. Target: record 2616, rank 1038.

## Verdict

**ACCEPT the frozen report as a complete, mathematically correct negative-answer proof in ZFC for the stated countable topological-group problem.** No mathematical correction patch is required. The source-free finite verifier and authenticated execution packet also pass this independent audit within the boundaries below.

This is an independent mathematical and reproducibility assessment, not a claim of publication, editorial acceptance, priority, or formal proof mechanization. The independently audited report has SHA-256 `ddde58f03f320c881b78e59b60a40f315e1811c7c88aaa25ce620c427afbb6ca`. The author freeze was preserved without modification.

The proof was challenged independently before any first-auditor conclusion was received. The first audit's written report was not used to establish the verdict. The finite reconstruction below was separately authored and does not import the candidate checker.

## 1. Exact target and source boundary

I independently inspected Problem 21.107 in the version-48 PDF, p.193. Its conclusion concerns one sequence of pairwise-disjoint finite subsets and eventual intersection with every open set; the threshold can depend on the set. The meaningful interpretation excludes the empty open set. The hypothesis is a countable topological group partitioned into countably many dense subsets. It does not impose metrizability, first countability, a uniform finite-block size, a covering condition on the blocks, or an algebraic condition on the dense pieces. The proposed group satisfies the stronger, explicit requirement of a partition into countably infinitely many nonempty dense pieces.

The version-48 predecessor 15.80 is on p.97, not p.98; p.98 is the earlier version-47 locator. Its uncountable box-product example cannot answer the countable target. The same version-48 annotation also mentions a Zelenyuk result about countable dense partitions in infinite abelian groups with finitely many involutions. That additional remark neither supplies a particular nonexpansive countable topology in the inspected passage nor applies to the present Boolean group, which has infinitely many involutions. This audit does not assert that the predecessor's annotation consists only of the box-product example, or certify an exhaustive literature search.

I also inspected Sipacheva's version-1 PDF, Section 8, p.25. The Mathias/free Boolean linear topology there has exactly the subgroup neighborhood base used by the candidate, so crediting the topology as standard is correct. The theorem proved here does not import a selectivity-dependent result from that paper.

Public references:

- E. I. Khukhro and V. D. Mazurov, eds., *The Kourovka Notebook*, version 48, Problem 21.107, p.193; predecessor 15.80, p.97: https://arxiv.org/pdf/1401.0300v48
- O. Sipacheva, *Free Boolean Topological Groups*, version 1, Section 8, p.25: https://arxiv.org/pdf/1612.04878v1

The locally inspected public-source PDF bytes independently match the candidate's published hashes: version 48, 1,476,795 bytes, SHA-256 `a646018b69344a06729ba0cfda50d3850e99fd6c04e798f58b6e82aef8c33462`; Sipacheva version 1, 423,481 bytes, SHA-256 `dddf0ef8a2bd5caae99086b3c0023c7f5b1ce0bf8c65f9d6e6598cf1d73f1f25`. The version-47 file also matches its listed 1,476,249-byte hash. No source PDF or source passage is included in this audit packet. Dataset matching and the broad search/status observations are not independently recertified by this second audit.

## 2. Infinite mathematical proof audit

### ZFC ingredient

A proper maximal filter extending the cofinite filter exists by Zorn's lemma. Unions of chains of proper filters remain proper filters, since every finite collection of members is contained in one filter in the chain. Maximality gives the ultrafilter decision property. A finite set cannot belong because its cofinite complement already does. This establishes the exact free ultrafilter required, in ZFC. No P-point, selective, rapid, Ramsey, or countable-intersection property is assumed at any stage.

### Group topology

The group is the finite subsets of the natural numbers under symmetric difference. It is countably infinite, abelian, and Boolean. For every ultrafilter member A, the finite subsets supported in A form a subgroup H_A. The identity H_A intersect H_B = H_(A intersect B) and finite-intersection closure of the ultrafilter give the required neighborhood refinement.

Whenever two basic cosets meet at x, their intersection is x plus the intersection subgroup. Thus the cosets genuinely form a topology. To verify joint continuity, a basic neighborhood of s+t contains the sum of the corresponding H_A-neighborhoods of s and t. This checks joint continuity, not merely separate continuity. Inversion is the identity and is continuous.

For different s and t, choose a coordinate in their symmetric difference and exclude that coordinate from A. This A is cofinite and hence belongs to the ultrafilter. The two H_A-cosets are disjoint, proving Hausdorffness. Every A is infinite, so H_A and every basic coset are infinite; the topology is nondiscrete. All subgroup cosets are clopen. No topology axiom is delegated to the finite tests.

### Dense partition

The exponent of 2 in |s|+1 exists and is unique for every finite s, including the identity. Therefore its level sets form a partition indexed by all nonnegative integers. For any fixed level j and any basic coset s+H_A, the allowed target cardinalities 2^j(2r+1)-1 are unbounded. Choose one at least |s|, and append exactly the required number of fresh coordinates from A outside s. There are enough because A is infinite and s is finite. Symmetric difference then equals disjoint union, gives the desired cardinality, and remains in the coset. Every color meets every basic coset, so each color is nonempty and dense. The argument covers arbitrary basic neighborhoods, arbitrary colors, and the identity color.

### Universal finite-block obstruction

Start with an arbitrary proposed sequence of pairwise-disjoint finite subsets of the group. Infinitely many empty blocks are already defeated by the nonempty open set consisting of the whole group. Otherwise a tail has no empty block. Since the group identity occurs in at most one block, a further tail also has no identity-containing block. This avoids applying the maximum function to the empty support.

For a surviving block F_n, take the finite nonempty set M_n of maxima of its members. For each natural k there are exactly 2^k group elements with maximum k. Pairwise disjointness of the original blocks therefore implies that k occurs in at most 2^k of the sets M_n. Importantly, the argument does not incorrectly assume the M_n are already disjoint.

For an infinite family of finite, nonempty, point-finite sets, an infinite pairwise-disjoint subsequence exists: a finite union of previously selected sets meets only finitely many remaining sets. Removing these forbidden indices and the finite index prefix always leaves a later choice. This is a recursion on natural numbers, with no special ultrafilter selection principle.

Split the selected maxima sets by the parity of their subsequence index, obtaining two disjoint unions C_0 and C_1. A proper filter cannot contain both. Select a parity whose union is not in the ultrafilter and take its complement A, which the ultrafilter must contain. Every member of every block at that parity has a maximum outside A, so no member of that block belongs to H_A. There are infinitely many such blocks with arbitrarily large original indices. The nonempty open identity neighborhood H_A thus refutes eventual hitting for this sequence.

The quantifier order is correct: the ultrafilter topology is fixed first; for every block sequence, the proof constructs a neighborhood allowed to depend on that sequence. The desired positive assertion would have to survive all neighborhoods, so one such neighborhood suffices to refute each proposed sequence. The proof does not need the blocks to cover the group, their sizes to be bounded, or the dense pieces to have any subgroup property.

These deductions establish the infinite theorem independently of any experimental output.

## 3. Independent finite reconstruction

`independent_checks.py` uses explicit finite sets rather than the candidate's bit-mask representation. It independently checks:

- 4,096 Boolean-group triples, including associativity, cancellation, and commutativity.
- 65,536 mixed-subgroup coset intersections, allowing different coordinate sets on the two sides.
- Exact maximum fibers for coordinates 0 through 15.
- 57,344 support-extension cases over eight colors and arithmetic progressions of periods 1 through 7, using a closed-form target cardinality instead of the candidate's search loop.
- 65,536 disjoint three-block assignments of all eight elements of the three-coordinate Boolean group, including the identity. It checks the finite-fiber occurrence bound, deletion through the identity-containing block, disjoint greedy maxima selection, and exclusion of each entire selected block by the relevant complement.

These are finite identities and finite instances of elementary steps. Arithmetic progressions serve only as examples of infinite coordinate sets for support extension; no ultrafilter membership is assigned to them. Neither script models a free ultrafilter with a finite principal ultrafilter.

The candidate's advertised counts were separately reconstructed as 16^3 = 4,096 group/coset cases, 13 maximum fibers, 256 times 6 times (1+2+3+4+5) = 23,040 coloring extensions, and 4^7 = 16,384 disjoint-block assignments. The reported JSON agrees exactly.

## 4. Software, trust, and execution audit

The actual account was UID 1000 and EUID 1000, running Python 3.12.14. The authenticated author harness passed in normal, -O, and -OO modes, including 18 malformed-fixture controls and 10 packet/manifest-tampering controls. Its independently rerun output is recorded in `AUTHOR_HARNESS_RERUN.json`.

The separate auditor runner also passed normal, -O, and -OO execution of the candidate checker and bootstrap. It tested 91 malformed fixture variants per mode: every fixture field as a boolean, float, negative integer, changed integer, string, null, list, or object; nonfinite constants, floating overflow, a 10,000-digit integer, duplicate keys, excessive input size, empty input, invalid UTF-8, trailing data, and a nonobject. Every rejection was nonzero and structured. The original harness additionally exercises missing and extra keys.

The checker uses exact type checks rather than isinstance for integer fields, so Python's boolean-as-integer subtype relation cannot silently pass. Parsed floats are checked for finiteness, and the schema then rejects even finite floats. Fixture values are exactly pinned before any combinatorial loop or bit shift, bounding computational input. Python integer arithmetic is exact. Executable checks use explicit exceptions rather than assert, so optimization does not erase validation.

The auditor directly confirmed that the actual frozen fixture rejects an attempted write-open and the actual frozen public directory rejects file creation. The author harness separately tested append/create failures on a read-only temporary copy. Positive runs used hostile working directories and import-path environment variables, with isolated Python (-I) and bytecode suppression (-B). Frozen public hashes remained unchanged.

The external bootstrap first checks the independently supplied manifest digest, then exact schema and file integrity. It excludes duplicate/unsafe names, symlink entries, missing files, and additional directory entries. It executes the verifier source and fixture from the already-authenticated byte snapshots, so those executable inputs are not reread after verification. The bootstrap and harness themselves were independently hashed before execution; a same-directory hash declaration alone is not treated as an independent trust anchor.

These controls are bounded reproducibility and hostile-input tests, not a security proof against a compromised operating system, compromised Python runtime, or concurrent adversary controlling every filesystem component. The immutable author report still labels its original submission as pending audit; this separate acceptance report does not silently rewrite that history.

## 5. Source-free allowlist and hashes

The author archive was independently checked to contain only these twelve regular files, plus the two containing directory entries:

- `public/README.md`
- `public/REPORT.md`
- `public/fixtures.json`
- `public/provenance.json`
- `public/sources.json`
- `public/verify.py`
- `external/AUDIT_INSTRUCTIONS.md`
- `external/MANIFEST.json`
- `external/PINS.json`
- `external/TEST_RESULTS.json`
- `external/bootstrap.py`
- `external/test_harness.py`

All archive file bytes match the frozen disk snapshot. The archive is 13,488 bytes, SHA-256 `1e9e605ee96cdceaca6d9e5ea3b007f0849d0383c8db5f7e4b0c84c35a68de5b`.

The independent author-snapshot inventory is `AUTHOR_SNAPSHOT.json`. Principal external pins are:

- Manifest: `31bd2aed10d96d5ada5344531e2207dd4388c8cb1328e3c448ac89be5b78ec8c`
- Bootstrap: `054dbe643ad4f78f13ea0595e4cab5379d438a33ab2fd2f6aed9f5125d9dcb57`
- Author harness: `5c6d1056179a95c647db5cc11028059c64c5abcdcabd69790cef892948c9ca27`
- External pin inventory: `cbf61f7d4163f50d15eb264e779bb79c9fc8a0566b571f0d9d9a3bf3fd96634d`

This second audit's deliverable allowlist is `INDEPENDENT_AUDIT.md`, `independent_checks.py`, `INDEPENDENT_RESULTS.json`, `AUTHOR_HARNESS_RERUN.json`, `AUTHOR_SNAPSHOT.json`, and `AUDIT_MANIFEST.json`. It contains authored mathematical analysis, code, test results, hashes, byte counts, public titles, and public URLs. It excludes copied sources, dataset contents, private coordination material, private paths, and personal data. The separate manifest pins the first five files; its own digest is supplied independently with the audit handoff.

No publication, queue change, outreach, or modification to the author freeze was performed in this audit.
