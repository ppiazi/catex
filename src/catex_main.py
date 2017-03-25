# -*- coding: utf-8 -*-
"""
Copyright 2015 Joohyun Lee(ppiazi@gmail.com)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import sys
import os
import getopt
import csv
import catex

__version__ = 'v0.0.1'

def print_usage():
    """
    사용법에 대한 내용을 콘솔에 출력한다.
    :return:
    """
    print("catex_main.py [-f files_name]")
    print("    Version %s" % __version__)
    print("    Options:")
    print("    -f : set target file")
    print("    -o : set output file")

class catex_main:
    def __init__(self):
        pass

    def __parse(self, row):
        in_file_start_line = 1
        in_file_ub = 0
        in_file_lb = 0

        try:
            temp_int = int(row[1])
            in_file_start_line = temp_int
        except Exception as e:
            print(str(e))
            in_file_start_line = 1

        try:
            temp_int = int(row[2])
            in_file_ub = temp_int
        except Exception as e:
            in_file_ub = 0

        try:
            temp_int = int(row[3])
            in_file_lb = temp_int
        except Exception as e:
            in_file_lb = 0

        return in_file_start_line, in_file_ub, in_file_lb

    def catex(self, file_name):
        self.result_db = []

        try:
            csv_file = open(file_name, "r", encoding='utf-8')
        except Exception as e:
            print(str(e))
            return

        csv_reader = csv.reader(csv_file)

        i = 0
        for row in csv_reader:
            in_file_name = ""
            in_file_start_line = 1
            in_file_ub = 0
            in_file_lb = 0

            # remove BOM from string
            try:
                in_file_name = row[0].replace(u'\ufeff', '')
            except Exception as e:
                print(str(e))
                in_file_name = row[0]

            if in_file_name == "":
                continue

            in_file_start_line, in_file_ub, in_file_lb = self.__parse(row)

            t_catex = catex.catex(in_file_name, in_file_start_line, in_file_ub, in_file_lb)
            t_key = "%s : %d %d %d" % (in_file_name, in_file_start_line, in_file_ub, in_file_lb)

            #print("(%d) Try to read : %s" % (i, t_key))
            ret = t_catex.catex()
            if ret != 0:
                print("Error to read %s" % (t_key))
                t_result = "File not found : %s" % (t_key)
            else:
                t_result = t_catex.get_code().strip()

            i = i + 1
            t_dic = {}
            t_dic["key"] = t_key
            t_dic["code"] = t_result

            self.result_db.append(t_dic)

    def save(self, output_file_name = ""):
        stdout = False
        stdout_str = ""
        if output_file_name == "":
            output_file_name = "output.csv"
            stdout = True

        try:
            output_csv = open(output_file_name, "w")
        except Exception as e:
            print(str(e))
            return 1

        writer = csv.writer(output_csv, lineterminator='\n')

        for t_item in self.result_db:
            t_list = []
            t_list.append(t_item["key"])
            t_list.append(t_item["code"])
            writer.writerow(t_list)

            if stdout == True:
                t_str = "%s\n%s\n\n" % (t_item["key"], t_item["code"])
                stdout_str = stdout_str + t_str

        output_csv.close()

        if stdout == True:
            print(stdout_str)


if __name__ == "__main__":
    optlist, args = getopt.getopt(sys.argv[1:], "f:o:")

    file_name = ""
    output_file_name = ""

    for op, p in optlist:
        if op == "-f":
            file_name = p
        elif op == "-o":
            output_file_name = p
        else:
            file_name = op
            print("Invalid Argument : %s / %s" % (op, p))

    if file_name == "":
        print_usage()
        os._exit(1)

    t_catex_main = catex_main()
    t_catex_main.catex(file_name)
    t_catex_main.save(output_file_name)
