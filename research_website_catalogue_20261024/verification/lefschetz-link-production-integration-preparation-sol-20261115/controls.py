"""Bounded static and in-memory controls only; never invoke Git or the installer."""
import sys
sys.dont_write_bytecode = True
import ast
import copy
import hashlib
import importlib.machinery
import importlib.util
import json
import struct
from pathlib import Path
from exact11_lib import O, BASE, need, parse_index, adoption_fields, safe_rel


def main():
    results = []

    def rejected(label, action):
        try:
            action()
        except (RuntimeError, ValueError, struct.error):
            results.append({'control': label, 'rejected': True})
        else:
            raise RuntimeError('missed control: ' + label)

    for name in ['exact11_lib.py', 'preflight.py', 'install_exact.py', 'controls.py', 'verify_preparation.py']:
        ast.parse((O / name).read_text())
    installer = ast.parse((O / 'install_exact.py').read_text())
    main_body = next(n for n in installer.body if isinstance(n, ast.FunctionDef) and n.name == 'main').body
    gate = next(i for i, n in enumerate(main_body) if isinstance(n, ast.Assign)
                and isinstance(n.value, ast.Call) and getattr(n.value.func, 'id', '') == 'root_adoption')
    dispatch = next(i for i, n in enumerate(main_body) if isinstance(n, ast.If))
    need(gate < dispatch, 'root adoption gate before mutation dispatch')
    tree = ast.parse((O / 'exact11_lib.py').read_text())
    # Only imports, literal/path assignments, and function definitions occur at library top level.
    need(not any(isinstance(n, (ast.With, ast.For, ast.While, ast.If, ast.Expr))
                 and not (isinstance(n, ast.Expr) and isinstance(n.value, ast.Constant)) for n in tree.body),
         'inert library top level')
    template = json.loads((O / 'ROOT_ADOPTION_TEMPLATE.json').read_bytes())
    rejected('false-authority preparation template', lambda: adoption_fields(template))
    valid = copy.deepcopy(template)
    valid['template_not_root_receipt'] = False
    flags = ['root_stage_adopted', 'independent_code_audit_adopted',
             'complete_current_helper_and_rendered_output_adopted', 'production_install_authorized']
    for key in flags:
        valid[key] = True
    adoption_fields(valid)  # Memory-only field fixture; no receipt or authority is created.
    for key in flags:
        bad = copy.deepcopy(valid); bad[key] = 1
        rejected('integer is not explicit boolean authority: ' + key, lambda bad=bad: adoption_fields(bad))
    bad = copy.deepcopy(valid); bad['commit_message'] = 'x\0y'
    rejected('invalid message rejected before mutation', lambda: adoption_fields(bad))
    for text in ['../public/file', '/public/file', 'research/../file', 'research\\file']:
        rejected('path escape ' + text, lambda text=text: safe_rel(text))

    raw = (O / 'private/shared-index.before').read_bytes()
    overlay = json.loads((O.parents[0] / 'lefschetz-link-private-stage-sol-20261115/OVERLAY_MANIFEST.json').read_bytes())['files']
    targets = {('public/' + r['path']).encode() for r in overlay}
    parsed = parse_index(raw, targets)
    need(parsed['count'] == json.loads((O / 'PREFLIGHT_CAPTURE.json').read_bytes())['Git']['index_record_count'],
         'actual fresh index extent, no inherited count')
    bad = bytearray(raw); bad[-1] ^= 1
    rejected('whole index checksum corruption', lambda: parse_index(bytes(bad), targets))

    def changed(offset, value):
        bad = bytearray(raw); bad[offset:offset + len(value)] = value
        bad[-20:] = hashlib.sha1(bad[:-20]).digest()
        return bytes(bad)

    rejected('unsupported v3 index', lambda: parse_index(changed(4, struct.pack('>I', 3)), targets))
    rejected('unmerged flags', lambda: parse_index(changed(72, b'\x10\x00'), targets))
    first_path = parsed['entries'][0][0]
    path_start = 12 + 62
    end = path_start + len(first_path)
    rejected('nonzero native padding', lambda: parse_index(changed(end, b'X'), targets))
    protected_path, protected_record = parsed['protected'][0]
    start = raw.find(protected_record)
    need(start >= 12 and raw.count(protected_record) == 1, 'unique actual protected raw record')
    for offset, label in [(0, 'stat bytes'), (24, 'mode'), (40, 'object identity')]:
        bad = bytearray(raw); bad[start + offset] ^= 1
        bad[-20:] = hashlib.sha1(bad[:-20]).digest()
        try:
            altered = parse_index(bytes(bad), targets)
        except RuntimeError:
            results.append({'control': 'protected raw ' + label, 'rejected': True})
        else:
            need(altered['protected'] != parsed['protected'], 'raw preservation fence detects ' + label)
            results.append({'control': 'protected raw ' + label, 'rejected': True})

    loader = importlib.machinery.SourceFileLoader('exact11_memory_hook', str(O / 'hooks/pre-push'))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    hook = importlib.util.module_from_spec(spec); loader.exec_module(hook)
    commit = 'a' * 40; url = 'memory://explicit-origin'
    args = ['pre-push', 'origin', url]
    environment = {'EXACT11_APPROVED_COMMIT': commit,
                   'EXACT11_APPROVED_PUSH_URL_SHA256': hashlib.sha256(url.encode()).hexdigest()}
    body = (commit + ' ' + commit + ' refs/heads/master ' + BASE + '\n').encode()
    need(hook.accepted(args, environment, body), 'positive pure actual-advertisement fixture')
    bad_bodies = [b'', body + body, body.replace(BASE.encode(), b'b' * 40),
                  body.replace(b'refs/heads/master', b'refs/heads/other'),
                  body.replace(commit.encode(), b'c' * 40),
                  b'(delete) ' + commit.encode() + b' refs/heads/master ' + BASE.encode() + b'\n']
    for i, bad in enumerate(bad_bodies):
        need(not hook.accepted(args, environment, bad), 'advertisement control ' + str(i))
        results.append({'control': 'actual advertisement ' + str(i), 'rejected': True})
    need(not hook.accepted(['pre-push', 'other', url], environment, body)
         and not hook.accepted(['pre-push', 'origin', url + '/other'], environment, body),
         'wrong remote name or actual push URL rejected')
    print(json.dumps({'status': 'PASS_STATIC_AND_MEMORY_ONLY_CONTROLS', 'controls': results,
                      'false_authority_dictionaries_only_in_memory': True, 'Git_or_installer_executed': False,
                      'network_subprocess_or_writes': False}, indent=2))


if __name__ == '__main__':
    main()
