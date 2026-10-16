"""Pure PR140 native metadata overlay; no I/O, execution or service authority.

Actual inputs require an independently accepted request SHA supplied out of band.
Receipt validation is structural: ROOT must establish authenticity before supplying
that SHA. The distinct fixture API produces explicitly non-authoritative evidence.
"""
import collections
import csv
import datetime
import hashlib
import io
import json
import re
import stat
import zipfile
from urllib.parse import urlsplit

K, CODE = '5100023', 'AMR-050-0023'
HEAD = '9e908ae58b5ceee6a0825bbebd8acf565db55340'
REVIEW = '374cf32e1f1b5885551fe8b3a02d43c749e7b392715cc4eb0b4ac77f628a865b'
STATEMENT = '70a4186cf9778db261377679ae614deec32ed1c2e80e209f809fba637b4e4b89'
PREFIX = 'unsolved_math_prioritization/'
ATTEMPT = PREFIX + 'attempts/' + K + '/'
BACKEND = ('assessments.json', 'state.json', 'history.jsonl', 'assessment_history.jsonl',
           'catalog.json', 'ranking.csv', 'summary.json', 'QUEUE.md')
CANONICAL = ('assessment.json', 'HISTORICAL_DESK_ASSESSMENT.json', 'PUBLICATION_EVIDENCE.json',
             'ACCEPTANCE_EVIDENCE.json', 'README.md', 'RESEARCH_LOG.md')
READONLY = ('SHORTLIST.md', 'queue.py', 'manifest.json', 'policy.json')
SHEET = '1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20'
GID = 1254632077
CLAIM = ('Unweighted vertex centroids of unprimed full-line antipedals at the origin and both foci '
         'are constant for a Poncelet billiard family on a>b>0 with 0<lambda<b^2, even least period '
         'N>=4 and distinct vertices, including simple and primitive star families in either orientation. '
         'Circle separate; repeated odd-period lists and endpoint/hyperbolic caustics excluded.')

def need(ok, message):
    if not ok: raise ValueError(message)
def canonical(value):
    return (json.dumps(value, sort_keys=True, ensure_ascii=False, indent=2, allow_nan=False)+'\n').encode()
def equal(left, right): return canonical(left)==canonical(right)
def sha(body): return hashlib.sha256(body).hexdigest()
def loads(body):
    def pairs(values):
        out={}
        for key,value in values:
            need(key not in out,'Duplicate JSON key');out[key]=value
        return out
    def invalid(value): raise ValueError('Nonfinite JSON constant: '+value)
    return json.loads(body, object_pairs_hook=pairs, parse_constant=invalid)
def stamp(value):
    need(isinstance(value,str),'UTC text required')
    when=datetime.datetime.fromisoformat(value.replace('Z','+00:00'))
    need(when.utcoffset()==datetime.timedelta(0),'UTC offset required')
    return when
def oid(value):return isinstance(value,str) and re.fullmatch('[0-9a-f]{40}',value) is not None
def digest(value):return isinstance(value,str) and re.fullmatch('[0-9a-f]{64}',value) is not None
def relative(value):
    need(isinstance(value,str) and value and not value.startswith('/') and '\\' not in value and
         all(part not in ('','..','.') for part in value.split('/')) and
         not any(ord(c)<32 or ord(c)==127 for c in value),'Safe relative path')
    return value
def https(value):
    if not isinstance(value,str) or any(ord(c)<33 or ord(c)==127 or c=='\\' for c in value):return False
    try:
        p=urlsplit(value)
        return p.scheme=='https' and bool(p.hostname) and p.username is None and p.password is None
    except ValueError:return False

def csv_records(body):
    text=body.decode('utf8')
    lines=[m.group(0) for m in re.finditer(r'[^\r\n]*(?:\r\n|\r|\n|$)',text) if m.group(0)]
    need(''.join(lines)==text,'CSV physical coverage')
    reader=csv.reader(io.StringIO(text,newline=''),strict=True);out=[];start=0
    for fields in reader:
        end=reader.line_num;out.append({'fields':fields,'body':''.join(lines[start:end]).encode(),'start':start,'end':end});start=end
    need(start==len(lines),'CSV record spans')
    return lines,out

def csv_overlay(body,target):
    lines,rows=csv_records(body);need(rows and 'id' in rows[0]['fields'],'CSV header')
    fields=rows[0]['fields'];need(len(fields)==len(set(fields)),'Duplicate CSV header')
    index=fields.index('id');need(all(len(r['fields'])==len(fields) for r in rows),'CSV row widths')
    ids=[r['fields'][index] for r in rows[1:]];need(len(ids)==len(set(ids)) and ids.count(K)==1,'CSV target identity')
    i=ids.index(K)+1;old=rows[i];last=lines[old['end']-1]
    ending='\r\n' if last.endswith('\r\n') else '\r' if last.endswith('\r') else '\n' if last.endswith('\n') else ''
    stream=io.StringIO(newline='');writer=csv.DictWriter(stream,fieldnames=fields,extrasaction='ignore',lineterminator='\r\n')
    writer.writerow({**target,'holds':'; '.join(target['holds']),'reasons':'; '.join(target['reasons'])})
    replacement=stream.getvalue()[:-2]+ending
    result=(''.join(lines[:old['start']])+replacement+''.join(lines[old['end']:])).encode()
    _,after=csv_records(result)
    need(len(after)==len(rows) and [r['fields'][index] for r in after[1:]]==ids and
         all(a['body']==b['body'] for j,(a,b) in enumerate(zip(rows,after)) if j!=i),'Unrelated CSV physical bytes/order')
    return result

