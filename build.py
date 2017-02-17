#!/bin/bash
#ecoding=utf-8
import markdown2
import re
import os
import shutil
import sys
import json
reload(sys)
sys.setdefaultencoding("utf8")
# 获取post文件夹中所有的文章
postList = os.listdir("post")
noteTemplate = open("template/note.html")
tempHTml = noteTemplate.read()
# 删除target目录
shutil.rmtree("target/post")
post_list = []
for post in postList:
    html = markdown2.markdown_path("post/"+post)
    # target 目录存放构建后的整站代码
    if not os.path.exists(r"target/post"):
        os.makedirs("target/post")
    # 将基础文件复制过去
    if os.path.exists(r"target/static"):
        shutil.rmtree("target/static")
    shutil.copytree("static","target/static")

    # print html
    # 获取文章的标题和时间
    res_h2 = r'<h2>(.*?)</h2>'
    h2_list = re.findall(res_h2, html, re.S | re.M)
    fileName = ""

    title = ""
    if len(h2_list) > 0 :
        title = h2_list[0]
    res_strong = r'<strong>(.*?)</strong>'
    strong_list = re.findall(res_strong, html, re.S | re.M)

    noteType = ""
    noteDate = ""
    if len(strong_list) >= 2 :
        noteType = strong_list[0]
        noteDate = strong_list[1]
    #   获取文章摘要
    res_blockquote = r'<blockquote>(.*?)</blockquote>'
    blockquote_list = re.findall(res_blockquote, html, re.S | re.M)
    post_blockquote = ""
    if len(blockquote_list) > 0:
        post_blockquote = blockquote_list[0].replace("\n","").replace("<p>","").replace("</p>","")

    html = html.replace("<h2>"+title+"</h2>","").replace("<strong>"+noteDate+"</strong>","").replace("<strong>"+noteType+"</strong>","")

    fileName = title + "-" + noteDate
    post_dict = {"title":title,"date":noteDate,"type":noteType,"summary":post_blockquote}
    post_list.append(post_dict)
    fp = open("target/post/"+fileName+".html","w")
    fp.write(tempHTml.replace("{{post-content}}",html)
             .replace("{{post-title}}",title)
             .replace("{{post-date}}",noteDate)
             .replace("{{post-type}}",noteType)
             .replace("<code>","<pre><code>")
             .replace("</code>","</code></pre>"))
    fp.close()
print json.dumps(post_list)



# yl= yaml.load(file("config.yaml"))
# print yl["author"]["name"]

# html = markdown2.markdown_path("README.md")
#
#
# res_tr = r'<code>(.*?)</code>'
# codeBlock = re.findall(res_tr,html,re.S|re.M)
# codeBlockCount = len(codeBlock)
# if codeBlockCount != 0 :
#     for i in range(codeBlockCount):
#         codeStr = codeBlock[i]
#         langType = codeStr.split("\n")[0]
#         codeStr = "<pre><code class='language-"+langType+"'>"+codeStr.replace(langType,"")+"</code></pre>"
#         print codeStr
# 第一个<h2>表示文章标题。
# 第一个<strong>标记了原创还是转载，第二个<strong>表示当前时间。
# 第一个<blockquote>表示文章的预览内容。
# 文章所有<code>标签会被加个<pre>标签包裹，同时<code>添加class=language-xxx属性。
# 生成的HTML

