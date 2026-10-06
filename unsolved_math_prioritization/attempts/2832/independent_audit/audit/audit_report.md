# Independent audit: KP-3.34 / ID 2832

Audit date: 2026-10-06. Catalog rank: 912. Outcome: accept the corrected derivative as a stopped partial investigation, with four of at most five approaches recorded. The universal stabilization bound is neither proved nor refuted. No novelty is claimed.

## Exact decision

The four original structural propositions are correct under the stated ordinary-stabilization and ambient-isotopy conventions. They are unchanged in the accepted derivative. The original packet needs one narrow source-hypothesis correction: the flip-genus lower bound attributed to Johnson's Theorem 1 applies to initial genus at least 2. The original citation paragraph omitted that restriction. The derivative inserts it and synchronizes the README, verification claims, and audit-status paragraph. This is a citation-domain correction, not a repair to any of the four proofs.

The acceptance report identifies both original and corrected archives and every member by SHA-256 and byte count. The original is preserved. The actual unified patch was applied with zero fuzz to a fresh extraction of the pinned original; all six resulting members match the corrected archive byte for byte. That replay verifies derivation and integrity, not the mathematical propositions.

## Input identity and inherited work

The original ZIP is 9,711 bytes with SHA-256 f6fa08d1a90fbb0b44f4098b260a7e22e99d2fd72f24f6e62df0f62791648244. Its external manifest is 1,376 bytes with SHA-256 1dcc35bc15ef26eca2791af98d1554dda4500da9290f7051e3c8959e17039db8. The archive has exactly the six declared, regular, non-executable members, with no duplicates, hidden extra files, unsafe paths, or CRC errors. Each member's actual bytes match its manifest entry.

All three complete input files were read and hashed, then parsed. The catalog has 15,458 entries; the problem corpus has 15,458 records; the report map has 6,701 keys. There is exactly one catalog and one problem-record match for ID 2832, and the catalog's rank is 912. KP-3.34 has no key in the report map; the prescribed lookup therefore gives an empty object. This is an absent separate report, not a substantive proof that happened to be omitted from inspection.

The entire exact-ID record, including its background literature-triage material, was inspected. The complete record/report pair was reconstructed using json.dumps([complete record, reports.get(problem_number,{})], sort_keys=True), with default separators and ASCII escaping, then encoded as UTF-8 without an added newline. Its SHA-256 is bcfe995308708c4f82d55cb096780b39eb2fd5f6f6f5cbb31a506ed434773e0f. The statement hash is d2ab0353b89652feee4e625ce936bf4f6a897e40616561e63fe9e52bf17a1f41. Both match the catalog and author metadata; the retained pair has the same complete JSON value. The inherited work is literature triage, with no separate substantive mathematical proof or computation to credit.

Full-corpus hashes, byte counts, and match results appear in input_verification.json. No corpus contents or exact record text are included in this audit deliverable.

## Foundations and conventions

The mathematical setting is one fixed connected, closed, orientable 3-manifold. Vertices are ambient-isotopy classes of embedded Heegaard splittings. In the ordered version, the isotopy must carry each labeled handlebody to the correspondingly labeled handlebody. An arbitrary self-homeomorphism is not a substitute for an ambient isotopy beginning at the identity. Forgetting labels gives the weaker unordered relation.

Ordinary stabilization has a unique ordered isotopy class at any specified final genus, and iterated stabilization composes. This is uniqueness above a fixed input. It is not injectivity of stabilization, uniqueness of a common minimal stabilization's destabilizations, or uniqueness of an unstabilized core. Several distinct lower-genus splittings may reach the same higher-genus class. None of the accepted arguments cancels a stabilization.

The standard local connected-sum construction with the genus-one splitting of the 3-sphere supplies the operation, respecting handlebody labels. Johnson's flip paper, Section 4 after Definition 10, explicitly gives uniqueness at fixed genus in its labeled setup. Reidemeister-Singer supplies eventual common stabilization. In the ordered setup eventual existence can also be understood by first using the unoriented theorem and then, if necessary, stabilizing to a flippable splitting. The ordinary flip construction has finite genus. No quantitative 2g bound for an arbitrary pair follows from this existence argument.

These classical facts are the mathematical dependencies. This audit checks their precise use and the cited statements; it does not supply new independent proofs of the full Reidemeister-Singer or Waldhausen theorems.

The notation P[h] means stabilization to absolute genus h, for an integer h at least g(P). It does not mean h added handles. Thus c(P,Q) is a minimum final genus, and is at least both input genera. Eventual existence makes the admissible set nonempty; well-ordering gives the minimum. Stabilization uniqueness and composition make all genera at or above that minimum admissible.

## Proposition 1: exact tower formula

For integers a >= g(P) and b >= g(Q), the formula c(P[a],Q[b]) = max(c(P,Q),a,b) is correct.

