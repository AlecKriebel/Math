#!/usr/bin/env python3
"""Actual command controls on disposable extractions, never the candidate."""
import datetime, hashlib, json, os, shutil, subprocess, tempfile, zipfile
from pathlib import Path

REVIEW = Path(__file__).resolve().parent
CANDIDATE = REVIEW.parents[1] / 'NEWpreprint_v1_0'
CANONICAL_ZIP = CANDIDATE / 'PR1071_preprint_v1_0_support.zip'
ROWS = []

def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def require(c, message):
    if not c:
        raise RuntimeError(message)

def refresh(root, names):
    p = root/'PACKAGE_MANIFEST.json'
    obj = json.loads(p.read_text())
    for row in obj['members']:
        if row['path'] in names:
            src = root/row['path']
            row['bytes'] = src.stat().st_size
            row['sha256'] = digest(src)
    p.write_text(json.dumps(obj, indent=2)+'\n')

def invocation(root, flags, tail):
    cp = subprocess.run(['python3', '-B', *flags, *tail], cwd=root,
                        text=True, capture_output=True, timeout=120)
    return {'argv': ['python3', '-B', *flags, *tail], 'cwd': str(root),
            'returncode': cp.returncode, 'stdout': cp.stdout, 'stderr': cp.stderr}

def case(label, flags, prepare, tail, expected_pass, target=None, expected_mutation=None):
    with tempfile.TemporaryDirectory(prefix='control-', dir=REVIEW/'scratch') as temp:
        workspace = Path(temp)
        root = workspace/'clean'
        with zipfile.ZipFile(CANONICAL_ZIP) as z:
            z.extractall(root)
        output = workspace/'output'
        output.mkdir()
        chosen = prepare(root, output, workspace)
        member = root/target if target else None
        before = digest(member) if member else None
        row = invocation(root, flags, tail(root, output, workspace, chosen))
        row.update({'control': label, 'mode': 'optimized' if flags else 'normal',
                    'expected_pass': expected_pass, 'outcome_as_predicted': (row['returncode'] == 0) == expected_pass})
        require(row['outcome_as_predicted'], label+' unexpected return code')
        if member:
            after = digest(member)
            row.update({'protected_input': target, 'before_sha256': before,
                        'after_sha256': after, 'input_bytes_changed': before != after,
                        'after_bytes': member.stat().st_size,
                        'expected_input_mutation': expected_mutation})
            require((before != after) == expected_mutation, label+' unexpected input preservation')
        ROWS.append(row)

def noop(root, output, workspace):
    return None

def archive_nested(root, output, workspace):
    return root/'custody/ROOT_MATH_AUDIT.md'

def archive_symlink(root, output, workspace):
    p = output/'alias.zip'
    p.symlink_to(root/'custody/ROOT_MATH_AUDIT.md')
    return p

def archive_hardlink(root, output, workspace):
    p = output/'alias.zip'
    os.link(root/'custody/ROOT_MATH_AUDIT.md', p)
    return p

def archive_root_alias(root, output, workspace):
    p = output/'alias.zip'
    p.symlink_to(root/'paper.tex')
    return p

def check_stdout_alias(root, output, workspace):
    (output/'normal').mkdir()
    os.link(root/'metadata.json', output/'normal/stdout.txt')
    return output

def check_receipt_alias(root, output, workspace):
    (output/'CHECK_RECEIPT.json').symlink_to(root/'metadata.json')
    return output

def pdf_tex_alias(root, output, workspace):
    os.link(root/'metadata.json', output/'paper.tex')
    return output

def pdf_log_alias(root, output, workspace):
    (output/'compile.stdout.txt').symlink_to(root/'metadata.json')
    return output

def manifest_symlink(root, output, workspace):
    dst = workspace/'identical_manifest.json'
    shutil.move(root/'PACKAGE_MANIFEST.json', dst)
    (root/'PACKAGE_MANIFEST.json').symlink_to(dst)
    return None

def leaf_symlink(root, output, workspace):
    dst = workspace/'identical_paper.tex'
    shutil.move(root/'paper.tex', dst)
    (root/'paper.tex').symlink_to(dst)
    return None

