"""Standard-library package invariants shared by the builder and offline runner.

This module performs no writes on import. Paths are lexical, never resolved
through symlinks. Every existing component from the filesystem root is checked.
These are deterministic local-file guards, not a concurrent-adversary sandbox.
"""
from pathlib import Path, PurePosixPath
import hashlib
import json
import os
import re
import stat

PREFIX = 'draft_pr_actual_claims_1100_1200_20261017/audits/pr1155_30000214'
PDF = 'spherefree-doubly-cm.pdf'
SOURCE = 'spherefree-doubly-cm-source-and-verification.zip'
KIT = 'zenodo-upload-kit.zip'
HERE = Path(os.path.abspath(__file__)).parent.parent
PUBLICATION_MEMBERS = (
    'main.tex', 'README.md', 'LICENSE.txt', 'zenodo-metadata.json',
    'zenodo-deposit.json', 'build_package.py', 'output/pdf/' + PDF,
    'verification/package_common.py', 'verification/verify_all.py',
    'verification/CONTROL_PLAN.json', 'verification/AUDIT_MEMBERS.json',
    'verification/EXPECTED_FINITE_INCIDENCE.stdout.json',
    'verification/REPLAY_RECEIPT.json', 'verification/PROVENANCE.json',
    'verification/README.md', 'verification/self_test.py',
    'verification/finite_incidence_and_threshold.py',
    'verification/optional_matrix_diagnostics.py',
)


def need(condition, message):
    if not condition:
        raise ValueError(message)


def encoded(value):
    return (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + '\n').encode('utf-8')


def byte_pin(data):
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def member_name(name):
    need(isinstance(name, str) and bool(name), 'empty/nontext member name')
    path = PurePosixPath(name)
    need(bool(path.parts) and not path.is_absolute() and '..' not in path.parts,
         'absolute/parent member path: ' + name)
    need(path.as_posix() == name and not any(c in name for c in '\\:<>"|?*')
         and all(ord(c) >= 32 and ord(c) != 127 for c in name),
         'noncanonical/nonportable member path: ' + name)
    reserved = {'CON', 'PRN', 'AUX', 'NUL'} | {'COM' + str(i) for i in range(1, 10)} | {'LPT' + str(i) for i in range(1, 10)}
    need(not any(part.endswith((' ', '.')) or part.split('.')[0].upper() in reserved
                 for part in path.parts), 'nonportable member component: ' + name)
    return name


def check_chain(path):
    path = Path(path)
    need(path.is_absolute() and '..' not in path.parts, 'noncanonical filesystem path: ' + str(path))
    cursor = Path(path.anchor)
    need(not cursor.is_symlink(), 'symlink filesystem root: ' + str(cursor))
    for index, part in enumerate(path.parts[1:]):
        cursor = cursor / part
        need(not cursor.is_symlink(), 'symlink ancestor/member: ' + str(cursor))
        if index < len(path.parts) - 2:
            need(not cursor.exists() or cursor.is_dir(),
                 'ancestor is not a directory: ' + str(cursor))
    return path


def audit_root():
    check_chain(HERE)
    candidate = check_chain(HERE / PREFIX)
    if candidate.exists():
        need(candidate.is_dir(), 'embedded audit root is not a directory')
        return candidate
    return check_chain(HERE.parent)


def safe(path):
    path = Path(path)
    need(path.is_absolute() and '..' not in path.parts, 'unsafe filesystem path: ' + str(path))
    roots = (HERE, audit_root())
    need(any(path == root or root in path.parents for root in roots),
         'path outside distribution roots: ' + str(path))
    return check_chain(path)


def read(path):
    path = safe(path)
    need(path.exists() and stat.S_ISREG(path.lstat().st_mode),
         'missing/nonregular input: ' + str(path))
    return path.read_bytes()


def pin(path):
    return byte_pin(read(path))


def load(path):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            need(key not in result, 'duplicate JSON key: ' + key)
            result[key] = value
        return result
    return json.loads(read(path), object_pairs_hook=unique,
                      parse_constant=lambda value: need(False, 'nonfinite JSON constant: ' + value))


