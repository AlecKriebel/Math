"""Pure PR141 proposal builder. No file, process, queue, network or Git I/O.

build_verified requires the SHA of the complete request independently accepted by
ROOT. Receipt parsing proves consistency, not service authenticity. Only ROOT can
establish authenticity and fresh direct-main custody before calling that API.
build_fixture always produces non-authoritative, visibly labeled fixture bytes.
Neither API installs, publishes, promotes or claims a native verification chain.
"""
import collections
import csv
import datetime
import hashlib
import io
import json
import math
import re
import stat
import zipfile
from urllib.parse import urlsplit

K, CODE, PR = '30003818', 'OWR-16164-012', 141
HEAD = '523247e3246a5f44c7b0089074bb304c1f642bd0'
PAIR = 'f855e1745dc45ab6730ea1bb21198f224bea8b850109adf1697e1a564efbdf8f'
STATEMENT = 'fec9adef5a04af5a2770093b729d81cfb4672a237cdc2cb928ed4fe2bd651826'
ORIGINAL_MANIFEST = 'c1e54b286a8229bb99051341815937c53a8203008a21bf900525d43d991cfe07'
PACKAGE_MANIFEST = '05d50f2a24abf580e90bf2bc61e5a0367f03d8edc0fd9fa395a36ceb476372d2'
DESIGN_EVIDENCE = 'f658c54bbc08d0327ba5b49c7fc1904b5bc87499bad7e14a113aa57b02d6b72f'
OLD_GUARD = '4c63feb6f3bcad8f2a219301c6ad243b155d3bbc83810bd8b3ec8ddcf698a260'
NEW_GUARD = '320d0b2882f5ceabfcc975c85089af68e9b830e6d0300ad1292f59b602fa2a70'
GUARD_RECEIPT = '809d7b560c7258d7c06f53aec4ecece8fccad9993cbf1fcd12a558088bf23696'
ORIGINAL_QUEUE_ROW = 'e0a93e7e0d63fbcf62bc121995673858d1745b273b1ed8d1091750802253b828'
CLEAN_GATE = 'f7ef00ec87857bade761702e6a264969c961997cc36d928b587a526b4cba0877'
ACTUAL_PUBLICATION = '9d1922bc41ff72c6e31d4c157f3a0ae5a914085de97f3a5055418262cd780287'
ACTUAL_SHEET = 'f58ec432f7566c24d7acf6bcd004ce2367694da464b0877db2ef9d8416592149'
ACTUAL_MERGE = 'd1a9addb6e4e9b266d3559d80c8e2b2343dc2325bb3b07fd95227695c5c03174'
PREFIX = 'unsolved_math_prioritization/'
ATTEMPT = PREFIX + 'attempts/' + K + '/'
BACKEND = ('assessments.json', 'state.json', 'history.jsonl', 'assessment_history.jsonl',
           'catalog.json', 'ranking.csv', 'summary.json', 'QUEUE.md')
CANONICAL = ('assessment.json', 'HISTORICAL_DESK_ASSESSMENT.json', 'PUBLICATION_EVIDENCE.json',
             'ACCEPTANCE_EVIDENCE.json', 'README.md', 'RESEARCH_LOG.md')
REPAIRS = ('verify.py', 'review/author_replay/verify.py', 'frozen_artifacts.json', 'review/review_summary.json')
READONLY = ('SHORTLIST.md', 'queue.py', 'manifest.json', 'policy.json')
UPLOADS = {'brownian_first_visit.pdf', 'brownian_first_visit_support.zip'}
SHEET, GID = '1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20', 1254632077
TITLE = 'An explicit joint Laplace transform for Brownian first-visit cell lengths on a circle'
CLAIM = ('Complete joint Laplace law for every finite k>=1 of independent continuing Brownian '
         'walkers on a normalized circle, arbitrary fixed distinct labeled seeds and independent-uniform '
         'or equidistant seeds. Explicit finite permutation sums and deterministic exit-kernel integrals '
         'give each coefficient, with cumulative physical clocks, a uniform factorial outer remainder '
         'and compact-simplex moment determinacy.')
CREDIT = ('Gomes Júnior–Lucena–da Silva–Hilhorst (1996); Miller (2013); '
          'Chatterjee–Nabahi–Terlov (2026); Baccara (2026); Si (2026); '
          'Fitzsimmons–Pitman (1999); Régnier–Dolgushev–Redner–Bénichou (2022).')
LIMITS = ('No named density, fast algorithm or certified inner quadrature. Finite-model and scalar '
          'diagnostics supplement the written proof; they do not prove the Brownian theorem. '
          'The dated bounded audit found no prior complete general target law; no absolute/exclusive '
          'priority or independent discovery is established. Gomes1996/Dicker2006 fulltext403 and '
          'Zenodo registry403 remain limitations; reopen priority on a concrete general-resolution source. '
          'Extensive AI use; unrefereed and no conventional human peer review.')

def need(ok, message):
    if not ok: raise ValueError(message)
def sha(body): return hashlib.sha256(body).hexdigest()
def canonical(value):
    stream=io.BytesIO()
    encoder=json.JSONEncoder(sort_keys=True,ensure_ascii=False,indent=2,allow_nan=False)
    for chunk in encoder.iterencode(value): stream.write(chunk.encode('utf8'))
    stream.write(b'\n');return stream.getvalue()
def equal(a, b): return canonical(a) == canonical(b)
def foreign_mapping_equal(before, after, target):
    # Match canonical equality after omitting target, without giant dictionaries.
    if len(before)-(target in before)!=len(after)-(target in after): return False
    return all(key==target or (key in after and equal(value,after[key])) for key,value in before.items())
def foreign_catalog_equal(before, after, target):
    # Match ordered canonical equality of the target-filtered record lists.
    left_count=len(before)-sum(row['id']==target for row in before)
    right_count=len(after)-sum(row['id']==target for row in after)
    if left_count!=right_count: return False
    left=(row for row in before if row['id']!=target)
    right=(row for row in after if row['id']!=target)
    return all(equal(a,b) for a,b in zip(left,right))
