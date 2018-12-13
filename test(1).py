# import js2py
import execjs
import requests, zlib, base64, json
from datetime import datetime


def c(e, t):
    n = len(e)
    r = n >> 2
    if t:
        r = r + 2
    i = [0 * i for i in range(r)]
    for o in range(n):
        i[o >> 2] |= ord(e[o]) << ((o & 3) << 3)
    if t:
        i[-1] = n
    return i


def base_(a):
    return base64.b64encode(a.encode()).decode().replace('=', ")")


ctx = execjs.compile("""
 function f(e, t) {
            return b(r(e, t))
        }
   function r(e, t) {
   return  a(v(c(e, true), s(c(t, false))))
           
        }
       function s(e) {
            return e["length"] < 4 && (e["length"] = 4),
            e
        }
 function c(e, t) {
            var n = e["length"]
              , r = n >> 2;
            (n & 3) !== 0 && ++r;
            var i;
            t ? (i = new Array(r + 1),
            i[r] = n) : i = new Array(r);
            for (var o = 0; o < n; ++o)
                i[o >> 2] |= e["charCodeAt"](o) << ((o & 3) << 3);
            return i
        }
        
        
function v(e, t) {
            var n, r, i, o, a, c, s = e["length"], u = s - 1;
            for (r = e[u],
            i = 0,
            c = Math.floor(6 + 52 / s) | 0; c > 0; --c) {
                for (i = i + 2654435769 & 4294967295,
                o = i >>> 2 & 3,
                a = 0; a < u; ++a)
                    n = e[a + 1],
                    r = e[a] = e[a] + ((r >>> 5 ^ n << 2) + (n >>> 3 ^ r << 4) ^ (i ^ n) + (t[a & 3 ^ o] ^ r)) & 4294967295;
                n = e[0],
                r = e[u] = e[u] + ((r >>>5 ^ n << 2) + (n >>> 3 ^ r << 4) ^ (i ^ n) + (t[u & 3 ^ o] ^ r)) & 4294967295
            }
            return e
}

function a(e, t) {
            var n = e["length"]
              , r = n << 2;
            if (t) {
                var i = e[n - 1];
                if (r -= 4,
                i < r - 3 || i > r)
                    return Sr;
                r = i
            }
            for (var o = 0; o < n; o++)
                e[o] = String["fromCharCode"](e[o] & 255, e[o] >>> 8 & 255, e[o] >>> 16 & 255, e[o] >>> 24 & 255);
            var a = e["join"]("");
            return t ? a["substring"](0, r) : a
        }
var b = function() {
            var e = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "+", "/"];
            return function(t) {
                var n, r, i, o, a, c, s;
                for (r = i = 0,
                o = t["length"],
                a = o % 3,
                o -= a,
                c = o / 3 << 2,
                a > 0&& (c += 4),
                n = new Array(c); r < o; )
                    s = t["charCodeAt"](r++) << 16 | t["charCodeAt"](r++) << 8 | t["charCodeAt"](r++),
                    n[i++] = e[s >> 18] + e[s >> 12 & 63] + e[s >> 6 & 63] + e[s & 63];
                return a == 1 ? (s = t["charCodeAt"](r++),
                n[i++] = e[s >> 2] + e[(s & 3) << 4] + "==") : a == 2 && (s = t["charCodeAt"](r++) << 8 | t["charCodeAt"](r++),
                n[i++] = e[s >> 10] + e[s >> 4 & 63] + e[(s & 15) << 2] + "="),
                n["join"]("")
            }
        }()
 function o(e) {
            for (var t = "/", n = "+", r = e["split"](""), i = [], o = 0; o < r["length"]; o++) {
                var a = r[o];
                a === "/" && (a = "("),
                a === n && (a = ")"),
                i["push"](a)
            }
            return i["reverse"]()["join"]("")
        }
 
 
""")


