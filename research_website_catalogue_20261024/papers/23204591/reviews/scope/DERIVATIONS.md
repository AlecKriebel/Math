# Final derivations and input audit

CORRECTION CONTROLLING THE IMMUTABLE TEXT BELOW: Demeter2006v1 printed page2 Remark1.3 states1/p+1/q<3/2, not2/3. Hence L3,L3 is included in that opposite-power convergence result. A personally viewed fresh raster confirms this. The paragraph in the copied immutable reconstruction below remains historical and is superseded here; no other mathematical step changes. See RECONCILIATION.md and OWN_FAILURE_HISTORY.json.

The following is an exact copy of the independently sealed primary-proof reconstruction, made before native code, native results or historical audit opinions. Its scientific comparison typo is retained visibly, not retroactively corrected in the original sealed artifact.

# Independent primary-proof reconstruction before native code or archived opinions

All nine actual pinned annular source sections,2667 lines in total, their main file, manuscript README and complete bibliography have now been personally read. The actual37-page PDF's first five pages were read directly, including its precise Theorems1.1 and1.2; I do not claim all37 PDF pages were viewed or text-read. All15 native checksum bindings match freshly acquired actual bodies. This reconstruction follows the immutable INITIAL and separate actual own proof/control results, and precedes native scientific code/results and archived scientific audit opinions. Current peer/root findings and peer control outputs remain unread.

## The imported interface actually states what the target requires

The actual October5 paper defines the same kernel1/t and the shifts F(x+t,y)G(x,y+t). Its Theorem1.1 covers complex L3 inputs, output L^(3/2), every finite real r>2, all positive rational endpoints, arbitrarily many increments inside a scale interval, and a pointwise supremum inside the output norm. Its finite-truncation lemma constructs one common full-measure set by the countable annuli1/m<|t|<m, proves absolute integrability there, and obtains endpoint continuity. Thus this is neither an old maximal theorem nor a fixed-partition norm estimate. No change of normalization, exponent, partition class or scalar/complex category is needed to apply it to the target's fixed-width proof.

The target's local implication was proved before this foreign exposure in PREEXPOSURE_PROOF.md. That result alone was explicitly conditional. The present independent work examines the actual new analytic proof needed to assess the original full claim; it does not replace that claim by the conditional implication.

## Matrix mechanism: supports, phase and dimension

For Phi(P)=tr(P^(3/2)), the positive square-root derivative solves AX+XA=K with A=sqrt(P). On a fixed support the Hessian is

    b_P(K)=(3/2)sum_ij |K_ij|²/(sqrt(p_i)+sqrt(p_j)).

The proof differentiates tr(P sqrt(P)) and obtains the factor3/2 correctly. Zero eigenspaces are handled by supported directions; formulas are not applied to a direction meeting an unregularized zero eigenspace. The order comparison P<=aQ gives b_P(K)>=a^(-1/2)b_Q(K): regularize both Grams by etaI, use square-root order and inverse order on Hilbert–Schmidt space, then take eta down to zero on the respective supports. The direction supported on P is also supported on Q because ker(Q) is contained in ker(P).

For an inserted Gram, the singular-value coefficient rho_i²rho_j²/(rho_i+rho_j) is bounded by(rho_i³+rho_j³)/4. Both row and column squared sums of the compressed insertion are bounded by its operator norm squared. This proves the stated3/4 insertion constant without a dimension factor.

For probability averages, A=int sqrt(T_omega) satisfies A²<=int T_omega by vector Cauchy–Schwarz, and hence A<=sqrt(int T_omega). The variational formula for an inverse positive quadratic form then gives joint convexity of b_T(K). The proof uses a fixed common support but no common lower eigenvalue. This is the hypothesis later supplied by invertible positive row rescaling; it would be an error to infer it from bounded norms alone.

For the cyclic trace, the block Hermitian matrix M collects the three edges and their adjoints. Its vertex terms A_v=MP_vM satisfy A_v<=M², and the inserted K_v are supported. Comparing costs and using the quadratic triangle inequality gives E>=Q/2, where

    Q=sum_ij q_i²q_j² |D_ij|²/(q_i+q_j),  q_i=|m_i|.

