# Root mathematical reconstruction of PR466

Frozen eligible head:77a27c5da92b8f42f79b2f27e40f5c9a6403ddb9. Mathematical verdict: no identified universal-claim blocker after full proof reconstruction; independent families remain pending. This is bounded AI-assisted analysis, not formal or human certification.

## Exact source and literal counterexample

Independently retrieved and visually inspected printed1763 of the [official report](https://ems.press/content/serial-article-files/46174), SHA15854a33755fcaae9620944f730823932f48c32f6a56b9ce057c0b1b5862e54f. The source defines normalized equator averaging on all continuous functions and its measure dual on all probability measures, using intrinsic spherical distance and finitep>=1. Its discussion explicitly admits translating point masses; no evenness, support or antipodal quotient appears. Normalized kernel measures have mass1, so no renormalization affects their dual probability images. Equators at u and -u coincide as measured sets. Thus Rdelta_u=Rdelta_-u while the unique coupling of those inputs costs pi^p and W_p=pi. This directly rules out any finite inverse constant, and any vanishing inverse modulus, on the stated class. It does not by itself say anything about injective even probabilities.

Workshop/report volume is2008. The [publisher metadata](https://ems.press/journals/owr/articles/2042) states publication30June2009. The historical SOURCE_GATE claim that a catalogue2009 label conflicts with the2008 report is overstrong: volume/workshop and publication year differ legitimately. This provenance wording issue does not affect the question or counterexample. Record the correction here, with frozen originals intact.

## Harmonics and density action

Take the Haar law of an ordered orthonormal pair in R^n. Its first vector is uniform, its second is conditionally uniform on the corresponding equator, and swapping the columns preserves the law. This proves self-adjointness and R(rho sigma)=(F rho)sigma, including normalized measures and the equal-weight n2 equator.

For H_k=Re(x1+i x2)^k, the planar second derivatives cancel, Euler gives degree k, and polar Laplacian gives eigenvalue L=k(k+n-2). Ambient gradient norm is k*r^(k-1); tangential projection cannot increase it. Hence H_k/k is globally1-Lipschitz along minimizing intrinsic geodesics. A planar rotation bypi/k negates H_k; mean0 follows. Even positive k gives antipodal evenness. Fix0<a<1 before varying k, so1+aH_k is always normalized, smooth, and bounded in[1-a,1+a]. No uniform derivative bound follows or is claimed.

The moment identity follows by decomposing an isotropic Gaussian into independent radius and uniform direction. Its real-vector polynomial identity extends to complex vectors with the bilinear form. For w=e1+i e2 and projectionP=I-uu^T, w.w=0 and (Pw).(Pw)=-(w.u)^2. Using equator dimension n-1 yields the stated nonzero lambda_(2m)=(-1)^m product(2j+1)/(n-1+2j). Hermitian replacement would invalidate this step; none is used.

For n>=3, independent Gaussian squares give r²~Beta(1,alpha), alpha=(n-2)/2>0. Uniform independent planar angle gives integral H_k²=M(2k)/2, and gradientLp<=k*M(p(k-1))^(1/p). All real finitep>=1 are admitted by beta integration; integrality only applies to positive even k.

## Transport reconstruction and inequality direction

For any coupling, the1-Lipschitz test H_k/k yields inputW1>=a*M(2k)/(2k)>0. ProbabilityL^p monotonicity yields inputWp>=inputW1. This is an elementary coupling inequality, so neither KR attainment nor a stronger metric equivalence is needed.

Let b=a*lambda_k, eta_t=1+t*b*H_k and v_t=b*gradH_k/(L*eta_t). Its denominator stays>=1-a on the compact time-sphere cylinder. Every fixedk has a smooth global flow. Divergence of eta_t*v_t equals-b*H_k, so the continuity equation holds with the stated sign. If J_t is the flow surface Jacobian, d/dt(eta_t(Phi_t)*J_t)=0; its initial value1 proves (Phi_t)#sigma=eta_t*sigma directly.

The graph coupling has endpoint distance no greater than path length. Jensen over the unit time interval then bounds itsp-cost by integral|v_t(Phi_t)|^p. Change of variables contributes eta_t, leaving eta_t^(1-p), bounded above by(1-a)^(1-p). This remains correct forp1 and every real finitep; atp1 that density factor is exactly1. Cancellingk againstL gives the output upper bound in the author proof. Since b≠0 and H_k is continuous nonzero, output differs fromsigma, so its actualWp is strictly positive. Division combines an input LOWER bound with an output UPPER bound in the correct orientation.

## Asymptotic and boundaries

Fixed-parameter gamma-ratio asymptotics give M(2k)~C1*k^-alpha, |lambda_k|~C2*k^-alpha, M(p(k-1))^(1/p)~C3*k^(-alpha/p), eachpositivefiniteconstant. The ratio bound is therefore~C*k^(alpha/p) with C>0, diverging for everyfixedfinitep andn>=3. It is not the actual ratio asymptotic, a sharp rate, or a bound uniform as p grows with k. No evenWinfinity result follows.

For n2, Rmu averages the quarter-turn and opposite quarter-turn. For evenmu the two pushes agree, so R is a single isometry. A beta formula with parameter0 is never used there. For n1 no normalized equator exists. Endpoints a0 and a1, constant/odd harmonic modes, finite bandwidth, derivative-bounded and restricted-support variants are excluded correctly.

Even probabilities lift projective probabilities symmetrically. Projecting any spherical coupling decreases distance. Conversely choose the cheaper antipodal sign for each projective pair and symmetrize the lift; its marginals are the unique even lifts and its spherical cost equals quotient cost. Thus merely quotienting antipodes cannot restore the same-order Lipschitz inverse in the proved even-density regime.

## Reproduction and priority separation

All29 references in three historical manifests match exact frozen SHA256/size. Four root replays reproduce591 author and3812 earlier independent controls byte for byte normally and optimized. The explicit check functions raise independently of Pythonassert optimization; the few internal domain asserts are called only on in-domain fixed loops. These diagnostics verify finite algebra/transcription, not infinite asymptotics or a continuum transport theorem. Fresh independent spectral controls are pending.

The original negative answer is a direct classical parity consequence; the same [normalized Funk transform and odd kernel](https://link.springer.com/article/10.1007/s13324-020-00383-2) are documented before this investigation. Precise prior printing of a Wasserstein sentence is a separate documentary question. Any possible novelty of the strengthened even-density statement cannot turn the unrestricted original question into a novel solved open problem. Independent priority reports and a new disposition adversary must test this classification before status action. No paper or remote disposition has been prepared.
