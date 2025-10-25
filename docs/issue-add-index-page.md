### Problem

The `pretty_print_chat.py` script currently converts individual Gemini log files (`.json`) into separate HTML files. However, it does not create a central index page to easily browse all the generated logs.

The current workaround involves an external shell script that runs after the Python script to find all `.html` files and generate an `index.html`. This is inefficient and makes the tool less self-contained.

### Proposed Solution

Enhance the `pretty_print_chat.py` script to automatically generate an `index.html` file at the root of the log directory (`~/.gemini/tmp`).

**Implementation Details:**

1.  **Collect File Paths:** While the script is running, it should collect the paths of all the HTML files it generates.
2.  **Generate Index:** After all other files have been processed, the script should create a new `index.html` file.
3.  **Add Links:** This `index.html` should contain a list of HTML links pointing to each of the generated log files.
4.  **Styling:** The index page should have some basic, clean CSS for readability.

This change will make the script a complete, standalone tool for browsing Gemini logs.
