# Reader's note: the unified end goal

**Alec Kriebel, with heavy assistance from ChatGPT 5.6 Sol (OpenAI)**

Research draft prepared 22 July 2026. Not peer reviewed.

> **Verification warning.** Alec Kriebel is a complete amateur and cannot
> independently verify these claims. This package is an experiment in the
> limits of AI-assisted mathematics and is published for expert checking.

## The point of Discovery 07

The repository had accumulated three technically related papers: a
22/44-variable cubic-to-quartic reduction, a 21-variable Special Image
construction, and a stronger 14-variable unipotent construction. Discovery 07
does not add their theorem counts. It identifies the common engine and gives
one self-contained proof.

For a Keller pencil `I + tH`, take its formal inverse `Q_t` and a linear
observable `lambda`. If every positive coefficient of

    lambda(Q_t(target))

is nonzero, two exact transfers are available.

- Abhyankar--Gurjar turns those coefficients into
  `E(lambda * A^m) != 0`, while `E(A^m) = 0`.
- Symmetrization followed by Zhao's inverse formula turns them into a nonzero
  directional derivative of `Delta^m(P^(m+1))`.

This is the paper's conceptual theorem. The large examples are realizations of
it, not unrelated computational claims.

## Headline package

The exact 14-variable map has 24 nonlinear monomials and satisfies

    det(I + s Jg) = 1,
    (Jg)^14 = 0,
    (Jg)^13 != 0.

Its special fiber is certified scheme-theoretically by

    4z + 1 - 27x^2,
    2y + 3x,
    x(x - 1)(x + 1),

so it consists of exactly three reduced rational points. A weighted dilation
conjugates every nonzero member `I + s g`, and the formal inverse observable
has a closed nonzero formula in all three residue classes modulo three.

The same coefficients prove failure of `SIC(14)` at every exponent and feed a
30-variable homogeneous degree-eight Hessian-nilpotent witness. A separate
rank-compressed cubic realization produces a 44-variable homogeneous quartic
with every-order nonvanishing. The first endpoint is smaller-dimensional; the
second is the canonical quartic case.

The real collision also refutes the stated Campbell,
Chamberland--Meisters, and Kulikov formulations. These are grouped as one
direct consequence family. Older dynamical counterexamples are not claimed as
new discoveries.

## The stopping rule

Discovery 07 is intended to be the canonical consequence paper. Discoveries
03, 05, and 06 remain immutable precursor records, not three additional
current publications. Discovery 04 remains independent.

After this consolidation, another numbered paper should clear a higher bar:
it should improve a meaningful extremal parameter, establish a new explicit
reduction class, or prove a genuinely new transfer theorem. Additional named
corollaries of the present inverse series belong here rather than in new
papers.
