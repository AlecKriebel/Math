# Mixed mock forms and modular-function equations: scope audit and obstructions

Author-written mathematical audit, 2026-10-21. Row 1897, ID 20000726; exact-question duplicate ID 20002515. No publication or queue edits. This report does not claim a full resolution of AIM problem 5.2 or novelty for existing examples.

## Question and verdict

The recovered exact question asks whether mixed mock modular forms satisfy differential equations with respect to a modular function. The legacy page was not independently fetched successfully in the recovery pass. A scalar homogeneous linear equation over C(t), a nonlinear differential-algebraic relation, a modular linear differential equation in tau, and an equation for a nonholomorphic completion are different requests. Raw forms and weight-zero normalizations are different unknowns.

Verdict: partial result with a rigorous obstruction. In the negative-integral-weight Bol class, a nonconstant periodic raw mock holomorphic part cannot satisfy a scalar linear ODE over any modular-function field. Its suitable weight-zero normalization can satisfy one. Thus a blanket raw linear assertion is false in any convention admitting this class, while a normalized or nonlinear assertion is not refuted. The original broad question remains under-specified; positive/half-integral mock weight and higher-depth classes are not settled here.

Notation: D=(2 pi i)^(-1)d/dtau, delta=d/dt, Delta=eta^24, j=E4^3/Delta. All branch arguments concern analytic germs on inverse modular-function charts. Coefficients called rational have field C(t), not an unrestricted field depending on the target function.

## Approach 1: audit the existing explicit weight-zero example

Guerzhoy defines the meromorphic primitive h by Dh=eta^20/E4^2 and h(i infinity)=0; E4 h is his holomorphic mixed mock solution. Ramanujan identities give Dj=−j E6/E4, hence h_j=−eta^20/(j E4 E6). Using eta^120=Delta^5 and E6^2=E4^3(j−1728)/j yields

(h_j)^6=1/[j^8(j−1728)^3],

h_jj+[4/(3j)+1/(2(j−1728))]h_j=0.

This is an exact re-verification of the existing result, not a new example. At infinity h~(6/5)j^(−5/6); its derivative has sixth-root branching. E4 h is NOT the unknown of this order-two equation. For J=j/1728 the constants change.

## Approach 2: finite-dimensional descent with the missing cusp argument supplied

Assume a meromorphic vector-valued form F of integral weight w>=0 on a finite-index subgroup Gamma, with r components, an actual finite-dimensional representation rho, and controlled cusp expansions: after a finite cusp cover these are finite sums of powers of log q times Laurent series with finite principal parts. The same control is assumed at every cusp. No assertion of finite-image monodromy is made.

Set G=F tensor (tau,1)^(symmetric w). Then G has r(w+1) components and transforms by constant matrices rho tensor Sym^w. Every coordinate of F is a coordinate of G. Choose a basis y_1,...,y_s of the C-span of the components; s<=r(w+1). Their Wronskian in delta is not identically zero, and its Cramer quotients give the unique monic order-s equation annihilating all y_i. Constant monodromy makes these quotients Gamma invariant. The Wronskian and each numerator have the same determinant-character transformation law.

Here is the essential cusp step. On a finite cover where cusp monodromy is unipotent, determinant character is 1. The Wronskian and numerators are invariant under the cusp deck transformation and have at most polynomial/logarithmic growth because of their stipulated expansions and their derivatives. A single-valued holomorphic punctured-disc function bounded by |q|^(−N)(1+|log|q||)^M has at most a pole: multiply by q^(N+1) and apply the removable singularity theorem. Therefore the numerator and denominator extend meromorphically; their quotient does too. Interior meromorphicity and finite cusp extension put all coefficients in K=C(X_Gamma). This excludes merely formal D-closure arguments.

