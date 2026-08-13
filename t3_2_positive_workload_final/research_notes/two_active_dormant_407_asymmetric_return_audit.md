# Independent audit: repeated neutral entries defeat the frozen asymmetric mark

Audit date: 2026-08-11 PDT.

## Strict verdict

**FAIL as written.**  The frozen asymmetric repair does not prove its
physical-step Foster--Feynman--Kac inequality (7.16i).  A zero-paid exact
self-macro can repeat polynomially many times before a slow base service.
After the self-macros are contracted, a paid exact physical return increments
the global mark `J` with probability tending to one.  Its `Psi` multiplier is
the fixed number `z1>1`, contradicting (7.16i).

This is a proof counterexample.  It is not a counterexample to descriptor-local
recurrence, T3-2, or C3.  No incidence or pair is promoted.  Every analytic,
pair-level, and global certification flag remains false.

The audited frozen hashes are:

    theorem  d7e3ba1548b8b5a3396f9b9aa5de458fd792039b10f780e57623696337ce64c7
    source   098969ceeef5589a5a17f000901f43f168583015ac435de8c025add5c412e6a2
    tests    ee51167d4948b8fff00d1ce4ae990d61aada1692656b1495d1e1e456359f8804

The displayed top-step inequality (7.16g) also lacks a typographical `+`
before `epsilon Psi`.  This audit reads the intended stronger inequality with
that plus sign.  The failure below is independent of the typo.

## Exact template, orientation, and rates

Use the exact normalized template

    L+ = {2U, V+I},       L0 = {0, I, 2I, U+I}.

It occurs once in the 146-template menu and in six physical generalized rows,
twice at each spectator cap 0, 1, and 2.  Orient the linkages by

    2U -> V+I -> 2U,
    0 -> I -> 2I -> U+I -> 0,

and set every rate constant to one.  Both orientations are strongly
connected.

Write `n` for the initial `V` population, `R=V-n`, and let `J` count paid
lower firings exactly as in the frozen note.  At a no-fast base
`(U,I,R,J)=(u,0,0,j)`, the word

    2U -> V+I,  2U -> V+I,  V+I -> 2U,  V+I -> 2U

has paid-status `(zero, paid, fast, fast)` and returns to

    (U,I,R,J)=(u,0,0,j+1).

It is an exact physical-state return except for the auxiliary proof mark `J`.
Consequently

    Psi(endpoint) / Psi(start) = z1 > 1;                         (A.1)

the `a_I`, `a_R`, and `phi_r(U)` factors cancel exactly.

## Contraction amplifies the paid return

Put `a=(u)_2`.  At the base, the neutral proper entry has rate `a`, while the
service entry `0->I` has rate one.  After the neutral entry, the fast cleanup
has rate asymptotic to `n`, whereas the paid duplicate proper entry has rate
asymptotic to `u^2`.  Hence a raw neutral attempt produces the paid exact
return with probability asymptotic to `u^2/n`.  A simple exact neutral return
occurs otherwise and starts another attempt.  There are order `u^2` attempts
before the rate-one service cut.  After those simple returns are contracted,
the probability that the next nonself outcome is the paid exact return is

    q_n = (1+o(1)) u^4 / (n+u^4).                                (A.2)

Take `n=m^3` and `u=floor(m/4)`, which is strictly below the frozen boundary
`L_n=floor(n^(1/3))`.  Then `q_n -> 1`.  The exact replay gives

| `m` | exact lower bound for `q_n` |
|---:|---:|
| `10^3` | `0.7869417` |
| `10^4` | `0.9745512` |
| `10^5` | `0.9974048` |
| `10^6` | `0.9997400` |

For the fixed `z1>1` required by (7.16d), eventually `q_n z1>1`.  Positivity
of the continuation kernel and (A.1) imply

    K_n Psi >= q_n z1 Psi > Psi.                                 (A.3)

This already contradicts intended (7.16i), before its positive occupation
charge is added.  If the paid exact returns are instead summed inside one
hybrid step, the corresponding `z1`-weighted geometric series fails for the
same reason (or grows to the `J=L_n` stop).  Thus the issue cannot be removed
by choosing which side of the skeleton step contains the exact return.

