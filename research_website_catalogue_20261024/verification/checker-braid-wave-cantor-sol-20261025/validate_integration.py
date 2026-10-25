"""Non-render checks of the owned checker extension; writes only this report folder."""
from pathlib import Path
import ast
import copy
import datetime
import difflib
import hashlib
import json
import re
import sys
import unicodedata
import warnings
import zipfile
from html import unescape

sys.dont_write_bytecode = True
OUT = Path(__file__).resolve().parent
R = OUT.parents[1]
CHECKER = R / 'verification/final-content-check.py'
IDS = {'23393596', '23358014', '23356964'}
before = (OUT / 'final-content-check.before.py').read_text()
after = CHECKER.read_text()
old_tree, new_tree = ast.parse(before), ast.parse(after)
results = {'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
           'completion_percent': 100,
           'scope': 'Non-render checker integration only. No generated/live page QA, rendering, deployment, browser, Sheet or Git action.',
           'checks': {}, 'papers': {}}


def check(name, value):
    results['checks'][name] = bool(value)


with warnings.catch_warnings(record=True) as caught:
    warnings.simplefilter('always')
    compile(after, str(CHECKER), 'exec')
check('syntax_without_warnings', not caught)


def named_assignment(tree, name):
    return next(n for n in tree.body if isinstance(n, ast.Assign)
                and any(isinstance(x, ast.Name) and x.id == name for x in n.targets))


old_paths = ast.literal_eval(named_assignment(old_tree, 'TEX_PATHS').value)
new_paths = ast.literal_eval(named_assignment(new_tree, 'TEX_PATHS').value)
check('all_original_source_paths_preserved', all(new_paths[k] == v for k, v in old_paths.items()))
check('only_three_source_paths_added', set(new_paths) - set(old_paths) == IDS)
results['registered_paths'] = {'old_count': len(old_paths), 'new_count': len(new_paths),
                              'added': {k: new_paths[k] for k in sorted(IDS)}}


def is_added_branch(node):
    if not isinstance(node, ast.If):
        return False
    condition = ast.unparse(node.test)
    return condition == 'rid in BRAID_WAVE_WREATH_IDS' or condition in {
        "rid == '" + rid + "'" for rid in IDS}


stripped = copy.deepcopy(new_tree)
paths_node = named_assignment(stripped, 'TEX_PATHS')
kept = [(k, v) for k, v in zip(paths_node.value.keys, paths_node.value.values)
        if ast.literal_eval(k) not in IDS]
paths_node.value.keys = [k for k, _ in kept]
paths_node.value.values = [v for _, v in kept]
stripped.body = [n for n in stripped.body if not (
    isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'BRAID_WAVE_WREATH_IDS' for t in n.targets)
    or isinstance(n, ast.FunctionDef) and n.name in {
        'normalized_braid_abstract', 'normalized_wave_abstract', 'normalized_wreath_abstract'})]
for node in stripped.body:
    if isinstance(node, ast.FunctionDef) and node.name == 'abstract_tokens':
        assert ast.unparse(node.body[0].test) == 'record_id in BRAID_WAVE_WREATH_IDS'
        node.body.pop(0)
    if isinstance(node, ast.For) and isinstance(node.target, ast.Name) and node.target.id == 'rid':
        node.body = [n for n in node.body if not is_added_branch(n)]
check('all_original_checker_ast_preserved', ast.dump(stripped) == ast.dump(old_tree))
(OUT / 'checker-additions.diff').write_text(''.join(difflib.unified_diff(
    before.splitlines(keepends=True), after.splitlines(keepends=True),
    fromfile='verification/final-content-check.py (before)',
    tofile='verification/final-content-check.py (after)')))


def helper_env(tree):
    env = dict(Path=Path, re=re, json=json, hashlib=hashlib, unicodedata=unicodedata,
               zipfile=zipfile, unescape=unescape)
    selected = []
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            selected.append(node)
        elif isinstance(node, ast.Assign) and all(isinstance(t, ast.Name) and t.id.isupper() for t in node.targets):
            try:
                ast.literal_eval(node.value)
            except (ValueError, TypeError):
                continue
            selected.append(node)
    exec(compile(ast.Module(body=selected, type_ignores=[]), '<checker helpers>', 'exec'), env)
    return env


old_env, new_env = helper_env(old_tree), helper_env(new_tree)
legacy_checks = {}
for rid, path in old_paths.items():
    source = (R / 'papers' / rid / 'sources' / path).read_text()
    if rid == '22089551':
        source = re.search(r'\\ifdefined\\japsubmission(.*?)\\else(.*?)\\fi', source, re.S).group(2)
    abstract = re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}', source, re.S).group(1)
    legacy_checks[rid] = old_env['abstract_tokens'](abstract, rid) == new_env['abstract_tokens'](abstract, rid)
