from user_interface import UserInterface
from logic import LogLogic
from data import LogData, AppError

if __name__ == '__main__':
    try:
        data = LogData()
    except AppError() as e:
        print(f"Config error: {e}")
        exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        exit(2)

    logic = LogLogic(data)
    ui = UserInterface(logic)
    logic.ui = ui
    logic.run()