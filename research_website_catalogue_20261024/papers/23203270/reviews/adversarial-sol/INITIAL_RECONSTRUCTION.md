# Original-only adversarial reconstruction: record 23203270

Phase: INITIAL. This is a sealed original-only reconstruction and test record, not a final review or promotion decision. No packaged audit, opinion, legacy review, support certificate, native program result, Lean source, or imported primary mathematical source was read before this reconstruction. The only mathematical source read was the complete controlling manuscript, in its original TeX, full outer-PDF text, and all six freshly rendered native page images. Mathematical deductions below were made by hand; no native mathematical code was executed.

Initial-phase objective completion estimate: 100% when sealed. Estimate toward a complete scientific assessment, including independent checking of essential imported input: 45%. The latter remains limited by the exact deferred interfaces below.

## Exact target and claim boundaries

The manuscript defines P=C[p,s,u,F,J], x=s^2+u^3+p^2 F, H=x^2 F-(1+2sx)J-p^2 J^2-pu, and A=P/(H). Its main claim is that A is smooth and integral of transcendence degree four; explicit C-algebra homomorphisms i:A -> B=C[p,s,u,m,e] and r:B -> A split with ri=1; their explicitly specified composite rho=ir is idempotent; and the image is not a polynomial C-algebra.

These are distinct targets. The first, maps, splitting, and idempotence admit direct checks from this manuscript. The final nonpolynomiality assertion depends on the exact upstream theorem for this exact complex algebra. A one-variable polynomial cylinder does not alone establish nonpolynomiality. Conversely nonpolynomiality alone does not provide the displayed explicit maps.

All algebra maps must be unital C-algebra maps. The ambient polynomial ring has five generators; the image has transcendence degree four. No assertion for arbitrary base fields, positive characteristic, real algebras, or ambient dimension four follows merely by relabeling. A result over another field, or for an algebra merely similar to A, would not fill the inherited-input gap. Neither an isomorphism after inverting p nor a stable isomorphism in more variables suffices for the displayed global five-variable claim.

The original native API has no metadata.version field. Its metadata.relations.version has index 0 and is_last=true; the native HTML displays "Version v1". These facts are recorded separately rather than substituting the HTML label for an absent API field. The complete native Description explicitly attributes cancellation, stabilization and nonpolynomiality to OpenAI, disclaims an ambient-four result, discloses the unreproduced full kernel build, and disclaims formal verification of the follow-on theorem. These disclosures are part of the claim scope.

## Independent hand reconstruction of the local algebra

### Dimension and domain; no use of nonpolynomiality

After inverting p, introduce y=s+x(x-u^3), z=sx+p^2 J. The inverse formulas are s=y-x(x-u^3), F=p^(-2)(x-s^2-u^3), J=p^(-2)(z-sx). Direct expansion gives

    xy-z(z+1)=p^2[x^2 F-(1+2sx)J-p^2 J^2],
    H=p^(-2)[xy-z(z+1)]-pu.

Thus over C[p,p^(-1)], H is linear in u with unit coefficient -p, in the independent coordinates x,y,z,u. Its quotient is C[p,p^(-1),x,y,z], a domain of transcendence degree four over C. The residue H mod p is the nonzero polynomial L=x0^2 F-(1+2s x0)J, x0=s^2+u^3. If H factored in the UFD P, one factor would be a unit after localization; such a factor in P is a constant times a nonnegative power of p. Since p does not divide H, that factor is a constant. Hence H is irreducible and prime. Also p remains nonzero in A because the displayed nonzero localization exists. This closes the p-torsion issue used below without presupposing a cylinder or nonpolynomiality theorem.

### The automorphism and quotient direction

Write D=((u-p^2w)^3-u^3)/p^2=-3u^2w+3p^2uw^2-p^4w^3, where the right side is the definition and contains no denominator. Under the manuscript's Phi substitution,

    s' = s+p^2 xD, u'=u-p^2w,
    F'=F-(1+2sx)D-p^2x^2D^2, J'=J-x^2D,

the square terms cancel to give s'^2+u'^3+p^2F'=x. Then y'=y and z'=z. Inverting p therefore gives Phi(H)=H+p^3w. Both sides are polynomials in the original domain P[w], so this identity holds there before any quotient. Replacing w by -w reverses u's translation and then fixes x,y,z; it reverses all generators after localization and hence before localization. This gives a global polynomial inverse, rather than only a birational inverse.

