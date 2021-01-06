import logging

def setup_logger(logger_name):
    logging.basicConfig(filemode='a', level=logging.INFO)

    logger = logging.getLogger(logger_name)
    logger.propagate = False
    
    i_handler = logging.FileHandler('logs/password_manager.log')
    e_handler = logging.FileHandler('logs/password_manager.log')
    i_handler.setLevel(logging.INFO)
    e_handler.setLevel(logging.ERROR)

    i_format = logging.Formatter(
        '%(asctime)s:%(name)s:%(lineno)d:%(levelname)s:%(message)s',
        datefmt='%d-%b-%y %H:%M:%S')
    e_format = logging.Formatter(
        '%(asctime)s:%(name)s:%(lineno)d:%(levelname)s:%(message)s',
        datefmt='%d-%b-%y %H:%M:%S')
    i_handler.setFormatter(i_format)
    e_handler.setFormatter(e_format)

    logger.addHandler(i_handler)
    logger.addHandler(e_handler)

    return logger