import unittest

from pydantic import ValidationError

from models import Task


class TestTask(unittest.TestCase):
    def test_create_valid_task(self):
        task = Task(id=1, title="学习 Python")

        self.assertEqual(task.id, 1)
        self.assertEqual(task.title, "学习 Python")
        self.assertFalse(task.completed)

    def test_empty_title_should_fail(self):
        with self.assertRaises(ValidationError):
            Task(id=1, title="")


if __name__ == "__main__":
    unittest.main()