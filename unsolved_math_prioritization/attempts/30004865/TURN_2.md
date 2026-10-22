# Turn 2: mixed multipartite detection and incomparability of the fixed tests

**2/5 substantive author turns.** Turn1's complete central negative answer is preserved unchanged. This turn addresses the source's separate multipartite realignment/SIC comparison: for every m>=3, each criterion detects mixed m-qubit states missed by the other. It also gives exact norms and thresholds for an even-party noisy GHZ family.

The bipartite superiority phenomenon for SIC is credited to Shang–Asadian–Zhu–Gühne and its universal implication to Jivulescu–Lancien–Nechita Theorem10.1. The local normalization and Gram identity below are their standard tester formulas. No historical novelty claim is made for the derived examples or formulas.

## 1. Fixing the maps and the complex output norm

Let H_d=M_d(C) with its Hilbert–Schmidt inner product. The realignment tester R is the identity into H_d, equivalently vectorization. Define the canonical SIC-Gram tester by

    L_d(X)=2^(-1/2)(X+(sqrt(d+1)−1) Tr(X) I/d).          (1)

It scales the normalized identity direction by sqrt((d+1)/2) and each traceless direction by 1/sqrt(2). Consequently

    <L_d(X),L_d(Y)>=(Tr(X*Y)+conjugate(Tr X)Tr Y)/2.     (2)

Both R and L_d are complex-linear S1-to-Hilbert contractions: for L_d, its squared output norm is (||X||_2²+|Tr X|²)/2<=||X||_1².

When a rank-one SIC of d² vectors exists, its normalized tester S satisfies exactly (2). Thus S and L_d differ by a unitary on their d²-dimensional outputs: (S L_d^(-1))* (S L_d^(-1))=1. Local unitaries preserve all Hilbert projective tensor norms. Every computation with L_d below is therefore exactly the actual SIC value in such dimensions, independent of the chosen SIC. In arbitrary dimensions we only assert the canonical Gram-map version unless SIC existence is supplied.

All explicit incomparability examples use d=2, where there is no existence gap. For example take the four Bloch vectors (1,1,1), (1,-1,-1), (-1,1,-1), (-1,-1,1), divided by sqrt(3), and projectors P_j=(I+n_j·sigma)/2. These form a qubit SIC, and S(X) has entries sqrt(3/4) Tr(P_j X).

Write

    r_m(rho)=||R^tensor m(rho)||_pi,
    s_m(rho)=||L_d^tensor m(rho)||_pi.

Here the norm is the complex projective norm across the m individual output Hilbert spaces, not the nuclear norm of a chosen bipartite flattening. Detection means a value strictly greater than1.

## 2. Orthogonal blocks and a real even-power certificate

We use two elementary projective-norm facts, with their complex-field justifications.

**Block lemma.** Suppose each local Hilbert space decomposes into corresponding orthogonal blocks H_(i,alpha), and T_alpha lies in tensor_i H_(i,alpha), with finitely many alpha. For m>=2,

    ||sum_alpha T_alpha||_pi=sum_alpha ||T_alpha||_pi.    (3)

The upper bound is the triangle inequality. For the lower bound choose, on each block, a norm-one multilinear functional attaining ||T_alpha||_pi, adjusting its phase. Extend by the local orthogonal projections and sum. Its value on unit vectors x_i has modulus at most

    sum_alpha product_i ||P_(i,alpha)x_i||
       <= product_i (sum_alpha ||P_(i,alpha)x_i||^m)^(1/m)
       <= product_i (sum_alpha ||P_(i,alpha)x_i||²)^(1/2)
       <=1.

The first inequality is Hölder and the second is l_m<=l_2 for m>=2. This gives a norm-one dual certificate for the sum. All spaces here are finite dimensional, so attainment causes no compactness issue.

**Even real-power lemma.** If m=2q, v_j have real coordinates in one fixed orthonormal basis of a complex Hilbert space, and c_j>=0, then

    ||sum_j c_j v_j^tensor m||_pi=sum_j c_j ||v_j||^m.   (4)

The upper bound comes from the displayed decomposition. For the lower bound use the complex multilinear functional

    B(x_1,x_2) B(x_3,x_4) ... B(x_(m−1),x_m),
    B(x,y)=sum_k x_k y_k.

It has norm at most1 by the ordinary absolute-value Cauchy–Schwarz inequality. On a repeated real vector its value is ||v||^m. Thus (4) is valid for the complex projective norm; no real/complex norm identification is assumed.

## 3. Noisy GHZ states: exact even-party formulas

Let

    |GHZ_(d,m)>=d^(-1/2) sum_(i=1)^d |i>^tensor m,
    rho_(p,d,m)=p |GHZ_(d,m)><GHZ_(d,m)|+(1−p) I/d^m,
    0<=p<=1.                                           (5)

For m=2q even,

    r_(2q)(rho)=pd+(1−p)d^(-q),                        (6)
    s_(2q)(rho)=p(1+(d−1)2^(-q))
                  +(1−p)((d+1)/(2d))^q.               (7)

To prove this, let D be the span of the diagonal matrix units, and regard every off-diagonal E_ij as its own one-dimensional orthogonal block. For realignment, the diagonal part of the output is

    (p/d)sum_i E_ii^tensor m+(1−p)(I/d)^tensor m.

Its norm is p+(1−p)d^(-q) by (4). The other d(d−1) blocks each have coefficient p/d and unit simple tensor. The block lemma adds their norms, proving (6).

