# Direct coding repair for consumed secret key

Checkpoint: 2026-10-06 21:22 Pacific / 2026-10-07 04:22 UTC.

Status: checkable finite-dimensional proof supplied below. Mathematical completion for this assigned direct-coding lemma: 95% pending adversarial review; contribution to the complete bosonic project is conditional on its other dependencies. Publication-package completion for this assigned note: 20%. These estimates are not evidence.

## 1. Exact claim and convention

Let a finite-dimensional channel isometry map A to BE. Fix finite alphabets X,Y, probabilities p(x)p(y|x), and input density operators rho_xy. Define sigma_xy^BE as the isometric outputs, sigma_x^Z = sum_y p(y|x)sigma_xy^Z, and sigma^Z = sum_x p(x)sigma_x^Z, for Z=B,E. All logarithms are base two. Put

    a = I(X;B), b = I(Y;B|X), c = I(Y;E|X).

For any nonnegative rates r<a and p<b (allow zero without requiring a strict inequality when the corresponding mutual information is zero), and any k>c, there are block codes transmitting a public label J at rate r and a private message M at rate p while consuming a uniform, independent, preshared key S at rate k. Bob may condition his decoder on S. They have vanishing decoding error and generated-message trace secrecy

    ||omega^{JM E^n} - pi^M tensor omega_target^{J E^n}||_1 -> 0.

The code and J may be disclosed to Eve. In particular, Eve is explicitly given J in the displayed criterion. The consumed S is traced out: the theorem does **not** promise joint secrecy of (M,S) after S has been used. Taking closures yields the corner (R,P,S_net)=(a,b,-c). This is the conventional consumed-resource interpretation, and must not silently be called satisfaction of the stronger condition printed in Hsieh–Wilde Eq. (4).

If a bounded nonnegative input cost operator G obeys 0<=G<=H I and the ensemble mean cost e=sum_xy p(x)p(y|x)Tr G rho_xy is strictly below N, the codes can simultaneously obey the average input constraint Tr G_n rho_code <= nN, where G_n=sum_i G_i. They can also be expurgated to obtain vanishing conditional error and conditional trace secrecy for every retained public/private message pair, with the key still averaged. Cost refers to the average over messages and the consumed key, not a maximum-cost condition on every key value.

## 2. Elementary projector ingredients

The only nontrivial external matrix inequality used in the proof is Hayashi–Nagaoka, Lemma 2 / Eq. (15) of arXiv:quant-ph/0206186v4: for 0<=T<=I and U>=0, the square-root-measurement element associated with T satisfies

    I - (T+U)^(-1/2) T (T+U)^(-1/2) <= 2(I-T)+4U.

Inverses mean generalized inverses on the support; the residual kernel can be made a failure outcome. The proof in that primary source was inspected. The gentle inequality used below,

    ||rho - sqrt(L)rho sqrt(L)||_1 <= 2 sqrt(1-Tr Lrho), 0<=L<=I,

follows by purifying rho, applying L to the purification, evaluating the trace norm of the difference of the two rank-one (one subnormalized) operators, and tracing out the purifier. It applies to the correct branch of a measurement; normalization of that branch is not needed.

For a fixed finite ensemble, the following spectral-projector assertions are consequences of the scalar weak law, or exponential scalar concentration with fixed positive tolerances. Delete zero-probability letters. A state has finitely many positive eigenvalues; the random variable minus log of its sampled positive eigenvalue is bounded. For a product of copies of a state, retain eigenvectors whose mean minus-log-eigenvalue differs from the state's entropy by at most delta. The retained trace tends to one, the rank is at most 2^{m(S+delta)}, and the restricted state is bounded above by 2^{-m(S-delta)} times the projector.

