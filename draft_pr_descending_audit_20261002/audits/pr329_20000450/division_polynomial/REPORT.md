# PR329 / problem20000450: independent division-polynomial audit

Verdict: **PASS within this mathematical family; no blocking mathematical finding.** This is an audit of the frozen one-turn candidate at head `96395a4f506af6a6045e3cd59afcba2db6b7e2e7`, not publication clearance or an external closure seal. The exact historical input is the twenty-one owned copies in `candidate/`, pinned by `CANDIDATE_INPUT_MANIFEST.json`. Geometry that identifies the entire plane normalization with the stated Weierstrass model is a prerequisite of this family's conclusion. I read its submitted argument and replayed its identities, but do not claim to have performed the separate geometry-family audit or read a sibling conclusion.

The strongest independently verified result is that, on every stated characteristic-zero nonsingular fiber of the displayed Weierstrass model, the candidate formulas give **all twenty-five geometric points of the fifth-torsion kernel**, with correct signs and no extra denominator exclusions. An independent generic chord/tangent computation produces every coefficient of the degree-ten residual polynomial. Exact resultants and the group-law argument below establish completeness and separability; finite-field enumeration is additional falsification evidence. The displayed twist transport, discriminants, modular rational identities and specialization field argument also withstand the checks below. The exact remaining procedural gap is root's full reading, independent replay and external closure. The remaining mathematical scope boundary is the separate proof that the original plane pencil has this normalization and origin; it is not an unsupported division-polynomial step hidden inside this verdict.

## Original target, assumptions and preserved independence

