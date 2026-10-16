#!/usr/bin/env python3
"""Check immutable stages, held families and exact stable ledger without edits."""
from pathlib import Path
import hashlib,json,re,stat,subprocess
if not __debug__:raise SystemExit('Assertions must remain enabled.')
P=Path(__file__).resolve().parent;N=P.parent;A=N.parent
sha=lambda b:hashlib.sha256(b).hexdigest()
mode=lambda p:format(stat.S_IMODE(p.stat().st_mode),'04o')
def utc():return subprocess.run(['/bin/date','-u','+%Y-%m-%dT%H:%M:%SZ'],capture_output=True,check=True).stdout.decode().strip()
started=utc();body_before=sha(Path(__file__).read_bytes())
checks=[]
for name in ['ROOT_PREPRINT02_SOURCE_GATE.json','ROOT_PREPRINT02_FIRST_CANDIDATE_GATE.json']:
    gate=A/name;d=json.loads(gate.read_text());records=[]
    for obj in d['objects']:
        path=N/obj['path'];assert path.exists() and not path.is_symlink(),str(path)
        assert mode(path)==obj['mode_octal'],(str(path),mode(path),obj['mode_octal'])
        if obj['type']=='directory':assert path.is_dir()
        else:
            assert path.is_file();content=path.read_bytes()
            if obj['path']=='RESEARCH_LOG.md':
                content=content[:obj['bytes']]
                prefix=N/('phase2/source_only_log_prefix.md' if name.startswith('ROOT_PREPRINT02_SOURCE_') else 'phase3/first_candidate_log_prefix.md')
                assert prefix.read_bytes()==content
            assert len(content)==obj['bytes'] and sha(content)==obj['sha256'],(name,obj['path'])
        records.append(obj)
    checks.append({'historical_gate':str(gate),'historical_gate_sha256':sha(gate.read_bytes()),
                   'object_count':len(records),'files':sum(o['type']=='file' for o in records),
                   'directories':sum(o['type']=='directory' for o in records),'log_append_only':True,
                   'all_old_file_bodies_modes_and_directory_modes_preserved':True,'objects':records})
fg=A/'ROOT_PREPRINT02_FAMILIES_GATE.json';f=json.loads(fg.read_text());families={}
for name,d in f['namespaces'].items():
    root=N/'families'/name;files={};dirs={'.':mode(root)}
    for p in sorted(root.rglob('*')):
        assert not p.is_symlink()
        rel=str(p.relative_to(root))
        if p.is_dir():dirs[rel]=mode(p)
        else:
            assert p.is_file();b=p.read_bytes();files[rel]={'bytes':len(b),'sha256':sha(b),'mode':mode(p)}
    assert files==d['payloads'],name+' family payload mismatch'
    assert dirs==d['directory_modes'],name+' family directory mismatch'
    families[name]={'file_count':len(files),'directory_count':len(dirs),'files':files,'directory_modes':dirs}
ledger=P/'CLAIM_STATUS.json';l=json.loads(ledger.read_text());original=[]
for line in (N/'FIRST_CANDIDATE_ASSESSMENT.md').read_text().splitlines():
    if re.match(r'^\| [CSM]\d{3} \|',line):original.append([x.strip() for x in line.split('|')[1:-1]])
assert len(original)==len(l['claims'])==74
for old,new in zip(original,l['claims']):
    assert [new[x] for x in ['id','original_location','original_claim','frozen_first_assessment']]==old
    assert new['exact_mathematical_gap'] is None
    for e in new['evidence']:
        b=(N/e['path']).read_bytes();assert len(b)==e['bytes'] and sha(b)==e['sha256']
assert l['publication_approval'] is False and l['candidate_repair_requested'] is False
assert sum(r['id'].startswith('C') for r in l['claims'])==61
assert sum(r['id'].startswith('S') for r in l['claims'])==9
assert sum(r['id'].startswith('M') for r in l['claims'])==4
assert all(r['historical_or_operational_limit'] for r in l['claims'])
md=(P/'CLAIM_STATUS.md').read_text();assert len(re.findall(r'^\| [CSM]\d{3} \|',md,re.M))==74
reports={}
for name in ['ARITHMETIC_MODULI_REPORT.md','SOURCE_PUBLIC_PACKET_REPORT.md','WHOLE_PREPRINT_REVIEW.md','CLAIM_STATUS.md','CLAIM_STATUS.json']:
    p=P/name;b=p.read_bytes();reports[name]={'bytes':len(b),'mode':mode(p),'sha256':sha(b)}
result={'status':'PASS_CURRENT_PRESERVATION_AND_LEDGER_CONSISTENCY_NOT_RELEASE_APPROVAL',
        'utc_start':started,'utc_end':utc(),'clock_argv':['/bin/date','-u','+%Y-%m-%dT%H:%M:%SZ'],
        'argv':['/opt/homebrew/bin/python3','-B',str(Path(__file__).resolve())],'cwd':str(P),
        'executed_body_sha256_before':body_before,'executed_body_sha256_after':sha(Path(__file__).read_bytes()),
        'early_stages':checks,'family_gate_sha256':sha(fg.read_bytes()),'held_families':families,
        'stable_claim_ids':74,'all_original_ledger_fields_preserved':True,'all_report_references_exact':True,
        'remaining_mathematical_gaps':0,'reports':reports,'publication_approval':False,
        'exact_operational_gap':'External ROOT closure of the final namespace, followed only by separately authorized downstream work.',
        'historical_limits_retained':True}
assert result['executed_body_sha256_before']==result['executed_body_sha256_after']
dest=P/'EARLY_STAGE_PRESERVATION.json';assert not dest.exists();dest.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'utc_start':result['utc_start'],'utc_end':result['utc_end'],
                  'source_files_preserved':checks[0]['files'],'first_candidate_files_preserved':checks[1]['files'],
                  'held_family_counts':{n:[d['file_count'],d['directory_count']] for n,d in families.items()},
                  'stable_claim_ids':74,'remaining_mathematical_gaps':0,'reports':reports,
                  'preservation_sha256':sha(dest.read_bytes()),'publication_approval':False},indent=2))
