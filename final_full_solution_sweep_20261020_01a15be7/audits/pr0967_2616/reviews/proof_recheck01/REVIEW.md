# Independent adversarial proof recheck: PR 967 / record 2616 / KOU-21.107

Audit date: 21 October 2026 UTC. Snapshot under review: commit `b356dec5cb01e5f536b9cfeece56ad08844c03cb`; author report SHA-256 `ddde58f03f320c881b78e59b60a40f315e1811c7c88aaa25ce620c427afbb6ca` (9,338 bytes).

**Verdict: the report gives a complete ZFC counterexample to the intended mathematical statement. No mathematical correction or unresolved proof gap was found.** The construction is a countably infinite, Hausdorff, nondiscrete Boolean topological group with an explicit partition into exactly countably infinitely many nonempty dense sets and no expansive sequence of pairwise-disjoint finite subsets. The conclusion is about validity; this audit makes no novelty, priority, editorial acceptance, or formal mechanization claim.

## Independence and scope

The exact author report and snapshot inventory were read first. Both primary PDFs were then retrieved directly, and the relevant complete pages were extracted, rendered, and visually inspected. `INITIAL_INDEPENDENT_ANALYSIS.md` was saved at 2026-10-21T20:31:34.991511Z, before reading either original audit, acceptance file, or historical closure. Its SHA-256 is `f321ba7aeb9df547e7f9a64b4627b0715c9f02e5e59957358281e7a9623fb1a9`. The initial independent reconstruction already identified the complete proof and the essential hypothesis controls. The two original audits were compared only afterwards.

This review addresses exact target matching, the infinite mathematics, source attribution, elementary computational controls, and local evidence custody. A separate reviewer is handling priority and duplicate searching; that work is neither assumed to prove the theorem nor recertified here. No individual or other research agent was contacted, and no original/shared source, branch, index, reference, acceptance, or release was changed. Commit/push publication is retained by the parent workflow.

## Primary evidence actually read

