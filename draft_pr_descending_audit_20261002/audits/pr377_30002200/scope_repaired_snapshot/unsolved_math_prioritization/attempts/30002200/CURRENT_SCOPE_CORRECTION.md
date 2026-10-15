# Current mathematical correction: extension direction

This note supersedes the exceptional-rank extension paragraph in the frozen CREDITED_PROOF_GUIDE.md and review/REVIEW.md, and the final extension assertion in each frozen checker. It does not alter the credited all-rank existence conclusion or assert a new solution.

At a=b=1, r=5, m=2, the actual primary sequence is

    0 -> C=(coker iota)[15] -> H_T*(X) -> Q=(ker iota)[14] -> 0,
    C=R[0] plus R[3]^5 plus K_2[6],
    Q=K_4[9] plus R[10]^5 plus R[13].

The free TARGET shifts in Ext1(Q,C) are0 and3. The shifts10 and13 belong to free QUOTIENT summands; these split automatically and cannot be used as Ext targets. Consequently the relevant target-minus-quotient differences are−9 and−6, not1 and4. AFP Lemma2.4, with polynomial generators of degree2, gives Ext1(K_4[9],R[l]) degree0 nonzero only if l−9=2. Neither actual target satisfies this condition. The K_4[9]-to-K_2[6] extension vanishes by parity. Thus the splitting conclusion is valid with the corrected justification.

For every odd rank2m+1, the free targets arise from high-cardinality V_J in the cokernel, of shifts3r−3|J| for |J|>m+1. The free quotient shifts arise from low-cardinality W_J in the kernel, of shifts3r−2−3|J| for |J|<m. These complement indices explain the final source's displayed direct-sum formula but cannot be interchanged inside its proof sequence. Corrected v4 nonfree shifts remain3m and3m+3. For m≥3 the relevant positive Ext into a free module occurs only in degree m−1>1. No rank is omitted.

The exact-order proof also requires no splitting. At the homogeneous maximal ideal C has depth m and Q has depth m+2, so the middle has depth exactly m by the depth lemma. Away from that ideal a variable is invertible and both localized Koszul terms are free. This proves the mth-syzygy inequalities at all primes and failure at m+1. For even rank the extra effective circle sphere has free cohomology Q[s] plus Q[s][3]. Polynomial extension preserves the lower bound and a witness prime excluding s retains depth m. Full enlarged maximal depth alone would give an incorrect inference.

The two original programs and their PASS outputs remain immutable historical arithmetic evidence. Their original final assertions checked the wrong shifts; replay success never established semantic correctness of those assertions. verify_corrected_source_cases.py and review/independent_check_corrected.py replace those assertions with shifts derived from the actual inclusion-map degrees. Their complete outputs are separately bound. Counts overlap the historical controls and are not additional distinct358064/983 discoveries. A new whole-package adversary must verify this repair before acceptance. All current publication wrappers bind this note and those corrected programs/receipts.

This is a rational b=1 construction. The source's blanket free-target splitting assertion for b>1 is not exported: Ext then contains R/(t_i^b), whose positive degrees can allow further classes. The separate Puppe splitting argument is not required by the nonsplit depth proof and is not newly certified here. The fixed-circle Euler t_j and the vanishing negative Morse-bundle Euler are different; the candidate's perfection uses reflection characters. The source's separate dimension bound requires effective action, and no minimal-dimension result is claimed.

Disposition remains credited already_solved,0/5. Extensive AI tools were used; this reconstruction is unrefereed and is not external human peer review. No paper, new DOI, Zenodo deposit, tracker row or release.
