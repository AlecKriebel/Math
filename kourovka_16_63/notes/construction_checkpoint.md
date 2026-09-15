# Construction checkpoint (independent verification in progress)

Candidate: p=1009. Rank-31 integral Lie algebra B with sl2 and modules U=V6,V=V4,W=V6,T=V2,R=V4,Z=V0. Exact raw transvectant brackets are specified by scripts/lie31.py and data/lie31_brackets.json.

Adapted basis starts x=h, y=e+f+U1+V0+R2, t=U0, then the original basis elements other than h,e,U0. Let A have weights (0,0,1,2,...,2) in this basis and L=p^2 A. Let i=1689 and candidate G=BCH(L/p^i L). The additive order is p^(31i)=p^52359. Since L is contained in p^2 B and p^i L contains p^(i+4)B, the quotient has nilpotency class at most 846, less than p.

Executed Python computations: integer Jacobi (4495 basis triples); B perfect; centre dimension 1; derivation dimension 30 and all derivations inner modulo p; x,y generate B modulo p; infinitesimal stabilizer of <x,y> subset <x,y,t> is zero. Derivation matrix delta_L has rank 931 and p-primary Smith valuations 0^87,1^55,2^758,3^6,4^25, summing to 1689. All arithmetic exact, not floating point. Need independent reconstruction/replay.

Proposed full-count argument: for i>=7, every automorphism of L/p^i L has a linear lift Q preserving A. Its bracket error on B is integral and zero mod p. Since x,y Lie-generate B, Q preserves B. Its reduction mod p preserves the two-step flag; the FULL flag stabilizer is trivial. Therefore Q is 1 mod p on B. The analogous argument for approximate derivations uses the zero infinitesimal flag stabilizer. Integral log/exp then gives a bijection between full finite automorphisms and the full kernel of delta_L mod p^i. A tensor-space factorization exp(X)-1=X U(X), with U integral invertible, is needed to justify equality of congruence conditions without loss of precision. Lattice amplitude is 2 on End(A) and 6 on bracket tensors; p=1009 exceeds all denominator bounds.

Full finite-field flag stabilizer proof: full Aut(B/Fp) has form exp(ad n) rho(s) tau^epsilon, n in N, s in PGL2(Fp), tau swapping V,R and negating Z. Prove this using H1(sl2,V_m)=0 for m=0,2,4,6 (not an unqualified positive-characteristic Levi theorem), followed by explicit equivariant block equations. Preserving the highest U line and the projected plane <h,e+f> forces s=1 or diag(-1,1). The latter is excluded by the U1 term in y; tau is excluded by the V0 and R2 terms. Remaining inner automorphisms fix the two Lie generators and hence are identity.

If the full-count lemma and independent computations pass, |Aut(G)|=p^(30i+1689)=p^(31i) at i=1689. This file records a candidate argument, not a claim of completed certification or peer review.