results['legacy_abstract_dispatch'] = legacy_checks
check('every_original_abstract_dispatch_unchanged', all(legacy_checks.values()))

sys.path.insert(0, str(R / 'scripts'))
from published_assets import asset_name, normalized_receipt_view

main_loop = next(n for n in new_tree.body if isinstance(n, ast.For)
                 and isinstance(n.target, ast.Name) and n.target.id == 'rid')
added = [n for n in main_loop.body if is_added_branch(n)]
common = next(n for n in added if ast.unparse(n.test) == 'rid in BRAID_WAVE_WREATH_IDS')
forbidden = {'h', 'visible_text', 'texts', 'frames', 'art'}


class SourceOnly(ast.NodeTransformer):
    def visit_Expr(self, node):
        if isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Name) and node.value.func.id == 'test':
            names = {x.id for x in ast.walk(node.value) if isinstance(x, ast.Name)}
            if names & forbidden:
                return ast.copy_location(ast.Pass(), node)
        return self.generic_visit(node)


source_only = ast.fix_missing_locations(SourceOnly().visit(copy.deepcopy(common)))
source_code = compile(ast.Module(body=[source_only], type_ignores=[]), '<source-only added checks>', 'exec')


def run_source_checks(env):
    observed = {}
    scope = dict(env)
    scope['test'] = lambda key, value: observed.update({key: bool(value)})
    exec(source_code, scope)
    return observed


