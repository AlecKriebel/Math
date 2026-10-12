# Fresh adversarial review of the upstream gap input

Checkpoint: 2026-10-07 06:13:25 UTC. Reviewer: independent internal AI subagent `metric_package_review2/upstream_falsifier`.

## Verdict and scope

No blocking counterexample, circular invocation of the desired same-dimensional gap, or substantive mathematical defect was found in the primary proof passages reviewed. This is a scoped adversarial reading of the mathematical proof, not a Lean verification, conventional human peer review, reproduction of every published input, or an independent priority certification. The source-backed result is that the pinned family 037 manuscript states the unrestricted boundary-zero complex algebraic klt gap in every dimension at least two and gives a coherent proof mechanism, including the central singular-slice bootstrap and its sole fourfold companion. The package describes it as a principal external input and does not falsely describe it as a theorem proved or formally certified by this follow-on note.

Assigned audit completion: 100% of the requested primary-source attack and provenance check. This percentage measures the completed review task, not a probability that the upstream theorem is correct. Parent mathematical resolution and publication percentages are not assigned by this scoped reviewer. No external individual was contacted; no Git, publication, or frozen-input mutation was performed.

I read `ORIGINAL_REQUEST.txt` and `/Users/alec/Documents/Math/AGENTS.md` before the mathematical review. I first read the primary upstream TeX independently and only subsequently read the packaged prior audits for factual and scope consistency. Their favorable verdicts were not evidence for the mathematical conclusion below.

## Exact reviewed version and member accounting

The read-only upstream clone `/Users/alec/Desktop/math` has HEAD `adc7f1241b42e322a6451854ab7e4b4c146bf78a`. The final source archive independently hashed to:

`fb1d5a800e6be789fe94a227940a7df4888343fe444a9f64fe1c6b602514cfda`.

The following final-archive members were separately extracted/read or compared byte for byte to the already read extraction. All four have identical contents in the final archive and `reproducibility/tmp/metric_review2`:

| Member | Bytes | SHA-256 | Actual inspection |
|---|---:|---|---|
| `main.tex` | 27698 | `de80fb7f84555b632956f21ed8e6e0d1ae6b32da010ee6a89b69a72eb3cf8193` | Read its upstream statement, diagram, boundary-zero/dimension scope, source attribution, and formalization disclaimer; used its bibliography to locate primary inputs. Other metric/index claims are outside this assigned upstream review. |
| `agent_notes/upstream_geometric_audit.md` | 15043 | `e8b6eb07096f36f7d25c867bbfd43c305938e713a8e748a7680c91ea2ff6e59c` | Entire 109-line member read after independent primary inspection; checked source hashes and scope qualifications. |
| `agent_notes/upstream_semigroup_audit.md` | 24869 | `b2566e1045f2ac902aadb7dcea84aac0745b5c14225035da8062b0d410cf4e61` | Entire 446-line member read after independent primary inspection; checked derivations against primary sections 04–07 and its express limitations. |
| `sources/PINNED_MANIFEST.json` | 4722 | `876e3db29cae7bb566c5557247c6db1e18bc97a1a051f7b179906adea325876c` | Entire 111-line member parsed; all 21 listed upstream files independently checked for byte size and SHA-256 against the pinned clone. Every entry matched. |

Every manifest member was checked for its claimed immutable identity. Content review differed appropriately by member: the high-dimensional `build/paper.tex`, all proof sections 01–08, and proof-route figure were read; the fourfold companion mathematical argument through its final theorem was read; both manuscript READMEs, upstream README, family 037 catalogue entry, relevant bibliography entries, Lean README, and formalization-catalog search were inspected. The two upstream PDFs, preamble, complete unrelated catalogue content, and unrelated Lean families were only included in the 21-entry identity check, not independently rendered or exhaustively reviewed. The other final-package members were assigned to the parent/other reviewers; this note does not claim an entire-package review.

Primary proof locations below are under the pinned directory
`preprints/The-ordinary-double-point-gap-in-every-dimension-September-24-2026/build/sections/`, unless explicitly stated otherwise. Labels identify exact statements without dependence on PDF pagination.

## The claim being attacked

For a singular closed point of a normal complex algebraic k-fold, k >= 2, with Q-Cartier canonical divisor and klt singularities near the point, and with zero boundary, the claim is

\[
\widehat{\operatorname{vol}}(x,X)\leq 2(k-1)^k.
\]

