import logging

logger = logging.getLogger(__name__)
formatter = logging.Formatter("%(asctime)s : %(message)s", "%Y-%m-%d %H:%M:%S")
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)