import os
import re
import subprocess

folder_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "BSOProgrammer")

os.chdir(folder_path)


def extract_functions(file_path):
    with open(file_path, "r") as f:
        contents = f.read()
        contents = set(
            re.findall(
                r"("
                + "(?:[a-zA-Z0-9_:&]+ )*"
                + "(?:[\w*&]+ )?"
                + "(?:\w*::)?"
                + "[\w<>=+-]+"
                + "\("
                + "(?:\n?[ \t]*[\w,:&\* ]+ [\w,:&\*\[\]]+(?: *//.*)?[ \t]*\n?)*"
                + " *\)"
                + " *(?:\s*: \w+\([\w \(\)]+\) ?)?(?: *//.*)?\n?"
                + "(?:\r?\n ?)?"
                + "\{"
                + "(?:(?:\n(?:\n?[\s]+.+\n)*)|(?:[\s]*\n)|(?:[^\}]+))*"
                + "\}"
                + ")",
                contents,
            )
        )
        # print(contents)
        wordsmem = []
        for fun in contents:
            # print(fun)
            head = fun.split("\n")[0]
            name = ""
            for word in head.split(" "):
                if re.search("\(", word):
                    name = word.split("(")[0]
                    ctr = 1
                    append = ""
                    while name + append in wordsmem:
                        append = "_" + str(ctr)
                        ctr += 1
                    name += append
                    wordsmem.append(name)
                    break
            with open(
                os.path.join(
                    folder_path,
                    "tmp",
                    os.path.splitext(os.path.basename(file_path))[0]
                    + "---"
                    + name
                    + ".cpp",
                ),
                "w",
            ) as tmp_file:
                tmp_file.writelines(fun)
            print(name)


if not os.path.isdir(os.path.join(folder_path, "tmp")):
    subprocess.run(["mkdir", "tmp"])

for file in os.listdir(folder_path):
    if file.endswith(".c") or file.endswith(".cpp"):
        file_path = os.path.join(folder_path, file)
        file_name = file_path.split(os.sep)[-1]
        extract_functions(file_path)
subprocess.run(["cloc", "--out=report.txt", "--by-file", folder_path + "/tmp/"])

for file in os.listdir(os.path.join(folder_path, "tmp")):
    os.remove(os.path.join(folder_path, "tmp", file))
os.rmdir(os.path.join(folder_path, "tmp"))
