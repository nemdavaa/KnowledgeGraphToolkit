import logging

class LoggingConfig:
    @staticmethod
    def setup(logger_name):
        formatter = logging.Formatter(
            fmt=f"%(asctime)s - %(levelname)s - [{logger_name}] - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        handler = logging.StreamHandler()
        handler.setFormatter(formatter)

        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.INFO)
        logger.addHandler(handler)
        logger.propagate = False  # Prevent duplicate logs

        return logger