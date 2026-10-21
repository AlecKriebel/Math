# PR301: independent surface-construction adversary

Checkpoint UTC 2026-10-05; surface-family audit completion estimate 95%. Original snapshot head 125d90fa3f5a4f90b813fec7a7c0f1918914d885. The target is the literal terminating theoretical algorithm, not efficiency, full software, priority, or a new classification theorem.

**Verdict within this family: PASS, with no mandatory mathematical correction found.** The general matching, corner-sector, color, dual-polygon, triangulation, and certificate arguments are checkable in CHECKABLE_DERIVATIONS.md. No route in this audit transfers basis extraction to an unsupported equivalent oracle. This is one adversarial approach family; promotion still requires the parent's independent reproduction and overall source/priority gate.

## Strongest verified result

For every promised finite-dimensional gentle quiver, the local matching completion is effective and unique up to fresh blossom labels. Its lozenge quotient has only circle/interval links. Green is the input's white dissection, has no interior punctures, and cutting the red dual dissection gives disks with exactly one white boundary occurrence. The quotient has a finite rational triangulation by an explicit fan-and-subdivision construction. Finite cutting and neighborhood operations decide the submitted handle certificate; elementary surface classification and rational approximation guarantee eventual acceptance. Once properly cut, the signed-side winding rule is applicable. The supplied proof details are mathematical deductions separate from the accepted PPP and APS theorems.

## Primary source evidence

Read complete relevant bodies rather than abstracts: PPP §§2.1,3.1,4.1–4.2; APS §§2,3,4.1,6,7 (including classification proof); original workshop contribution printed pp161–164, PDF pages19–22. Key locations:

- PPP arXiv v2 pp2–3 Definition2.2: blossom construction. pp10–11 Definitions4.6/4.8, Proposition4.9 and Theorem4.10: lozenges, duality and inverse. pp11–12 Remark4.11: permitted paths, color punctures, boundary matching and genus. p12 Remark4.13 identifies this with the OPS surface.
- APS final pp8–10 Definitions3.7–3.9, Proposition3.11 and Proposition3.13: admissible marked surfaces and dual polygons. pp11–13 Lemmas3.16/3.18 and Proposition3.20: line field, signed rule, peripheral orientation. pp13–14 Definition4.1/Theorem4.3: quiver conversion and finite-dimensional iff no white punctures. pp19–27 Theorem6.1, Remark7.2, Theorem7.4/proof and Remark7.6: applicability and exact remaining computational question.
- Plamondon Problem3.4 printed p163 asks for an algorithm, without an efficiency or implementation requirement. Printed p162 imposes the finite-dimensional/no-white-puncture condition.

Exact fetched source SHA256 values match the immutable submitted SOURCE_HASHES:

| Local PDF | SHA256 |
|---|---|
| sources/ppp_arxiv_v2.pdf | 49026e4606c41d8729cfaad4395bb1ade989140aa44df99eedee6c9177b721ea |
| sources/aps_final.pdf | 42a3956f82fa7098dd37941c2d1bc5a767ad2a46afd6b3bb2b069c10db0c56f1 |
| sources/owr2020_3.pdf | b1be25a647257979a03e04e59a4c558b3d61e9dc6c9597de010eb9721ef66a6d |

The relevant PPP lozenge figures and APS disk/signed-side/orientation pages were also rendered and visually read. Extraction can lose negation strokes; the PDF figures and definitions were used to resolve that risk.

## Exact construction probes

surface_fixture_audit.py is a fresh finite-incidence checker. It creates lozenges, glues the precise colored sides, retains corner and edge occurrences, checks every vertex link, computes topology, cuts the dual arcs by disabling red gluings, and checks each cut polygon is a disk with one white mark. It independently derives peripheral winding from collar sectors. It does **not** implement general handle search or claim to be the proposed complete-invariant software.

The exhaustive universe is all arrow endpoint multisets on one or two labeled vertices, with arrow indices in lexicographic endpoint order and at most two incoming/outgoing incidences, and all quadratic relation tables passing gentleness and acyclic permitted-successor tests. It contains 25 finite inputs and 47 completion choices. Every choice passed; completion choices gave identical topological/color data. Selected additional three-vertex fixtures passed as well.

| Fixture | Surface (g,b,p) | White boundary counts | Boundary winding | Puncture winding |
|---|---|---|---|---|
| k, one isolated vertex | (0,1,0) | 2 | 2 | none |
| k × k | two copies (0,1,0) | 2 on each | 2 on each | none |
| one loop x with x²=0 | (0,1,1) | 1 | 1 | -1 |
| three-cycle, all length-two compositions related | (0,1,1) | 3 | 3 | -3 |
| two parallel arrows a,b:0→1, c:1→0, relations ac,cb | (1,1,0) | 1 | -2 | none |
| two-arrow fork | (0,1,0) | 4 | 2 | none |
| one-arrow A2 | (0,1,0) | 3 | 2 | none |

For all cases, peripheral winding sum equals 4-2(b+p)-4g. These probes test genuine quotient/corner/sector mechanisms rather than merely recomputing the stated invariant formula.

Full exact native command requests, source snapshots for each tested version, actual PID/start/end/time, full compressed stdout and stderr are under captures/. First run captures/surface_fixtures failed because the checker mistakenly required equal color counts on cut-open polygons, where red endpoint occurrences are duplicated. It is explicitly a checker bug, not mathematical evidence against the candidate. The corrected topology run is captures/surface_fixtures_corrected; final collar-sector run is captures/collar_sector_fixtures. Both exit0. The final detailed gluing witnesses are surface_fixture_results.json. An ancillary display-only JSON summary command had a syntax typo and was corrected; it changed no computation or artifact.

## Mandatory versus optional findings

**Mandatory:** none found in the surface/topology scope. The full connected classification and category product claims remain accepted source/application inputs, and the parent must judge the overall complete invariant independently. This audit supplies no priority certificate and no timing bound.

**Optional expository improvements:**

1. Fix the conversion deterministically as green=white/red=black from the local quiver rule, instead of suggesting a test that could sound like an unspecified recognition problem.
2. Spell out that a dissection arc concatenates two colored sides through an original quiver vertex; retaining the auxiliary blossom points as boundary subdivisions must not add algebra vertices or APS marks.
3. Include the rational fan-and-subdivision argument and a note that cutting splits sector occurrences, especially for self-loops and relation-cycle punctures.
4. Explain why every required peripheral collar crosses a dual arc on nonzero inputs; k's disk has two white and two black marks and one arc, while the empty-dissection one-white disk represents the excluded zero algebra.

These improve reproducibility. The submitted wording already points to the published construction and sufficient sector-preserving operations, so I do not classify their absence as a mathematical failure of this literal theoretical algorithm.

## Exact remaining gap

No unresolved construction/topology gap found. Remaining work is independent reproduction by the parent, review by other materially distinct families, overall classification-key/source-scope validation, and priority review. Computational coverage does not establish the universal claim; the general deductions do the universal work. No historical independent review was consulted, no original file was altered, and no Git/index/remote/shared-control/external communication action was taken.