Conditional projectors are tensor products of these projectors after grouping positions with equal x or equal (x,y). With x^n having type close to p_X, and y^n drawn from product_i p(y_i|x_i), conditional type concentration and these spectral laws give, uniformly in such x^n, the following assertions. For each system Z and any prescribed delta>0 there are projectors P=P_{x^n}^Z and Q=Q_{x^n,y^n}^Z, with Q=0 on conditionally atypical y^n, such that, for all sufficiently large n,

    rank P <= 2^{n(H(Z|X)+delta)},
    P sigma_{x^n}^Z P <= 2^{-n(H(Z|X)-delta)} P,
    rank Q <= 2^{n(H(Z|XY)+delta)},
    Q sigma_{x^n,y^n}^Z Q <= 2^{-n(H(Z|XY)-delta)} Q,
    Tr P sigma_{x^n}^Z >= 1-epsilon_n,
    E_y Tr Q sigma_{x^n,y^n}^Z >= 1-epsilon_n,
    epsilon_n -> 0.

Here sigma_{x^n} is product_i sigma_{x_i}; sigma_{x^n,y^n} is product_i sigma_{x_i,y_i}; Q commutes with the latter. To check uniformity: every positive x has n_x>=np(x)/2 for sufficiently narrow typicality, and every positive (x,y) has n_xy>=np(x)p(y|x)/4 on conditional typicality. The finitely many spectral laws therefore have lengths tending uniformly to infinity. Empirical entropy averages differ from the displayed p-weighted entropies by at most delta after reducing the type and spectral tolerances. Positions for zero-probability pairs never arise. Scalar union bounds handle the finite number of groups.

The unconditional analogue, with the alphabet x alone and the average sigma^Z, gives a global P and a conditional Q_{x^n} of rank at most 2^{n(H(Z|X)+delta)}, with P sigma^{Z tensor n} P bounded above by 2^{-n(H(Z)-delta)}P and both expected retained traces tending to one. These are precisely the rank, operator-norm and retained-mass properties needed below; no unproved operator concentration assertion is used.

## 3. Conditional packing bound

Fix a typical x^n and draw L independent y^n(l) from product_i p(y_i|x_i). Set Gamma_l=P Q_l P for system B and define the square-root POVM D_l=(sum_t Gamma_t)^(-1/2) Gamma_l (sum_t Gamma_t)^(-1/2). Gamma_l lies between zero and I. Its own-word expected acceptance obeys

    E[1-Tr Gamma_l sigma_l] <= epsilon_n+2 sqrt(epsilon_n).

Indeed Tr Gamma_l sigma_l=Tr Q_l P sigma_l P; compare it with Tr Q_l sigma_l using gentleness of P and then Jensen's inequality. For t!=l independence conditional on x^n gives

    E Tr Gamma_t sigma_l
      = E Tr Q_t P sigma_{x^n} P
      <= 2^{-n(H(B|X)-delta)} E rank Q_t
      <= 2^{-n(b-2delta)}.

The Hayashi–Nagaoka inequality therefore bounds the expected average error by

    u_n = 2epsilon_n+4sqrt(epsilon_n)+4L 2^{-n(b-2delta)}.

It tends to zero whenever log_2 L/n < b-2delta. Exactly the same argument for the unconditional projectors, with sigma^{B tensor n}, gives random HSW public packing at every r<a-2delta. This supplies the needed random-code expectation statement, rather than merely the existence of an unrelated public code.

## 4. Conditional soft covering without operator Chernoff

Fix a typical x^n and draw K independent y^n(s). For system E set tau_s=P Q_s sigma_s Q_s P and bar_tau=E tau_s. Then

    0<=tau_s<=A P,  A=2^{-n(H(E|XY)-delta)}, Tr tau_s<=1,
    D=rank P<=2^{n(H(E|X)+delta)}.

Two applications of gentleness and trace-norm contraction under multiplication by P give

    E||sigma_s-tau_s||_1
      <=2 sqrt(E[1-Tr P sigma_s])+2 sqrt(E[1-Tr Q_s sigma_s])
      <=4 sqrt(epsilon_n).

The independence of the samples cancels all centered cross terms:

    E Tr[(K^{-1}sum_s tau_s-bar_tau)^2]
      = K^{-1}(E Tr tau_s^2-Tr bar_tau^2) <= A/K.

