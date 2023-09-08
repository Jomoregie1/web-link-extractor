import logging


def setup_logging(log_level=logging.INFO, log_filename="app.log"):
    # Reset logging configuration
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    logging.basicConfig(
        level=log_level,
        format='%(asctime)s [%(levelname)s]: %(message)s',
        handlers=[
            logging.FileHandler(log_filename),
            logging.StreamHandler()
        ]
    )