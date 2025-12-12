from ThreeTier.logic import LogLogic
from data import AppError

class UserInterface:

    def __init__(self, logic:LogLogic):
        self.logic = logic
        self.menu = {
            1: self.print_all,
            2: self.print_by_some,
            3: self.print_category,
            4: self.print_categories,
            5: self.print_statistics,
            6: self.print_filtered,
            7: self.print_line,
            8: self.call_exit
        }

    def run(self):
        print("Welcome to log analyser")
        while True:
            print(self.print_menu())
            choice = int(input("Enter your choice:"))
            if choice not in self.menu.keys():
                print("Invalid choice.")
                break
            try:
                gen = self.menu[choice]()
                item = next(gen)
            except Exception as e:
                print("Wrong input.")
                break

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

    def print_all(self):
        yield self.logic.get_all()
        a = yield "Press enter to continue:"

    def print_by_some(self):
        how_many = yield "How many lines at once do you want to see:"
        try:
            how_many = int(how_many)
        except ValueError:
            raise AppError("Number of lines must be a number.")

        grouped_lines = self.logic.get_some(how_many)
        for lines in grouped_lines:
            yield lines
            a = yield "Press enter to continue:"

    def print_category(self):
        category = yield "Enter category of logs you want to see:"
        yield self.logic.filter_category(category)
        a = yield "Press enter to continue:"

    def print_categories(self):
        yield self.logic.get_categories()
        a = yield "Press enter to continue:"

    def print_statistics(self):
        yield self.logic.get_statistics()
        a = yield "Press enter to continue:"

    def print_filtered(self):
        filtered = yield "Enter keyword to filter logs:"
        yield self.logic.custom_filter(filtered)
        a = yield "Press enter to continue:"

    def print_line(self):
        line_number = yield "Enter line number:"
        try:
            line_number = int(line_number)
        except ValueError:
            raise AppError("Number of line must be a number.")
        yield self.logic.get_line(line_number)
        a = yield "Press enter to continue:"

    def print_menu(self):
        menu_str = ""
        for key, value in self.menu.items():
            menu_str += f"{key}. {value.__name__}\n"
        return menu_str

    def call_exit(self):
        print("Goodbye!")
        self.logic.exit()