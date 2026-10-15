# Independent adversarial whole-package review 01

PR #1024 / problem 30001113 / OWR-2492-004. Review completed 13 October 2026 UTC (12 October PDT). This is an AI adversarial review, not human peer review or a formal proof-assistant certificate.

**Verdict: PASS for the exact submitted candidate package; zero actionable findings, including zero low-severity necessary repairs.** The unrestricted no-recipient theorem is supported by a complete derivation. The extra component-prorepresentability variant remains outside the example. Attribution, bounded priority wording, reproducibility, archive inventory, source/PDF/metadata agreement and publication-stage disclosures are consistent. This review does not authorize publication, merge, closure or outreach, and does not turn an acknowledged bounded priority search into exhaustive originality.

The reviewed archive is `publication/local_deformation_devissage_source_verification_v1.zip`, SHA-256 `f41f904512ab3019da10069a6017fb45b6cb82fff7b49ab49ac4f8ea00dc95dc`. Submitted head: `37b4b2fa44368f49e534e4982bd11f5667e0bf36`. Every candidate file was pinned at start in [INPUT_PINS.json](INPUT_PINS.json). No prior acceptance was used as a premise. I first read the proposed note and independently reconstructed its arguments; supporting family reports were subsequently inspected for consistency and provenance. No candidate was edited.

## Claim and success criterion

Let k=F4, G=(F4,+), N=(F2,+), Q=G/N, and rho(a)(t)=t/(1+at). The claim is that for actual local-action deformation functors on local Artinian W(k)-algebras, with all identity-reducing coordinate conjugations allowed, there are no prorepresentable F and arbitrary natural maps D_N^Q -> F <- D_Q making the restriction-induction factorization D_G -> D_N^Q x_F D_Q formally smooth. F's tangent dimension is unrestricted. A valid disproof would require an error in the full-series restriction kernel, triviality of the quotient tangent under an allowed conjugator, a detectable tangent under some natural prorepresentable recipient, failure of the fixed-subfunctor/basepoint argument, or exclusion of the example by original quantifiers. None was found.

## Complete independent mathematical reconstruction

### Action, fixed rings and full fixed fields

For a,b in k, substitute t/(1+bt) into t/(1+at): the result is t/(1+(a+b)t). The t^2 coefficient of a nonidentity action is a, so the action is faithful and every nonidentity element has order-of-displacement two, hence conductor one and trivial second ramification group.

Set y=t^2/(1+t). The relation t^2+yt+y=0 is exact. For the N-generator, t/(1+t)=t+y; substituting into y leaves y fixed. The leading orders of y^m and t y^m are 2m and 2m+1, respectively, each with leading coefficient one. For any series f(t), successively subtract its leading term using the appropriate one of these monomials. The remaining t-order strictly increases, so the process converges and gives f=A(y)+t B(y) with A,B in k[[y]]. Such a decomposition is unique because nonzero A(y) and t B(y) have leading orders of different parity. Invariance forces y B(y)=0, hence B=0 in the domain k[[y]]. Thus the full fixed ring, rather than a truncation, is k[[t]]^N=k[[y]].

Multiplying a Laurent series by a sufficiently large power of y makes it integral, so the same decomposition works with A,B in k((y)). The identical invariance argument gives k((t))^N=k((y)). The polynomial for t has derivative y, nonzero in this field, so the extension is separable of degree two.

Choose u satisfying u^2+u+1=0. Since u(u+1)=1, direct substitution gives rho(u)(y)=t^2/((1+ut)(1+(u+1)t))=t^2/(1+t+t^2)=y/(1+y). The induced Q-action is the weakly ramified involution sigma(y)=y/(1+y). Repeating the leading-parity decomposition for z=y^2/(1+y) gives k[[y]]^Q=k[[z]] and k((y))^Q=k((z)), with basis 1,y. In particular, any nonzero invariant Laurent series has even y-valuation. All these arguments use complete formal series and convergent subtraction.

### Algebraic derivations and the sharp integral lattice

Perfectness of k in characteristic two implies every h(t) has a unique expression a(t)^2+t b(t)^2: take square roots of the even and odd coefficients. An arbitrary algebraic k-derivation d kills squares and therefore satisfies d(h)=d(t)b(t)^2=d(t)h'(t). This proves that every algebraic derivation is a continuous coefficient derivation, without first assuming continuity. Hence Theta=k[[t]] partial_t; the same reasoning applies to Laurent fields.

A coefficient derivation b(y) partial_y on k((y)) extends uniquely across the separable field extension. Differentiating y gives y'=t^2/(1+t)^2, so its extension is a(t) partial_t with a(t)=b(y)(1+t)^2/t^2. Uniqueness makes the extension N-invariant. Conversely, an N-invariant derivation restricts to the fixed field and is recovered by this formula. If b is nonzero, ord_t a=2 ord_y b-2. Thus integrality is equivalent to ord_y b>=1, giving the exact restriction lattice Theta^N = M = y k[[y]] partial_y.

