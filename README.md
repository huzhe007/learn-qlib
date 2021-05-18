## qlib 学习

### qlib功能以及解决什么问题
一个量化投资系统，是为了将AI的技术和量化投资相结合，帮助用户实现量化投资
+ Qlib可以改变传统的量化研究，Paper提出了传统量化研究的问题，例如，交易信号都是通过线性模型产生的，这种方式过于原始，我们应该使用更多新的方法挖掘交易信号。强化学习（reinforcement learning) 可以提供从数据到最后交易执行end-to-end的解决办法。

+ AI技术要求高性能的基础架构，因为高频交易需要巨大的数据了来生成交易信号，因为对系统的基础框架提出了挑战。

+ 金融数据存在噪声数据，机器学习的算法多数以数据作为驱动，很容易出现过度拟合等。

+ 超参数优化限制了量化研究，因为不同的机器学习算法优化的方式不一样，很多的量化研究人员的也许并不了解，巨大的学习成本让很多的人放弃使用机器学习算法进行优化。

+ 传统量化研究工具过时并且不完善，传统的量化研究工具，比如投资组合优化工具OLPS，只提供的简单的投资组合选择，并且只支持Matlab和Octave。其他的量化平台也并不完善。
### 如何使用qlib
#### 数据下载
```shell
python3 scripts/get_data.py qlib_data --target_dir ~/.qlib/qlib_data/cn_data --region cn

# 加载数据
import qlib
qlib.init(provider_uri='~/.qlib/qlib_data/cn_data')


# 创建指定格式的时间序列
from qlib.data import D
D.calendar(start_time='2010-01-01', end_time='2017-12-31', freq='day')[:5]

# 提取指定时间范围内沪深300的股票代码
instruments = D.instruments(market='csi300')
D.list_instruments(instruments=instruments, start_time='2010-01-01', end_time='2017-12-31', as_list=True)[:20]
```    

### 工作流
workflow，我们只需要在工作流中构建数据集，训练模型，回测和评估，之后就可以使用qrun自动运行整个工作流程，并在jupyter notebook中给出图形报告分析。
+ 数据
    + 加载数据
    + 处理数据
    + 数据切片
+ 模型
    + 训练与推导
    + 保存与加载
+ 评价
    + 预测信号分析
    + 回测

### 如何运行
```shell
# 运行单个
qrun configuration.yaml
# 运行多个参考run_all_model.py，写一个Python脚本
python run_all_model.py --models=lightgbm
# 参考examples中workflow_by_code脚本，在Notebook中执行
```

+ 基于notebook的例子
workflow_by_code.ipynb

### 参考资料
+ [《微软面向AI量化架构Qlib深度解析》](https://zhuanlan.zhihu.com/p/336309286)
+ [《微软首个AI量化投资开源平台Qlib上手体验》](https://cloud.tencent.com/developer/article/1763064)