# Markov-limit topology: an infinite candidate distance and a zero-time obstruction

**Original target unresolved; three scoped approaches; independent review pending.** The proposed distance in Aldous's 2018 slide can be infinite even for a normalized two-dimensional torus diffusion limit. A trace-adapted weight gives a complete separable realization with continuous positive-time transition densities, under a stated semigroup hypothesis. However, its completion can add a state that immediately disperses into a nontrivial mixture. Thus this construction does not in general produce the required Feller process. No novelty or full-resolution claim is made.

## 1. Exact target and conventions

[Aldous's maintained problem page](https://www.stat.berkeley.edu/~aldous/Research/OP/compact.html) links a seven-page [original note](https://www.stat.berkeley.edu/~aldous/Talks/MCcompact.pdf) and five [2018 slides](https://www.stat.berkeley.edu/~aldous/Research/OP/talk_towsner_2018.pdf). The original compactness is a compactness assertion about sequences of finite reversible chains, not an assumption that a proposed state space is compact. For a finite chain with stationary probability π, the relevant kernel is its transition **density** relative to π. With n uniform states, this is n times the transition probability. The trace is G(t)=Σ_x P_t(x,x), normalized by G(1)=2, and the boundedness assumption controls G(t) at every positive time.

Convergence is distributional convergence of arrays of transition densities sampled at independent stationary states, for finitely many array coordinates and times. It is not a given path-space convergence or a pre-existing common state topology. The final slide suggests

\[
d_0(x,x')^2=\int_0^\infty e^{-t}\int
 |p_t(x,y)-p_t(x',y)|^2\,\pi(dy)\,dt.\tag{1}
\]

It asks for a natural complete separable state topology and a Feller process realization. Formula (1) is introduced as an example, so its failure does not disprove existence of another topology. The preceding slide leaves the condition at time zero as unspecified “pinning.”

[Towsner's measure-theoretic result](https://arxiv.org/abs/1404.3815), Electron. J. Probab.20(2015), no.77, DOI10.1214/EJP.v20-4188, supplies density-array limits and discusses quotienting indistinguishable states. Its Definition2.6 specifies continuity at **positive** times in L²; it does not itself give Feller behavior at time zero on a complete state topology. [Landim's topology](https://arxiv.org/abs/1310.3646) concerns convergence of paths when some states become instantaneous. It does not supply the requested state-space realization for arbitrary density-array limits.

Throughout the positive construction below, we explicitly assume a symmetric strongly continuous Markov semigroup on L² of a standard probability space, with trace-class operators at all positive times. This is a precise stronger zero-time hypothesis than the positive-time continuity in Towsner's definition; it holds in both explicit examples below. We preserve the information visible to the transition densities by a measurable map and may identify states having identical density rows. We do not assert a pointwise bijection preserving arbitrary invisible labels.

A necessary process-level property will be

\[
P_t(z,\cdot)\Rightarrow\delta_z\quad(t\downarrow0)
\quad\hbox{for every state }z.\tag{2}
\]

In particular any realization with paths right-continuous at their initial time must satisfy (2). Positive-time continuity of kernels alone does not prove (2), regardless of the convention used for the word Feller.

## 2. The slide's distance diverges on a genuine finite-grid limit

On the flat torus \(\mathbb T^2=\mathbb R^2/\mathbb Z^2\), with Haar probability, take the heat semigroup with generator aΔ, a>0. Its density and trace are

\[
p_t(x,y)=\sum_{k\in\mathbb Z^2}e^{-4\pi^2a|k|^2t}
 e^{2\pi i k\cdot(x-y)},\qquad
G(t)=\sum_{k\in\mathbb Z^2}e^{-4\pi^2a|k|^2t}.
\]

There is a unique a>0 with G(1)=2. Indeed the trace is continuous and strictly decreasing from infinity to one as a ranges from zero to infinity.

For x=(0,0) and x′=(1/2,0), Parseval's identity followed by Tonelli's theorem gives

\[
d_0(x,x')^2
=4\sum_{\substack{k_1\in\mathbb Z\text{ odd}\\k_2\in\mathbb Z}}
\frac{1}{1+8\pi^2a(k_1^2+k_2^2)}=\infty.\tag{3}
\]

To see divergence without an asymptotic approximation, take positive odd k₁=m and |k₂|≤m. These 2m+1 terms contribute at least
\(4(2m+1)/(1+16\pi^2am^2)\), a positive constant times 1/m. The harmonic sum over odd m diverges. Thus (1) is not a finite metric in this example. The torus itself already has a compact Feller realization, so (3) concerns the proposed formula only.

### Verification that this is in the finite-chain limit setting

For integers n≥3, take the n×n torus grid with nearest-neighbor jump rate n² in each of its four directions. It is irreducible, reversible, and has uniform stationary distribution. With centered frequency representatives k, its generator eigenvalues are

\[
\lambda_n(k)=4n^2\left(\sin^2\frac{\pi k_1}{n}
 +\sin^2\frac{\pi k_2}{n}\right).
\]

They satisfy
\(16|k|^2\le\lambda_n(k)\le4\pi^2|k|^2\).
Let a_n be the unique time factor making
\(\sum_k e^{-a_n\lambda_n(k)}=2\).
The four first nonzero modes imply
\(a_n\ge\log4/(4\pi^2)>0\).
The lower eigenvalue bound gives a uniform finite upper bound on a_n (one may take a_n≤1). The finite Fourier sums therefore converge, uniformly on compact positive-time intervals and uniformly in grid locations against their limiting torus positions, to the displayed heat kernel. Dominated convergence of the traces gives a_n→a.

More explicitly, the density with respect to the uniform grid measure is the finite Fourier sum, without a factor 1/n². Its terms are bounded by the summable Gaussian \(e^{-16ct|k|^2}\), where c=log4/(4π²). Every fixed frequency converges to its torus frequency. Coupling a stationary grid point as \(\lfloor nU\rfloor/n\), U uniform on the torus, proves convergence of every finitely sampled density array, including its diagonal entries. Also
\(G_n(t)\le\sum_{k\in\mathbb Z^2}e^{-16ct|k|^2}<\infty\)
uniformly in n for each t>0. Thus the example satisfies the required boundedness and normalization, rather than merely being a diffusion unrelated to the finite-chain setting.

## 3. A positive-time completion theorem

Let \((E,\pi)\) be a standard probability space and \((P_t)_{t\ge0}\) a symmetric strongly continuous Markov semigroup on L²(π), with P_t trace class for every t>0. Write
\(G(t)=\operatorname{Tr}P_t\), and suppose the semigroup has transition densities. On a suitable conull set, choose its coherent L² density rows
\(K_t(x)=p_t(x,\cdot)\), t>0.

For clarity, these row versions can be obtained from the spectral representation. If \(-L\) has eigenfunctions e_j and eigenvalues λ_j≥0, remove the null set on which
\(\sum_j e^{-2\lambda_j s}e_j(x)^2\)
is infinite for some positive rational s. Then
\(K_t(x)=\sum_j e^{-\lambda_jt}e_j(x)e_j\)
exists in L² for every t>0 and satisfies
\(K_{t+s}(x)=P_sK_t(x)\).
Positivity and integral one first hold at all rational times on a common conull set and then at every positive time by this semigroup identity. The canonical pair kernel is
\(p_t(x,y)=\langle K_{t/2}(x),K_{t/2}(y)\rangle\);
it agrees with the original densities almost everywhere, and with their diagonal values when the diagonal Chapman–Kolmogorov convention is imposed.

Set

\[
w(t)=\frac{e^{-t}}{1+G(2t)},\qquad
j(x)=(K_t(x))_{t>0}\in
\mathcal H=L^2((0,\infty)\times E,w(t)\,dt\,\pi(dy)).\tag{4}
\]

Fubini gives

\[
\int_E\|j(x)\|_{\mathcal H}^2\,\pi(dx)
=\int_0^\infty w(t)G(2t)\,dt\le1.
\]

Thus j is defined almost everywhere, after another conull restriction. This is a measurable map into a separable Hilbert space. Push π forward to ν=j_*π and let \(\bar E=\operatorname{supp}\nu\). Removing a final null set, j(E) lies in and is dense in \(\bar E\). The space \(\bar E\) is closed in a separable Hilbert space, hence complete and separable. Its metric is \(d(j(x),j(y))=\|j(x)-j(y)\|\); equal rows are identified.

**Positive-time theorem.** There are symmetric nonnegative jointly continuous densities \(\bar p_t(z,z')\), t>0, on \(\bar E\) with respect to ν, with integral one and the Chapman–Kolmogorov identity at every state. They preserve the original off-diagonal sampled density arrays. The diagonal entries are also preserved when the original densities use the canonical values \(p_t(x,x)=\|K_{t/2}(x)\|_2^2\), as imposed by diagonal Chapman–Kolmogorov in Towsner’s setting. For each fixed t>0, the kernel maps every bounded Borel function to a continuous function.

**Proof.** Contractivity of P_s and row coherence imply that
\(\|K_t(x)-K_t(y)\|_2\)
is nonincreasing in t. With \(W_t=\int_0^t w(s)\,ds>0\),

\[
\|K_t(x)-K_t(y)\|_2\le W_t^{-1/2}\|j(x)-j(y)\|_{\mathcal H}.\tag{5}
\]

Therefore each row map extends uniquely to a Lipschitz map
\(K_t:\bar E\to L^2(\pi)\).
The cone of nonnegative functions and the condition of integral one are closed in L² on a probability space, so every extended row is still a probability density. Row coherence extends by continuity. Define

\[
\bar p_t(z,z')=\langle K_{t/2}(z),K_{t/2}(z')\rangle.\tag{6}
\]

This is symmetric, nonnegative and jointly continuous. For any z, its pullback along j in the second variable equals K_t(z) almost everywhere, by row coherence and symmetry; first check this on the dense original image, then use L² continuity. Consequently it integrates to one, and for bounded Borel f,

\[
\bar P_tf(z)=\langle K_t(z),f\circ j\rangle,\qquad
|\bar P_tf(z)-\bar P_tf(z')|
\le W_t^{-1/2}\|f\|_{L^2(\nu)}d(z,z').\tag{7}
\]

For Chapman–Kolmogorov, its left side pulled back in the integration variable is
\(\langle K_s(z),K_t(z')\rangle\).
It equals (6) at time s+t on the dense original image and hence everywhere by continuity. Formula (6) also gives the canonical diagonal values. Thus stationary samples have the same off-diagonal density arrays; repeated sample indices also agree under the stated canonical-diagonal hypothesis. ∎

This proves a positive-time kernel statement. It does not prove (2), strong continuity on a space of continuous functions, local compactness, or a right-continuous path realization from every point.

One further conclusion holds in stationarity. With \((X_0,X_t)\) sampled from \(\nu(dz)\bar P_t(z,dz')\),

\[
\mathbb E\,d(X_0,X_t)^2
=2\int_0^\infty w(s)\bigl[G(2s)-G(2s+t)\bigr]ds
\longrightarrow0.\tag{8}
\]

The identity follows by expanding the squared Hilbert norm and using the trace of P_tP_{2s}; dominated convergence uses w(s)G(2s)≤e^(−s). This is an averaged assertion and gives no control at an exceptional added state.

## 4. This completion can add an instantaneous mixture state

Here is a symmetric trace-class example satisfying the hypotheses of Section3 in which the very weight (4) fails to give (2). This is a counterexample to an automatic completion-to-Feller inference, not to the existence of every other state topology.

### A reversible fast-leaf chain

On \(S=\{a,b,1,2,\ldots\}\), set

\[
\pi_S(n)=16^{-n},\qquad \pi_S(a)=\pi_S(b)=7/15.
\]

Their total is one. From leaf n jump to each hub a,b at rate \(2^{n-1}\); between a and b use rate one. Choose the reverse hub-to-leaf rates by detailed balance:

\[
q(a,n)=q(b,n)=\frac{15}{14}\,8^{-n}.
\]

Each leaf has total rate \(r_n=2^n\), and each hub has total rate
\(c=1+15/98=113/98\).
The chain is nonexplosive: between successive visits to leaves it must spend an exponential holding time of fixed positive mean at a hub. Reversibility is exact.

Its L² semigroup has finite trace at every positive time. To verify this, conjugate −Q by multiplication by \(\sqrt{\pi_S}\). The result is a diagonal operator D with the leaf diagonal entries 2^n and two hub entries c, plus a bounded finite-rank self-adjoint perturbation B. The two hub-to-leaf vectors have squared ℓ² norm
\(\sum_n (2^{-n}/(2\sqrt{7/15}))^2=5/28\),
and the hub-to-hub block is bounded. One can take \(\|B\|<2\). The minimum principle therefore bounds the heat trace by

\[
G_S(t)\le e^{2t}\left(2+\sum_{n\ge1}e^{-2^nt}\right)<\infty.
\]

The connected chain has a simple constant eigenfunction; compact resolvent and the preceding summability imply G_S(t)→1 as t→∞.

Let \(A_t=(K_t^S(a)+K_t^S(b))/2\). Conditioning on the first exit from leaf n gives

\[
K_t^S(n)=e^{-r_nt}\frac{1_{\{n\}}}{\pi_S(n)}
 +\int_0^t r_ne^{-r_ns}A_{t-s}\,ds.\tag{9}
\]

The hub rows have uniformly bounded L² norms for all t≥0, since their initial atomic densities belong to L² and the semigroup is contractive. Their L² continuity implies that the second term in (9) tends to A_t for each fixed positive t.

### A trace contribution that suppresses the short-time leaf spike

Take the disjoint union of this chain and Brownian motion on \(\mathbb T^8\), with stationary measure
\(\pi=\tfrac12\pi_S+\tfrac12\mathrm{Haar}\).
Let P_t^0 be the block-diagonal semigroup. Add independent rate-one resets to π:

\[
P_t=\Pi+e^{-t}(P_t^0-\Pi),\qquad \Pi f=\int f\,d\pi.\tag{10}
\]

This is a conservative symmetric strongly continuous Markov semigroup. It has strictly positive densities at all positive times, and

\[
G(t)=1+e^{-t}\bigl(G_S(t)+G_{\mathbb T^8}(t)-1\bigr)<\infty.
\]

The eight-dimensional heat trace is bounded below by a positive constant times t^(−4) for 0<t≤1: retain the Fourier modes with all coordinates bounded by a fixed multiple of t^(−1/2). Thus the weight in (4) satisfies \(w(t)\le Ct^4\) for all t>0, after enlarging C for t≥1.

The trace decreases continuously from infinity to one, so a fixed time rescaling makes G(1)=2 if desired. All ensuing limits are unchanged by that rescaling, with only constants in the estimates changing. This example is asserted as a reversible trace-class process; the proof does not require a separate finite-uniform-grid approximation of this mixed state space.

### The added midpoint and failure at time zero

Apply the Hilbert embedding (4) to (10). The reset terms cancel when comparing the leaf row to the mean of the hub rows. In the full L²(π) norm, this difference is the star-chain difference in (9), multiplied by a harmless factor \(\sqrt2e^{-t}\).

The squared weighted norm of the initial leaf spike is bounded by

\[
\frac{C}{\pi_S(n)}\int_0^\infty t^4e^{-2r_nt}\,dt
=\frac{24C}{32\pi_S(n)r_n^5}
=\frac{3C}{4r_n}\longrightarrow0.\tag{11}
\]

The remaining difference between the convolution term in (9) and A_t is uniformly bounded in L² and converges pointwise for every t>0. Dominated convergence against the integrable weight w proves

\[
j(n)\longrightarrow z:=\tfrac12(j(a)+j(b))
\quad\hbox{in }\mathcal H.\tag{12}
\]

Every j(n) lies in the support of the pushed-forward measure because n is an atom of positive mass. Hence z belongs to the completed state space \(\bar E\).

The two hub images are distinct. Indeed \(1_{\{a\}}-1_{\{b\}}\) is an eigenfunction of the star chain with eigenvalue \(-211/98\), and of (10) with eigenvalue \(-309/98\). It distinguishes their rows at every positive time. Therefore z has positive distance from each hub image.

The extended row at z, by (5) and (12), is the arithmetic mean of the two hub rows. Consequently

\[
\bar P_t(z,\cdot)=\tfrac12\bar P_t(j(a),\cdot)
 +\tfrac12\bar P_t(j(b),\cdot),\qquad t>0.\tag{13}
\]

From a hub the original process stays at that hub until its first jump or reset, with total rate c+1. Hence its law tends to the point mass at that hub as t↓0, even in the Hilbert metric. Choose a bounded continuous function f on \(\bar E\) that is zero at z and one at both hub images, for example a truncated multiple of the distance to z. Equation (13) gives

\[
\bar P_tf(z)\longrightarrow1\ne0=f(z).
\]

This violates (2). No right-continuous realization started at z can have these transition probabilities. In particular, positive-time Lipschitz kernels and the stationary continuity (8) cannot justify silently declaring the completion a Feller process.

## 5. Exact remaining gap

The original problem asks for some suitable topology and process realization. Section2 disproves only the displayed distance. Section3 constructs continuous positive-time density kernels on a complete separable quotient/completion under an explicit strongly continuous L² semigroup hypothesis. Section4 shows that this particular repair can introduce a bad entrance state, even when that hypothesis holds. It does not rule out removing suitable null states, selecting a different complete metric, or finding another natural representation with the required process behavior.

A full answer must specify the zero-time pinning, how null sets and indistinguishable states are handled, and why the chosen realization has the required time-zero and path properties at every retained state. Those steps have not been established here. The record remains **unsolved, 3/5 attempts**. All computational controls are bounded exact checks of formulas and finite models, not a replacement for these proofs or a claim to classify all Markov limits.