def loads(body):
    def pairs(items):
        out = {}
        for key, value in items:
            need(key not in out, 'Duplicate JSON key'); out[key] = value
        return out
    def invalid(value): raise ValueError('Nonfinite JSON value: '+value)
    def number(value):
        result = float(value); need(math.isfinite(result), 'Nonfinite JSON numeric overflow'); return result
    return json.loads(body, object_pairs_hook=pairs, parse_constant=invalid, parse_float=number)
def stamp(value):
    need(isinstance(value, str), 'UTC text required')
    when = datetime.datetime.fromisoformat(value.replace('Z', '+00:00'))
    need(when.utcoffset() == datetime.timedelta(0), 'UTC offset required'); return when
def digest(value): return isinstance(value, str) and re.fullmatch('[0-9a-f]{64}', value) is not None
def oid(value): return isinstance(value, str) and re.fullmatch('[0-9a-f]{40}', value) is not None
def relative(value):
    need(isinstance(value, str) and value and not value.startswith('/') and '\\' not in value and
         all(part not in ('', '..', '.') for part in value.split('/')) and
         not any(ord(c)<32 or ord(c)==127 for c in value), 'Safe relative path'); return value
def unique_paths(names):
    names = list(names)
    need(len(names)==len(set(names)) and len(names)==len({relative(n).casefold() for n in names}),
         'Duplicate or casefold-colliding paths')
def https(value):
    if not isinstance(value, str) or any(ord(c)<33 or ord(c)==127 or c=='\\' for c in value): return False
    try:
        p=urlsplit(value)
        return p.scheme=='https' and bool(p.hostname) and p.username is None and p.password is None
    except ValueError: return False
def pin(body): return {'bytes':len(body), 'sha256':sha(body)}
def check_pin(body, spec):
    need(isinstance(spec, dict) and set(spec)=={'bytes','sha256'} and type(spec['bytes']) is int and
         spec['bytes']>=0 and digest(spec['sha256']) and type(body) is bytes and equal(pin(body), spec), 'Exact full body pin')
def csv_records(body):
    text=body.decode('utf8')
    lines=[m.group(0) for m in re.finditer(r'[^\r\n]*(?:\r\n|\r|\n|$)', text) if m.group(0)]
    need(''.join(lines)==text, 'CSV physical coverage')
    reader=csv.reader(io.StringIO(text, newline=''), strict=True); out=[]; start=0
    for fields in reader:
        end=reader.line_num;out.append({'fields':fields,'body':''.join(lines[start:end]).encode(),'start':start,'end':end});start=end
    need(start==len(lines), 'CSV complete record spans'); return lines,out
def csv_scoped(body, target):
    lines, rows=csv_records(body)
    need(rows and 'id' in rows[0]['fields'], 'CSV header')
    fields=rows[0]['fields']; need(len(fields)==len(set(fields)), 'Duplicate CSV header')
    need(all(len(r['fields'])==len(fields) for r in rows), 'CSV widths')
    index=fields.index('id'); ids=[r['fields'][index] for r in rows[1:]]
    need(len(ids)==len(set(ids)) and ids.count(K)==1, 'CSV unique target')
    i=ids.index(K)+1; old=rows[i]; last=lines[old['end']-1]
    ending='\r\n' if last.endswith('\r\n') else '\r' if last.endswith('\r') else '\n' if last.endswith('\n') else ''
    values=dict(zip(fields,old['fields']))
    need(values['local_status']=='queued' and values['turns_used']=='0' and values['eligible']=='True' and
         values['rank']==str(target['rank']) and values['holds']=='; '.join(target['holds']), 'CSV baseline reconciliation required')
    # Overlay five strings onto the parsed old record, preserving even unusual
    # lexical representations of all other target fields.
    values.update(rank='',local_status='claimed_solved',turns_used='1',eligible='False',desk_note=target['desk_note'])
    stream=io.StringIO(newline=''); writer=csv.DictWriter(stream,fieldnames=fields,lineterminator='\r\n');writer.writerow(values)
    replacement=stream.getvalue()[:-2]+ending
    result=(''.join(lines[:old['start']])+replacement+''.join(lines[old['end']:])).encode()
    _, after=csv_records(result); allowed={'rank','local_status','turns_used','eligible','desk_note'}
    need(len(after)==len(rows) and all(a['body']==b['body'] for j,(a,b) in enumerate(zip(rows,after)) if j!=i),
         'Unrelated CSV physical bytes/order')
    need(all(old['fields'][j]==after[i]['fields'][j] for j,f in enumerate(fields) if f not in allowed), 'Target CSV source/score/hold changed')
    return result
def queue_overlay(body, note, doi, require_original_row=False):
    need(isinstance(note,str) and not any(c in note for c in '|\r\n'), 'One campaign note cell')
    lines=body.decode().splitlines(keepends=True)
    matches=[i for i,line in enumerate(lines) if line.startswith('| ') and len(line.split('|'))>=3 and line.split('|')[2].strip()==K+' / '+CODE]
    need(len(matches)==1, 'Unique campaign target'); i=matches[0]; old=lines[i]
    ending='\r\n' if old.endswith('\r\n') else '\r' if old.endswith('\r') else '\n' if old.endswith('\n') else ''
    cells=old.rstrip('\r\n').split('|')
    need(len(cells)==14 and cells[8].strip()=='claimed_solved' and cells[9].strip()=='1/5', 'Fresh merged QUEUE claimed_solved 1/5 required')
    need(not cells[12].strip(), 'Existing result requires reconciliation')
    if require_original_row: need(sha(old.encode())==ORIGINAL_QUEUE_ROW, 'Exact submitted campaign row before overlay')
    changed=list(cells);changed[11]=' '+note+' ';changed[12]=' https://doi.org/'+doi+' '
    need(all(changed[j]==cells[j] for j in range(14) if j not in (11,12)), 'Campaign unrelated cell change')
    lines[i]='|'.join(changed)+ending; return ''.join(lines).encode()
def append_event(body, event):
    need(not body or body.endswith(b'\n'), 'History complete newline-terminated preimage')
    return body+json.dumps(event,ensure_ascii=False,allow_nan=False,separators=(',',':')).encode()+b'\n'
