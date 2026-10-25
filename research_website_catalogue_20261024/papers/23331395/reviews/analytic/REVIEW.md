# Independent analytic review — Zenodo 23331395

Paper: Positive tangent-bundle Seshadri constants characterize projective space, Alec Kriebel, version 1.0, 12 October 2026.
Public PDF SHA-256: `f3e5619c7e1560c45f7793b0f7e4dabfbbf66d08f568f3478b5bb8f35779ea17` (91,056 bytes).

**PASS_WITH_STATED_SCOPE_LIMITS. No unresolved substantive defect found.** The complete five-page PDF and packaged TeX were read and the argument reconstructed without reading archived or new reviewer verdicts. This is AI-assisted review, not human peer review, formal certification, or a novelty certificate.

## Claim and strongest verified result

For smooth integral projective X of dimension n>=1 over an algebraically closed field of arbitrary characteristic, positivity of the quotient-convention relative Seshadri constant of T_X at one closed point x implies X=P^n over that field. The full theorem is supported by the argument, using its explicitly identified established inputs. No general-point or characteristic-zero restriction is needed in the new reduction.

## Proof reconstruction and attempted failure modes

1. **Normalization and splitting.** For a rational integral curve C through x, a normalization f:P1→C→X has k(C)=k(P1). A splitting quotient of f*T_X onto O(a_i) gives a lift to P(T_X) whose image function field lies between these equal fields. Its total generic degree is one, even in positive characteristic. The Seshadri numerator is a_i and pushforward is [C], so every a_i>=1. Hence f*T_X is ample and both H1(f*T_X(-0)) and H1(f*T_X(-0-infinity)) vanish. This uses actual quotients on P1, not ordinary slopes on arbitrary positive-characteristic curves.

2. **Existence at the same point.** Fulger–Murayama Corollary 4.6's proof was directly inspected: it produces a rational curve through the actual prescribed x in arbitrary characteristic. Thus the minimum d of very-ample A-degree over ALL rational integral images through x exists. The minimum survives algebraically closed field extension: a smaller-degree normalization gives a point of a finite-type pointed Hom scheme, hence a closed k-point. Its image has no larger degree and is rational by Lüroth, including inseparable cases, contradicting d. No uncountability assumption is used.

3. **Stable-map boundary.** A geometric genus-zero nodal domain has rational components and tree dual graph. Starting at the marking, follow contracted components to a nonconstant component whose image contains x. The degree sum d>=e_v(A.C_v)>=A.C_v>=d, with e_v FULL generic degree, forces exactly one nonconstant component and e_v=1. Any contracted subtree of t vertices attaches once and has at most one mark; its special-point incidence total is at most 2(t-1)+1+1=2t, contradicting the stability lower bound 3t. Thus the domain is P1 and the map birational. The marking initially on a contracted component, and inseparable multiple covers, are both covered. The absolute minimum across all images is essential and is correctly used.

4. **Actual moduli scheme.** Abramovich–Oort Theorem 2.8 and Section 2.5 supply the proper finite-presentation Artin stack with finite stabilizers and a projective coarse scheme for arbitrary-characteristic projective targets. Its actual evaluation fibre M_x is proper and nonempty. Geometric automorphisms of a birational map are identity on a dense open. Infinitesimal automorphisms are source vector fields killed by dg; birational normalization has generically injective differential even for singular image, so these vanish. A finite stabilizer with one geometric point and zero tangent space is trivial by Nakayama. The finite augmentation ideal on an atlas has zero geometric fibres, so inertia is trivial also over nonreduced bases.

5. **Representability and marking.** Stacks 04SZ makes M_x an algebraic space. Its map to the full coarse Q is proper (proper source over k, separated target) and locally quasi-finite (coarse geometric points identify isomorphism classes). Stacks 03XX and 02LS give a scheme finite over projective Q. No wild closed-fibre/coarse-base-change claim is used. The universal curve has smooth geometric P1 fibres and is proper flat, hence smooth. The marking is a relative Cartier divisor. Its degree-one line bundle gives a rank-two pushforward and a projective-bundle identification by base change; the finite/Nakayama/flatness argument also handles nilpotent bases. Locally splitting the quotient provided by the section gives pointed trivializations.

