# -*- coding: utf-8 -*-
import base64
import json
import random
import re
import time
import zlib
from urllib import parse
from Crypto.Cipher import AES
from scrapy.selector import Selector


class MeituanEncryptor(object):

    def __init__(self, data, ts):
        self.ts = ts
        time.sleep(0.01)
        self.data = data
        self.url = "http://m.waimai.meituan.com/waimai/mindex/home?"
        self.ver_url = "https://verify.meituan.com/v2/app/general_page?"
        brVD_list = [
            [320, 568], [414, 736], [375, 667],
            [768, 1024], [412, 732],
            [375, 812], [1024, 1366]
        ]
        self.brVD = random.choice(brVD_list)
        self.brR = [self.brVD, self.brVD, 24, 24]

    def compress_data(self, data):
        """压缩token和sign参数的方法
        转为JSON字符串，使用zlib压缩，再使用base64编码
        """
        json_data = json.dumps(data, separators=(',', ':')).encode("utf-8")
        compressed_data = zlib.compress(json_data)
        base64_str = base64.b64encode(compressed_data).decode()
        return base64_str

    # 外卖店铺相关sign
    def get_sign(self):
        """构造sign（请求的URL中一个参数）
        由各种乱七八糟的信息组成的字典，进行URL编码，URL参数拼接，然后压缩
        """
        self.data["channel"] = '6'
        self.data["needRegions"] = '7'
        clean_data = {
            key: value
            for key, value in self.data.items()
            if key not in ["mtWmPoiId", "dpShopId", "source", "fontName", "_"]
        }
        sign_data = []
        for key in sorted(clean_data.keys()):
            sign_data.append(key + "=" + str(clean_data[key]))
        sign_data = "&".join(sign_data)
        compressed_data = self.compress_data(sign_data)
        self.sign = compressed_data
        return compressed_data

    # 店铺相关token
    def get_token(self, rid=100009):
        """构造_token（请求的URL中一个参数）
        由各种乱七八糟的信息（包括sign)组成的字典，转为JSON字符串后压缩
        """
        token_data = {
            "rId": rid,
            "ver": "1.0.6",
            "ts": self.ts,
            "cts": round(time.time() * 1000),
            "brVD": self.brVD,
            "brR": self.brR,
            "bI": [self.url, ""],
            "mT": ["137,191", "133,30", "155,62", "191,29", "50,31", "78,31"],
            "kT": ["\xc3\xa5,INPUT", "\xc3\xa5,INPUT", "\xc3\xa5,INPUT", "\xc3\xa5,INPUT", "\xc3\xa5,INPUT",
                   "\xc3\xa5,INPUT", "\xc3\xa5,INPUT", "\xc3\xa5,INPUT", "\xc3\xa5,INPUT", "\xc3\xa5,INPUT",
                   "\xc3\xa5,INPUT", "\xc3\xa5,INPUT", "\xc3\xa5,INPUT", "\xc3\xa5,INPUT", "\xc3\xa5,INPUT",
                   "\xc3\xa5,INPUT", "\xc3\xa5,INPUT", "\xc3\xa5,INPUT", "\xc3\xa5,INPUT", "\xc3\xa5,INPUT",
                   "\xc3\xa5,INPUT", "\\b,INPUT", "\\b,INPUT", "\\b,INPUT", "\xc3\xa5,INPUT", "\xc3\xa5,INPUT",
                   "\xc3\xa5,INPUT", "\xc3\xa5,INPUT", "\xc3\xa5,INPUT", "\xc3\xa5,INPUT"],
            "aT": ["137,191,LI", "133,30,INPUT", "155,62,LI", "191,29,INPUT", "50,31,DIV", "78,31,DIV"],
            "tT": [],
            "aM": "",
            "sign": self.get_sign()
        }
        compressed_data = self.compress_data(token_data)
        self.token = compressed_data
        return compressed_data

    # 滑块验证的sign
    def get_verify_sign(self):
        self.data["id"] = '71'
        clean_data = {
            key: value
            for key, value in self.data.items()
            if key not in ["mtWmPoiId", "dpShopId", "source", "fontName", "_"]
        }
        sign_data = []
        for key in sorted(clean_data.keys()):
            sign_data.append(key + "=" + str(clean_data[key]))
        sign_data = "&".join(sign_data)
        compressed_data = self.compress_data(sign_data)
        self.sign = compressed_data
        return compressed_data

    # 滑块验证的token
    def get_verify_token(self, local_url, request_code, local_ip, rid=100009):
        ver_url = "https://verify.meituan.com/v2/app/general_page?action=spiderindefence&requestCode={}&succCallbackUrl=https://m.waimai.meituan.com/waimai/mindex/yodaverify?redirecturl={}&flag=200&mtsiRemoteIp={}&mtsiDropStrategy=factor_dp_takeaway_iuuid_hcv_black".format(
            request_code, local_url, local_ip)
        ver_url_en = parse.quote(ver_url, encoding='utf-8')
        token_data = {
            "rId": rid,
            "ver": "1.0.6",
            "ts": self.ts,
            "cts": round(time.time() * 1000),
            "brVD": self.brVD,
            "brR": self.brR,
            "bI": [ver_url_en, local_url],
            "mT": [],
            "kT": [],
            "aT": ["137,191,LI", "133,30,INPUT", "155,62,LI", "191,29,INPUT", "50,31,DIV", "78,31,DIV"],
            "tT": ["400.2531433105469,360,1,2095",
                   "389.1139221191406,358.9873352050781,1,2078",
                   "374.93670654296875,357.9747009277344,1,2061",
                   "363.7974548339844,357.9747009277344,1,2045",
                   "352.6582336425781,358.9873352050781,1,2028",
                   "338.48101806640625,362.02532958984375,1,2011",
                   "323.2911376953125,365.06329345703125,1,1995",
                   "311.1392517089844,364.0506286621094,1,1978",
                   "290.8861083984375,362.02532958984375,1,1961",
                   "266.582275390625,358.9873352050781,1,1944",
                   "236.2025146484375,356.9620056152344,1,1929",
                   "200.75949096679688,358.9873352050781,1,1911",
                   "167.34178161621094,366.075927734375,1,1894",
                   "133.92405700683594,373.1645812988281,1,1878",
                   "103.54430389404297,380.2531433105469,1,1861",
                   "80.25316619873047,383.2911682128906,1,1844"],
            "aM": "",
            "inputs": [],
            "buttons": [],
            "broP": {},
            "sign": self.get_verify_sign()
        }
        compressed_data = self.compress_data(token_data)
        self.token = compressed_data
        return compressed_data

    def get_xforwith(self, html_text=None):
        """构造X-FOR-WITH（headers中的一项）
        将时间、屏幕像素等多种信息组成的字典（见以下data变量）转为JSON字符串
        然后使用AES加密，AES加密模式为CBC
        加密的密钥和IV一样，构造方式为：
        一开始进入的网页里有个meta元素（一般为页面最后一个meta元素了），id为六位随机字母组成
        取其content（很长），然后从第0个字符开始，每10个取一个字符，最多取16个字符）
        """
        if html_text is not None:
            sel = Selector(text=html_text)
            meta_content = sel.xpath("//meta")[-1].xpath("./@content").extract_first()
            aes_key = "".join([meta_content[i * 10] for i in range(16)])
            aes_key = aes_key.encode()
            self.aes_key = aes_key
        aes_key = self.aes_key
        aes_iv = aes_key
        aes_mode = AES.MODE_CBC
        aes_cryptor = AES.new(aes_key, aes_mode, aes_iv)
        data = {
            "ts": self.ts,
            "cts": round(time.time() * 1000),
            "brVD": [411, 823],
            "brR": [[411, 823], [411, 823], 24, 24],
            # "brVD": self.brVD,
            # "brR": self.brR,
            "aM": ""
        }
        json_data = json.dumps(data, separators=(",", ":")).encode()
        json_data = json_data + b"\r" * (16 - len(json_data) % 16)
        # print(json_data)
        x_for_with = base64.b64encode(aes_cryptor.encrypt(json_data))
        return x_for_with

    def get_mta(self, cookies, ua):
        """构造__mta（cookies中的一项）
        第一部分：把各种信息的字符串拼起来，然后进行一些神奇的hash处理
        第二部分-第四部分：由三个时间戳组成，具体哪个代表什么不大清楚，但可以都一样
        第五部分：从1开始，会随着时间增长一直加，不过就按1来吧
        以上五部分使用"."来拼接
        """
        hash_data = "Netscape" + "undefined" + "zh-cn" + "iPhone"
        hash_data += ua
        hash_data += ("0" + "x".join([str(x) for x in self.brVD]))
        cookies = "; ".join(["%s=%s" % item for item in cookies.items()])
        hash_data += cookies
        hash_data += self.url
        i = 3
        j = len(hash_data)
        while i > 0:
            hash_data += str(i ^ j)
            i -= 1
            j += 1
        n = 0
        i = 0
        e = len(hash_data) - 1
        while e >= 0:
            i = ord(hash_data[e])
            n = (n << 6 & 268435455) + i + (i << 14)
            i = 266338304 & n
            if i != 0:
                n = n ^ i >> 21
            e -= 1

        time1 = str(round(time.time() * 1000))
        time2 = time1
        time3 = time2
        mta = ".".join([str(n), time1, time2, time3, "1"])
        return mta

    def get_lxsdk(self, ua):
        """构造_lxsdk_cuid和_lxsdk（两者一样，都是cookie中的一项）
        由五部分组成，各部分之间用"-"连接
        第一部分：时间戳转16进制，字符串再接上200转16进制的字符串
        第二部分：0-1之间的随机数，转16进制小数，去掉小数点
        第三部分：User-Agent字符串每四位分段，然后进行一些神奇的处理
        第四部分：屏幕总像素数量转16进制
        第五部分：时间戳转16进制，字符串再接上200转16进制的字符串
        """

        def get_part2():
            rnd_num = random.random()
            num = rnd_num
            result = "0"
            while num >= 1e-10:
                num = num * 16
                int_part = int(num)
                result += hex(int_part)[2:]
                num = num - int_part
            return result

        def get_part3(ua):
            result = 0
            split4_list = re.sub("(.{4})", "\\1\0", ua).rstrip("\0").split("\0")
            for part in split4_list:
                part_ascii = [ord(c) for c in part[::-1]]
                part_result = 0
                for i in range(len(part_ascii)):
                    part_result |= part_ascii[i] << 8 * i
                result = result ^ part_result
            return hex(result)[2:]

        screen = self.brVD
        part1 = hex(round(time.time() * 1000))[2:] + hex(200)[2:]
        part2 = get_part2()
        part3 = get_part3(ua)
        part4 = hex(screen[0] * screen[1])[2:]
        part5 = hex(round(time.time() * 1000))[2:] + hex(200)[2:]
        return "-".join([part1, part2, part3, part4, part5])

    def get_lxsdk_s(self):
        """构造_lxsdk_s（cookies中的一项）
        第一部分是时间戳转16进制字符串
        第二部分-第四部分都是由三个字符组成，每个字符是1-65537之间的随机数
        转16进制后取第一位（相当于随机16进制字符吧）
        这四部分用"-"连接，之后又加上"//NaN"（反正每次都是以这个结尾，要URL编码）
        """
        part_list = []
        part_list.append(hex(round(time.time() * 1000))[2:])
        for i in range(3):
            rnd_hexchr_list = []
            for j in range(3):
                rnd_hexchr = hex(round(1 + 65536 * random.random()))[2]
                rnd_hexchr_list.append(rnd_hexchr)
            part_list.append("".join(rnd_hexchr_list))
        return "-".join(part_list) + "%7C%7C22"
        # return "-".join(part_list) + "%7C%7CNaN"


if __name__ == '__main__':
    # from urllib import parse
    #
    # ver_url = "https://verify.meituan.com/v2/app/general_page?action=spiderindefence&requestCode={}&succCallbackUrl=https://m.waimai.meituan.com/waimai/mindex/yodaverify?redirecturl={}&flag=200&mtsiRemoteIp={}&mtsiDropStrategy=factor_dp_takeaway_iuuid_hcv_black"
    # ver_url_en = parse.quote(ver_url, encoding='utf-8')
    # print(ver_url_en)
    pass