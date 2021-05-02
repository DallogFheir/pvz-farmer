from argparse import ArgumentParser


class ArgParserWithLog(ArgumentParser):
    def __init__(self):
        super().__init__()
        self.add_argument(
            "-l",
            "--log-level",
            type=str,
            default="INFO",
            choices=("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"),
            help="set logging level",
        )


class ArgParserWithLogAndFrames(ArgParserWithLog):
    def __init__(self):
        super().__init__()
        self.add_argument(
            "frames",
            type=int,
            help="set how many frames should be dedicated to coin picking",
        )


zen_parser = ArgParserWithLogAndFrames()
tree_parser = ArgParserWithLog()
farmer_parser = ArgParserWithLogAndFrames()
farmer_parser.add_argument(
    "zen-garden",
    type=int,
    help="set how many loops of Zen Garden farming before switching to the Tree of Wisdom farming",
)
