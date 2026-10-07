# Complete adversarial package review one — candidate 1

Reviewer: internal independent package reviewer `package_review_one`.

**Decision: candidate 1 requires a reproducibility repair and a fresh complete-package review.** No substantive mathematical defect was found in the exact consequence note or the complete pivotal October 4 construction. Withholding a duplicate novelty Zenodo deposit is warranted by affirmative public disclosure evidence. This verdict does not authorize treating candidate 1 as a clean final package: its documented archive reproduction command fails from a fresh extraction.

## Exact checkpoint and scope

Audit completed at 2026-10-06T22:29:25.280916-07:00. Estimated completion of this assigned audit: mathematical/source review 100%; package review 100%. Estimated readiness of candidate 1 as an audited repository note: 90%, pending the one demonstrated packaging repair and required fresh review. Progress toward an authorized new-discovery Zenodo publication remains 0% because the user's duplication gate applies; a DOI and tracker entry were not created or verified.

I started from the complete original request in `notes/ORIGINAL_REQUEST.txt`, not earlier favorable source-review summaries. I read the full current `main.tex`, the four-page frozen `paper.pdf`, README, CURRENT_THEOREM, dependency ledger, approach table, publication status, algebra proof, both source audits, both priority/provenance audits, priority search ledger, exact decoded prior-public triage files and their API/version evidence, research log, executable verification/reproduction/checkpoint files, and saved build/layout/native/checkpoint receipts. I then independently read all seven primary October 4 proof sections, its top-level paper source, bibliography, repository and manuscript READMEs and Lean scope documentation. I inspected the actual Lean declaration identified by the catalogue as well as its comparator. The numerical source PDF was authenticated by hash; I did not render all 31 upstream PDF pages or rebuild the earlier Lean theorem. Neither operation would establish a numerical witness or formalize the October 4 argument.

Every file in the frozen candidate manifest matched its listed size and SHA-256. All 34 archive members passed CRC, safe-relative-path and regular-file checks and matched the corresponding frozen worktree bytes. The archive was actually extracted into the reviewer's owned directory and its documented reproduction command was run there. The original frozen `paper.pdf`, manuscript, archive and shared Git were never modified. Internal subreview spawning was attempted but failed due storage exhaustion; this report is my own review, not an aggregation of an unexecuted subagent pass. No external individuals were contacted. Read-only public-source requests were used for priority authentication.

## Substantive finding: the archive cannot finish its documented reproduction

`verification/reproduce.py`, candidate-1 SHA-256 `4e378705a59aed6a4a990cb5cde897fd2435b9f8ff74b75e4d6e7cae303d92c0`, writes `project/'receipts/clean_reproduction.json'` at line 31. It never creates the `receipts` directory. `source-and-audit.zip` contains no `receipts/` member or receipt file, so ordinary extraction does not create that directory.

Reproduction from an untouched extraction with Python 3.14.6 and Tectonic 0.16.9 confirmed the defect. Compilation, text assertions, PDF information, font extraction and copying the generated PDF all completed. The process then exited 1 with `FileNotFoundError` at that receipt write. The missing path was inside `reviews/package_review_one_work/extracted/receipts/`. Its exact stderr is preserved as `reviews/package_review_one_work/reproduce.stderr.txt`. An earlier successful build in the full project folder does not exercise this boundary because that folder already contains receipts.

Required repair: create the receipt parent directory in `reproduce.py` before writing, or otherwise make the documented clean extraction command self-contained. Rebuild the archive and manifest and give the entire exact revised package to a new independent reviewer. This defect is not a mathematical counterexample, but it blocks a clean-package verdict under the user's reproduction requirement. I did not silently add the directory to the extracted package to make the advertised command pass.

The newly generated PDF has SHA-256 `34da935ec8f5cb3f865aaba8d7ef9f627e25bd5e488098690af35c5df9a948cd`. Its extracted text is byte-identical to that of the frozen PDF. Different PDF timestamp bytes are already disclosed by the reproduction script. Thus the failure is in receipt completion, not manuscript compilation or content.