For the lower bound, any common stabilization of the already-stabilized inputs is, by composition, a common stabilization of the original inputs. Its genus also cannot be below a or b. For the upper bound, put h equal to the displayed maximum. Stabilize a common representative at the minimal original common genus to h. Fixed-genus uniqueness identifies it with both P[a][h] and Q[b][h]. No destabilization of that representative is required.

If counts r,s of added handles were used instead, the right side would be max(c(P,Q),g(P)+r,g(Q)+s). This resolves the possible indexing ambiguity without changing the packet, which already defines absolute-genus brackets explicitly.

For equal original genus g, the deficit is c(P,Q)-g. After r stabilizations of both inputs, the new deficit must be measured from the new initial genus g+r. Subtracting g+r from max(c(P,Q),g+r) gives max(c(P,Q)-g-r,0), exactly the stated law. Measuring again from the old g would be wrong. The law does not bound the original deficit.

## Proposition 2: ultrametric inequality

Let h=max(c(P,Q),c(Q,R)). It is at least the genus of every input. The two equalities at their possibly different common genera can both be stabilized to h. The two appearances of Q then identify by fixed-genus uniqueness, so equality is transitive at genus h. Consequently c(P,R)<=h. There is no summation of stabilization costs.

On one fixed-genus stratum, d=c-g is symmetric and nonnegative. It is zero precisely when the original ordered classes are equal, because stabilization to the unchanged genus is the identity. Subtracting g preserves the maximum inequality. Thus d is an integer-valued ultrametric there. The packet does not incorrectly call c itself a metric across all genera: c(P,P)=g(P), and no variable-genus deficit is being asserted to be a metric. Repeated application gives the finite-chain consequence at height 2g, but it does not construct a chain with the needed edge bounds.

## Proposition 3: unequal-genus core reduction

Every destabilization lowers genus by one, so any sequence of ordinary destabilizations stops after finitely many steps. The terminal core need not be unique. Choose any such cores P0,Q0 of genera p,q. If the two original inputs have genus g, then P=P0[g] and Q=Q0[g] as classes. Proposition 1 gives c(P,Q)=max(c(P0,Q0),g), independently of the choices of destabilizing disks or sequences.

Sufficiency of the proposed core bound follows by k=max(p,q)<=g: max(2k,g)<=2g. Necessity applies the original equal-genus assertion to P0[k] and Q0[k], whose common genus is max(c(P0,Q0),k). These inputs need not be unstabilized. The required inequality follows for every pair of cores, including pairs with unequal genera. The two directions are sound, and restricting only to equal-genus unstabilized pairs would leave a genuine gap.

The smallest-counterexample consequence is also correct. If both genus-g inputs were stabilized, they would each admit a genus-(g-1) predecessor. The same tower formula would force those predecessors to violate the conjectured bound at g-1. Here both-stabilized already implies g>=1, so no negative-genus object is introduced. The conclusion is only that at least one input is unstabilized. It does not establish that both inputs are unstabilized or that either input has minimum genus among all splittings of the manifold.

The equivalence proof is valid even when a chosen core has genus zero. It makes no Hempel-distance argument and does not depend on the genus restriction introduced in the citation correction.

## Proposition 4: bounded-height paths

For integer H, the graph contains classes of genus at most H, and an edge is one ordinary stabilization with the induced labels. A connected component means connectivity by a finite edge path; the graph need not be finite.

If the common genus is at most H, ascend from each endpoint to a minimal common representative. Reversing one of the ascents gives the requisite path and never exceeds H. Conversely, along any finite path, stabilize each vertex to H. Both ends of every edge then give the same genus-H class by composition and uniqueness. Transitivity along the path identifies the endpoints at H, proving the common-genus bound. The claim concerns endpoints that are vertices; if H is below either input genus, its stated premise does not apply.

This is an exact certificate criterion, not a proof that the height-2g graph connects every genus-g pair. Unbounded Reidemeister-Singer connectivity supplies no height control. Diagrammatic moves interpreted only up to a homeomorphism cannot silently be used as ordered ambient-isotopy edges.

## Geometric route and source limits

The pinned 2011 upper-bound manuscript states its same-side spine criterion in Lemmas 2-3. A designated spine with n locally maximal horizontal components relative to the other splitting's sweep-out yields a common genus at most p+q+n-1. The manuscript's construction addresses why the complement is a handlebody; the Betti number of an arbitrary union of abstract spines would not suffice. Matching the designated sides is needed in the ordered version.

For p=q=g, the sufficient case n=1 gives the target height 2g. The packet explicitly leaves unproved the global claim that every pair admits that position. It neither treats the condition as necessary nor uses it as an established universal normal form.

Theorem 1 of the same manuscript states a larger bound for both isotopy conventions. For positive equal genus its integral specialization is floor(7g/2-1), which does not establish the desired bound in general. The unrestricted printed formula has a degenerate p=q=0 issue; neither this audit nor the packet uses it there. The four structural propositions do not rely on the manuscript's global bound. The audit checked the statement and the cited local construction, not the manuscript's full 34-page proof or its asserted theorem as a new independently certified result.

## Sharp examples and the correction

