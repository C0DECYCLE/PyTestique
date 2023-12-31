import os
import sys
from PyTestique import PyTestique, PyTestiqueAsserts
from file_manager import read_file, create_file, delete_file


#################### read file tests #########################


def test_read_file_not_exist():
    file_name = "test_file_read_text.txt"
    PyTestiqueAsserts.assertIsNone(read_file(file_name))


def setup_read_file_content():
    file_name = "test_file_read_content.txt"
    file_content = "This is a test file."
    with open(file_name, "w") as file:
        file.write(file_content)


def test_read_file_content():
    file_name = "test_file_read_content.txt"
    file_content = "This is a test file."
    PyTestiqueAsserts.assertEqual(file_content, read_file(file_name))


def teardown_read_file_content():
    file_name = "test_file_read_content.txt"
    if os.path.exists(file_name):
        os.remove(file_name)


#################### create file tests #########################


def test_create_file_true():
    file_name = "test_file_create.txt"
    result = create_file(file_name)
    PyTestiqueAsserts.assertTrue(os.path.exists(file_name))
    PyTestiqueAsserts.assertTrue(result)


def teardown_create_file_true():
    file_name = "test_file_create.txt"
    if os.path.exists(file_name):
        os.remove(file_name)


def test_create_file_content():
    file_name = "test_file_create_content.txt"
    file_content = "I have created a file"
    create_file(file_name, file_content)
    PyTestiqueAsserts.assertTrue(os.path.exists(file_name))
    with open(file_name, "r") as file:
        PyTestiqueAsserts.assertEqual(file.read(), file_content)


def teardown_create_file_content():
    file_name = "test_file_create_content.txt"
    if os.path.exists(file_name):
        os.remove(file_name)


#################### delete file tests #########################


def setup_delete_file_exist():
    file_name = "test_file_delete_exist.txt"
    file_content = "This is a test file."
    with open(file_name, "w") as file:
        file.write(file_content)


def test_delete_file_exist():
    file_name = "test_file_delete_exist.txt"
    result = delete_file(file_name)
    PyTestiqueAsserts.assertFalse(os.path.exists(file_name))
    PyTestiqueAsserts.assertTrue(result)


def teardown_delete_file_exist():
    file_name = "test_file_delete_exist.txt"
    if os.path.exists(file_name):
        os.remove(file_name)


def test_delete_file_not_exist():
    file_name = "test_file_delete_not_exist.txt"
    result = delete_file(file_name)
    PyTestiqueAsserts.assertFalse(os.path.exists(file_name))
    PyTestiqueAsserts.assertFalse(result)


PyTestique(sys.argv, globals())
