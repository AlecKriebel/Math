"""Build owned copies only; never mutate shared scripts, configs or public site."""
from pathlib import Path
import ast
import copy
import datetime
import difflib
import hashlib
import json
import re
import unicodedata
import warnings

O = Path(__file__).resolve().parent
R = O.parents[1]
LIVE = Path('/Users/alec/Desktop/alec-dev/aleckriebel.com/public')
STAGE = O / 'public'
RID = '23306332'
TEX = 'published-source/nonunique_nearest_stable_complex_quadratics_verification/nonunique_nearest_stable_complex_quadratics_verification/nonunique_nearest_stable_complex_quadratics.tex'


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def fresh(path, text):
    with path.open('x') as stream:
        stream.write(text)


def once(text, old, new):
    assert text.count(old) == 1, old
    return text.replace(old, new, 1)


old_renderer = (O / 'inputs/render_page.before.py').read_text()
renderer = once(old_renderer, 'ROOT = Path(__file__).resolve().parents[1]', 'ROOT = Path(' + repr(str(R)) + ')')
renderer = once(renderer, "SITE = Path('/Users/alec/Desktop/alec-dev/aleckriebel.com/public/research')", 'SITE = Path(' + repr(str(STAGE / 'research')) + ')')
fresh(O / 'render_page.stage.py', renderer)
fresh(O / 'renderer-staging-overrides.diff', ''.join(difflib.unified_diff(
    old_renderer.splitlines(keepends=True), renderer.splitlines(keepends=True),
    fromfile='scripts/render_page.py (unchanged original)', tofile='owned render_page.stage.py')))
old = (O / 'inputs/final-content-check.before.py').read_text()
proposed = once(old, " '23356964':'published-source/generic-wreath-hyperfiniteness-verification/note.tex',\n", " '23356964':'published-source/generic-wreath-hyperfiniteness-verification/note.tex',\n '23306332':" + repr(TEX) + ',\n')
proposed = once(proposed, "BRAID_WAVE_WREATH_IDS=", "def normalized_quadratic_abstract(body):\n return ' '.join(body.replace('$z^2$','z²').split())\nBRAID_WAVE_WREATH_IDS=")
proposed = once(proposed, 'def abstract_tokens(tex,record_id=None):\n', "def abstract_tokens(tex,record_id=None):\n if record_id=='23306332':return wt(normalized_quadratic_abstract(tex))\n")
proposed = once(proposed, " record=json.loads((p/'sources/record.json').read_text())['metadata'];test('record_metadata',", " record_file=p/'sources'/('metadata.json' if rid=='23306332' else 'record.json')\n record=json.loads(record_file.read_text())['metadata'];test('record_metadata',")
proposed = once(proposed, " result['papers'][rid]={'checks':checks,", (O / 'quadratic-checks.block.txt').read_text() + " result['papers'][rid]={'checks':checks,")
fresh(O / 'final-content-check.proposed.py', proposed)
fresh(O / 'proposed-shared-checker.diff', ''.join(difflib.unified_diff(
    old.splitlines(keepends=True), proposed.splitlines(keepends=True),
    fromfile='a/verification/final-content-check.py', tofile='b/verification/final-content-check.py')))

# These infrastructure adaptations are private to the staging execution.
stage_checker = once(proposed, "sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts'))", 'sys.path.insert(0, ' + repr(str(R / 'scripts')) + ')')
stage_checker = once(stage_checker, 'R=Path(__file__).resolve().parents[1]', 'R=Path(' + repr(str(R)) + ')')
stage_checker = once(stage_checker, '\n   good=q.is_file()\n', "\n   if not q.is_file() and u.path in ('/','/blog/','/favicon.ico'):\n    q=Path(" + repr(str(LIVE)) + ")/unquote(u.path).lstrip('/')\n    if q.is_dir():q=q/'index.html'\n   good=q.is_file()\n")
fresh(O / 'final-content-check.stage.py', stage_checker)
fresh(O / 'checker-staging-overrides.diff', ''.join(difflib.unified_diff(
    proposed.splitlines(keepends=True), stage_checker.splitlines(keepends=True),
    fromfile='proposed production checker', tofile='owned stage checker')))

before_tree, proposed_tree = ast.parse(old), ast.parse(proposed)


def named_assignment(tree, name):
    return next(n for n in tree.body if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == name for t in n.targets))


old_paths = ast.literal_eval(named_assignment(before_tree, 'TEX_PATHS').value)
new_paths = ast.literal_eval(named_assignment(proposed_tree, 'TEX_PATHS').value)
assert len(old_paths) == 46 and set(new_paths) - set(old_paths) == {RID}
assert all(new_paths[k] == v for k, v in old_paths.items())
restored = copy.deepcopy(proposed_tree)
paths = named_assignment(restored, 'TEX_PATHS').value
pairs = [(k, v) for k, v in zip(paths.keys, paths.values) if ast.literal_eval(k) != RID]
paths.keys, paths.values = [k for k, _ in pairs], [v for _, v in pairs]
restored.body = [n for n in restored.body if not (isinstance(n, ast.FunctionDef) and n.name == 'normalized_quadratic_abstract')]


