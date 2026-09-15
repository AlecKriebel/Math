# Unfinished second-family route (not imported)

No Lean SOS theorem is supplied here. The exact Python preflight separately
checks the following symbolic identity; that is not a Lean proof.

For arbitrary unitary A_l,B_y, with only cross-party commutation, put
Bhat_l=sum_y i^(ly)B_y, P_l=4 lambda_l I-A_l Bhat_l and
F=sum_l Re(conjugate(lambda_l) A_l Bhat_l). Then the intended chain is:

1. Prove the actual source coefficient specialization and sum |lambda_l|²=1.
2. Prove Fourier orthogonality gives sum Bhat_l^dagger Bhat_l=16I.
3. Expand sum P_l^dagger P_l. A_l^dagger A_l=I eliminates each Alice factor;
   the scalar term is 16I and the Fourier term is another 16I. Cross terms
   are -8F. Thus `(1/8) sum P_l^dagger P_l = 4I-F`.
4. The augmented gap adds `(1/2)(I-A0 B4)^dagger(I-A0 B4)`.
5. Prove a nonnegative expectation/trace for each square under every allowed
   normalized mixed state. Do not restrict local dimensions to four.
6. Prove the PVM-to-unitary encoding for arbitrary PVMs; prove the explicit
   full witness's PVMs, Fourier compression, annihilation, and aligned term.
7. Combine with the physical target table only after these steps are checked.

Use the coefficients in Functionals.lean rather than define a replacement
functional by its SOS. Proving an identity conditional on a normalization or
unitarity assumption is a helper, not the complete physical endpoint.

The first-family upper bound is a separate problem. Its source route includes
partial-isometry polar factors and functional calculus. This file contains no
attempt to substitute the second family's bound for the first.
