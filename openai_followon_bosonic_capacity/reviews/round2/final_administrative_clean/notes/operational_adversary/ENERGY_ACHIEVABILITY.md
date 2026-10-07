# Energy-controlled achievability and generated-secret private coding

Timestamp: 2026-10-07T04:24:58.942753+00:00
Status: checkable construction reducing energy control to finite-dimensional established packing/decoupling/covering primitives. This does not certify the upstream entropy premise. Mathematical/operational audit completion estimate 90%; publication-package completion estimate 5%.

## 1. Finite Gaussian ensemble approximation with strict cost slack

Fix N_0<N (N=0 uses the unit-resource cones). Quantum seed rho_alpha=D(alpha) theta_M D(alpha)^dagger has M=lambda N_0 and centered isotropic Gaussian displacement variance v=(1-lambda)N_0. Truncate the Gaussian to |alpha|<=R and normalize. Its conditional mean-square displacement decreases. Partition the disk into finitely many cells, replacing alpha in each cell by its conditional mean alpha_j. Jensen gives sum_j p_j|alpha_j|^2<=v, and the mean displacement remains zero. Therefore the discrete ensemble average photon cost is <=M+v=N_0.

The trace-norm map alpha->D(alpha)theta_M D(alpha)^dagger is uniformly continuous on a compact disk. Displacement quantization converges in trace norm; sending R to infinity converges to the original averaged thermal state. All averaged states obey one common mean-energy bound N_0. The oscillator Gibbs entropy continuity property (finite partition function at every inverse temperature) therefore implies convergence of the averaged Bob entropy. Conditional input/Bob/Eve entropies before cutoff are exactly g(M),g(eta M),g((1-eta)M), regardless of alpha.

Now apply the CPTP vacuum-replacement Fock cutoff T_K(rho)=P_K rho P_K+Tr[(I-P_K)rho]|0><0| to each of the finitely many conditional states. This never increases photon cost and converges to each rho_j in trace norm. Conditional energies are uniformly bounded by M+R^2, hence their input/Bob/Eve entropies converge by energy-constrained continuity. Purify each finite state T_K(rho_j) using a reference of dimension at most K+1. The pure-loss isometry maps this input space into finite Bob and Eve spaces, each spanned by number states 0,...,K. Thus all coding primitives below are finite-dimensional. Order the limits: for each fixed N_0, R, mesh, K, carry out coding; then increase approximation quality, and finally let N_0 increase to N. No cutoff is sent to infinity along an unproved coding error estimate.

For the private ensemble, independently truncate and centroid-quantize centered Gaussians alpha,beta of variances (1-lambda)N_0 and lambda N_0. Centering is preserved by conditional centroids. Therefore E|alpha_j+beta_k|^2=E|alpha_j|^2+E|beta_k|^2<=N_0. Replace each coherent vector by P_K|alpha_j+beta_k>/||P_K|alpha_j+beta_k>||. Its photon distribution is Poisson conditioned on n<=K, so its conditional mean photon number does not increase. The resulting finite nested pure ensemble has cost <=N_0. Uniform compact-amplitude convergence plus energy entropy continuity gives convergence of the four private entropies, including the per-pure-input Bob entropy tending to zero. Degenerate Gaussian variances at lambda=0 or 1 use the one-point distribution at zero.

## 2. Exact spectral-type energy lemma

Let rho=sum_i p_i |i><i| be a finite-dimensional input state, deleting zero p_i. Let H be the bounded restriction of photon number (||H||<=K), and e_i=<i|H|i>. For a rational type q with counts l q_i integers, let P_q be the span of all tensor eigenbasis strings with exactly those counts. Then

P_q H_l P_q = l(sum_i q_i e_i) P_q,   H_l=sum_{a=1}^l H_a.                 (E1)

Proof: H_a changes only one tensor index. An offdiagonal eigenbasis change i->j with i!=j changes the spectral type, so its compression to one fixed type is zero. Each diagonal entry has exactly l q_i occurrences of e_i. This proves the operator identity, not merely a cost statement for one mixed seed. In particular EVERY state, including arbitrary coherent/entangled states, supported on P_q has exactly the cost in (E1).

