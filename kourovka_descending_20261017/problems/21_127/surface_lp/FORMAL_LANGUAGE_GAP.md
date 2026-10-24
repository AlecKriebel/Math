# Word-equation descriptions do not yet give a rational scl program

Prepared October 24, 2026 UTC. This records an attempted alternative finite encoding and the exact missing implication. No RAAG irrational example is claimed.

## What is available

Diekert–Jeż–Kufleitner, *Solutions of Word Equations Over Partially Commutative Structures*, ICALP 2016, Theorem 1, DOI [10.4230/LIPIcs.ICALP.2016.127](https://doi.org/10.4230/LIPIcs.ICALP.2016.127), gives an effective EDT0L description of solutions of equations in RAAGs using a finite automaton accepting a rational set of endomorphisms. Its satisfiability and finiteness tests follow from that automaton. The group version and subsequent paragraph include finite systems.

For a FIXED pair of integers n,k, the condition

    [x1,y1] ... [xk,yk] = w^n

is one such equation, quadratic in its unknown group elements. Thus it can be decided whether cl(w^n)<=k. If w is in the commutator subgroup, searching k upward halts, so each cl(w^n) is computable. Enumerating n produces rational upper bounds min_{1<=j<=n} cl(w^j)/j converging to scl(w). This is a computability fact about finite commutator length and a one-sided approximation, not rationality of its stable limit. The number of unknowns grows with k; the source does not produce one fixed finite automaton whose additive weights encode all genus/exponent pairs.

A current paper, Diekert–Natterer–Thumm, *Quadratic Equations in Graph Products of Groups and the Exponent of Periodicity*, Groups, Complexity, Cryptology 18(1) (2026), 3:1–3:32, published April 1, DOI [10.46298/jgcc.2026.18.1.17585](https://doi.org/10.46298/jgcc.2026.18.1.17585), Corollary 7.1, states that an infinite quadratic-equation solution set in a RAAG has unbounded exponent of periodicity in every shortlex normal form. This is not a semilinearity or rational-slope theorem for all genus/exponent pairs. Its general scope includes groups where quadratic solvability itself can be undecidable; it is not an optimization theorem.

## A finite endomorphism system can already have an irrational infimum

Let the working letters be A,B and terminal letters be a,b. Let psi fix the terminals and act by

    psi(A)=ABA, psi(B)=AB.

After n>=1 iterations, terminalize A to a and B to b. This is an EDT0L language with a finite control automaton: apply psi one or more times, then apply the terminalizing endomorphism. If (u_n,v_n) counts the terminal letters a,b, then

    (u_0,v_0)=(1,0),
    (u_{n+1},v_{n+1})=(2u_n+v_n,u_n+v_n).

In particular v_n>0 for n>=1 and (u_n,v_n)=(F_{2n+1},F_{2n}). The ratios r_n=u_n/v_n obey

    r_1=2,  r_{n+1}=(2r_n+1)/(r_n+1).

Let phi=(1+sqrt(5))/2. For r>phi, the displayed fractional transformation has value strictly between phi and r: subtracting r has numerator -r^2+r+1<0, while subtracting phi has the same positive sign as r-phi. Therefore r_n decreases to a limit L>=phi. Its recurrence implies L^2-L-1=0, hence L=phi. Consequently

    inf_{n>=1} u_n/v_n = phi,

which is irrational, despite the finite integer endomorphism description. Closing these count vectors under finite addition does not change the infimum: the ratio of a sum is a denominator-weighted average of its summands' ratios. Thus even allowing disjoint-union-style additivity does not by itself produce a rational cone or a rational stable value.

This elementary example is NOT asserted to be a solution set of a particular RAAG commutator equation, nor are u_n and v_n surface genus and boundary degree. It falsifies only the proposed general implication from a finite endomorphism description plus additive count objectives to a rational optimal ratio. A proof must establish stronger structure specific to admissible surfaces, such as a genuine rational polyhedral cone with a realization theorem.

## Remaining gap

One would need a uniform encoding for all powers and genera, control of the relevant two-parameter image, and proof that its stable lower boundary has rational slope. A finite description of each individual quadratic equation, unbounded periodicity, and computability of each finite genus do not supply those steps. The route remains blocked pending a materially stronger mechanism.