The boundary is sharp: b=1 yields a pole of order two; b=y yields a(t)=1+t and is integral. Using all of Theta-sharp instead of M, or incorrectly imposing b in y^2 k[[y]], changes cohomology and would invalidate the argument. The published note uses the correct lattice.

### Complete-series cohomology and restriction injectivity

For quotient conjugation, the coefficient operator is T f=(1+y)^2 f(y/(1+y)). It squares to the identity. If f lies in y k[[y]], T f=f is equivalent to invariance of f/y^2. The latter has y-valuation >=-1. Since an invariant Laurent series is a Laurent series in z, its valuation is even; it must therefore have valuation >=0. Consequently M^Q=y^2 k[[z]] partial_y.

For every full series H(z), substitution fixes H and gives (T-1)(y H(z))=y^2 H(z). Thus every invariant is an actual coboundary with an explicitly convergent full-series preimage. Conversely (T-1)^2=0 in characteristic two, so every coboundary is invariant. The cyclic formula gives H^1(Q,M)=ker(1+T)/(T-1)M=0. There is no inverse-limit argument or unsupported inference from finitely many monomials.

For an actual first-order lift, writing rho_A(g)=(id+e c(g))rho(g) identifies group relations with the cocycle equation. All identity-reducing conjugations change c by a coboundary. Suppose a G-cocycle restricts to zero in H^1(N,Theta). Subtract the corresponding Theta-coboundary to make it vanish on N. Comparing c(nu) and c(un) shows c(u) is N-invariant, because G is abelian and the N-values vanish. The relation u+u=0 gives (1+T)c(u)=0. The preceding full-series identity provides m in Theta^N with c(u)=(T-1)m. Subtracting this second coboundary preserves the zero N-values and kills c(u). The generators now have zero cocycle, so the entire cocycle is zero. Hence TD_G -> TD_N is injective.

The actual fixed subfunctor has D_N^Q(A) literally contained in D_N(A), so restriction into it has the same zero tangent kernel. No prorepresentability or tangent-space replacement of that subfunctor is needed.

An additional boundary calculation confirms the nonzero quotient direction. For Theta-sharp=k[[y]] partial_y, invariant coefficients are (1+y)k[[z]]: the valuation allowance is now -2 for f/y^2. Using the basis A(z)+y B(z), (T-1)f=y^2(A+B), so H^1(Q,Theta-sharp)=k, represented by 1+y. Also Theta-sharp/Theta^N=k with trivial Q-action, and H^1(Q,k)=k. The prescribed obstruction tangent is indeed one-dimensional. These dimensions are not assumptions of the theorem.

### The actual involution class and every allowed conjugator

Let B=k[e]/e^3, A=k[e]/e^2, and j(e)=e+e^2. The map j fixes k, is involutive, and is a local W(k)-algebra automorphism via W(k)->k. Consider sigma_e(y)=(y+e)/(1+y). Its constant coefficient is nilpotent and its linear coefficient 1+e is a unit. Such substitutions are continuous: the nilpotent constant ensures arbitrarily high powers eventually have arbitrarily high y-order. Its matrix M_e=[[1,e],[1,1]] has square (1+e)I, with invertible determinant. It is an involution lifting the nonidentity residual action, hence an actual faithful Q-lift.

The identity-reducing substitution chi(y)=(1+e)y+e, matrix C=[[1+e,e],[0,1]], satisfies M_(e+e^2) C=(1+e) C M_e in B. Both sides are [[1+e,e^2],[1+e,1+e]]. The projective unit scalar does not affect substitution. Ring-substitution order reverses ordinary function order; either equivalent conjugating direction is allowed. Thus the actual class x=[sigma_e] in D_Q(B), not a versal parameter alone, is fixed by j.

Its reduction v in D_Q(A) is nonzero. Every identity-reducing coordinate substitution over A is y+e h(y) for an arbitrary full h in k[[y]], including h(0). Expanding a conjugacy equation to first order would require 1/(1+y)=h(sigma(y))-sigma'(y)h(y), up to sign. The right side has constant term h(0)-h(0)=0, while the left has constant one. This excludes every allowed conjugator, not only matrices or polynomials. Normalizing the infinitesimal cocycle gives 1+y, in agreement with the independent cohomology calculation.

The cubic nilpotency is essential for this displayed matrix identity, but sufficient: the same identity fails with a nonzero e^3 discrepancy over k[e]/e^4. This is a verified boundary, not a gap, because the proof only needs the cubic object.