For nonconstant t in K, write d=[K:C(t)]. The K-span of the first s derivatives of any coordinate is delta-stable. As a C(t)-space it has dimension at most ds, proving an order bound d r(w+1) over C(t). This restriction of scalars is required if t is not a Hauptmodul. For the previously considered weight-four, two-dimensional KZ solution space the bound is ten, not a claim of an explicit or minimal operator.

Negative weights do not admit this polynomial cancellation. A meromorphic scalar section of the same weight can instead normalize F to weight zero, possibly on a finite cover, but this proves an equation for F/a, not F. Mertens–Raum Theorem II(1) embeds weakly modular times mock forms with nonpositive integral mock weight into a finite-dimensional vector-valued form, retaining the original coordinate and total weight. The raw conclusion applies only when that total weight is nonnegative and the cusp hypotheses hold. Their theorem does not supply positive or half-integral mock-weight coverage.

## Approach 3: projective Bol reduction, including higher-genus descent

Work first with trivial characters and even integral weights. Let f_i be holomorphic parts with mock weights w_i=1−n_i<=0, n_i odd positive, and assume explicitly the Bol-image property D^(n_i)f_i=M_i in the weakly holomorphic modular space of weight n_i+1. This is the hypothesis supplied by the relevant harmonic weak Maass theorem, not an assertion for arbitrary objects called mock forms. Let A_i be meromorphic modular forms of even weights a_i with common total W=a_i+w_i. Put v=Dt, u_i=v^((n_i−1)/2)f_i, and

B_n u = v^(−(n+1)/2) D^n[v^((1−n)/2)u].

Bol covariance shows B_n is monic of order n with coefficients in K=C(X_Gamma); its coefficients are invariant meromorphic differential expressions in t and v, with finite cusp principal parts. Thus B_(n_i)u_i=M_i/v^((n_i+1)/2) is in K. Moreover U=v^(−W/2) sum A_i f_i = sum r_i u_i, where r_i=A_i/v^(a_i/2) is in K.

The space spanned over K by 1 and the first n_i jets of each u_i is delta-stable, of dimension <=1+sum n_i. Consequently U has an equation over K of that order, and over C(t) of order <=[K:C(t)](1+sum n_i). The genus-zero version and its finite-sum argument already occur in duplicate ID 20002515 and are not reclaimed as novel. The higher-genus rational descent removes that particular genus-zero restriction, but does not remove mock-weight or character restrictions. Finite characters can be killed on a finite cover if all other hypotheses persist.

For n=3, B_3=delta^3+2{tau,t}delta+delta{tau,t}; this identifies the projective connection explicitly. For n=1 it is simply delta. No unsupported explicit Poincare-series image is invented here.

## Approach 4: raw negative-weight obstruction

### Theorem

Let Gamma be a congruence subgroup, m>=1 an integer, and f a nonconstant holomorphic function on H with a nonzero translation period. Suppose D^(m+1)f transforms as a meromorphic modular form of weight m+2 on Gamma with scalar character chi. Then the raw f, as a multivalued function of any nonconstant modular function t for any finite-index subgroup, satisfies no nonzero homogeneous scalar linear ODE over C(t). In particular it satisfies no such ODE over C(j).

The same conclusion holds for algebraic-function coefficients after finite field descent. It concerns the unnormalized function and linear equations only.

### Proof

Intersect the two groups if necessary. Bol covariance says

D^(m+1)(f|_(−m)gamma−chi(gamma)f)=0.

Since H is connected, the difference is a polynomial P_gamma(tau) of degree at most m. Thus

f(gamma tau)=(c tau+d)^(−m)[chi(gamma)f(tau)+P_gamma(tau)].

A rational function of tau which has a nonzero period is constant: a finite pole would yield infinitely many poles; a polynomial periodic function is constant. Therefore f is not rational in tau.

