# Independent scoped audit: critical massive Dirac potentials

Problem 30005664 / OWR-14297742-004, queue rank 779. Review date: 5 October 2026.

## Verdict

**PASS for the five expressly limited propositions. The original optimization problem remains unresolved after 5/5 substantive author approaches.** This is a fresh independent AI audit of the frozen author artifact, not human peer review or formal proof-assistant certification. No new proof attempt at the unresolved global problem was undertaken. No first-discovery or novelty claim is certified.

The author ZIP SHA-256 is `9ab3bab00933cd5dbdbc423eafd7f60c114a13bfb7fcdafb8f5569f29c8503aa`; its manifest SHA-256 is `a69d19e3fdbf80a824b18b8c2527ce1de4029ebe5639ad020160a9cbb021cc88`. All eight frozen members, their exact allowlist, their manifest hashes, and their equality with the supplied author directory were checked. The freeze was not edited.

The original author checker was separately replayed: all 957 controls passed and output was byte-identical. The newly written checker independently reconstructs the same 957-control coverage and adds 35 exact controls. It does not import or execute author code. It uses a different recursive Clifford representation, the variable t=r² for the radial operator, independently differentiated matrix polynomials, and additional mass-symbol, spinor-index, beta-integral and sharp-witness checks. All 992 independent controls pass. These calculations support, but do not replace, the analytic audit below.

No proposition needs a mathematical correction. The main added clarification is important: **the sharp number 4m/p belongs to the closed scalar upper-component Schur form, not the spectrum of the full Dirac operator.** Its sharpness witness does not reconstruct an L² lower spinor component for 2<p≤3. This does not invalidate the author theorem, whose domain is explicitly the scalar form closure. Section 6 below supplies the precise distinction that should accompany any abbreviated description.

## 1. Target and external dependencies

The primary target is the nonnegative electrostatic potential problem for D_m−VI, with m>0 and the lower edge −m of the massive free gap. It is not a mass-type perturbation Vβ, a massless zero-mode question, or arbitrary membership of −m in the spectrum. The essential spectrum already contains that endpoint at V=0. The critical strength is obtained by an interior-gap limit.

The complete Gontier contribution in the official Oberwolfach report, printed pages 2288–2291, was read. Page 2290 was independently rendered and visually checked. The finite-width candidate requires finite p>d≥2; the report's broader surrounding theorem and its m=1 displayed formula must not hide this restriction or the general mass factor m^(p−d).

DGPV's arXiv v2 and final publisher version were checked at the definitions, operator-domain statement, interior variational formulation, candidate, and explicit open questions. Its Proposition 2.1 supplies the distinguished self-adjoint realization; in the audited range p>d, d≥2, the domain is H¹. Its equations (3.2)–(3.3) and Theorem 3.1 supply the inverse-strength variational formulation in this range. The all-dimensional algebra in the note does not purport to reprove these imported operator/optimization results. Their hypotheses match its use. DGPV §5.4 already supplies the candidate and upper bound in d=2,3; that credit is essential.

References:

