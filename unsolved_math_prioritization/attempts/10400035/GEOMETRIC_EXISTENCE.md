# Geometric existence lemma for the ordinary two-string category

## Result

There exists an ordinary smooth ordered two-string link `L = L_1 union L_2` in `D^2 x [0,1]`, with the prescribed endpoints `(p_i,0)` and `(p_i,1)` and with each component oriented from bottom to top, such that:

1. its actual three-dimensional exterior is a genus-two handlebody, hence its actual fundamental group is the free group `F_2`; and
2. the standard individual closure of `L_1`, after forgetting `L_2`, is a trefoil. In particular its ordinary Conway coefficient is `a_2(L_1)=1`.

This is a **source-backed existential lemma with a complete primary drawing recovered**, followed by an explicit category-conversion argument. It is not a claim that a complete marked Wirtinger presentation or a Milnor-invariant vector was independently calculated from that drawing. No linking number, longitude, or Milnor coefficient is assigned here.

## Primary source and exact scope

Joao Miguel Nogueira, *Prime knot complements with meridional essential surfaces of arbitrarily high genus*, Topology and its Applications 194 (2015), 427-439, DOI `10.1016/j.topol.2015.05.088`.

The retained author preprint is arXiv:1706.03719v1, https://arxiv.org/pdf/1706.03719v1. Its Section 2, PDF page 2, defines free tangles using the **actual** complement group or, equivalently, handlebody exterior. Its Appendix, Section 4, PDF pages 13-14, supplies a proper two-arc tangle in a ball whose first capped arc is a trefoil and whose exterior is a handlebody. The second capped arc is identified there as a `(3,-4)` torus knot; that additional identification is not needed for this lemma. The original ambient category is PL, expressly stated on PDF page 2.

The missing arXiv Figure 13 was recovered in the author's institutional primary preprint:

- Joao Miguel Nogueira, *Knot complements with meridional essential surfaces of arbitrarily high genus*, Universidade de Coimbra departmental preprint 14-09, received February 27, 2014.
- Direct PDF: https://www.mat.uc.pt/preprints/ps/p1409.pdf
- Verified departmental listing: https://www.mat.uc.pt/preprints/2014.html, entry 14-09.
- Appendix Section 4 is on PDF/printed pages 14-15; the complete relevant drawings are Figures 9 and 10 on page 15. Figure 10 is the construction corresponding to arXiv Figure 13. The same trefoil, tunnel-slide, and handlebody assertions appear in this appendix.
- The PDF page was rendered and visually inspected. Figure 9(a) displays the black first arc with the trefoil pattern; Figure 9(b) marks its tunnel. Figure 10(a) indicates sliding the tunnel ends; Figure 10(b) displays the resulting black first arc and blue second arc, each proper in the depicted ball. Artwork is present, with crossings shown by interrupted understrands.

The author's research page https://www.mat.uc.pt/~nogueira/Research.htm independently identifies the published article and its journal/pages. The publisher article endpoint returned HTTP 403 during this pass. Therefore no publisher-PDF retrieval or byte-for-byte equivalence with the 2014 or 2017 files is claimed. The 2014 preprint and 2017 arXiv version have different titles and other revisions; the appendix construction, rather than equality of their full articles, is the relevant agreement.

The appendix result is an unnumbered construction, **not** the paper's numbered Theorem 1. Its required hypotheses are just those of the displayed tangle: two disjoint properly embedded PL arcs in a PL ball, with the first capped arc trefoil and the indicated unknotting tunnel. Essentiality, primeness of some subsequently constructed knot, and the main theorem about essential surfaces are not hypotheses needed here. The handlebody conclusion follows in the appendix from the unknotting tunnel and the displayed slide. We cite that verified construction; we do not replace its tunnel argument with an assertion that every arbitrary two-tangle is free.

## Conversion to the exact ordinary string-link category

Let `(B,s_1 union s_2)` be the tangle in the appendix. Retain its component labels. Write the distinct endpoints of `s_i` as `q_i^-` and `q_i^+`; either choice of the two endpoints is allowed, but make the choice once and retain it.

### 1. Smoothing and boundary marking

A finite PL arc system in a PL three-ball is tame. Identify the ball with a standard ball, round each polygonal corner in disjoint sufficiently small balls, and straighten the arcs in disjoint boundary collars. This produces a smooth proper arc system ambient isotopic to the PL one; thus neither the complement homeomorphism type nor either capped-arc knot type changes. This uses ordinary local smoothing of a tame one-dimensional embedding in dimension three, and does not assume anything about its knots or group.

Regard `C=D^2 x [0,1]` with its corner rounded away from the prescribed endpoints as an oriented ball. Choose an orientation-preserving ball identification `B -> C`. Its four endpoint images are four distinct boundary points. An orientation-preserving isotopy of the boundary sphere moves this ordered configuration to

`q_i^- -> (p_i,0)` and `q_i^+ -> (p_i,1)`, for `i=1,2`.

For example, move the four points successively along simple paths avoiding the other current points, with isotopies supported in thin neighborhoods of those paths; temporary spare positions avoid occupied destinations. Such surface isotopies extend into a boundary collar of the ball. Composing gives an orientation-preserving ball diffeomorphism `h` with the specified endpoint images. Choose and fix one such `h`. Small disjoint endpoint-collar isotopies make the image arcs standard straight vertical segments near their ends.