class Crawl(object):
    def __init__(self, request_code):
        self.request_code = request_code
        self.headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',

            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Content-Length': '1695',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'verify.meituan.com',
            'Origin': 'https://verify.meituan.com',
            'Referer': 'https://verify.meituan.com/v2/web/general_page?action=spiderindefence&requestCode=85ab155a39ac4e568074c296814ea072&platform=1000&adaptor=auto&succCallbackUrl=https%3A%2F%2Foptimus-mtsi.meituan.com%2Foptimus%2FverifyResult%3ForiginUrl%3Dhttp%253A%252F%252Fwww.dianping.com%252Fshanghai%252Fch10%252Fg110&theme=dianping',
            # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36',
        }
        self.ts = self.getTime()
        self.cts = self.getTime() + 1000

    def getTime(self):
        d1 = datetime(1970, 1, 1)
        d2 = datetime.now()
        d3 = int((d2 - d1).total_seconds() * 1000)
        return d3

    def url_encode(self, data):
        """token解码"""
        if isinstance(data, str):
            data = data.replace(" ", "").encode()
            base_data = zlib.compress(data)
            data = base64.b64encode(base_data)
            return data
        else:
            data = str(data)
            return self.url_encode(data)

    def url_decode(self, data):
        """token编码"""
        if isinstance(data, str):
            data = base64.b64decode(data)
            base_data = zlib.decompress(data)
            return base_data

    def get_token(self):
        "behavior==UjvbtCfaPfxTG0AUf4xOHaunceq3un8B)4KOI4ySv1rvaVehtk9PA8dV3fJf0UP2nYAMyUXvAQ64fT6stIYSG4Dq5y2I4cl7nH6ukeVVRCHbPZwR12wgveaLuL8Zw7mMMs4DsH7nLz8lcZgucrINkDOLwS8pSh002P0vNf51V99dnMxQP0XrF3HHj7fzWvuXn2FkCanKbpHJFvDXWh2YAqVysSVZyhK5ojXBETYY9J2unkpgTuwsx3B3vWBFRZ2ZHA2TcyK8fwiAaxFUCP3GveG6F070z4UdKOXFfzbbBVdurkfys(cdcUnlwLwHmBtrT(nJ6FEJFo0Y(A4BB1iB5)xxdT4&fingerprint=undefined&id=71&request_code=586fce5b3afa4bab8990006f78deceba"
        'behavior==UjvbtCfaPfxTG0AUf4xOHaunceq3un8B)4KOI4ySv1rvaVehtk9PA8dV3fJf0UP2nYAMyUXvAQ64fT6stIYSG4Dq5y2I4cl7nH6ukeVVRCHbPZwR12wgveaLuL8Zw7mMMs4DsH7nLz8lcZgucrINkDOLwS8pSh002P0vNf51V99dnMxQP0XrF3HHj7fzWvuXn2FkCanKbpHJFvDXWh2YAqVysSVZyhK5ojXBETYY9J2unkpgTuwsx3B3vWBFRZ2ZHA2TcyK8fwiAaxFUCP3GveG6F070z4UdKOXFfzbbBVdurkfys(cdcUnlwLwHmBtrT(nJ6FEJFo0Y(A4BB1iB5)xxdT4'
        be_ = 'behavior={}{}'.format(self.behavior(),
                                     '&fingerprint=undefined&id=71&request_code={}'.format(self.request_code))

        sign = self.url_encode(json.dumps(be_)).decode()

        token = {"ver": "1.0.6", "rId": "100019", "ts": 1544597145552, "cts": 1544597149131, "brVD": [533, 938],
                 "brR": [[1920, 1080], [1920, 1040], 24, 24], "bI": [
                "https://verify.meituan.com/v2/web/general_page?action=spiderindefence&requestCode=586fce5b3afa4bab8990006f78deceba&platform=1000&adaptor=auto&succCallbackUrl=https%3A%2F%2Foptimus-mtsi.meituan.com%2Foptimus%2FverifyResult%3ForiginUrl%3Dhttp%253A%252F%252Fwww.dianping.com%252Fshop%252F69089926&theme=dianping",
                ""],
                 "mT": ["614,255,1565", "526,258,1548", "464,258,1530", "429,258,1514", "411,258,1496", "408,258,1488",
                        "407,258,1196", "409,256,1180", "410,255,1143", "411,254,1064", "412,254,1047", "414,253,1031",
                        "420,251,1013", "428,248,998", "435,247,982", "441,245,963", "444,245,948", "446,245,930",
                        "449,245,896", "449,246,814", "448,245,797", "447,244,781", "444,237,763", "444,218,748",
                        "444,186,730", "445,139,714", "449,107,697", "449,96,681", "450,93,664", "447,93,646",
                        "442,93,631", "439,94,613", "435,95,597", "433,99,547", "434,105,531", "438,106,514",
                        "452,105,499", "478,92,480", "512,45,464", "525,18,456"], "kT": [], "aT": [], "tT": [],
                 "aM": "", "inputs": [], "buttons": [],
                 "broP": ["Chrome PDF Plugin", "Chrome PDF Viewer", "Native Client"],
                 "sign": "behavior==UjvbtCfaPfxTG0AUf4xOHaunceq3un8B)4KOI4ySv1rvaVehtk9PA8dV3fJf0UP2nYAMyUXvAQ64fT6stIYSG4Dq5y2I4cl7nH6ukeVVRCHbPZwR12wgveaLuL8Zw7mMMs4DsH7nLz8lcZgucrINkDOLwS8pSh002P0vNf51V99dnMxQP0XrF3HHj7fzWvuXn2FkCanKbpHJFvDXWh2YAqVysSVZyhK5ojXBETYY9J2unkpgTuwsx3B3vWBFRZ2ZHA2TcyK8fwiAaxFUCP3GveG6F070z4UdKOXFfzbbBVdurkfys(cdcUnlwLwHmBtrT(nJ6FEJFo0Y(A4BB1iB5)xxdT4&fingerprint=undefined&id=71&request_code=586fce5b3afa4bab8990006f78deceba"
                 }
        token = {"ver": "1.0.6", "rId": "100019", "ts": 1544597858984, "cts": 1544597977143, "brVD": [533, 938],
                 "brR": [[1920, 1080], [1920, 1040], 24, 24], "bI": [
                "https://verify.meituan.com/v2/web/general_page?action=spiderindefence&requestCode=586fce5b3afa4bab8990006f78deceba&platform=1000&adaptor=auto&succCallbackUrl=https%3A%2F%2Foptimus-mtsi.meituan.com%2Foptimus%2FverifyResult%3ForiginUrl%3Dhttp%253A%252F%252Fwww.dianping.com%252Fshop%252F69089926&theme=dianping",
                ""],
                 "mT": ["663,257,1587", "603,257,1571", "532,257,1554", "474,260,1537", "439,260,1521", "415,260,1504",
                        "410,260,1495", "408,260,1423", "408,261,1391", "408,262,1312", "408,263,1255", "407,263,1208",
                        "406,263,1155", "404,264,1138", "399,266,1121", "394,267,1104", "390,267,1088", "389,267,911",
                        "390,267,895", "439,250,787", "447,250,771", "451,250,759", "453,250,743", "455,250,727",
                        "457,250,655", "458,250,639", "460,250,623", "462,247,605", "469,230,588", "478,183,572",
                        "486,128,554", "496,60,539"], "kT": [], "aT": [], "tT": [], "aM": "", "inputs": [],
                 "buttons": [], "broP": ["Chrome PDF Plugin", "Chrome PDF Viewer", "Native Client"],
                 "sign": sign,
                 }
        return token

    def behavior(self):
        t = base_(self.request_code)
        e = '{"env":{"zone":[230,33],"client":[391,243.5],"Timestamp":[1544597858997,1544597860376],"count":1,"timeout":0},"trajectory":[{"point":[[0,408,261,1379],[0,415,260,1491],[0,439,260,1509],[0,474,260,1524],[0,532,257,1541],[0,603,257,1558],[0,663,257,1574]]}]}'
        # e='{"env":{"zone":[230,33],"client":[391,243.5],"Timestamp":[1544598948203,1544598971763],"count":1,"timeout":0},"trajectory":[{"point":[[0,422,252,23560],[0,435,254,23724],[0,447,256,23734],[0,482,257,23751],[0,537,257,23770],[0,607,257,23785],[0,694,257,23802]]}]'
        # e='{"env":{"zone":[230,33],"client":[391,243.5],"Timestamp":[1544599047682,1544599073170],"count":1,"timeout":0},"trajectory":[{"point":[[0,413,265,25488],[0,426,270,25598],[0,459,270,25616],[0,511,270,25633],[0,569,273,25649],[0,610,273,25665]]}]}'
        s = ctx.call('f', e, t)
        behavior = ctx.call('o', s)
        print(behavior)
        return behavior

    def splider_(self):
        data_token = self.get_token()
        token = self.url_encode(json.dumps(data_token)).decode()
        url = 'https://verify.meituan.com/v2/ext_api/spiderindefence/verify?id=71'
        data = {
            'request_code': self.request_code,
            'behavior': self.behavior(),
            'fingerprint': 'undefined',
            '_token': token}
        print(data)
        r = requests.post(url, headers=self.headers, data=data)
        print(r.json())


if __name__ == '__main__':
    requests_code = '42728c8f15b840798a996fb567cb8ca2'
    splider = Crawl(requests_code)
    # splider.Get_sign(splider.behavior(),requests_code)
    splider.get_token()
    splider.splider_()
    # splider.Get_sign(splider.behavior(),requests_code)
