# Root mathematical reconstruction: PR377

UTC2026-10-03T05:22Z. Frozen head75bea4d3be9904e90c3843892671a440ba4d2c42. This reconstruction follows candidate exposure and subsequent independent-family reports; it is not blind rediscovery. Root fetched all four controlling PDFs independently, verified their complete historical hashes, read the relevant primary proofs and hypotheses, and visually inspected six controlling pages. The whole frozen packet is **not yet acceptable**: the extension direction requires an explicit global repair. Workflow55%; the exact existence question has a credited prior positive resolution.

## Exact question and credited answer

The literal Franz contribution in OWR49/2012 printed2954–2956 uses rational equivariant cohomology for T=(S1)^r. For a rational Poincaré duality space the largest possible nonfree syzygy order is floor((r−1)/2); the question asks whether this is attained for r≥5. The printed formulas use undeclared n. Their surrounding rank notation and AFP Corollary1.4/Proposition5.12 make the intended parameter r. It cannot consistently be read as the dimension of the manifold.

For r=2m+1 take a=b=1 and the all-one vector in Franz's big polygon construction. For r=2m+2 take (0,1,…,1), which gives an extra S3 factor. These answer the exact existence/sharpness request over Q. This is Matthias Franz's prior result, not a new discovery or a minimal-dimension theorem. [ArXiv's primary record](https://arxiv.org/abs/1403.4485v4) dates v1 to18March2014 and corrected v4 to12June2023. [OUP metadata](https://academic.oup.com/imrn/article-abstract/2015/24/13379/2363634) identifies IMRN2015 pp13379–13405, DOI10.1093/imrn/rnv090, published online16April2015. The fully read v4 is an author version, not a fresh reading of the inaccessible publisher PDF. The actual published Franz–Huang2020 PDF independently credits this prior maximal order; its Section2 characteristic-zero convention includes Q. Its full general-length classification is not needed here.

## Geometry, exact rank and technical hypotheses

Let X be the zero set of F(u,z)=sum u_j inside (S3)^r, where |u_j|²+|z_j|²=1. It is compact. At a point with some z_j≠0, any complex variation of u_j is allowed by a compensating variation of z_j, so dF is surjective. If all z vanish and a nonzero real covector annihilates dF, each u_j is collinear with its representing complex vector. Since each has modulus1, u_j equals plus or minus one common unit vector. An odd signed sum cannot be zero. Hence0 is a regular value, and X is a smooth manifold of dimension3r−2. The oriented ambient product and the globally ordered two real constraints orient its normal bundle and therefore X.

Every point can be joined to u=0 by scaling u_j with λ decreasing to0 and assigning z_j modulus sqrt(1−λ²|u_j|²), using its original phase when nonzero and a chosen fixed phase when initially zero. This gives a path for each starting point; it does not assert continuous choices over all X or a deformation retraction. The endpoint set (S1)^r is connected, so X is connected and a rational PD space.

The coordinate torus acts on z_j. At u=0 and all z_j=1 the stabilizer is trivial, establishing full effective rank. At any point the stabilizer is precisely the coordinate subtorus for the zero z coordinates. There are finitely many such types. The orbit skeleta are finite unions of coordinate-zero loci in a compact real algebraic manifold; they are compact semialgebraic sets, locally contractible and of finite cohomology. X is Hausdorff, second countable, locally compact and finite dimensional. AFP Sections3.1,3.5, Assumptions3.2/4.1 therefore apply, including characteristic0. The extra even-rank sphere is acted on by an additional effective circle, and has the same required properties.

Zero length in the even case is generic because the remaining odd sum cannot be bisected. The equations factor as S3×X_odd. A sufficiently small positive replacement is optional and stays in the same chamber; the exact zero-length product already suffices. No almost-free, free-action, integral-coefficient or positive-characteristic variant of the question is being silently imposed or resolved.

## Equilateral Morse proof and distinct Euler classes

On Y=(S3)^r minus X use f=−|sum u_j|². Sublevels bounded away from0 are compact. A critical point must have z=0, and the u_j align with a common unit vector, with signs s_j=−1 on a short J and +1 otherwise. Put j=|J|≤m and q=r−2j>0. Each critical manifold P_J is a circle.

Writing u_j=s_j exp(iθ_j)sqrt(1−|w_j|²) near a critical point, the quadratic variation of f is

    q Σ s_j(θ_j²+|w_j|²) − (Σ s_j θ_j)².

The angular matrix q diag(s)−ss^T kills the common rotation vector. For j>0 its remaining eigenvalues are −r once, −q repeated j−1 times, and q repeated r−j−1 times. For j=0 they are r repeated r−1 times. The w block has2j negative directions. Thus the normal index is3j, with exactly one tangential zero direction. This verifies the source's intended Morse–Bott conclusion despite its derivative-sign and extrema/nondegeneracy wording errors. The unweighted f is used only for the equilateral case; no general-length claim is inferred.

Reflection of an imaginary z coordinate gives a (Z/2)^r action preserving f. The negative-bundle orientation character is the product of the reflections indexed by J. Different critical subsets have distinct characters, including those at the same critical value. Relative Morse groups carry those characters, whereas previously attached groups carry earlier distinct ones. Over Q the connecting maps therefore vanish. The geometric cycles V_J (dimension3j) and W_J (dimension3j+1) represent the two Thom generators at P_J and give the homology basis by induction. This is a reflection-character argument. The negative bundle contains TS1 factors and has zero equivariant Euler for nonempty J; it is not the separate fixed-sphere normal bundle whose Euler is t_j below.

## Equivariant inclusion and actual extension direction

The cycles lift to equivariant fundamental classes, yielding free R bases in Y and (S3)^r. The fixed circle inside the jth sphere has a normal complex line with Euler t_j. Naturality, the diagonal circle class and product orientations give

    iota(V_J)=V_J,
    iota(W_J)=Σ_(i outside J) (−1)^(#{j in J:j>i}) t_i V_(J union {i}).

The Euler calculation here belongs to the fixed-circle inclusion, not the negative Morse bundle. Identity columns remove the short V_J. For smaller W_J one obtains free kernel combinations; at the middle cardinality m the remaining map is signed exterior multiplication by Σt_i e_i. Squaring gives cancellation of each distinct pair in opposite orders. Exactness is the Koszul exactness of the regular sequence t_1,…,t_r, not a conclusion from finite samples.

The Koszul syzygy K_j is normalized to be generated in degree0. Minimality gives pd(K_j)=r−j and depth at the homogeneous maximal ideal equal to j. Away from that maximal ideal some t_i is invertible, the localized Koszul complex contracts, and K_j is free. In particular K_m is a genuine nonfree mth syzygy. Complement duality identifies the middle cokernel with K_m and the middle kernel with K_(m+2), plus the stated free classes. Equivariant Poincaré–Alexander–Lefschetz duality gives

    0 → C=(coker iota)[3r] → H_T*(X) → Q=(ker iota)[3r−1] → 0.

The corrected v4 shifts are K_m[3m] in C and K_(m+2)[3m+3] in Q. They differ by an odd degree; the intrinsic degrees and resolution shifts are even, so their graded Ext1 in degree0 vanishes. Free summands of Q split automatically. For m≥3, Ext1(K_(m+2),R)=0 since the sole positive Ext into R is in degree r−(m+2)=m−1>1. At the exceptional m=2,r=5 the actual sequence has

    C=R[0] ⊕ R[3]^5 ⊕ K_2[6],
    Q=K_4[9] ⊕ R[10]^5 ⊕ R[13].

**Mandatory frozen-packet defect:** the guide and previous review/checkers use10,13 as free target shifts. Those are free quotient shifts. The free Ext targets are0,3, with target-minus-quotient differences−9,−6. AFP Lemma2.4 permits a degree0 nonzero extension of K_4[9] by R[l] only when l−9=2. Neither actual target is exceptional, so splitting still follows. The wrong arithmetic assertions replay successfully because they test the wrong objects. Their successful receipts cannot certify the defective justification. The correction must supersede every echoed current assertion and bind corrected programs/receipts globally while preserving the frozen record.

General b>1 splitting language in the source requires extra care: Ext into R then involves R/(t_i^b), not just a one-degree field. The present reconstruction uses b=1. It does not promote that generalized claim or rely on an unchecked Puppe splitting argument.

## Exact order without splitting; even rank

There is also a splitting-independent proof. At every prime different from the homogeneous maximal ideal, C and Q are free and their extension splits locally, so the middle is free. At the maximal ideal depth C=m and depth Q=m+2. The depth lemma forces the middle depth exactly m. The localized depth criterion gives an mth syzygy and excludes order m+1. Thus the exact-order conclusion does not depend on the corrected splitting calculation and is not circularly inferred from the target upper bound.

For the extra circle on S3, the Borel construction is the unit sphere bundle of 1⊕L. Its Euler c_2 is zero. The Gysin sequence gives a free Q[s]-module with generators in degrees0 and3. Equivariant Kunneth over Q identifies the even-rank module with two shifts of the odd module extended to R[s]. Flat extension preserves the mth-syzygy lower bound. The prime generated by all old t_i but not s has height2m+1 and middle depth m, showing failure of order m+1. Equivalently, a failed next regular sequence survives faithful polynomial extension. Depth at the full enlarged maximal ideal is m+1 and alone would give the wrong answer. Every requested odd/even rank is covered; r5 andr6 both have exact order2.

## Evidence and remaining acceptance gate

Root has read all three frozen executable sources, all substantive author/review metadata and manifests, the original problem and relevant primary proof chain. Four full fresh PDFs match exact historical bindings. The controlling EMS rank typo, v4 extension direction, AFP graded Ext and upper-bound proof, and FH characteristic0 convention were visually checked. Full original checker streams and nested/Git bindings are being reproduced independently. These finite checks supplement universal arguments; they do not prove topology, classification, all-rank exactness or novelty by enumeration.

The [author's correction page](https://math.sci.uwo.ca/~mfranz/papers.html) adds effective action to the separate Proposition7.4 dimension bound, omitted even in v4. That proposition is unused, and the witnesses here are effective. The prior repository search is explicitly bounded and has not been reproduced; it is unnecessary for this direct credited positive literature answer. The current source family initially repeated the wrong exceptional shifts; the independent algebra family falsified them. Root agrees with the algebra objection and with the scope-limited geometry conclusion. A global correction, complete updated replay/bindings and a new whole-package adversary remain necessary before acceptance as already_solved,0/5. No new paper or DOI is authorized for this credited partial disposition.
