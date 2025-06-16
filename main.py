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
        self.root.geometry("1000x700")
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
        title_label.pack(pady=(0, 20))

        # Level and score info
        info_frame = tk.Frame(main_frame, bg='#1a1a1a')
        info_frame.pack(fill=tk.X, pady=(0, 10))

        self.level_label = tk.Label(info_frame, text="Level: 1",
                                font=('Arial', 14), fg='#ffffff', bg='#1a1a1a')
        self.level_label.pack(side=tk.LEFT)

        self.score_label = tk.Label(info_frame, text="Score: 0",
                                font=('Arial', 14), fg='#ffffff', bg='#1a1a1a')
        self.score_label.pack(side=tk.RIGHT)

        # Add tutorial button
        tutorial_btn = tk.Button(info_frame, text="📚 Tutorial",
                                command=lambda: show_tutorial(self.root),
                                font=('Arial', 10), bg='#9b59b6', fg='#ffffff')
        tutorial_btn.pack(side=tk.RIGHT, padx=(0, 10))

        # Circuit area
        circuit_frame = tk.Frame(main_frame, bg='#2a2a2a', relief=tk.RAISED, bd=2)
        circuit_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))

        # Circuit title
        circuit_title = tk.Label(circuit_frame, text="Quantum Circuit",
                                font=('Arial', 16, 'bold'), fg='#00ff88', bg='#2a2a2a')
        circuit_title.pack(pady=10)

        # Circuit canvas - Fixed size to match draw_circuit method
        self.circuit_canvas = tk.Canvas(circuit_frame, width=900, height=300,
                                    bg='#1a1a1a', highlightthickness=0)
        self.circuit_canvas.pack(pady=10)

        # Gate placement area
        self.gate_frame = tk.Frame(circuit_frame, bg='#2a2a2a')
        self.gate_frame.pack(fill=tk.X, padx=20, pady=10)

        # Available gates
        gates_label = tk.Label(main_frame, text="Available Gates",
                            font=('Arial', 14, 'bold'), fg='#ffffff', bg='#1a1a1a')
        gates_label.pack()

        self.gates_frame = tk.Frame(main_frame, bg='#1a1a1a')
        self.gates_frame.pack(pady=10)

        # Control buttons
        controls_frame = tk.Frame(main_frame, bg='#1a1a1a')
        controls_frame.pack(fill=tk.X, pady=10)

        self.run_button = tk.Button(controls_frame, text="🚀 Run Circuit",
                                command=self.run_circuit, font=('Arial', 12, 'bold'),
                                bg='#00ff88', fg='#000000', padx=20)
        self.run_button.pack(side=tk.LEFT, padx=5)

        self.clear_button = tk.Button(controls_frame, text="🔄 Clear",
                                    command=self.clear_circuit, font=('Arial', 12),
                                    bg='#ff6b6b', fg='#ffffff', padx=20)
        self.clear_button.pack(side=tk.LEFT, padx=5)

        self.hint_button = tk.Button(controls_frame, text="💡 Hint",
                                    command=self.show_hint, font=('Arial', 12),
                                    bg='#4ecdc4', fg='#000000', padx=20)
        self.hint_button.pack(side=tk.LEFT, padx=5)

        # Status area
        status_frame = tk.Frame(main_frame, bg='#2a2a2a', relief=tk.SUNKEN, bd=2)
        status_frame.pack(fill=tk.X, pady=(10, 0))

        self.status_label = tk.Label(status_frame, text="Ready to solve puzzles!",
                                    font=('Arial', 12), fg='#ffffff', bg='#2a2a2a')
        self.status_label.pack(pady=10)

        # State display
        self.state_display = tk.Text(status_frame, height=6, width=60,
                                    font=('Courier', 10), bg='#1a1a1a', fg='#00ff88')
        self.state_display.pack(pady=5)

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
        """Draw the quantum circuit visualization"""
        self.circuit_canvas.delete("all")

        # Get current level info for proper qubit count
        level = self.levels[self.current_level]
        num_qubits = level['qubits']

        # Circuit dimensions - Updated for larger canvas
        wire_start = 100
        wire_end = 800
        circuit_height = 300
        qubit_spacing = circuit_height // (num_qubits + 1)

        # Draw input/output dividers and labels
        input_x = wire_start - 40
        output_x = wire_end + 40

        # Input section
        self.circuit_canvas.create_line(input_x, 30, input_x, circuit_height - 30,
                                    fill='#00ff88', width=3)
        self.circuit_canvas.create_text(input_x - 30, circuit_height // 2, text="Input",
                                    fill='#00ff88', font=('Arial', 14, 'bold'), angle=90)

        # Output section
        self.circuit_canvas.create_line(output_x, 30, output_x, circuit_height - 30,
                                    fill='#00ff88', width=3)
        self.circuit_canvas.create_text(output_x + 30, circuit_height // 2, text="Output",
                                    fill='#00ff88', font=('Arial', 14, 'bold'), angle=90)

        # Draw quantum wires for each qubit
        for qubit in range(num_qubits):
            y_pos = (qubit + 1) * qubit_spacing + 30

            # Wire line
            self.circuit_canvas.create_line(wire_start, y_pos, wire_end, y_pos,
                                        fill='#ffffff', width=3)

            # Qubit labels - Fixed positioning
            self.circuit_canvas.create_text(wire_start - 15, y_pos, text=f"q{qubit}",
                                        fill='#ffffff', font=('Arial', 12, 'bold'))

        # Draw gates
        gate_width = 50
        gate_height = 40
        gate_spacing = 90

        for i, gate in enumerate(self.placed_gates):
            x = wire_start + 60 + i * gate_spacing

            if gate == 'CNOT' and num_qubits > 1:
                # Special handling for CNOT gate (control and target)
                control_y = qubit_spacing + 30
                target_y = 2 * qubit_spacing + 30

                # Control qubit (dot)
                self.circuit_canvas.create_oval(x - 8, control_y - 8, x + 8, control_y + 8,
                                            fill='#ffffff', outline='#ffffff')

                # Connection line
                self.circuit_canvas.create_line(x, control_y, x, target_y,
                                            fill='#ffffff', width=3)

                # Target qubit (X symbol)
                self.circuit_canvas.create_oval(x - 20, target_y - 20, x + 20, target_y + 20,
                                            fill='none', outline='#ffffff', width=3)
                self.circuit_canvas.create_line(x - 12, target_y - 12, x + 12, target_y + 12,
                                            fill='#ffffff', width=3)
                self.circuit_canvas.create_line(x - 12, target_y + 12, x + 12, target_y - 12,
                                            fill='#ffffff', width=3)
            else:
                # Single qubit gates
                y_pos = qubit_spacing + 30

                # Gate box
                self.circuit_canvas.create_rectangle(x - gate_width//2, y_pos - gate_height//2,
                                            x + gate_width//2, y_pos + gate_height//2,
                                            fill='#4ecdc4', outline='#ffffff', width=3)

                # Gate label
                self.circuit_canvas.create_text(x, y_pos, text=gate,
                                            fill='#000000', font=('Arial', 16, 'bold'))

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

            # Check if puzzle is solved
            if self.check_solution(final_state, level):
                self.puzzle_solved()
            else:
                self.status_label.config(text="Not quite right. Try again!")

            # Display current state
            self.display_current_state(final_state.data)

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

        messagebox.showinfo("Congratulations!",
                           f"Puzzle solved! Score: {100 - len(self.placed_gates) * 5}")

        # Move to next level
        if self.current_level < len(self.levels) - 1:
            self.load_level(self.current_level + 1)
        else:
            messagebox.showinfo("Game Complete!",
                               f"You've completed all levels! Final Score: {self.score}")

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
