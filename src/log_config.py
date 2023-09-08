import logging


def setup_logging(log_level=logging.INFO, log_filename="app.log"):
    """
    Configures the logging module with custom settings.

    Args:
    - log_level (int): The logging level threshold. By default, it is set to logging.INFO.
    - log_filename (str): The name of the log file where logs should be written.
      Default is "app.log".

    This function sets up the logging to write logs both to the specified file
    and to the console. Before setting up, it resets any existing logging configuration.
    """
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