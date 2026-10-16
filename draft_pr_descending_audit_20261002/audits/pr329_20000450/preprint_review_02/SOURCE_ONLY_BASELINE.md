# SOURCE-ONLY BASELINE: AIM Question 17

Written UTC: 2026-10-04T12:11:03Z

## Exposure and status boundary

This is a new, independent reviewer baseline. I have read only the applicable root AGENTS.md, the PDF skill/runtime documentation, my task instructions, and the original AIM source obtained independently in this namespace. I have not opened any candidate manuscript, candidate PDF, deposit metadata, verification ZIP, PR source, prior audit directory/report, gate, tracker, or status snippet. The parent supplied the identifiers PR329 and problem20000450 solely for routing; those identifiers are not mathematical evidence. No external individual has been contacted. A read-only branch query returned main; no Git or index changes were made.

Completion estimates at this checkpoint: source-only preparation 100%; the requested complete independent preprint/package audit 10%; solution of the original mathematical problem is not assessed, because no proposed solution has been examined. This baseline is a statement of scope and adversarial standards, not an approval, a seal, or a mathematical conclusion about the candidate.

## Actual source and physical-page verification

Source URL: https://www.aimath.org/WWN/qptsurface2/qptsurface2.pdf

Native retrieval was executed with the exact argv, working directory, actual native UTC start/end, complete stdout/stderr, and exit status preserved in native_receipts/source_download.json, .stdout, and .stderr. Start 2026-10-04T12:06:52Z; end 2026-10-04T12:06:53Z; exit 0; HTTP 200; application/pdf; 502057 bytes; no redirect. The response headers are source.http_headers.txt. Its Last-Modified value is a server-file timestamp, not a date of mathematical discovery.

The downloaded bytes are qptsurface2.pdf. Native SHA-256: 8b64d2f6b91f791c35afae10b2ef79c15a927a94c2142a56386f80c8b8a596e6. Native pdfinfo independently counts 59 physical PDF pages. The count was obtained before extracting/rendering physical page 51. Both qptsurface2.page_01.png and qptsurface2.page_51.png were visually inspected; the printed page labels are 1 and 51 respectively. The full layout-preserving text, separate page texts, render commands, and their complete native receipts are preserved. The browser PDF parser independently corroborated 59 pages; the native retrieval and render remain the primary artifacts.

The frontmatter identifies an AIM workshop proceedings/problem collection on rational and integral points on higher-dimensional varieties. The workshop occurred in Palo Alto, 11-20 December 2002; the displayed document version is 22 November 2004, 11:41:01. Frontmatter credits John Voight and William McCallum primarily for lecture notes and the problem list, and William Stein for glossary, photographs, and arrangement. These editorial credits do not establish that every statement is a theorem or identify all prior literature.

## Exact original target, with all four remarks retained

Question 17, attributed there to McCallum, starts with a regular pentagon P and its circumcircle C, and forms the plane equation E: P + lambda C^2 = 0. It calls the plane curve a quintic with five double points and geometric genus one, and identifies five points at infinity using the slopes of the five side lines. The operative request is: “Compute the 5-torsion of E.”

The four ensuing remarks have distinct content and must not be conflated:

1. The five points at infinity are stated to be among the 5-torsion.
2. McCallum gives the motivation: these genus-one curves are principal homogeneous spaces, prospective 5-torsion elements of the Tate-Shafarevich group. The remark relates lambda, viewed as a parameter on X_1(5), to a twist of its universal elliptic curve and stresses explicit models. This is workshop motivation, not proof of local solubility, nontriviality, exact period, or a global Tate-Shafarevich class for any specialization.
3. Ellenberg asks how this pencil of elliptic curves relates to the conference talks. No specific theorem or required answer is stated.
4. Voloch asks whether regularity is necessary and mentions variants, including replacing the circle by a star pentagon. This poses a scope-extension question; it supplies neither a classification nor a precise algebraic definition of every variant.

An answer limited to five distinguished points, or to a generic cyclic subgroup, must say explicitly that it is narrower than computation of the whole 5-torsion. The other four statements are historical source content that a candidate may prove, refine, qualify, or leave open, but must not silently elevate into deductions.

## Assumptions the source leaves unspecified

The source does not fix the coefficient field, a coordinate system, a scale/orientation/translation of the pentagon, or the equation normalizations for P and C. The visible Euclidean construction suggests characteristic zero and real algebraic coordinates, but that is an interpretation requiring declaration in any algebraic treatment. A regular pentagon is not automatically defined over Q in a chosen Euclidean coordinate frame; fields of definition, descent, and rationality must be stated separately from geometric statements over an algebraic closure.

P as a geometric polygon must be interpreted as an equation, normally the product of its five supporting side-line equations. C must be interpreted as a quadratic equation for its circumcircle. Multiplying the individual line equations or circle equation by nonzero constants reparametrizes lambda. An identification with a modular parameter cannot ignore that normalization.

