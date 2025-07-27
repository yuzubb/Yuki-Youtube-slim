import json
import requests
import urllib.parse
import time
import datetime
import random
from cache import cache
from typing import Union
from fastapi import FastAPI, Request, Response, Cookie
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

# Youtube-python ライブラリをインポート
from Youtube import Search

# FastAPI アプリケーションと Jinja2Templates の初期化
# このコードが動作するためには、'templates' という名前のディレクトリが必要です
app = FastAPI()
templates = Jinja2Templates(directory="templates")

# グローバル変数 logs を定義
logs = []

max_api_wait_time = 3
max_time = 10
apis = [r"https://nyc1.iv.ggtyler.dev",r"https://cal1.iv.ggtyler.dev",r"https://invidious.nikkosphere.com",r"https://lekker.gay",r"https://invidious.f5.si",r"https://invidious.lunivers.trade",r"https://invid-api.poketube.fun",r"https://pol1.iv.ggtyler.dev",r"https://eu-proxy.poketube.fun",r"https://iv.melmac.space",r"https://invidious.reallyaweso.me",r"https://invidious.dhusch.de",r"https://usa-proxy2.poketube.fun",r"https://id.420129.xyz",r"https://invidious.darkness.service",r"https://iv.datura.network",r"https://invidious.jing.rocks",r"https://invidious.private.coffee",r"https://youtube.mosesmang.com",r"https://iv.duti.dev",r"https://invidious.projectsegfau.lt",r"https://invidious.perennialte.ch",r"https://invidious.einfachzocken.eu",r"https://invidious.adminforge.de",r"https://inv.nadeko.net",r"https://invidious.esmailelbob.xyz",r"https://invidious.0011.lt",r"https://invidious.ducks.party"]
url = requests.get(r'https://raw.githubusercontent.com/mochidukiyukimi/yuki-youtube-instance/main/instance.txt').text.rstrip()

apichannels = []
apicomments = []
[[apichannels.append(i),apicomments.append(i)] for i in apis]
class APItimeoutError(Exception):
    pass


def apirequest(url):
    global apis
    global max_time
    starttime = time.time()
    for api in apis:
        if  time.time() - starttime >= max_time -1:
            break
        try:
            res = requests.get(api+url,timeout=max_api_wait_time)
            if res.status_code == 200:
                return res.text
            else:
                print(f"エラー:{api}")
                apis.append(api)
                apis.remove(api)
        except:
            print(f"タイムアウト:{api}")
            apis.append(api)
            apis.remove(api)
    raise APItimeoutError("APIがタイムアウトしました")

def apichannelrequest(url):
    global apichannels
    global max_time
    starttime = time.time()
    for api in apichannels:
        if  time.time() - starttime >= max_time -1:
            break
        try:
            res = requests.get(api+url,timeout=max_api_wait_time)
            if res.status_code == 200:
                return res.text
            else:
                print(f"エラー:{api}")
                apichannels.append(api)
                apichannels.remove(api)
        except:
            print(f"タイムアウト:{api}")
            apichannels.append(api)
            apichannels.remove(api)
    raise APItimeoutError("APIがタイムアウトしました")

def apicommentsrequest(url):
    global apicomments
    global max_time
    starttime = time.time()
    for api in apicomments:
        if  time.time() - starttime >= max_time -1:
            break
        try:
            res = requests.get(api+url,timeout=max_api_wait_time)
            if res.status_code == 200:
                return res.text
            else:
                print(f"エラー:{api}")
                apicomments.append(api)
                apicomments.remove(api)
        except:
            print(f"タイムアウト:{api}")
            apicomments.append(api)
            apicomments.remove(api)
    raise APItimeoutError("APIがタイムアウトしました")

            

def get_data(videoid):
    global logs
    t = json.loads(apirequest(r"api/v1/videos/"+ urllib.parse.quote(videoid)))
    return [{"id":i["videoId"],"title":i["title"],"authorId":i["authorId"],"author":i["author"]} for i in t["recommendedVideos"]],list(reversed([i["url"] for i in t["formatStreams"]]))[:2],t["descriptionHtml"].replace("\n","<br>"),t["title"],t["authorId"],t["author"],t["authorThumbnails"][-1]["url"]

