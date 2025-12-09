import os
import re
import sys
import configparser

class AppError(Exception):
    pass

class App:

    def __init__(self, log_path):
        self.log_path = log_path
        self.actions = {
            1: self.show_all,
            2: self.show_category,
            3: self.show_filter,
            4: self.show_some,
            5: self.exit
        }

    def run(self):
        print("Welcome to log analyser")
        while True:
            print(self.show_menu())
            choice = int(input("Enter your choice:"))

            gen = self.actions[choice]()
            item = next(gen)

            while True:
                print(item)

                if type(item) is str and item.endswith(":"):
                    user_input = input()
                    try:
                        item = gen.send(user_input)
                    except StopIteration:
                        break
                else:
                    try:
                        item = next(gen)
                    except StopIteration:
                        break

    def show_all(self):
        with open(self.log_path, 'r') as file:
            yield file.read()

    def show_category(self):
        category = yield "Enter category of logs you want to see:"
        with open(self.log_path, 'r') as file:
            category_lines = str
            for line in file:
                if re.match(fr'^{re.escape(category)}\S',line):
                    category_lines += line + '\n'

            if category_lines == str:
                return "No logs found for that category."
            else:
                return category_lines


    def show_filter(self, what):
        pass

    def show_some(self, how_many):
        pass

    def show_menu(self):
        menu_str = ""
        for key, value in self.actions.items():
            menu_str += f"{key}. {value.__name__}\n"
        return menu_str

    def exit(self):
        sys.exit(0)

    @staticmethod
    def load_config(path="config.ini"):
        if not os.path.isfile(path):
            raise AppError(f"Config file '{path}' not found.")

        config = configparser.ConfigParser()
        config.read(path)
        log_file_path=config['DEFAULT']['log_path']

        if log_file_path == "":
            raise AppError("Log file path not found in config file. Please check the config file (default is config.ini) file.")
        if not re.match(r'.+\.txt$',log_file_path):
            raise AppError("Log file have to be a text file.")

        return log_file_path