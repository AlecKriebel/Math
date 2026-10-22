# Independent generation-family audit: PR1330 / 30003185

Date: 2026-10-22 UTC. Head: `cd07418b0517f90e2928918b91c120ec08ff5b0c`.
Family:192-class generation, exact centralizer product, and385-block probability bridge.

## Verdict and boundary

**No fatal gap or counterexample was identified in the generation family at the stated large-dimensional natural-group scope.** The replacement192-class theorem follows from the checked subspace estimates, the inspected Burness non-subspace theorem and corrected Liebeck–Pyber–Shalev count. The perfect central-cover step, exact second-derived centralizer calculation, conditional sampling law and graph escape argument also withstand the checks below.

This is **conditional on the separate marginal-count inputs**: the symplectic construction must give the stated κ/log n probability for each separately selected factor; the orthogonal construction must give its stated counted graph mass and polynomial supply. I checked the exact half-mass spinor refinement and the interfaces it needs, but did not independently audit every polynomial coefficient/mass estimate in the marginal proofs. This report is not an unconditional whole-PR mathematical acceptance or an adoption of another family's conclusions.

No new mathematical repair to the pinned generation text is required by this audit. The supplied LPS correction is already reflected in its actual head blob and is correct. No positive historical originality or full-solution priority certificate follows from this bounded review. Constant-class random generation is credited prior work, and the extra-sample diagonal-escape strategy already appears in the unitary literature. The current argument's rigorous natural-cover treatment and explicit constants may be useful refinements, but firstness has not been established.

This is independent AI argument review with bounded exact finite controls, without human peer review or formal proof certification. Only this new review folder was written. The sealed PR1327 review was left unchanged. No publication, merge, service/row change, comment, Git/index/ref change, commit, push, CASE, outside-person contact, or other-family coordination occurred.

## Binding, original target, and duplicate check

`PINNED_MEMBER_HASHES.json` binds all34 supplied paths to their actual pinned Git blobs and records content SHA-256 hashes. The complete relevant proofs read were CLASS_GENERATION(193 lines), SUBSPACE_LEMMA(129), NON_SUBSPACE_LEMMA(40), EQUAL_NEGATIVE_DIMENSIONS(23), and GENERATION_BRIDGE(200), together with the source correction patch, complete README/dependency map/source register, and the orthogonal trace-form/spectral portions needed for the half-mass refinement. Acceptance documents were not treated as proofs.

