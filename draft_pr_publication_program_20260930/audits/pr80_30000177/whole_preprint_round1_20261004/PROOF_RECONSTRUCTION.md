# Independent proof reconstruction and boundary adjudication

The full-density determinant artifact verifies all finite states. Analytical reconstruction independently supplies the interpretation:

For letters x,y, the unencoded Bell branches on R are psi+/2,psi+/2,00/sqrt(2),0. Pauli x permutes the four Bell projectors; Pauli y conjugates their residual matrices. Tensor products over resource copies produce a cqMAC. Complete classical forwarding places J^nR^n in one local laboratory.

Uniform product twirls give S(omega_xy)=3/2, S(mean_y)=S(mean_x)=3, S(mean_xy)=3+h2(1/4). Primary Winter Theorem9 accepts nonnegative rates and has exactly the two conditional3/2 constraints and sum3/2+h2(1/4) constraint. Its codebooks are Cartesian products and error is uniform average error, rather than maximal error.

For a target interior rate R with a zero component, choose R' strictly componentwise above it and still interior. Winter gives sufficiently large codes with rates above R for a sequence of small errors/slacks. Let desired sizes be K_i=floor(2^(nR_i)), with K_i=1 at R_i=0. Choose uniformly random K_i-subsets of the two message sets independently. The expected uniform average error of the product subset is the full code's average error, because each original message pair has the same inclusion weight K1K2/(N1N2). Consequently a product subset exists with no larger error. Retain its encoder words; retain the corresponding POVM elements and assign all unused elements to one selected decoded label. This remains a complete POVM and cannot lower success probabilities on the selected pairs. Rates then converge to R_i and error tends to zero. At (0,0), both message sets may be singletons and a constant decoder has zero error.

For N1N2>=2, standard Fano yields the manuscript inequality. Then I(M;Mhat)/n is bounded below by (log2 N1+log2 N2)/n minus h2(e_n)/n and e_n log2(N1N2-1)/n, so it approaches the sum rate. For N1N2=1, the correct information statement is I=0 directly; the log2(0) display should not be evaluated. This last expression-domain observation was supplied after FIRST by ROOT and independently confirmed here.

Pinching J blocks of the joint decoder preserves each success probability because outputs are diagonal there. Each block is a POVM on local R^n; the physical implementation uses only receiver1→receiver2 classical Bell outcomes. There is no additional sender disclosure, feedback or quantum link across receivers.

The original LO marginal expression gives2h2(1/4)<2. The achievable strict LOCC rate exceeds2, so the historical classification follows. These deductions do not certify one-copy advantage, optimal capacity or novelty of the Bell/MAC method.
