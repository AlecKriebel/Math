# Operational achievability and preservation of the average photon constraint

Checkpoint: 2026-10-06 21:22:43 Pacific (2026-10-07 04:22:43 UTC).

This supplements CONDITIONAL_DERIVATION.md and PRIVATE_SECURITY_DEFECT_AND_REPAIR.md. It closes the previously recorded mean-cost direct-coding audit item. The entropy premise (VE) remains wholly separate. The private proof here uses conventional **generated-resource secrecy (GEN)** and does not assert the false literal joint consumed-resource secrecy promise printed in the cited papers.

## 1. Finite approximants with strict energy margin

Fix \(N>0\), \(0<N'<N\), and a desired sharing parameter \(\lambda\in[0,1]\). The alphabet/Fock approximations in CONDITIONAL_DERIVATION.md produce:

* a finite quantum ensemble \(\{p_x,\rho_x\}\), with a purification of each \(\rho_x\), all supported on the physical photon subspace \(\mathcal H_K=\operatorname{span}\{|0\rangle,\ldots,|K\rangle\}\);
* a finite private ensemble \(\{p_xp_{y|x},\psi_{xy}\}\), each \(\psi_{xy}\) pure and supported on \(\mathcal H_K\).

Both have average one-use photon cost

\[
\mu=\operatorname{Tr}a^\dagger a\sum_xp_x\rho_x\le N'
\]

(with \(\rho_x=\sum_yp_{y|x}\psi_{xy}\) in the private case). Their entropy values tend to the Gaussian target values at \(N'\). On this fixed finite channel, the one-use cost observable \(G=a^\dagger a|_{\mathcal H_K}\) is positive and has \(\|G\|_\infty=K\); its block observable \(G_n=\sum_jG_j\) has \(\|G_n\|_\infty=nK\). Pure loss and its complement both preserve this finite photon cutoff. The following arguments take the coding block length to infinity **with this finite approximant held fixed**. Only afterward are alphabet and cutoff limits taken.

## 2. Quantum father: the required input-distribution statement is explicit

Primary source: Hsieh–Wilde, *Entanglement-assisted communication of classical and quantum information*, arXiv:0811.4227v4 (3 March 2010), IEEE Trans. Inf. Theory **56**, 4682–4704, DOI 10.1109/TIT.2010.2053903. In its Sec. VI.C, Definition 2, Eq. (50), a random father code is called \(\rho\)-like precisely when its **expected channel input density operator** is close in trace norm to \(\rho^{\otimes n}\). Proposition 2 asserts such codes. Sec. VI.D, Definition 3 and Proposition 3, assert the corresponding statement for every typical classical string \(x^n\), with target \(\rho_{x^n}=\bigotimes_j\rho_{x_j}\). This includes averaging the operational maximally mixed quantum source and consumed entanglement in each code input; it is not merely a claim about an output or a reference system.

The source constructs a classically enhanced father code by choosing public/classical codewords \(x^n(m)\) in a strongly typical set, applying a random conditional father code to each, decoding the classical message first and then the quantum message. Proposition 4 gives the HSW code, and Sec. VI.F gives vanishing expected combined classical/quantum error. Its Appendix A proves the \(\rho\)-like property including internal expurgation. We use this property directly, without appending an uncontrolled maximum-message-error expurgation that might change cost.

For every \(p\)-typical string with

\[
\left|\frac{n_x}{n}-p_x\right|\le\delta\quad\text{for each }x,
\]

put \(c_x=\operatorname{Tr}G\rho_x\in[0,K]\). Then

\[
\frac1n\operatorname{Tr}G_n\rho_{x^n}
=\sum_x\frac{n_x}{n}c_x
\le\mu+\delta\sum_xc_x
\le\mu+\delta|X|K.
\]

If \(\mathbb E_C\bar\rho_{C,m}\) is the average physical input of the conditional random father code for message \(m\), the cited proposition gives

\[
\|\mathbb E_C\bar\rho_{C,m}-\rho_{x^n(m)}\|_1\le\epsilon.
\]

The bounded cutoff observable therefore gives, for every classical message,

\[
\frac1n\operatorname{Tr}G_n\mathbb E_C\bar\rho_{C,m}
\le\mu+\delta|X|K+K\epsilon.
\]

Averaging uniform classical messages yields exactly the same bound for the expected operational average code input. Taking \(\delta,\epsilon\) sufficiently small makes the last expression \(\le N''\) for some fixed \(N'<N''<N\). This proves the requisite average-cost statement, rather than assuming that input-state entropy calculations automatically constrain the constructed code.

### Simultaneous selection of low error and admissible cost

Let \(Z_C\ge0\) be the combined operational trace-distance/error criterion of the random classically enhanced father code; the source construction gives \(\mathbb E Z_C\to0\). Let \(A_C=\operatorname{Tr}G_n\bar\rho_C/n\ge0\) be its average photons per use. The preceding paragraph gives \(\mathbb E A_C\le N''\). Markov gives

\[
\Pr\{A_C>N\}\le\frac{N''}{N}<1,
\quad
\Pr\{Z_C>\sqrt{\mathbb E Z_C}\}\le\sqrt{\mathbb E Z_C}.
\]

For large enough \(n\), the good-cost event and the vanishing-error event have a nonempty intersection. A deterministic code chosen in that intersection has average photons at most \(N\) and vanishing error. Rates approach the father point

\[
\left(I(X;B),\frac12I(A;B|X),-\frac12I(A;E|X)\right).
\]

Adding the usual noiseless resource cone gives the three entropic dynamic inequalities. Those ideal resource conversions do not add photons to the noisy channel inputs. The code is used on the maximally mixed/entangled-reference source required by the original dynamic convention; no maximum-cost guarantee for every arbitrary quantum source is inferred from this average-cost selection.

## 3. Private father under GEN: direct construction without the defective promise

The private source is inconsistent if one interprets its secrecy formulas as promises about consumed key remaining jointly independent of Eve. The underlying random covering construction nevertheless supports the conventional **message-only / generated-resource** statement, which can be checked independently.

Primary inputs for this check:

* Hsieh–Luo–Brun (HLB), *Secret-key-assisted private classical communication capacity over quantum channels*, arXiv:0806.3525v1, Phys. Rev. A **78**, 042306 (2008). Section III defines the cq protocol's security by its decoded **private message** decoupled from Eve, Eq. (11); no consumed-key share occurs in the ideal secret output. Its Corollary 1 / Eq. (16) and direct proof Eqs. (22)–(24) give trace-norm quantum covering by averaging over the shared key.
* Devetak, *The private classical capacity and quantum capacity of a quantum channel*, arXiv:quant-ph/0304127v6 (21 October 2004), IEEE Trans. Inf. Theory **51**, 44–55 (2005). Lemma 2 is the Ahlswede–Winter operator Chernoff bound; the direct proof of Theorem 1 develops the typical-subspace trace-norm covering and cq packing arguments. Appendix A gives the strongly/conditionally typical definitions and estimates needed to paste conditional ensembles.
* Hsieh–Wilde, *Public and private communication with a quantum channel and a secret key*, Phys. Rev. A **80**, 022306 (2009), arXiv:0903.3920v1. Sec. VI, Propositions 3–5, supplies random private code input closeness and conditional code pasting plus the public HSW decoder. Its printed Eq. (4) asserts excess joint consumed-key secrecy; we **do not use that assertion**. Its actual averaging-over-key covering mechanism is read with the correctly specified GEN output promise.

The HLB generic quantum capacity formula has a later correction (Wilde, Phys. Rev. A **83**, 046303 (2011)); this note does not use that generic optimization. It uses only its finite cq packing/covering mechanism, directly supported by Devetak's Chernoff/typical estimates. This is an inherited coding construction, not a claim of new machinery.

### The finite cq lemmas being used

For a finite ensemble \(\{p_y,\tau_y^{BE}\}\) on finite-dimensional systems:

1. **Packing.** A codebook of \(2^{mP}\) sequences sampled from the pruned strongly typical distribution, with product output states at Bob, has a decoder with expected average error tending to zero whenever \(P<I(Y;B)\).
2. **Covering.** For \(2^{mS}\) independent sampled sequences, their average product Eve output is close in expected trace norm to the pruned average product state (and hence to \((\sum_yp_y\tau_y^E)^{\otimes m}\)) whenever \(S>I(Y;E)\). This follows by projecting onto the typical and conditionally typical subspaces, applying the operator Chernoff bound with typical rank exponent \(H(E)\) and conditional eigenvalue exponent \(H(E|Y)\), then removing those projections by the gentle measurement lemma. The threshold is their difference \(I(Y;E)\). Uniform finite error bounds hold for sufficiently large \(m\); the tail estimates are stronger than needed here.

These are exactly the direct-code lemmas just identified, applied to the fixed finite cutoff channel. To obtain conditional versions for \(x^n\), partition the positions into the finitely many \(x\)-classes and paste the corresponding one-ensemble codes. Tensor-product trace distances are at most the sum of the finitely many class distances. No unproved infinite-dimensional covering lemma is used.

### A conditional private code with an indexed shared key

For the seed \(p_xp_{y|x}\psi_{xy}\), let

\[
r_x=I(Y;B)_{\omega_x},\qquad s_x=I(Y;E)_{\omega_x},
\]

where \(\omega_x=\sum_yp_{y|x}|y\rangle\langle y|\otimes U\psi_{xy}U^\dagger\). Choose a public codebook \(x^n(k)\), each \(\delta\)-typical, of rate slightly below \(I(X;B)\), with the HSW decoder for target outputs \(\bigotimes_jB_{x_j(k)}\), where \(B_x=\sum_yp_{y|x}B_{xy}\).

For every \(x\) with \(p_x>0\), choose a fixed uniform private submessage \(m_x\) with rate below \((p_x-\delta)_+(r_x-\gamma)_+\) per total channel use, and an independent uniform shared key subregister \(s_x^{\mathrm{key}}\) with rate at least \((p_x+\delta)(s_x+\gamma)\) per total channel use. Integer rounding is sublinear. The tensor product of the submessages is the private message \(m\), and the tensor product of the keys is the consumed key \(s\). Their dimensions are fixed across all public messages. As \(\delta,\gamma\downarrow0\), their total rates approach

\[
P_0=\sum_xp_xr_x=I(Y;B|X),\qquad
S_0=\sum_xp_xs_x=I(Y;E|X).
\]

For each public \(k\), each key value \(s\), and each private message \(m\), generate the physical product input by independently sampling the \(y\)-sequence in each \(x\)-class from its pruned conditional distribution. This is an ordinary finite lookup encoding map \((k,m,s)\mapsto y^n(k,m,s)\), allowed by the general CPTP encoder; it need not obey the unnecessary restricted cyclic-encryption form printed in the earlier father paper.

For each known \(k,s\), Bob decodes the private submessage in each \(x\)-class using the packing lemma. The actual class length lies between \(n(p_x-\delta)\) and \(n(p_x+\delta)\), so the chosen private rate is below its packing threshold and the key rate is above its covering threshold. The public HSW measurement is performed first. Its expected error remains small because, for each \(k\), averaging the random inner code and uniform private/key indices gives the pruned product input close to \(\bigotimes_j\rho_{x_j(k)}\). Linearity controls the expected public decoding error. The gentle measurement lemma and Jensen control its expected disturbance, after which the conditional private decoders have vanishing expected average error. This is the code-pasting argument behind the cited public/private father construction, now with a correct secrecy promise.

For each fixed \(k,m\), average Eve's state over the shared key. In each \(x\)-class, the covering lemma makes it close to a state depending only on the public word \(k\), not on \(m_x\). Since the keys for the finitely many classes are independent, their averages tensor together. Thus

\[
\mathbb E_C\frac1{|K||M|}\sum_{k,m}
\left\|\frac1{|S|}\sum_s E_{k,m,s}-\zeta_k^E\right\|_1\longrightarrow0,
\]

where \(\zeta_k^E\) is a product state depending only on \(k\). This is exactly the trace norm of the generated-message/public-reference/Eve cq state's deviation from \(\pi^M\otimes\sum_k |K|^{-1}|k\rangle\langle k|\otimes\zeta_k^E\). It proves GEN for this father code. It says nothing about Eve being independent of the joint pair \((M,S_B)\), which generally would be false.

Only **average uniform-source secrecy** is needed, so there is no union over exponentially many messages or a semantic-security upgrade. All input observables remain bounded by \(nK\). The same typical-cost calculation and Markov selection as in Sec. 2 selects one random lookup table satisfying the mean energy budget and vanishing sum of public error, private error, and GEN trace distance. Alternatively, strongly conditional typical product words give direct cost control, but the expected-cost argument alone already proves the required average constraint.

The achievable father resource point is therefore

\[
\left(I(X;B),\ I(Y;B|X),\ -I(Y;E|X)\right)
\]

under GEN, with average noisy-channel input cost at most \(N\). Adding the conventional one-time-pad, private-to-public, and key-distribution resource cone gives the full one-seed private inequalities. Generated-key privacy composes in the usual way because every key used for encryption is **consumed** and is omitted from the final secret-output promise. The zero-channel cone is thereby admissible under GEN, whereas it was excluded by the literal condition (LIT).

## 4. Ordered limits and exact claim

For each finite approximant use the fixed \(N'<N\) margin, take block length to infinity, and obtain the corresponding finite-seed rates and trace-decoupling guarantee with mean cost at most \(N\). Then let the alphabet/cutoff approximations converge, so their four entropy values converge by bounded-energy continuity; finally let \(N'\uparrow N\). Rates on faces are included by capacity-region closure. The parameter endpoints are implemented by point-mass distributions rather than zero-variance densities. At \(N=0\), no approximation is necessary: the channel inputs are vacuum and only the explicitly checked noiseless resource cones are used.

This proves achievability of the quantum region in its original net-resource convention, and of the private region in the explicitly repaired GEN convention. Combined with the repaired converse and (VE), it is a complete **conditional** mathematical reduction for those models. It is not an unconditional proof of (VE), not a proof of the literal-source private target, not a formal verification, and not publication clearance.
