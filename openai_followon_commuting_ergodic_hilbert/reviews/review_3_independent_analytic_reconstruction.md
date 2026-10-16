# Independent reconstruction of the full annular analytic dependency

Reviewer: internal analytic subagent for complete package review 3.
Review checkpoint: 2026-10-07T05:49:37Z.
Completion of this analytic reconstruction: 100%.

## Scope and verdict

I first read `/Users/alec/Documents/Math/AGENTS.md` and `research/ORIGINAL_REQUEST.txt`. I read current `main.tex` and all nine copied upstream section sources directly, without using earlier research conclusions, review reports, responses, dependency ledgers, or computational supplements as evidence. The mathematical verdict was formed by reconstructing the proof below. The upstream clone on the Desktop remained untouched. I made no candidate or Git changes.

**Verdict: no substantive analytic dependency gap found in the current copied October 5 annular manuscript.** Its pointwise, all-scale annular variation statement matches exactly the input needed by current `main.tex`, lines 79–98. The proof establishes the stated complex-input bound with the partition supremum inside the output norm. I found no circular invocation of a triangular-Hilbert, Mikhlin, or cross-scale orthogonality theorem. The actual current rough-kernel proof uses BV translation estimates and Plancherel within a frequency block, followed by its own uniform frequency-block lemma. An older source or a different family 082 formulation should not be substituted for this one.

This verdict concerns the analytic dependency and the mathematical reduction in `main.tex`. It does not certify priority, provenance hashes against the Desktop clone, package redistribution rights, deposit metadata, archived code, or PDF appearance; those are assigned to the complete-package reviewer. It is a direct mathematical audit, not a formal verification or conventional human peer review.

Below, section filenames mean the files under `sources/upstream/Annular-variation-of-the-triangular-Hilbert-transform-at-the-symmetric-point-October-5-2026/build/sections/`.

## 1. Precise claim and dependency chain

The required estimate is upstream `introduction.tex`, lines 15–34:

\[
\left\|\sup_{J\ge1,\,0<t_0<\cdots<t_J,\,t_j\in\mathbb Q}
\left(\sum_j|B_{t_{j-1},t_j}(F,G)|^r\right)^{1/r}\right\|_{3/2}
\le C_r\|F\|_3\|G\|_3,\qquad r>2.
\]

The source does not prove merely fixed-partition norm variation. Its count quantity `introduction.tex`, lines 120–140, is the pointwise supremum of sums of up to \(n\) absolute annular increments over pairwise disjoint rational radius intervals. Its proof has this chain:

1. Dimension-free cyclic matrix inequality and supported Hessian/order/averaging identities (`matrix.tex`).
2. Integrated Gaussian heat identities, strict comparable-variance dissipation, and unequal-variance single-edge dissipation (`heat.tex`).
3. Repeated output-dependent masks give a \(C\sqrt n\) smooth-annulus linearization (`smooth.tex`).
4. Narrow-variance row refinement and square summation of output-dependent coefficients give a uniform frequency-block estimate (`frequency.tex`).
5. BV Fourier bounds, a finite cutoff, and odd-kernel moment removal give \(C\sqrt n\log(2+n)\) rough-family bounds (`rough.tex`, lines 82–319).
6. Pairing endpoints at each output produces uniformly bounded Gaussian kernels independent of the number of jumps; only their jump counts enter the Fourier bounds (`rough.tex`, lines 335–485).
7. Step-choice approximation, finite-menu measurable selection, density, and rank summation give the full count and variation estimates (`completion.tex`).

All positive scales are allowed. The only restrictions on mesh size appear before a finite set of endpoint/frequency choices is sent to the continuum. They do not persist in the final estimate.

## 2. Cyclic matrix estimate, support, and complex phase

The quadratic cost is

\[
b_P(K)=\frac32\sum_{i,j}\frac{|K_{ij}|^2}{\sqrt{p_i}+\sqrt{p_j}}
\]