Let d_q=rank P_q and tau_q=P_q/d_q. Choose q=q_l with ||q_l-p||_1=O(1/l). The classical type bounds give

D(tau_q || rho^tensor l)=l D(q||p)+l H(q)-log d_q=O(log l).               (E2)

Here D(q||p)=O(1/l^2) for fixed positive p, and l H(q)-log d_q<=r log(l+1), where r=rank rho. Every one-mode marginal of tau_q is rho_q=sum_i q_i|i><i|. For any finite-dimensional output channel Phi, write sigma=Phi(rho). Data processing gives D(Phi^tensor l(tau_q)||sigma^tensor l)=O(log l). On the support of sigma,

S(Phi^tensor l(tau_q))
= -l Tr[Phi(rho_q)log sigma] - D(Phi^tensor l(tau_q)||sigma^tensor l).

Since ||rho_q-rho||_1=O(1/l) and log sigma is bounded on its finite support,

S(Phi^tensor l(tau_q))/l -> S(Phi(rho)).                                (E3)

Take Phi to be the identity, Bob channel or complementary Eve channel. Zero output eigenvalues cause no divergence: Phi(rho_q) and every full output lie in the support of sigma because q and p have the same input support for sufficiently large l.

## 3. Preserve the average-output entropy and the classical rate

Using one conditional label x repeated l times would lose the desired classical rate. Instead start with a fixed finite ensemble {p_x,rho_x} from Section 1, and use a whole label sequence z=x^l as the superletter label.

Draw z from p_X^tensor l, conditioned on a classical typical set with tolerance delta_l=l^(-1/4). Its excluded probability is exponentially small in sqrt(l), and every x with p_x>0 occurs l[p_x+O(delta_l)] times. For each group of n_x equal symbols x, replace rho_x^tensor n_x by tau_(q_x(n_x)), with q_x(n_x)=spectrum(rho_x)+O(1/n_x). Permute the tensor factors back into z order. Call the result tau_z and its supporting type-product subspace P_z. Each tau_z is uniform on P_z.

The same one-site compression argument yields
P_z H_l P_z = c_z P_z,
c_z=sum_x n_x sum_i q_(x,i)(n_x) e_(x,i)
<=l[N_0+delta_l sum_x Tr(H rho_x)+O(1/l)]<lN                           (E4)
for all typical z and sufficiently large fixed l. Thus the budget holds uniformly for every quantum state in every conditional coding subspace P_z.

