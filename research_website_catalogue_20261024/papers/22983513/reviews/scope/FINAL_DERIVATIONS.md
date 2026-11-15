# Final scope deductions and reproducibility

The immutable INITIAL_RECONSTRUCTION.md contains the full independent eight-family
proof reconstruction. Primary reading confirms the required category and prior
identities; no substantive mathematical gap requiring repair or narrowing was
found. This file adds the explicit negative/scope and reproducibility checks.

## The domain argument is sufficient on arbitrary bounded open sets

Zero extension to an enclosing box establishes positivity and compact resolvent
for the H0^1 form without smooth boundary or a connectedness assumption. The
distributional operator-domain characterization follows by testing the form on
Cc-infinity and density. Multiplication by bounded x_alpha preserves H0^1 and
gives a distributional Laplacian in L², so x_alpha u is in Dom H. The derivative
v=-2partial_alpha u is NOT automatically asserted to satisfy a Dirichlet
condition. It enters Dom H only under the temporary assumption that x_alpha u
is a finite eigenfunction sum. Differentiation of an interior distribution
equation then yields (H-E)v=0. Since v=(H-E)w is simultaneously in the range
and kernel of the same self-adjoint H-E, v=0. Approximation integration by parts
instead gives <w,v>=1. This establishes the obstruction for every real
normalized eigenfunction and each coordinate, including disconnected domains
and arbitrary eigenvalue multiplicities. No boundary normal derivative,
ground-state positivity, H² regularity or unique continuation is assumed.

The classical trace/norm series are absolutely convergent by Dom H and
Cauchy-Schwarz. Inner spectral blocks cancel exactly, including degenerate
energies; threshold terms vanish. At every real z>E1, vanishing of the positive
remainder would put x_alpha u1 in the finite span of E_k<=z. The obstruction
therefore gives strictness, not merely a nonnegative remainder. At z=E1 the
empty lower set makes both sides zero; extending strictness to this endpoint
would be false. Compact resolvent, not a numerical cutoff, justifies finiteness
of the relevant spectral subspace.

The completed square uses mean(E²), not mean(E) or M2 unsquared. Both endpoint
tests include all lower energies and ignore zero-weight tied threshold terms.
When E[J+1]>E1, the upper endpoint lies strictly inside the quadratic roots;
when E[J+1]=E1, D=4E1²/n²>0 and gap0. Thus every finite J in the original
category is covered. No simplicity/positive-gap premise is inserted.

## Source normalization and genuine negative controls

Actual OWR printed415 has the missing square; actual HS1995 Proposition6 has
the squared second moment. Scaling lengths by c sends both corrected sides to
c^-4 times themselves. The literal unsquared display is not homogeneous and
is not the theorem being claimed. For n=1,J=1 and normalized interval E1=1,
scaling to c=10 gives M1²=9/10000 and M2=sqrt5/100>2/100, making the literal
M1²-M2 negative while the squared gap is nonnegative. This is a counterexample
to treating the literal old display as a universal inequality; it is not a
counterexample to the explicitly corrected original target.

On the interval E_j=j² (length pi), the exact gap deficit is

    D-(E[J+1]-E[J])²/4=(2J+1)(3J²+2J+2)/12>0.

Disconnected equal intervals create E2=E1 and exercise the exceptional ground
branch. Rescaling drives the absolute deficit to0; no scale-independent uniform
positive deficit follows from finite strictness. Abstract finite matrices cannot
realize the coordinate TRK rule for every eigenvector: summing the symmetric
matrix first moments cancels to0, whereas a rule equal1 for every row would sum
to its positive dimension. Synthetic finite matrices can check cancellation
algebra only. The supplied program states this limitation correctly.

For an independent infinite-support check, on (0,pi), product-to-sum and
integration give

    a_1k=(1/pi)[(((-1)^(k-1)-1)/(k-1)²)
                    -(((-1)^(k+1)-1)/(k+1)²)]
         =-8k/[pi(k²-1)²] for even k,

and zero for odd k>=3; the diagonal is pi/2. Thus an even k beyond every finite
threshold gives a strictly positive spectral-tail summand. My exact controls
check this rational/sign consequence through z=10^20, without pretending a
finite truncated sum equals the full trace rule or proving a rough-domain
theorem by interval examples.

## Meaningful supplied replay and materially different checks

The entire16378-byte `verification/verify.py` was personally inspected before
execution. It uses only standard-library exact Fractions, explicit checks that
remain active under-O, complete box prefixes certified by omitted-mode lower
bounds, multiplicities, length scaling, finite cancellation algebra and three
negative controls. Its output path is configurable. The exact owned copy
`supplied_verify_copy.py` was used with outputs confined to this review folder.
No builder/site copy/finalizer was run; no source program/result file was edited.

Normal and optimized runs each pass7016checks/1312certified box-J cases and
three negative controls. Their complete JSON objects are identical and match
the unchanged deposited results.json. This is reproduction of what the program
claims, not formal verification of the analytic proof.

My independently written `independent_checks.py` does not import the supplied
checker. It enumerates exact box spectra using a monotone priority-queue frontier
over modes and disconnected components. Every unseen mode has a monotone path
from all-one coordinates; its first unpopped predecessor frontier has no larger
energy. Hence sorted popped values form a complete exact prefix, with all equal
energies retained. This differs from the supplied rectangular-cutoff certificate.
Six families, including unequal disconnected intervals/rectangles, give960gap
cases,1134real-threshold cases,399zero gaps and two repeated-ground branch
cases; every check passes. It independently checks length scaling, interval
closed form and nonzero Fourier tails. Exact case digest is in the JSON.

These finite checks are falsification attempts and algebra/replay evidence.
The form-domain, self-adjointness, spectral-support and remainder deductions
establish the universal full original theorem. No empirical boundary regularity,
precision assumption, human review or proof-assistant certification is hidden.