def _receipt(obj, role, fixture):
    need(isinstance(obj,dict) and obj.get('schema')=='pr141-native-data-'+role+'/v1', 'Explicit '+role+' schema')
    need(obj.get('fixture') is fixture and obj.get('actual_receipt') is (not fixture), 'Actual/fixture roles cannot mix')
    if not fixture:
        need(obj.get('template_only') is False and type(obj.get('actual_ROOT_PID')) is int and obj['actual_ROOT_PID']>0, 'Authentic ROOT observation required')
    stamp(obj['UTC'])
def package_contents(manifest_body, uploads, working):
    manifest=loads(manifest_body)
    need(sha(manifest_body)==PACKAGE_MANIFEST and manifest['schema']=='pr141-publication-package-manifest/v1' and
         manifest['original_head']==HEAD and manifest['self_excluded']=='PACKAGE_MANIFEST.json' and
         manifest['excluded']==['brownian_first_visit.log'], 'Frozen PR141 package identity')
    files=manifest['files']; need(isinstance(files,dict) and len(files)==54 and set(working)==set(files), 'Exact full54 working package')
    unique_paths(files)
    for name,spec in files.items():
        need(set(spec)=={'bytes','sha256','mode'} and type(spec['mode']) is int and spec['mode']==420, 'Working file mode420')
        check_pin(working[name], {k:spec[k] for k in ('bytes','sha256')})
    need(set(uploads)==UPLOADS and all(uploads[n]==working[n] for n in uploads), 'Exact two reviewed upload bodies')
    inner=loads(working['SUPPORT_MANIFEST.json'])
    need(inner['schema']=='brownian-first-visit-support-manifest/v1' and inner['self_excluded']=='SUPPORT_MANIFEST.json', 'PR141 inner self-excluded SUPPORT manifest')
    expected=set(files)-UPLOADS
    need(len(expected)==52 and set(inner['files'])==expected-{'SUPPORT_MANIFEST.json'}, 'Exact52 support members,51 inner pins')
    for name,spec in inner['files'].items(): need(equal(spec,files[name]), 'Inner/outer member full pins')
    with zipfile.ZipFile(io.BytesIO(uploads['brownian_first_visit_support.zip'])) as archive:
        entries=archive.infolist(); names=[e.filename for e in entries];unique_paths(names)
        need(len(names)==52 and set(names)==expected and 'PACKAGE_MANIFEST.json' not in names, 'Exact PR141 ZIP topology')
        need(sum(e.file_size for e in entries)<=8_000_000, 'Bounded ZIP decompression')
        for entry in entries:
            mode=entry.external_attr>>16
            need(not entry.is_dir() and not stat.S_ISLNK(mode) and stat.S_IFMT(mode) in (0,stat.S_IFREG) and not entry.flag_bits&1, 'Safe regular unencrypted ZIP member')
            need(archive.read(entry)==working[entry.filename], 'Archive exact whole logical body')
    metadata=loads(working['metadata.json'])
    need(metadata['title']==TITLE and equal(metadata,loads(working['zenodo-deposit.json'])['metadata']), 'Exact intended full descriptive metadata')
    return metadata
def metadata_fields(actual, intended, doi, record_id):
    need(isinstance(actual,dict) and all(k in actual and equal(actual[k],v) for k,v in intended.items()), 'Every supplied metadata field exact')
    extras={k:v for k,v in actual.items() if k not in intended}
    need(set(extras)<={'doi','imprint_publisher','prereserve_doi'}, 'Only explicit provider metadata additions')
    if 'doi' in extras: need(extras['doi']==doi, 'Provider DOI addition')
    if 'imprint_publisher' in extras: need(extras['imprint_publisher']=='Zenodo', 'Provider imprint addition')
    if 'prereserve_doi' in extras: need(equal(extras['prereserve_doi'],{'doi':doi,'recid':record_id}), 'Provider reserved record fields')
    return extras

