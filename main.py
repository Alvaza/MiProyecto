import tkinter as tk
from app.core.engine import CalculatorEngine
from app.data.database_manager import DatabaseManager
from app.ui.calculador_gui import CalculatorGUI

def main() -> None:
    root = tk.Tk()
    engine = CalculatorEngine()
    db_manager = DatabaseManager()
    app = CalculatorGUI(root, engine, db_manager)
    root.mainloop()

if __name__ == "__main__":
    main()
