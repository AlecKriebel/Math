# Fresh adversarial derivations before submitted-code reproduction

These calculations are derived from the published claims, not from archived verdicts. They are mathematical evidence for the downstream reduction; they do not prove the external EPnI. All trace norms below are unhalved.

## Operational quantifiers and errors

Use a sequence of finite block codes, every gross input and output register having logarithmic dimension O(n), with both reliability trace error and generated-secret trace error tending to zero. Fix the finite gross rates before taking errors to zero. If d_W is the dimension of the generated secret, conditional-entropy continuity on the finite classical W alone bounds the secrecy information by O(epsilon log d_W)+O(h_2(epsilon)), independently of the dimension of the optical environment. Thus I(W;XE^n)=o(n). This is weak, uniform-source trace secrecy; it neither asserts arbitrary-message semantic security nor secrecy after revealing a consumed key. Finite gross rates are essential here.

For the quantum model, use the complete joint correctness condition of QDC Eq. (4): uniform classical message, maximally entangled logical reference/output, and generated ebits in product. Its continuity errors likewise have dimension given by finite generated resource registers. Do not replace entanglement transmission by an unspecified average fidelity claim.

## Zero-energy obstruction and OTP

A positive Hamiltonian with one-dimensional vacuum kernel has Tr G rho=0 only for rho=|0><0|. A convex average of nonnegative input energies is zero only when every positive-weight conditional input is vacuum. Bob's optical output is consequently fixed vacuum.

Write W=(M,T_A), V=(J,S_B), and L for consumed public data. The literal secrecy target makes W uniform and independent of LV. For every decoder, the comparison-state probability of correctly recovering W is 1/d_W. Contractivity and the variational characterization of trace distance change that probability by at most epsilon_sec/2. Reliability changes ideal success one by at most epsilon_rel/2. Hence

    1 <= 1/d_W + (epsilon_sec+epsilon_rel)/2.

For d_W>=2 the sum of errors must be at least one; eventually d_W=1 along any vanishing-error sequence. This conclusion is independent of the number of consumed noiseless resources.

For independent uniform d-valued M,S and L=M+S mod d, actual mass on each valid triple is 1/d^2. For an arbitrary comparison public probability q_l, its independent-uniform-pair mass is q_l/d^2. In block l there are d valid pairs and d^2-d invalid pairs. Since 0<=q_l<=1, the L1 difference in that block is

    d(1-q_l)/d^2 + (d^2-d)q_l/d^2
      = 1/d + (1-2/d)q_l.

Summing gives exactly 2(1-1/d), for every q, not only the actual uniform public marginal. Tracing S instead gives an exactly uniform independent M,L pair. This separates the literal and generated-secret criteria without EPnI.

## Corrected private converse

Keep X=(K,L), Y=(W,V), with every named register classical except B,E. The generated public/private labels K,M are initially independent of the preshared key S_B; J,L may depend on them. Correctness and secrecy yield the finite-register information lower bounds with o(n) terms.

The first bound uses

    I(KM;BLJS_B)
      = I(KM;B|LJS_B)+I(KM;LJ|S_B)
      <= I(KMLJS_B T_A;B)+H(LJ)
      <= I(XY;B)+H(L)+H(J).

The equality uses I(KM;S_B)=0, not independence of KM from the encoder outputs LJ. Subtract the consumed public/private register logarithms.

The second exact chain identity is

    I(W;BV|X)-I(W;E|X)
      = I(WV;B|X)-I(WV;E|X)
        + I(W;V|X)-I(V;B|X)+I(V;E|WX).

The positive remainder terms sum to I(V;WE|X), at most H(V|X) because V is classical. The negative I(V;B|X) may be discarded. Subtract log|V|; do not infer I(WV;XE)=o(n) from the generated-secret promise.

For the third exact identity, the difference between

    I(KW;BLV)-I(W;E|KL)

and

    I(KLWV;B)-I(WV;E|KL)

equals

    -I(LV;B)+I(KW;LV)+I(V;E|KWL).

The last two terms equal I(KW;L)+I(V;KWE|L), and are at most H(L)+H(V). Subtract all consumed register logarithms. Classicality is necessary for the H(V) upper bound with quantum side information.

For a degradable channel and spectral refinement Z of rho_xy, adding Z increases the first mutual information by I(Z;B|XY)>=0 and the last two private differences by I(Z;B|XY)-I(Z;E|XY)>=0. This is data processing through the degrading map. The three refined expressions are respectively at most H(bar B), H(B|X)-H(E|X), H(bar B)-H(E|X), since the conditional refined BE state is pure. This is an upper bound on every original ensemble, and does not assume Gaussian optimality.

## Scalar entropy transfer and the common parameter

Let L(u)=ln(1+1/u), u>0. For f_t(s)=g(t g^{-1}(s)),

    f_t'(g(u)) = t L(tu)/L(u),
    d/du f_t'(g(u))
      = t[(tu+1)L(tu)-(u+1)L(u)]
        /[u(u+1)(tu+1)L(u)^2].

The function h(u)=(u+1)L(u) has derivative L(u)-1/u<0, by ln(1+x)<x. Thus f_t is convex for 0<t<1 and concave for t>1, with continuous endpoint extensions. At t=0 it is constant ("increasing" in the manuscript must mean nondecreasing).

