# Adversarial prior-classification report: PR445 / 30002737

Verdict: **PASS for a qualified attribution to a published prior example and an `already_solved` classification of the literal unrestricted target.** Frank and Manibo's Example 10, with their character diffraction correspondence, supplies an earlier weighted counterexample. Their singular chi_1 and chi_3 sectors also directly yield an injective positive real weighting, whose actual physical hull retains the chi_2 absolutely continuous factor. This is a logical application of their result; neither the particular positive formula nor an answer to van Enter's named conjecture is claimed to be printed in that paper. This report does not certify earliest priority or the novelty of the later unweighted planar construction.

The strongest checked statement is conditional on accepting the published singularity result, including its expressly asserted numerical error bound. This reviewer has reconstructed the structural application and independently replayed the integral diagnostically, but has not produced an interval certificate for that bound. A statement that this particular review independently certified the historical numerical bound would fail this review.

Audit scope: classification mathematics only. No root classification proposal or action helper yet existed at assignment. I did not inspect peer final reports or a final root priority verdict. The initial checkpoint and initial full report were written before root supplied a proposed positive real specialization; I independently checked that subsequently supplied mechanism below. The original frozen research package was read for its target, scope, and prior report; its construction is not refuted by this priority finding. No external communication, Git/PR/status mutation, paper, DOI, or new original proof search was performed. Completion estimate: 100% of the assigned classification audit; the separate independently certified numerical-reproduction task remains open in this review.

## Exact target and source binding

