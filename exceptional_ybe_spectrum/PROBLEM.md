# Exceptional unitary Yang--Baxter dimension spectrum

## Primary question

Let \(V=\mathbb C^d\), let \(q=e^{i\pi/3}\), and let
\(P\in\operatorname{End}(V\otimes V)\) be an orthogonal projection of rank
\(d^2/2\).  Put

\[
P_1=P\otimes I_d,\qquad P_2=I_d\otimes P.
\]

Determine exactly which even positive integers \(d\) admit a solution of

\[
P_1P_2P_1-P_2P_1P_2=\frac13(P_1-P_2).
\tag{YB-P}
\]

Equivalently, for \(H=I-2P\), require

\[
H=H^*,\qquad H^2=I,\qquad \operatorname{Tr}H=0,
\]

and

\[
H_1H_2H_1-H_2H_1H_2=\frac13(H_1-H_2).
\tag{YB-H}
\]

Then

\[
R=-P+q(I-P)
\]

is a unitary Yang--Baxter matrix with eigenvalues \(-1,q\), each of
multiplicity \(d^2/2\).

## Known boundary data

- An exact solution exists for \(d=4\).
- Tensoring that solution with spectator identities gives solutions for every
  \(d\) divisible by four.
- The originating classification excludes \(d=2\).
- Odd \(d\) cannot have rank \(d^2/2\).
- The unresolved dimensions are \(d\equiv2\pmod4\), beginning with \(d=6\).

## Scope discipline

The primary problem is existence in the matrix class defined above.  The
following are separate properties and must not be silently assumed:

1. scalar left and right partial traces;
2. standardness;
3. agreement of the entire tensor-space trace with a specified Markov trace;
4. faithful localization of the Jones--Wenzl quotient.

Any implication among these properties must be proved with its hypotheses
stated explicitly.

## Target outcomes

The preferred outcome is a proof of the complete spectrum.  This may be:

- exactly the multiples of four;
- every even \(d\ge4\);
- or another explicitly characterized set.

If the complete spectrum remains out of reach, the fallback must still be an
exact structural theorem that materially narrows the problem.  Numerical
failure at \(d=6\) is not a theorem.