def _build(request_bytes, bodies, trusted_request_sha256, fixture):
    need(type(request_bytes) is bytes and digest(trusted_request_sha256) and sha(request_bytes)==trusted_request_sha256, 'Independently accepted request SHA required')
    request=loads(request_bytes)
    need(request_bytes==canonical(request), 'Canonical whole request')
    fields={'schema','mode','UTC','source','prior','before','readonly','original_manifest','original_files','design_evidence',
            'guard','package','clean_gate','reviews','publication','tracker','merge','fresh_main','authentication','input_pins'}
    need(set(request)==fields and request['schema']=='pr141-pure-native-data-request/v1' and
         request['mode']==('fixture' if fixture else 'actual'), 'Explicit actual/fixture PR141 request')
    now=stamp(request['UTC']); need(now>=stamp('2026-10-07T00:00:00Z'), 'Present-dated import, not retroactive native history')
    specs=request['input_pins'];need(isinstance(specs,dict) and set(specs)==set(bodies) and len(specs)<=256, 'Declared input set equals supplied bodies')
    unique_paths(specs)
    for name,spec in specs.items(): check_pin(bodies[name],spec)
    used=set()
    def read(name):
        need(isinstance(name,str) and name in specs, 'Declared body reference');used.add(name);return bodies[name]
    def obj(name): return loads(read(name))
    source,prior=obj(request['source']),obj(request['prior'])
    need(type(source.get('id')) is int and source['id']==int(K) and source['problem_number']==CODE and
         isinstance(prior,dict) and not prior, 'Exact source record with backend prior {}, never wrapper/report:null')
    sourcehash=sha(source['statement'].encode()); pairhash=sha(json.dumps([source,prior],sort_keys=True).encode())
    need(sourcehash==STATEMENT and pairhash==PAIR, 'Exact authenticated original source pair')
    evidence_body=read(request['design_evidence']);need(sha(evidence_body)==DESIGN_EVIDENCE, 'Closed design evidence pin')
    design=loads(evidence_body)
    need(design['original_queue_read_only_GH_observation']['physical_row_sha256']==ORIGINAL_QUEUE_ROW, 'Original claimed1/5 queue pin')
    original_manifest_body=read(request['original_manifest']);need(sha(original_manifest_body)==ORIGINAL_MANIFEST, 'Immutable original20 manifest')
    archive=loads(original_manifest_body);inventory=archive['files'];need(archive['head']==HEAD and len(inventory)==20, 'PR141 original files[] schema')
    names=[r['path'] for r in inventory];unique_paths(names)
    need(set(request['original_files'])==set(names), 'Full original20 bodies required')
    originals={n:read(label) for n,label in request['original_files'].items()}
    for item in inventory:
        body=originals[item['path']];need(type(item['mode']) is int and item['mode']==420 and oid(item['Git_blob']), 'Original file mode/blob')
        check_pin(body,{k:item[k] for k in ('bytes','sha256')})
        need(hashlib.sha1(b'blob '+str(len(body)).encode()+b'\0'+body).hexdigest()==item['Git_blob'], 'Full original Git blob address')
    need(read(request['source'])==originals['source_record.json'], 'Exact archived source bytes')
    author=loads(originals['status.json']);turns=originals['turns.jsonl']; events=[loads(line) for line in turns.splitlines()]
    need(author['status']=='claimed_solved' and type(author['substantive_approaches']) is int and author['substantive_approaches']==1 and
         type(author['max_approaches']) is int and author['max_approaches']==5 and author['model']=='gpt-6-astra' and
         author['reasoning_effort']=='xhigh' and len(events)==1 and type(events[0]['family']) is int and events[0]['family']==1 and
         events[0]['independent_review']=='pending', 'Preserved real author ledger1/5; no native transitions invented')
    scope={PREFIX+n for n in BACKEND}|{ATTEMPT+n for n in CANONICAL+REPAIRS}
    need(set(request['before'])==scope and set(request['readonly'])=={PREFIX+n for n in READONLY}, 'Exact18 remote/four readonly scope')
    before={p:(read(l) if l is not None else None) for p,l in request['before'].items()}
    readonly={p:read(l) for p,l in request['readonly'].items()}
    need(all(before[PREFIX+n] is not None for n in BACKEND) and all(before[ATTEMPT+n] is None for n in CANONICAL[:4]), 'Complete backend and four genuinely new metadata paths')
    for n in CANONICAL[4:]+REPAIRS: need(before[ATTEMPT+n]==originals[n], 'Fresh canonical preimage equals submitted original')
    need(('## '+K+' —').encode() not in readonly[PREFIX+'SHORTLIST.md'], 'SHORTLIST target absent, whole readonly')
    policy=loads(readonly[PREFIX+'policy.json']);dependency=loads(readonly[PREFIX+'manifest.json'])
    need(type(policy.get('turn_limit')) is int and policy['turn_limit']==5, 'Five-turn native policy')
    if not fixture:
        for name in ('queue.py','manifest.json','policy.json'):
            check_pin(readonly[PREFIX+name],{k:design['native_preimages'][name][k] for k in ('bytes','sha256')})
        need(dependency['revision']=='37e53eabe540fb458758e198be61634bd02ee008', 'Pinned dataset revision')
    guard=request['guard'];need(set(guard)=={'body','receipt'}, 'Only exact reviewed guard repair')
    repaired=read(guard['body']);repair_body=read(guard['receipt']);repair=loads(repair_body)
    need(len(repaired)==5911 and sha(repaired)==NEW_GUARD and sha(repair_body)==GUARD_RECEIPT and
         originals['verify.py']==originals['review/author_replay/verify.py'] and sha(originals['verify.py'])==OLD_GUARD and
         originals['verify.py'].count(b' assert b,group\n')==1 and
         originals['verify.py'].replace(b' assert b,group\n',b' if not b:raise RuntimeError(group)\n',1)==repaired, 'Exact canonical guard delta; portable relocation rejected')
    need(repair['new_verify_sha256']==NEW_GUARD and repair['archived_original_unchanged'] is True and
         all(r['byte_identical_original_normal_receipt'] is True for r in repair['positive_runs']), 'Dated separately bound guard receipt')
    package=request['package'];need(set(package)=={'manifest','working_files','upload_files'}, 'Full frozen package choices')
    package_body=read(package['manifest']);working={relative(n):read(l) for n,l in package['working_files'].items()}
    uploads={relative(n):read(l) for n,l in package['upload_files'].items()};intended=package_contents(package_body,uploads,working)
    clean_gate=read(request['clean_gate']);need(sha(clean_gate)==CLEAN_GATE, 'Exact ROOT clean same54/52 R1/R2 gate')
    reviews=[];identities=[]
    need(isinstance(request['reviews'],list) and len(request['reviews'])==2 and len(set(request['reviews']))==2, 'Two fresh independent same-manifest review receipts')
    for i,label in enumerate(request['reviews'],1):
        review=obj(label);_receipt(review,'review',fixture); raw=obj(review['raw_result']); report=read(review['raw_report'])
        need(review['round']==i and type(review['round']) is int and review['package_manifest_sha256']==PACKAGE_MANIFEST and
             review['reviewed_manifest']==package['manifest'] and review['mandatory_findings']==[] and
             review['verdict']=='PASS' and review['whole_package_reviewed'] is True and digest(review['raw_report_sha256']) and
             review['raw_report_sha256']==sha(report), 'Truthful preserved R1/R2 and full report binding')
        if i==1:
            need(raw['schema']=='pr141-fresh-whole-publication-adversary-round1/v1' and raw['verdict']=='PASS' and
                 raw['mandatory_issues']==[] and raw['reviewed_manifest']['sha256']==PACKAGE_MANIFEST and
                 raw['package_full_member_count']==54 and raw['ZIP_member_count']==52, 'Actual R1 full same package result')
            need(equal(review['optional_findings'],raw['optional_improvements']), 'Preserve all R1 optional findings')
        else:
            need(raw['schema']=='pr141-fresh-whole-publication-review-round2/v1' and
                 raw['verdict']=='PASS_NO_MANDATORY_WHOLE_PACKAGE_DEFECT_FOUND' and
                 all(raw[k]==[] for k in ('mandatory_mathematical_corrections','mandatory_publication_package_corrections','mandatory_attribution_corrections')) and
                 raw['exact_frozen_package_manifest_sha256']==PACKAGE_MANIFEST and raw['round1_report_or_verdict_used'] is False and
                 raw['independent_math_conclusions_formed_before_prior_report_read'] is True, 'Fresh independent clean R2 exact final bytes')
            need(review['optional_findings']==[], 'R2 no required optional refinement')
        need(stamp(raw['UTC'])<=stamp(review['UTC'])<=now and isinstance(review['reviewer_identity'],str) and review['reviewer_identity'], 'Review timestamp/identity')
        reviews.append(review);identities.append(review['reviewer_identity'])
    need(len(set(identities))==2 and stamp(reviews[0]['UTC'])<=stamp(reviews[1]['UTC']), 'Distinct ordered reviewer identity; no invented repair lineage')
    pub=obj(request['publication']);_receipt(pub,'publication',fixture);metadata_body=read(pub['metadata_response']);metadata=loads(metadata_body);doi=pub['version_DOI']
    if fixture: need(doi=='FIXTURE_DOI_NOT_A_PUBLICATION' and metadata['id']=='FIXTURE_RECORD_NOT_A_SERVICE_ID', 'Visibly unusable synthetic publication')
    else:
        need(isinstance(doi,str) and re.fullmatch(r'10\.5281/zenodo\.[1-9][0-9]*',doi) is not None and
             type(metadata['id']) is int and metadata['id']>0 and str(metadata['id'])==doi.rsplit('.',1)[1] and
             pub['record_URL']=='https://zenodo.org/records/'+str(metadata['id']), 'Actual version DOI and provider record')
    need(pub['published'] is True and pub['original_head']==HEAD and pub['package_manifest_sha256']==PACKAGE_MANIFEST and
         metadata['doi']==doi and (metadata.get('submitted') is True or metadata.get('is_published') is True), 'Published final package, not reserved draft')
    additions=metadata_fields(metadata['metadata'],intended,doi,metadata['id'])
    need(set(pub['downloaded_files'])==UPLOADS, 'Full two-file downloads')
    shape=pub['metadata_file_schema'];need(shape in ('record','deposition'), 'Explicit provider file schema')
    key,size=('key','size') if shape=='record' else ('filename','filesize')
    file_rows=metadata['files'];need(isinstance(file_rows,list) and len(file_rows)==2 and len({r[key] for r in file_rows})==2, 'Exact provider files')
    byname={r[key]:r for r in file_rows};need(set(byname)==UPLOADS, 'No provider extra or missing upload')
    for name,body in uploads.items():
        need(read(pub['downloaded_files'][name])==body, 'Uploaded/downloaded full bodies')
        checksum=('md5:' if shape=='record' else '')+hashlib.md5(body).hexdigest()
        need(type(byname[name][size]) is int and byname[name][size]==len(body) and byname[name]['checksum']==checksum, 'Provider exact byte counts/checksums')
    tracker=obj(request['tracker']);_receipt(tracker,'tracker',fixture);row=tracker['row'];cells=tracker['cells']
    need(tracker['spreadsheet_id']==SHEET and type(tracker['gid']) is int and tracker['gid']==GID and
         type(row) is int and row>=2 and tracker['original_head']==HEAD and tracker['version_DOI']==doi and
         isinstance(cells,list) and len(cells)==4 and all(isinstance(c,str) for c in cells), 'Target tracker identity and four cells')
    selected="'Math Puzzles'!A"+str(row)+':D'+str(row)
    need(tracker['range']==selected and cells[0]=='https://doi.org/10.4171/OWR/2018/23' and
         cells[2]=='https://doi.org/'+doi and K+' / '+CODE in cells[3], 'Exact source/DOI/problem tracker row')
    need(cells[1]=='' or (tracker.get('existing_chat_authorized') is True and https(cells[1])), 'Blank or separately authorized existing chat')
    append=obj(tracker['append_response']);readback=obj(tracker['readback_response']);second=obj(tracker['second_readback_response']);update=append['updates']
    need(append['spreadsheetId']==SHEET and update['updatedRange']==selected and
         all(type(update[k]) is int and update[k]==n for k,n in (('updatedRows',1),('updatedColumns',4),('updatedCells',4))) and
         update['updatedData']['values']==[cells] and readback['range']==selected and readback['values']==[cells] and
         second['range']==selected and second['values']==[cells] and tracker['readback_response']!=tracker['second_readback_response'],
         'Raw exact four-cell append/two distinct readbacks')
    merge=obj(request['merge']);_receipt(merge,'merge',fixture);provider=obj(merge['provider_response']);merged=stamp(merge['merged_at'])
    need(type(provider['number']) is int and provider['number']==PR and provider['head']['sha']==HEAD and
         provider['base']['ref']=='main' and provider['merged'] is True and provider['merge_commit_sha']==merge['merge_commit'] and
         provider['merged_at']==merge['merged_at'] and provider['html_url']=='https://github.com/AlecKriebel/Math/pull/141', 'Raw original-head main merge')
    if not fixture: need(oid(merge['merge_commit']), 'Real merge commit OID')
    fresh=obj(request['fresh_main']);_receipt(fresh,'fresh-main',fixture)
    need(fresh['merged_original_head']==HEAD and fresh['merge_commit']==merge['merge_commit'] and fresh['merge_ancestor_verified'] is True and
         fresh['complete_fresh_MAIN_preimages_verified'] is True and equal(fresh['preimages'],request['before']) and
         equal(fresh['readonly'],request['readonly']) and equal(fresh['canonical_originals'],request['original_files']), 'Complete fresh remote/main original20 and18 preimages')
    if not fixture: need(oid(fresh['MAIN_commit']) and fresh['direct_remote_MAIN']==fresh['MAIN_commit'], 'Fresh direct-main identity')
    main_raw=obj(fresh['provider_main_response']);ancestry=obj(fresh['ancestry_receipt']);tree=obj(fresh['scoped_tree'])
    _receipt(ancestry,'main-ancestry',fixture)
    need(main_raw['object']['sha']==fresh['MAIN_commit'] and ancestry['MAIN_commit']==fresh['MAIN_commit'] and
         ancestry['merge_commit']==merge['merge_commit'] and ancestry['merge_is_ancestor'] is True,
         'Raw direct-main response and separately pinned ancestry witness')
    expected_tree={**{p:(None if b is None else b) for p,b in before.items()},
                   **{ATTEMPT+n:b for n,b in originals.items() if ATTEMPT+n not in before}}
    need(isinstance(tree,dict) and set(tree)==set(expected_tree), 'Complete32 scoped preimages including four absences')
    for path,body in expected_tree.items():
        item=tree[path]
        if body is None: need(item is None, 'Four new canonical metadata paths genuinely absent')
        else:
            need(isinstance(item,dict) and set(item)=={'bytes','sha256','Git_blob','mode'} and
                 type(item['mode']) is int and item['mode']==420 and
                 item['Git_blob']==hashlib.sha1(b'blob '+str(len(body)).encode()+b'\0'+body).hexdigest(), 'Scoped full preimage mode/blob')
            check_pin(body,{k:item[k] for k in ('bytes','sha256')})
    need(all(stamp(r['UTC'])<=stamp(pub['UTC']) for r in reviews) and stamp(pub['UTC'])<=stamp(tracker['UTC'])<=merged<=stamp(fresh['UTC'])<=now,
         'Reviews, publication, tracker, merge, fresh main, present import chronology')
    auth_body=read(request['authentication']);auth=loads(auth_body);_receipt(auth,'authentication',fixture)
    need(auth['owner']=='ROOT' and auth['original_head']==HEAD and auth['source_pair_hash']==PAIR and auth['statement_hash']==STATEMENT and
         auth['original_effort']=='1/5' and type(auth['new_central_proof_search_turns']) is int and auth['new_central_proof_search_turns']==0 and
         auth['original_author_turn_ledger_present'] is True and auth['original_native_transition_ledger_present'] is False,
         'ROOT truthful effort/source ledger authentication')
    roles={'package':package['manifest'],'whole_package_R1':reviews[0]['raw_result'],'whole_package_R2':reviews[1]['raw_result'],
           'R1_report':reviews[0]['raw_report'],'R2_report':reviews[1]['raw_report'],'publication':pub['raw_role_receipt'],
           'provider_metadata':pub['metadata_response'],'tracker':tracker['raw_role_receipt'],'tracker_append':tracker['append_response'],
           'tracker_readback':tracker['readback_response'],'tracker_second_readback':tracker['second_readback_response'],
           'merge':merge['raw_role_receipt'],'merge_provider':merge['provider_response'],'clean_gate':request['clean_gate'],
           'fresh_main':request['fresh_main'],'direct_main_provider':fresh['provider_main_response'],
           'main_ancestry':fresh['ancestry_receipt'],'scoped_preimage_tree':fresh['scoped_tree'],
           'guard_receipt':guard['receipt'],'original20_manifest':request['original_manifest']}
    need(set(auth['roles'])==set(roles), 'All raw authority roles, not booleans alone')
    for role,label in roles.items(): check_pin(read(label),auth['roles'][role])
    raw_pub=obj(pub['raw_role_receipt']);raw_tracker=obj(tracker['raw_role_receipt']);raw_merge=obj(merge['raw_role_receipt'])
    if fixture:
        for raw,role in ((raw_pub,'published-fullbody'),(raw_tracker,'tracker-readback'),(raw_merge,'original-head-merge')): _receipt(raw,role,True)
        need(raw_pub['DOI']==doi and raw_pub['published'] is True and raw_pub['package_manifest_sha256']==PACKAGE_MANIFEST and
             raw_pub['authenticated_provider_metadata_sha256']==sha(metadata_body) and equal(raw_pub['intended_metadata'],intended), 'Raw publication role exact provider linkage')
        need(raw_tracker['spreadsheet_id']==SHEET and raw_tracker['gid']==GID and raw_tracker['range']==selected and
             equal(raw_tracker['cells'],cells) and raw_tracker['append_response_sha256']==sha(read(tracker['append_response'])) and
             raw_tracker['readback_response_sha256']==sha(read(tracker['readback_response'])), 'Raw tracker role body linkage')
        need(raw_merge['original_head']==HEAD and raw_merge['merge_commit']==merge['merge_commit'] and raw_merge['merged_at']==merge['merged_at'] and
             raw_merge['provider_response_sha256']==sha(read(merge['provider_response'])), 'Raw merge role provider linkage')
    else:
        need(sha(read(pub['raw_role_receipt']))==ACTUAL_PUBLICATION and
             raw_pub['schema']=='pr141-actual-published-fullbody-verification/v1' and raw_pub['DOI']==doi and raw_pub['published'] is True and
             raw_pub['package_manifest_sha256']==PACKAGE_MANIFEST and raw_pub['authenticated_deposition_sha256']==sha(metadata_body) and
             equal(raw_pub['metadata'],intended) and raw_pub['whole_package_clean_gate_sha256']==CLEAN_GATE, 'Existing authentic publication role exact deposition linkage')
        need(sha(read(tracker['raw_role_receipt']))==ACTUAL_SHEET and raw_tracker['schema']=='pr141-actual-gws-sheet-receipt/v1' and
             raw_tracker['spreadsheet_id']==SHEET and type(raw_tracker['sheet_id']) is int and raw_tracker['sheet_id']==GID and
             raw_tracker['range']==selected and raw_tracker['row_index']==row and equal(raw_tracker['values'],cells) and
             raw_tracker['single_append'] is True and raw_tracker['both_distinct_actual_full_cell_readbacks_equal'] is True,
             'Existing authentic tracker role full four-cell linkage')
        for name,label in (('append',tracker['append_response']),('readback',tracker['readback_response']),('independent_readback',tracker['second_readback_response'])):
            record=raw_tracker['processes'][name]
            check_pin(read(label),{k:record['stdout'][k] for k in ('bytes','sha256')})
            need(record['exit_code']==0 and record['reaped'] is True and record['group_absent'] is True, 'Closed actual tracker child custody')
        need(sha(read(merge['raw_role_receipt']))==ACTUAL_MERGE and raw_merge['schema']=='pr141-actual-original-head-main-merge/v1' and
             raw_merge['original_head']==HEAD and raw_merge['merge_commit']==merge['merge_commit'] and raw_merge['merged_at']==merge['merged_at'] and
             raw_merge['merged'] is True and equal(raw_merge['actual_provider_merged_readback'],provider) and
             raw_merge['processes']['merged_readback']['stdout']['sha256']==sha(read(merge['provider_response'])),
             'Existing authentic merge role exact provider linkage')
    need(auth['DOI']==doi and auth['package_manifest_sha256']==PACKAGE_MANIFEST and auth['MAIN_commit']==fresh['MAIN_commit'] and
         auth['merge_commit']==merge['merge_commit'] and equal(auth['tracker_cells'],cells) and auth['tracker_range']==selected and
         equal(auth['provider_added_metadata_fields'],additions) and stamp(fresh['UTC'])<=stamp(auth['UTC'])<=now, 'ROOT whole accepted roles and fresh chronology')
    assessments=loads(before[PREFIX+'assessments.json']);states=loads(before[PREFIX+'state.json']);catalog=loads(before[PREFIX+'catalog.json'])
    need(isinstance(assessments,dict) and K in assessments and isinstance(states,dict) and K not in states, 'Existing target state requires reconciliation')
    need(isinstance(catalog,list) and all(isinstance(r,dict) and isinstance(r.get('id'),str) for r in catalog) and
         len({r['id'] for r in catalog})==len(catalog) and sum(r['id']==K for r in catalog)==1, 'Catalog unique identities')
    need(type(dependency['records']) is int and dependency['records']==len(catalog), 'Manifest complete record count')
    for r in catalog:
        need(type(r.get('eligible')) is bool and type(r.get('present')) is bool and type(r.get('turns_used')) is int and
             isinstance(r.get('holds'),list) and all(isinstance(h,str) for h in r['holds']), 'Typed native booleans/counts/holds')
    target=next(r for r in catalog if r['id']==K);historical=assessments[K]
    need(target['problem_number']==CODE and target['review_hash']==historical['review_hash']==PAIR and
         target['statement_hash']==historical['statement_hash']==STATEMENT and historical['id']==K and
         target['local_status']=='queued' and target['turns_used']==0 and target['eligible'] is True and target['present'] is True and
         type(target['turn_limit']) is int and target['turn_limit']==5 and target['holds']==historical['holds']==[], 'Target source/hold/native queued preimage')
    # All authenticated target source/probability/score/policy fields must match
    # the exact desk baseline; publication does not grant a new ranking model.
    need(equal(historical,design['native_preimages']['assessments.json']['target']) and
         equal(target,design['native_preimages']['catalog.json']['target'][0]), 'Target desk/source/score/policy drift requires fresh reconciliation')
    _,csv_rows=csv_records(before[PREFIX+'ranking.csv']);csv_fields=csv_rows[0]['fields']
    need('id' in csv_fields and len(csv_fields)==len(set(csv_fields)), 'Complete unique CSV header')
    csv_matches=[dict(zip(csv_fields,r['fields'])) for r in csv_rows[1:] if len(r['fields'])==len(csv_fields) and r['fields'][csv_fields.index('id')]==K]
    need(len(csv_matches)==1 and equal(csv_matches[0],design['native_preimages']['ranking.csv']['target'][0]),
         'Target CSV complete source/score/hold baseline drift requires reconciliation')
    for name in ('history.jsonl','assessment_history.jsonl'):
        body=before[PREFIX+name]; need(not body or body.endswith(b'\n'), 'Complete ledger prefix')
        for line in body.splitlines():
            record=loads(line);need(isinstance(record,dict) and str(record.get('id'))!=K, 'Existing target native history requires reconciliation')
    summary=loads(before[PREFIX+'summary.json'])
    baseline={'records':len(catalog),'eligible':sum(r['eligible'] for r in catalog),'assessed':len(assessments),
              'holds':dict(collections.Counter(h.split(':')[0] for r in catalog for h in r['holds']))}
    need(equal(summary,baseline), 'Exact baseline summary counts before update; reject unrelated drift')
    note=CLAIM+' Earlier painting and classical methods credited: '+CREDIT+' '+LIMITS+' Original reported1/5; present import adds0 central turns.'
    if fixture: note='FIXTURE ONLY; NO PUBLICATION, MERGE, TRACKER OR ACCEPTANCE OCCURRED. '+note
    imported={'schema':'pr141-dated-native-import-baseline/v1','at':request['UTC'],'id':K,'status':'claimed_solved','turns_used':1,
              'event':'dated_import_of_authenticated_author_count','original_head':HEAD,'original_budget':'1/5','review_hash':PAIR,'statement_hash':STATEMENT,
              'original_author_turn_ledger_present':True,'original_structured_ledger_present':True,'original_native_transition_ledger_present':False,
              'new_central_proof_search_turns':0,'fixture':fixture,'original_queue_row_sha256':ORIGINAL_QUEUE_ROW,
              'original_author_ledger_pin':pin(turns),'original_status_pin':pin(originals['status.json']),'original_readiness_pin':pin(originals['readiness.json']),
              'provenance':'Present-dated compatibility import of the real author one-family report; not a reconstructed backend CLI chain. Original author independent_review=pending remains verbatim.'}
    accepted={'schema':'pr141-proposed-scoped-native-evidence/v1','fixture':fixture,'actual_receipt':not fixture,'at':request['UTC'],
              'PR':PR,'id':K,'original_head':HEAD,'literal_status':'claimed_solved','original_effort':'1/5','new_central_proof_search_turns':0,
              'original_author_turn_ledger_present':True,'original_native_transition_ledger_present':False,'dated_import_baseline':imported,
              'exact_scope':CLAIM,'credited_predecessors':CREDIT,'limits_and_priority':LIMITS,'original_model':author['model'],
              'original_reasoning_effort':author['reasoning_effort'],'package_manifest_sha256':PACKAGE_MANIFEST,'review_hash':PAIR,'statement_hash':STATEMENT,
              'preserved_review_receipts':reviews,'provider_metadata_additions':additions,'raw_role_pins':auth['roles'],'authentication_pin':pin(auth_body),
              'actual_merge_commit':merge['merge_commit'],'actual_merged_at':merge['merged_at'],'fresh_MAIN_commit':fresh['MAIN_commit'],
              'native_publication_or_local_installation_performed':False,'backend_verified_solved_transition_claimed':False,
              'remote_changed_paths':18,'local_installation_paths':32,'remote_byte_unchanged_canonical_paths':14,'input_pins':specs}
    assessment={**historical,'note':note,'rationale':CLAIM+' Classical machinery and preceding painting work credited.',
                'remaining_gap':LIMITS+' Native publication, local readback and separate program bookkeeping remain future actions.',
                'first_experiment':'Preserve original20 and both historical verification receipts; install reviewed guard-only repairs and actual roles in an independently reviewed later transaction.',
                'sources':list(dict.fromkeys(historical['sources']+['https://doi.org/'+doi])),'reviewed_at':request['UTC'],
                'original_budget':'1/5','new_central_proof_search_turns':0,'publication_DOI':doi,'native_import_provenance':accepted}
    ass_after={**assessments,K:assessment}; state_after={**states,K:imported}
    projected={**target,'local_status':'claimed_solved','turns_used':1,'eligible':False,'rank':None,'desk_note':note}
    cat_after=[projected if r['id']==K else r for r in catalog]
    summary_after={**summary,'eligible':baseline['eligible']-1}
    need(foreign_mapping_equal(assessments,ass_after,K) and
         foreign_mapping_equal(states,state_after,K) and
         foreign_catalog_equal(catalog,cat_after,K), 'Unrelated typed records/order/ranks preserved')
    pub_evidence={'schema':'pr141-proposed-publication-evidence/v1','fixture':fixture,'actual_receipt':not fixture,'DOI':doi,'version_DOI':doi,
                  'record_URL':pub['record_URL'],'full_provider_metadata':metadata,'package_manifest_sha256':PACKAGE_MANIFEST,
                  'uploaded_downloaded_body_pins':{n:pin(b) for n,b in uploads.items()},'original_head':HEAD,'original_budget':'1/5',
                  'new_central_proof_search_turns':0,'tracker_range':selected,'tracker_four_cells':cells,'raw_role_pins':auth['roles']}
    provenance={'schema':'pr141-current-guard-revision-provenance/v1','at':repair['UTC'],'repair_receipt_pin':pin(repair_body),
                'original_submitted_attempt_is_immutable':True,'current_guard_sha256':NEW_GUARD,'submitted_guard_sha256':OLD_GUARD,
                'September30_review_checked_October7_guard_bytes':False,'historical_verification_receipts_unchanged':True,
                'meaning':'Current guard-only source pins. Sept30 reviewer verdict and outputs remain historical; Oct7 robustness receipt is separate, not a new mathematical review.'}
    frozen_old=loads(originals['frozen_artifacts.json']);frozen={**frozen_old,'verify.py':NEW_GUARD,
                 '_current_revision_provenance':{**provenance,'original_submitted_pins':frozen_old}}
    review_old=loads(originals['review/review_summary.json']);review_current={**review_old,'hashes':{**review_old['hashes'],'author_replay/verify.py':NEW_GUARD},
                 'verdict_scope':'Historical September30 submitted proof/replay; no October7 guard-byte review is attributed to that reviewer.',
                 'current_guard_revision':{**provenance,'original_submitted_review_summary':review_old}}
    suffix=('\n\n## '+request['UTC']+' — proposed publication metadata and dated author-effort import\n\n'+note+'\n\n'
            'Version DOI: '+doi+'. Original20 remains immutable under original_submitted_attempt. Both canonical guard copies have SHA256 '+NEW_GUARD+
            '; the separately dated repair receipt binds robustness checks. September30 review and unchanged verification receipts remain historical. '
            'These proposed bytes do not assert native installation or program completion.\n').encode()
    log=('\n\n'+request['UTC']+': Proposed scoped native data after full actual role validation. Original author1/5 imported at this timestamp; '
         'zero new central proof-search turns. Remote delta18; separate local inventory32 includes14 remote-unchanged canonical originals. '
         'Native integration estimate80% pending scoped writer/public and local readback plus separate bookkeeping. '+note+'\n').encode()
    outputs={PREFIX+'assessments.json':canonical(ass_after),PREFIX+'state.json':canonical(state_after),
             PREFIX+'history.jsonl':append_event(before[PREFIX+'history.jsonl'],imported),
             PREFIX+'assessment_history.jsonl':append_event(before[PREFIX+'assessment_history.jsonl'],{'event':'dated_publication_assessment_import','at':request['UTC'],'id':K,'assessment':assessment,'fixture':fixture}),
             PREFIX+'catalog.json':canonical(cat_after),PREFIX+'ranking.csv':csv_scoped(before[PREFIX+'ranking.csv'],{**target,'desk_note':note}),
             PREFIX+'summary.json':canonical(summary_after),PREFIX+'QUEUE.md':queue_overlay(before[PREFIX+'QUEUE.md'],note,doi,not fixture),
             ATTEMPT+'assessment.json':canonical(assessment),ATTEMPT+'HISTORICAL_DESK_ASSESSMENT.json':canonical(historical),
             ATTEMPT+'PUBLICATION_EVIDENCE.json':canonical(pub_evidence),ATTEMPT+'ACCEPTANCE_EVIDENCE.json':canonical(accepted),
             ATTEMPT+'README.md':before[ATTEMPT+'README.md']+suffix,ATTEMPT+'RESEARCH_LOG.md':before[ATTEMPT+'RESEARCH_LOG.md']+log,
             ATTEMPT+'verify.py':repaired,ATTEMPT+'review/author_replay/verify.py':repaired,
             ATTEMPT+'frozen_artifacts.json':canonical(frozen),ATTEMPT+'review/review_summary.json':canonical(review_current)}
    local={**{ATTEMPT+n:b for n,b in originals.items()},**outputs}
    unchanged={ATTEMPT+n for n in originals}-set(outputs)
    need(set(outputs)==scope and len(outputs)==18 and len(local)==32 and len(unchanged)==14 and
         all(local[p]==originals[p[len(ATTEMPT):]] for p in unchanged), '18 remote delta distinct from32 complete local inventory')
    need(used==set(specs), 'Every declared input consumed, no hidden surplus authority')
    return {'fixture':fixture,'status':'FIXTURE_NOT_AUTHORITY' if fixture else 'PROPOSED_DATA_ONLY_NOT_NATIVE_ACCEPTANCE',
            'outputs':outputs,'local_installation_inventory':local,'remote_unchanged_canonical_paths':sorted(unchanged),
            'preserved_readonly':readonly,'accepted_evidence':accepted,'baseline_summary':baseline,'summary_after':summary_after}

def build_verified(request_bytes, bodies, trusted_request_sha256):
    """Only after ROOT authenticates all actual roles and accepts the whole SHA."""
    return _build(request_bytes,bodies,trusted_request_sha256,False)
def build_fixture(request_bytes, bodies):
    """Synthetic controls only; never actual acceptance or service authority."""
    return _build(request_bytes,bodies,sha(request_bytes),True)