def ancestors_within_root(root, output, workspace):
    shutil.move(root/'custody/reviews', root/'custody/real_reviews')
    (root/'custody/reviews').symlink_to(root/'custody/real_reviews')
    return None

def broken_member(root, output, workspace):
    with (root/'paper.tex').open('a') as f:
        f.write('\n% deliberate byte corruption\n')
    return None

def changed_metadata(field, value):
    def prepare(root, output, workspace):
        for filename in ['metadata.json', 'metadata_wrapped.json', 'deposit.json']:
            p = root/filename
            obj = json.loads(p.read_text())
            metadata = obj if filename == 'metadata.json' else obj['metadata']
            if field == 'orcid':
                metadata['creators'][0]['orcid'] = value
            else:
                metadata[field] = value
            p.write_text(json.dumps(obj, indent=2)+'\n')
        refresh(root, ['metadata.json', 'metadata_wrapped.json', 'deposit.json'])
        return None
    return prepare

def promoted_status(root, output, workspace):
    p = root/'STATUS.json'
    x = json.loads(p.read_text())
    x['publication_ready'] = x['issues_resolved'] = True
    p.write_text(json.dumps(x, indent=2)+'\n')
    refresh(root, ['STATUS.json'])
    return None

def changed_custody(root, output, workspace):
    p = root/'custody/submitted/PROOF.md'
    p.write_text(p.read_text()+'\nDeliberate changed historical copy.\n')
    refresh(root, ['custody/submitted/PROOF.md'])
    return None

def source_fault(root, output, workspace):
    p = root/'paper.tex'
    before = p.read_text()
    after = before.replace(r'\overline{\widehat h(\xi)}', r'\widehat h(\xi)')
    require(before != after, 'control did not remove conjugation')
    p.write_text(after)
    refresh(root, ['paper.tex'])
    return output

def binding_fault(kind):
    def prepare(root, output, workspace):
        obj = json.loads((CANDIDATE/'UPLOAD_BINDINGS.json').read_text())
        archive = workspace/'bound.zip'
        archive.write_bytes(CANONICAL_ZIP.read_bytes())
        if kind == 'pdf':
            obj['pdf']['sha256'] = '0'*64
        elif kind == 'manifest':
            obj['manifest_sha256'] = '0'*64
        elif kind == 'missing-archive':
            archive.unlink()
        elif kind in ['order', 'timestamp', 'permissions']:
            with zipfile.ZipFile(CANONICAL_ZIP) as old:
                names = old.namelist()
                if kind == 'order':
                    names.reverse()
                with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_STORED) as new:
                    for i, name in enumerate(names):
                        info = zipfile.ZipInfo(name, date_time=(2026,10,14,0,0,0))
                        info.create_system = 3
                        info.external_attr = 0o100644 << 16
                        if i == 0 and kind == 'timestamp':
                            info.date_time = (2026,10,14,0,0,2)
                        if i == 0 and kind == 'permissions':
                            info.external_attr = 0o100755 << 16
                        new.writestr(info, old.read(name))
            obj['archive']['sha256'] = digest(archive)
            obj['archive']['bytes'] = archive.stat().st_size
        binding = output/'binding.json'
        binding.write_text(json.dumps(obj, indent=2)+'\n')
        return (binding, archive)
    return prepare

