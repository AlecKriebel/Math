# Independent adversarial review:30003955

**Verdict: PASS for the stated partial results and unresolved disposition.** No proof of the unrestricted OWR question is supplied or certified. No mathematical correction is required before an explicitly unresolved partial-result PR. This is an independent AI audit, not external peer review or a novelty certificate.

Reviewed artifact: `PARTIAL.md`, SHA256 `ab85b2029c8f4e0e931aeac63ea42aad1a6a2e34f7425428e1f9224fd5bddd43`. A byte-identical snapshot is retained as `reviewed_partial.md`. Review performed2026-09-30, gpt-6-astra, xhigh. The author’s source artifact was not edited.

## 1. Source and scope

The first requested problem-page lookup was unavailable. I then independently checked the original [OWR40/2018 report](https://publications.mfo.de/bitstream/handle/mfo/3662/OWR_2018_40.pdf?isAllowed=y&sequence=1), Problem12, printed p2528, including its rendered page. Gekhtman asks about an essential-boundary four-holed sphere with disconnected lifted interior, then asks the pants variant and offers regular covers as an optional restriction. The mathematical target in the artifact matches this text.

The conventional closed oriented surfaces denoted by \(S_g\) are used throughout. “Essential boundary” means that each boundary curve is noncontractible in the ambient closed surface. The source does not require the boundary components to be pairwise nonisotopic. This matters: the two sides of a cut nonseparating curve are parallel in the ambient surface but remain essential. Adding a pairwise-nonisotopic condition would change the statement and could invalidate genus-two examples.

The review certifies these sufficient hypotheses only:

- a nontrivial cyclic intermediate cover;
- intransitivity of every at-most-three-generated monodromy subgroup;
- base genus \(g\ge2|G|\), where \(G\) is the finite monodromy image.

All other cases remain outside the proof. In particular, a proper image subgroup is not enough for an irregular cover.

## 2. Monodromy and passage between subsurfaces

The component/orbit criterion is correct for both regular and irregular covers. Restrict the covering to the connected interior of a subsurface. Every lifted component meets the fiber over a chosen interior base point, by path lifting. Two fiber points are in the same component exactly when the lift of a based loop joins them. Thus components are precisely the orbits of the restricted monodromy image. Changing the connecting base-point path conjugates the image and relabels the same orbit structure.

In a regular degree-\(d\) covering the monodromy action is regular, up to the standard left/right-action convention, and a subgroup \(A\) has \([G:A]\) orbits. Properness is then equivalent to intransitivity. The negative control in §5 correctly shows why this implication fails in an irregular action.

The factor-cover implication also has the correct direction. If the intermediate preimage has two or more components, their preimages in the total cover form disjoint nonempty relatively open-and-closed sets. Surjectivity ensures none disappears. The reverse direction is not asserted.

An essential-boundary four-holed sphere is incompressible in the ambient closed surface. A curve dividing its four boundary circles into two pairs is nontrivial in its fundamental group, hence essential in the ambient surface. Either resulting pants subsurface therefore has essential boundary. Its monodromy subgroup is contained in a conjugate of the four-holed-sphere image, so restriction cannot merge orbits. The four-holed conclusion indeed implies the pants conclusion under each sufficient condition.

## 3. Cyclic-factor argument

The reduction to a prime cyclic quotient is sound. A connected prime cyclic cover corresponds to a nonzero character on first homology modulo\(p\). Scaling one nonzero coordinate to1 and choosing integer coordinate lifts with that coordinate exactly1 produces a primitive integral class. Poincaré duality gives a primitive integral homology class. On a closed oriented surface, primitive homology classes are represented by nonseparating simple curves; this follows from the integral symplectic basis theorem and realization of symplectic basis changes by surface homeomorphisms.

Let \(c\) be that curve. The character vanishes on every loop disjoint from\(c\), because it is algebraic intersection with\([c]\) modulo\(p\). Extend\(c\) to a cut system. The collar complement is connected, genus0, and has\(2g\) boundary components; every boundary is essential. Its fundamental group maps trivially under the cyclic character. A central planar subsurface obtained by dividing those circles into four nonempty groups is a four-holed sphere. Each of its boundary loops is nontrivial in the cut-system complement, whose inclusion is injective on fundamental groups, so the ambient essentiality claim follows. The\(g=2\) case uses the entire four-holed complement and is valid.

The restricted cyclic covering is trivial and has\(p\) components. The factor argument proves the claimed result for the original covering. The statements about nonperfect and solvable regular deck groups follow from their nontrivial abelianization. The artifact correctly declines to extend this merely from nonperfect monodromy in an irregular action: the point stabilizer must lie in the kernel of the cyclic character to obtain the needed intermediate cover.

## 4. Generator counts

A sphere with\(b\) boundary components has free fundamental group of rank\(b-1\). Therefore rank3 is correct for the four-holed case and rank2 for pants. In a regular action, a group requiring more than three generators cannot be the image of the former, and more than two suffices for the latter. Essential four-holed spheres exist for every\(g\ge2\), including parallel-boundary realizations when necessary. No converse is claimed.

## 5. Detailed audit of the large-genus construction

This is the most geometric part and is valid as written. The following expands its implicit surface facts.

### 5.1 A killed nonseparating curve in a genus-\(m\) handle block

For \(m=|G|\), choose the usual disjoint handle curves with based paths in an embedded tree in their complement. These are geometric generators, not arbitrary representatives of homology classes. If one image is the identity, that handle curve works. Otherwise the\(m\) images lie among\(m-1\) nonidentity elements, so two based images agree.

For the equal pair, thicken the unique connecting tree arc to a narrow band, with its interior disjoint from all selected curves. Band-summing the first curve with the reverse orientation of the second gives a simple closed curve freely homotopic to the based product\(a_j a_k^{-1}\), up to overall conjugation and orientation. The use of the same embedded tree for based representatives and the band is important: it avoids an uncontrolled extra conjugating element between the factors. The artifact supplies this requirement. Its monodromy is therefore trivial.

Its homology is\([a_j]-[a_k]\), a nonzero primitive vector in the independent handle classes. A separating curve has zero homology, so the constructed simple curve is nonseparating in the handle block. No assertion that arbitrary equal-image loops admit a simple product is being used.

### 5.2 Two disjoint blocks and the genus-two subsurface

When\(g\ge2m\), two disjoint one-boundary genus-\(m\) blocks can be chosen using the standard connected-sum decomposition. Even at equality their exterior is an annulus, so there is no loss of a connecting region. The two killed curves lie in different blocks and are disjoint. Each has a simple dual intersecting it once within its own block; the regular neighborhood of the pair is a one-holed torus.

The complement of the interiors of these two one-holed tori is connected. Join their distinct boundary components by a properly embedded arc in this complement. A narrow band along the arc, together with the tori, has a genus-two regular neighborhood with one boundary component. Cutting along an arc joining distinct boundary components leaves the exterior connected. Thus the exterior of the resulting genus-two subsurface has genus\(g-2\) and one boundary. Since\(m\ge2\), the bound ensures\(g\ge4\); neither side of its boundary is a disk.

### 5.3 Five holes, trivial image, and essentiality

Cutting along the two killed curves, one in each handle, leaves a connected five-holed sphere\(F\): cutting preserves Euler characteristic\(-3\), adds four boundary components, and removes both handles. Four boundary loops are conjugates of the killed curves or their inverses. These four generate\(\pi_1(F)\), since its fifth boundary is their inverse product. Hence the whole image is trivial.

Inside\(F\), cut off pants containing the two boundary copies of the first killed curve. The remaining component is a four-holed sphere\(H\). Its boundaries are the two copies of the second killed curve, the old genus-two boundary, and the newly introduced separating circle. The first two are essential because the original curve is nonseparating; the old boundary separates genus2 from genus\(g-2\); and gluing the first pair of boundary copies back together turns the removed pants into a one-holed torus bounded by the new circle. That circle therefore separates genus1 from genus\(g-1\), and is essential. All four boundaries pass the source requirement.

The inclusion\(H\subset F\) preserves trivial monodromy, so the full degree-\(d\) cover restricts to\(d\) separate copies. The numerical consequences\(|G|\le d!\) for any monodromy action and\(|G|=d\) for a regular action are correct. These are coarse sufficient bounds only.

## 6. Negative control and literature obstruction

I independently reconstructed the\(S_3\) example. The two commutators multiply to the identity, the image is\(S_3\), and the pants image is\(A_3\). It has two orbits in the regular six-point action and one orbit in the natural three-point action. The genus calculations follow from\(h-1=d(g-1)\). This is a valid counterexample to descent of disconnectedness for a fixed subsurface, not to the general existence question.

The cited [Funar–Pagotto paper](https://arxiv.org/abs/2004.09174), v2, Theorem1.2 and §5.2, does state existence of finite simple characteristic quotients with no essential simple-loop class in their kernels. I checked those passages independently. Consequently a strategy requiring *trivial* monodromy on an essential planar subsurface cannot work for every cover. There is no contradiction with the desired disconnectedness: a nontrivial proper subgroup suffices in a regular action. This source limitation is used correctly.

A bounded independent search found the original question and relevant nongeometric-kernel literature, but no general resolution. This does not certify exhaustive open status or originality of these sufficient conditions.

## 7. Independent checks and final disposition

The original31-assertion checker was inspected. Independently written `independent_checks.py` verifies all subgroups of\(S_3\) and\(S_4\) in regular/natural actions, the explicit surface relation,782 primitive character lifts,50,068 pigeonhole tuples, and Euler/gluing controls for genera4–30. All53,830 exact assertions pass. Large counts here are repeated elementary controls, not thousands of independent proof ideas.

Computation does not establish geometric embeddedness or boundary essentiality; those are supplied by the written audit above. No mandatory correction was found. The exact frozen partial artifact passes for its stated scope and is suitable for publication only with the unresolved general-case status and unconfirmed novelty preserved.
