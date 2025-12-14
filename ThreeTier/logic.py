import re
import sys

from ThreeTier.data import LogData


class LogLogic:
    def __init__(self, data_access: LogData):
        self.data = data_access
        self._is_running = False
        self.ui = None

    def run(self):
        self._is_running = True
        while self._is_running:
            self.ui.run()

    def get_all(self):
        return self.data.read_all()

    def get_some(self, number_of_lines):
        if number_of_lines < 1:
            return "Invalid number of lines"

        lines = self.data.read_all_by_lines()
        group_lines = []
        now_group = ""
        counter = 1
        for line in lines:
            now_group += line

            if counter == number_of_lines:
                group_lines.append(now_group)
                now_group = ""
                counter = 0

            counter += 1

        if now_group != "":
            group_lines.append(now_group)

        return group_lines

    def get_line(self, line_number):
        if line_number < 1:
            return "Invalid line number"

        counter = 1
        for line in self.data.read_all_by_lines():
            if counter == line_number:
                return line
            counter += 1

        return "Line not found"

    def filter_category(self, category):
        if category == "":
            return "No category entered"
        lines = ""
        for line in self.data.read_all_by_lines():
            if re.match(fr'^{re.escape(category)}[\s\S]*', line):
                lines += line

        if len(lines) == 0:
            return "No logs found for that category."
        return lines

    def custom_filter(self, keyword):
        if keyword == "":
            return "No keyword entered"
        lines = ""
        for line in self.data.read_all_by_lines():
            if re.search(keyword, line):
                lines += line

        if len(lines) == 0:
            return "No logs found for this filter."

        return lines

    def get_categories(self):
        categories_list = []
        for line in self.data.read_all_parsed():
            category = line[0]
            if category not in categories_list:
                categories_list.append(category)

        ret_categories = ""
        for i in range(len(categories_list)):
            ret_categories += categories_list[i] + "\n"
        return ret_categories

    def get_statistics(self):
        category_stats = {}
        for line in self.data.read_all_parsed():
            category = line[0]
            if category not in category_stats.keys():
                category_stats[category] = 1
            else:
                category_stats[category] += 1

        ret_stats = ""
        for key, value in category_stats.items():
            ret_stats += f"{key}: {value} lines \n"
        return ret_stats

    def exit(self):
        self._is_running = False