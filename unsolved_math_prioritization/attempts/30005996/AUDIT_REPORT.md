# Independent mathematical audit: problem 30005996

Date: 8 October 2026. Disposition: accept the packet as an unresolved five-route report, not as a solution, disproof, or novelty certificate. No sixth proof-search route was attempted. The supplied authored originals were preserved byte for byte.

## 1. Controlling statement and source scope

The controlling source is Federico Franceschini's contribution, joint with Alessio Figalli, in Oberwolfach Report 37/2024, printed pp. 2141–2144. The setup and the isolated-singularity upper question were checked in the PDF text and the rendered printed pp. 2141 and 2143. Primary source: https://ems.press/content/serial-article-files/50045 ; DOI https://doi.org/10.4171/owr/2024/37 .

The packet correctly restores the whole setup: a smooth bounded domain, a positive increasing convex finite-valued nonlinearity on R, f(0)>0, finite integral of 1/f from 1 to infinity, superlinearity f(t)/t -> infinity, the positive zero-Dirichlet Gelfand branch, and its finite strictly positive extremal parameter. The extremal solution is the increasing limit of the minimal stable branch. Its weak stable formulation includes local H^1 regularity and local integrability of f(u) and f'(u), with the distributional equation and the quadratic-form stability inequality. The source's extremal theorem explicitly identifies the extremal solution with this weak stable class. Thus the local integrability used in the cutoff argument is available.

The packet correctly interprets isolation as an interior singular point with a punctured neighborhood of regular points. This is stronger than saying merely that u is large at one point, and weaker than uniform boundedness on the whole punctured ball. The pointwise expressions are evaluated on the classical representative away from zero.

The initial source setup does not state a separate C^k requirement, although it uses f'. Retaining a differentiable-convex convention is reasonable and is explicitly disclosed. A differentiable convex function on an open interval has a continuous derivative: the derivative is monotone and has the intermediate-value property. This supports the continuity of V away from zero used in Routes 1 and 4. The C^2 hypothesis in the source's later singular-set theorem must not be imported into this question; the packet does not do so. Route 3's C^3 assumption is genuinely additional and is restricted to that calculation.

Writing V=lambda* f'(u*) preserves the target exactly because lambda* is fixed, finite and positive. A fixed-problem finite limsup is the target; a universal dimension-only constant at a fixed common scale is not required. No uniformity in the family of domains or nonlinearities is silently added.

## 2. Route 1: cutoff, liminf, thickness, radial result

Accepted as written.

- The linear radial cutoff has gradient magnitude 1/r on an annulus of volume omega_n(2^n-1)r^n. Its energy is exactly omega_n(2^n-1)r^(n-2). Bounded smooth approximation and local integrability of V justify the nonsmooth cutoff.
- Dividing the ball mass bound by the volume of B_r minus B_(r/2) gives exactly 2^n r^(-2). Selecting a point with no larger value, or using an arbitrarily small error, and using |x|<=r proves the liminf upper statement. It does not prove a limsup or annular-supremum bound.
- A relative superlevel volume lower bound in B_(|x|/4)(x) yields exactly 16(2^n-1)/(c theta). The required doubled ball still avoids zero, and lies in the domain for sufficiently small |x|. The uniformity of c and theta is indispensable.
- In the radial nonincreasing case, convexity makes V radially nonincreasing. Testing with the first Dirichlet eigenfunction on B_r gives r^2 V(r)<=lambda_1(B_1). Approximation in H^1_0 is justified by the form inequality; it extends the weighted quadratic form continuously. Rotational invariance plus minimality gives symmetry for the ball's classical minimal branch, and the limit retains radial monotonicity.
- The first-eigenfunction proof and the upper constant are already in Villegas's Theorem 1.1 and its proof. The packet gives appropriate credit and does not present the radial case as an arbitrary-domain resolution.

Primary comparison: https://arxiv.org/pdf/2005.14334 , Theorem 1.1 on printed p. 2 and upper-bound proof on pp. 6–7. Its nonlinearity is C^1 on [0,infinity); the present source class restricts to that domain and is compatible.

## 3. Route 2: stable-potential concentration

Accepted as an obstruction to the expressly weaker implication only.

For r_k=2^(-k), rho_k=2^(-3k-4), and a_k=2^(-k), rho_k/r_k=2^(-2k-4)<=1/64. The ratio of the sum of adjacent support radii to their center separation is 9*2^(-2k-6)<=9/256<1. The supports therefore are disjoint, remain inside B_1, and have zero as their only accumulation point. The sum is smooth on every compact subset of the punctured ball.

