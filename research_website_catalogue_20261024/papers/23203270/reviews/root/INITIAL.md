# Root source-first reconstruction — row188 /23203270

17 November 2026 UTC. Initial scientific coverage estimate35%. No final disposition. The complete362-line native TeX, all six native PDF text pages and all six fresh root-rendered page images have been personally read. Native API metadata and its complete Description were read. Current scope/adversarial mathematical findings, imported primary proof bodies, archived audits and symbolic code have not been opened. The earlier rights exposure is explicitly retained in PRE_ORIGINAL_RIGHTS_EXPOSURE_20261117.json: it included author assertions about inherited cancellation/nonpolynomiality and an explicit five-component consequence. Thus this is original-first proof reconstruction with disclosed author assertions, not zero-exposure blindness. Native paper/Description themselves also contain favorable audit assertions; these are hypotheses, not proof premises.

The controlling outer manuscript is Zenodo23203270 paper.pdf,74424B, SHA256c579ec3442f4bcdf68ed737ad8bc65328682158845ed2e14e6636b2b119f52c6. The declared date is6October2026, created7October04:54:17.591002UTC, updated10October21:27:07.249789UTC. Native version field is absent; do not invent v1. Native assets are ZIP then PDF. Original authored content is CC BY4; bundled OpenAI Lean/config material retains Apache2. Original manuscript title: An explicit complex polynomial retract in five variables: a consequence of affine-space cancellation failure.

## Exact original claim and central dependency

Over C, P=C[p,s,u,F,J], x=s²+u³+p²F and H=x²F−(1+2sx)J−p²J²−pu. A=P/(H) should be smooth integral of transcendence degree4, have an explicit cylinder A[w]≅C[p,s,u,m,e]=B, split maps i:A→B,r:B→A with ri=id, and a five-component polynomial idempotent ir whose image is nonpolynomial. The concrete maps must remain polynomial at p=0. The decisive nonpolynomiality statement A not≅C^[4] is imported from the exact cited OpenAI theorem; it does not follow from checking coordinate identities or random examples. No ambient-four-variable claim is made. The general inclusion/evaluation cylinder-to-retract mechanism is classical and credited.

## Own check of the polynomial flow

On p≠0 use y=s+x(x−u³),z=sx+p²J. The inverse coordinates are s=y−x(x−u³), F=(x−s²−u³)/p², J=(z−sx)/p². Define Δ=−p²∂u holding p,x,y,z fixed. Differentiating x,y,z gives Δs=−3p²xu², ΔF=(6sx+3)u², ΔJ=3x²u². These are polynomial in the original ring, so the locally nilpotent localized derivation restricts to P. In those coordinates H=p^−2(xy−z(z+1))−pu, giving ΔH=p³.

Write D=((u−p²w)³−u³)/p²=−3u²w+3p²uw²−p⁴w³. The source formulas preserve x,y,z: changes to s and u³ cancel in y; changes to s and J cancel in z; expansion of s²+u³+p²F cancels its D terms. They are the stated exponential flow and have inverse with parameter−w. Consequently ΦH=H+p³w and Φ gives A[w]≅T=P[w]/(H+p³w), with a two-sided polynomial inverse. This does not depend on the unproved nonpolynomiality input.

## Own check of the cylinder formulas

Put x0=s²+u³. The (F,J)→(L,M) matrix is [[x0²,−(1+2sx0)],[1−2sx0,4s²]]. Its determinant is4s²x0²+(1−2sx0)(1+2sx0)=1. Hence f(L)=4s²L+(1+2sx0)M and j(L)=(2sx0−1)L+x0²M are exact inverse coordinates. Expanding the original equation gives H(L)=L−pu+p²Q(L)+p⁴f(L)³ with Q=2x0f²−2sfj−j². Its constant C=M²(2x0+6sx0²+4s²x0³−x0⁴) and coefficient formulas q1,q2 follow by ordinary quadratic expansion, so Q=C+LQ1 has no division.

