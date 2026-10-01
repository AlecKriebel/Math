# Independent full review: the Airy worked example

**Verdict: PASS_COMPLETE_WORKED_EXAMPLE_SOURCE_TARGET. No mandatory mathematical correction.**

This verdict binds `PROOF.md` SHA-256 `c3f2da4e8764d9aa1e8007e548161db44b41b322bd4bf8537fda520cadd2b7b7` and `FROZEN_MANIFEST.json` SHA-256 `d0758639b6f29e98b9da14cc23d035d6ec88868edd7dbe0a103a132182aef6ab`. All fourteen listed author artifacts remain unchanged. The source checkpoint is preserved as a historical input. I did not contribute to the author route.

The accepted outcome is one explicitly normalized relationship among a genuine wild harmonic bundle, its compact conformal connection limit, the Airy scalar oper, and the all-order WKB/EO/DM expansions. The first substantive turn supplies that worked example. This is a source-scoped classical-consequence result, with no finding of historical novelty. It is **not** a proof of convergence of the harmonic family's Stokes data or a general wild conformal-limit theorem.

## 1. Exact original scope

I independently read the recovered primary Problem 1.28 and the official AIM workshop page. Boalch asks for the relation among the four named constructions in at least one example. The original contains neither an Airy restriction nor an explicit demand for convergence in a topology controlling Stokes filtrations. The imported/generated title cannot add those requirements.

All four named objects occur in the candidate: the radial harmonic metric satisfies the actual wild Hitchin equations and prescribed end growth; its flat twistor family has the stated compact limit; that limit is the Airy oper; and both recursions produce its WKB expansion in the specified normalization. This constitutes the requested worked relationship. The qualification about the topology is essential to that judgment and must remain prominent in any summary. No general moduli-space identification, equality of differently extended holomorphic bundles or full description of wild nonabelian Hodge theory is inferred.

## 2. Radial existence, frame and Hitchin equation

The complete MSWW primary formulas in Section 3.2 supply a global positive radial Painleve solution with differentiated expansions at zero and infinity. Section 3.3 specifies the complex gauge taking the fixed holomorphic Higgs field `[[0,1],[x,0]]dx` to the unitary fiducial frame. Pullback of the unit metric gives exactly the author's H_R, rather than its inverse. This is important because the R-dependent unitary-frame Higgs entries themselves diverge at small R.

The metric scalar `v_R=(1/2)log(r)+h_R` satisfies

`v_(x barx)=R^2(exp(2v_R)-|x|^2 exp(-2v_R))`.

The Chern curvature coefficient is its negative on the first diagonal entry, and the commutator coefficient has the opposite sign. The factor one-quarter between the complex second derivative and the real Laplacian gives precisely the factor eight in the radial ODE. The choice `rho=(8/3)R r^(3/2)` yields the factor one-half in the Painleve equation. Holomorphicity and metric adjunction give the vanishing cross terms, so the displayed twistor family is flat for every nonzero zeta.

The differentiated expansion makes `k(z)=|z|^(1/2)exp(h_1(|z|))` a positive smooth radial function at zero. Its local expansion is in powers of |z|^2; the complete derivative bounds ensure actual smoothness, not merely a formal series. The metric and curvature identity therefore extend across the turning point. The classical radial solution is global on the plane, not just an exterior or punctured-disc construction.

## 3. This is a wild harmonic-bundle example

The ramified coordinate x=t^2 diagonalizes the Higgs field in the meromorphic eigenbasis `(1,t),(1,-t)`. The eigenforms of R phi are `+/-2R t^2 dt`, with primitives `+/-2R t^3/3`. In u=1/t the primitives have pole order three and the eigenforms pole order four.

Direct Hermitian multiplication gives the stated Gram matrix `2|t|` times the cosh/sinh matrix. The end expansion gives the decoupled growth and exponentially small normalized off-diagonal term, with the source's polynomial prefactors and differentiated estimates understood. The deck transformation exchanges the eigenlines, while the original metric descends. In the original basis the norm growth is |x|^(+/-1/4). These data are actual specified growth conditions at the irregular end.