I inspected the original AIM Question17 and all four remarks on physical/printed page51, first as the supplied original image and then as independently extracted text and a render. The original asks to compute fifth torsion of the normalization of the regular-pentagon pencil. Its first remark says the five infinity points are among the fifth-torsion points. That five-point cyclic subgroup alone would not answer the question. I fixed the target to all twenty-five geometric points of a smooth genus-one normalization, with an explicit origin, field and parameter normalization. The later remarks motivate five-torsion torsors, a twist of the universal X_1(5) family with its marked point, and related pencils; they do not require an unconditional Tate–Shafarevich result or a solution for nonregular/star polygons. The stronger full-level X(5) cover is a separate input to the candidate computation. This interpretation and prospective independent chord mechanism were frozen in `SOURCE_ONLY_BASELINE.md` at 2026-10-04T08:46:23.807654Z before candidate exposure. [Original AIM problem list](https://www.aimath.org/WWN/qptsurface2/qptsurface2.pdf).

The operative assumptions are characteristic zero, K=Q(sqrt(5)), the explicit regular-pentagon coordinate and side-product scaling, and origin O=[0:1:0] on the normalization. For finite lambda the allowed fibers satisfy lambda not in {0,-5sqrt(5),-phi^5}, with phi=(1+sqrt(5))/2. Lambda infinity is not an elliptic fiber. A chart pole is not a singular fiber. I tested the allowed plane-cusp parameter, j=0 and j=1728 fibers, singular parameters, and characteristic five as distinct boundaries. Arithmetic field statements concern lambda in K; the generic statement concerns K(lambda). No claim that all twenty-five points are K-rational is assumed.

The first candidate assessment and independent closure plan were frozen at **2026-10-04T08:50:45.905098Z**, before inherited reviewer or status bodies. The initial read was complete TURN_1.md, FINAL_RESULT.md, SOURCE_THEORY.md and verify_turn1.py. The root pin manifest incidentally exposed the administrative `claimed_solved` label; this was disclosed and was not mathematical evidence. The native generic chord, finite-field and model results were produced before opening inherited scientific verdicts. The log records that opening at 2026-10-04T09:06:29.952711Z. I subsequently read all twenty-one attempt files completely, including inherited reports and manifests, treating them as claims to check. No raw imported earlier report, outside-attempt QUEUE body, sibling mechanics, or root scientific baseline was read. Ordinary Weierstrass mathematics was prior background; no unexpected prior PR329 knowledge arose.

## Independent group law and the marked points

For a general Weierstrass equation

    y^2+a1*x*y+a3*y = x^3+a2*x^2+a4*x+a6,

substitution of a line y=s*x+h gives a cubic with quadratic coefficient a2-s^2-a1*s. Thus the third intersection has abscissa s^2+a1*s-a2-x1-x2. Reflecting the third intersection gives

    x(P+Q)=s^2+a1*s-a2-x1-x2,
    y(P+Q)=-(s+a1)*x(P+Q)-h-a3,
    -(x,y)=(x,-y-a1*x-a3).

The tangent follows by implicit differentiation:

    s=(3*x^2+2*a2*x+a4-a1*y)/(2*y+a1*x+a3).

These formulas were derived before any imported division-polynomial recurrence was used. On

    D_beta: y^2+(1-beta)*x*y-beta*y=x^3-beta*x^2,

P=(0,0) has horizontal tangent. Its third intersection is (beta,0), whose reflection is 2P=(beta,beta^2). The line through P and 2P has slope beta, and the same law gives 3P=(beta,0)=-2P. Consequently 5P=O. P is nonzero, so its order is exactly five. Negation gives -P=(0,beta). For beta nonzero the four displayed points are distinct. This verifies the ordinate signs, rather than recognizing the Tate equation by name.

Completing the square gives v=y+((1-beta)*x-beta)/2 and

    4*v^2=T_beta(x)
    T_beta=4*x^3+(beta^2-6*beta+1)*x^2+2*(beta^2-beta)*x+beta^2.

Our finite-field implementation works directly with the uncompleted general Weierstrass equation and the derived law. It therefore does not merely repeat the candidate's completed-square multiplication routine.

## Generic derivation of the fifth polynomial

`independent_chord.py` works over Q(c2,c1,c0,x) with v^2=f=x^3+c2*x^2+c1*x+c0. It has no candidate imports. Write the doubled slope as v*f'/(2*f). Then

    x2=f*(f'/(2*f))^2-c2-2*x,
    v2/v=-1+(f'/(2*f))*(x-x2),
    slope(P+2P)/v=((v2/v)-1)/(x2-x),
    x3=f*(slope(P+2P)/v)^2-c2-x2-x.

The universal line-intersection Vieta identity and a direct doubled-curve identity check justify these expressions. The triple point lies on the cubic because the line already meets it at P and 2P and the Vieta root is the third intersection. Expanding a redundant huge rational expression for f(x3) is not needed for this deduction.

Set b2=4c2, b4=2c1, b6=4c0, b8=4c2*c0-c1^2. Direct extraction from these group-law expressions gives

    psi3 = 4*f*(x-x2)
         = 3*x^4+b2*x^3+3*b4*x^2+3*b6*x+b8,

    H6 = 16*f^2*(v2/v)
       = 2*x^6+b2*x^5+5*b4*x^4+10*b6*x^3+10*b8*x^2
         +(b2*b8-b4*b6)*x+b4*b8-b6^2,

    psi5 = 4*f*psi3^2*(x2-x3)
         = 16*f^2*H6-psi3^3.

Since psi2=2v and psi4=psi2*H6, the last expression is precisely psi4*psi2^3-psi3^3. This derives the fifth recursion from the chord computation instead of accepting the shipped recurrence as the result. The resulting polynomial has degree twelve and leading coefficient five. Specializing c2=(beta^2-6beta+1)/4, c1=(beta^2-beta)/2 and c0=beta^2/4, exact polynomial division gives

    psi5=x*(x-beta)*R_beta(x).

Every one of the eleven displayed coefficients of R_beta agrees individually with this independently obtained quotient, including its leading coefficient five. The native record prints both the generic and specialized coefficient lists. The optional two quintic factors displayed in the candidate verifier were separately checked in `independent_quintic_factors.py` against this own chord-derived quotient: 5*Rplus*Rminus=R_beta. That check uses our recorded independently derived coefficients, not a candidate import. A deliberately altered quintic coefficient fails the identity.

## Completeness, separability and all twenty-five points

The exact Tate discriminant is Delta=beta^5*(beta^2-11beta-1). The generic native algebra verifies

    Res_x(psi5,T_beta)=Delta^6,
    Res_x(psi5,psi3)=Delta^8,
    R_beta(0)=5*beta^8,
    R_beta(beta)=5*beta^12.

On every allowed fiber these are nonzero. A root of psi5 is therefore neither a branch point v=0 nor a triple-law denominator x2=x. At such a root the chord identity forces x(2P)=x(3P). Two points of the same abscissa on this completed cubic are either equal or opposite. Equality 2P=3P would imply P=O, impossible for a finite point. Hence 3P=-2P and 5P=O. Conversely a nonzero fifth-torsion point is neither second nor third torsion, so the same law is defined and forces the displayed psi5 to vanish. Thus its roots describe exactly the nonzero kernel, not a larger algebraic set.

For a nonsingular elliptic curve in characteristic zero, [5] has degree25 and is separable. Translations identify its local behavior at each point, so its kernel consists of twenty-five distinct geometric points. This standard theorem was independently checked in the primary multiplication-map derivation, not inferred from our finite samples. Pairing the twenty-four nonzero points by negation gives twelve distinct abscissae because a nonzero point of order five cannot have order two. The independently derived degree-twelve polynomial therefore has twelve simple roots. Removing x=0 and x=beta leaves ten simple R_beta roots, disjoint from the marked subgroup. For each root the two ordinates are

    y=(-( (1-beta)*x-beta ) +/- sqrt(T_beta(x)))/2.

The resultant shows T_beta(x) is nonzero, so the two signs are distinct. Together these are twenty further points; adding the four marked points and O gives exactly twenty-five. Every nonzero point has exact order five. There is no rationality assertion about all these coordinates. The complete division-polynomial/group-law degree and separability argument is in sections5.5–5.6 of the primary [Sutherland lecture notes, dated September26,2023](https://math.mit.edu/classes/18.783/2023/LectureNotes5.pdf).

A useful independent universal squarefreeness certificate is

    disc_x(psi5)=5^11*Delta^22.

Here is the proof of the exponent, which the code correctly does not claim to infer from one sample. Translate to the short equation v^2=x^3+A*x+B. With weights wt(x)=2, wt(A)=4 and wt(B)=6, psi5 has weight24 and degree12, so its discriminant has weight264. Over C, the completeness/separability argument above says this discriminant has no zeros off the irreducible locus 4A^3+27B^2=0. By factorization in C[A,B], every nonconstant irreducible factor is this one, hence the discriminant is a constant times Delta^e. Delta has weight12, giving e=22. Exact integer evaluation at A=0,B=1, where Delta=-432, gives the constant5^11; the native code verifies that equality. Translating x to remove c2 does not change root differences, so the identity holds for the general monic cubic as well. This certificate is a symbolic deduction plus an exact constant calculation, not finite-field extrapolation.

## Model, denominators and special fibers

`independent_model.py` independently expands the candidate's full Tate-to-Weierstrass transport and compares all four cubic coefficients. Put r=sqrt(5), d=5+2r, delta^2=d, alpha=1-r/5, gamma=2r/5,

    beta=(11-5r)*lambda/(2*(lambda+5r)),
    k=4*(lambda+5r)/r, q=d*k^2,
    xi=q*(x-beta), eta=(k*delta)^3*v.

This is an actual equation isomorphism over K(delta), preserving O, rather than a j-invariant coincidence. In particular (k*delta)^6=q^3 gives the correct quadratic-twist scale. Replacing d with its conjugate deliberately fails the transport identity. The independently computed discriminant is

    Delta_W=2^24*(161-72r)*lambda^5*(lambda+5r)^5*(lambda+phi^5)
           =q^6*Delta_beta.

Thus there are exactly the three listed finite nonsingular exceptions for this model. The beta limits map lambda=-phi^5 and lambda infinity to the two quadratic Tate cusp roots; beta=0 occurs at lambda=0 and the parameter itself has a pole at lambda=-5r. No additional j=0 or j=1728 exclusions occur: exact gcds of c4 or c6 with Delta_beta are constants, and the torsion proof did not require distinct automorphism-free unmarked j-values.

For the inverse plane chart the candidate uses s=a3/xi, z=s-alpha*lambda, t=z-5-2r, where a3=(-112+48r)*lambda^2*(lambda+5r)/5. Substituting xi=q(x-beta), our exact identities are

    z+gamma*lambda=(gamma-alpha)*lambda*x/(x-beta),
    a+4r*t=4r*(z+gamma*lambda), a=40+20r+8lambda.

The poles xi=0 or z+gamma*lambda=0 therefore occur only at Tate x=beta or x=0, respectively. These are already in the known cyclic subgroup; R_beta has neither abscissa. Since q, a3, lambda and gamma-alpha are nonzero on every allowed fiber, all twenty remaining points have well-defined affine inverse coordinates in the candidate formulas. No extra specialization or denominator exception is being suppressed. The inverse image of z=0 on the allowed plane-cusp parameter lambda=-(25+10r)/4 is a two-torsion branch point; it cannot be one of these fifth-torsion points. The model discriminant at that parameter is nonzero. The separate normalization extension is needed to identify the marked subgroup with the five infinity branches; I do not conflate affine chart failure with failure of torsion or ellipticity.

The candidate's complete coefficient reductions from its line product to the conic/quartic and its plane-to-model identities were read and replayed in the owned copy of verify_turn1.py. Those identities are compatible with the independently checked model and denominators. The global irreducibility/normalization argument remains the stated separate geometry prerequisite of this family, rather than an independently re-certified geometry conclusion here.

## Full division field and arithmetic specializations

The degree-ten polynomial already computes the full geometric points. The stronger field claims require the full-level moduli input, not just that coordinate polynomial or finite-field tests. I independently retrieved the primary Fisher paper and read Lemma1.1, the Tate equation and discriminant on printed172–173, and complete Lemma3.4 and its proof on printed194. Original page images172 and194 were also inspected. I do not claim a complete reading of the entire paper. Its Lemma3.4 identifies the full-level cover C_(tau^5) with the Tate parameter tau*f(tau)/g(tau), preserving the marked order-five embedding. Lemma1.1 supplies uniqueness and absence of a nontrivial automorphism of a curve with such a marked point. The relevant result is this cover identification, not the paper's rational-field rank theorem. [Fisher, JEMS3(2001), primary paper](https://ems.press/content/serial-article-files/31488).

The candidate's elementary identities were checked independently, including both involutions:

    epsilon(tau)=(phi*tau+1)/(tau-phi),
    iota(v)=(phi^5*v+1)/(v-phi^5),
    tau*f(tau)/g(tau)=iota(epsilon(tau)^5),
    iota(beta)=-1/(lambda+phi^5).

Over a field containing zeta5, a fixed nonzero marked P and a fixed Weil pairing identify the fine full-level fiber with the five choices Q+jP. There is no residual pointed automorphism. It is a finite etale degree-five cover away from the Tate cusps. The Fisher cover identification and these identities consequently identify its field with adjoining theta, theta^5=lambda+phi^5 (the intervening -1 power/inversion causes no field change). This fiber is the full coordinate field of a compatible basis P,Q. This argument applies to every allowed specialization, including j=0 and1728: both covers are the normalization with the same function-field extension of the smooth cusp-complement base, so a generic equality of covers extends there. It is not a claim that a rational-function identity alone proves the moduli assertion, or that a degree-five polynomial is always irreducible upon specialization.

The twist adds delta. In fact the coordinates of the image of marked P=(0,0) are

    xi_P=-q*beta in K,
    eta_P=-k^3*d*delta*beta/2.

Its nonzero K coefficient shows delta belongs to the full W-torsion field. The Weil pairing shows zeta5 belongs as well. The fine-cover argument supplies the compatible basis over K(zeta5,theta), and the twist transfers it over K(delta,zeta5,theta), with the reverse containment from the same basis-field description. Thus

    K(E_lambda[5])=K(delta,zeta5,theta), theta^5=lambda+phi^5.

For the generic K(lambda) statement, lambda+phi^5 has valuation one at its simple zero and is not a fifth power. For a specialized lambda in K, set a=lambda+phi^5 in K^*. The two quadratic extensions K(delta) and K(zeta5) are distinct: the former is real (d has norm5 and is not a square in K), the latter is imaginary. Their composite L has degree4 over K. An element a of K that is a fifth power in L is already one in K: if u^5=a, N_(L/K)(u)^5=a^4, so (a/N(u))^5=a. Conversely a fifth power in K is one in L. Kummer theory over L therefore gives degree1 or5, leading to total degree4 or20 exactly as stated. For the non-power case K(zeta5,theta)/K is D10, with rotation theta->zeta5*theta and complex conjugation inverting it. Its unique quadratic subfield is K(zeta5), so adjoining the distinct K(delta) produces D10 x C2. When a is a fifth power the field is the biquadratic L. No irreducibility assumption on every special fiber is made.

The independent delta involution acts on W-torsion by -I, hence there is no nonzero K-rational fifth torsion. Over the real field K(delta), the marked subgroup exists; E(R)[5] is cyclic of order5 because the real Lie group has one or two components and identity component a circle. Thus that is the entire K(delta)-rational fifth-torsion subgroup. For the claimed generic matrices, choose P as first vector and a complex-conjugation -1 eigenvector as second; conjugation is diag(1,-1), the fivefold deck generator is a nontrivial upper transvection and can be normalized by its generator, and the delta involution is -I. These choices account for the basis dependence of the displayed matrices. This supports the candidate arithmetic statements conditional on the proved identification of E_lambda with the displayed W model.

## Native falsification and reproducibility evidence

All results below are genuine child-process executions captured by `native_capture.py`, with UTC start/end, actual argv, actual resolved executable, current code pins at execution, exit code, full stdout and stderr. They are not self-reported generated JSON substituted for exit evidence. Symbolic native runs used the permitted local dependency runtime, resolving to Python3.14.6 with SymPy1.14.0. The finite program requires only the standard library and used system Python3.14.6 directly. No geometry mechanics were read to use the dependency runtime. Empty stderr files have SHA256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

| Native record stem | Actual exit | stdout bytes / SHA256 | Role |
|---|---:|---|---|
| independent_generic_chord_final | 0 | 3363 / `8a559115cea45c0c7943433e770c6f8d6a206e418b23f890658bc2639a5876a4` | Generic derivation, all eleven coefficients, exact resultants and boundary controls |
| independent_finite_controls | 0 | 4471 / `16769d0ceb89c88b4ad8dd352328e29b7bf3a9137bc0377ff0c7be816056f7a8` | Direct general-Weierstrass enumeration, independent of shipped multiplication |
| independent_model_identities_final | 0 | 1297 / `68be1db7ca03ffcad2ca9c7a9cdeb664aa4a992cb45b5b1ac41e0a38833a86d9` | Full transport, discriminants, all poles and modular rational identities |
| independent_quintic_factor_final | 0 | 201 / `626dd069dc6c35b9c324ef457c387ab1d3971090ddc7f3187834d652347e1fe5` | Optional two quintic factors against the own chord result |
| candidate_verifier_owned | 0 | 421 / `a87be352f021c6826fecf2ddb7bcae9703be0b8ba0ee39e7af2990328181d07f` | Exact historical verifier run on owned candidate only |

I read all these complete stdout/stderr bodies. The candidate run agrees byte-for-byte with its check JSON. It reports88918 assertions,388 finite fibers,30012 enumerated affine points,28460 inverse plane checks,68 full fifth-torsion and320 cyclic fibers. Those counts are controls, not substitutes for the universal proofs.

Our independent finite program enumerates138 nonsingular beta fibers and6112 affine points over primes7,11,31,41,61, testing fifth multiplication on every point. The polynomial and direct kernel agree in every case. It checks all marked-point signs and includes both cyclic and full geometric rational kernels, plus j=0 and1728 examples. The full-kernel fiber counts are respectively0,0,4,6,10. Wrong ordinate constants are rejected in all138 fibers; a changed R coefficient in65 fibers; deleting the known subgroup factor or deleting one ordinate branch in all138. The generic check rejects a coefficient mutant, detects repeated roots at singular beta=0, and detects that characteristic five drops psi5's degree to10. The nonsingular characteristic-five control has only five rational kernel points and is explicitly not used to assert twenty-five distinct geometric points. No finite sample is presented as an all-fiber proof.

Three unsuccessful historical audit runs remain preserved, with original code snapshots and complete native records:

1. `independent_generic_chord` was deliberately terminated by SIGTERM after a redundant expensive rational triple-membership expansion. Actual child exit was-15, with zero-byte stdout/stderr. Original body is preserved as `independent_chord_initial_slow.py`. The later Vieta proof removes the redundant calculation and supplies its mathematical justification.
2. `independent_generic_chord_optimized` exited1 because my prospective check incorrectly expected R(beta)=5beta^10. Actual algebra gave5beta^12; hand summation of all eleven coefficients confirmed it before inherited reviewer exposure. Original body is `independent_chord_expectation_bug.py`; stderr is849 bytes, SHA `e88b4bf8c84dedbbf81eb6f23e1ca73702b7fddfa14e52e9dad84be78ce9e998`. Only the reviewer expectation was corrected, with no candidate edit.
3. `independent_model_identities` exited1 because an exact-zero specialization was not recognized by cancel with a quadratic extension. The failed body is `independent_model_initial_zero_test.py`; stderr is1388 bytes, SHA `1c34fb4f77ad84e34154990348d59aa373f40d59c475c495cf2e911e352b3dde`. An exact simplify fallback recognized the same zero and the full rerun passed. This is an audit simplification limitation, not a candidate counterexample.

`HISTORICAL_CODE_ALIASES.json` binds the code hashes recorded at those original paths to the byte-identical preserved historical bodies. The current three core programs have remained unchanged after root's read request. These failures are neither silently overwritten nor mislabeled native successes.

## Artifact consistency, attribution and disposition

The owned twenty-one candidate file bodies match the released snapshot pins, including modes0644 and independently calculated Git-blob SHA1 (a hash calculation, with no Git mutation). The inner AUTHOR_MANIFEST binds eleven payload files and excludes itself; PUBLICATION_MANIFEST binds twenty and excludes itself; REVIEW_MANIFEST binds five and excludes itself. Their counts and pins are checked by the read-only verifier. The recorded original check JSON and our native replay agree. Primary input/read scopes and all exposure stages are explicit in `PRIMARY_INPUTS.json` and `READ_LEDGER.json`. No private original primary PDF is part of the public replay payload.

The candidate credits Tate normal form, Fisher's full-level cover and the standard division-polynomial recurrence, and acknowledges the imported partial computation. It does not claim first historical priority, a new abstract modular theorem, a Sha/local-condition result or the nonregular-polygon variants. Fisher's version/pages are consistent with the independently retrieved2001 paper. The completed degree-ten coordinate expansion and explicit model-specific field simplification can be stated as this computation without erasing those inputs. I did not independently rerun the bounded historical search recorded in SOURCE_GATE and do not promote it to a universal novelty certificate. The submitted AI-assisted review disclosure does not purport to be human peer review or a formal proof certificate. This audit likewise supplies neither.

No actionable blocking issue was found in the division-polynomial/group-law/model-transport/field-specialization scope. An optional exposition improvement is to include the exact resultants and chart-pole identities above in the main manuscript, making its all-fiber denominator and separability assertions easier to inspect. This is not a repair required for the mathematics verified here. No candidate body was edited.

Run `verify_review.py --scope public --python /path/to/SymPy-python` for the public mathematical records/candidate integrity and all five current native computations, or `--scope full` for the entire owned historical namespace, private primary pins, native receipt streams and historical code bodies as well. Both are read-only. Replay compares complete mathematical JSON, allowing only the explicit interpreter provenance field to differ in the generic output; exit0, empty stderr and SymPy1.14.0 are checked. This is deliberate interpreter portability, not a discarded mathematical discrepancy. Native stdout hashes remain the exact historical bodies above. The full verifier binds historical candidate copies, not live originals that another authorized action might later repair. It cannot replace scientific reading or root's external seal.

All review payloads are held unsealed for root reading and replay. `REVIEW_RESULT.json` retains family PASS, publication_clearance=false and external_closure_pending=true. No publishing, contacting individuals, shared Git/index/branch/PR mutation or primary redistribution occurred, and all PR344 files were left unchanged.
