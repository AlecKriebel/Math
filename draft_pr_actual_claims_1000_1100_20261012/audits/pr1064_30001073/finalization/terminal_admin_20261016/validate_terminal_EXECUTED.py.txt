#!/usr/bin/env python3
"""Actual local replays and negative controls; all mutations stay in own tmp."""
from pathlib import Path
import datetime, hashlib, io, json, os, shutil, struct, subprocess, sys, zipfile, zlib
HERE=Path(__file__).resolve().parent;AUDIT=HERE.parent.parent;PACKAGE=AUDIT/'preprint_v1_0';TMP=HERE/'tmp';KIT=TMP/'kit'
def need(c,m):
 if not c:raise RuntimeError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(p.read_text())
def write(p,d):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,indent=2)+'\n')
def rec(p,root):
 b=p.read_bytes();return {'path':p.relative_to(root).as_posix(),'bytes':len(b),'sha256':sha(b)}
def cli(script,*args,optimized=False):return [sys.executable,'-I','-B',*(['-O'] if optimized else []),str(script),*map(str,args)]

def raw_zip():
 b=(PACKAGE/'support.zip').read_bytes();pos=0;local=[];detail=[];date=((2026-1980)<<9|10<<5|14)
 while b[pos:pos+4]==b'PK\x03\x04':
  _,needver,flags,method,t,d,crc,cs,us,nl,xl=struct.unpack_from('<I5H3I2H',b,pos)
  name=b[pos+30:pos+30+nl].decode();data=b[pos+30+nl+xl:pos+30+nl+xl+cs];plain=zlib.decompress(data,-15)
  need(needver==20 and flags==0 and method==8 and t==0 and d==date and xl==0,'raw local header')
  need(len(plain)==us and zlib.crc32(plain)&0xffffffff==crc and plain==(PACKAGE/name).read_bytes(),'raw deflate/CRC/payload')
  local.append((name,pos,crc,cs,us));detail.append({'name':name,'local_header_offset':pos,'bytes':us,'compressed_bytes':cs,'crc32':crc,'sha256':sha(plain)});pos+=30+nl+xl+cs
 central=pos;centralrows=[]
 while b[pos:pos+4]==b'PK\x01\x02':
  _,made,nv,flags,method,t,d,crc,cs,us,nl,xl,cl,disk,internal,external,offset=struct.unpack_from('<I6H3I5H2I',b,pos)
  name=b[pos+46:pos+46+nl].decode();need(made==(3<<8|20) and nv==20 and flags==0 and method==8 and t==0 and d==date and xl==0 and cl==0 and disk==0 and internal==0 and external==0o100644<<16,'raw central header')
  centralrows.append((name,offset,crc,cs,us));pos+=46+nl+xl+cl
 need(local==centralrows,'all local/central records')
 count=len(local);need(struct.unpack_from('<I4H2IH',b,pos)==(0x06054b50,0,0,count,count,pos-central,central,0) and pos+22==len(b),'raw EOCD/no trailer')
 need([r[0] for r in local]==load(PACKAGE/'SUPPORT_ALLOWLIST.json')['members'],'raw member order')
 independent=io.BytesIO()
 with zipfile.ZipFile(independent,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9,strict_timestamps=True) as z:
  for n in [r[0] for r in local]:
   i=zipfile.ZipInfo(n,(2026,10,14,0,0,0));i.create_system=3;i.external_attr=0o100644<<16;i.internal_attr=0;i.compress_type=zipfile.ZIP_DEFLATED;z.writestr(i,(PACKAGE/n).read_bytes(),compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
 need(independent.getvalue()==b,'independent CLOSED zip rebuild')
 write(HERE/'CLOSED_ZIP.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'archive':rec(PACKAGE/'support.zip',PACKAGE),'members':detail,'raw_local_central_payload_CRC_EOCD_exact':True,'no_prefix_gaps_extra_comments_trailer':True,'independent_deflate9_rebuild_byte_equal':True,'python':sys.version,'zlib':zlib.ZLIB_VERSION,'cross_environment_compressor_identity_qualified':True})

def main():
 need(not KIT.exists(),'new validation scratch required');KIT.mkdir()
 need(not (HERE/'EXECUTIONS.jsonl').exists(),'preserve previous process receipts')
 rows=[];semantic=[];guards=[]
 def run(label,args,success=True,cwd=KIT,expected_text=None):
  p=subprocess.run(args,cwd=cwd,capture_output=True,text=True)
  row={'label':label,'argv':args,'cwd':str(cwd),'expected_success':success,'returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr};rows.append(row)
  with (HERE/'EXECUTIONS.jsonl').open('a') as f:f.write(json.dumps(row)+'\n');f.flush()
  need((p.returncode==0)==success,'unexpected process result '+label)
  if expected_text:need(expected_text in p.stderr,'wrong rejection reason '+label)
  if len(rows)%50==0:print('settled commands',len(rows),flush=True)
  return row
 raw_zip()
 with zipfile.ZipFile(PACKAGE/'support.zip') as z:z.extractall(KIT)
 archive=(PACKAGE/'support.zip').read_bytes();allow=load(PACKAGE/'SUPPORT_ALLOWLIST.json')['members']
 fullchecks=[];finite=[]
 for opt in [False,True]:
  mode='optimized' if opt else 'normal'
  run(mode+' canonical strict verifier',cli(PACKAGE/'verify_package.py','--require-deposit-binding',optimized=opt),cwd=PACKAGE)
  run(mode+' clean README verifier absent binding allowed',cli(KIT/'verify_package.py',optimized=opt))
  run(mode+' clean README diagnostics',cli(KIT/'run_checks.py','--out-dir','tmp/checks-'+mode,optimized=opt))
  c=load(KIT/('tmp/checks-'+mode+'/CHECKS.json'));fullchecks.append(c)
  need(len(c['receipts'])==17 and all((r['returncode']==0)==(r['name'] in ['original_normal','guard_normal','guard_optimized']) for r in c['receipts']),'actual diagnostic control receipts')
  project=lambda d:{k:v for k,v in d.items() if k not in ['completed_utc','python','platform']}
  baseline=load(PACKAGE/'support/history/root_reproduction/FINITE_CHECKS.json')
  original=load(KIT/('tmp/checks-'+mode+'/original_normal/FINITE_CHECKS.json'))
  gn=load(KIT/('tmp/checks-'+mode+'/guard_normal/FINITE_CHECKS.json'));go=load(KIT/('tmp/checks-'+mode+'/guard_optimized/FINITE_CHECKS.json'))
  need(project(original)==project(baseline),'full original projected JSON vs ROOT')
  need(project(gn)==project(go)==project(load(PACKAGE/'support/FRESH_GUARD_NORMAL.json'))==project(load(PACKAGE/'support/FRESH_GUARD_OPTIMIZED.json')),'full guard projected JSON differs')
  finite.append({'outer_mode':mode,'original_normal_asserts_active':True,'original_full_projected_JSON_equals_ROOT_baseline':True,'guard_full_projected_JSON_equals_both_frozen_baselines':True,'full_original':original,'full_guard_normal':gn,'full_guard_optimized':go})
  run(mode+' clean README archive build',cli(KIT/'build_archive.py','--output','tmp/rebuilt-'+mode+'.zip',optimized=opt))
  need((KIT/('tmp/rebuilt-'+mode+'.zip')).read_bytes()==archive,'README rebuilt complete bytes')
  run(mode+' clean README archive verify',cli(KIT/'verify_package.py','--archive','tmp/rebuilt-'+mode+'.zip',optimized=opt))
  run(mode+' required absent binding',cli(KIT/'verify_package.py','--require-deposit-binding',optimized=opt),False,expected_text='required deposit binding absent')
  checker=KIT/'support/history/reviews/package_04/independent_rigorous_controls.py'
  r=run(mode+' independent rigorous complete JSON',cli(checker,optimized=opt))
  normal=load(PACKAGE/'support/history/reviews/package_04/INDEPENDENT_NORMAL.json');optimized=load(PACKAGE/'support/history/reviews/package_04/INDEPENDENT_OPTIMIZED.json')
  need(json.loads(r['stdout'])==normal==optimized,'rigorous complete JSON differs')
  need(sha(r['stdout'].encode())=='3a78eac75ceb08583a0ae09927d944b296039aae15e17b1cddf8df708fe8e523','rigorous exact output bytes')
  for fault in ['endpoint','drop-entry-mass','drop-sequential']:run(mode+' independent rigorous fault '+fault,cli(checker,'--fault',fault,optimized=opt),False)
  fullchecks[-1]['independent_rigorous_full_JSON_equal_to_both_whole04_outputs']=True
 need({k:v for k,v in fullchecks[0].items() if k not in ['checked_utc','receipts']}=={k:v for k,v in fullchecks[1].items() if k not in ['checked_utc','receipts']},'full top runner semantic JSON differs')
 write(HERE/'CHECKER_REPLAY.json',{'scope':'Full mathematical objects compared, not count-only. Only original/guard runtime completed_utc/python/platform are projected; original executes normal only with active assertions. All other fields compared. Supplied Decimal diagnostics are finite non-interval corroboration; independent whole04 Fraction interval/formal-log controls are finite, not universal proof.','supplied_runner_records':fullchecks,'complete_finite_objects':finite,'rigorous_whole04_JSON_exact_equal_both_modes':True,'rigorous_faults_rejected_both_modes':3})
 # Add exact local excluded records for guard and required-binding controls.
 # The new stage seal does not exist until sealing; its test sentinel is labelled.
 excluded=load(PACKAGE/'EXCLUSION_LEDGER.json')['local_package_files']
 for name in excluded:
  if name=='support.zip':continue
  dest=KIT/name;dest.parent.mkdir(parents=True,exist_ok=True)
  if (PACKAGE/name).exists():shutil.copyfile(PACKAGE/name,dest)
  else:
   need(name=='TERMINAL_OUTPUT_PINS_20261016.json','unrecognized absent excluded input');write(dest,{'test_sentinel_only':'Future excluded dated stage-seal path; actual stage seal is created after all validation writes settle.'})
 protected=[p for p in sorted(KIT.rglob('*')) if p.is_file() and p.relative_to(KIT).parts[0]!='tmp' and p!=KIT/'support.zip']
 originals={p.relative_to(KIT).as_posix():p.read_bytes() for p in protected}
 def unchanged():
  for n,b in originals.items():need((KIT/n).read_bytes()==b,'protected fixture changed '+n)
 def refresh():
  m=json.loads(originals['SUPPORT_MANIFEST.json'])
  for r in m['entries']:
   b=(KIT/r['path']).read_bytes();r.update(bytes=len(b),sha256=sha(b))
  write(KIT/'SUPPORT_MANIFEST.json',m)
 def restore(*names):
  for n in [*names,'SUPPORT_MANIFEST.json']:(KIT/n).write_bytes(originals[n])
  unchanged()
 fixture=KIT/'tmp/alias';fixture.mkdir()
 probe=KIT/'tmp/writer_probe.py';marker=KIT/'tmp/writer_opened.txt'
 probe.write_text('import pathlib,runpy,sys,zipfile\nmarker=pathlib.Path(sys.argv[1]);script=sys.argv[2];sys.argv=sys.argv[2:]\noriginal=zipfile.ZipFile\ndef wrapper(*args,**kw):\n mode=kw.get("mode",args[1] if len(args)>1 else "r")\n if mode in ("w","a","x"):marker.write_text("opened")\n return original(*args,**kw)\nzipfile.ZipFile=wrapper\nrunpy.run_path(script,run_name="__main__")\n')
 status='TERMINAL_STATUS_20261016.json'
 variants=[('stage','UNREVIEWED'),('snapshot_date','2026-10-14'),('whole_package_reviews_completed',3),('whole_package_reviews_required',1),('latest_complete_review','support/history/reviews/package_03/VERDICT.json'),('root_complete_review_adoption','support/history/ROOT_WHOLE_PACKAGE_REVIEW_03.json'),('actionable_P0_P1_P2_P3',1),('latest_complete_review_root_adopted',False),('new_complete_whole_review_currently_required',True),('root_terminal_administration_adoption_required',False),('root_external_final_integrity_required',False),('ready_for_submission',True),('publication_ready',True),('published',True),('issues_updated',True),('issues_resolved',True),('ascending_publication_hold_after_pr',1033),('novelty','NEW'),('historical_priority','KNOWN'),('individual_unsupported_historical_reference_occurrences',0),('universal_historical_pointer_authentication_claim',True)]
 for opt in [False,True]:
  mode='optimized' if opt else 'normal'
  # All protected bytes, including the13 exact local exclusion paths, are guarded.
  for p in protected:
   out=fixture/'hardlink.zip';os.link(p,out)
   run(mode+' protected hardlink '+p.relative_to(KIT).as_posix(),cli(KIT/'build_archive.py','--output',out,optimized=opt),False,expected_text='cannot overwrite protected package input ')
   need(out.read_bytes()==originals[p.relative_to(KIT).as_posix()],'hardlink bytes changed');out.unlink();unchanged()
  for n in [status,'TERMINAL_OUTPUT_PINS_20261016.json','publication/zenodo-deposit.json','publication/DEPOSIT_BINDING.json','paper.pdf','metadata.json']:
   for kind in ['direct','symlink','directory-symlink','case']:
    out=KIT/n
    link=None
    if kind=='symlink':link=fixture/'file.zip';link.symlink_to(out);out=link
    elif kind=='directory-symlink':link=fixture/'dir';link.symlink_to(out.parent,target_is_directory=True);out=link/out.name
    elif kind=='case':out=out.parent/out.name.swapcase();need(out.exists() and out.samefile(KIT/n),'case-alias filesystem unavailable')
    run(mode+' protected '+kind+' '+n,cli(probe,marker,KIT/'build_archive.py','--output',out,optimized=opt),False,expected_text='cannot overwrite protected package input ')
    need(not marker.exists(),'writer opened for rejected protected output')
    if link:link.unlink()
    unchanged();guards.append({'mode':mode,'path':n,'alias':kind,'rejected_before_writer':True})
  # Physical case-ancestor containment must reject absent internal descendants.
  for scriptroot in [KIT,Path(str(KIT).swapcase())]:
   need(scriptroot.samefile(KIT),'case alias root absent')
   for suffix in ['fresh.zip','fresh-parent/one/two.zip']:
    out=scriptroot/suffix
    run(mode+' case-root containment '+str(scriptroot)+' '+suffix,cli(scriptroot/'build_archive.py','--output',out,optimized=opt),False,expected_text='inside package output must be support.zip or under tmp/')
    need(not out.exists() and not (KIT/'fresh-parent').exists(),'rejected containment created output/parent')
  for label,out in [('tmp',KIT/'tmp/allowed.zip'),('tmp-case',Path(str(KIT/'tmp').swapcase())/'allowed-case.zip'),('external',TMP/(mode+'-external.zip')),('designated',KIT/'support.zip')]:
   run(mode+' allowed archive '+label,cli(KIT/'build_archive.py','--output',out,optimized=opt));need(out.read_bytes()==archive,'allowed output bytes differ');unchanged()
  run(mode+' required actual binding',cli(KIT/'verify_package.py','--require-deposit-binding',optimized=opt))
  good=(KIT/'publication/DEPOSIT_BINDING.json').read_bytes()
  for label,mutate in [('missing-fields',lambda d:d.clear()),('wrong-size',lambda d:d['paper_pdf'].update(bytes=74899)),('wrong-zip-hash',lambda d:d['support_archive'].update(sha256='0'*64)),('extra-field',lambda d:d.update(extra=True)),('wrong-schema',lambda d:d.update(schema_version=2))]:
   d=json.loads(good);mutate(d);write(KIT/'tmp/bad-binding.json',d)
   run(mode+' malformed binding '+label,cli(KIT/'verify_package.py','--deposit-binding','tmp/bad-binding.json',optimized=opt),False)
  for field,value in variants:
   d=json.loads(originals[status]);d[field]=value;write(KIT/status,d);refresh()
   r=run(mode+' coherent terminal semantic '+field,cli(KIT/'verify_package.py',optimized=opt),False,expected_text='dated ')
   need('hash mismatch' not in r['stderr'],'semantic rejection masked by hash');restore(status);semantic.append({'mode':mode,'file':status,'field':field,'value':value,'coherent_manifest':True,'rejected_semantically':True})
  for name,field,value in [('support/history/reviews/package_04/VERDICT.json','verdict','ACTIONABLE_FINDINGS'),('support/history/ROOT_WHOLE_PACKAGE_REVIEW_04.json','whole_reviews_completed',3)]:
   d=json.loads(originals[name]);d[field]=value;write(KIT/name,d)
   copies=json.loads(originals['COPY_MAP.json']);pins=json.loads(originals['SAFE_INPUT_PINS.json'])
   for row in copies['copies']:
    if row['package_path']==name:row.update(bytes=(KIT/name).stat().st_size,sha256=sha((KIT/name).read_bytes()))
   pins['records']=copies['copies'];write(KIT/'COPY_MAP.json',copies);write(KIT/'SAFE_INPUT_PINS.json',pins);refresh()
   r=run(mode+' coherent copied evidence semantic '+name,cli(KIT/'verify_package.py',optimized=opt),False,expected_text='dated ');need('hash mismatch' not in r['stderr'] and 'copy map mismatch' not in r['stderr'],'copied evidence guard masked');restore(name,'COPY_MAP.json','SAFE_INPUT_PINS.json')
   semantic.append({'mode':mode,'file':name,'field':field,'coherent_manifest_copy_map_safe_pins':True,'rejected_semantically':True})
  for n in ['SUPPORT_MANIFEST.json','SUPPORT_ALLOWLIST.json']:
   actual=KIT/n;saved=KIT/'tmp'/('saved-'+n);actual.rename(saved);actual.symlink_to(saved)
   run(mode+' bootstrap same-byte symlink '+n,cli(KIT/'verify_package.py',optimized=opt),False,expected_text='missing/symlink member '+n);actual.unlink();saved.rename(actual);unchanged()
  # PDF preflight only: canonical aliases rejected before any compiler lookup/run.
  pdfdir=fixture/'pdf-parent';pdfdir.symlink_to(KIT,target_is_directory=True)
  for out in [KIT,pdfdir,Path(str(KIT).swapcase())]:run(mode+' PDF canonical directory alias '+str(out),cli(KIT/'build_pdf.py','--out-dir',out,optimized=opt),False,expected_text='PDF output aliases canonical paper.pdf')
  pdfdir.unlink()
  for kind in ['hardlink','symlink']:
   dest=fixture/('pdf-'+mode+'-'+kind);dest.mkdir();child=dest/'paper.pdf'
   if kind=='hardlink':os.link(KIT/'paper.pdf',child)
   else:child.symlink_to(KIT/'paper.pdf')
   run(mode+' PDF child '+kind+' alias',cli(KIT/'build_pdf.py','--out-dir',dest,optimized=opt),False,expected_text='PDF output aliases canonical paper.pdf');need(child.read_bytes()==originals['paper.pdf'],'PDF sentinel changed')
  unchanged()
 # The native uploader check returns before state/token/client creation.
 tool=AUDIT.parents[2]/'zenodo_deposit_tool/zenodo.py'
 write(HERE/'EXTERNAL_INPUT_PINS.json',{'scope':'Read-only local native uploader implementation; check branch returns before state, token/client creation or network access. No service mode executed.','entries':[{'path':str(tool),'bytes':tool.stat().st_size,'sha256':sha(tool.read_bytes())}]})
 r=run('native uploader LOCAL check',cli(tool,'check',PACKAGE/'publication/zenodo-deposit.json'),cwd=PACKAGE);native=json.loads(r['stdout'])
 need(native['files']==[{'name':n,'size':(PACKAGE/n).stat().st_size,'sha256':sha((PACKAGE/n).read_bytes())} for n in ['paper.pdf','support.zip']],'native full asset identities')
 meta=load(PACKAGE/'metadata.json');need(all(load(PACKAGE/n)['metadata']==meta for n in ['publication/release_metadata.json','publication/zenodo.json','publication/zenodo-deposit.json']),'native bibliographic object differs')
 need(load(PACKAGE/'publication/zenodo-deposit.json')['files']==[{'path':'../paper.pdf','name':'paper.pdf'},{'path':'../support.zip','name':'support.zip'}],'native paths changed')
 write(HERE/'NATIVE_LOCAL_CHECK.json',{'scope':'Actual local check only; no state/token/client/service/DOI operation. Bibliographic object and native manifest preserved exactly.','result':native,'binding':load(PACKAGE/'publication/DEPOSIT_BINDING.json'),'all_three_wrappers_equal_bare_metadata':True,'native_paths_exact':True})
 unchanged()
 write(HERE/'SEMANTIC_AND_GUARD_CONTROLS.json',{'pass':True,'protected_inputs':len(protected),'all_protected_hardlinks_rejected_both_modes':len(protected)*2,'local_exclusion_paths':excluded,'future_new_stage_seal_path_uses_labelled_test_sentinel':True,'semantic_controls':semantic,'prewriter_alias_controls':guards,'bootstrap_same_byte_allowlist_and_manifest_symlinks_rejected_both_modes':True,'case_ancestor_absent_descendant_containment_rejected_both_modes':True,'PDF_preflight_rejects_aliases_both_modes_no_compile':True,'protected_sentinels_unchanged':True,'static_filesystem_only_no_hostile_concurrent_mutation_claim':True})
 write(HERE/'REPRODUCTION_RECEIPTS.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pass':True,'actual_top_level_subprocess_commands':len(rows),'successes':sum(r['returncode']==0 for r in rows),'expected_nonzero_rejections':sum(r['returncode']!=0 for r in rows),'four_standard_library_README_commands_clean_extraction_both_modes':True,'canonical_strict_required_binding_both_modes':True,'full_mathematical_JSON_compared':True,'independent_raw_CLOSED_ZIP_and_byte_identical_deflate9_rebuild':True,'unchanged_PDF_not_compiled_or_rerendered':True,'all_processes_settled':True,'scratch_retained_ignored':True,'archive':rec(PACKAGE/'support.zip',PACKAGE),'members':len(allow)})
 with (HERE/'RESEARCH_LOG.md').open('a') as f:f.write('\n'+datetime.datetime.now(datetime.timezone.utc).isoformat()+' — 80% of bounded terminal administration: all '+str(len(rows))+' actual top-level commands settled with expected outcomes. Full mathematical JSON normal/optimized comparisons, rigorous finite faults, coherent current-status/evidence semantics, complete protected hardlinks, prewriter aliases, physical case containment, bootstrap links, strict binding and local native manifest checks passed. No PDF compile/render. Final custody/diffs/stage ledgers and terminal seal remain; ROOT external final integrity remains a separate required act.\n')
 print(json.dumps({'pass':True,'actual_commands':len(rows),'protected_inputs':len(protected),'semantic_controls':len(semantic),'members':len(allow)},indent=2))

if __name__=='__main__':main()