### Naturality for every prorepresentable recipient

For any natural eta:D_Q -> h_R, let psi:R->B be eta_B(x). Since j_*x=x, naturality forces j psi=psi, element by element. For c0+c1 e+c2 e^2, j adds c1 e^2, so B^j=k+k e^2. Reduction B->A maps B^j exactly into constants. Therefore eta_A(v) factors R->k->A. The local W(k)-algebra map R->k is its specified residue map, so the image is the residue basepoint.

This argument is unaffected by mixed characteristic, relations in R, its tangent dimension, obstructed directions, or nonlinear behavior of eta. It uses only Hom-representability and naturality on valid equicharacteristic objects of the original W(k)-category. It does not require eta to extend from any subfunctor, impose a tangent formula, or replace D_Q with a hull.

Independently, the prior injection A=k[e]/e^2 -> k[w]/w^3, e->w^2, makes v equal to the basepoint as an actual deformation class. One explicit matrix witnessing this is C_w=[[1+w,w],[0,1]], with M_(w^2) C_w=(1+w) C_w M_0. Every Hom-functor preserves the injection on target rings. Naturality then gives eta_A(v)=eta_A(0). This independently recovers the collapse argument and confirms the necessity of the current credit to the published Proposition 6.1.

### Actual fixed subfunctor and the small extension

The residual point over k is unique. For A, its base-change 0_N is fixed by Q: in this equicharacteristic object the original full G-action lifts by extending coefficients, and commutativity preserves the N-action. Thus 0_N is a genuine element of D_N^Q(A), not a fictitious cohomological invariant. Naturality along k->A makes any f:D_N^Q->h_R send it to the residue basepoint, without an extra pointedness assumption.

For any putative F and f,g, the recipient-collapse argument gives f_A(0_N)=g_A(v). Hence (0_N,v) belongs to the actual fibre product over A and reduces to its unique point over k. The surjection A->k is small, since (e) is annihilated by A's maximal ideal. Formal smoothness would supply w in D_G(A), over the residual G-point, with restriction 0_N and induction v. Injective tangent restriction forces w=0_G. Induction is natural, so its base-change image is 0_Q, contradicting v!=0. This is precisely the source's required lifting condition, already violated on the first-order small extension.

The example has nonprorepresentable involution component functors. It does not address the variant where both D_N and D_Q are assumed prorepresentable, and provides no contradiction to the separately conditional obstruction-space theorems.

## Primary-source quantifiers, credit and bounded priority

Fresh downloads from official hosts are pinned in [sources/RETRIEVAL.json](sources/RETRIEVAL.json); third-party bodies remain solely in ignored `sources/raw/`. The fresh hashes agree with the package's source records. The thesis landing page gave a web 403, but its official advertised content endpoint returned the full PDF successfully; no body-inspection gap remains for the thesis question.

