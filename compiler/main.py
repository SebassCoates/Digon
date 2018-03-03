import sys


def get_text(filename):
    with open(filename, "r") as fs:
        text = fs.read()

    return text;



filename = sys.argv[1]
text = get_text(filename)
print text