The original OWR contribution was freshly recovered; complete printedpp2160–2161 were text-read and p2161 visually inspected. It explicitly sets the modified even-output target as C_G(t)'', uses independent uniform samples in the natural representation, defines the closed strong interval, and asks for separate fixed-eigenspace marginal probabilities. It already cites prior constant-class generation as a component. The singular informal word describing C_G(t)'' does not override its displayed second-derived target; in the current large-dimensional natural groups that target is a direct product. The generation argument does not require projective involutions, similitudes, all dimensions, or a bound on bit/field-operation runtime. [Original primary contribution](https://ems.press/content/serial-article-files/46642)

A fresh read-only GWS CLI GET returned191 rows. Six semantic keyword leads concerned unrelated geometry, deformation, Chow, representation-period or Poisson questions. None matched30003185, PR1330, Bray sampling or this generation target. This is a complete tracker read, not a worldwide or complete owned-deposition inventory. See `GWS_DUPLICATE_CHECK.json`.

##1. Every invariant subspace, with closed endpoints

Let e be the natural factor dimension, x a specified strong natural involution, and V=A perpendicular B its eigenspace decomposition. Write a+b=e, a,b>=e/3. Odd characteristic makes x semisimple, so every invariant subspace W splits as (W cap A) direct sum (W cap B). Its summands are orthogonal. A nondegenerate invariant W has both summands nondegenerate; a totally singular invariant W has both summands totally singular.

For a fixed nondegenerate k-space type, full-isometry orbit–stabilizer gives

    N(e,k,type)=|D(V)|/(|D(W)| |D(W-perp)|).

The explicit order-product correction bounds are valid uniformly q>=3:

    7/8<=psi<=1 for Sp,
    7/6<=eta<=8/3 for positive-dimensional O, with |O(0)|=1.

They give (21/128)q^{k(e-k)}<=N<=2q^{k(e-k)}; at most two orthogonal types occur. Empty component spaces contribute1. These constants are deliberately loose but consistent even at dimension1 or the split plane.

For totally singular k-spaces, building an ordered singular basis and dividing by the number of bases gives

    T(e,k)=product_{j=0}^{k-1} N_{e-2j}/(q^{k-j}-1),

where N_d is the number of nonzero singular vectors in the residual geometry. For Sp it is q^d-1, for odd O it is q^{d-1}-1, and for O^epsilon_{2m} it is (q^{m-1}+epsilon)(q^m-epsilon). The residual even sign is unchanged by removing hyperbolic planes. Factoring leading powers gives

    (1/2)q^{F_sigma(e,k)}<=T(e,k)<=8q^{F_sigma(e,k)},
    F_sigma(e,k)=ke-(3k^2+sigma k)/2,
    sigma=-1 for Sp, +1 for O.

The denominator normalized product is at least1/2 for q>=3. Negative numerator factors have distinct positive exponents; positive factors are bounded by product_{h>=0}(1+q^{-h})<4. In particular the terminal split-plane factor and both families of maximal split singular spaces are retained. An impossible singular dimension has count0 and is never used as a positive denominator.

Put i=dim(W cap A), j=dim(W cap B), k=i+j. The nondegenerate exponent loss is

    Delta_nd=ib+ja-2ij
             >=ek/3-k^2/2>=ek/12 for k<=e/2.

For totally singular W, i<=a/2 and j<=b/2 imply ib+ja>=4ij. Therefore

    Delta_ts=ib+ja-3ij >=(ib+ja)/4>=ek/12.

No strict endpoint inequality is used. The sums over component dimensions and types give the common individual-class bound

    P(x fixes a specified relevant k-space)<=128(k+1)q^{-ek/12}.

For Omega-class sampling this really is the full-O ratio. The centralizer O(A) times O(B) contains reflections of square and nonsquare spinor norm, since the eigenspaces have dimension at least3. Their determinant/spinor images generate O/Omega, so O=Omega C_O(x) and the actual x-classes agree. A uniform Omega-class element is thus uniform on the full-O class. This reasoning does not assume that the subspace orbit itself remains a single Omega-orbit; split maximal-singular orbits cause no omitted factor.

A degenerate nonzero invariant W has a nonzero invariant totally singular radical W cap W-perp. A nondegenerate invariant W of dimension greater than e/2 may be replaced by W-perp. Hence every reducible subgroup fixes some counted nonzero subspace with k<=e/2. There are at most12q^{ek} such spaces for each k.

For e>=384,

    128(k+1)<=256^k<=3^{8k}<=q^{ek/48}.

Thus192 independent samples from any individually prescribed strong classes have reducibility probability bounded by

    12 sum_{k>=1} q^{ek}[q^{-ek/16}]^{192}
      =12 sum_{k>=1}q^{-11ek}
      <13q^{-11e}<(1/2)q^{-e}.

The supporting e>=192 bound uses q^{ek/24} for constant absorption and gives13q^{-7e}; it is also valid, although the integrated theorem only needs the simpler e>=384 route. Independence, not identical classes, is what the product estimate uses.

**Status:** all invariant subspaces are accounted for; no endpoint, split-orbit, parity or zero-component gap identified.

##2. Non-subspace maximals and natural generation

Fresh primary inspection checked Burness Definitions1–2, Theorem1, Table1 and Corollary1, with the formula visually inspected on p3. For the simple quotient S=J/Z(J), J=Sp_e(q) or Omega(V), e>=384, its dimension parameter is the natural e: the small exceptional representation isomorphisms do not occur. A maximal subspace stabilizer in the odd-characteristic groups stabilizes a nonzero proper totally singular or nondegenerate subspace. For a non-subspace maximal M the faithful coset action S/M satisfies

    fpr(x-bar,S/M)<|x-bar^S|^{-1/2+1/e+iota},
    0<=iota<=1/(e-2).

All remaining table corrections are bounded by this iota in the active dimension range. The original theorem covers prime-order elements; the image of a strong natural order-two matrix is a nontrivial involution. These precise hypotheses are present. [Burness primary manuscript](https://seis.bristol.ac.uk/~tb13602/docs/fpr1.pdf)

The natural strong class has size at least(21/128)q^{ab}, with ab>=2e^2/9. Class projection to S has equal fibers of size at most|Z(J)|<=2. Consequently

    |x-bar^S|>=(21/256)q^{2e^2/9}>=q^{e^2/5} for e>=16.

This central-fiber allowance is needed when x and -x project to the same element. Since 1/e+1/(e-2)<=1/6, the single-class membership ratio in M is at most q^{-e^2/15}. For192 independent prescribed classes the probability of lying in that fixed M is at most q^{-192e^2/15}.

Fresh LPS Theorem1.1 inspection, including its definition of max(G), confirms a bound on actual maximal subgroups:

    max(G)<=C r^{-2/3}|G|.

The patch correctly replaces the overly general |S| formulation by |G| and then specializes G=S. Since |S|<q^{e^2} and r>=1, the union over all non-subspace maximals is at most Cq^{-59e^2/5}. The displayed absolute d0>=max(384,sqrt(log_3(2max(1,C)))) makes C<=q^{e^2}/2, so that error is at most(1/2)q^{-e}. No numerical C or d0 is claimed or needed for this asymptotic existence theorem. [LPS primary manuscript](https://www.ma.imperial.ac.uk/~mwl/WALL.PDF)

Together with the subspace estimate this gives probability at least1-q^{-e} for generation of S. To lift it, if KZ(J)=J, then centrality and perfectness give

    J=J'=(KZ(J))'=K'<=K.

Thus K=J, with no additional probability loss. Taylor's actual theorems on Sp perfectness/simple projective quotient and Omega perfectness/simple quotient, plus its determinant/spinor kernel theorem, were checked at the stated large-dimensional hypotheses. Natural Omega has center of size at most2; no assertion about a larger abstract Spin center is being substituted. [Taylor primary corrected text, Theorems8.7–8.8,11.45–11.51](https://www.maths.usyd.edu.au/u/don/papers/gcg.pdf)

**Status:** the192-class theorem is proved relative to the stated established literature; the old inaccessible exact PS2011 scope is not an active dependency. Its source correction is sufficient, not a transfer of the central difficulty to another unsupported generation claim.

##3. Orthogonal half-mass refinement and exact membership

Here the full marginal counting theorem is a conditional input, but its extra factor1/2 is an active generation obligation and was independently checked.

For a squarefree polynomial f=f_star f0 with s distinct irreducible factors, a self-adjoint primary summand is one-dimensional over its finite extension field. Its symmetric trace form is Tr(cuv), and changing the basis changes c by a square. There are two trace-form square classes per factor; each operator centralizer has order2. The norm identity chi_q(Norm c)=chi_extension(c) means each nonsquare change flips the ground-field discriminant. Exactly2^{s-1} configurations realize the fixed total discriminant of A, and their orbit weights are equal, namely |O(A)|/2^s.

The construction has a distinguished factor of degree k divisible by4 and a positive-degree squarefree remainder, hence s>=2. Impose square discriminant on the distinguished primary space. Exactly one of its two trace-form choices passes. Exactly2^{s-2} choices of the remaining factors restore the fixed total discriminant. This retains exactly half of the counted operators for each individual admissible f. It does not assert statistical independence of spinor norm and the original event.

The graph-embedding count depends on the fixed total discriminants and determinant signs of K and I+K, which are determined by f, and not on the individual trace-form choices. This also holds when the graph has codimension0: the required total-discriminant compatibility is retained. Therefore the same half factor applies to the unconditional counted probability mass, not merely to a chart-conditional distribution.

The distinguished primary determinant det(K_star) is square. Hence its negative spaces U_star in A and F(U_star) in B have equal discriminant classes; both are square after the refinement. Each negative dimension is k. The spinor norm of -I on a negative k-space is

    product Q(v_i)=2^{-k}disc(beta_W) modulo squares.

For even k the scalar2^{-k} is square, and determinant(-I_W)=1. Thus each component restriction lies in the actual Omega factor. This yields the refined event

    z in Omega(A) times Omega(B), with z|_U strong,

of probability at least the conditional input's half mass, giving kappa=1/10000000. Every symplectic component already lies in Sp of its nondegenerate eigenspace.

The actual event used for first-success selection is admissibility plus strongness, an invariant union of component classes. It need not be the particular counted graph subset: the latter only supplies the lower bound. Consequently no unproved conjugacy invariance of an auxiliary trace-form chart subset enters the sampling proof.

**Status:** refinement and membership checked, conditional on the separate marginal supply/mass inequalities. No odd-q, codimension0 or trace-form-weight exception identified.

##4. Product classes and the exact centralizer target

For every sample g in the actual ambient G and c in C=C_G(t), right multiplication g -> gc sends z(g)=inv(tt^g) to z(g)^c. Therefore its distribution is constant on C-classes. Every z centralizes t, so C preserves both t-eigenspaces; equal dimensions do not permit their interchange while commuting with t.

For Sp, C is exactly Sp(A) times Sp(B). For O/SO/Omega let D=O(A) times O(B); C is respectively D or the kernel in D of total determinant, or of total determinant and spinor norm. A commuting involution z has four nondegenerate joint eigenspaces for t,z. One has dimension at least n/4>=3. Reflections in that joint eigenspace realize the full determinant/spinor quotient while centralizing z. Hence D=C C_D(z), so the actual C-class of z equals its D-class, a product of component O-classes. Conditional on those two classes, the components are independently uniform.

Admissibility and strongness are class properties, so the same product-class law remains true after conditioning on the selected target event. For a strong Omega component, its full-O class equals its Omega class by the eigenspace-centralizer reflection argument. The class-generation theorem is therefore applied to the actual group and actual uniform class law it requires.

Let L=Sp(A) times Sp(B) or Omega(A) times Omega(B). In all active ambient groups L<=C, L is perfect, and C/L is abelian. Thus

    L=L'<=C'<=L, and C'=C''=C^infinity=L.

This proves the exact target, rather than assuming C'' is one quasisimple factor or confusing SO with Omega. In particular classes lying in Omega cannot generate SO; the pinned replacement makes no such assertion.

##5. Every projected-product graph and central-lift case

Suppose K<=D has projections containing L_A,L_B. Since D_U/L_U is abelian and L_U is perfect,

    K'<=L_A times L_B, with both projections equal L_U.

Passing to S_U=L_U/Z(L_U), Goursat's lemma gives either the full product or a graph of one isomorphism phi:S_A -> S_B. This covers arbitrary graph/field/diagonal automorphisms without classifying them. A nonisomorphic pair simply has no graph case; the proof need not assert that isomorphism implies equal dimensions or types.

If the image is full, K'Z=L_A times L_B, so perfectness and centrality imply L=(K'Z)'=K''<=K'. This eliminates hidden proper subgroups surjecting onto the full simple product.

If the image is a graph Delta_phi and H1=<K,z> still fails to contain L, its derived image must be a graph containing Delta_phi, hence that same fixed graph. Since z normalizes H1', its two conjugation automorphisms must satisfy

    a_B(z_B)=phi a_A(z_A) phi^{-1}.

There is no union over possible phi: K already fixes the graph before the extra independent output is drawn. Nor must phi lift to the natural covering groups.

The kernel of D_U -> Aut(S_U) has size at most2. If h acts trivially on S_U, then hxh^{-1}=x f(x), where centrality makes f:L_U -> Z(L_U) a homomorphism. Perfectness makes f trivial, so h centralizes L_U. For Sp, transvection image lines force a linear centralizer to fix every line and be scalar. For Omega, the common fixed space of the Siegel transformations with a given singular u is exactly its line. Fixing all singular lines forces a common scalar on a hyperbolic summand; the two singular vectors e1+w-Q(w)f1 and e1-w-Q(w)f1 force the same scalar on each anisotropic vector w. An isometry scalar is +/-I. Taylor11.24 supplies the actual Omega membership of the used Siegel transformations.

Thus, after fixing z_A and the component classes of the independent extra sample, at most two z_B values satisfy the graph condition. If its B component is strong, its full-isometry class has size at least

    (7/8)q^{2b^2/9} in Sp,
    (21/128)q^{2b^2/9} in O.

The graph failure probability is consequently at most2/class_size<13q^{-2b^2/9}. The two central lifts are included in the numerator. No simultaneous strongness of the A component is needed.

A useful deliberate counterexample to the discarded literal-diagonal shortcut is the subgroup {(x,y): yZ=xZ} in J times J, for perfect J=SL_2(5), |J|=120, |Z|=2. It has order240, projects onto both factors, is proper, and is not a literal graph (which would have order120). Its simple-quotient image is a graph. The current proof correctly handles this phenomenon through K' and the simple quotients. Independently, the finite Sp4(3) guard below shows that two central lifts can lie in the very same strong natural class, so replacing the numerator2 by1 is not generally justified.

**Status:** all projected-product and central-cover cases are covered; no unsupported automorphism-union or lift assumption identified.

##6.385 disjoint blocks and confidence

Put c=192, choose385 disjoint independent blocks of length

    L=ceil(kappa^{-1} log n log(385/eta)).

There are192 A-blocks,192 B-blocks and one B-extra block. In a block select the first admissible output strong on its named factor, if any. The input marginal gives block failure at most exp(-kappa L/log n)<=eta/385. The union bound makes collection failure at most eta; it does not use a simultaneous two-factor marginal.

Condition on every block succeeding. That event is the intersection of events in independent blocks, so the blocks remain independent. Conditional on first success at position j, preceding failures concern independent samples and do not bias the output at j beyond its target event. Averaging over j yields exactly the single-output target-conditioned law. The same remains true after the component classes are specified.

The192 A restrictions therefore satisfy the arbitrary prescribed-class generation theorem, giving conditional failure at most q^{-a}; likewise the192 B restrictions give q^{-b}. The B-extra output is still independent of the group K generated from the other384 selections. The fixed-graph argument adds at most13q^{-2b^2/9}. Hence

    P(failure)<=eta+q^{-a}+q^{-b}+13q^{-2b^2/9}.

At the actual dimension thresholds, a,b greatly exceed12; even the weaker exact bound2/3^{12}+13/3^{32}<1/20 suffices. Setting eta=1/20 gives success greater than0.9. Independent repetition r=ceil(log(1/delta)/log10), retaining every original output, gives failure at most10^{-r}<=delta and sample count O(log n(1+log(1/delta))). The selected outputs are only a proof device. The algorithm need not certify which batch succeeded; containing the selected subgroup suffices.

The result is for all odd q and all existing strong involutions in the named actual groups at a sufficiently large absolute dimension. Parity, determinant and spinor restrictions are not discarded. It is not an all-n positive marginal claim, a fixed-multiplier vanishing-error claim, or a runtime/sampler-construction bound.

##7. Equal negative dimensions and boundary controls

For conjugate t,s in odd characteristic, y=ts satisfies tyt=y^{-1}. Extend scalars and pair the generalized lambda/lambda^{-1} spaces for lambda not +/-1. Both t,s interchange the two members, giving equal signed dimensions as integer multiplicities. On the generalized+1 space, y has odd unipotent order; an odd square root of y conjugates t to s. On the generalized-1 space, y=-u with u of odd unipotent order; the same argument conjugates t to tu=-s, so t-positive equals s-negative there. Global conjugacy of t,s then forces equal positive/negative t-dimensions on that generalized-1 summand. The power |y|/2 kills unipotent parts and selects complete reciprocal pairs, plus possibly the balanced generalized-1 summand. Thus the two t-eigenspaces intersect the negative space of inv(y) in the same dimension, without a semisimplicity assumption on y or a trace argument invalid in small characteristic.

For ambient symplectic eigenspace dimensions2a and4a, simultaneous component strongness would force the common negative dimension to equal4a/3. It is impossible if3 does not divide a. This is compatible with the current bridge because its marginals and blocks are separate. In Sp4, restrictions to a symplectic plane are only+/-I and can never be strong. That low-dimensional counterexample does not contradict the asymptotic theorem.

##8. Independent exact finite guards

`independent_generation_controls.py` is newly authored for this review; no candidate program was supplied or represented as replayed. Its output is in `FINITE_CONTROLS_RESULT.json`.

- Exhaustive RREF subspaces of four-dimensional F3 spaces in symplectic, split orthogonal and nonsplit orthogonal forms verify the invariant nondegenerate/singular decomposition convolutions. Maximal split singular spaces number8 in O4+(3); none are silently dropped. Sp4(3) has90 nondegenerate planes and hence90 strong natural involutions in the specified class.
- Both x and -x occur in that Sp4(3) class, so the projective fiber has two values in one class; the exact2/90=1/45 graph bound is visible in a concrete case. This dimension is only a structural guard, below the large-rank theorem cutoff.
- The complete117-element conjugacy class of rank-one-negative involutions in GL3(3), paired with a fixed t, passes the equal-negative identity. Products have orders1,2,3,4,6, including nonsemisimple cases.
- Exact integer checks cover2,255,648 nondegenerate and1,141,430 singular exponent-loss cases through dimension120, including closed balance endpoints. Exact rational/integer checks also verify the Burness exponent/class-size slack and the stated constant absorption at representative boundary dimensions. The written inequalities prove the general statements; finite dimensions do not do so.
- A weighted finite mixture of product-class supports has the exact first-success conditional law predicted by the proof: length3 success probability7/8 and each target atom probability1/4 after conditioning. The general independence conclusion follows from the written product-measure argument, not from this toy model.

These controls do not simulate or formally verify the large-dimensional theorem, test all marginal polynomial counts, or give a numeric value for the published absolute C.

##9. Generation-specific priority and source limits

The original2016 target already credits Praeger–Seress2011 constant-class generation. That generation input is therefore not itself the original unresolved marginal problem. Its DOI must not be marked as prior full-solution coverage of the2016 question. The replacement192-class theorem is a sufficient independently checked derivation from older Burness/LPS results; it bypasses, rather than authenticates, the former exact Omega source gate.

I inspected the primary GPRD arXiv1812.01362v2 introduction, Theorems1–2 and §11.1. It already treats independent class-random components and an extra output to defeat a diagonal obstruction for GL/GU. Its body contains shortcuts about literal diagonal subgroups of quasisimple products and a two-marginal collection bound. The current bridge explicitly avoids those shortcuts with simple quotients, a kernel allowance of2, and separate disjoint first-success blocks. This shows a need for the current justifications; it is not evidence of priority for those general repairs. [GPRD primary manuscript](https://arxiv.org/pdf/1812.01362v2)

A bounded three-query mechanism search located the original2011 generation article's bibliographic record, the2013 coauthored survey restatement and older strong-preinvolution material. The original2011 DOI endpoint was inaccessible through the web tool; its full theorem/ambient Omega definitions were not recovered. The inspected2013 summary was not promoted to original-article authentication. No dependency DOI was treated as a publication resolving the marginal Sp/O problem. No complete later Sp/O resolution or earlier instance of this exact bridge/192 constant was verified by the bounded search, and no absence or firstness conclusion follows.

Primary bytes and exact access scopes are in `SOURCE_ACCESS.json`. Original contribution, Burness theorem pages, LPS theorem page, relevant Taylor theorems and GPRD§11.1 were freshly inspected. Complete PDFs were retained within the8MiB cap, but complete underlying proofs of Burness's series, the LPS theorem, Taylor's whole book and the GPRD paper were not re-audited. Their established results are legitimate imports, not claims newly proved here. Full marginal mass proofs remain the explicitly separate input boundary.

The closed manifest verifies this folder's exact regular-file member set, hashes, all34 pinned Git inputs, main branch, finite-control reproducibility and the8MiB limit. It establishes evidence identity, not mathematical truth or historical priority. The strongest verified conclusion of this family is the conditional generation-and-product bridge stated above; the remaining whole-solution obligations are the independent marginal/source-scope family and any positive originality gate required for promotion.