def queue_overlay(body,note,doi):
    need(isinstance(note,str) and not any(c in note for c in '|\r\n'),'Single campaign note cell')
    text=body.decode();lines=text.splitlines(keepends=True)
    matches=[i for i,line in enumerate(lines) if line.startswith('| ') and len(line.split('|'))>=3 and line.split('|')[2].strip()==K+' / '+CODE]
    need(len(matches)==1,'Unique campaign target row');i=matches[0];old=lines[i]
    ending='\r\n' if old.endswith('\r\n') else '\r' if old.endswith('\r') else '\n' if old.endswith('\n') else ''
    cells=old.rstrip('\r\n').split('|')
    need(len(cells)==14 and cells[8].strip()=='claimed_solved' and cells[9].strip()=='2/5','Fresh merged original QUEUE claimed_solved 2/5 required')
    # Result must be empty before this first publication overlay; reconcile otherwise.
    need(not cells[12].strip(),'Existing result requires reconciliation')
    changed=list(cells);changed[11]=' '+note+' ';changed[12]=' https://doi.org/'+doi+' '
    need(all(changed[j]==cells[j] for j in range(14) if j not in (11,12)),'Campaign rank/score/status/effort/source changed')
    lines[i]='|'.join(changed)+ending
    return ''.join(lines).encode()

def append_event(body,event):
    need(not body or body.endswith(b'\n'),'History needs complete newline-terminated preimage')
    return body+json.dumps(event,ensure_ascii=False,allow_nan=False,separators=(',',':')).encode()+b'\n'

def csv_scoped(body,target):
    result=csv_overlay(body,target)
    _,old=csv_records(body);_,new=csv_records(result);fields=old[0]['fields'];index=fields.index('id')
    i=next(j for j,row in enumerate(old[1:],1) if row['fields'][index]==K)
    allowed={'rank','local_status','turns_used','eligible','desk_note'}
    need(all(old[i]['fields'][j]==new[i]['fields'][j] for j,f in enumerate(fields) if f not in allowed),
         'Target CSV source/score/hold discrepancy requires reconciliation; never normalize it')
    return result

def validate_legacy_pins(original):
    need(original['original_queue_row_sha256']=='0976537e7836d8d1a7dac530af9d0cc5a66dcdba3b670ddb38942d38e8439114' and
         original['original_author_log_sha256']=='4670501b285b8d577b53097a7fdb17cabc0abc7ba28a88f28a258e583da4ffb3',
         'Exact authenticated original queue row and author log for legacy 2/5')

def package_contents(package_body,uploads):
    manifest=loads(package_body)
    need(manifest['schema']=='k405-publication-package-manifest/v1' and set(uploads)=={'antipedal_centroids.pdf','antipedal_centroids_support.zip'},'Exact PDF/support package')
    inventory=manifest['members']
    need(isinstance(inventory,list) and 8<=len(inventory)<=128 and len({m['relative'] for m in inventory})==len(inventory),'Whole package member inventory')
    members={relative(m['relative']):m for m in inventory}
    for member in inventory:
        need(type(member['bytes']) is int and member['bytes']>=0 and digest(member['sha256']),'Package member full pin')
    pdf=uploads['antipedal_centroids.pdf']
    need(members['antipedal_centroids.pdf']['bytes']==len(pdf) and members['antipedal_centroids.pdf']['sha256']==sha(pdf),'PDF bound to exact manifest')
    logical={'antipedal_centroids.pdf':pdf}
    with zipfile.ZipFile(io.BytesIO(uploads['antipedal_centroids_support.zip'])) as archive:
        entries=archive.infolist();names=[e.filename for e in entries]
        expected=(set(members)-{'antipedal_centroids.pdf'})|{'PACKAGE_MANIFEST.json'}
        need(len(names)==len(set(names)) and set(names)==expected,'Exact complete support ZIP member set')
        for entry in entries:
            relative(entry.filename);mode=entry.external_attr>>16
            need(not entry.is_dir() and not stat.S_ISLNK(mode) and stat.S_IFMT(mode) in (0,stat.S_IFREG) and not entry.flag_bits&1,'Safe regular unencrypted ZIP member')
            body=archive.read(entry)
            if entry.filename=='PACKAGE_MANIFEST.json':need(body==package_body,'Archive exact reviewed package manifest')
            else:
                need(len(body)==members[entry.filename]['bytes'] and sha(body)==members[entry.filename]['sha256'],'Full logical support body mismatch')
                logical[entry.filename]=body
    return logical

def full_delta(before,after):
    def pin(body):return None if body is None else {'bytes':len(body),'sha256':sha(body)}
    return [{'relative':name,'before':pin(before.get(name)),'after':pin(after.get(name))}
            for name in sorted(set(before)|set(after)) if before.get(name)!=after.get(name)]

