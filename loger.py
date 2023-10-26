import logging
import os


def setup_logging():
    # Создаем директорию "log" (если не существует)
    log_directory = 'log'
    os.makedirs(log_directory, exist_ok=True)

    # Имя файла логов
    log_filename = 'app.log'
    log_path = os.path.join(log_directory, log_filename)

    # Настройка логирования
    logging.basicConfig(level=logging.DEBUG)

    # Создаем логгер
    logger = logging.getLogger(__name__)

    # Создаем обработчик для файла с указанием кодировки UTF-8
    file_handler = logging.FileHandler(log_path, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)

    # Настраиваем формат сообщения
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # Добавляем обработчик к логгеру
    logger.addHandler(file_handler)

    logger.propagate = False

    return logger
logger = setup_logging()