- Gontier contribution, [Many-Body Quantum Systems, OWR 20 (2023)](https://ems.press/journals/owr/articles/14297742), DOI 10.4171/OWR/2023/39, publisher publication 18 April 2024.
- Dolbeault, Gontier, Pizzichillo and Van Den Bosch, [Keller and Lieb–Thirring estimates of the eigenvalues in the gap of Dirac operators, arXiv:2210.03091v2](https://arxiv.org/abs/2210.03091v2), 24 July 2023; [final publisher PDF](https://ems.press/content/serial-article-files/47110?nt=1), Revista Matemática Iberoamericana 40 (2024), 649–692, DOI 10.4171/RMI/1443.

## 2. All-dimensional candidate and genuine threshold state

Write X=α·x and s=μ²+|x|². The Clifford relations give X²=|x|²I, βX=−Xβ, and

    (μ−iX)(μ+iX)=sI.

The positive β eigenspace is nontrivial because any α_j is an invertible isometry exchanging the positive and negative eigenspaces. The stated N=2^floor((d+1)/2) supports the d+1 Hermitian anticommuting generators. No extra angular ansatz is assumed in the calculation.

For Ψ=C s^(−p/2)(μ+iX)ξ, βξ=ξ, the residual of (D_m+m−V)Ψ has scalar coefficient d−p+2mμ and X coefficient zero when V=pμ/s. Thus μ=(p−d)/(2m)>0 and C=(pμ)^((p−1)/2) give both the equation and |Ψ|²=V^(p−1). The mass symbol is α·k+mβ, whose square is (|k|²+m²)I. This fixes the sign and gap conventions independently.

Near the origin these profiles are smooth. At infinity |Ψ| has order r^(1−p), while its first derivative has order r^(−p). L² requires p>1+d/2 and the gradient requires p>d/2. Finite p>d≥2 satisfies both strictly. The result is a genuine H¹ threshold eigenfunction of this bounded smooth potential. It is not merely a formal resonance. No L²-unit normalization was imposed: the Kerr amplitude is fixed by the pointwise density identity.

The radial beta integral is

    ∫R^d s^(−p) dx = π^(d/2) μ^(d−2p) Γ(p−d/2)/Γ(p).

It gives the exact candidate norm to power p as p^p μ^(d−p) C(p,d), and hence the factor m^(p−d). Direct beta recursions also give 2m‖P_+Ψ‖²/∫V^p=(p−d)/p. These expressions are dimensionally and algebraically consistent.

The upper bound a_*≤A is justified by an interior resolvent limit, not an inverse at the threshold. Put w=VΨ=(D_m+m)Ψ. Its decay is O(r^(−p−1)), so w∈L²∩L^(2p/(p+1)). If I=∫V^p, then ‖w‖_q²=I^((p+1)/p) and ⟨w,Ψ⟩=I. For t denoting the spectral variable of D_m+m, the support is t≤0 or t≥2m. When 0<ε<m,

    |t²/(t−ε)| ≤ 2|t|.

The right side is integrable against the spectral measure of the H¹ spinor. Dominated convergence proves the required quadratic limit I and therefore the upper bound. No uniform upper bound on the variational supremum follows from this one test spinor.

## 3. Restricted-width optimization

For b=d+2mμ and W_μ=bμ/(μ²+r²), the same residual vanishes with exponent b. Since b>d≥2, its explicit state is H¹. With p fixed separately,

    J(μ)=C(p,d)(d+2mμ)^p μ^(d−p),
    (log J)'=d[2mμ−(p−d)]/[μ(d+2mμ)].

It changes sign exactly once, at μ=(p−d)/(2m). Also J→∞ at μ↓0 and μ→∞; at the latter endpoint J grows like a positive constant times μ^d. The minimum is global and unique on this specified branch. This proves neither a classification of threshold rational potentials nor radial/global optimality. Away from b=p, the branch spinor need not satisfy the Kerr normalization for the separately fixed p.

## 4. Pohozaev and concentration boundaries

For q=2p/(p−1), the H¹→L^q embedding needed by the action holds throughout p≥d≥2. The action is real differentiable on H¹. The additional assumption that the L²-preserving dilation curve is H¹-differentiable authorizes the exact scaling derivative. A smooth spinor with x·∇Ψ∈H¹ is sufficient. The proof does not quietly infer that assumption for arbitrary weak threshold states.

The amplitude and dilation equations give T+2m‖P_+Ψ‖²=I and T=dI/p. At p=d, P_+Ψ=0. Since D_0 exchanges the β eigenspaces, projection of the nonlinear equation onto the negative eigenspace gives |Ψ|^(q−2)Ψ=0. Thus no nonzero spinor in the stated class exists. This is not a nonexistence theorem for every resonance or every possible endpoint optimizer. The explicit states satisfy the dilation assumption by the same derivative decay estimates.

For p=d on the width branch, J(μ)=C(d,d)(d+2mμ)^d is strictly increasing. Its infimum is approached as μ↓0 and never attained at positive μ. The change of variables x=μy gives the weak finite-measure limit d^d C(d,d)δ_0 by dominated convergence against every bounded continuous test function. Pointwise away from zero the potentials tend to zero. The limit of the p>d norm formula as p↓d agrees with this constant, using ε log ε→0. A finite norm limit is not a finite-width function at μ=0.

Under V_t(x)=tV(tx), the comparison mass is tm and ‖V_t‖_p=t^(1−d/p)‖V‖_p. This confirms why an unmodified massless conformal statement does not prove a fixed-positive-mass lower bound.

## 5. Schur operator, closure, and all angular modes

In the specified two-dimensional Pauli convention,

    D_m+m−V = [[2m−V, P*], [P, −V]],
    P=−i(∂_1+i∂_2),  P*=−i(∂_1−i∂_2).

For smooth components the second row says v=V^−1Pu. The scalar expression obtained from the first is P*wP+2m−V, w=V^−1. The form to audit is

    Q[u]=‖sqrt(w)Pu‖²+∫(2m−V)|u|².

### Closability and its concrete domain

The operator sqrt(w)P on C_c^∞ is closable in L². Indeed, if u_j→0 in L² and sqrt(w)Pu_j→F in L², testing against a compactly supported smooth function, with division by sqrt(w), forces F=0 distributionally. Thus the completion specified by the author embeds injectively into L². The potential term is bounded because 0<V≤p/μ. Consequently Q is a closed semibounded form on that completion after addition of a sufficiently large L² multiple.

For this weight, the completion also equals the maximal distributional graph domain {u∈L²: sqrt(w)Pu∈L²}. One way to see density is to first use cutoffs at radius R: on their annulus w|∇χ_R|² is uniformly bounded, so the extra cutoff error is bounded by the L² tail of u. Local ellipticity of P gives H¹_loc, since |symbol(P)|=|k|. Standard local mollification then gives C_c^∞ approximation. This also excludes hidden point-supported components at the origin.

### Fourier bookkeeping

For upper mode n,

    P(f(r)e^(inθ))=−i e^(i(n+1)θ)(f'−nf/r).

For lower mode j, P* produces upper mode j−1 with radial factor −i(g'+jg/r). Thus a full two-component angular channel consists of upper n and lower n+1, both with total angular momentum n+1/2 under −i∂_θ+σ_3/2. The author integer n refers to the upper component. In particular, its term “nonradial” means the upper-component projection onto n≠0; it does not mean the modulus is nonradial.

With radial measure r dr, integration by parts gives

    L_n=−r^−1∂_r(rw∂_r)+n²w/r²+n w'/r+2m−V.

The sign of n w'/r is positive, and omitting that term or forgetting the n+1 lower index would change the result.

### Factorization and passage to infinitely many modes

For k=|n| and h_n=r^k(μ²+r²)^(−p/2), direct independent calculation gives

    L_n h_n=c_n h_n,
    c_n=2n/μ for n≥0,
    c_n=2|n|(p−2)/(pμ) for n<0.

On a compact radial annulus, expanding f=h_ng and integrating a total derivative proves the exact identity

    Q_n[f]=∫r w h_n² |g'|² dr+c_n∫r|f|² dr.

The calculation works for complex g by taking the real cross term. Positivity of h_n on the open radial interval is sufficient; high-mode h_n need not belong to L². There is therefore no finite-mode truncation assumption in the lower bound.

A smooth compactly supported u can first be cut off near zero with a logarithmic radial cutoff. Since w and u are bounded there, the additional derivative energy is O(1/|log ε|); the remaining terms converge by dominated convergence. Radial weights then give exact Parseval decompositions for L² and sqrt(w)P, with the shifted Fourier index still orthogonal. Finite Fourier sums converge in the graph/form norm. Boundedness of 2m−V passes the potential term to the limit. Finally the definition of the closure extends the inequalities to the full form domain.

Every c_n is nonnegative and every n≠0 satisfies c_n≥2(p−2)/(pμ)=4m/p. Summing the mode inequalities therefore proves Q≥0 and Q[u]≥(4m/p)‖u_nr‖². No claim about competing potentials is used.

### Kernel

If Q[u]=0, the nonradial bound removes every n≠0 component. In the radial sector, apply the factorization on compact subintervals to a form-core approximation; local H¹ convergence and lower semicontinuity give (f/h_0)'=0. Hence f is a constant times h_0. Conversely h_0 and its weighted derivative are integrable; cutoff errors vanish. Thus the scalar kernel is exactly the complex span of h_0. Its reconstructed lower component is i(r/μ)h_0 e^(iθ), which is H¹ when p>2 and recovers the author threshold spinor up to its scalar normalization.

## 6. Sharpness, and the full-spinor distinction

The scalar function u_−1=(x_1−ix_2)(μ²+r²)^(−p/2) is smooth at the origin and has L² and weighted P-energy tails of order ∫r^(3−2p)dr. It therefore lies in the form domain for every p>2. Infinity-cutoff errors are O(R^(4−2p)) and tend to zero. The factorization gives equality at 4m/p, so this is an attained sharp scalar-form constant.

However, with this precise upper function, the second Dirac row reconstructs

    v=−i/(pμ) (μ²+r²)^(−p/2) [2μ²+(2−p)r²].

For p>2 its nonzero leading tail is r^(2−p). Hence v∈L² if and only if p>3, with logarithmic failure at p=3. This is why the scalar form domain must not be identified with a domain of full H¹ pairs under the unbounded inverse V^−1. Even for p>3 this pair is not a threshold eigenspinor: its first row equals c_−1u, which is nonzero. Smooth compactly supported approximants do reconstruct H¹ pairs and approach the same scalar quotient, but that does not convert the quotient into a Dirac eigenvalue gap.

The weighted-modulus counterexample is also correct. For a nonzero real f supported in r>μ and u=f(r)e^(−iθ), the difference between weighted P-energy and weighted modulus-gradient energy is

    2π/(pμ) ∫(μ²/r−r)f² dr < 0.

Its sign is strict. It refutes that particular weighted scalar-reduction shortcut, not the fixed-potential theorem or the global conjecture.

## 7. Source, dataset, and prior-attempt verification

The complete pinned problems and prior-report corpus files were independently read and rehashed, totaling 149,266,659 bytes. Their hashes and sizes match the repository manifest read afresh at commit `24ae23df9ad6c9def619cdbdf2ec8066f506788f`. There are 15,458 problem records and 6,701 prior-report entries. The numeric ID matches uniquely. The statement hash matches the complete catalog, whose Git blob ID was also recomputed and checked against the repository listing.

The review binding was independently rebuilt using the repository rule SHA256(json.dumps([problem, prior_report], sort_keys=True)); it equals `4770883cfbb578cb13938241c495d2f9967f78602a9419ecf905c240f2fbd149`. The exact prior-report key OWR-14297742-004 is absent. This absence says nothing about other keys, external literature, or private research. The source record's older literature assessment was not accepted as a current proof of open status.

All five complete source PDFs were independently rehashed against the recorded fingerprints. Their actual inspection scope and current official-site checks are in SOURCE_REVIEW.json. The audit adds a relevance screen of the two-dimensional spinor CKN preprint [arXiv:2506.08318](https://arxiv.org/abs/2506.08318): its power-weighted interpolation and coupled linearized-operator problem is distinct from this fixed massive endpoint problem. Neither it nor the three-dimensional [CKN paper](https://arxiv.org/abs/2504.16909) supplies the missing global bound.

The public [Nice slides](https://www.ceremade.dauphine.fr/~dolbeaul/Lectures/files/Nice-5-2-2026.pdf), slide 32, were independently rendered and still state the conjecture. Their title-slide date inconsistency is preserved. A current author publication list and the August 2026 institutional seminar description were also screened. This is bounded evidence, not a universal open-problem certificate.

At the pinned repository snapshot, the actual attempts directory has 62 entries, the target path returns 404, and exact-path commit history is empty. Fresh PR searches for the numeric ID and “Aubin” returned no entries; “Dirac” returned unrelated records, inspected by title and purpose. The related-target group file does not list this ID. These checks do not cover deleted branches, private work, or unindexed material. The attempted live problem-page and Hugging Face row reads were unavailable; no live-row identity match is asserted. Complete pinned-file identity is independently established.

## 8. Retained scope and stopping point

The missing result is a_*≥A uniformly over admissible potentials, equivalently the missing upper bound for the limiting variational supremum, together with the appropriate equality/attainment description. The explicit candidate supplies only the reverse bound. The width branch, Pohozaev identity, boundary concentration and frozen-potential Schur positivity do not fill that gap. No endpoint-resonance classification, optimizer uniqueness, radial/global minimization theorem, nonlinear Hessian stability, or novelty result is certified.

Keep the original status unresolved and 5/5. The audit and its clarifications are verification of the existing scoped claims, not a sixth proof approach. The safe audit payload contains authored review prose, exact code/results, hashes, byte counts and public bibliographic/provenance metadata only. No source PDF, source extract, image, raw corpus, or private coordination record belongs in it.