The quotient-map orientation is important: the image of the source relation H under Phi is the target relation H+p^3w. Therefore Phi induces A[w] -> T=P[w]/(H+p^3w), with inverse induced by Phi^(-1). This uses neither the later q,g inverse argument nor the imported nonpolynomiality. T is consequently a domain with nonzero p by the preceding domain argument.

The derivation assertion also passes this test: in localized coordinates Delta=-p^2 partial_u, while its displayed values lie in P and preserve P. Every localized polynomial is killed by a high enough power of this derivation, so restriction is locally nilpotent. This implication is valid because localization here is an injective embedding of domains.

### The determinant-one change and certificates

The (F,J) -> (L,M) matrix has determinant

    4s^2x0^2+(1+2s x0)(1-2s x0)=1.

Its inverse is exactly f(L)=4s^2L+(1+2s x0)M and j(L)=(2s x0-1)L+x0^2 M. The displayed q1,q2 are the coefficients of Q(L)-Q(0), where Q=2x0 f^2-2sfj-j^2. In particular its constant coefficient is

    Q(0)/M^2 = 2x0(1+2s x0)^2-2s(1+2s x0)x0^2-x0^4
               =2x0+6s x0^2+4s^2x0^3-x0^4.

This quotient notation is just a coefficient calculation, not division required in any map. Expanding x=x0+p^2F gives exactly H(L)=L-pu+p^2Q(L)+p^4 f(L)^3.

Let R=H(L)+p^3w and h=u-pQ(L)-p^3f(L)^3-p^2w. Then the short exact identity R=L-ph is a useful independent check. With L*=pu-p^2C and e0=-w-pf(L)^3-Q1(L)h,

    p^3 e0-(L-L*)
      =-R+p^2(Q-C)-p^3Q1 h
      =-R+p^2 Q1(L-ph)
      =(p^2Q1-1)R.

No cancellation or inversion of p enters this certificate. Substituting L*=p(u-pC) into H(L) similarly gives H(L*)=p^3[(u-pC)Q1(L*)+pf(L*)^3].

### Both inverse compositions, all generators

In B, ell=pu-p^2C+p^3e=p(u-pC+p^2e), and W=-e-(u-pC+p^2e)Q1(ell)-pf(ell)^3. Expansion using Q=C+ell Q1 gives H(ell)+p^3W=0. Hence g:T -> B is well-defined. The source of q is free, so its specified generator images define q:B -> T without a relation to check.

Substitution in h gives h(ell,W)=u-pC+p^2e, because the remaining Q1 coefficient is -p ell+p^2(u-pC+p^2e)=0. Thus e0(ell,W)=e. The inverse linear change recovers M; consequently gq fixes p,s,u,m,e individually, without invoking a point sample.

Conversely, the certificate in T gives L=L*+p^3e0, so qg fixes L, M, p,s,u and hence F,J. Applying the defining relation to w and qg(w) gives p^3(qg(w)-w)=0. Since T is a domain with p nonzero by the earlier independent Phi/domain argument, qg(w)=w. This is not circular: the domain proof and Phi quotient isomorphism did not use qg=1. It checks the last generator, which cannot be inferred just from recovery of L,M. Thus the isomorphism here is an actual unlocalized polynomial algebra isomorphism A[w] -> B.

### Split maps, formula evaluation, and spectra

Set theta=g Phi_bar. Coefficient inclusion jmath and evaluation epsilon at w=0 satisfy epsilon jmath=1_A independently of any polynomiality assertion. Therefore i=theta jmath and r=epsilon theta^(-1) satisfy ri=1_A. Each correction in Phi^(-1) contains w, so evaluation recovers r(p,s,u,m,e)=(p,s,u,M,E_A) with precisely the manuscript's E_A. Applying g to Phi's generator images gives its X,D,S,U,Fcal,Jcal inclusion formulas. Well-definedness of i follows from g(Phi(H))=g(H+p^3w)=0.

The five rho components are exactly i applied to the five values of r. Consequently rho^2=i(ri)r=ir. The ring image is i(A), and ker(ir)=ker r because i is injective. On schemes pi=Spec(i) and sigma=Spec(r) obey pi sigma=1, so the affine-space map is sigma pi. Its scheme-theoretic image has coordinate ring B/ker r, isomorphic to A. This direction check avoids reversing the section and retraction.

An additional checkable consequence of these maps is ker r=(W): theta carries the evaluation kernel (w) in A[w] to (theta(w))=(W) in B. This is an original-only deduction, not an independent proof that the quotient is nonpolynomial.

### Smoothness, zero parameter, and other fibers

