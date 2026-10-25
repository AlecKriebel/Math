# Independent analytic review — Zenodo 23524971

## Disposition and exact result

**PASS for the stated mathematical theorem, at its exact hypotheses.** I found no substantive defect in the published all-load positive-recurrence proof. This is an AI mathematical review, not independent human peer review, a proof-assistant certificate, a publication decision, or a worldwide novelty certificate.

The strongest supported result is: for each **fixed real** arrival rate \(\lambda>0\), the six-rate continuous-time Markov chain in equation (1), on \(\mathbb N_0^4\), is nonexplosive, irreducible and positive recurrent, and consequently has a unique stationary probability distribution. Every finite initial state is included. The proof constructs one globally defined, coercive function with generator at most \(-1\) outside a finite, load-dependent set, and supplies a legitimate continuous-time recurrence argument.

There is **no identified remaining mathematical gap in this result**. Its scope does not include an aggregate seed upload cap, visible empty waiting rooms, a different sampling protocol, uniform control as the arrival rate grows, finite stationary population moments, quantitative delay guarantees, or geometric ergodicity. The preserved primary-source access limits below restrict historical attribution/priority verification, not the self-contained six-rate proof.

## Reviewed object and independence

- Record: 23524971; deposited version 1.0; manuscript dated 20 October 2026 and marked “Unrefereed preprint draft.”
- Published six-page `dfc_stability.pdf`: 75,006 bytes; SHA-256 `bee5abffcfdb1ce8bc50f706480c81c4a80e8d609bec2a9d99c6aa4e9b805036`.
- Published ZIP: 251,455 bytes; SHA-256 `38664f12e8d2e74fa46b3f11363a071ec100aad62ece713b578293a6593d9a0e`.
- Read the entire published PDF through its text extraction, the complete `main.tex`, and the necessary original mathematical proof `original/TURN_4.md`. The PDF inside the archive is byte-identical to the separately deposited PDF. Exact source/receipt bindings are recorded in `evidence.json`.
- Before reading any packaged helper, reconstructed the proof and wrote/executed `fresh_controls.py`. This applies the actual generator directly and solves the corrector backwards from its reflecting terminal equation, independently of the manuscript's prefix-sum implementation.
- No current sibling report or dedicated historical assessment body was opened. In particular, `original/RESULT_ACCEPTED.md`, `ROOT_ANALYTIC_ASSESSMENT.md`, historical final-review files and current scope findings were not read. Necessary `TURN_4.md` includes its author's old candidate/completion statements, and `README.md` includes summaries of old review/control statuses; these were incidentally seen and were not evidence for the verdict. Executed selected mathematical controls hash some historical files as opaque bytes; their assessment prose was not interpreted.
- All 92 extracted source-file hashes were preserved. No source, proof, old review, publication draft, website, spreadsheet, Git state or external service was edited.

## Exact model and hypotheses

Write the state as \((a,b,x,y)\), where \(a,b\) are empty peers with assigned first-chunk choices and \(x,y\) have only the corresponding chunk. A new peer independently chooses one of the two first chunks uniformly. The permanent seed carries both chunks. Completed peers leave immediately. Empty peers are excluded from the sampling denominator \(D=x+y+1\).

The rates are arrivals \(\lambda/2\) to each waiting room; first downloads \(a(x+1)/D\) and \(b(y+1)/D\); and departures \(x(y+1)/D\) and \(y(x+1)/D\). Decrements with zero coordinates have zero rate. These exact transition rates, rather than an informal file-sharing description, determine the theorem. In particular, seed demand may grow with an invisible waiting-room population. No rate parameter is required to be rational; rational arithmetic below is only a finite test mechanism.

The positive-load assumption is material: at zero arrival rate, the origin is absorbing and the full state space is not irreducible. Removing the permanent seed or changing the denominator would also change the reachability or drift arguments. Neither modification is covered.

## Independent reconstruction of the proof

### 1. Clock, reachability and elementary workload

Let \(W=2a+2b+x+y\). Every arrival raises \(W\) by two and every other transition reduces it by one. Construct arrivals with an independent Poisson clock. If \(P_\lambda(t)\) arrivals have occurred, the number of internal events is at most \(W(0)+2P_\lambda(t)\), so the total number of transitions is at most \(W(0)+3P_\lambda(t)\). This precludes an explosion and does not presume stationarity. Each state's total rate is finite; alternatively it is bounded by \(\lambda+a+b+x+y\).

