"""Check the independent audit's own counts, raw receipts and immutable closure."""
from pathlib import Path
import datetime,json

HERE=Path(__file__).resolve().parent.parent
def require(ok,msg):
    if not ok:raise RuntimeError(msg)
def read(name):return json.loads((HERE/'receipts'/name).read_text())
def main():
    before=read('original_before.json');after=read('original_after.json')
    require(before['files']==after['files'] and before['head']==after['head'],'original changed')
    require(before['file_count']==after['file_count']==26 and before['total_bytes']==after['total_bytes']==147731,'inventory count')
    baseline=read('actual_reproduction.json')
    require(len(baseline['commands'])==6,'baseline command count')
    for n,row in enumerate(baseline['commands']):
        require(row['returncode']==0 and row['stderr']=='','baseline raw failure')
        result=json.loads(row['stdout'])
        require(result['uid']==result['euid']==501,'actual account')
        require(result['status']=='PASS','baseline status')
        require(result['optimization' if n<3 else 'harness_optimization']==n%3,'actual optimization')
        if n<3:
            require(result['author_finite_checks_per_mode']==16**3+13+256*6*15+4**7==43533,'author count')
            require(result['independent_finite_checks']==16**3+16**4+16+256*8*28+4**8==192528,'historical auditor count')
            require(result['fresh_source_bindings']==result['fresh_corpus_bindings']=='NOT_RUN','source/corpus boundary')
        else:require(result['negative_controls']==len(set(result['negative_labels']))==53,'mutation negative count')
    archive=read('archive_initial_inspection.json')
    require(archive['utc']<baseline['commands'][0]['launch_utc'],'archive not inspected before execution')
    require(archive['all_file_bytes_match_disk'] and len(archive['members'])==14 and not archive['extraction_performed'],'original archive')
    finite=[];archives=[]
    for mode in ['normal','O','OO']:
        launch=read('finite_'+mode+'_launch.json');require(launch['returncode']==0 and launch['stderr']=='','new finite failure')
        result=json.loads(launch['stdout']);result.pop('optimization');result.pop('utc');finite.append(result)
        launch=read('archive_'+mode+'_launch.json');require(launch['returncode']==0 and launch['stderr']=='','new archive failure')
        result=json.loads(launch['stdout']);require(len(result['observations'])==31,'archive observation count')
        require(all(v['accepted']==v['expected_accept'] for v in result['observations']),'archive discrepancy')
        result.pop('optimization');result.pop('utc');archives.append(result)
    require(finite[0]==finite[1]==finite[2],'new finite mode discrepancy')
    require(archives[0]==archives[1]==archives[2],'new archive mode discrepancy')
    execution=read('new_execution_adversary.json')
    rows=[json.loads(line) for line in (HERE/'receipts/new_execution_commands.jsonl').read_text().splitlines()]
    require(len(rows)==execution['command_count']==409,'actual new child command count')
    for row in rows:
        if 'expected_accept' in row:raise RuntimeError('receipt format unexpectedly changed')
    for mode in execution['modes']:
        require(mode['rejected']==133 and mode['unstructured_rejections']==['deep_array'],'malformed rejection scope')
    deep=[v for v in rows if v['label'].endswith(':deep_array')]
    require(len(deep)==3 and all(v['returncode']!=0 and 'RecursionError' in v['stderr'] for v in deep),'deep-array actual failure lost')
    require(execution['positive_write_and_create_readbacks'] and len(execution['actual_readonly_denials'])==2,'actual OS write controls')
    require(execution['active_hostile_import_positive_control'] and execution['isolated_import_marker_absent'],'active import controls')
    outer=read('outer_cli_boundaries.json')
    require(len(outer)==22 and all(v['returncode']!=0 for v in outer),'actual outer CLI negatives')
    launch_names=['execution_adversary_launch.json','outer_boundaries_launch.json','authenticate_after_launch.json']
    require(all(read(n)['returncode']==0 and read(n)['stderr']=='' for n in launch_names),'independent launcher failure')
    result=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),all_consistency_checks_passed=True,
                original_files=26,original_bytes=147731,current_uid=501,current_euid=501,
                actual_bootstrap_modes=3,actual_mutation_modes=3,mutation_negatives_per_mode=53,
                new_black_box_child_commands=409,new_malformed_variants_per_mode=133,
                optional_unstructured_deep_json_rejections_preserved=3,
                new_archive_and_binding_observations_per_mode=31,new_outer_cli_negative_commands=22,
                historical_runtime_and_original_write_probe_claims='NOT_REPRODUCED',
                original_directory_write_probes='NOT_RUN: originals are immutable',
                fresh_source_bindings='NOT_RUN',fresh_corpus_bindings='NOT_RUN',
                infinite_proof_mechanized=False,free_ultrafilter_simulated=False)
    (HERE/'receipts/receipt_validation.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
