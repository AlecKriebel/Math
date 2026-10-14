# Independent check of direct AU vacuum/projection states

**Edition note.** This supporting check predates the final direct-state proof. Its Section 5 obligations are discharged in [the complete theorem](../pass2_skein/DIRECT_GEOMETRIC_STATE_THEOREM.md) and [final independent audit](../pass2_audit/INDEPENDENT_AUDIT.md).

14 October 2026. PASS2 for Roberts Problem 1.7 / 10400007. This report checks the direct geometric recipe developed in the direct skein construction; it does not replace that construction's full anomaly and normalization audit.

## 1. What is genuinely available before RT comparison

Let \(V_k(\Sigma)\) be the Andersen–Ueno anomaly-corrected horizontal-section space and let

\[
\mathcal H_k(\Sigma)=H_0(\mathcal T(\Sigma);\mathcal L_k(\Sigma)),
\qquad \theta_\Sigma:V_k(\Sigma)\overset\sim\longrightarrow\mathcal H_k(\Sigma).
\]

The local system and \(\theta\) are those accepted in PASS1. They do not depend on the Jones polynomial. For a geometric cut of a surface along disjoint curves, AU sewing gives an isomorphism from a direct sum over labels on the cut surface to the original space. This is a direct geometric construction, not just an isomorphism asserted after RT comparison.

