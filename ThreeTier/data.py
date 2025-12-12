import configparser
import os
import re


class AppError(Exception):
    pass

class LogData:
    def __init__(self):
        self.filepath = self.load_config()

    def read_all(self):
        with open(self.filepath, 'r') as file:
            return file.read()

    def read_all_by_lines(self):
        lines = []
        with open(self.filepath, 'r') as file:
            for line in file:
                lines.append(line)
        return lines

    def read_all_parsed(self):
        lines_parsed = []
        with open(self.filepath, 'r') as file:
            for line in file:
                lines_parsed.append(line.split(" "))

        return lines_parsed

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