# PyTestique - A Lightweight Python Testing Framework

> PyTestique is a lightweight testing framework for Python designed to simplify the process of writing and executing unit tests. It is meant for small to medium-sized projects and provides a simple and easy-to-use interface for writing and running tests. (https://github.com/C0DECYCLE/PyTestique)

## Key Features:
- Simplified test assertion
- Test timing
- Error handling
- Selective test execution with patterns
- Detailed console output

## Design Decisions:
Our group decided to try this task as professionally as we can, focusing on industry standard, having a clean GitHub repository and writing clean and scalable code. We started this by meeting up in person and writing our core structure of PyTestique on a whiteboard (Attachment: whiteboard_1.jpg and whiteboard_2.jpg; whiteboard_Pytestique_drawio.png is a more readable version of the whiteboard made with draw.io).

The main take-away in our structuring of the project was scalability and making it easy for the user to use. So we settled on a strong object-oriented approach. We also wanted every function to only focus on one thing to improve readability and scalability. We decided that Pytestique adds all tests, runtimes, states, etc. to separate dictionaries, which then get used in the executioner to return a coherent result for the user. We used this approach once more for scalability by easy interaction with the given data. We also added all of our PyTestique code in a separate file after asking the professor for allowance, as this is how the user would interact with PyTestique in a realistic situation.

The three of us had experience in Git, so we set up our GitHub repository under https://github.com/C0DECYCLE/PyTestique, settling on naming convention and workflow. We also opened up issues with things we wanted to implement (later we added more) and formed our Milestone. 

While working on the project, we realized it would be smart to form a separate PytestiqueUtils Class to insure, that utility functions are in a separate place. Once more for scalability and clean code.

We kept communicating throughout the process over discord and talking/meeting in person. On GitHub every pull request had to be approved by another member to reduce bugs and improve cleaner code.

In the end we didn't exactly adapt our structure form the whiteboard, but it gave us a good overview off the project. Final structure can be seen in the attachments under structure_Pytestique_end_drawio.png, created on draw.io.

## How to Use PyTestique:

1. Installation: PyTestique is a single Python source file. You can include it in your project by checking out the source file.

2. Writing Tests: To write tests, define functions that start with the prefix "test_". You can include setup and teardown functions by using the prefixes "setup_" and "teardown_", respectively. Use the provided assertion methods to check test conditions by using "PyTestiqueAsserts.".

3. Running Tests: Create an instance of PyTestique and pass your system argv and globals to it. You can also specify a test pattern to run a subset of tests by writting --select "pattern" in the command line.

5. Viewing Results: The test results will be printed to the console. You'll see which tests passed, which failed, and any errors that occurred during testing.

## Examples:

Here's an example of a simple test using PyTestique:

```
import sys
from PyTestique import PyTestique, PyTestiqueAsserts

def test_addition():
	addition = 1 + 1
	solution = 2
	PyTestiqueAsserts.assertEqual(addition, solution)

PyTestique(sys.argv, globals())
```

Run it in the command line:

`python example.py --select pattern`
