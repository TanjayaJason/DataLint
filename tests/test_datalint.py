import hashlib
import json
import pytest
from typer.testing import CliRunner
from datalint.core import inspect
from datalint.cli import app

def make(tmp_path,text):
    p=tmp_path/'data.csv'
    p.write_text(text,encoding='utf-8')
    return p

def test_all_rules_and_no_source_mutation(tmp_path):
    path=make(tmp_path,'id,amount,status,constant\n1,2,paid,same\n1,2,paid,same\n2,, Paid ,same\n3,many,unknown,same\n4,150,paid,same\n,3,paid,same\n')
    cfg=tmp_path/'rules.yaml'
    cfg.write_text('columns:\n  id:\n    required: true\n    unique: true\n  amount:\n    type: number\n    maximum: 100\n  status:\n    allowed: [paid]\n  absent: {}\n',encoding='utf-8')
    before=hashlib.sha256(path.read_bytes()).digest()
    result=inspect(path,cfg)
    assert {f['rule'] for f in result['findings']} == {f'DL{i:03d}' for i in range(1,12)}
    assert before == hashlib.sha256(path.read_bytes()).digest()
    assert result == inspect(path,cfg)
    assert all(len(f['record_examples']) <= 5 for f in result['findings'])

def test_clean_data(tmp_path):
    report=inspect(make(tmp_path,'id,amount\nA,1\nB,2\n'))
    assert report['findings'] == []
    assert report['columns'][1]['inferred_type'] == 'number'

@pytest.mark.parametrize('text',['','id,id\n1,2','id,\n1,2','id,amount\n1'])
def test_invalid_csv(tmp_path,text):
    with pytest.raises(ValueError):
        inspect(make(tmp_path,text))

def test_multiline_record_number_and_privacy(tmp_path):
    path=make(tmp_path,'id,note\n1,"private\nsynthetic note"\n2,\n')
    result=inspect(path)
    finding=next(f for f in result['findings'] if f['rule']=='DL002')
    assert finding['record_examples'] == [2]
    assert 'synthetic note' not in json.dumps(result)

def test_reject_invalid_config(tmp_path):
    path=make(tmp_path,'id\n1\n')
    cfg=tmp_path/'rules.yaml'
    cfg.write_text('max_null_fraction: 2',encoding='utf-8')
    with pytest.raises(ValueError):
        inspect(path,cfg)

def test_cli_json_and_exit_codes(tmp_path):
    path=make(tmp_path,'id,amount\nA,1\nB,many\n')
    cfg=tmp_path/'rules.yaml'
    cfg.write_text('columns:\n  amount:\n    type: number\n',encoding='utf-8')
    runner=CliRunner()
    result=runner.invoke(app,[str(path),'--json'])
    assert result.exit_code == 0,result.output
    assert json.loads(result.output)['records']==2
    assert runner.invoke(app,[str(path),'--config',str(cfg),'--fail-on-error']).exit_code==2
    assert runner.invoke(app,[str(tmp_path/'missing.csv')]).exit_code==1
