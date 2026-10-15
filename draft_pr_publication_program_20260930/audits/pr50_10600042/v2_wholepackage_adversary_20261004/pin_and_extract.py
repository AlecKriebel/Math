import datetime, hashlib, json, pathlib, shutil, zipfile
root = pathlib.Path(__file__).resolve().parent
repo = root.parents[3]
a50 = root.parent
inputs = [repo/'AGENTS.md', repo/'unsolved_math_prioritization/AGENTS.md',
          a50/'original/source_record.json']
inputs += sorted((a50/'publication_package_v2').glob('*'))
primary = a50/'current_promotion_adversary_20261004/private'
inputs += [primary/x for x in ['survey.pdf','survey_publisher_correct.pdf','gks.pdf','kamada.pdf','kl.pdf',
                              'nencka_scan_153.webp','nencka_scan_154.webp','nencka_scan_004.webp']]
rows=[]
for p in inputs:
    if p.is_file():
        body=p.read_bytes()
        rows.append({'path':str(p.relative_to(repo)), 'bytes':len(body),'sha256':hashlib.sha256(body).hexdigest()})
record={'pinned_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'inputs':rows}
(root/'INPUT_PINS.json').write_text(json.dumps(record,indent=2)+'\n')
snap=root/'private'/'primary'
snap.mkdir(parents=True,exist_ok=True)
for p in inputs:
    if p.parent == primary:
        shutil.copyfile(p,snap/p.name)
ex=root/'private'/'extracted'
ex.mkdir(parents=True,exist_ok=True)
zpath=a50/'publication_package_v2/even-strand-markov-verification-v2.zip'
with zipfile.ZipFile(zpath) as z:
    bad=z.testzip()
    entries=[{'name':i.filename,'bytes':i.file_size,'compressed_bytes':i.compress_size,'date_time':i.date_time,
              'mode':oct(i.external_attr>>16),'sha256':hashlib.sha256(z.read(i.filename)).hexdigest()} for i in z.infolist()]
    assert all(not pathlib.PurePosixPath(i.filename).is_absolute() and '..' not in pathlib.PurePosixPath(i.filename).parts for i in z.infolist())
    z.extractall(ex)
(root/'ZIP_INVENTORY.json').write_text(json.dumps({'bad_crc_member':bad,'entries':entries},indent=2)+'\n')
print(json.dumps(record,indent=2))
print(json.dumps({'bad_crc_member':bad,'entries':entries},indent=2))
