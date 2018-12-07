# -*- coding: utf-8 -*-
import base64
import json
import time
import zlib
import execjs


class MeituanEncryptor(object):
    def compress_data(self, data):
        """压缩token和sign参数的方法
        转为JSON字符串，使用zlib压缩，再使用base64编码
        """
        json_data = json.dumps(data, separators=(',', ':')).encode("utf-8")
        compressed_data1 = zlib.compress(json_data)
        base64_str = base64.b64encode(compressed_data1).decode()
        return base64_str

    def compress_data1(self, data):
        """压缩token和sign参数的方法
        转为JSON字符串，使用zlib压缩，再使用base64编码
        """
        print(data.encode())
        compressed_data2 = zlib.compress(data.encode())
        base64_str = base64.b64encode(compressed_data2).decode()
        return base64_str

    # 相关sign
    def get_sign(self):
        """构造sign（请求的URL中一个参数）
        由各种乱七八糟的信息组成的字典，进行URL编码，URL参数拼接，然后压缩
        """
        # 双层引号不能换行,表单数据
        sign_data = '"endDate=2018-12-07&getNewVo=1&lastLabel=&nextLabel=&requestWmPoiId=-1&signToken=Nw;1;qim1`[vGrD-36L:E4t:p27G[Qg`7h@{cadLIpNV{XUsEZDcEnIVLc2[vjH@){`2nCXdkK`:K2z4RP0Mhwz3ga2x-zChCs1QK6OpcMgIAdhhx@X@5Q7h)cVGPtfS3nP@npR`t{w4S[LaUOR;ZC&sortField=1&startDate=2018-12-07&wmOrderPayType=2&wmOrderStatus=-2"'
        sign_data1 = self.compress_data1(sign_data)
        return sign_data1

    # 相关token
    def get_token(self):
        """构造_token（请求的URL中一个参数）
        由各种乱七八糟的信息（包括sign)组成的字典，转为JSON字符串后压缩
        """
        url = "http://e.waimai.meituan.com/v2/order/history?ignoreSetRouterProxy=true"
        ver_url = "http://e.waimai.meituan.com/?time=1544076028099"
        ts = int(time.time() * 1000)
        time.sleep(0.01)
        token_data = {
            "rId": 100007,
            "ts": ts,
            "cts": int(time.time() * 1000),
            "brVD": [1920, 1080],
            "brR": [[1920, 1080], [1920, 1040], 24, 24],
            "bI": [url, ver_url],
            "mT": [],
            "kT": [],
            "aT": [],
            "tT": [],
            "sign": self.get_sign()
        }
        token_data1 = self.compress_data(token_data)
        # url编码这里用python的编码有问题所以调用js
        token_data1 = self.get_urlencode(token_data1)
        return token_data1

    def get_js(self):
        f = open("behavor_js.js", 'r', encoding='utf-8')  # 打开JS文件
        line = f.readline()
        htmlstr = ''
        while line:
            htmlstr = htmlstr + line
            line = f.readline()
        return htmlstr

    # 调取js
    def get_urlencode(self, data2):
        jsstr = self.get_js()
        ctx = execjs.compile(jsstr)  # 加载JS文件
        return ctx.call('f3', data2)  # 调用js方法  第一个参数是JS的方法名，后面的data是js方法的参数


if __name__ == '__main__':
    pass