def valid_pin(value):
    return (isinstance(value, dict) and set(value) == {'bytes', 'sha256'}
            and type(value['bytes']) is int and value['bytes'] >= 0
            and isinstance(value['sha256'], str)
            and re.fullmatch('[0-9a-f]{64}', value['sha256']) is not None)


def audit_member_name(name):
    member_name(name)
    parts = PurePosixPath(name).parts
    lowered = [part.lower() for part in parts]
    excluded = {'private', 'tmp', 'temp', 'rendered', '__pycache__',
                'publication', '.git', 'source_bodies', 'third_party',
                'thirdparty', 'extracts', 'extract', 'renders', 'render', 'raw', 'raw_responses', 'text', 'texts'}
    need(not any(part in excluded for part in lowered), 'excluded audit member: ' + name)
    need(not any(re.search(r'(^|[_\-.])(logs?|gates?)([_\-.]|$)', part)
                 for part in lowered), 'log/gate audit member: ' + name)
    need(not any('final' in part and 'review' in part for part in lowered),
         'final review is outside the frozen archive: ' + name)
    need(PurePosixPath(name).suffix.lower() not in
         {'.pdf', '.html', '.htm', '.xml', '.png', '.jpg', '.jpeg', '.webp', '.gif', '.pyc', '.txt'},
         'body/render/cache extension excluded: ' + name)
    need(not any('stdout' in part or 'stderr' in part for part in lowered),
         'raw process log excluded: ' + name)
    return name


def read_allowlist():
    allowed = load(HERE / 'verification/AUDIT_MEMBERS.json')
    need(isinstance(allowed, dict) and bool(allowed), 'empty/nonobject audit allowlist')
    folded = set()
    for name, wanted in allowed.items():
        audit_member_name(name)
        need(name.casefold() not in folded, 'case-colliding audit member: ' + name)
        folded.add(name.casefold())
        need(valid_pin(wanted), 'invalid authored-member pin: ' + name)
    for required in ('root_reproduction/finite_incidence_and_threshold.py', 'ROOT_PDF_QA.json'):
        need(required in allowed, 'required authored member absent: ' + required)
    return allowed


def verify_audit(allowed):
    audit = audit_root()
    for name, wanted in sorted(allowed.items()):
        need(pin(audit / name) == wanted, 'authored member pin mismatch: ' + name)


def verify_pdf_qa():
    qa = load(audit_root() / 'ROOT_PDF_QA.json')
    need(isinstance(qa, dict) and valid_pin(qa.get('source')) and valid_pin(qa.get('pdf')),
         'invalid PDF/source QA pins')
    need(type(qa.get('pages')) is int and qa['pages'] > 0, 'invalid PDF QA page count')
    need(pin(HERE / 'main.tex') == qa['source'], 'PDF QA source mismatch')
    pdf = read(HERE / 'output/pdf' / PDF)
    need(byte_pin(pdf) == qa['pdf'] and pdf.startswith(b'%PDF-'), 'PDF QA frozen-PDF mismatch')
    return qa


def verify_manifest(allowed):
    path = safe(HERE / 'SOURCE_MANIFEST.json')
    if not path.exists():
        return
    manifest = load(path)
    expected = set(PUBLICATION_MEMBERS) | {PREFIX + '/' + name for name in allowed}
    need(isinstance(manifest, dict) and set(manifest) == expected,
         'source manifest membership mismatch')
    for name, wanted in sorted(manifest.items()):
        member_name(name)
        need(valid_pin(wanted), 'invalid source manifest pin: ' + name)
        need(pin(HERE / name) == wanted, 'source manifest pin mismatch: ' + name)


def output_path(path):
    path = safe(path)
    need(path == HERE / 'PACKAGE_RECEIPT.json'
         or path in (HERE / 'output' / SOURCE, HERE / 'output' / KIT),
         'unapproved package output: ' + str(path))
    need(not path.exists() or stat.S_ISREG(path.lstat().st_mode),
         'output destination is not a regular file: ' + str(path))
    return path