on the support of \(P\); this is the second derivative of \(\operatorname{tr}(P^{3/2})\), by differentiating \(A^2=P\) (`matrix.tex`, lines 54–92). Zero eigenvalues are not inverted. The order comparison \(P\le aQ\Rightarrow b_P(K)\ge a^{-1/2}b_Q(K)\) is valid even when the supports differ: \(\ker Q\subseteq\ker P\), and positive-definite regularization plus operator square-root monotonicity proves the comparison (`matrix.tex`, lines 100–144).

The joint-convexity proof has no hidden commutativity assumption. If \(A=\int\sqrt{T_\omega}\,d\nu\), vector Cauchy–Schwarz gives \(A^2\le\overline T\); square-root order therefore gives \(A\le\sqrt{\overline T}\). The inverse quadratic-form variational formula then proves the averaged-cost inequality on the common support (`matrix.tex`, lines 182–245). This is the crucial averaging used in frequency refinement.

For the cyclic trace let \(M\) be the three-block Hermitian adjacency matrix and \(D\) the block diagonal Hermitian insertion. The embedded stars satisfy \(A_v=MP_vM\le M^2\), and \(K_v=MP_vDM\) is supported on \(A_v\). Consequently

\[
\mathcal E=\sum_v b_{T_v}(R_v^*D_vR_v)
\ge\frac13b_{M^2}(MDM)\ge\frac12Q,
\quad
Q=\sum_{i,j}\frac{q_i^2q_j^2}{q_i+q_j}|D_{ij}|^2,
\]

where \(q_i=|m_i|\) in an eigenbasis of \(M\), arranged decreasingly (`matrix.tex`, lines 314–365). Vanishing \(q_i\) contribute zero.

The cubic trace bound is checkable by grouping triples according to the multiplicity of the smallest index. With \(A_i=q_i^3|D_{ii}|^2\) and \(E_i=q_i\sum_{j>i}q_j^2|D_{ij}|^2\), those three groups contribute at most \(3D_*E_i\), \(3D_*\sqrt{A_iE_i}\), and \(D_*A_i\), respectively. Thus

\[
|\operatorname{tr}((DM)^3)|
\le D_*(A+3E+3\sqrt{AE})
\le5D_*(A/2+E)\le5D_*Q.
\]

This retains the signs of eigenvalues and allows the two remaining indices to coincide (`matrix.tex`, lines 366–403). It does not use an entrywise absolute-value estimate with a dimension loss.

The six closed triangular walks give \(\operatorname{tr}((DM)^3)=6\operatorname{Re}\tau\). Multiplying \(W_0\) by a scalar unit phase rotates \(\tau\) to \(|\tau|\) while simultaneously unitarily conjugating each affected star Gram and its insertion; the total cost stays unchanged. Hence \(|\tau|\le(5/3)D_*\mathcal E\) (`matrix.tex`, lines 405–430). Complex diagonal windows are split into their real and imaginary Hermitian diagonal parts; the eight-term expansion gives the stated constant \(20/3\), without treating non-Hermitian insertions as Hermitian (`matrix.tex`, lines 432–444).

## 3. Heat identities and dissipation

For fixed finite arrays, \(R_v=D_{\rm row}R_v^0D_{\rm col}\) has constant rank. Pure row changes preserve the kernel of \(R_v\); column changes with the row fixed preserve its range. The source uses the correct Gram for each derivative and separately proves joint smoothness by a full-rank factorization (`heat.tex`, lines 96–143).

For Gaussian scores \(N=(u-p)/\sigma\), \(\partial_pw=Nw\) and \(2\partial_\sigma w=\partial_p^2w\). The Hessian chain rule therefore gives

\[
2\partial_s e_v=\sum_i\alpha_i\partial_{p_i}^2e_v
-\alpha_vV_v-\sum_{w\ne v}\alpha_wY_{v,w},
\qquad
\partial_{p_{v+1}}\partial_{p_{v-1}}e_v=Z_v.
\]

Integrated over \(\Pi_d\), each pure second center derivative and the mixed column derivative equals \(\partial_d^2J_v\), by changing which coordinate is dependent (`heat.tex`, lines 193–208). This equality is integrated, not falsely pointwise. The Gaussian and score bounds justify differentiating and integrating by parts on every compact positive scale interval (`heat.tex`, lines 145–191).

