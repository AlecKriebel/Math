# Circular assume–guarantee reasoning: complete proof candidate

**Problem 30001199 / OWR-3394-009. Three substantive author turns used. Independent review pending.**

The exact finite-dimensional continuous-time linear rule in the 2009 source is proved in TURN_3.md, using the quotient construction of TURN_2.md. This is a corrected proof of an affirmative theorem already stated in 2010, not a claim to have first discovered that theorem. Final repository disposition must await an independent source and proof audit.

## Exact result and scope

Components have constant real matrices, dynamics x'=Ax+Bu+Ld and output y=Cx. Disturbances are freely varying, with no magnitude or energy constraint. A simulation is a linear, output-preserving relation that is full over all source initial states and matches every source disturbance by a target disturbance while preserving the relation. Feedback is u1=-y2, u2=y1, and the ordered output pair is observed.

If P1||Q2 is fully simulated by Q1||Q2 and Q1||P2 is fully simulated by Q1||Q2, then P1||P2 is fully simulated by Q1||Q2. No extra injectivity, controllability, stability or disturbance-rank assumption is required. This says nothing about arbitrary nonlinear systems, labeled transition systems, restricted disturbances or other composition semantics.

## Proof mechanism

1. Quotient each specification by its maximal controlled-invariant output-nulling subspace. The quotient is fully bisimilar for the same interconnection input, and replacing components preserves both premises and the conclusion.
2. With those subspaces zero, each repeated context component has equal state in the two copies. The full premise relations are unique graphs q1=F p1+E q2 and q2=H q1+J p2.
3. The disturbance quantifiers imply E(im L2) is contained in im L1 and H(im L1) is contained in im L2. Their drift identities imply that the stabilized image of EH is controlled invariant and output nulling. It must therefore be zero: EH is nilpotent.
4. The finite inverse S=(I-EH)^(-1) gives a full initial-state graph q1=S(F p1+EJ p2), q2=H q1+J p2. It also preserves im L1. This same inverse solves the simultaneous target-disturbance equations, establishing trajectory simulation for every source disturbance.
5. Lift through the quotient bisimulations to the original specification states.

The implementation-to-specification initial state depends only on the implementation initial state, not on future disturbances. Zero-dimensional quotient spaces are included.

## Primary credit and dependency qualification

The problem is the closed-feedback question in Arjan van der Schaft's contribution, jointly with Florian Kerber and Harsh Vinjamoor, to *Control Theory: On the Way to New Application Fields*, OWR 11/2009, printed pp.655–658, DOI 10.4171/OWR/2009/11. The publisher PDF was downloaded and the relevant pages visually inspected:

- https://ems.press/journals/owr/articles/3394
- https://ems.press/content/serial-article-files/46211

Kerber and van der Schaft, *Compositional analysis for linear systems*, Systems & Control Letters 59 (2010), 645–653, DOI 10.1016/j.sysconle.2010.08.002, **Theorem 4**, already asserts the affirmative rule. The change of the first-role B signs, with performance output H=C and external inputs zero, matches the 2009 source convention. Primary indexed text and institutional metadata were read:

- https://pure.rug.nl/ws/portalfiles/portal/2629447/2010SystContLettKerber.pdf
- https://research.rug.nl/en/publications/compositional-analysis-for-linear-systems/

The 2010 binary endpoints returned access errors; no visual PDF inspection is claimed for that article. DEPENDENCY_CHECK.md gives a narrow exact diagnostic against the displayed instantaneous-kernel enlargement in indexed Lemma 1, equation (22), and its Appendix A argument. It is not a counterexample to Theorem 4. The present proof does not use that enlargement. Historical novelty of this replacement proof mechanism is unestablished. No external author contact or public priority claim is part of this packet.

## Controls and frozen history

- Dependency diagnostic: 14 exact assertions
- Turn 1: 540 exact assertions; separately labeled finite-field proposal search
- Turn 2: 2,207 exact assertions on 140 quotient fixtures
- Turn 3: 4,614 exact assertions on 112 full-rule fixtures, including nonzero nilpotent cycles, 100 fixtures with implementation disturbances, and zero-dimensional quotient cases
- Total exact assertions: 7,375; finite searches supplement rather than prove the theorem

Earlier files retain their historical unresolved status and hashes. TURN_STATE_v3.json and this document describe the current candidate. No additional author search is needed while the independent audit is pending.
