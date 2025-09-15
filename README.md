# 远程服务器IP
- 114.55.149.212

# 数据库
## SQL Server端口号
- 1433
## 源数据库表结构
### SPE_LIST
| 序号 | 字段名      | 字段类型     | 备注                  |
|:----:|------------|-------------|-----------------------|
| 1    | ID         | int         | 该条数据的标识符       |
| 2    | SPE_CODE   | nvarchar(20)| 瓶身条码               |
| 3    | LIS_CODE   | nvarchar(20)| 标本编号(或LIS编号)    |
| 4    | PA_NAME    | nvarchar(20)| 病人姓名               |
| 5    | SPE_TYPE   | nvarchar(20)| 标本类型               |
| 6    | Category   | nvarchar(20)| 培养瓶类型             |
| 7    | CASE_CODE  | nvarchar(20)| 病历号                 |
| 8    | HOS_CODE   | nvarchar(20)| 住院号                 |
| 9    | PA_Sex     | nvarchar(2) | 病人性别               |
| 10   | PA_Age     | Tinyint     | 年龄                   |
| 11   | PA_Ageunit | nvarchar(2) | 年龄单位               |
| 12   | MA_CODE    | Tinyint     | 机器号                 |
| 13   | CAB_CODE   | nvarchar(2) | 仓位号                 |
| 14   | POS_CODE   | nvarchar(3) | 瓶位号（例如：B12）含模块号 |
| 15   | Department | nvarchar(30)| 送检科室               |
| 16   | SUB_DTime  | Datetime    | 送检日期               |
| 17   | SPE_Result | Tinyint     | 检测结果【1：在检 2：阳性 3：阴性】 |
| 18   | IN_DTime   | Datetime    | 置瓶时间               |
| 19   | OUT_DTime  | Datetime    | 取瓶时间               |
| 20   | AL_DTime   | Datetime    | 报警时间               |
| 21   | AL_Hours   | int         | 报警时长               |
| 22   | SET_Hours  | int         | 预置时长               |
| 23   | IF_Checking| bit         | 是否在检               |
| 24   | IF_Anon    | bit         | 是否匿名               |
| 25   | IF_Again   | bit         | 是否二次置瓶           |
| 26   | IN_DTime_Again | Datetime | 二次置瓶时间（备用）   |
### SPE_DATA
| 序号 | 字段名      | 字段类型     | 备注                          |
|:----:|------------|-------------|-------------------------------|
| 1    | ID         | Bigint      | 该条数据的标识符               |
| 2    | SPE_CODE   | nvarchar(20)| 标本编号                       |
| 3    | RD_Value   | int         | 检测值                         |
| 4    | RD_DTime   | Datetime    | 检测时间                       |
| 5    | AL_Point   | tinyint     | 报警点【0：未报警，2：阳性，3：阴性】 |
| 6    | AL_NO      | tinyint     | 算法标志                       |


# 项目目录结构
```
BloodCultureInstrument/
├── Makefile                   
├── README.md
├── LICENSE
├── .gitattributes
├── .gitignore
├── dataset/
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