for rid in sorted(IDS):
    p = R / 'papers' / rid
    c = json.loads((p / 'publication.json').read_text())
    gate = json.loads((p / 'promotion.json').read_text())
    textpath = p / c['source_binding']['source_tex_path']
    source = textpath.read_text()
    a = re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}', source, re.S).group(1)
    raw_receipt = json.loads((p / 'sources/receipt.json').read_text())
    env = dict(new_env, R=R, p=p, c=c, gate=gate, rid=rid, source=source, a=a,
               textpath=textpath, raw_receipt=raw_receipt,
               receipt=normalized_receipt_view(raw_receipt), asset_name=asset_name,
               record=json.loads((p / 'sources/record.json').read_text())['metadata'])
    positive = run_source_checks(env)
    check(rid + '_source_checks', all(positive.values()))
    public_keys = ['title', 'description', 'abstract', 'plain_language', 'result', 'why_it_works',
                   'limitations', 'background', 'collaboration', 'ai_disclosure', 'edition_note']
    public_text = '\n'.join(json.dumps(c[k], ensure_ascii=False) if isinstance(c[k], (list, dict))
                            else c[k] for k in public_keys)
    # This confirms the planned literal assertions match approved config text;
    # it does not construct HTML or claim that text has been rendered.
    snippets = {}
    for block in added:
        if block is not common and ast.unparse(block.test) != "rid == '" + rid + "'":
            continue
        for node in ast.walk(block):
            if not (isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == 'test'):
                continue
            test_name = ast.literal_eval(node.args[0])
            expression = node.args[1]
            if not (isinstance(expression, ast.Call) and isinstance(expression.func, ast.Name)
                    and expression.func.id == 'all' and isinstance(expression.args[0], ast.GeneratorExp)):
                continue
            gen = expression.args[0]
            if ast.unparse(gen.elt) != 'x in unescape(h)':
                continue
            phrases = eval(compile(ast.Expression(gen.generators[0].iter), '<planned phrases>', 'eval'), env)
            predicate = compile(ast.Expression(expression), '<planned content predicate>', 'eval')
            snippets[test_name] = {'pass': all(x in public_text for x in phrases),
                                   'phrase_count': len(phrases),
                                   'missing': [x for x in phrases if x not in public_text],
                                   'predicate_on_config_text_passes': eval(predicate, dict(env, h=public_text)),
                                   'required_phrase_omission_rejected': not eval(predicate, dict(env, h=public_text.replace(phrases[0], '[omitted]')))}
    check(rid + '_planned_scope_snippets_match_config', all(
        x['pass'] and x['predicate_on_config_text_passes'] and x['required_phrase_omission_rejected']
        for x in snippets.values()))
    normalizer = env[{'23393596': 'normalized_braid_abstract',
                      '23358014': 'normalized_wave_abstract',
                      '23356964': 'normalized_wreath_abstract'}[rid]]
    negative = {}
    private_test = next(n.value for n in common.body if isinstance(n, ast.Expr)
                        and isinstance(n.value, ast.Call) and isinstance(n.value.func, ast.Name)
                        and n.value.func.id == 'test' and ast.literal_eval(n.value.args[0]) == 'no_private_custody_or_replay')
    private_predicate = compile(ast.Expression(private_test.args[1]), '<private-audit predicate>', 'eval')
    private_env = dict(env, visible_text=public_text.lower(), expected_clearance_sha=gate['root_clearance_sha256'])
    negative['approved_config_has_no_private_audit_story'] = eval(private_predicate, private_env)
    negative['injected_dated_audit_story_rejected'] = not eval(private_predicate,
        dict(private_env, visible_text=public_text.lower() + '\n25 october 2026: checks passed'))
    sentences = re.split(r'(?<=\.)\s+', c['abstract'])
    for label, index in [('first_sentence', 0), ('middle_sentence', len(sentences) // 2),
                         ('last_sentence', len(sentences) - 1)]:
        changed = ' '.join(x for i, x in enumerate(sentences) if i != index)
        negative[label + '_omission_rejected'] = (normalizer(a) != changed
            and new_env['abstract_tokens'](a, rid) != new_env['wt'](changed))
    old_symbol, new_symbol = {'23393596': ('m≥3', 'm>3'),
                              '23358014': ('{0}', '{1}'),
                              '23356964': ('ℤ ≀ ℤ', 'ℤ × ℤ')}[rid]
    changed = c['abstract'].replace(old_symbol, new_symbol, 1)
    negative['mathematical_symbol_change_rejected_by_full_text'] = changed != c['abstract'] and normalizer(a) != changed
    for label, mutate, required_failure in [
        ('root_clearance_hash', lambda e: e['gate'].__setitem__('root_clearance_sha256', '0' * 64), 'root_clearance_binding'),
        ('scope_status_rewrite', lambda e: e['gate']['reviews']['scope']['verdict'].__setitem__('status', 'PASS'), 'frozen_scope_chronology_preserved'),
        ('source_tex_hash', lambda e: e['c']['source_binding'].__setitem__('source_tex_sha256', '0' * 64), 'abstract_source_binding'),
        ('frozen_scope_hash', lambda e: e['c']['source_binding'].__setitem__('frozen_scope_content_sha256', '0' * 64), 'frozen_scope_candidate_binding')]:
        mutated = dict(env, gate=copy.deepcopy(gate), c=copy.deepcopy(c))
        mutate(mutated)
        negative[label + '_mutation_rejected'] = run_source_checks(mutated)[required_failure] is False
    if rid == '23358014':
        mutated = dict(env, raw_receipt=copy.deepcopy(raw_receipt))
        mutated['raw_receipt']['files'] = mutated['raw_receipt'].pop('assets')
        negative['raw_assets_schema_rewrite_rejected'] = run_source_checks(mutated)['raw_assets_receipt_preserved'] is False
    check(rid + '_negative_controls', all(negative.values()))
    results['papers'][rid] = {'source_only_checks': positive,
                             'planned_public_scope_config_coverage': snippets,
                             'negative_controls': negative,
                             'abstract': {'words': len(c['abstract'].split()),
                                          'sentences': len(sentences),
                                          'tex_sha256': hashlib.sha256(textpath.read_bytes()).hexdigest()},
                             'publication_sha256': hashlib.sha256((p / 'publication.json').read_bytes()).hexdigest(),
                             'promotion_sha256': hashlib.sha256((p / 'promotion.json').read_bytes()).hexdigest()}

baseline = json.loads((OUT / 'frozen-before.json').read_text())
changed = [name for name, sha in baseline['paper_files_sha256'].items()
           if hashlib.sha256((R / name).read_bytes()).hexdigest() != sha]
check('all_frozen_paper_and_clearance_bytes_unchanged', not changed)
results['frozen_custody'] = {'files_compared': len(baseline['paper_files_sha256']),
                            'changed': changed}
results['checker_before_sha256'] = hashlib.sha256(before.encode()).hexdigest()
results['checker_after_sha256'] = hashlib.sha256(after.encode()).hexdigest()
results['status'] = 'PASS' if all(results['checks'].values()) else 'ISSUES_FOUND'
(OUT / 'validation.json').write_text(json.dumps(results, indent=2, ensure_ascii=False) + '\n')
print(json.dumps({'status': results['status'], 'checks': results['checks'],
                  'legacy_dispatches': len(legacy_checks),
                  'source_checks': {rid: len(results['papers'][rid]['source_only_checks']) for rid in sorted(IDS)},
                  'snippet_gaps': {rid: {k: v['missing'] for k, v in results['papers'][rid]['planned_public_scope_config_coverage'].items() if v['missing']} for rid in sorted(IDS)},
                  'checker_sha256': results['checker_after_sha256'],
                  'frozen_files_compared': results['frozen_custody']['files_compared']}, ensure_ascii=False))
raise SystemExit(0 if results['status'] == 'PASS' else 1)