At p=0, H=L and the determinant-one change gives A/(p)=C[s,u,M]. The H partial derivatives with respect to F,J are x0^2 and -(1+2s x0); their coefficients satisfy the displayed unit identity, so they have no common zero. The open set p nonzero is a Laurent polynomial algebra. The smoothness argument therefore covers every point and does not omit x0=0, s=0, or u=0.

At p=0, ell=0, f=(1+2s x0)m, j=x0^2m, W=-e-u kappa m, D=-3u^2W, S=s,U=u. Applying the linear inverse to Fcal,Jcal gives M'=m-D=m+3u^2W and L'=0. Then E'=-u kappa M'. Thus rho(0,s,u,m,e)=(0,s,u,M',-u kappa M'), and W at the output is zero. The second application fixes every output component. This argument includes m=0 and kappa=0 because kappa is the coefficient polynomial, never q1 divided in a ring. At u=0 the output is simply (0,s,0,m,0), also consistent with idempotence.

For a nonzero complex constant a, A/(p-a)=C[x,y,z] using u=a^(-3)[xy-z(z+1)]. Thus both generic and zero parameter fibers are polynomial threefolds. This does not prove that the total A is a polynomial fourfold. It does show why restricting this example to p=0 cannot establish a negative result in ambient dimension four: that restricted image is polynomial of transcendence degree three.

## Independent falsification tests on the inherited mechanism as stated in the original

The following checks use only the formulas printed in the controlling manuscript. They do not replace an examination of the imported proof.

1. **Dimensions.** R=C[x,y,z,u]/(xy-z(z+1)) has dimension three, and adjoining tau before modification has dimension four. The determinant algebra S=C[a,d,b,c,u]/(ac-bd-1) has dimension four. These counts fit a one-dimensional torus-bundle transfer; no dimension collapse itself supplies nonpolynomiality.

2. **Bundle map and principalization formula.** The substitution (x,y,z)=(ab,dc,db) respects xy=z(z+1) because ac=bd+1. Write t=x-u^3, s_R=dc-abt, and v=a^2t-d^2. Then exact division-free identities are

       z-s_R x=b^2v,
       x-s_R^2-u^3=(c^2-b^2t)v.

   The coefficients generate the unit ideal: (c^2-b^2t,b^2)=(c^2,b^2)=S because (b,c)=S follows from ac-bd=1. Therefore the stated pullback of I really is (v). This tests the boundary charts a=0 and d=0 as well; neither permits silently dividing by a globally. It does not establish a lift of an arbitrary locally nilpotent derivation.

3. **Weights.** For weights (1,1,-1,-1,0), each term of v has degree two and the determinant relation has degree zero. For auxiliary weights (0,3,-3,0,2), the highest part of v is -(d^2+a^2u^3), of degree six, while a^3b has degree -3. Thus the indicated highest-part equation is dimensionally and grading consistent, provided the required homogeneous locally nilpotent E exists and extraction preserves the relevant hypotheses.

4. **A direct rigidity check.** Suppose, as an exact conditional hypothesis, D is a locally nilpotent derivation of S and D^2(N)=0 for N=d^2+a^2u^3. Work in Frac(S)[T] and put A(T)=exp(TD)a, Dd(T)=exp(TD)d, U(T)=exp(TD)u. Then Dd(T)^2+A(T)^2U(T)^3=N+T D(N) is a nonzero polynomial of degree at most one. The determinant identity implies gcd(A,Dd)=1. A common factor of Dd and U would have its square divide that nonzero linear polynomial, so gcd(Dd,U)=1. Hence the three terms in this polynomial sum are pairwise coprime.

   The polynomial abc inequality in characteristic zero gives, writing alpha=deg A, delta=deg Dd, nu=deg U,

       2delta <= delta+alpha+nu,
       2alpha+3nu <= delta+alpha+nu.

   These force nu=0 and delta=alpha if any term is nonconstant. If alpha=delta>0, leading coefficients would make -u^3 a square in Frac(S), impossible: Frac(S)=C(a,d,b)(u), and its valuation at u has odd value three on -u^3. Thus alpha=delta=nu=0 and D fixes a,d,u. If all terms are constant the same conclusion holds directly. The abc inequality used here follows by applying the derivative Wronskian to a coprime sum: the product of each term divided by its radical divides the Wronskian, while its degree is at most the sum of the degrees of the two selected terms minus one. A zero Wronskian in characteristic zero would force the coprime summands to be constant, already the separate case. This records the precise standard algebraic interface rather than treating an orbit sample as proof.

