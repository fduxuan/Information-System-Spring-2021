# 基本简介

![](assets/logo.png)



<p align="center">
  <img src="https://img.shields.io/badge/测试覆盖率-100%25-success" />
  <img src="https://img.shields.io/badge/生产版本-v1.0-blue" />
</p>
<p align="center">
 <img src="https://img.shields.io/badge/服务端-FastAPI-blueviolet" />
  <img src="https://img.shields.io/badge/客户端-Vue-green" />
  <img src="https://img.shields.io/badge/UI支持-AntD-bb0eb5" />
  <img src="https://img.shields.io/badge/文档-Material&Mkdocs-lightgrey" />
  <img src="https://img.shields.io/badge/仓库支持-gitea-orange" />
  <img src="https://img.shields.io/badge/流水线支持-drone-important" />
  <img src="https://img.shields.io/badge/部署支持-Docker-069e5c" />
</p>


<br>

**SOFT630016.01: 信息系统设计与数据分析** 

 **计算机科学技术学院，复旦大学，上海**

-----



!!! hint "声明"
    该项目是一个前后端Web项目，所有代码均为我们 **{++自行完成++}**
**贡献者:** 方煊杰，蒋艳琪，施杰，徐艺文 (按首字母排序）


---

## 框架

### 服务端

<img src="https://img.shields.io/badge/API文档-Swagger-blueviolet" />

* `FastAPI`    `Python`

* `文档地址`: [http://106.14.244.24:8080/document](http://106.14.244.24:8080/document)

* `工作量`: **1754 行**

```
(venv) ☁  Backend [master] cloc * --exclude-dir=db,venv
      26 text files.
      26 unique files.                              
       2 files ignored.

github.com/AlDanial/cloc v 1.82  T=0.07 s (383.9 files/s, 39387.5 lines/s)
-------------------------------------------------------------------------------
Language                     files          blank        comment           code
-------------------------------------------------------------------------------
Python                          21            456            334           1716
Dockerfile                       1              8              0             21
YAML                             1              2             10             14
Markdown                         1              1              0              2
Bourne Shell                     1              0              0              1
-------------------------------------------------------------------------------
SUM:                            25            467            344           1754
-------------------------------------------------------------------------------

```



---

### 客户端

<img src="https://img.shields.io/badge/Vue-AntD-informational" />

* `展示地址`: [http://106.14.244.24:8080](http://106.14.244.24:8080)
* `工作量`：**5611 行**
* `测试账号`：账号 admin@qq.com  密码 admin123

```
☁  Frontend [master] ⚡  cloc src 
      48 text files.
      48 unique files.                              
       0 files ignored.

github.com/AlDanial/cloc v 1.82  T=0.11 s (427.9 files/s, 66025.4 lines/s)
-------------------------------------------------------------------------------
Language                     files          blank        comment           code
-------------------------------------------------------------------------------
Vuejs Component                 34            748            835           5230
JavaScript                      13            102            108            369
CSS                              1              2              0             12
-------------------------------------------------------------------------------
SUM:                            48            852            943           5611
-------------------------------------------------------------------------------

```