The scope explicitly permits nonisolated points and does not assume quotient, complete-intersection, toric, smoothable, or hypersurface structure. The equality assertion characterizes analytic ODPs; the follow-on density transfer only requires the upper bound. The high-dimensional proof uses k = 2,3,4 as bases and induction for k >= 5. Thus the cubic application needs the entire transverse range 2 through n, including the unrestricted fourfold base; a hypersurface-only theorem would be insufficient.

## Cone reduction, finite degree, and the small case

Source: `02-cone-reduction.tex`, labels `cone:product`, `cone:edim`, `end:odp-value`, `cone:reduction`, `cone:approximation`; `03-small-stabilizers.tex`, complete proof.

* The source applies stable degeneration to a normalized-volume minimizer and the polystable refinement preserves its discrepancy and Reeb volume. Global minimizing status is again invoked on the final cone. Therefore the preserved quantity is the infimum, rather than merely a test value.
* The smooth-factor comparison is in the correct direction. Extending an N-dimensional valuation of discrepancy A and volume sigma by a parameter of weight A/N gives discrepancy A+A/N and volume N sigma/A. Its normalized density in dimension N+1 equals the original N-dimensional normalized density. Taking the infimum yields the required upper comparison.
* At a nonvertex point, the grading orbit specializes to the vertex. Lower semicontinuity gives vertex density <= nonvertex density. A singular transverse slice would then have density <= p_(n-1) by the lower-dimensional induction, contradicting p_(n-1) < p_n. This forces a smooth puncture without assuming a bound in dimension n.
* The canonical index-q cover is a separate finite-degree use: it is crepant and has a single point over the vertex. Its normalized density is q times the original density. The universal smooth-value bound d <= 1 gives d <= 1/q; the lower hypothesis p_n > 1/2 forces q = 1. This uses the universal bound, not the target gap. Minimality of the local canonical index rules out a nonzero residue-degree unit in the canonical-cover fiber, supporting the one-point-fiber argument.
* Finite generation gives finitely many positive generator values and hence finitely many occurring values below a fixed cutoff. The finite-discrepancy Izumi inequality makes cancellation terminate modulo the square of the maximal ideal. Thus embedding dimension can only increase on passage to the associated graded, and the subsequent flat refinement has the same correct semicontinuity direction. The final cone cannot be smooth if the original germ is singular.
* Primitive lattice approximations have absolute error tending to zero, not only normalized relative error. Division by the gcd retains this property. On an irrational ray bounded primitive canonical weights would force a constant lattice subsequence and a rational ray. This justifies the later integer rounding.

