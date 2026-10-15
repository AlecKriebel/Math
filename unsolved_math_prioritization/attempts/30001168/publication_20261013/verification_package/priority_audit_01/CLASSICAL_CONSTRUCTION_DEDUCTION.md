# Classical-construction applicability check

Audit date: 2026-10-14 UTC. This note checks priority implications; it is not a new research effort or a replacement of the accepted proof.

The author proof has been read directly. Its decisive geometry is a long exact product cylinder with smooth compact caps, followed by volume normalization. The spectrum is bounded using all longitudinal Dirichlet modes, rather than a fixed number of eigenvalues or a spectral limit theorem. The resulting normalized heat mass approaches `sqrt(pi)/e`, which exceeds the independently verified all-time round bound. The finite authored example and rational certificate avoid any need to promote this limit argument into the theorem.

Ammann and Jammes's author manuscript dated 8 December 2008, corresponding to the 2011 chapter *The supremum of first eigenvalues of conformally covariant operators in a conformal class*, supplies an earlier conformal cylindrical-blowup mechanism. Section 3.2 defines positive smooth `F_L` equal to `r^-1` on the annulus `e^-L <= r <= 1/2`; Example 1 in section 2.5 gives the Yamabe cylinder threshold `(n-2)^2/4`. The first arXiv version was submitted in 2007. The chapter DOI is `10.1017/CBO9780511863219.002`. See the broader lane's source ledger for versions, hashes and complete locators.

For the round sphere conformal class, one may first choose a smooth conformal background that is exactly Euclidean in a coordinate ball. In stereographic coordinates the round metric is a smooth positive multiple of the Euclidean metric, so a smooth positive multiplier that cancels that factor in a smaller ball does this. The inverse-radius annulus is then an exact unit-radius product cylinder. This is a specialization of the earlier construction; an arbitrary background in the general theorem would only be asymptotically cylindrical.

One must also choose the permitted caps explicitly. A-J's inequality `F_L <= r^-1` below `e^-L` alone does not force the cap volume to be uniformly bounded for every permitted `F_L`. A fixed rescaled smooth radial cap `F_L(r)=e^L f(e^L r)`, with `f` constant near zero, equal to `1/x` near one and at most `1/x` on `(0,1]`, is permitted. Under `x=e^L r`, its cap volume is independent of `L`. Thus this specialization has cylinder length `ell=L-log(2)` and volume `4*pi*ell+O(1)` in dimension three.

On that cylinder the operator is `-d_s^2 + Delta_S2 + 1/4`. Extending the longitudinal, sphere-constant Dirichlet modes by zero and applying standard quadratic-form min-max gives

```
lambda_k <= 1/4 + (pi*k/ell)^2,
Tr(exp(-4Y)) >= exp(-1) * sum_{k>=1} exp(-4*pi^2*k^2/ell^2).
```

After volume normalization to `2*pi^2` and the corresponding time change, the elementary Gaussian sum estimate yields

```
liminf F_L(4a_L) >= sqrt(pi)/e.
```

Consequently an elementary strict all-time bound `C_round < sqrt(pi)/e`, such as the accepted proof's `C_round < 129/200`, completes an existence counterexample using this classical construction and standard spectral tools. No below-threshold fixed-index convergence theorem is required.

This audit therefore rejects any claim that the cylinder construction or its spectral mechanism is new. The qualitative negative conclusion is a straightforward assembled consequence of classical geometry, min-max and the round comparison. No earlier paper explicitly asserting that exact assembled conclusion has yet been located in the bounded corpus. That absence supports neither worldwide priority nor substantial conceptual novelty. The possible contribution should be described narrowly as the application to the exact Morpurgo maximum comparison, a completely specified smooth finite witness, and independently checkable quantitative separation.

Falsifiable distinction: a prior source that states the exact normalized maximum violation, or one that already combines an admissible compact conformal cylinder with a strict round maximum comparison, would supersede the possible exact-target assembly contribution. A source merely proving unbounded normalized first eigenvalues or fixed-index convergence does not state it, although its construction remains materially sufficient once the standard additional steps above are supplied.
