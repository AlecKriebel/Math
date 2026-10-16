# Audit checklist: preferred-cover proof

All claims here refer to CANONICAL_COVER_THEOREM.md in this directory.

| Required issue | Resolution |
|---|---|
| Fixed standard pair, no coordinate substitution | Formulas reconstruct exactly u=κ² and v=κ_s with z=x+iy, w=x−iy |
| Imported coefficients η=i du/v and q=du²/(4uv²) | Derived directly from dlog(dz/dw)=2iκ ds and du=2κv ds |
| Arbitrary genus | Function-field norm, trace, Pic⁰ divisor test, and Riemann–Roch do not assume genus zero |
| Singularities and infinity | Work on smooth projective normalization and use meromorphic identities everywhere |
| Arbitrary covers eliminated | Unique least log exponent n, forced cover a^n=f, and universality into every source field |
| Irreducibility of preferred cover | Norm of a hypothetical smaller-degree root contradicts minimality of n |
| No later cover can repair exactness | Trace primitive divided by extension degree yields a primitive downstairs |
| Residue integrality not confused with global condition | Residue divisor must be torsion and remaining holomorphic differential must vanish |
| Exactness not replaced by residue vanishing | Both complete meromorphic exactness tests remain; base rational ODEs are equivalent |
| Actual plane source, not abstract normalization only | Coordinates z,w give integral affine image; invariants imply C(z,w)=K(a) |
| Nonisotropic source | dz dw=q≠0 |
| Degree greater than one | u nonconstant excludes every line of nonzero metric |
| Exact prescribed signature image closure | u,v recovered intrinsically on plane curve and generate injected K=C(S) |
| Finite algebraic checks instead of unknown source functions | Two rational linear ODEs on K; bounded Riemann–Roch proof in the differential-equations report |
| Minimal cover and signature degree | Field generation proves source field is precisely K(a), hence degree n |
| Computability qualifications | Abstract C theorem distinguished from effective exact coefficient-field model |
| No novelty or full AIM claim | Only frozen complex SE(2,C), fixed rational pair scope asserted |

## Potential wording traps avoided

1. Finite monodromy is not invoked without regular singularities; essential exponentials of exact meromorphic differentials are excluded by the simple-pole test.
2. No proof assumes that every integral-residue differential is logarithmic on a positive-genus curve.
3. The norm is used to detect algebraic exponential existence; the trace is separately used to descend additive primitives.
4. A root choice and constant rescaling do not change exactness and only produce an SE(2,C) rotation of the reconstructed curve.
5. The function-field embedding K⊂C(z,w) is proved from rational differential invariants; it is not assumed from the map used to construct the image.
6. The open-stratum argument never divides by identically zero u or v. Degenerate strata require a separate argument.
