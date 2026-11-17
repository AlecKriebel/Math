# Focused source-only interface reconstruction

This informed audit retains prior row164 scope/source exposure; it is not a new blind family. The current full actual source and eight fresh page images were read before current/old local opinions and foreign proof bodies. The following are actual deductions/checks of the specified interface, not a full-paper scientific disposition. The exact foreign strong-duality and comparison statements remain to be checked after this seal.

1. Set and cone conventions. D={0}∪[1,infinity) is closed. Both C_square and C_triangle are closed, exclude the origin and have Euclidean distance at least1 from it in R^(2n). Removing the origin therefore does not destroy closedness. C_triangle⊂C_square, so imposing square signs is stronger and its feasible functions are also triangle feasible. (u,0),(0,u),(u,u) with|u|≥1 lie in C_triangle and C_square; (u,−u) with|u|≥1 lies in both. No |x+y| condition is present. g real Schwartz with real nonnegative Fourier transform is even; ifg(u)<0, g(u)g(−u)>0 disproves the naive tensor-product feasibility claim.

2. Compact graph hypotheses to authenticate. On Q_r=[0,r]^n, use edges0<|x−y|<1. This edge set is open. Every finite clique has a clique neighbourhood: singletons have a small open ball of diameter<1; for a finite clique, choose sufficiently small balls preserving each strict pairwise distance<1, and each same-ball diameter<1. The disjunctive product graph likewise has the compact metric vertex space and this packing property: any two different nearby product vertices have a differing coordinate of distance<1, and for finitely many clique pairs preserve one witnessing strict coordinate edge. Allowed supports in a factor are distance0 or>=1; in the product each coordinate has that property. The full diagonal is separated from the allowed off-diagonal by a distance gap, making its mass functional continuous on the allowed support, despite not being continuous on arbitrary measures of the whole square.

3. Exact weak duality, independently checked. A feasible finite nonnegative symmetric measure mu pairs nonnegatively with every continuous PSD kernel, has allowed support and diagonal mass1. For dualK withK−1PSD, off-diagonal allowedK≤0 and diagonal≤M,

 mu(total)=<1,mu> <= <K,mu> <= M mu(diagonal)=M.

This establishes weak duality with the stated constant shift and trace normalization. It does not alone establish strong duality. Feasible primal measures exist (one unit diagonal atom). A finite clique-neighbourhood cover and subordinate partition of unityphi_i give a continuous finite-rank dual kernel: ifthere arem functions withsumphi_i=1, K=m sumphi_i(x)phi_i(y) hasK−1PSD and vanishes on nonedges. Thus the dual objective is finite. This does not bypass the need to inspect the cited infinite-dimensional strong-duality theorem.

4. Measure product inequality. Letmu be product-primal feasible. D_i={x_i=y_i}, A=mu(D_1)>=mu(D_1∩D_2)=1. The first pushforward has diagonal massA and total massm=mu(total); dividing byA makes it primal feasible forfactor1, since pullbacksK1⊗1 are continuousPSD. Letnu2 be the second pushforward ofmu restricted toD_1. It is finite/nonnegative/symmetric, supported on factor2 allowed pairs, has diagonal mass1 and total massA. For any continuousPSD K2, exp(−t|x1−y1|²)K2(x2,y2) is continuousPSD by Schur products. It converges pointwise to1_D1 K2, dominated by||K2||infinity against finite|mu|. Hence the restricted pushforward isPSD without treating1_D1 as a continuous test kernel. Thusm/A<=theta1 andA<=theta2 implym<=theta1theta2. No assertion that arbitrary restrictions ofPSD measures arePSD was used.

5. Periodization. For a two-point Schwartz-feasibleg andT=r+1,

 K_T(x,y)=T^n sum_{k inZ^n}g(x−y+Tk).

Its torus Fourier coefficients arehat g(k/T), including coefficienthat g(0)=1. After subtracting the constant1 all coefficients remain nonnegative, soK_T−1PSD. For a cube nonedge thek=0 term has norm>=1. For k≠0, a coordinate of x−y+Tk has absolute value>=T−r=1. Thus every term has the correct nonpositive sign, including equality at the boundary. Its diagonal isT^n(g(0)+sum_{k≠0}g(Tk)). The tail tends0 by an absolutely convergent Schwartz majorant forN>n; dividing by r^n gives limsup theta(Q_r)/r^n<=g(0). Taking infima is legitimate without an attainedg. The factorT^n, coefficient0 and division by r^n were all kept.

6. Averaging a dual product kernel. LetV=Q_r×Q_r⊂R^(2n), W=vol(V)=r^(2n), and letK be continuous dual feasible with diagonal boundM. K=(K−1)+1 isPSD. It has a continuous Hilbert feature mapPhi on compactV. ExtendingPhi by0 gives a strongly measurable bounded compactly supported L² function (its range is separable because the original image is compact). The zero-extended kernel need not be continuous across the cube boundary, but its stationary correlation

 h(z)=integral <Phi(t+z),Phi(t)>dt

is continuous by L² translation continuity, real/even, compactly supported andPSD (Gram of translated feature functions). It is L¹. By Bochner/distributional Fourier positivity its continuous Fourier transform is nonnegative. In fact its Fourier transform is also L¹: integratehat h against increasing Gaussian cutoffs and use Fourier inversion/approximate identities plus monotone convergence to obtain integralhat h=h(0). No smoothness of the zero extension was assumed.