For the small-stabilizer case, the exact orbifold-curve input is appropriate: a representable one-stack-point rational curve has anticanonical degree plus inverse age at most dim(B)+1. This is Proposition 2.6, whose Fano-orbifold hypotheses match the quotient. It does not require the separate ample-tangent hypothesis from another theorem. I inspected that primary statement directly in [Li–Zhou, arXiv:2502.11847v1](https://arxiv.org/html/2502.11847v1).

The minimal-degree denominator/inertia calculation makes em/ell an integer in [1,(N+1)/N], forcing e = 1 and ell = m. The deformation Euler characteristic keeps the torsor and source fixed, and represents trivial tangent characters by m; it therefore subtracts the invariant fiber correctly. Stable graph-map properness plus a terminal positive-degree leaf shows that the vertex fiber of evaluation is the unique contracted map. Positive grading then makes evaluation finite by graded Nakayama. The symmetric product over its generic sheets produces a nonzero tensor; using a trace here would indeed risk cancellation, but the source does not do that.

The Ricci-flat tensor Bochner argument has the correct rank-dependent homogeneity: a derivation-weight tau tensor of rank b has norm degree tau+b. A positive norm-power with radial exponent in (2-2n,0) would integrate to a negative Laplacian on a compact link if tau+b < 0. Hence tau >= -b. Pairing with generator differentials controls character norm by O(b), so the changing tensor rank cancels from the approximation error. The resulting integer inequality forces nm = r. Trivial tangent action then forces m = 1, and the Fano-index classification gives the ordinary quadric or affine space. No same-dimensional gap enters this case.

## Central large-stabilizer attack: why the bootstrap is not circular

Sources: `04-jet-interiority.tex` through `07-bootstrap.tex`, particularly `adj:implication`, `adj:saturation`, `filt:reduced`, `filt:structure`, `boot:slice-tests`, `boot:slice-klt`, `boot:slice-singular`, `boot:character-shares`, `boot:refined-estimate`, `boot:holder`, `boot:upper`.

### Semigroup and adjoint order

The nonsaturated Taylor semigroup count supplies only leading density. The source separately proves compatible eventual jets and the exact generated congruence lattice, so its counting density after coordinate scaling is s, not 1/s. The fixed embedded cone gives a uniform Bezout order bound, which provides coercivity for the differentiated exponential integrals. Near-minimality of the degree tests gives a one-sided derivative >= -eta with eta -> 0; it does not assume exact stationarity of approximating gradings.

The universal exponential estimate places the canonical lattice point c0 in the strict interior. Its scalar optimizer has exact constant

\[
C_*={3\over4}e^{4/3}-{e\over3}<2.
\]

The finite-dimensional maximizer analysis uses distinct-coefficient stationarity, exponential size bias, and strict single crossing; the negative splitting-direction Hessian excludes a repeated high coefficient. Escape at fixed dimension and the later dimension limit are separately controlled. A diverging exceptional coefficient causes no hidden interchange requiring its growth to be slower than sqrt(N).

The adjoint implication is proved *without* assuming c0 interior. A finite list of initial sections surrounds the shifted interior point; scalar weights realize only the finite necessary monomial comparisons. Weighted blowup stacks retain their exceptional inertia. The canonical shift supplies the positive nef-and-big difference, Howald's smooth-uniformizer criterion gives the desired restricted multiplier section, and vanishing lifts it. Normal pushdown removes exceptional-only poles and recovers the selected initial. Only after this independent implication is proved is c0 interior used to obtain rational polyhedrality and saturation. Consequently there is no `interiority -> lifting -> interiority` cycle.

The support-form argument addresses irrational/nonpolyhedral boundaries explicitly. A differentiable support whose primitive height is not one has a forbidden lattice strip point; recurrence moves it just outside the cone while its canonical shift is strictly inside. The adjoint implication contradicts that configuration. An interior ball bounds all height-one lattice normals and makes their number finite. Saturation and interior translation then follow from facet inequalities.

### Filtrations and singularity of the slice

Subduction terminates in each original degree, so finite semigroup generation actually gives finite algebra/Rees generation. The two tracked canonical shifts are (r,N) for the first graded ring and (r,n) for the second. The regular parameter on the extended Rees space has action weight -1, giving the rational top form lambda^(-Q) Omega_C wedge d(lambda) and discrepancy comparison

\[
A_C(w)\leq A_{\mathfrak X}(V)+(Q-1)V(\lambda).
\]

The first quotient D is proved reduced using the original lower-volume hypothesis, not presumed normal: a multiplicity nu >= 2 would give volume <= 1 and discrepancy <= N+1/nu, hence (N+1/2)^(N+1) < 2N^(N+1) for N >= 4. Cohen–Macaulayness upgrades generic reducedness to reducedness. The basis-compatible second filtration has the actual algebra identity gr_W(S) = D[v], rather than merely the desired Hilbert series. A hypothetical free T-grading on D would make it polynomial, and then make S polynomial, contradicting singularity. Thus there is a nonvertex second stabilizer of order h >= 2. This h is distinct from the original maximal stabilizer m.

The level slice through an active homogeneous function has a finite etale product cover with Gm. Therefore it is a normal Gorenstein algebraic germ of the same dimension n, with a nonzero parameter lambda_Y of primitive character -1. It is klt away from lambda_Y = 0. Every quasi-monomial centered slice test restricts to a centered cone test, with

\[
A_C(w)\leq N\ell+A_Y(u),\qquad \operatorname{vol}(w)\leq\ell^{-n},\quad \ell=u(\lambda_Y)>0.
\]

Klt at the slice point is then proved: a nonpositive-discrepancy divisor supported over lambda_Y = 0 can be approximated by monomial valuations centered at the point. Their discrepancy/parameter ratio tends to a nonpositive value. The displayed cone comparison would force the original normalized volume <= N^n, contradicting the hypothesis >= 2N^n. The proof handles a nonpositive upper bound before taking an nth power.

Crucially, **the slice is not asserted singular merely because some earlier ring is singular**. Its singularity is proved separately in `boot:slice-singular`. If the W-Rees slice were smooth, the other central ring D would be either smooth or a minimal hypersurface whose relation has character -1 mod h. Its other deformation has invariant T-parameter t. Equivariant formal generator lifting gives either no relation or one relation of nontrivial character, which cannot contain a term depending only on t. Setting all other formal coordinates to zero creates a mu_h-fixed formal section. An active positive-T function remains a unit on that section. But the generic T-fiber is standard affine N-space with every coordinate of character one; for h >= 2 its fixed-point scheme is precisely the origin, where every positive-T function vanishes. This contradiction proves singularity of the slice. It defeats the proposed failure in which degeneration accidentally produces a smooth same-dimensional slice.

### Exact discount and supremum

The genuine slice minimizer is mu_h-invariant by uniqueness normalized by discrepancy. Multiplication by powers of the nonzero primitive-character parameter injects character quotients into one another with fixed cutoff shifts. Each character therefore carries exactly 1/h of the leading colength. This would fail for a trivial character action; the primitive parameter is essential and is present.

The colength split is exact. Restriction divided by lambda_Y^p injects its second term into the single character p mod h, yielding

\[
\operatorname{vol}(w)\leq\min_{0\leq x\leq1}
 \{x^n/\ell^n+(1-x)^n\sigma/h\}.
\]

Direct optimization and Holder give

\[
d(o,C)\leq (N/n)^n+d(y,Y)/h
 \leq p_n/2+M_n/2.
\]

Here Y is already proved singular, boundary-zero, algebraic and klt, of dimension n; its minimizing density is legitimately bounded by the *definition* of M_n. The only a priori bound on M_n is the universal M_n <= 1. The desired M_n <= p_n has not been used. If M_n > p_n, singular densities approaching M_n reduce to fixed cones. An infinite small-stabilizer subsequence would classify the cone as smooth/ODP and contradict density > p_n. Otherwise one sufficiently far large-stabilizer grading gives the displayed strict discount. Passing to the density supremum gives M_n <= (p_n+M_n)/2 and hence M_n <= p_n. The supremum need not be attained; constants may depend on each fixed cone. No new unsupported equivalent assertion replaces the central target.

The equality return also has a coherent mechanism: equality forces h = 2, A' = N ell, and after ell = 1, sigma = 2, A_C(w) = 2N, volume = 2^(-N). A single-power strict count proves w(v) <= 2. The changing chosen section has characters in a fixed finite set of bounded-length generator monomials. Absolute grading error then gives Nm-r = o(1); integer rounding returns to the small case. Equality is additional to the upper bound used by the follow-on paper.

## Fourfold base and hypersurface edge cases

The companion is `preprints/The-normalized-volume-gap-in-dimension-four-September-24-2026/build/paper.tex`, SHA-256 `2e1eb5a05a308182d34d75eb428474fbe11cce86445cb01bc4e654e9a5e25390`.

Its theorem does not assume hypersurface structure. It reduces volume >= 162 to an isolated Gorenstein graded cone, using the established nonisolated bound 4096/27 and the universal 256 bound on the canonical cover. The jet comparison has discrepancy r+3 alpha and the correctly integrated volume factor h/(1+alpha(mh)^(1/3))^3. The normalized strict derivative at m/r >= 2/5 uses 324/5 > 64. Integer Gorenstein discrepancies then give A >= 3.

The companion's signed Hilbert duality/Fourier argument excludes root frequencies through stabilizer bounds and constructs a low-weight function without assuming a chosen set generates the maximal ideal. Its low-weight ideal threshold comparison has the correct direction. A homogeneous lc boundary of total weight < 5/2 excludes the vertex as a center. Affine subadjunction plus the curve/surface/threefold canonical-module arguments rules out a positive-dimensional minimal center and yields lct(m) > 3/2. Together with A >= 3, this makes a general hyperplane section terminal Gorenstein. The cDV classification bounds embedding dimension by five, and only then does the proof use Liu's established lci gap. No use of the unrestricted fourfold target precedes this structural conclusion.

In the higher-dimensional return, a singular normal k-dimensional local ring of embedding dimension <= k+1 has embedding dimension exactly k+1. Independent linear equations cut the smooth ambient germ to that dimension; the remaining height-one prime in its regular local ring is principal. This is a genuine hypersurface consequence, not a premise about all starting germs.

Source `08-conclusion.tex`, `end:hypersurface-test`, treats arbitrary positive rational weights via an m-primary ideal, inversion of adjunction, multiplicity, and a divisor computing the ideal's lct. It does **not** pretend that the weighted-order function on a reducible/nonreduced hypersurface initial ring is a valuation. The Hilbert coefficient and ideal-power sandwiches give

\[
\widehat{\operatorname{vol}}(x,X)\leq
 {d_F(\sum_iw_i-d_F)^k\over\prod_iw_i}.
\]

The relevant published inversion-of-adjunction statement permits a smooth ambient variety, normal effective Cartier hypersurface, and a primary subscheme restricted to it. Those hypotheses hold here; the ambient weight valuation gives the required upper threshold. I inspected [Ein–Mustata, Theorem 1.1, arXiv:math/0301164v2](https://arxiv.org/html/math/0301164v2).

For multiplicity q >= 3, equal weights give q(k+1-q)^k. Klt requires q < k+1; the derivative (k+1)(1-q)(k+1-q)^(k-1) is strictly negative for 1 < q < k+1. Thus this bound is strictly below 2(k-1)^k. In dimension two, klt already excludes q >= 3 by the same ambient discrepancy test.

If q = 2, the quadratic rank is at least one by definition. A degenerate rank supplies a null direction. Weighting one such direction 1-epsilon and all others 1 gives d_F = 2 for 0 < epsilon < 1/3 and bound

\[
 B_k(\epsilon)={2(k-1-\epsilon)^k\over1-\epsilon},
 \quad B_k(0)=2(k-1)^k,
 \quad (\log B_k)'(0)=-1/(k-1)<0.
\]

This covers *every* degenerate rank, including ranks one and two, without requiring an irreducible quadratic initial form. The exact limiting constant is the target ODP value, approached strictly from below. An explicit choice epsilon = 1/(3k) works in every k >= 2: the logarithmic derivative has numerator -1+(k-1)epsilon and remains negative throughout that interval.

There is also a direct stronger check for ranks one and two. Give each nonzero quadratic variable weight 1 and all quadratic-null variables weight 2/3. Every cubic-or-higher term has weight >= 2, so d_F = 2 even when extra cubic terms tie. The ideal-based test permits those ties. If rank rho is one or two and s = k+1-rho, the bound is

\[
 2\bigl(k-1-s/3\bigr)^k(3/2)^s
 =\begin{cases}
 2(k-3/2)^k,&\rho=1,\\
 (4/3)(k-1)^k,&\rho=2.
 \end{cases}
\]

Both are exact rational-weight constants and strictly smaller than 2(k-1)^k for every k >= 2. They also equal the limits obtained when all null weights 1-epsilon tend to 2/3. Rank zero belongs to q >= 3 rather than to the multiplicity-two case. At full quadratic rank the holomorphic Morse lemma gives an analytic ODP. The reverse ODP equality uses a genuine minimizing degree valuation: source `end:odp-value` identifies it by uniqueness and the irreducibility of harmonic polynomial pieces under SO(k+1), then computes discrepancy k-1 and volume 2. The exceptional two-ambient-variable representation case lies outside k >= 2.

## Independent exact checks and formalization truthfulness

Inline standard-library Fraction checks independently reproduced:

* the exponential tail upper certificate 917330371/241805655 < 1897/500;
* the e lower partial sum 1957/720 > 1359/500;
* C_* < 3879/2000 < 2;
* the rank-one/rank-two formulas and strict comparisons at k = 2,3,4,5,6,10,50 using exact rational arithmetic. The formulas above, rather than this finite sample, prove the all-k comparison.

The fourfold numerical contradiction constants were also read and checked against their analytic derivations: M2 = 61/64, M4 = 685/256, M6 = 11101/1024, coefficient 50065/9216, conservative fourfold gap 209183/1440000, and threefold gap 19/324. The parent is separately rerunning the deposited arithmetic certificates.

At the pin, `lean/docs/037.md` is absent. The formalization catalogue has no ordinary-double-point/normalized-volume/Fano gap entry. A search of actual declarations found unrelated uses of `normalizedVolume` as ordinary probability/Riemannian normalization, not a formalization of normalized volumes of klt germs. Those were not treated as proof evidence; no Lean build was performed or asserted. Thus the final manuscript's explicit statement that no Lean verification of the gap or the consequence is claimed, the README's no-formal-verification statement, and both audits' disclaimers agree with actual scope.

All 21 source-manifest identities match. Both packaged audits accurately limit their scope, distinguish written proof inspection from formal verification, and leave their complementary inputs explicit. No factual provenance or scope mismatch was identified in those assigned members.

## Remaining limits

The conclusion remains a scoped primary-proof audit. Published inputs such as stable degeneration/finite generation, uniqueness/finite degree, semicontinuity, Collins–Szekelyhidi existence, twisted-map properness, vanishing, semigroup canonical duality, subadjunction, Reid's cDV classification, and Liu's lci gap were checked for their stated role and local hypotheses, but their complete original proofs were not independently reconstructed here. Only the two particularly pertinent primary statements identified above were newly browsed in this turn. A later correction to any pivotal input could change the mathematical status. No such failed input or explicit unresolved internal step was found in the audited chain.

This note does not validate the separate Li–Liu-to-metric bridge, Spotti–Sun's complete cubic transfer, modern moduli terminology, boundary isometry rigidity, novelty, PDF layout, publication metadata, or deposit/tracker actions. Those remain other reviewers' assignments. The appropriate use of this result is as one fresh source-backed check of the pinned external gap input, with no claim of formal or human-refereed certification.
