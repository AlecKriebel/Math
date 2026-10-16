# Resumption addendum to the priority comparisons

This addendum preserves `PRIOR_COMPARISON_DERIVATIONS.md`, the original checker,
its completed normal/optimized outputs and the original source-access records.
It adds a more literal classical-encoding comparison and corrects one source
author description. No submitted artifact or earlier review was modified.

## The classical union, including its exact local distinction

For each variable prime p_i, let V_i contain residues other than 0 and 1.
For a normalized clause C, let F_C contain its unique falsifying **Boolean**
residue modulo the product of its variable primes. The actual classical union is

    Bad_SM = (union_i V_i) union (union_C F_C).

The candidate's allowed clause set A_C contains the satisfying Boolean residues.
Consequently its complement also contains local non-Boolean residues. Thus
F_C is generally **not** the entire complement of A_C. Nevertheless,

    (union_i V_i) union (union_C complement(A_C)) = Bad_SM,

because every additional residue in a local clause complement is already in
some V_i. The complete allowed-predicate intersection is therefore exactly
the complement of Stockmeyer--Meyer's union, although the individual clause
languages are not pairwise complements without the variable-invalid union.
This qualification strengthens the comparison in Section 2 of the original
derivations; it changes no claim of the candidate.

The successor `check_classical_union_resume.py` implements the two sides
separately: it directly tests the unique falsifying residue for the earlier
construction, and builds the allowed sets by scanning CRT representatives of
satisfying local Boolean assignments. It compares 278 formulas and 29,190
residue positions, including clauses of length one and two, empty formulas and
inconsistent unit clauses. Its explicit three-variable clause control finds 97
non-Boolean residues that distinguish a local clause complement from the
single failed Boolean residue. Two damaged implications are rejected. Complete
normal and optimized JSON are byte-identical. These are finite diagnostics,
not a substitute for the universal set identity above.

## Source naming corrections and editions

The retained `Esparza_survey.pdf` is Javier Esparza's sole-author
*Decidability and complexity of Petri net problems -- an introduction*.
The wording "Esparza-Nielsen" in Section 6 of the original derivations should
therefore read "Esparza's survey". The other retained primary body is
Cheng--Esparza--Palsberg's *Complexity Results for 1-safe Nets*. The latter's
set-valued flow relation, unit enabling thresholds and update rule were read on
PDF page 4. No Nielsen authorship is attributed to the retained survey.

The Stockmeyer--Meyer Theorem 6.1 proof is on PDF/printed pages 7--8 of the
retained STOC 1973 preliminary report. Gramlich is the sole author of the
retained MFCS 2003 reconstruction (Fact 3, PDF pages 5--6; the title page gives
LNCS 2747, pages 460--469). The old acquisition ID `Gramlich_Schnitger` is an
opaque filename only. It is not a bibliographic assertion.

The acquisition ID `Hujsa_single_shared` is also an opaque mistaken discovery
label. Its actual retained title is *Target-oriented Petri Net Synthesis*, by
Best, Devillers, Erofeev and Wimmel. It is not the unavailable Hujsa--Devillers
weighted-net proof, and is not used to resolve that gap. Its template year on
the manuscript first page is not adopted as a verified publication date.

## Full-result and stronger-restriction implication audit

The earlier priming lemma supplies the bank multiplicities exactly. The
classical encoding supplies the variable/clause periods and their SAT meaning.
The root-last viewpoint and conserved-mass comparison also have earlier
antecedents. These facts remove any basis for asserting that the corresponding
ideas are new. A self-contained proof can and should use them with attribution.

The complete candidate theorem still requires the following checkable bridge:
q physical counters per bank; q unit outputs for every counter toppling;
distinct return vertices with outdegree one; a single ordinary root whose
outdegree is Q; nonnegative initial root mass; root stability exactly at total
bank maximum; a legal infinite checkpoint schedule in the unsatisfiable case;
least action to preclude a different halting schedule; and polynomial expansion
of only local prime products. The oriented version needs distinct return
vertices for the counter's former direct root output. None of the inspected
source statements by itself supplies that entire bridge with these graph,
configuration, conservation, strong-connectivity, chip-size and decision
restrictions. The two earlier ingredients together explain much of the proof,
but are not a source quotation of the complete restricted HALTING theorem.
This is not a proof that no earlier derivation exists.

In particular, a generalized rotor system's branching arc-state reachability
reduction cannot be restricted to ordinary halting just by declaring chip-firing
to be a VAS subclass. Sandpilization's all-input halting theorem is a different
quantifier. A lower bound for simulating a long terminating game is not a
many-one hardness proof. Optimization over additional chip distributions is not
the supplied-configuration language. The exact transfer gaps and controls are
in Sections 3--7 of the original derivations.

The original Mayr--Weihmann construction and the complete Hujsa--Devillers
weighted-net proofs remain unread. Public title/abstract/structural snippets
are discovery aids only. Their possible additional consequences, along with
unlocated older work, keep full-result, realization and oriented-strengthening
priority **UNKNOWN**. The report accordingly supports a credited complete
proof with explicit audit limits, without worldwide openness or firstness.
