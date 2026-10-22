# Independent review: 2861 / KP 3.63

**Verdict: PASS_CREDITED_KNOWN_METHOD_WITH_EFFECTIVITY_LIMIT.** The Gaussian formula, its fixed-manifold convergent geometric truncation, and the published-source correction are valid. No required mathematical correction was found. This is not certification of a uniformly terminating, arbitrary-tolerance algorithm from every triangulated input.

Reviewed 2026-09-30 by a separate adversarial AI reviewer (gpt-6-astra, xhigh). No novelty or human-peer-review certificate is given.

Frozen SOURCE_STATUS.md SHA-256:
4ab7e3bbf6bea8c543b7e9163750ae4c09b903cececc0a895fc937b3b6301a4e

## 1. Exact original and published scope

K3 Problem3.63 and its remarks on printed pp.176–177 concern the real Dirac eta invariant of a specified spin structure on a closed oriented hyperbolic three-manifold. They do not request merely an integer residue or the reduced invariant.

The [official JEMS record](https://ems.press/journals/jems/articles/14297701) confirms Lin–Lipnowski's publication: online April10,2024, in volume27 (2025), pp.4201–4281. I checked the full [published PDF](https://ems.press/content/serial-article-files/51185), including the spin lift definitions, odd trace formula, formula(14), AppendixC.2 and Gaussian extension in AppendixD. Printed pp.4206,4226 and4235 were also visually checked.

The source's Floer-theoretic results impose rational-homology-sphere and minimal-L-space conditions. AppendixC.2 starts with a general closed hyperbolic three-manifold group and its lift; no first-Betti-number restriction enters the spin trace formula itself. Setting the twisting character to zero selects the genuine spin case. The paper expressly discusses nonzero Dirac kernel at p.4226. These observations justify the general closed-spin application in the artifact.

Section5's numerical propositions are stated in the paper's rational-homology-sphere setting with particular volume/injectivity-radius bounds. The reviewed convergence argument does not export those numerical constants to arbitrary Y: it uses the general fixed-manifold Weyl growth and its own elementary geometric estimate. The underlying spinor small-support trace calculation can supply local count estimates when its geometric inputs are certified; that is distinct from treating every tabulated numerical proposition as hypothesis-free.

## 2. Half-angle, orientation and multiplicities

Section2.1 defines the complex length from the eigenvalue of modulus greater than one of the lifted matrix. Thus if that eigenvalue is
\[
\lambda_\gamma=e^{\ell_\gamma/2+i\theta_\gamma},
\]
the spin holonomy parameter is \(\theta_\gamma\) modulo \(2\pi\), while the ordinary rotation is \(2\theta_\gamma\) modulo \(2\pi\). The submitted definition matches the source.

Changing a spin lift by a sign changes \(\theta\) by \(\pi\): the sine numerator changes sign and the denominator does not. On an m-th iterate, the sign changes by \((-1)^m\), consistent with the source's Lie-spin convention. Replacing this by an arbitrary choice of the ordinary half-angle would lose essential spin data.

The sums retain all nontrivial group conjugacy classes, with their iterates and primitive-length factors. In particular, inverse elements have the same unordered pair of SL2 eigenvalues, so their expanding eigenvalue is the same; one must not automatically negate \(\theta\) and cancel their sine terms. Nor can one combine the two orientations into one unoriented geodesic without adjusting the counting convention. The artifact explicitly prevents this error.

The spectral eigenvalues are those of the source Dirac operator with their usual complex multiplicities. Spin eigenvalues may have even multiplicity from quaternionic symmetry; they must not be counted once per quaternionic eigenspace while retaining the same trace coefficient. The source's AppendixC calibrates the sign against the chosen orientation, which is the convention used here.

The denominator identity is exact:
\[
|1-e^{\ell+2i\theta}|\,|1-e^{-\ell-2i\theta}|
=e^\ell+e^{-\ell}-2\cos2\theta.
\]
There is no missing square root or extra factor2.

## 3. Gaussian and raw-eta normalization

With the declared Fourier convention, \(\widehat G(t)=\sqrt{2\pi}e^{-t^2/2}\). Its positive half-line integral is \(\pi\). For \(K_T(x)=T^{-1}G'(x/T)\), its transform is \(iTt\widehat G(Tt)\). Substitution into the source's odd formula, whose spectral side has coefficient one half, gives precisely the displayed \(G_T\) with geometric coefficient2.

The geometric primitive satisfies
\[
\frac{d}{dT}\left(-\frac1\ell e^{-\ell^2/(2T^2)}\right)
=-\frac{\ell}{T^3}e^{-\ell^2/(2T^2)}.
\]
It vanishes at \(T=0\). Dividing the resulting integral by \(\pi\) therefore gives the **negative** coefficient \(-2/\pi\) and the iterate factor \(\ell_0/\ell\).

For a nonzero signed eigenvalue, substitution \(u=T|\lambda|\) gives the remainder
\(\operatorname{sgn}(\lambda)\operatorname{erfc}(L|\lambda|/\sqrt2)\).
A zero eigenvalue contributes zero before integration and is excluded in the eta series. No half-kernel correction is introduced. This is the raw APS eta value, not \((\eta+\dim\ker D)/2\).

AppendixD permits the Gaussian and its derivative. These particular functions have the needed rapid decay for both trace sides and justify the use made here. The report does not need any broad interpretation of that appendix beyond these specific Schwartz test functions.

## 4. Absolute convergence and the diagonal cutoff

For fixed \(L>0\), polynomial Weyl growth and Gaussian decay imply absolute convergence of the spectral remainder. For \(L\ge1\), its absolute summands are dominated by those with \(L=1\), whose sum is finite. Each nonzero eigenvalue's term tends to zero. Dominated convergence therefore proves decay of the complete remainder for a fixed manifold, including manifolds with a kernel.

The geometric counting bound is valid. Conjugate each element so its axis meets a Dirichlet domain contained in \(B(o,D)\). It then moves o by at most \(\ell+2D\). Choose one representative per class; distinct classes give distinct group elements. Disjoint orbit balls of radius r around these points lie in \(B(o,x+2D+r)\). The hyperbolic ball-volume estimate
\[
\operatorname{Vol}(B(R))=\pi(\sinh2R-2R)\le\frac\pi2e^{2R}
\]
gives exactly the submitted constant \(C\) in \(Ce^{2x}\).

For \(\ell\ge a>0\), the denominator is at least \(e^\ell(1-e^{-a})^2\). Grouping the omitted classes into \([k,k+1)\) gives the stated majorant
\[
\frac{2Ce^2}{\pi(1-e^{-a})^2}
\sum_{k\ge R}e^{k-k^2/(2n^2)}.
\]
At \(R=4n^2\), the initial exponent is \(-4n^2\), and consecutive exponent differences are at most \(-3\). The geometric-series bound follows. The strict cutoff in \(A_n\) causes no omission of equality cases, since the tail includes length exactly \(4n^2\).

Consequently the finite geometric sums \(A_n\) converge to the raw eta invariant. This is a direct consequence of the imported trace theorem and elementary estimates, not a new trace theorem.

## 5. Effective computation boundary

The source specifies Dirichlet-domain and complete finite conjugacy-class/length-spectrum data as input. A specified spin lift can be found by sign equations on a presentation, with the remaining choices forming an \(H^1(Y;\mathbb Z/2)\) torsor. This does not require finite first homology when only a genuine spin structure is being computed.

What is proved here is convergence for each fixed manifold. The geometric remainder has a modulus once its geometric constants and input are certified. The spectral dominated-convergence argument supplies no uniform computable modulus in the absence of certified information about the small nonzero spectrum. A possibly nontrivial kernel is harmless in the identity but does not solve the task of distinguishing zero from arbitrarily small nonzero eigenvalues in numerical input.

The artifact correctly avoids claiming that a general triangulation-to-tolerance program is implemented or proved to terminate. It also does not certify SnapPy's floating-point geometry for arbitrary inputs. Those limitations must remain prominent if the queue is classified as a known-method correction.

The published Weeks value, approximately0.989992, and its accuracy warning are both explicitly present on p.4206. The decimal inherits the odd-signature eta computation's accuracy in Snap. This review checks that statement and the normalization arithmetic, not the numerical input or rigorous error bars for those digits. The existence of a published geometric method is the main source correction; no independently certified decimal example is claimed here.

## 6. Exact controls and recommendation

The submitted verifier was replayed unchanged in an isolated working directory with its required SOURCE_STATUS.md. All **99 assertions** and its receipt reproduced byte for byte.

An independent standard-library checker passes **1,487 exact rational/integer assertions**, covering the denominator, half-angle sign changes, iterates, inverse-class eigenvalue convention, diagonal cutoff exponents, and raw-versus-reduced kernel distinction. A shrinking-gap control illustrates why a fixed-manifold convergence proof is not a uniform spectral-gap estimate. No actual geodesic enumeration, Dirac spectral computation or eta decimal is certified by these tests.

**Recommendation:** a credited known-method/source correction is supported for the literal K3 request. If “compute” is strengthened to require a uniformly certified arbitrary-precision stopping algorithm from every triangulation, that stronger interpretation remains outside the verified result. Keep the publication's attribution, the all-manifold spin scope, kernel allowance, exact conjugacy multiplicities and the explicit effectivity qualification. No mandatory mathematical change is required.
