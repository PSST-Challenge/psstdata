import logging

import psstdata

logger = logging.getLogger(psstdata.__name__)

formatter = logging.Formatter('%(name)s %(levelname)s: %(message)s')
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)