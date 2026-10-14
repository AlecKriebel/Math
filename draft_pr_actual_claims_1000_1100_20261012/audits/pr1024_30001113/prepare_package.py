"""Assemble authored portable evidence; never alter the submitted snapshot."""
import ast
import hashlib
import json
import pathlib
import shutil

ROOT = pathlib.Path(__file__).resolve().parent
PUB = ROOT / 'publication'


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')


def main():
    for name in ('checks/current', 'expected', 'evidence'):
        (PUB / name).mkdir(parents=True, exist_ok=True)
    for name in ('check_conjugacy.py', 'verify_exact.py'):
        shutil.copyfile(ROOT / 'submitted/current' / name,
                        PUB / 'checks/current' / name)
    shutil.copyfile(ROOT / 'submitted/check_corrected_case.py',
                    PUB / 'checks/check_corrected_case.py')
    shutil.copyfile(ROOT / 'submitted/FINITE_CONTRACT.json',
                    PUB / 'expected/FINITE_CONTRACT.json')

    original = ROOT / 'reviews/functor_01/verify_functor_identities.py'
    tree = ast.parse(original.read_text())
    guards = []

    class ExplicitGuards(ast.NodeTransformer):
        def visit_Assert(self, node):
            if node.msg is not None:
                raise RuntimeError('unexpected assertion message')
            guards.append({'original_line': node.lineno,
                           'test_ast': ast.dump(node.test, include_attributes=False),
                           'test_source': ast.unparse(node.test)})
            return ast.copy_location(ast.Expr(ast.Call(
                func=ast.Name(id='require', ctx=ast.Load()),
                args=[node.test, ast.Constant('original assertion at line ' + str(node.lineno))],
                keywords=[])), node)

    tree = ExplicitGuards().visit(tree)
    if len(guards) != 11:
        raise RuntimeError('expected all 11 original assertions')
    require = ast.parse('def require(test, message):\n    if not test:\n        raise RuntimeError(message)\n').body[0]
    # Keep the module docstring and imports, insert the guard before arithmetic.
    tree.body.insert(3, require)
    ast.fix_missing_locations(tree)
    adapted = PUB / 'checks/verify_functor_identities_explicit_guards.py'
    adapted.write_text('# Guard adaptation; original independent source is retained in evidence.\n' +
                       ast.unparse(tree) + '\n')
    adapted_tests = [ast.dump(node.args[0], include_attributes=False)
                     for node in ast.walk(ast.parse(adapted.read_text()))
                     if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
                     and node.func.id == 'require']
    if adapted_tests != [g['test_ast'] for g in guards]:
        raise RuntimeError('arithmetic assertion predicates changed')
    write_json(PUB / 'evidence/GUARD_ADAPTATION.json', {
        'original': 'functor_review_01/verify_functor_identities.py',
        'original_sha256': hashlib.sha256(original.read_bytes()).hexdigest(),
        'adapted': '../checks/verify_functor_identities_explicit_guards.py',
        'adapted_sha256': hashlib.sha256(adapted.read_bytes()).hexdigest(),
        'all_11_test_asts_identical': True,
        'changes': 'Replace Assert with explicit RuntimeError guard; AST unparse and guard definition only.',
        'guards': guards,
        'scope': 'Finite arithmetic corroboration, not an all-natural-map or formal-series proof.'})
    shutil.copyfile(ROOT / 'reviews/functor_01/CHECKS.json',
                    PUB / 'expected/verify_functor_identities.json')
    write_json(PUB / 'expected/INDEPENDENT_CONTROLS.json', {
        'missing_parameter_shift': 'original assertion at line ' + str(guards[1]['original_line']),
        'fixed_ring_identity': 'original assertion at line ' + str(guards[5]['original_line'])})

    # Only authored records; no third-party PDF/text/image source bodies.
    targets = {
        ROOT / 'submitted': PUB / 'evidence/submitted',
        ROOT / 'root_reproduction': PUB / 'evidence/root_reproduction',
        ROOT / 'reviews/formal_series_01': PUB / 'evidence/formal_series_review_01',
        ROOT / 'reviews/functor_01': PUB / 'evidence/functor_review_01',
        ROOT / 'reviews/priority_01': PUB / 'evidence/priority_review_01',
    }
    for source, destination in targets.items():
        destination.mkdir(parents=True, exist_ok=True)
        for path in sorted(source.rglob('*')):
            if path.is_file() and 'sources' not in path.relative_to(source).parts:
                target = destination / path.relative_to(source)
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(path, target)
    shutil.copyfile(ROOT / 'SUBMITTED_PINS.json', PUB / 'evidence/SUBMITTED_PINS.json')
    shutil.copyfile(ROOT / 'sources/SOURCE_RETRIEVAL.json',
                    PUB / 'evidence/ROOT_SOURCE_RETRIEVAL.json')
    write_json(PUB / 'evidence/CURRENT_REVIEW_STATE.json', {
        'mathematics': 'two fresh independent families passed; universal claims proved in text',
        'priority': 'bounded audit with mandatory prior attribution adopted',
        'fresh_whole_package_reviews': [],
        'actionable_concerns': 'whole-package reviews pending',
        'preprint_ready': False,
        'published': False,
        'historical_stage_files_unchanged': True})
    metadata = {
        'title': 'A characteristic-two counterexample to dévissage for local deformation functors',
        'upload_type': 'publication', 'publication_type': 'preprint',
        'description': '<p>A negative answer to Byszewski’s unrestricted fibre-product question for local deformation functors (Oberwolfach Report 54/2008, p.3039; 2009 thesis Question 6.4.4; arXiv:1112.0352v1, Question 4.4). For the weakly ramified additive F4 action t → t/(1+at) and its F2 subgroup, restriction–induction cannot factor formally smoothly over any prorepresentable recipient, regardless of tangent dimension. The proof uses actual unframed deformation classes, with nilpotent constant coordinate changes allowed, and an exact zero-kernel tangent restriction calculation. The variant imposing prorepresentability of the subgroup and quotient deformation functors remains unaddressed.</p><p>The additive action, involution parameter-shift conjugacy and tangent-cohomology framework are established prior ingredients. Recipient tangent collapse is credited as an elementary consequence of Byszewski–Cornelissen (2009), Proposition 6.1, with the direct matrix calculation of Proposition 4.1 reproduced. The contribution is combining these ingredients to exclude the proposed unrestricted factorization. A bounded priority audit located no matching negative assertion in inspected primary bodies; it does not certify exhaustive originality or continued openness through 2026.</p><p>The deposit includes the proof, TeX source, source/priority supplement, authored independent adversarial reviews and portable exact arithmetic verification (Python 3.10 or later; standard library only). Finite diagnostics support identities and selected controls; the written proof supplies full formal-series and arbitrary-natural-map claims. AI tools were used extensively in solving, verifying, source auditing and preparation. This is an unrefereed preprint with AI adversarial reviews; no formal proof-assistant certificate, conventional human peer review or journal acceptance is claimed.</p>',
        'creators': [{'name': 'Kriebel, Alec', 'affiliation': 'Independent researcher',
                      'orcid': '0009-0001-9320-500X'}],
        'access_right': 'open', 'license': 'cc-by-4.0',
        'publication_date': '2026-10-12', 'version': '1.0', 'language': 'eng',
        'keywords': ['local deformation functors', 'equivariant deformation theory',
                     'weak ramification', 'characteristic two', 'Klein four group',
                     'formal smoothness', 'restriction and induction', 'counterexample',
                     'exact verification', 'unrefereed preprint'],
        'references': [
            'J. Byszewski, Dévissage for local deformation functors, Oberwolfach Reports 54/2008, 3038–3040.',
            'J. Byszewski, Cohomological aspects of equivariant deformation theory, Ph.D. thesis, Utrecht University (2009), Question 6.4.4. https://dspace.library.uu.nl/handle/1874/33749',
            'J. Byszewski, Deformation functors of local actions, arXiv:1112.0352v1 (2011).',
            'J. Byszewski and G. Cornelissen, Which weakly ramified group actions admit a universal formal deformation?, Ann. Inst. Fourier 59 (2009), 877–902. DOI: 10.5802/aif.2450. Propositions 4.1 and 6.1.']}
    write_json(PUB / 'metadata.json', metadata)


if __name__ == '__main__':
    main()
