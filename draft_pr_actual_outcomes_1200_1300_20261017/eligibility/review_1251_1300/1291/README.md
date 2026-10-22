# Local tangent-line models of symplectic surfaces

Problem **6000010 / AMR-059-0010**. This packet gives a complete local characterization in **real dimension two**, under the explicitly defined canonical symplectic/statistical Codazzi tangent-bundle construction.

## Accepted result

For a positive compatible symplectic surface \((N,\omega,J)\), set \(g(U,V)=\omega(U,JV)\). A neighborhood of a chosen point \(p\) is isomorphic, preserving both \(\omega\) and \(J\), to an open part of the tangent bundle of a Riemannian interval with a torsion-free statistically compatible affine connection **if and only if** there is a local Killing field \(X\) for \(g\) with **\(X(p)\ne0\)**.

The original question uses “compatible” without defining it there. This report adopts the explicit canonical symplectic construction and the statistical Codazzi condition, supported by a direct tensor calculation and Satoh's treatment. It does not resolve other unspecified interpretations or the unrestricted-dimensional problem. No novelty claim is made.

## What the proof includes

- Both directions, including all mixed and derivative terms, positive definiteness, orientation, and recovery of the almost complex structure.
- The distinction between a field nonzero at the chosen point and a merely nontrivial local Killing field. A rotational example has no tangent-line model at its center even though it has one at every nearby noncentral point.
- The necessary curvature diagnostic \(dK\wedge d|\operatorname{grad}K|_g^2=0\), an explicit failure example, and proof that vanishing of this diagnostic is not sufficient.
- The exact locally-flat restriction when the base connection is required to be Levi-Civita, and local models at every point of every constant-curvature surface.
- The higher-dimensional torsion/curvature formula, with no higher-dimensional converse, global recognition theorem, or current-literature-status claim.

## Contents

- [Full proof](PROOF.md)
- [Mathematical audit](AUDIT.md)
- [Acceptance and artifact bindings](ACCEPTANCE.json)
- [Public source metadata](SOURCE_PINS.json)
- [Aggregate verification results](CHECK_RESULTS.json)
- [Public artifact manifest](MANIFEST.json)

## Evidence and limits

The proof is self-contained. The mathematical audit reconstructed it independently and checked the original problem and relevant Satoh definitions directly. Existing symbolic and integrity checks were rerun successfully with Python normal, -O, and -OO modes. Source-document bytes were matched to their recorded hashes. These checks are supporting evidence, not formal proof certification or external human peer review.

The public files contain authored mathematics and public bibliographic and aggregate verification metadata. No copied source documents, source extracts, datasets, or checking scripts are included.

## Primary references

1. Hitoshi Furuhata, Hiroshi Matsuzoe and Hajime Urakawa, *Open Problems in Affine Differential Geometry and Related Topics*, Interdisciplinary Information Sciences 4 (1998), 125–127. Takashi Kurose's question is item 3(d), printed p. 126. [Original PDF](https://www.jstage.jst.go.jp/article/iis/4/2/4_2_125/_pdf/-char/en).
2. Hiroyasu Satoh, *Almost Hermitian structures on tangent bundles*, arXiv:1908.10824v2, 21 March 2025. The relevant locations are Definition 2.1 and equation (2.3), p. 4, and Theorem 3.1, p. 8. [Pinned-version PDF](https://arxiv.org/pdf/1908.10824v2).
