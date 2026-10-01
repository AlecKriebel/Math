# Exact source gate: 10400196 / AMR-103-0196

Source checked 2026-10-01. The truncated imported title is Deloup's Question 10.21, Ohtsuki's *Problems on invariants of knots and 3-manifolds*, printed p.526 (PDF page154). The whole subsection 10.3.2 and preceding finite-type definitions were read; the question page was inspected visually. The pinned record and its prior OPEN-TRIAGE report were read. That report contains no prior proof attempt.

The question seeks a mod-16 lift of the Gauss–Brown phase associated with a Spin^c structure, motivated by a degree-one invariant in Spin^c Goussarov–Habiro theory. It is not an unqualified request to reproduce the classical spin Rochlin invariant. Its notation is abbreviated: a normalized phase lies in Q/Z; multiplying by eight gives the Brown normalization in Q/8Z. For nonhomogeneous quadratic functions the Brown value need not be an integer modulo8, so a general rational mod-16 lift has codomain Q/16Z. The integral spin case alone permits Z/16Z.

## Required distinctions

1. The published Deloup–Massuyeau paper, Topology44(2005),509–555, canonically associates a quadratic function on H2(M;Q/Z) to every closed oriented Spin^c three-manifold. It descends to the finite group Tor H1(M;Z) when the Chern class is torsion, including all rational homology spheres. General non-torsion structures require care: their finite-section Gauss sums need not be independent of the section. The short problem must not silently be treated as a canonical finite sum on every Spin^c structure.
2. A bare pointwise lift can be chosen by taking representatives. Since the canonical finite Gauss phase is Y^c_1-invariant, such a phase-only lift is still degree zero. It does not provide the intended new order-one information. Connected-sum additivity and recovery of the spin Rochlin invariant are natural possible requirements, but the short question does not spell them out. Results using either extra requirement must state it.
3. Deloup–Massuyeau Example3.5, printed p.554, already proves that the classical spin Rochlin invariant does not descend along Spin→Spin^c on all three-manifolds. On T³ two spin structures have the same Spin^c image but Rochlin values8 and0. This known fact settles that stronger descent requirement. It does not by itself rule out a lift of the mod8 Gauss phase with different spin values.
4. Their Definition3.3 gives degree at most d by vanishing of alternating sums over d+1 disjoint Y-surgeries. Their Theorem2 and Corollary2 classify degree-zero Spin^c data. No arbitrary equivalence between Y2-classification and degree-one invariants is assumed.

The primary 2005 paper and the source subsection are the initial mathematical inputs. A current targeted primary-literature search also found the later Massuyeau surgery-equivalence survey and related torsion/Floer work, but no verified theorem answering the exact intended lift. That bounded search is not a novelty or historical-openness certificate. The existing non-descent example and all classical Gauss-sum inputs are credited. No outreach is permitted.

## Prior campaign gate

Exact-ID and exact Deloup/Question10.21 all-state PR searches, both established main target-directory histories, the local all-ref target log, both usual remote branch prefixes, and the related-target grouping returned no earlier exact campaign attempt. The broader mod16/spin PR query found unrelated PR16 (embedding dimensions), not coverage of this target. QUEUE rank286 is queued0/5, but that alone was not used as the gate. Source triage consumes no author turn; the first substantive algebraic attempt is recorded separately.

Only the attempt's public mathematical notes and checks may be checkpointed. Full source PDFs/text/images and imported records are reading copies outside the packet. No original-target resolution is claimed at this stage.

## Turn2 convention clarification

Massuyeau’s primary spin paper, Lemma12, states B(phi)=-R modulo8; the published Deloup–Massuyeau boundary convention agrees with it. Ohtsuki’s abbreviated sentence uses the positive relationship. Turn2 carries an explicit sign epsilon and gives the construction in either convention; it does not silently identify the two quadratic functions. The sign exchange leaves the Turn1 isometry and nonexistence argument unchanged. The actual source’s omission of finite-phase domain and additivity hypotheses continues to be disclosed.
