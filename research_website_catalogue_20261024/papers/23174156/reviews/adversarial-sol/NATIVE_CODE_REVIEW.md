# Full-weight native route: static audit and one literal failed attempt

The complete current verification/verify.py was personally read before any execution, as were its literal constants and its only local file input, the packaged pr95_note.tex (identical to the already read controlling native TeX). Program pin:2895 bytes, SHA2562cccb1fb0178cf4dca63a85a26d95fd3bf629578fd53cdb7d7711e93aaa3285e. It imports NumPy plus the Python standard library; there are no local module imports, input parameters, network operations or source writes. It writes verification.json only in its current directory and prints a short result. No archived output, deliberately false input, run_all.py, optimized run, second checker or altered copy was run.

## Static mathematical mapping

For each label lambda=(a1,a2,a3,a4), ai>=0, sum<=5, the code forms y_i=sum_(j>=i) a_j+4-i and x_i=5y_i-sum(y). This is5(lambda+rho) in centered Euclidean coordinates. All126 labels are included; zero is first. Each of120 permutations has its inversion parity computed directly. The matrix numerator is

    N(x,y)=sum_w det(w) zeta_100^[-2 (x.wy/5)],

which is sum_w det(w) exp[-2pi i (lambda+rho,w(mu+rho))/10]. The integer divisibility guard is correct because all x coordinates share one residue mod5 and sum to zero. Symmetry permits exactly8001 entries. The actual normalized matrix is cN, c=-1/(100sqrt5); the stored arrays are Weyl numerators, not an assertion that the normalized vacuum scalar is an algebraic integer.

The twist exponent [(|x|^2-|x0|^2)/5] in zeta_100 gives exp[pi i (|lambda+rho|^2-|rho|^2)/10]. The exact convolutions use NumPy object arrays, initialized with Python integer entries, not fixed-width machine integers or floating arithmetic. Reduction x^40=x^30-x^20+x^10-1 is implemented by the four descending offsets10,20,30,40 with signs+,-,+,-. The omitted final high coefficients are no longer used by the descending algorithm. Conjugation uses zeta^j -> zeta^(-j mod100). Phi_100 is the actual cyclotomic polynomial of the specified complex root, so reduction/equality are exact in that chosen field.

The two contractions are A=N theta^5 N and B=N theta^3 N theta^2 N, at the vacuum entry. They are the appropriate words for the negative continued fractions [5] and [3,2], up to the conjugation/framing conventions already controlled by the proof and primary interface. Writing DD=|N00|^2, AA=|A|^2, BB=|B|^2, normalized squared magnitudes would be

    h1=AA/(50000 DD),  h2=BB/(50000^2 DD),

because c^2=1/50000 and each word is divided by the same s=cN00 exactly once. Thus comparing50000 AA with BB correctly compares h1 with h2; the unequal number of S factors has NOT been lost. This is the important full-weight normalization falsification target. The code keeps these factors separate rather than pretending both contractions share the same scalar.

Seven polynomial targets are enforced by explicit require/raise guards. Cardinalities and nonvanishing are also guarded. The literal targets translate, using zeta^20-zeta^30=(sqrt5-1)/2, to

    DD=225-100sqrt5,
    AA=343750000+62500000sqrt5,
    BB=14062500000000+6250000000000sqrt5,
    50000 AA-BB=3125000000000(1-sqrt5).

If those targets are actually produced, the normalized values equal the hand-derived paper values. Merely reading these expected constants does not demonstrate that the program computed them. No native execution success or polynomial output is claimed here.

## Actual ordinary invocation

The small owned custody wrapper run_native_once.py was read in full before its sole execution. It verifies all186 source files and18 child directories, source terminal pins, modes and exact extent before/after; it then invokes the unchanged native program once with the inherited existing Python environment and an owned native-run working directory. It does not import/run any other original code or change any mathematical input.

At2026-11-16T22:16:42Z, the native child exited1 after about0.04 seconds at its line3 import. Literal stderr:

    Traceback (most recent call last):
      File "/Users/alec/Documents/Math/research_website_catalogue_20261024/papers/23174156/sources/published-source/container-001/tree/verification/verify.py", line 3, in <module>
        import numpy as np,itertools,json,hashlib
    ModuleNotFoundError: No module named 'numpy'

stdout is exactly0 bytes; stderr is302 bytes. No verification.json or arithmetic artifact exists from this attempt. native-run/RECEIPT.json,3361 bytes, SHA256ae6033e0347ddfe7c838fba03da8b97b9645bcec581ebd217a589f66da496572, retains argv, Python3.14.6 identity, exit, elapsed time, program/input pins, streams and matching complete source guards. The wrapper's own exit0 reports successful custody capture, not successful arithmetic. No dependency was installed and no alternative environment, retry or replacement checker was used.

This is a transparent finite-reproduction limitation. It does not disprove the exact proof, whose exhaustive character reduction and five surviving Weyl terms have independent hand derivations frozen before this code was opened. The native program supplies no fresh successful computational evidence in this review. Historical assertions about prior optimized/false-target campaigns remain author assertions, not current reproduced results or additional independent proof.
