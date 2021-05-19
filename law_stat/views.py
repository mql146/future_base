from django.shortcuts import render

# Create your views here.




from django.http import HttpResponse
from .models import Provision
import os
import sys
import re
from pyecharts.charts import Bar,WordCloud
from pyecharts.components import Table
from pyecharts import options as opts
from pyecharts.options import ComponentTitleOpts
from pyecharts.globals import SymbolType
import json
from random import randrange
import jieba

def make_law_init(request):
    if 'has data':
        return HttpResponse('law data has init')
    else:
        with open('./law_stat/static/minfa.txt','r') as f:
            lines = f.readlines()
        file_text = ''.join(lines)
        flags=set()

        boundary = ['','','','','']
        levels = ['编','分编','章','节','条']
        hit_records=[]

        for i in range(len(lines)):
            line = lines[i]
            head = line.split('　')[0]
            
            for j in range(len(levels)):
                seg = levels[j]
                m = re.match('第[一二三四五六七八九十百千万]*'+seg,head)
                if m:
                    start,end=m.span()
                    flags.add(head[start:end])
                    boundary[j] = head[start:end]
                    for k in range(j+1,len(boundary)):
                        boundary[k] = ''
                    hit_records.append([i]+boundary)

        print(len(hit_records))
        records = []
        for i in range(1,len(hit_records)):
            pre = hit_records[i-1]
            now = hit_records[i]
            start_index = len(lines[pre[0]].split('　')[0])+1
            records.append(pre[1:]+[''.join(lines[pre[0]:now[0]])[start_index:]])
        print(len(records))

        try:
            for record in records:
                m = Provision()
                m.compose_name = record[0]
                m.arrange_name = record[1]
                m.chapter_name = record[2]
                m.section_name = record[3]
                m.provision_name = record[4]
                m.content = record[5]
                m.save()
            return HttpResponse('successful to init law data')
        except Exception as e:
            print(e)
            return HttpResponse('failed to init law data')


def view_law_provision(request):
    ctx ={}
    if request.POST:
        rows = list(Provision.objects.filter(compose_name=request.POST['compose_name']).values_list("compose_name", "arrange_name", "chapter_name", "section_name", "provision_name",'content'))
        ctx['object_list'] = rows[:5]
        word_dict={}
        for row in rows:
            for word in jieba.cut(row[5]):
                if word_dict.get(word) is None:
                    word_dict[word]=0
                word_dict[word]+=1
        

    bar = Bar()
    bar.add_xaxis(["衬衫", "毛衣", "领带", "裤子", "风衣", "高跟鞋", "袜子"])
    bar.add_yaxis("商家A", [114, 55, 27, 101, 125, 27, 105])
    bar.add_yaxis("商家B", [57, 134, 137, 129, 145, 60, 49])
    bar.set_global_opts(title_opts=opts.TitleOpts(title="某商场销售情况"))
    ctx['data'] = json.loads(bar.dump_options_with_quotes())

    return render(request, "law_stat/index.html", ctx)
    return HttpResponse(content=open("./templates/law_stat/index.html").read())

def bar_base() -> Bar:
    c = (
        Bar()
        .add_xaxis(["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"])
        .add_yaxis("商家A", [randrange(0, 100) for _ in range(6)])
        .add_yaxis("商家B", [randrange(0, 100) for _ in range(6)])
        .set_global_opts(title_opts=opts.TitleOpts(title="Bar-基本示例", subtitle="我是副标题"))
        .dump_options_with_quotes()
    )
    return c

