import logging

logger = logging.getLogger("MeteoLogger")
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler(filename='meteo.log', encoding='utf-8', mode='w')
file_handler.setLevel(logging.INFO)

file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_format)

logger.addHandler(file_handler)