Assuming the finite-mode sharp vacuum entropy bound for every n and finite-energy input, apply it first to the degrading map kappa=(1-eta)/eta<=1 and then Jensen. Set s=H(B|X)/n; the common energy bound gives s<=g(eta N). For N>0 there is lambda with s=g(eta lambda N), yielding H(E|X)/n>=g((1-eta)lambda N). Applying the sharp eta bound to rho_x and Jensen gives f_eta(H(A|X)/n)<=s, hence H(A|X)/n<=g(lambda N). These are simultaneous bounds with a single lambda, not separate optimizations.

Finite average energy controls entropy integrals by the concave thermal maximum, so countable/measurable ensembles cause no divergent-entropy subtraction. The premise must cover arbitrary internal multimode entanglement. The weaker linear or exponential quantum EPI is insufficient to recover these sharp functions at unequal entropy levels.

## Corners, signs and all resource orthants

Put A=g(lambda N), B=g(eta lambda N), E=g((1-eta)lambda N), T=g(eta N). The quantum father corner is (T-B,(A+B-E)/2,(-A-E+B)/2). Its three facet values are T+A-E, B-E, T-E. Adding teleportation t=(-2,1,-1), superdense coding d=(2,-1,-1), and entanglement distribution e=(0,-1,1) yields exactly the displayed translated cone: their coefficients are minus one half of the respective third, second, first facet deficits.

The private corner is (T-B,B,-E). Its facets are T,B-E,T-E. For a displacement (r,p,s), the OTP, private-to-public, and private-to-key coefficients are -(r+p+s), -(p+s), -(r+p). These are nonnegative exactly when all three displacement facet inequalities hold. This proves equality of the translated cones in every sign orthant, not merely containment of the three generators. Discarding resources is included in each cone.

The net-resource convention permits finite gross seed input and output; it does not establish that a point with zero net key can be implemented with zero gross initial key. Finite compositions of ideal uniform independent generated secrets and OTP/private conversions preserve the final generated-secret promise by trace contraction; consumed registers are removed. No superlinear catalyst is needed or allowed.

## Direct coding and average cost

For a finite cq ensemble, sample independent satellites for each public/private/key triple. Given key, Bob packs only the private-message subcode, at rate below I(Y;B|X). Averaging unknown key covers Eve at key rate above I(Y;E|X). The finite typical projectors give rank D<=2^{n(H(E|X)+delta)} and positive subnormalized truncated states tau<=A P, A=2^{-n(H(E|XY)-delta)}. Independence, even for noncommuting matrices, gives

    E Tr[(K^{-1}sum tau_s-E tau_s)^2] <= A/K,
    E||K^{-1}sum tau_s-E tau_s||_1 <= sqrt(DA/K).

Gentle truncation contributes a vanishing term. No union over exponentially many messages is necessary for the average, uniform-message criterion. The public decoder depends only on cloud centers, so its expected error on sampled satellites is exactly its error on ensemble-average cloud outputs. Gentleness preserves the private decoder's success. A secrecy target depending on the public word can be replaced by the actual marginal at a further factor two in the error, by trace contraction and triangle inequality. Thus the supplement's target-state version implies the manuscript's actual-marginal version.

For energy, first fix N'<N and a finite alphabet/Fock cutoff K. The per-use cost is bounded by K, so input trace error contributes at most K epsilon, not an estimate for an unbounded Hamiltonian. The CEF rho-like random-code property gives expected input closeness to the conditional product state for maximally mixed logical source/consumed ebits. Conditional typical types change cost by at most |X|delta K. A strict mean margin makes Pr(cost<=nN) bounded below by a fixed positive constant by Markov; the probability of bad decoding/secrecy tends to zero. Their intersection contains a valid deterministic code. The private random lookup construction also has independent positions and bounded cost, so Hoeffding is available. Code selection does not postselect unknown quantum data.

The order is: fixed strict energy margin and finite approximant; n->infinity; alphabet/Fock approximation; N' up to N; capacity closure. Truncating and normalizing a number-cutoff state cannot increase its mean number, since all removed levels exceed all retained levels. Gaussian first moments control discarded label tails. For the converse, K may depend on each fixed block and its finite resource dimensions; choose its trace and entropy errors first, then take n limits. Uniformity in growing n at a fixed K is neither available nor required.

## Boundaries and closure

At N=0 use the exact vacuum argument and both conversion cones, without dividing by N. At eta=1/2, the private union is dominated by lambda=0; Q+E and P+S are at most zero. At eta=1, the lambda=1 member dominates both unions. At lambda=0/1 use point masses when Gaussian variances vanish. At eta=0 the channel is vacuum-output, but the manuscript capacity claims explicitly have eta>=1/2; the degrading-parameter argument must not be extended through division by eta. No claim for eta<1/2 follows from it.

For fixed finite N and eta in the claimed range, s belongs to a compact interval. The facet right sides are continuous and concave in s: f_{1/eta} is concave and -f_kappa is concave. Their hypographs intersect in a convex set; projection preserves convexity. To prove closedness, take a convergent sequence of finite rate triples, extract a convergent lambda subsequence, and pass continuous inequalities. The rate space need not be bounded. These arguments justify the union and closure and avoid any claim about N->infinity uniformly in eta near one.

## Exact external boundary

The downstream sharp capacity equalities require the sharp finite-energy multimode vacuum entropy bound for every finite block. The pinned OpenAI Theorem 1.1 and Corollary 1.2 state precisely a sufficient premise, but a theorem label is not a proof validation. This adversarial review has inspected those statements and the cutoff proof, not independently established the entire Sections 3--6 EPnI proof or run a Lean kernel build. Its strongest equalities are therefore explicitly conditional on that premise. The OTP refutation, corrected information identities, cone algebra, coding inner bounds, and boundary checks do not depend on EPnI.