Dumas–Neitzke Section 2.4 gives the same polynomial wild-Hitchin category and growth requirement. After swapping the two basis vectors, the candidate has polynomial P_2=-x. One can check the R convention explicitly: conjugating `R[[0,x],[1,0]]` by `diag(R^(-1/2),R^(1/2))` gives `[[0,R^2 x],[1,0]]`. The corresponding metric scalar changes from v_R to v_R+log R and its end growth is `(1/2)log|R^2 x|`, as required. This is a constant gauge at fixed R, not an identification of different displayed frames.

The candidate correctly keeps its affine meromorphic object separate from DM's chosen compactification lattice. Irregular type and the scalar oper are identified; equality of distinct holomorphic extensions without filtration shifts is not used.

## 4. The exact compact C-infinity limit

The scaling identity is exact, not asymptotic:

`H_R=diag(R^(-1/3)k(R^(2/3)x), R^(1/3)/k(R^(2/3)x))`.

Let epsilon=R^(2/3). Radial smoothness implies `grad log k(0)=0`. For the connection coefficient, one derivative brings an epsilon, and vanishing of the gradient at zero supplies a second epsilon on a fixed compact set. Higher derivatives are at least as small: for first additional derivatives the factor is epsilon^2, and higher factors are harmless for epsilon<=1. Differentiated smooth remainders justify this for every fixed seminorm. The constant diagonal R factors disappear under differentiation.

The two adjoint entries after multiplication by R^2 are respectively `bar(x) R^(8/3)k(epsilon x)^(-2)` and `R^(4/3)k(epsilon x)^2`. Positivity and smoothness of k bound both it and its reciprocal with all needed derivatives on the shrinking compact argument set. Thus both the Chern-connection error and adjoint contribution have the claimed O(R^(4/3)) bounds. Multiplication by hbar or its reciprocal is uniform on compact subsets of C*.

The result includes compact sets containing x=0. WKB expansions later use a simply connected domain avoiding the turning point, a different and correctly stated restriction. For compact families of finite paths, the usual parallel-transport integral equation gives the additional transport conclusion. None of these estimates is uniform at infinity as R tends to zero. Consequently none implies Stokes-coordinate convergence.

## 5. Scalarization and all-order recursion

The horizontal column `(psi,-hbar psi')` gives exactly `hbar^2 psi''=x psi`; no sign or factor-of-two discrepancy remains. The plus sign in the connection reverses the eigenvalue label of the positive WKB exponential, which the proof explicitly records. R tends to zero at fixed hbar before formal WKB expansion; the two limiting procedures are not interchanged.

The EO data, kernel and pulled-back differential sign give `omega_(0,3)=-dt_0dt_1dt_2/(2t_0^2t_1^2t_2^2)` and `omega_(1,1)=-dt/(16t^4)`. Stable integration from infinity gives the positive-sheet coefficients 5/48 and 5/64. Under the change from DM's coordinate s to t=-2/s, x and y become t^2 and t, the Bergman kernel is unchanged, and the source basepoint s=0 becomes t=infinity. The signs in DM's stable primitive formula cancel exactly under this substitution. The unstable logarithm agrees up to the expressly allowed constant normalization.

DM Sections 7.1–7.2 give the all-order Airy comparison, not merely low-order examples. The extra apparent residue is zero in this genus-zero setting. Remark 5.7's warning against a blanket higher-genus residue/PDE equivalence is preserved. With the source theorem applied, Riccati uniqueness fixes all derivative coefficients, and decay of the stable primitives at infinity fixes their constants. Classical Airy sectorial solutions realize the limiting formal expansions; this does not identify limits of sectorially normalized positive-R solutions.

## 6. Independent checks and final boundary

All fourteen author entries, the historical source checkpoint and all nine pinned reading inputs matched. The author's 103-control receipt replayed byte-for-byte. A separately authored checker, importing no author checker, passed **970 exact controls**. It reconstructs EO residue recursion through complexity four, obtaining stable principal coefficients

`5/48, 5/64, 1105/9216, 565/2048`,

and independently matches 64 Riccati/amplitude orders, Hermitian matrices, ramified growth algebra and compact Taylor scaling. The analytic existence and C-infinity arguments are reviewed above; finite coefficients are not treated as proof of the cited all-order theorem.

The accepted disposition can stop original research after this one substantive turn because the literal request is for one worked relation example. Classical sources and the exact scaling deduction must remain distinguished. No peer-review, community-validation, historical-priority, Stokes-limit or general wild-moduli claim is certified. Publication requires the parent's separate authorization.
