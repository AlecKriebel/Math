# Algebraic dimensions of base and fibre cannot simply be added

An algebraic-reduction approach might try to obtain one meromorphic function along a generic fibre and add it to functions from the base. That addition is invalid without a relative extension theorem.

Use a non-projective elliptic K3 surface f:X→P¹ with connected fibres and NS(X)=Z[F], F²=0, where F is the fibre class. Such surfaces are standard examples documented in Daniel Huybrechts, *Lectures on K3 Surfaces*, author draft, Chapter 3, Example 3.2 and Chapter 17, §1, “Elliptic K3 surfaces”:
https://www.math.uni-bonn.de/people/huybrech/K3.html
https://www.math.uni-bonn.de/people/huybrech/K3Global.pdf
The author identifies this file as a prepublication draft, rather than the corrected published text.

Every irreducible curve C⊂X has C·F=0, since its divisor class is an integral multiple of F. If C dominated P¹, C·F would be the positive degree of f|C. Therefore every curve is vertical.

Let g be a global meromorphic function on X. Its polar divisor has finitely many vertical components. Away from finitely many base values (also omitting singular fibres and indeterminacy points), g restricts to a holomorphic function on a compact smooth elliptic fibre, and hence is constant there. It follows by meromorphic descent for a proper map with connected fibres that g∈f* M(P¹). Thus

    a(X)=1,       a(P¹)=1,       a(F)=1.

In particular the proposed inequality a(X)≥a(P¹)+a(F) would say 1≥2.

This is only a counterexample to that general addition step. It is not a counterexample to the positive-normal-bundle question: every smooth curve C in this X has deg N_{C/X}=C²=0, so no such curve has positive normal bundle. The target's positivity must do genuine work in extending fibrewise meromorphic functions. Merely observing that a fibre is algebraic does not provide this extension.