The published Hass-Thompson-Thurston theorem uses ordered handlebodies and ambient isotopy. Its genus-g examples, for integer g>1, require exactly g additional stabilizations. The example description uses one underlying surface with the two labels interchanged; the accompanying construction achieves final genus 2g. This establishes sharpness of a proposed ordered bound, not a violation of it. Upon forgetting the order those particular initial surfaces are already identical. The paper expressly separates unordered equivalence and equivalence by homeomorphism; no claim about either is imported from its theorem.

Johnson's flip paper defines flip genus as a final genus. Its Theorem 1 has the explicit hypothesis g>=2 and lower bound min(2g,d_H/2). The introduction records the upper bound 2g. The abstract's wording about a number of stabilizations must not override the body's precise final-genus definition. The original packet interpreted final genus correctly but omitted g>=2 in its attribution; correction.patch fixes that omission. Hempel distance for low-complexity surfaces is not silently substituted into this theorem.

For an ordered splitting P and its label reversal, stabilization commutes with label reversal, so their least ordered common genus is the least genus at which the stabilized splitting can be flipped. The cited lower and upper flip bounds therefore concern this special pair. The lower bound is never greater than 2g, and the flip upper construction precludes using a flip pair to refute the proposed 2g bound. No universal upper bound for two unrelated splitting classes follows.

## Source inspection and search provenance

All four retained PDFs have the exact byte counts and SHA-256 values declared by the author; text was freshly extracted from those PDF bytes for this audit. K3's Problem 3.34 was read and visually checked on printed/PDF page 156. It presents the optimal genus-g stabilization bound as open and does not resolve the order convention in that paragraph. The ordered interpretation is stronger, with the weaker unordered version kept separate.

For the flip paper, pages 1-2 and Section 4, page 8, were read and visually inspected. For Hass-Thompson-Thurston, the opening definition and pages 2030-2032 were read, and the theorem, convention warning, example, and sharp upper construction were visually checked. For the upper-bound manuscript, opening definitions and pages 2-4 were inspected, including the theorem, its two-convention declaration, and Lemmas 2-3. These are bounded source inspections; they are not full proof audits of the cited literature.

The public K3 and Hass-Thompson-Thurston PDF endpoints and both arXiv abstract records were also opened during this audit. The upper-bound abstract record displayed only v1 (2011), with no journal reference or withdrawal notice displayed. Absence of a displayed notice is not a certification of publication, correctness, or non-withdrawal elsewhere. The specialized Seifert-fibered flipping paper's abstract was rechecked, but this auditor did not retrieve or hash its PDF. That does not independently verify the author's earlier unretained PDF-opening inspection.

The author's unsuccessful live problem-page retrieval and subsequent HTTP 403 remain reported historical limitations. This audit did not retry that denied endpoint. Exact-record verification and the public primary problem source supply the statement identity instead.

Six bounded repository searches were independently repeated through the approved GitHub connector: three issue/PR queries and three default-branch code searches, with maximum 20 results each. All returned empty lists. Several targeted public searches for recent common-stabilization results identified no full solution in the inspected results. These checks are not exhaustive searches of branches, commits, unpublished work, or the literature, and confer no novelty claim. Hashes verify the retained PDF bytes, not byte identity of a separately fetched web rendering.

## Packet-wide and final acceptance boundaries

Every original member and every corrected member was read. README, status, approach log, verification claims, proof text, and source metadata agree that the work is partial and that the universal assertion is unresolved. The log records four bounded approaches out of five; the audit checks those recorded arguments and does not reconstruct an otherwise unrecorded execution history. Both generality and stop condition are preserved.

The safe audit package includes only the authored original and corrected text, authored audit and acceptance material, the correction patch, and permissible verification metadata. It excludes copied PDFs, rendered pages, extracted source text, full datasets, exact record contents, connector responses, and private coordination material. All included files are regular non-executable data files. No repository publication, branch change, queue edit, or external communication was performed.

Accepted scope: the corrected stopped-partial packet and the four stated structural reductions. Not accepted or claimed: a proof or refutation of KP-3.34, a new sharp universal bound, a finite search establishing an infinite theorem, a novelty claim, exhaustive current-literature coverage, or full independent verification of the cited papers.

## Public references

- K3: A New Problem List in Low-Dimensional Topology, author preliminary version, Problem 3.34, printed p.156: https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf
- Hass, Thompson, Thurston, Stabilization of Heegaard splittings, Geometry & Topology 13 (2009), 2029-2050: https://msp.org/gt/2009/13-4/gt-v13-n4-p05-p.pdf
- Johnson, Flipping and stabilizing Heegaard splittings, arXiv:0805.4422v1: https://arxiv.org/abs/0805.4422
- Johnson, An upper bound on common stabilizations of Heegaard splittings, arXiv:1107.2127v1: https://arxiv.org/abs/1107.2127
- Schultens, Flipping Heegaard splittings of Seifert fibered spaces, arXiv:2208.10565v1: https://arxiv.org/abs/2208.10565
