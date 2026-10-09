#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""البوت الموحّد — جيزي 🔴 + أوريدو 🟠 (نسخة فيسبوك)"""
import os,re,sys,json,time,uuid,base64,sqlite3,random,threading,subprocess,urllib3,logging,hashlib,requests
from datetime import datetime,timedelta,timezone as tz
from pathlib import Path
from flask import Flask,request
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
logging.getLogger('werkzeug').setLevel(logging.ERROR)
logging.getLogger('waitress').setLevel(logging.ERROR)
from waitress import serve
app=Flask(__name__)

# ==================== الإعدادات ====================
FB_TOKEN="EAAXxIRbrgTgBStNMQ1IerDrJV7LSZBjGBY5LQoM5HxI3OiUoAun6cIXG4FkpMjrIdXZCtxw5XrbN33TyPO8QVgH3P2IjKrIPbjZB69R826a6JJzB57hCXn3Ak0NCR02wCHoOPeK9QZCdlaCezilQsteKlsjRVSxZCr0TaRH38gzmAYVUZAhJWIZC0phZAt5Rulc6leq3hAgMcibkcvNkQmNlXrQl"
VERIFY_TOKEN="boykta_secret_2026"
PORT=50123
CF_TOKEN="eyJhIjoiMGEyN2E3Y2VkZDY5YWRjMWNmZjFkYjc0MDI0YzFiNjgiLCJ0IjoiYjRiOWVhMWUtMGI4ZC00MmRhLTljYTAtZGYxZWI5NThjZTZiIiwicyI6Ik5qTTFOR0ZoWW1RdE9UUTBZaTAwTXpCakxUZzBaRFF0WlRZMU5qQTRPR1V3WlRFMiJ9"
ADMIN_ID=6860937572

DJ_CLIENT_ID="87pIExRhxBb3_wGsA5eSEfyATloa"
DJ_CLIENT_SECRET="uf82p68Bgisp8Yg1Uz8Pf6_v1XYa"
DJ_BASE="https://apim.djezzy.dz/mobile-api"
DJ_HEADERS={'User-Agent':"MobileApp/3.0.0",'Accept':"application/json",'Content-Type':"application/json",'accept-language':"fr",'Connection':'keep-alive'}
COOLDOWN_1GB=86400
COOLDOWN_2GB=604800
COOLDOWN_3GB=604800
DZ_HEADERS=DJ_HEADERS
DZ_BASE_URL=DJ_BASE
PAGE_FOLLOW_TEXT="📢 تابعنا"

OO_BFF="https://apis.ooredoo.dz/api/ooredoo-bff"
OO_AUTH="https://apis.ooredoo.dz/api/auth/realms/myooredoo/protocol/openid-connect/token"
OO_CLIENT="myooredoo-app"
X_VERSION="1.5.15"
X_SIG="5c7641dbb82cf11066df68afc91541c967640106a95192740b43d51a5ce6777a"

RATE_PLAN_NAMES={"654":"Dima","627":"N'YOOZ","682":"N'YOOZ","625":"La Gold","626":"La Gold Jdida","628":"Ooredoo POP","629":"Dima+","630":"Anazik","631":"Anafilx","632":"YOOZ","633":"Ooredoo Pro"}
INACTIVITY_SECONDS=600

INTEGRITY_1=("JWBTpxXcH7KY9EXYeIRp8NjQMx2dt3vF8ejjoARazyoFzOw6Cu8+wkeV+zSVHSTeI6a12SG/FU+Q/9uBrcN71Rl"
"YO4CulD2x375NKwJRAInar8DVUilHBKUfjEsoHd6EwfLCfdYzLNXJu9POfEf6tqKn3PUe0pY6qZxWLhyVAFHw8Qwb"
"52ZqdI2soCH4S3mrz+OZL+YovdGSUKlXKIkxVroAMTAg3jljLF7gvXaEsB/O3uW+tbkBMwSX2uTOwf+rh3sgOF/"
"zPhKCFgRvZmU1o87Fa96Y/+wOcK+UpfXTCBYVrvQ1wG6ryC7vHMSqgUhYJK4tbSoti0zv4av9pwxh9Iv2MgsMENj"
"yKBK/TuFZxEG3xQCKj1LTMgn2xBEeKcbsKrEW3xDRwsccGI3D7GHnbUlhdI4ujDIRQVKHaZSwhTp+32Cr4EB/Qt"
"8p/xRbdgCde9MUlM4AYIGlfyVoHSkOvTu5c0DIIy1EhowtAkbKIJl49wsYKWvpT/nXFWzeXP3R2qzaclCnIb9qih"
"hrarmwz8l8XH2T+f7AK2uSNiuWLG5Fy2mM/YLmuJPZT9Ciag/mpy7JGImKNQAcFbSAInBdKQjUKT+COzZfrXj5r"
"wil9/HDMtuzIovq8hrQGY+roTfVPheTLWmcjkVCOL8VXAHjPb22vOuqrkMioWT9CQ5O8RgW7RKHrObeKQMp8F7tS"
"jOqkxYDFkPVN1G4nkEBrTlPKK9YtPl+j7IuH9fGcDTwhCTTqP8peuBryW0L11tApvAEi7VkJyBxpVxW")
INTEGRITY_2=("JWBTpxXcH7KR/kzaHeUUydDWODuU4i3H4fL9gCgKzyYfyN4qLJJE8keV+zSVHSTeI6aEyC2tbSza/NGmkflQ/Ug"
"aNZSN9SKxz7tcdQckHY25n6mOaDZ9PPMQmF4sKZqDwebce/c1SNGNn6qvTULW/L348aJvy7Vii6dyPTu3OSPV9Aw"
"KwGwQKNHN61HyK3jx/fa8Os5ux9u3Q654YLZrAJ99QGEm/C9nEBPmlHC98RjovLGBnuJOGx6k7fnyrt/Ogy5fNg"
"+tBgi5HEsoXDAwutX7TOWfx4YKHpKW//TvPRQgp69e2Xqa+CvGJJ+a/WlPMPhRCSsfo0OG04mVvlkc8eXiLzV/GP"
"uJCEmcRf9Z6V+xoDyMtU7OZ3XT5BMhI/D/N68LsRn/9dIBH6X7n0WAW3tzeKZK1zENWFKrd7aLlzEdwFzO/1JTQs"
"EDom5TRie0Kd5yic4BGvS1C1BsA2wJhzyiZ2j7RUE9m8tOAkPEIs929FYIfmH8XcCQKHT0TqT0+N+wCiyfNawPlD"
"hZWcObscFZeEmKgvqiUFCoCj6xI1hvyHK0nu7fnZ/sGc6oNT/SrFjubYWjOyoYFL7gMnlYAhyjZhjuAwN1m1/wjw"
"rOx8DbFr2NW8qb3hv+CIzK1zL3LDryKjqNkTxcOp4aJnmSTa73guCEmWc7pnLkLw5O8RgW7RKHrObeeQ0l9lu4H"
"WXwlhdWRxvVMQDimhtTrGASL6sIuaxyhOkrH4HFImP70SaCoK9+euMxnzkPjg9HqPIFj+I0KSMloVxW")

BASE_DIR=Path(os.path.expanduser("~"))/"fb_unified"
SESSIONS_DIR=BASE_DIR/"sessions"
for d in(BASE_DIR,SESSIONS_DIR):d.mkdir(parents=True,exist_ok=True)
DB_PATH=str(BASE_DIR/"boykta.db")

logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(levelname)s - %(message)s',handlers=[logging.StreamHandler(),logging.FileHandler(str(BASE_DIR/"fb.log"),encoding='utf-8')])

STEPS_FILE=BASE_DIR/"user_steps.json"
user_steps={}
_PROFILE_CACHE={}

def _new_session(headers=None):
    s=requests.Session()
    a=requests.adapters.HTTPAdapter(pool_connections=10,pool_maxsize=20,max_retries=2,pool_block=False)
    s.mount('http://',a);s.mount('https://',a);s.verify=False
    if headers:s.headers.update(headers)
    return s

def safe_request(method,url,json=None,headers=None,timeout=15):
    try:
        s=requests.Session();s.verify=False
        r=s.request(method,url,json=json,headers=headers,timeout=timeout)
        try:j=r.json()
        except:j=None
        return {'status':r.status_code,'json':j,'text':r.text[:500]}
    except requests.exceptions.Timeout:
        return {'status':0,'json':None,'text':'timeout'}
    except Exception as e:
        return {'status':0,'json':None,'text':str(e)[:200]}

def dz_extract_msg(j):
    if not j:return ""
    if isinstance(j,dict):
        msg=j.get("message")
        if isinstance(msg,dict):return msg.get("ar") or msg.get("en") or msg.get("fr") or ""
        if isinstance(msg,str):return msg
    return ""

def init_db():
    conn=sqlite3.connect(DB_PATH,timeout=15,check_same_thread=False)
    c=conn.cursor()
    try:c.execute("PRAGMA journal_mode=WAL")
    except:pass
    try:c.execute("PRAGMA synchronous=NORMAL")
    except:pass
    c.execute('''CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, username TEXT, join_date TEXT, is_logged_in INTEGER DEFAULT 0, last_phone TEXT)''')
    try:c.execute("ALTER TABLE users ADD COLUMN last_phone TEXT")
    except:pass
    c.execute('''CREATE TABLE IF NOT EXISTS numbers (phone TEXT PRIMARY KEY, user_id INTEGER, token TEXT, last_activation_1gb REAL DEFAULT 0, last_activation_2gb REAL DEFAULT 0, last_activation_3gb REAL DEFAULT 0, last_activation_offers REAL DEFAULT 0, added_date TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS stats (id INTEGER PRIMARY KEY)''')
    if c.execute("SELECT COUNT(*) FROM stats WHERE id=1").fetchone()[0]==0:
        c.execute("INSERT INTO stats (id) VALUES (1)")
    all_cols=["total_1gb","total_2gb","total_3gb","total_offers","oo_logins","oo_snap","oo_youtube","oo_byop30","oo_byop40","oo_bundles","oo_spins","oo_balance","oo_offers_view","dz_logins","oo_gaming_view","oo_ff_bought","oo_gifts","sp_yt","sp_ig","sp_fb","sp_wa","sp_tt","inet_5g","inet_10g","inet_30g","sp_data_30g","sp_data_40g","sp_data_50g","sp_data_60g","sp_data_70g","sp_data_80g","sp_data_90g","oo_soccer_enrolls","oo_stars_activated","oo_gifts_sent"]
    existing=[r[1] for r in c.execute("PRAGMA table_info(stats)").fetchall()]
    for col in all_cols:
        if col not in existing:
            try:c.execute(f"ALTER TABLE stats ADD COLUMN {col} INTEGER DEFAULT 0")
            except:pass
    conn.commit();conn.close()
init_db()

def db_query(q,p=(),fetch=False,fetchall=False):
    for attempt in range(3):
        try:
            conn=sqlite3.connect(DB_PATH,timeout=15,check_same_thread=False)
            c=conn.cursor();c.execute(q,p)
            r=None
            if fetch:r=c.fetchone()
            elif fetchall:r=c.fetchall()
            else:conn.commit()
            conn.close();return r
        except sqlite3.OperationalError as e:
            logging.error(f"DB try {attempt+1}: {e}");time.sleep(0.2*(attempt+1))
        except Exception as e:
            print(f"DB: {e}");return None
    return None

def inc_stat(field):
    try:db_query(f"UPDATE stats SET {field} = COALESCE({field}, 0) + 1 WHERE id = 1")
    except:pass

def save_steps():
    try:
        clean={}
        for k,v in user_steps.items():
            if isinstance(v,dict):
                clean[str(k)]={kk:vv for kk,vv in v.items() if kk in("step","phone","msisdn","display","last_activity","gift_beneficiary","gift_bundles")}
            else:clean[str(k)]=v
        STEPS_FILE.write_text(json.dumps(clean,ensure_ascii=False))
    except:pass

def load_steps_saved():
    try:
        if STEPS_FILE.exists():
            d=json.loads(STEPS_FILE.read_text())
            return {int(k):v for k,v in d.items()}
    except:pass
    return {}

# ==================== FB API ====================
def fb_send(uid,text):
    url=f"https://graph.facebook.com/v17.0/me/messages?access_token={FB_TOKEN}"
    try:
        r=requests.post(url,json={"recipient":{"id":uid},"message":{"text":text}},timeout=5)
        if r.status_code!=200:print(f"⚠️ FB {r.status_code}: {r.text[:150]}",flush=True)
        return r.status_code==200
    except Exception as e:
        print(f"❌ FB: {e}",flush=True);return False

def fb_typing(uid):
    url=f"https://graph.facebook.com/v17.0/me/messages?access_token={FB_TOKEN}"
    try:requests.post(url,json={"recipient":{"id":uid},"sender_action":"typing_on"},timeout=5)
    except:pass

