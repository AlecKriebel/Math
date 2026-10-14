# Checkable source-to-claim implications

These are priority-audit derivations, not a replacement manuscript. The frozen submitted theorem statements are the interface. All Robin couplings below are attractive, with outward derivative equal to beta times the trace. The dimension of the boundary is m = n - 1. The source HHRV uses d for this dimension and m for its mass; those two source symbols must not be confused with the present notation.

## D1. Every compact graph in n >= 4: a complete earlier-theorem corollary

The relevant earlier primary theorem is Hoang, Hundertmark, Richter and Vugalter (HHRV), *Quantitative Bounds Versus Existence of Weakly Coupled Bound States for Schrodinger Type Operators*, Ann. Henri Poincare 24 (2023), 783-842, version of record published 10 September 2022, DOI [10.1007/s00023-022-01228-3](https://doi.org/10.1007/s00023-022-01228-3), Theorem A.6, one-based PDF page 35 (printed page 817) in the freshly retrieved publisher PDF. It gives, for boundary dimension m >= 3 and mass beta >= 0,

    T_beta = sqrt(|p|^2 + beta^2) - beta,
    C_m = [m/(m-2)] * omega_m/(2*pi)^m,
    N(T_beta + V) <= theta^2/(1-2*theta)^2
                     * C_m * integral [theta^(-2) V_-]^ (m/2)
                         [theta^(-2) V_- + 2*beta]^ (m/2),
    0 < theta < 1/2.

Here omega_m is the unit-ball volume and N counts strictly negative eigenvalues, including multiplicity. The theorem assumes the form and essential-spectrum hypotheses of its Section 2. No geometric Robin result is attributed to HHRV. The 2017 arXiv v2 Theorem 3.6 has the same majorant but a different factor theta^2/(1-4 theta)^2 and range 0 < theta < 1/4. The current derivation and theta = 1/4 certificate use the journal formula only; the older formula could instead be used with theta = 1/8. The geometry-to-operator bridge follows explicitly.

Let f be a compactly supported W^{1,infinity} function and Omega_f = {y > f(x)}. Put M = ||f||_infinity, G = ||grad f||_infinity, D = sqrt(1+G^2)-1, c = 1/[2(1+G^2)], and K = supp f. Define a bounded H1 isomorphism by

    U(x,t) = exp(beta*f(x)) * u(x,t+f(x)),    t > 0.

This is an H1 isomorphism because flattening is bi-Lipschitz and exp(beta*f) and its inverse are bounded Lipschitz multipliers. It does not use exp(beta*y) as a globally bounded multiplier. Write b = partial_t U + beta U and g = grad f. The chain rule and integration over each vertical fiber give the exact identity

    Q_f[u] = q_f[u] + beta^2 ||u||^2
      = integral_H exp(-2*beta*f) (|grad_x U - g*b|^2 + |b|^2)
        - beta integral exp(-2*beta*f)
                  (sqrt(1+|g|^2)-1) |U(x,0)|^2.

For a compact core this follows by expansion: the vertical identity is
integral |partial_t U|^2 + beta^2 |U|^2
= integral |partial_t U + beta U|^2 + beta |U(x,0)|^2.
Every term in the final identity is continuous on H1, so density extends it to every form function. This is an explicit all-form geometric comparison.

The elementary vector estimate

    |a|^2 + |b|^2 <= 2(1+G^2) (|a-g*b|^2 + |b|^2)

therefore implies

    Q_f[u] >= a_beta [ E_beta[U] - v_beta integral_K |U(x,0)|^2 ],
    a_beta = exp(-2*beta*M) c > 0,
    v_beta = beta D exp(4*beta*M)/c,
    E_beta[U] = integral_H (|grad_x U|^2 + |partial_t U + beta U|^2).

Next fix a tangential momentum p, rho = sqrt(|p|^2+beta^2), and a0(x) = U(x,0). Completion of the vertical square, followed by the unitary tangential Fourier transform, gives

    E_beta[U]
      = integral_p integral_0^infinity |partial_t U_hat + rho U_hat|^2 dt dp
        + integral_p (rho-beta) |a0_hat(p)|^2 dp
      >= <a0, T_beta a0>.

This establishes the exact boundary reduction directly, including the nondecaying attractive baseline. Frank and Laptev, [arXiv:0711.3473](https://arxiv.org/abs/0711.3473), Theorem 3.2 / Lemma 3.4, already document the underlying Robin-to-relativistic duality, but their stated form-compactness hypothesis does not cover the entire constant coefficient beta + v_beta 1_K. We do not apply that theorem outside its hypotheses; the displayed square identity supplies the required extension.

For fixed beta > 0, T_beta + 1 has a form norm equivalent to H^{1/2}(R^m). Multiplication by |V|^{1/2} for V = -v_beta 1_K is compact from that space to L2: enclose K in a ball and use the local compact embedding H^{1/2} -> L2. V is bounded, hence relatively form small, and relatively form compactness preserves the essential spectrum [0,infinity). These facts verify HHRV Section 2, including the stronger quantitative-bound hypotheses for -V_-. Consequently N = 0 implies T_beta - v_beta 1_K >= 0, rather than merely excluding a selected trial function.

Set theta = 1/4 in Theorem A.6. Then

    N(T_beta - v_beta 1_K)
       <= |K| C_m/4 * [16 v_beta (16 v_beta + 2 beta)]^(m/2).

For 0 < beta <= 1 put C_f = D exp(4M)/c, so v_beta <= beta C_f. Thus

    N <= L_f beta^m,
    L_f = |K| C_m/4 * [16 C_f (16 C_f+2)]^(m/2) < infinity.

If D = 0, compact support implies f = 0 and the domain is flat. Otherwise choose beta_0 <= 1 with L_f beta_0^m <= 1/2, for example

    beta_0 = min(1, (1/(2 L_f))^(1/m)).

The integer N is then zero for every beta in (0,beta_0]. The all-form comparisons prove Q_f >= 0. Combining this with the frozen accepted essential-spectrum proof gives exactly the submitted Theorem B.

**No central gap remains in this implication.** The lower-dimensional HHRV bound diverges at p = 0 when m = 1 or 2 because T_beta(p) behaves like |p|^2/(2 beta). Therefore this route does not incorrectly imply absence in n = 2 or 3. The submitted Hardy-trace certificate remains a valid self-contained proof; its broad conclusion is also obtainable from this earlier theorem and elementary geometry. Exact prior publication of this geometric corollary remains UNKNOWN.

## D2. Explicit f = h/100 in R4 at beta = 1 via the same source

Use the frozen accepted bump estimates M < 1/100, G < 1/50, D < 1/5000, and c > 1250/2501. The elementary exponential series gives exp(1/25) < 25/24. Hence

    v_1 < (1/5000) (25/24) (2501/1250) = 2501/6000000.

Put s = 16 v_1. Then s < 2501/375000 < 1/100, and s(s+2) < 201/10000 < 1/40. In boundary dimension three, C_3 = 1/(2*pi^2) and |K| <= 4*pi/3. The source bound becomes

    N(T_1 - v_1 1_K) <= [s(s+2)]^(3/2)/(6*pi) < 1/240 < 1.

The last bound uses s(s+2) < 1 and pi > 1. Thus N = 0 and D1 proves q_f[u] >= -||u||^2 for every u. The accepted essential interval yields spectrum [-1,infinity). This is an additional exact certificate for the specified example, independent of the submitted weighted Hardy-trace constant. For any prescribed beta_* > 0, replacing f by epsilon h makes v_beta_* tend to zero, and the same bound proves absence for epsilon sufficiently small. This is not absence for one fixed nonzero graph at every beta.

## D3. n = 2,3 nongraph binding: what standard criticality does and does not supply

Exner and Minakov, [arXiv:1406.7624v1](https://arxiv.org/abs/1406.7624v1), Section 5, Theorem 5.2 proof on one-based PDF pages 20-21, use the physical-coordinate trial psi_j(x) exp(-beta y), Stokes' formula, and a boundary factor beta (Gamma_1'(s)-1). For their orientation the outward vertical normal is -Gamma_1'(s). This is exactly minus beta (1+nu_y), the submitted defect in ambient dimension two. The mechanism itself is established. Their stated single infinite C4 curve need not be a graph, but it does not include compact extra boundary components or ambient dimension three.

The broader accepted theorem can be expressed through standard mixed-boundary criticality without pretending that flat-domain criticality transfers automatically. On the actual smooth compactly perturbed domain define

    P_0 = -Delta + beta^2,
    B_0 u = partial_nu u + beta nu_y u,
    phi = exp(-beta y).

Then P_0 phi = 0 and B_0 phi = 0. The pair is symmetric and has smooth local coefficients; take the entire boundary as the Robin part and the Dirichlet part empty. Phi and its inverse are locally bounded. Pinchover and Versano, [arXiv:2008.03699v1](https://arxiv.org/abs/2008.03699v1), Assumptions 2.3, Definition 3.15 and equations (3.8)-(3.9), then identify its transformed energy as integral_Omega phi^2 |grad v|^2. Their Theorem 6.4 characterizes criticality by a locally normalized null sequence.

For m = 1 or 2, the accepted linear or logarithmic tangential cutoffs equal to one around the alteration have gradient energy tending to zero. Add vertical cutoffs and choose their heights after each tangential cutoff so the exponential tail error tends to zero; smoothing gives the core required by the criticality theorem. Normalize on a fixed interior ball. This verifies the null sequence on the actual domain, including its topology. Therefore (P_0,B_0) is critical.

The target shifted Robin form differs from this auxiliary form by

    - beta integral_boundary (1+nu_y) |u|^2.

That coefficient is nonnegative and compactly supported. Its phi-weighted total is strictly positive for every nontrivial perturbation, by the normal-rigidity argument in the accepted proof. The same constructed null sequence has a strictly positive limiting trace mass on this compact defect. Subtracting it gives a negative form value and hence binding below the accepted essential threshold.

This is a complete application of a standard ground-state/null-sequence mechanism **after** verifying the geometry, defect positivity, and null sequence. It is not a literal earlier theorem asserting the full nongraph n = 3 result. In particular, PV Remark 5.22 concerns perturbations of the interior potential with fixed boundary operator; it must not be silently relabeled a theorem about arbitrary boundary or domain deformations. Exact earlier priority for the full n = 3 assertion, and for the added-boundary-component planar scope, remains UNKNOWN.

## D4. Why delta-interaction results do not settle a selected Robin side

Suppose a smooth surface separates two domains. The direct sum of attractive Robin forms with strength beta on both sides has the larger domain H1(Omega_+) direct-sum H1(Omega_-). Restrict it to traces that agree across the surface, namely H1(R^n), and its two boundary terms sum to minus 2 beta times the surface trace squared. This restriction is exactly the delta-interaction form of strength alpha = 2 beta. Thus, in the quadratic-form/min-max sense,

    H_Robin,+ direct-sum H_Robin,- <= H_delta,2beta.

Absence of below-threshold delta spectrum cannot imply absence for the smaller direct-sum operator. Delta binding implies binding on at least one Robin side, but does not identify the prescribed side. On a flat plane the reflection-even decomposition gives an exact selected-side relation; reflection across a general graph is not a Euclidean isometry, so that decomposition is unavailable. Extra compact boundary components can introduce still more complementary domains. These explicit domain/order gaps prevent importing the 2017 delta expectations or singular-interaction comparison theorems as the full Robin theorem. D1 uses only a genuinely flat auxiliary boundary operator after a proven geometric comparison.
