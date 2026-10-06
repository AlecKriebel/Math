# Independent derivation and adversarial checks

## Scope and independence

This is a priority/verification audit, not a new solution attempt. New central proof-search turns: **0**. Original effort is recorded as 2/5 by the parent. The submitted status/head supplied for comparison are `claimed_solved` and `fb50facb2a7389bb272bbf0b5cbd80c24c79b992`; this audit reads the repaired candidate file at the named sibling path, so it does not certify that this repaired content exists in that Git commit. No sibling reviewer REPORT, VERDICT, or OWN_ANALYSIS was used. INITIAL_HYPOTHESES.md records the pre-source mechanism and competing hypotheses.

Let M be a closed oriented smooth three-manifold with cooriented taut C2 foliation F without spherical leaves. Let alpha, omega be global C1 forms, alpha nonsingular, d alpha = alpha wedge omega, and omega wedge d omega nowhere zero. For the smooth statement, omega is smooth; alpha may remain C1. Tightness for C1 omega is only the candidate's stated absence of embedded C2 disks with Legendrian boundary and boundary tangent planes distinct from ker omega. All conclusions below import the ET neighborhood theorem and smooth Gray stability; those deep theorems are not re-proved here.

## Three-dimensional affine criterion

For an integrable one-form a and a contact one-form b, direct expansion on a three-manifold gives

    (C a + B b) wedge d(C a + B b)
      = C B [a wedge d b + b wedge d a] + B^2 b wedge d b,

because C,B depend only on the parameter and a wedge d a=0. This is exactly n=1 of Dathe-Khoule2012 Theorem2.2, rather than a different coefficient convention. Put Q=a wedge d b+b wedge d a and V=b wedge d b. In the orientation for which V>0, Q>=0 suffices for every C>0, B>0, including Q=0. Necessity in the theorem uses B->0, C->1 at the foliated endpoint. No derivative of the volume is required.

For the candidate a=alpha,b=omega, d alpha=alpha wedge omega implies omega wedge d alpha=0. Also

    0 = d(d alpha) = d(alpha wedge omega)
      = d alpha wedge omega - alpha wedge d omega
      = - alpha wedge d omega.

For C1 forms the same identity holds distributionally: d alpha equals a C1 two-form alpha wedge omega, its distributional derivative equals the continuous product-rule expression, and d^2 alpha=0. Thus alpha wedge d omega=0 pointwise. Consequently Q=0 **term by term**, and

    (alpha+t omega) wedge d(alpha+t omega) = t^2 V.

Equivalently beta_s=omega+s alpha satisfies beta_s wedge d beta_s=V for every real constant s. The candidate's central affine mechanism is literally a specialization of the earlier general criterion/expansion. It is not protected from that antecedent by alpha being nonclosed.

## Smooth tightness deduction

If alpha and omega are smooth, ker beta_s tends uniformly to ker alpha as s->+infinity, because ker beta_s=ker(alpha+s^-1 omega), alpha has a positive lower norm bound, and M is compact. Choose **finite** S large enough for ker beta_S to enter the ET C0 tightness neighborhood. The path s in [0,S] is smooth and contact, so smooth Gray stability transfers tightness to ker beta_0=ker omega. There is no Gray theorem applied at the foliated endpoint t=0 or at infinity. This deduction is our stated corollary of the earlier affine criterion plus preexisting contact-topology results, not a literal tightness theorem located in Dathe-Khoule2012.

This also shows the connection with the already printed Dathe-Rukimbira2008 Proposition3.4: it uses near-foliation tightness followed by contact-path equivalence for a closed defining form. That proposition is not literally applicable to general alpha here, but its topological proof pattern predates the candidate. Dathe-Khoule's extension from closed to integrable defining forms supplies the relevant general contact mechanism.

If omega is smooth but alpha is C1, the exact beta_s need not be a smooth family in space. Smooth Gray cannot be applied directly. Fix the same finite S, approximate alpha by a smooth a, and keep omega itself smooth. Uniform C1 closeness of omega+s a to beta_s on M times [0,S] preserves contactness, because the exact contact volume V has a positive lower bound. Its endpoint stays in the ET neighborhood. Smooth Gray on this approximated finite path proves tightness of the original smooth omega. This is a routine finite-interval smoothing supplement, not a need for low-regularity Gray and not a new contact criterion.

For arbitrary smooth eta sufficiently C1 close to a C1 omega, the same argument with eta+s a proves that every such smooth eta is tight. The chosen a need not remain integrable. Thus the approximation step preserves source C2 foliation regularity rather than replacing it by a smooth foliation.

## Extra C1/C2-disk assertion

