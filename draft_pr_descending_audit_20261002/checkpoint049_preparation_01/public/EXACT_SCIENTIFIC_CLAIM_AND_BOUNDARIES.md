# Exact claim and boundaries

Let F be Q or R. Define Q_F(g) as the finite sums sum_i a_i^2 + g sum_j b_j^2 with polynomial factors a_i,b_j in F[x,y,z], allowing arbitrary finite degrees. A rational certificate means rational polynomial square factors, equivalently rational positive-semidefinite Gram data. Requiring only rational coefficients in real-SOS multiplier polynomials is a weaker condition and is not the obstruction asserted here.

Take g=1-x^2-y^2-z^2 and the classical Scheiderer quartic

```text
f=x^4+xy^3+y^4-3x^2yz-4xy^2z+2x^2z^2+xz^3+yz^3+z^4.
```

Set p=1+f. Specify moments indexed by every alpha in N^3 of total degree at most four: m_(0,0,0)=1, m_(4,0,0)=-1, all others zero. The nonnegative representing-measure convention is essential.

The closed unit ball K={g>=0} is nonempty and compact, and the displayed rational ball generator makes Q_Q(g) Archimedean. The rational 35-entry vector m has no nonnegative representing measure, even on R^3, because its x^4 moment is negative. Its linear moment functional satisfies L_m(p)=0. The fixed p has minimum one on K and belongs to 1+Q_R(g), but not to 1+Q_Q(g), at every finite multiplier degree. The proof is the classical rational-SOS obstruction for f followed by the local degree-four argument at the origin. Higher-degree weighted terms may cancel; the proof does not rely on their inability to cancel.

The real certificate is the identity 4f=U^2-beta V^2 displayed in paper.tex, for a negative real root beta in (-2,-1) of beta^3-4beta-1. The exact checker clears denominators and reduces modulo that cubic. Numerical approximations are unnecessary.

The following controls limit the conclusion:

- The moment matrix M_2(m) is not positive semidefinite: its diagonal indexed by x^2 equals m_(4,0,0)=-1. No PSD-input case is established.
- The same m has the rationally certifiable separator q=1+x^4, with L_m(q)=0 and q-1=(x^2)^2. The claim does not exclude every rational separator.
- The polynomial p itself belongs to Q_Q(g), by Powers' strictly positive rational ball theorem. This does not imply p-1 belongs to that module.
- For every rational c>1, cp-1 is strictly positive on K, so cp belongs to 1+Q_Q(g); L_m(cp)=0. For c=1 the normalized rational obstruction holds. For c<1, cp(0)-1<0, so even a real normalized certificate is impossible.
- A rational-coefficient list of real-SOS multipliers already exists: sigma_0=f, sigma_1=0. It is rational square factors, rather than that weaker coefficient condition, that are impossible.
- The companion arXiv:2302.06927v1 Corollary 2 has a strict-margin sufficient regime min_K p>1. This minimum-one example is outside that regime. No conclusion about a stronger regime's present openness follows.
- No new quartic, Galois construction, local obstruction, first irrational-infeasibility result, algorithm, minimal relaxation degree, or general Archimedean-descent theorem is claimed.

The example exhibits the phenomenon asked about in the literal fixed-polynomial OWR question under the explicitly stated rational-square convention. That convention is supported by the question's rational-SOS context; the source does not formally define it, and no unpublished author intention or approval is asserted. The contribution is an explicit application and clarification of normalization, with established ingredients credited in the note.

The finite 2,059-check replay is supporting evidence for specified identities and representative controls. The all-degree and Galois conclusions follow from the written proofs and credited theorems, not from finite searches or nonnegativity samples. The literature comparison is bounded; it proves no worldwide absence or current-openness statement.
