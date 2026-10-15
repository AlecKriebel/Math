# Reproduction

From this directory run:

    python check_candidate.py
    python encode_system.py 1 1

Compare output byte-for-byte with check_receipt.json and example_system.json,
respectively. Python 3 and installed SymPy 1.14.0 are used. There is no
external downloaded executable, simulation, numerical optimizer, or CAD/QE
solver call. The generator's 50,000-node output safeguard is only a software
safety limit; the theorem's explicit finite bound has no such restriction.

The first command passes 16,697 exact assertions. It checks conditional
Carathéodory reductions of concrete two/three-date models, all retained
martingale/reference constraints and q expectations, the generator's
quadratic equations, the positive-part encoding, full eight-ary witnesses,
and the exact boundary example. The generated two-date, one-call-per-date
system has 21 nodes, 102 existential variables and 219 predicates before
input conditions. General quantifier elimination is a cited classical
algorithmic theorem, not a computation performed here.

Verify the full artifact manifest and separately pinned primary reading
files. Reading PDFs/XML stay local; only the source metadata, mathematical
proof, code and receipts belong in the public research checkpoint.
