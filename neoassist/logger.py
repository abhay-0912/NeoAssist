import logging

logging.basicConfig(
    filename="neoassist.log",
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("NeoAssist")