The estimate in (7.16h) counts the probability `O(U^2/n)` once per opened
macro.  It omits the order-`U^2` repetitions of this exact neutral macro before
the degree-zero service cut.  That is the precise missing factor.

## The hostile state is historically reachable

The objection is not based on an unreachable interior state.  Starting from
the valid cap-two base `(U,I,R,J)=(2,0,0,0)`, the physical word

    2U -> V+I, I -> 2I, V+I -> 2U,
    2U -> V+I, 2I -> U+I, V+I -> 2U

has statuses `(zero, paid, fast, paid, paid, fast)` and maps

    (u,0,0,j) -> (u+1,0,0,j+3).                                 (A.4)

No fast firing in (A.4) starts at `R=0`, so no service occurs.  Repeating
(A.4) `k=floor(L_n/4)` times reaches

    U = L_n/4+O(1),        J = 3L_n/4+O(1),

while remaining strictly inside every auxiliary boundary.  Every finite word
has positive probability under the stated positive rates.

## What survives

The exact reserve calculation survives: before first old-active service,
`R=V-n` is nonnegative; a lower firing cannot decrease it and increases it by
at most one; every `V+I` firing has `Delta R=-1`; and a fast firing starting at
`R=0` is terminal service.  Every nonterminal fast step also has
`Delta I<=1`.

The bounded compact corrector and the uniform bounded-jump ratio for
`phi_r=D_r+(1+u)^(r+1)+kappa_r(u)` survive in isolation.  The asymmetric
top-phase physical-step estimate, including the actual terminal reward, also
has no counterexample once (7.16g) is read with its missing plus sign.  The
failure is the subsequent composition with the repeatedly contracted base
kernel.

Therefore (7.16k), the all-`J` endpoint and duration bounds, the arbitrary-q
boundary deductions in (8.2)--(8.2a), and the exhaustion used in (8.6a) do not
follow from the frozen proof.  The fourth-power Taylor algebra is correct only
conditional on those missing estimates.

## Verified repair architecture

A viable next repair is two-level rather than global in `J`:

1. Reset the **local** `J,I,R` proof marks at every physical no-fast base
   return.  Exact physical self-returns are then deleted completely.  A
   nonexact return retains its actual `U` endpoint and enters a second killed
   one-species base resolvent.
2. Use the asymmetric Feynman--Kac mark only inside one opened top excursion.
   It still controls arbitrary paid order within that excursion.
3. Prove a second perturbation theorem for the resulting nonself base kernel,
   then use its killed Green operator to sum all base returns and promotion
   hits.

The finite case split supports this architecture.  The only exact proper pair
whose self source has degree two and whose lower maximal I-free cut has degree
zero is the witness above.  Its apparent `U^4/n` perturbation is exactly the
deletable paid self-return.  Any nonexact outcome uses a lower paid clock of
rate at most `O(UI)` at the opened state, so its effective rate is at most
`O(U^3/n)`.  At `U<=n^(1/3)` this is `O(1)`, while the degree-zero lower cut is
necessarily service; its loss of order `phi_r(U)` dominates bounded-jump
errors of order `U^r`.

The other five exact `{2U,V+I}` templates have lower cut degree one, so their
remaining nonexact perturbation ratio is

    O(U^3/n) / U = O(U^2/n) = O(n^(-1/3)).

The exact `{U,V+I}` and `{0,V+I}` pairs have still safer degree comparisons.
If the proper support is larger than an exact pair, strong connectivity gives
a fixed-probability cut per excursion, so the order-`U^2` repetition factor is
absent.  No nonexact outward event of order `U^4/n` was found.

This case split is evidence for the proposed repair, not its proof.  The next
snapshot must explicitly construct the second killed base resolvent, delete
only exact physical self-loops, retain actual endpoints of every nonexact
return, and prove the arbitrary-order local-boundary union.  Until then all
certification flags must remain false.

Reproduce the audit with

    PYTHONPATH=src python3 -B src/two_active_dormant_407_asymmetric_return_audit.py
    PYTHONPATH=src python3 -B -m unittest \
      tests/test_two_active_dormant_407_asymmetric_return_audit.py -v