For a Hermitian matrix supported on a D-dimensional subspace, its trace norm is at most sqrt(D) times its Hilbert–Schmidt norm. Jensen's inequality consequently gives

    E||K^{-1}sum_s sigma_s-sigma_{x^n}^E||_1
      <=8 sqrt(epsilon_n)+sqrt(DA/K)
      <=8 sqrt(epsilon_n)+2^{-n(k-c-2delta)/2},

where K>=2^{nk}. This bound tends to zero for k>c+2delta. The variance identity is valid for noncommuting random matrices; it uses only independence, linearity and positivity, not simultaneous diagonalization. This is sufficient for average trace secrecy. A doubly exponential probability estimate and union bound over exponentially many messages are unnecessary.

## 5. Construction and reliability

Choose J_n=floor(2^{nr}), M_n=floor(2^{np}), K_n=ceil(2^{nk}). Draw each cloud center x^n(j) independently from p_X tensor n. For every triple (j,m,s), independently conditional on the center, draw y^n(j,m,s) from product_i p(y_i|x_i(j)). On a message pair (j,m) and the preshared key s, Alice sends product_i rho_{x_i(j),y_i(j,m,s)}. The entire selected codebook is deterministic and public once chosen.

Bob first uses the public HSW square-root POVM Lambda_j constructed solely from the cloud centers and the channel x->sigma_x^B. He then uses the conditional packing POVM D_m^{j,s}, constructed from the satellite subcode indexed by (j,s). He knows s. For an atypical cloud center the latter may be any POVM; the probability of such a center tends to zero.

Conditional on all centers, averaging a transmitted satellite over its random draw gives exactly sigma_{x^n(j)}^B. Since the public decoder depends only on centers, its expected error on the true satellite code equals its expected error in the public random HSW code. Write v_n for this expected public error, so v_n->0. The expected conditional private error on the unmeasured satellite is at most u_n plus the probability of an atypical center, hence w_n->0.

For any realization of the codebook, correct joint-decoding probability is the average of

    Tr D_m^{j,s} sqrt(Lambda_j) sigma_{jms}^B sqrt(Lambda_j).

Comparing the subnormalized correct-public branch with sigma_{jms}^B by gentleness shows that the total expected decoding error is at most w_n+2sqrt(v_n), which tends to zero. This comparison already includes the public failure probability; one must not renormalize the correct branch and then forget its probability.

## 6. Secrecy and derandomization

For fixed (j,m), Eve's physical state after averaging the uniform consumed key is

    zeta_jm = K_n^{-1}sum_s sigma_{jms}^E.

For a typical center the preceding soft-covering estimate applies to this entire key-indexed collection. On an atypical center use the trivial trace-norm bound two. Thus

    E[(J_n M_n)^{-1}sum_jm ||zeta_jm-sigma_{x^n(j)}^E||_1] -> 0.

Because j and m are classical orthogonal blocks, that average is exactly the trace norm in the secrecy claim with

    omega_target^{J E^n}
      = J_n^{-1}sum_j |j><j| tensor sigma_{x^n(j)}^E.

This is a legitimate target state depending on the deterministic public code. Both the code and the actual public label are available to Eve. Bob's local trace-preserving decoding does not change the JE marginal. The consumed key may be correlated with the generated message and Eve at the end, and has not been included in the security promise.

Let F_n be the sum of the code's actual average decoding error and the displayed secrecy norm. Its ensemble expectation tends to zero, so Markov's inequality gives a high-probability set on which F_n tends to zero. The cost argument next proves that this set intersects the admissible-energy set; choose one deterministic code in the intersection for each n.

## 7. Average photon cost and expurgation

Define h(x,y)=Tr G rho_xy in [0,H]. The selected code's average cost per use is

    C_n=(n J_n M_n K_n)^{-1}sum_i,j,m,s h(x_i(j),y_i(j,m,s)).

For distinct positions i the entire random collections of cloud and satellite letters are independent. Each position's average V_i is in [0,H], and E V_i=e. Thus Hoeffding's scalar inequality gives, for every t>0,

    Pr{C_n>e+t} <= exp(-2nt^2/H^2).

This remains valid even if one or both message sets have cardinality one. Choose e<N''<N; the probability of C_n>N'' tends to zero. Together with Markov's inequality for F_n, it supplies the admissible deterministic code asserted above. No unbounded observable is estimated by trace-distance continuity; G is bounded because the photon cutoff is fixed before the n->infinity coding limit.

