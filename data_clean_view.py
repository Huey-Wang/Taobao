import numpy as np
import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Bar, Map, Page, Pie
# from pyecharts.commons.utils import JsCode

columns = ['地点', '价格', '收货人数']
df = pd.read_csv(r'F:\pythoncode\淘宝\goodsinfo.csv', names=columns)
df['省'] = df['地点'].str[:2].str.strip()
df['区/县'] = df['地点'].str[3:].str.strip()
df1 = df.drop('地点', axis=1)
a = df1['收货人数'].str.replace(r'人收货', '')
a = a.str.replace(r'+', '')
a = a.str.replace(r'万', '')
a = a.astype(float)
copy_a = a
a = a[np.array(a) < 11] * 10000
copy_a[:len(a)] = a
df1['收货人数'] = copy_a
# df1.to_csv('F:\pythoncode\淘宝\info.csv')

# 计算各省订单数
saletotal = df1['收货人数'].groupby(df1['省']).sum().sort_values(ascending=False)
maxvalue = saletotal[0]
minvalue = saletotal[-1]
values = saletotal.tolist()
provinces = saletotal.index.tolist()
# 获得pie图数据
new_value = saletotal[6:].sum()
pievalue = saletotal[:6].tolist()
pievalue.append(new_value)
pieprovinces = provinces[:6]
pieprovinces.append('其他省份')

# 计算四川省销售分布
salezone = df1.groupby(df1['省'])
sichuan = dict(list(salezone))
sichuan = pd.DataFrame(sichuan['四川'], columns=['价格', '收货人数', '区/县'])
sichuan = sichuan['收货人数'].groupby(sichuan['区/县']).sum().sort_values(ascending=False)
value_sichuan = sichuan.tolist()
maxvalue1 = value_sichuan[0]
distincts = sichuan.index.tolist()
for i, distinct in enumerate(distincts):
    if distinct == '凉山':
        distincts[i] = distinct+'彝族自治州'
    else:
        distincts[i] = distinct+'市'


# --------------------------------------------------数据可视化 -------------------------------------------------------#

#  全国橙子分布
def chinamap() -> Map:
    c = (
        Map()
        .add("橙子销量", [list(z) for z in zip(provinces, values)], "china")
        .set_global_opts(
            title_opts=opts.TitleOpts(title="全国橙子哪家强"),
            visualmap_opts=opts.VisualMapOpts(max_=maxvalue, is_piecewise=True,
                                              pieces=[{"min": minvalue, "max": 1000}, {"min": 1000, "max": 10000},
                                                      {"min": 10000, "max": 20000}, {"min": 20000, "max": 40000},
                                                      {"min": 40000, "max": 60000}, {"min": 100000, "max": 120000},
                                                      {"min": 400000, "max": 500000}, {"min": 500000, "max": 600000},
                                                      {"min": 600000, "max": maxvalue}]),
        )  # .render("全国橙子哪家强.png")
    )
    return c


def bar_sale() -> Bar:
    c = (
        Bar()
        .add_xaxis(provinces)
        .add_yaxis('', values)
        .set_global_opts(
            legend_opts=opts.LegendOpts(pos_right="20%"),
            visualmap_opts=opts.VisualMapOpts(is_show=False, max_=maxvalue, is_piecewise=True,
                                              pieces=[{"min": minvalue, "max": 1000}, {"min": 1000, "max": 10000},
                                              {"min": 10000, "max": 20000}, {"min": 20000, "max": 40000},
                                              {"min": 40000, "max": 60000}, {"min": 100000, "max": 120000},
                                              {"min": 400000, "max": 500000}, {"min": 500000, "max": 600000},
                                              {"min": 600000, "max": maxvalue}]),
        )  # .render("销量bar.png")
    )
    return c


def page_draggable_layout():
    page = Page(layout=Page.DraggablePageLayout)
    page.add(
        chinamap(),
        bar_sale(),
    )
    page.render("面板图.html")


def salepie():
    c = (
        Pie()
        .add(
            "",
            [list(z) for z in zip(pieprovinces, pievalue)],
            radius=["40%", "55%"],
            label_opts=opts.LabelOpts(
                position="outside",
                formatter="{a|{a}}{abg|}\n{hr|}\n {b|{b}: }{c}  {per|{d}%}  ",
                background_color="#eee",
                border_color="#aaa",
                border_width=1,
                border_radius=4,
                rich={
                    "a": {"color": "#999", "lineHeight": 22, "align": "center"},
                    "abg": {
                        "backgroundColor": "#e3e3e3",
                        "width": "100%",
                        "align": "right",
                        "height": 22,
                        "borderRadius": [4, 4, 0, 0],
                    },
                    "hr": {
                        "borderColor": "#aaa",
                        "width": "100%",
                        "borderWidth": 0.5,
                        "height": 0,
                    },
                    "b": {"fontSize": 16, "lineHeight": 33},
                    "per": {
                        "color": "#eee",
                        "backgroundColor": "#334455",
                        "padding": [2, 4],
                        "borderRadius": 2,
                    },
                },
            ),
        )
            .set_global_opts(title_opts=opts.TitleOpts(title="中国橙子哪家强"))
            .render("pie_rich_label.html")
    )


#  四川橙子分布
def sichuanmap():
    c = (
        Map()
        .add("橙子销量", [list(z) for z in zip(distincts, value_sichuan)], "四川")
        .set_global_opts(
            title_opts=opts.TitleOpts(title="四川销售分布"),
            visualmap_opts=opts.VisualMapOpts(max_=maxvalue1, is_piecewise=True,
                                              pieces=[{"min": 0, "max": 1000},{"min": 1000, "max": 3000},
                                                          {"min": 300000, "max": maxvalue1}]),
        )
        .render("map_sichuan.html")
    )


def sichuanbar():
    d = (
        Bar()
        .add_xaxis(distincts)
        .add_yaxis("橙子销量", value_sichuan)
        .set_global_opts(xaxis_opts=opts.AxisOpts(
            axislabel_opts=opts.LabelOpts(interval=0)),
            title_opts=opts.TitleOpts(title="四川销量分布"))
        .render("bar_sichuan.html")
    )


page_draggable_layout()
sichuanmap()
sichuanbar()
