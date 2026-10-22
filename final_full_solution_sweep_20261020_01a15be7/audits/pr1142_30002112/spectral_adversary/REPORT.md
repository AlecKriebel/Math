# Independent spectral, counting, asymptotic and target-scope audit

Problem 30002112 / OWR-12005-004 / PR 1142.

**Verdict: the spectral and asymptotic implication is valid for every fixed integer m>=2, conditional on the exact geometric input below. No off-by-one, multiplicity, zero-mode, exponent or source-scope defect was found.** This report independently reconstructs that implication. It does not independently certify the geometric existence theorems or historical priority; those are separate review families.

The reviewed head is `c29139d2c2a98f1a0284d0dc794c88f51c680a0c`, against base `f6caddda8f8be2cdb3e91494325d8f7f365bc3fc`. The actual head PROOF.md has SHA-256 `c4608dbf5f9e39b398f7db20100273fdab085598382293f8224488585015f658` (10,412 bytes). I read the proof and scope documents before any old AUDIT conclusion; no old AUDIT was used. All work is contained in this family folder. No external person was contacted, and no provider, Git, index, ref, PR or GWS write was performed.

## 1. Exact hypothesis being tested

Fix m>=2. Assume that for each integer q>=1 there is a smooth compact connected embedded hypersurface H_q inside B(0,1/2) in R^(m+1), such that:

1. Its induced intrinsic m-area is exactly q.
2. Its first positive intrinsic Laplace-Beltrami eigenvalue is strictly larger than T_q=q(q+m-1).
3. It bounds a smooth cavity U_q whose closure lies inside B(0,1/2), and Omega_q=B(0,1) minus the closure of U_q is a connected smooth domain with boundary S^m disjoint union H_q.

Put rho_m=|S^m|, omega_{m+1}=|B(0,1)|, S_q=|boundary Omega_q|=q+rho_m, V_q=|Omega_q|, and v_m=omega_{m+1}(1-2^(-(m+1))). Assume the direct geometric consequences v_m<=V_q<=omega_{m+1}. These are the complete geometric inputs used below. No metric uniformity as q varies is assumed.

The success criterion is the limit

R_q = lambda_{k_q}(boundary Omega_q) S_q^(2/m) /
      (I(Omega_q)^(1+2/m)+k_q^(2/m)) -> infinity,

with all zero modes and multiplicities included and indices starting at 1. Proving only a limit on one fixed domain would not suffice.

## 2. Primary target and indexing, checked afresh