def test_view(request):
    bar = Bar()
    bar.add_xaxis(["衬衫", "毛衣", "领带", "裤子", "风衣", "高跟鞋", "袜子"])
    bar.add_yaxis("商家A", [114, 55, 27, 101, 125, 27, 105])
    bar.add_yaxis("商家B", [57, 134, 137, 129, 145, 60, 49])
    bar.add_yaxis("商家C", [randrange(0, 100) for _ in range(6)])
    bar.set_global_opts(title_opts=opts.TitleOpts(title="某商场销售情况"))

    word_cloud = WordCloud()
    rows = list(Provision.objects.values_list("compose_name", "arrange_name", "chapter_name", "section_name", "provision_name",'content'))
    word_dict={}
    for row in rows[:5]:
        for word in jieba.cut(row[5]):
            if word_dict.get(word) is None:
                word_dict[word]=0
            word_dict[word]+=1
    data = [(k,v) for k,v in word_dict.items()]
    word_cloud.add(series_name="法编分析", data_pair=data, word_size_range=[6, 66])
    word_cloud.set_global_opts(
        title_opts=opts.TitleOpts(
            title="法编分析", title_textstyle_opts=opts.TextStyleOpts(font_size=23)
        ),
        tooltip_opts=opts.TooltipOpts(is_show=True),
    )

    words = [
        ("Sam S Club", 10000),
        ("Macys", 6181),
        ("Amy Schumer", 4386),
        ("Jurassic World", 4055),
        ("Charter Communications", 2467),
        ("Chick Fil A", 2244),
        ("Planet Fitness", 1868),
        ("Pitch Perfect", 1484),
        ("Express", 1112),
        ("Home", 865),
        ("Johnny Depp", 847),
        ("Lena Dunham", 582),
        ("Lewis Hamilton", 555),
        ("KXAN", 550),
        ("Mary Ellen Mark", 462),
        ("Farrah Abraham", 366),
        ("Rita Ora", 360),
        ("Serena Williams", 282),
        ("NCAA baseball tournament", 273),
        ("Point Break", 265),
    ]
    c = WordCloud()
    c.add("", words, word_size_range=[20, 100], shape=SymbolType.DIAMOND)
    c.set_global_opts(title_opts=opts.TitleOpts(title="WordCloud-shape-diamond"))
    return HttpResponse(c.render_embed())

    data = {
        "code": 200,
        "msg": "success",
        "data": json.loads(c.dump_options_with_quotes()),
    }
    json_str = json.dumps(data)
    response = HttpResponse(
        json_str,
        content_type="application/json",
    )
    response["Access-Control-Allow-Origin"] = "*"
    
    return response

def get_law_provision(request):
    table = Table()

    headers = ["compose_name", "arrange_name", "chapter_name", "section_name", "provision_name",'content']
    rows = list(Provision.objects.values_list("compose_name", "arrange_name", "chapter_name", "section_name", "provision_name",'content'))
    
    table.add(headers, rows)
    table.set_global_opts(
        title_opts=ComponentTitleOpts(title="民法典", subtitle="法条概览")
    )
    table.render('ddf.html')
    return HttpResponse(content=open('./ddf.html').read())


def test_post(request):
    ctx ={}
    if request.POST:
        ctx['rlt'] = request.POST['q']
    print(request.POST)
    print(type(request.POST['q']))
    return render(request, "law_stat/test_post.html", ctx)
    
def test_word_cloud(request):
    words = [
        ("Sam S Club", 10000),
        ("Macys", 6181),
        ("Amy Schumer", 4386),
        ("Jurassic World", 4055),
        ("Charter Communications", 2467),
        ("Chick Fil A", 2244),
        ("Planet Fitness", 1868),
        ("Pitch Perfect", 1484),
        ("Express", 1112),
        ("Home", 865),
        ("Johnny Depp", 847),
        ("Lena Dunham", 582),
        ("Lewis Hamilton", 555),
        ("KXAN", 550),
        ("Mary Ellen Mark", 462),
        ("Farrah Abraham", 366),
        ("Rita Ora", 360),
        ("Serena Williams", 282),
        ("NCAA baseball tournament", 273),
        ("Point Break", 265),
    ]
    c = WordCloud()
    c.add("", words, word_size_range=[20, 100], shape=SymbolType.DIAMOND)
    c.set_global_opts(title_opts=opts.TitleOpts(title="WordCloud-shape-diamond"))

    word_cloud = WordCloud()
    rows = list(Provision.objects.values_list("compose_name", "arrange_name", "chapter_name", "section_name", "provision_name",'content'))
    word_dict={}
    for row in rows[:5]:
        for word in jieba.cut(row[5]):
            if word_dict.get(word) is None:
                word_dict[word]=0
            word_dict[word]+=1
    data = [(k,v) for k,v in word_dict.items()]
    word_cloud.add(series_name="法编分析", data_pair=data, word_size_range=[6, 66])
    word_cloud.set_global_opts(
        title_opts=opts.TitleOpts(
            title="法编分析", title_textstyle_opts=opts.TextStyleOpts(font_size=23)
        ),
        tooltip_opts=opts.TooltipOpts(is_show=True),
    )
    return HttpResponse(word_cloud.render_embed())