The L^(n/2) norm of each scaled bump is a_k times the bump norm. Minkowski's inequality applies for n>=3, and sum a_k=1. The chosen epsilon makes the spike form bound at most one quarter of the Dirichlet energy. The inverse-square baseline has coefficient H_n/2 and contributes at most one half, by Hardy. The resulting 3/4 form bound has a genuine strict margin.

The Hardy square completion has the correct sign. Removing a small ball and passing to the limit is valid for smooth compactly supported tests when n>=3, with the boundary error of order r^(n-2). The baseline's scaled mass is exactly H_n n omega_n/[2(n-2)]=n(n-2)omega_n/8. The cutoff argument gives the upper mass bound on every 0<r<1/2, with coefficient (3/4)omega_n(2^n-1).

The baseline belongs to L^q exactly when q<n/2; the spikes belong to L^(n/2), hence to every stated lower L^q on this finite-volume domain. Finally r_k^2 V(x_k)=H_n/2+epsilon 2^(3k+8), so the weighted pointwise limsup is infinite. There is no asserted construction of u, f, extremality, or zero boundary data. The stable potential is not a counterexample to the source problem.

## 4. Route 3: differential identities and nonlinearity countertests

Accepted under the stated C^3 condition where it is used.

The chain rule gives -Delta V=F''(u)F(u)-F'''(u)|grad u|^2 for F=lambda* f. Both lambda factors in the first term and the single lambda factor in the second are correct. Under the two explicitly extra inequalities, -Delta V<=A V^2 follows. This alone does not supply the missing critical-scale L-infinity estimate or a usable uniform Harnack constant.

The oscillatory test f(t)=exp(t)[1+(2/5)sin(t)] has the stated derivatives. The lower bounds for f, f', and f'' are strictly positive, whereas f'''(3pi/4)/exp(3pi/4)=1-(4/5)sqrt(2)<0. The exponential comparison establishes both source growth conditions. Thus convexity does not imply the proposed third-derivative sign even inside the smooth admissible source class.

For the second construction, h vanishes on (-infinity,-1], has nonnegative bounded first derivative, and nonnegative second derivative. Although each summand can have a linear tail, the sum is locally finite because t_k-delta_k tends to infinity. It is therefore smooth on R; exp(t) supplies strict positivity and strict first- and second-derivative positivity. The pointwise bounds at t_k give exactly the exponent k^2-2k+2 in the lower bound for f''f/(f')^2. No overlap assumption is needed for those estimates. The ratio is unbounded, and f>=exp(t) establishes the source growth conditions.

The log-gradient bridge has the correct constant: along the segment from x to y in B_(|x|/4)(x), length divided by the minimum radius is at most 1/3. Thus the factor is exp(-K/3), and the thickness bound is 16(2^n-1)exp(K/3). None of these derivative identities or example nonlinearities claims a solution of the extremal problem.

## 5. Route 4: point selection, normalization, entire obstruction

Accepted with the compactness limitation intact.

On the closed ball of radius r_j/2 centered at x_j, d_j sqrt(V) is continuous and vanishes on the boundary. Its maximum is interior and positive for large j. At distance less than d_j(y_j)/2 from the maximizer, the ratio of sqrt(V) is at most 2. This gives V/V(y_j)<=4 on B_(R_j), with R_j>=r_j sqrt(V(x_j))/4 -> infinity. Also |y_j| lies between r_j/2 and 3r_j/2, and d_j(y_j)<=r_j/2, so rho_j/|y_j|->0. These are genuine point-selection consequences.

For a_j=f(s_j)/f'(s_j) and rho_j^2=1/[lambda* f'(s_j)], the rescaled equation has coefficient one; g_j(0)=g'_j(0)=1, and g'_j(v_j)=V/V(y_j). Stability has the same scaling factor. Since the selected potential is positive, division by f'(s_j) is valid. Neither a point normalization nor the derivative bound along v_j's image is an asserted compactness theorem. The packet correctly does not claim locally uniform control of v_j or a convergent family of g_j.

Independent radial differentiation verifies w=-log(1+r^2) and G(t)=2(n-2)exp(t)+4exp(2t). The linearized potential has coefficients 2(n-2) and 8. The exact Hardy-comparison numerator is 2(n-2)+2(n-6)r^2. It is nonnegative for n>=6, and H_n-2(n-2)=(n-2)(n-10)/4, giving stability for every n>=10. No singularity occurs at the origin in this example.

G(0)=2n and G'(0)=2n+4. Hence a=n/(n+2) and rho^2=1/(2n+4) produce precisely the normalized PDE. The profile is nonpositive and g' is increasing, so g'(v)<=g'(0)=1 everywhere. This is a valid obstruction to a blanket Liouville assertion based only on the displayed normalized properties. It need not arise from a blow-up of a fixed positive extremal solution, and it is not a bounded-domain zero-Dirichlet counterexample. The stated extra rigidity/compactness gap is real.