For L_d the vectors a_i=L_d(E_ii) lie in the real diagonal subspace, with ||a_i||=1, while z=L_d(I/d) has norm sqrt((d+1)/(2d)). Each off-diagonal E_ij is scaled by1/sqrt(2), and these blocks remain mutually orthogonal and orthogonal to D. Equation (4) gives diagonal norm p+(1−p)((d+1)/(2d))^q. Adding the d(d−1) off-diagonal norms p/(d 2^q) gives (7).

The exact strict detection thresholds are therefore

    p_R=(1−d^(-q))/(d−d^(-q)),
    p_S=(1−((d+1)/(2d))^q)
           /(1+(d−1)2^(-q)−((d+1)/(2d))^q).            (8)

For q=1 these are equal to1/(d+1), the credited bipartite isotropic-state threshold. For every q>=2,d>=2, p_S>p_R. After cross-multiplying the positive denominators, the sign is that of

    (d−1)[1−2^(-q)−((d+1)/(2d))^q+2^(-q)d^(-q)],

which is positive because (1/2)^q+(3/4)^q<1 for q>=2 and (d+1)/(2d)<=3/4. Hence there is a nonempty interval of mixed states detected by realignment but missed by SIC. For four qubits at p=1/2, the exact values are

    r_4=9/8,     s_4=29/32.                            (9)

These are full projective-norm values, not flattening estimates.

## 4. A three-qubit separation with certified bounds

For arbitrary m>=2, the same block decomposition gives the useful estimates

    r_m(rho_(p,d,m)) >= pd+(1−p)d^(1−m),               (10)
    s_m(rho_(p,d,m)) <= p(1+(d−1)2^(-m/2))
                         +(1−p)((d+1)/(2d))^(m/2).     (11)

For (10), on the realignment diagonal block the dual functional sum_i (e_i*)^tensor m has norm at most1 by Hölder, and evaluates the diagonal part to p+(1−p)d^(1−m). Add the exact off-diagonal block norms p(d−1) using (3). For (11), use the given positive simple-tensor decomposition of the diagonal part as an upper bound, and again add the exact off-diagonal norms. No equality is asserted for odd m.

Now take m=3,d=2,p=9/20. Equations (10)-(11) imply

    r_3 >=83/80>1,
    s_3 <=9/20+(33sqrt(3)+18sqrt(2))/160
          <9/20+(33·7/4+18·3/2)/160
          =627/640<1.                                 (12)

Both square-root upper bounds are strict and elementary. Thus this particular mixed three-qubit state is detected by realignment and missed by the exact normalized qubit SIC criterion. Its entanglement follows from the valid realignment certificate, without needing a separate classification of GHZ white-noise separability.

## 5. Separation in the other direction

Consider the two-qubit density matrix

    eta_p=p |Phi+><Phi+|+(1−p)|0><0| tensor I/2,
    |Phi+>=(|00>+|11>)/sqrt(2).                         (13)

For this family, direct two-by-two singular-value calculations give

    r_2(eta_p)=p+sqrt((1+p²)/2),
    s_2(eta_p)=(p+sqrt(3+p²))/2.                        (14)

For clarity, use the Hilbert–Schmidt orthonormal Pauli basis (I,X,Y,Z)/sqrt(2). The realignment coefficient matrix has entries C_00=1/2, C_z0=(1−p)/2, C_zz=C_xx=p/2, C_yy=-p/2, all others0. Its identity/Z block is triangular, and its nuclear norm is sqrt(((1+p)/2)²+((1−p)/2)²). The two other singular values total p.

Applying L_2 on both sides scales the identity coordinate by sqrt(3/2) and other coordinates by1/sqrt(2). The corresponding block entries are3/4, sqrt(3)(1−p)/4 and p/4; its nuclear norm is sqrt(3+p²)/2. The two other singular values total p/2. This proves (14), including p=0 endpoints by continuity or direct evaluation.

Thus SIC detects eta_p precisely when p>1/4, whereas realignment detects it precisely when p>2−sqrt(3). At p=4/15,

    r_2=(8+sqrt(482))/30<1,
    s_2=(4+sqrt(691))/30>1,                             (15)

because 482<22² and 691>26². The density matrix (13) is manifestly positive and trace-one; the SIC certificate proves it entangled. The qualitative bipartite advantage is already known; (13)-(15) provide an explicit rational control for extending it to the multipartite setting.

## 6. Neither fixed tester dominates for any m>=3

For a pure local projector P, ||R(P)||=||L_d(P)||=1. Appending pure local states to any state therefore preserves both of its tester projective norms, by the crossnorm property. Append pure qubit factors to the three-qubit state in (12), and to the two-qubit state in (15). For every m>=3 this gives mixed m-qubit states in both strict detection differences:

    r_m>1 but s_m<1,
    s_m>1 but r_m<1.                                   (16)

Hence neither source fixed criterion is universally stronger in the multipartite setting. This does not contradict the credited two-party implication r_2>1 => s_2>1. It answers the qualitative domination question but is not a classification of all mixed multipartite states. The appended-factor examples are not asserted to be genuinely multipartite entangled. The even-party formulas give a nontrivial detected mixed family, with the actual SIC qualification in Section1.

## Controls and remaining scope

verify_turn2.py checks the rational even-party thresholds, coefficient certificates, exact radical comparisons and the Pauli-block algebra. The projective-norm and arbitrary-party conclusions are proved by the dual certificates above, not inferred from sampled tensors. General mixed-state detection regions and more refined quantitative comparisons remain open in this packet; turn1's central completeness result and its independent review stay unchanged.