The permanent seed makes every required first download and final download strictly possible. Any state can reach zero through finitely many such events while avoiding arrivals. From zero, first generate the required \(a+x\) and \(b+y\) arrivals, then choose exactly \(x\) and \(y\) first downloads while avoiding departures. Each finite prescribed sequence has positive probability. Thus the whole countable state space is irreducible for \(\lambda>0\).

With \(u=[a(x+1)+b(y+1)]/D\), \(d=[2xy+x+y]/D\), and \(Z=a+x-b-y\), direct generator calculation gives
\[
\mathcal LW=2\lambda-u-d,\qquad \mathcal LZ=(y-x)/D.
\]
First downloads preserve \(Z\), and all jumps changing it have size one and combined rate \(\lambda+d\). Also \(u+d\ge n/(n+1)\), where \(n=a+b+x+y\): its numerator is \(n+ax+by+2xy\), while \(D\le n+1\). This independently confirms the manuscript's elementary small-load observation, without treating it as the all-load result.

### 2. Rounded imbalance and a finite, real-parameter corrector

The derivative of the rounded absolute value \(h_m\) is the clipping of \(z/m\) to \([-1,1]\). It is globally \(1/m\)-Lipschitz, so the Taylor upper bound remains valid across both rounding endpoints. For the manuscript's positive constants
\[
\beta=17\lambda/8,\quad q=7/8,\quad c=2(\beta+4),\quad m=4c,
\]
the identity \(c/(2m)=1/8\) gives equation (4):
\[
\mathcal L(W+ch_m(Z))\le\beta-u-qd+c h'_m(Z)(y-x)/D.
\]
The final term is bounded in absolute value by \(c\). If \(Z\ge m\) and \(x\ge3(y+1)\), it is at most \(-c/2\).

Set \(\theta=\beta+c+4\), \(\gamma=(\theta+1)/(\theta+2)\), \(\eta=(1+\gamma)/2\). The reflected finite birth–death chain on \(0,\ldots,R\) has weights \(\gamma^k\). Its mean grows strictly to \(\theta+1\), so a finite integer \(R\) can satisfy both margins in (5) for **every real** positive load. A useful independent formula is
\[
\mu_R=\frac\gamma{1-\gamma}-\frac{(R+1)\gamma^{R+1}}{1-\gamma^{R+1}},
\]
and hence \(\mu_R>\theta\) is equivalent to \((R+2)\gamma^{R+1}<1\). This also confirms existence without an effectivity or rationality assumption.

The prefix conditional mean is strictly below the full mean, which makes every displayed \(t_k\) negative and \(g\) nonnegative and decreasing. Telescoping verifies \(Q_Rg=k-\mu\). The terminal equation is essential: \(Rg(R-1)=R-\mu\). Independently, solving this terminal equation and then the interior equations backwards determines the same increments; the fresh controls checked also the remaining equation at zero.

For actual \(y\), births are \((b/D)(y+1)\), deaths are \(y(x+1)/D\le y\). If \(b/D\ge\gamma\), increasing the coefficient of a nonpositive birth increment and decreasing the coefficient of a nonnegative death increment gives \(\mathcal Lg(y)\le y-\mu\). At \(y=R\) the birth increment is zero. At \(y=R+1\), the downward successor has \(g(R)=0\), so all increments vanish. Thus the endpoint extension used later is valid. The same reasoning applies to \(x\).

### 3. Interfaces are controlled pointwise, even for huge waiting rooms

For \(J_X=f(b/D)g(y)\), the exact product rule uses the **post-jump** value of \(g\) in the cutoff error. A first download increases \(D\), does not increase either waiting-room numerator, and decreases any affected corrector value. Since \(f\) is nondecreasing and \(g\ge0\), both first-download interface errors are nonpositive. This handles rates proportional to arbitrarily large \(a,b\); no averaging argument is being substituted for an unbounded error.

An arrival changes one cutoff by at most \(\ell/D\). A departure has \(D\ge2\). For its unchanged numerator \(w\), either the old cutoff is already saturated and the change is zero, or \(w<\eta D\), giving
\[
0\le f(w/(D-1))-f(w/D)\le\ell\eta/(D-1)\le2\ell/D.
\]
This remains correct for \(D=2\); there are no departures when \(D=1\). Summing two products gives the remainder \(\ell G(\lambda+4d)/D\) in (8). The coarser bound (9) follows because first downloads decrease each entire product, an arrival raises their sum by at most \(G\), and a departure raises it by at most \(2G\). Both estimates are valid globally.

