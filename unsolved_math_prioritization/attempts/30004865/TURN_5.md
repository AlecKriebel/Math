# Turn 5: entanglement boundaries versus the fixed-tester regions

**5/5 substantive author turns; final proof-attempt turn.** This completes the comparison between the exact detector regions from turn 4 and actual separability on that same three-qubit family. The central all-tester counterexample remains unchanged. The original source's unrestricted mixed-state classification and output-dimension trade-off are not resolved, so the full source bundle remains a scoped partial result.

## 1. Scope and attribution

Write t=|z| and retain the states

    rho_(p,z)=p(P_000+P_111)/2+(1-p)I_8/8
               +(z/2)|000><111|+(conjugate(z)/2)|111><000|,
    0<=p<=1,  0<=t<=(1+3p)/4.                         (1)

Here P_x=|x><x|. Set a=(1+3p)/8 and b=(1-p)/8. The two distinguished diagonal entries are a; the other six are b. A local diagonal unitary removes the phase of z, preserving separability and both tester values. Thus (1) is locally equivalent to the nonnegative-p part of the familiar GHZ-symmetric family.

The separability boundaries below are established prior results, not new discoveries: Eltschka and Siewert, *Entanglement of three-qubit Greenberger-Horne-Zeilinger-symmetric states*, arXiv:1304.6095v1, equations (11)-(12), recover them under x=t/2 and y=sqrt(3)p/4. Their discussion also credits the known noisy-line thresholds 1/5 and 3/7. The biseparable matrix-element criterion used below is from Gühne and Seevinck, *Separability criteria for genuine multiparticle entanglement*, arXiv:0905.1349v3, Observation 1. We supply direct proofs and finite decompositions to make the comparison self-contained. No novelty claim is made.

For (1), the exact classification is:

    fully separable               iff t <= (1-p)/4;
    biseparable                   iff t <= 3(1-p)/4;
    genuinely tripartite entangled iff t > 3(1-p)/4.    (2)

All inequalities are intersected with the physical region in (1). Biseparable means a convex mixture of states product across possibly different nontrivial bipartitions; it includes fully separable states. In particular, the middle region can be non-fully-separable without being genuinely tripartite entangled.

## 2. Full separability: necessity and an explicit finite decomposition

Partial transposition on the first qubit moves the 000/111 coherence into the block on |100>,|011>, whose eigenvalues are b+t/2 and b-t/2. Full separability implies positive partial transpose, so t<=2b is necessary. The identical condition follows at each other single-qubit cut.

For sufficiency, choose phi with z=t exp(i phi), arbitrary when t=0. Put q(theta)=(|0>+exp(i theta)|1>)/sqrt(2). Average the sixteen product projectors

    q(theta_1) tensor q(theta_2) tensor q(-phi-theta_1-theta_2),
    theta_1,theta_2 in {0,pi/2,pi,3pi/2},

with equal weights, and call the state sigma_phi. Its diagonal is uniformly 1/8 and its only off-diagonal entries are

    (sigma_phi)_(000,111)=exp(i phi)/8,
    (sigma_phi)_(111,000)=exp(-i phi)/8.                (3)

Indeed, for matrix coordinate x,y in {0,1}^3, let delta_j=x_j-y_j. The phase average vanishes unless delta_1-delta_3 and delta_2-delta_3 are both multiples of four. These differences lie between -2 and 2, so both must be zero. The surviving possibilities are x=y or the pair 000,111 in either order. This proves (3) exactly, including complex phases.

Now

    rho_(p,z)=4t sigma_phi
                +(a-t/2)(P_000+P_111)
                +(b-t/2) sum_(x!=000,111) P_x.         (4)

The coefficients in (4) sum to one. If t<=2b, all are nonnegative because a>=b, and every summand is fully separable. This proves the first equivalence in (2), without treating positive partial transpose as sufficient in general. At p=1, only t=0 satisfies the condition and (4) reduces to the expected diagonal mixture.

## 3. Biseparability: necessity and an explicit finite decomposition

Every biseparable three-qubit state omega satisfies

    |omega_(000,111)| <= sqrt(omega_(100,100) omega_(011,011))
                       +sqrt(omega_(010,010) omega_(101,101))
                       +sqrt(omega_(001,001) omega_(110,110)). (5)

For completeness, for a pure state product across A|BC, its coefficients factor as alpha_i beta_jk. Its 000/111 coherence has modulus exactly the square root of the product of its 100 and 011 diagonal entries. The analogous equality holds for a product across the other two cuts and the respective pair. In a convex biseparable decomposition, assign each pure component to one cut for which it is product. The triangle inequality bounds the total coherence by the three sums of component magnitudes. Weighted Cauchy-Schwarz bounds each such sum by the square root of the corresponding partial diagonal totals. Each partial total is bounded by the full diagonal entry, giving (5). This proof allows distinct cuts in different components.

For (1), inequality (5) says t/2<=3b, so t<=6b is necessary.

To prove sufficiency, average the four A|BC product projectors on the normalized vectors

    (|0>+exp(i theta)|1>)/sqrt(2)
       tensor (|00>+exp(-i(phi+theta))|11>)/sqrt(2),
    theta in {0,pi/2,pi,3pi/2},

and call the state tau_A. It has diagonal entries 1/4 on 000,011,100,111 and zero elsewhere, with its only coherence exp(i phi)/4 at 000,111 and the conjugate at 111,000. Phase averaging verifies this directly: the unwanted exponents are plus/minus one or two, never nonzero multiples of four. Define tau_B and tau_C by moving the singled-out qubit, and set tau=(tau_A+tau_B+tau_C)/3. This is biseparable. Its distinguished diagonal entries are 1/4, its other six entries 1/12, and its distinguished coherence exp(i phi)/4. Therefore

    rho_(p,z)=2t tau
                +(a-t/2)(P_000+P_111)
                +(b-t/6) sum_(x!=000,111) P_x.         (6)

