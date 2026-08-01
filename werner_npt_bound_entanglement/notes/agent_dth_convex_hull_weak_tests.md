# Convex-hull weak tests for the exact DTH pseudomoment

## Scope

This note records discovery calculations on the exact complete-PPT
five-replica pseudomoment.  The input moment itself is read from

`verification/certificates/dth_complete_ppt_pseudomoment.json.gz`.

The tests below are valid necessary conditions for membership in the convex
hull of physical Veronese--Segre atoms.  They do **not** use rank-one minors
of the mixed moment, since those minors are not convex-hull-valid.  All
calculations in this note use floating-point linear algebra after exact source
decoding, so their role is to close weak discovery routes, not to establish a
new exact theorem.

## 1. Invariant realignment tests

The source was reconstructed in the selected 103-element local permutation
diagram basis.  The reconstruction residual was

\[
9.18\times10^{-14}.
\]

The decoded trace and purity were

\[
\operatorname{Tr}R=1.000000045336621,
\qquad
\operatorname{Tr}R^2=2.990409743901875\times10^{-6}.
\]

Rather than forming the full operator, each local realignment was decomposed
into its (SU(3)) highest-weight multiplicity maps, and the three physical
sites were combined only at the multiplicity level.  The resulting CCNR
ratios were

\[
\frac{\|\mathcal R_{A:BC}(R)\|_1}{\operatorname{Tr}R}
=0.34222337487346804,
\]

and

\[
\frac{\|\mathcal R_{C:AB}(R)\|_1}{\operatorname{Tr}R}
=0.03002314070801796.
\]

Pair symmetry gives the same result for (B:AC).  Independent Frobenius
audits recovered the source purity with relative errors
(3.21\times10^{-14}) and (3.67\times10^{-14}), respectively.

Both ratios are far below the separating threshold (1).  Consequently
ordinary realignment/cross-norm criteria cannot detect the missing
identical-(w) relation in this pseudomoment.

## 2. Cheapest one-site third-(w) extension

Trace out two of the three physical qutrit sites.  The resulting local
five-replica marginal (R_1) is full rank on dimension (3^5=243).  Its
numerical spectral data are

\[
\lambda_{\min}(R_1)=0.0012442350000158417,
\qquad
\lambda_{\max}(R_1)=0.01584521979159017,
\]

and

\[
\operatorname{Tr}(R_1^2)=0.0058919244242064866.
\]

Any physical mixture of atoms

\[
(w\otimes w)\otimes z
\]

has, after adding a third copy of (w), a local seven-replica extension
whose three two-pair marginals all equal (R_1).  This is a convex-hull-valid
necessary condition even though it discards all correlations among the three
physical sites.

After (U(3))-twirling, write the extension in the local Schur--Weyl form

\[
X=\bigoplus_{\lambda\vdash7,\ \ell(\lambda)\le3}
I_{S_\lambda(\mathbb C^3)}\otimes X_\lambda,
\qquad X_\lambda\succeq0.
\]

The eight Specht dimensions are

\[
1,6,14,15,14,35,21,21,
\]

so the real-symmetric formulation has only

\[
\sum_\lambda \frac{f_\lambda(f_\lambda+1)}2=1444
\]

variables.  For each of the three choices of two retained bivector pairs,
the 120 permutation moments were constrained to equal the corresponding
moments of (R_1).  The numerically resolved rank of the affine map is 172; the
next singular values form a roundoff cluster near zero, separated from the
last retained singular value by more than eleven decimal orders.

Alternating exact-affine and block-PSD projections found a robust feasible
extension.  With the stronger imposed floor

\[
X_\lambda\succeq5\times10^{-5}I
\quad\hbox{for every local block},
\]

the final relative marginal residual was

\[
7.61\times10^{-15}.
\]

Thus even the cheapest third-identical-(w) symmetric-extension shadow is
comfortably satisfied.  This rules it out as the missing separator.  The
next test must retain correlations between physical sites, or impose a
genuinely global Grassmann/Veronese catalecticant relation.

## Reproduction

- `discovery/agent_dth_realignment_probe.py` performs the invariant CCNR
  calculations and Frobenius audits.
- `discovery/agent_dth_local_extension_probe.py` reconstructs the one-site
  marginal, builds Young-orthogonal (S_7) blocks, imposes all three equal
  two-pair marginals, and runs the block-PSD feasibility projection.

Neither script is an exact verifier.  Their negative conclusions are only
that the tested necessary conditions do not separate the recorded exact
pseudomoment.
