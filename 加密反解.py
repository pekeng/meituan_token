import zlib
import base64
from urllib import parse

_token = "eJxdj01vgjAAQP+LBxIPJLQ6WSAkLMgYAflUZuRCRztgQkFaBeHP68XLbi/vnd6CULxFnGhQAu8igKIkCwXhHhmSVgNCjRh30Q+pNYGS8YU9uVwJ499N0FY21kQgsKqg+/ZMqOYNKlAvVQOy9Gb1W3G1cRVzzZUOylYaFplc6nOOsGt3XjIfD8w8bXOT2ombw/T296Uv5wxS44jPTqY4cFpHgbQrh2lVIDiKk1EaDITOxu/yXWF/4LIc9aP+FsrlMk+sgP/GKxrotIsyPg/rOHXRwY/UkyGwtuefFanxc4px1PP/00Pj95j0Abrv792zvETMEb8yTYSLB/VpY2I="
# _token = parse.unquote(_token)
print(_token)
s = base64.b64decode(_token)
s = zlib.decompress(s)
print(s)
