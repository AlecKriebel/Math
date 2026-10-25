# Independent geometric and closed-form audit: PR 765 / problem 30005613

Audit family: geometry, point capacity, and closed Dirichlet forms.
Prepared 2026-10-16 UTC. Candidate head: 021518f6f65a86658f72e0b31bfa0814bf1aa25d.
Author PROOF.md SHA256: 5d1bab0b62ac5f78c69b0d82babd0b79fa4944097470fa760fdb3c485e362a20.

## Result and exact scope

The mathematical candidate passes this independent family audit. I found no mathematical correction required within its stated existential scope. The finite-window analytic input can be proved directly from the form spaces; it does not merely transfer the main difficulty to an unsupported continuity assertion. My complete cross-check of the finite-rank argument likewise found no gap. This is an AI audit of the candidate, not human peer review or a historical-priority certification.

For each d>=2 the candidate chooses both growing cube half-widths and positive shrinking zero-thickness interface apertures. The resulting open connected set has a Dirichlet Laplacian, defined by the closed form on H_0^1, with a complete eigenbasis, spectrum and essential spectrum [0,infinity), no zero eigenfunction, and zero absolutely/singular continuous spectral subspaces. Countably many positive eigenvalues are dense; the claim does not make every spectral point an eigenvalue. No conclusion for arbitrary preassigned towers, boundary smoothing, Neumann conditions, positive-length corridors, or effective aperture sizes is being audited.

The initial independent position was written at 2026-10-16T04:42:23.601874Z, SHA256 41cf73751f8991b0860fe69e3811a3609cc2f42196d4312a5ec4d86086bcc8dd, before reading inherited audit verdicts or the other new family's work. No inherited mathematical audit or other new-family derivation was used subsequently. The later reading of SNAPSHOT.json exposed its queue-row summary but supplied no mathematical step below.

## Source question, version, and quantifiers

