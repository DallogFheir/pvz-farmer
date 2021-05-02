from .utils.argparser import tree_parser
from .utils.exceptions import NoMoneyError
from .utils.logger import logger
from pathlib import Path
import pyautogui as pyag
from time import sleep


class ToWFarmer:
    def __init__(self, logger):
        path = Path(__file__).parent / "imgs"
        self.tree_path = path / "tree"
        self.shop_path = path / "shop"
        self.logger = logger

    def start(self):
        try:
            self.logger.info("started Tree of Wisdom farmer")
            self.tree = pyag.locateCenterOnScreen(str(self.tree_path / "tree.png"))
            if self.tree is None:
                self.logger.critical("couldn't locate tree, can't run")
                exit()
            self.logger.info("located tree")

            food = pyag.locateCenterOnScreen(str(self.tree_path / "food.png"))
            no_food = pyag.locateCenterOnScreen(str(self.tree_path / "no_food.png"))
            self.food = food if food is not None else no_food
            self.logger.info("located tree food")

            self.shop = pyag.locateCenterOnScreen(str(self.shop_path / "shop.png"))

            while True:
                self.feed_tree()
                sleep(2)
        except (pyag.FailSafeException, NoMoneyError):
            pass
        finally:
            self.logger.info("stopped Tree of Wisdom farmer")

    def feed_tree(self):
        no_food = pyag.locateCenterOnScreen(str(self.tree_path / "no_food.png"))
        if no_food is not None:
            self.logger.info("no tree food")
            self.buy_food()
            sleep(1)

        pyag.moveTo(self.food)
        pyag.click()
        pyag.moveTo(self.tree)
        pyag.click()
        self.logger.info("fed tree")

    def buy_food(self):
        pyag.moveTo(self.shop)
        pyag.click()
        sleep(1)
        food = pyag.locateCenterOnScreen(str(self.tree_path / "food_shop.png"))
        while True:
            sold_out = pyag.locateCenterOnScreen(
                str(self.tree_path / "food_sold_out.png")
            )
            if sold_out is not None:
                break

            pyag.click(food)
            sleep(0.5)

            no_money_ok = pyag.locateCenterOnScreen(str(self.shop_path / "ok.png"))
            if no_money_ok is not None:
                self.logger.info("out of money")
                pyag.moveTo(no_money_ok)
                pyag.click()
                go_back = pyag.locateCenterOnScreen(str(self.shop_path / "go_back.png"))
                pyag.moveTo(go_back)
                pyag.click()
                raise NoMoneyError

            yes = pyag.locateCenterOnScreen(str(self.shop_path / "yes.png"))
            pyag.moveTo(yes)
            pyag.click()
        self.logger.info("bought tree food")
        sleep(0.5)
        go_back = pyag.locateCenterOnScreen(str(self.shop_path / "go_back.png"))
        pyag.moveTo(go_back)
        pyag.click()


if __name__ == "__main__":
    args = vars(tree_parser.parse_args())
    logger.setLevel(args["log_level"])
    farmer = ToWFarmer(logger).start()