- [OWR 54/2008](https://ems.press/content/serial-article-files/46200), Byszewski contribution pp.3038-3040: perfect field, faithful local action, identity-reducing conjugacy. The question on p.3039 imposes prorepresentability on F; Theorem 3 separately adds it to D_N and D_Q.
- [Utrecht thesis (2009)](https://dspace.library.uu.nl/handle/1874/33749), Question 6.4.4 and Remark 6.4.5/Theorem 6.4.7: the same separation of unrestricted question and conditional results.
- [arXiv:1112.0352v1](https://arxiv.org/abs/1112.0352v1), Definitions 1.1-1.2, Section 1, Proposition 2.4, Question 4.4, Remark 4.5 and Theorem 4.9: the example and first-order surjection are valid, with the component assumptions separately stated.
- [Published Byszewski-Cornelissen (2009)](https://doi.org/10.5802/aif.2450), Section 2.1 explicitly permits nilpotent constant coefficients; Proposition 4.1 pp.895-896 gives the exact parameter-shift conjugacy; Proposition 6.1 p.899 gives failure to preserve the injection used above.

The paper, README, supplement and both metadata representations consistently credit the known additive action, matrix conjugacy, involution pathology and tangent-cohomology framework. They correctly present recipient collapse as an elementary consequence of Proposition 6.1, and describe the assembled no-factorization obstruction as the contribution. They do not claim first discovery, exhaustive originality or verified continued openness through 2026. The three formulations are treated as one question.

The recorded priority ledger really contains 65 queries and 11 source/version records, and all 11 underlying source-body pins match locally retained originals. I additionally inspected relevant primary statements for the earlier BC version (Proposition 5.5), Dokchitser's constant-group quotient criterion and separate smooth-group-functor question, the 2012 order-five universality result, Obus's prime-to-p quotient restriction criterion, Dang's cyclic tower question, the 2022 explicit Klein-four family and the 2025 metacyclic cyclic-p-Sylow hypotheses. These focused checks agree with the package's scope comparisons; they are not fresh full proof audits of every cited theorem. Four additional search queries located no matching negative factorization assertion. The no-match observation remains bounded evidence; unindexed work and other omissions remain possible. No external communication was prepared or initiated.

## Portable checks, exact contracts and adversarial controls

[PORTABLE_39.json](receipts/PORTABLE_39.json) records an independent replay of all 39 packaged executions: nine baselines, twelve actual-source controls and eighteen runtime controls, across normal/-O/-OO. Every complete stdout, stderr and exit code matched the fixed references. Mathematical source files and the original adapter match their submitted counterparts byte for byte. The historical UID1000 harness was not replayed and is not represented as portable proof.

[INTEGRITY.json](receipts/INTEGRITY.json) checks all eleven assertion predicates against the adaptation record and the current explicit guards. Beyond predicate comparison, restoring guards to assertions and removing the inserted helper produces an AST identical to the entire original arithmetic program. There is no hidden arithmetic, control-flow or output-expression change. The adapted source contains no assertions and retains checks under optimization.

[EXTRA_CONTROLS.json](receipts/EXTRA_CONTROLS.json) records three additional complete 39-case passes from extracted archive copies, with the outer runner in normal/-O/-OO. Under outer -OO, nine damaged-package controls were rejected: extra stdout, extra stderr, wrong exit, unrelated RuntimeError, missing source-mutation anchor, syntax error, missing source file, disabled independent guards and wrong intended failure reason. Complete diagnostics are retained. Five direct recursive-JSON challenges reject nested bool/int equality, int/float equality, list-shape differences, extra keys and string/int differences. These checks test that malformed or unrelated failures cannot be silently accepted as intended controls.

[INDEPENDENT_MATH_CHECKS.json](receipts/INDEPENDENT_MATH_CHECKS.json), generated by an independently written arithmetic program, additionally checks three nonzero F4 parameter shifts in cubic rings, their failure in quartic rings, the square-root injection conjugacy, 1024 first-order polynomial conjugators including constants, and selected series prefixes at precisions 17,33,41. An explicit finite-cohomology challenge shows that even cutoffs create a spurious highest-order class in M, while odd cutoffs do not. Enlarging or shrinking the lattice also changes finite H1. This is direct evidence against replacing the full-series proof with truncation-based conclusions. None of these computations is presented as quantification over all formal series or natural transformations.

## Inventory, provenance, PDF and metadata

The archive contains exactly 108 entries: 107 manifest-listed files plus the manifest. All byte lengths, hashes, CRCs, filenames, sort order, fixed timestamps, modes and compression metadata checked correctly. Every archive member equals its current authored local counterpart. Rebuilding the declared archive recipe in memory reproduces the assigned ZIP byte for byte. There are no duplicate or traversal paths and no redistributed third-party raw source bodies. The separate deposit envelope has metadata exactly equal to metadata.json. Local build logs and render PNGs outside the declared deposit are excluded; they are not missing archive members.

All 27 original submitted files match both their pins and the actual files in Git commit 37b4b2fa44368f49e534e4982bd11f5667e0bf36. The current mathematical copies and fixed contract remain unchanged. Every relative navigation link in README, SUPPLEMENT and the evidence index resolves. The index clearly maps historical absolute paths to provenance and preserves stage-specific acceptance/holds, counts and source-search limits; these do not masquerade as current release approval. The pending whole-package gate is openly stated, with `preprint_ready=false` and `published=false`.

The five-page PDF was independently rendered at 110 dpi and every page visually inspected. Equations, proof order, text and bibliography agree with the TeX source. There is no clipping, missing glyph, overlap or broken reference. The first theorem continues onto page 2 but remains unambiguous; the page-5 bibliography is readable. The desktop compiler independently returned success, recorded in [COMPILE.json](receipts/COMPILE.json). The source, PDF, README, supplement and metadata agree on title, author, ORCID, date, unrestricted scope, the untouched variant, prior credit, extensive AI use and unrefereed status.

## Limits and disposition

The strongest independently verified result is the exact unrestricted no-prorepresentable-recipient theorem for the specified F4/F2 action, together with a consistent and reproducible authored package. There are no blockers and no required repairs of any severity in this pinned input. The remaining limits are explicitly disclosed: the component-prorepresentable variant is not resolved; finite programs are corroboration rather than infinite proofs; no proof assistant or human peer-review certificate exists; priority is bounded; only macOS/Python 3.14.6 was actually executed here; optimization/isolated flags are not a general security sandbox; and the historical permission harness was not replayed.

Completion of this assigned fresh whole-package review: **100%**. This verdict applies to the exact input hashes, not subsequent revisions or publication operations.
