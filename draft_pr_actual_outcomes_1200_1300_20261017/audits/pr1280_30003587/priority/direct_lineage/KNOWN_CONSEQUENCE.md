# An outer arbitrary-period consequence of equivariant uniqueness

This is an authored deduction, not an assertion that the cited paper explicitly states the CK theorem. It is independent of the candidate's periodic return-corner mechanism.

Use Gabe-Szabo [arXiv:2205.04933v1](https://arxiv.org/pdf/2205.04933v1) Theorem5.8 pp45-46, Definition1.15 p13, Proposition3.14 p29; in [v3](https://arxiv.org/pdf/2205.04933v3), the corresponding locators are Theorem5.8 p46, Definition1.15 p13, Proposition3.15 p29. The v1 public timestamp is 10 May2022.

Let alpha be a pointwise outer action of a finite abelian group G on a unital Kirchberg algebra A. Suppose, for each g, alpha_g is equivariantly homotopic to id through unital embeddings. Finite groups are exact and amenable; their actions are amenable. Proposition3.14/3.15 supplies isometric shift absorption. Thus Theorem5.8 applies to the unital equivariant embeddings (id,1) and (alpha_g,1), whose KK^G classes agree by the homotopy.

Definition1.15 and Theorem5.8 give unitaries u_t in A with

    Ad(u_t)(a) -> alpha_g(a),
    max_{h in G} ||alpha_h(u_t)-u_t|| -> 0.

Put b_t=|G|^{-1} sum_h alpha_h(u_t). Then b_t lies exactly in A^alpha and ||b_t-u_t|| ->0. Eventually b_t is invertible. Its polar unitary

    w_t=b_t(b_t* b_t)^{-1/2}

lies in A^alpha and satisfies ||w_t-u_t|| ->0. Sampling t tending to infinity gives the required implementing sequence. No relation among choices for different g is used.

For an edge-diagonal action, fix g and choose real theta_e with exp(i theta_e)=chi_e(g). The maps

    delta_t(p_v)=p_v,
    delta_t(S_e)=exp(i t theta_e) S_e,  0 <= t <=1,

are automorphisms by the graph universal relations and commute with every alpha_h. They join id to alpha_g. This proves the outer edge-diagonal conclusion for every graph period. For the narrower OWR CK definition, the generator eigenvector condition supplies the same path directly.

Boundary: if the action has a nontrivial inner kernel, the uniqueness theorem's shift-absorption hypothesis fails for that action. A quotient/coboundary argument or another mechanism is still required. This note does not attribute the full non-outer target to Gabe-Szabo and does not certify novelty of any remaining reduction.