The source does not specify which lambda values are intended, whether the plane curve is irreducible, whether all five double points are ordinary nodes, whether additional singularities occur, or whether a smooth projective normalization is intended. It does not specify an origin for a group law. A smooth genus-one torsor has a Jacobian; a chosen geometric point identifies it with that Jacobian, but a rational identification requires a rational point over the claimed field. Saying a point is torsion on the plane curve without an origin or a divisor-class convention is ambiguous.

The source does not define “compute” as a full coordinate presentation, a splitting field, a Galois representation, a finite group scheme, a division polynomial, or a distinguished order-five subgroup. The strongest natural characteristic-zero interpretation is a checkable complete description of J[5] for the Jacobian J of the smooth projective genus-one curve, together with the identification of the five distinguished points under a stated origin. Over an algebraically closed characteristic-zero field J[5] has 25 points and abstract group (Z/5Z)^2; the field-rational subgroup can be smaller. This standard group-law baseline is separate from the source's unproved assertion about the five infinity points.

The source's Sha and modular language leaves the base field, torsor class, local-solubility hypotheses, and whether “twist” refers to an unpointed genus-one torsor, an elliptic curve, or a marked modular object unspecified. X_1(5), its compactification, its cusps, and the chosen marked order-five point require explicit conventions. A single five-point orbit does not by itself establish a rational point of X_1(5) over the original field.

## Source-independent geometric/algebraic boundary derivations

For a concrete characteristic-zero reference interpretation, put the five vertices on the unit circle at angles 2*pi*j/5. The side through vertices j and j+1 has equation

    L_j(x,y) = cos((2j+1)*pi/5)*x + sin((2j+1)*pi/5)*y - cos(pi/5),
    P(x,y) = product_{j=0}^4 L_j(x,y),    C(x,y)=x^2+y^2-1.

These equations are merely an explicit normalization chosen independently for adversarial testing. Their coefficient field is the field generated by the displayed trigonometric algebraic numbers; no claim of Q-definition is being made. In homogeneous coordinates, let P_5=product L_j(X,Y,Z) and C_2=X^2+Y^2-Z^2. The degree-five homogenization is

    F_lambda(X,Y,Z)=P_5(X,Y,Z)+lambda*Z*C_2(X,Y,Z)^2.

The factor Z is essential: C_2^2 is degree four. Omitting it changes the projective problem. On Z=0, the five side directions give the five roots of P_5(X,Y,0). They are distinct because the five side lines of this regular odd-sided polygon are pairwise nonparallel. Thus the restriction to the line at infinity has simple roots; at each such point a derivative with respect to X or Y is nonzero, so those five plane points are smooth for every finite lambda in this normalization. They lift uniquely to the normalization on an irreducible fiber. This proves smoothness and distinctness here, not order five.

At each pentagon vertex, two side factors vanish and C vanishes. Both summands therefore have vanishing value and linear part. Local coordinates u,v along the two adjacent side equations give a quadratic term

    a*u*v + lambda*(b*u+c*v)^2,

with a nonzero and, for a nonsingular circle meeting neither side tangentially at the vertex, b,c nonzero. The quadratic term can acquire a repeated factor at exceptional lambda values. The original genus inference is valid for a geometrically integral quintic with exactly five ordinary double points and no further singularity: arithmetic genus (5-1)(5-2)/2=6, and the five node delta-invariants subtract five. Mere existence of five unspecified double points does not establish that conclusion for every fiber.

The lambda=0 fiber is the union of five lines, so it is reducible and cannot be treated as one elliptic curve. In the projective pencil, write F_[s:t]=s*P_5+t*Z*C_2^2. The parameter [0:1] gives the line at infinity plus a double conic, a nonreduced fiber. Any all-fiber claim needs a precise extension/model or explicit exclusions. A generic calculation on Q(lambda) does not determine those boundary fibers. Additional finite exceptional parameters must be derived rather than guessed from these two obvious fibers.

Further boundary cases: a proposed nonregular polygon may have parallel sides and coalesced directions at infinity; a conic may be reducible, singular, or tangent to a side; adjacent or nonadjacent vertices may collide; roots can move into extension fields; affine coordinate denominators can vanish at torsion points or at parameter values where another chart is needed. In characteristic 5, the geometric-point interpretation of 5-torsion changes and [5] is inseparable; characteristic 2 changes many circle/quadratic arguments. Neither characteristic is included without a separate theorem. Scale changes, reordering of vertices, orientation reversal, origin changes, and Galois conjugation must preserve whatever intrinsic object is claimed.

## Success criteria for a complete proposed answer

Each theorem must identify its base field, parameter domain, geometric object (plane curve, normalization, Jacobian, torsor, or singular model), and group-law conventions. Hypotheses must ensure the object exists and meets the genus-one/smoothness claims used later. A claimed classification must state and verify both directions and all exceptional cases.

A full torsion computation must prove completeness, not merely exhibit five points: specify the 25 geometric 5-torsion points or a complete finite algebra/group scheme with a verified equivalence to J[5]; prove the group-law relation and exact order of any displayed nonidentity point; locate the infinity points; distinguish rational torsion, geometric torsion, and Galois action; and verify any coordinate maps on their entire stated domain, using additional charts where necessary. If the proposed achievement is only a cyclic order-five subgroup or a regular-pentagon special case, it may still be a contribution, but the title, abstract, conclusion, and deposit metadata must match that narrower result.