Ordering q_i nonincreasingly gives Q>=A/2+E', with A=sum q_i³|D_ii|² and E'=sum_{i<j}q_i q_j²|D_ij|². The expansion of tr((DM)³) splits by whether its smallest index appears once, twice or three times. These contributions are bounded respectively by3D_*E',3D_*sqrt(AE'),D_*A. Therefore |tr((DM)³)|<=5D_*Q. The combinatorial grouping includes the case of equal other indices and retains signs of m_i.

The block trace is6Re(tau), not6|tau| automatically. The proof changes one edge by a unit complex phase. Its two incident row stars change by right unitary multipliers, so their energies and inserted costs are unchanged even though the auxiliary Q can change. Reapplying Q<=2E to the changed block matrix recovers6|tau| and gives the constant5/3. Splitting complex diagonal insertions into real and imaginary parts yields the eight Hermitian terms with each individual cost occurring four times. No unjustified real-only reduction or dimension-dependent Fourier decomposition is used.

## Heat mechanism and its genuinely integrated identities

The finite grid uses w_v(i)=h g_(sigma_v)(u_i-p_v) and W_v(i,j)=A_v(i,j)sqrt(w_v(i)w_(v+1)(j)). A row star has fixed kernel when its row density changes and fixed range when its column densities change. A full-rank factorization of the fixed unweighted star proves joint smoothness of the nonzero spectrum, so rank-deficient Grams do not justify differentiating a nonexistent inverse on the whole space.

The chain rule gives2d_s e_v=sum alpha_i d_(p_i)²e_v-alpha_v V_v-sum_(w!=v)alpha_wY_(v,w). On the center plane sum p_i=d, integrating a pure derivative in any center gives d_d²J_v. Reparametrizing between two free-coordinate charts gives the same integrated mixed derivative int Z_v. There is no claimed pointwise equality of the pure and mixed derivatives.

The comparison between neighboring columns and one row is Y_(w+1,w)+Y_(w-1,w)<=sqrt(2)V_w. It follows from T_w<=2diag(A*A,B*B), discarding nonnegative off-block entries in the Hessian metric, and then comparing each single-edge Gram with its neighbor's larger row Gram. Supports are checked at both comparisons. The unfavorable mixed terms cost half the sum of the two Y terms. For rates a permutation of(1,11/10,11/10), the resulting row coefficients are -1+(3/5)sqrt(2) and -11/10+(1/2)sqrt(2), both strictly negative. This leaves genuine integrated dissipation.

The mesh mass bound sum_i h g_sigma(u_i-p)<=1+2h/sqrt(2pi sigma) is uniform when sigma>=h². Weighted Hölder bounds each cubic Hilbert–Schmidt edge norm by M times its weighted cubed-entry sum; the product of the two Gaussian masses contributes M, not M², after its square root. Integrating over the two incident centers gives h²sum|A|³. Each edge belongs to two stars. Thus initial integrated energies have a dimension-free L3 bound. The finite-mesh restriction is enforced before taking the Riemann limit at fixed positive endpoints.

For unequal rates, the summed three-star energy need not decrease. The proof does not assert that it does. It instead deletes one incident edge and uses the exact single-edge dissipation, whose plane integral is independent of d. This separate mechanism is essential at high frequency.

## Smooth switching and the frequency mechanism

Disjoint annuli make the mask of the dual edge bounded by1 and give total entrywise jump size at most2n times the original entry. The rank-change derivative controls each energy jump by products containing two norms of the changing edge. The Gaussian expectation of those row/column terms is bounded by one-dimensional maximal operators with a switch-independent majorant. After summing jumps, normalizing the three input norms to n^(-1/2),1,1 makes n(n^(-3/2)+2n^(-1)) bounded. Rescaling gives the required square-root loss. Replacing this by a linear count of complete energy resets would be weaker and insufficient.

The smooth identity has k_s=(t/sqrt(s))g_s and k_1*k_1*k_1=-g_3'''. Its integrated kernel is[P(|t|/epsilon)-P(|t|/R)]/t, where P(v)=2int_0^v(-g_3''')(u)du and c0=2g_3''(0) is nonzero. The error is exactly E_epsilon-E_R with the stated signs. This identity holds for either sign of t; endpoint values have no effect on the integrals.

