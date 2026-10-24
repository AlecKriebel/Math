# Independent delta audit: the proposed log-volume bridge countermodel

Completed 2026-10-24 20:34 UTC. Bounded-review completion estimate: **100%**.
Full Kourovka 21.128 remains **unsolved**. This is a review of a limitation,
not a new solution or a priority claim.

**Verdict: PASS for the stated unrestricted countermodel.** No substantive
objection was found to `root_invariants/LOG_VOLUME_BRIDGE_COUNTERMODEL.md`.
The example correctly disproves that log canonical volume, or that volume
divided by absolute Euler characteristic, is an invariant of the abstract
fundamental group or ordinary homotopy type throughout all finite-homotopy-type
smooth affine aspherical complex varieties. It does not test the additional
reflection-complement or cohomological-dimension hypotheses mentioned in the
note.

## Source input

I independently opened the publisher's full primary PDF of Seidel–Smith,
*The symplectic topology of Ramanujam's surface*, Comment. Math. Helv. 80
(2005), 859–881, at
<https://ems.press/content/serial-article-files/43066>, and read p.859.
The abstract states that Ramanujam's surface is affine and contractible.
The introduction describes it as an open complement in the smooth
Hirzebruch surface F1 and explicitly states log Kodaira dimension two.
Thus smoothness, affineness, contractibility, and log general type of the
same surface are supported. The construction is credited there to Ramanujam;
these are classical inputs rather than new discoveries.

The independently fetched PDF has 216907 bytes and SHA256
`883798702a38a87b87f72ceaa679837171432687a56be8e51c5654630ec44db3`,
matching the root's source metadata. The input-note and metadata hashes are
preserved in `DELTA_BRIDGE_RECEIPT.json`.

## Mathematical checks

Let R denote that surface. A smooth projective SNC compactification
\((X,D)\) exists in characteristic zero. Log Kodaira dimension two means
\(L=K_X+D\) is big, so
\(v_R=\limsup 2h^0(X,mL)/m^2>0\). No unsupported exact numerical value for
\(v_R\) is needed. For the affine plane compactified by a line in
\(\mathbb P^2\), \(K+D=-2H\), which has no positive pluricanonical sections
and volume zero. Both open surfaces are contractible, hence have the same
homotopy type, trivial fundamental group, and Euler characteristic one.
This already proves the first assertion.

For the nontrivial-group version let
\(C=\mathbb P^1\setminus\{0,1,\infty\}\). Its coordinate ring is
\(\mathbb C[t,t^{-1},(t-1)^{-1}]\), so C is smooth affine, and it has the
homotopy type of a wedge of two circles. Products preserve smoothness and
affineness, and therefore
\(V=R\times C\) and \(W=\mathbb A^2\times C\) are smooth affine
threefolds. Contracting the first factor gives homotopy equivalences to C.
In particular both have finite CW homotopy type, group \(F_2\), vanishing
higher homotopy groups, and Euler characteristic \(-1\). Alternatively,
their universal covers are products of contractible spaces. These claims
use genuine contractibility, not merely acyclicity of the first factor.

On \(X\times\mathbb P^1\), the boundary
\((D\times\mathbb P^1)\cup(X\times\{0,1,\infty\})\) is SNC, and the
log canonical line bundle is
\(L\boxtimes\mathcal O_{\mathbb P^1}(1)\). Degree-zero Künneth for sections
therefore gives the exact identity, for every positive integer m,

\[
h^0(X\times\mathbb P^1,m(K+D_{\rm prod}))
 =h^0(X,mL)(m+1).
\]

Consequently

\[
\begin{aligned}
\operatorname{logvol}(V)
 &=\limsup_m \frac{6h^0(X,mL)(m+1)}{m^3}\\
 &=3\limsup_m\left(\frac{2h^0(X,mL)}{m^2}\right)
                          \left(1+\frac1m\right)
 =3v_R>0.
\end{aligned}
\]

The surface volume is finite, and multiplication of its bounded nonnegative
normalized section-growth sequence by a sequence tending to one preserves
the limsup. Thus the coefficient three is correct; no nefness or mistaken
intersection-number replacement is being assumed for the surface divisor.

For W, the analogous product compactification has log bundle
\(\mathcal O_{\mathbb P^2}(-2)\boxtimes
\mathcal O_{\mathbb P^1}(1)\). Every positive m has zero global sections,
because its restriction to every \(\mathbb P^2\) fiber has negative degree.
Thus \(\operatorname{logvol}(W)=0\). Since both Euler characteristics have
absolute value one, the proposed normalized ratios also differ.

## Scope and remaining gap

These examples satisfy the advertised same-dimensional, affine, smooth,
finite-homotopy-type and aspherical conditions. They do not have group
cohomological dimension three: \(\operatorname{cd}F_2=1\). R is not a
hyperplane complement, and neither product is asserted to be one. The note
correctly excludes both potential overextensions.

Accordingly the countermodel validates the warning that asphericity alone
does not turn the preceding algebraic finite-cover obstruction into a group
commensurability obstruction. A theorem specifically recognizing finite
covers of the reflection complements as algebraic varieties would require
additional hypotheses and proof. Nothing in this audit supplies or refutes
such a theorem.

This delta review is independent AI mathematical checking with an actual
primary-source re-fetch. It does not constitute human peer review, a
novelty audit, or publication clearance for a complete Kourovka solution.
