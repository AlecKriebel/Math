# Independent primary-source and exact-target adversarial audit: PR24

**Verdict: PASS_SCOPED_RESULT_ONLY.** The frozen proof correctly establishes a straight Euclidean triangulation with congruent complete closed vertex-centered radius-\(\sqrt{10}\) restrictions, maximum triangle diameter \(\sqrt{10}\), translation subgroup exactly \(2\mathbb Z\times\{0\}\), and non-cocompact full symmetry group. No mandatory mathematical correction was found. The original problem is not promoted to solved, the construction is credited to its prior family, and novelty is not certified. Current publication metadata requires the concrete corrections below.

Audited target: **10000062 / AMR-099-0062**, PR [24](https://github.com/AlecKriebel/Math/pull/24), original head **6b702110d1bd4b9220e2033fa5eed030911ce8c6**, actual merge base **01358d66fc67d1c462bddf31c0d4ee5b120e6737**. Scientific artifact: frozen CANDIDATE.md, SHA-256 **3df33716dab169f07c9ff24434023d2945fc8121e03519f91a0a3fdb1ea30f84**. This report concerns those exact bytes, rather than a future repaired head.

## Independence, criterion and source precision

At **2026-10-01T20:40:25.870946+00:00**, I sealed [SEALED_CRITERION.md](SEALED_CRITERION.md), SHA-256 **2abaeea02be46ab2dbda8bb011d226477aa33d4aced8e51b5721775677761101**, before reading CANDIDATE.md, programs, readiness/status, historical reviews, root conclusions or sibling reports. The first read comprised the literal pinned input, its prior_report, root/nested AGENTS, snapshot metadata, primary source text and figures. The early reconstruction of the prior family and separate claim categories is preserved unaltered. Historical material was read only afterward. No new proof-search turn was used.

The pinned question is Benjamini–Tessera Q5.7 in the [archived author manuscript](https://arquivo.pt/noFrame/replay/20201231041538id_/http://www.wisdom.weizmann.ac.il/~itai/erd100.pdf), dated 16.07.12, PDF p.7. The diameter bound is at most \(r\); the balls and isometries are ambient metric objects; reflections are allowed; both ambient planes appear. Section 5/5.1 places it among global rigidity questions from local information. Neither that context nor the manuscript's earlier Pinwheel discussion defines the intended periodicity convention. [Oxford slides](https://people.maths.ox.ac.uk/drutu/workshopGG/IBenjamini1.pdf), p.119, repeat the question. Both question pages were visually inspected.

The alternate author erdos.pdf has search-indexed Q5.7 on p.6, but its full file was unavailable in this pass: direct access and the attempted archived URL failed. Thus I independently verify the pinned archived p.7 and the full relevant slides, and do not falsely claim full-file verification of the alternate p.6 version. `erdosp6` is a page/version shorthand, not a verified separate live filename. Download hashes and failures are in [source_download_manifest.json](source_download_manifest.json); versions, inspections and the bounded searches are in [priority_checks.json](priority_checks.json).

| Claim category | Outcome at the frozen head |
| --- | --- |
| Exact Q5.7 under a demonstrated source definition of periodic | Unresolved: the definition is absent |
| Euclidean cocompact/crystallographic/rank-two conclusion | Refuted by the verified example |
| Euclidean existence of any nonzero translation | The example has a horizontal translation, so it does not refute this |
| Hyperbolic full metric-ball result or classification | Untreated |
| Novel layering or historical priority of metric specialization | Not claimed or established |

An Euclidean counterexample suffices to refute a universal E²-or-H² **cocompactness** assertion. A separate hyperbolic example is not logically necessary for that refutation. It would still be wrong to infer a hyperbolic classification or an unconditional answer to the source's undefined conclusion.

## Prior family and the metric distinction

Frettlöh–Garber, [Symmetries of Monocoronal Tilings](https://dmtcs.episciences.org/2142/pdf), DMTCS 17:2 (2015), 203–234, DOI 10.46298/dmtcs.2142, defines coronas, permits mirrored matches, and distinguishes translation rank from compact fundamental domains. Theorem 2.2 allows one-periodic planar monocoronal tilings. Its Section 2.3/Figure 8 and Appendix A.1.2/Figure 17 already supply independently chosen triangular layers. The arXiv [v1](https://arxiv.org/pdf/1402.4658v1), submitted 19 February 2014, has 26 pages; the published paper has 32. The relevant Figure 17 is arXiv p.15 / published p.221. Both relevant constructions and the published figures were checked.

My independently sealed coordinate reconstruction maps the candidate into that prior family: horizontal base \(b=2\), symmetric height \(H=3\), chiral height \(h=1\), chiral offset \(a=1/2\). The mirrored offset \(3/2\) is \(-1/2\) modulo the horizontal period. Reversing the order of the symmetric/chiral strips reindexes the same family. The resulting four distinct edge lengths are \(2,\sqrt{10},\sqrt5/2,\sqrt{13}/2\), so the four-length triangular case applies without a degeneracy. The schematic drawing fixes no height ratio that would exclude this choice. Arbitrary symbolic layering and a single exceptional layer are already prior mechanisms.

Full radius-\(r\) balls imply congruent vertex coronas here: every point of an incident triangle lies within distance \(r\) of its central vertex, because the entire triangle has diameter at most \(r\). The reverse implication is unsupported; balls can also meet nonincident cells. I found no explicit theorem asserting this diameter-radius full-ball upgrade in the inspected Frettlöh–Garber text. The proof below therefore checks a real extra condition, but its absence from these inspected sources does not certify novelty. Under ordinary straight locally finite face-to-face tiling assumptions, their Theorem 2.2 also already supplies a nonzero Euclidean translational period from the induced monocoronality.

## Universal reconstruction and falsification of the mathematics

### Triangulation, shape and threshold

For arbitrary \(\epsilon_j\in\{-1,1\}\), put \(\delta_j=1+\epsilon_j/2\), \(a_0=0\), and \(a_{j+1}=a_j+\delta_j+1\). The rows are

\[
 L_{j,k}=(a_j+2k,4j),\qquad U_{j,k}=(a_j+\delta_j+2k,4j+1).
\]

The short strip joins each lower vertex to the two adjacent upper vertices, and likewise the tall strip joins \(U_j\) to \(L_{j+1}\). Equivalently, partition each strip into parallelograms of width 2 and split each along the lower-right/upper-left diagonal. This proves disjoint interiors, complete coverage, straight face-to-face gluing and no crossings. Row gaps 1 and 3 and row spacing 2 prove local finiteness. The triangles have areas 1 and 3; squared side sets are respectively \(\{5/4,13/4,4\}\) and \(\{4,10,10\}\). Convex-triangle diameter is the largest side, so \(r=\sqrt{10}\) is both the bound and the attained maximum. Equality in the source's at-most bound is essential to the stated example and is permitted.

### Full closed balls, including every extra cap and boundary-only cell

Translate a lower-row center to \((0,0)\). Relative row phases and heights are

\[
 (-1-\delta_{-1},-4),\quad(-1,-3),\quad(0,0),\quad(\delta_0,1),\quad(\delta_0+1,4),
\]

with period 2 in each row. Since \(r<4\), no row at height \(\pm4\), or any farther row, enters the disk. This does **not** justify dropping cells from those rows; the small cap below \(y=-3\) must still be checked. All geometry at heights above \(-3\) that can meet the ball is determined by \(\delta_0\) and the fixed tall strips. The potential previous-symbol dependence lies in the short strip below \(-3\).

The circle meets \(y=-3\) at exactly \(p=(-1,-3),(1,-3)\). Each downward edge at either point has vector \(v=(h,-1)\), \(|h|\le3/2\). Hence

\[
 p\cdot v=3\pm h\ge3/2>0,\qquad
 |p+t v|^2=10+2t(p\cdot v)+t^2|v|^2>10\quad(t>0).
\]

Those entire edges are outside except for their endpoints. Edges descending from any other upper-row vertex have \(|x|\ge3/2\) and \(|y|\ge3\) throughout the potentially relevant strip, giving squared distance at least \(45/4>10\). The lower horizontal edges are at \(y=-4\). Consequently the cap is contained in the unique triangle based on the fixed segment from \((-1,-3)\) to \((1,-3)\); its apex may change, but every changed sloping boundary remains outside. The full clipped face piece is unchanged.

The two boundary points cannot be discarded. At each one, the six incident edges contribute three positive-length traces and three singleton traces. The six incident faces contribute four positive-area pieces and two singleton face pieces. The cyclic incidence pattern is preserved for either previous symbol. This checks multiplicities of distinct cells that collapse to the same point, rather than identifying all such cells as one geometric point. Convexity ensures each clipped face/edge is connected, so this reasoning leaves no disconnected pieces hidden by the signature.

The two values of \(\delta_0\) are exchanged by horizontal reflection, using offsets modulo 2; the surrounding symmetric strips match. For an upper-row root use

\[
 H(x,y)=(\delta_0-x,1-y),\qquad
 a'_i=\delta_0-a_{-i}-\delta_{-i},\quad \delta'_i=\delta_{-i}.
\]

Direct substitution gives \(a'_{i+1}-a'_i=\delta'_i+1\), and interchanges upper/lower row roles and their triangles. Translation handles arbitrary layer and horizontal indices. This proves the full closed-ball statement for **every** infinite symbol sequence and every vertex, including all restricted vertices, positive and singleton edges, faces and incidences. Reflections may be needed for local matches; a direct-isometry-only version is not asserted.

### Intrinsic full symmetry obstruction and sequence controls

Length-2 edges are exactly the horizontal row edges; all other edge lengths differ. Their connected straight lines are therefore intrinsic to the triangulation. Any ambient symmetry must preserve the horizontal direction, so its linear part is \(\operatorname{diag}(s_x,s_y)\), \(s_x,s_y\in\{\pm1\}\). This eliminates an assumed row-preserving restriction: row preservation has been proved from an invariant metric marker. The translation subgroup has index at most four in the full symmetry group.

For translations, the height-1/height-3 pattern forces vertical displacement \(4m\), never an upper/lower row swap. The uniquely shorter sloping short-band edge points upward with horizontal displacement \(-\epsilon_j/2\). Thus a translation requires \(\epsilon_{j+m}=\epsilon_j\) for every \(j\). In the chosen sequence \(\epsilon_0=-1\) and \(\epsilon_j=1\) for \(j\ne0\), this forces \(m=0\), and row spacing then forces the horizontal displacement to lie in \(2\mathbb Z\). Conversely those horizontal translations preserve all cells. The translation subgroup is therefore exactly the claimed one.

I checked the broader sequence actions rather than assuming the single-defect argument applies to every sequence. With \(s_y=1\), a possible symmetry has vertical offset \(4m\) and requires \(\epsilon_{j+m}=s_x\epsilon_j\). With \(s_y=-1\), the offset is \(4m+1\) and requires \(\epsilon_{m-j}=-s_x\epsilon_j\). The horizontal phase condition follows by substituting the row coordinates and recurrence. Constant or alternating sequences admit vertical screw periods; hence local homogeneity alone does not make **every** family member non-cocompact. For the single defect, reflection actions requiring a complemented cofinite sequence fail. The half-turn \((x,y)\mapsto(1/2-x,1-y)\) does preserve it, so this example has additional nontranslation symmetry rather than a trivial full group. The complementary defect has the corresponding half-turn with horizontal constant \(3/2\).

Finally a finite extension of horizontal translations cannot have a compact fundamental domain: the images of any compact set under finitely many representatives have bounded vertical coordinate, and horizontal translations cannot enlarge that bound. This rules out cocompactness of the **full** group, not just rank-two translation periodicity. The implication is universal and does not come from finite patch tests.

## Reproduction and genuinely fresh controls

All programs ran only in ignored temporary copies or this family's own directory, with standard-library rational arithmetic and no installation. The submitted verifier and its historical submitted copy both pass 16 rooted cases and reproduce the frozen receipt byte for byte. The historical independent verifier reproduces its 212 successful assertions / 64 rooted cases and its receipt byte for byte. Input/output hashes and exit statuses are in [reproduction_results.json](reproduction_results.json).

[New independently coded controls](new_controls.py) import neither submitted program. They reconstruct strips from parallelograms, calculate exact segment minima, encode active oriented half-planes of clipped faces, and canonically label collapsed edges by cyclic order. Vertex–edge–face incidences are compared, rather than only counts. All **158 checks**, including **128 rooted full-cell incidence comparisons** over six independent bits, shifted lower/upper roots and horizontal indices, pass. Symbols outside the six-bit range follow a different rule. The complete result is [new_control_results.json](new_control_results.json).

The fresh controls enlarge the row guard from 3 to 7; verify that deleting singleton traces changes the signature; preserve equality at squared radius 10 but distinguish the prior-layer canonical signatures at 10.01; test constant/alternating screw periods, the defect and complemented-defect half-turns, and reject nonzero single-defect symbol shifts from −8 through 8. At the claimed radius the signature has 8 vertices, 28 positive-length edges, 6 singleton edges, 23 positive-area faces and 4 singleton faces.

These tests are supporting falsifiable checks. The analytic height and cap inequalities establish infinite locality, and the intrinsic row and sequence argument establishes global symmetry. The larger-radius control shows that the particular canonical comparison fails; it does not prove that no other ball isometry could exist at every larger radius. No stronger radius theorem, strict diameter margin or universal global conclusion from finite samples is added.

## Pinned corpus, duplicate, budget and exact-history audit

The raw source corpus is pinned to revision **37e53eabe540fb458758e198be61634bd02ee008**. Both cached raw files match their recorded byte sizes and SHA-256 values. Among 15,458 records, the exact ID and code each occur once, and the normalized statement has only the same record. The full source payload and imported prior report match input_record.json and the SQLite copy literally. Keyword-related records and the related-target-group file contain no equivalent target found by this bounded comparison. See [corpus_checks.json](corpus_checks.json).

The imported report is literature triage: it reports no resolution and provides no proof. Its suggested remaining work does not turn the periodicity conclusion into an assumption. The saved catalog/readiness hashes and scope are consistent with that literal input. Accessible base history has no prior attempt folder for this ID. Current read-only GitHub ID/code searches find only PR24, and the only matching remote head is the audited head. These are bounded accessible-repository/corpus observations, not worldwide nonexistence claims.

Every one of the **16** frozen attempt files matches both the snapshot manifest and the exact head bytes. The candidate already existed at commit **612af5df300f940d30be4d78cfc84b7922469193**, 2026-09-30 04:27 UTC, with its current scientific hash. Subsequent commits document scope (04:31), add review (04:44), and edit the queue (04:49). The historical frozen header saying review was pending belongs to the candidate's earlier stage; the later review and status are explicit. No frozen history was rewritten. See [integrity_checks.json](integrity_checks.json) and [provenance_checks.json](provenance_checks.json).

The ledger records **1/5** substantive proof attempts within the original 04:13–06:13 UTC budget. Status and readiness keep the full source unresolved and new_discovery_claim false. This audit adds **zero** new proof-search turns and does not reset the original budget. No paper or release is supplied by this head.

## Concrete publication metadata repairs and remaining gap

The exact diff contains **17 paths: 16 attempt files and one shared QUEUE.md row**. The original PR body says only the attempt folder changes, and README says no shared queue changes. Both statements are false. The queue row changes queued 0/5 to an unsolved 1/5 note with the correct narrow mathematical scope. Current descriptions must name the queue change; preserved original snapshots must remain historical evidence.

At the exact head, state.json, history.jsonl and assessment_history.jsonl contain no record for 10000062, and the queue engine's allowed states do not include the handwritten label unsolved. Thus the historical queue edit is not a canonical state/turn transition. A present repair should record the scoped partial in the accepted state system and retain the already used 1/5, with transparent history. Parent owns this repair, the final current-head checks and any authorized Git/PR actions. This family performed none of those mutations.

The strongest verified outcome is the scoped Euclidean non-cocompact construction with a horizontal period and a complete metric-ball proof. The exact remaining source gap is the meaning of periodicity; the hyperbolic full-ball case is also unclassified. Priority remains bounded by the listed primary-source inspection and searches. Frettlöh–Garber hyperbolic corona results, Ahara–Akiyama–Hayashi–Komatsu rhombus configurations and Goodman-Strauss weakly aperiodic triangle tilings do not supply the omitted full-ball proof. Benjamini's [2026 fixed-source paper, v2](https://arxiv.org/pdf/2606.13271v2), addresses a different graph-metric approximation problem. No inference from those leads is promoted to a target result.

**Disposition:** accept the exact scientific artifact as a verified scoped partial, correct the current scope/queue metadata, preserve the historical records and attribution, and withhold full-source-solved or novelty promotion. Audit completion 100%; subjective original full-source discovery estimate remains 20%, with the exact gap stated above. No external individual was contacted; no installation, release, publishing, Git mutation, PR mutation or shared/canonical mutation was performed by this family.
