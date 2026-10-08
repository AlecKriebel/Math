# Source and scope audit

Audit date: 8 October 2026. Problem 10300008 / AMR-102-0008.

## Exact primary target

Danny Calegari, *Problems in foliations and laminations of 3-manifolds*,
arXiv:math/0209081v1, 8 September 2002, printed page 10, Question 4.2.
Journal reference supplied by arXiv: Proceedings of Symposia in Pure
Mathematics 71 (2003), 297--335.

Primary links: https://arxiv.org/abs/math/0209081v1 and
https://arxiv.org/pdf/math/0209081v1 .

The task concerns a prescribed collection of taut foliations of a
three-manifold. It asks for obstructions to one Riemannian metric making the
collection leafwise minimal after isotopy. Mean curvature zero is intended;
this is not the dynamical use of minimality meaning density of every leaf.
The metric is allowed to change. The question does not itself specify a
finite index set, add coorientability, or impose a hyperbolic metric.
The surrounding preceding remark discusses C2 regularity. Our theorems use
smooth, oriented, cooriented data, and flag that narrower scope.

The phrase about isotopy is not formalized further in the question. We
investigate the independent-isotopy interpretation and explicitly distinguish
the common-ambient-isotopy variant. The primary remarks give a PL
recurrent-weight observation for sufficiently close plane fields and discuss
replacing foliations by monotone-equivalent laminations. Neither statement is
a proved smooth common-metric classification. The full PDF was downloaded,
extracted, and printed page 10 was rendered and visually inspected.

## Corpus reconciliation and mathematical corrections

The full local problems and research-results corpus files were rehashed and
joined on AMR-102-0008 after checking uniqueness. Both hashes match the
recorded immutable revision 37e53eabe540fb458758e198be61634bd02ee008. The
complete selected problem and report were inspected. The wording agrees with
the primary question; the report contains literature-search triage, not an
authored substantive proof attempt. See the metadata-only corpus bindings.

The imported summary needs the following corrections:

1. For a surface foliation in dimension three, the characteristic calibration
   is a two-form, not a three-form. The ambient volume is a three-form.
2. Simultaneous minimality supplies one characteristic form per foliation;
   a single form calibrating different tangent planes is not necessary.
   Route 1 proves this directly using the flat three-torus.
3. The dedicated Sullivan minimal-foliation characterization is the 1979
   paper below. His 1976 *Cycles for the dynamical study of foliated manifolds
   and complex manifolds* is a different foundational article.
4. *Minimal surfaces in foliated manifolds* (1986), pages 1--32, is by Joel
   Hass alone. A Hass--Thurston authorship attribution is incorrect.
5. No theorem about incompatibility for a generic metric establishes
   nonexistence after choosing some metric and isotoping the foliations.

## Credited literature and inspected scope

- Dennis Sullivan, *A homological characterization of foliations consisting
  of minimal surfaces*, Commentarii Mathematici Helvetici 54 (1979),
  218--223, https://doi.org/10.1007/BF02566269 . The author's bibliography
  https://www.math.stonybrook.edu/~dennis/publications/ verifies title and
  bibliographic data; primary indexed text supports the characteristic-form
  calculation. A complete local text inspection of the scanned paper was not
  achieved. No uninspected general theorem from it is needed for our new
  arguments: equation (1) and its consequences are proved directly.
- Joel Hass, *Minimal surfaces in foliated manifolds*, Commentarii
  Mathematici Helvetici 61 (1986), 1--32,
  https://doi.org/10.1007/BF02621899 . Authorship/pages are corroborated by
  Calegari's reference 67 and Hass's own publication list:
  https://www.math.ucdavis.edu/~hass/Research/HassPublicationsGrouped.pdf .
  A complete local copy of the article was not inspected. It is not used as
  a black-box simultaneous-existence theorem.
- Hoan Nguyen, *Minimal foliations, codimension-one stable norms, and a
  question of Bangert*, https://arxiv.org/abs/2608.18428v2 , revised
  22 September 2026. The full PDF was downloaded and extracted; Theorem 1.2,
  its hypotheses, and the acknowledgement of overlapping independent work
  were inspected. It gives positive families of calibrated torus foliations,
  not arbitrary prescribed foliations on arbitrary three-manifolds. The
  arXiv record observed in this audit lists a preprint and no journal
  publication. No refereed-status claim is made.
- Fernando C. Marques, Andre Neves, and Ao Sun, *Rigidity and non-rigidity of
  the stable norm on T^n*, https://arxiv.org/abs/2608.15376v1 , submitted
  15 August 2026. Its full PDF was downloaded and extracted, and Theorem 5.1
  and the surrounding cofactor ansatz were inspected. This independently
  supplies related positive torus families. The observed record is a
  preprint; no journal or peer-review status is inferred.
- Barbot--Fenley--Potrie, *On transverse R-covered minimal foliations*,
  https://arxiv.org/abs/2501.14489 , with v2 dated 25 June 2026. The primary
  HTML explicitly uses minimality for dense leaves. It therefore cannot be
  substituted for the zero-mean-curvature problem. Only the relevant
  terminology/statement was inspected, not every proof.

## Prior-attempt and semantic-duplicate gate

Read-only GitHub PR searches in AlecKriebel/Math for the exact ID/code,
simultaneous minimality, Question 4.2, taut foliations, and minimal surfaces
found no prior substantive attempt at this target. Branch searches for the
ID, minimal, foliat, calibration and simultaneous were inspected through
their returned terminal cursors. The default-branch attempts directory
contains no 10300008 entry. Exact-ID/default-branch code searches returned
no match. A recursive-tree read failed in transport; the smaller attempts
directory read succeeded. The historical problems/ path returned 404.

Relevant nearby results are different targets:
- https://github.com/AlecKriebel/Math/pull/858 : KP-3.18 asks about a closed
  hyperbolic manifold with a minimal foliation in its hyperbolic metric.
- https://github.com/AlecKriebel/Math/pull/184 : Calegari Q10.6,
  Godbillon--Vey bounds.
- https://github.com/AlecKriebel/Math/pull/801 : Calegari Q8.3,
  R-covered foliation existence.
- https://github.com/AlecKriebel/Math/pull/720 : a complex-algebraic foliation
  conjecture, not this three-dimensional Riemannian common-metric problem.
- https://github.com/AlecKriebel/Math/pull/691 : a different Question 4.2
  about hyperbolic conformal boundary.

The adjacent Calegari Q4.1 corpus report discusses a SINGLE foliation's
metric space and contains search-only triage. Its exact-ID PR search was
empty. The complete problems corpus was scanned for minimal-foliation and
simultaneous-foliation targets; no same-target substantive report was found.
These bounded negative findings do not prove absence of unpublished work or
an unindexed semantic equivalent.

## Current-status limit

Queries included exact simultaneous-minimality wording, Calegari Q4.2,
common metrics for taut foliations, calibration compatibility, and dated
2025--2026 variants. Recent positive torus work was identified and credited.
No source inspected here claims a complete answer to this prescribed-
foliation obstruction question. This is a bounded search result, not proof
that the question remains open globally. The accurate outcome is that our
five-route investigation does not solve it.
