"""Normal actual finalize path as positive control for the separate crash probe."""
import contextlib,hashlib,io,json,pathlib,sys
R=pathlib.Path(__file__).resolve().parent
raw=(R/'probe_finalization_recovery.py').read_bytes();prefix=raw.decode().split('first_error=None\n',1)[0]
prefix=prefix.replace("'private_finalize_crash_'","'private_finalize_positive_'").replace("crash={'once':True}","crash={'once':False}")
space={'__name__':'positive_inert_own_fixture','__file__':str(R/'probe_finalization_recovery.py')};exec(compile(prefix,str(R/'probe_finalization_recovery.py'),'exec',dont_inherit=True,optimize=sys.flags.optimize),space)
n,p,need=space['n'],space['p'],space['need'];first=io.StringIO()
with contextlib.redirect_stdout(first):n['finalize'](None,{})
current=n['load'](p/'CURRENT_STATE.json');inventory=n['load'](p/'inventory.json');need(952 in current['completed_prs'] and inventory[0]['disposition']=='accepted_merged_preprint_published' and inventory[0]['doi']=='10.5281/zenodo.17','normal local finalize did not update both views')
second=io.StringIO()
with contextlib.redirect_stdout(second):n['finalize'](None,{})
need(json.loads(second.getvalue())['already_finalized'] is True and space['counts']['inventory_write_attempts']==1,'normal rerun did not preserve completed inventory')
print(json.dumps({'status':'PASS_NORMAL_ACTUAL_FINALIZATION_POSITIVE_CONTROL','outer_optimization':sys.flags.optimize,'actual_core_compile_optimize':sys.flags.optimize,'derived_fixture_source_sha256':hashlib.sha256(raw).hexdigest(),'adaptations':['own fixture prefix only','disable one-shot injected I/O error only; actual core unchanged'],'both_local_views_updated':True,'normal_rerun_already_finalized':True,'real_Git_or_service_mutations':0,'scope':'Same actual finalize/setup and synthetic external boundaries as crash probe, without the injected save failure.'},sort_keys=True))
