IDENTICAL = -1


def singleline_diff(line1, line2):
    """
    Inputs:
      line1 - first single line string
      line2 - second single line string
    Output:
      Returns the index where the first difference between 
      line1 and line2 occurs.

      Returns IDENTICAL if the two lines are the same.
    """
    if line1 == line2:
        return IDENTICAL
    else:
        for num in range(0, min(len(line1), len(line2))):
            if line1[num] != line2[num]:
                return num
        return min(len(line1), len(line2))


def singleline_diff_format(line1, line2, idx):
    """
    Inputs:
      line1 - first single line string
      line2 - second single line string
      idx   - index at which to indicate difference
    Output:
      Returns a three line formatted string showing the location
      of the first difference between line1 and line2.

      If either input line contains a newline or carriage return,
      then returns an empty string.

      If idx is not a valid index, then returns an empty string.
    """
    indicate = ""
    if idx == IDENTICAL:
        return indicate
    if 0 <= idx <= min(len(line1), len(line2)):
        for index in range(0, idx + 1):
            if index == idx:
                indicate = indicate + "^"
            else:
                indicate = indicate + "="
        return line1 + "\n" + indicate + "\n" + line2 + "\n"
    else:
        return indicate


def multiline_diff(lines1, lines2):
    """
        Inputs:
          lines1 - list of single line strings
          lines2 - list of single line strings
        Output:
          Returns a tuple containing the line number (starting from 0) and
          the index in that line where the first difference between lines1
          and lines2 occurs.

          Returns (IDENTICAL, IDENTICAL) if the two lists are the same.
    """
    length = len(lines1) - len(lines2)
    for index in range(0, min(len(lines1), len(lines2))):
        diff = singleline_diff(lines1[index], lines2[index])
        if diff != IDENTICAL:
            return index, diff
    if length > 0:
        return len(lines2), 0
    elif length < 0:
        return len(lines1), 0
    else:
        return IDENTICAL, IDENTICAL


def get_file_lines(filename):
    """
    Inputs:
      filename - name of file to read
    Output:
      Returns a list of lines from the file named filename.  Each
      line will be a single line string with no newline ('\n') or
      return ('\r') characters.

      If the file does not exist or is not readable, then the
      behavior of this function is undefined.
    """
    with open(filename, "r") as file:
        content = file.readlines()
    for index in range(0, len(content)):
        if content[index] != "\n":
            content[index] = content[index].rstrip()
    return content


def file_diff_format(filename1, filename2):
    """
    Inputs:
      filename1 - name of first file
      filename2 - name of second file
    Output:
      Returns a four line string showing the location of the first
      difference between the two files named by the inputs.

      If the files are identical, the function instead returns the
      string "No differences\n".

      If either file does not exist or is not readable, then the
      behavior of this function is undefined.
    """
    file1 = get_file_lines(filename1)
    file2 = get_file_lines(filename2)
    if "\n" in file1:
        file1.remove("\n")
    if "\n" in file2:
        file2.remove("\n")
    diff = tuple(multiline_diff(file1, file2))
    if diff == (IDENTICAL, IDENTICAL):
        return "No differences\n"
    else:
        if len(file1) != 0 and len(file2) != 0:
            return "Line " + str(diff[0]) + ":\n" + \
                singleline_diff_format(file1[diff[0]], file2[diff[0]], diff[1])
        elif len(file1) == 0:
            return "Line " + str(diff[0]) + ":\n" + \
                singleline_diff_format("", file2[diff[0]], diff[1])
        else:
            return "Line " + str(diff[0]) + ":\n" + \
                singleline_diff_format(file1[diff[0]], "", diff[1])
# print(file_diff_format("abc.txt", "efg.txt"))