## Independent attempts to falsify the mathematics

### Scalar algebra, module handedness and coefficient extension

The proof works in any nonzero unital associative ring with `ab=1`, `ac=0`, `c≠0`. Setting `f=ba` gives `f²=f`; `e=1-f` gives `e²=e` without any commutativity or characteristic hypothesis. `ec=c` certifies `e≠0`, while `e=1` would give `a=a(ba)=0`, contradicting `ab=1`. The zero-ring boundary is expressly excluded. Dropping the nonzero-annihilator condition can produce `e=0`, so that condition has not been silently discarded.

Complementarity gives `R=baR⊕eR`. The identity `b=bab` proves `baR=bR`. Both maps `L_b` and `L_a` multiply on the left and are therefore right-module maps; `L_aL_b=1` and `L_bL_a` restricts to the identity on `bR`. The explicit absorption maps `(ar,er)` and `(u,p)↦bu+p` compose to the identity using `ae=eb=0` and `ep=p`. Swapping these for right multiplication would fail: taking `s=1,r=a` would demand `ab=ba`, precisely the equality excluded here. No handedness error was found.

The summand `P=eR` contains the nonzero element `e`, is cyclic and finitely generated, and is projective as a direct summand of `R_R`. Group completion gives `[R]=[R]+[P]`, hence `[P]=0`; it cannot justify `P=0` or a nonzero class. The manuscript correctly states that augmentation splits a copy of `K_0(F_2)=Z` from `K_0(R)`, so it does not confuse this one vanishing class with a vanishing entire group. General projective cancellation is violated by this witness, but is not said to be equivalent to direct finiteness.

For any characteristic-two field `K`, the prime-field embedding is injective and the group elements remain independent basis vectors. It preserves both `e≠0` and `e−1≠0`. This is the same group and the same scalar element for every such field, not a field-dependent construction. There is no extension to odd characteristic or characteristic zero, and no analytic reduced-C*-algebra inference. The exact arbitrary-field scalar conjecture in Öinert Problem 1(c) supports the stated positive-characteristic specialization. I independently opened that primary text and Gardam's pinned reduction source. The classical reduction is accurately attributed as an older elementary implication; earliest-original attribution is not claimed.

### Balanced finite types, conditioning and diameter

The primary source fixes `q=128,v=16513,p=129/16513`; seven Fano complements create the unique parity exception, and the alphabet has 16520 letters paired into 8260 generators. The counts `(129m−1)/4` and `129(m−1)/4` are integral for `m≡1 mod4`; the total extra incidence is exactly balanced with every ordinary label. Eventual per-line capacity is valid because `7·129/(4·16513)<1`. This is not a claim of admissibility at every small parameter.

The squared-turn contraction is strictly below 1, with exact ordinary bound `71589573988/72026254783`. The extra row bound must be divided by the vector value 4; its ratio is `195474585/311633336`. The long-word threshold absorbs the fixed `4|T|` prefactor; it is not applied to short words indiscriminately.

The source proves the girth event nonempty by switching away a bad edge against a distant good edge of the same matching. The two required smallness conditions on `c_0` control both the expected short-cycle count and the excluded-radius ball. The loop and overlapping-slot cases do not invalidate the switch. The conditioned prescription bound follows from an injective switch count, rather than division by an uncontrolled girth probability. The bound is then valid for a sufficiently small linear number of prescriptions as needed in expansion. Rounding `ceil(129k/2)` leaves exponent at least 62.5; the union bound is summable. The diameter argument handles disconnected graphs by growing balls and spacing them along a geodesic. No unexplained connectivity assumption was found.

### Repeated-edge patterns and the unbounded arrangement quantifier

I read and reconstructed the entire 594-line bounded-pattern proof. The image graph has bounded cycle rank by the weighted nonbacktracking-walk argument; marking endpoints and branch points gives boundedly many chains. A repeated traversal is not counted as a fresh random edge prescription. Stage `j` uses distinct edges with multiplicity at least `j`, and the incidence inequality gives total `V_j−E_j−k_j≤0`, with the fixed root paid for exactly once. The boundary with two interval endpoints at one vertex is covered by counting endpoint incidences with multiplicity.

