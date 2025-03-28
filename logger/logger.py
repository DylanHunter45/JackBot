import logging

class JackBotLogger:
    _instance = None

    def __new__(cls, log_file_path="./" ,log_level=logging.INFO):
        if not cls._instance:
            cls._instance = super(JackBotLogger, cls).__new__(cls)
            cls._instance._instance = logging.getLogger("jackbot-logger")
            if log_level == logging.DEBUG:
                cls._instance._instance.setLevel(logging.DEBUG)
            elif log_level == logging.WARNING:
                cls._instance._instance.setLevel(logging.WARNING)
            elif log_level == logging.CRITICAL:
                cls._instance._instance.setLevel(logging.CRITICAL)
            else:
                cls._instance._instance.setLevel(logging.INFO)
        file_handler = logging.FileHandler(log_file_path)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        cls._instance._instance.addHandler(file_handler)
        return cls._instance
    
    def log_info(cls, message):
        cls._instance.info(message)

    def log_warning(cls, message):
        cls._instance.warning(message)

    def log_error(cls, message):
        cls._instance.error(message)

    def log_critical(cls, message):
        cls._instance.critical(message)