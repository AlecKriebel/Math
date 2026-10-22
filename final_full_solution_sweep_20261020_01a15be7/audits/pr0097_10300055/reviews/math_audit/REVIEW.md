# Independent mathematical audit of PR97

Date: 2026-10-21 UTC. Reviewer scope: problem10300055 / AMR-102-0055, Calegari Question13.2. Mathematical-audit completion: **100%**. This percentage concerns this bounded review, not the repository-wide sweep or historical-priority research.

**Verdict: the corrected mathematical statement passes.** I found no counterexample or substantive gap in its proof under its explicit hypotheses. The usual smooth tightness conclusion follows from classical contact topology. The extra conclusion for C1 forms is valid with the corrected, explicitly restricted C2-disk definition. This is a mathematical verdict, **not historical-novelty or publication clearance**.

The mechanism checkpoint was saved before historical verdicts could influence the analysis. No `prior_*` verdict files were read at any point. I independently retrieved the original question and primary papers, reconstructed the proof, tested the possible failure points below, and replayed the scripts in copies contained in this directory. No external messages, PR actions, publication actions, spreadsheet writes, or repository-branch/index changes were made.

## 1. Exact target and assumptions

The original question was recovered from [Calegari's 2002 preprint](https://arxiv.org/pdf/math/0209081v1), printed p29, Question13.2 and its immediately preceding hypotheses. It asks for conditional tightness when a defining form for the specified minimal taut C2 foliation admits a contact Godbillon–Vey connection form. It does not ask the reviewer to construct that connection form. The source's separate sign/existence problem is not solved here.

The candidate works in the closed oriented interpretation of the fundamental-class evaluation. A global defining form alpha is necessarily nowhere zero and coorients the foliation. The source's closed transversal meeting every leaf implies usual tautness. Minimality excludes compact spherical leaves. Thus the source's intended smooth contact-form case fits the candidate's theorem. Atoroidality and the nonzero Godbillon–Vey evaluation are not needed for this conditional implication; weakening those assumptions is harmless.

The precise result verified here is this. Let M be a closed oriented smooth three-manifold, and let F be a cooriented taut C2 foliation with no spherical leaves. Suppose alpha and omega are C1 one-forms, alpha is nowhere zero,

    d alpha = alpha wedge omega,

and omega wedge d omega is nowhere zero. Then:

1. Every sufficiently C1-close smooth one-form is a tight contact form in the usual smooth sense.
2. There is no embedded C2 disk whose boundary is tangent to ker omega and whose disk/contact planes are distinct along its boundary.
3. In particular, when omega is smooth, ker omega is tight in the usual sense. Alpha itself need only be C1.

No claim about arbitrary weaker disk regularity or equivalence of all low-regularity definitions is needed.

## 2. Reconstruction and attempt to invalidate the pencil

Differentiating the connection equation gives

    0 = d(d alpha) = d alpha wedge omega - alpha wedge d omega
      = -alpha wedge d omega.

This is valid for C1 forms without assuming second derivatives of alpha: d(d alpha)=0 as a distribution; alpha wedge omega is C1; its exterior derivative is continuous and satisfies the product rule. A continuous coefficient vanishing as a distribution vanishes pointwise. The two other mixed expressions vanish directly:

    alpha wedge d alpha = 0,
    omega wedge d alpha = 0.

Consequently, for every constant real s,

    beta_s = omega + s alpha,
    beta_s wedge d beta_s = omega wedge d omega.

This universal identity proves contactness of the entire finite pencil, including its nonvanishing. It has the same sign on each connected component. There is no unsupported assumption that a connection form can be normalized or chosen independently in different charts. The defining and connection forms are global by hypothesis.

In coordinates, identifying one-forms and two-forms with vectors A,W,K by the Euclidean volume form, the general expansion has exactly the residual

    (W+s A) dot (K+s A cross W) - W dot K = s A dot K.

The differentiated relation is precisely A dot K=0. This calculation does not assume that d omega was initially given an artificially special parametrization. The independent script verifies the polynomial identity with all nine coefficients independent.

The restriction to constant s is essential. Replacing s by h(x) introduces omega wedge d h wedge alpha. The candidate explicitly avoids this false generalization. The independent coordinate model also retains and checks this error term.

## 3. Uniform limit and the finite use of Gray stability

Fix a metric, put m=min|alpha|>0 and W=max|omega|, and take s>0. The normalized covectors of alpha+omega/s and alpha differ by at most 2W/(m s). Thus their kernels converge uniformly in C0 to the tangent planes of F. Compactness is used both here and in the positive contact-volume margin below; no conclusion on arbitrary noncompact manifolds is being asserted.

The primary published formulation needed is stronger than existence of some tight approximation: **every sufficiently close contact structure is tight**. It is stated in [Vogel2011, p42](https://msp.org/gt/2011/15-1/gt-v15-n1-p03-p.pdf), attributed there to Eliashberg–Thurston. [Dathe–Rukimbira2008, Proposition3.3, p5](https://arxiv.org/pdf/0812.3389) independently records the neighborhood statement and points to *Confoliations*, p50. I did not obtain the original book; these explicitly stated primary-paper formulations suffice for the application. The sphere exception is excluded by the theorem's hypotheses.

Choose one finite S with ker beta_S inside that neighborhood. If the forms are smooth, beta_s for 0<=s<=S is a smooth family of smooth contact structures on a closed manifold. [Vogel2016, Theorem2.9, p2451](https://msp.org/gt/2016/20-5/gt-v20-n5-p01-p.pdf) gives precisely the smooth Gray theorem used here. The resulting isotopy transports an overtwisted disk if one exists, so tightness at S proves tightness at 0. Neither a foliation endpoint nor an infinite interval is part of the Gray application.

For a negative contact form, reverse ambient orientation on that component before using the positive formulation. Tautness and existence of an overtwisted disk are unchanged. The chosen positive scaling 1/S also preserves the coorientation in the limit. Disconnected manifolds are handled component by component.

## 4. The C1 extension survives a separate quantitative check

Orient each component by omega wedge d omega and write that form as c(x)dV. Compactness gives c0=min c>0. On the fixed interval [0,S], let B bound both |beta_s| and |d beta_s|. If a smooth approximation a to alpha and a smooth eta near omega satisfy

    |eta+s a-beta_s| <= delta,
    |d(eta+s a-beta_s)| <= delta

uniformly, the contact-volume error is at most 2B delta+delta^2. Choose delta with this bound below c0/2. The C1 errors of a and eta can be chosen below delta/(1+S), or a stricter bound if needed to stay in the open endpoint neighborhood.

One fixes a sufficiently accurate smooth a first and then takes a whole sufficiently small C1 neighborhood of omega for eta. Smooth approximation of C1 sections on a compact smooth manifold follows by a finite chart cover, convolution, and a partition of unity. The family eta+s a is smooth in position and s, remains contact on the entire interval, and has a tight endpoint. Smooth Gray stability makes ker eta tight.

The approximation a is not required to remain integrable. Imposing that unnecessary condition would create a gap; the actual argument uses only openness of contactness on this one finite interval. Also, this proof never invokes Gray stability for a merely C1 contact family.

## 5. Simultaneous smoothing of the overtwisted disk

The disk criterion is checked against [Dathe–Rukimbira2008, p5](https://arxiv.org/pdf/0812.3389) and [Vogel2011, Definition1.3 and its contact specialization, pp42–43](https://msp.org/gt/2011/15-1/gt-v15-n1-p03-p.pdf). It uses Legendrian boundary and distinct disk/contact planes along that boundary. This is a valid smooth overtwisted-disk criterion; requiring contact tangency of the whole disk boundary is an alternative model, not a counterexample to the stated criterion.

For a smooth disk with boundary gamma, choose a smooth tube S1 times D2 and its globally defined angular one-form dt. Given smooth theta_j tending to a C1 theta in C1, the functions

    q_j(t)=theta_j(gamma'(t))

tend to zero in C1, since theta(gamma')=0. Subtract q_j(t)chi(u,v)dt, with chi equal to one near the core. The correction is smooth, supported strictly inside the tube, tends to zero in C1, and annihilates gamma' exactly. Uniform contactness and the positive angle between the distinct boundary planes persist.

For a C2 disk, approximate its embedding in C2 by smooth embeddings. Embedding is preserved for sufficiently accurate approximations on the compact disk. In a fixed smooth tube around a nearby smooth core, the boundary graphs can be written

    gamma_j(t)=(t,U_j(t),V_j(t)),
    (U_j,V_j) -> (U,V) in C2.

After setting q_j=theta_j(gamma_j'), use the correction

    q_j(t)chi(u-U_j(t),v-V_j(t))dt.

This is smooth and makes each gamma_j exactly Legendrian. By the chain rule,

    q_j' = D theta_j(gamma_j)[gamma_j',gamma_j']
           + theta_j(gamma_j)[gamma_j''],

in component notation. C1 convergence of the forms and C2 convergence of the curves imply q_j and q_j' tend uniformly to zero, because the limiting pullback is identically zero. The first derivatives of the correction are bounded by a fixed multiple of |q_j|+|q_j'|: derivatives of the cutoff introduce only uniformly bounded U_j' and V_j'. Thus the corrections tend to zero in C1. Distinct disk/contact planes persist by C1 convergence of the embeddings along their compact boundary. Smooth overtwisted contact forms arbitrarily close to theta would result.

Applied to omega, this contradicts the whole neighborhood of tight smooth forms from Section4. This proves the corrected C2-disk conclusion. The C2 requirement is doing actual work; an unrestricted C1-disk version would require a new argument.

The original candidate's assertion of equivalence among unspecified low-regularity tightness/disk conventions was not established. The corrected candidate removes that definitional overreach. It also states its smoothing lemma on a closed manifold, matching the uniform openness argument. No further mathematical repair of the corrected theorem is required.

## 6. Reproducibility and limits of the computations

Frozen input hashes are in `SNAPSHOTS.json`. Successful receipts are:

| Replay | Assertions | Outcome |
|---|---:|---|
| Original supplied verify.py |87|PASS|
| Corrected supplied verify.py |87|PASS|
| New independent_falsification.py |22|PASS|

The initial default and bundled Python attempts failed because neither had SymPy. This was an environment issue, resolved in a reviewer-local virtual environment with SymPy1.14.0 and mpmath1.3.0; no global packages were changed. Exact pins are in `requirements.txt`. The supplied scripts and candidates were copied into this directory before execution, so their outputs could not modify the source snapshots.

To reproduce, create an isolated Python environment from `requirements.txt`, then run the two copied `verify.py` scripts and `independent_falsification.py`. Their receipts retain candidate/script hashes and scope statements. The independent script checks general symbolic jets and a periodic moving-boundary model; these are algebraic and local diagnostics. No finite test proves the global Eliashberg–Thurston theorem, Gray stability, or historical novelty. The universal mathematical argument is the proof above with its explicit classical inputs.

## 7. Classical antecedent and exact remaining gap

I independently read the relevant [Dathe–Khoule2012 author-uploaded full text, Definition2.1 and Theorem2.2, pp102–103](https://www.researchgate.net/publication/258228980_Sur_les_deformations_d%27un_feuilletage_de_codimension_1_en_structures_de_contact). In dimension three, its mixed-form criterion specializes here to zero, and its explicitly allowed choice C(t)=1, B(t)=t gives alpha+t omega. This is the same plane-field family after positive scaling. Thus the affine mechanism is already covered by that published work; it should not be advertised as a new construction.

[Khoule–Manso–Ndiaye–War2025, Theorem6.2, pp32–33](https://arxiv.org/pdf/2503.00454v1) reproduces that criterion with historical C1 attribution. Its displayed equality after Eq62 incorrectly drops the general nonnegative mixed term. The corrected candidate notices this. In the present zero-mixed-term specialization the equality is independently valid. None of the later preprint's unrelated dynamical claims is needed or endorsed.

The final tightness implication is a short corollary of this mechanism and established neighborhood/Gray results. I have not established whether the exact application to Calegari's question was explicitly recorded earlier, whether the final2003 chapter changed it, or whether the low-regularity refinement has a historical firstness claim. The mathematical audit cannot supply the still-required novelty clearance. It supplies a checkable full proof of the stated conditional smooth conclusion and the narrowly defined C1 extension.

**Disposition:** preserve the corrected theorem and proof as mathematically valid classical reasoning. Do not label it mathematically rejected. Do not infer novel-publication eligibility from this verdict. The remaining publication gate is priority/originality, not an unrepaired mathematical defect.
