# Grushin converse Bessel pair formulation audit

14 October 2026. Source-scope review only. No converse is proved or disproved here.

## Result

The question in Prasun Roychowdhury's contribution to Oberwolfach Report 14/2025 is located in the last paragraph of printed page 606, PDF page 28. It points to two different forward results: Ganguly–Jotsaroop–Roychowdhury (GJR), Corollary 3.1 and Theorem 1.3. The report does not supply a fully quantified conjecture. Its two inequality families, version-dependent dimension range, weight signs, endpoint conventions and solution-dependent remainder must be kept distinct. [OWR](https://ems.press/content/serial-article-files/51358?nt=1)

The Hardy antecedents can be written without presupposing the desired positive solution. The cited Hardy–Rellich display already contains such a solution. Keeping its source meaning in a converse antecedent would assume the conclusion. Removing its remainder, or substituting an independently quantified positive function, creates a separate proposed formulation. Neither substitution is an explicit formula in the OWR paragraph.

A conservative acceptance contract therefore preserves the source-faithful Hardy branches and records unresolved choices for Hardy–Rellich. A result for strictly positive leading weights, only the newer dimension range, or a newly specified remainder-free inequality must carry those restrictions. It cannot silently settle every interpretation of the original question.

## Primary source versions

- OWR: *Mini-Workshop: Hardy Inequalities in Discrete and Continuum Settings*, 2025, pp.579–614; Roychowdhury's contribution pp.606–607. The question is on p.606 and the cited references are on p.607. [DOI](https://doi.org/10.4171/OWR/2025/14)
- GJR v1, submitted 8 April 2024: *Hardy and Rellich identities and inequalities for Grushin operators via spherical vector fields and Bessel pairs*. Setup p.2; Theorem 1.3 p.6, inequality (1.5), side condition (1.6); Definitions 2.1–2.2 p.13; Corollary 3.1 p.14. Its stated range is n≥1 and Q≥3. [Versioned PDF](https://arxiv.org/pdf/2404.05510v1)
- GJR v2, submitted 20 March 2025: setup n≥2 and Q≥4; Theorem 1.3 pp.6–7, inequality (1.6), condition (1.7); Definitions 2.1–2.2 pp.13–14; Corollary 3.1 p.15. [Versioned PDF](https://arxiv.org/pdf/2404.05510v2)
- GJR v3, submitted 3 October 2026: *Hardy and Rellich identities and inequalities for Baouendi-Grushin operators via spherical vector fields*. Setup p.2; Theorem 1.3 p.7; Definitions 2.1–2.2 p.14; Corollary 3.1 p.16. The stated range remains n≥2 and Q≥4, and the theorem numbering and displayed formulas relevant here agree with v2. The arXiv record labels this final and to appear in *Annali della Scuola Normale Superiore di Pisa, Classe di Scienze*. The PDF itself gives 6 October 2026 as its document date; that is distinct from its listed 3 October submission date. [Versioned PDF](https://arxiv.org/pdf/2404.05510v3), [arXiv record](https://arxiv.org/abs/2404.05510)

The OWR reference uses the 2024 title matching v1 but does not select a version. The March 2025 workshop preceded v2, while report publication followed v2. These facts leave the intended historical/current dimension scope unresolved. This audit does not infer an erratum or a reason for the change.

## Source-fixed setting

Write z=(x,t) in R^n×R and use

\[
X_i=\partial_{x_i},\qquad Y=|x|\partial_t,\qquad
\nabla_G=(\nabla_x,|x|\partial_t),\qquad
L_G=\Delta_x+|x|^2\partial_t^2.
\]

The homogeneous dimension, gauge, and gauge-gradient factor are

\[
Q=n+2,\qquad \rho(x,t)=(|x|^4+4t^2)^{1/4},\qquad
\psi=|\nabla_G\rho|^2=|x|^2/\rho^2.
\]

Fix 0<R≤∞, put B_R={z:ρ(z)<R}, and let T_R=C_c^∞(B_R\{0}), with real-valued tests and Lebesgue measure dz=dx dt. GJR's radial derivative ∂ρ is differentiation in its polar coordinates, with angular variables fixed. Its radial gradient has squared norm ψ|u_ρ|². This is the α=1, one-vertical-variable setting. The source does not automatically encompass arbitrary Baouendi–Grushin parameters, multiple vertical variables, or arbitrary vector fields. [GJR v3, pp.2,10–11](https://arxiv.org/pdf/2404.05510v3)

The weights are one-variable radial profiles V(r),W(r) on (0,R), evaluated at ρ in the integrals. GJR Definition 2.2 uses C¹ profiles. Define the exact target property

\[
B_Q(V,W;R):\quad
\text{there is a positive solution }f\text{ on }(0,R)\text{ of }
(r^{Q-1}Vf')'+r^{Q-1}Wf=0.
\]

The coefficient of W is exactly one. A positive solution for cW at an unspecified c>0, on only a smaller interval, or merely near an endpoint is not this conclusion. Definition 2.1's ordinary Bessel equation is (Vf′)′+Wf=0; the cited Grushin results instead use Definition 2.2. An ordinary Bessel-pair notation must therefore absorb the r^(Q−1) factors explicitly. [GJR v3, p.14](https://arxiv.org/pdf/2404.05510v3)

The source says positive solution but does not separately specify a solution regularity convention in its definition. A later formal statement must specify classical versus flux-classical or weak meaning, especially if V is allowed to vanish. It must not replace positive by nonnegative or replace a solution by a supersolution without establishing the needed connection.

## Hardy branches whose formulas are fixed

Corollary 3.1 assumes B_Q(V,W;R) and V≥0 and gives both of the following, for every u∈T_R:

\[
H_G(V,W):\quad
\int_{B_R} V(\rho)|\nabla_Gu|^2\,dz
\geq \int_{B_R}W(\rho)u^2\psi\,dz;
\]

\[
H_\rho(V,W):\quad
\int_{B_R} V(\rho)\psi|u_\rho|^2\,dz
\geq \int_{B_R}W(\rho)u^2\psi\,dz.
\]

Consequently the source supports separately asking H_G⇒B_Q and H_ρ⇒B_Q, with all non-Bessel hypotheses stated explicitly. The second display is a radial-gradient inequality for all tests, not a statement restricting u to radial functions. A radial-only test formulation is a further branch or intermediate assertion whose relation to these premises must be justified. The OWR wording does not select just one of the two corollary displays. This audit does not establish any converse or equivalence among these premises. [GJR v1, p.14](https://arxiv.org/pdf/2404.05510v1), [GJR v3, p.16](https://arxiv.org/pdf/2404.05510v3)

## Hardy–Rellich branches requiring an explicit choice

For notation, put

\[
A_V[u]=\int_{B_R}V(\rho)\frac{(L_Gu)^2}{\psi}\,dz,
\]

\[
D_{V,W}[u]=\int_{B_R}\left[W(\rho)+(Q-1)
\left(\frac{V(\rho)}{\rho^2}-\frac{V'(\rho)}{\rho}\right)\right]|\nabla_Gu|^2\,dz,
\]

\[
E_{V,f}[u]=\int_{B_R}V(\rho)f(\rho)^2
\left|\nabla_G\left(\frac{u_\rho}{f(\rho)}\right)\right|^2\,dz,
\qquad
S_Q[V]=(Q-5)V/r^2+3V'/r-V''.
\]

Theorem 1.3 assumes B_Q, a positive solution f of that ODE, V≥0, and S_Q[V]≥0, then asserts

\[
A_V[u]\geq D_{V,W}[u]+E_{V,f}[u]\qquad (u\in T_R).
\]

The remainder and its dependence on the ODE solution are part of the cited display. The source defines the pair at C¹ regularity but writes V″ in the side condition; a pointwise classical formulation needs an explicit additional differentiability convention, for example V∈C²(0,R). [GJR v1, p.6](https://arxiv.org/pdf/2404.05510v1), [GJR v3, p.7](https://arxiv.org/pdf/2404.05510v3)

There are at least three different readings:

1. **Preserve the source meaning of f.** If a converse antecedent already stipulates that f is a positive solution of the displayed ODE, B_Q is already assumed. This is not a substantive necessity theorem.
2. **Proposed remainder-free core.** Ask whether A_V[u]≥D_{V,W}[u] for every test forces B_Q. The forward theorem supplies this core after dropping the nonnegative remainder, but this solution-free antecedent is an interpretive choice, not an additional displayed conjecture in OWR. Record separately whether S_Q[V]≥0 is retained. A theorem without that restriction would have a wider weight class than a converse restricted to the forward hypotheses.
3. **Proposed independent-function remainder.** Ask whether existence of a separately specified positive function g, with no ODE assumption, such that A_V≥D_{V,W}+E_{V,g} for all tests forces B_Q. The same g must serve every test if that is the chosen quantifier. Requiring the inequality for every g, choosing g separately for each u, or concluding that this particular g solves the ODE are different statements. None is selected by the OWR paragraph.

Deleting the correction (Q−1)(V/r²−V′/r), replacing the right side by a weighted u² integral, or changing to a (Q+2)-dimensional Bessel pair would create still other problems. GJR Proposition 7.1 explicitly uses a shifted pair involving W+QV′/r; it is not permission to rename the pair in the question.

## Weight signs and endpoints cannot be silently repaired

**Literal nonnegative branch.** Definitions 2.1–2.2 state C¹ weights; Corollary 3.1 and Theorem 1.3 add V≥0. They do not explicitly require V>0 or W>0. The printed class therefore admits a vanishing leading coefficient, potentially including V≡0, and does not exclude nonpositive W. Such a branch may have elementary degenerate behavior unrelated to the regular second-order Bessel equation. Any objection using that behavior must be reported as a literal-degenerate branch finding; it does not, without clarification, settle the likely intended strictly-positive-weight problem. No degenerate example is tested or certified here.

**Regular leading-weight branch.** Requiring V>0 is a natural way to obtain the usual regular ODE interpretation on compact interior subintervals, but it narrows the printed V≥0 class. Independently, W real-valued, W≥0 and W>0 are different choices. No default sign repair is authorized by the OWR paragraph. If one of these classes is adopted for a theorem, the remaining source-relevant classes must stay visibly unresolved or excluded by an explicit scope decision.

**Open-interval convention.** GJR asks for positivity on (0,R). It does not impose an endpoint value, normalization, boundedness, integrability or derivative limit for f at 0 or R. It does not require f to extend to R, or specify behavior at infinity when R=∞. Tests are compactly supported away from the origin and outer boundary. A result only under added endpoint assumptions, or only for unpunctured-ball tests, must be identified as such.

**Comparison with Euclidean references.** The inspected 2007 Ghoussoub–Moradifam author manuscript has additional assumptions: its Theorem 2.1 uses positive weights, integrability of r^(d−1)V near zero and divergence of the reciprocal integral; its Theorem 3.3 includes endpoint decay and a different weight condition involving both V and W. It also uses a Bessel-pair scale convention involving β(V,W;R). Those hypotheses and conventions cannot be imported merely because OWR cites the Euclidean analogy. The inspected manuscript is arXiv:0709.1954v1, not verified as the full 2011 journal version of record. [Historical manuscript](https://arxiv.org/pdf/0709.1954v1), [journal record](https://doi.org/10.1007/s00208-010-0510-x)

## Domain and test-class gates

- The source punctures only the origin. T_R can meet the axis x=0 at t≠0, where ψ=0. For Hardy–Rellich, an exact formalization must say how A_V is interpreted there and whether tests with infinite weighted energy are allowed. Removing that axis, demanding finite energy or requiring strict regularity of the quotient are changes requiring explicit treatment. No finite-energy equivalence is certified here.
- ∂ρu in the remainder is the source's polar radial derivative, not ∂|x|u. Gauge-radial functions and Euclidean-radial functions are different classes.
- Passing from a compactly supported radial u(r) to v(r)=u′(r) does not automatically produce arbitrary compactly supported v. The primitive must satisfy the original support requirements. A later Hardy–Rellich necessity argument must account for this test-class issue rather than citing a one-dimensional equivalence on a different class.
- An unresolved future proof question is whether radial derivatives, which have zero ordinary integral, are dense in the relevant weighted one-dimensional energy space under S_Q[V]≥0. This is a proposed proof gate, not a source assertion or a density result established by this audit.
- The desired solution is global on the fixed (0,R). A necessity result on every smaller compact annulus or only after reducing R is not by itself the requested conclusion.
- The historical n=1, Q=3 case remains a separate branch if one works only with the current n≥2, Q≥4 source. No bound on Q independent of Q=n+2 should be silently substituted.

## Conservative acceptance contract

Before a mathematical pass, identify the exact branch by the tuple: source version; dimension range; fixed R; weight regularity and signs; endpoint assumptions; test class and energy convention; Hardy display or Hardy–Rellich antecedent; side-condition choice; solution meaning and coefficient normalization.

A positive resolution must establish the exact B_Q conclusion on the entire (0,R), for every admissible pair satisfying the chosen inequality. It must handle test-class/endpoint passages and the axis convention, and must not assume a positive ODE solution in its antecedent. A negative resolution must give an admissible pair satisfying the selected inequality for every allowed test and establish failure of that exact B_Q property. A numerical check or a few trial functions cannot establish those universal requirements.

The following scope dispositions are mandatory:

- **Source formulas fixed, mathematics unattempted:** the two Hardy displays and the literal forward Hardy–Rellich display.
- **Formulation unresolved:** which Hardy–Rellich converse antecedent is intended; degenerate versus regular leading weights; any W-sign restriction; solution regularity for vanishing V; any endpoint/energy conventions; and historical versus current dimension scope.
- **Restricted result only:** work imposing V>0, W>0, new endpoint hypotheses, only Q≥4, or a specific newly selected Hardy–Rellich antecedent, until its relation to the broader source question is explicitly established.
- **No full-resolution credit:** a circular ODE-solution premise; an isolated degenerate-weight objection presented as settling the regular problem; a result only for some rescaling cW; or a result for one branch presented as answering all Hardy/Hardy–Rellich branches.

A full source-question disposition requires either coverage of the remaining source-relevant branches or an explicit, documented choice of intended scope. Until then, retain the question as formulation-pending with no mathematical resolution claimed. This audit supplies a statement map and acceptance criteria, not an openness certificate or proof audit.
