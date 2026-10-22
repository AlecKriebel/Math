**Integrated reader status.** Accepted supplementary identity. It explains why separate marginal balance cannot be replaced by simultaneous balance. See the [integrated theorem](../README.md) and [dependency map](../DEPENDENCIES.md).

# Equal negative dimensions for a product of conjugate involutions

Let the field have odd characteristic. Let t,s be conjugate involutions on a finite-dimensional vector space, put y=ts, and let z=inv(y). Then

dim(E_−(z)∩E_+(t)) = dim(E_−(z)∩E_−(t)).

This requires no semisimplicity of y and, in fact, no bilinear form. The order is finite in the applications here. If y has odd order, z=I and the statement is immediate. Otherwise write |y|=2^h m with m odd and h≥1.

Extend scalars to an algebraic closure; all dimensions at issue are unchanged. From t y t=y^−1, both t and s exchange the generalized λ- and λ^−1-spaces. For λ≠±1 the sum of such a reciprocal pair consequently has equal positive and negative dimensions for t and also for s: in block form either involution interchanges two equal-dimensional summands. These dimensions are integer multiplicities, not traces in the ground field.

On the generalized +1-space V_+, y is unipotent of odd order. If o is this order, choose r with 2r≡1 modulo o. Then y^−r t y^r=t y^(2r)=ty=s. Hence the t- and s-negative dimensions agree on V_+.

On the generalized −1-space V_−, write y=−u with u unipotent of odd order. We have t u t=u^−1 and s=−tu. The same odd-root conjugation shows tu is conjugate to t on this space, so the s-negative dimension equals the t-positive dimension there. Since t and s are conjugate on the entire vector space, their global negative dimensions agree. Contributions from V_+ and all reciprocal pairs already agree, so on V_− the t-negative and t-positive dimensions must agree as well.

Raising to |y|/2 kills every unipotent part, because the characteristic is odd. On each generalized λ-space, z is scalar −I exactly when λ's multiplicative order has two-part 2^h, and is +I otherwise. Thus z selects complete reciprocal pairs among λ≠±1, all balanced for t. It is +I on V_+. It is −I on V_− when h=1, and +I there when h>1; V_− is balanced in either case by the preceding argument. Its complete negative space is therefore balanced for t, proving the equality.

In the symplectic application, t and z commute and their joint eigenspaces are nondegenerate, so these intersection dimensions are also even. If the t-eigenspaces have dimensions 2a and 4a and both restrictions of z were strong, their common negative dimension R would satisfy

R∈[2a/3,4a/3]∩[4a/3,8a/3] = {4a/3}.

When 3 does not divide a this is not an integer, so simultaneous success is impossible. The separate marginal probability theorem avoids this obstruction.