Parametrize each image arc from `(p_i,0)` to `(p_i,1)` and orient it in that direction. This produces an ordinary ordered fixed-endpoint string link. All subsequent isotopies in this category fix the boundary. The initial choice of a marking is construction data; no quotient by changes of marking is imposed.

Here **upward means the component orientation from the bottom endpoint to the top endpoint**. It does not impose monotonicity of the height coordinate along an entire component. Requiring such monotonicity would be an additional braid hypothesis, absent from the ordinary string-link definition and false for the trefoil component here.

### 2. Actual exterior and its rank

The diffeomorphism `h` and the collar isotopies carry regular neighborhoods to regular neighborhoods up to isotopy. Consequently the compact exterior of `L` is homeomorphic to the compact exterior of `s_1 union s_2`, which the cited construction proves is a handlebody.

Its boundary is obtained from the sphere `boundary B` by deleting four small endpoint disks and gluing the two lateral annuli of the regular neighborhoods of the arcs. It is connected and has Euler characteristic `2-4=-2`; hence it is a closed orientable surface of genus two. A handlebody with this boundary is a genus-two handlebody, retracting onto a bouquet of two circles. Thus

`pi_1(C minus L) = pi_1(C minus interior N(L)) is isomorphic to F_2`.

The first equality denotes the natural isomorphism coming from regular-neighborhood deformation, not a literal equality of spaces. No nilpotent completion is being substituted. No assertion that standard bottom meridians form an abstract free basis is needed or made.

### 3. Individual closure survives the chosen marking

First forget `s_2`. A boundary cap for `s_1` is a simple arc `c` on the unpunctured sphere `boundary B` joining its two endpoints, with interior disjoint from `s_1`. Then `s_1 union c`, with a small outward push of the cap and corners rounded, is Nogueira's knot `K(s_1)`.

Any two simple arcs on a sphere joining the same two points are isotopic relative to those points when there are no additional punctures to avoid. Equivalently, a regular neighborhood of either cap is a disk, and the complementary region in the sphere is also a disk; the elementary bigon-removal argument gives the relative isotopy. It follows that the capped knot type of a single proper arc is independent of its cap. This statement is used **after the other component is forgotten**. It does not assert that all cap systems are isotopic on a four-punctured sphere or that a two-component closure is independent of boundary marking.

The map `h` sends `c` to a boundary cap for `L_1`. Extend the orientation-preserving ball map across the outside ball (or extend the boundary isotopy by a collar). The capped knot remains the trefoil. The standard individual closure used for a string-link component employs a boundary-parallel outside arc; it is isotopic, after forgetting `L_2`, to a small outward push of a boundary cap. Cap independence therefore identifies it with the image of `K(s_1)`. Endpoint-collar straightening does not change it.

Reversing a component orientation does not change its Conway polynomial. Even an accidental mirror choice in identifying a drawing would not affect `a_2` of a trefoil; however the construction above already specifies an orientation-preserving ball map. The normalized trefoil Alexander polynomial is `t-1+t^(-1)=1+(t^(1/2)-t^(-1/2))^2`; with `z=t^(1/2)-t^(-1/2)` its Conway polynomial is `1+z^2`. Hence `a_2(L_1)=1`.

This argument works for **every** chosen orientation-preserving boundary marking sending one endpoint of each labeled arc to its required bottom point and the other to its required top point. Pairwise linking and Milnor data can depend on that marking. The free exterior and the individual first-component value do not.

## What this establishes, and what remains external

The geometric existence claim is available for use in the first proof. The complete primary drawing supplies the necessary visual source evidence. A theorem-level existential argument is enough when the remainder of a proof uses only freeness and the first component's `a_2`, and either matches linking symbolically or proves an assertion for every marking.

This file does not supply a certified explicit marked crossing list, a Wirtinger simplification, a numerical linking number, or any Milnor-invariant computation. A later proof needing any of those must obtain it separately. The appendix's assertion about the second component is not independently checked here and is unnecessary. This lemma alone settles neither of Stanford's two questions. It gives no invariant vanishing on **every** free-exterior string link.

## Retention and precise text locations

- ArXiv PDF: 420491 bytes; SHA256 `6426f07a35c87d985429361e85d8d8528d05154b2ec10db0d84cdb5584fe848b`.
- ArXiv text lines 83-84: PL category; 87-92: actual-group and handlebody definition; 669-675: appendix and first trefoil; 690: missing artwork marker; 696-705: tunnel slide, second arc and handlebody proof.
- Coimbra PDF: 305322 bytes; SHA256 `455b0187bbf9b8214022236ac7a949ecdc5e3a13f7e92aec802ed6d9f9f6d98b`; 16 pages, retrieved with HTTP 200 on 2026-10-09.
- Coimbra retained layout text lines 551-571: appendix statement, exact free-tangle definition, cap definition, trefoil and tunnel-slide construction, handlebody argument. Lines 581-592: captions of complete Figures 9 and 10. Lines 595-597 finish the essentiality argument, which is not used here.
- PDF identities and the historical visual-inspection record are summarized in SOURCES.json; the underlying source and local inspection artifacts are not included.

Copied source PDFs, extracted text, and rendered source artwork remain private supporting evidence. This authored mathematical lemma and public bibliographic metadata are separate from those source bodies. No repository publication, remote mutation, or queue edit was performed in this task.
