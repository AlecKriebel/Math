"""Independent archive/ledger identity audit. Never executes published code."""
from pathlib import Path, PurePosixPath
import datetime, hashlib, json, re, subprocess, zipfile
from copy import deepcopy
O=Path(__file__).resolve().parent; I=O/'inputs'; REPO=O.parents[2]
def sha(b):return hashlib.sha256(b).hexdigest()
def git(*a):return subprocess.check_output(['git',*a],cwd=REPO,stderr=subprocess.PIPE)
def manifest_errors(payloads,manifest,manifest_name):
    errors=[]; rows=manifest['files']; names=[f['path'] for f in rows]
    if len(names)!=len(set(names)) or set(names)!=set(payloads)-{manifest_name}:errors.append('manifest_exact_inventory')
    for f in rows:
        b=payloads.get(f['path'])
        if b is None or len(b)!=f['bytes'] or sha(b)!=f['sha256']: errors.append('manifest_payload:'+f['path'])
    return errors
def ledger_matches(rows,pid,pr,doi):
    idpat=re.compile(r'(?<!\d)'+re.escape(pid)+r'(?!\d)')
    prurl='https://github.com/AlecKriebel/Math/pull/'+str(pr)
    return [i for i,row in enumerate(rows,1) if row and idpat.search(row[0]) and len(row)>3 and row[2]=='https://doi.org/'+doi and re.search(re.escape(prurl)+r'(?!\d)',row[3])]