The authoritative target is Conjecture 1 at printed p.2996, PDF p.10, in [Oberwolfach Report 53/2014](https://ems.press/content/serial-article-files/46543), DOI [10.4171/OWR/2014/53](https://doi.org/10.4171/OWR/2014/53). It asks whether absence of an absolutely continuous diffraction component forces the same absence in dynamics. It has no printed dimension, weight positivity, real-weight, or unweighted restriction. The preceding paragraph describes individual configurations as translation bounded measures and the translation representation on the invariant probability space. The contribution's remaining page is references. The precursor [arXiv:1310.0267v2](https://arxiv.org/abs/1310.0267v2), pp.2-3, explicitly permits many-valued finite spin states on Z^d and states the same question. These statements support the ordinary unrestricted measure formulation. Complex scattering weights are not expressly required or forbidden. The recoverable positive specialization below removes the need to choose a complex-physical-weight interpretation.

The prior primary source is N. P. Frank and N. Manibo, [Spectral theory of spin substitutions](https://www.aimsciences.org/article/doi/10.3934/dcds.2022105), DCDS 42(11) (2022), 5399-5435, DOI [10.3934/dcds.2022105](https://doi.org/10.3934/dcds.2022105). The journal page independently confirms the 2022 issue and online publication on 2022-08-08. The versioned [arXiv record](https://arxiv.org/abs/2108.08642v1) records submission on 2021-08-19; this review does not use its uninspected Example 5.4 as a separate proof source. The published PDF's SHA-256 is `7e4a477cbfc7c43e3384a5c082d30617418c9fd9b027921103664bd27b390954`.

I inspected complete relevant printed pages visually, including Example 10 p.5430/PDF32, Proposition 14 pp.5426-5427/PDF28-29, Theorem 4.5 pp.5417-5418/PDF19-20, its unitarity proof pp.5419-5420/PDF21-22, Proposition 2 p.5406/PDF8, the substitution definition and comparison pp.5409-5410/PDF11-12, Proposition 12 pp.5424-5425/PDF26-27, Proposition 10 p.5421/PDF23, and Appendix A pp.5431-5433/PDF33-35. Receipts and own-code input hashes are separate files. Foreign PDFs, extracts, and page renders remain ignored private inputs.

## Noncircular hypothesis checks

Use C4 exponent notation: a letter is (g,d), with g modulo 4 and d in {0,1}. The printed input-digit/output-digit definition applied to

    W = [[1,i],[1,-1]]

gives

    S(g,0) = [(g,0),(g+1,1)],
    S(g,1) = [(g,0),(g+2,1)].

The checker reconstructs the eight-letter incidence matrix exactly. Its fourth power has every entry positive, with minimum 1 and maximum 4. Thus the substitution is primitive. The first letter of S(0,0) is (0,0), providing a prolongable fixed ray; standard compactness of legal centered subwords gives a nonempty bilateral subshift. The digit system (2,{0,1}) is the ordinary unit digit system. Proposition 2 therefore gives minimality and unique ergodicity, without assuming aperiodicity.

Squaring the spin gives the exact four-letter factor on (g mod 2,d). Its matrix is

    chi_2(W) = [[1,-1],[1,1]],

whose Gram matrix is 2I. This is not the source's printed standard Rudin-Shapiro spin matrix [[1,1],[1,-1]]. The initial suggested shortcut identifying them by a simple letter renaming is withdrawn. The actual fixed squared ray q_n satisfies

    q_(2n) = q_n,
    q_(2n+1) = (-1)^(n+1) q_n.

This proves aperiodicity directly. If q has an eventual period 2r, its even-position recurrence gives eventual period r. Repeatedly halving therefore reduces an eventual period to an odd p. Apply the odd-position recurrence at n and n+p sufficiently far along the ray. Eventual periodicity equates q_(n+p) with q_n and q_(2n+2p+1) with q_(2n+1), while the parity factor changes sign. This is impossible because q_n is always +1 or -1. Hence q is not eventually periodic. Its primitive factor subshift is minimal; a periodic point in that subshift would make it a finite periodic orbit and force the fixed ray to be eventually periodic. Thus the squared spin factor, and consequently its parent, are aperiodic. This argument never invokes Theorem 4.5 to verify its own hypotheses. The finite checker verifies the factor intertwining on every letter and the displayed recurrences on a 65,536-site ray; the finite checks supplement this analytic proof.

An orientation ambiguity also needs care. Definition 3.5 treats the first W index as the input digit, but the displayed cocycle uses diag(1,z)W. Direct output-row/input-column Fourier assembly yields diag(1,z)W^T. For this particular W,

    W^T = D W D^(-1),   D = diag(1,i).

D is unitary and commutes with diag(1,z). Thus the two complete cocycles are unitarily conjugate for all x and every power, with identical operator and Frobenius norms. The displayed numerical bound applies to the stated substitution despite that index convention. This repair is exact and has no approximation.

## The actual physical hull retains the absolutely continuous component

Let Sigma be the labelled primitive substitution subshift, and Y its spin-only image in {1,i,-1,-i}^Z. The map from Sigma to Y is a continuous shift factor. Whether it is a conjugacy is irrelevant and is not assumed. The pushed-forward invariant probability is the unique invariant probability on Y. Consider the physical measure

    omega_y = sum_n y_n delta_n.

Every coefficient has modulus 1, so omega_y is translation bounded and its support is exactly Z. Its R-translation hull is the ordinary unit suspension of Y. Indeed, the lattice support determines the translation phase modulo Z, and the coefficients determine the complete spin sequence. The usual seam identification accounts for the ambiguity in integer representatives. The map from the compact suspension to the measure hull is continuous and bijective, hence a homeomorphism. In particular, hidden digit labels are not needed for this statement.

Now define on the actual weighted measure hull

    P(sum_n y_n delta_(n-u)) = sum_n y_n^2 delta_(n-u).

This is coefficient-wise squaring at each existing support point, not multiplication of two measures as distributions. It is a continuous factor: on symbolic transversals it is a one-block map, it commutes with the shift, and its induced suspension map respects the seam. It commutes with real translations and preserves the support phase. Its image is the actual chi_2 spin-comb hull. Thus absolutely continuous spectrum in the squared comb pulls back isometrically into the physical chi_1 comb's L2 space. Faithfulness of chi_1 identifies its four spin values, but does not imply digit recovery and is not used to assert that.

Theorem 4.5(b) and Appendix A, Corollary 2, give Lebesgue diffraction for the squared spin weights, because chi_2(W)/sqrt(2) is unitary. Equivalently its coordinate q_0 has torus Haar spectral measure and correlations delta_(m,0). This use is legitimate after the independent primitivity and aperiodicity checks above. On the unit suspension, the bounded section observable H([y,u])=y_0^2 has correlation

    C_H(t) = integral_0^1 delta_(floor(u+t),0) du = (1-|t|)_+.

For either translation-sign convention, its R spectral measure has density sinc^2(k) with sinc(k)=sin(pi k)/(pi k). It is nonzero and equivalent to one-dimensional Lebesgue measure. H is a well-defined bounded measurable observable; the section seam is measure zero. This establishes absolutely continuous R dynamics in the actual original weighted-comb hull, not merely in a larger labelled extension.

## Recoverable positive real specialization

After the initial independently written report, root proposed the weighting

    w(g) = 3 + Re((1+2i)g).

I independently checked its values on g=1,i,-1,-i: respectively 4,1,2,5. Thus its weights are positive, real, and injective, and the finite lookup Q(4)=Q(2)=1, Q(1)=Q(5)=-1 recovers g^2 from the physical weight. The visible weight sequence retains the squared-spin factor, regardless of hidden digits. The same symbolic-transversal/suspension construction proves that the lookup is a continuous real-translation-equivariant factor of the actual positive-weight comb hull. The section observable Q(w_0) therefore has the sinc-squared R spectral density computed above.

The decomposition is exact:

    w(g) = 3 + (1+2i)g/2 + (1-2i)g^3/2.

The constant, chi_1, and chi_3 sectors are distinct invariant orthogonal subspaces of the labelled L2 representation. Once the two nontrivial sectors are singular, their finite linear sum is singular, and Appendix A identifies its spectral measure with the positive physical comb's fundamental diffraction. More precisely it is

    sigma_w = 9 delta_0 + (5/4) sigma_F1 + (5/4) sigma_F3.

Cross spectral terms vanish by invariant sector orthogonality; singularity of the sum would also follow without this exact formula from the linearity of the singular spectral subspace. Uniform spin frequencies give mean 3 and mean square 23/2, agreeing with the formula's total mass 9+5/4+5/4. Its physical R diffraction is the periodized singular measure.

The chi_3 numerical dependence requires no separate approximation: with the displayed Fourier convention, B_chi3(x)=conjugate(B_chi1(-x)); hence the same identity holds for the full products and their Frobenius norms. Reflection x to -x preserves the torus integral, so any valid chi_1 integral bound applies identically to chi_3. Full rank holds in both cases. This is an exact reflection check; the reported error bound itself retains the qualification below.

This specialization is a reviewer-verified inference from the source's existing character-sector results and general weighting correspondence. No claim is made that the formula w was printed there or that it is a new research result. It supplies a positive real one-dimensional weighted witness, so positivity or a real-only weight convention does not obstruct the prior application. Unweighted point-set strengthenings remain distinct.

## Physical diffraction and the numerical qualification

Appendix A and Proposition 14 identify the torus spectral measure of the scalar spin observable F_1=sum_d f_d^(chi_1) with the fundamental physical diffraction of omega_y. F_1 belongs to H^(chi_1), which Example 10 asserts to be singular. Physical diffraction on R is its Z-periodic lift. If a torus measure is carried by a Haar-null set, this lift is carried by the countable union of its integer translates and remains singular relative to R Lebesgue measure. There is no conversion of a singular torus measure into an absolutely continuous R measure.

The source's numerical argument bounds the exponent by the operator-norm integral, and replaces that norm by the larger Frobenius norm. Its tabulated quantity is

    G_N = (1/N) integral_0^1 log(||B^(N)(x)||_F^2) dx,

an upper bound for twice the relevant exponent. At N=12 it reports G_12=0.688005 and error below 0.001, whereas the threshold is log(2). Even allowing displayed rounding, a conservative upper value 0.689006 lies below the exact lower bound

    log(2) > 2(1/3 + 1/81 + 1/1215) = 842/1215.

The margin is more than 0.003998. Consequently the source's stated numerical-error assertion is sufficient for its strict inequality. This reviewer has checked the normalization, the matrix order, the comparison direction, and this margin.

My independent midpoint replay at 65,536 points gives G_12 approximately 0.6879966061, consistent with the published value and reported error. It is a diagnostic, not a validated enclosure: no quadrature or rounding bound is proved. In particular, the deliberately coarse 4,096-point N=13 replay yields about 0.7166, illustrating aliasing from the doubling cocycle. Agreement across larger grids cannot certify the printed error claim. This report's numerical status must remain explicit even if another reviewer subsequently produces a certificate.

## Classification consequence and boundaries

For the literal unrestricted translation bounded measure target, the published results therefore provide singular physical diffraction and a nonzero absolutely continuous component of actual physical-hull dynamics, even with positive real physical weights through the verified specialization. The inputs predate the frozen 2026 construction. Attribution as a prior application and correction to `already_solved` are justified with the above source dependence disclosed. The frozen unweighted planar construction remains a valid stronger-form witness if accepted by its own mathematical audits. This classification does not decide whether that strengthening had previously appeared.

The following claims are not supported here: that Frank and Manibo printed an explicit answer to van Enter's named conjecture or the particular positive weighting above; that the weighted example is an unweighted set; that these inputs settle a newly imposed unweighted one-dimensional version; that this is the earliest counterexample; or that this reviewer independently certified the historical integral error. Such assertions should not be inserted into the record.

Actual counts for this qualified classification: structural blockers 0; mandatory mathematical repairs 0; repairs made to this review's preliminary shortcuts 2; unresolved structural target gaps 0 under the ordinary unrestricted reading and acceptance of the published result; unresolved independently certified numerical-reproduction gaps 1. A stronger claim of an entirely independently certified prior-example proof has blocker count 1 until that numerical gap is closed. Root remains responsible for reviewing any classification proposal/action helper and for any authorized repository changes.