For a frequency block D, narrowing one row to b'=theta*s, theta=1/(16D²), is not paid for by the comparable-rate three-star bound. The exact modulated Gaussian convolution uses omega'=a*omega/(a-b') and prefactor exp(omega²*a*b'/(2(a-b'))). Because omega²*b' is bounded uniformly on the slab, the prefactor is bounded. Differentiating the narrower Gaussian gives the negative refined score. Its coefficient has magnitude at most C(q)sqrt(theta*s). Common row supports permit the joint-convexity step and give cost <=C(q)theta*s times the averaged refined row cost.

The center shift has probability density g_((1-theta)s). Differentiating that density adds1-theta to the plane diffusion coefficient2+theta, producing exactly3 in the averaged heat identity. The resulting row-cost inequality has column terms with coefficient1/2. Those are paid by single-edge dissipation; unchanged edges telescope over the whole interval, while the switched edge is paid slab by slab. Frequency cubic costs sum because |mu|³<=C1|mu|² and sum_k int|mu|²d(xi)/D is bounded at every output pair.

The mixed boundary term is controlled using the actual covariance matrix

    s[[2theta,-theta],[-theta,3]],

whose determinant is theta(6-theta)s² and which is at most4s*diag(theta,1). These two facts bound the bivariate Gaussian by a product of widened one-dimensional densities with an absolute prefactor. The two line-maximal operators then give a majorant independent of scale, frequency and theta. The output index map(i,j)->(i_v,-i_v-i_w) is a lattice bijection. Consequently mixed boundary jumps sum against coefficient squares, not a separate supremum over frequency at each scale. This is precisely the stronger joint coefficient hypothesis the proof states.

Finally the integrated cost includes theta, so the small variance causes no D-dependent constant. Each logarithmic slab has length log(3/2), and after multiplying the inserted windows back into the weighted trace their convolution is independent of the auxiliary slab variable. Riemann sums are taken only after a fixed finite block and finite scale set have been chosen; the mesh can then meet the D-dependent lower-variance constraint. No uniform assertion on a fixed coarse mesh at arbitrarily large D is used.

## Hard endpoints, moments and the pointwise supremum

The rough-family argument assumes three vanishing moments. Its triple primitive U has Gaussian tails on both sides precisely because those three moments vanish. Dividing U by a sufficiently wide fixed Gaussian gives f with bounded first three derivatives; the third derivative is BV with total variation O(m). Fourier bounds follow both from the fourth derivative measure and from a translation difference of f'''. The latter yields the square integral over a frequency block, not merely a frequency supremum.

The cutoff P_*=(2+n)^8 makes the L5 error from each active group at most C/n under m<=A sqrt(n), so at most An active groups have a bounded total maximal-envelope error. The modes of f give the differentiated modulated Gaussian windows exactly: convolution of three equal modulations preserves that modulation while the variances add. With mu=D*(D³ fhat)/sqrt(n), the bounds m<=A sqrt(n) and sum m<=An provide respectively the uniform coefficient bound and the joint square-integral bound. Only O(log(2+n)) blocks remain.

Odd kernels may have a nonzero first moment. The proof explicitly subtracts u*phi with int z phi=1 and handles the remainder through Psi=phi-(1/2)Dil_2 phi. Its first moment vanishes and the identity

    Dil_(2^k)phi=sum_(j<J)2^(-j)Dil_(2^(k+j))Psi
                      +2^(-J)Dil_(2^(k+J))phi

has a summable outer coefficient. The last term costs at most C2^(-J)n and tends to zero for each fixed n. Oddness alone is not confused with all three moment conditions.

Within one half-open dyadic endpoint bin, annuli whose two endpoints lie in the bin contribute paired differences; their total normalized lengths are at most1. At most one interval enters through each boundary, leaving at most two unpaired endpoint terms. For paired hard pieces, at most one disjoint radius interval contains any fixed |z|; for the smooth pieces the alpha derivative is integrated over a total length at most1. This yields size and classical derivative bounds independent of the number of jumps, with jumps still explicitly counted. Large-count groups are few; small-count groups meet the rough-family hypothesis. Complex endpoint coefficients and shared endpoints do not alter those bounds away from the endpoint null sets.

The completion then removes step-menu restrictions before taking any infinite supremum. Finite measurable choice sets are approximated on a compact support by rectangular step sets. A finite menu's endpoints remain bounded away from zero, so the approximating forms converge. Four complex phases recover at least half the modulus of each selected increment. Positive L3 dual tests bound every finite maximum in L^(3/2); monotone exhaustion gives the full count. General L3 inputs follow first for each fixed finite menu using the finite-annulus norm bound, then by a second exhaustion. There is no unproved measurable selector for an infinite menu.

For a partition's decreasing increments d_l, d_(2^j)<=S_(2^j)/2^j. Grouping ranks yields V_r<=sum_j2^(j/r-j)S_(2^j). The count bound produces sum_j(1+j)2^(j(1/r-1/2)), convergent exactly in the stated r>2 range. Thus the imported proof genuinely retains output-dependent partitions and all positive scales.

## Actual comparisons and categorical limits

The actual Demeter2006v1 Theorem1.2 is an almost-everywhere Hilbert-series result for opposite powers of one transformation and bounded inputs. Its Remark1.3 states a strict exponent condition1/p+1/q<2/3; it is not a cited proof of the present equality p=q=3 case. The target only attributes the single-transformation result's configuration, not that endpoint range.

The actual Becker–Durcik2603.20173v1 Corollary1.4 concerns double recurrence averages under T^i,T^-i. At output exponent p>=1 its displayed condition gives r>2, including the L3,L3 to L^(3/2) comparison. Its discussion around(1.8) explicitly distinguishes general commuting transformations. This is a comparison of averages and configurations, not an application of that corollary to the present Hilbert sums.

The actual Demeter–Thiele0803.1268v1 Section6 and footnote36 already describe continuous-to-lattice transfer with cell-constant functions and transfer along two-dimensional orbit arrays. The actual DKST1603.00631v3 Section5 integrates positive-area phases and proves a finite-window transfer. Their principal estimate is norm variation at L4,L4 to L2 for a fixed endpoint list, not the present pointwise all-partition inequality. I read these author preprint editions, not every page of their journal typography or their entire foundational proofs.

All five original published Calderon pages349–353 were personally read from the explicit public full-text PNG assets in the official PMC article. The publisher DOI returned403HTML; the advertised PMC PDF route returned a browser proof-of-work HTML page, whose scripts/cookies were not executed. The five page images are a distinct openly supplied representation, not a downloaded PDF or bypass. The original Theorem1 and its finite-window proof provide the classical linear semilocal transference context; they are not a direct theorem about this bilinear variation operator. The target proves its own finite-window argument.

The actual pinned lean/docs/082.md, registration metadata, solution Main.lean, coordinate interface and comparator challenge statement were read statically. The registered MainEstimate controls a maximal norm over hard annular endpoints; it has no r-variation family. The challenge file's placeholder is a comparator problem stub, not a claimed compiled solution. No Lean build or axiom audit was performed. The documentation title does not broaden the actual registered proposition, and no absence claim about every other possible library file follows from this focused inspection. The target explicitly declines a formalization claim for the new variation theorem.

## Current conclusion before native scientific support exposure

The original local implication and the actual required new primary proof have been independently reconstructed, with their materially different mechanisms and failure alternatives recorded. I have not found a substantial unresolved mathematical defect in these checked arguments. This is a provisional scientific assessment at the ordinary extensive AI-review level, not formal verification or peer corroboration. Static native code/support consistency and final input/closure reconciliation remain. No archived audit conclusion or current peer/root finding is being used. No repair, narrowed replacement, worldwide absence or earliest-priority claim is supplied. A follow-up question remains null because no precise substantial publishable question has been established by this review.

## Post-freeze consistency and limits

All native scientific support bodies were subsequently read as supplied historical material; their agreement is not independent corroboration. The deposited finite checker and cached output do not validate the analytic theorem; no native scientific execution occurred here. The actual registered Lean maximal interface is a bounded positive observation, not an absence proof about all files or a formalization of variation. Full native source custody and pure final closure are orthogonal to scientific proof.
