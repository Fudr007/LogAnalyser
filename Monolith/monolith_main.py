from Monolith.app import App

if __name__ == "__main__":
    try:
        cfg = App.load_config()
    except Exception as e:
        print("Configuration error:", e)
        exit(1)

    application = App(cfg)
    application.run()