If a maximum over retained public/private message pairs is required, let f_jm be their conditional error averaged over S plus ||zeta_jm-sigma_{x^n(j)}^E||_1. The average is F_n. Delete public rows with row average exceeding sqrt(F_n); the fraction deleted is at most sqrt(F_n). In each remaining row delete private messages with f_jm>F_n^(1/4); the fraction deleted is at most F_n^(1/4). Keep the same number of private messages in every row and relabel them, depending on j. Each retained pair then has f_jm->0; J and M can again be chosen independently and uniformly on their retained sets. Key size and key distribution are unchanged. Rates change by o(1). Because all costs are nonnegative, the new average cost is at most N'' divided by the two retained fractions, hence <=N for sufficiently large n. Arbitrary further deletions to equalize row sizes have the same lower bound on retained fractions. The resulting claim is about message-pair conditional secrecy with the consumed key averaged; it is not a joint secrecy claim for that key, nor a semantic-security theorem.

If G=0 or e=0, the cost is identically zero: nonnegative h with zero ensemble mean vanishes on the sampled support. If e=N exactly, approach the desired point with ensembles of cost strictly below N and use closure. For bosonic Gaussian ensembles this can be achieved by reducing modulation/thermal energy before finite-alphabet discretization and photon cutoff; that approximation is a separate task and is not proved by this finite-dimensional lemma.

## 8. Endpoints and scope of the repair

If a=0 use one cloud. If b=0 use one private message. At c=0 take arbitrarily small positive k and pass to closure, giving zero consumed-key rate; one may also omit the key if the ensemble's conditional Eve states are exactly identical. With a bosonic per-mode photon cutoff H, pure loss maps the cutoff input into finite B and E supports with photon number at most H, so this finite proof applies without output truncation. For a general finite input channel whose outputs are infinite dimensional, a separate output approximation would be required.

The lemma proves achievability of the father corner under conventional secrecy. Combined algebraically with private-to-public, private-to-key, and one-time-pad resource vectors

    (1,-1,0), (0,-1,1), (-1,1,-1),

the corner has the usual three half-space bounds

    R+P<=a+b, P+S<=b-c, R+P+S<=a+b-c.

Indeed their deficits are precisely the three nonnegative coefficients of these conversion vectors, in order second, first, third. Algebra alone does not prove every catalyst-elimination convention: sequencing, composition error control, and permitted resource cancellation must be treated in the overall dynamic-capacity argument. The standard finite-block father proof above does not supply or assume a residual-secret-key promise.

## 9. Primary-source cross-check and attribution

Hsieh–Wilde, arXiv:0903.3920v1, Sec. IV Eq. (4), includes Bob's consumed-key register in its secrecy target; its discussion confirms that interpretation. That condition exceeds the conventional consumed-key promise, and ordinary OTP fails it. Its Sec. VI pastes conditional private codes into an HSW public code. The present construction follows that established architecture, but supplies a direct generated-message secrecy proof and bounded-cost selection without invoking its stronger condition.

The preceding Hsieh–Luo–Brun paper, arXiv:0806.3525v1 / Phys. Rev. A 78, 042306 (2008), Sec. III.A Eq. (11), measures secrecy of the decoded message and Eve after tracing the consumed-key registers. Its covering argument randomizes Eve by averaging the shared key. Devetak, arXiv:quant-ph/0304127 (IEEE Trans. Inf. Theory 51, 44–55 (2005)), provides the established cq packing/covering private-coding architecture. The key-selected random satellite proof is a rederivation/repair using known machinery, not evidence that a new coding theorem has priority. Any novelty claim needs a separate literature audit.

Sources actually inspected online on 2026-10-06 Pacific: https://arxiv.org/pdf/0903.3920 ; https://arxiv.org/pdf/0806.3525 ; https://arxiv.org/pdf/quant-ph/0304127 ; https://arxiv.org/pdf/quant-ph/0206186 . Exact remotely retrieved byte hashes, without cached PDFs, are recorded separately.
