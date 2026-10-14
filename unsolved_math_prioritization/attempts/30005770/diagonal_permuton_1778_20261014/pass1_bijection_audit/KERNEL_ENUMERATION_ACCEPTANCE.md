# Independent acceptance of exact kernel enumeration

Shared PASS 1, 14 October 2026. Reviewed artifact: `pass1_entropy/KERNEL_ENUMERATION_APPENDIX.md`, 7160 bytes, SHA-256 `a57401941f3ec1296e7880d791a495c4daec92d8c714e92435c1e73d443c5181`.

**Accepted without a requested mathematical correction.** This appendix derives the proper beta-tree generating function directly from the exact labeled-tree specification. It therefore removes the external counting-formula dependency from the accepted height argument. It neither replaces Bóna's permutation–tree bijection/minima preservation nor extends the two proven target cases.

Checks completed:

1. Every relaxed label is bounded by subtree size minus one. Coefficients in the root-label variable are therefore polynomials, making the formal substitution U(z)=1+O(z) and differentiation valid.
2. The catalytic equation exactly sums all permitted root labels and nonempty ordered child sequences. The proper-root equation T=z(1+C) is exact.
3. The kernel F=P_b after substituting B(z,u) and C(z) has F(0,u)=1-u. Its u derivative at (0,1) is -1. The formal implicit function theorem produces U, and the formal chain rule gives P=P_b=P_u=0 at the kernel point.
4. Direct independent expansion verifies `P+(1-b)P_b=(1-u)(1-b)^2+zu^2`. Eliminating z in P_u factors exactly as `(bU-b+1)(2bU-b-U+1)=0`. The first factor has constant term1 and is invertible; the second determines the admissible branch.
5. The resulting equations `U=(1-beta)/(1-2beta)`, `z=beta(1-2beta)` and `C=beta(1-3beta)/(1-2beta)^2` have zero residual in each of P, P_b and P_u. I independently derived these equations before receiving the appendix. The beta branch with zero constant term is uniquely `(1-sqrt(1-8z))/4`.
6. The cancellation by beta is valid in the integral domain Q[[z]] because beta=z+O(z^2) is nonzero; all remaining denominators are units. No invalid inverse of a zero-constant-term series is used.
7. Substitution gives the stated T(z), corrected coefficients, radius1/8, critical value5/32 and Stirling constant3/(16sqrt(pi)). These match independent direct label enumeration through8 vertices recorded in this reviewer's finite checks.

The appendix is purely formal until the explicit coefficient formula is obtained, so no circular appeal to the analytic radius or the height theorem occurs. It is a valid replacement for the previously cited enumerative input. The labeled-tree height and permuton proofs remain accepted with their restricted alpha132/alpha213 scope.