The simultaneous offset grid has `s→∞` and `s=o(L)` uniformly for each fixed pattern bound. Comparison overlaps exceeding half a block give a partial matching of occurrences. Translation self-links have nonzero displacement and a forest equality graph; reflection self-links force a fixed inverse letter or adjacent inverse letters, forbidden by reducedness. Word-bin projections at a stage are bounded by assignments on the entire link component; using a minimum-bin block absent from that stage is valid because these are projections of full string assignments. Fixed-stage expectations use injective image-graph embeddings and distinct prescriptions. The argument bounds a realization by the minimum of its separate stage first moments. Multiplication of their deterministic upper bounds introduces no probabilistic-independence assumption.

The resulting `epsilon` is fixed independently of `K_0,C,I`. The planar reduction subsequently chooses closure, cutting and separator constants and only then takes `n` large. It extracts one system with the same fixed triple from every finite arrangement regardless of its original size. This avoids transferring the central assertion to an uncontrolled union over all arrangement sizes. The digon/Euler count permits disconnected neighborhoods and multi-boundary complementary regions. Closures retain original segments without cancellation; all appended occurrences remain unpaired. Separator deletion and bad-cluster budgets leave a positive surviving total. At most one short cluster can contain the intact exceptional interval, and that exceptional cost is strictly below half the original total because an ordinary boundary is required. The externally cited Lipton–Tarjan separator is used in its usual stated scope; I did not reprove that classical theorem here.

### Cone pictures, root protection and torsion

I independently read the complete cone-picture proof, including all four surgeries. Replacing each graph component's cone by a basis-relator complex is a relative homotopy equivalence: both replacements are contractible CW pairs containing the same graph. The pictures use abstract cone factorizations and never require the attached cone image to embed.

Minimal boundary length gives cyclic immersion for inner disks and linear immersion with distinct fixed endpoints for the rooted boundary. A nonempty such boundary cannot fill in the rose alone, so a rooted failure has an ordinary inner disk. Same-edge pairs lift to the same actual abstract graph edge, not merely a coincident label. Joining two inner disks, joining inner to exterior, exterior self-bands, and inner self-bands each lower length while retaining the relevant failure. For an exterior self-band the retained complementary disk contains the marked break, preserves root and endpoint, and requires no new filling of the discarded loop. For an inner self-band in a sphere, one lift of the same contractible abstract cone supplies both caps; their H_2 classes sum to the original class. Hurewicz guarantees that at least one new sphere stays essential. These points are necessary and are present in the primary argument.

Consequently arrangement exclusion separately yields `pi_2(X)=0` and protected roots; protection is not inferred from asphericity alone. The simply connected two-dimensional universal cover is acyclic and therefore contractible by Hurewicz and Whitehead. Restricting its length-two free `ZG` resolution to a prime-order cyclic subgroup remains free. Its impossible vanishing of cohomology in degree greater than two contradicts the displayed periodic cyclic resolution. Thus torsion-freeness is supported by the actual October 4 proof, not an earlier torsion example.

The deterministic product-graph parity argument correctly cancels component contributions even when different components have coincident group labels. Only the root contributes to the identity coefficient of `c` by protection. This yields the precise scalar triple needed by the follow-on. No substantive gap was found in this chain.

## Explicitness and formalization boundaries

The source establishes existence at sufficiently large admissible `m` and selects an unlisted matching outcome. A spanning tree in every component supplies the finite relators `w_x t w_y^{-1}` for non-tree edges. The root-path sums give the actual scalar elements in that selected presentation. The follow-on neither lists a numerical `m`, matching, relator set or support nor supplies a numerical multiplication certificate. Its claims are correctly existential, which the original request explicitly permits.

