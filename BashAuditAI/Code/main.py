from config.config_manager import ConfigManager
from ui.ui_main import App

def main():
    cfg = ConfigManager()
    cfg.load()  # yoksa default olusturur
    app = App(cfg)
    app.mainloop()

if __name__ == "__main__":
    main()
