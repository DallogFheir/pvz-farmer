from .utils.argparser import farmer_parser
from .utils.logger import logger
from pathlib import Path
import pyautogui as pyag
from time import sleep
from .tow_farmer import ToWFarmer
from .zen_farmer import ZenGardenFarmer

if __name__ == "__main__":
    try:
        path = Path(__file__).parent / "imgs"

        arrow = pyag.locateCenterOnScreen(str(path / "arrow.png"))

        args = vars(farmer_parser.parse_args())
        logger.setLevel(args["log_level"])
        zen_farmer = ZenGardenFarmer(args["frames"], logger)
        tree_of_wisdom_farmer = ToWFarmer(logger)

        logger.info("started script")

        while True:
            zen_farmer.start(args["zen-garden"])
            pyag.moveTo(arrow)
            pyag.click()
            pyag.click()
            pyag.click()
            sleep(1)
            tree_of_wisdom_farmer.start()
            pyag.moveTo(arrow)
            pyag.click()
    except pyag.FailSafeException:
        logger.info("ended script")
