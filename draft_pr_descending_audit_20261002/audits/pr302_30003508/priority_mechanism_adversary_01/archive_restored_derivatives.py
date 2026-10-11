import datetime,hashlib,json,lzma,os,pathlib,sys
R=pathlib.Path(__file__).resolve().parent
history=json.loads((R/'SOURCE_COMPACTION.json').read_text())
record={'actual_pid':os.getpid(),'argv':sys.argv,'cwd':os.getcwd(),'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'semantics':'After ROOT requested retention of all historically pinned derivative bodies, the same retained scanned primary PDF was re-rendered by the same executable and parameters. Each reproduced PNG is authenticated against its original whole-body SHA and then retained complete in byte-lossless XZ. No hash-only retirement remains. Prior retirement event and failed budget assertion are retained as historical evidence.','restored_derivative_archives':[]}
for item in history['retired_render_derivatives']:
 o=item['original'];p=pathlib.Path(o['path']); b=p.read_bytes()
 assert len(b)==o['bytes'] and hashlib.sha256(b).hexdigest()==o['sha256'],p
 q=p.with_suffix('.png.xz');c=lzma.compress(b,preset=6);q.write_bytes(c)
 assert lzma.decompress(q.read_bytes())==b
 record['restored_derivative_archives'].append({'original':o,'archive':{'path':str(q),'bytes':len(c),'sha256':hashlib.sha256(c).hexdigest(),'mode':oct(q.stat().st_mode&0o777)},'reproduction_matches_original_exact_bytes':True,'decompression_verified':True,'new_renderer_native_execution':'process_evidence/restore_render_hansen1993/execution.json'})
 p.unlink()
record['ended_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
(R/'RESTORED_DERIVATIVE_ARCHIVES.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({'original_derivative_bodies_fully_restored_and_retained':len(record['restored_derivative_archives']),'stored_bytes':sum(p.stat().st_size for p in R.rglob('*') if p.is_file()),'operational_budget_note':'ROOT expressly preferred a small explained overrun to loss of historically pinned evidence.'}))