Set L*=pu−p²C, h=u−pQ−p³f³−p²w and t=H+p³w. Then t=L−ph. With e0=−w−pf³−Q1h, direct expansion gives p³e0−(L−L*)=(p²Q1−1)t. Also H(L*)=p³[(u−pC)Q1(L*)+pf(L*)³]. Both are exact identities in the coefficient polynomial ring, before passing to a quotient.

In B let ell=L*+p³e=p(u−pC+p²e), and W=−e−(u−pC+p²e)Q1(ell)−pf(ell)³. Expansion immediately gives H(ell)+p³W=0. Substituting into h gives h(ell,W)=u−pC+p²e, since p ell Q1 cancels p²(u−pC+p²e)Q1. Thus e0(ell,W)=e. The map g:T→B and q:B→T recover all B generators, while qg recovers p,s,u,M,L via the determinant-one change and the certificate. To recover w, the defining equation implies p³(qg(w)−w)=0. Cancellation is justified by the independent domain argument below, not by evaluating only p≠0 and ignoring torsion.

## Own check of domain, smoothness and dimensions

In P[p^−1] the coordinates p,x,y,z,u are independent and H has unit u coefficient−p. Thus H is irreducible/prime there. A factor becoming a unit on localization would be a constant times a power of p, since P is a UFD. But H mod p=L is nonzero, so p does not divide H; no such nonunit factor occurs. Therefore H is irreducible and prime in P, A is a domain and p is nonzero in it. Localization A[p^−1]=C[p,p^−1,x,y,z] has transcendence degree4. This supplies the cancellation needed above without circular use of nonpolynomiality.

For p≠0 the Laurent polynomial presentation is smooth. At p=0, partials H_F=x0² and H_J=−(1+2sx0) cannot vanish simultaneously by the determinant identity. The hypersurface Jacobian criterion gives smoothness everywhere. This is over characteristic0; no implicit extension to positive characteristic is made.

## Own check of retraction, spectra and zero fiber

With theta=g Φbar, coefficient inclusion j:A→A[w] and evaluation epsilon at w=0 give i=theta j and r=epsilon theta^−1. Thus ri=id, (ir)²=ir and image(ir)=i(A). All displayed r and i formulas are the corresponding compositions: evaluation removes every exponential correction, while inclusion substitutes the factored W into the flow. No denominator occurs in a final map.

On spectra, Spec(r) is a closed embedding because r is surjective; Spec(i) is its retraction. Kernel(ir)=kernel(r) since i is injective, so the scheme-theoretic image has coordinate algebra B/kernel(r)≅A. This checks the reversed order of maps and the scheme-theoretic image claim, not merely a set-theoretic point image.

At p=0, ell=0, f=(1+2sx0)m,j=x0²m and W=−e−u kappa m, where kappa is the polynomial bracket q1/m rather than a rational division. S=s,U=u,D=−3u²W, and the transformed F,J are the same determinant-one column times m'=m+3u²W. Hence rho=(0,s,u,m',−u kappa m'), and its next W is0. A second application fixes it identically. This independently checks the limiting fiber; the source has not silently thrown it away.

## Strongest result and exact remaining gap

The explicit polynomial cylinder, split maps, idempotence, image, domain/smoothness/dimension and zero-fiber mechanisms pass this original-only reconstruction. Conditional on the precise imported nonpolynomiality theorem, the image cannot be a polynomial algebra in any number of variables, since its transcendence degree is4. The manuscript's brief summary of degeneration, normalized additive lift, auxiliary leading derivation and rigidity is not a substitute for those actual proof bodies. In particular, formal source names, purported static checks and favorable author audits are insufficient to establish that central input.

Remaining work: authenticate complete original source bytes/modes/topology, inspect actual pinned primary Sections3–6 and any essential lower-level proof interfaces, then compare the two independently sealed current reviewer families; inspect actual symbolic code/certificates and one appropriate ordinary native attempt already made by a family before any extra execution. Source-only native scientific executions0. No final scientific verdict or defect alleged merely because an input is unread. No private/promotional page, Sheet canonical URL, website publication, new priority claim or follow-up is approved. Follow_up=null. If a substantive written-proof gap survives review, defer the complete original in the Sheet and move on without a repaired promotional substitute.
