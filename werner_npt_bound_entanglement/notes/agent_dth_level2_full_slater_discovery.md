# Complete degree-three fixed-marginal Slater discovery

## Status

The complete site-averaged five-replica pseudomoment has a **strictly
positive degree-three fixed-marginal extension at floating-point discovery
precision**.  This is the first complete positive result across all 118
active output blocks; earlier tests covered only selected negative sectors.

This note does not claim an exact extension theorem.  Exact rational
reconstruction in the seed coordinates of
`agent_dth_level2_rational_seed_compression.md` remains required.  The test
also imposes only positivity, the degree-three Grassmann quotient, and the
prolonged holomorphic Omega equation.  Prolonged mixed support and grouped
PPT conditions remain separate constraints.

## 1. Lossless finite system

Exact physical-site averaging reduces the target to 761 coordinates.  The
new exact source census and numerical intertwiner engine reduce the source
from

\[
487\text{ ordered blocks},\quad519434\text{ symmetric variables}
\]

to

\[
112\text{ shape orbits},\quad171\text{ PSD components},\quad
87540\text{ symmetric variables}.
\]

The reduced affine normal operator is full rank and has numerical spectrum

\[
\boxed{
49.32837146994441
\le\lambda(AA^*)\le
490.0150623081329.
}
\tag{1}
\]

The direct reduced Kraus compiler produces 19592 effective matrices.  Its
output agrees with explicit expansion through all 487 ordered blocks to
(3.76\times10^{-13}) in the random audit, while the complete marginal
covariance error in the independent source-transport audit is
(1.93\times10^{-10}) before scaling by the very small moment.

## 2. Strict floor

Start from the saved full floor-zero Douglas--Rachford point, reduce it to the
171 components, subtract the desired physical-block floor, and affine-project
once.  At

\[
t=10^{-14},
\]

ten direct reduced Douglas--Rachford iterations give the shifted problem

\[
\begin{aligned}
\text{invariant marginal residual}&=2.76\times10^{-20},\\
\text{shifted PSD defect}&=1.80\times10^{-17},\\
\text{least shifted component eigenvalue}&=-1.71\times10^{-17}.
\end{aligned}
\tag{2}
\]

After restoring the exact numerical floor shift, the least ordered physical
block eigenvalue is

\[
\boxed{9.9901\times10^{-15}>0,}
\tag{3}
\]

and the expanded 487-block source has zero floating-point PSD defect.  Its
unaveraged raw target residual is (1.91\times10^{-17}); the difference from
the much smaller invariant residual in (2) is the accumulated numerical
transport covariance error, not a missing invariant equation.

This is a numerical Slater point.  It rules out interpreting the extensive
nullity of the unshifted Douglas--Rachford output as evidence of a forced
face.

## 3. A posteriori exact-correction scale

If (2) is reconstructed in the exact rational source and target charts, the
right-inverse theorem gives the uniform correction bound

\[
\frac{\|e\|}{\sqrt{\lambda_{\min}(AA^*)}}
\approx
\frac{2.76\times10^{-20}}{\sqrt{49.328}}
<4.0\times10^{-21}.
\tag{4}
\]

This is more than six orders of magnitude below the numerical floor (3).
Thus the remaining difficulty is exact chart reconstruction and rigorous
roundoff control, not SDP conditioning.  Formula (4) is not yet a rigorous
bound because the current Kraus charts were built by floating-point SVD.

## 4. The apparent null face is not exposed

The unshifted reduced candidate has 1612 component eigenvalues at most
(10^{-12}), spread over 120 of the 171 components.  Let (P_F) project onto
their direct sum and form, on the complete 761-dimensional invariant target,

\[
H_F=A(I-P_F)A^*.
\tag{5}
\]

A functional (y) whose dual slack (A^*y) is supported on those kernels would
belong to (\ker H_F).  The computed spectrum is instead

\[
\boxed{
10.6471011208894
\le\lambda(H_F)\le
475.429110500698.
}
\tag{6}
\]

There is no small eigenvalue even at relative threshold (10^{-6}).  On the
32-dimensional subspace of scalar shape-orbit functionals the corresponding
minimum is (54.3161).  Consequently the observed candidate kernels cannot
be the support of any nonzero dual exposing slack.  They are one boundary
point selected by the projection algorithm inside a feasibility problem that
also has numerical interior points.

This facial conclusion is discovery-layer numerical evidence.  It is useful
for choosing the next calculation but is not promoted to an exact theorem.

## 5. Reproduction

The relevant scripts are

* `discovery/agent_dth_level2_source_symmetry.py`;
* `discovery/agent_dth_level2_source_reduced_full.py`; and
* `discovery/agent_dth_level2_exposing_face.py`.

The full raw and reduced map caches and candidate pickles are disposable
NumPy discovery artifacts and are intentionally not committed.

## 6. Next exact step

Use the rational 720-term source projector and rank-at-most-three Omega
deflation to build every reduced marginal block over (\mathbb Q).  Round the
Slater source in those rational charts, solve the 761-dimensional rational
normal equation for the exact residual, and certify all 171 corrected PSD
components by rational LDL or interval Cholesky.  A successful replay proves
that the recorded negative five-replica pseudomoment survives the positive
fixed-marginal part of the degree-three lift.  It would not yet decide the
prolonged support/PPT extension or physical DTH.