def validate_revision_relationship(revision,before,after,logical_names,old_hash,new_hash,fixture):
    need(revision.get('schema')=='pr140-actual-R1-to-final-package-repair-relationship/v1' and
         revision['R1_reviewed_manifest_sha256']==old_hash and revision['final_package_manifest_sha256']==new_hash,'Exact raw precursor/final relationship')
    if not fixture:
        need(revision['owner']=='ROOT' and revision['fixture_only'] is False and
             type(revision['actual_ROOT_PID']) is int and revision['actual_ROOT_PID']>0,'Actual ROOT relationship observation')
        need(len(before)==len(after)==29,'Complete actual 29-member packages')
    else:need(revision['fixture_only'] is True,'Synthetic relationship remains explicitly a fixture')
    rows=revision['full29_member_comparison']
    need(isinstance(rows,list) and len(rows)==len(before) and set(before)==set(after) and
         {r['relative'] for r in rows}==set(before),'Complete unique raw working-member coverage')
    for row in rows:
        name=row['relative']
        for role,body in [('R1',before[name]),('final_R2',after[name])]:
            pin=row[role];need(pin['bytes']==len(body) and pin['sha256']==sha(body),'Complete raw revision member-body pin')
        need(row['full_body_equal'] is (before[name]==after[name]),'Truthful raw full-body equality')
    changed={name for name in before if before[name]!=after[name]}
    need(set(revision['changed_working_files'])==changed and
         set(revision['changed_publication_members'])==changed&logical_names,'Exact raw changed-member sets')
    need(revision['R1_mandatory_findings']==[] and revision['optional_bibliography_correction_applied'] is True and
         revision['TEX_exact_single_printed_title_substitution'] is True and
         revision['all_mathematical_proof_text_equations_assumptions_and_code_unchanged'] is True and
         revision['all_metadata_verification17_README_audit_summary_license_unchanged'] is True and
         revision['new_fresh_R2_review_of_final_package_is_PASS_with_no_findings'] is True and
         revision['R1_is_not_claimed_to_have_reviewed_final_changed_bytes'] is True and
         revision['repair_loop_fulfilled_by_dated_R1_then_repair_then_fresh_clean_final_R2'] is True,'Truthful documented reviewed repair loop')
    if not fixture:
        old=b'Eighty New Invariants of N-Periodics in the Elliptic Billiard'
        new=b'Eighty New Invariants in the Elliptic Billiard'
        need(before['antipedal_centroids.tex'].count(old)==1 and
             before['antipedal_centroids.tex'].replace(old,new,1)==after['antipedal_centroids.tex'],'Only exact printed-title substitution in TEX')
        need(changed=={'PACKAGE_MANIFEST.json','antipedal_centroids.log','antipedal_centroids.pdf',
             'antipedal_centroids.tex','antipedal_centroids_support.zip','priority_and_provenance.md'},'Exact approved six-file correction, no hidden proof/metadata/code change')

def metadata_fields(actual,intended,doi,record_id):
    need(isinstance(actual,dict) and isinstance(intended,dict) and intended,'Complete metadata dictionaries')
    need(all(k in actual and equal(actual[k],v) for k,v in intended.items()),'Every supplied metadata field remains exact')
    extras={k:v for k,v in actual.items() if k not in intended}
    need(set(extras)<={'doi','imprint_publisher','prereserve_doi'},'Only authenticated Zenodo provider additions allowed')
    if 'doi' in extras:need(extras['doi']==doi,'Provider DOI addition')
    if 'imprint_publisher' in extras:need(extras['imprint_publisher']=='Zenodo','Provider imprint addition')
    if 'prereserve_doi' in extras:
        need(equal(extras['prereserve_doi'],{'doi':doi,'recid':record_id}),'Provider reserved DOI/record id')
    return extras

def _receipt(obj,role,fixture):
    need(isinstance(obj,dict) and obj.get('schema')=='pr140-native-data-'+role+'/v1','Explicit normalized '+role+' schema')
    if fixture:
        need(obj.get('fixture') is True and obj.get('actual_receipt') is False,'Label synthetic receipt as fixture, never actual')
    else:
        need(obj.get('actual_receipt') is True and obj.get('fixture') is False and obj.get('template_only') is False and
             type(obj.get('actual_ROOT_PID')) is int and obj['actual_ROOT_PID']>0,'Actual accepted ROOT receipt required: '+role)
    stamp(obj['UTC'])

