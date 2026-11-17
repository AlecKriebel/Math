# INITIAL boundary and adversarial checks

These are manual checks from native definitions, not native-program runs. The external theorem bodies remain unread.

| Boundary | Check and implication |
|---|---|
| n=2 | Tangent determinant is 1-dimensional; endpoint coefficient n+1 is 3. The ODE h''+h=f h^(p-1) gives a direct regularity bootstrap after positive weak existence. |
| n=1 | Excluded by the exact claim. No inference from a 0-dimensional determinant convention is used. |
| Lower-dimensional body | Excluded. V=0 would destroy the probability normalization and the volume-power argument. |
| Origin outside/on boundary | Excluded by full-dimensional origin symmetry. Positive min h is used for logarithms, noninteger powers, Wulff inclusions and nonsingular PDE coefficients. |
| p approaches 0 from above | Jensen remains strict for each p>0 but degenerates at p=0; its strictness cannot establish arbitrary-measure endpoint uniqueness. A different smooth endpoint mechanism is explicitly required. |
| p=0, singular data | Counterexample checked below. Equal cone-volume measures do not determine arbitrary bodies. |
| p=0, smooth strictly positive data | The local path retains positive curvature only near t=0; that is sufficient. Global regularity for q_t on [0,1] is not used. |
| p=1 | Outside the stated theorem. Ordinary surface-area measure is translation invariant; imposed origin symmetry fixes translation. No claim about unrestricted centers is made. |
| p=n | Outside the stated range; scaling exponent n-p vanishes. Dilates have identical L_n measures, so fixed-data uniqueness without normalization fails. |
| f vanishes, is singular, or lacks evenness | Outside H1. Strict positivity supplies lower bounds and positive curvature; evenness supplies the admissible symmetric class. |
| Singular S_K | Jensen equality gives r constant only S_K-almost everywhere. Classical mixed-volume equality, rather than continuity on an unproven full support, is required to recover the whole body. |
| Normalized versus unnormalized data | nu_K loses scale; H2 compares the unnormalized measures S_(K,p). At p=0 total S_(K,0)=nV, whereas the cone-volume total is V and nu total is 1. |
| Translation/homothety | Classical equality allows cK+x. Common center 0 removes x, and fixed data with n-p>0 remove c. Both removals are necessary steps. |
| One-sided t interval | q_t is a smooth explicit path across 0, and its PDE identity holds for t>=0 in a neighborhood. Two derivatives at 0 from that side are valid. |
| Determinant positivity | Positive determinant alone is insufficient for a general symmetric matrix. The proof also uses Q>=0 from convexity, then obtains Q>0. |
| Smooth even testing | Even eta suffice because the Euler-Lagrange residual is itself smooth even; arbitrary non-even variations are not needed. |

## Equal-volume box check

For B(a)=product_i[-a_i,a_i], V=2^n product_i a_i. The facet normal +e_i or -e_i has (n-1)-area product_(j!=i)(2a_j)=V/(2a_i). At either normal h=a_i. Thus each atom of S_(B,0)=h dS_B is V/2, each cone-volume atom is V/(2n), and each probability atom is 1/(2n). There are 2n atoms, giving the correct totals nV, V, and 1.

For a=(1,...,1) and b=(s,s^-1,1,...,1) with s>0 and s!=1, the products and volumes agree. The measures S_(B,0) agree at every atom but the supports differ at e1. This works for every n>=2, including n=2. At p>0 each corresponding atom is V/(2 a_i^p), so the same pair is no longer an equality example unless the side lengths agree. This directly checks the advertised endpoint boundary and the normalization factors.

## Falsification attempts and remaining limits

I checked the two sandwich signs, the t<0 ordering, the factor n in the logarithmic derivative, the scale power n-p, the finite Borel measure identity used for equal-volume comparison, the n+1 endpoint coefficient, the nonsymmetric-matrix trace issue, and the sufficiency of a local path. None of these manual checks discharges the central upstream theorem or the existence/regularity primary hypotheses. Assertions that prior audits passed or a source declaration had a certain scope are exposure, not evidence adopted by this reviewer. The route is conditional rather than blocked: it identifies deep imported inputs instead of claiming to have proved them. If an imported input does not meet its exact interface, the affected conclusion must remain deferred; no extended repair is authorized in this INITIAL phase.
