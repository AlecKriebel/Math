# Author turn 1: cover-stable obstructions and the residual torsion route

**Scoped partial deductions; the original existence question is unresolved.** This turn tests the direct invariant-obstruction strategy. The foliated norm obstruction in the source cannot distinguish the downstairs failure from an upstairs success; ordinary rational characteristic classes cannot do so either. The residual torsion and non-equivariance issues are identified, not solved.

## 1. Exact transfer formula for the foliated seminorm

Let p:N to M be a finite unbranched covering of degree d and let F be a foliation. Work with ordinary real singular homology and the transverse-chain seminorm used in the source, in any degree for which it is defined. If Tr is the homology transfer, then

||Tr(a)||_(p*F) = d ||a||_F.                         (1)

Indeed, a transverse singular simplex has exactly d lifts, and every lifted simplex is transverse to the lifted foliation with the same affine pullback condition. Summing the lifts defines a chain map with l1 norm at most d times the original norm. Thus the left side is at most d times the right seminorm. Conversely, pushing a transverse chain on N down to M preserves transversality and cannot increase its l1 norm. The chain identity p_* Tr=d id, together with absolute homogeneity of the seminorm, gives the reverse inequality. Infima need not be attained, and regularity of the covering is unnecessary. The argument also works for infinite seminorm values in the extended sense.

This is the ordinary covering counterpart of the credited norm functoriality in Calegari's Lemma2.2.7. It is not a new invariant.

Suppose now that isotopic copies of p*G converge to p*F in the plane-field topology of the cited semicontinuity theorem. Every isotopy acts trivially on homology and preserves the foliated norm of a fixed homology class. Theorem3.1.2 therefore gives

||Tr(a)||_(p*F) >= ||Tr(a)||_(p*G).

By (1), ||a||_F>=||a||_G downstairs for every a. This recovers the original Question13.4 remark by a chain-level argument. Consequently, finding a strict norm inequality in the opposite direction cannot produce the requested downstairs-only obstruction: it would already rule out the stipulated upstairs convergence. The source's usual branching obstruction is likewise unchanged under a finite cover, because the lifted universal-cover foliation and its leaf space do not change.

These deductions use the source's actual semicontinuity hypotheses. They do not assert a converse from norm inequalities to geometric convergence, or extend a theorem to a different noncompact topology without verification.

## 2. Plane-field homotopy imposes additional necessary conditions

For this section assume M is closed and connected, and use uniform geometric convergence of continuous tangent planes. A connected finite cover suffices; if an originally chosen cover has several components, an isotopy starting at the identity preserves each component and one may restrict to it.

Let h_n be endpoints of isotopies starting at the identity on N, with h_n(p*G) converging to p*F. For sufficiently large n the two limiting-nearby distributions are connected by the short Grassmannian homotopy pointwise. Compactness makes a common small-angle neighborhood available. The distribution h_n(p*G) is itself homotopic as a plane field to p*G along the isotopy. Hence

p*(TG) and p*(TF) are homotopic unoriented plane fields.   (2)

No convergence of derivatives of h_n, of Godbillon–Vey forms, or of isotopy paths is needed. Only the actual tangent distributions converge.

Let nu_F and nu_G be the normal line bundles. Equation (2) gives

p*(w_1(nu_F)-w_1(nu_G))=0 in H^1(N;Z/2).

The cohomological transfer composed with pullback is multiplication by d. Thus an odd-degree cover forces w_1(nu_F)=w_1(nu_G) downstairs. A difference of normal orientability classes can only be hidden by an even-degree cover. This is a necessary restriction, not a realization of such an example.

If M is oriented and both F and G are cooriented, choose their induced tangent-plane orientations. Because the original convergence is unoriented, it permits a global sign choice on connected N. For some sign sigma in {+1,-1}, (2) yields

p*(e(TF)-sigma e(TG))=0 in H^2(N;Z).

Applying cohomological transfer gives

d(e(TF)-sigma e(TG))=0.                             (3)

In particular e(TF)=sigma e(TG) rationally. If H^2(M;Z) is torsion-free, the equality holds integrally. When convergence is explicitly coorientation-preserving, sigma is +1; that extra requirement is not silently imposed on Question13.4. Ordinary integral cohomology H^2, rather than homology H_2, is meant in this assertion.

The transfer identity used here can be checked on singular cochains by evaluating a cochain upstairs on the sum of all lifts of a downstairs simplex. Evaluating a pulled-back cochain on that sum returns d times its downstairs value. Characteristic classes are then used only through their standard naturality and homotopy invariance.

Thus a proposed rational Euler-class distinction is incompatible with the cover premise. Torsion Euler differences killed by the chosen cover are not excluded by (3), but no taut-foliation realization, upstairs isotopy or limit construction is obtained from their formal possibility.

## 3. Equivariance pinpoints a genuine missing step

For a regular cover with deck group D, suppose there actually exists a convergent sequence of isotopies H_(n,t) upstairs for which every H_(n,t) commutes with D. Each entire path descends to an isotopy on M starting at the identity. Since pullback by a finite covering identifies downstairs distributions with the D-invariant distributions upstairs and preserves local convergence, their endpoints give the required downstairs convergence.

This proves descent under an explicit equivariant-isotopy hypothesis. The original problem does not supply that hypothesis. Invariance of the initial and limiting foliations does not imply that each intermediate foliation or each isotopy path is D-invariant. No averaging argument is invoked: averaging tangent forms need not preserve integrability, while averaging generating vector fields need not preserve the endpoint orbit-limit behavior.

A nonregular cover cannot simply be declared regular without checking that the given isotopies lift to the chosen further cover. That bookkeeping would be a separate step in any construction or descent theorem; none is needed for Sections1–2.

## 4. Outcome and next route

The direct real-norm and rational-characteristic-class counterexample strategies are obstructed by the cover premise itself. A successful example needs a subtler downstairs obstruction, potentially torsion or a failure of equivariant orbit closure, together with an actual pair of taut foliations on a hyperbolic manifold. Conversely, the elementary equivariant descent result does not prove arbitrary isotopies can be made equivariant.

One substantive author turn complete; original unresolved. Next turn should attack the residual finite-group equivariance mechanism or an explicit taut-foliation construction rather than repeat the norm inequality. These arguments are exact deductions, so no numerical simulation or irrelevant finite checker is offered as a proof substitute. Completion estimate15%.
