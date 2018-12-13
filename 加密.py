# -*- coding: utf-8 -*-
import base64
import json
import time
import zlib
import execjs


class MeituanEncryptor(object):
    def __init__(self, endDate, getNewVo, lastLabel, nextLabel, requestWmPoiId, signToken, sortField, startDate,
                 wmOrderPayType, wmOrderStatus):
        self.endDate = endDate
        self.getNewVo = getNewVo
        self.lastLabel = lastLabel
        self.nextLabel = nextLabel
        self.requestWmPoiId = requestWmPoiId
        self.signToken = signToken
        self.sortField = sortField
        self.startDate = startDate
        self.wmOrderPayType = wmOrderPayType
        self.wmOrderStatus = wmOrderStatus

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
        sign_data = '"endDate={}&getNewVo={}&lastLabel={}&nextLabel={}&requestWmPoiId={}&signToken={}&sortField={}&startDate={}&wmOrderPayType={}&wmOrderStatus={}"'.format(
            self.endDate,
            self.getNewVo,
            self.lastLabel,
            self.nextLabel,
            self.requestWmPoiId,
            self.signToken,
            self.sortField,
            self.startDate,
            self.wmOrderPayType,
            self.wmOrderStatus,
        )
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
            "ts": 1544427092919,
            "cts": 1544427092919,
            "brVD": [1920, 1080],
            "brR": [[1920, 1080], [1920, 1040], 24, 24],
            "bI": [url, ver_url],
            "mT": [],
            "kT": [],
            "aT": [],
            "tT": [],
            "sign": self.get_sign()
        }
        print(1111)
        print(token_data)
        print(2222)
        token_data1 = self.compress_data(token_data)
        # url编码这里用python的编码有问题所以调用js
        token_data1 = self.get_urlencode(token_data1)
        return token_data1

    @staticmethod
    def get_js():
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
    call1 = MeituanEncryptor(endDate="2018-12-10",
                            getNewVo="1",
                            lastLabel="",
                            nextLabel="",
                            requestWmPoiId="6149813",
                            signToken="z-dZEPTuGvdXx4@fj2{GCZe:QMHwFMk46z`gZw@lz;wjuHlFoXi-qAg1UEWIO0Cz)TnqLAISmz3-TZLaKR4;3va;zj-IQ5pAuTn0MPi{X[Ale3aWaNxuvvDCuP)jejDotgCkCR;IwnNN7SHr64s6je",
                            sortField="1",
                            startDate="2018-12-10",
                            wmOrderPayType="2",
                            wmOrderStatus="-2")
    print(call1.get_token())
