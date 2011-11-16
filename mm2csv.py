#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 2011/11/14

@author: adatch
'''

import sys, os.path
from xml.etree.ElementTree import *

class CMMParse:
    '''
    classdocs
    '''
    maxDepth = 0
    depth = 0
    text = "TEXT"
    builtin = "BUILTIN"
    btnOK = "button_ok"
    node = "node"
    icon = "icon"
    record = []
    table = []

    def __init__(self):
        pass

    def recursive(self, elem):
        #depthがmaxDepthを上回ったらmaxDepthに代入
        self.depth += 1
        if self.depth > self.maxDepth:
            self.maxDepth = self.depth

        #タグとテキスト出力
        self.record.append("\"" + elem.get(self.text) + "\",")

        #childあったらそれぞれのchildで再帰的にroop
        children = elem.getchildren()
        if not len(children):
            #なければ1行分をtableに出力
            self.table.append(self.record[:])
        else:
            for child in children:
                #ノードの時のみ再帰
                if child.tag == self.node:
                    self.recursive(child)
                else:
                    continue

        #depth--してリターン
        self.depth -= 1
        self.record.pop()
        return

    #各行のノード数を揃える
    def fixsize(self):
        for record in self.table:
            recdepth = len(record)
            for i in range(self.maxDepth - recdepth):
                record.insert(-1, "\"-\",")

    #カンマ区切りの文字列を作る
    def csvBuild(self):
        self.csvString = ""
        for record in self.table:
            for node in record:
                self.csvString += node
            self.csvString = self.csvString[:-1] + "\n" #余分なカンマをとって改行をつける

'''
メイン処理
'''
if __name__ == '__main__':
    argvs = sys.argv
    argc = len(argvs)
    if (argc != 2):
        print 'Usage: # python %s MindMap filename' % argvs[0]
        quit()

    mmfile = argvs[1]
    mmparse = CMMParse()
    tree = parse(mmfile)
    mapElem = tree.getroot()
    root = mapElem.getchildren()[0]
    mmparse.recursive(root)
    mmparse.fixsize()
    mmparse.csvBuild()

    csvfilename, ext = os.path.splitext(mmfile)
    csvfilename += ".csv"
    csvfile = open(csvfilename, "w")
    csvfile.write(mmparse.csvString.encode('utf-8'))
    csvfile.close()