| Primary item | Relevant location | Actual retrieved bytes | SHA-256 |
|---|---|---:|---|
| [Kourovka Notebook, arXiv 1401.0300v48](https://arxiv.org/pdf/1401.0300v48) | Complete PDF/printed pp. 193 and 97; 21.107 and predecessor 15.80 | 1,476,795 | `a646018b69344a06729ba0cfda50d3850e99fd6c04e798f58b6e82aef8c33462` |
| [Sipacheva, Free Boolean Topological Groups, arXiv 1612.04878v1](https://arxiv.org/pdf/1612.04878v1) | Complete PDF/printed p. 25, Section 8, especially final paragraph | 423,481 | `dddf0ef8a2bd5caae99086b3c0023c7f5b1ce0bf8c65f9d6e6598cf1d73f1f25` |

The Section 8 heading and opening context on Sipacheva p. 24 were additionally checked by text extraction only after the independent reconstruction. Direct HTTP retrievals completed at 20:30:24.269917Z and 20:30:24.181421Z respectively, both status 200 with no URL redirect. Full headers and exact timestamps are recorded in ignored `private/retrievals.json`. The downloaded PDFs, selected-page text, and rendered page images are private evidence and are not included as public source bodies. These fresh PDF bytes exactly match the candidate's published source pins.

The current problem concerns a **countable** topological group, arbitrary pairwise-disjoint finite blocks, and eventual intersection with each open set; the threshold may depend on that set. Neither first countability nor metrizability is required. The published wording omits “nonempty” before “open”; the meaningful interpretation must exclude the empty open set. The proof produces a nonempty open obstruction and therefore addresses that stronger intended interpretation.

The predecessor's box-product counterexample is uncountable. Its other annotation refers to a resolvability result for abelian groups with finitely many involutions; it neither supplies the present obstruction in the inspected passage nor applies to this Boolean group. The predecessor is on p. 97 of v48. Version 47, the official repository page, and the current version-history page were **not** independently retrieved in this recheck; no claim about their present status is made.

Sipacheva's p. 25 identifies the filter-relative Mathias topology with the free Boolean linear group topology and gives the finite-subset subgroup base. The candidate correctly credits that construction as standard. The topology identification can also be checked directly: after replacing A by its intersection with a cofinite tail beyond max(s), the coset s + H_A is the Mathias basic set [s,A]. These refinements establish the same topology. For the empty support, use the usual threshold -1. No stronger ultrafilter property is imported from adjacent results.

## Independent proof reconstruction and falsification attempts

### Ultrafilter and exact set-theoretic assumptions

A maximal proper filter extending the cofinite filter exists by Zorn's lemma: a chain union is a proper filter because every finite list of members lies in a single chain member. If a set C is outside a maximal filter, adjoining it cannot preserve properness, so an existing member is disjoint from C. Upward closure places the complement of C in the filter. A proper filter cannot contain both complementary sets. No finite set can be a member because its cofinite complement already is.

Fix any such free ultrafilter U before considering any block sequence. The proof requires only finite intersections, exclusion of finite sets/cofinite membership, and the decision of each subset. It does not require selectivity, a P-point, rapidity, Ramsey properties, countable completeness, a pseudointersection, CH, or a bound on block sizes. The later recursive index choices can be made by choosing the least eligible natural number, so no hidden ultrafilter selection principle occurs.

### Countability, topological group axioms, separation, and nondiscreteness

Let G be the finite subsets of N, with symmetric difference as addition and empty support as identity. The binary support encoding s -> sum_{k in s} 2^k is a bijection with N. Thus G is countably infinite, abelian, and Boolean.

For A in U, H_A is the subgroup of finite subsets of A. Its subgroup property and H_A intersect H_B = H_(A intersect B) imply that the cosets form a genuine topology base: if two cosets contain x, their intersection is x + H_(A intersect B). At a pair (s,t), the sum of s + H_A and t + H_A equals (s+t) + H_A, which proves joint continuity. Inversion is identity. This verifies a topological group, rather than only a separately continuous operation.

If s differs from t, exclude a coordinate k of their symmetric difference by taking the cofinite A = N minus {k}. The two H_A cosets cannot meet, since a meeting would put s+t in H_A. This proves Hausdorff separation. Every A is infinite, so every H_A and every basic coset is infinite; no singleton is open. Cosets are clopen because their complements are unions of other cosets. The Hausdorff clopen base also supplies complete regularity under conventions that require it: an appropriate clopen neighborhood separates a point from a closed set by its continuous characteristic function.

### Exactly countably many dense pieces

Color each finite support s by v_2(|s|+1). This is defined uniquely, including at the identity, whose color is 0. For any fixed color j and coset s + H_A, choose q >= |s| in the unbounded progression 2^j(2r+1)-1. The infinite set A minus s contains q-|s| fresh points, giving t in H_A disjoint from s and |s+t| = q. Thus s+t belongs to the specified coset and has color j.

Every color meets every nonempty basic open set, so each color class is nonempty and dense. Distinct classes are disjoint and all supports have a color. This proves an actual partition into exactly countably infinitely many nonempty dense sets; no algebraic property of those pieces is presumed.

### Every pairwise-disjoint finite block sequence is defeated

Take an arbitrary sequence F_n of pairwise-disjoint finite subsets of G. If infinitely many blocks are empty, the nonempty open set G is missed infinitely often. Otherwise discard an initial segment through the last empty block. By disjointness the identity belongs to at most one block; discard a further initial segment through that block if present. Every remaining block is nonempty and contains only nonempty finite supports. This preprocessing is essential because max(empty) is undefined.

For each remaining index n, let M_n be the finite nonempty set of maxima of supports in F_n. Exactly 2^k nonempty supports have maximum k. Since each support occurs in at most one block, k occurs in at most 2^k of the M_n. Their sizes may be unbounded and the M_n may overlap heavily; the conclusion used is **point-finiteness**, not disjointness or a uniform bound.

After finitely many selections, the union B of the selected M_n is finite. Only finitely many other M_n meet B, by a finite union of the point-finite exceptions. Avoid those indices and the finite initial index interval. A later eligible index therefore exists. Induction yields strictly increasing n_i with pairwise-disjoint M_(n_i). This is a full infinite recursion, not an extrapolation from a finite greedy sample.

Let C_0 and C_1 be the unions of the even and odd selected maxima sets. They are disjoint. A proper filter cannot contain both; choose a side C_epsilon outside U, and use decisiveness to obtain A = N minus C_epsilon in U. **Both sides may lie outside U**, which is harmless. The sides need not cover N, and the complement of their combined union is not what is asserted to belong to U.

For each selected index i of parity epsilon, every support s in F_(n_i) has max(s) outside A. Hence s is not a subset of A, so F_(n_i) misses H_A entirely. This is a single nonempty open identity neighborhood missing infinitely many blocks at unbounded original indices. It gives precisely

\[
\forall (F_n)\text{ pairwise-disjoint finite},\quad
\exists A\in U\quad\forall m\quad\exists n>m:
F_n\cap H_A=\varnothing.
\]

The topology is fixed before the arbitrary sequence; its defeating neighborhood is allowed to depend on the sequence. The argument does not require the blocks to cover G, have bounded size, or come from the dense partition. Showing infinitely many misses, rather than merely one miss, is exactly what negates the eventual threshold.

## Meaningful controls and what they rule out

`independent_checks.py` was authored independently of the candidate checker, using explicit sets and a closed-form admissible cardinality. The final execution used a byte-identical fresh private copy, isolated Python with bytecode disabled, and no external imports. `INDEPENDENT_EXECUTION.json` records the run; `INDEPENDENT_RESULTS.json` records:

- 4,096 Boolean-group triples, 65,536 mixed-subgroup/coset cases, and 240 coordinate-separation pairs.
- Exact maximum-fiber sizes for k=0,...,13.
- 12,544 fresh-support/color extensions over seven colors and arithmetic progressions of periods 1,...,7. These reservoirs test support extension only; they are not declared ultrafilter members.
- All 16,384 labeled disjoint assignments of seven nonidentity supports, with 95,980 finite complement-decision algebra cases.
- All 65,536 assignments including the identity. These include 55,330 cases requiring empty/identity prefix excision and 42,591 with a surviving nonempty finite tail.

The finite principal atom in the complement truth table checks only “at least one disjoint side is outside a proper ultrafilter, and its complement is inside.” It does not represent a free ultrafilter or certify infinite density, nondiscreteness, or the existence of an infinite disjoint subsequence. No finite test can certify those infinite assertions.

The adversarial controls distinguish the following genuine failures of altered arguments:

| Alteration | Failure or counterexample |
|---|---|
| Replace maximum by minimum | The disjoint singleton blocks containing supports {0,k} have the same minimum 0 for every k; the required finite-fiber bound fails. |
| Drop block disjointness | Repeated blocks containing support {0} violate the maximum occurrence bound. More generally, increasing finite initial enumerations of G eventually meet every nonempty set if overlap is allowed. |
| Replace a free ultrafilter by a principal one | The minimal identity neighborhood has only two points and contains both identity and its generating singleton. The topology is not Hausdorff and cannot have three disjoint dense pieces meeting that neighborhood. |
| Assert exactly one parity union belongs to U | With a principal atom outside two disjoint finite unions, both unions are nonmembers. The valid proof uses only “at least one nonmember.” |
| Complement the union of both parities | If one parity union is a member, the combined union is also a member, so its complement is not. The candidate complements a chosen nonmember side instead. |
| Drop ultrafilter decisiveness, keeping only the cofinite filter | The parity split has no cofinite side or cofinite complement. The corresponding group actually admits an expansive sequence, as constructed below. |
| Drop finiteness of blocks | The already proved dense partition itself becomes an expansive sequence of infinite blocks. Finiteness is essential to the thinning mechanism. |

For the cofinite-filter control, enumerate every basic cylinder (k,p) specifying the first k coordinates with pattern p contained in {0,...,k-1}. At stage n, choose one new finite support in each of the first n+1 cylinders by appending a unique coordinate larger than all previous coordinates and at least k. Each stage is finite, no support is reused, and every cylinder is met at every sufficiently late stage. This is an explicit infinite expansive construction in the cofinite topology. The script checks its first 40 stages, using 820 distinct supports; the general argument, not the prefix count, proves the control.

As an additional sanity check, any countable Hausdorff nondiscrete group with a countable base admits such a construction: each basic open set is infinite, so stage n can choose fresh representatives in its first n+1 basic open sets. A countable first-countable group has a countable base by translation. Consequently the candidate topology must fail first countability, consistent with the target imposing no such condition. This does not supply an alternative proof of the candidate; it identifies a boundary at which the positive statement would hold.

## Comparison with the original audits

After the initial independent proof was saved, both original mathematical audits were read. Their conclusions and proof mechanisms agree with the reconstruction above. They correctly flag the eventual quantifier, identity/empty-block preprocessing, point-finiteness before thinning, no special-ultrafilter hypothesis, the version-48 p. 97 predecessor locator, and the standard topology attribution. No unresolved audit contradiction or inherited mathematical gap was found. The present proof does not infer correctness from their conclusions. In particular, this recheck independently added explicit controls for the cofinite-filter expansive construction, the invalid minimum map, principal-filter separation failure, and parity decision variants.

Only the inspected author harness was rerun; the historical publication verifier was not run, and its broad mutation harness was inspected but not executed. Neither publication control is independently recertified here. Historical source searches, earlier operating-system versions, and prior run identities were not treated as newly observed facts.

## Custody and reproducibility

`run_reproduction.py` verifies every one of the 26 supplied original files against `SOURCE_SNAPSHOT.json`, including byte count, SHA-256, and Git blob ID. It runs the preexisting author code only from a fresh private copy after its writes were inspected. The harness writes only disposable copies below that private replay's explicitly set temporary directory. The final independent finite checks likewise ran from a fresh byte-matching private copy. No original or sealed source was executed in place or modified.

On this host the actual run used Python 3.14.6, UID/EUID 501. The copied author harness passed in normal, -O, and -OO modes; each mode rejected 18 malformed fixtures, and all modes rejected the 10 packet/manifest tampering controls. Its read-only append/create probes failed as intended and hostile imports did not execute. `AUTHOR_HARNESS_RERUN.json` preserves the actual receipt rather than copying the older run's environment claims. All 26 original file hashes remained unchanged. The 13,488-byte author archive contains 12 regular files and two allowed directory entries, with every file body byte-identical to its supplied author snapshot. It was inspected without extracting it.

These are local custody checks of the parent's supplied immutable snapshot, not an independent live authentication of GitHub commit ancestry. The primary PDF retrievals were independently fresh. Full raw PDF bodies, renderings, retrieval headers, copied originals, and execution streams remain under ignored `private/`; public analysis contains only authored discussion, bibliographic metadata, checks, and hashes.

The final `EVIDENCE_MANIFEST.json` inventories every public and private evidence file by relative path, byte count, and SHA-256, excluding only the manifest and its detached `SEAL.sha256`. The detached seal binds that manifest; the independently delivered digest is the external comparison value. `verify_seal.py` requires that digest explicitly, checks the complete file set and every body, and rejects symlinks. After the seal is made, this review directory is not to be edited or rerun in place. For reproduction, work in a new disposable copy and preserve this sealed evidence.

The local original snapshot custody can be rerun from a copy of `run_reproduction.py` placed in a new sibling review folder under the same `reviews/` directory; it reads the supplied original snapshot and creates only new private replay files in that new review folder. The independent finite script writes only standard output and can be run from a fresh private copy with `python3 -I -S -B`. Do not overwrite the sealed JSON outputs while reproducing.

## Exact remaining gap

**Mathematical validity gap: none found.** The strongest verified result is the full infinite ZFC counterexample with the stated exact hypotheses, proved in prose and supported by finite algebraic and hypothesis controls. The unavoidable interpretive boundary is the primary statement's omission of “nonempty” before “open,” which the candidate handles in the mathematically meaningful way. The proof remains nonconstructive in its free ultrafilter and is not formally mechanized.

Priority, exhaustive literature completeness, external editorial confirmation, GitHub's live authenticity, and a security proof for the operating system are outside this independent proof audit. No unresolved issue in those categories is silently promoted to a mathematical assumption. Completion estimate for this assigned proof recheck: 100% once the detached manifest seal verifies.
