# Exact domain, path and update

The problem is about a finite real-valued harmonic function u on **all of R^n**, with n>=3, that is not constant. It asks for a path along which both |x| and u(x) tend to positive infinity. It does not ask for a fixed ray, a rate in terms of |x|, finite total length, monotonicity of u along the path, or a bound on the number of straight segments.

The statement and immediately following Update3.2 were read in the original2018 PDF and visually checked on printed p.60/PDF p.61. The update records the desired existence theorem; a historical sentence about path regularity is followed by an explicit affirmative statement for the continuous/harmonic case and the citation of Carleson's polygonal theorem. The imported title-only/web-search report is not evidence that this remains open.

The source's nonconstant bounded subharmonic example is max(−1,−r^(2−n)), with value−1 at0 by continuous extension. It has supremum0. The cited theorem requires unboundedness above, so this example is outside its hypotheses. Harmonic nonconstancy implies that unboundedness by the one-sided Liouville argument given in SOURCE_PROOF.md.

The constructed path is a continuous parametrization on[1,infinity), formed by finitely many straight segments on each bounded parameter interval. Every compact subset of space meets only finitely many of its polygonal pieces. Thus it is a proper path to infinity, and u tends to positive infinity along its entire tail, not just along a subsequence of vertices. Simplicity/injectivity and a smooth parametrization are not asserted because they are not required for the source question.

Credit: Fuglede, *Asymptotic paths for subharmonic functions*, Math. Ann.213(1975),261–274, as cited by the source update; Carleson(1976), whose primary paper was retrieved and read. The present proof audit covers the continuous case independently of the fine-potential/Brownian-motion steps and the discontinuous case's technical approximation argument.
