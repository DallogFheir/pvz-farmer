from .utils.argparser import zen_parser
import cv2
from .utils.logger import logger
import numpy as np
from pathlib import Path
from PIL import ImageGrab
import pyautogui as pyag
from time import sleep


class ZenGardenFarmer:
    def __init__(self, frames, logger):
        self.logger = logger
        self.frames_for_coins = frames
        self.path = Path(__file__).parent / "imgs"

    def start(self, loops=float("inf")):
        try:
            self.logger.info("started Zen Garden farmer")

            self.locate_tools()
            if "water" not in self.tools:
                self.logger.critical("couldn't locate water, can't run")
                exit()

            self.shop = pyag.locateCenterOnScreen(str(self.path / "shop" / "shop.png"))

            i = 0
            while i < loops:
                self.satisfy_needs()
                self.pick_up_coins()
                i += 1
        except pyag.FailSafeException:
            pass
        finally:
            self.logger.info("stopped Zen Farmer")

    def locate_tools(self):
        tools = {}

        for tool in (self.path / "tools").iterdir():
            tool_name = tool.stem.rstrip("1").rstrip("2")

            coords = pyag.locateCenterOnScreen(str(tool))

            if coords is not None:
                tools[tool_name] = coords
                self.logger.info("located " + tool_name)

                if tool_name == "water":
                    self.no_click_zone = coords.y + 50
            else:
                self.logger.debug("failed to locate " + tool_name)

        self.tools = tools

    def satisfy_needs(self):
        for need in (self.path / "needs").iterdir():
            need_name = need.stem

            need_locs = list(pyag.locateAllOnScreen(str(need)))

            if len(need_locs) != 0:
                self.logger.info(
                    "located "
                    + str(len(need_locs))
                    + " instances of need of "
                    + need_name
                )

                if need_name in ("spray", "fertilizer"):
                    no_tool = pyag.locateOnScreen(
                        str(self.path / "tools" / f"{need_name}2.png")
                    )

                    if no_tool is not None and self.shop is not None:
                        self.logger.info("no " + need_name)
                        pyag.moveTo(self.shop)
                        pyag.click()
                        sleep(1)
                        tool = pyag.locateCenterOnScreen(
                            str(self.path / "shop" / f"{need_name}.png")
                        )
                        pyag.click(tool)
                        sleep(0.5)

                        no_money_ok = pyag.locateCenterOnScreen(
                            str(self.path / "shop" / "ok.png")
                        )
                        if no_money_ok is not None:
                            self.logger.info("out of money")
                            pyag.moveTo(no_money_ok)
                            pyag.click()
                            go_back = pyag.locateCenterOnScreen(
                                str(self.path / "shop" / "go_back.png")
                            )
                            pyag.moveTo(go_back)
                            pyag.click()
                            break

                        yes = pyag.locateCenterOnScreen(
                            str(self.path / "shop" / "yes.png")
                        )
                        pyag.moveTo(yes)
                        pyag.click()
                        self.logger.info("bought " + need_name)
                        sleep(0.5)
                        go_back = pyag.locateCenterOnScreen(
                            str(self.path / "shop" / "go_back.png")
                        )
                        pyag.moveTo(go_back)
                        pyag.click()

                for need_loc in need_locs:
                    click_x = need_loc.left - 35
                    click_y = need_loc.top + 30

                    if need_name in self.tools:
                        tool = self.tools[need_name]

                        pyag.click(tool)
                        pyag.moveTo(x=click_x, y=click_y)
                        pyag.click()

                if need_name in self.tools:
                    self.logger.info("satisfied needs for " + need_name)
                else:
                    self.logger.debug("couldn't satisfy needs for " + need_name)

    def pick_up_coins(self):
        templates = {
            "silver": [
                cv2.imread(str(path))
                for path in (self.path / "coins" / "silver_coins").iterdir()
            ],
            "gold": [
                cv2.imread(str(path))
                for path in (self.path / "coins" / "gold_coins").iterdir()
            ],
        }

        for i in range(self.frames_for_coins):
            self.logger.info(f"picking up coins - frame {i+1}")

            frame = cv2.cvtColor(np.array(ImageGrab.grab()), cv2.COLOR_RGB2BGR)

            hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            silver_mask = cv2.inRange(hsv_frame, (0, 0, 120), (1, 1, 255))
            gold_mask = cv2.inRange(hsv_frame, (20, 70, 100), (30, 255, 255))

            masked_frames = {
                "silver": cv2.bitwise_and(frame, frame, mask=silver_mask),
                "gold": cv2.bitwise_and(frame, frame, mask=gold_mask),
            }

            for coin, threshold, color in (
                ("silver", 0.8, (0, 0, 255)),
                ("gold", 0.8, (255, 0, 0)),
            ):
                for template in templates[coin]:
                    width, height, _ = template.shape

                    matches = cv2.matchTemplate(
                        masked_frames[coin], template, cv2.TM_CCOEFF_NORMED
                    )
                    res = np.where(matches >= threshold)

                    locs = list(zip(*res[::-1])) * 2
                    rects_to_group = [
                        (
                            int(loc[0]),
                            int(loc[1]),
                            width,
                            height,
                        )
                        for loc in locs
                    ]
                    rects, _ = cv2.groupRectangles(rects_to_group, 1, 0.8)

                    if len(rects) != 0:
                        for x, y, w, h in rects:
                            click_x = x + w // 2
                            click_y = y + h // 2
                            if click_y > self.no_click_zone:
                                pyag.moveTo(click_x, click_y)
                                pyag.click()
                                self.logger.debug(f"tried to pick up {coin} coin")

                diamond = pyag.locateCenterOnScreen(
                    str(self.path / "coins" / "diamond.png")
                )
                if diamond is not None:
                    pyag.moveTo(diamond)
                    pyag.click()
                    self.logger.debug("tried to pick up diamond")


if __name__ == "__main__":
    args = vars(zen_parser.parse_args())
    logger.setLevel(args["log_level"])
    farmer = ZenGardenFarmer(args["frames"], logger).start()