7. Signs and scale. Ifz∈C_square andt,t+z∈V, their two coordinate displacements are each0 or length>=1 and not both0. They are a distinct nonedge of the product, soK(t+z,t)<=0. Integration preserves the sign on all axes and length-one boundaries. Alsoh(0)=integral_VK(t,t)dt<=MW, whereas

 hat h(0)=integral_{V²}K(s,t)dsdt>=W².

The latter follows by integratingK−1PSD against the constant test function, justified by its continuous feature map. Thereforeh/hat h(0) has objective<=M/W. ReplacingW² byW would yield the wrong scale. Producttheta bound divided byW=r^(2n) then compares with(theta(Q_r)/r^n)². No diagonal-attainment theorem is needed; choose a dual objective within arbitraryepsilon of its infimum.

8. Exact regularization obligation. Mere convolution can spoil sign on thin axes: at(0,y), nearby samples have a short nonzero first coordinate and may not lie inC_square. Dilation alone also leaves that coordinate0. Thus 'smooth and dilate' without a sign-repair margin is not a proof. The required statement is approximation of the objective by real Schwartz functions, with Fourier transform everywhere nonnegative, positive integral/normalization and sign at EVERY point of the same C_square, including its axes. This is weaker than existence of an objective-preserving converter or optimizer and must not be confused with either.

9. Own direct check of the needed compact-support regularization statement. Work in d=2n, and suppose h is the actual continuous, compactly supported, real/even, Fourier-positive function above, withB=hat h(0)>0 and h<=0 on a sign setS whose points all have|z|>=1. Choose a nonnegative even C_c^infinity functionpsi of integral1 supported inB(0,1/2). Putrho=psi*psi. Thenrho is nonnegative, even, C_c^infinity, supported inB(0,1), integral1 andhat rho=(hat psi)²>=0. Forrho_epsilon(z)=epsilon^-d rho(z/epsilon), the functionh_epsilon=h*rho_epsilon is C_c^infinity (henceSchwartz), even/real and Fourier-positive. It has integralB and converges uniformly toh. Withsupporth⊂B(0,R) andepsilon<=1, allh_epsilon have support⊂B(0,R+1).

Set c=1/2, alpha=d+1 and

 q(z)=(c−|z|²)exp(−alpha|z|²).

With the exact2pi Fourier convention,

 hat q(xi)=(pi/alpha)^(d/2) exp(−pi²|xi|²/alpha)
             [c−d/(2alpha)+pi²|xi|²/alpha²].

The constant c−d/(2alpha)=1/[2(d+1)] is positive, sohat q>=0 and its integralhat q(0)>0. q is strictly negative at EVERY|z|>=1. On1<=|z|<=R+1, −q>=m=(1/2)exp(−alpha(R+1)²)>0. Giveneta>0, chooseepsilon so||h_epsilon−h||infinity<=eta m. Thenf=h_epsilon+eta q<=0 onS insideB(0,R+1); outside that ballh_epsilon=0 andeta q<0. This includes thin axes, coincident-point diagonals and exact distance-one boundary points because only|z|>=1 was used. Fourier positivity is preserved by the sum. Normalize by integralB+eta hat q(0)>0. Its objective tends h(0)/B aseta→0 andepsilon→0. Thus the actual averaged compacth can be approximated within the very same Schwartz sign program. This checks the exact asserted value-comparison step deductively, not by replacing it with an unsupported equivalent difficulty or changing the manuscript's target. It does not claim that every unspecified continuous class/citation theorem has these hypotheses; the actual primary theorem still needs examination.

For the focused planar case d=4, q=(1/2−|z|²)e^(−5|z|²) andhat q=(pi/5)² e^(−pi²|xi|²/5)(1/10+pi²|xi|²/25). The constants, signs and normalizations are explicit. This is a checkable analytic construction, not a numerical experiment or a source-file repair.

10. Dilation controls to compare with primaries. If a primary uses forbidden-distance thresholda>0, a normalized feasible scalar functiong_a maps to threshold1 by g_1(x)=a^n g_a(ax), sohat g_1(0)=1 and its objective multiplies bya^n. A product function maps byF_1(x,y)=a^(2n)F_a(ax,ay), multiplying the objective bya^(2n). The square comparison respects these factors. Conversely threshold-a objectives are a^-nL_1 and a^-2nP_1. Any primary omission of the isolated0-distance or use of strict rather than closed inequalities must be compared explicitly; it cannot be dismissed by a change of radius.

11. Conditional target status. The source argument from compact strong duality through marginal/product inequality, periodization and correlation has been reconstructed above. Strong duality for the exact positive/nonnegative measure cone and actual packing-graph hypotheses remains a named external obligation until its corrected primary is read. The cited CDLS statements must be matched in their exact versions, not attributed an arbitrary-closed-set theorem merely from a slogan. This audit will give a focused interface disposition only, with no new group proof, planar-certificate validation campaign, full-paper pass, novelty or optimizer claim. No native scientific execution or foreign primary/opinion body has been used in this INITIAL.
