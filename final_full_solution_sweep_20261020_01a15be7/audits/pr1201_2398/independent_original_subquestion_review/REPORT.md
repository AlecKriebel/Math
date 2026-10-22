# Independent original-subquestion review: PR1201 / problem2398 / EP944

Review completed 2026-10-22 UTC. Own bounded review100%; parent sweep79%. Review scope is the FIRST original question printed on page113 of Erdős1989, its exact relation to this PR, mathematical sufficiency of the retained prior results, and reconciliation of existing publication identities. No provider, Git, ledger, or parent-owned file was changed.

## Verdict and mandatory disposition

**YES: the first original question has a complete affirmative prior answer in the material represented by PR1201.** Treat this as a complete prior solution requiring existing-publication accounting, rather than excluding it as partial. It is already stated and proved in Alex Chan's NBER Working Paper35757, September2026, DOI [10.3386/w35757](https://doi.org/10.3386/w35757). The resolving DOI and official NBER PDF were independently retrieved, and the decisive finite construction has been independently reproduced here.

**Do not create a new Zenodo record or claim a new discovery.** The existing supporting dataset is [10.7910/DVN/PULBFB](https://doi.org/10.7910/DVN/PULBFB). The registered data archive checksum matches the publicly available GitHub release ZIP exactly. Ema Skottová and Raphael Steiner's stronger prior theorem for all k>=5 and all r>=1 is separately published at [10.48550/arXiv.2508.08703](https://doi.org/10.48550/arXiv.2508.08703). That arXiv DOI alone does not contain Chan's k=4 construction.

This does not solve the distinct arbitrary-r question at k=4,r>=2, or determine the requested optimal order-dependent resilience. Chan's particular graph has exact three-color defect2 and consequently fails robustness against two arbitrary edge deletions. Preserve that residual statement without letting it erase the complete first original question.

No substantive mathematical objection remains to the first-question acceptance at the stated conventional-proof and independent finite-computation boundary. Existing publication-record reconciliation and fresh checks before any action remain the parent's work.

## Immutable PR binding and eligibility

Fresh read-only connector metadata and complete changed-file comparison agree:
- PR1201 is open and draft.
- Head e4cd1f31dbce8f60931012d96ea214de9c1e1ab7.
- Base and merge-base 4b27092a448d53b61408355ce44ec38d103a1ce4.
- Exactly eight added paths under unsolved_math_prioritization/attempts/2398; no QUEUE.md change.
- All eight complete API blob texts equal the local immutable head-path objects and the saved source bytes. SHA-1 Git blob identity and SHA-256 byte identities were recomputed.
- Complete body SHA-256 9f30782066479439bc0d21870cd2de471fd9baf6f2a80f4501e18ace26da5f93.

See LIVE_SOURCE_BINDING_CHECK.json and the private fresh connector receipts. The complete PR body, README, acceptance, full30957-byte PROOF.md, source metadata, and the relevant audit corrections and finite-audit sections were examined. Full source hashing is identity evidence, not proof acceptance by itself.

The absence of a QUEUE.md edit invokes independent eligibility inference. The PR explicitly accepts all k>=5/r>=1 and the finite k=4/r=1 example. Their union contains all parameters of the first original question. The PR's disclaimers about resolving the entire stronger EP944 bundle do not remove that mathematical fact. The omission of historical computational programs from its prose edition also does not exclude this first solution: fresh public inert data and independently authored exhaustive code now reproduce the finite step.

## Exact original questions and provenance

Fresh original source: Paul Erdős, On some aspects of my work with Gabriel Dirac, Annals of Discrete Mathematics41 (1989),111–116, printed113, PDF page3:
https://users.renyi.hu/~p_erdos/1989-19.pdf

Original PDF786149 bytes, SHA-2568f533914582f1c7101a679d85847383d5b736c2347c8bb84691875b11fa5987c. This reviewer visually inspected the rendered page, rather than trusting the extraction that loses the equality bar.

The first question is exactly:
For every integer k>=4, does there exist a finite simple graph G with
chi(G)=k, chi(G-v)=k-1 for every vertex v, and chi(G-e)=k for every edge e?

The subsequent question strengthens this to every k>=4 and every positive integer r, with immunity to any r deleted edges. The paragraph then asks an order-dependent quantitative question and the largest such resilience function. The paragraph explicitly presents these as successive questions. Single-edge immunity for every k>=4 is therefore a full original subquestion, not an invented fixed-parameter substitute.

The fresh ErdősProblems944 page still says k=4,r=1 remains open. That is a discrepancy with the later NBER claim, not a falsification of an explicit graph whose required properties are checked here. This review does not claim that the curator or mathematical community has accepted Chan's work. The 1989 primary wording, mathematical argument, publication PDF and independently reproduced finite object control this bounded disposition. No outreach was initiated or prepared. NBER's introduction cites Dirac1952 for attribution, while the later literature dates this particular conjecture to1970; this report relies on the unambiguous 1989 primary statement and does not adopt an unsupported1952 origin date.

## Independent finite proof of the k=4 case

The public fixed source is alexgocardinal/dirac-critical-graph at commit697307af42505b11490fdc74c04eda5c7ec76c51. Public source URLs and exact pins are in SOURCE_PINS_INITIAL.json. No author code, Lean project, certificate program, or candidate PR code was imported or executed.

The graph is reconstructed from the mathematical specification. Vertices are pairs (a,i) in Z12 x Z5, labelled5a+i, with product
(a,i)(b,j)=(a+b mod12, i+2^a j mod5).
The inverse-closed right-Cayley generator set is
{(1,0),(11,0),(5,1),(7,2),(6,0),(6,3)}.

Own code reconstructs every edge, then compares the complete edge set with both public inert edge-list and graph6 data. The graph has60 vertices,180 edges, degree6. Its canonical sorted edge-list SHA-256 is85914250312a4fe8d1a67d747fea2ee1772c9762796af90095efa61fb4c0400c, identical to the NBER AppendixA checksum, registered supporting dataset, fixed public source and frozen release. All60 explicit left-multiplication permutations were checked for bijectivity, adjacency preservation, and sending0 to the desired vertex.

Own verifier1 exhausts all proper three-colorings of G-0 up to global color permutation using color-invariant DSATUR vertex choice and first-use color labels. It visits1519 nodes and64 dead ends, retaining16 complete color-permutation orbits. In every orbit each of the three colors occupies exactly two of the six root neighbors {5,26,30,33,37,55}. There is no timeout, node bound, floating point, external solver or author certificate premise. A zero-domain branch is impossible to extend; all introduced color choices are tried, and unused color names are interchangeable because the vertex choice depends only on color-equality patterns. These facts justify completeness of the quotient enumeration.

Own verifier2 uses a distinct domain-copying, singleton-propagation recursion, minimum-domain/static-degree vertex selection, and every available color branch. It uses no color or graph-orbit quotient. Fixing c(1)=0,c(6)=1 only for the puncture enumeration is exhaustive modulo global color renaming because1 and6 are adjacent. It finds exactly16 normalized proper colorings in167 nodes. Their neighbor tuple is always(1,1,0,2,2,0). The entire16-element set independently equals the NBER AppendixB template, not merely its count or boundary profile. Separately, the same solver directly rejects three-colorability of G and of all180 individual edge-deleted graphs:181 unsatisfiable instances,142522 nodes. No cutoff or finite-sample extrapolation is used.

The mathematical bridge is short. A proper coloring of G-0 extends to a four-coloring of G by a fresh color at0. If G or G-e were three-colorable for an edge incident to0, restricting to G-0 would force the color of0 onto two of its neighbors. At most one such conflict can be removed by e. Thus G and all root-incident edge deletions require four colors. The explicitly checked transitive automorphisms transport this to every edge and give three-colorings of every G-v. A two-coloring of any G-v would extend to a three-coloring of G with a fresh color at v, a contradiction. Therefore:
chi(G)=4, all60 vertex deletions have chromatic number3, and all180 edge deletions have chromatic number4.

Giving0 one of the existing puncture colors creates exactly two monochromatic edges, with a complete checked witness retained. Conversely, any three-color assignment with at most one monochromatic edge restricts to a proper puncture coloring after deleting an incident vertex, contradicting the verified balanced-neighborhood property after symmetry transport. The exact three-color defect is therefore2. This proves the finite case and also its precise failure for r=2.

Verifier1 was checked with malformed edge data and a deliberately invalid coloring, all rejected. Verifier2 was compared against literal three-color assignment enumeration on every labelled graph of order1 through4,75 cases, before the graph runs. These are implementation controls; the universal mathematical conclusion rests on the exhaustive full60-vertex searches and explicit symmetry proof.

All normal, -O and -OO runs passed with zero stderr and byte-identical complete outputs:
- verify_chan_independent.py:8850 bytes, SHA-256ca179d4d08a0063fb38873a658148a10cbaa54c98fc2137b603f0b60ade7f259; output35619 bytes, SHAd901772c1e72a4ea0cbb923a5de5f84917cfc7c01ef02f0485e17550b770d65d.
- verify_chan_direct.py:5210 bytes, SHA-256b85634ed6669f66d5d15a43d3e0cf6e33adb65219f016f3fafb287e09aff01c8; output28605 bytes, SHA1cb63140d3776a4d28ba30abce4fa1576096c689bece48eff604acd14f1e3a91.

Output witnesses, per-instance node counts, rejection controls and exact receipts are retained privately. This is a fresh conventional finite proof using trusted independently authored exhaustive code. It is not Lean replay, a kernel-only certificate, a claim that reported author logs were regenerated, or evidence about an unbounded graph family.

## The k>=5 component and repaired-proof boundary

Jensen's published2002 result already proves the one-edge existence statement for every k>=5, DOI10.1016/S0012-365X(02)00262-5. The primary university-hosted July2001 preprint was retrieved and its relevant Theorem5 statement and proof read. Its arbitrary-m strengthening concerns edges incident to a common vertex; do not misstate it as an arbitrary-edge-set theorem. For one deleted edge that distinction vanishes. Its conventional theorem may be cited as prior mathematical input; this report does not certify the entire unrelated dense-critical-graph paper.

A second route uses the PR's fully retained repair of Skottová–Steiner's all-k>=5/all-r>=1 construction. The complete repaired PROOF.md was read and its important dependencies challenged, including the exceptional k=6,8 cases. Its lower construction is independent of both Chan's finite graph and the externally imported Conlon–Fox upper-bound lemma.

The decisive lower proof checks are:
1. Parameters m>18r+2, q>=24r+12 and4|q give p=(k-1)m for odd k or2(k-1)m for even k, and N=qp+1. The explicit periodic puncture coloring excludes all edge-distance sets, including the reverse cyclic offset1. The repaired even residue expansion avoids the falsely printed positive congruence.
2. An unaffected3p interval supplies equal counts in sliding p-windows. Corrected odd clique partitions and the even C5[K2] independent-set bound force local balance and hence p-periodicity.
3. Ordinary block arguments cover odd k>=7/even k>=10. The separately closed exceptional argument for k=6,8 uses ring balance, signed forbidden distance -(2m-1), ringwise change-point status, one occurrence per color per ring, and the corrected non-change chain ending t_i-2. It does not assume the later two-option lemma. Counting the resulting runs supplies the otherwise missing two-block bridge.
4. Full blocks may be selected in the necessary translated period window because its first two positions are forbidden for the missing color. The retained T1 endpoint supplies all residues modulo2m. This yields the two allowed expected colors at each tested vertex.
5. The global deletion budget forces a color occurring more than2r times in a2m interval onto one parity. The first deviation contradicts that fact for k>=6. At k=5 the separately counted intersection has at least2m-16r-1 positions, leaving at least2m-18r-1 occurrences of the other color; m>18r+2 handles the endpoint losses and forces both parities.
6. At most2r affected vertices ensure a3p unaffected core in every L=qp/4 interval. Propagated p-periodicity then equates v0 and v(N-1) along the chain v0,vp,...,v(qp), contrary to their surviving cycle edge.

No substantive gap was found in this repaired lower chain. Specializing r=1 suffices for every k>=5 in the first original question. Full-prior all-r lower existence is a verified stronger component, not a novelty claim. The retained gluing/quantitative sections were also read but are unnecessary to close the first question. This review does not promote the omitted Conlon–Fox proof, an unaudited universal formalization, or every statement in all cited upstream papers as independently certified.

## Prior publication and support reconciliation

Official primary NBER page:
https://www.nber.org/papers/w35757
Official primary PDF:
https://www.nber.org/system/files/working_papers/w35757/w35757.pdf
DOI:
https://doi.org/10.3386/w35757

Title: Buying a Station or Relaxing a Constraint? Spectrum Repacking and Dirac's Conjecture.
Author: Alex Chan. NBER Working Paper35757, September2026.

The complete14-page PDF was read, including Section3, AppendixA, all16-coloring AppendixB, and references. The abstract, Theorem2 and Corollary2 explicitly state the finite construction and every-k>=4 first-question conclusion. Its group, generators, vertex numbering, graph checksum, balanced-puncture proof and normalized-coloring template all match the independently verified object. Its higher-k deduction credits Jensen2002 and separately Skottová–Steiner2025. This is semantic result matching, not title matching.

Fresh PDF440279 bytes, SHA-256c20f54b865a2600905a7bcb3a0aa949ddc80ac8f83dac0d69ec48017354f107b. Resolving the DOI returns this same PDF byte for byte; Crossref returns the correct sole author, title, NBER series and September2026 issue. The registry creation timestamp is2026-09-15; no exact day of mathematical discovery is inferred. Primary NBER cover says the paper has not been peer-reviewed. Its text discloses AI assistance. This review adds extensive independent AI mathematical/computational auditing and does not assert formal independent human peer review.

Supporting Harvard Dataverse DOI10.7910/DVN/PULBFB is DataCite-registered, findable, datasetversion1.0, available/submitted2026-09-10. Its title retains the earlier Dirac/antitrust framing. Fixed repository CITATION.cff and the public release connect that archive with Chan's60-vertex construction. The metadata's frozen ZIP SHA-25601bcc4420465143dff00b605b2140ae225dc44a445a540c8e9c49ffec9de92d7 exactly equals the freshly downloaded public GitHub release ZIP356258 bytes. All68 ZIP members were inventoried and hashed without extracting or executing programs. Three copies of the canonical graph and the structured certificate5959d3f0943bba98e2278ae567f7bbe2a406e41f7ce2015fa6e0101b9449e195 match the registered hashes and pinned source. This verifies accessible supporting material bound by the registered archive checksum.

Direct Dataverse landing/API retrieval returned403. Do not describe it as a successful Dataverse payload download or a direct landing-page inspection. The public release is not marked immutable by GitHub; the content hash and DataCite binding freeze the reviewed bytes. Earlier antitrust/spectrum titles and the NBER title are related by the exact mathematical construction and metadata chain; do not fabricate a journal-version relation.

Skottová–Steiner's DOI independently resolves to the arXiv record. Its theorem is all k>=5, all r>=1 and quantitative growth; it leaves k=4 open as of that source. A fresh author research page labels it submitted. No journal DOI was authenticated in the bounded primary search, which is not a proof that no later journal record exists.

Ferudun2026, DOI10.48550/arXiv.2606.18462, was checked as a cited primary priority lead. Its abstract states small-order exclusions and structural restrictions for6-regular candidates, and explicitly leaves the k=4/r=1 existence problem open at that point. It does not supersede the complete Chan graph. It must not be counted as an earlier full solution based on its theorem wording or citation alone.

These prior records precede this PR's2026-10-11 creation. Thus no new resolution is attributable to this PR or this sweep. No assertion of Chan's worldwide first discovery, continuing global literature completeness or community acceptance is necessary for the deduplication conclusion.

## Fresh ledger check and exact proposed row

The live Google Workspace CLI read the complete numeric gid1254632077 before substantive finite mathematical auditing, again after discovering the dataset DOI, and again at2026-10-22T05:44:06.242487Z after identifying the NBER DOI, and finally at2026-10-22T05:54:24.215563Z with precise DOI/name/result regular expressions. The latest snapshot contains183 rows; its raw SHA-256 isf1c0b25f00801ac15d8e1c71b4f8deb90d56320336ea1adfbb64476e28c9357b.

All populated rows have exactly the existing schema:
A Original Problem; B Solution Chat URL; C DOI; D Notes.
Queries covered EP944/problem2398, PR1201, all three relevant publication DOI strings, construction/publication titles, Dirac, vertex-critical/critical-edge semantics and author identities. No matching result or DOI was present. Broad Chan/Steiner/1201 substring hits were manually separated from unrelated words, geometric Steiner results and OWR-12012. Raw unrelated rows remain private.

LEDGER_ROW_PROPOSAL.json supplies a four-cell proposal, with blank chat URL. It uses NBER DOI10.3386/w35757 as the publication DOI, sole authorAlex Chan and the exact title; its notes credit the dataset, Jensen and Skottová–Steiner separately. No new upload or append was performed. The parent must perform a fresh live semantic/DOI check immediately before action, update a matching row if one now exists, and read back the final row. This report's finite review is complete; publication accounting is pending until that reconciliation is actually done.

## Replay, privacy and limitations

Read verify_review_bundle.py and BOTH verifier sources completely before execution. The bundle verifier is network-free and read-only. It checks the sealed member hashes, cached PR/source identities, registry/archive consistency and the two fresh finite proofs; optional --optimized replays normal/-O/-OO. It neither rereads the live spreadsheet nor certifies current provider state. Byte identity is not scientific acceptance; the separate mathematical derivations and exhaustive-search completeness arguments above supply the proof boundary.

All copied external source bytes, full provider responses, spreadsheet rows, raw computational outputs and certificate payloads are private_sources and marked private in SEALED_MANIFEST.json. They are audit inputs, not permission to redistribute publisher PDFs or ledger contents. Authored reports, proposed-row metadata and independently written checkers remain separate. No public publication package is being proposed for this already published result.

No source candidate or author program was executed. Only independently authored Python, trusted PDF/text/image utilities and read-only source/provider retrieval were used. No communication with parallel agents, human researchers or external individuals occurred; only parent-task progress reporting was sent. No branch/index/ref/provider/ledger mutation occurred, and no earlier closed review range was reopened.