class RestoreLegacyMetadataRead(ast.NodeTransformer):
    def visit_Name(self, node):
        if node.id == 'record_file':
            return ast.copy_location(ast.parse("p/'sources/record.json'", mode='eval').body, node)
        return node


for node in restored.body:
    if isinstance(node, ast.FunctionDef) and node.name == 'abstract_tokens':
        assert ast.unparse(node.body[0].test) == "record_id == '23306332'"
        node.body.pop(0)
    if isinstance(node, ast.For) and isinstance(node.target, ast.Name) and node.target.id == 'rid':
        node.body = [x for x in node.body if not (
            isinstance(x, ast.If) and ast.unparse(x.test) == "rid == '23306332'"
            or isinstance(x, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'record_file' for t in x.targets))]
        RestoreLegacyMetadataRead().visit(node)
assert ast.dump(restored) == ast.dump(before_tree)

# The renderer copy differs in exactly its ROOT and SITE assignments.
renderer_tree = ast.parse(renderer)
for name in ['ROOT', 'SITE']:
    named_assignment(renderer_tree, name).value = copy.deepcopy(named_assignment(ast.parse(old_renderer), name).value)
assert ast.dump(renderer_tree) == ast.dump(ast.parse(old_renderer))


def helper_env(tree):
    env = dict(Path=Path, re=re, unicodedata=unicodedata)
    nodes = []
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            nodes.append(node)
        elif isinstance(node, ast.Assign) and all(isinstance(t, ast.Name) and t.id.isupper() for t in node.targets):
            try:
                ast.literal_eval(node.value)
            except (ValueError, TypeError):
                continue
            nodes.append(node)
    exec(compile(ast.Module(body=nodes, type_ignores=[]), '<checker pure helpers>', 'exec'), env)
    return env


before_env, proposed_env = helper_env(before_tree), helper_env(proposed_tree)
legacy = {}
for rid, path in old_paths.items():
    source = (R / 'papers' / rid / 'sources' / path).read_text()
    if rid == '22089551':
        source = re.search(r'\\ifdefined\\japsubmission(.*?)\\else(.*?)\\fi', source, re.S).group(2)
    abstract = re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}', source, re.S).group(1)
    legacy[rid] = before_env['abstract_tokens'](abstract, rid) == proposed_env['abstract_tokens'](abstract, rid)
assert all(legacy.values())
warning_messages = []
for name in ['render_page.stage.py', 'final-content-check.proposed.py', 'final-content-check.stage.py']:
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter('always')
        compile((O / name).read_text(), str(O / name), 'exec')
        warning_messages.extend(str(x.message) for x in caught)
assert not warning_messages
shell = {str(LIVE / rel): {'bytes': (LIVE / rel).stat().st_size, 'sha256': sha(LIVE / rel)}
         for rel in ['index.html', 'blog/index.html', 'favicon.ico']}
fresh(O / 'shell-inputs-before.json', json.dumps(shell, indent=2) + '\n')
report = {'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'completion_percent': 35,
          'status': 'PASS', 'old_mappings': 46, 'new_mappings': 47,
          'only_new_mapping': {RID: TEX}, 'all_original_mappings_preserved': True,
          'all_original_checker_ast_preserved_after_removing_new_branch_and_reversing_narrow_metadata_adapter': True,
          'metadata_adapter_changes_only_23306332_path': True,
          'all_46_legacy_abstract_dispatches_unchanged': legacy,
          'renderer_copy_changes_only_ROOT_and_SITE': True,
          'syntax_warnings': warning_messages, 'shared_checker_sha256': sha(R / 'verification/final-content-check.py'),
          'proposal_sha256': sha(O / 'final-content-check.proposed.py'),
          'stage_checker_sha256': sha(O / 'final-content-check.stage.py'),
          'production_patch_sha256': sha(O / 'proposed-shared-checker.diff'),
          'staging_link_policy': 'Only missing homepage/blog/favicon shell dependencies use original public tree read-only; target page/assets, research index/CSS and sitemap/robots must resolve in owned staging.'}
fresh(O / 'integration-static-checks.json', json.dumps(report, indent=2) + '\n')
print(json.dumps({'status': 'PASS', 'old_mappings_preserved': 46,
                  'legacy_abstract_dispatches_unchanged': len(legacy),
                  'proposal_sha256': report['proposal_sha256'], 'syntax_warnings': []}))
