import logging


def setup_logging(log_level=logging.INFO, log_filename="app.log"):
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s [%(levelname)s]: %(message)s',
        handlers=[
            logging.FileHandler(log_filename),
            logging.StreamHandler()
        ]
    )
