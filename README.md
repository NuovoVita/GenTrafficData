# 生产流量数据

生产流量数据，做流量特性的功能测试和性能测试。

## 一、搭建开发环境

### 1. 环境

Win 和 Linux 都支持
Python >= 3.8
Redis >= 3.x

### 2. 依赖包安装

```bash
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt -i https://pypi.douban.com/simple
```

## 二、生成流量数据

```bash
# 这是生成所有数据的入口，采用多进程方式，生成9中流量测试数据。
python3 gen_traffic_main.py

# 当然，也可以单独生成每一种的流量数据。以攻击流量测试数据为例：
python3 gen_attack_traffic_data.py
```

## 参考

- [详解multiprocessing多进程-process模块](https://blog.csdn.net/brucewong0516/article/details/85776194)
