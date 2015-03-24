# -*- coding: utf-8 -*-
import json
import os
 
 
class JsonFile(object):
    """
    初期化はファイル名を指定する
    >>> jsonfile = JsonFile('filename.json')

    保存する時はキーワード引数で指定する
    >>> jsonfile.save(key1='value1', key2='value2')

    読み出す時はdictが返ってくる（ファイルがなければNoneが返る）
    >>> data = jsonfile.load()
    >>> data['key1']
    u'value1'
    >>> data['key2']
    u'value2'

    いらなくなったら捨てる
    >>> jsonfile.delete()
    """
    def __init__(self, file_name):
        self.file_name = file_name
 
    def save(self, **kwds):
        try:
            with open(self.file_name, mode='w') as f:
                data = json.dumps(kwds)
                f.write(data)
        except IOError:
            print u'Not allowed to write files to this path "%s".' % self.file_name
 
    def load(self):
        try:
            with open(self.file_name, mode='r') as f:
                return json.load(f)
        except IOError:
            return None
 
    def delete(self):
        if os.path.exists(self.file_name):
            os.remove(self.file_name)