The candidate's disk-smoothing lemma is separate from the affine criterion. If theta is C1 and an embedded C2 disk D has Legendrian boundary gamma and boundary tangent planes distinct from ker theta, take smooth theta_j->theta in C1 and smooth embeddings D_j->D in C2. In a fixed smooth tube around a nearby smooth reference curve, reparameterize the boundaries as graphs (t,u_j(t),v_j(t)). Let q_j(t)=theta_j(gamma'_j(t)). C1 convergence of theta_j and C2 convergence of gamma_j imply q_j->0 in C1; the derivative contains D theta_j and gamma''_j, explaining the C2 requirement. Subtract

    q_j(t) chi(u-u_j(t),v-v_j(t)) dt.

The correction is smooth, annihilates gamma'_j exactly since dt(gamma'_j)=1, and tends to zero in C1. The translated cutoff stays supported in the fixed tube, with uniform first derivative bounds. Contactness and the strictly positive boundary angle persist. Each D_j is therefore a smooth overtwisted disk for a smooth contact form arbitrarily C1 close to theta. This contradicts the preceding tightness of all close smooth forms.

I find no gap in this bounded regularization argument. I have not found a prior literal theorem with this exact C1/C2-disk conclusion in the sources read. That absence does **not** verify novelty; this is a modest extra regularization assertion whose historical priority remains unresolved. It does not revive firstness of the smooth tightness corollary.

## Adversarial hypothesis outcomes

- **Stronger regularity:** original2012 body declares the underlying manifold C-infinity and uses smooth functions elsewhere; Theorem2.2 does not explicitly spell out C1 form regularity in the retrieved original. The2025 coauthor reproduction expressly attributes the theorem to2012 in the C1 setting. For n=1, the first-derivative expansion and the candidate's distributional identity independently verify the relevant C1 contactness. Smooth Gray still needs the finite smoothing above.
- **Nonzero first derivative:** neither original Definition2.1 nor Theorem2.2 requires Q>0. With B=t the form derivative at0 is omega, while the contact-volume derivative at0 is0. This allowed case is precisely the candidate's case.
- **Closed alpha:** closedness occurs in later corollaries/theorems; the main Theorem2.2 assumes integrability. Alpha wedge d alpha=0 suffices.
- **Different C,B:** original permits C>0 continuous at0 with C(0)=1 and nonnegative continuous strictly increasing B with B(0)=0, expressly identifying C=1,B=t as linear deformation. The2025 reproduction strengthens B to smooth; B=t meets both.
- **Wrong mixed term/sign:** n=1 gives alpha wedge d omega+omega wedge d alpha. Both terms vanish under the convention in the candidate. No sign substitution is needed.
- **Positivity:** the original convention takes contact volume positive. Reverse M's orientation, separately on components if needed, for a negative contact form. Tautness, existence of a disk, and tightness survive orientation reversal.2025 prints both signs explicitly. This does not shrink the target.
- **Forbidden endpoint:** Definition2.1 explicitly allows alpha_0=alpha to be foliated and requires contactness only for t>0. Our Gray interval starts/ends at contact forms and is finite.
- **Literal prior answer:** complete transcribed original body and references contain no tightness/isotopy/Calegari conclusion found. This is a paper-bounded absence, not exhaustive literature exclusion or historical firstness.

## Source errors and their effect

The original2012 binomial-lemma proof calls the space of2-forms a commutative subalgebra. Degree2 forms are not closed under wedge; the even-degree graded algebra is commutative, and its binomial identity for2-forms is correct. This wording error does not affect n=1, where no higher powers are used.

The2025 reproduction's formula(62) is the correct expansion. Immediately afterward it asserts that the volume divided by B^(n+1) equals V from the hypothesis Q>=0. In general the correct expression is V+(C/B)Q, so only >=V follows. The original2012 proof uses the correct inequality. In our case Q=0, the printed equality is exactly correct. This typo cannot defeat the covering conclusion.

The later original2012 Theorem2.9 proof claims an epsilon of B^-1(-a) and infers a zero from outer bounds aC <= C alpha(Z)+B <= bC-a. Such bounds do not establish a zero, and B need not attain -a; an appropriately small epsilon from C(0)=1,B(0)=0 repairs the local sign argument. That later closed-form obstruction is not used in our n=1 zero-Q deduction. No general endorsement of every theorem/proof in the paper is being made.

## Exact remaining gap

No mathematical gap was found in the bounded smooth tightness corollary, conditional on the imported classical theorems, or in the repaired finite-interval/C2-disk regularization checked here. The gap is publication/priority: the candidate omits a materially covering general antecedent; no exact prior explicit answer or exhaustive novelty clearance has been established; novelty of the extra C1 disk assertion is unverified. This audit grants no publication clearance and no PR95 waiver applies to PR97.
