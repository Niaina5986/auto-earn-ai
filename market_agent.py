"""Crypto quotes are informational. No exchange orders or wallet access."""
import json,urllib.parse,urllib.request
from config import USER_AGENT,TIMEOUT,ENABLE_CRYPTO
COINS=['bitcoin','ethereum','solana','binancecoin','ripple','dogecoin']
def crypto_market_snapshot():
 if not ENABLE_CRYPTO:return {'enabled':False,'coins':[]}
 url='https://api.coingecko.com/api/v3/simple/price?'+urllib.parse.urlencode({'ids':','.join(COINS),'vs_currencies':'usd','include_24hr_change':'true','include_market_cap':'true'})
 try:
  req=urllib.request.Request(url,headers={'User-Agent':USER_AGENT})
  with urllib.request.urlopen(req,timeout=TIMEOUT) as r:d=json.loads(r.read().decode())
  return {'enabled':True,'coins':[{'asset':k,'price_usd':v.get('usd'),'change_24h_pct':v.get('usd_24h_change'),'market_cap_usd':v.get('usd_market_cap')} for k,v in d.items()]}
 except Exception as e:return {'enabled':True,'coins':[],'error':str(e)}
def scan_arbitrage(quotes=None,fees=None):
 if not quotes:return {'status':'not_enough_data','opportunities':[],'reason':'Requires timestamped prices from multiple exchanges plus trading, withdrawal, network and slippage costs.'}
 fees=fees or {};out=[]
 for asset,rows in quotes.items():
  rows=[r for r in rows if isinstance(r.get('price'),(int,float)) and r['price']>0]
  if len(rows)<2:continue
  lo=min(rows,key=lambda r:r['price']);hi=max(rows,key=lambda r:r['price']);gross=(hi['price']-lo['price'])/lo['price']*100;net=gross-float(fees.get(asset,0))
  if net>0:out.append({'asset':asset,'buy_exchange':lo.get('exchange'),'sell_exchange':hi.get('exchange'),'gross_spread_pct':round(gross,4),'estimated_cost_pct':fees.get(asset,0),'estimated_net_pct':round(net,4),'status':'paper signal only'})
 return {'status':'paper_analysis_only','opportunities':out}