The neighbor comparison is

\[
Y_{w+1,w}+Y_{w-1,w}\le\sqrt2V_w.
\]

Indeed \(T_w\le2\operatorname{diag}(A^*A,B^*B)\); apply order comparison, discard the nonnegative off-diagonal entries of the resulting metric, and compare each single-edge Gram with the neighboring full star (`heat.tex`, lines 237–258). Combining this with \(2Z_v\le Y_{v,v+1}+Y_{v,v-1}\) leaves strict dissipation for permutations of rates \((1,11/10,11/10)\). The two coefficients are \(-1+(3/5)\sqrt2<0\) and \(-11/10+(1/2)\sqrt2<0\) (`heat.tex`, lines 260–270).

The initial-energy bound is dimension free because weighted Hölder bounds each edge Hilbert–Schmidt norm cubed by the weighted cubic array sum, and each Gaussian mass is uniformly bounded when \(\sigma\ge h^2\) (`heat.tex`, lines 278–314). The source does not claim full-star dissipation for the very unequal rates needed later. It instead retains a single edge, where the mixed term vanishes and

\[
-2\partial_sJ^e_{v,w}=\iint(\alpha_vV^e_{v,w}+\alpha_wY^e_{v,w}).
\]

The coefficient of the wide column cost is then exactly one (`heat.tex`, lines 331–380).

## 4. Repeated masks and smooth annuli

At each output index, disjoint radius intervals imply \(|A_0^s|\le|A_0|\) and a total jump modulus at most \(2n|A_0|\), also for complex coefficients and simultaneous switches (`smooth.tex`, lines 36–54). Across rank-changing switches the derivative of \(\operatorname{tr}((R^*R)^{3/2})\) is valid by regularization, and its entry gradient is bounded by the corresponding row norm times column norm (`matrix.tex`, lines 255–289).

For the two changed stars the resulting jump is bounded by

\[
C\sum_{i,j}w_0(i)w_1(j)|\delta A(i,j)|(2XY+HY+QX).
\]

The Gaussian probability measure for fixed \((i,j)\) gives line-maximal majorants for \(X,Y,H,Q\). The shear changes \((i,j)\mapsto(i,-i-j)\) or \((j,-i-j)\) preserve counting measure, so the majorants have cubic norms controlled by the original edge norms. Hölder and the total jump count yield exactly \(Cn(n_0^3+n_0^2(n_1+n_2))\), with two copies of the dual norm in the mixed terms (`smooth.tex`, lines 68–128).

The narrow-row comparison turns the base window cost into \(CsV_v^{\rm n}\), whose rates are the strictly dissipative comparable rates. Normalizing the three original norms to \((n^{-1/2},1,1)\) makes the energy bound uniform; rescaling gives \(C\sqrt n\prod_vn_v\) (`smooth.tex`, lines 133–171). There is no hidden fixed-output partition in this argument.

The exact convolution/scaling identity

\[
I_{\varepsilon,R}(t)
=c_0\mathbf1_{\{\varepsilon<|t|<R\}}/t+E_\varepsilon(t)-E_R(t)
\]

has \(c_0=2g_3''(0)\ne0\); its sign is immaterial after taking the absolute fixed reciprocal. It follows directly from \(k_1=-g_1'\), \(k_1*k_1*k_1=-g_3'''\), and the scale substitution (`smooth.tex`, lines 181–205).

## 5. Uniform frequency blocks: no frequency-size loss

For frequency size \(D\), use \(\theta=(16D^2)^{-1}\), variance \(a=qL^2\), slab \(2a<s<3a\), and refined row variance \(b'=\theta s\). The required mesh condition makes every variance at least \(h^2\) (`frequency.tex`, lines 130–147). With \(\omega=\xi/L\), the normalized window is \((L/D)(g_a e^{i\omega u})'\), and its ratio to \(g_s\) is bounded independently of \(D\) (`frequency.tex`, lines 153–168).

The exact modulated Gaussian identity is

