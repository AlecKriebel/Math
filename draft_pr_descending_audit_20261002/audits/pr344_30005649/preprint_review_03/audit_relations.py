"""Owned, read-only relations check; never consult historical external paths."""
import datetime, hashlib, json, pathlib, stat, zipfile
R=pathlib.Path(__file__).resolve().parent
P=R/'packet/qss-self-duality-verification'
def require(condition,message):
    if not condition: raise ValueError(message)
def pin(p):
    require(p.is_file() and not p.is_symlink(),f'not regular: {p}')
    return dict(size=p.stat().st_size,mode=oct(stat.S_IMODE(p.stat().st_mode)),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def load(p): return json.loads(p.read_text())
def bound(p,b):
    x=pin(p);size=b.get('size',b.get('bytes'))
    require(x['size']==size and x['sha256']==b['sha256'],f'bytes mismatch {p}')
    if 'mode' in b: require(int(x['mode'],8)==int(b['mode'],8),f'mode mismatch {p}')
def check():
    c=load(R/'candidate_inputs.json')['inputs'];require(len(c)==8,'eight author inputs required')
    for name,b in c.items(): bound(R/'candidate'/name,b)
    for name,b in load(R/'primary_inputs.json')['sources'].items(): bound(R/'sources'/name,b)
    for name,b in load(R/'supporting_inputs.json')['inputs'].items(): bound(R/name,b)
    members=load(R/'public_members.json')['members'];require(len(members)==33,'33 members required')
    with zipfile.ZipFile(R/'candidate/qss-self-duality-verification.zip') as z:
        names=z.namelist();require(len(names)==len(set(names))==33,'duplicate/extra ZIP names')
        require(set(names)=={b['path'] for b in members},'ZIP inventory')
        for b in members:
            n=b['path'];i=z.getinfo(n);data=z.read(n)
            require(not i.is_dir() and not pathlib.PurePosixPath(n).is_absolute() and '..' not in pathlib.PurePosixPath(n).parts,'unsafe ZIP member')
            require(i.file_size==b['size'] and i.CRC==b['crc'] and stat.S_IMODE(i.external_attr>>16)==int(b['mode'],8),'ZIP metadata')
            require(stat.S_ISREG(i.external_attr>>16),'ZIP regular file mode')
            require(hashlib.sha256(data).hexdigest()==b['sha256'],'ZIP content')
            bound(R/'packet'/n,b);require((R/'packet'/n).read_bytes()==data,'extracted duplicate')
    require({str(q.relative_to(R/'packet')) for q in (R/'packet').rglob('*') if q.is_file()}==set(names),'extracted complete inventory')
    manifest=load(P/'MANIFEST.json')['files']
    require(set(manifest)=={str(q.relative_to(P)) for q in P.rglob('*') if q.is_file()}-{'MANIFEST.json'},'32 manifest payloads')
    for n,b in manifest.items():bound(P/n,b)
    for b in load(P/'priority/PUBLIC_MANIFEST.json')['payloads']:bound(P/'priority'/b['path'],b)
    s=load(P/'SOURCE_IDENTITY.json');derivatives=[]
    for n,b in s['reviewed_original_control_pins'].items():
        original=R/'original_controls'/pathlib.PurePosixPath(n).name;bound(original,b)
        text=original.read_text()
        if n in s['control_derivations']:
            d=s['control_derivations'][n];bound(original,d['reviewed_original'])
            for edit in d['edits']:
                require(text.count(edit['literal_old'])==edit['occurrences'],f'literal count {n}')
                text=text.replace(edit['literal_old'],edit['literal_new'])
            require(text.encode()==(P/n).read_bytes(),f'exact derivative {n}')
            bound(P/n,d['public_derivative']);derivatives.append(n)
        else:require(original.read_bytes()==(P/n).read_bytes(),f'unchanged original {n}')
        bound(P/n,s['control_source_pins'][n])
    reg=(R/'candidate/intrinsic_formula_regressions.txt').read_text()
    insertion=s['control_derivations']['controls/verify_intrinsic.py']['edits'][3]
    require(insertion['literal_new']==reg+'def main():','actual eighth-input dependency')
    duplicate_pairs=[('qss-self-duality-note.tex','manuscript.tex'),('zenodo-deposit.json','zenodo-deposit.json'),('verify_supplement.py','verify_supplement.py'),('CONTROL_FORMULA_CORRECTION.md','CONTROL_FORMULA_CORRECTION.md')]
    for a,b in duplicate_pairs:require((R/'candidate'/a).read_bytes()==(P/b).read_bytes(),f'duplicate {a}')
    for b in load(P/'MECHANISM_SOURCES.json'):
        bound(R/'sources'/b['relative_path'],b)
    require(s['source_pdf_sha256']==pin(R/'sources/owr2023-42.pdf')['sha256'],'primary source identity')
    for stem in ('SOURCE_ONLY_FREEZE','FIRST_MATHEMATICAL_ASSESSMENT'):
        b=load(R/(stem+'.pin.json'));bound(R/b['path'],b)
    source=datetime.datetime.fromisoformat(load(R/'SOURCE_ONLY_FREEZE.pin.json')['written_utc'])
    first=datetime.datetime.fromisoformat(load(R/'FIRST_MATHEMATICAL_ASSESSMENT.pin.json')['written_utc'])
    candidate=datetime.datetime.fromisoformat(load(R/'receipts/snapshot-candidate.json')['started_utc'])
    unzip=datetime.datetime.fromisoformat(load(R/'receipts/extract-packet.json')['started_utc'])
    require(source<candidate<first<unzip,'independence chronology')
    receipt_count=0
    for file in sorted((R/'receipts').glob('*.json')):
        d=load(file);stem=file.stem
        start=datetime.datetime.fromisoformat(d['started_utc']);end=datetime.datetime.fromisoformat(d['ended_utc'])
        require(start.tzinfo is not None and end.tzinfo is not None and start<=end,'native receipt UTC relation')
        require(isinstance(d['command'],list) and bool(d['command']) and isinstance(d['exit_code'],int),'native receipt command/status')
        bound(R/'receipts'/(stem+'.stdout'),d['stdout']);bound(R/'receipts'/(stem+'.stderr'),d['stderr']);receipt_count+=1
    labels=('default','full','priority','honda','semilinear','intrinsic','integral_flag')
    for label in labels:
        a=R/'receipts'/('py314-'+label+'.stdout');b=R/'receipts'/('py312-'+label+'.stdout')
        require(a.read_bytes()==b.read_bytes(),f'complete cross-runtime equality {label}')
        for runtime in ('py314','py312'):
            d=load(R/'receipts'/(runtime+'-'+label+'.json'))
            require(d['exit_code']==0 and d['stderr']['size']==0 and d['watched_inputs_unchanged'],f'positive receipt {runtime}-{label}')
        if label not in ('default','full'):require(a.read_bytes()==(P/'expected'/(label+'.stdout')).read_bytes(),f'complete expected stream {label}')
    require((R/'receipts/py314-version.stdout').read_text().strip()=='Python 3.14.6','native system version')
    require((R/'receipts/py312-version.stdout').read_text().strip()=='Python 3.12.14','native bundled version')
    require((R/'receipts/independent-py314.stdout').read_bytes()==(R/'receipts/independent-py312.stdout').read_bytes(),'independent output equality')
    for runtime in ('py314','py312'):
        d=load(R/'receipts'/('independent-'+runtime+'.json'));require(d['exit_code']==0 and d['stderr']['size']==0,'independent native receipt')
    mutations=load(R/'mutation_summary.json')['mutations'];require(len(mutations)==8,'eight mathematical negative executions')
    for row in mutations:
        stem=row['receipt'];d=load(R/'receipts'/(stem+'.json'))
        require(d['exit_code']!=0 and not d['manifest_verifier_invoked'] and d['mathematical_rejection'],'direct negative execution')
        require(row['stderr']==(R/'receipts'/(stem+'.stderr')).read_text(),'negative complete stream relation')
        script=R/'mutants'/stem.split('-negative-')[1]/pathlib.Path(d['command'][-1]).name
        bound(script,d['mutant_control']);bound(P/'controls'/script.name,d['original_control'])
        text=(P/'controls'/script.name).read_text()
        if d['literal_old'] is not None:
            require(text.count(d['literal_old'])==1,'mutant literal unique')
            require(text.replace(d['literal_old'],d['literal_new']).encode()==script.read_bytes(),'exact mathematical mutant')
        else:require(text.encode()==script.read_bytes(),'Honda script unchanged')
        spec=load(script.parent/'construction.json');original=load(P/'controls/construction.json')
        if d['changed_input']:original['honda_basis_indices']=[0,1,3]
        require(spec==original,'mutant input relation')
    replay=load(R/'replay_summary.json')
    require(all(replay['complete_cross_runtime_output_equality'].values()) and replay['after_equal'],'replay summary')
    for name,folder in [('packet',P),('candidate',R/'candidate'),('original_controls',R/'original_controls')]:
        require({str(q.relative_to(folder)):pin(q) for q in sorted(folder.rglob('*')) if q.is_file()}==replay['before'][name],'watched frozen replay input')
    metadata=load(R/'candidate/zenodo-deposit.json')['metadata']
    require(metadata['creators'][0]['orcid']=='0009-0001-9320-500X' and metadata['publication_type']=='preprint' and metadata['license']=='cc-by-4.0','author/license/type metadata')
    require('unrefereed' in metadata['description'] and 'AI tools were used extensively' in metadata['description'] and 'No first-discovery or first-priority' in metadata['description'],'disclosures')
    return dict(author_inputs=8,zip_members=33,manifest_payloads=len(manifest),exact_control_derivatives=derivatives,unchanged_control_or_input=['check_realization.py','construction.json'],duplicate_pairs=duplicate_pairs,native_receipt_count=receipt_count,complete_streams_equal=True,independence_order_checked=True)
if __name__=='__main__':print(json.dumps(check(),indent=2,sort_keys=True))
