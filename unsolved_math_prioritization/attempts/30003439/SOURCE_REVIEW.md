# Source dependencies and claim boundaries

Problem 30003439 / OWR-15219-008 asks for an algebraic convex cone with a
negative-curvature normal barrier that is not a hyperbolicity cone. The
accompanying complete analytic proof provides exactly that example in the
original three-dimensional space.

## Source roles

1. Tunçel's contribution to Oberwolfach Report 14/2017, printed pp. 797–800,
   gives the target on p. 799 and its homogeneous-polynomial definition of
   algebraicity. [Report DOI](https://doi.org/10.4171/owr/2017/14)
2. Nesterov–Tunçel gives the scalar self-concordance and negative
   third-derivative-curvature conventions. Its dual-cone example is not
   used as a shortcut to a barrier on the primal cone.
   [Preprint](https://arxiv.org/abs/1412.1857)
3. Dahl–Tunçel–Vandenberghe uses the matrix self-concordance convention
   and equivalent concavity of fixed cone-direction gradients. The proof
   includes a direct mixed bound matching that convention. The broader
   every-regular-cone existence question remains outside the theorem.
   The recorded inspection was of arXiv v2 dated 12 June 2026 and the
   author-hosted PDF internally revised 16 June 2026.
   [Version record](https://arxiv.org/abs/2509.10263)
4. Hildebrand's Theorem 3.2, family 5, already contains the exact one-sided
   cone: p=3, q=3/2, with (x1,x2,x3)=(x,z,y). The cone is not claimed to
   be new. That paper's hyperbolic affine spheres do not assert polynomial
   hyperbolicity of this cone, and no affine-sphere result is imported
   as a barrier theorem. [Source](https://arxiv.org/abs/1305.4814)

## What is proved directly

The full manuscript proves regular algebraic convex geometry, positive
Hessian, boundary blow-up, scalar and mixed self-concordance, logarithmic
homogeneity with parameter 100, and the universal negative-curvature
inequality. Exact matrix/minor and square identities cover all cone
rays, including the singular t=1 direction and the e_x endpoint.
An irreducible boundary-divisibility argument and a nonreal-root
obstruction exclude every homogeneous hyperbolic defining polynomial
in the same space, rather than only excluding the displayed cubic.

These analytic arguments require no omitted computation. The audit's
recorded finite tests supplement the proof. The added mixed bridge and
endpoint PSD decomposition were already present and verified in the
accepted audit; no mathematical correction was required.

## Review and historical limits

The bounded source screen did not identify an exact prior certificate for
the same cone/barrier pair in its inspected results. It does not certify
novelty, priority, worldwide literature absence or exhaustive current
openness. This AI-assisted manuscript and audit are unrefereed; acceptance
is not external human peer review, journal acceptance or proof-assistant
certification.

[SOURCE_METADATA.json](SOURCE_METADATA.json) records public source titles,
URLs, PDF byte identities and historical retrieval/inspection scope.
Edition preparation rechecked frozen byte identities and publication
integrity, without new scholarly retrieval, source-text inspection,
literature search or a rerun of the original mathematical programs.
Programs, raw outputs, datasets, copied source documents/text/images and
private coordination material are not distributed.