\[
g_a(u)e^{i\omega u}
=e^{\omega^2ab'/(2(a-b'))}
\int g_{b'}(u-d)e^{ia\omega d/(a-b')}g_{a-b'}(d)\,dd.
\]

The prefactor is bounded since \(\omega^2b'\lesssim q\). Differentiating the narrow Gaussian expresses each real/imaginary inserted Gram as an average \(\int\alpha(d)U_v^d\,d\nu_s(d)\) with \(|\alpha(d)|\lesssim_q\sqrt{\theta s}\). All refined Grams have the same support; joint convexity thus gives

\[
b_{T_v}(K_v)\lesssim_q\theta s\int V_v(p_0,\ldots,p_v+d,\ldots,p_2;s)\,d\nu_s(d).
\]

These are `frequency.tex`, lines 170–229. The positive Gaussian average changes the row variance, without assuming a frequency multiplier theorem.

Averaging the plane heat identity against \(\nu_s=g_{(1-\theta)s}\) changes the plane second-derivative coefficient from \(2+\theta\) to \(3\): its additional \(1-\theta\) comes from differentiating \(\nu_s\) and integrating twice by parts. Consequently

\[
\theta\widetilde V_v
\le-2\partial_s\widetilde J_v+\tfrac12\sum_{w\ne v}\widetilde Y_{v,w}.
\]

This is `frequency.tex`, lines 231–270. Each column cost is paid by the single-edge dissipation with wide column rate one (`frequency.tex`, lines 271–311).

The delicate mixed boundary term is also uniform in \(\theta\). The probability measure obtained from the changing edge has centers \(p_v,p_w,d\) independent with variances \(\theta s,s,(1-\theta)s\). Adding the Gaussian sampling noise for the unchanged edge gives covariance

\[
\Sigma=s\begin{pmatrix}2\theta&-\theta\\-\theta&3\end{pmatrix}.
\]

It satisfies \(\Sigma\le4s\operatorname{diag}(\theta,1)\) and \(\det\Sigma=\theta(6-\theta)s^2\). Both the exponent and the determinant prefactor are therefore controlled by the product of Gaussians at variances \(4\theta s\) and \(4s\), with an absolute constant. Two line maximal operators give a majorant independent of \(s,\theta,k,\xi\); the shear map is a lattice bijection (`frequency.tex`, lines 82–127). Thus boundary summation pays

\[
\sum_{i,j}h^2|A_0(i,j)|^2\mathcal H_v(i,j)
\sum_k\int|\mu_{ij,k}(\xi)|^2\,d\xi/D,
\]

which is bounded by \(C(C_1)n_0^2(n_1+n_2)\), not a sum of separate frequency suprema (`frequency.tex`, lines 316–380). Cubic switching costs are summable because \(|\mu|^3\le C_1|\mu|^2\). The fixed-edge initial energy is paid only once. This proves the integrated score estimate uniformly in frequency size and scale count.

Integration over each slab with \(ds/s\) yields a constant logarithmic length \(\log(3/2)\); plane integration convolves the three windows exactly. Normalization turns the sum-of-cubes estimate into the product estimate (`frequency.tex`, lines 390–423). Riemann sums are taken only after the bounded frequency integral, and the finite step boundaries have measure zero. For general cubic inputs the integrable Gaussian scalar-kernel majorant and determinant-one Hölder changes prove continuity (`frequency.tex`, lines 452–485).

## 6. Hölder envelope, Fourier energy, and endpoint counts

The Gaussian pointwise envelope uses exponents \(5/2,5/2,5\), whose reciprocals sum to one. Each input's Gaussian integral is bounded by its directional line maximal function. The \(L^{6/5}\) maximal bound, followed by spatial Hölder, gives the \(L^{3/2}\) product bound (`rough.tex`, lines 15–72). The strict gap \(5/2<3\) is essential and is supplied; the proof does not accidentally use the unbounded \(L^1\) maximal endpoint.

For kernels with three vanishing moments, the triple primitive \(U\) can be represented by a left tail or right tail. Both have Gaussian decay, including two derivatives. Choosing a sufficiently broad \(g_{3q}\) makes \(f=U/g_{3q}\) and its first three weak derivatives uniformly Gaussian bounded, with BV costs at most \(Cm\) (`rough.tex`, lines 121–159).

For \(|\xi|\sim D\), the derivative measure of \(f'''\) gives \(|D^3\widehat f|\le Cm/D\). The energy estimate is more efficient than squaring that pointwise estimate: the BV translation bound gives \(\|f'''(\cdot+D^{-1})-f'''\|_1\le Cm/D\), and the uniform supremum bound turns this into the same bound for its squared \(L^2\) norm. Plancherel then gives

\[
\int_{\Xi_D}|D^3\widehat f(\xi)|^2\,d\xi\le Cm/D,
\]

because \(|e^{i\xi/D}-1|\ge2\sin(1/2)\) when \(D\le|\xi|<2D\) (`rough.tex`, lines 161–193). This is the only Fourier orthogonality step in the current proof. It is within one block and requires no asserted cross-scale orthogonality for the entangled form.

A cutoff at \(P_*=(2+n)^8\) has Gaussian-envelope error \(C(m/P_*)^{1/5}\) per nonzero scale. Since \(m\lesssim\sqrt n\), this is \(O(n^{-1})\); there are \(O(n)\) nonzero groups (`rough.tex`, lines 195–238). For the block coefficient \(c=D^3\widehat f\chi\), take \(\mu=Dc/\sqrt n\). Then

\[
|\mu|\lesssim m/\sqrt n\lesssim1,
\qquad
\sum_k\int|\mu_k|^2\,d\xi/D
\lesssim\sum_km_k/n\lesssim1.
\]

The normalization has no residual \(D\) loss. There are only \(O(\log(2+n))\) blocks below the cutoff. This proves the rough-family bound (`rough.tex`, lines 240–278). Odd kernels remove their first moments by \(\Psi=\varphi-\tfrac12\operatorname{Dil}_2\varphi\) and a convergent dilation identity; the remainder is \(O(2^{-J}n)\) and tends to zero (`rough.tex`, lines 280–319).

For endpoint kernels, pairing annuli whose two endpoints lie in the same half-open dyadic radius group gives total paired length at most one after scaling. There are at most two unpaired endpoint contributions. The smooth paired terms and their derivatives are bounded by that length; for the hard parts, disjointness allows at most one paired indicator difference at each radius. Gaussian tail derivatives are uniformly bounded for endpoint parameters in \([1,2]\) (`rough.tex`, lines 356–465). Therefore the entire grouped kernel has a uniform Gaussian bound independent of its jump count. Groups with \(m_k>\sqrt n\) number at most \(2\sqrt n\) and use the pointwise envelope; the remaining groups use the rough-family theorem with \(\sum m_k\le2n\) (`rough.tex`, lines 467–485). Choices and grouping remain output dependent throughout.

## 7. Completion, boundaries, and effect on the candidate

The final step-choice estimate becomes an arbitrary measurable finite-menu estimate by rectangle approximation on the compact dual support. Finite choices of phase from \(\{1,-1,i,-i\}\) capture at least half of every complex increment's modulus, sufficient for duality. Countable rational exhaustion and then approximation of the two inputs give the count bound for all complex cubic inputs (`completion.tex`, lines 8–61). Every finite truncation has common measurable representatives and endpoint continuity by the elementary finite-annulus bound (`preliminaries.tex`, lines 16–43).

For any chosen partition, arrange increments decreasingly. Its largest \(2^j\) members are admissible in the disjoint-annulus count quantity, so \(d_{2^j}\le2^{-j}\mathcal S_{2^j}\). Dyadic rank groups give

\[
V_r\le\sum_{j\ge0}2^{j/r-j}\mathcal S_{2^j},
\quad
\|V_r\|_{3/2}\lesssim\|F\|_3\|G\|_3
\sum_{j\ge0}(1+j)2^{j(1/r-1/2)}.
\]

The sum converges precisely in the stated range \(r>2\) (`completion.tex`, lines 63–88). The estimate is uniform in the partition before taking the pointwise supremum. There is no fixed-partition exchange of supremum and norm.

Current `main.tex`, lines 127–218, correctly restricts this full estimate on fixed output boxes of area \(1/64\). The overlap length is at least \(1/8\), negative windows are included exactly by half-integer radial endpoints, and the common error satisfies \(|\delta_k|/\ell\le3/(13k^2)\). Disjoint shells bound its whole variation by an absolutely summable kernel. The norm factor is exactly \(8\,4^{2/3}C_r+\pi^2/13\). No null phase evaluation or shrinking width is used.

The finite-window orbit argument `main.tex`, lines 223–266, handles arbitrary commuting invertible transformations by invariance, Cauchy–Schwarz, and the Følner box ratio. It first fixes the finite truncation menu and only later takes the countable variation supremum. Finite scalar variation implies a Cauchy sequence by ordered disjoint pairs; the maximal bound supplies domination for the full tail norm and complex bilinearity (`main.tex`, lines 268–285). The stated no-\(r=2\), no noncommuting, no one-sided Cesàro, and no extended-input-exponent boundaries (`main.tex`, lines 287–300) are accurate.

I specifically attacked changing support, complex phase, small variance, covariance normalization, the Fourier coefficient normalization, discontinuous hard cutoffs, simultaneous mask switches, negative lattice indices, output-dependent partitions, and all-scale/countable measurability. None exposed an unsupported central claim in the inspected current proof. The source's Lean scope is not needed for this verdict and is not claimed as formal verification by the candidate.

## Reviewed source hashes

SHA-256:

```
main.tex: b487be2a3233d56facde9713681733e5e6d7a8539ff6d78a94cf7d7db796f10f
completion.tex: 0d14e5d2a234b36044627628ad1dd960929dd357f3b5fc4e85feb84fe3a7c7d3
consequences.tex: b2ce161f18a7e204d893a5792e5d1832ea2c9b3de24eec26c6278c202341c64f
frequency.tex: d7c8163675bcee6040efcab72c6ad0146aed9eccc00ee42d933382f0e6213ec2
heat.tex: c6a85b01fdecf3a7b03bf3ba25ec03a3da68ab71c3c85c5d82da139ce1ebd3c6
introduction.tex: 0c1678042ab9a0e3c5c21c1acd280d1a43b8e3c65e019bf78f7509a49f26422e
matrix.tex: 914af3c5e87cd4af52b1c7a9e7f2a4ac03d82b9456b8be50b69ffbbbee59f9ad
preliminaries.tex: 305281fb7f26046eea88b4087beba843ab6e48a62be6158f3a987bd91a68ddb0
rough.tex: f5a80e111befed4781b7a9b0d75f2b8d15646c08580c3ad98fe95d48bc877064
smooth.tex: dc964effac57c11797de4dba23fa8137978baec49c430f43a46324f49ecc08ee
```

## Additional adversarial cross-check

An additional unprimed internal agent was assigned the matrix, heat, frequency, and rough primary sources only. It returned: **no substantive flaw and no unresolved mathematical gap found within those four files**. Its independent checks reconstructed support/order comparison at `matrix.tex`, lines 326–340; cubic trace and complex-phase recovery at lines 344–444; fixed-support heat differentiations and neighbor comparison at `heat.tex`, lines 97–143 and 238–258; exact modulated Gaussian identity and bounded prefactor at `frequency.tex`, lines 183–213; common-support convexity and the factor \(\theta s\) at lines 170–223; boundary covariance, determinant, and Gaussian domination at lines 83–127; the averaged heat coefficient \((2+\theta)+(1-\theta)=3\) at lines 242–253; single-edge and square-coefficient payments at lines 264–380; and Plancherel plus frequency normalization at `rough.tex`, lines 178–193 and 240–274. It made no files or Git changes.

The exact analytic remaining gap after this reconstruction and independent cross-check is **none identified**. This is evidence from two direct analytic reconstructions; it is not formal certification. No numerical evidence is used as proof or included in the candidate package by this audit.
