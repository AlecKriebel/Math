# Independent source reconstruction and topology family (before candidate access)

Seal UTC: 2026-10-03T22:02:20.327543+00:00
Candidate access: none; no candidate theorem, proof, code, verdict, sibling report, or QUEUE has been opened.
Completion estimate: 25% of this adversarial audit. Discovery goal is the correctness of the frozen claimed solution, not a numerical theorem probability.

## Exact original target

OWR 49/2009, Keller's report occupies printed pages 2713-2715 (PDF pages 15-17, 1-based). The conjecture is on printed p.2715. In the model X=[-1/2,1/2], D={u in L1(X):u>=0 a.e., integral u=1}, with the inherited L1 metric, define phi(u)=integral x u(x) dx and F(u)=P_{G(phi(u))}u. T_r has two increasing onto fractional-linear branches, f_r(x)=((r+4)x+r+1)/(2rx+2) and f_r(x)-1, split at alpha_r=-r/4. Endpoint/split values are irrelevant for L1 equivalence classes. G(x)=A tanh(Bx/A), 0<A<=0.4, 6<B<=16 in the original bistable target. Let C_j={u:F^n u ->u_j in L1}; original conclusion sought is C_0=boundary_D(C_+)=boundary_D(C_-). Boundary is relative to D. Stable regime B<=6 is outside the three-basin conjecture.

OWR reports three fixed points and convergence for every density, and relative L1 openness of C_+,C_-. It additionally reports density of C_+ union C_- in D. That last assertion by itself only makes C_0 the boundary of the union; it does not ensure both signs approach every neutral point.

## Prior full-paper results and assumptions

Author-hosted BKZ is a 36-page December 19, 2008 preprint, not automatically an exact publisher PDF. arXiv abstract binds identifier 0812.4040v1 to submission 2008-12-21 and journal CMP 292 (2009), 237-270, DOI 10.1007/s00220-009-0854-9. Author PDF and current rendered arXiv v1 PDF have different bytes and different title-page dates (arXiv rendering says November 10, 2018), so mathematical matching must be equation/theorem based, not a claim of byte identity.

BKZ Section 2 assumes odd, strictly increasing S-shaped G mapping X to [-0.4,0.4]; C2 suffices except finite-dimensional analyticity. Assumption I: G'(x)<=25-50|G(x)|. Assumption II: H(r)=G(phi(u_r)) is S-shaped (S-shapedness of G alone does not imply this). Theorem 2/Proposition 3 prove exhaustive L1 convergence and stable-basin openness on D. B=G'(0)>6 is bistable. Section 5.1 proves this via conditional expectations on the nonautonomous full-branch partitions and shadowing with the *same* parameter sequence, not by global contraction of F.

BKZ D0 consists of u(x)=integral_Y w_y(x)dmu(y), Y=[-2/3,2/3], w_y(x)=(1-y^2/4)/(1-xy)^2. The IFS transports mu via increasing sigma_r(y)=2(y+r)/((r+1)y+r+4), tau_r(y)=2(y+r)/((r-1)y-r+4), with p_r(y)=1/2-(r+y)/(4+ry). Section 4 monotonicity, shrinking support intervals, Lemmas 12-13 and Proposition 4 prove C_0 intersect D0 lies on *both* boundaries. Exact unresolved prior gap: neutral rough densities outside D0. I read all source theorem and proof material in Sections 2-6 and Appendix A (including the source's limited BV-to-L1 differentiability statement); no L1 differentiable stable-manifold theorem can be imported from Proposition 5.

## Independent topology deductions (to test candidate, not assume it)

1. D0 is compact in L1: P(Y) is weakly compact and y->w_y is uniformly Lipschitz into L1. Every member is bounded between 1/2 and 2. Therefore D0 is NOT dense in D. Let u=4 on the two endpoint intervals of length 1/8 and zero elsewhere. It is symmetric, hence in C_0 by exactness of T0, but dist_L1(u,D0)>=1: on its support each v in D0 has at most half the mass, and equality of total masses doubles the deficit. Approximation by arbitrary analytic densities is not approximation by this analytic mixture class.

2. Fixed-map noninvertibility does not prevent relative openness. For h=P_T u and target g in D, define v=u(g/h) o T where h o T>0. Where h=0, u is zero on almost every corresponding preimage and one may add any positive right-inverse lift of g 1_{h=0}. With disjoint supports, P_T v=g and ||v-u||1=||g-h||1. For T0 a right inverse is g o T0, since T0 preserves Lebesgue measure. This is an exact relative-ball lifting mechanism, including vanishing h, not an application of the Banach open mapping theorem to the positive cone.

3. A self-consistent preprocessing candidate: q_r(x)=(x+r/4)/(1+rx), so T_r=T0 o q_r. q_r fixes endpoints and has derivative (1-r^2/4)/(1+rx)^2>0. Q(u)=P_{q_{G(phi(u))}}u could be a homeomorphism of D. Given v, put u=P_{q_{-r}}v and solve r=G(integral q_{-r}(x)v(x)dx). q_{-r}(x) decreases in r strictly for interior x, so r-G(mean) is strictly increasing and has endpoint signs at +/-0.4. Thus unique r exists. Continuous dependence follows from ||v-v'||1 controlling the means and compact uniqueness in r; strong L1 continuity of smooth composition follows by approximation with continuous densities and uniformly bounded Jacobians. This mechanism handles unbounded and vanishing densities. It suggests F=P0 o Q is open, but openness alone does not prove the target basin equality.

4. Caution for boundary pullback: a continuous open F and A open satisfy F^{-1}(boundary A)=boundary(F^{-1}A), by neighborhood images and continuity. Here F^{-1}C_+=C_+ holds by convergence tail equivalence. Consequently both basin boundaries are completely backward invariant. But F^n u->1 and 1 on both boundaries does NOT automatically put every u in C0 on both boundaries: a uniform quantitative neighborhood growth or a density/lifting mechanism is needed. Any route merely replacing this gap by 'the neutral basin is the stable manifold' in L1 is blocked absent a new mechanism.

5. Rough topology falsifiers to pursue: zero output fibers; endpoint densities singular yet integrable; nonunique conditional branch allocations; cumulative functions with flat pieces; discontinuous u and parameter-dependent composition; false claim that D has an ambient L1 open ball; misuse of stochastic order for T0 (a nonmonotone folding map); operator-norm versus strong continuity; and illicit interchange of long-time/approximation limits.

## Source receipt identifiers

Source raw files and HTTP headers are private. SHA256:
- OWR PDF b4a8d328316d093cde2d23a9b13e8b869e33b46626735494de473045bbc26169.
- BKZ author PDF c1b9ca5c4edbba4d06513634a649589185a63a53f0b0a9f14ebb8a9fc8289642.
- arXiv v1 rendered PDF 6a182868c1d2d4a09c8cfaa513ba9314cce522c3b08fe71728264399df7d7861.

Primary URLs: https://ems.press/content/serial-article-files/46250 ; https://mat.univie.ac.at/~zweimueller/MyPub/bkz.pdf ; https://arxiv.org/abs/0812.4040 .

## Family map and current strongest result

Topology/rough-density family: exact fixed-PFO relative lifting and self-consistent preprocessing homeomorphism have independently reconstructed mechanisms; these should be tested fully after candidate access. Full neutral-boundary equality remains unverified. D0 non-density is an independently verified obstruction to naive analytic-core extension. No novelty certificate or human peer-review claim is made.