def get_search(q, page):
    """
    Youtube-python を使用して検索を実行し、結果を整形します。
    元のコードの apirequest に代わるものです。
    """
    global logs

    # 1ページあたりの項目数を20と仮定し、ページネーションのためのオフセットとリミットを計算
    items_per_page = 20
    offset = (page - 1) * items_per_page

    # Youtube-python を使用して検索を実行し、結果の辞書リストを取得します
    search_results_raw = Search(q, offset=offset, limit=items_per_page).result()

    def load_search(i):
        # 期間文字列（例: "3:45", "1:05:30"）を秒数に変換するヘルパー関数
        def duration_str_to_seconds(duration_str: str) -> int:
            if not duration_str:
                return 0
            parts = list(map(int, duration_str.split(':')))
            if len(parts) == 3: # 時:分:秒 形式
                return parts[0] * 3600 + parts[1] * 60 + parts[2]
            elif len(parts) == 2: # 分:秒 形式
                return parts[0] * 60 + parts[1]
            return 0

        if i["type"] == "video":
            # 動画の詳細を抽出し、元のコードのフォーマットに合わせます
            total_seconds = duration_str_to_seconds(i.get("duration", "0:00"))
            formatted_length = str(datetime.timedelta(seconds=total_seconds))
            thumbnail_url = i["thumbnails"][-1]["url"] if i.get("thumbnails") else None

            return {
                "title": i["title"],
                "id": i["id"],
                "authorId": i["channel"]["id"] if "channel" in i else "N/A",
                "author": i["channel"]["name"] if "channel" in i else "N/A",
                "length": formatted_length,
                "published": i.get("publishedTime", "N/A"),
                "type": "video",
                "thumbnail": thumbnail_url
            }
        elif i["type"] == "playlist":
            # プレイリストの詳細を抽出し、フォーマットに合わせます
            thumbnail_url = i["thumbnails"][-1]["url"] if i.get("thumbnails") else None
            video_count = int("".join(filter(str.isdigit, i.get("videoCount", "0"))))

            return {
                "title": i["title"],
                "id": i["id"],
                "thumbnail": thumbnail_url,
                "count": video_count,
                "type": "playlist"
            }
        else: # それ以外はチャンネルタイプと仮定
            # チャンネルの詳細を抽出し、フォーマットに合わせます
            thumbnail_url = i["thumbnails"][-1]["url"] if i.get("thumbnails") else None
            if thumbnail_url and not thumbnail_url.startswith("https"):
                thumbnail_url = r"https://" + thumbnail_url

            return {
                "author": i["name"],
                "id": i["id"],
                "thumbnail": thumbnail_url,
                "type": "channel"
            }
    
    return [load_search(i) for i in search_results_raw]
def get_channel(channelid):
    global apichannels
    t = json.loads(apichannelrequest(r"api/v1/channels/"+ urllib.parse.quote(channelid)))
    if t["latestVideos"] == []:
        print("APIがチャンネルを返しませんでした")
        apichannels.append(apichannels[0])
        apichannels.remove(apichannels[0])
        raise APItimeoutError("APIがチャンネルを返しませんでした")
    return [[{"title":i["title"],"id":i["videoId"],"authorId":t["authorId"],"author":t["author"],"published":i["publishedText"],"type":"video"} for i in t["latestVideos"]],{"channelname":t["author"],"channelicon":t["authorThumbnails"][-1]["url"],"channelprofile":t["descriptionHtml"]}]

def get_playlist(listid,page):
    t = json.loads(apirequest(r"/api/v1/playlists/"+ urllib.parse.quote(listid)+"?page="+urllib.parse.quote(page)))["videos"]
    return [{"title":i["title"],"id":i["videoId"],"authorId":i["authorId"],"author":i["author"],"type":"video"} for i in t]

def get_comments(videoid):
    t = json.loads(apicommentsrequest(r"api/v1/comments/"+ urllib.parse.quote(videoid)+"?hl=jp"))["comments"]
    return [{"author":i["author"],"authoricon":i["authorThumbnails"][-1]["url"],"authorid":i["authorId"],"body":i["contentHtml"].replace("\n","<br>")} for i in t]

