import os
import re
import sys
import configparser

class AppError(Exception):
    pass

class App:

    def __init__(self):
        self.log_path = self.load_config()
        self.actions = {
            1: self.show_all,
            2: self.show_category,
            3: self.show_filter,
            4: self.show_by_some,
            5: self.show_line,
            6: self.categories,
            7: self.statistics,
            8: self.exit
        }

    def run(self):
        print("Welcome to log analyser")
        while True:
            print(self.show_menu())
            choice = int(input("Enter your choice:"))
            if choice not in self.actions.keys():
                print("Invalid choice.")
                break
            gen = self.actions[choice]()
            item = next(gen)

            while True:
                try:
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
                except AppError as e:
                    print(f"Error: {e}")

    def show_all(self):
        with open(self.log_path, 'r') as file:
            yield file.read()
            a = yield "Press enter to continue:"

    def show_category(self):
        category = yield "Enter category of logs you want to see:"
        if category == "":
            raise AppError("No category entered.")
        with open(self.log_path, 'r') as file:
            category_lines = "\n"
            for line in file:
                if re.match(fr'^{re.escape(category)}[\s\S]*',line):
                    category_lines += line

            if category_lines == "\n":
                yield "No logs found for that category."
            else:
                yield category_lines
                a = yield "Press enter to continue:"

    def show_filter(self):
        filter = yield f"Enter filter for which you want to search:"
        if filter == "":
            raise AppError("No filter entered.")
        with open(self.log_path, 'r') as file:
            filter_lines = "\n"
            for line in file:
                if re.search(filter,line):
                    filter_lines += line

            if filter_lines == "\n":
                yield "No logs found for that category."
            else:
                yield filter_lines
                a = yield "Press enter to continue:"

    def show_by_some(self):
        how_many = yield "How many lines at once do you want to see:"
        try:
            how_many = int(how_many)
            if how_many <= 0:
                raise ValueError()
        except ValueError:
            raise AppError("Invalid number of lines, enter a valid number.")
        with open(self.log_path, 'r') as file:
            counter = 1
            now_lines = "\n"
            for line in file:
                now_lines += line
                counter += 1
                if counter > how_many:
                    yield now_lines
                    a = yield "Press enter to continue:"
                    now_lines = ""
                    counter = 1
            if now_lines != "":
                yield now_lines
                a = yield "Press enter to continue:"

    def show_line(self):
        line_number = yield "Enter line number:"
        try:
            line_number = int(line_number)
            if line_number < 1:
                raise ValueError()
        except ValueError:
            raise AppError("Invalid line number, enter a valid number.")

        with open(self.log_path, 'r') as file:
            count = 1
            for line in file:
                if count == line_number:
                    yield line
                    a = yield "Press enter to continue:"
                    break
                count += 1

    def categories(self):
        categories_list = []
        with open(self.log_path, 'r') as file:
            for line in file:
                category = line.split(" ")[0]
                if category not in categories_list:
                    categories_list.append(category)
        if len(categories_list) == 0:
            yield "No categories found."
        else:
            yield "\n".join(categories_list)
            a = yield "Press enter to continue:"

    def statistics(self):
        category_dict = {}
        with open(self.log_path, 'r') as file:
            for line in file:
                category = line.split(" ")[0]
                if category not in category_dict.keys():
                    category_dict[category] = 1
                else:
                    category_dict[category] += 1

        pretty_print = "\n"
        for key in category_dict.keys():
            pretty_print += f"{key}: {category_dict[key]} lines \n"

        if pretty_print == "\n":
            yield "No statistics found."
        else:
            yield pretty_print
            a = yield "Press enter to continue:"

    def show_menu(self):
        menu_str = ""
        for key, value in self.actions.items():
            menu_str += f"{key}. {value.__name__}\n"
        return menu_str

    def exit(self):
        sys.exit(0)

    def load_config(self, path="config.ini"):
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