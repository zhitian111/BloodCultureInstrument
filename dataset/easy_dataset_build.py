import pyarrow as pa  # 导入PyArrow核心库，用于处理Arrow数据结构
import pyarrow.csv as csv  # 导入PyArrow CSV处理模块，用于于读取CSV文件并转换为Arrow表格
import pyarrow.feather as feather  # 导入Feather格式处理模块，用于读写Arrow格式文件


def main():
    # 读取数据CSV文件（datas.csv）并转换为Arrow Table
    # Arrow Table是PyArrow中用于存储结构化数据的核心对象，采用列式存储
    data_table = csv.read_csv("original_data/datas.csv")

    # 从数据表格中删除指定列（"SPE_CODE"和"RD_DTime"）
    # drop()方法支持传入列名列表，批量删除不需要的列，返回新的Table对象
    data_table = data_table.drop(["SPE_CODE", "RD_DTime"])

    # 将处理后的data_table写入Arrow格式文件（.arrow扩展名）
    # Feather格式是基于Arrow的高效存储格式，读写速度快且保留完整数据类型
    feather.write_feather(data_table, "data.arrow")

    # 读取标签CSV文件（labels.csv）并转换为Arrow Table
    label_table = csv.read_csv("original_data/labels.csv")

    # 从标签表格中删除指定列（"SPE_CODE"）
    label_table = label_table.drop(["SPE_CODE"])

    # 将处理后的label_table写入另一个Arrow格式文件
    feather.write_feather(label_table, "label.arrow")


# 当脚本直接运行时，执行main()函数
if __name__ == "__main__":
    main()
