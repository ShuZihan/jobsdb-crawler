import logging
import os
from datetime import datetime


def init_logger(config) -> logging.Logger:
    # init log dir
    os.makedirs("logs", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(
        config["log_dir"], f"jobsdb_{config['keywords']}_{timestamp}.log"
    )

    # init logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # clear logger handler
    if logger.hasHandlers:
        logger.handlers.clear()

    # init logger formatter
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S"
    )

    # init file handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(getattr(logging, config["file_log_level"].upper()))
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # init console Handler
    if config["enable_console"]:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(getattr(logging, config["console_log_level"].upper()))
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    config_str = "\n".join([f"{k}: {v}" for k, v in config.items()])
    # logging.info(f"config: \n{config_str}")
    separator = "=" * 50
    logging.info(f"\n{separator}\n🔧 Configurations:\n{config_str}\n{separator}")

    return logger
