#!/bin/bash
#ecoding=utf-8
import markdown2
import re
import os
import shutil
import sys
import json
import time
reload(sys)
sys.setdefaultencoding("utf8")

def printlog(msg):
    print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+"  "+msg


printlog("开始构建")
# 获取post文件夹中所有的文章
postList = os.listdir("post")
noteTemplate = open("template/note.html")
tempHTml = noteTemplate.read()
# 删除target目录
shutil.rmtree("target/post")
post_list = []
# 将基础文件复制过去
if os.path.exists(r"target/static"):
    shutil.rmtree("target/static")
shutil.copytree("static", "target/static")

printlog("开始文章转化...")
for post in postList:
    html = markdown2.markdown_path("post/"+post)
    # target 目录存放构建后的整站代码
    if not os.path.exists(r"target/post"):
        os.makedirs("target/post")

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
    # 去掉标题和时间\类型
    html = html.replace("<h2>"+title+"</h2>","").replace("<strong>"+noteDate+"</strong>","").replace("<strong>"+noteType+"</strong>","")
    # 代码高亮
    res_code = r'<code>(.*?)</code>'
    codeList = re.findall(res_code,html,re.S|re.M)

    for code in codeList:
        codeType = code.split("\n")[0]
        srcCode = "<code>" + code + "</code>"
        newCode = "<pre><code class='language-"+codeType+"'>"+code.replace(codeType+"\n","")+"</code></pre>";
        html = html.replace(srcCode,newCode)
    fileName = title + "-" + noteDate
    # 拿到一张图片
    res_img = r'<img src="../static/image/(.*?)" alt="" />'
    img_list = re.findall(res_img, html, re.S | re.M)
    img_name = ""
    if len(img_list) > 0 :
        img_name = img_list[0]
    if img_name == "" :
        img_name = 'default.jpg'
    post_dict = {"title":title,"date":noteDate,"type":noteType,"summary":post_blockquote,"thumb":"static/image/"+img_name}
    post_list.append(post_dict)
    fp = open("target/post/"+fileName+".html","w")
    fp.write(tempHTml.replace("{{post-content}}",html)
             .replace("{{post-title}}",title)
             .replace("{{post-date}}",noteDate)
             .replace("{{post-type}}",noteType)
             .replace("<code>","<pre><code>")
             .replace("</code>","</code></pre>"))
    fp.close()
    printlog("["+title+"]转化完成")

printlog("文章转化完成")
# 把主页复制进去
index = open("target/index.html","w")
index.write(open("index.html").read());
index.close()
printlog("首页已生成")
printlog("开始写入目录数据")
# 写入菜单数据
dj = open("target/data.json","w")
dj.write(json.dumps(post_list))
dj.close()
printlog("目录数据写入完成")
printlog("构建结束")
