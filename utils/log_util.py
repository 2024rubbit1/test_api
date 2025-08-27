# utils/log_util.py
import logging
import os


def get_logger(name=__name__):
    logger = logging.getLogger(name)
    if logger.handlers:  # 避免重复添加 Handler
        return logger

    logger.setLevel(logging.INFO)
    # 定义日志格式
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    # 控制台输出
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../logs')
    os.makedirs(log_dir, exist_ok=True)
    file_handler = logging.FileHandler(os.path.join(log_dir, f"{name.split('.')[-1]}.log"))
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger
