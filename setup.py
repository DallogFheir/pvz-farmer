from setuptools import setup

setup(
    name="pvz-farmer",
    version="1.0.0",
    description="Plants vs. Zombies farmer",
    author="DallogFheir",
    author_email="dallog.fheir@gmail.com",
    url="https://github.com/DallogFheir/pvz-farmer",
    packages=["pvz_farmer", "pvz_farmer.utils"],
    package_dir={"pvz_farmer": "src"},
    package_data={
        "pvz_farmer": [
            "imgs/*.png",
            "imgs/coins/*.png",
            "imgs/coins/gold_coins/*.png",
            "imgs/coins/silver_coins/*.png",
            "imgs/needs/*.png",
            "imgs/shop/*.png",
            "imgs/tools/*.png",
            "imgs/tree/*.png",
        ]
    },
    install_requires=["opencv-python~=4.5.1.48", "Pillow>=8.2,<9.1", "PyAutoGui~=0.9.52"],
)
