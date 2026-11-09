"""Focused regression tests for viewer core behaviour.

Run on Windows: python -m unittest discover -s tests -p "test_core_regressions.py"
These tests exercise extracted methods without creating a Qt window.
"""
import ast
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

SOURCE = Path(__file__).resolve().parents[1] / "app.py"
TREE = ast.parse(SOURCE.read_text(encoding="utf-8"))
VIEWER = next(n for n in TREE.body if isinstance(n, ast.ClassDef) and n.name == "PhotoViewer")


def method(name, namespace=None):
    node = next(n for n in VIEWER.body if isinstance(n, ast.FunctionDef) and n.name == name)
    module = ast.Module(body=[node], type_ignores=[])
    ast.fix_missing_locations(module)
    env = dict(namespace or {})
    exec(compile(module, str(SOURCE), "exec"), env)
    return env[name]


class FakePixmap:
    def __init__(self, width=100, height=100, depth=32):
        self.w, self.h, self.bits = width, height, depth
        self.saved_to = None

    def width(self): return self.w
    def height(self): return self.h
    def depth(self): return self.bits

    def save(self, path):
        self.saved_to = path
        return True


class ViewerRegressionTests(unittest.TestCase):
    def test_cache_memory_limit(self):
        trim = method("_trim_image_cache")
        viewer = SimpleNamespace(image_cache={
            "one": FakePixmap(4000, 4000),
            "two": FakePixmap(4000, 4000),
            "three": FakePixmap(4000, 4000),
        })
        trim(viewer)
        self.assertEqual(list(viewer.image_cache), ["two", "three"])

    def test_empty_folder_preserves_current_photo(self):
        msg = SimpleNamespace(information=lambda *_: None, warning=lambda *_: None)
        load = method("load_directory", {
            "SUPPORTED": {".jpg"}, "QMessageBox": msg, "APP_NAME": "Test"
        })
        with tempfile.TemporaryDirectory() as directory:
            viewer = SimpleNamespace(
                files=[Path("existing.jpg")], index=0,
                image_cache={"old": object()}
            )
            load(viewer, Path(directory))
            self.assertEqual(viewer.files, [Path("existing.jpg")])
            self.assertEqual(viewer.index, 0)
            self.assertIn("old", viewer.image_cache)

    def test_save_copy_includes_rotation(self):
        pix = FakePixmap()
        chooser = SimpleNamespace(getSaveFileName=lambda *_: ("rotated.png", "PNG"))
        messages = SimpleNamespace(information=lambda *_: None, warning=lambda *_: None)
        save = method("save_copy", {"QFileDialog": chooser, "QMessageBox": messages})
        viewer = SimpleNamespace(
            current_pixmap=FakePixmap(), transformed_pixmap=lambda: pix,
            statusBar=lambda: SimpleNamespace(showMessage=lambda *_: None)
        )
        save(viewer)
        self.assertEqual(pix.saved_to, "rotated.png")
        self.assertIsNone(viewer.current_pixmap.saved_to)

    def test_no_transform_if_not_rotated(self):
        original = object()
        transform = method("transformed_pixmap")
        self.assertIs(transform(SimpleNamespace(current_pixmap=original, rotation=0)), original)


if __name__ == "__main__":
    unittest.main()
