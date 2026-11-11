import tkinter as tk
from tkinter import messagebox
from typing import Optional
from app.core.engine import CalculatorEngine
from app.data.database_manager import DatabaseManager


class CalculatorGUI:
    """Interfaz gráfica con teclado numérico clásico para la calculadora."""

    def __init__(self, root: tk.Tk, engine: CalculatorEngine, db: DatabaseManager) -> None:
        self.root = root
        self.engine = engine
        self.db = db

        # Variables de estado de la pantalla
        self.current_input: str = ""
        self.first_number: Optional[float] = None
        self.operator: Optional[str] = None

        self.root.title("Calculadora Modular")
        self.root.geometry("340x520")
        self.root.resizable(False, False)
        self._build_ui()

    def _build_ui(self) -> None:
        # Pantalla principal (Visor)
        self.display_var = tk.StringVar(value="0")
        display = tk.Entry(
            self.root,
            textvariable=self.display_var,
            font=("Arial", 24, "bold"),
            justify="right",
            state="readonly",
            bd=10
        )
        display.pack(fill="x", padx=15, pady=15)

        # Contenedor de botones
        buttons_frame = tk.Frame(self.root)
        buttons_frame.pack(padx=15, pady=5)

        # Distribución de la botonera (texto, fila, columna)
        buttons = [
            ("7", 0, 0), ("8", 0, 1), ("9", 0, 2), ("/", 0, 3),
            ("4", 1, 0), ("5", 1, 1), ("6", 1, 2), ("*", 1, 3),
            ("1", 2, 0), ("2", 2, 1), ("3", 2, 2), ("-", 2, 3),
            ("C", 3, 0), ("0", 3, 1), (".", 3, 2), ("+", 3, 3),
        ]

        for text, row, col in buttons:
            btn = tk.Button(
                buttons_frame,
                text=text,
                font=("Arial", 14, "bold"),
                width=5,
                height=2,
                command=lambda t=text: self._on_button_click(t)
            )
            btn.grid(row=row, column=col, padx=3, pady=3)

        # Botón Igual (=) ocupando todo el ancho inferior
        btn_equal = tk.Button(
            buttons_frame,
            text="=",
            font=("Arial", 14, "bold"),
            bg="#4CAF50",
            fg="white",
            height=2,
            command=self._calculate_result
        )
        btn_equal.grid(row=4, column=0, columnspan=4, sticky="we", padx=3, pady=5)

        # Sección de Historial SQLite
        tk.Label(self.root, text="Historial reciente (SQLite):", font=("Arial", 9, "bold")).pack(pady=(10, 2))
        self.listbox_history = tk.Listbox(self.root, width=45, height=6, font=("Arial", 9))
        self.listbox_history.pack(padx=15, pady=5)

        self._refresh_history()

    def _on_button_click(self, char: str) -> None:
        """Maneja los clics en números, punto decimal, operadores y limpieza."""
        if char == "C":
            self._clear()
        elif char in "0123456789.":
            if char == "." and "." in self.current_input:
                return  # Evitar múltiples puntos decimales
            self.current_input += char
            self.display_var.set(self.current_input)
        elif char in "+-*/":
            if self.current_input:
                self.first_number = float(self.current_input)
                self.operator = char
                self.current_input = ""
                self.display_var.set(f"{self.first_number} {self.operator}")

    def _calculate_result(self) -> None:
        """Delega el cálculo al motor y guarda el resultado en la base de datos."""
        if self.first_number is None or not self.operator or not self.current_input:
            return

        second_number = float(self.current_input)

        try:
            if self.operator == "+":
                result = self.engine.add(self.first_number, second_number)
            elif self.operator == "-":
                result = self.engine.subtract(self.first_number, second_number)
            elif self.operator == "*":
                result = self.engine.multiply(self.first_number, second_number)
            elif self.operator == "/":
                result = self.engine.divide(self.first_number, second_number)
            else:
                return

            # Formatear resultado para evitar '.0' innecesario en enteros
            formatted_result = int(result) if result.is_integer() else round(result, 6)
            self.display_var.set(str(formatted_result))

            # Guardar en SQLite y actualizar lista visual
            operation_str = f"{self.first_number} {self.operator} {second_number}"
            self.db.save_operation(operation_str, result)
            self._refresh_history()

            # Preparar estado para continuar operando con el resultado
            self.current_input = str(formatted_result)
            self.first_number = None
            self.operator = None

        except ValueError as e:
            messagebox.showerror("Error Matemático", str(e))
            self._clear()

    def _clear(self) -> None:
        """Reinicia la pantalla y las variables de estado."""
        self.current_input = ""
        self.first_number = None
        self.operator = None
        self.display_var.set("0")

    def _refresh_history(self) -> None:
        """Carga las operaciones desde SQLite en el cuadro de lista."""
        self.listbox_history.delete(0, tk.END)
        for _, op, res, ts in self.db.get_history():
            self.listbox_history.insert(tk.END, f"[{ts[11:]}] {op} = {res}")
