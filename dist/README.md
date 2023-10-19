PyTestique - A Lightweight Python Testing Framework (https://github.com/C0DECYCLE/PyTestique)

PyTestique is a lightweight testing framework for Python designed to simplify the process of writing and executing unit tests. It is meant for small to medium-sized projects and provides a simple and easy-to-use interface for writing and running tests.

Key Features:
- Simplified Test Assertion
- Test Timing
- Error Handling
- Customizable Test Execution

Design Decisions:
Our group decided to try this task as professionally as we can, focusing on industry standard, having a clean github repository and writting clean and scalable code. We started this by meeting up in person and writting our core structure of PyTestique on a whiteboard (Attachment: whiteboard_1.jpg and whiteboard_2.jpg; whiteboard_Pytestique_drawio.png is a more readable version of the whiteboard made with draw.io).

In the end we didn't exactly adapt our strcture form the whiteboard, final version can be seen in the attachments under structure_Pytestique_end_drawio.png, created on draw.io.


How to Use PyTestique:

1. Installation: PyTestique is a single Python source file. You can include it in your project by copying and pasting the source code or by importing it as a module.

2. Writing Tests: To write tests, define functions that start with the prefix "test_". You can include setup and teardown functions by using the prefixes "setup_" and "teardown_", respectively. Use the provided assertion methods to check test conditions by using "PyTestiqueAsserts.".

3. Running Tests: Create an instance of PyTestique and pass your test functions and global context to it. You can also specify a test pattern to run a subset of tests by writting --select ""pattern"" after calling the file.

4. Viewing Results: The test results will be printed to the console. You'll see which tests passed, which failed, and any errors that occurred during testing.

Examples:

Here's an example of a simple test using PyTestique:

	from pytestique import PyTestique

	def test_addition():
		addition = 1 + 1
		solution = 2
		PyTestiqueAsserts.assertEqual(addition, solution)
	
	if name == "main":
		PyTestique(sys.argv, globals())


Contributing: PyTestique is open-source, and contributions are welcome. If you'd like to add new features, improve existing functionality, or fix bugs, feel free to submit pull requests on the project's repository.

License: See the LICENSE file for more details.

Conclusion: PyTestique is a simple and lightweight testing framework for Python that aims to make the testing process straightforward and easy to understand. It's a great choice for projects where you want to write tests without the complexity of a full-fledged testing suite. Give it a try, and let us know how it works for your testing needs!