Primary locations in [AU, arXiv:math/0306235v2](https://arxiv.org/pdf/math/0306235v2): Theorem 12.1 constructs the map on flat sections; Theorem 12.2 removes complex-structure/coordinate choices; Definition 12.2 handles unstable surfaces via vacuum insertions; Proposition 12.3 and Theorem 12.3 give naturality; Proposition 12.4 gives disjoint-union compatibility; Theorem 12.4 gives commutativity of separate sewings. Appendix §14.4, equation (80), constructs sewing by contraction with dual affine-module bases in a convergent series; Theorem 14.6 supplies convergence and horizontality.

Choosing a direct-sum component of the inverse sewing map is consequently an actual specified linear operation on these geometric local systems' horizontal sections, and hence on their ordinary local-system \(H_0\). It is not an ordinary continuous-map pushforward on Teichmüller spaces, and should not be described as one.

## 2. Direct handlebody vector and compression projection

Let \(H_g\) be an embedded handlebody and choose a complete nonseparating meridian-disk system \(D\). Cutting its boundary along \(\partial D\) gives a sphere with \(2g\) marked points. AU inverse sewing identifies

\[
V_k(\partial H_g)\cong
\bigoplus_{\lambda_1,\ldots,\lambda_g}
V_k(S^2;\lambda_1,\lambda_1^*,\ldots,\lambda_g,\lambda_g^*).
\]

The all-zero component is canonically identified with the vacuum sphere line by propagation. After fixing its unit once, inclusion gives a vector \(v_D\); projection gives a covector \(\epsilon_D\), with \(\epsilon_D(v_D)=1\). Both are defined before any exterior RT state is mentioned.

For a compressionbody \(C:\Sigma_g\to T\) with \(r=g-1\) nonseparating compression disks and connected negative boundary torus, the same inverse sewing, all-zero projection, and propagation define a direct map

\[
p_C:V_k(\Sigma_g)\longrightarrow V_k(T).
\]

If \(E_K=C\cup_f H_g\) is a relative Heegaard presentation of a knot exterior, the raw candidate is

\[
p_C\,V_k(f)\,v_D.
\]

The knot-specific input is now the actual compression data and the geometric gluing map of the exterior. It is no longer defined by taking the entire vector \(Z^{\rm RT}(E_K)(1)\) and renaming it. Comparison with RT can still be used to prove independence and identify the answer; using a comparison in a proof does not undo the direct definition.

## 3. Independent stabilization normalization check

The raw formula needs a scalar for every compression handle. Let \(i_0\) and \(p_0\) be the vacuum inclusion/projection for a torus cut, and let \(S\) denote the meridian–longitude interchange with the explicitly chosen anomaly lift. Put

\[
s_k=p_0V_k(S)i_0.
\]

In the conventional unitary \(SU(2)_k\) normalization, \(s_k=S_{00}\) and \(\mathcal D_k=s_k^{-1}\). A cancelling Heegaard stabilization uses dual, once-intersecting meridians, not the same meridian on both sides. Its raw local contribution is therefore \(s_k\), while \(p_0i_0=1\) is a different gluing.

It follows that the stabilization-corrected candidate has the factor

\[
\boxed{h_k(E_K)=\theta_T\!\left(s_k^{-(g-1)}p_CV_k(f)v_D\right).}
\]

For one extra cancelling genus, the raw vector multiplies by \(s_k\), and the prefactor acquires \(s_k^{-1}\); the product is unchanged. The formula avoids a common error: calling the same-curve identity \(p_0i_0=1\) a cancelling 1/2-handle pair. Same-curve gluing introduces the \(S^1\times S^2\) factor. In the WRT convention \(Z(S^3)=s_k\) and \(Z(S^1\times S^2)=1\), a connected sum with \(S^1\times S^2\) multiplies a state by \(s_k^{-1}\), agreeing with the above correction.

This calculation fixes the magnitude and local normalization once the extension/anomaly convention is fixed. It does not license dropping the central phase of an arbitrary lift of \(S\). All occurrences of \(S\), \(f\), sewing and boundary Lagrangians must use the same extended-surface convention. The main construction must account for the Maslov/weight correction globally; the local scalar computation alone is not a substitute.

## 4. A direct fundamental-colored filling functional

Cut the peripheral torus along its meridian \(m\). Inverse sewing gives

\[
F_m:V_k(T)\longrightarrow\bigoplus_{\lambda=0}^{k}V_k(S^2;\lambda,\lambda^*).
\]

For the fundamental label \(1\), the summand is one-dimensional. Fix a nonzero coordinate \(c_1:V_k(S^2;1,1^*)\to\mathbb C\), for example the normalized two-point affine block in the source convention. Define

\[
\epsilon_1^m=c_1\,\operatorname{pr}_1F_m,
\qquad
f_k^{\rm geom}=\epsilon_1^m\theta_T^{-1}.
\]

This is a geometric factorization covector. It does not use an independently constructed orientation-reversal duality pairing, so AU's statement that their duality structure was transported from RT is not by itself a blocker for this particular contraction. It also does not prove that an arbitrary three-dimensional cobordism map has been constructed without comparison.

Changing the nonzero coordinate \(c_1\) multiplies both the knot numerator and its unknot denominator by the same scalar. Thus the normalized contraction is independent of this choice. For the unknot exterior, the compressible slope is the preferred longitude \(\ell\). Its raw vacuum is the longitude vacuum \(v_\ell\), and the coefficient \(\epsilon_1^m(v_\ell)\) is \(S_{10}\) in the standard basis, up to the same harmless two-point normalization. The standard \(SU(2)_k\) value

\[
S_{10}=\sqrt{\frac{2}{k+2}}\sin\!\left(\frac{2\pi}{k+2}\right)
\]

is nonzero for every integer \(k\ge1\). The standard affine-character matrix formula is recorded, with half-integer spin indexing, in [Ginsparg, *Applied Conformal Field Theory*, equation (9.50a)](https://homes.psd.uchicago.edu/~sethi/Teaching/P483-F2003/ginsparg.pdf). No division by zero arises. The fundamental filling identification, including its framing and any common scalar, can then be proved via the structure-preserving comparison; it need not be used to define the functional.

## 5. Exact remaining proof boundary

For the direct recipe, AU sewing itself and the operations above are real geometric input. The local stabilization calculation has a specified correction. To conclude a natural knot-exterior class, the completed proof must still verify either directly or by the structure-preserving comparison:

1. the handlebody vector's independence of disk-system slides and boundary identifications;
2. the compression map's corresponding independence;
3. the global central-extension/weight correction for the relative Heegaard decomposition;
4. the exact relation to the fundamental-colored filling, and source Jones normalization.

These are finite, meaningful obligations. They are not grounds to reject the earlier accepted transported theorem, and they are not assertions that the obligations cannot be met. A correct comparison proof after the direct definitions is legitimate. The precise improvement is that the knot-dependent class now has a geometric vacuum/sewing recipe before that comparison is invoked.

The full polynomial can use the already accepted exact finite interpolation once the normalized root values are identified. The qualitative source-level significance of this stronger construction remains for separate assessment; this check does not claim historical novelty or a literature-status resolution.
