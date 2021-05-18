'''

QLIB名称       baostock名称
change          pctChg       涨跌幅
close           close       复权收盘价
factor                      复权因子
high            high        复权最高价
low             low         复权最低价
open            open        复权开盘价
volume          volume       成交量


未做数据清理，例如未剔除低价股、低流动性股票，训练集和测试集较短，未进行参数优化等
'''

import baostock as bs
import pandas as pd
import time
import akshare as ak
import numpy as np


if __name__ == "__main__":
    ### 第一步_获取所有股票的代码
    
    # 深证A指
    all_sz = ak.stock_info_sz_name_code(indicator="A股列表")
    # 上证指数
    all_sh1 = ak.stock_info_sh_name_code(indicator="主板A股")
    all_sh2 = ak.stock_info_sh_name_code(indicator="主板B股")
    # 次新股
    all_new = ak.stock_zh_a_new()
    # 创业板

    #风险警示板

    #退市股,终止上市

    #st股,*st股


    df1 = 'sz' + all_sz.A股代码
    df2 = 'sh' + all_sh1.COMPANY_CODE
    df3 = 'sh' + all_sh2.COMPANY_CODE
    df4 = all_new.symbol

    t1 = np.array(df1)
    t2 = np.array(df2)
    t3 = np.array(df3)
    t4 = np.array(df4)

    stock_sz = np.hstack([t1, 'sz399107'])
    stock_sh = np.hstack([t2, t3, 'sh000001'])
    stock_new = t4


    stock_item = {'深证A指': stock_sz, '上证指数': stock_sh}
    stock_item = {'次新股': stock_new}

    #### 第二步 登陆baostock系统 ####
    lg = bs.login()
    # 显示登陆返回信息
    # print('login respond error_code:'+lg.error_code)
    # print('login respond  error_msg:'+lg.error_msg)

    #### 第三步 获取沪深A股历史K线数据 ####
    data_start = '2018-01-01'
    data_end = '2021-01-22'
    # 详细指标参数，参见“历史行情指标参数”章节；“分钟线”参数与“日线”参数不同。“分钟线”不包含指数。
    # 分钟线指标：date,time,code,open,high,low,close,volume,amount,adjustflag
    # 周月线指标：date,code,open,high,low,close,volume,amount,adjustflag,turn,pctChg
    # 日线指标 : date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg
    for key, value in stock_item.items():
        for single_stock in value:
            if single_stock not in stock_new:###需做数据清洗,去除掉退市股、风险警示股票、次新股等
                ### 默认后复权；复权状态(1：后复权， 2：前复权，3：不复权）
                rs = bs.query_history_k_data_plus(single_stock,
                                                  "code,date,open,high,low,close,volume,amount,turn,pctChg",
                                                  start_date=data_start,
                                                  end_date=data_end,
                                                  frequency="d")

                ### 只查询一个价格就可以计算复权因子
                bfq = bs.query_history_k_data_plus(single_stock,
                                                   "open",
                                                   start_date=data_start,
                                                   end_date=data_end,
                                                   frequency="d",
                                                   adjustflag='3')

                # print('query_history_k_data_plus respond error_code:'+rs.error_code)
                # print('query_history_k_data_plus respond  error_msg:'+rs.error_msg)

                #### 打印结果集 ####
                data_list = []
                while (rs.error_code == '0') & rs.next():
                    # 获取一条记录，将记录合并在一起
                    imf = rs.get_row_data()
                    # 去除中间的·
                    imf[0] = imf[0][:2] + imf[0][3:]
                    bfq_open = float(bfq.get_row_data()[0])
                    hfq_open = float(imf[3])
                    factor = '{:.7f}'.format(hfq_open / bfq_open)
                    imf.append(factor)
                    data_list.append(imf)

                new_columns = rs.fields
                new_columns[-1] = 'change'
                new_columns.append('factor')
                # print(rs.fields)
                result = pd.DataFrame(data_list, columns=new_columns)
                #### 结果集输出到csv文件 ####
                if len(result) > 2 :
                    result.to_csv("./csv_data/%s/%s.csv" % (key, single_stock), index=False)

    #### 登出系统 ####
    bs.logout()