def start_tunnel():
    print("🚀 النفق...",flush=True)
    try:
        p=subprocess.Popen(["cloudflared","tunnel","--no-autoupdate","run","--token",CF_TOKEN],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        print(f"✅ PID: {p.pid}\n",flush=True)
    except Exception as e:print(f"❌ {e}\n",flush=True)

# ==================== جيزي ====================
def dj_request_otp(phone):
    url=f"{DJ_BASE}/oauth2/registration"
    params={'msisdn':phone,'client_id':DJ_CLIENT_ID,'scope':"smsotp"}
    payload={"consent-agreement":[{"marketing-notifications":False}],"is-consent":True}
    try:
        r=_new_session(DJ_HEADERS).post(url,params=params,json=payload,timeout=45)
        logging.info(f"[DJ-OTP] {phone} → {r.status_code}")
        return r.status_code==200
    except Exception as e:
        logging.error(f"DJ OTP: {e}");return False

def dj_verify_otp(phone,otp):
    url=f"{DJ_BASE}/oauth2/token"
    clean=''.join(filter(str.isdigit,otp))
    if len(clean)!=6:return None
    payload={'otp':clean,'mobileNumber':phone,'scope':"djezzyAppV2",'client_id':DJ_CLIENT_ID,'client_secret':DJ_CLIENT_SECRET,'grant_type':"mobile"}
    h=DJ_HEADERS.copy();h['Content-Type']="application/x-www-form-urlencoded"
    for i in range(3):
        try:
            r=_new_session(h).post(url,data=payload,timeout=45)
            logging.info(f"[DJ-VERIFY] {phone} → {r.status_code}")
            if r.status_code==200:return r.json().get('access_token')
            if r.status_code==401:return "EXPIRED"
        except Exception as e:logging.error(f"DJ verify: {e}")
        if i<2:time.sleep(3)
    return None

def dj_extract_balance_info(raw):
    info={"main":0,"due":0}
    if not raw:return info
    data=raw.get("data",raw) if isinstance(raw,dict) else {}
    if isinstance(data,dict):
        try:info["main"]=float(data.get("mainBalance",0) or 0)
        except:info["main"]=0
        try:info["due"]=float(data.get("due",0) or 0)
        except:info["due"]=0
    return info

def dj_check_balance(token,phone):
    h=DJ_HEADERS.copy();h['Authorization']=f"Bearer {token}";h['User-Agent']="MobileApp/3.0.7"
    s=_new_session(h)
    out={"status":"SUCCESS","balance":0,"due":0}
    try:
        r=s.get(f"{DJ_BASE}/api/v1/subscribers/main-balance/{phone}",timeout=25)
        logging.info(f"[DJ-BAL] {phone} → {r.status_code}")
        if r.status_code==200:
            bi=dj_extract_balance_info(r.json())
            out["balance"]=bi["main"];out["due"]=bi["due"]
        elif r.status_code==401:return {"status":"EXPIRED","balance":0,"due":0}
        else:return {"status":"FAILED","balance":0,"due":0}
    except Exception as e:
        logging.error(f"DJ bal: {e}");return {"status":"FAILED","balance":0,"due":0}
    return out

def dj_extract_price(p):
    try:
        m=re.search(r'(\d+)',str(p))
        if m:return int(m.group(1))
    except:pass
    return None

def dz_activate_paid_offer(token,phone,package_code,offer_type,offer_name,price):
    h=DZ_HEADERS.copy();h['Authorization']=f"Bearer {token}"
    def _try_post(url,label):
        r=safe_request('POST',url,json={"packageCode":package_code},headers=h,timeout=12)
        if r['status']==401:return {"success":False,"token_expired":True,"msg":"⚠️ انتهت جلستك اعد إرسال رقمك"}
        if r['status'] in[200,201,202]:
            srv=dz_extract_msg(r['json']) if r['json'] else ""
            if srv:
                low=srv.lower()
                for kw in['غير متوفر','غير متوفرة','not available','not found','déjà','already','solde','رصيد','insufficient']:
                    if kw in low:
                        if 'رصيد' in low or 'solde' in low or 'insufficient' in low:
                            return {"success":False,"token_expired":False,"msg":f"❌ رصيدك غير كافي لتفعيل {offer_name}\n💰 المطلوب: {price} د.ج"}
                        return {"success":False,"token_expired":False,"msg":f"⚠️ {srv}"}
            return {"success":True,"token_expired":False,"msg":f"✅ ━━━ تم التفعيل بنجاح ━━━\n\n🎉 {offer_name}\n💰 السعر: {price} د.ج\n\n{PAGE_FOLLOW_TEXT}"}
        if r['status']==402:
            return {"success":False,"token_expired":False,"msg":f"❌ رصيدك غير كافي لتفعيل {offer_name}\n💰 المطلوب: {price} د.ج"}
        srv=dz_extract_msg(r['json']);code=r.get('status','?')
        info=srv if srv else f"كود: {code}"
        return {"success":False,"token_expired":False,"msg":f"⚠️ تعذر تفعيل {offer_name}\n\nℹ️ {info}"}
    if offer_type=="shake":
        shake_url=f"{DZ_BASE_URL}/api/v1/services/shake/{phone}"
        for _ in range(4):
            res_get=safe_request('GET',shake_url,headers=h,timeout=8)
            if res_get['status']==401:return {"success":False,"token_expired":True,"msg":"⚠️ انتهت جلستك"}
            if res_get['status']==200:break
            time.sleep(0.3)
        r_post=_try_post(shake_url,"shake")
        if not r_post.get("success") and not r_post.get("token_expired"):
            fb=_try_post(f"{DZ_BASE_URL}/api/v1/subscribers/activate-product/{phone}","fb")
            if fb.get("success") or fb.get("token_expired"):return fb
            if any(k in fb.get("msg","") for k in['رصيد','غير متوفر','تم التفعيل']):return fb
        return r_post
    return _try_post(f"{DZ_BASE_URL}/api/v1/subscribers/activate-product/{phone}","activate")

def dz_activate_offer_70_4g(token,phone):
    h=DZ_HEADERS.copy();h['Authorization']=f"Bearer {token}"
    def _try_post(url,label):
        r=safe_request('POST',url,json={"packageCode":"BTLINTSPEEDDAY2GO"},headers=h,timeout=12)
        if r.get('status')==401:return {"success":False,"token_expired":True,"msg":"⚠️ انتهت جلستك"}
        if r.get('status') in[200,201,202]:
            return {"success":True,"token_expired":False,"msg":f"✅ ━━━ تم التفعيل بنجاح ━━━\n\n🟢 عرض: 4 جيجابايت\n💰 السعر: 70 د.ج\n⏱️ الصلاحية: 24 ساعة\n\n{PAGE_FOLLOW_TEXT}"}
        if r.get('status')==402:return {"success":False,"token_expired":False,"msg":"❌ رصيدك غير كافٍ"}
        srv=dz_extract_msg(r.get('json'));status=r.get('status')
        info=srv if srv else f"كود: {status}"
        return {"success":False,"token_expired":False,"msg":f"⚠️ تعذر التفعيل\nℹ️ {info}"}
    shake_url=f"{DZ_BASE_URL}/api/v1/services/shake/{phone}"
    for _ in range(3):
        res_get=safe_request('GET',shake_url,headers=h,timeout=8)
        if res_get.get('status')==401:return {"success":False,"token_expired":True,"msg":"⚠️ انتهت جلستك"}
        if res_get.get('status')==200:break
        time.sleep(0.5)
    r_post=_try_post(shake_url,"shake")
    if not r_post.get("success") and not r_post.get("token_expired"):
        fb=_try_post(f"{DZ_BASE_URL}/api/v1/subscribers/activate-product/{phone}","fb")
        if fb.get("success") or fb.get("token_expired"):return fb
    return r_post

def dz_activate_offer_90_5g(token,phone):
    h=DZ_HEADERS.copy();h['Authorization']=f"Bearer {token}"
    def _try_post(url,label):
        r=safe_request('POST',url,json={"packageCode":"BTL500MBDAY"},headers=h,timeout=12)
        if r.get('status')==401:return {"success":False,"token_expired":True,"msg":"⚠️ انتهت جلستك"}
        if r.get('status') in[200,201,202]:
            return {"success":True,"token_expired":False,"msg":f"✅ ━━━ تم التفعيل بنجاح ━━━\n\n🟣 عرض: 5 جيجابايت\n💰 السعر: 90 د.ج\n⏱️ الصلاحية: 24 ساعة\n\n{PAGE_FOLLOW_TEXT}"}
        if r.get('status')==402:return {"success":False,"token_expired":False,"msg":"❌ رصيدك غير كافٍ"}
        srv=dz_extract_msg(r.get('json'));status=r.get('status')
        info=srv if srv else f"كود: {status}"
        return {"success":False,"token_expired":False,"msg":f"⚠️ تعذر التفعيل\nℹ️ {info}"}
    shake_url=f"{DZ_BASE_URL}/api/v1/services/shake/{phone}"
    for _ in range(3):
        res_get=safe_request('GET',shake_url,headers=h,timeout=8)
        if res_get.get('status')==401:return {"success":False,"token_expired":True,"msg":"⚠️ انتهت جلستك"}
        if res_get.get('status')==200:break
        time.sleep(0.5)
    r_post=_try_post(shake_url,"shake")
    if not r_post.get("success") and not r_post.get("token_expired"):
        fb=_try_post(f"{DZ_BASE_URL}/api/v1/subscribers/activate-product/{phone}","fb")
        if fb.get("success") or fb.get("token_expired"):return fb
    return r_post

def dj_activate_1gb(token,phone):
    h=DJ_HEADERS.copy();h['Authorization']=f"Bearer {token}"
    s=_new_session(h)
    for i in range(10):
        target="2137"+"".join([str(random.randint(0,9)) for _ in range(8)])
        try:
            inv=s.post(f"{DJ_BASE}/api/v1/services/mgm/send-invitation/{phone}",json={"msisdnReciever":target},timeout=15)
            if inv.status_code==401:return "EXPIRED"
            if inv.status_code==403 or "limit" in inv.text.lower():return "LIMIT"
            if inv.status_code==201:
                time.sleep(1.5)
                act=s.post(f"{DJ_BASE}/api/v1/services/mgm/activate-reward/{phone}",json={"packageCode":"MGMBONUS1Go"},timeout=15)
                if "success" in act.text.lower() or act.status_code==200:return "SUCCESS"
        except:pass
        time.sleep(1)
    return "FAILED"

def dj_activate_2gb(token,phone):
    h=DJ_HEADERS.copy();h['Authorization']=f"Bearer {token}";h['User-Agent']="MobileApp/3.0.7"
    s=_new_session(h)
    endpoints=[(f"{DJ_BASE}/api/v1/services/shake/{phone}","GIFTWALKWIN2GO"),(f"{DJ_BASE}/api/v1/services/walk/activate-reward/{phone}","GIFTWALKWIN2GO"),(f"{DJ_BASE}/api/v1/subscribers/activate-product/{phone}","GIFTWALKWIN2GO")]
    last=0
    for url,code in endpoints:
        try:
            r=s.post(url,json={"packageCode":code},timeout=20)
            last=r.status_code
            if r.status_code==401:return "EXPIRED"
            if r.status_code in(200,201):
                if "already" in r.text.lower():return "LIMIT"
                return "SUCCESS"
            if r.status_code==402:return "NO_BALANCE"
            if r.status_code==429:return "RATE_LIMIT"
        except:pass
        time.sleep(0.3)
    if last==403:return "NOT_ALLOWED"
    return "FAILED"

def dj_activate_3gb(token,phone):
    h=DJ_HEADERS.copy();h['Authorization']=f"Bearer {token}"
    s=_new_session(h)
    url=f"{DJ_BASE}/api/v1/services/walk/activate-reward/{phone}"
    res=[]
    for pkg in["GIFTWALKWIN2GO","MGMBONUS1Go"]:
        try:
            r=s.post(url,json={"packageCode":pkg},timeout=20)
            if r.status_code in[200,201] or "success" in r.text.lower():res.append(True)
            elif r.status_code==401:return "EXPIRED"
            else:res.append(False)
            time.sleep(1)
        except:res.append(False)
    return "SUCCESS" if any(res) else "FAILED"

# ==================== أوريدو ====================
def _now_ms():return str(int(time.time()*1000))
def _iid():return str(uuid.uuid4())+_now_ms()
def _pld(x):return base64.b64encode(json.dumps({"platform":"android","is-physical-device":True,"device-id":x},separators=(",",":")).encode()).decode()
def _fp():return os.urandom(32).hex()
def _corr():return str(uuid.uuid4())+_now_ms()
def _exdid(at):
    try:
        p=at.split(".");pad=len(p[1])%4
        return json.loads(base64.b64decode(p[1]+"="*(4-pad) if pad else p[1])).get("device-id")
    except:return None
def _mps(at):
    d=_exdid(at) or _iid()
    return base64.b64encode(json.dumps({"platform":"android","is-physical-device":True,"device-id":d},separators=(",",":")).encode()).decode()

def oo_quick_detect(at):
    rp="";is_yooz=False;is_dima=False
    try:
        p=at.split(".");pad=len(p[1])%4
        payload=json.loads(base64.b64decode(p[1]+"="*(4-pad) if pad else p[1]))
        rp_code=str(payload.get("ratePlan") or "")
        if rp_code in RATE_PLAN_NAMES:
            rp=RATE_PLAN_NAMES[rp_code]
            rp_up=rp.upper().replace("'","").replace(" ","")
            is_dima="DIMA" in rp_up
            is_yooz="YOOZ" in rp_up
    except:pass
    return {"rate_plan":rp,"is_yooz":is_yooz,"is_dima":is_dima}

def _oo_req(method,url,headers,content=b"",timeout=20):
    try:
        s=_new_session()
        data=content if isinstance(content,bytes) else content.encode()
        r=s.request(method,url,headers=headers,data=data,timeout=timeout,allow_redirects=False)
        try:body=r.json()
        except:body={"_raw":r.text[:500]}
        return r.status_code,dict(r.headers),body
    except Exception as e:
        logging.debug(f"_oo_req: {e}")
        return 0,{},{"_error":str(e)[:100]}

def _base_hdrs(msisdn,iid_val,psig,corr,ts,fp=None):
    return {"user-agent":"Dart/3.11 (dart:io)","accept-encoding":"gzip","x-msisdn":msisdn,"x-device-fingerprint":fp or _fp(),"x-platform-origin":"mobile-android","x-correlation-id":corr,"platform":"android","x-version":X_VERSION,"x-signature":X_SIG,"x-platform-data-signature":psig,"x-timestamp":ts,"x-instance-id":iid_val}

def _web_hdrs(msisdn,at,meta,ct=""):
    ts=_now_ms()
    iid_val=meta.get("tok_instance_id") or _iid()
    psig=meta.get("tok_plat_sig") or _pld(iid_val)
    fp=meta.get("tok_fingerprint") or _fp()
    h={"User-Agent":"Dart/3.11 (dart:io)","Accept-Encoding":"gzip","x-msisdn":msisdn,"x-device-fingerprint":fp,"x-platform-origin":"web","authorization":f"Bearer {at}","x-correlation-id":_corr(),"platform":"web","x-version":X_VERSION,"x-signature":X_SIG,"x-platform-data-signature":psig,"x-timestamp":ts,"x-instance-id":iid_val,"origin":"https://my.ooredoo.dz","referer":"https://my.ooredoo.dz/"}
    if ct:h["content-type"]=ct
    return h

def ooredoo_send_otp_sync(msisdn):
    ts=_now_ms();iid_val=_iid();psig=_pld(iid_val);fp=_fp()
    device={"instance_id":iid_val,"plat_sig":psig,"fp":fp}
    nonce,chronos="",""
    try:
        h3=_base_hdrs(msisdn,iid_val,psig,_corr(),ts,fp=fp)
        h3.update({"content-type":"application/json; charset=utf-8","x-native-integrity-token":INTEGRITY_1,"x-path":"/api/auth/realms/myooredoo/protocol/openid-connect/token","x-method":"POST"})
        _,rh3,_=_oo_req("POST",f"{OO_BFF}/checkpoint/token",h3,b"{}",timeout=20)
        nonce=rh3.get("x-nonce-id") or rh3.get("X-Nonce-Id") or ""
        chronos=rh3.get("x-chronos-id") or rh3.get("X-Chronos-Id") or ""
    except:pass
    try:
        h4={"User-Agent":"Dart/3.11 (dart:io)","Accept-Encoding":"gzip","x-msisdn":msisdn,"x-device-fingerprint":fp,"x-platform-origin":"mobile-android","platform":"android","x-version":X_VERSION,"x-signature":X_SIG,"x-timestamp":ts,"x-platform-info":psig,"x-force-update":"true","x-instance-id":iid_val,"content-type":"application/x-www-form-urlencoded"}
        if nonce:h4["x-nonce-id"]=nonce
        if chronos:h4["x-chronos-id"]=chronos
        body=f"client_id={OO_CLIENT}&grant_type=password&username={msisdn}"
        c4,_,_=_oo_req("POST",OO_AUTH,h4,body,timeout=30)
        logging.info(f"[OO-OTP] {msisdn} → {c4}")
        if c4==429:return {"device":device,"otp_sent":False,"status":429,"reason":"rate_limit"}
        if c4==0:return {"device":device,"otp_sent":False,"status":0,"reason":"network"}
        return {"device":device,"otp_sent":True,"status":c4}
    except Exception as e:
        logging.error(f"❌ OOREDOO OTP: {e}")
        return {"device":device,"otp_sent":False,"status":-1,"reason":"exception"}

def ooredoo_verify_otp_sync(msisdn,otp,device):
    iid_val=device.get("instance_id") or _iid()
    psig=device.get("plat_sig") or _pld(iid_val)
    fp_otp=device.get("fp") or _fp()
    ts=_now_ms()
    nonce,chronos="",""
    try:
        h6=_base_hdrs(msisdn,iid_val,psig,_corr(),ts,fp=fp_otp)
        h6.update({"content-type":"application/json; charset=utf-8","x-native-integrity-token":INTEGRITY_2,"x-path":"/api/auth/realms/myooredoo/protocol/openid-connect/token","x-method":"POST"})
        _,rh6,_=_oo_req("POST",f"{OO_BFF}/checkpoint/token",h6,b"{}",timeout=15)
        nonce=rh6.get("x-nonce-id") or rh6.get("X-Nonce-Id") or ""
        chronos=rh6.get("x-chronos-id") or rh6.get("X-Chronos-Id") or ""
    except:pass
    h7={"User-Agent":"Dart/3.11 (dart:io)","Accept-Encoding":"gzip","x-msisdn":msisdn,"x-device-fingerprint":fp_otp,"x-platform-origin":"mobile-android","platform":"android","x-version":X_VERSION,"x-signature":X_SIG,"x-timestamp":ts,"x-platform-info":psig,"x-force-update":"true","x-instance-id":iid_val,"content-type":"application/x-www-form-urlencoded"}
    if nonce:h7["x-nonce-id"]=nonce
    if chronos:h7["x-chronos-id"]=chronos
    body=f"client_id={OO_CLIENT}&grant_type=password&username={msisdn}&otp={otp}"
    c7,_,j7=_oo_req("POST",OO_AUTH,h7,body,timeout=30)
    logging.info(f"[OO-VERIFY] {msisdn} → {c7}")
    if c7==200 and isinstance(j7,dict) and "access_token" in j7:
        at=j7["access_token"]
        return {"access_token":at,"refresh_token":j7.get("refresh_token",""),"expires_in":j7.get("expires_in",0),"tok_fingerprint":fp_otp,"tok_instance_id":_exdid(at) or iid_val,"tok_plat_sig":_mps(at),"tok_timestamp":ts,"issued_at":int(time.time())}
    if c7 in(400,401,403):return "wrong_otp"
    return None

def ooredoo_refresh_token_sync(msisdn,rt,device):
    iid_val=device.get("instance_id") or _iid();psig=device.get("plat_sig") or _pld(iid_val)
    fp_otp=device.get("fp") or _fp();ts=_now_ms()
    h=_base_hdrs(msisdn,iid_val,psig,_corr(),ts,fp=fp_otp)
    h.update({"content-type":"application/x-www-form-urlencoded","x-native-integrity-token":INTEGRITY_1,"x-path":"/api/auth/realms/myooredoo/protocol/openid-connect/token","x-method":"POST"})
    _,rh,_=_oo_req("POST",f"{OO_BFF}/checkpoint/token",h,b"{}",timeout=15)
    nonce=rh.get("x-nonce-id") or rh.get("X-Nonce-Id") or ""
    chronos=rh.get("x-chronos-id") or rh.get("X-Chronos-Id") or ""
    if not nonce or not chronos:return None
    h2={"User-Agent":"Dart/3.11 (dart:io)","Accept-Encoding":"gzip","x-msisdn":msisdn,"x-device-fingerprint":fp_otp,"x-nonce-id":nonce,"x-platform-origin":"mobile-android","platform":"android","x-version":X_VERSION,"x-signature":X_SIG,"x-chronos-id":chronos,"x-timestamp":ts,"x-platform-info":psig,"x-force-update":"true","x-instance-id":iid_val,"content-type":"application/x-www-form-urlencoded"}
    body=f"client_id={OO_CLIENT}&grant_type=refresh_token&refresh_token={rt}"
    c2,_,j2=_oo_req("POST",OO_AUTH,h2,body,timeout=30)
    if c2==200 and "access_token" in j2:
        at=j2["access_token"]
        return {"access_token":at,"refresh_token":j2.get("refresh_token",rt),"expires_in":j2.get("expires_in",0),"tok_instance_id":_exdid(at) or iid_val,"tok_plat_sig":_mps(at),"tok_fingerprint":fp_otp,"tok_timestamp":ts,"issued_at":int(time.time())}
    return None

def oo_check_balance(msisdn,at,meta):
    h=_web_hdrs(msisdn,at,meta)
    c,_,resp=_oo_req("GET",f"{OO_BFF}/subscriptions/getAccountInfo",h,timeout=20)
    if c==200:return {"status":"ok","data":resp if isinstance(resp,dict) else {}}
    if c==401:return {"status":"unauthorized"}
    return {"status":"error","code":c}

def oo_get_profile(msisdn,at,meta):
    cache_key=hashlib.md5((msisdn+at[-16:]).encode()).hexdigest()
    now=time.time()
    if cache_key in _PROFILE_CACHE:
        ts_cached,data_cached=_PROFILE_CACHE[cache_key]
        if now-ts_cached<300:return data_cached
    iid_val=meta.get("tok_instance_id") or _iid()
    psig=meta.get("tok_plat_sig") or _pld(iid_val)
    fp=meta.get("tok_fingerprint") or _fp()
    h_ck=_base_hdrs(msisdn,iid_val,psig,_corr(),_now_ms(),fp=fp)
    h_ck.update({"content-type":"application/json; charset=utf-8","x-native-integrity-token":INTEGRITY_1,"x-path":"/api/ooredoo-bff/userInfo/personal","x-method":"GET"})
    _,rh_ck,_=_oo_req("POST",f"{OO_BFF}/checkpoint/token",h_ck,b"{}",timeout=10)
    n=rh_ck.get("x-nonce-id","") or rh_ck.get("X-Nonce-Id","")
    ch=rh_ck.get("x-chronos-id","") or rh_ck.get("X-Chronos-Id","")
    iso_ts=datetime.now(tz.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")+"Z"
    h={"user-agent":"Dart/3.11 (dart:io)","accept-encoding":"gzip","x-msisdn":msisdn,"x-device-fingerprint":fp,"x-platform-origin":"mobile-android","authorization":f"Bearer {at}","x-correlation-id":_corr(),"platform":"android","x-version":X_VERSION,"x-signature":X_SIG,"accept":"*/*","x-platform-data-signature":psig,"x-timestamp":iso_ts,"x-instance-id":iid_val}
    if n:h["x-nonce-id"]=n
    if ch:h["x-chronos-id"]=ch
    c,_,resp=_oo_req("GET",f"{OO_BFF}/userInfo/personal",h,timeout=12)
    if c==200 and isinstance(resp,dict):
        result={"status":"ok","data":resp}
        _PROFILE_CACHE[cache_key]=(now,result)
        return result
    return {"status":"unauthorized" if c==401 else "error","code":c}

def oo_get_active(msisdn,at,meta):
    h=_web_hdrs(msisdn,at,meta)
    c,_,resp=_oo_req("GET",f"{OO_BFF}/bundle/getActivePackages?msisdn={msisdn}",h,timeout=20)
    if c==200:return {"status":"ok","data":resp if isinstance(resp,dict) else {}}
    if c==401:return {"status":"unauthorized"}
    return {"status":"error","code":c}

def oo_activate_snapchat(msisdn,at,meta):
    h=_web_hdrs(msisdn,at,meta)
    c,_,_=_oo_req("POST",f"{OO_BFF}/snap-chat/apply",h,timeout=20)
    if c==200:return "ok"
    if c==500:return "already_active"
    if c==401:return "unauthorized"
    return "error"

def oo_purchase_byop(msisdn,at,meta,validity="Biweekly",limited=None,unlimited=None):
    h=_web_hdrs(msisdn,at,meta,"application/json; charset=utf-8")
    body=json.dumps({"validity":validity,"limitedBundleDetails":limited or [],"unlimitedBundleDetails":unlimited or []},separators=(",",":"))
    c,_,_=_oo_req("POST",f"{OO_BFF}/bundle/purchase/byop",h,body,timeout=30)
    if c==200:return {"status":"ok"}
    if c==409:return {"status":"conflict","message":"الرصيد غير كافي"}
    if c==401:return {"status":"unauthorized"}
    return {"status":"error","code":c}

def oo_purchase_planned(msisdn,at,meta,code):
    h=_web_hdrs(msisdn,at,meta,"application/json; charset=utf-8")
    body=json.dumps({"bundleCode":code},separators=(",",":"))
    c,_,_=_oo_req("POST",f"{OO_BFF}/cvm/dynamic-bundle-purchase",h,body,timeout=30)
    if c==200:return {"status":"ok"}
    if c==409:return {"status":"conflict","message":"الرصيد غير كافي"}
    if c==401:return {"status":"unauthorized"}
    return {"status":"error","code":c}

def oo_spin_status(msisdn,at,meta):
    iid_val=meta.get("tok_instance_id") or _iid()
    psig=meta.get("tok_plat_sig") or _pld(iid_val)
    fp=meta.get("tok_fingerprint") or _fp()
    ts=_now_ms()
    h_ck=_base_hdrs(msisdn,iid_val,psig,_corr(),ts,fp=fp)
    h_ck.update({"content-type":"application/json; charset=utf-8","x-native-integrity-token":INTEGRITY_1,"x-path":"/api/ooredoo-bff/gamification/status","x-method":"GET"})
    _,rh_ck,_=_oo_req("POST",f"{OO_BFF}/checkpoint/token",h_ck,b"{}",timeout=15)
    n=rh_ck.get("x-nonce-id","") or rh_ck.get("X-Nonce-Id","")
    ch=rh_ck.get("x-chronos-id","") or rh_ck.get("X-Chronos-Id","")
    h=_web_hdrs(msisdn,at,meta)
    if n:h["x-nonce-id"]=n
    if ch:h["x-chronos-id"]=ch
    c,_,resp=_oo_req("GET",f"{OO_BFF}/gamification/status",h,timeout=20)
    logging.info(f"[OO-SPIN-STATUS] → {c} | {str(resp)[:150]}")
    if c==200:return {"status":"ok","data":resp if isinstance(resp,dict) else {}}
    if c==401:return {"status":"unauthorized"}
    return {"status":"error","code":c}

def oo_spin_wheel(msisdn,at,meta):
    iid_val=meta.get("tok_instance_id") or _iid()
    psig=meta.get("tok_plat_sig") or _pld(iid_val)
    fp=meta.get("tok_fingerprint") or _fp()
    ts=_now_ms()
    h_ck=_base_hdrs(msisdn,iid_val,psig,_corr(),ts,fp=fp)
    h_ck.update({"content-type":"application/json; charset=utf-8","x-native-integrity-token":INTEGRITY_1,"x-path":"/api/ooredoo-bff/gamification/play","x-method":"GET"})
    _,rh_ck,_=_oo_req("POST",f"{OO_BFF}/checkpoint/token",h_ck,b"{}",timeout=15)
    n=rh_ck.get("x-nonce-id","") or rh_ck.get("X-Nonce-Id","")
    ch=rh_ck.get("x-chronos-id","") or rh_ck.get("X-Chronos-Id","")
    h=_web_hdrs(msisdn,at,meta)
    if n:h["x-nonce-id"]=n
    if ch:h["x-chronos-id"]=ch
    c,_,resp=_oo_req("GET",f"{OO_BFF}/gamification/play",h,timeout=25)
    logging.info(f"[OO-SPIN-PLAY] → {c} | {str(resp)[:200]}")
    if c==200:
        if isinstance(resp,dict):
            g=resp.get("giftName")
            lp=resp.get("playedTime") or resp.get("lastPlayedTime") or ""
            if g:return {"status":"ok","gift":g,"validity_hour":resp.get("validityHour"),"last_played":lp}
        return {"status":"ok","gift":None}
    if c==401:return {"status":"unauthorized"}
    if c==403:return {"status":"not_eligible"}
    if c==409:return {"status":"already_played"}
    return {"status":"error","code":c}

def oo_get_plans(msisdn,at,meta):
    h=_web_hdrs(msisdn,at,meta)
    c,_,resp=_oo_req("GET",f"{OO_BFF}/anazik/service/getSubPlans",h,timeout=20)
    if c==200:return {"status":"ok","plans":resp.get("data",[]) if isinstance(resp,dict) else []}
    if c==401:return {"status":"unauthorized"}
    return {"status":"error","code":c}

def oo_soccer_eligibility(msisdn,at,meta):
    h=_web_hdrs(msisdn,at,meta)
    c,_,resp=_oo_req("GET",f"{OO_BFF}/soccer/eligibility-check",h,timeout=20)
    if c==401:return {"status":"unauthorized"}
    if c!=200:return {"status":"error","code":c}
    if not isinstance(resp,dict):return {"status":"error","code":c}
    status_srv=str(resp.get("status","")).upper()
    eligible=bool(resp.get("isEligible") or resp.get("eligible") or resp.get("canActivate"))
    enrolled=(status_srv=="ACTIVE")
    selected=""
    try:
        opts=resp.get("options",{})
        attrs=opts.get("attribute",[]) if isinstance(opts,dict) else []
        for a in attrs:
            if isinstance(a,dict) and a.get("key")=="current_value":
                selected=str(a.get("value") or "")
                break
    except:pass
    if status_srv=="INACTIVE" and not eligible:
        enrolled=False;eligible=False
    return {"status":"ok","eligible":eligible,"enrolled":enrolled,"selected_team":selected.upper() if selected else "","raw_status":status_srv,"raw":resp}

def oo_soccer_clubs(msisdn,at,meta):
    h=_web_hdrs(msisdn,at,meta)
    url="https://apis.ooredoo.dz/cms/v2/api/soccer-clubs?locale=ar&populate=%2A"
    c,_,resp=_oo_req("GET",url,h,timeout=20)
    if c!=200 or not isinstance(resp,dict):return {"status":"error","code":c}
    clubs=[]
    for item in resp.get("data",[]):
        attrs=item.get("attributes",{})
        code=(attrs.get("club_name") or "").upper()
        if code:clubs.append({"code":code,"colors":attrs.get("club_colors","")})
    return {"status":"ok","clubs":clubs}

def oo_soccer_activate(msisdn,at,meta,team="MCA"):
    team=team.upper()
    h=_web_hdrs(msisdn,at,meta,"application/json; charset=utf-8")
    c,_,resp=_oo_req("POST",f"{OO_BFF}/soccer/activate?selectedTeam={team}",h,b"{}",timeout=25)
    if c==200 and isinstance(resp,dict):
        if str(resp.get("status","")).lower()=="true":return {"status":"ok","data":resp}
        return {"status":"failed","msg":resp.get("reason") or "فشل"}
    if c==401:return {"status":"unauthorized"}
    if c==409:return {"status":"already","msg":"مسجل مسبقاً"}
    if c==400:return {"status":"already","msg":"الرقم مسجل مسبقاً"}
    return {"status":"error","code":c,"resp":resp}

def oo_check_noudjoum_status(msisdn,at,meta):
    h=_web_hdrs(msisdn,at,meta)
    for url in[f"{OO_BFF}/noudjoum/status",f"{OO_BFF}/noudjoum/account",f"{OO_BFF}/noudjoum/profile"]:
        try:
            c,_,resp=_oo_req("GET",url,h,timeout=12)
            if c==401:return {"status":"unauthorized"}
            if c==200 and isinstance(resp,dict):
                enrolled=bool(resp.get("enrolled") or resp.get("isEnrolled") or resp.get("active") or resp.get("isActive") or resp.get("subscribed") or resp.get("points") is not None)
                return {"status":"enrolled" if enrolled else "not_enrolled","points":resp.get("points") or resp.get("balance") or 0}
        except:pass
    return {"status":"unknown"}

def oo_enroll_noudjoum(msisdn,at,meta):
    h=_web_hdrs(msisdn,at,meta,"application/json; charset=utf-8")
    c,_,resp=_oo_req("POST",f"{OO_BFF}/noudjoum/enroll",h,b"",timeout=25)
    logging.info(f"[NOUDJOUM-ENR] {msisdn} → {c} | {str(resp)[:200]}")
    if c in(200,201):return {"status":"ok"}
    if c==409:return {"status":"already"}
    if c==401:return {"status":"unauthorized"}
    if c==403:return {"status":"not_eligible"}
    if c==500:
        body=str(resp).lower()
        if "not eligible" in body or "mass programme" in body:return {"status":"not_eligible"}
        return {"status":"error","code":500}
    if c==400:
        body=str(resp).lower()
        if "already" in body or "déjà" in body or "activ" in body:return {"status":"already"}
        return {"status":"not_eligible"}
    return {"status":"error","code":c}

def oo_get_beneficiary_bundles(msisdn,at,meta,beneficiary):
    h=_web_hdrs(msisdn,at,meta)
    url=f"{OO_BFF}/bundle/others/eligible-bundles?beneficiaryMsisdn={beneficiary}"
    c,_,resp=_oo_req("GET",url,h,timeout=20)
    logging.info(f"[GIFT-LIST] {beneficiary} → {c}")
    if c==401:return {"status":"unauthorized"}
    if c!=200 or not isinstance(resp,dict):return {"status":"error","code":c}
    bundles=_extract_bundles_from_response(resp)
    if not bundles:return {"status":"empty"}
    return {"status":"ok","bundles":bundles}

def _extract_bundles_from_response(resp):
    try:
        rdata=(resp.get("body",{}).get("getBundlesResponse",{}).get("responseData",[]))
        if not isinstance(rdata,list):return []
        out=[]
        for item in rdata:
            b=_normalize_bundle(item)
            if b.get("code"):out.append(b)
        return out
    except Exception as e:
        logging.error(f"[GIFT-LIST] extract: {e}")
        return []

def _normalize_bundle(item):
    attrs=item.get("attributes",{}) or {}
    code=attrs.get("code","") or ""
    name_obj=attrs.get("name",{}) or {}
    name=(name_obj.get("ar") or name_obj.get("en") or name_obj.get("fr") or code)
    price="?"
    instances=attrs.get("instances",[]) or []
    if instances and isinstance(instances[0],dict):
        inst_attrs=instances[0].get("attributes",{}) or {}
        price=inst_attrs.get("price","?") or "?"
    amount=attrs.get("periodic-amount","") or ""
    unit=attrs.get("periodic-unit","") or ""
    validity=_format_validity(amount,unit)
    data_str,extras=_extract_allowances(instances)
    family=attrs.get("product-family","") or ""
    return {"code":code,"name":name,"price":price,"data":data_str,"extras":extras,"validity":validity,"family":family}

def _format_validity(amount,unit):
    try:amt=int(float(amount))
    except:amt=amount
    if not amount:return ""
    units_ar={"day":"يوم","days":"يوم","week":"أسبوع","weeks":"أسبوع","month":"شهر","months":"شهر","hour":"ساعة","hours":"ساعة"}
    u=units_ar.get(str(unit).lower(),unit)
    return f"{amt} {u}".strip()

def _extract_allowances(instances):
    if not instances or not isinstance(instances[0],dict):return "",""
    inst_attrs=instances[0].get("attributes",{}) or {}
    allowances=inst_attrs.get("allowances",[]) or []
    data_parts=[];extras_parts=[]
    dest_icons={"YT":"▶️ YouTube","FB":"📘 Facebook","SC":"👻 Snapchat","IG":"📷 Instagram","Tt":"🎵 TikTok","WA":"💬 WhatsApp"}
    unit_map={"GB":"جيجا","MB":"ميجا","DZD":"دج","MINUTES":"دقيقة","MIN":"دقيقة","HOURS":"ساعة"}
    for a in allowances:
        if not isinstance(a,dict):continue
        aat=a.get("attributes",{}) or {}
        u_type=aat.get("usage-type","") or ""
        u_val=aat.get("usage-value")
        u_unit=aat.get("usage-unit","") or ""
        u_unlim=bool(aat.get("unlimited-usage"))
        dest=aat.get("destination","any") or "any"
        if u_type=="data":
            if u_unlim:
                icon=dest_icons.get(dest,"♾️")
                extras_parts.append(f"{icon} غير محدود")
            else:
                unit_ar=unit_map.get(str(u_unit).upper(),u_unit)
                if dest=="any":data_parts.append(f"{u_val} {unit_ar}".strip())
                else:
                    icon=dest_icons.get(dest,dest)
                    extras_parts.append(f"{icon} {u_val} {unit_ar}".strip())
        elif u_type=="money":extras_parts.append(f"💰 {u_val} دج")
        elif u_type=="voice":
            if u_unlim:extras_parts.append("📞 مكالمات غير محدودة")
            else:extras_parts.append(f"📞 {u_val} دقيقة")
    return (" + ".join(data_parts) if data_parts else ""," | ".join(extras_parts) if extras_parts else "")

def oo_gift_purchase(msisdn,at,meta,bundle_code,beneficiary):
    h=_web_hdrs(msisdn,at,meta,"application/json; charset=utf-8")
    body=json.dumps({"bundleCode":bundle_code,"beneficiary":beneficiary},separators=(",",":"))
    c,_,resp=_oo_req("POST",f"{OO_BFF}/bundle/others/bundle-purchase",h,body.encode(),timeout=30)
    logging.info(f"[GIFT] {msisdn} → {beneficiary} | {c}")
    if c in(200,201):return {"status":"ok","data":resp}
    if c==401:return {"status":"unauthorized"}
    if c==409:
        code=str(resp.get("code") or "") if isinstance(resp,dict) else ""
        body_low=str(resp).lower()
        if "credit" in body_low or "balance" in body_low or "not_enough" in code.lower():return {"status":"no_balance","msg":"رصيدك غير كافٍ"}
        return {"status":"conflict","msg":"الإهداء غير ممكن حالياً"}
    if c==403:return {"status":"not_allowed","msg":"رقم المستفيد غير مؤهل"}
    if c==400:return {"status":"bad_request","msg":"رقم المستفيد غير صحيح"}
    return {"status":"error","code":c,"msg":str(resp)[:150]}

def oo_save(uid,d):(SESSIONS_DIR/f"oo_{uid}.json").write_text(json.dumps(d,ensure_ascii=False))
def oo_load(uid):
    f=SESSIONS_DIR/f"oo_{uid}.json"
    return json.loads(f.read_text()) if f.exists() else None
def oo_clear(uid):
    f=SESSIONS_DIR/f"oo_{uid}.json"
    if f.exists():f.unlink()

def dz_save_session(uid,phone,token):
    try:(SESSIONS_DIR/f"dz_{uid}.json").write_text(json.dumps({"phone":phone,"token":token,"issued_at":time.time()},ensure_ascii=False))
    except:pass
def dz_load_session(uid):
    try:
        f=SESSIONS_DIR/f"dz_{uid}.json"
        return json.loads(f.read_text()) if f.exists() else None
    except:return None
def dz_clear_session(uid):
    try:
        f=SESSIONS_DIR/f"dz_{uid}.json"
        if f.exists():f.unlink()
    except:pass

def o_mask(m):
    if not m:return "?"
    if len(m)>=6:return m[:4]+"xxxx"+m[-2:]
    return m
def dz_mask(m):return "0"+m[3:] if m.startswith("213") else m

def oo_ensure_valid(uid,user):
    if not user or not user.get("access_token"):return None
    issued=user.get("issued_at",0);exp=user.get("expires_in",0)
    if issued and exp and (time.time()-issued)<(exp-1800):return user
    ref=ooredoo_refresh_token_sync(user["msisdn"],user.get("refresh_token",""),{"instance_id":user.get("tok_instance_id"),"plat_sig":user.get("tok_plat_sig"),"fp":user.get("tok_fingerprint")})
    if ref:
        user.update(ref);oo_save(uid,user);return user
    return None

def time_until_spin(last):
    if not last:return {"avail":True,"str":""}
    try:
        s=str(last).replace("Z","+00:00")
        try:ldt=datetime.fromisoformat(s)
        except:ldt=datetime.fromisoformat(s.replace("Z","")).replace(tzinfo=tz(timedelta(hours=1)))
        if ldt.tzinfo is None:ldt=ldt.replace(tzinfo=tz(timedelta(hours=1)))
        next_spin=ldt+timedelta(hours=24)
        now=datetime.now(tz.utc)
        remaining=(next_spin-now).total_seconds()
        if remaining<=0:return {"avail":True,"str":""}
        h=int(remaining//3600);mi=int((remaining%3600)//60)
        parts=[]
        if h>0:parts.append(f"{h} ساعة")
        if mi>0:parts.append(f"{mi} دقيقة")
        if not parts:parts.append("أقل من دقيقة")
        return {"avail":False,"str":" و ".join(parts)}
    except:return {"avail":True,"str":""}

_stop_threads=threading.Event()

def oo_auto_refresh():
    while not _stop_threads.is_set():
        try:
            time.sleep(900)
            for f in list(SESSIONS_DIR.glob("oo_*.json")):
                try:
                    uid_s=f.stem.replace("oo_","")
                    if not uid_s.isdigit():continue
                    u=oo_load(int(uid_s))
                    if not u or not u.get("access_token"):continue
                    issued=u.get("issued_at",0);exp=u.get("expires_in",0)
                    if issued and exp and (time.time()-issued)>=(exp-600):
                        oo_ensure_valid(int(uid_s),u)
                except:pass
        except:pass

def dz_auto_refresh():
    while not _stop_threads.is_set():
        try:
            time.sleep(900)
            for f in list(SESSIONS_DIR.glob("dz_*.json")):
                try:
                    uid_s=f.stem.replace("dz_","")
                    if not uid_s.isdigit():continue
                    s=dz_load_session(int(uid_s))
                    if not s:continue
                    st=dj_check_balance(s["token"],s["phone"])
                    if isinstance(st,dict) and st.get("status")=="EXPIRED":dz_clear_session(int(uid_s))
                except:pass
        except:pass

def steps_saver_worker():
    while not _stop_threads.is_set():
        try:time.sleep(30);save_steps()
        except:pass

def reset_steps_worker():
    while not _stop_threads.is_set():
        try:
            time.sleep(4*3600)
            for uid in list(user_steps.keys()):
                user_steps[uid]={"step":"await_phone","last_activity":time.time()}
            save_steps()
        except:pass

# ==================== النصوص ====================
WELCOME_HEADER=("مرحبا بك في موح بوت 👋\n\n"
"بوت موح يقدم تفعيل عروض انترنت في مختلف الشبكات الجزائرية 🇩🇿\n\n"
"1️⃣ • أدخل الرقم 📱\n2️⃣ • أكمل الخطوات ✅\n"
"3️⃣ • إختر عرض مناسب 🛒\n4️⃣ • انتظار الرد ... 🔍")
WELCOME_FOOTER="للبدء أرسل رقم هاتفك 📱"
OTP_MSG="✅ تم إرسال الرمز بنجاح\n\nيرجى نسخ أو كتابة الرمز المكون من 6 أرقام الذي تلقيته في رسالة على هاتفك 📱"
SOCCER_CLUB_NAMES={"MCA":"مولودية الجزائر","MCO":"مولودية وهران","JSS":"شبيبة الساورة","MOB":"مولودية بجاية","JSD":"شبيبة الجلفة"}

def send_welcome(cid):
    fb_send(cid,WELCOME_HEADER)
    fb_send(cid,WELCOME_FOOTER)

AVAILABLE_OFFERS={
"OFFREJEUNE1200":{"name":"🎁 IZZY 120","price":"120 دج","validity":"30 يوم","data":"10 جيجا","bonus":"يوتيوب","description":"✅ 10 جيجا"},
"DOVINTSPEEDMONTH30GoPRE":{"name":"🚀 1500 دج","price":"1500 دج","validity":"30 يوم","data":"60 جيجا","bonus":"سرعة","description":"✅ 60 جيجا"},
"DOVINTSPEEDMONTH15GoPRE":{"name":"🚀 1000 دج","price":"1000 دج","validity":"30 يوم","data":"30 جيجا","bonus":"سرعة","description":"✅ 30 جيجا"},
"DOVINTSPEEDMONTH6GoPRE":{"name":"🚀 500 دج","price":"500 دج","validity":"30 يوم","data":"12 جيجا","bonus":"سرعة","description":"✅ 12 جيجا"},
"DOVINTSPEEDWEEK3GoPRE":{"name":"🚀 300 دج","price":"300 دج","validity":"7 أيام","data":"10 جيجا","bonus":"سرعة","description":"✅ 10 جيجا"},
"DOVINTSPEEDWEEK2GoPRE":{"name":"🚀 150 دج","price":"150 دج","validity":"7 أيام","data":"4 جيجا","bonus":"سرعة","description":"✅ 4 جيجا"},
"DOVINTSPEEDDAY1GoPRE":{"name":"📱 100 Da - 2GB - 24H","price":"100 دج","validity":"24 ساعة","data":"2 جيجا","bonus":"سرعة","description":"✅ 2 جيجا"},
"DOVINTSPEEDDAY250MoPRE":{"name":"🚀 50 دج","price":"50 دج","validity":"24 ساعة","data":"600 ميجا","bonus":"سرعة","description":"✅ 600 ميجا"},
"DOVINTSPEEDDAY100MoPRE":{"name":"🚀 30 دج","price":"30 دج","validity":"24 ساعة","data":"300 ميجا","bonus":"سرعة","description":"✅ 300 ميجا"},
"MIXTEPRE1500":{"name":"🔄 MIXTE 1500","price":"1500 دج","validity":"30 يوم","data":"40 جيجا","bonus":"3000 دج","description":"✅ 40 جيجا"},
"MIXTEPRE1000":{"name":"🔄 MIXTE 1000","price":"1000 دج","validity":"30 يوم","data":"15 جيجا","bonus":"2000 دج","description":"✅ 15 جيجا"},
"MIXTEPRE100":{"name":"🔄 MIXTE 100","price":"100 دج","validity":"24 ساعة","data":"1 جيجا","bonus":"300 دج","description":"✅ 1 جيجا"},
"MIXTEONNET50":{"name":"🔄 MIXTE ON 50","price":"50 دج","validity":"24 ساعة","data":"60 دقيقة","bonus":"جيزي","description":"✅ 60 دقيقة"},
"FAMILY2000":{"name":"👨‍👩‍👧 FAMILY 2000","price":"2000 دج","validity":"30 يوم","data":"20 جيجا","bonus":"2000 دج","description":"✅ 20 جيجا"},
"FAMILY3000":{"name":"👨‍👩‍👧 FAMILY 3000","price":"3000 دج","validity":"30 يوم","data":"50 جيجا","bonus":"4000 دج","description":"✅ 50 جيجا"},
"FAMILY4000":{"name":"👨‍👩‍👧 FAMILY 4000","price":"4000 دج","validity":"30 يوم","data":"100 جيجا","bonus":"6000 دج","description":"✅ 100 جيجا"},
"BTL10GB72H":{"name":"📱 190 دج - 10GB","price":"190 دج","validity":"72 ساعة","data":"10 جيجا","bonus":"وطني","description":"✅ 10 جيجا"},
"BTL500MBDAY":{"name":"📱 90 دج - 5GB","price":"90 دج","validity":"24 ساعة","data":"5 جيجا","bonus":"وطني","description":"✅ 5 جيجا"},
"BTLDATA2WEEKS":{"name":"📱 400 دج - 4GB","price":"400 دج","validity":"15 يوم","data":"4 جيجا","bonus":"وطني","description":"✅ 4 جيجا"},
"2GBMONTH":{"name":"📱 250 دج - 3GB","price":"250 دج","validity":"30 يوم","data":"3 جيجا","bonus":"وطني","description":"✅ 3 جيجا"},
"1GBFB3DAY":{"name":"📱 70 Da - FB - 3GB - 72H","price":"70 دج","validity":"72 ساعة","data":"3 جيجا فيسبوك","bonus":"فيسبوك فقط","description":"⚠️ فيسبوك فقط"},
"BTLINTSPEEDDAY2Go":{"name":"📱 70 Da - 4GB - 24H","price":"70 دج","validity":"24 ساعة","data":"4 جيجا","bonus":"سرعة","description":"✅ 4 جيجا"}}

FREEFIRE_BUNDLES={"ff500":{"code":"ATL_30D_FREEFIRE_500_v1","name":"FreeFire 500","points":500,"price":500},"ff1000":{"code":"ATL_30D_FREEFIRE_1000_v1","name":"FreeFire 1000","points":1000,"price":1000},"ff2000":{"code":"ATL_30D_FREEFIRE_2000_v1","name":"FreeFire 2000","points":2000,"price":2000},"ff3000":{"code":"ATL_30D_FREEFIRE_3000_v1","name":"FreeFire 3000","points":3000,"price":3000},"ff5000":{"code":"ATL_30D_FREEFIRE_5000_v1","name":"FreeFire 5000","points":5000,"price":5000}}

SPECIAL_BUNDLES={
"sp_wa_15d":{"icon":"💬","name":"واتساب","app":"WA","validity":"Biweekly","validity_ar":"15 يوم","price":50},
"sp_fb_7d":{"icon":"📘","name":"فيسبوك","app":"FB","validity":"Weekly","validity_ar":"أسبوع","price":80},
"sp_fb_30d":{"icon":"📘","name":"فيسبوك","app":"FB","validity":"Monthly","validity_ar":"شهر","price":200},
"sp_ig_15d":{"icon":"📷","name":"انستغرام","app":"IG","validity":"Biweekly","validity_ar":"15 يوم","price":100},
"sp_ig_30d":{"icon":"📷","name":"انستغرام","app":"IG","validity":"Monthly","validity_ar":"شهر","price":200},
"sp_yt_7d":{"icon":"▶️","name":"يوتيوب","app":"YT","validity":"Weekly","validity_ar":"أسبوع","price":80},
"sp_yt_15d":{"icon":"▶️","name":"يوتيوب","app":"YT","validity":"Biweekly","validity_ar":"15 يوم","price":100},
"sp_yt_30d":{"icon":"▶️","name":"يوتيوب","app":"YT","validity":"Monthly","validity_ar":"شهر","price":200},
"sp_tt_15d":{"icon":"🎵","name":"تيك توك","app":"2Go_Tt","validity":"Biweekly","validity_ar":"15 يوم","price":100},
"sp_data_30g":{"icon":"🌐","name":"30 جيجا","app":None,"limited":[{"account":"data","allocation":30}],"validity":"Monthly","validity_ar":"شهر","price":950},
"sp_data_40g":{"icon":"🌐","name":"40 جيجا","app":None,"limited":[{"account":"data","allocation":40}],"validity":"Monthly","validity_ar":"شهر","price":1050},
"sp_data_50g":{"icon":"🌐","name":"50 جيجا","app":None,"limited":[{"account":"data","allocation":50}],"validity":"Monthly","validity_ar":"شهر","price":1250},
"sp_data_60g":{"icon":"🌐","name":"60 جيجا","app":None,"limited":[{"account":"data","allocation":60}],"validity":"Monthly","validity_ar":"شهر","price":1350},
"sp_data_70g":{"icon":"🌐","name":"70 جيجا","app":None,"limited":[{"account":"data","allocation":70}],"validity":"Monthly","validity_ar":"شهر","price":1475},
"sp_data_80g":{"icon":"🌐","name":"80 جيجا","app":None,"limited":[{"account":"data","allocation":80}],"validity":"Monthly","validity_ar":"شهر","price":1600},
"sp_data_90g":{"icon":"🌐","name":"90 جيجا","app":None,"limited":[{"account":"data","allocation":90}],"validity":"Monthly","validity_ar":"شهر","price":1700}}

INTERNET_BUNDLES={
"inet_5g":{"icon":"🔴","name":"5 جيجا - يوم","code":"ATL_24H_DATA_90DZD_5Go","data":"5 جيجا","validity_ar":"يوم","price":90},
"inet_10g":{"icon":"🟠","name":"10 جيجا - 3 أيام","code":"ATL_72H_DATA_190DZD_10Go","data":"10 جيجا","validity_ar":"3 أيام","price":190},
"inet_30g":{"icon":"🟡","name":"30 جيجا - أسبوع","code":"ATL_7D_DATA_490DZD_30Go","data":"30 جيجا","validity_ar":"أسبوع","price":490}}

NOUDJOUM_INFO_TEXT=("⭐ برنامج نجوم — Noudjoum\n━━━━━━━━━━━━━━━━\n\n"
"📖 الوصف:\nبرنامج ولاء من Ooredoo يمنحك نقاط مقابل كل شحن،\nوتحوّلها إلى دقائق / SMS / إنترنت.\n\n"
"🎁 الفوائد:\n• 💰 كل 250 دج شحن شهري = 5 نقاط\n• 🎉 مكافأة ترحيبية عند التسجيل\n• ⏳ النقاط صالحة 24 شهر\n\n"
"📋 الشروط:\n✅ الرقم نشط\n✅ الشريحة مفعّلة منذ أكثر من 3 أشهر")
NOUDJOUM_SUCCESS_TEXT=("🎉 مبروك!\n\n⭐ تم تسجيلك في برنامج نجوم بنجاح\n\n━━━━━━━━━━━━━━━━\n"
"📱 عمليات سريعة:\n• *511*1# — رصيد النقاط\n• *511*2# — استبدال بدقائق\n• *511*3# — استبدال بجوائز")
NOUDJOUM_ALREADY_TEXT=("✅ أنت مسجّل مسبقاً في نجوم\n\n📱 *511*1# — رصيد النقاط\n📱 *511*2# — استبدال بدقائق")
NOUDJOUM_LOCKED_TEXT=("🔒 غير مؤهل لبرنامج نجوم\n\n❌ أحد الشروط التالية غير مستوفى:\n• الشريحة أقل من 3 أشهر\n• الرقم غير نشط\n\n📞 خدمة العملاء: 333")
GIFT_INFO_TEXT=("🎁 إهداء اشتراك\n━━━━━━━━━━━━━━━━\n\n📖 الوصف:\nأهدِ باقة إنترنت لأي رقم Ooredoo آخر.\nالمبلغ يُخصم من رصيدك.\n\n"
"⚠️ ملاحظة: لا يمكن الإهداء لنفس الرقم\n\n📱 أدخل رقم المستفيد:\nمثال: 05XXXXXXXX")

def get_stats_text():
    s=db_query("""SELECT total_1gb,total_2gb,total_3gb,total_offers,oo_logins,oo_snap,oo_youtube,oo_byop30,oo_byop40,oo_bundles,oo_spins,oo_balance,oo_offers_view,dz_logins,oo_gaming_view,oo_ff_bought,sp_yt,sp_ig,sp_fb,sp_wa,sp_tt,inet_5g,inet_10g,inet_30g,oo_gifts,sp_data_30g,sp_data_40g,sp_data_50g,sp_data_60g,sp_data_70g,sp_data_80g,sp_data_90g,oo_soccer_enrolls,oo_stars_activated,oo_gifts_sent FROM stats WHERE id=1""",fetch=True)
    if not s:s=(0,)*34
    while len(s)<34:s=s+(0,)
    users=db_query("SELECT COUNT(*) FROM users",fetch=True)[0] or 0
    dz=db_query("SELECT COUNT(*) FROM numbers",fetch=True)[0] or 0
    return(f"📊 الإحصائيات\n👥 {users} | 📱 {dz}\n\n🔴 جيزي:\n  🎁 1G: {s[0]} | 2G: {s[1]} | 3G: {s[2]}\n  💰 العروض: {s[3]}\n\n🟠 أوريدو:\n  🔐: {s[4]}  👻: {s[5]}  🎡: {s[10]}\n  ⚽️ Sport: {s[32]} | 🎮 FF: {s[15]}\n  ⭐ نجوم: {s[33]} | 🎁 إهداءات: {s[34] if len(s)>34 else 0}\n\n⚡ تطبيقات: ▶️{s[16]} 📷{s[17]} 📘{s[18]} 💬{s[19]} 🎵{s[20]}\n🌐 إنترنت: 🔴{s[21]} 🟠{s[22]} 🟡{s[23]}")

# ==================== القوائم النصية ====================
def DZ_MENU(uid=None):
    txt=("🔴 جيزي\n📋 القائمة:\n"
    "1️⃣ تفعيل 1 جيجا (يومي)\n"
    "2️⃣ تفعيل 2 جيجا (أسبوعي)\n"
    "3️⃣ تفعيل 3 جيجا\n"
    "4️⃣ كشف الرصيد\n"
    "5️⃣ عرض 70 دج - 4GB\n"
    "6️⃣ عرض 90 دج - 5GB\n"
    "7️⃣ 100 دج - 2GB\n"
    "8️⃣ 190 دج - 10GB\n"
    "9️⃣ العروض الكاملة\n"
    "🔟 تغيير الرقم")
    return txt

def OO_MENU(services=None,uid=None):
    lines=["🟠 أوريدو\n📋 القائمة:"]
    lines.append("1️⃣ كشف الرصيد")
    lines.append("2️⃣ عروضي")
    is_yooz=services.get("is_yooz",False) if services else False
    if is_yooz:
        lines.append("3️⃣ سناب ✅")
    else:
        lines.append("3️⃣ سناب 🔒")
    if not is_yooz:
        lines.append("4️⃣ Ooredoo Sport")
        lines.append("5️⃣ Free Fire")
    lines.append("6️⃣ هديتي")
    lines.append("7️⃣ عروض خاصة")
    lines.append("8️⃣ إنترنت")
    lines.append("9️⃣ الباقات")
    lines.append("🔟 الإعدادات")
    return "\n".join(lines)

def OO_SETTINGS_MENU(services=None):
    is_yooz=services.get("is_yooz",False) if services else False
    lines=["⚙️ الإعدادات:"]
    if not is_yooz:lines.append("1️⃣ نجوم Noudjoum")
    else:lines.append("1️⃣ نجوم ❌ (غير متاح لـ YOOZ)")
    lines.append("2️⃣ إهداء اشتراك")
    lines.append("3️⃣ تغيير الرقم")
    lines.append("↩️ رجوع → اكتب 0")
    return "\n".join(lines)

# ==================== المعالج ====================
def handle_message(uid,text):
    text=text.strip()
    if not text:return
    now=time.time()
    cur=user_steps.get(uid,{})
    step=cur.get("step","await_phone")
    last_activity=cur.get("last_activity",0)
    if step in("dz_menu","oo_menu") and last_activity and (now-last_activity)>INACTIVITY_SECONDS:
        user_steps[uid]={"step":"await_phone","last_activity":now}
        send_welcome(uid);return
    digits=re.sub(r"\D","",text)
    is_phone=re.match(r"^0[567]\d{8}$",digits) is not None

    # ===== رقم جديد =====
    if step=="await_phone":
        if not is_phone:send_welcome(uid);return
        msisdn="213"+digits[1:]
        if digits.startswith(("07","06")):
            row=db_query("SELECT token FROM numbers WHERE phone=? AND user_id=?",(msisdn,uid),fetch=True)
            if row and row[0] and row[0]!="EXPIRED":
                user_steps[uid]={"step":"dz_menu","phone":msisdn,"last_activity":now}
                fb_send(uid,f"📱 {dz_mask(msisdn)} ✅\n🔴 جيزي\n\n{DZ_MENU(uid)}");return
            fb_typing(uid)
            ok=dj_request_otp(msisdn)
            if ok:
                user_steps[uid]={"step":"dz_verify_otp","phone":msisdn,"display":digits,"last_activity":now}
                fb_send(uid,OTP_MSG)
            else:fb_send(uid,"❌ تعذر إرسال الرمز")
            return
        if digits.startswith("05"):
            existing=oo_load(uid)
            if existing and existing.get("msisdn")==msisdn and existing.get("access_token"):
                user_steps[uid]={"step":"oo_menu","last_activity":now}
                send_oo_menu(uid,existing);return
            fb_typing(uid)
            result=ooredoo_send_otp_sync(msisdn)
            if not result.get("otp_sent"):
                r=result.get("reason","");code=result.get("status","?")
                if r=="rate_limit":msg="⏳ محاولات كثيرة، انتظر 60 ثانية"
                elif r=="network":msg="❌ مشكل في الاتصال"
                else:msg=f"❌ تعذر الإرسال\n💡 كود: {code}"
                fb_send(uid,msg);return
            user_steps[uid]={"step":"oo_await_otp","msisdn":msisdn,"device":result["device"],"last_activity":now}
            fb_send(uid,OTP_MSG);return
        send_welcome(uid);return

    # ===== OTP جيزي =====
    if step=="dz_verify_otp":
        if not text.isdigit() or len(text)!=6:fb_send(uid,"❌ 6 أرقام");return
        phone=cur.get("phone")
        fb_typing(uid)
        token=dj_verify_otp(phone,text)
        if token and token!="EXPIRED":
            db_query("INSERT OR REPLACE INTO numbers (phone,user_id,token,added_date) VALUES (?,?,?,?)",(phone,uid,token,datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            dz_save_session(uid,phone,token)
            db_query("INSERT OR IGNORE INTO users (user_id,username,join_date,is_logged_in) VALUES (?,?,?,1)",(uid,"fb",datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            db_query("UPDATE users SET is_logged_in=1 WHERE user_id=?",(uid,))
            inc_stat("dz_logins")
            user_steps[uid]={"step":"dz_menu","phone":phone,"last_activity":time.time()}
            fb_send(uid,f"✅ تم التحقق!\n📱 {dz_mask(phone)}\n\n{DZ_MENU(uid)}")
        else:fb_send(uid,"❌ الرمز خاطئ")
        return

    # ===== OTP أوريدو =====
    if step=="oo_await_otp":
        m=re.search(r"\b(\d{6})\b",text)
        if not m:fb_send(uid,"⚠️ ابعث 6 أرقام");return
        otp=m.group(1);ms=cur.get("msisdn");device=cur.get("device",{})
        fb_typing(uid)
        result=ooredoo_verify_otp_sync(ms,otp,device)
        if result=="wrong_otp":fb_send(uid,"❌ الرمز خاطئ");return
        if not result:fb_send(uid,"❌ فشل التحقق");return
        user={"msisdn":ms,"device":device,**result}
        oo_save(uid,user)
        inc_stat("oo_logins")
        db_query("INSERT OR IGNORE INTO users (user_id,username,join_date,is_logged_in) VALUES (?,?,?,1)",(uid,"fb",datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        db_query("UPDATE users SET is_logged_in=1 WHERE user_id=?",(uid,))
        user_steps[uid]={"step":"oo_menu","last_activity":time.time()}
        send_oo_menu(uid,user);return

    # ===== قائمة جيزي =====
    if step=="dz_menu":
        phone=cur.get("phone")
        row=db_query("SELECT token FROM numbers WHERE phone=?",(phone,),fetch=True)
        if not row or row[0]=="EXPIRED":
            user_steps[uid]={"step":"await_phone","last_activity":now};send_welcome(uid);return
        token=row[0]
        if text=="1":
            fb_typing(uid)
            last=(db_query("SELECT last_activation_1gb FROM numbers WHERE phone=?",(phone,),fetch=True) or [0])[0] or 0
            if time.time()-last<COOLDOWN_1GB:
                r=int(COOLDOWN_1GB-(time.time()-last));fb_send(uid,f"❌ لم تكمل 24س\n⏱️ {r//3600}س {(r%3600)//60}د");return
            fb_send(uid,"⏳ جاري التفعيل...")
            res=dj_activate_1gb(token,phone)
            if res=="SUCCESS":
                db_query("UPDATE numbers SET last_activation_1gb=? WHERE phone=?",(time.time(),phone))
                inc_stat("total_1gb");fb_send(uid,f"✅ تم تفعيل 1 جيجا 🎉\n📱 {dz_mask(phone)}")
            elif res=="EXPIRED":
                db_query("UPDATE numbers SET token='EXPIRED' WHERE phone=?",(phone,))
                user_steps[uid]={"step":"await_phone","last_activity":now};fb_send(uid,"⚠️ انتهت الجلسة")
            elif res=="LIMIT":fb_send(uid,"⚠️ لم تكمل 24 ساعة")
            else:fb_send(uid,"❌ فشل")
            return
        if text=="2":
            fb_typing(uid)
            last=(db_query("SELECT last_activation_2gb FROM numbers WHERE phone=?",(phone,),fetch=True) or [0])[0] or 0
            if time.time()-last<COOLDOWN_2GB:fb_send(uid,"❌ لم تكمل أسبوع");return
            fb_send(uid,"⏳ جاري التفعيل...")
            res=dj_activate_2gb(token,phone)
            if res=="SUCCESS":
                db_query("UPDATE numbers SET last_activation_2gb=? WHERE phone=?",(time.time(),phone))
                inc_stat("total_2gb");fb_send(uid,"✅ تم تفعيل 2 جيجا 🎉")
            elif res=="EXPIRED":
                db_query("UPDATE numbers SET token='EXPIRED' WHERE phone=?",(phone,))
                user_steps[uid]={"step":"await_phone","last_activity":now};fb_send(uid,"⚠️ انتهت")
            elif res=="NO_BALANCE":fb_send(uid,"❌ الرصيد غير كافي")
            elif res=="LIMIT":fb_send(uid,"⚠️ لم تكمل الأسبوع")
            else:fb_send(uid,"❌ فشل")
            return
        if text=="3":
            fb_typing(uid)
            last=(db_query("SELECT last_activation_3gb FROM numbers WHERE phone=?",(phone,),fetch=True) or [0])[0] or 0
            if time.time()-last<COOLDOWN_3GB:fb_send(uid,"❌ لم تكمل أسبوع");return
            fb_send(uid,"⏳ جاري التفعيل...")
            res=dj_activate_3gb(token,phone)
            if res=="SUCCESS":
                db_query("UPDATE numbers SET last_activation_3gb=? WHERE phone=?",(time.time(),phone))
                inc_stat("total_3gb");fb_send(uid,"✅ تم تفعيل 3 جيجا 🎉")
            elif res=="EXPIRED":
                db_query("UPDATE numbers SET token='EXPIRED' WHERE phone=?",(phone,))
                user_steps[uid]={"step":"await_phone","last_activity":now};fb_send(uid,"⚠️ انتهت")
            else:fb_send(uid,"❌ فشل")
            return
        if text=="4":
            fb_typing(uid)
            result=dj_check_balance(token,phone)
            if result.get("status")=="EXPIRED":
                db_query("UPDATE numbers SET token='EXPIRED' WHERE phone=?",(phone,))
                user_steps[uid]={"step":"await_phone","last_activity":now};fb_send(uid,"⚠️ انتهت");return
            if result.get("status")=="FAILED":fb_send(uid,"❌ تعذر الجلب");return
            bal=result.get("balance",0);due=result.get("due",0)
            t=f"💳 رصيد الرقم\n📱 {dz_mask(phone)}\n━━━━━━━━━━━━━━━\n💰 الرصيد: {bal} دج"
            if due>0:t+=f"\n⚠️ الدين: {due} دج"
            fb_send(uid,t);return
        if text=="5":
            fb_typing(uid)
            r=dz_activate_offer_70_4g(token,phone)
            if r.get("token_expired"):
                db_query("UPDATE numbers SET token='EXPIRED' WHERE phone=?",(phone,))
                user_steps[uid]={"step":"await_phone","last_activity":now};fb_send(uid,r["msg"]);return
            if r.get("success"):
                db_query("UPDATE numbers SET last_activation_offers=? WHERE phone=?",(time.time(),phone));inc_stat("total_offers")
            fb_send(uid,r["msg"]);return
        if text=="6":
            fb_typing(uid)
            r=dz_activate_offer_90_5g(token,phone)
            if r.get("token_expired"):
                db_query("UPDATE numbers SET token='EXPIRED' WHERE phone=?",(phone,))
                user_steps[uid]={"step":"await_phone","last_activity":now};fb_send(uid,r["msg"]);return
            if r.get("success"):
                db_query("UPDATE numbers SET last_activation_offers=? WHERE phone=?",(time.time(),phone));inc_stat("total_offers")
            fb_send(uid,r["msg"]);return
        if text=="7":
            fb_typing(uid)
            o=AVAILABLE_OFFERS.get("DOVINTSPEEDDAY1GoPRE")
            r=dz_activate_paid_offer(token,phone,"DOVINTSPEEDDAY1GoPRE","shake",o["name"],100)
            if r.get("token_expired"):
                db_query("UPDATE numbers SET token='EXPIRED' WHERE phone=?",(phone,))
                user_steps[uid]={"step":"await_phone","last_activity":now};fb_send(uid,r["msg"]);return
            if r.get("success"):
                db_query("UPDATE numbers SET last_activation_offers=? WHERE phone=?",(time.time(),phone));inc_stat("total_offers")
            fb_send(uid,r["msg"]);return
        if text=="8":
            fb_typing(uid)
            o=AVAILABLE_OFFERS.get("BTL10GB72H")
            r=dz_activate_paid_offer(token,phone,"BTL10GB72H","shake",o["name"],190)
            if r.get("token_expired"):
                db_query("UPDATE numbers SET token='EXPIRED' WHERE phone=?",(phone,))
                user_steps[uid]={"step":"await_phone","last_activity":now};fb_send(uid,r["msg"]);return
            if r.get("success"):
                db_query("UPDATE numbers SET last_activation_offers=? WHERE phone=?",(time.time(),phone));inc_stat("total_offers")
            fb_send(uid,r["msg"]);return
        if text=="9":
            lines=["🌐 العروض الكاملة:"]
            codes=["DOVINTSPEEDMONTH30GoPRE","DOVINTSPEEDMONTH15GoPRE","DOVINTSPEEDMONTH6GoPRE","DOVINTSPEEDWEEK3GoPRE","DOVINTSPEEDWEEK2GoPRE","DOVINTSPEEDDAY1GoPRE","DOVINTSPEEDDAY250MoPRE","DOVINTSPEEDDAY100MoPRE","MIXTEPRE1500","MIXTEPRE1000","MIXTEPRE100","MIXTEONNET50","FAMILY2000","FAMILY3000","FAMILY4000","BTL10GB72H","BTL500MBDAY","BTLINTSPEEDDAY2Go"]
            for i,code in enumerate(codes,1):
                o=AVAILABLE_OFFERS.get(code,{})
                lines.append(f"{i}. {o.get('name')} - {o.get('price')}")
            lines.append("\n📩 ابعث رقم العرض")
            user_steps[uid]["step"]="dz_offer_pick";user_steps[uid]["last_activity"]=now
            fb_send(uid,"\n".join(lines));return
        if text=="10":
            oo_clear(uid);dz_clear_session(uid)
            user_steps[uid]={"step":"await_phone","last_activity":now};send_welcome(uid);return
        fb_send(uid,DZ_MENU(uid));return

    # ===== اختيار عرض جيزي =====
    if step=="dz_offer_pick":
        phone=cur.get("phone")
        codes=["DOVINTSPEEDMONTH30GoPRE","DOVINTSPEEDMONTH15GoPRE","DOVINTSPEEDMONTH6GoPRE","DOVINTSPEEDWEEK3GoPRE","DOVINTSPEEDWEEK2GoPRE","DOVINTSPEEDDAY1GoPRE","DOVINTSPEEDDAY250MoPRE","DOVINTSPEEDDAY100MoPRE","MIXTEPRE1500","MIXTEPRE1000","MIXTEPRE100","MIXTEONNET50","FAMILY2000","FAMILY3000","FAMILY4000","BTL10GB72H","BTL500MBDAY","BTLINTSPEEDDAY2Go"]
        if not text.isdigit() or not(1<=int(text)<=len(codes)):
            fb_send(uid,"❌ رقم غالط");return
        code=codes[int(text)-1];o=AVAILABLE_OFFERS.get(code,{})
        row=db_query("SELECT token FROM numbers WHERE phone=?",(phone,),fetch=True)
        if not row:user_steps[uid]={"step":"await_phone","last_activity":now};send_welcome(uid);return
        fb_typing(uid);fb_send(uid,f"⏳ جاري تفعيل {o.get('name')}...")
        price=dj_extract_price(o.get('price','0')) or 0
        of_type="shake" if code.startswith("BTL") else "activate"
        r=dz_activate_paid_offer(row[0],phone,code,of_type,o.get("name","العرض"),price)
        if r.get("token_expired"):
            db_query("UPDATE numbers SET token='EXPIRED' WHERE phone=?",(phone,))
            user_steps[uid]={"step":"await_phone","last_activity":now};fb_send(uid,r["msg"]);return
        if r.get("success"):
            db_query("UPDATE numbers SET last_activation_offers=? WHERE phone=?",(time.time(),phone));inc_stat("total_offers")
        user_steps[uid]["step"]="dz_menu";user_steps[uid]["last_activity"]=now
        fb_send(uid,r["msg"]);return

    # ===== قائمة أوريدو =====
    if step=="oo_menu":
        user=oo_load(uid)
        if not user:user_steps[uid]={"step":"await_phone","last_activity":now};send_welcome(uid);return
        user=oo_ensure_valid(uid,user)
        if not user:user_steps[uid]={"step":"await_phone","last_activity":now};fb_send(uid,"⚠️ انتهت الجلسة");return
        ms=user["msisdn"];at=user["access_token"]
        meta={k:user.get(k,"") for k in["tok_instance_id","tok_plat_sig","tok_fingerprint","tok_timestamp"]}
        qd=oo_quick_detect(at)
        is_yooz=qd.get("is_yooz",False)
        if text=="1":
            fb_typing(uid);inc_stat("oo_balance")
            r=oo_check_balance(ms,at,meta)
            if r["status"]=="ok":
                try:b=float(r.get("data",{}).get("accountBalance",0) or 0)
                except:b=0
                p=oo_get_profile(ms,at,meta)
                prof=""
                if isinstance(p,dict) and p.get("status")=="ok":
                    pd=p.get("data",{})
                    if pd.get("ratePlan"):prof+=f"\n🎁 العرض: {pd.get('ratePlan')}"
                    if pd.get("startDate"):prof+=f"\n📅 {pd.get('startDate')[:10]}"
                fb_send(uid,f"💰 {b} دج\n📱 {o_mask(ms)}{prof}")
            elif r["status"]=="unauthorized":user_steps[uid]={"step":"await_phone","last_activity":now};oo_clear(uid);fb_send(uid,"⚠️ انتهت")
            else:fb_send(uid,"❌")
            return
        if text=="2":
            fb_typing(uid);inc_stat("oo_offers_view")
            r=oo_get_active(ms,at,meta)
            if r["status"]!="ok":fb_send(uid,"❌");return
            d=r.get("data",{})
            lines=[f"📋 عروضك\n💰 {d.get('accountBalance','?')} دج\n"]
            snap=d.get("snapchatAllocation")
            if snap and isinstance(snap,dict):
                acc=snap.get("account",{})
                if acc and acc.get("account"):
                    exp=(acc.get("expiryDate") or "")[:10]
                    lines.append(f"👻 Snapchat — 💎 {acc.get('balance','?')}")
                    if exp:lines.append(f"   📅 {exp}")
            byob=d.get("byobBundlesPackage",{})
            if isinstance(byob,dict):
                for bnd in byob.get("dynamicBundle") or []:
                    if not isinstance(bnd,dict):continue
                    exp_s=(bnd.get("expiryDate") or "")[:10]
                    for lim in (bnd.get("limitedAccountListInformations",{}).get("limitedAccountListInformations",[]) or []):
                        if not isinstance(lim,dict):continue
                        n=lim.get("limitedAccountName","")
                        v=lim.get("limitedAccountValue","?")
                        u=lim.get("limitedAccountUnit","")
                        lines.append(f"📦 {n}: {v} {u}")
                        if exp_s:lines.append(f"   📅 {exp_s}")
                    for u_ in (bnd.get("unlimitedAccountListInformations",{}).get("unlimitedAccountListInformations",[]) or []):
                        if not isinstance(u_,dict):continue
                        lines.append(f"♾️ {u_.get('unlimitedAccountName','')}")
                        if exp_s:lines.append(f"   📅 {exp_s}")
            if len(lines)<=2:lines.append("📭 لا توجد باقات نشطة")
            fb_send(uid,"\n".join(lines));return
        if text=="3":
            fb_typing(uid)
            if is_yooz:
                r=oo_activate_snapchat(ms,at,meta)
                if r=="ok":inc_stat("oo_snap");fb_send(uid,f"✅ تم تفعيل سناب!\n📱 {o_mask(ms)}")
                elif r=="already_active":fb_send(uid,"⚠️ مفعلة مسبقاً")
                elif r=="unauthorized":user_steps[uid]={"step":"await_phone","last_activity":now};oo_clear(uid);fb_send(uid,"⚠️ انتهت")
                else:fb_send(uid,"❌")
            else:
                fb_send(uid,f"👻 سناب شات\n❌ متاح لأرقام N'YOOZ فقط\n📦 عرضك: {qd.get('rate_plan') or 'غير معروف'}")
            return
        if text=="4" and not is_yooz:
            fb_typing(uid)
            elig=oo_soccer_eligibility(ms,at,meta)
            if elig.get("status")=="unauthorized":user_steps[uid]={"step":"await_phone","last_activity":now};oo_clear(uid);fb_send(uid,"⚠️ انتهت");return
            if elig.get("status")!="ok":fb_send(uid,"❌");return
            if elig.get("enrolled"):
                team=elig.get("selected_team","")
                nm=SOCCER_CLUB_NAMES.get(team,team) if team else "؟"
                fb_send(uid,f"✅ مشترك مسبقاً\n🏆 {nm} ({team})");return
            if not elig.get("eligible"):fb_send(uid,"❌ غير مؤهّل");return
            r=oo_soccer_clubs(ms,at,meta)
            if r["status"]!="ok":fb_send(uid,"❌ تعذر جلب الأندية");return
            clubs=r.get("clubs",[])
            lines=["⚽️ Ooredoo Sport\n🎁 كل هدف = 1GB\n⚠️ ما تبدلش النادي\n\n🏆 اختر نادي:"]
            for i,c in enumerate(clubs[:20],1):
                nm=SOCCER_CLUB_NAMES.get(c["code"],c["code"])
                lines.append(f"{i}. {nm}")
            lines.append("\n📩 ابعث رقم النادي")
            user_steps[uid]["step"]="oo_soccer_pick";user_steps[uid]["clubs"]=clubs;user_steps[uid]["last_activity"]=now
            fb_send(uid,"\n".join(lines));return
        if text=="5" and not is_yooz:
            lines=["🎮 Free Fire:"]
            for i,(k,v) in enumerate(FREEFIRE_BUNDLES.items(),1):
                lines.append(f"{i}. {v['name']} — {v['price']} دج")
            lines.append("\n📩 ابعث الرقم")
            user_steps[uid]["step"]="oo_ff_pick";user_steps[uid]["last_activity"]=now
            fb_send(uid,"\n".join(lines));return
        if text=="6":
            fb_typing(uid)
            s=oo_spin_status(ms,at,meta)
            if s["status"]=="unauthorized":user_steps[uid]={"step":"await_phone","last_activity":now};oo_clear(uid);fb_send(uid,"⚠️ انتهت");return
            if s["status"]!="ok":fb_send(uid,"❌");return
            d=s.get("data",{})
            if d.get("played"):
                lt=d.get("lastPlayedTime") or d.get("playedTime") or ""
                ti=time_until_spin(lt)
                if ti["avail"]:fb_send(uid,"🎁 جربت حظك اليوم\n💡 جرب غداً")
                else:fb_send(uid,f"🎁 جربت حظك اليوم\n⏳ بعد: {ti['str']}")
                return
            r=oo_spin_wheel(ms,at,meta)
            if r["status"]=="ok":
                inc_stat("oo_spins");g=r.get("gift")
                if g:
                    inc_stat("oo_gifts");v=r.get("validity_hour")
                    vs=f"\n⏰ {v} ساعة" if v else ""
                    fb_send(uid,f"🎉 مبروك!\n🎁 {g}{vs}\n📱 {o_mask(ms)}")
                else:fb_send(uid,"😅 ما ربحتش هالمرة")
            elif r["status"]=="already_played":fb_send(uid,"🎁 جربت حظك اليوم")
            elif r["status"]=="not_eligible":fb_send(uid,"🎁 الرقم غير مؤهّل")
            else:fb_send(uid,"❌")
            return
        if text=="7":
            lines=["⚡ العروض الخاصة:"]
            for i,(k,v) in enumerate(SPECIAL_BUNDLES.items(),1):
                lines.append(f"{i}. {v['icon']} {v['price']} دج - {v['name']}")
            lines.append("\n📩 ابعث الرقم")
            user_steps[uid]["step"]="oo_sp_pick";user_steps[uid]["last_activity"]=now
            fb_send(uid,"\n".join(lines));return
        if text=="8":
            lines=["🌐 باقات إنترنت:"]
            for i,(k,v) in enumerate(INTERNET_BUNDLES.items(),1):
                lines.append(f"{i}. {v['icon']} {v['price']} دج — {v['data']}")
            lines.append("\n📩 ابعث الرقم")
            user_steps[uid]["step"]="oo_inet_pick";user_steps[uid]["last_activity"]=now
            fb_send(uid,"\n".join(lines));return
        if text=="9":
            fb_typing(uid)
            r=oo_get_plans(ms,at,meta)
            if r["status"]=="ok":
                plans=r.get("plans",[])
                if not plans:fb_send(uid,"📋 ما كايناش")
                else:
                    lines=["📋 الباقات:"]
                    for p in plans:
                        det=p.get("details",{})
                        lines.append(f"• {p.get('offer','?')} — {det.get('price','?')} دج")
                    fb_send(uid,"\n".join(lines))
            else:fb_send(uid,"❌")
            return
        if text=="10":
            fb_send(uid,OO_SETTINGS_MENU(qd))
            user_steps[uid]["step"]="oo_settings";user_steps[uid]["last_activity"]=now;return
        fb_send(uid,OO_MENU(qd,uid));return

    # ===== إعدادات أوريدو =====
    if step=="oo_settings":
        user=oo_load(uid)
        if not user:user_steps[uid]={"step":"await_phone","last_activity":now};send_welcome(uid);return
        user=oo_ensure_valid(uid,user)
        if not user:user_steps[uid]={"step":"await_phone","last_activity":now};fb_send(uid,"⚠️ انتهت");return
        ms=user["msisdn"];at=user["access_token"]
        meta={k:user.get(k,"") for k in["tok_instance_id","tok_plat_sig","tok_fingerprint","tok_timestamp"]}
        qd=oo_quick_detect(at)
        if text=="1":
            if qd.get("is_yooz"):
                fb_send(uid,"❌ نجوم غير متاح لأرقام N'YOOZ");user_steps[uid]["step"]="oo_menu";return
            fb_typing(uid)
            st=oo_check_noudjoum_status(ms,at,meta)
            prof=oo_get_profile(ms,at,meta)
            months=0
            if isinstance(prof,dict) and prof.get("status")=="ok":
                pd=prof.get("data",{})
                start=pd.get("startDate") or ""
                if start:
                    try:
                        sd=datetime.fromisoformat(start.replace("Z","+00:00"))
                        months=int((datetime.now(tz.utc)-sd).days/30)
                    except:pass
            if st.get("status")=="unauthorized":user_steps[uid]={"step":"await_phone","last_activity":now};oo_clear(uid);fb_send(uid,"🔐 انتهت");return
            if months>0 and months<3:
                fb_send(uid,NOUDJOUM_INFO_TEXT+f"\n\n🔒 غير مؤهل بعد\n📅 عمر الشريحة: {months} شهر\n⏳ تحتاج: 3 أشهر\n📊 الفرق: {3-months} شهر")
                user_steps[uid]["step"]="oo_menu";return
            txt=NOUDJOUM_INFO_TEXT
            if months>0:txt+=f"\n\n📅 شريحتك نشطة منذ: {months} شهر"
            stv=st.get("status","unknown")
            if stv=="enrolled":
                txt+=f"\n\n✅ مسجّل — رصيدك: {st.get('points',0)} نقطة\n\nاكتب 'تحقق' للتحقق"
            elif stv=="not_enrolled":
                txt+="\n\n❌ غير مسجّل — اكتب 'سجل' للتسجيل"
            else:txt+="\n\n⚠️ اكتب 'سجل' للتسجيل مباشرة"
            user_steps[uid]["step"]="oo_noudj";user_steps[uid]["last_activity"]=now
            fb_send(uid,txt);return
        if text=="2":
            user_steps[uid]={"step":"oo_gift_await_number","last_activity":now}
            fb_send(uid,GIFT_INFO_TEXT);return
        if text=="3":
            oo_clear(uid);dz_clear_session(uid)
            user_steps[uid]={"step":"await_phone","last_activity":now};send_welcome(uid);return
        if text=="0":
            user_steps[uid]["step"]="oo_menu";user_steps[uid]["last_activity"]=now
            send_oo_menu(uid,user);return
        fb_send(uid,OO_SETTINGS_MENU(qd));return

    # ===== نجوم =====
    if step=="oo_noudj":
        user=oo_load(uid)
        if not user:user_steps[uid]={"step":"await_phone","last_activity":now};send_welcome(uid);return
        user=oo_ensure_valid(uid,user)
        if not user:user_steps[uid]={"step":"await_phone","last_activity":now};fb_send(uid,"⚠️ انتهت");return
        ms=user["msisdn"];at=user["access_token"]
        meta={k:user.get(k,"") for k in["tok_instance_id","tok_plat_sig","tok_fingerprint","tok_timestamp"]}
        if text in("سجل","تسجيل"):
            fb_typing(uid)
            r=oo_enroll_noudjoum(ms,at,meta)
            if r.get("status")=="unauthorized":user_steps[uid]={"step":"await_phone","last_activity":now};oo_clear(uid);fb_send(uid,"🔐");return
            if r.get("status")=="ok":inc_stat("oo_stars_activated");fb_send(uid,NOUDJOUM_SUCCESS_TEXT)
            elif r.get("status")=="already":fb_send(uid,NOUDJOUM_ALREADY_TEXT)
            elif r.get("status")=="not_eligible":fb_send(uid,NOUDJOUM_LOCKED_TEXT)
            else:fb_send(uid,"❌ فشل التسجيل")
            user_steps[uid]["step"]="oo_menu";return
        if text in("تحقق","تحقق مجدداً"):
            fb_typing(uid)
            st=oo_check_noudjoum_status(ms,at,meta)
            if st.get("status")=="enrolled":fb_send(uid,f"✅ مسجّل\n💰 {st.get('points',0)} نقطة")
            elif st.get("status")=="not_enrolled":fb_send(uid,"❌ غير مسجّل")
            else:fb_send(uid,"⚠️ تعذر")
            user_steps[uid]["step"]="oo_menu";return
        if text=="0":
            user_steps[uid]["step"]="oo_menu";send_oo_menu(uid,user);return
        fb_send(uid,"📩 ابعث 'سجل' أو 'تحقق'");return

    # ===== إهداء - رقم =====
    if step=="oo_gift_await_number":
        dg=re.sub(r"\D","",text)
        if not re.match(r"^05\d{8}$",dg):
            fb_send(uid,"❌ رقم غير صحيح\nمثال: 05XXXXXXXX");return
        beneficiary="213"+dg[1:]
        user=oo_load(uid)
        if not user:fb_send(uid,"❌ جلسة");return
        ms_l=user["msisdn"]
        if beneficiary==ms_l:
            fb_send(uid,"🚫 لا يمكن الإهداء لنفس الرقم");return
        at_l=user["access_token"]
        meta_l={k:user.get(k,"") for k in["tok_instance_id","tok_plat_sig","tok_fingerprint","tok_timestamp"]}
        fb_typing(uid)
        r=oo_get_beneficiary_bundles(ms_l,at_l,meta_l,beneficiary)
        if r.get("status")=="unauthorized":
            user_steps[uid]={"step":"await_phone","last_activity":now}
            fb_send(uid,"🔐 انتهت الجلسة");return
        if r.get("status")!="ok" or not r.get("bundles"):
            user_steps[uid]={"step":"await_phone","last_activity":now}
            fb_send(uid,f"⚠️ تعذر جلب العروض\n✅ {dg}");return
        user_steps[uid]={"step":"oo_gift_await_bundle","gift_beneficiary":beneficiary,"gift_bundles":r["bundles"],"last_activity":time.time()}
        fb_send(uid,oo_format_gift_list_text(r["bundles"],beneficiary))
        fb_send(uid,"👇 ابعث رقم العرض (1, 2, 3...)");return

    # ===== إهداء - اختيار عرض =====
    if step=="oo_gift_await_bundle":
        if not text.isdigit():fb_send(uid,"❌");return
        idx=int(text)-1
        bundles=cur.get("gift_bundles",[])
        if idx<0 or idx>=len(bundles):fb_send(uid,"❌");return
        b=bundles[idx]
        user=oo_load(uid)
        if not user:user_steps[uid]={"step":"await_phone","last_activity":now};send_welcome(uid);return
        user=oo_ensure_valid(uid,user)
        if not user:user_steps[uid]={"step":"await_phone","last_activity":now};fb_send(uid,"⚠️ انتهت");return
        ms=user["msisdn"];at=user["access_token"]
        meta={k:user.get(k,"") for k in["tok_instance_id","tok_plat_sig","tok_fingerprint","tok_timestamp"]}
        fb_typing(uid);fb_send(uid,"⏳ جاري الإهداء...")
        r=oo_gift_purchase(ms,at,meta,b.get("code"),cur.get("gift_beneficiary"))
        if r.get("status")=="ok":
            inc_stat("oo_gifts_sent")
            fb_send(uid,f"🎉 تم الإهداء!\n📦 {b.get('name')}\n💳 {b.get('price')} دج")
        elif r.get("status")=="no_balance":fb_send(uid,"❌ الرصيد غير كافي")
        elif r.get("status")=="unauthorized":user_steps[uid]={"step":"await_phone","last_activity":now};oo_clear(uid);fb_send(uid,"⚠️ انتهت")
        else:fb_send(uid,"❌ فشل")
        user_steps[uid]["step"]="oo_menu";return

    # ===== اختيار باقة إنترنت =====
    if step=="oo_inet_pick":
        keys=list(INTERNET_BUNDLES.keys())
        if not text.isdigit() or not(1<=int(text)<=len(keys)):fb_send(uid,"❌");return
        bi=INTERNET_BUNDLES[keys[int(text)-1]]
        user=oo_load(uid)
        if not user:user_steps[uid]={"step":"await_phone","last_activity":now};send_welcome(uid);return
        user=oo_ensure_valid(uid,user)
        if not user:user_steps[uid]={"step":"await_phone","last_activity":now};fb_send(uid,"⚠️ انتهت");return
        ms=user["msisdn"];at=user["access_token"]
        meta={k:user.get(k,"") for k in["tok_instance_id","tok_plat_sig","tok_fingerprint","tok_timestamp"]}
        fb_typing(uid);fb_send(uid,f"⏳ جاري تفعيل {bi['name']}...")
        r=oo_purchase_planned(ms,at,meta,bi["code"])
        if r["status"]=="ok":inc_stat("oo_bundles");fb_send(uid,f"✅ {bi['name']}!")
        elif r["status"]=="conflict":fb_send(uid,"❌ الرصيد غير كافي")
        elif r["status"]=="unauthorized":user_steps[uid]={"step":"await_phone","last_activity":now};oo_clear(uid);fb_send(uid,"⚠️ انتهت")
        else:fb_send(uid,"❌ فشل")
        user_steps[uid]["step"]="oo_menu";return

    # ===== اختيار عرض خاص =====
    if step=="oo_sp_pick":
        keys=list(SPECIAL_BUNDLES.keys())
        if not text.isdigit() or not(1<=int(text)<=len(keys)):fb_send(uid,"❌");return
        bi=SPECIAL_BUNDLES[keys[int(text)-1]]
        user=oo_load(uid)
        if not user:user_steps[uid]={"step":"await_phone","last_activity":now};send_welcome(uid);return
        user=oo_ensure_valid(uid,user)
        if not user:user_steps[uid]={"step":"await_phone","last_activity":now};fb_send(uid,"⚠️ انتهت");return
        ms=user["msisdn"];at=user["access_token"]
        meta={k:user.get(k,"") for k in["tok_instance_id","tok_plat_sig","tok_fingerprint","tok_timestamp"]}
        fb_typing(uid);fb_send(uid,f"⏳ جاري تفعيل {bi['name']}...")
        if bi.get("limited"):r=oo_purchase_byop(ms,at,meta,bi["validity"],bi["limited"],[])
        elif bi.get("app"):r=oo_purchase_byop(ms,at,meta,bi["validity"],None,[bi["app"]])
        else:r={"status":"error"}
        if r["status"]=="ok":inc_stat("oo_bundles");fb_send(uid,f"✅ {bi['name']}!")
        elif r["status"]=="conflict":fb_send(uid,"❌ الرصيد غير كافي")
        elif r["status"]=="unauthorized":user_steps[uid]={"step":"await_phone","last_activity":now};oo_clear(uid);fb_send(uid,"⚠️ انتهت")
        else:fb_send(uid,"❌ فشل")
        user_steps[uid]["step"]="oo_menu";return

    # ===== اختيار Free Fire =====
    if step=="oo_ff_pick":
        keys=list(FREEFIRE_BUNDLES.keys())
        if not text.isdigit() or not(1<=int(text)<=len(keys)):fb_send(uid,"❌");return
        bi=FREEFIRE_BUNDLES[keys[int(text)-1]]
        user=oo_load(uid)
        if not user:user_steps[uid]={"step":"await_phone","last_activity":now};send_welcome(uid);return
        user=oo_ensure_valid(uid,user)
        if not user:user_steps[uid]={"step":"await_phone","last_activity":now};fb_send(uid,"⚠️ انتهت");return
        ms=user["msisdn"];at=user["access_token"]
        meta={k:user.get(k,"") for k in["tok_instance_id","tok_plat_sig","tok_fingerprint","tok_timestamp"]}
        fb_typing(uid);fb_send(uid,f"⏳ جاري تفعيل {bi['name']}...")
        r=oo_purchase_planned(ms,at,meta,bi["code"])
        if r["status"]=="ok":inc_stat("oo_ff_bought");fb_send(uid,f"✅ {bi['name']}!")
        elif r["status"]=="conflict":fb_send(uid,"❌ الرصيد غير كافي")
        elif r["status"]=="unauthorized":user_steps[uid]={"step":"await_phone","last_activity":now};oo_clear(uid);fb_send(uid,"⚠️ انتهت")
        else:fb_send(uid,"❌ فشل")
        user_steps[uid]["step"]="oo_menu";return

    # ===== اختيار نادي Sport =====
    if step=="oo_soccer_pick":
        clubs=cur.get("clubs",[])
        if not text.isdigit() or not(1<=int(text)<=len(clubs)):fb_send(uid,"❌");return
        team=clubs[int(text)-1]["code"]
        user=oo_load(uid)
        if not user:user_steps[uid]={"step":"await_phone","last_activity":now};send_welcome(uid);return
        user=oo_ensure_valid(uid,user)
        if not user:user_steps[uid]={"step":"await_phone","last_activity":now};fb_send(uid,"⚠️ انتهت");return
        ms=user["msisdn"];at=user["access_token"]
        meta={k:user.get(k,"") for k in["tok_instance_id","tok_plat_sig","tok_fingerprint","tok_timestamp"]}
        fb_typing(uid)
        r=oo_soccer_activate(ms,at,meta,team)
        nm=SOCCER_CLUB_NAMES.get(team,team)
        if r["status"]=="ok":inc_stat("oo_soccer_enrolls");fb_send(uid,f"🎉 تم التسجيل!\n🏆 {nm} ({team})")
        elif r["status"]=="already":fb_send(uid,"✅ مشترك مسبقاً")
        elif r["status"]=="unauthorized":user_steps[uid]={"step":"await_phone","last_activity":now};oo_clear(uid);fb_send(uid,"⚠️ انتهت")
        else:fb_send(uid,f"❌ {r.get('msg') or r.get('code','?')}")
        user_steps[uid]["step"]="oo_menu";return

    # ===== افتراضي =====
    user_steps[uid]={"step":"await_phone","last_activity":now}
    send_welcome(uid)

def oo_format_gift_list_text(bundles,beneficiary=None):
    disp=""
    if beneficiary:
        disp="0"+beneficiary[3:] if beneficiary.startswith("213") else beneficiary
    lines=["🎁 قائمة العروض للإهداء","━━━━━━━━━━━━━━━━"]
    if disp:lines.append(f"📱 المستفيد: {disp}")
    lines.append(f"📦 عدد العروض: {len(bundles)}")
    lines.append("")
    for i,b in enumerate(bundles[:30],1):
        price=b.get("price","?")
        name=b.get("name") or b.get("code") or ""
        data_v=b.get("data","");extras=b.get("extras","")
        validity=b.get("validity","");family=b.get("family","")
        if "social" in family.lower():icon="📱"
        elif "smart" in family.lower():icon="✨"
        else:icon="🌐"
        lines.append(f"{i}. {icon} {name}")
        if data_v:lines.append(f"   🌐 {data_v}")
        if extras:lines.append(f"   ➕ {extras}")
        if validity:lines.append(f"   ⏱️ {validity}")
        lines.append(f"   💳 {price} دج")
        lines.append("")
    return "\n".join(lines)

def send_oo_menu(uid,user):
    ms=user["msisdn"];at=user["access_token"]
    qd=oo_quick_detect(at)
    services={"rate_plan":qd.get("rate_plan") or "","is_yooz":qd.get("is_yooz",False),"is_dima":qd.get("is_dima",False)}
    fb_send(uid,f"📱 {o_mask(ms)} ✅\n📦 {services['rate_plan'] or '...'}\n\n{OO_MENU(services,uid)}")

# ==================== Flask ====================
HTML="""<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="UTF-8">
<title>موح بوت</title></head><body style="font-family:Tahoma;background:#0f172a;color:#fff;text-align:center;padding:50px">
<h1 style="color:#0ea5e9">👽 موح بوت</h1><p>النظام يعمل ✅</p>
<p><strong>Younes Laldji</strong> — Oum el-Bouaghi</p></body></html>"""

@app.route('/',methods=['GET'])
def home():return HTML,200

@app.route('/webhook',methods=['GET','POST'])
def webhook():
    if request.method=='GET':
        if request.args.get("hub.verify_token")==VERIFY_TOKEN:
            return request.args.get("hub.challenge")
        return "Failed",403
    if request.method=='POST':
        try:
            d=request.json
            if not d or d.get('object')!='page':return "OK",200
            for e in d.get('entry',[]):
                for ev in e.get('messaging',[]):
                    m=ev.get('message',{})
                    if 'text' in m and not m.get('is_echo'):
                        sid=ev.get('sender',{}).get('id')
                        if sid:
                            user_steps.setdefault(sid,{"step":"await_phone","last_activity":time.time()})
                            user_steps[sid]["last_activity"]=time.time()
                            threading.Thread(target=handle_message,args=(sid,m['text']),daemon=True).start()
        except Exception as ex:print(f"❌ Webhook: {ex}",flush=True)
        return "EVENT_RECEIVED",200

if __name__=='__main__':
    print(f"🚀 موح بوت شاعل على البورت {PORT}\n",flush=True)
    saved=load_steps_saved()
    user_steps.update(saved)
    print(f"📥 {len(saved)} حالة محفوظة",flush=True)
    threading.Thread(target=oo_auto_refresh,daemon=True).start()
    threading.Thread(target=dz_auto_refresh,daemon=True).start()
    threading.Thread(target=steps_saver_worker,daemon=True).start()
    threading.Thread(target=reset_steps_worker,daemon=True).start()
    threading.Thread(target=start_tunnel,daemon=True).start()
    serve(app,host='0.0.0.0',port=PORT,threads=2,clear_untrusted_proxy_headers=True)