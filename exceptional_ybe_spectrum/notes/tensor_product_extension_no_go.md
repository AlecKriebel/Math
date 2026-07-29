# Tensor products give only spectator stabilization

**Date:** 2026-07-29
**Scope:** the tensor-product operation on unitary \(R\)-matrices used in
Lechner, Proposition 3.6
**Status:** exact elementary lemma; no conclusion about other gluing
operations

Let

\[
q=e^{i\pi/3},\qquad \Sigma=\{-1,q\},
\]

and let \(R\) be an exceptional \(R\)-matrix.  Lechner recalls that the
tensor product \(R\boxtimes S\), after regrouping tensor factors, is
unitarily equivalent to \(R\otimes S\).  Hence

\[
\dim(R\boxtimes S)=\dim R\dim S,\qquad
\sigma(R\boxtimes S)=\sigma(R)\sigma(S).
\tag{1}
\]

The following observation closes this standard extension route.

## Proposition

If \(S\) is unitary and \(R\boxtimes S\) has spectrum contained in
\(\Sigma\), then \(S=I\).  In particular, tensoring an exceptional solution
can preserve the exceptional two-eigenvalue class only by spectator
identity stabilization.

## Proof

Take \(\mu\in\sigma(S)\).  Equation (1) implies

\[
\mu\Sigma\subseteq\Sigma.
\]

Multiplication by \(\mu\neq0\) is injective, so the two-element subset on
the left must equal \(\Sigma\).  Thus \(\mu\) belongs to the multiplicative
stabilizer of \(\Sigma\).

If \(-\mu=-1\), then \(\mu=1\), which indeed fixes \(\Sigma\).  The only
other way to send \(-1\) into \(\Sigma\) is \(-\mu=q\), or
\(\mu=-q\).  But then

\[
\mu q=-q^2=e^{-i\pi/3}\notin\{-1,q\}.
\]

Therefore the stabilizer is trivial and every eigenvalue of \(S\) equals
\(1\).  A unitary matrix with singleton spectrum \(\{1\}\) is the identity.
\(\square\)

## Consequence and limitation

Starting from the published \(d=4\) witness, the tensor-product operation
therefore produces exactly the known dimensions \(4m\), by taking
\(S=I_m\).  It cannot produce \(d=6\).

This proposition does not exclude a new colored gluing, off-diagonal
coupling, vertex--face conversion, or a solution unrelated to a tensor
product.  In particular, it is not a divisibility theorem.

## Source audit

The dimension and spectrum formula (1) was checked in the displayed
definition immediately before Lechner, Proposition 3.6, on page 15 of
arXiv:2603.20158v1.  Pages 15--16 were also rendered and visually checked
to guard against a text-extraction normalization error.
