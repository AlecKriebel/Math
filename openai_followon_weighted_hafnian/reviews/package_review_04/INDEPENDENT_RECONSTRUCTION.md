# Independent reconstruction before prior audit conclusions

## Original target and success criteria
Every explicitly binary-encoded even-order symmetric nonnegative rational off-diagonal matrix must admit a uniform relative-error FPRAS, exact zero detection, and an unconditional TV sampler with every-execution polynomial bit time. Diagonal irrelevant; m=0 has hafnian 1; no density/connectivity/minimum-weight promise. The approximation premise is pinned OpenAI general-simple-graph FPRAS, not a finite-test assertion or assumed proof certificate.

## Own gadget reconstruction
After each binary digit, every source-to-current-sink path has precisely two extensions, plus one new direct path for a 1 digit. Thus w -> 2w+b. All arcs go forward in creation order, with a before z. Split internal vertices have an identity matching or precisely one incoming and one outgoing selected arc. Full matching must contain the unique selected source-to-sink path; any other selected component would be a cycle, excluded by acyclicity. After deleting both terminals every nonidentity component would be a cycle. One-terminal deletion is odd order. Therefore signature is (W,1,0,0), including W=1. Vertices are 4ell-2; internal count 4ell-4; edges at most 6ell-5. No hidden cycle or parallel edge found.

Each internal vertex of a glued gadget must be covered inside that gadget. Its covered endpoint count has even parity, hence 0 or 2; all original vertices used once gives an original matching. Independent full/terminal-deleted restrictions biject with the global fiber. Shared endpoints do not create a partial-use exception. Original pairs unique and internals fresh imply simplicity, even for direct terminal edges and mixed orientations. Fiber is product We.

D=product positive-support denominators has O(L) bits; We=pe D/qe has O(L) bits; sum bitlengths O(L^2); original order/edge count O(L) under explicit matrix encoding. D^m has O(mL+1) bits. Graph adjacency labels add only O(log L), so every required construction/scaling operation is polynomial in full bit input. This covers disconnected support, below-one fractions, redundant input fractions and extremely small positive Z >= D^-m.

## Own FPRAS wrapper reconstruction
Use exact general-graph feasibility on support, return 0 only if infeasible. Empty input returns 1. On feasible input C>=1, replacing an upstream failed zero by 1 changes no successful execution, because epsilon<1. Divide by exact positive D^m. If upstream output is a nonnegative rational with uniform every-tape polynomial bit time as stated, output positivity, failure bound, and bit time transfer. The dependency itself requires independent primary-source scrutiny.

## Own sampling reconstruction
Each step retains exact witness, discards infeasible children, and uses their true counts for ideal branch probabilities. Ideal recursion telescopes to 1/Z. Every output remains feasible even if arbitrary failed estimates vanish or are enormous; all-zero estimates return stored witness. At each fixed past adaptive history fresh oracle tapes make bad-current-call probability at most j gamma. On all-good calls normalized law differs by at most alpha/(1-alpha). Common-floor CDF changes TV by <(j-1)/2^b. Integrate good/bad laws without conditioning final output on global success; couple until first disagreement and sum over at most k stages, at most k^2 candidate outcomes. With alpha=eta/(4k), gamma=eta/(4k^2), 2^-b <= eta/(4k^2), bound is <5eta/6. Fixed draws have no rejection loop. All rational output lengths are bounded by oracle every-tape bit time; rational sums/CDF floors remain polynomial. Uniform expanded law projects exactly to weighted law by proven fibers; TV contracts under projection.

## Initial finding and scope
No substantive reduction/sampler defect found on reconstruction. Priority, upstream proof/formal scope, exact reproduction and PDF QA remain independent tasks. This is my own argument record, not reliance on earlier favorable audits. Files read: original USER_REQUEST.txt, AGENTS.md, complete main.tex, detailed gadget proof, sampling proof (full read completed in subsequent receipt), gadget and sampling implementation. Finite enumeration is corroboration only.

Recorded 2026-10-07T06:08:13.217179+00:00