A torsor/Sha claim needs an explicit cohomological or equivalent geometric construction, descent/cocycle verification, and proof of local solubility at every relevant place for each claimed global example. Period, index, and class order are distinct. Modular claims need a checked parameter change, nonsingular-domain comparison, j-invariant/discriminant compatibility, and the relevant marked structure; a matching j-invariant alone is insufficient to prove a claimed twist or rational marked-model isomorphism.

Any nonregular-pentagon or star-pentagon result must define its input family and separate sufficient from necessary conditions. Any all-fiber theorem needs singular/reducible/nonreduced fiber treatment, including maps and divisor interpretation at each exceptional parameter. Explicit computations require reproducible exact arithmetic with preserved actual command receipts, code, inputs, and outputs, and a proof that finite computations establish the stated universal claim. Sampling is only evidence, never a proof of completeness or a quantified assertion over all parameters.

Source and priority claims must cite the workshop attribution and distinguish 2002 workshop date, 2004 displayed version date, and later server timestamp. Novelty needs independent primary-source comparison at the appropriate later stage. A prior review or automated PASS is neither a theorem nor evidence of absence of prior art. Paper/PDF/deposit metadata must agree on claims, authorship, date/version, assumptions, limitations, and references.

## Materially distinct falsifiable adversarial routes

| Family | Mechanism and concrete falsifier | Evidence now | Status / exact remaining gap |
|---|---|---|---|
| Local/projective geometry | Compute singular locus, tangent cones, delta-invariants, normalization, infinity intersections, and special fibers; falsify genus/smoothness or “all lambda” by one missed singular/reducible fiber. | Homogenization and obvious zero/infinite boundaries derived above. | Planned; no candidate formula exposed and no complete discriminant computed. |
| Intrinsic divisors and group law | Independently form principal divisors/line-section classes on the normalization and test 5(P_i-P_0)=0, exact order, and completeness without assuming a coordinate normal form. A divisor valuation disagreement or nonprincipal asserted divisor falsifies the torsion argument. | Need for origin/divisor convention identified. | Planned; no actual torsion divisor proved. |
| Direct algebraic torsion elimination | Derive Jacobian or a verified birational model, form [5] kernel/division equations, compare schemes and count 25 distinct geometric points in char 0. Missing points, extra solutions, denominator failures, or incorrect field descent falsify full computation. | Standard size of geometric J[5] gives a completeness target. | Planned; no candidate model, division polynomial, or map tested. |
| Moduli/marked structures | Independently compare invariants and marked point to X_1(5)/Tate-type normal form, including parameter changes, discriminants, ramification, and cusps. Same j but wrong marked structure or unsupported field of isomorphism falsifies stronger claims. | Source motivation, not a proved identification. | Planned; parameter normalization and moduli map uncomputed. |
| Arithmetic torsor/descent | Independently verify cocycles, fields, torsor/Jacobian distinction, period/index/class order, and all local places for global Sha claims. A failed local place, coboundary, or hidden rational origin contradicts a claimed Sha example. | Original source leaves these data unspecified. | Planned; no global specialization or local-solubility claim examined. |
| Degeneration and counterexample construction | Drive parameters to every boundary, vary polygon/conic shape, and check parallel/tangent/degenerate configurations. Seek minimal exact counterexamples to necessary/sufficient classifications. | Zero/infinity fibers and nonregular risks identified. | Planned; no universal extension or classification evaluated. |
| Proof/code/output and publication consistency | Independently rerun exact certificates, challenge quantifier transfer and coverage, compare every claim in proof, PDF, text, code, outputs, and deposit metadata, and compare primary prior art. A reproducible contradictory output, missing implication, overbroad metadata statement, or omitted prior result is a falsifier. | Original source provenance preserved. | Planned; candidates and package intentionally unavailable. |

These routes must remain independent long enough to avoid importing a candidate's pivotal unproved claim. A route that merely reduces the central task to an equivalent unsupported assertion is blocked until a materially new mechanism/evidence appears. Failure records and exact gaps will be retained. Procedural exposure limits and historical receipt limits will be reported separately from current deductive correctness.

## Strongest verified statement and remaining gap

Verified here: independently retrieved exact source bytes; 59-page count; frontmatter; physical page 51 and all four remarks; exact interpretation boundaries; the stated independent homogenization, distinct smooth infinity points for finite lambda in the explicit regular normalization, local quadratic form, genus-count qualification, and obvious reducible/nonreduced pencil boundaries. No torsion computation, candidate theorem, novelty claim, Sha class, or publication readiness has been verified. The entire candidate and package remain unexamined. The next stage requires an explicit release from the parent and will initially be limited to candidate TeX/PDF/deposit metadata, followed by a frozen complete claim ledger before any verification ZIP or previous review exposure.