The actual declaration `OAI.KaplanskyCounterexample.finitelyPresented_counterexample` in `lean/OAI/RingTheory/DirectFiniteness/FinitelyPresented.lean`, lines 35–40, explicitly includes an element of odd prime order and an unspecified finite field of characteristic two. The comparator contains `sorry` and is not the proof. The actual declaration's SHA-256 is `b7a90d24bd01b71d1a31a4a07c32b722bca3788b981f1f9e58e67ecf602686b2`. Neither supplies the torsion-free `F_2` assertion under review. The package correctly avoids any full-formalization or human-refereeing claim.

## Priority decision authenticated independently

Fresh unauthenticated requests returned HTTP 200 for both exact prior-public files at commit `f27318d83bd7000ef817957a9a4b3087de28d198`. Their bytes equal the saved evidence:

- [Prior report, section 4](https://github.com/AlecKriebel/Math/blob/f27318d83bd7000ef817957a9a4b3087de28d198/openai_followon_batch2_20261006/REPORT.md), SHA-256 `20746bbc95ea76c2661f51fb1c987e36004cc6a07de7a0fc3cd5184da08c8763`.
- [Prior algebra notes, section 1](https://github.com/AlecKriebel/Math/blob/f27318d83bd7000ef817957a9a4b3087de28d198/openai_followon_batch2_20261006/agent_notes/algebra_groups.md), SHA-256 `d0ecbc688e8ff706c3c392a8cfcbb9cb6b3a51228c32c22420b7a6c0d7f1de66`.

Together they already state the scalar idempotent, every characteristic-two field extension, cyclic projective absorption and zero K_0 class, and identify the same `1−ba`, direct-sum decomposition and isomorphism maps. Their upstream-validation caveat means they are not certification of the input, but their public disclosure does defeat advertising the expanded elementary consequence as an unpublished new discovery. No substantive new mechanism was found in the follow-on. The user's duplication rule therefore warrants withholding the duplicate novelty deposit; this is not an authorization to claim a completed publication objective, reserved DOI or tracker row.

A fresh path-history request for the October 4 source returned only `adc7f1241b42e322a6451854ab7e4b4c146bf78a`, recorded at `2026-10-06T21:58:50Z`, with no later correction shown. The source's October 4 manuscript date is not a demonstrated public-release date. Recorded commit dates do not establish earliest public accessibility; no first-priority claim is justified or used. Companion and earliest-original historical audits remain bounded as their reports explicitly disclose. Those limits do not weaken the direct affirmative duplication witness.

## Executable, layout and custody checks

The exact supplemental checker ran successfully from the extracted archive and returned contraction `71589573988/72026254783`, seven Fano lines and 256 abstract shift samples. Its calculations check elementary finite incidences, rational contraction, balance and boundary examples only. They do not certify the source's random-existence theorem or multiply a target-group numerical witness. The code and README accurately state this limitation. Assertions are used as ordinary Python checks; no claim of a hardened adversarial theorem prover is made.

`checkpoint.py` was reviewed as code but not executed: it can push to remote main. The supplied receipts record matching remote commit IDs and preserved shared HEAD/index. I did not independently rerun those publication operations. The code's concurrency behavior and credential setup are not mathematical proof dependencies.

The frozen PDF has four pages, correct author/ORCID/title metadata, no encryption, JavaScript or forms, and embedded fonts. All four pages were rendered at 72 dpi and visually inspected. Formula layout, references, pagination and margins are clean; no clipping, overlap or missing-reference marks were seen. Source assertions and bibliography agree with the PDF text. The archive includes the self-contained manuscript and scripts but excludes local third-party source copies; source retrieval is linked and hashes are provided. All 104 rows in SOURCE_MANIFEST and all 85 rows in PRIORITY_SOURCE_MANIFEST match local evidence. All 15 files of the October 4 primary folder also equal their actual blobs at the pinned commit in the read-only upstream clone. This authenticates the precise input rather than trusting its copied filename.

Machine-readable review evidence is preserved under `reviews/package_review_one_work/`: `archive_receipt.json` records every archive member and hash; `independent_custody_receipt.json` records pinned-blob authentication, fresh remote byte equality and PDF comparison; `priority_read_receipt.json` records the saved metadata review and fresh upstream history. The failed clean reproduction stdout/stderr are retained. Owned extraction/render intermediates were removed after review to prevent accidental publication of duplicate scratch copies; the original archive is sufficient to replay the defect.

## Final scope and required next action

Strongest accepted mathematical result: the entire original existential core follows from the exact October 4 construction and the self-contained classical ring/module calculation. This review found no substantive proof gap in the construction or consequence. Acceptance is a source-level mathematical audit with a named external dependency, not formal verification, numerical certification, conventional peer review or evidence of novelty.

One substantive packaging concern remains: the reproducibility command fails from the delivered archive. Repair it, re-freeze exact hashes and obtain a new complete-package adversarial review from scratch. This review does not approve a later changed package merely because the expected code change is small. The publication-withheld status is correct and should remain unless a genuinely new justified in-scope contribution or explicit revision of the user's objective changes the gate.

## Exact frozen payload hashes

The manifest itself has SHA-256 `1b2f99131c9ea819268e390479a910eedbd354962b152fce591604875fbf533c`. The following table is an exhaustive byte/size validation of its frozen payload; primary scientific inputs additionally have their authenticated exact hashes in the custody receipt and source manifests.

| Path | Bytes | SHA-256 |
|---|---:|---|
| `main.tex` | 14416 | `445851559e86811878782b608fe055f573d330c0263166825a16cc025b319c57` |
| `README.md` | 4476 | `d3815e3d9545ff30491341fd3d092c8e69d4cff06e27e5fa95c846e0a9c5887a` |
| `CURRENT_THEOREM.md` | 2295 | `d8caebbbf1a168e7dc9ac3c40918a37fdc95bf02279d194916adb7d5698bb154` |
| `DEPENDENCY_LEDGER.md` | 2963 | `9a912019eac3ed970e91209e19153a4bc0fb43dbe2102ed991b0344e7b55f9d3` |
| `APPROACH_TABLE.md` | 1451 | `38688e3adc1eed1693c3c6e1724c89acd397de58c064ae31192bed5d7a5c445f` |
| `PUBLICATION_STATUS.json` | 689 | `837eab0d2d6cca63e534804221be296d39c8fe7c379e095f7500792c396c4a9e` |
| `notes/ALGEBRA_PROOF.md` | 14603 | `d37107eb351e368988b2f6eb66960243a82a43386aff97fed267f9944b36066f` |
| `notes/PRIORITY_AUDIT.md` | 14166 | `630e4e0d5f329d5ad18e91b00c91a699a68fd1294c73ee9cfbfb696b1efbd598` |
| `notes/CLASSICAL_PROVENANCE_AUDIT.md` | 11968 | `2d117ce4ecb096c3b021eadbec51b4c8a194c5d70a2dfd6b1e16c280ff7863c6` |
| `reviews/source_combinatorics.md` | 19536 | `3ab0430a850619450f14c3c1670fe12c954a274f2a875272184a98a7be61f112` |
| `reviews/source_topology.md` | 17183 | `862c5dea66b6b42331772d43c6c3dd88b3693a2c4919caa2405cb988d3000a21` |
| `verification/verify.py` | 2260 | `a8b6985630c6b2850541d07716e65254f0191c1ec9ff89fae5a83f2a4db44cbe` |
| `verification/reproduce.py` | 2202 | `4e378705a59aed6a4a990cb5cde897fd2435b9f8ff74b75e4d6e7cae303d92c0` |
| `sources/SOURCE_MANIFEST.json` | 27226 | `5b566eec62c8ed20a52e14a1088f0bfa9c3783eea8740f31d2cf1115e9d5cb12` |
| `sources/PRIORITY_SOURCE_MANIFEST.json` | 22926 | `3edc47a1c702dfa02e9dba13c9793d6955d181cc1587fb5ff294deab98985254` |
| `sources/UPSTREAM_LICENSE.txt` | 11357 | `c71d239df91726fc519c6eb72d318ec65820627232b2f796219e87dcf35d0ab4` |
| `notes/priority_evidence/AUDIT_HASHES.json` | 577 | `78e9206073711b1d0dc66c7a8fa33ca70075ecf97582ae1037048d22d9d6730f` |
| `notes/priority_evidence/QUERY_TIME.txt` | 33 | `97e60748fc019ae8a0ea9cf0f7bf7d30a84fdc64fbde33d0455dba7afd923b97` |
| `notes/priority_evidence/REMOTE_TRIAGE_ALGEBRA.md` | 7464 | `d0ecbc688e8ff706c3c392a8cfcbb9cb6b3a51228c32c22420b7a6c0d7f1de66` |
| `notes/priority_evidence/REMOTE_TRIAGE_REPORT.md` | 17807 | `20746bbc95ea76c2661f51fb1c987e36004cc6a07de7a0fc3cd5184da08c8763` |
| `notes/priority_evidence/SEARCH_LOG.md` | 5251 | `ee155b4a0f7e014d2b3bd28fe2025d2c22ef8e599fa3a2c2ac849a656cca0899` |
| `notes/priority_evidence/remote_commits.json` | 1098 | `b3fba14a30e34f4fd5ba49b8d87e89836bdf82239a2edfed6e9be26726fd1925` |
| `notes/priority_evidence/remote_commits.json.headers.json` | 1492 | `c3e120f2afdf7e7f704259730c53068bde29645da9c9dda3946fdacf6bc21b05` |
| `notes/priority_evidence/remote_oct4_history.json` | 1098 | `b3fba14a30e34f4fd5ba49b8d87e89836bdf82239a2edfed6e9be26726fd1925` |
| `notes/priority_evidence/remote_oct4_history.json.headers.json` | 1492 | `543e58c122a8a87f290834c8dead5d2cf10f7ae05227321c1523e7dfd4ba615a` |
| `notes/priority_evidence/remote_public_events.json` | 42445 | `60482bf0b591877aec6c52997db9f2f069ba3c361b8319c03026f8f9171f722a` |
| `notes/priority_evidence/remote_releases.json` | 2 | `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945` |
| `notes/priority_evidence/remote_repo.json` | 5865 | `f68fe55a2c890539955764c429da794be48e6b62a19278e03d6125bd3d4d2fc5` |
| `notes/priority_evidence/remote_repo.json.headers.json` | 1492 | `ad8c2c98c126f9303202b1a9ea0e430af180287973688f72ce60044719d60d43` |
| `notes/priority_evidence/remote_tags.json` | 2 | `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945` |
| `notes/priority_evidence/triage_algebra_commits.json` | 3353 | `47ca3352aa6effbf5eb3a91aaebb99991be5bf34d22ac1d472bef86c58d415b5` |
| `notes/priority_evidence/triage_remote_algebra_status.json` | 11358 | `74b3d2bfea3423d4d24c12d915c833d09c8ff3d8aeb714bc50b0c74d7785af6a` |
| `notes/priority_evidence/triage_remote_report_status.json` | 25483 | `c85c21aa7e48ab3829712de8c986ed9b354751f0636ebaebac3cd2f8101f68f0` |
| `notes/priority_evidence/triage_report_commits.json` | 3353 | `47ca3352aa6effbf5eb3a91aaebb99991be5bf34d22ac1d472bef86c58d415b5` |
| `paper.pdf` | 63820 | `128201717ddb4aa259da63136add2d8b727c0f86482ea420f316b7ed41a201e6` |
| `source-and-audit.zip` | 109603 | `be9120e222ded416f7df9bfa0828e6a698c487b02667220cf5e86aca7be1683c` |

Original request SHA-256: `e9a57bae398aeb56c13b087592890c4004d873eff2cb3c55c627ef6a1d2c8295`.
