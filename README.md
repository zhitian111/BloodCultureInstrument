# 远程服务器IP
- 114.55.149.212

# 数据库
## SQL Server端口号
- 1433
## 表结构


# 项目目录结构
```
BloodCultureInstrument/
├── Makefile                   
├── README.md
├── LICENSE
├── .gitignore
├── data/
├── model/
├── src/
│   ├── python/
│   │   └── requirements.txt
├── db/
│   └── scripts/
├── build/
│	├── obj/
│	└── bin/
├── docs/
├── .temp/
└── scripts/
```
单独强调一下python这部分，考虑到我们使用的虚拟环境方案不一致（python3-venv、anaconda、pycharm...），我们需要单独使用一个requirements.txt文件来同步我们python的运行环境。其他语言类似python单开文件夹即可，但涉及到依赖库等情况，同样需要指明依赖。
# 编码规范

