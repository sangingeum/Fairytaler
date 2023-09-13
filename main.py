from AppController import *

if __name__ == "__main__":
    model = AppModel()
    view = AppGUI()
    AppController(view, model)
    view.mainloop()
