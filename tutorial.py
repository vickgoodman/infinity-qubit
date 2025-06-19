import tkinter as tk
from tkinter import ttk, messagebox
import json
import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import Aer
from qiskit.quantum_info import Statevector
import math
from PIL import Image, ImageTk
import pygame

class TutorialWindow:
    def __init__(self, parent, return_callback=None):
        self.parent = parent
        self.return_callback = return_callback
        
        # Create the window as a Toplevel but make it independent
        self.window = tk.Toplevel(parent)
        self.window.title("🎓 Quantum Gates Tutorial")
        self.window.geometry("900x700")
        self.window.configure(bg='#1a1a1a')
        self.window.resizable(False, False)
        
        # Make window independent and visible even if parent is withdrawn
        self.window.transient()  # Remove parent dependency
        self.window.grab_set()
        self.window.focus_set()
        
        # Handle window close event
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Center window on screen instead of parent
        self.center_window_on_screen()
        
        # Gate information
        self.gate_info = {
            'H': {
                'name': 'Hadamard Gate',
                'description': 'Creates superposition by transforming |0⟩ to |+⟩ and |1⟩ to |-⟩',
                'example': 'H|0⟩ = |+⟩ = (|0⟩ + |1⟩)/√2',
                'input_state': '|0⟩',
                'target_state': '|+⟩',
                'color': '#ff6b6b'
            },
            'S': {
                'name': 'S Gate (Phase)',
                'description': 'Applies a 90° phase shift to |1⟩ state',
                'example': 'S|1⟩ = i|1⟩',
                'input_state': '|1⟩',
                'target_state': 'i|1⟩',
                'color': '#74b9ff'
            },
            'T': {
                'name': 'T Gate (π/8)',
                'description': 'Applies a 45° phase shift to |1⟩ state',
                'example': 'T|1⟩ = e^(iπ/4)|1⟩',
                'input_state': '|1⟩',
                'target_state': 'e^(iπ/4)|1⟩',
                'color': '#a29bfe'
            },
            'CZ': {
                'name': 'Controlled-Z Gate',
                'description': 'Applies Z gate to target qubit if control qubit is |1⟩',
                'example': 'CZ|11⟩ = -|11⟩',
                'input_state': '|11⟩',
                'target_state': '-|11⟩',
                'color': '#fd79a8'
            },
            'X': {
                'name': 'Pauli-X Gate (NOT)',
                'description': 'Flips qubit state: |0⟩↔|1⟩',
                'example': 'X|0⟩ = |1⟩, X|1⟩ = |0⟩',
                'input_state': '|0⟩',
                'target_state': '|1⟩',
                'color': '#4ecdc4'
            },
            'Y': {
                'name': 'Pauli-Y Gate',
                'description': 'Combination of X and Z gates with phase',
                'example': 'Y|0⟩ = i|1⟩, Y|1⟩ = -i|0⟩',
                'input_state': '|0⟩',
                'target_state': 'i|1⟩',
                'color': '#55a3ff'
            },
            'Z': {
                'name': 'Pauli-Z Gate',
                'description': 'Applies phase flip to |1⟩ state',
                'example': 'Z|0⟩ = |0⟩, Z|1⟩ = -|1⟩',
                'input_state': '|1⟩',
                'target_state': '-|1⟩',
                'color': '#45b7d1'
            },
            'CNOT': {
                'name': 'Controlled-NOT Gate',
                'description': 'Flips target qubit if control qubit is |1⟩',
                'example': 'CNOT|10⟩ = |11⟩, CNOT|00⟩ = |00⟩',
                'input_state': '|10⟩',
                'target_state': '|11⟩',
                'color': '#ffeaa7'
            }
        }
        
        self.setup_ui()
        
        # Ensure window is visible and on top
        self.window.lift()
        self.window.focus_force()
    
    def center_window(self):
        """Center the window on the parent"""
        self.window.update_idletasks()
        parent_x = self.parent.winfo_x()
        parent_y = self.parent.winfo_y()
        parent_width = self.parent.winfo_width()
        parent_height = self.parent.winfo_height()
        
        x = parent_x + (parent_width // 2) - 450
        y = parent_y + (parent_height // 2) - 350
        self.window.geometry(f"900x700+{x}+{y}")

    def center_window_on_screen(self):
        """Center the window on the screen"""
        self.window.update_idletasks()
        
        # Get screen dimensions
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        
        # Get window dimensions
        window_width = 900
        window_height = 700
        
        # Calculate position
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        self.window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    def setup_ui(self):
        """Setup the tutorial interface"""
        # Main Menu button in top right corner
        if self.return_callback:
            main_menu_btn = tk.Button(self.window, text="🏠 Main Menu",
                                     command=self.return_to_main_menu,
                                     font=('Arial', 10, 'bold'), bg='#00ff88', fg='#000000',
                                     padx=15, pady=5)
            main_menu_btn.place(x=780, y=10)

        # Title
        title_label = tk.Label(self.window, text="🎓 Quantum Gates Tutorial",
                              font=('Arial', 24, 'bold'), fg='#00ff88', bg='#1a1a1a')
        title_label.pack(pady=(20, 10))
        
        # Explanation text box
        explanation_frame = tk.Frame(self.window, bg='#2a2a2a', relief=tk.RAISED, bd=2)
        explanation_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        explanation_text = tk.Text(explanation_frame, height=6, width=80,
                                  font=('Arial', 11), bg='#1a1a1a', fg='#ffffff',
                                  wrap=tk.WORD, relief=tk.FLAT, padx=10, pady=10)
        explanation_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Insert explanation text
        explanation = """Quantum gates are the fundamental building blocks of quantum circuits. Unlike classical logic gates that work with bits (0 or 1), quantum gates operate on qubits that can exist in superposition states. 

Each gate performs a specific transformation on quantum states:
• Single-qubit gates (H, X, Y, Z, S, T) operate on individual qubits
• Two-qubit gates (CNOT, CZ) create entanglement between qubits
• Gates are reversible and preserve quantum information

Click on any gate below to see an interactive demonstration of how it works!"""
        
        explanation_text.insert(tk.END, explanation)
        explanation_text.config(state=tk.DISABLED)
        
        # Gates grid
        gates_frame = tk.Frame(self.window, bg='#1a1a1a')
        gates_frame.pack(pady=20)
        
        # Gate order: H S T CZ (top row), X Y Z CNOT (bottom row)
        gate_order = [
            ['H', 'S', 'T', 'CZ'],
            ['X', 'Y', 'Z', 'CNOT']
        ]
        
        for row_idx, row in enumerate(gate_order):
            row_frame = tk.Frame(gates_frame, bg='#1a1a1a')
            row_frame.pack(pady=10)
            
            for col_idx, gate in enumerate(row):
                self.create_gate_button(row_frame, gate)
        
        # Close button (only if no return callback)
        if not self.return_callback:
            close_frame = tk.Frame(self.window, bg='#1a1a1a')
            close_frame.pack(pady=20)
            
            close_btn = tk.Button(close_frame, text="✖ Close Tutorial",
                                 command=self.window.destroy,
                                 font=('Arial', 12, 'bold'), bg='#ff6b6b', fg='#ffffff',
                                 padx=20, pady=10)
            close_btn.pack()
    
    def return_to_main_menu(self):
        """Return to main menu"""
        if self.return_callback:
            self.window.destroy()
            self.return_callback()

    def on_closing(self):
        """Handle window close event"""
        if self.return_callback:
            self.window.destroy()
            self.return_callback()
        else:
            self.window.destroy()

    def create_gate_button(self, parent, gate):
        """Create a clickable gate button"""
        gate_frame = tk.Frame(parent, bg='#1a1a1a')
        gate_frame.pack(side=tk.LEFT, padx=15, pady=10)
        
        # Gate button
        gate_info = self.gate_info[gate]
        btn = tk.Button(gate_frame, text=gate,
                       command=lambda g=gate: self.open_gate_tutorial(g),
                       font=('Arial', 18, 'bold'), 
                       bg=gate_info['color'], fg='#000000',
                       width=4, height=2, relief=tk.RAISED, bd=3)
        btn.pack()
        
        # Gate name label
        name_label = tk.Label(gate_frame, text=gate_info['name'],
                             font=('Arial', 10, 'bold'), fg='#ffffff', bg='#1a1a1a')
        name_label.pack(pady=(5, 0))
    
    def open_gate_tutorial(self, gate):
        """Open individual gate tutorial"""
        GateTutorial(self.window, gate, self.gate_info[gate])


class GateTutorial:
    def __init__(self, parent, gate, gate_info):
        self.parent = parent
        self.gate = gate
        self.gate_info = gate_info
        self.placed_gates = []
        
        self.window = tk.Toplevel(parent)
        self.window.title(f"🎓 {gate_info['name']} Tutorial")
        self.window.geometry("1000x800")
        self.window.configure(bg='#1a1a1a')
        self.window.resizable(False, False)
        
        # Make window modal
        self.window.transient(parent)
        self.window.grab_set()
        self.window.focus_set()
        
        self.center_window()
        self.setup_ui()
        
        # Initialize sound if available
        self.sound_enabled = False
        try:
            if hasattr(parent, 'master') and hasattr(parent.master, 'sound_enabled'):
                self.sound_enabled = parent.master.sound_enabled
                self.sounds = getattr(parent.master, 'sounds', {})
        except:
            pass
    
    def center_window(self):
        """Center the window on the parent"""
        self.window.update_idletasks()
        parent_x = self.parent.winfo_x()
        parent_y = self.parent.winfo_y()
        parent_width = self.parent.winfo_width()
        parent_height = self.parent.winfo_height()
        
        x = parent_x + (parent_width // 2) - 500
        y = parent_y + (parent_height // 2) - 400
        self.window.geometry(f"1000x800+{x}+{y}")
    
    def setup_ui(self):
        """Setup the gate tutorial interface"""
        # Title
        title_label = tk.Label(self.window, text=f"{self.gate_info['name']} Tutorial",
                              font=('Arial', 20, 'bold'), fg='#00ff88', bg='#1a1a1a')
        title_label.pack(pady=(20, 10))
        
        # Description
        desc_frame = tk.Frame(self.window, bg='#2a2a2a', relief=tk.RAISED, bd=2)
        desc_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        desc_label = tk.Label(desc_frame, text=self.gate_info['description'],
                             font=('Arial', 12), fg='#ffffff', bg='#2a2a2a',
                             wraplength=800, justify=tk.CENTER)
        desc_label.pack(pady=15)
        
        example_label = tk.Label(desc_frame, text=f"Example: {self.gate_info['example']}",
                                font=('Arial', 11, 'italic'), fg='#00ff88', bg='#2a2a2a')
        example_label.pack(pady=(0, 15))
        
        # Circuit area
        circuit_frame = tk.Frame(self.window, bg='#2a2a2a', relief=tk.RAISED, bd=3)
        circuit_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        circuit_title = tk.Label(circuit_frame, text="Interactive Circuit",
                                font=('Arial', 14, 'bold'), fg='#00ff88', bg='#2a2a2a')
        circuit_title.pack(pady=10)
        
        # Canvas for circuit visualization
        self.canvas = tk.Canvas(circuit_frame, width=800, height=200,
                               bg='#1a1a1a', highlightthickness=0)
        self.canvas.pack(pady=10)
        
        # Gate placement button
        gate_frame = tk.Frame(circuit_frame, bg='#2a2a2a')
        gate_frame.pack(pady=10)
        
        self.gate_btn = tk.Button(gate_frame, text=f"Add {self.gate} Gate",
                                 command=self.add_gate,
                                 font=('Arial', 12, 'bold'),
                                 bg=self.gate_info['color'], fg='#000000',
                                 padx=20, pady=10)
        self.gate_btn.pack(side=tk.LEFT, padx=10)
        
        # Control buttons
        run_btn = tk.Button(gate_frame, text="🚀 Run Circuit",
                           command=self.run_circuit,
                           font=('Arial', 12, 'bold'),
                           bg='#00ff88', fg='#000000',
                           padx=20, pady=10)
        run_btn.pack(side=tk.LEFT, padx=10)
        
        clear_btn = tk.Button(gate_frame, text="🔄 Clear",
                             command=self.clear_circuit,
                             font=('Arial', 12, 'bold'),
                             bg='#ff6b6b', fg='#ffffff',
                             padx=20, pady=10)
        clear_btn.pack(side=tk.LEFT, padx=10)
        
        # Results area
        results_frame = tk.Frame(self.window, bg='#2a2a2a', relief=tk.RAISED, bd=3)
        results_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        results_title = tk.Label(results_frame, text="Results",
                                font=('Arial', 14, 'bold'), fg='#00ff88', bg='#2a2a2a')
        results_title.pack(pady=(10, 5))
        
        self.results_text = tk.Text(results_frame, height=8, width=80,
                                   font=('Courier', 10), bg='#1a1a1a', fg='#ffffff',
                                   relief=tk.SUNKEN, bd=2)
        self.results_text.pack(pady=10, padx=20)
        
        # Close button (only if no return callback)
        if not self.return_callback:
            close_frame = tk.Frame(self.window, bg='#1a1a1a')
            close_frame.pack(pady=20)
            
            close_btn = tk.Button(close_frame, text="✖ Close Tutorial",
                                 command=self.on_closing,
                                 font=('Arial', 12, 'bold'), bg='#ff6b6b', fg='#ffffff',
                                 padx=20, pady=10)
            close_btn.pack()
        
        # Initialize display
        self.draw_circuit()
        self.display_initial_info()
    
    def add_gate(self):
        """Add the tutorial gate to the circuit"""
        if len(self.placed_gates) < 3:  # Limit gates
            self.placed_gates.append(self.gate)
            self.draw_circuit()
            self.play_sound(self.gate)
    
    def clear_circuit(self):
        """Clear all gates"""
        self.placed_gates = []
        self.draw_circuit()
        self.display_initial_info()
    
    def draw_circuit(self):
        """Draw the quantum circuit"""
        self.canvas.delete("all")
        
        # Determine number of qubits based on gate
        num_qubits = 2 if self.gate in ['CNOT', 'CZ'] else 1
        
        # Circuit dimensions
        wire_start = 100
        wire_end = 700
        circuit_height = 200
        qubit_spacing = circuit_height // (num_qubits + 1)
        
        # Draw quantum wires
        for qubit in range(num_qubits):
            y_pos = (qubit + 1) * qubit_spacing
            
            # Wire line
            self.canvas.create_line(wire_start, y_pos, wire_end, y_pos,
                                   fill='#ffffff', width=3)
            
            # Qubit labels
            self.canvas.create_text(wire_start - 30, y_pos,
                                   text=f"q{qubit}", fill='#ffffff',
                                   font=('Arial', 12, 'bold'))
        
        # Draw gates
        gate_width = 60
        gate_height = 50
        gate_spacing = 120
        
        for i, gate in enumerate(self.placed_gates):
            x = wire_start + 100 + i * gate_spacing
            
            if gate in ['CNOT', 'CZ'] and num_qubits > 1:
                # Two-qubit gates
                control_y = qubit_spacing
                target_y = 2 * qubit_spacing
                
                if gate == 'CNOT':
                    # Control dot
                    self.canvas.create_oval(x - 8, control_y - 8, x + 8, control_y + 8,
                                           fill='#ffffff', outline='#ffffff')
                    # Connection line
                    self.canvas.create_line(x, control_y, x, target_y,
                                           fill='#ffffff', width=3)
                    # Target (X symbol)
                    self.canvas.create_oval(x - 20, target_y - 20, x + 20, target_y + 20,
                                           fill='', outline='#ffffff', width=3)
                    self.canvas.create_line(x - 12, target_y - 12, x + 12, target_y + 12,
                                           fill='#ffffff', width=3)
                    self.canvas.create_line(x - 12, target_y + 12, x + 12, target_y - 12,
                                           fill='#ffffff', width=3)
                elif gate == 'CZ':
                    # Control dot
                    self.canvas.create_oval(x - 8, control_y - 8, x + 8, control_y + 8,
                                           fill='#ffffff', outline='#ffffff')
                    # Connection line
                    self.canvas.create_line(x, control_y, x, target_y,
                                           fill='#ffffff', width=3)
                    # Target dot
                    self.canvas.create_oval(x - 8, target_y - 8, x + 8, target_y + 8,
                                           fill='#ffffff', outline='#ffffff')
            else:
                # Single qubit gates
                y_pos = qubit_spacing
                
                # Gate box
                self.canvas.create_rectangle(x - gate_width//2, y_pos - gate_height//2,
                                           x + gate_width//2, y_pos + gate_height//2,
                                           fill=self.gate_info['color'], outline='#ffffff', width=2)
                
                # Gate label
                self.canvas.create_text(x, y_pos, text=gate,
                                       fill='#000000', font=('Arial', 16, 'bold'))
    
    def run_circuit(self):
        """Run the quantum circuit and show results"""
        if not self.placed_gates:
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, "Add some gates first!\n")
            return
        
        try:
            # Determine circuit size
            num_qubits = 2 if self.gate in ['CNOT', 'CZ'] else 1
            qc = QuantumCircuit(num_qubits)
            
            # Set initial state based on gate
            if self.gate_info['input_state'] == '|1⟩':
                qc.x(0)
            elif self.gate_info['input_state'] == '|10⟩':
                qc.x(0)
            elif self.gate_info['input_state'] == '|11⟩':
                qc.x(0)
                qc.x(1)
            
            # Apply gates
            for gate in self.placed_gates:
                if gate == 'H':
                    qc.h(0)
                elif gate == 'X':
                    qc.x(0)
                elif gate == 'Y':
                    qc.y(0)
                elif gate == 'Z':
                    qc.z(0)
                elif gate == 'S':
                    qc.s(0)
                elif gate == 'T':
                    qc.t(0)
                elif gate == 'CNOT' and num_qubits > 1:
                    qc.cx(0, 1)
                elif gate == 'CZ' and num_qubits > 1:
                    qc.cz(0, 1)
            
            # Get final state
            final_state = Statevector(qc)
            
            # Display results
            self.display_results(final_state.data, num_qubits)
            
        except Exception as e:
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, f"Error: {str(e)}\n")
    
    def display_results(self, state_vector, num_qubits):
        """Display the quantum state results"""
        self.results_text.delete(1.0, tk.END)
        
        self.results_text.insert(tk.END, f"Initial State: {self.gate_info['input_state']}\n")
        self.results_text.insert(tk.END, f"Gates Applied: {' → '.join(self.placed_gates)}\n")
        self.results_text.insert(tk.END, "-" * 50 + "\n")
        
        self.results_text.insert(tk.END, f"Final State Vector:\n")
        for i, amplitude in enumerate(state_vector):
            if abs(amplitude) > 0.001:
                basis_state = f"|{i:0{num_qubits}b}⟩"
                real_part = amplitude.real
                imag_part = amplitude.imag
                
                if abs(imag_part) < 0.001:
                    self.results_text.insert(tk.END, f"{basis_state}: {real_part:.3f}\n")
                else:
                    self.results_text.insert(tk.END, f"{basis_state}: {real_part:.3f} + {imag_part:.3f}i\n")
        
        self.results_text.insert(tk.END, f"\nProbabilities:\n")
        for i, amplitude in enumerate(state_vector):
            probability = abs(amplitude) ** 2
            if probability > 0.001:
                basis_state = f"|{i:0{num_qubits}b}⟩"
                self.results_text.insert(tk.END, f"{basis_state}: {probability:.3f} ({probability*100:.1f}%)\n")
    
    def display_initial_info(self):
        """Display initial information"""
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, f"Gate: {self.gate_info['name']}\n")
        self.results_text.insert(tk.END, f"Description: {self.gate_info['description']}\n")
        self.results_text.insert(tk.END, f"Example: {self.gate_info['example']}\n")
        self.results_text.insert(tk.END, "-" * 50 + "\n")
        self.results_text.insert(tk.END, "Click 'Add Gate' to place the gate on the circuit,\n")
        self.results_text.insert(tk.END, "then click 'Run Circuit' to see the results!\n")
    
    def play_sound(self, sound_name):
        """Play sound if available"""
        if self.sound_enabled and hasattr(self, 'sounds') and sound_name in self.sounds:
            try:
                if self.sounds[sound_name]:
                    self.sounds[sound_name].play()
            except:
                pass

def show_tutorial(parent, return_callback=None):
    """Show the tutorial window"""
    TutorialWindow(parent, return_callback)