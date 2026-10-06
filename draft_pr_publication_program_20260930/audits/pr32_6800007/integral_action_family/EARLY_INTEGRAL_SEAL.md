# Early independent integral-action seal for PR32

Sealed UTC: 2026-10-02T01:15:57.900314+00:00; audit completion 20%. Only literal author-hosted primary TeX and CANDIDATE.md were read. No PR32 old review, checker/results, metadata/readiness/sourceaudit/history, or sibling-family conclusions read. PR30 family is a different closed effort and remains immutable.

Primary TeX SHA256: 33d853a6de512584aeedfaf5b491bcc7f0cf02d2964e8b1f1be67a5b3b97c48e; CANDIDATE SHA256: 501c9a536246ad06b29e16720c613bcb292c863857849f837bb0250c45a58050.

## Source interpretation

In the Manifolds modelled on flag manifolds section, the second question is the seventh question globally and asks the homotopy classification of totally real immersions of real 3-manifolds into SL(3,C)/upper Borel, then expressly states that Gromov's h-principle applies. The candidate adopts homotopies through totally real immersions on a fixed smooth second-countable boundaryless M, ordered holomorphic flag lines, no orientability/compactness/properness assumption. This is not a classification of embeddings, unparametrized images or nearly-Kahler flag data. This family audits the formal integral classification conditional on the claimed parametric h-principle; another independent family must validate that analytic input and source convention.

## Exact candidate formulas as hypotheses

A=H1(M;Z), B=H2(M;Z), C=H3(M;Z), delta=beta(w1(TM)). Index pairs (x,y) satisfy -4x-2y=delta. D(p,q)=(-4p-2q,(2x+y)cup p+(x+2y)cup q). Claimed fiber is a torsor for C directsum cokerD. Claimed existence iff delta in2B iff w1^2=0.

## Independent derivation and exact potential falsifiers

1. Formal data need BOTH a determinant-preserving SU3 trivialization of ordered ambient line sum E0 and an isomorphism Erho to the generally nontrivial fixed E=TMcomplex. Model this as the homotopy fiber of Map(M,BT2)->Map(M,BSU3)xMap(M,BU3) over (*,tau). Substituting a free U3 trivialization in the first factor should produce an erroneous H1 coordinate.
2. The rank3/stable inclusion is highly connected enough for loops on the relative4-dimensional pair (Mxs1,Mxpoint) and homotopies of dimension5. A Postnikov map (c1,c2):BU->KZ2xKZ4 is an equivalence through the relevant degrees because pi2,pi4 are Z and odd low groups zero, with integral c2 generator onS4. This must be checked integrally and relative, including infinite3CW; no finite-domination assumption or rational Chern character allowed.
3. Relative K-theory of that split product pair agrees with K^-1(M). Projection to M splits restriction, so the relative class is determined by the ordinary virtual difference [V]-[pr*E]; a forgotten fixed identification must not create an extra kernel. Stable translation from the tau component makes the gauge/mapping loop group abelian. Chern coordinates on the virtual difference give A directsum C; multiplication's c2 cross term vanishes because both relative c1 classes include t and t²=0.
4. For line loop classes xi+hi*t, sumxi=sumhi=0. The SU coordinate -c2/t is a=sumxi cuphi. Tangent root loop first coordinate is k=2(h3-h1). Ordinary c2(V)/t has coefficient delta*k - sumroots r*kroot. Virtual c2 cancels exactly delta*k; negative slant gives b=sumroots r*kroot=3a. Identity is integral even for torsion; coefficients2,3,-4 must not be divided.
5. A nontrivial ordinary-vs-virtual mutant should be detected on actual RP2xs1: E has delta generating H2=Z2, and a determinant loop t makes delta*t generate H3=Z2. This manifold has no admissible TR index, but is a genuine target-component test rather than an abstract torsion table. For loops arising from the torus representation k is even, so delta*k vanishes since2delta=0; testing only representation loops can miss the virtual-coordinate error.
6. pi0 of the full homotopy fiber over one connected source component is the full pi1Y orbit quotient, stabilizer imagepi1X. It is not a gauge classification over fixed f. Since target pi1 is abelian, it is a group torsor. Image must be precisely (a,k,3a). Integral change (u,m,v)->(v-3u,m,u) splits off C and leaves cokerD; no rational operation or assumptionCfree.
7. Existence: rank3 bundles over3CW classified byc1, SU3 bundles trivial, so every admissible pair is formally realized. delta is complex orientation-line c1 and2torsion; delta in2B iff reductionzero iffSq1w1=w1². Nonorientable examples can fail (RP2xs1 and RP2xR) or succeed (Kleinbottlexs1, where w1 lifts from integralbase anddelta0). Infinite/noncompact ordinary cohomology must not be replaced by compact-support cohomology.

## Independent preliminary conclusion and next controls

The integral formulas appear coherent under these standard relative/Postnikov facts. No mathematical counterexample identified yet; they remain hypotheses pending primary theorem and old-code audit. Key attack routes are relative identification loss, unstable pi4(SU2) contamination, incorrect ordinaryChern coordinate, absent SU determinant, fixed-f-only action, and rational torsion loss. Independently written cochain/virtual-Chern and quotient controls will implement these mutants; finite checks cannot prove the homotopy-fiber or stability theorem.
