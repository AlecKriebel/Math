# Pointwise quadratic bounds for extremal solutions

## Source target

Let Omega be a smooth bounded domain in R^n. The surrounding setup in Oberwolfach Report 37/2024, pp. 2141–2143, takes f:R->R positive, increasing, and convex, additionally requiring f(0)>0, integral_1^infinity dt/f(t)<infinity, and f(t)/t->infinity. Consider

    -Delta u_lambda=lambda f(u_lambda) in Omega,
    u_lambda>0 in Omega,  u_lambda=0 on the boundary.

Let u* be the increasing limit of the minimal stable branch as lambda approaches the finite positive extremal parameter lambda*. Suppose 0 is an isolated interior singularity: u* is unbounded near 0 and locally bounded at every other point of a sufficiently small punctured ball. The question is whether

    limsup_(x->0) |x|^2 f'(u*(x)) < infinity.

The source's initial setup uses f' without separately specifying a C^k class. We retain its differentiable-convex convention rather than importing the C^2 hypothesis from its later singular-set theorem. The C^3 calculations in Route 3 are explicitly conditional. Smooth countertests lie within the differentiable class.

Source: https://ems.press/content/serial-article-files/50045 , §3.1 and its preceding setup.

## Normalization and success criterion

Throughout the arguments, V=lambda* f'(u*). Because lambda* is fixed, finite, and strictly positive, finiteness of limsup |x|^2V is equivalent to the target. The question permits a constant depending on the fixed problem; it does not demand a universal bound at a prescribed scale across all domains and nonlinearities.

A full proof must cover the stated arbitrary-domain isolated-singularity case. A disproof must produce one admissible nonlinearity and a genuine positive zero-Dirichlet extremal solution with an isolated singularity and divergent limsup. A generic stable potential, an entire solution with different boundary behavior, a family of regular solutions, or a radial special case does not meet that criterion. Low-dimensional regularity does not resolve the high-dimensional singular case.

## Disposition

Unfinished after five substantive routes. No full proof, no extremal counterexample, and no novelty claim. The report supplies exact partial lemmas and explicit tests falsifying several weaker proposed implications.
