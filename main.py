import tkinter as tk
from tkinter import ttk, messagebox
import json
import numpy as np
# Updated Qiskit imports for newer versions
from qiskit import QuantumCircuit
from qiskit_aer import Aer
# from qiskit.primitives import Sampler
from qiskit.quantum_info import Statevector
import math

try:
    from game_tutorial import show_tutorial
except ImportError:
    def show_tutorial(parent):
        messagebox.showinfo("Tutorial", "Tutorial module not found")

class QubitPuzzleGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Infinity Qubit")
        self.root.geometry("2000x1200")
        self.root.configure(bg='#1a1a1a')

        # Game state
        self.current_level = 0
        self.placed_gates = []
        self.score = 0
        self.levels = self.load_levels()

        # Initialize UI
        self.setup_ui()
        self.load_level(self.current_level)

    def setup_ui(self):
        # Main frame
        main_frame = tk.Frame(self.root, bg='#1a1a1a')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Title
        title_label = tk.Label(main_frame, text="🔬 Infinity Qubit",
                            font=('Arial', 24, 'bold'), fg='#00ff88', bg='#1a1a1a')
        title_label.pack(pady=(0, 10))

        # Level and score info - Centered under title
        info_frame = tk.Frame(main_frame, bg='#1a1a1a')
        info_frame.pack(pady=(0, 20))

        self.level_label = tk.Label(info_frame, text="Level: 1",
                                font=('Arial', 16, 'bold'), fg='#ffffff', bg='#1a1a1a')
        self.level_label.pack(side=tk.LEFT, padx=20)

        self.score_label = tk.Label(info_frame, text="Score: 0",
                                font=('Arial', 16, 'bold'), fg='#ffffff', bg='#1a1a1a')
        self.score_label.pack(side=tk.LEFT, padx=20)

        # Add tutorial button - moved to top right corner
        tutorial_btn = tk.Button(main_frame, text="📚 Tutorial",
                                command=lambda: show_tutorial(self.root),
                                font=('Arial', 10), bg='#9b59b6', fg='#ffffff')
        tutorial_btn.place(relx=0.98, rely=0.02, anchor='ne')

        # Circuit area - Made much larger
        circuit_frame = tk.Frame(main_frame, bg='#2a2a2a', relief=tk.RAISED, bd=3)
        circuit_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))

        # Circuit title
        circuit_title = tk.Label(circuit_frame, text="Quantum Circuit",
                                font=('Arial', 20, 'bold'), fg='#00ff88', bg='#2a2a2a')
        circuit_title.pack(pady=15)

        # Circuit canvas - Doubled in size (900x300 -> 1800x600)
        self.circuit_canvas = tk.Canvas(circuit_frame, width=1800, height=600,
                                    bg='#1a1a1a', highlightthickness=0)
        self.circuit_canvas.pack(pady=15)

        # Gate placement area
        self.gate_frame = tk.Frame(circuit_frame, bg='#2a2a2a')
        self.gate_frame.pack(fill=tk.X, padx=20, pady=15)

        # Available gates - Centered
        gates_label = tk.Label(main_frame, text="Available Gates",
                            font=('Arial', 16, 'bold'), fg='#ffffff', bg='#1a1a1a')
        gates_label.pack(pady=(10, 5))

        self.gates_frame = tk.Frame(main_frame, bg='#1a1a1a')
        self.gates_frame.pack(pady=10)

        # Control buttons - Centered under available gates
        controls_frame = tk.Frame(main_frame, bg='#1a1a1a')
        controls_frame.pack(pady=(15, 10))

        self.run_button = tk.Button(controls_frame, text="🚀 Run Circuit",
                                command=self.run_circuit, font=('Arial', 14, 'bold'),
                                bg='#00ff88', fg='#000000', padx=25, pady=8)
        self.run_button.pack(side=tk.LEFT, padx=10)

        self.clear_button = tk.Button(controls_frame, text="🔄 Clear",
                                    command=self.clear_circuit, font=('Arial', 14),
                                    bg='#ff6b6b', fg='#ffffff', padx=25, pady=8)
        self.clear_button.pack(side=tk.LEFT, padx=10)

        self.hint_button = tk.Button(controls_frame, text="💡 Hint",
                                    command=self.show_hint, font=('Arial', 14),
                                    bg='#4ecdc4', fg='#000000', padx=25, pady=8)
        self.hint_button.pack(side=tk.LEFT, padx=10)

        # Status area - Made much larger and more prominent
        status_frame = tk.Frame(main_frame, bg='#2a2a2a', relief=tk.RAISED, bd=3)
        status_frame.pack(fill=tk.X, pady=(15, 0))

        # Status title
        status_title = tk.Label(status_frame, text="🔍 Quantum State Information",
                            font=('Arial', 16, 'bold'), fg='#00ff88', bg='#2a2a2a')
        status_title.pack(pady=(10, 5))

        self.status_label = tk.Label(status_frame, text="Ready to solve puzzles!",
                                    font=('Arial', 14), fg='#ffffff', bg='#2a2a2a')
        self.status_label.pack(pady=5)

        # State display - Made much larger with better formatting
        self.state_display = tk.Text(status_frame, height=12, width=100,
                                    font=('Courier', 12), bg='#1a1a1a', fg='#00ff88',
                                    relief=tk.SUNKEN, bd=2)
        self.state_display.pack(pady=15, padx=20)

    def load_levels(self):
        """Load puzzle levels from JSON or create default levels"""
        try:
            with open('levels.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return self.create_default_levels()

    def create_default_levels(self):
        """Create default puzzle levels"""
        levels = [
            {
                "name": "First Superposition",
                "description": "Transform |0⟩ into |+⟩ (equal superposition)",
                "input_state": "|0⟩",
                "target_state": "|+⟩",
                "available_gates": ["H", "X", "I"],
                "qubits": 1,
                "hint": "The Hadamard gate (H) creates superposition from |0⟩"
            },
            {
                "name": "Bit Flip",
                "description": "Transform |0⟩ into |1⟩",
                "input_state": "|0⟩",
                "target_state": "|1⟩",
                "available_gates": ["H", "X", "Z"],
                "qubits": 1,
                "hint": "The X gate flips |0⟩ to |1⟩"
            },
            {
                "name": "Phase Flip",
                "description": "Transform |+⟩ into |-⟩",
                "input_state": "|+⟩",
                "target_state": "|-⟩",
                "available_gates": ["H", "X", "Z"],
                "qubits": 1,
                "hint": "The Z gate adds a phase flip"
            },
            {
                "name": "Bell State",
                "description": "Create entangled state |Φ+⟩ from |00⟩",
                "input_state": "|00⟩",
                "target_state": "|Φ+⟩",
                "available_gates": ["H", "X", "CNOT"],
                "qubits": 2,
                "hint": "Apply H to first qubit, then CNOT"
            }
        ]

        # Save levels to file
        with open('levels.json', 'w') as f:
            json.dump(levels, indent=2, fp=f)

        return levels

    def load_level(self, level_index):
        """Load a specific level"""
        if level_index >= len(self.levels):
            messagebox.showinfo("Congratulations!", "You've completed all levels!")
            return

        level = self.levels[level_index]
        self.current_level = level_index

        # Update UI
        self.level_label.config(text=f"Level: {level_index + 1}")
        self.status_label.config(text=f"{level['name']}: {level['description']}")

        # Clear previous state
        self.placed_gates = []
        self.clear_circuit()

        # Setup available gates
        self.setup_gates(level['available_gates'])

        # Draw circuit
        self.draw_circuit()

        # Show initial and target states
        self.display_states(level)

    def setup_gates(self, available_gates):
        """Setup available gate buttons"""
        # Clear existing gates
        for widget in self.gates_frame.winfo_children():
            widget.destroy()

        gate_colors = {
            'H': '#ff6b6b',  # Red
            'X': '#4ecdc4',  # Cyan
            'Z': '#45b7d1',  # Blue
            'I': '#96ceb4',  # Green
            'CNOT': '#ffeaa7'  # Yellow
        }

        for gate in available_gates:
            color = gate_colors.get(gate, '#ffffff')
            btn = tk.Button(self.gates_frame, text=gate,
                          command=lambda g=gate: self.add_gate(g),
                          font=('Arial', 12, 'bold'), bg=color, fg='#000000',
                          width=6, height=2)
            btn.pack(side=tk.LEFT, padx=5)

    def add_gate(self, gate):
        """Add a gate to the circuit"""
        if len(self.placed_gates) < 10:  # Limit gates
            self.placed_gates.append(gate)
            self.draw_circuit()

    def clear_circuit(self):
        """Clear all placed gates"""
        self.placed_gates = []
        self.draw_circuit()

    def draw_circuit(self):
        """Draw the quantum circuit visualization - Updated for larger canvas"""
        self.circuit_canvas.delete("all")

        # Get current level info for proper qubit count
        level = self.levels[self.current_level]
        num_qubits = level['qubits']

        # Circuit dimensions - Doubled all values for 2x size
        wire_start = 200
        wire_end = 1600
        circuit_height = 600
        qubit_spacing = circuit_height // (num_qubits + 1)

        # Draw input/output dividers and labels - Scaled up
        input_x = wire_start - 80
        output_x = wire_end + 80

        # Input section
        self.circuit_canvas.create_line(input_x, 60, input_x, circuit_height - 60,
                                    fill='#00ff88', width=6)
        self.circuit_canvas.create_text(input_x - 60, circuit_height // 2, text="Input",
                                    fill='#00ff88', font=('Arial', 24, 'bold'), angle=90)

        # Output section
        self.circuit_canvas.create_line(output_x, 60, output_x, circuit_height - 60,
                                    fill='#00ff88', width=6)
        self.circuit_canvas.create_text(output_x + 60, circuit_height // 2, text="Output",
                                    fill='#00ff88', font=('Arial', 24, 'bold'), angle=90)

        # Draw quantum wires for each qubit
        for qubit in range(num_qubits):
            y_pos = (qubit + 1) * qubit_spacing + 60

            # Wire line - Thicker
            self.circuit_canvas.create_line(wire_start, y_pos, wire_end, y_pos,
                                        fill='#ffffff', width=6)

            # Qubit labels - Larger
            self.circuit_canvas.create_text(wire_start - 30, y_pos, text=f"q{qubit}",
                                        fill='#ffffff', font=('Arial', 20, 'bold'))

        # Draw gates - All doubled in size
        gate_width = 100
        gate_height = 80
        gate_spacing = 180

        for i, gate in enumerate(self.placed_gates):
            x = wire_start + 120 + i * gate_spacing

            if gate == 'CNOT' and num_qubits > 1:
                # Special handling for CNOT gate - Scaled up
                control_y = qubit_spacing + 60
                target_y = 2 * qubit_spacing + 60

                # Control qubit (dot) - Larger
                self.circuit_canvas.create_oval(x - 16, control_y - 16, x + 16, control_y + 16,
                                            fill='#ffffff', outline='#ffffff')

                # Connection line - Thicker
                self.circuit_canvas.create_line(x, control_y, x, target_y,
                                            fill='#ffffff', width=6)

                # Target qubit (X symbol) - Larger
                self.circuit_canvas.create_oval(x - 40, target_y - 40, x + 40, target_y + 40,
                                            fill='none', outline='#ffffff', width=6)
                self.circuit_canvas.create_line(x - 24, target_y - 24, x + 24, target_y + 24,
                                            fill='#ffffff', width=6)
                self.circuit_canvas.create_line(x - 24, target_y + 24, x + 24, target_y - 24,
                                            fill='#ffffff', width=6)
            else:
                # Single qubit gates - Doubled size
                y_pos = qubit_spacing + 60

                # Gate box - Larger
                self.circuit_canvas.create_rectangle(x - gate_width//2, y_pos - gate_height//2,
                                            x + gate_width//2, y_pos + gate_height//2,
                                            fill='#4ecdc4', outline='#ffffff', width=6)

                # Gate label - Larger font
                self.circuit_canvas.create_text(x, y_pos, text=gate,
                                            fill='#000000', font=('Arial', 32, 'bold'))

    def run_circuit(self):
        """Execute the quantum circuit and check result"""
        if not self.placed_gates:
            self.status_label.config(text="Add some gates first!")
            return

        level = self.levels[self.current_level]

        try:
            # Create quantum circuit
            qc = QuantumCircuit(level['qubits'])

            # Initialize circuit to the input state
            initial_state = self.get_initial_state(level)
            if level['input_state'] == "|1⟩":
                qc.x(0)  # Start with |1⟩
            elif level['input_state'] == "|+⟩":
                qc.h(0)  # Start with |+⟩
            elif level['input_state'] == "|-⟩":
                qc.x(0)
                qc.h(0)  # Start with |-⟩
            elif level['input_state'] == "|00⟩":
                pass  # Already starts with |00⟩
            # Add more initial states as needed

            # Apply gates
            for gate in self.placed_gates:
                if gate == 'H':
                    qc.h(0)
                elif gate == 'X':
                    qc.x(0)
                elif gate == 'Z':
                    qc.z(0)
                elif gate == 'I':
                    qc.id(0)  # Identity gate
                elif gate == 'CNOT' and level['qubits'] > 1:
                    qc.cx(0, 1)

            # Get final state using Statevector
            final_state = Statevector(qc)

            # Display current state FIRST (before checking solution)
            self.display_current_state(final_state.data)

            # Check if puzzle is solved
            if self.check_solution(final_state, level):
                self.status_label.config(text="🎉 Puzzle solved! Great job!")
                self.puzzle_solved()
            else:
                self.status_label.config(text="Not quite right. Try again!")

        except Exception as e:
            self.status_label.config(text=f"Error: {str(e)}")

    def check_solution(self, final_state, level):
        """Check if the current state matches the target"""
        target_state = self.get_target_state(level)

        # Calculate fidelity
        fidelity = abs(np.vdot(target_state, final_state.data)) ** 2
        return fidelity > 0.99  # Allow for small numerical errors

    def get_target_state(self, level):
        """Get the target quantum state"""
        target = level['target_state']

        if target == "|0⟩":
            return np.array([1, 0])
        elif target == "|1⟩":
            return np.array([0, 1])
        elif target == "|+⟩":
            return np.array([1, 1]) / np.sqrt(2)
        elif target == "|-⟩":
            return np.array([1, -1]) / np.sqrt(2)
        elif target == "|00⟩":
            return np.array([1, 0, 0, 0])
        elif target == "|Φ+⟩":  # Bell state
            return np.array([1, 0, 0, 1]) / np.sqrt(2)

        return np.array([1, 0])  # Default

    def get_initial_state(self, level):
        """Get the initial quantum state"""
        initial = level['input_state']

        if initial == "|0⟩":
            return np.array([1, 0])
        elif initial == "|1⟩":
            return np.array([0, 1])
        elif initial == "|+⟩":
            return np.array([1, 1]) / np.sqrt(2)
        elif initial == "|-⟩":
            return np.array([1, -1]) / np.sqrt(2)
        elif initial == "|00⟩":
            return np.array([1, 0, 0, 0])
        elif initial == "|Φ+⟩":  # Bell state
            return np.array([1, 0, 0, 1]) / np.sqrt(2)

        return np.array([1, 0])  # Default

    def puzzle_solved(self):
        """Handle puzzle completion"""
        self.score += 100 - len(self.placed_gates) * 5  # Bonus for efficiency
        self.score_label.config(text=f"Score: {self.score}")

        # Create a custom congratulations dialog - Made even larger
        congrats_window = tk.Toplevel(self.root)
        congrats_window.title("🎉 Congratulations!")
        congrats_window.geometry("800x600")  # Made even larger
        congrats_window.configure(bg='#1a1a1a')
        congrats_window.resizable(False, False)

        # Make sure it stays on top and is modal
        congrats_window.transient(self.root)
        congrats_window.grab_set()
        congrats_window.focus_set()
        congrats_window.lift()
        congrats_window.attributes('-topmost', True)

        # Center on parent window - Updated for new size
        congrats_window.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - 400
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - 300
        congrats_window.geometry(f"800x600+{x}+{y}")

        # Congratulations content - Larger spacing and fonts
        title_label = tk.Label(congrats_window, text="🎉 PUZZLE SOLVED! 🎉",
                            font=('Arial', 32, 'bold'), fg='#00ff88', bg='#1a1a1a')
        title_label.pack(pady=(50, 30))

        score_label = tk.Label(congrats_window, text=f"Score: {100 - len(self.placed_gates) * 5}",
                            font=('Arial', 24, 'bold'), fg='#ffffff', bg='#1a1a1a')
        score_label.pack(pady=20)

        efficiency_label = tk.Label(congrats_window, text=f"Gates Used: {len(self.placed_gates)}",
                                font=('Arial', 20), fg='#ffffff', bg='#1a1a1a')
        efficiency_label.pack(pady=15)

        if len(self.placed_gates) <= 2:
            bonus_label = tk.Label(congrats_window, text="🌟 EXCELLENT EFFICIENCY! 🌟",
                                font=('Arial', 18, 'bold'), fg='#ffd700', bg='#1a1a1a')
            bonus_label.pack(pady=20)

        # Button frame for better spacing
        button_frame = tk.Frame(congrats_window, bg='#1a1a1a')
        button_frame.pack(pady=(50, 40))

        # Continue button - Made MUCH larger and more prominent
        continue_btn = tk.Button(button_frame, text="🚀 Continue to Next Level",
                                command=lambda: self.continue_to_next_level(congrats_window),
                                font=('Arial', 20, 'bold'), bg='#00ff88', fg='#000000',
                                padx=60, pady=25, relief=tk.RAISED, bd=5)
        continue_btn.pack(pady=20)

        # Focus on the button so Enter key works
        continue_btn.focus_set()

        # Bind keys
        congrats_window.bind('<Return>', lambda e: self.continue_to_next_level(congrats_window))
        congrats_window.bind('<Escape>', lambda e: self.continue_to_next_level(congrats_window))
        congrats_window.bind('<space>', lambda e: self.continue_to_next_level(congrats_window))

        # Add a close button as backup - Also larger
        close_btn = tk.Button(button_frame, text="❌ Close",
                            command=lambda: congrats_window.destroy(),
                            font=('Arial', 14), bg='#ff6b6b', fg='#ffffff',
                            padx=30, pady=15)
        close_btn.pack(pady=10)

    def continue_to_next_level(self, dialog_window):
        """Close dialog and advance to next level"""
        dialog_window.destroy()
        self.advance_level()

    def advance_level(self):
        """Advance to the next level"""
        # Move to next level
        if self.current_level < len(self.levels) - 1:
            self.load_level(self.current_level + 1)
        else:
            # Game complete dialog - also larger
            complete_window = tk.Toplevel(self.root)
            complete_window.title("🏆 Game Complete!")
            complete_window.geometry("600x450")  # Made taller
            complete_window.configure(bg='#1a1a1a')
            complete_window.resizable(False, False)

            # Make sure it stays on top
            complete_window.transient(self.root)
            complete_window.grab_set()
            complete_window.focus_set()
            complete_window.lift()
            complete_window.attributes('-topmost', True)

            # Center on parent window
            complete_window.update_idletasks()
            x = self.root.winfo_x() + (self.root.winfo_width() // 2) - 300
            y = self.root.winfo_y() + (self.root.winfo_height() // 2) - 225
            complete_window.geometry(f"600x450+{x}+{y}")

            title_label = tk.Label(complete_window, text="🏆 CONGRATULATIONS! 🏆",
                                font=('Arial', 24, 'bold'), fg='#ffd700', bg='#1a1a1a')
            title_label.pack(pady=(30, 15))

            complete_label = tk.Label(complete_window, text="You've completed all levels!",
                                    font=('Arial', 18), fg='#ffffff', bg='#1a1a1a')
            complete_label.pack(pady=10)

            final_score_label = tk.Label(complete_window, text=f"Final Score: {self.score}",
                                        font=('Arial', 20, 'bold'), fg='#00ff88', bg='#1a1a1a')
            final_score_label.pack(pady=15)

            # Button frame
            button_frame = tk.Frame(complete_window, bg='#1a1a1a')
            button_frame.pack(pady=(20, 20))

            restart_btn = tk.Button(button_frame, text="Play Again",
                                command=lambda: self.restart_from_complete(complete_window),
                                font=('Arial', 14, 'bold'), bg='#00ff88', fg='#000000',
                                padx=40, pady=12, relief=tk.RAISED, bd=3)
            restart_btn.pack(pady=10)

            # Focus and key bindings
            restart_btn.focus_set()
            complete_window.bind('<Return>', lambda e: self.restart_from_complete(complete_window))

    def restart_game(self):
        """Restart the game from level 1"""
        self.current_level = 0
        self.score = 0
        self.placed_gates = []
        self.load_level(0)

    def show_hint(self):
        """Show hint for current level"""
        hint = self.levels[self.current_level]['hint']
        messagebox.showinfo("Hint", hint)

    def display_states(self, level):
        """Display input and target states"""
        self.state_display.delete(1.0, tk.END)
        self.state_display.insert(tk.END, f"Input State: {level['input_state']}\n")
        self.state_display.insert(tk.END, f"Target State: {level['target_state']}\n")
        self.state_display.insert(tk.END, f"Qubits: {level['qubits']}\n")
        self.state_display.insert(tk.END, "-" * 40 + "\n")

    def display_current_state(self, state_vector):
        """Display the current quantum state"""
        # Clear the display first to avoid accumulation
        self.state_display.delete(1.0, tk.END)

        # Show level info again
        level = self.levels[self.current_level]
        self.state_display.insert(tk.END, f"Input State: {level['input_state']}\n")
        self.state_display.insert(tk.END, f"Target State: {level['target_state']}\n")
        self.state_display.insert(tk.END, f"Qubits: {level['qubits']}\n")
        self.state_display.insert(tk.END, "-" * 40 + "\n")

        # Show current state
        self.state_display.insert(tk.END, f"Current State Vector:\n")
        for i, amplitude in enumerate(state_vector):
            if abs(amplitude) > 0.001:  # Only show non-zero amplitudes
                self.state_display.insert(tk.END, f"|{i:0{len(bin(len(state_vector)-1))-2}b}⟩: {amplitude:.3f}\n")
        self.state_display.insert(tk.END, "\n")
        self.state_display.see(tk.END)

def main():
    root = tk.Tk()
    game = QubitPuzzleGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()