I retrieved the actual [OWR 33/2012 report](https://ems.press/content/serial-article-files/46403), read Colbois's whole talk on printed pp.2034-2036, and visually checked those pages. Theorem 3 on p.2035 applies to bounded Euclidean domains with smooth boundary. The question on p.2036 asks whether the product of the isoperimetric factor and index factor can be replaced by their weighted sum, with dimension-only constants. The talk adds no connected-boundary restriction.

I also retrieved [Colbois-El Soufi-Girouard, arXiv:1007.0826v2](https://arxiv.org/pdf/1007.0826) and read/visually checked pp.1, 2 and 14. Its introduction takes boundary dimension at least 2 and numbers eigenvalues from lambda_1=0; Theorem 1.1 is the cited multiplicative bound for smooth bounded domains. Example 3.1 explicitly treats a boundary with two components and counts two zero modes. That example has a different ambient geometry and is not itself the present Euclidean counterexample. The source convention therefore supports using a disconnected boundary here.

Fresh PDF hashes, retrieval times and candidate pins are in INPUT_PINS.json. Third-party PDF, extracted text and page images remain under private/sources. Source acquisition used public primary documents only. This bounded scope check is not a historical novelty search or a claim that no other paper contains the same argument.

## 3. Direct sum and exact sphere spectrum

For compact smooth components M and H, L^2(M disjoint union H) is the orthogonal direct sum L^2(M) plus L^2(H), and the Dirichlet form is the sum of component Dirichlet forms. The associated nonnegative self-adjoint Laplace-Beltrami operator is consequently Delta_M direct sum Delta_H. Extending a component eigenbasis by zero on the other component gives a complete union eigenbasis. Hence the spectrum, including multiplicities and zeros, is the multiset union of component spectra. This is the standard compact-manifold spectral theorem and quadratic-form construction, not a new analytic existence claim.

On a connected compact manifold the kernel consists of constants: zero energy forces the weak gradient to vanish and thus the function to be constant. Thus our boundary has precisely two zero modes. Connectedness of Omega itself does not reduce that multiplicity. The normal orientation of the cavity does not change the intrinsic metric or intrinsic Laplacian.

For the unit S^m, homogeneous harmonic polynomials of degree ell restrict to eigenfunctions with eigenvalue ell(ell+m-1). This follows from the polar-coordinate identity for the Euclidean Laplacian applied to r^ell Y(theta). The harmonic decomposition P_ell=H_ell direct sum |x|^2 P_(ell-2) yields

d_(m,ell)=binom(ell+m,m)-binom(ell+m-2,m).

Here P_ell denotes homogeneous polynomials of degree ell in m+1 variables; its dimension is the number of nonnegative exponent tuples summing to ell, namely binom(ell+m,m). Negative-degree polynomial spaces are zero. The restrictions give the complete spherical spectrum, for example by harmonic decomposition and density of polynomial restrictions. These are standard spherical-harmonic facts, explicitly derived here to identify the counting convention; they are not an original spectral formula.

For m>=2 and ell>=0 this convention handles ell=0 and ell=1 without ambiguity: the subtractive term is zero, d_(m,0)=1 and d_(m,1)=m+1. Also ell(ell+m-1) is strictly increasing for ell>=0. Therefore the sphere has exactly

N_q = sum_(ell=0)^(q-1) d_(m,ell)
    = binom(q+m-1,m)+binom(q+m-2,m)

eigenvalues strictly less than T_q. The identity follows by telescoping the shifted polynomial-dimension sum, leaving the last two terms. It applies also to q=1, where N_1=1.

The inner component contributes exactly one eigenvalue strictly less than T_q, its zero. The number of eigenvalues below T_q on the union is consequently N_q+1. The first eigenvalue equal to T_q is at

k_q=N_q+2.

The complete block equal to T_q occupies indices N_q+2 through N_q+1+d_(m,q), inclusive. This establishes lambda_(k_q)=T_q and identifies the first index, rather than merely an index somewhere in a repeated block.

Boundary checks: for q=1, the union begins with 0,0,m and k_1=3; for q=2, N_2=m+2 and k_2=m+4. In dimension m=2, d_(2,ell)=2ell+1, N_q=q^2 and k_q=q^2+2. Omitting the second zero shifts the first rank incorrectly downward by one. A merely equal inner gap would preserve the first rank but add an extra T_q multiplicity; a gap below T_q can invalidate the displayed eigenvalue at k_q. The candidate's strict gap is sufficient.

## 4. Area, isoperimetric exponent and scale

Write p=1+2/m and a=(m+2)/(m+1). Direct substitution gives the exact identity

I(Omega_q)^p = (S_q/V_q^(m/(m+1)))^p = S_q^p V_q^(-a),

because [m/(m+1)](1+2/m)=(m+2)/(m+1). The lower volume bound thus implies I^p<=v_m^(-a) S_q^p. No volume limit is needed.

Under an ambient dilation by t>0, induced lengths scale by t, eigenvalues by t^(-2), boundary area by t^m, and domain volume by t^(m+1). Hence both lambda_k |boundary Omega|^(2/m) and I are invariant. The requested estimate and the counterexample quotient are dimensionless. This check also confirms that no boundary-area/volume power was interchanged.

## 5. Exact contradiction and growth rates

For q>=m, binomial products give

k_q <= 2(q+m)^m+2 <= 2^(m+2) q^m.

For the second inequality, q+m<=2q, so the first summand is at most 2^(m+1)q^m; the remaining 2 is no larger than the unused same-size allowance. Therefore

k_q^(2/m) <= C_m q^2,   C_m=2^(2+4/m)<=16.

Using T_q>=q^2 and the exact area S_q=q+rho_m yields

1/R_q
 = (I^p+k_q^(2/m))/(T_q S_q^(2/m))
 <= v_m^(-a) S_q/T_q + C_m q^2/(T_q S_q^(2/m))
 <= v_m^(-a)(q+rho_m)/q^2 + C_m/(q+rho_m)^(2/m) -> 0.

Every quantity in the quotient is positive, so R_q tends to positive infinity. This proof uses exact component spectra and elementary bounds, with no Weyl-law approximation.

For additional diagnosis, polynomial binomial asymptotics give k_q/q^m -> 2/m!, while T_q/q^2 -> 1 and S_q/q -> 1. These involve one explicit integer polynomial for each fixed dimension; they do not concern varying metrics.

* If m>2, then p<2. The bound on V_q makes I^p/q^2 tend to zero, while k_q^(2/m)/q^2 tends to (2/m!)^(2/m). Consequently

  R_q/q^(2/m) -> (m!/2)^(2/m).

* If m=2, both denominator terms have order q^2. Since k_q=q^2+2,

  (R_q/q) [1+V_q^(-4/3)] -> 1.

  In particular R_q=Theta(q), with positive uniform bounds obtained from v_2<=V_q<=omega_3. A single limiting value for R_q/q would require additional information about V_q, and the proof does not assume such information.

For any finite real A,B, set A_+=max(A,0), B_+=max(B,0). Their weighted target sum is no larger than max(A_+,B_+)(I^p+k_q^(2/m)). If this maximum is zero it is already smaller than the positive left side; otherwise R_q exceeding that maximum contradicts the proposed bound. Thus the conclusion excludes all finite signed pairs, as the README and status claim, even though the displayed contradiction in the proof is written for positive constants.

Fixed-domain Weyl asymptotics are unaffected: both domain and k vary with q. The established multiplicative inequality is also unaffected because it retains both large factors. This is an intrinsic boundary Laplace-Beltrami result, not a statement about domain Dirichlet, Neumann or Steklov spectra.

## 6. A root-free rational escape bound

This section gives an explicit checkable large-q bound without approximating pi, gamma functions or fractional powers. It is auxiliary to the analytic proof.

Let n=m+1, b=(2/n)^n(1-2^(-n)), D=max(1,b^(-2)), and r=n*2^n. The unit ball contains the cube [-1/n,1/n]^n and lies in [-1,1]^n. Hence v_m>=b and rho_m<=r. Since 0<a<2, v_m^(-a)<=D. For q>=max(m,r), S_q<=2q and the previous calculation gives

1/R_q <= 2D/q + 16 q^(-2/m).

For any positive integer M, it is enough to require q>=4DM and q^2>=(32M)^m. These conditions make each summand at most 1/(2M), proving R_q>=M. A wholly rational/integer choice is

q=(32M)^m+ceil(4DM)+m+r.

The second condition follows because 32M>=1 and m>=2. Finite checks in our new program verify these sufficient inequalities, including enormous exact q and k values, without evaluating a fractional power. They do not establish the geometric input.

## 7. Dimension one and scope boundary

Dimension m=1 is a positive elementary case with this indexing. A bounded planar smooth domain has compact smooth boundary, a finite disjoint union of one-dimensional closed connected manifolds. Each component is intrinsically a circle with some length L_i>0. Let L=sum_i L_i. Its component eigenvalues are 0 and (2pi j/L_i)^2 for j>=1, with multiplicity two.

At t=(2pi k/L)^2 the number of union eigenvalues at most t is

sum_i [1+2 floor(k L_i/L)].

For every x>=0, 1+2floor(x)>=x: it is clear for 0<=x<1, and for x>=1 use floor(x)>=x-1. The displayed count is therefore at least sum_i kL_i/L=k. Thus

lambda_k(boundary Omega) L^2 <=4pi^2 k^2

for every k>=1, including k inside the zero eigenspace. One may take A_1=0 and B_1=4pi^2, or any positive A_1 if strictly positive constants are demanded. This proof is independent of the cavity mechanism.

CEG explicitly sets dimension at least 2. The candidate accurately restricts its negative result to m>=2, so it does not claim a false m=1 extension. If the OWR question is read as allowing m=1 as well, the complete dimensional statement is positive for m=1 and negative for each m>=2. Nothing here addresses the restricted class with connected boundary. That restriction is absent from the actual original statement and would be a different problem.

## 8. Reproducible finite diagnostics and adversarial controls

I wrote checks/exact_checks.py from scratch; no captured or original candidate code was executed. It uses explicit conditionals and exceptions, with no assert-dependent validation. Three fresh source copies were run under normal Python, -O and -OO. All passed with identical semantic JSON after removing the optimization-mode field. checks/RUN_SEAL.json independently pins the source, commands, UTC starts, exit codes and before/after hashes; final manifest membership is sealed separately.

Per mode the diagnostics cover 45 independently enumerated polynomial-dimension cases, 2,976 telescoping count cases, 2,480 index bound cases, 64 actual finite sorted multiset checks, 75 rational escape certificates, and 3,072 rational circle-union checks. Controls detect omitted cavity zero, a sub-threshold inner gap, ignored sphere multiplicities, and equal-threshold extension of the repeated block. An additional control demonstrates why equality at k+1 alone does not validate the first rank when multiplicity exceeds one.

The first diagnostic attempt contained a reviewer error: it expected an inner gap equal to T to change the first rank. That is false; equality increases multiplicity while preserving the rank. I corrected that control and preserved the failed source/output in checks/runs/initial_control_error_normal and the explanation in checks/INITIAL_DIAGNOSTIC_ERROR.json. It is not a candidate-proof defect. The three final copies use SHA-256 `6f48ddef034a61fadacb85f18efd9b74a3fcb0fcaeb5d160744e55326e98f121`.

These finite checks supplement the proof. They are neither a formal proof certificate nor a numerical construction of any H_q.

## 9. Strongest result, gap and completion

The strongest result verified in this family is: **the exact stated geometric input implies the claimed divergent quotient for every fixed m>=2, with all zero modes/multiplicities and the exact index k_q, and it refutes every finite pair of constants for the literal primary-source domain class.** The original source imposes no connected-boundary requirement. The m=1 boundary case admits an independent universal positive bound.

No spectral/counting/asymptotic gap remains. The geometric existence/smoothing/topology inputs remain a separate-family dependency of this report, and historical priority is outside its assigned scope. This family has not read or imported another family's mathematical conclusion. Standard compact spectral theory and spherical harmonics are credited foundations, not claims of new theorems or formal machine verification. No route was marked blocked, because the spectral implication closes rather than transferring its core difficulty elsewhere.

Completion estimate for this assigned family: **100%**. This percentage is not an estimate for the whole parent research/publication task. No outreach is necessary to reproduce these checks; outside specialist review could still improve scholarly confidence, and only the human may initiate it.