The official OWR contribution, printed pp.2077-2078, asks for an example of this tower geometry with both continuous spectral types absent. The report does not quantify over every preassigned tower. Its volume/report year is 2023; the EMS publisher lists publication on 18 April 2024. The cached label 2024 therefore reflects publication timing, not a different report. [Official OWR report](https://ems.press/content/serial-article-files/47475), [publisher metadata](https://ems.press/journals/owr/articles/14297736).

The candidate uses the parameter freedom of KL, not a replacement geometry: in Section 3, PDF p.4, centers after the first are left to be chosen during construction; p.5 chooses each new cube before opening the next window. Its Section 5 asks the continuous-spectrum question. Thus the candidate's existential cube choice is within the cited construction. The stronger universal fixed-tower theorem is neither supplied by these sources nor proved here. [KL arXiv:2205.08172v2, 20 May 2024](https://arxiv.org/pdf/2205.08172v2).

The 23 September 2026 survey, Open Problem 1 on PDF p.16, restates the remaining singular-continuous question in this example. Visual inspection matters: its preceding point-spectrum formulas have closure bars lost by text extraction. The candidate explicitly supplies the correct spectral-type meaning. This is a source-status observation, not an exhaustive subsequent-literature search. [Krejcirik arXiv:2609.28602v1](https://arxiv.org/pdf/2609.28602v1).

## 1. Exact finite geometry and common L2 space

Let p=(x_n+a_n)e_1, D_0=O_n union Q_a(x), x=x_n+a_n+a, a>a_n+1, and D_delta=D_0 union Q_delta(p), with 0<delta<a_n.

For y in Q_delta(p) with y_1<p_1, its first coordinate lies strictly in the last old cube's first-coordinate interval; all transverse coordinates have absolute value <delta<a_n. Hence y lies in that old cube. If y_1>p_1, the same argument with a> a_n puts y in the new cube. Consequently

D_delta minus D_0 = {y_1=p_1, |y_j|<delta for j=2,...,d}.

This is an open window in a zero-thickness interface screen, a set of d-dimensional Lebesgue measure zero. D_delta is open because it is the union of three open sets, including the full connector cube; it is connected because that connector has nonempty open overlaps with both formerly separated pieces. Treating the displayed face alone as an open subset of R^d would be wrong; the full union establishes openness.

Thus all these finite domains have canonically identical L2 spaces modulo null sets, although their H_0^1 spaces change. The disconnected form space splits into H_0^1(O_n) direct_sum H_0^1(Q_a(x)): split compactly supported smooth approximants over its two components, then take closure. This also proves the corresponding operator/resolvent direct sum.

Previous windows stay fixed. The argument only uses that O_n is a bounded open set containing its last cube. No smoothness of the old screens or aperture edges is needed.

## 2. Bounded-domain compactness requires no boundary regularity

Choose one bounded open rectangular box B containing every D_delta for 0<delta<delta_*. By definition and approximation by compactly supported smooth functions, zero extension maps H_0^1(D_delta) isometrically into H_0^1(B); its image is closed in H^1(B). The same holds for D_0 and O_n. Poincare in B gives a positive lower spectral bound. The compact embedding H_0^1(B) into L2(B) gives compact Dirichlet resolvents on every bounded open subset in question.

In particular, neither a global Lipschitz-boundary theorem nor compact embedding of H^1 of a slit domain is needed. The form domain is H_0^1, not unrestricted H^1.

## 3. Point cutoffs, including the dimension-two boundary case

The key local fact is that a point can be removed at vanishing H1 cost in d>=2. Here is an explicit usable construction.

Take a smooth real function theta with theta=0 on (-infinity,0], theta=1 on [1,infinity), and 0<=theta<=1.

For d>=3 define zeta_r(y)=theta(|y-p|/r-1). It vanishes on B_r(p), equals one outside B_2r(p), and

integral |gradient zeta_r|^2 =
|S^(d-1)| r^(d-2) integral_1^2 |theta'(s-1)|^2 s^(d-1) ds -> 0.

Also ||1-zeta_r||_2^2 <= volume(B_2r) ->0.

For d=2 and 0<r<1 define, away from p,

zeta_r(y)=theta(log(|y-p|/r^2)/log(1/r)),

and set zeta_r=0 on B_(r^2)(p). It equals one outside B_r(p). The constant values near the endpoints make this a smooth cutoff, including at p. Polar integration gives

integral |gradient zeta_r|^2 =
(2*pi/log(1/r)) integral_0^1 |theta'(s)|^2 ds ->0,

while ||1-zeta_r||_2^2 <= pi*r^2 ->0. A linear radial cutoff alone has nonvanishing energy in d=2; the logarithmic profile is essential to this argument.

For bounded u in H^1(B), zeta_r u ->u in H^1(B): the terms (1-zeta_r)u and (1-zeta_r)gradient u tend to zero by dominated convergence, and ||u gradient zeta_r||_2 <= ||u||_infinity ||gradient zeta_r||_2 ->0.

For arbitrary u, first truncate its real and imaginary parts at magnitude M. The usual Sobolev Lipschitz chain rule, with truncation fixing zero, preserves every H_0^1(D) and gives convergence to u in H1 as M->infinity. This avoids the invalid estimate that would bound an arbitrary Sobolev function pointwise.

## 4. Intersection of shrinking form spaces

Embed V_delta=H_0^1(D_delta) and V_0=H_0^1(D_0) into H_0^1(B). Clearly V_0 is contained in every V_delta. I claim

intersection_(0<delta<delta_*) V_delta = V_0.        (G1)

For bounded u in the intersection, choose the cutoff from Section 3 and choose delta so small that Q_delta(p) is contained in the cutoff's zero ball. Approximate u by phi_m in C_c^infinity(D_delta). The functions zeta_r phi_m are smooth, and their supports are compact subsets of D_0: the only points added by the connector lie strictly inside the zero ball. Multiplication by the fixed smooth bounded cutoff is continuous in H1. Thus zeta_r u is in V_0. Let r->0 and use Section 3 and the closedness of V_0. This puts bounded u in V_0. Apply the argument to truncations and let M->infinity to prove (G1) for arbitrary u.

All old windows remain present in D_0 throughout this proof. The cutoff does not replace them or assume that all apertures are closing simultaneously.

This also avoids ambiguity about writing H_0^1(D_0 union {p}) when that union is not open. The checkable statement is the intersection (G1) of ordinary open-domain form spaces.

## 5. Mosco and strong resolvent convergence

Let delta_j->0, without requiring that this sequence be monotone. If u_j in V_delta_j converges weakly in H1(B), then for every fixed s>0, eventually u_j belongs to V_s. A norm-closed linear subspace is weakly closed, so its weak limit lies in every V_s and hence in V_0 by (G1). This is the weak-limit half of Mosco convergence.

For any v in V_0 the constant choice v_j=v lies in every V_delta_j and converges strongly in H1. This is the recovery half.

One can derive resolvent convergence without invoking a black-box equivalence. Use

b(u,v)=integral_B(gradient u dot conjugate(gradient v)+u conjugate(v)).

For fixed f in the common L2 space, u_j=R_delta_j f is uniformly bounded in H_0^1(B), since b(u_j,u_j)=<f,u_j> and ||u_j||_b<=||f||_2. Every weak H1 limit belongs to V_0 and satisfies b(u,v)=<f,v> for v in V_0. Uniqueness gives u=R_0 f. The variational identities also imply convergence of b-norms, so weak convergence improves to strong H1 convergence. In particular R_delta f->R_0 f strongly in L2.

## 6. Upgrade to operator-norm resolvent convergence

Strong convergence by itself would not justify spectral-projection control. Here bounded containment supplies the missing uniform compactness.

For every delta and every ||f||_2<=1, the variational estimate above puts R_delta f in a fixed bounded ball of H_0^1(B). These images are collectively precompact in L2(B).

Suppose operator-norm convergence failed. There would be delta_j->0 and unit f_j with ||(R_delta_j-R_0)f_j|| bounded below by a positive constant. Pass to f_j weakly converging to f. Collective compactness gives a subsequence of u_j=R_delta_j f_j strongly converging in L2 and weakly in H1. By (G1) its limit u is in V_0. Testing against v in V_0 gives b(u,v)=<f,v>, so u=R_0 f. Since R_0 is compact, R_0 f_j->R_0 f strongly. The claimed lower bound is contradicted. Therefore

||(A_D_delta+1)^(-1)-(A_D_0+1)^(-1)|| ->0.        (G2)

This is a complete direct reconstruction of the candidate's external analytic input for this geometry. It is not a finite-computation inference.

The source check agrees: KL Proposition 2.2 requires nested exterior approximation, the correct interior of the intersection, and stability under its boundary set Gamma. Here intersection D_delta = D_0 union {p}, whose interior is D_0 for d>=2; the shrinking window leaves no other persistent added point. For a decreasing aperture sequence Gamma={p}. Its displayed Gamma includes closures over tail unions, confirmed visually. The point cutoff argument supplies the required capacity stability. Proposition 2.3 additionally requires containment in a fixed bounded set and yields convergence in operator norm of zero-extended resolvents. These hypotheses hold stage by stage, including in d=2. No uniform estimate as n grows is required, because each new aperture is chosen only after finitely many parameters are fixed.

A source explanatory sentence mentions equal closures. Equal closures alone would not imply a null symmetric difference for arbitrary open sets; this audit instead uses the explicit interface identity in Section 1. Thus no inappropriate generalization of that sentence enters the proof.

## 7. Nonresonance and complete spectral clusters

For a cube of half-width a, eigenvalues are pi^2 |m|^2/(4a^2), with every m_i a positive integer. For finite protected S and a in a bounded interval, resonance with lambda in S bounds |m|^2. Only finitely many multiindices occur; each forbids at most one a. The interval (a_n+1,a_n+2) therefore contains an admissible choice.

At the disconnected limit, each protected eigenspace is precisely its old eigenspace, extended by zero; the new cube contributes none at that eigenvalue. By compact resolvent every protected eigenvalue is isolated with finite multiplicity. Choose disjoint small intervals with endpoints outside the disconnected spectrum. Under (G2), use isolated nonzero eigenvalues of the bounded resolvent and fixed contours to obtain norm convergence of their Riesz projections. The sum over any finite protected collection converges in norm.

Multiplicity and splitting do not invalidate this: the complete spectral cluster inside an interval is transported. Projections at norm distance less than one have equal rank by injectivity in both directions. No eigenvector phase choice or simple-spectrum assumption is needed.

## 8. Infinite union, local finiteness, and Hilbert-space identification

Write s_n=x_n+a_n. The recurrence gives s_n=2 sum_(j<=n) a_j, starting with left endpoint zero. Since a_(n+1)>a_n+1 and a_1=1, a_n>=n (strict for n>1); hence s_n->infinity at least quadratically. Every bounded subset of R^d meets only finitely many cubes and connectors. Apertures are positive and satisfy delta_n<2^(-n), so they shrink.

The nested connected open O_n have a connected open union O. It contains Euclidean balls of radius a_n, so is quasi-conical. Its measure is the sum of the cube measures, since the extra countable collection of faces is null; this sum is infinite. L2(O) is canonically the Hilbert direct sum of the cube L2 spaces, and their fixed sine bases give an orthonormal basis of L2(O).

For V=H_0^1(O), zero-extended V_n=H_0^1(O_n) are increasing closed subspaces. If phi is in C_c^infinity(O), its compact support is covered by the increasing open O_n; a finite subcover puts its entire support in one O_N. Thus the union V_n is dense in V. This compact-support argument actually does not need the additional local-finiteness fact.

With the same b inner product, the zero-extended finite-domain resolvent solution R_n f is the b-orthogonal projection of Rf onto V_n. Density proves strong H1 and hence strong L2 convergence R_n f->Rf. The norms are bounded by one. Norm resolvent convergence on the full infinite union is neither asserted nor needed here.

## 9. Cross-check of protected subspaces and completeness

At stage n all protected projections P_n^k are finite sums of complete eigenspaces, nested in k. New-cube nonresonance and (G2) allow one positive aperture satisfying the finitely many bounds ||P_(n+1)^k-P_n^k||<epsilon_n, k<=n, with unchanged ranks. The simultaneously required geometric upper bounds on delta are compatible with choosing it sufficiently small.

A new finite spectral cutoff can then contain all older protected clusters and approximate the current finite test family F_n. It is allowed to cease being a low-energy cutoff after later transport; this is an important and valid part of the construction.

For fixed k, summability of epsilon_n gives norm convergence P_n^k->P^k to an orthogonal projection of the same finite rank. Nesting passes to the norm limits. Each zero-extended P_n^k commutes with the zero-extended finite-domain resolvent R_n; using strong convergence R_n->R and norm convergence P_n^k->P^k gives RP^k=P^kR.

Each range(P^k) therefore reduces R. The resolvent of the actual Dirichlet Laplacian is injective, so its restriction to this finite-dimensional space has strictly positive eigenvalues. If Rv=mu v, mu>0, then v belongs to dom(A) and Av=(mu^(-1)-1)v. Thus range(P^k) is in the pure point spectral subspace. This explicitly prevents escape of a nonzero limiting vector to infinite energy.

For each fixed cube sine-basis vector f, it belongs to every sufficiently late F_n. The birth approximation error is <2^(-n), and the later projection tail is at most sum_(j>=n)2^(-j-2)=2^(-n-1). Hence ||(I-P^n)f||->0. The pure point subspace is closed and contains all P^n f, so it contains every basis vector and therefore all L2(O). Both continuous spectral subspaces vanish. This is a completeness proof, not merely a construction of dense eigenvalues or an application of trace-class invariance.

## 10. Actual operator Weyl sequences and the zero mode

Let chi in C_c^infinity(B_1(0)) have L2 norm one, choose |xi|^2=lambda>=0, and set r_n=a_n/2. With c_n the n-th cube center, define

u_n(y)=r_n^(-d/2) chi((y-c_n)/r_n) exp(i xi dot y).

It belongs to C_c^infinity(O), hence to the form-defined Dirichlet operator domain, where Au_n=-Delta u_n. Its norm is one. The product rule gives

||(A-lambda)u_n|| <= r_n^(-2)||Delta chi||_2
 +2|xi|r_n^(-1)||gradient chi||_2 ->0.

The supports are pairwise disjoint, so the sequence is orthonormal and therefore weakly null. It also escapes spatially. These are singular Weyl sequences for every lambda>=0, including lambda=0. Nonnegativity proves spectrum=essential spectrum=[0,infinity).

If Au=0, the form identity gives integral |gradient u|^2=0. A Sobolev function with zero weak gradient is constant on each connected open component, and O is connected. Infinite measure forces the L2 constant to be zero. Thus zero is a spectral limit and is not an eigenvalue.

## 11. Falsification controls and limitations

The independent controls.py uses only the Python standard library. Its saved CONTROLS.json reports PASS_DIAGNOSTICS_ONLY and checks 16,400 exact rational sample points across d=2,3,4,6: the connector adds exactly its middle-face points on those samples. Six radial cutoff scales distinguish vanishing logarithmic energy in d=2 from constant-energy linear cutoffs; they also illustrate vanishing linear energy in d=3 and divergence in d=1.

The analytic d=1 negative control is stronger than arithmetic: two touching intervals plus any positive window form (0,2), whereas the zero window gives (0,1) union (1,2). Lowest eigenvalues pi^2/4 and pi^2 imply a positive +1-resolvent norm gap at least 0.19640077079162574. The function sin(pi*x/2) has nonzero trace at the removed point. Thus blindly applying the same limit in d=1 would be false.

A resonance control compares the old d=2 (1,1) eigenvalue at half-width one to the new (2,2) eigenvalue at half-width two: the direct-sum cluster has extra rank. This is an illustrative general fixed-width control, not a chosen width for the candidate's strict interval (2,3). In fact an internal resonant width also exists: half-width sqrt(5) with multiindex (1,3) has the same eigenvalue pi^2/2. The finite exceptional-set selection therefore has real content.

The controls certify none of Mosco convergence, exact all-point geometry, effective aperture sizes, the infinite construction, or pure point completeness. Those assertions are established by the arguments above. No discretized Laplacian was used.

## 12. Provenance, operational status, and remaining gap

All 39 original snapshot files were independently hash/size checked read-only at 2026-10-16T04:47:09Z: 262738 bytes, zero mismatches. The author proof and complete selected record were read, including the empty prior-report object. No original artifact or script was modified. No Git/index/ref mutation, external communication, further proof-search turn, or other-problem work occurred.

Fresh primary-source bytes are identified in SOURCE_RECEIPTS.json. Downloaded bodies and rendered pages were kept only in this family's ignored scratch and removed after inspection. Render observations preserve the important closure-bar and geometry checks; full copyrighted bodies are not retained.

Within the candidate's precise mathematical claim, I find no remaining unproved step or required repair. Root integration, the separate spectral family's review, priority assessment, any human peer review, and any publication decision are separate. Storage ENOSPC temporarily interrupted optional control refinement and final receipt/report creation after the first passing controls run. Those failed writes left the existing control files unchanged; later successful writes retained the first control version and documented the failure. Artifact closure is determined by the separately checked MANIFEST.json.