5. **The shift conclusion once rigidity holds.** A nonzero LND of S fixing a,d,u has Db=a h and Dc=d h with h in C[a,d,u]. Indeed on the a-chart S_a=C[a,a^(-1),d,u,b], local nilpotence over C(a,d,u)[b] forces Db to be constant in b. The d-chart gives the corresponding statement for Dc. Their common rational coefficient is polynomial because C[a,a^(-1),d,u] intersect C[a,d,d^(-1),u] in C[a,d,u], and a Dc=d Db forces the indicated divisibilities. A homogeneous such derivation has first-weight shift deg(h)+2>=2. Thus the final positive-shift contradiction does follow from a nonzero homogeneous E of nonpositive first-weight shift and its stated highest-part hypotheses. This conditional check does not produce that E.

These computations did not uncover a local algebra counterexample. That observation is limited to the displayed calculations; it does not validate the unexamined imported theorem or its central transfer. In particular a bare assertion that polynomiality of A yields the required E transfers the central difficulty to an unsupported implication. That route remains deferred until the exact imported argument is opened after authorization.

## Exact deferred imported interfaces and gaps

The local cylinder and retract reconstruction above does not require an imported stabilization theorem. The nonpolynomiality part requires an independently supported statement that this exact A over C is not C^[4], with no additional genericity, real-form, equivariance, grading-preserving-isomorphism, localization, or stable-only qualifier. The exact pinned identity is the manuscript's OpenAI source commit adc7f1241b42e322a6451854ab7e4b4c146bf78a and its claimed Theorem 1.1/Sections 3-6. This is an interface description from the original citation, not authentication or reading of that imported source.

To test the mechanism rather than trust its abstract, the following are necessary separately:

- An exact filtration/valuation and comparison identifying the relevant degeneration with G=R[tau,I/tau^2]. The notation alone does not prove an equality of associated graded rings, finite generation, smoothness, saturation, or that a polynomiality assumption passes to the desired derivation statement.
- A justified implication from an arbitrary C-algebra isomorphism A=C^[4] to a nonzero homogeneous LND of G with the specified positive-degree invariant. A derivation respecting a preselected presentation cannot simply be assumed to exist because a ring is polynomial.
- The bundle/line-bundle lift, including extension across all determinant charts, its preservation of local nilpotence and nonzeroness, normalization denominators, and the exact way the invariant supplies E^2(v)=0 and a nonpositive first-weight shift. The principalization identity alone does not imply these lifting properties.
- The highest-part extraction must preserve nonzero local nilpotence and the first-weight sign, and must actually yield E'^2(N)=0. The grading arithmetic checked above establishes only compatibility, not the preceding existence hypothesis.
- The final rigidity can be checked using the conditional derivation argument above, but its application requires the exact E furnished by the preceding interfaces. A false lift, an uncontrolled shift, or a vanished highest part would leave the central gap open despite correct terminal rigidity.

The historical attribution and novelty bounds are separate from the algebra. Exact statements from Costa, Nagamine, the characteristic-zero transcendence-degree-two result, and the dated Chakraborty-Pal source would be needed to verify the history. The original already limits its novelty to explicit transport for this example and describes its search as bounded evidence. No original-only calculation can independently establish global priority or a public disclosure date from a manuscript date. Formal statement matching and kernel completeness require their own later source inspection; the original expressly does not claim a reproduced full build.

## Attempted counterexample families and stopping rule

The attempts covered wrong base field and dimensional transfer; stable versus actual polynomiality; generic-local versus global maps; p-torsion and irreducibility; missing generator w in the inverse; reversed algebra/scheme directions; hidden divisions by p or m; p=0, u=0, x0=0, m=0 and zero coefficient kappa; polynomial special fibers versus a polynomial total space; the determinant charts; grading signs; and the conditional orbit-polynomial rigidity. Each mechanism, evidence, and exact gap is stated above. No package result was used as evidence.

The strongest result supported by this INITIAL reconstruction is the original-only hand derivation of the smooth integral algebra, explicit actual cylinder isomorphism, split maps, idempotent, and stated fibers, together with precise conditional checks on parts of the inherited mechanism. The exact outstanding scientific gap is independent verification of the imported nonpolynomiality input, particularly its transfer to the required derivation; priority and formal scope are also unverified. This is a record of evidence and gaps, with no final verdict or new promotion.

INITIAL stopping rule: after creation of INITIAL_MANIFEST.json and INITIAL_SEAL.json, make no further mathematical reading, execution, or assessment until the root checkpoint and an explicit RESUME. All mechanisms and assessments remain withheld from root messages until that checkpoint. No external individual was contacted, and no outreach was prepared.