## 6. Route 5: nonlinear compatibility and cylindrical equations

Accepted as a necessary-condition analysis, not as existence or classification.

Differentiation gives grad(-Delta u)=F'(u)grad u=V grad u, and, when F'' exists, grad V=F''(u)grad u. The requirement that -Delta u have the same value on all components of a level set is a genuine global condition. A prescribed stable potential supplies none of these constraints. The radial statement is understood in the source-admissible decreasing radial setting of Route 1; a generic monotone coordinate without that setting does not supply extremality.

For u=-2log r+psi(theta), the Laplacian gives -Delta_S psi+2(n-2)=lambda exp(psi), with r^2V=lambda exp(psi). A smooth profile on the compact sphere is bounded. An unbounded angular profile repeats its failure of local boundedness along a nonzero-radius ray and fails the isolated-singularity hypothesis. Boundary data and extremality remain independent requirements.

For t=-log r and u=2t+w, the correct cylinder equation is -w_tt+(n-2)w_t-Delta_S w+2(n-2)=lambda exp(w). Under phi=r^(-(n-2)/2)zeta, the radial measure becomes dr/r, equivalently dt with the orientation reversed. The radial energy expands into zeta_t^2, H_n zeta^2, and a derivative cross term that integrates to zero for compact support. The angular term has coefficient one. This verifies the stated stability form. For fixed lambda>0, the target is equivalent to a uniform upper bound for w on all sufficiently far cylindrical slabs, including the angular variable. The packet neither constructs nor excludes such a compatible unbounded profile and makes no claim that the exponential subproblem settles every convex nonlinearity.

## 7. Primary-source version and interpretation checks

Figalli–Franceschini's inspected PDF is arXiv:2606.21546v2. The arXiv abstract/version page confirms the revision date of 25 August 2026. The PDF's opening pages and Theorem 1.4 / Remarks 1.3–1.5 were inspected. Theorem 1.4 bounds a limsup of scaled integrals; Remark 1.5 extracts a pointwise lower conclusion. Neither gives the target pointwise upper bound. The packet's distinction is correct. The v2 PDF and the previously retrieved unversioned PDF have the same SHA-256 and byte count. This establishes byte equality only. Primary links: https://arxiv.org/abs/2606.21546 and https://arxiv.org/pdf/2606.21546v2 .

The unsuccessful author-hosted/v1 retrieval attempts are historical retrieval facts. They do not establish theorem wording or byte identity for unavailable files, and this audit does not promote them to inspected sources. No journal-acceptance claim is made.

Villegas's primary preprint was checked for its hypotheses, exact Theorem 1.1 bounds, and eigenfunction proof. The radial credit is accurate. This audit does not inherit the controlling report's apparent bibliographic inconsistency in its Villegas reference; the authored packet uses the verified preprint instead.

Yu–Zhou's arXiv:2609.06673v1 introduction and main theorem concern singular extremal solutions for varying nonlinearities on thin ellipsoids, and comparison with regular Gelfand solutions there. That statement addresses dependence on the nonlinearity and domain. Its abstract/main theorem is not the target pointwise estimate. The construction's full proof and general literature completeness are not certified here. Primary link: https://arxiv.org/pdf/2609.06673 .

## 8. Computational evidence and acceptance boundary

The original checker has 23 exact symbolic/rational checks. The independent checker derives and checks 41 identities, inequalities, scaling factors and sign conditions. Neither is an analytic proof assistant: Hardy, density, local finiteness, source admissibility, and the boundary of each conclusion were reviewed mathematically above.

REPRODUCIBILITY.json records the completed positive, injected-failure, semantic-mutant, and integrity-negative runs in Python normal, -O and -OO modes. All test processes ran with real/effective UID 1000. The copied packet and test inputs were frozen with file mode 0444 and directory mode 0555. Direct attempts to modify an existing file, create a file, and create a directory in the packet were denied in each mode. Original and frozen-input hashes were checked after all runs.

A deliberately altered mathematical sentence, followed by recomputation of its checksum manifest, passes the original integrity verifier. This is an intentional boundary check, not an undetected mathematical acceptance: verify_packet.py explicitly promises integrity and selected claim-label consistency, not proof certification. Mathematical prose must remain tied to this human-reviewed frozen input. Hashes, scripts and metadata cannot replace the present mathematical review.

No mathematical patch is required. The packet is accepted only as a bounded five-route partial report with unresolved full target, no extremal counterexample, no novelty claim, and no numerical evidence. The source-free freeze contains authored material and public verification metadata only. No source PDFs/text, raw datasets, private sources, or private coordination material are included.