### 4. The exterior-region cover is exhaustive

All constants and a suitable integer \(N\) are finite at fixed load; \(1-\eta>0\). For \(V=W+ch_m(Z)+J_X+J_Y\):

1. If \(\min(x,y)\ge R+1\), every present and one-step successor corrector value is zero. Also \(d\ge\min(x,y)\). The selected \(R\) therefore gives \(\mathcal LV<-2\). Using \(R+1\), rather than \(R\), is necessary for the successor claim.
2. Suppose \(y\le R\), \(x\ge N\). The other corrector and its successors vanish. Direct bounds give \(d\le2R+1\), \((x-y)/D\ge1/2\), and \(qd\ge y\). The interface remainder is at most one. If \(b/D\ge\eta\), the full corrector gives the margin \(\beta+c-\mu+1<-3\). If \(b/D<\eta\), the choice of \(N\) forces \(Z\ge m\), while \(f(b/D)(y-\mu)\le y\); this gives \(\mathcal LV\le\beta-c/2+1-u=-3-u\). The whole cutoff ramp is included. Interchanging types covers the opposite corner.
3. Outside the preceding regions, \(\min(x,y)\le R\) and \(\max(x,y)<N\), hence \(x+y\le N+R\). Bound (9) controls \(J\), while \(u\ge(a+b)/(N+R+1)\). Therefore \(\mathcal LV\le-1\) when \(a+b>B\), for exactly the stated finite threshold \(B\).

Consequently (16) holds outside the finite set \(F\). This is a single function throughout; no state-dependent choice of unrelated Lyapunov functions or unaccounted switching interface appears.

### 5. Positive recurrence follows for the continuous-time chain

The bound \(|Z|\le W\), the rounded-absolute estimate and \(0\le J\le2G\) give
\[
W\le V\le(1+c)W+cm/2+2G.
\]
Its individual jumps are bounded, for example by \(2+c+2G\). On a finite population localization, all generator and stopping terms are finite. Dynkin's identity stopped at the first hit of \(F\), time \(t\), and a finite population exit gives expected stopped duration at most \(V(s)\). Nonexplosion removes the population cutoff on every finite time interval, and nonnegativity/Fatou followed by monotone convergence gives \(E_s\tau_F\le V(s)\). No integrability of a hypothetical stationary law was used.

The finite-set-to-state step is also sound. For each state in \(F\), a fixed finite positive-rate path to zero can finish within a common positive time \(T\), with a common positive probability. The workload bound \(W(T)\le W(0)+2P_\lambda(T)\) and linear growth of \(V\) uniformly bound the expected cost of a trial followed by return to \(F\). At every new trial the conditional success probability is bounded below. The strong Markov property and a geometric bound on the number of trials give finite expected hitting time of zero; independence of trial duration and success is not needed. Holding at zero has mean \(1/\lambda\), and its two exit neighbors have finite expected return time. The resulting finite-mean regeneration cycle supplies a stationary probability. Irreducibility gives uniqueness and positive recurrence.

Thus the proof uses a countable-state argument with the clock accounted for, not an unjustified discrete jump-chain recurrence transfer or an assumed invariant measure.

## Fresh controls and unmodified replay

`fresh_controls.py` passed at **12,693 distinct states across three separate load instances**, \(\lambda=1/8,1,3\), with \(R=58,89,167\). State counts per instance were 4,675, 3,975 and 4,043. The backwards Poisson solve checked all 317 corresponding reflecting-chain states. Generator checks included 1,062 states outside the stated finite set, the two scarcity corners, both-correctors-zero states, threshold neighbors, zero populations, rounding contacts and waiting-room coordinates as large as one billion. All arithmetic in assertions was exact rational arithmetic.

The generator and interface comparisons were computed directly, rather than asserting only formulas used to construct the parameters. Controls confirm the intended sharp distinctions: with \(\lambda=3\), removing \(J\) gives positive drift \(36000051/8000008\) at \((0,10^6,10^6,0)\); reversing the cutoff creates a strictly positive first-download interface term. Independent enumeration gives Common Chunk's one-peer departure probability \(7/8\), versus this model's \(1/2\). These are controls of incorrect alternatives, not counterexamples to the published theorem.

After those fresh checks, the following published programs were inspected and run unmodified in an isolated temporary copy:

- `original/checks/turn4_checks.py`: 71,165 assertions; exact output matched.
- `reviews/foster_recheck_02/exact_falsification.py`: 315,600 assertions, including 20 mutation controls; exact output matched.
- `reviews/priority_recheck_02/identity_controls.py`: all 4,096 grid states and protocol comparisons matched, excluding only its volatile UTC field.
- `reviews/priority_recheck_02/theorem_transfer_control.py`: its floating-point diagnostic matched, excluding only UTC; this diagnostic is not proof of its limiting statement.
- `identity_controls.py --false-identity`: failed with the required intentional rejection marker.

The top-level manifest's 91 payload entries were checked, and all 92 original extracted file hashes were equal before and after. The complete-package launcher was **not** run, and no complete historical-reproduction claim is made: its obsolete rounds and verdict-dependent historical wrappers were unnecessary here. `replay-results.json` gives exact commands/scripts, return codes, hashes and output comparisons. Fresh and replayed assertion counts are not combined as independent evidence. No simulation was used to infer recurrence.

## Primary interfaces, attribution and limits

Raw primary bytes and their acquisition receipts were read from the scope agent's primary-source cache, without opening its findings. `primary-reading-ledger.json` binds the source hashes and exact reading coverage.

- [Norros–Reittu–Eirola, arXiv:0910.5577v1](https://arxiv.org/abs/0910.5577v1): checked the continuous-time stability definition and Section 3.2/Figure 2. It gives these six rates and the invisible waiting-room convention. Its Conjecture 3.4 has the opposite, high-load-instability direction. It cannot be cited as the same stability conjecture.
- [Oberwolfach Report 48/2010](https://ems.press/content/serial-article-files/46306?nt=1): read Norros's complete contribution on printed pages 2782–2783. It explicitly formulates the stochastic-stability conjecture despite the unstable differential-equation behavior. This fresh public primary source supports the historical target.
- [2011 work, DOI 10.1007/s11134-011-9209-2](https://doi.org/10.1007/s11134-011-9209-2): checked Section 3.2, Figure 2 and Conjecture 3.6 in the **retained January 5, 2011 author proof**. Its HAL cover submission date is a different date. The final publisher body was not available in this review. The retained PDF is not represented as a newly fetched or publisher-final copy.
- [Meyn–Tweedie III](https://faculty.eng.ufl.edu/meyn/wp-content/uploads/sites/671/archive/spm_files/Papers_pdf/meytweIII.pdf): checked Section 4.1, conditions CD2 and Theorems 4.1–4.3. The general theorem requires nonexplosion and a closed petite set, with the test function bounded there. In this countable discrete setting a finite set admits a common-time atom minorization by the finite paths above. The manuscript additionally proves the needed recurrence step directly. Using drift against the constant function one does not establish a stationary population moment.
- Oguz–Anantharam–Norros, Allerton 2012: read the full retained five-page body, including operative Foster functions and conclusion. Its sampling uses the whole population, three samples and a protected departure rule; its state and kernel differ. The one-peer witness independently verifies the manuscript's distinction. The final rare-chunk conjecture concerns another algorithm. This copy is retained, not freshly authenticated. The newly fetched [Berkeley technical report](https://www2.eecs.berkeley.edu/Pubs/TechRpts/2012/EECS-2012-6.html) was inspected for the related model/algorithm context only, not treated as the final conference or later journal edition.

No classical method is credited to this paper: the model and historical conjecture, Foster recurrence principle, finite birth–death Poisson equation and rounded Lipschitz estimate are prior tools. The checked contribution is their particular pointwise combination providing an all-load certificate for this chain. The final 2011 publisher edition, final 2015 journal extension and all later literature were not comprehensively inspected. No claim that the conjecture was still open in 2026, or that no earlier exact theorem exists anywhere, is justified by this review.

## Remaining gap and publication boundary

**Mathematical gap:** none identified for equation (1) and Theorem 1. **Review limits:** finite controls cannot establish universal quantifiers; the all-real/all-state conclusion rests on the analytic argument reconstructed above. This is not formal verification or human peer review. Historical source-version/access limits remain as stated and do not justify priority rhetoric.

A public description can accurately say that the paper establishes positive recurrence at each fixed positive load for this exact two-chunk chain and addresses the stated 2010/retained-2011 conjecture. It should keep the permanent seed, invisible waiting rooms and model-specific rate scope visible, and should not present this as a blanket guarantee for practical file sharing or a bounded-upload protocol. No new conjecture or follow-up proposal was generated by this review.
