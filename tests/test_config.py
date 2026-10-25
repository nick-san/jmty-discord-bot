import unittest
from pathlib import Path
from src.config import load_yaml


class TestConfig(unittest.TestCase):
    def test_load_car_parts_config(self):
        config = load_yaml("car_parts.yaml")
        self.assertIn("targets", config)
        targets = config["targets"]
        self.assertGreater(len(targets), 0)
        target = targets[0]
        self.assertIn("name", target)
        self.assertIn("url", target)
        self.assertIn("webhook_env", target)

    def test_load_cars_hokkaido_config(self):
        config = load_yaml("cars_hokkaido.yaml")
        self.assertIn("webhook_env", config)
        self.assertIn("urls", config)
        self.assertIn("keywords", config)
        self.assertIn("MT", config["keywords"])

    def test_load_non_existent_file(self):
        with self.assertRaises(FileNotFoundError):
            load_yaml("non_existent_file.yaml")


if __name__ == "__main__":
    unittest.main()