6. **Surjective evaluation at fixed x.** The degree-d pointed Hom scheme is the pointed-parametrization torsor under smooth Aut(P1,0). The two H1 vanishings establish smoothness of this Hom scheme and its evaluation at infinity using fixed-source obstruction theory. This is characteristic-free infinitesimal smoothness, not a characteristic-zero generic-smoothness substitution. Smooth descent gives smoothness of M_x at the chosen map. Its unique local irreducible component has reduced closure H. A neighborhood maps into H; smooth evaluation gives an open image, properness of U gives closed image, and integrality of X gives surjectivity. Smoothness with geometrically integral fibres over integral H makes U integral. The marking remains an actual contracted section.

7. **Numerical generation.** Fibre degrees b=D.C are constant; birationality ensures agreement with image-curve degree. L=O_X(dD) tensor A^(-b) pulls back to degree zero on every P1 fibre. With h0=1,h1=0, base change gives e*L=pi*B. Pulling back along the genuine marking gives B=(e sigma)*L, trivial because e sigma=x. This is also the Picard decomposition of a projective-line bundle. The cited descent hypotheses hold: proper flat finite presentation, geometrically connected fibres, and reduced H for 0EX7.

8. **All curves, including inseparable lifts.** For any integral curve Gamma in X, a closed point of nonempty U_eta has a finite residue extension K/k(Gamma). Its reduced closure Gamma' is a proper integral curve dominating Gamma. Projection gives 0=q deg(L|Gamma), where q is positive TOTAL generic degree. This is an equality of integers, unaffected when characteristic divides q. It tests curves avoiding x and positive-genus curves too. Thus d[D]=b[A] numerically, and rho(X)=1 because A is nonzero. No assertion that Pic(X) itself is cyclic is required.

9. **Fano reduction.** For D=-K_X, b is the positive sum of tangent splitting degrees, hence -K_X is numerically a positive rational multiple of A. The difference-of-powers identity gives positive top intersections on every integral subvariety; the numerically trivial difference pairs with a real one-cycle. Nakai–Moishezon applies in any characteristic, and smoothness makes -K_X Cartier. The directly inspected Fulger–Murayama Proposition 4.8(1) then gives X=P^n. Their Conjecture 4.9 is separately stated and never an input.

## Boundary controls

- n=1 gives epsilon(T_X;x)=2-2g and hence genus zero. Over algebraically closed k this is P1.
- Singular rational images require only generic differential injectivity, not immersion everywhere.
- Wild finite group schemes and nonreduced parameter spaces are explicitly addressed.
- Mere freeness would fail: on P1 x P1 a fibre has tangent pullback O(2) plus O and its fixed-point family does not sweep the surface. Strictly positive splitting is essential.
- Fulger–Murayama Example 4.2 confirms the converse constants 2 for P1 and 1 for higher projective space. Singular varieties are outside the theorem.

## Primary sources checked and limits

- Fulger–Murayama final-numbering manuscript: https://par.nsf.gov/servlets/purl/10198624. Corollary 4.6 proof, Proposition 4.8, Conjecture 4.9 and Example 4.2 directly read. Web fetch failed but direct retrieval succeeded. Its hash is recorded in source_bindings.json. Same-point rational existence and Fano characterization are accepted established inputs; their underlying bend-and-break and Mori theory was not independently reproved.
- Abramovich–Oort: https://arxiv.org/pdf/math/9808074. Definitions, Theorem 2.8, Sections 2.4–2.5 inspected; arbitrary characteristic and finite possibly nonreduced stabilizers are explicitly included.
- Stacks Project statement bodies and relevant hypotheses inspected: https://stacks.math.columbia.edu/tag/04SZ, https://stacks.math.columbia.edu/tag/03XX, https://stacks.math.columbia.edu/tag/02LS, https://stacks.math.columbia.edu/tag/0B91, https://stacks.math.columbia.edu/tag/0EX7, https://stacks.math.columbia.edu/tag/0GKA.
- Gounelas, Proposition 4.7 and proof: https://ems.press/content/serial-article-files/26314?nt=1. Corroborates the two-point deformation mechanism; the manuscript also supplies the precise pointed obstruction argument itself.
- Fujino–Miyamoto, field convention and Theorem 1.3: https://www.math.kyoto-u.ac.jp/~fujino/Nakai-Moishezon3.pdf. Criterion includes arbitrary characteristic.

The numerical-generation principle is proved in the paper, so Andreatta–Occhetta serves as attribution rather than an unchecked black box. The full Kollár monograph and all foundational proofs behind imported theorems were not reaudited. No finite computation is claimed to verify this universal geometric argument. Historical priority requires separate literature review. No substantive gap requiring deferral was found; no repair or manuscript alteration was attempted. Temporary third-party reference files were removed after inspection and hash recording because the filesystem exhausted free space.