for flags in [[], ['-O']]:
    for label, prepare in [('archive nested member', archive_nested),
                           ('archive external symlink to nested member', archive_symlink),
                           ('archive external hardlink to nested member', archive_hardlink)]:
        case(label, flags, prepare, lambda root,out,ws,p:['scripts/build_archive.py','--out',str(p)], True,
             target='custody/ROOT_MATH_AUDIT.md', expected_mutation=True)
    case('archive resolved root-level alias rejected', flags, archive_root_alias,
         lambda root,out,ws,p:['scripts/build_archive.py','--out',str(p)], False,
         target='paper.tex', expected_mutation=False)
    for label, prepare in [('checker stdout hardlink overwrites input', check_stdout_alias),
                           ('checker receipt symlink overwrites input', check_receipt_alias)]:
        case(label, flags, prepare, lambda root,out,ws,p:['scripts/check.py','--out',str(p)], True,
             target='metadata.json', expected_mutation=True)
    for label, prepare in [('PDF source-copy hardlink overwrites input', pdf_tex_alias),
                           ('PDF stdout symlink overwrites input', pdf_log_alias)]:
        case(label, flags, prepare, lambda root,out,ws,p:['scripts/build_pdf.py','--out',str(p)], True,
             target='metadata.json', expected_mutation=True)
    case('manifest bootstrap symlink passes default verification', flags, manifest_symlink,
         lambda root,out,ws,p:['scripts/verify_package.py'], True)
    case('manifest bootstrap symlink fails strict external verification', flags, manifest_symlink,
         lambda root,out,ws,p:['scripts/verify_package.py','--require-bindings','--bindings',str(CANDIDATE/'UPLOAD_BINDINGS.json'),'--archive',str(CANONICAL_ZIP)], False)
    case('manifest bootstrap symlink passes archive builder preflight', flags, manifest_symlink,
         lambda root,out,ws,p:['scripts/build_archive.py','--out',str(out/'rebuilt.zip')], True)
    case('ordinary payload leaf symlink rejected', flags, leaf_symlink,
         lambda root,out,ws,p:['scripts/verify_package.py'], False)
    case('internal ancestor symlink passes current containment policy', flags, ancestors_within_root,
         lambda root,out,ws,p:['scripts/verify_package.py'], True)
    for label, prepare in [('ordinary payload corruption', broken_member),
                           ('coherent metadata title drift', changed_metadata('title','Different title')),
                           ('coherent metadata license drift', changed_metadata('license','cc0-1.0')),
                           ('coherent metadata ORCID drift', changed_metadata('orcid','0000-0000-0000-0000')),
                           ('coherent premature review promotion', promoted_status),
                           ('changed historical copy with refreshed outer hash', changed_custody)]:
        case(label, flags, prepare, lambda root,out,ws,p:['scripts/verify_package.py'], False)
    case('missing required bindings', flags, noop,
         lambda root,out,ws,p:['scripts/verify_package.py','--require-bindings','--bindings',str(out/'missing.json')], False)
    for kind in ['pdf','manifest','missing-archive','order','timestamp','permissions']:
        case('strict present binding fault '+kind, flags, binding_fault(kind),
             lambda root,out,ws,p:['scripts/verify_package.py','--require-bindings','--bindings',str(p[0]),'--archive',str(p[1])], False)
    case('checker conjugation fault with refreshed manifest', flags, source_fault,
         lambda root,out,ws,p:['scripts/check.py','--out',str(p)], False)

# Official CFF root enum check, independently of any candidate verifier.
schema = json.loads((REVIEW/'private/cff_schema_1_2_0.json').read_text())
type_lines = [line for line in (CANDIDATE/'CITATION.cff').read_text().splitlines() if line.startswith('type:')]
require(len(type_lines) == 1, 'CFF root type field missing/duplicated')
value = type_lines[0].split(':',1)[1].strip()
allowed = schema['properties']['type']['enum']
require(value not in allowed, 'Expected root CFF enum defect was absent')
cff = {'schema_url':'https://raw.githubusercontent.com/citation-file-format/citation-file-format/1.2.0/schema.json',
       'schema_sha256':digest(REVIEW/'private/cff_schema_1_2_0.json'),
       'declared_root_type':value,'root_type_allowed_enum':allowed,
       'root_type_invalid':True,'reference_type_enum_includes_unpublished':
           'unpublished' in schema['definitions']['reference']['properties']['type']['enum'],
       'validation_scope':'The exact offending root enum is checked from the official v1.2.0 JSON schema. No complete YAML/JSON-schema validation library is installed, and no full-schema validation is claimed.'}
report = {'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(), 'actual_commands':ROWS,
          'command_count':len(ROWS),'all_outcomes_as_predicted':True,'citation_enum_validation':cff,
          'candidate_or_prior_records_modified':False,'disposable_cases_deleted_after_hash_custody':True}
(REVIEW/'PACKAGE_CONTROL_RECEIPTS.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'command_count':len(ROWS),'unexpected_outcomes':0,'protected_input_overwrites':sum(x.get('input_bytes_changed',False) for x in ROWS),'citation_enum_validation':cff},indent=2))
