# A finite congruence cannot simply stand in for disk cancellation

Prepared October 24, 2026 UTC. Exact obstruction to a particular relaxation; not an obstruction to every finite rational program, and not a counterexample to rationality.

Let

    G=<a,b,c,d | [a,b]=[b,c]=[c,d]=1>

be the P4 RAAG, and put g=[b,d]=b d b^{-1} d^{-1}. Killing a and c retracts G onto the free subgroup <b,d>. Hence scl_G(g)=scl_{F(b,d)}([b,d])=1/2. The last equality is the standard free commutator computation, stated for example in Heuer, arXiv:1802.01107v3, §2.2; its proof uses the free-group 1/2 gap and the once-punctured-torus upper bound. It is established input, not a new calculation here.

For N>=2 let G_N=G/<<b^N>>. In EVERY group the following identity holds, with factors ordered from i=N-1 down to i=0:

    product_i b^i [b,d] b^{-i} = [b^N,d].             (1)

It follows either by direct telescoping or induction. In G_N the right side is the identity. A sphere with N holes therefore maps to a K(G_N,1), with each oriented boundary conjugate to g. All these boundaries have degree +1 over the same loop g, so the total degree is N. Its Euler characteristic is 2-N. The surface formula for scl gives

    scl_{G_N}(g) <= (N-2)/(2N) = 1/2 - 1/N < 1/2.   (2)

The N=2 surface is an annulus and gives zero. The word g remains nontrivial in G_N, since killing a and c retracts G_N onto C_N*Z and [b,d] is reduced there. No exact claim for scl in that quotient beyond (2) is needed.

Now consider any proposed relaxation that replaces exact vanishing of middle-torus winding in Z^{b,c} by vanishing in a finite quotient Q and consequently allows a b^N loop to be capped as a disk at zero extra cost. The image of b has finite order, so some N>=2 is killed. Equation (1) and the sphere construction are then allowed by that relaxation. Its optimum on the SAME fixed input word [b,d] is at most the strictly smaller number (2). It therefore cannot equal scl_G(g).

Equivalently, before imposing b^N=1 one can use a sphere with N+2 holes mapped to G: N holes carry the conjugates of g appearing in (1), and the other two carry suitable conjugates of b^N and b^{-N}. Its boundary relation is (1) followed by the inverse of [b^N,d]. Falsely capping those last two holes converts its Euler characteristic -N into 2-N. Thus the obstruction is a concrete forbidden capping operation, not just an inference from changing the target group.

A method may still record finite congruence data together with an exact transportability condition or an additional defect cost. Chen's theorem does precisely require hypotheses and an asymptotic-promotion argument; no claim is made that it uses this invalid relaxation. The point is that arbitrary finite winding congruences, by themselves, never give an exact disk criterion even for this fixed P4 word. The displayed feasible objective values 1/2-1/N approach 1/2 as N tends to infinity. This proves neither convergence of the relaxed optima nor finite rationality in a general input; only upper bounds on those optima have been proved here.

Primary sources consulted: Chen, *Scl in graphs of groups*, arXiv:1904.08360v2, §§4–5 (disk promotion and its commensurability assumptions); Heuer, *Gaps in scl for Amalgamated Free Products and RAAGs*, arXiv:1802.01107v3, §2.2 and Theorem 7.3; the parent priority audit contains the original Kourovka source. These source scopes are not generalized to arbitrary RAAG words.