A finite-index subgroup contains all powers of some lower unipotent matrix; choose gamma_n=(1 0;Ln 1) for n=1,2,... with a fixed L>0. Suppose a finite C-linear relation among branches f(gamma_n tau) holds. Substitution gives A(tau)f(tau)+B(tau)=0, where A=sum a_n chi(gamma_n)/(Ln tau+1)^m and B is rational. Nonrationality of f forces A=B=0. The poles of the summands in A are distinct, at −1/(Ln), and chi is nonzero. Comparing principal parts forces every a_n=0. These branch germs are therefore linearly independent in arbitrarily large finite sets.

They really are analytic-continuation branches over t: join a generic tau to gamma_n tau inside H while avoiding the discrete inverse image of branch values, poles, and any putative ODE singularities. Projecting gives a loop in the t-plane; continuation of the germ along that loop gives f(gamma_n tau). A scalar order-N ODE at an ordinary point has an N-dimensional solution space, which is incompatible with the branch independence. This proves the theorem.

### Applications and limitations

Nonconstant periodic negative-integral-weight harmonic weak Maass holomorphic parts satisfying the Bol-image theorem fall directly under this result; a cuspidal-shadow hypothesis avoids a nonholomorphic constant Fourier term, and without it the stated Bol-image property must be checked rather than assumed; the modular factor may be 1. For a genuinely mixed product A f of negative total weight, with A nonzero scalar modular and f as above, the same argument applies whenever A's scalar weight makes the denominator exponent positive: factor out A(tau) and separate the nonrational f from rational period-polynomial terms. This allows holomorphic modular factors, provided the total weight remains negative. An actual example must still be checked against the chosen definition of mixed mock form; the theorem does not assert that every convention permits every growth behavior.

A source-verified nonzero-mock-weight example is f_Delta from Mertens–Raum Section 3.2, Example 3.10, of mock weight −10 and shadow a nonzero multiple of Delta. Its explicit representation has rho(T) block diagonal with first entry 1, so f_Delta is 1-periodic. Its nontrivial degree-ten polynomial cocycle is displayed there; it cannot be the cocycle of a constant function (which under S would have only degree-zero and degree-ten terms). Thus f_Delta is nonconstant and the theorem applies directly. More importantly, E4 f_Delta is a genuinely mixed product with a holomorphic-at-cusp modular factor of weight 4 and a nonzero-weight mock factor, of total weight −6. Factoring out E4 in the branch argument proves that this raw mixed product is not D-finite over C(j), nor over any modular-function field. This conclusion does not rely on the weak modular factor in the next example. It is compatible with Mertens–Raum: their embedding has negative total weight, where the polynomial weight-cancellation argument is unavailable. It says nothing against an MLDE in tau or a normalized equation.

There is also a concrete example wholly anchored to the inspected Guerzhoy source: F=E4 h/Delta. The differential Dh has weight 2 with a sixth-order character, so h(gamma tau)=chi_5(gamma)h(tau)+C_gamma. The cusp normalization gives h(tau+1)=exp(5 pi i/3)h(tau), hence nonconstant 6-periodicity. F transforms by (c tau+d)^(−8)(E4/Delta)(chi_5 h+C_gamma). The same distinct-pole argument proves raw F is not D-finite over C(j). It is holomorphic on H because E4 h is, and Delta has no H zeros. This particular example uses the weakly holomorphic modular factor E4/Delta and has exponential cusp growth; it must NOT be advertised as belonging to a convention requiring polynomial cusp growth or holomorphic-at-cusp modular factors. Its mock factor is weight zero, not an NSZ genuinely nonzero-weight example.

## Approach 5: nonlinear differential-algebraic versus linear conclusions

The obstruction does not prohibit nonlinear equations. In the even-weight Bol class of Approach 3, v=Dt is a meromorphic modular form of weight 2; Approach 2 makes it D-finite over C(t), with controlled cusp hypotheses. The normalized U is D-finite as well. The differential-algebraic elements over C(t) form a field and are closed under algebraic extensions. Therefore the raw F=v^(W/2)U is differentially algebraic even when W<0, because integer powers and reciprocals preserve differential algebraicity. This uses the concrete Bol and modular-form equations, not the tautology that arbitrary functions generate differential fields. It establishes existence of a nonzero polynomial relation among finitely many derivatives, without falsely asserting linearity or providing a minimal relation. Thus in a concrete negative-weight class the raw linear and nonlinear answers differ.

