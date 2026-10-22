# Independent analytic freeze: global minimizer family

UTC: 2026-10-16 05:20:12. Completion estimate: 70% of this audit. Original research effort remains 1/5. Prior source/audits conclusions remain unread. No other-family findings received.

## Independently reached provisional conclusion

The candidate's global-minimization mechanism is mathematically sound PROVIDED its explicit special real filtration and central-ring identification in PROOF §6 hold. I have not found a torus-only/global inference gap: the proof uses a product soliton to establish central weighted K-semistability, then the global Han–Li criterion. That criterion genuinely quantifies over all valuations on the ORIGINAL variety, including valuations not of product form. BLXZ supplies absolute uniqueness and identifies the first canonical degeneration. This is a conditional applicability finding, not independent certification of the geometry or irrationality families.

## Actual primary controls checked

- Han–Li, arXiv:2009.01010v1 (actual PDF SHA256 939691d9bd0c24444f43b944b91c1ac9684fef628d3b23393cc7f6fd3b5db0ff), printed p. 3 Theorem 1.5 equates infima over all linearly bounded filtrations, special test configurations, and all real valuations. Printed pp. 33–34 Theorem 5.3 explicitly says a valuation inducing a special real test configuration is a minimizer over Val(X) iff its central pair is Ding/K-semistable. The converse proof degenerates an arbitrary special competitor, and Theorem 1.5 then gives the full-domain result; no product restriction occurs.
- Han–Li printed pp. 20–21 Definitions 2.42, 2.46, Theorems 2.43–2.44 and equations (110)–(115) fix g(x)=exp(-<xi,x>) and its sign, with an explicit opposite-sign warning relative to Tian–Zhu. Printed p. 28 Definition 4.1 gives beta-tilde(v)=A(v)+log integral exp(-lambda) dDH_probability. Printed p. 8 Definition 2.8 and p. 19 Lemma 2.37 distinguish raw valuation filtration from the canonically normalized special action.
- BLXZ, arXiv:2103.15278v4, actual PDF (June 21, 2023) SHA256 8d56f0d92d9146ea85c53be8c04fc02e90f4b09a57fc3f591a996d1b040c1351, 443588 bytes: printed p. 2 Theorem 1.2 asserts unique valuation computing h, finite generation, and first degeneration. Theorem 1.3 gives K-polystability iff KRS existence for klt log Fano pairs. Printed p. 18 Theorem 4.9 gives generalized soliton existence iff reduced uniform g-Ding stability; Definition 4.10 specializes g=exp(-x). Printed p. 25 Corollary 5.9 upgrades g-Ding polystability to reduced uniform stability. Remark 5.10 resolves dependence on the chosen torus.
- Miao–Wang arXiv:2401.13999v2, actual PDF SHA256 85285e55a256fe342d511f716530ed790801d695bdd5f21090ff9d56039b8049, printed p. 9 Theorem 2.14 gives the valuative global criterion. Printed pp. 10–12 §3.1 explicitly identifies family 2.23(a), the ord_Htilde degeneration, positive scalar a, discrepancy shift by 1, and the exact measure rho(s)=(2+s)^2 on [-1,0], (2-s)^2 on [0,2]. Printed p. 12 Theorem 3.2 supplies weighted K-polystability of the first factor. Thus the proof's prior-result dependence is explicit and central, rather than circular.
- Han–Li generalized YTD actual body: printed p. 3 equation (6), Definition 2 and p. 4 Theorem 7/Remark 8 apply to klt singularities and finite-energy potentials. Printed p. 17 Corollary 31 gives boundedness on a resolution of weak KRS potentials. Wang–Zhu actual body Theorem 1.1 (preprint p. 1) supplies toric existence; §2 Lemma 2.1 and ensuing integral characterization supply the unique vector field, with the sign translated using Han–Li conventions.

## Checkable normalization calculation

On X=V×S, let k be E-order, and (i,j) the S-character of a degree-m section. The raw valuation weight is lambda=ak+b(j+m). Since A_X(v)=a+b, the canonical weight is lambda-mA=a(k-m)+bj. Write s=k/m-1 and y=j/m. Then the normalized DH probability law is the product of rho(s) ds/5 and (2+y)dy/4, and

beta-tilde_X(v) = log[(1/5) integral_{-1}^2 exp(-as)rho(s)ds] + log[(1/4) integral_{-1}^1 exp(-by)(2+y)dy].

This formula checks the sign and normalization on the explicit candidate. At a=b=0 it is 0. The derivative at zero in the two coordinate directions is respectively -1/12 and -1/6; hence the positive a,b orientation decreases H. Positive scalar rescaling is not an invariance: the exact scales matter. This separable formula is NOT being used as the global proof.

The character calculation ord_D(z^i w^j)=j and section order j+m is consistent with the inward normal (0,1), and with subtracting b rather than adding it in the canonical action. The valuation lies on K(X); its center E×D and discrepancy a+b agree with the SNC local monomial model. Nondivisoriality requires a/b irrational and remains assigned to the independent family.

## Product soliton: bounded justification of the only analytic product step

Use normalized Monge–Ampere measures MA_n(phi)=omega^n/n!. If factor canonical metrics solve exp(-theta_Z)MA_3(phi_Z)=exp(-phi_Z) and exp(-theta_S)MA_2(phi_S)=exp(-phi_S), then phi=phi_Z+phi_S and theta=theta_Z+theta_S satisfy

MA_5(phi)=MA_3(phi_Z) tensor MA_2(phi_S),
exp(-theta)MA_5(phi)=exp(-phi_Z-phi_S).

The first identity is the binomial expansion with the factorials included. The product canonical bundle is the exterior tensor product, so the right side is its canonical volume. Pullbacks to resolutions have bounded potentials (Han–Li Corollary 31); Bedford–Taylor/nonpluripolar products have no mass on the analytic singular locus. Equality on the regular locus therefore extends as an equality of measures. The metric is invariant under the product tori, and hence under the smaller torus generated by the candidate vector. BLXZ Theorem 1.3 gives K-polystability, hence semistability. This supplies exactly the hypothesis of Han–Li Theorem 5.3, without assuming H-minimizers tensorize.

## Boundary attacks and remaining review work

No unsupported product additivity theorem, torus-only reduction, uniqueness only up to scaling, or wrong-variety substitution was found. The actual global criterion requires a SPECIAL real degeneration, not merely a finitely generated graded ring of an arbitrary valuation; candidate §6 claims the requisite klt anticanonical central ring and construction. Need record an explicit bounded clarification that finite generation means finite generation of the real-weight filtration in the standard geometric sense, rather than a literal semigroup algebra over every element of a dense ordered rank-two group. This is a wording/definition subtlety, not currently a counterexample.

Pending: save final theorem-control table and complete safe manifest/privacy checks; optionally inspect previous reports only after transmitting this substantive freeze. No historical priority verdict is made.
