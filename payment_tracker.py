import json,time
from config import ROOT
def create_revenue_ledger():
 p=ROOT/'reports'/'revenue_ledger.json'
 if not p.exists():p.write_text(json.dumps({'created_at':int(time.time()),'currency':'USD','verified_revenue_total':0.0,'transactions':[],'note':'Only add transactions verified on the payment platform.'},indent=2),encoding='utf-8')
 d=json.loads(p.read_text(encoding='utf-8'));d['verified_revenue_total']=round(sum(float(x.get('net_amount_usd',0)) for x in d.get('transactions',[]) if x.get('verified') is True),2);p.write_text(json.dumps(d,indent=2),encoding='utf-8');return d
