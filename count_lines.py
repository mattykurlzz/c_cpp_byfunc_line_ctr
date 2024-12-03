import os
import re
import subprocess

folder_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "BSOProgrammer")

os.chdir(folder_path)


def extract_functions(file_path):
    start_line, end_line, line_ctr, par_ctr = 0, 0, -1, 0
    func_started = False
    func_name = ""
    with open(file_path, "rb") as f:
        contents = f.readlines()
        for line in contents:
            line_ctr += 1
            if re.search("^((([a-zA-Z0-9_]* )?[a-zA-Z0-9_]+)|([a-zA-Z0-9_ ]*[a-zA-Z0-9_]+::[a-zA-Z0-9_]+)) *\([A-Za-z0-9_ ,&(\*)]*(\) *{?)?\r?\n$", line.decode()):
                func_started = True
                print(line)
                func_name = re.search("([A-Za-z0-9_]+ )*[A-Za-z0-9_]+(\(|:)", line.decode()).string.split('(')[0].split(' ')[-1] #re.findall("[a-z_]+ ?\(.*\) {\r\n$", line.decode())[0].split('(')[0]
                print(func_name + " found on " + str(line_ctr))
                start_line = line_ctr
            if func_started and re.search("{", line.decode()):
                par_ctr += re.findall("{", line.decode()).__len__()
            if func_started and re.search("}", line.decode()):
                par_ctr -= re.findall("}", line.decode()).__len__()
                if par_ctr == 0:
                    print("func ended on " + str(line_ctr))
                    end_line = line_ctr
                    func_started = False
                    if(not os.path.isdir(os.path.join(folder_path, "tmp"))):
                        subprocess.run(["mkdir",  "tmp"])
                    with open(
                        os.path.join(folder_path, "tmp" , os.path.splitext(os.path.basename(file_path))[0]+ '---' + func_name + ".cpp"), "wb"
                    ) as tmp_file:
                        print(tmp_file.name)
                        tmp_file.writelines(contents[start_line : end_line + 1])


for file in os.listdir(folder_path):
    if file.endswith(".c") or file.endswith(".cpp"):
        file_path = os.path.join(folder_path, file)
        file_name = file_path.split(os.sep)[-1]
        extract_functions(file_path)
subprocess.run(["cloc",  "--out=report.txt", "--by-file", folder_path + "/tmp/"])

for file in os.listdir(os.path.join(folder_path, "tmp")):
    os.remove(os.path.join(folder_path, "tmp", file))
os.rmdir(os.path.join(folder_path, "tmp"))
