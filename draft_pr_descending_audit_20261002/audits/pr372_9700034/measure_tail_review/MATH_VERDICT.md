# Sealed mathematical verdict before programs and receipts

## Verdict

PASS SCOPED: the measure/probability statements in TURN_1 through TURN_5 are correct under their stated hypotheses and credited primary inputs. No mandatory mathematical correction was found in those statements. This is neither an overall merge decision nor a historical novelty certificate. The general target remains unresolved: no proof from ordinary SIRSN axioms of E sup_i len R(0,U_i)<infinity, and no genuine SIRSN counterexample.

This verdict was sealed after reading the complete five TURN proofs and the candidate FINAL_RESULT/README/source-scope/source-map, and after fresh primary-source reading. No candidate checker, stored count, receipt, manifest verdict, prior review, parent result or sibling result was read. A second combined read suffered truncation in supplementary source-scope output; the complete source-scope and source-map were reread separately before this seal. The five TURN proof bodies were fully visible.

## Reconstructed mechanisms and adversarial findings

### TURN 1: common Poisson envelope and moments

The crucial event is {M>2^m r_0, Tau<=T} subset intersection_{j<=m}{V(2^j r_0)>=2^j r_0/T}. An initial arclength-r piece of a finite-length speed-limited path stays within radius r regardless of a later return or excursion. It spends at least r/V(r) travel time. This implication is simultaneous for every route and has no endpoint cardinality factor.

For each deterministic record-index composition, previous upper speed records exclude all sufficiently fast old lines; the new line-space layer is independent of revealed older layers. The product upper bound is unconditional. Summing over the binomial(m,k) record choices gives 2^{-(gamma-1)(m+1)} a(1+a)^m. This avoids the source's unjustified-looking conditional-display notation: a bound on P(E_m) is used for an intersection event, never as P(E_m|Tau<=T). Tau may be arbitrarily dependent on speed records.

Choosing a=2^{gamma-1-kappa}-1>0 and r_0 proportional to T^{(gamma-1)/(gamma-d)} is legitimate only gamma>d and 0<kappa<gamma-1. With T_n proportional to (n+1)^{1/(gamma-1)}, the threshold grows as (n+1)^{1/(gamma-d)} 2^{(n+1)/kappa} and probability falls as 2^{-n}. Layer integration of qth moments converges precisely by q<kappa<gamma-1. The boundary q=gamma-1 is not proved. In d=2 gamma>2 permits q=1; in other dimensions gamma>d>=2 likewise implies gamma-1>1.

A concrete measurable line-process envelope can be specified if desired: let Y be the first b_n for which Tau<=T_n and the corresponding deterministic E_{m(n)} fails, with infinity if none. Each event is measurable, and P(Y>b_n)<=2^{-n}; hence Y finite almost surely and has all q<gamma-1 moments. Every route considered has length <=Y. This makes the stated common-envelope wording precise without an uncountable measurable route supremum. Endpoint independence pertains to the original network law, while the bound works for any countable endpoints whose measurable routes exist in that realization. The binary bound is a direct credited primary consequence.

### TURN 2: countable extension and critical field

The cardinality |G_n|<=(9)(4^n), parent length sqrt(2)2^{-n}, and finite maximum <=sum of powers give ||A_n||_p<=9^{1/p}2^{alpha/2}C^{1/p}2^{-n(alpha-2/p)}. Nonnegative partial sums and Minkowski produce an Lp envelope when alpha p>2. The random location kernel E|F(U)-F(g_n(U))|^p bound is obtained by integration of the two-length joint FDD, not by independence of lengths. Markov/Borel-Cantelli convergence for each sampled endpoint, then a countable intersection, transfers the grid envelope. No measurable continuum field is assumed.

Triangle inequality (TM) is explicitly additional and yields |F(u)-F(v)|<=len R(u,v), so p>2 route moments suffice. Feasible nontrivial SIRSN length fields cannot satisfy the increment bound with alpha>1: subdivision and Minkowski imply ||F(u)-F(v)||_p<=C^{1/p}|u-v|^alpha N^{1-alpha}->0. Thus the nonempty SIRSN range is p>2 and 2/p<alpha<=1. This restriction does not invalidate the theorem, but helps interpret its strength.

The translated log-log field is jointly measurable, nonnegative, anchored at zero, with f>=|u|. Its tail pi exp(-2e^t) gives every finite marginal moment. The radial gradient energy is exactly 2pi after s=log(1/r), and bounded truncations with repaired center values are Lipschitz. Translation averaging controls the L2 increment by 2pi|h|^2; the two reverse-triangle inequalities give the displayed 2+4pi constant. Every level has positive-area endpoint sets near the translated singularity, and independent infinitely many samples hit each. The example is valid at the critical alpha p=2. It is not a compatible route network and is not used as a SIRSN counterexample.

### TURN 3: exact support tail, visibility and two-route obstruction

For exchangeable indicator samples, direct moment expansion gives E(Q_n-Q_m)^2=(a-b)(1/n-1/m). The L2 limit has squared error (a-b)/n. Squares n=k^2 provide summable error probabilities; monotone counts squeeze to all n. Finite permutation invariance implies E[I_1 1_B]=E[Q1_B]; on {Q=0} all indicators vanish. This is the missing step that rules out a finite or zero-density exceptional set of exceedances in an exchangeable infinite sequence.

The rational right-continuous construction gives a jointly measurable tail Q(t). For every fixed real t it agrees with the empirical limit because of dominance and equal mean. Simultaneous event equality {M>t}={Q(t)>0} follows from rational strict thresholds. Tonelli gives exact E M=integral P(Q>0). It is not a proof of a jointly measurable route version.

