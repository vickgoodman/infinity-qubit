import tkinter as tk
from tkinter import messagebox

class TutorialWindow:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Quantum Gates Tutorial")
        self.window.geometry("600x500")
        self.window.configure(bg='#1a1a1a')

        self.setup_tutorial()

    def setup_tutorial(self):
        # Title
        title = tk.Label(self.window, text="🔬 Quantum Gates Tutorial",
                        font=('Arial', 20, 'bold'), fg='#00ff88', bg='#1a1a1a')
        title.pack(pady=20)

        # Tutorial text
        text_frame = tk.Frame(self.window, bg='#2a2a2a', relief=tk.RAISED, bd=2)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        tutorial_text = tk.Text(text_frame, font=('Arial', 12), bg='#1a1a1a',
                               fg='#ffffff', wrap=tk.WORD)
        tutorial_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        tutorial_content = """
🌟 QUANTUM GATES EXPLAINED

🔹 H (Hadamard Gate)
   • Creates superposition: |0⟩ → |+⟩ and |1⟩ → |-⟩
   • Essential for quantum algorithms
   • Example: H|0⟩ = (|0⟩ + |1⟩)/√2

🔹 X (Pauli-X / NOT Gate)
   • Flips qubit states: |0⟩ → |1⟩ and |1⟩ → |0⟩
   • Quantum equivalent of classical NOT gate
   • Example: X|0⟩ = |1⟩

🔹 Z (Pauli-Z Gate)
   • Adds phase flip: |0⟩ → |0⟩, |1⟩ → -|1⟩
   • Affects the phase of superposition states
   • Example: Z|+⟩ = |-⟩

🔹 I (Identity Gate)
   • Does nothing - leaves state unchanged
   • Useful for timing and circuit optimization
   • Example: I|ψ⟩ = |ψ⟩

🔹 CNOT (Controlled-NOT)
   • Two-qubit gate: flips target if control is |1⟩
   • Creates entanglement between qubits
   • Example: CNOT|10⟩ = |11⟩

🎯 QUANTUM STATES

• |0⟩ and |1⟩: Basic computational states
• |+⟩ = (|0⟩ + |1⟩)/√2: Positive superposition
• |-⟩ = (|0⟩ - |1⟩)/√2: Negative superposition
• |Φ+⟩ = (|00⟩ + |11⟩)/√2: Bell state (entangled)

🚀 PUZZLE SOLVING TIPS

1. Start with the input state
2. Think about what each gate does
3. Use hints when stuck
4. Try to use fewer gates for higher scores
5. Experiment with different gate combinations

Good luck solving the quantum puzzles!
        """

        tutorial_text.insert(tk.END, tutorial_content)
        tutorial_text.config(state=tk.DISABLED)

        # Close button
        close_btn = tk.Button(self.window, text="Got it!", command=self.window.destroy,
                             font=('Arial', 12, 'bold'), bg='#00ff88', fg='#000000')
        close_btn.pack(pady=10)

def show_tutorial(parent):
    TutorialWindow(parent)