def get_replies(videoid,key):
    t = json.loads(apicommentsrequest(fr"api/v1/comments/{videoid}?hmac_key={key}&hl=jp&format=html"))["contentHtml"]



def check_cokie(cookie):
    if cookie == "True":
        return True
    return False







from fastapi import FastAPI, Depends
from fastapi import Response,Cookie,Request
from fastapi.responses import HTMLResponse,PlainTextResponse
from fastapi.responses import RedirectResponse as redirect
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_csrf_protect import CsrfProtect
from pydantic import BaseModel
from typing import Union


app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
app.mount("/css", StaticFiles(directory="./css"), name="static")
app.mount("/blog", StaticFiles(directory="./blog", html=True), name="static")
app.add_middleware(GZipMiddleware, minimum_size=1000)

from fastapi.templating import Jinja2Templates
template = Jinja2Templates(directory='templates').TemplateResponse

class CsrfSettings(BaseModel):
    secret_key:str = "".join(random.choices("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890",k=50))

@CsrfProtect.load_config
def get_csrf_config():
    return CsrfSettings()




@app.get("/", response_class=HTMLResponse)
def home(response: Response,request: Request,yuki: Union[str] = Cookie(None)):
    if check_cokie(yuki):
        response.set_cookie("yuki","True",max_age=60 * 60 * 24 * 7)
        return template("home.html",{"request": request})
    return redirect("/blog")

@app.get('/watch', response_class=HTMLResponse)
def video(v:str,response: Response,request: Request,yuki: Union[str] = Cookie(None),proxy: Union[str] = Cookie(None)):
    if not(check_cokie(yuki)):
        return redirect("/")
    response.set_cookie(key="yuki", value="True",max_age=7*24*60*60)
    videoid = v
    t = get_data(videoid)
    response.set_cookie("yuki","True",max_age=60 * 60 * 24 * 7)
    return template('video.html', {"request": request,"videoid":videoid,"videourls":t[1],"res":t[0],"description":t[2],"videotitle":t[3],"authorid":t[4],"authoricon":t[6],"author":t[5],"proxy":proxy})

@app.get("/search", response_class=HTMLResponse,)
def search(q:str,response: Response,request: Request,page:Union[int,None]=1,yuki: Union[str] = Cookie(None),proxy: Union[str] = Cookie(None)):
    if not(check_cokie(yuki)):
        # FastAPI でのリダイレクトには RedirectResponse を使用します
        return RedirectResponse(url="/", status_code=302)
    
    response.set_cookie("yuki","True",max_age=60 * 60 * 24 * 7)
    
    return templates.TemplateResponse("search.html", {"request": request,"results":get_search(q,page),"word":q,"next":f"/search?q={q}&page={page + 1}","proxy":proxy})
@app.get("/hashtag/{tag}")
def search(tag:str,response: Response,request: Request,page:Union[int,None]=1,yuki: Union[str] = Cookie(None)):
    if not(check_cokie(yuki)):
        return redirect("/")
    return redirect(f"/search?q={tag}")


@app.get("/channel/{channelid}", response_class=HTMLResponse)
def channel(channelid:str,response: Response,request: Request,yuki: Union[str] = Cookie(None),proxy: Union[str] = Cookie(None)):
    if not(check_cokie(yuki)):
        return redirect("/")
    response.set_cookie("yuki","True",max_age=60 * 60 * 24 * 7)
    t = get_channel(channelid)
    return template("channel.html", {"request": request,"results":t[0],"channelname":t[1]["channelname"],"channelicon":t[1]["channelicon"],"channelprofile":t[1]["channelprofile"],"proxy":proxy})

@app.get("/answer", response_class=HTMLResponse)
def set_cokie(q:str):
    if q.count() > 10:
        return "ランダム"
    return "文章"