The coefficients sum to one. Positivity of (1) gives a-t/2>=0. The condition t<=6b gives b-t/6>=0. Thus (6) is a biseparable decomposition throughout the claimed region, proving the second equivalence in (2). Outside that region (5) is violated, proving genuine tripartite entanglement. There is no inference that negativity across all cuts alone is sufficient for genuine entanglement.

## 4. Exact ordering of four thresholds

Define

    theta_F(p)=(1-p)/4,
    theta_B(p)=3(1-p)/4,
    theta_R(p)=1-(1+p)^(3/2)/(2sqrt(2)),
    theta_S(p)=2sqrt(2)(1-(3+p)^(3/2)/8).              (7)

The last two are the exact realignment and SIC thresholds from turn 4. For every 0<=p<1,

    theta_F(p) < theta_R(p) < theta_B(p) < theta_S(p). (8)

All four vanish at p=1. Here are exact proofs of the three strict comparisons.

For theta_R>theta_F, both sides of the equivalent inequality

    (1+p)^(3/2)/(2sqrt(2)) < (3+p)/4

are positive. After squaring and multiplying by 16, their difference is

    (3+p)^2 - 2(1+p)^3 = (1-p)(2p^2+7p+7)>0.         (9)

For theta_R<theta_B, the corresponding positive-square comparison is

    2(1+p)^3 - (1+3p)^2 = (1-p)^2(2p+1)>0.           (10)

Finally, let h=theta_S-theta_B. Then h(1)=0 and

    h'(p)=3/4-(3sqrt(2)/8)sqrt(3+p)<0                 (11)

on [0,1], because sqrt(2(3+p))>2. Hence h(p)>0 before 1.

These comparisons are across the full stated p interval. The physical upper bound t<=(1+3p)/4 can make some vertical intervals empty; no state outside it is included.

## 5. Interpretation and exact examples

Equations (2), (7), and (8) completely compare the two fixed criteria with these two separability notions on family (1):

- Every genuinely tripartite entangled state in the family is detected as entangled by realignment, since t>theta_B implies t>theta_R. This is a statement about the family, not a completeness theorem for realignment on arbitrary states.
- Realignment detection alone is not an exact certificate of genuine entanglement, even within this family: the region theta_R<t<=theta_B is biseparable.
- SIC detection on this family implies genuine tripartite entanglement, since t>theta_S implies t>theta_B. The converse fails.
- Non-fully-separable states missed by both tests occur exactly for theta_F<t<=theta_R, subject to positivity. Non-detection never establishes separability.
- Realignment-only detection occurs exactly for theta_R<t<=theta_S, subject to positivity; both detect exactly for t>theta_S. There are no SIC-only states in this particular family. Turn 2's globally incomparable multipartite examples are unaffected.

On the noisy line z=p, full separability holds exactly for p<=1/5 and biseparability exactly for p<=3/7. Combining (8) with the unique detector roots from turn 4 yields

    1/5 < alpha_R < 3/7 < 1/2 < alpha_S < 1.          (12)

The last strict comparison around 1/2 is already certified in turn 4. Three controls make the distinctions concrete:

1. At p=z=2/5 the state is non-fully-separable and biseparable. It is missed by both tests. For realignment, its diagonal norm has square 343/1000<(3/5)^2, so r_3<1. Since theta_S>theta_R, SIC misses it as well.
2. At p=z=3/7 the state is on the biseparable boundary and is detected by realignment: the diagonal norm has square 125/343>(4/7)^2=112/343. Thus r_3>1 does not imply genuine entanglement.
3. At p=z=1/2 the state is genuinely tripartite entangled, realignment detects it, and SIC misses it. The exact tester certificates in turn 4 apply unchanged.

At p=1, both detectors exceed one precisely when t>0, matching the Schmidt-correlated case and genuine entanglement in turn 3. The t=0 state is fully separable. At p=0 the physical upper bound equals theta_F=1/4, so the whole allowed slice is fully separable.

## 6. Final budget and source-wide status

This final turn resolves the separability-versus-detection gap identified in turn 4 on the specified family. It is a genuine derivation, using explicit finite decompositions and the exact threshold comparison, not an extra packaging turn. The five author turns are now consumed. No sixth author search is authorized.

Frozen results available for a fresh independent audit are:

1. A complete negative answer to unreshuffled local-tester completeness, via the two-qutrit state (19I-9F)/144 and the general Werner interval.
2. Incomparability of the two fixed criteria for multipartite mixed states, with explicit examples for every number of parties m>=3; those examples need not be genuinely multipartite entangled.
3. Exact full complex projective norms for all multipartite Schmidt-correlated states and even-party noisy GHZ states, with actual-SIC existence qualifications.
4. Exact three-qubit tester norms and detector regions for family (1), now compared with its credited full- and biseparability boundaries.

Still unresolved in this packet are general mixed-state detection classification, broader quantitative comparison beyond the proved families, and the output-dimension versus computational-performance trade-off. No claim of resolving the entire source bundle or certifying historical novelty is made. Publication remains subject to independent review and the parent's gate.

The standard-library controls in verify_turn5.py check the finite decompositions, partial-transpose blocks, physical and boundary cases, polynomial identities, and rational examples. The universal statements follow from the written proofs, not from finite sampling.
