# Independent check of the shorter bridge and its historical limits

This check occurred after `INDEPENDENCE_CHECKPOINT.json` was frozen. It examines the complete bridge subsequently supplied for combination; it does not convert a current derivation into an earlier printed theorem.

## Mathematical check

Kunisch-Meinlschmidt Theorem 4.3 in [arXiv 1907.02744v1](https://arxiv.org/pdf/1907.02744v1), printed 19-21, states Frechet C2 differentiability from L1(0,T;H) into the energy/Strichartz state space. Its displayed derivative formulas give, at zero energy data/control, `S(0)=0`, `S'(0)=L`, `S''(0)=0`. The complete printed proof was read, but its claimed invertibility onto arbitrary C([0,T];E) has a codomain problem: at zero the derivative is minus the trajectory embedding, which cannot be onto arbitrary continuous energy pairs. Those pairs need not be derivative-compatible or have the required additional Strichartz regularity. This is a limitation of the printed argument, not a disproof of the differentiability statement. The local repair below establishes exactly the derivative fact needed here and thus the Banach-space Taylor conclusion

`||S(u)-Lu||_Y = o(A^2)`, uniformly as `A=||u||_L1 -> 0`.

The required local repair is checkable using only the earlier Lemma2.9 wave bound and the interpolation used by the source. Let Y0 be the Banach space of zero-initial-data position trajectories with continuous-energy pair and L4(L12) norm. The linear Duhamel operator L maps L1(H) boundedly into Y0. The quintic map N(y)=y^5 is a continuous five-linear diagonal polynomial into L1(H), because Y0 embeds continuously into L5(L10). Define Phi(y,u)=y-Lu+L(N(y)) as a map Y0 x L1(H) to Y0. It is C2 (in fact polynomial), and D_yPhi(0,0)=I on Y0. The Banach implicit-function theorem, in this correct codomain, supplies a local C2 mild solution map. Differentiating at zero gives S-prime=L and S-second=0. Source uniqueness identifies it with the actual state. No claim to certify the printed broad global inverse argument is needed. This is a present elementary local repair of the source argument using established analytic estimates, not a newly proved global differentiability theorem.

Uniformity means that the supremum of the remainder divided by A squared over controls of positive mass at most a tends to zero as a tends to zero. Endpoint H and H^-1 traces are bounded on Y.

For the chosen actual wave data, the eigenmode calculation gives `x=(e,y_u(1)) <= A/pi + d(A) A^2`, where `d(A)>=0` tends to zero. The exact tracking-plus-sparse expression, with all other terms nonnegative, is at least

`q_A(x)=A-pi x+x^2/2`.

For small A, `b=A/pi+d(A)A^2 < pi`. Since `q_A` decreases for `x<pi`, substitution into the **whole** expression is justified even for negative x. It yields

`J(u)-J(0) >= A^2/(2pi^2)-pi d(A)A^2+d(A)A^3/pi+d(A)^2 A^4/2 >= A^2/(4pi^2)`.

Thus zero is a genuine strict local optimizer in L1 and therefore also L2 and L-infinity. Any fixed positive pointwise cap can be used for this local conclusion. Smallness of the cap and the bathtub estimate are required for the submitted stronger global claim, not this minimal local core. This is a valid, short mathematical bridge; it leaves no unsupported central PDE-optimality assumption.

The ordinary source cone is `{0}` because the complete derivative is at least the integral of `(1-sin(pi t))||v(t)||`, positive for every nonzero Lebesgue direction. The only equality time has measure zero. Bounded truncation proves the full L1/L2 tangent cone; source subgradient and zero-multiplier conventions agree with the source.

The centered pulses `u_h=h e 1_(|t-1/2|<h)` have mass `2h^2`, squared L2 norm `2h^3` and L-infinity norm h. Their linear endpoint is `2h sin(pi h)/pi^2 e` and linear endpoint velocity is zero. The uniform Taylor remainder is `o(h^4)`. Consequently the real objective gap is

`(pi^2/3+2/pi^2)h^4+o(h^4)`,

and its ratio to squared L2 distance tends to zero. This directly refutes the source L-infinity-localized growth conclusion at the genuine local optimizer. It also refutes the OWR L2-neighborhood version. These calculations are a complete core counterexample before invoking a general NDC theorem.

## Prior abstract theorem and correct specialization

Borchard-Wachsmuth [arXiv 2311.14538v1](https://arxiv.org/pdf/2311.14538v1), uploaded 24 November 2023, contains Assumption 2.1 on printed p.4, NDC on p.6 and Theorem 2.18 with complete proof on p.15. Its [2024 final article](https://jnsao.episciences.org/14959/pdf), published 18 December 2024, has the same necessary-condition theorem at pp.12-13; current arXiv v3 is dated 17 December 2024 and matches final PDF bytes. Both versions were freshly retrieved, pinned, and read for the exact assumptions/theorem/proof. Theorem 2.18 says norm-squared growth implies NDC. Its proof substitutes the standing Taylor expansion into the growth inequality and divides by squared distance. It does not assert existence of any particular counterexample or wave target.

The Hilbert-space application is mathematically valid: take `X=Y=L2(0,1;H)`, `G=||u||_L1+I_U`, and `F` the smooth costs. H and X are separable. G is proper and closed convex. Source C2 Taylor expansion on L1 implies one on L2, since A is bounded by the L2 norm. The source gives bounded F-prime and F-second, with

`F''(0)[v,v] = ||(Lv)(1)||_H^2 + nu ||(Lv)_t(1)||_H^-1^2`.

For normalized pulses `v_h=u_h/sqrt(2h^3)`, the L2 norm is one and the sequence is weakly null; this follows by absolute continuity of any L2 test's integral on the shrinking interval. The NDC expression is exactly

`1/h - sin(pi h)/(pi h^2) + sin(pi h)^2/(pi^4 h)`

and equals `(pi^2/6+1/pi^2)h+O(h^3)`, tending to zero. Theorem 2.18 therefore excludes positive L2-neighborhood growth.

For the source's smaller L-infinity neighborhood, the bare application with G does not alone address that topology. This is easily repaired: if source growth held for `||u||_infinity < epsilon`, restrict G further to the closed convex cap `||u||_infinity <= delta < min(rho,epsilon)`. That set is L2 closed. All controls in it have the postulated growth, so BW's L2 quadratic-growth premise holds for the restricted G. The same pulses eventually lie in that set and have the same NDC expression, giving a contradiction. Alternatively the direct objective calculation already proves failure in L-infinity with no abstract theorem. This routine localization repair avoids overstating the theorem's bare neighborhood.

## Historical inference: what this does and does not establish

The shorter bridge is a valid present derivation using earlier published analysis and a familiar necessary-condition framework. It shows that the core does not require the stronger global-optimality machinery, O(A^5) contraction, target-response theorem, or optional enhancement. It supports calling the construction elementary and crediting the established mechanisms.

It does **not** establish that an earlier source already printed or resolved the actual wave counterexample. BW Theorem 2.18 does not choose the realizable adjoint/target, prove a corresponding local minimum, or supply the concentrating controls. Theorem 4.3 states a differentiability theorem, not a negative existence theorem; its needed local conclusion has the codomain repair above, while the printed global inverse step is not certified. Their application here still includes the choice `target=pi e`, the threshold maximum, the composite scalar local-minimum calculation and pulse witness. All inputs being old is not sufficient: many new applications are proofs from old tools.

A genuinely routine specialization of an earlier covering negative theorem would count under the stated priority criterion, even without an earlier verbatim example. No earlier theorem supplying the central counterexample class was located in this bounded audit. Therefore this shard cannot promote the valid bridge into **verified historical prior resolution** merely because the calculations are short. The degree of mathematical routine-ness is an editorial/novelty judgment; it is not an authenticated priority date for the wave construction.

The strongest defensible recent recommendation is: retain the scoped mathematical negative theorem and its explicit zero-cone mechanism, strongly credit the old source/framework, and refrain from worldwide firstness; **do not equate novelty uncertified with already solved**. An authenticated earlier negative local-optimizer result or a genuinely covering theorem plus parameter specialization would change that recommendation. The stronger auxiliary results cannot retarget the core gate around such evidence if it appears.

No classification or publication action is taken by this check. The initial independent checkpoint remains byte unchanged. The earlier draft report and mistaken hand-estimated timestamp log are privately preserved as history; public research log records the correction and subsequent combined check.
