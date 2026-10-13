# Independent algebra reproduction criteria

Scope: PR 411 at ac8b960bdda61c154cc30d7e3aba70389a9b139e, problem 6800014, author budget remains 2/5. No new author proof-search turns.

Hypothesis: for the five-dimensional almost-abelian bracket with A=J direct sum uE12, 0<u<1/2, the standard metric has F=Scal^2/|Ric|^2=1/3, is a local maximum among all inner products on the fixed Lie algebra, is not a solvsoliton, and has a same-group metric with larger F. I have not read the author's proof, checkers, or historical audit before writing these criteria.

Pass criteria: derive Ricci directly from the Koszul formula; compute exact first/second variations of F under conjugacy; identify all flat directions and show that they are actual symmetry or constant-F families; justify a complete local slice and a uniform transverse negative Hessian/Taylor argument (a semidefinite Hessian alone is insufficient); independently exhibit the derivation obstruction; give an exact conjugate matrix with larger F. Check endpoints u=0, u=1/2, and parameter homothety conventions. Seal this derivation/code/results before inspecting historical material. Then read all nineteen source files, verify receipt and internal hashes, reproduce each distinct checker in an isolated private copy under normal and optimized Python, and run controls that test what checker success really certifies.

Verdicts distinguish mathematical truth, original proof sufficiency, reproducibility, and checker trust-boundary behavior. Publication is restricted to a positive whitelist of original review artifacts; copied source, retrievals, environments, fixtures, raw outputs, caches, and logs are private.