ledger=json.loads((O/'private/ledger.fresh.json').read_text()); rows=ledger['values']; inv=json.loads((I/'rest_inventory.json').read_text());prs={p['number']:p for p in inv['pull_requests']}; results=[];controls=[]
for n in [810,815,822,826]:
    d=json.loads((I/f'PR{n:04d}_PUBLICATION_COVERAGE_DETAILS.json').read_text());p=O/f'private/public/pr{n:04d}';meta=json.loads((p/'record.json').read_text());fetch=json.loads((p/'FETCH_RECEIPT.json').read_text());errors=[];fs=[]
    if meta['doi']!=d['doi'] or int(meta['id'])!=d['record'] or meta['state']!='done': errors.append('public_record_identity_or_state')
    if len(fetch['reads'])!=4 or any(x.get('status')!=200 for x in fetch['reads']) or fetch['reads'][0].get('final_url','').rstrip('/')!='https://zenodo.org/records/'+str(d['record']): errors.append('doi_or_public_fetch')
    if {f['key'] for f in meta['files']}!={f['name'] for f in d['public_files']}: errors.append('public_record_file_inventory')
    for f in d['public_files']:
        b=(p/f['name']).read_bytes(); live=next(x for x in meta['files'] if x['key']==f['name']);ok=len(b)==f['bytes']==live['size'] and sha(b)==f['sha256'] and live['checksum']=='md5:'+hashlib.md5(b).hexdigest();fs.append({'file':f['name'],'bytes':len(b),'sha256':sha(b),'pass':ok})
        if not ok:errors.append('public_file:'+f['name'])
    archive=zipfile.ZipFile(next(p.glob('*.zip')));names=archive.namelist();payloads={name:archive.read(name) for name in names};mn='MANIFEST.json' if n==810 else 'package_index.json';manifest=json.loads(payloads[mn]);smn='SOURCE_MANIFEST.json' if n==810 else 'root_evidence/SOURCE_MANIFEST.json';sm=json.loads(payloads[smn]);manerr=manifest_errors(payloads,manifest,mn)
    if len(names)!=len(set(names)) or archive.testzip() is not None or any(PurePosixPath(s).is_absolute() or '..' in PurePosixPath(s).parts for s in names):errors.append('archive_structural')
    if len(names)!=d['archive_members'] or len(manifest['files'])!=d['manifested_payloads'] or sha(payloads[mn])!=d['manifest_sha256']:errors.append('manifest_count_or_pinned_hash')
    errors.extend(manerr)
    head=d.get('source_head') or d['original_source_head'];prefix='unsolved_math_prioritization/attempts/'+d['problem_id']+'/'
    maps=[]
    for f in sm['files']:
        if n==810:path=f['source_path'];member='source/'+f['snapshot_path']
        elif n==815:path=f['repo_path'];member=f['path']
        elif n==822:path=prefix+f['path'];member='source/'+f['path']
        else:path=f['repo_path'];member='source/'+f['path']
        b=payloads.get(member);old=git('show',head+':'+path);current=git('show',prs[n]['headRefOid']+':'+path)
        exact=b is not None and b==old and len(b)==f['bytes'] and sha(b)==f['sha256'];maps.append({'path':path,'archive_member':member,'bytes':len(old),'sha256':sha(old),'historical_equal':exact,'current_equal':b==current})
        if not exact:errors.append('historical_source:'+path)
    tree=git('ls-tree','-r','--name-only',head,'--',prefix).decode().splitlines()
    source_members={s for s in names if s.startswith('source/')}
    if set(tree)!={x['path'] for x in maps} or source_members!={x['archive_member'] for x in maps}:errors.append('complete_historical_source_inventory')
    cached=d.get('original_bindings') or d['original_source_bindings'];cachemap={x.get('path') or x['source_path']:x for x in cached}
    if set(cachemap)!={x['path'] for x in maps}:errors.append('root_provenance_inventory')
    for m in maps:
        c=cachemap[m['path']]
        if c['bytes']!=m['bytes'] or c['sha256']!=m['sha256'] or c.get('current_head_match',c.get('current_equal'))!=m['current_equal']:errors.append('root_provenance_binding:'+m['path'])
    differences=[x['path'] for x in maps if not x['current_equal']]
    disclosed=d.get('current_outer_wrapper_differences',d.get('current_wrapper_differences'))
    if n==810:disclosed=[prefix+s for s in disclosed]
    if set(differences)!=set(disclosed):errors.append('undisclosed_current_difference')
    note=payloads['preprint/note.tex' if n==810 else 'note.tex'];pdf=(p/next(f['name'] for f in d['public_files'] if f['name'].endswith('.pdf'))).read_bytes();copies=[]
    for path in json.loads((O/'SCOPE_RESULTS.json').read_text())['results']:
        if path['pr']!=n:continue
        for s in path['paths']:
            if '/publication_' in s and (s.endswith('/note.tex') or s.endswith('/note.pdf')):
                want=note if s.endswith('.tex') else pdf;actual=git('show',prs[n]['headRefOid']+':'+s);copies.append({'path':s,'equal':actual==want,'bytes':len(actual),'sha256':sha(actual)})
    if not copies or any(not c['equal'] for c in copies):errors.append('current_publication_copy')
    pdf_member='note.pdf' in payloads
    if pdf_member!=d['public_pdf_in_zip'] or pdf_member and payloads['note.pdf']!=pdf:errors.append('standalone_pdf_archive_binding')
    match=ledger_matches(rows,d['problem_id'],n,d['doi']);allid=[j for j,r in enumerate(rows,1) if re.search(r'(?<!\d)'+d['problem_id']+r'(?!\d)',' '.join(r))];alldoi=[j for j,r in enumerate(rows,1) if d['doi'] in ' '.join(r)]
    if match!=[d['ledger_row']] or allid!=match or alldoi!=match:errors.append('ledger_unique_identity')
    # Meaningful adversarial controls against identity and payload substitution.
    dup=deepcopy(rows);dup.append(deepcopy(rows[d['ledger_row']-1])); controls.append({'pr':n,'control':'duplicate exact target row','rejected':len(ledger_matches(dup,d['problem_id'],n,d['doi']))!=1})
    wrongdoi=deepcopy(rows);wrongdoi[d['ledger_row']-1][2]='https://doi.org/10.5281/zenodo.99999999';controls.append({'pr':n,'control':'DOI substituted while title retained','rejected':not ledger_matches(wrongdoi,d['problem_id'],n,d['doi'])})
    wrongpr=deepcopy(rows);wrongpr[d['ledger_row']-1][3]=wrongpr[d['ledger_row']-1][3].replace('/pull/'+str(n),'/pull/'+str(n+1));controls.append({'pr':n,'control':'PR substituted while problem and DOI retained','rejected':not ledger_matches(wrongpr,d['problem_id'],n,d['doi'])})
    sample=maps[0]['archive_member'];bad=dict(payloads);bad[sample]=bad[sample]+b'X';controls.append({'pr':n,'control':'archived original bytes corrupted','rejected':bool(manifest_errors(bad,manifest,mn))})
    missing=dict(payloads);del missing[sample];controls.append({'pr':n,'control':'archived original omitted','rejected':bool(manifest_errors(missing,manifest,mn))})
    extra=dict(payloads);extra['unmanifested.txt']=b'payload';controls.append({'pr':n,'control':'unmanifested payload added','rejected':bool(manifest_errors(extra,manifest,mn))})
    results.append({'pr':n,'problem_id':d['problem_id'],'doi':d['doi'],'ledger_row':d['ledger_row'],'public_title':meta['metadata']['title'],'public_files':fs,'members':len(names),'manifested_payloads':len(manifest['files']),'original_source_head':head,'historical_originals':maps,'historical_source_count':len(maps),'current_equal_count':sum(x['current_equal'] for x in maps),'current_wrapper_differences':differences,'public_pdf_in_zip':pdf_member,'current_copies':copies,'ledger_identity_rows':match,'all_problem_id_rows':allid,'all_doi_rows':alldoi,'errors':errors,'pass':not errors})
out={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'ledger_row_count':len(rows),'ledger_max_columns':max(map(len,rows)),'results':results,'controls':controls,'pass':all(x['pass'] for x in results) and all(c['rejected'] for c in controls),'scope':'Publication identity and byte coverage; no new mathematical, priority or novelty certification.'}
(O/'PUBLICATION_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'pass':out['pass'],'controls':len(controls),'all_controls_rejected':all(c['rejected'] for c in controls),'public_files':sum(len(x['public_files']) for x in results),'manifested':sum(x['manifested_payloads'] for x in results),'originals':sum(x['historical_source_count'] for x in results),'results':[(x['pr'],x['pass'],x['errors']) for x in results]}))
