import os

# ---------------------- 1. 精确计算项目根目录（适配文件位置：lib/python_lib/global_config.py） ----------------------
# 当前文件绝对路径
CURRENT_FILE_PATH = os.path.abspath(__file__)
# 父目录：lib/python_lib
LIB_PYTHON_DIR = os.path.dirname(CURRENT_FILE_PATH)
# 祖父目录：lib
LIB_DIR = os.path.dirname(LIB_PYTHON_DIR)
# 曾祖父目录：项目根目录（最终需要的根路径）
ROOT_PATH = os.path.dirname(LIB_DIR)

# 验证根目录是否正确（启动时打印，便于调试）
print(f"📌 项目根目录已确认：{ROOT_PATH}")

# ---------------------- 2. 定义路径变量（严格区分目录DIR和文件FILE） ----------------------
# 核心目录路径（DIR结尾）
DATASET_DIR = os.path.join(ROOT_PATH, "dataset")  # 数据集总目录
MODEL_DIR = os.path.join(ROOT_PATH, "model")  # 模型存储目录
LIB_DIR = os.path.join(ROOT_PATH, "lib", "python_lib")  # 代码库目录
PROCESSED_DATA_DIR = os.path.join(DATASET_DIR, "processed_data")  # 处理后数据目录
ORIGINAL_DATA_DIR = os.path.join(DATASET_DIR, "original_data")  # 原始数据目录

# 关键文件路径（FILE结尾）
PROCESSED_DATA_FILE = os.path.join(PROCESSED_DATA_DIR, "data.arrow")  # 处理后的数据文件
PROCESSED_LABEL_FILE = os.path.join(PROCESSED_DATA_DIR, "label.arrow")  # 处理后的标签文件

# ---------------------- 3. 统一路径字典（便于其他模块引用） ----------------------
PATH_CONFIG = {
    # 根目录
    "ROOT": ROOT_PATH,
    # 目录路径
    "DATASET_DIR": DATASET_DIR,
    "MODEL_DIR": MODEL_DIR,
    "LIB_DIR": LIB_DIR,
    "PROCESSED_DATA_DIR": PROCESSED_DATA_DIR,
    "ORIGINAL_DATA_DIR": ORIGINAL_DATA_DIR,
    # 文件路径
    "PROCESSED_DATA_FILE": PROCESSED_DATA_FILE,
    "PROCESSED_LABEL_FILE": PROCESSED_LABEL_FILE
}


# ---------------------- 5. 提供便捷的路径获取函数（可选，进一步简化引用） ----------------------
def get_path(key):
    """通过key快速获取路径，自动检查key合法性"""
    if key not in PATH_CONFIG:
        raise KeyError(f"路径配置中不存在key：{key}，可用key：{list(PATH_CONFIG.keys())}")
    return PATH_CONFIG[key]