@app.get("/playlist", response_class=HTMLResponse)
def playlist(list:str,response: Response,request: Request,page:Union[int,None]=1,yuki: Union[str] = Cookie(None),proxy: Union[str] = Cookie(None)):
    if not(check_cokie(yuki)):
        return redirect("/")
    response.set_cookie("yuki","True",max_age=60 * 60 * 24 * 7)
    return template("search.html", {"request": request,"results":get_playlist(list,str(page)),"word":"","next":f"/playlist?list={list}","proxy":proxy})

@app.get("/info", response_class=HTMLResponse)
def viewlist(response: Response,request: Request,yuki: Union[str] = Cookie(None)):
    global apis,apichannels,apicomments
    if not(check_cokie(yuki)):
        return redirect("/")
    response.set_cookie("yuki","True",max_age=60 * 60 * 24 * 7)
    return template("info.html",{"request": request,"Youtube_API":apis[0],"Channel_API":apichannels[0],"Comments_API":apicomments[0]})

@app.get("/suggest")
def suggest(keyword:str):
    return [i[0] for i in json.loads(requests.get(r"http://www.google.com/complete/search?client=youtube&hl=ja&ds=yt&q="+urllib.parse.quote(keyword)).text[19:-1])[1]]

@app.get("/comments")
def comments(request: Request,v:str):
    return template("comments.html",{"request": request,"comments":get_comments(v)})

@app.get("comments/{videoid}",response_class=PlainTextResponse)
def replies(key):
    return get_replies(videoid,key)

@app.get("/thumbnail")
def thumbnail(v:str):
    return Response(content = requests.get(fr"https://img.youtube.com/vi/{v}/0.jpg").content,media_type=r"image/jpeg")

@app.get("/bbs",response_class=HTMLResponse)
def view_bbs(request: Request,name: Union[str, None] = "",seed:Union[str,None]="",verify:Union[str,None]="false",yuki: Union[str] = Cookie(None), csrf_protect:CsrfProtect = Depends()):
    if not(check_cokie(yuki)):
        return redirect("/")
    res = HTMLResponse(requests.get(fr"{url}bbs?name={urllib.parse.quote(name)}&seed={urllib.parse.quote(seed)}&verify={urllib.parse.quote(verify)}",cookies={"yuki":"True"}).text)
    csrf_protect.set_csrf_cookie(res)
    return res

@app.get("/bbs/api",response_class=HTMLResponse)
@cache(seconds=5)
def view_bbs(request: Request,t: str,verify: Union[str,None] = "false"):
    print(fr"{url}bbs/api?t={urllib.parse.quote(t)}&verify={urllib.parse.quote(verify)}")
    return requests.get(fr"{url}bbs/api?t={urllib.parse.quote(t)}&verify={urllib.parse.quote(verify)}",cookies={"yuki":"True"}).text

@app.get("/bbs/result")
def write_bbs(request: Request,name: str = "",message: str = "",seed:Union[str,None] = "",verify:Union[str,None]="false",yuki: Union[str] = Cookie(None), csrf_protect:CsrfProtect = Depends()):
    if not(check_cokie(yuki)):
        return redirect("/")
    try:
        csrf_protect.validate_csrf_in_cookies(request)
    except:
        return redirect("/bbs?name="+urllib.parse.quote(name)+"&seed="+urllib.parse.quote(seed))
    requests.get(fr"{url}bbs/result?name={urllib.parse.quote(name)}&message={urllib.parse.quote(message)}&seed={urllib.parse.quote(seed)}&verify={urllib.parse.quote(verify)}",cookies={"yuki":"True"})
    return redirect(f"/bbs?name={urllib.parse.quote(name)}&seed={urllib.parse.quote(seed)}&verify={urllib.parse.quote(verify)}")

@app.get("/bbs/commonds",response_class=HTMLResponse)
def view_commonds(request: Request,yuki: Union[str] = Cookie(None)):
    if not(check_cokie(yuki)):
        return redirect("/")
    return template("commonds.html",{"request":request})


@app.exception_handler(500)
def page(request: Request,__):
    return template("APIwait.html",{"request": request},status_code=500)

@app.exception_handler(APItimeoutError)
def APIwait(request: Request,exception: APItimeoutError):
    return template("APIwait.html",{"request": request},status_code=500)