A nonholomorphic completion is a separate unknown. With xi_k H=g, one has partial_(bar tau)H=(i/2)y^(−k)overline(g). For a holomorphic modular factor A and a local t-coordinate,

partial_(bar t)(AH)=(i/2)A y^(−k)overline(g)/overline(dt/dtau).

This anomaly PDE neither proves nor disproves a holomorphic scalar ODE for A H^+.

## Additional falsification test: why cusp hypotheses are essential

Finite-dimensional constant monodromy alone is insufficient. The weight-zero invariant g(tau)=exp(exp(j(tau))) has trivial monodromy but an essential cusp singularity. As a function of t=j it is not D-finite. If it satisfied an order-N rational-coefficient ODE, outside finitely many poles its companion first-order system along the positive real axis would have polynomially bounded coefficients. Gronwall's inequality would bound its solution norm by exp(C x^M) for some finite M, whereas exp(exp(x)) exceeds every such bound. This is a direct obstruction, not a claim about the standard mixed mock class, from which this wild cusp behavior is excluded.

## Literature gate and unresolved scope

Guerzhoy's example is published prior art. Mertens–Raum's finite-dimensional construction explicitly restricts mock weight to nonpositive integers. Nagatomo–Sakai–Zagier (published 2024), printed page 6, explains why weight-zero KZ mock factors are special and expresses doubt about MLDEs for genuinely nonzero mock weights. This is a conjectural remark, NOT an impossibility theorem. Their modular-operator conventions, scalar modular-function ODEs, and weakly meromorphic normalized constructions must not be conflated. No reconciliation of all conventions or global literature classification is claimed here.

Five substantive approaches have been completed: explicit elimination, finite-dimensional descent with cusp repair, projective Bol reduction and field descent, branch-independence obstruction, and differential-algebraic/PDE separation. None resolves all meanings of the original question. No novelty is claimed for their classical ingredients or the duplicate normalization theorem. The negative-weight obstruction is an authored deduction, not a literature-priority claim.

## Public source references

- AIM original problem location: http://aimpl.org/gromwitnumthry/5/ (exact wording recovered from corpus, not newly live-verified). Workshop context: https://aimath.org/pastworkshops/gromwitnumthryrep.pdf
- P. Guerzhoy, A mixed mock modular solution of the Kaneko–Zagier equation, Ramanujan J. 36 (2015), 149–164. https://math.hawaii.edu/~pavel/publications/mixed_mock_r.pdf ; DOI 10.1007/s11139-013-9496-9. Inspected locally, especially printed pp.2–3.
- M. H. Mertens and M. Raum, Modular forms of virtually real-arithmetic type I: Mixed mock modular forms yield vector-valued modular forms, Math. Res. Lett. 28 (2021), 511–561. https://arxiv.org/abs/1712.03004 ; Theorem II and remarks inspected locally.
- K. Nagatomo, Y. Sakai and D. Zagier, Modular linear differential operators and generalized Rankin-Cohen brackets, Trans. Amer. Math. Soc. 377 (2024), 7657–7698. DOI 10.1090/tran/9222. https://people.mpim-bonn.mpg.de/zagier/files/preprints/NSZ.pdf ; printed pp.3–4 and 6 inspected locally.
- J. H. Bruinier, K. Ono and R. C. Rhoades, Differential operators for harmonic weak Maass forms and the vanishing of Hecke eigenvalues, Math. Ann. 342 (2008), 673–693. https://arxiv.org/abs/0802.0963 . Bol-image theorem is used only under explicit hypotheses; duplicate report provides provenance, and no uninspected explicit image formula is claimed.
