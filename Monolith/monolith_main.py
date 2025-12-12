from Monolith.app import App, AppError

if __name__ == "__main__":
    try:
        application = App()
    except AppError as e:
        print("Configuration error:", e)
        exit(1)
    except Exception as e:
        print("Unexpected error:", e)
        exit(2)

    application.run()