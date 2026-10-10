# Initial trace and source scope audit

This audit concerns the inspected saved arXiv:math/0304481v2 PDF, labeled13 May2003 with a generated title-page date8 November2018. It is **not** a claim about an independently inspected journal proof. The journal landing page was read, but its full subscription PDF was not obtained. A fresh public-web retrieval of the v2 PDF returned a cache miss.

## Spacetime convergence does not include the initial trace

The v2 paper's Young-measure topology in §3.2 uses integrals against dt dx over the spacetime cylinder. In Proposition2, printed p.22, the functional displayed before(32) also includes an integral of the initial entropy against phi(0,x), and the text treats this full functional as continuous in that topology.

That continuity does not follow from the stated topology. Fix distinct states A,B in D and let U_n(t,x)=B for0<=t<=1/n and U_n(t,x)=A for t>1/n; smooth the time transition if desired. Then U_n→A strongly in every finite spacetime Lp, and their spacetime Young measures converge, while U_n(0,x)=B. The initial entropy pairing is not controlled. In the dt dx quotient it is not even a well-defined function of an equivalence class without extra trace information.

This counterexample concerns the topology, not a solution of(L) and not a hydrodynamic counterexample. The stochastic evolution could provide extra control; that control must be stated and proved rather than inferred from spacetime convergence.

## Weak initial profiles do not control nonlinear initial entropy

On the unit torus let U_n(x) alternate equally between A=(0,1) and B=(0,−1) on intervals of length1/(2n). Then U_n converges weakly to U_0=(0,0). With c=1/2, the affine entropy S_c=rho+c u−c² takes values1/4 and−3/4, so

∫|S_c(U_n)| dx=1/2,    ∫|S_c(U_0)| dx=1/4.

Thus weak convergence of conserved fields does not identify the nonlinear initial entropy. This can also occur with mesoscopically resolved microscopic species blocks whose physical width goes to zero but is much larger than the averaging width. The scalar-face dynamics of such a configuration may erase that layer for every positive time; the example does not dispute that possibility.

Fritz–Nagy2006 explicitly distinguishes a weak initial profile from the strong initial entropy condition in its §2.3, printed pp.374–375. Its scalar trace repair in §5.2, p.389, invokes a scalar uniqueness theorem. The independently retrieved Chen–Rascle paper defines precisely the scalar weak Cauchy equation plus interior entropy inequalities and proves the missing strong initial continuity when the scalar flux has no affine interval. This supports the scalar-face theorem in REPORT.md. It cannot be imported without proof into the genuine two-component interior.

## Literature check and limitations

The inspected Bressan–Goatin preprint supplies exact state-domain and strong-in-time hypotheses. The 2025 Bressan–Marconi–Vaidya paper is a useful later prior-result lead, but its Temple semigroup construction does not by itself verify stochastic-limit membership or resolve the degenerate state. These are source-scope findings, not new counted proof attempts. No broad novelty or exhaustive-open-status certificate is made.

Sources and byte/hash metadata appear in EXACT_TARGET.md and SOURCE_METADATA.json. No third-party source text or source PDF is included in this authored packet.