Let p_l(z) be the pruned label distribution, bar_tau_l=sum_z p_l(z)tau_z, and bar_rho=sum_x p_x rho_x. Consider the original joint classical/input product ensemble Omega_l and the modified ensemble Omega_l'. Their relative entropy obeys
D(Omega_l'||Omega_l)=D(p_l||p_X^tensor l)+sum_z p_l(z)D(tau_z||rho_z)=O(log l),
because each n_x is proportional to l and there are finitely many x. Consequently
D(bar_tau_l||bar_rho^tensor l)=O(log l),
and the same holds after Bob's product channel.

Rounding each conditional spectrum changes the per-mode marginal by O(1/l); conditioning on the typical set changes expected symbol frequencies by an exponentially small amount. The ensemble and state are permutation invariant when identical count rules are used for all sequences of the same type. The finite-output cross-entropy identity from (E3) therefore gives
S(B^tensor l(bar_tau_l))/l -> S(B bar_rho).
Similarly, averaging the conditional (E3) identities gives
sum_z p_l(z)S(tau_z)/l -> sum_x p_x S(rho_x),
sum_z p_l(z)S(B^tensor l tau_z)/l -> sum_x p_x S(B rho_x),
sum_z p_l(z)S(E^tensor l tau_z)/l -> sum_x p_x S(E rho_x).               (E5)
These are exactly the four quantum entropies required by WHG Proposition 1. The construction uses a finite (possibly enormous) superletter alphabet for each fixed l; there is no asymptotic cardinality restriction.

## 4. Father codes on uniform restricted subspaces

Apply the established finite-dimensional father decoupling theorem to each restricted physical superletter channel with input space P_z and maximally mixed seed tau_z. The underlying random isometric subspace code can be sampled with a Haar unitary on P_z^tensor m. For any fixed encoding subspace dimension and maximally mixed quantum source/ebit halves, Haar invariance gives EXACTLY
E_C rho_(C,z)=tau_z^tensor m.

Unlike a general weighted seed, no claim that a maximally mixed typical subspace is trace-close to rho^tensor m is needed here. The standard father decoupling proof gives a vanishing average quantum error at any strict backoff from 1/2 I(A;B) and with strict excess over 1/2 I(A;E). The Haar ensemble has the exact expected input property needed for HSW piggybacking.

Paste these father codes for an outer classical sequence of superletter labels, as in Hsieh--Wilde arXiv:0811.4227v4 Propositions 3--4 and Section VI.E. The decoder first decodes the classical label by HSW and then decodes the appropriate father code; the gentle measurement estimate preserves quantum fidelity. All conditional encoders output into tensor products of the P_z spaces. By (E4), any state they encode, including one entangled with the message/reference, has mean total cost <physical_uses*N. Discarding unused o(m) positions can be done with vacuum, or preparing their designated tau_z states satisfies the same uniform cost bound. Classical message expurgation and derandomization cannot increase the uniform subspace cost bound. This closes the energy step without altering quantum systems after encoding.

Primitive dependency still required, stated explicitly: the ordinary finite-dimensional father Haar-decoupling theorem. The CEF Appendix A offers a weighted rho-like proof via a coherified private-code construction; that route should not be used uncritically given defects in the old private-key statements. The uniform-state construction above permits use of the direct father decoupling theorem from Abeyesinghe--Devetak--Hayden--Winter instead. It has not been formally verified in this project; it is an established coding theorem dependency.

## 5. Private father corner from generated-message-only secrecy

The erroneous requirement that consumed key remain secret jointly with generated message is unnecessary for achievability. Work with a finite cq channel y->(B,E), chosen distribution p_y, and a table of independent product codewords indexed by private message m and preshared key s. The key is uniform and unknown to Eve. For a fixed key s, Bob knows the column codebook and HSW-decodes m reliably at any rate P<I(Y;B). For a fixed message m, averaging the unknown key s mixes a row of L=2^(nS) iid Eve states. Quantum covering gives a common Eve state whenever S>I(Y;E). The obtained secrecy state is pi^M tensor omega^E after averaging over S, not pi^(M S) tensor omega^E.

The primary covering primitive is Devetak, arXiv:quant-ph/0304127, Lemma 2 (Ahlswede--Winter operator Chernoff), Lemma 3 (gentle measurement), and the direct proof of Theorem 1. Its typical projected states satisfy a norm bound 2^(-n[H(E|Y)-delta]) and live in output typical support rank at most 2^(n[H(E)+delta]). After spectral trimming, normalized expectation is bounded below by a factor proportional to 2^(-n[I(Y;E)+O(delta)]). For L=2^(n[I(Y;E)+strict_gap]), operator Chernoff makes the covering failure probability decrease faster than an ordinary exponential. Undoing typical projections gives vanishing trace distance. Choosing strict gaps allows exponentially small typical-tail and trace-distance bounds; the finite message-register continuity estimate then also gives mutual-information strong secrecy. No Eve access to the consumed key is assumed after conditioning the generated message; the key is consumed.

For each outer typical x^n, paste these scalar cq codes in x-groups, with independent key and private-message subblocks, so the rates approach I(Y;B|X) and I(Y;E|X). Pasting produces a product target rho_(x^n) and expected input trace-close to it. The outer HSW code at R<I(X;B) then piggybacks on these private codes, with its gentle measurement preserving inner reliability. Eve may additionally be given the public message x-label; covering is imposed for each outer label and private message after averaging the key. Thus the corner
(R,P,S_net)=(I(X;B), I(Y;B|X), -I(Y;E|X))
is achieved under conventional generated-secret security.

This suffices for every one-state private polyhedron: add the known unit cone generated by secret-key distribution, one-time pad and private-to-public transmission, with correct accounting of consumed key. There is no need to establish a larger superposition region with an extra local randomization variable before obtaining the target corner.

## 6. Private input cost directly by classical type pruning

For the finite pure ensemble {p_x p_(y|x),psi_xy}, let e_xy=Tr(H psi_xy). Construct the random outer/inner tables with conditionally pruned typical sequences (the same pruning used in the primary covering proof). Every selected product word then has joint symbol frequencies within delta of p_xy. Its exact mean photon cost is
sum_a e_(x_a,y_a) <= n[N_0+delta sum_xy e_xy]<nN
for sufficiently small fixed delta. This is mean photon cost of a product quantum codeword; it does not claim a deterministic photon-number occupation cutoff.

Pruning conditional distributions changes expected input states by only the typical-tail probability and preserves the packing and covering estimates with strict gaps. No post-encoding quantum projection or abort is needed, and no new public leakage register is introduced. Averaging messages and key preserves the same cost bound; classical expurgation preserves it as well. Tensor-product private words are sufficient for this achievability construction, while the converse still allows arbitrary entangled states across noisy uses.

## 7. Alternate cutoff proof if a code-family expected input statement is used

For comparison, fixed finite cutoff K and conditional product targets rho_(x^n) suffice; they need not combine to a globally iid theta^tensor n. If E_C rho_(C,m) is gamma_n-close to its product target and every target has mean energy <=n(N-Delta), classical Chernoff/Hoeffding on the photon measurements gives target probability above nN at most exp(-2nDelta^2/K^2). A total-photon vacuum-replacement preencoder therefore has expected failure at most that tail plus gamma_n. Its Stinespring isometry differs from the identity-with-fixed-success-environment on any purified input by trace distance <=2sqrt(2q). This bounds reliability/secrecy disturbance even when Eve receives the failure garbage. Average disturbance tends to zero by Jensen; deterministic input photon support is <=nN for every resulting code.

This alternate proof requires actual gamma_n decay for the selected code ensemble, and strong mutual-information secrecy requires sufficiently fast (e.g. exponential) decay. The exact spectral-type quantum construction and private joint-type pruning above avoid relying on this alternate step.


## 8. Direct primary check of the uniform-seed father dependency

Read Abeyesinghe--Devetak--Hayden--Winter, arXiv:quant-ph/0606225, Sections IV/V/VIII and Appendix A. Section IV.2 proves the Haar decoupling bound by a second-moment calculation. Section V transposes the Haar reference transformation to Alice and writes W_2=W_1 U^T (Eq.(32)). Section VIII explicitly selects a typical spectral type with a maximally mixed input on that type subspace. This primary proof does not depend on the disputed private-key theorem.

For our uniform restricted seed tau=P/d, the finite encoder can have a fixed averaged input arbitrarily close to tau^tensor m. Select a logical key-entanglement dimension S near 2^(m[I(A;E)/2+gap]), a logical quantum-message dimension M=floor(d^m/S), and an embedding W_1:C^(M S)->P^tensor m. The maximally mixed encoded input is W_1 pi_(MS) W_1^dagger, so
||W_1 pi_(MS) W_1^dagger-tau^tensor m||_1=2(1-MS/d^m)<=2S/d^m=O(1/M).
Transposing the reference Haar unitary changes W_1 to W_1 U^T, which leaves this averaged input exactly unchanged. Thus the input closeness does not depend on selecting a favorable random code. With a positive limiting quantum rate, M grows exponentially. Rank-one seeds have no quantum father contribution and use ordinary HSW; zero quantum boundary rates follow by closure.

The usual output typical projections in the direct decoupling proof have exponentially small excluded probability at fixed rate slack. They do not change the physical encoder support: the encoder remains in P^tensor m. Transferring the projected-state error estimate back to the actual unprojected channel uses the gentle-measurement and triangle estimates of the primary proof. This is the established father theorem with an additional elementary uniform-seed input observation; the follow-on capacity theorem itself is not formalized here.

Attribution: exact spectral types already appear in ADHW's father proof. Do not present the type machinery as an invented protocol or as an independent solution of a known coding theorem. The operator compression identity (E1) and the full-sequence relative-entropy bookkeeping supply transparent energy control for the present reduction, but any novelty claim for them requires literature audit.