def _build(request_bytes,bodies,trusted_request_sha256,fixture):
    need(type(request_bytes) is bytes and digest(trusted_request_sha256) and sha(request_bytes)==trusted_request_sha256,'Out-of-band accepted whole request SHA required')
    request=loads(request_bytes)
    need(request_bytes==canonical(request),'Canonical request bytes required')
    need(set(request)=={'schema','mode','UTC','source','prior','before','readonly','original','package','reviews','publication','tracker','merge','fresh_main','accepted_paths','accepted_support','review_repair_relationship','acceptance_inputs','original17_manifest','role_inputs','input_pins'},'All data choices explicit')
    need(request['schema']=='pr140-pure-native-data-request/v1' and request['mode']==('fixture' if fixture else 'actual'),'Actual and fixture APIs cannot be interchanged')
    now=stamp(request['UTC']);specs=request['input_pins']
    need(isinstance(specs,dict) and set(specs)==set(bodies) and 1<=len(specs)<=256,'Declared whole-body input set')
    for name,spec in specs.items():
        relative(name);need(set(spec)=={'bytes','sha256'} and type(spec['bytes']) is int and spec['bytes']>=0 and digest(spec['sha256']),'Full byte pin')
        need(type(bodies[name]) is bytes and len(bodies[name])==spec['bytes'] and sha(bodies[name])==spec['sha256'],'Input drift: '+name)
    used=set()
    def read(name):
        need(isinstance(name,str) and name in specs,'Undeclared input');used.add(name);return bodies[name]
    def obj(name):return loads(read(name))
    source,prior=obj(request['source']),obj(request['prior'])
    need(str(source.get('id'))==K and source.get('problem_number')==CODE and isinstance(prior,dict) and prior,'Full source/prior pair')
    sourcehash=sha(source['statement'].encode());pairhash=sha(json.dumps([source,prior],sort_keys=True).encode())
    if not fixture:need(sourcehash==STATEMENT and pairhash==REVIEW,'Fixed authenticated PR140 source pair')
    before_names={PREFIX+x for x in BACKEND}|{ATTEMPT+x for x in CANONICAL}
    need(set(request['before'])==before_names and set(request['readonly'])=={PREFIX+x for x in READONLY},'Exact fourteen writable/four readonly input scope')
    before={path:(read(label) if label is not None else None) for path,label in request['before'].items()}
    readonly={path:read(label) for path,label in request['readonly'].items()}
    need(all(before[PREFIX+x] is not None for x in BACKEND),'Complete merged backend preimages')
    need(all(before[ATTEMPT+x] is None for x in CANONICAL[:4]) and all(before[ATTEMPT+x] is not None for x in CANONICAL[4:]),'Fresh canonical metadata additions and merged README/log required')
    need(('## '+K+' —').encode() not in readonly[PREFIX+'SHORTLIST.md'],'Target SHORTLIST must remain absent and whole readonly')
    policy=loads(readonly[PREFIX+'policy.json']);need(type(policy.get('turn_limit')) is int and policy['turn_limit']==5,'Five-turn policy')
    original=obj(request['original']);_receipt(original,'original',fixture)
    need(original['original_head']==HEAD and original['original_budget']=='2/5' and original['original_structured_ledger_present'] is False and original['original17_preserved'] is True,'Original effort/archive custody')
    need(digest(original['original_queue_row_sha256']) and digest(original['original_author_log_sha256']),'Original row/log complete pins')
    if not fixture:validate_legacy_pins(original)
    merge=obj(request['merge']);_receipt(merge,'merge',fixture);provider=obj(merge['provider_response'])
    need(provider['number']==140 and provider['head']['sha']==HEAD and provider['base']['ref']=='main' and provider['merged'] is True,'Actual original-head merge required')
    need(provider['merge_commit_sha']==merge['merge_commit'] and provider['merged_at']==merge['merged_at'],'Merge raw-provider identity/time')
    if not fixture:need(oid(merge['merge_commit']) and https(provider['html_url']) and provider['html_url']=='https://github.com/AlecKriebel/Math/pull/140','Actual merge OID/URL')
    merged_at=stamp(merge['merged_at']);need(merged_at<=now,'Merge must precede preparation')
    fresh=obj(request['fresh_main']);_receipt(fresh,'fresh-main',fixture)
    need(fresh['merged_original_head']==HEAD and fresh['merge_commit']==merge['merge_commit'] and
         fresh['merge_ancestor_verified'] is True and equal(fresh['preimages'],request['before']) and
         equal(fresh['readonly'],request['readonly']) and fresh['complete_fresh_MAIN_preimages_verified'] is True,'Fresh merged MAIN and complete pinned preimages')
    if not fixture:need(oid(fresh['MAIN_commit']) and fresh['direct_remote_MAIN']==fresh['MAIN_commit'],'Fresh direct remote MAIN identity')
    need(merged_at<=stamp(fresh['UTC'])<=now,'Fresh merged preimage chronology')
    package=request['package'];need(set(package)=={'manifest','upload_files'},'Final package choices')
    package_body=read(package['manifest']);package_hash=sha(package_body);package_manifest=loads(package_body)
    uploads=package['upload_files'];need(isinstance(uploads,dict) and 1<=len(uploads)<=8,'Bounded exact upload inventory')
    upload_bodies={relative(name):read(label) for name,label in uploads.items()}
    need(set(upload_bodies)=={'antipedal_centroids.pdf','antipedal_centroids_support.zip'} and
         package_manifest['schema']=='k405-publication-package-manifest/v1','Exact current PDF/support archive package')
    logical=package_contents(package_body,upload_bodies)
    reviews=request['reviews'];need(isinstance(reviews,list) and 2<=len(reviews)<=8 and len(set(reviews))==len(reviews),'Distinct ordered whole-package review receipts')
    reviewers=[];review_objects=[];review_hashes=[]
    for label in reviews:
        review=obj(label);_receipt(review,'clean-package-review',fixture)
        reviewed_body=read(review['reviewed_manifest']);review_hash=sha(reviewed_body)
        need(review['package_manifest_sha256']==review_hash and review['reviewed_manifest_sha256']==review_hash and
             review['whole_package_reviewed'] is True and review['mandatory_findings']==[] and
             review['verdict']=='PASS','Truthful complete reviewed manifest, no unresolved mandatory finding')
        reviewers.append(review['reviewer_identity']);review_objects.append(review);review_hashes.append(review_hash)
    need(all(isinstance(r,str) and r for r in reviewers) and len(set(reviewers))==len(reviewers),'Fresh distinct reviewer identities')
    need(review_hashes[-1]==package_hash and all(stamp(a['UTC'])<=stamp(b['UTC']) for a,b in zip(review_objects,review_objects[1:])),'Fresh last independent review covers final package')
    repair_label=request['review_repair_relationship'];repair=None;revision_body=None;clean_gate_body=None
    different=[i for i,h in enumerate(review_hashes) if h!=package_hash]
    if different:
        need(different==[0] and isinstance(repair_label,str),'Only first preserved precursor may differ with complete repair relationship')
        repair=obj(repair_label);_receipt(repair,'review-repair',fixture)
        need(repair['from_review']==reviews[0] and repair['to_review']==reviews[-1] and
             repair['from_manifest']==review_objects[0]['reviewed_manifest'] and
             repair['to_manifest']==package['manifest'],'Exact precursor/final reviewer and manifest relationship')
        precursor_body=read(repair['from_manifest'])
        prior_uploads={relative(name):read(label) for name,label in repair['from_upload_files'].items()}
        precursor_logical=package_contents(precursor_body,prior_uploads)
        need(equal(repair['complete_logical_member_delta'],full_delta(precursor_logical,logical)) and
             repair['complete_logical_member_delta'],'Full exact precursor/final member-body delta, not relabeled R1')
        extra=repair['additional_working_bodies'];need(set(extra)=={'antipedal_centroids.log'},'Complete additional compilation-log body pair')
        full_before={**precursor_logical,'PACKAGE_MANIFEST.json':precursor_body,'antipedal_centroids_support.zip':prior_uploads['antipedal_centroids_support.zip']}
        full_after={**logical,'PACKAGE_MANIFEST.json':package_body,'antipedal_centroids_support.zip':upload_bodies['antipedal_centroids_support.zip']}
        for name,labels in extra.items():
            need(set(labels)=={'before','after'},'Exact full working-body pair')
            full_before[name]=read(labels['before']);full_after[name]=read(labels['after'])
        revision_body=read(repair['raw_revision_receipt']);revision=loads(revision_body)
        validate_revision_relationship(revision,full_before,full_after,set(logical),review_hashes[0],package_hash,fixture)
        clean_gate_body=read(repair['clean_gate'])
        gate=loads(clean_gate_body)
        need(gate['schema']=='pr140-root-clean-publication-gate/v1' and gate['R1_mandatory_findings']==[] and
             gate['R1_optional_printed_title_correction_globally_applied'] is True and
             gate['R1_reviewed_candidate_preserved'] is True and
             gate['fresh_new_independent_R2_has_no_mandatory_or_optional_findings'] is True and
             gate['package_manifest_sha256']==package_hash,'Actual documented correction and fresh final clean-review gate')
        need(stamp(repair['UTC'])<=now,'Relationship observed before current preparation')
        if not fixture:
            need(review_hashes[0]=='0d4f2a1fe22d06a787712b60821d477b54880c63c3f5716307a7a2eb0cf4b00f' and
                 sha(clean_gate_body)=='57875b4262f147550b19f00a8443daacb889e4f2dd2d6bb116291bee86fdcf11','Actual preserved R1 and genuine clean-package gate')
    else:need(repair_label is None,'No invented repair relationship for same-package reviews')
    pub=obj(request['publication']);_receipt(pub,'publication',fixture);metadata_body=read(pub['metadata_response']);metadata=loads(metadata_body)
    doi=pub['version_DOI']
    if fixture:need(doi=='FIXTURE_DOI_NOT_A_PUBLICATION','Fixture DOI must be visibly unusable')
    else:need(re.fullmatch(r'10\.5281/zenodo\.[1-9][0-9]*',doi) is not None,'Actual version DOI required')
    need(pub['package_manifest_sha256']==package_hash and pub['original_head']==HEAD and pub['published'] is True and
         metadata['doi']==doi and (metadata.get('submitted') is True or metadata.get('is_published') is True),'Actual final package/DOI/full metadata binding')
    if not fixture:need(str(metadata['id'])==doi.rsplit('.',1)[1] and pub['record_URL']=='https://zenodo.org/records/'+str(metadata['id']),'Actual record/version URL')
    need(isinstance(metadata.get('metadata'),dict) and metadata['metadata'],'Full publication descriptive metadata required')
    need(set(pub['downloaded_files'])==set(uploads),'All actual publication files downloaded')
    intended_metadata=loads(logical['metadata.json'])
    need(equal(intended_metadata,loads(logical['zenodo-deposit.json'])['metadata']),'Exact supplied package/deposit metadata')
    provider_additions=metadata_fields(metadata['metadata'],intended_metadata,doi,metadata['id'])
    need(all(stamp(review['UTC'])<=stamp(pub['UTC']) for review in review_objects),'Whole-package reviews precede actual publication')
    shape=pub['metadata_file_schema'];need(shape in ('record','deposition'),'Explicit raw Zenodo metadata schema')
    key,size=('key','size') if shape=='record' else ('filename','filesize')
    declared=metadata['files'];need(isinstance(declared,list) and len(declared)==len(uploads) and len({f[key] for f in declared})==len(declared),'Exact record file inventory')
    bykey={f[key]:f for f in declared};need(set(bykey)==set(uploads),'No missing/extra publication file')
    for name,body in upload_bodies.items():
        downloaded=read(pub['downloaded_files'][name]);need(downloaded==body,'Full uploaded/downloaded body mismatch')
        checksum=('md5:' if shape=='record' else '')+hashlib.md5(body).hexdigest()
        need(bykey[name][size]==len(body) and bykey[name]['checksum']==checksum,'Record complete file size/checksum')
    tracker=obj(request['tracker']);_receipt(tracker,'tracker',fixture)
    need(tracker['spreadsheet_id']==SHEET and tracker['gid']==GID and tracker['version_DOI']==doi and tracker['original_head']==HEAD,'Actual target spreadsheet/DOI identity')
    cells=tracker['cells'];row=tracker['row'];need(type(row) is int and row>=2 and isinstance(cells,list) and len(cells)==4 and all(isinstance(c,str) for c in cells),'Exact four tracker cells')
    selected="'Math Puzzles'!A"+str(row)+':D'+str(row)
    need(tracker['range']==selected and cells[0]=='https://arxiv.org/abs/2004.12497' and cells[2]=='https://doi.org/'+doi and K+' / '+CODE in cells[3],'Exact source/range/DOI/notes')
    need(cells[1]=='' or (tracker.get('existing_chat_authorized') is True and https(cells[1])),'Blank or separately authorized existing chat URL')
    append=obj(tracker['append_response']);readback=obj(tracker['row_readback_response'])
    update=append['updates'];need(update['updatedRange']==selected and update['updatedRows']==1 and update['updatedColumns']==4 and update['updatedCells']==4 and update['updatedData']['values']==[cells],'Actual append four-cell response')
    need(readback['range']==selected and readback['values']==[cells],'Actual exact four-cell row readback')
    need(stamp(pub['UTC'])<=stamp(tracker['UTC'])<=merged_at,'Actual publication, tracker then merge chronology')
    paths=request['accepted_paths'];need(set(paths)=={'proof','author_checker','independent_checker','publication_package','original_archive'},'Explicit accepted support path choices')
    for value in paths.values():relative(value)
    need(paths['original_archive'].endswith('/audits/pr140_5100023/original'),'Preserved original archive link')
    support=request['accepted_support'];need(set(support)=={'proof','author_checker','independent_checker'},'Explicit full accepted repair bodies required')
    allowed_support={
      'proof':{'2ef6528382d380d435fe085c7a760b62cf2202484a082b2cff0cfc465ae5090d',sha(logical['antipedal_centroids.tex'])},
      'author_checker':{'f5ba54e69a5089f7c25c6926b983cdb4700ad6484010cf7dd6a53067808c232e',sha(logical['verification/author_exact.py'])},
      'independent_checker':{'5503341c648fe5bdab3c34bf59ae137d48c906ef8349a0d01af8aacdc0d6cd17',sha(logical['verification/independent_exact.py'])}}
    for role,label in support.items():
        need(sha(read(label)) in allowed_support[role],'Link only accepted repair or exact published support body; original checker output is not repaired evidence')
    authentication_body=read(request['acceptance_inputs']);authentication=loads(authentication_body)
    original_manifest_body=read(request['original17_manifest'])
    if fixture:
        need(authentication.get('fixture_only') is True and authentication.get('actual_ROOT_PID') is None,'Fixture authentication cannot describe a real ROOT action')
    else:
        need(authentication.get('schema')=='pr140-actual-native-publication-inputs/v1' and authentication.get('owner')=='ROOT' and authentication.get('fixture_only') is False and type(authentication.get('actual_ROOT_PID')) is int and authentication['actual_ROOT_PID']>0,'Actual ROOT input authentication')
        need(sha(original_manifest_body)=='687a08ae8eba9789f65a8a4c64650b9de7ea2ac6a4b970710cc9a33b83ebb672','Frozen whole original17 manifest')
    need(authentication['original_head']==HEAD and authentication['review_hash']==pairhash and authentication['statement_hash']==sourcehash and authentication['original_effort']=='2/5' and authentication['new_central_proof_search_turns']==0,'ROOT source/effort identity')
    need(authentication['package_finally_reviewed_and_published'] is True and authentication['actual_tracker_row_verified'] is True and authentication['actual_original_head_merge_verified'] is True and authentication['DOI']==doi and authentication['package_manifest_pin']['sha256']==package_hash,'ROOT actual publication/tracker/merge binding')
    need(authentication['PR140_merge']['original_head']==HEAD and authentication['PR140_merge']['commit']==merge['merge_commit'] and authentication['PR140_merge']['merged_at']==merge['merged_at'],'ROOT exact original-head merge')
    need(authentication['sheet']['spreadsheet_id']==SHEET and authentication['sheet']['gid']==GID and authentication['sheet']['title']=='Math Puzzles' and authentication['sheet']['range']==selected and authentication['sheet']['values']==cells,'ROOT exact tracker cells')
    roles={'package','whole_package_R1','whole_package_R2','publication','tracker','merge'}
    need(set(authentication['roles'])==roles and set(request['role_inputs'])==roles,'Six actual authority role bodies')
    for role,label in request['role_inputs'].items():
        body=read(label);spec=authentication['roles'][role]
        need(spec['bytes']==len(body) and spec['sha256']==sha(body),'Complete actual authority role body')
    if not fixture:
        actual_pub=loads(read(request['role_inputs']['publication']))
        need(actual_pub.get('schema')=='pr140-actual-published-fullbody-verification/v1' and actual_pub['published'] is True and
             actual_pub['DOI']==doi and actual_pub['package_manifest_sha256']==package_hash and
             actual_pub['authenticated_deposition_sha256']==sha(metadata_body) and
             equal(actual_pub['metadata'],intended_metadata),'Raw complete deposition and every supplied field bound to actual ROOT publication receipt')
        dep_pin=authentication['raw_deposition_pin']
        need(dep_pin['bytes']==len(metadata_body) and dep_pin['sha256']==sha(metadata_body) and
             authentication['intended_metadata_exactly_matches_all_supplied_provider_fields'] is True and
             set(authentication['provider_added_metadata_fields'])==set(provider_additions),'ROOT complete raw deposition and provider additions')
        if repair is not None:
            need(authentication['R1_reviewed_manifest_sha256']==review_hashes[0] and
                 authentication['R2_final_reviewed_manifest_sha256']==package_hash,'ROOT truthful accepted reviewed manifests')
            pin=authentication['review_relationship_pin']
            need(pin['bytes']==len(revision_body) and pin['sha256']==sha(revision_body),'Actual ROOT repair relationship full-body pin')
    need(stamp(authentication['UTC'])<=now,'ROOT authentication precedes current preparation')
    note=('Accepted scoped k405 centroid theorem for even least period N>=4, distinct vertices and nondegenerate confocal elliptical caustics, including primitive stars and either orientation; full-line unweighted unprimed antipedals. Source least-period reading qualified. Exact later Ferudun overlap credited; September 30 PR precedes the specific October 1 deposit, without absolute/exclusive priority or independent-discovery claim. Published AI-assisted unrefereed note. Original 2/5, validation 0.')
    if fixture:note='FIXTURE ONLY, NOT PUBLICATION OR ACCEPTANCE. '+note
    accepted={'schema':'pr140-scoped-native-acceptance/v1','fixture':fixture,'actual_receipt':not fixture,
      'at':request['UTC'],'PR':140,'id':K,'literal_status':'claimed_solved','literal_native_status':'claimed_solved','original_effort':'2/5','original_head':HEAD,
      'review_hash':pairhash,'statement_hash':sourcehash,'exact_scope':CLAIM,
      'source_least_period_qualification':'Supported primitive-period interpretation, not a formal source definition.',
      'later_exact_overlap_DOI':'10.5281/zenodo.23092466','absolute_priority_established':False,
      'exclusive_theorem_novelty_over_later_note':False,'independent_discovery_established':False,
      'original_budget':'2/5','new_central_proof_search_turns':0,'original_structured_ledger_present':False,
      'package_manifest_sha256':package_hash,'clean_review_receipt_labels':reviews,
      'actual_reviewed_manifest_sha256s':review_hashes,'review_repair_relationship_label':repair_label,
      'review_repair_relationship_sha256':sha(read(repair_label)) if repair_label is not None else None,
      'provider_metadata_additions':provider_additions,
      'publication_receipt_label':request['publication'],'tracker_receipt_label':request['tracker'],
      'merge_receipt_label':request['merge'],'fresh_MAIN_receipt_label':request['fresh_main'],
      'original_archive':paths['original_archive'],'accepted_paths':paths,'input_receipt_pins':specs,
      'native_publication_or_local_installation_performed':False}
    imported={'schema':'pr140-dated-native-import-baseline/v1','at':request['UTC'],'id':K,'status':'claimed_solved','turns_used':2,
      'review_hash':pairhash,'statement_hash':sourcehash,'original_budget':'2/5','original_head':HEAD,
      'original_structured_ledger_present':False,'new_central_proof_search_turns':0,
      'original_queue_row_sha256':original['original_queue_row_sha256'],'original_author_log_sha256':original['original_author_log_sha256'],
      'event':'dated_import_of_authenticated_author_count','provenance':'Present dated import of legacy submitted effort; not a recovered original structured event.','fixture':fixture}
    accepted['dated_import_baseline']=imported
    accepted['legacy_import']=imported
    accepted['actual_acceptance_inputs_sha256']=sha(authentication_body)
    accepted['original17_manifest_sha256']=sha(original_manifest_body)
    accepted['actual_merge_commit']=merge['merge_commit']
    accepted['actual_merged_at']=merge['merged_at']
    ass0=loads(before[PREFIX+'assessments.json']);states=loads(before[PREFIX+'state.json']);rows=loads(before[PREFIX+'catalog.json'])
    need(isinstance(ass0,dict) and K in ass0 and isinstance(states,dict) and K not in states,'Target existing-state reconciliation required')
    need(isinstance(rows,list) and len({r['id'] for r in rows})==len(rows) and sum(r['id']==K for r in rows)==1,'Catalog identity set')
    dependency=loads(readonly[PREFIX+'manifest.json'])
    need(dependency['records']==len(rows),'Complete catalog count matches immutable manifest')
    if not fixture:
        need(dependency['revision']=='37e53eabe540fb458758e198be61634bd02ee008' and sha(readonly[PREFIX+'queue.py'])=='f72aee023f837bad092da58531c2cc069ce2cf094e835d090221107d20f07ab2','Accepted readonly dataset/runtime source identity')
    target=next(r for r in rows if r['id']==K);historical=ass0[K]
    need(target['problem_number']==CODE and target['review_hash']==historical['review_hash']==pairhash and
         target['statement_hash']==historical['statement_hash']==sourcehash and target['local_status']=='queued' and
         type(target['turns_used']) is int and target['turns_used']==0,'Fixed target source identity/queued native preimage')
    need(historical.get('id')==K,'Historical target assessment identity')
    overlay={'note':note,'rationale':'Opposite-edge focal antipedal identity plus finite circle-action half-period pairing and unconstrained first variation proves the scoped all-period result. The written proof supplies dynamics; exact checks are supplements.',
      'remaining_gap':'No accepted mathematical gap for the stated primitive-even scope. Absolute/exclusive priority and independent discovery remain unestablished. Native integration and final program bookkeeping await later actual receipts.',
      'first_experiment':'Preserve original17 and legacy effort; install only separately reviewed accepted repairs and actual publication evidence, never relabel original checker outputs as repaired accepted runs.',
      'sources':list(dict.fromkeys(historical.get('sources',[])+['https://doi.org/'+doi,'https://doi.org/10.5281/zenodo.23092466'])),
      'reviewed_at':request['UTC'],'original_budget':'2/5','new_central_proof_search_turns':0,'original_structured_ledger_present':False,
      'publication_DOI':doi,'package_manifest_sha256':package_hash,'native_import_provenance':accepted}
    assessment={**historical,**overlay};ass={**ass0,K:assessment};state={**states,K:imported}
    projected={**target,'local_status':'claimed_solved','turns_used':2,'eligible':False,'rank':None,'desk_note':note}
    catalog=[projected if r['id']==K else r for r in rows]
    need([r for r in catalog if r['id']!=K]==[r for r in rows if r['id']!=K],'Unrelated complete catalog rows/order/ranks')
    need({k:v for k,v in ass.items() if k!=K}=={k:v for k,v in ass0.items() if k!=K} and {k:v for k,v in state.items() if k!=K}==states,'Unrelated assessment/state records')
    summary=loads(before[PREFIX+'summary.json']);summary.update(records=len(catalog),eligible=sum(r['eligible'] for r in catalog),assessed=len(ass),holds=dict(collections.Counter(h.split(':')[0] for r in catalog for h in r['holds'])))
    publication_evidence={'schema':'pr140-published-native-evidence/v1','fixture':fixture,'actual_receipt':not fixture,
      'version_DOI':doi,'DOI':doi,'Sheet_range':selected,'record_URL':pub['record_URL'],'full_publication_metadata':metadata,
      'original_budget':'2/5','new_central_proof_search_turns':0,'actual_acceptance_inputs_sha256':sha(authentication_body),
      'uploaded_downloaded_body_pins':{n:{'bytes':len(b),'sha256':sha(b)} for n,b in upload_bodies.items()},
      'package_manifest_sha256':package_hash,'review_hash':pairhash,'statement_hash':sourcehash,'original_head':HEAD,
      'tracker_range':selected,'tracker_four_cells':cells,'publication_receipt_pin':specs[request['publication']],
      'tracker_receipt_pin':specs[request['tracker']],'actual_merge_commit':merge['merge_commit'],'actual_merged_at':merge['merged_at']}
    readme=('\n\n## '+request['UTC']+' — scoped publication acceptance metadata\n\n'+note+'\n\n'
      'Version DOI: '+doi+'. Accepted proof: '+paths['proof']+'. Accepted explicit-guard checkers: '+paths['author_checker']+' and '+paths['independent_checker']+'. Publication package: '+paths['publication_package']+'. Preserved original17 audit archive: '+paths['original_archive']+'. Original verifier outputs remain historical; accepted repaired runs are separately bound. No human peer review is claimed. Native publication/local installation and final program completion are not asserted by these proposed bytes.\n').encode()
    log=('\n\n'+request['UTC']+': Proposed native metadata overlay after actual original-head merge '+merge['merge_commit']+', publication '+doi+' and exact four-cell tracker readback '+selected+'. Math and bounded qualified priority accepted; legacy effort 2/5 imported at this time, validation adds zero central proof-search turns. Original17 retained; fresh MAIN preimages and unrelated rows/ranks/scores/holds/history are preserved. Native integration 80% pending actual scoped publication/local readback and final program bookkeeping. AI-assisted unrefereed result; no absolute/exclusive priority or independent-discovery claim. '+('FIXTURE ONLY; none of these fixture actions occurred. ' if fixture else '')+'\n').encode()
    outputs={PREFIX+'assessments.json':canonical(ass),PREFIX+'state.json':canonical(state),
      PREFIX+'history.jsonl':append_event(before[PREFIX+'history.jsonl'],imported),
      PREFIX+'assessment_history.jsonl':append_event(before[PREFIX+'assessment_history.jsonl'],{'id':K,**assessment}),
      PREFIX+'catalog.json':canonical(catalog),PREFIX+'ranking.csv':csv_scoped(before[PREFIX+'ranking.csv'],projected),
      PREFIX+'summary.json':canonical(summary),PREFIX+'QUEUE.md':queue_overlay(before[PREFIX+'QUEUE.md'],note,doi),
      ATTEMPT+'assessment.json':canonical(assessment),ATTEMPT+'HISTORICAL_DESK_ASSESSMENT.json':canonical(historical),
      ATTEMPT+'PUBLICATION_EVIDENCE.json':canonical(publication_evidence),ATTEMPT+'ACCEPTANCE_EVIDENCE.json':canonical(accepted),
      ATTEMPT+'README.md':before[ATTEMPT+'README.md']+readme,ATTEMPT+'RESEARCH_LOG.md':before[ATTEMPT+'RESEARCH_LOG.md']+log}
    need(set(outputs)==before_names and used==set(specs),'Exact fourteen outputs/all authenticated inputs consumed')
    return {'fixture':fixture,'status':'FIXTURE_NOT_AUTHORITY' if fixture else 'PROPOSED_AFTER_VERIFIED_ACTUAL_RECEIPTS_NOT_INSTALLED',
            'outputs':outputs,'preserved_readonly':readonly,'accepted_evidence':accepted}

def build_verified(request_bytes,bodies,trusted_request_sha256):
    """ROOT supplies genuine complete custody and an independently accepted SHA."""
    return _build(request_bytes,bodies,trusted_request_sha256,False)

def build_fixture(request_bytes,bodies):
    """Synthetic source controls only; output can never carry actual authority."""
    return _build(request_bytes,bodies,sha(request_bytes),True)
