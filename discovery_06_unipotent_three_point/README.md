# Discovery 06: a 14-variable unipotent map with a three-point fiber

Status: **branch draft; not peer reviewed**.

This directory gives an exact rational polynomial map

    T = identity + g : A^14 -> A^14

whose Jacobian is everywhere unipotent and which has three displayed rational
points in one fiber. Generically, \(Jg\) is a single nilpotent Jordan block of
size 14. The vector \(g\) has 24 monomials.

The same object gives a particularly strong counterexample to the Special
Image Conjecture. For

    A(xi,Z) = -sum xi_j*g_j(Z),   b=x+y+u11,

every positive power of \(A\) lies in \(\ker(E_{14})\), while \(bA^m\) lies
outside it for **every** positive exponent \(m\). The obstruction is an
explicit three-residue-class coefficient formula, not a finite computation.

Start with [NOTE.md](NOTE.md). The typeset paper is
[the rendered PDF](output/pdf/unipotent_three_point.pdf), and the exact sparse
certificate is [unipotent14_sparse.json](output/unipotent14_sparse.json).

## Verification

The primary checker uses exact SymPy arithmetic:

    ../.venv/bin/python verify_symbolic.py

Regenerate and independently check the sparse certificate with:

    ../.venv/bin/python export_certificate.py
    python3 verify_exported_stdlib.py

The expected certificate SHA-256 is

    ce6ca33b38c808a973b18da3d5f4a1f5a647c7836c2fbd78889fa7ffb3ba746c

Build the PDF with:

    python3 render_paper.py

## Scope of the size claim

The construction uses constant nilpotent state-space data

    g(X,U) = (H2(X)+B*U, -C(X)-N*U).

Eleven states, hence dimension 14, are minimal in this stated realization
ansatz; 24 monomials are also minimal there. No claim of global minimality
among all polynomial reductions is made.

## Authorship and warning

Author: Alec Kriebel, with heavy assistance from ChatGPT 5.6 Sol (OpenAI).

Alec Kriebel is a complete amateur exploring the limits of AI-assisted
mathematics and cannot independently verify the claims. The construction,
proof, and exact checkers are released for expert review. Passing the checks
does not substitute for peer review, and the priority statements are
provisional.
