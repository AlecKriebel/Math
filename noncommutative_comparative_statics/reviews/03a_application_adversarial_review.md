# Checkpoint 3A — Application and Computation Adversarial Review

**Reviewer:** independent application-adversary subagent  
**Initial verdict:** no-go as an empirical validation checkpoint; pass as an
arithmetic/self-consistency demonstration after revision.

## Recomputed results

The reviewer regenerated the JSON byte-for-byte and independently checked:

- affine residual \(-0.42\), correction norm
  \(0.42/\sqrt3=0.2424871131\), and numerical-zero rectified residual;
- configuration endpoints \((3,1)\), \((2,2)\), and defect \(\sqrt2\);
- allocation signature \((A_\mu^+,A_\mu^-,C_\mu)=(0,1,0)\);
- normalized smooth differences converging to \((-2,1)\).

No numerical error was found.

## Objections

1. The words “held-out,” “independently declared,” and “validation” were
   unsupported. The program evaluated formulas at \(\lambda=2\); it did not
   perform a calibration/data split. The guard was constructed to separate
   the two endpoints.
2. The original script declared the active-set and jump defect arrays instead
   of computing them from response maps.
3. The script recorded only smooth defect norms, so it did not check the
   claimed vector limit \((-2,1)\).
4. The allocation fibers and maps were declared, not inferred from a
   capacity/compatibility engine. The nonexpansiveness check has singleton
   domains and is correspondingly elementary.
5. A fixed-scale four-part signature does not distinguish quadratic smooth
   from linear active-set behavior. That requires an amplitude-indexed family.
6. “Full affine gauge covariance” was overbroad for a single
   one-dimensional numerical instance.
7. An unspecified reservation, lookahead, or migration policy cannot be said
   to change the signature without defining the alternative maps.

## Revisions made

- Reclassified the evidence as reproducible formal self-consistency and
  prospective falsifiability, not empirical validation.
- Renamed the configuration result a closed-form formula check and described
  calibration/holdout only as a future experimental protocol.
- Marked the guard as constructed in this paper; a prospective guard would
  have to be declared before route outcomes are observed.
- Implemented the active-set projections and an explicit constant-jump
  protocol.
- Recorded and asserted convergence of the normalized smooth vector.
- Qualified the affine gauge computation as one one-dimensional instance.
- Described allocation as evaluation of a declared finite partial-map model.
- Replaced “cross-domain portability” by “formal cross-domain compatibility.”
- Specified two alternative allocation protocols: reserve server 2 for the
  flexible job, or migrate it there when the rigid job arrives.
- Added a pinned NumPy/SciPy dependency manifest and reproduction command.
- Computed the complete point-mass configuration signature, including
  \(V_{\mu,M}=1/\sqrt2\) at \(M=2\).

## Disposition

The review found the arithmetic reliable but forced a material reduction in
the evidential claim. Checkpoint 3 may pass only as formal verification of
model consequences. A second adversarial review was requested after these
changes.