All three upper criteria are correct. Deterministic visible mass gives P(M>t)<=a/h; polynomial h integrates to the stated (1+L)^{alpha+1} formula. Random visibility must use invariant V, as stated: E[VQ(t)]=E[V1_{L1>t}] by truncation; Holder is applied jointly, never assuming V independent of lengths. Negative-frequency Holder yields P(Q>0)<=a^{q/(q+1)}R_q^{1/(q+1)} and the sufficient power condition sq>beta+q+1. The pair lower bound follows from Cauchy-Schwarz with b=E Q^2>=a^2; the 0/0 convention is harmless. Passing from finite Paley-Zygmund bounds to the infinite supremum is monotone.

The hard polynomial positive-mass conditions are quite restrictive: if the maximum S is finite, Q(t)>=c(1+t)^(-alpha) on t<S forces a conditional atom of mass at least c(1+S)^(-alpha) at S by t increasing to S. The random version has the same property with c=1/V. Generic continuous peaks without a maximum plateau fail these hypotheses. That is a scope caution, not a counterexample to the sufficient theorem. The inverse-frequency criterion is not subject to this particular hard plateau requirement.

The scalar J mixture is a decisive control: sum 2^{-j}2^{-j^2}2^{js}<infinity for every s, but conditional on each J the rare upper value is eventually observed and M=2^J. It is finite almost surely and E M=infinity. A frequency condition that only averages mass cannot replace support control. No planar realization is asserted.

### TURN 4: finite exterior arcs and two exact unresolved variables

The planted-origin extension is expressly provided by Aldous (6.4), together with the intrinsic major-road extension of Proposition 6.3. Space-time PPP arrivals in the disk give iid uniform endpoints and can be completed outside the disk independently. Countably many relevant radii allow a common probability-one event; no uncountable sample assertion is required.

The radius-3 circle has finite expected major-road intersections <=(2/pi)p*(6pi)=12p. Every open exterior component of a compatible injective route is a compact subarc with distinct boundary endpoints. The finite crossing set leaves at most binomial(N,2) distinct subarcs, each witnessed by an actual finite-length route. This gives a.s. finite exterior union and confinement radius, not any first moment. Random witness selection may be badly biased; no expectation bound is inferred.

At the fixed root with annular destinations, dyadic root rings have route-union inclusion in E_{eta2^{-j-1}}, expected ring lengths (3pi/2)p eta 2^{-j}, hence 3pi p eta in total. Edge intensity gives zero expected length on deterministic ring boundaries. The middle is bounded by E_eta inside radius3. The route decomposition bounds M_A by those two integrable pieces plus J_eta and O; the converse J_eta,O<=M_A makes the equivalence exact. No limit eta->0 is needed or asserted.

Each disk shell's infinite subsequence is iid uniform on that shell and independent of the network, by conditional iid thinning. Its maximal law is 2^{-k}M_A by coherent scale-invariant FDDs and countable supremum limits. Summing expectations requires no independence between shells. E M_A<=E M_disc<=2 E M_A proves equivalence of integrability. The exact unresolved quantities remain the first moments of terminal neighborhood maxima and finite exterior maximal lengths.

### TURN 5: mixtures and fixed-base affine family

Countable mixtures preserve consistency, measurability, compatibility and similarity invariance. Nonnegative finite-lambda edge intensities average, and monotone convergence commutes the lambda limit with the mixture. Independent destinations can be sampled after the mixing choice. No spatial ergodicity hypothesis is present.

If the universal finite-H assertion holds but no linear bound H<=C(Delta+p) exists, pick actual laws with ratios>=4^j and weights 2^{-j}/[Z(Delta_j+p_j)]. Since b>=1, 0<Z<=1, the mixed b has finite expectation 1/Z while mixed H diverges. This is a valid contradiction only with actual genuine SIRSN laws. An assignment of formal triples or scalar fields does not meet that premise. The criterion is a legitimate logical reduction, not a constructed counterexample.

For fixed bounded-stretch base law, affine distortion and outer independent rotation preserve the FDD network laws. The major-road inclusion under the linear map gives p_lambda<=||A||^2 p0/det A=lambda p0, enough for genuine-model status. Transverse variation c0>0 follows from the source no-initial-straight-segment result: similarity invariance and independent PPP pair integration transfer exclusion of straight paths to a fixed pair. Finite c0 follows from bounded stretch. The projected variation lower bound and the angular event |u_y|>=1/2 with probability2/3 give Delta_lambda>=lambda c0/6 for large lambda. The combined constant K=8C0Delta0/c0 uniformly bounds H_lambda/Delta_lambda. Mixing cannot defeat it. This constant is base-dependent, so it gives no universal estimate across all SIRSNs.

## Strongest checked conclusion and exact gap

The packet proves model-specific maximum moments; explicit additional joint-law sufficient criteria; a.s. confinement and integrable root/middle pieces from ordinary axioms; and a legitimate mixture equivalence plus a failed fixed-base affine route. It proves neither the required general terminal/exterior first moments nor actual unbounded-ratio network families. It supplies no evidence for the boundary q=gamma-1 moment, no automatic second-moment SIRSN theorem, and no global priority/novelty or current unresolved-status certification.

## Completion checkpoint

Mathematical audit completion estimate 70%; the source/candidate probability mechanisms are reconstructed. General research discovery completion cannot be estimated defensibly beyond partial progress; target remains open in this packet. Program/source agreement and controlled replays remain required before the complete REPORT.
