# Independent adversarial audit: exact root selections over all R⁶

**Target:** 10800007 / AMR-107-0007, Vassiliev, Problem 2A.  
**Verdict:** **PASS_COMPLETE_LITERAL_SOURCE_NO_COVER_OBSTRUCTION.** No mandatory mathematical correction.  
**Recommended classification:** `claimed_solved`, 1/5, expressly for the printed all-R⁶, open-cover, exact-section formulation. The source's suggested finite-genus interpretation is inconsistent with those requirements; a repaired problem is not resolved by this verdict.  
**Review type:** separate adversarial AI source/proof review, not human peer review. The obstruction is classical, and no novelty or historical-priority claim is certified.

## 1. Frozen material and source check

The reviewed `NO_COVER.md` has SHA-256

`d88322ab825acd97914b898018116f2544dc92c460fe3c37ac86eeab331a8448`.

The submitted checker has SHA-256

`bffca8826261f1df435486cda2c0f2010809ceee744d8df21cb321dc42583bef`;

its receipt has SHA-256

`acd3997a76816fcc6c22745ec0fb47d66569735247ebab1e95f63dbbc10ff7d9`.

I read the complete candidate and checker, independently inspected the final journal's rendered p. 205, read the surrounding Section 2 in the complete published PDF, and checked the currently available journal HTML. The original arXiv manuscript agrees. All three define ordinary continuous exact selections on open subsets covering the entire six-dimensional real coefficient space. The coefficient perturbations are arbitrary affine-linear real polynomials. There is no deletion of a discriminant in Problem 2A. Problem 2B separately allows a fixed positive approximation error. The immediately following section does explicitly remove an essential ramification set for its different question, which is not a qualification on Problem 2A.

Primary source: V. A. Vassiliev, *A Few Problems on Monodromy and Discriminants*, Arnold Mathematical Journal **1** (2015), 201–209, §2, p. 205. [Published PDF](https://armj.math.stonybrook.edu/pdf-Springer-final/015-0011-9.pdf), [journal HTML](https://armj.math.stonybrook.edu/html-articles/Files-2015-2024/15-11/), [author preprint](https://arxiv.org/abs/1504.01997).

## 2. Independent derivation of the local obstruction

Set the four nonconstant coefficients to zero, and set the constants to \(a_0=-u\), \(b_0=-v/2\). The equations then read
\[
 x^2-y^2=u,\qquad 2xy=v,
\]
so the solution correspondence on this real two-plane is precisely \(w^2=\zeta\), where \(w=x+iy\) and \(\zeta=u+iv\). In particular, the factor of two in the second equation has been accounted for. There are no other solutions of the restricted real system. The slice is a continuous injective linear map into the six-dimensional coefficient space, with zero mapped to zero.

Assume a section exists on any open neighborhood \(U\) of the zero coefficient vector. The inverse image of \(U\) under the slice map contains a complex disk centered at zero. Choose any sufficiently small circle \(|\zeta|=r\) in this disk. Restricting and normalizing the section gives a continuous map
\[
 q:S^1\longrightarrow S^1,
 \qquad q(e^{i\theta})=r^{-1/2}s(re^{i\theta}),
 \qquad q(z)^2=z.
\]
The induced degree therefore satisfies \(2\deg(q)=1\), impossible because the degree is an integer. This independently derives the conclusion without making an assumption about the chosen branch at one point.

The submitted proof replaces degree theory with an elementary path from 1 to −1. Its squared path is closed, and the quotient of a putative selected root by the original path is a continuous map to \(\{1,-1\}\). Connectedness makes this quotient constant, while the endpoint comparison makes it change sign. Both line-segment formulas agree at the joining point, are nonzero everywhere, and remain in the unit disk. Choosing the scaling constant with strict squared modulus below the disk radius places the entire loop inside the required neighborhood. The proof checks out.

## 3. Attempts to evade the obstruction

- **A global obstruction alone would be insufficient.** The argument is local at the zero coefficient vector. Every open neighborhood contains a small complete circle in the constant-coefficient slice. Shrinking the neighborhood does not remove the obstruction.
- **Additional roots away from the slice do not help.** The selection must still be an exact solution at each point of the slice, where its only possible values are the two complex square roots (and zero at the ramified parameter).
- **Multiplicity is irrelevant to point-valued continuity.** At the zero parameter, all real solution values coalesce at the origin. Algebraic multiplicities do not create additional values of a map into R².
- **Disconnected open sets do not help.** One still obtains a disk in the inverse image of the member containing zero; no global connectedness hypothesis on that member is needed.
- **Arbitrarily many open sets do not help.** Any cover of all R⁶ contains a member containing zero. That member alone would violate the local theorem. Thus the admissible-cover class is empty, not merely devoid of finite covers. Writing the covering number as infinity requires the explicitly stated extended convention.
- **The argument uses ordinary topology and exact sections.** Allowing locally closed pieces, deleting ramified parameters or replacing sections by approximate selections changes the target.

These points rule out the most plausible scope and topology shortcuts.

## 4. The source's finite-cover hint and the status decision

The source's subsequent square-root remark is incompatible with its own exact-section definition over the whole complex plane. The corresponding punctured-plane statement does have covering number two. The two slit domains in the candidate are open, cover C minus zero, and support the indicated continuous argument branches. One branch over the full punctured plane is impossible by the same degree calculation. Neither slit domain includes zero as an interior point.

This mismatch is materially disclosed in the candidate, and should remain prominent in its title, abstract and status description. It does not invalidate the literal theorem: the journal repeats both the all-R⁶ parameter space and the exact-section requirement, rather than merely omitting a qualification in a shortened title. The section is specifically about maps that need not be fiber bundles. Therefore I recommend a complete literal-source disposition, rather than pretending to solve an unspecified repaired finite-genus question. If the project instead changes its target to such a repaired problem, this package cannot support a solved status for that different target.

The approximate question is genuinely excluded. On the slice, zero is within epsilon of a square root whenever the parameter modulus is smaller than epsilon squared. Thus this exact local obstruction does not establish an obstruction to Problem 2B. The candidate makes precisely this limited observation and no claim about a global approximate cover.

## 5. Reproduction and independent diagnostics

The submitted standard-library checker was run in an isolated copy beside the frozen artifact. All **5,618 assertions** passed, and its written receipt reproduced byte for byte.

The separate checker in this bundle uses rational points on the upper unit semicircle, rather than the submitted two-segment root path. Squaring them produces 40 closed polygons whose exact winding is one, with all polygon edges checked to avoid zero. It also verifies the six-coefficient substitution independently, the nonzero real Jacobian away from the branch point, scaled coefficient-ball bounds, root distances for the approximate diagnostic, and the frozen artifact hash. All **14,891 exact assertions** passed.

These controls check algebra and finite diagnostics only. Neither sampled polygons nor finitely many integers prove the topological theorem. The proof is the all-integer degree obstruction (or the submitted connectedness argument), combined with openness at zero.

## 6. Final assessment

The frozen package is correct and complete for the exact printed Problem 2A. No mathematical revision is required. Preserve its literal-source qualification, the distinction between an empty cover class and the extended value infinity, the unresolved repaired/approximate variants, and the absence of a novelty claim. This audit does not assert that the journal author intended the literal infinite answer, or that no erratum exists beyond the sources recovered.
