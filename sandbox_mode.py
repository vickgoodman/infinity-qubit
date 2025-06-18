import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
import pygame

class SandboxMode:
    def __init__(self, root):
        self.root = root
        self.root.title("Quantum Sandbox Mode")
        
        # Initialize sound system (optional - can reuse from main)
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            self.sound_enabled = True
        except:
            self.sound_enabled = False
        
        # Get screen dimensions for adaptive sizing
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        window_width = int(screen_width * 0.8)
        window_height = int(screen_height * 0.8)
        
        # Center the window
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.configure(bg='#1a1a1a')
        
        # Store dimensions
        self.window_width = window_width
        self.window_height = window_height
        
        # Sandbox state
        self.num_qubits = 1
        self.placed_gates = []
        self.initial_state = "|0⟩"
        self.available_gates = ["H", "X", "Y", "Z", "S", "T", "CNOT", "CZ", "Toffoli"]
        
        # Setup UI
        self.setup_ui()
        self.update_circuit_display()
    
    def setup_ui(self):
        """Setup the sandbox UI"""
        # Main container
        main_frame = tk.Frame(self.root, bg='#1a1a1a')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_font_size = max(18, int(self.window_width / 70))
        title_label = tk.Label(main_frame, text="🛠️ Quantum Circuit Sandbox",
                              font=('Arial', title_font_size, 'bold'), 
                              fg='#f39c12', bg='#1a1a1a')
        title_label.pack(pady=(0, 20))
        
        # Control panel
        self.setup_control_panel(main_frame)
        
        # Circuit display area
        self.setup_circuit_area(main_frame)
        
        # Action buttons
        self.setup_action_buttons(main_frame)
        
        # Results area
        self.setup_results_area(main_frame)
    
    def setup_control_panel(self, parent):
        """Setup the control panel for qubits and initial state"""
        control_frame = tk.Frame(parent, bg='#2a2a2a', relief=tk.RAISED, bd=2)
        control_frame.pack(fill=tk.X, pady=(0, 15))
        
        control_title = tk.Label(control_frame, text="Circuit Configuration",
                                font=('Arial', 14, 'bold'), fg='#00ff88', bg='#2a2a2a')
        control_title.pack(pady=(10, 5))
        
        # Qubit controls
        qubit_frame = tk.Frame(control_frame, bg='#2a2a2a')
        qubit_frame.pack(pady=10)
        
        tk.Label(qubit_frame, text="Number of Qubits:", 
                font=('Arial', 12), fg='#ffffff', bg='#2a2a2a').pack(side=tk.LEFT, padx=(20, 5))
        
        self.qubit_var = tk.IntVar(value=1)
        qubit_spinbox = tk.Spinbox(qubit_frame, from_=1, to=4, textvariable=self.qubit_var,
                                  command=self.on_qubit_change, font=('Arial', 12), width=5)
        qubit_spinbox.pack(side=tk.LEFT, padx=5)
        
        # Initial state selection
        state_frame = tk.Frame(control_frame, bg='#2a2a2a')
        state_frame.pack(pady=10)
        
        tk.Label(state_frame, text="Initial State:", 
                font=('Arial', 12), fg='#ffffff', bg='#2a2a2a').pack(side=tk.LEFT, padx=(20, 5))
        
        self.state_var = tk.StringVar(value="|0⟩")
        state_options = ["|0⟩", "|1⟩", "|+⟩", "|-⟩", "|0⟩⊗|0⟩", "|0⟩⊗|1⟩", "|1⟩⊗|0⟩", "|1⟩⊗|1⟩"]
        state_combo = ttk.Combobox(state_frame, textvariable=self.state_var, 
                                  values=state_options, state="readonly", font=('Arial', 11))
        state_combo.pack(side=tk.LEFT, padx=5)
        state_combo.bind('<<ComboboxSelected>>', self.on_state_change)
    
    def setup_circuit_area(self, parent):
        """Setup the circuit visualization area"""
        circuit_frame = tk.Frame(parent, bg='#2a2a2a', relief=tk.RAISED, bd=2)
        circuit_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        circuit_title = tk.Label(circuit_frame, text="Quantum Circuit",
                                font=('Arial', 14, 'bold'), fg='#00ff88', bg='#2a2a2a')
        circuit_title.pack(pady=(10, 5))
        
        # Circuit canvas
        canvas_width = int(self.window_width * 0.9)
        canvas_height = int(self.window_height * 0.4)
        
        self.circuit_canvas = tk.Canvas(circuit_frame, width=canvas_width, height=canvas_height,
                                       bg='#1a1a1a', highlightthickness=0)
        self.circuit_canvas.pack(pady=10)
        
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        
        # Available gates
        self.setup_gate_panel(circuit_frame)
    
    def setup_gate_panel(self, parent):
        """Setup the gate selection panel"""
        gate_frame = tk.Frame(parent, bg='#2a2a2a')
        gate_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(gate_frame, text="Available Gates:", 
                font=('Arial', 12, 'bold'), fg='#ffffff', bg='#2a2a2a').pack(anchor=tk.W)
        
        # Gate buttons
        buttons_frame = tk.Frame(gate_frame, bg='#2a2a2a')
        buttons_frame.pack(fill=tk.X, pady=5)
        
        gate_colors = {
            'H': '#ff6b6b', 'X': '#4ecdc4', 'Y': '#45b7d1', 'Z': '#96ceb4',
            'S': '#feca57', 'T': '#ff9ff3', 'CNOT': '#ffeaa7', 'CZ': '#a29bfe',
            'Toffoli': '#fd79a8'
        }
        
        for gate in self.available_gates:
            color = gate_colors.get(gate, '#ffffff')
            btn = tk.Button(buttons_frame, text=gate,
                           command=lambda g=gate: self.add_gate(g),
                           font=('Arial', 10, 'bold'), bg=color, fg='#000000',
                           width=8, height=1)
            btn.pack(side=tk.LEFT, padx=3, pady=2)
    
    def setup_action_buttons(self, parent):
        """Setup action buttons"""
        action_frame = tk.Frame(parent, bg='#1a1a1a')
        action_frame.pack(pady=10)
        
        btn_font = ('Arial', 12, 'bold')
        btn_pady = 8
        btn_padx = 20
        
        run_btn = tk.Button(action_frame, text="🚀 Run Circuit",
                           command=self.run_circuit, font=btn_font,
                           bg='#00ff88', fg='#000000', padx=btn_padx, pady=btn_pady)
        run_btn.pack(side=tk.LEFT, padx=10)
        
        clear_btn = tk.Button(action_frame, text="🔄 Clear Circuit",
                             command=self.clear_circuit, font=btn_font,
                             bg='#ff6b6b', fg='#ffffff', padx=btn_padx, pady=btn_pady)
        clear_btn.pack(side=tk.LEFT, padx=10)
        
        undo_btn = tk.Button(action_frame, text="↶ Undo",
                            command=self.undo_gate, font=btn_font,
                            bg='#f39c12', fg='#000000', padx=btn_padx, pady=btn_pady)
        undo_btn.pack(side=tk.LEFT, padx=10)
    
    def setup_results_area(self, parent):
        """Setup the results display area"""
        results_frame = tk.Frame(parent, bg='#2a2a2a', relief=tk.RAISED, bd=2)
        results_frame.pack(fill=tk.X)
        
        results_title = tk.Label(results_frame, text="Quantum State Results",
                                font=('Arial', 14, 'bold'), fg='#00ff88', bg='#2a2a2a')
        results_title.pack(pady=(10, 5))
        
        # Results text display
        self.results_text = tk.Text(results_frame, height=8, width=80,
                                   font=('Courier', 10), bg='#1a1a1a', fg='#00ff88',
                                   relief=tk.SUNKEN, bd=2)
        self.results_text.pack(pady=10, padx=20)
    
    def add_gate(self, gate):
        """Add a gate to the circuit"""
        # For multi-qubit gates, we need to specify which qubits
        if gate in ['CNOT', 'CZ'] and self.num_qubits < 2:
            messagebox.showwarning("Warning", f"{gate} gate requires at least 2 qubits")
            return
        elif gate == 'Toffoli' and self.num_qubits < 3:
            messagebox.showwarning("Warning", "Toffoli gate requires at least 3 qubits")
            return
        
        # For simplicity, apply multi-qubit gates to consecutive qubits
        if gate in ['CNOT', 'CZ']:
            self.placed_gates.append((gate, [0, 1]))
        elif gate == 'Toffoli':
            self.placed_gates.append((gate, [0, 1, 2]))
        else:
            # Single qubit gate - apply to first qubit by default
            # In a more advanced version, you could let users select the target qubit
            self.placed_gates.append((gate, [0]))
        
        self.update_circuit_display()
        
        # Play sound if available
        if self.sound_enabled:
            try:
                # Create a simple beep for gate placement
                frequency = 440
                duration = 0.1
                sample_rate = 22050
                frames = int(duration * sample_rate)
                arr = np.sin(2 * np.pi * frequency * np.linspace(0, duration, frames))
                arr = (arr * 16383).astype(np.int16)
                sound = pygame.sndarray.make_sound(arr)
                sound.set_volume(0.3)
                sound.play()
            except:
                pass
    
    def clear_circuit(self):
        """Clear all gates from the circuit"""
        self.placed_gates = []
        self.update_circuit_display()
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, "Circuit cleared. Ready for new gates.\n")
    
    def undo_gate(self):
        """Remove the last placed gate"""
        if self.placed_gates:
            self.placed_gates.pop()
            self.update_circuit_display()
    
    def on_qubit_change(self):
        """Handle change in number of qubits"""
        self.num_qubits = self.qubit_var.get()
        self.placed_gates = []  # Clear gates when changing qubit count
        self.update_circuit_display()
        
        # Update available initial states based on qubit count
        if self.num_qubits == 1:
            states = ["|0⟩", "|1⟩", "|+⟩", "|-⟩"]
        elif self.num_qubits == 2:
            states = ["|00⟩", "|01⟩", "|10⟩", "|11⟩", "|++⟩"]
        else:
            states = ["|000⟩", "|001⟩", "|010⟩", "|011⟩", "|100⟩", "|101⟩", "|110⟩", "|111⟩"]
        
        # Update state combobox (you'd need to store a reference to it)
        # For now, just reset to |0⟩
        self.state_var.set(states[0])
    
    def on_state_change(self, event=None):
        """Handle change in initial state"""
        self.initial_state = self.state_var.get()
        self.update_circuit_display()
    
    def update_circuit_display(self):
        """Update the circuit visualization"""
        self.circuit_canvas.delete("all")
        
        if self.num_qubits == 0:
            return
        
        # Circuit drawing parameters
        wire_start = 50
        wire_end = self.canvas_width - 50
        qubit_spacing = self.canvas_height // (self.num_qubits + 1)
        
        # Draw qubit wires
        for qubit in range(self.num_qubits):
            y_pos = (qubit + 1) * qubit_spacing
            
            # Draw wire
            self.circuit_canvas.create_line(wire_start, y_pos, wire_end, y_pos,
                                           fill='#ffffff', width=2)
            
            # Qubit label
            self.circuit_canvas.create_text(wire_start - 20, y_pos,
                                           text=f"q{qubit}", fill='#ffffff',
                                           font=('Arial', 10, 'bold'))
        
        # Draw gates
        gate_x_start = wire_start + 80
        gate_spacing = 120
        
        for i, (gate, qubits) in enumerate(self.placed_gates):
            x = gate_x_start + i * gate_spacing
            
            if len(qubits) == 1:
                # Single qubit gate
                qubit = qubits[0]
                if qubit < self.num_qubits:
                    y_pos = (qubit + 1) * qubit_spacing
                    
                    # Gate box
                    self.circuit_canvas.create_rectangle(x - 25, y_pos - 20,
                                                        x + 25, y_pos + 20,
                                                        fill='#4ecdc4', outline='#ffffff', width=2)
                    
                    # Gate label
                    self.circuit_canvas.create_text(x, y_pos, text=gate,
                                                   fill='#000000', font=('Arial', 12, 'bold'))
            
            elif len(qubits) == 2 and gate in ['CNOT', 'CZ']:
                # Two-qubit gate
                control_qubit, target_qubit = qubits
                if control_qubit < self.num_qubits and target_qubit < self.num_qubits:
                    control_y = (control_qubit + 1) * qubit_spacing
                    target_y = (target_qubit + 1) * qubit_spacing
                    
                    # Control dot
                    self.circuit_canvas.create_oval(x - 8, control_y - 8,
                                                   x + 8, control_y + 8,
                                                   fill='#ffffff', outline='#ffffff')
                    
                    # Connection line
                    self.circuit_canvas.create_line(x, control_y, x, target_y,
                                                   fill='#ffffff', width=2)
                    
                    if gate == 'CNOT':
                        # Target (X symbol)
                        self.circuit_canvas.create_oval(x - 15, target_y - 15,
                                                       x + 15, target_y + 15,
                                                       fill='', outline='#ffffff', width=2)
                        self.circuit_canvas.create_line(x - 10, target_y - 10,
                                                       x + 10, target_y + 10,
                                                       fill='#ffffff', width=2)
                        self.circuit_canvas.create_line(x - 10, target_y + 10,
                                                       x + 10, target_y - 10,
                                                       fill='#ffffff', width=2)
                    elif gate == 'CZ':
                        # Target (Z symbol)
                        self.circuit_canvas.create_oval(x - 8, target_y - 8,
                                                       x + 8, target_y + 8,
                                                       fill='#ffffff', outline='#ffffff')
    
    def run_circuit(self):
        """Execute the quantum circuit and display results"""
        try:
            # Create quantum circuit
            qc = QuantumCircuit(self.num_qubits)
            
            # Set initial state
            self.set_initial_state(qc)
            
            # Apply gates
            for gate, qubits in self.placed_gates:
                if gate == 'H' and len(qubits) == 1:
                    qc.h(qubits[0])
                elif gate == 'X' and len(qubits) == 1:
                    qc.x(qubits[0])
                elif gate == 'Y' and len(qubits) == 1:
                    qc.y(qubits[0])
                elif gate == 'Z' and len(qubits) == 1:
                    qc.z(qubits[0])
                elif gate == 'S' and len(qubits) == 1:
                    qc.s(qubits[0])
                elif gate == 'T' and len(qubits) == 1:
                    qc.t(qubits[0])
                elif gate == 'CNOT' and len(qubits) == 2:
                    qc.cx(qubits[0], qubits[1])
                elif gate == 'CZ' and len(qubits) == 2:
                    qc.cz(qubits[0], qubits[1])
                elif gate == 'Toffoli' and len(qubits) == 3:
                    qc.ccx(qubits[0], qubits[1], qubits[2])
            
            # Get final state
            final_state = Statevector(qc)
            
            # Display results
            self.display_results(final_state)
            
        except Exception as e:
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, f"Error executing circuit: {str(e)}\n")
    
    def set_initial_state(self, qc):
        """Set the initial state of the quantum circuit"""
        state = self.initial_state
        
        if state == "|1⟩" and self.num_qubits >= 1:
            qc.x(0)
        elif state == "|+⟩" and self.num_qubits >= 1:
            qc.h(0)
        elif state == "|-⟩" and self.num_qubits >= 1:
            qc.x(0)
            qc.h(0)
        elif state == "|01⟩" and self.num_qubits >= 2:
            qc.x(1)
        elif state == "|10⟩" and self.num_qubits >= 2:
            qc.x(0)
        elif state == "|11⟩" and self.num_qubits >= 2:
            qc.x(0)
            qc.x(1)
        elif state == "|++⟩" and self.num_qubits >= 2:
            qc.h(0)
            qc.h(1)
        # Add more initial states as needed
    
    def display_results(self, state_vector):
        """Display the quantum state results"""
        self.results_text.delete(1.0, tk.END)
        
        # Circuit summary
        self.results_text.insert(tk.END, f"Circuit Summary:\n")
        self.results_text.insert(tk.END, f"Qubits: {self.num_qubits}\n")
        self.results_text.insert(tk.END, f"Gates: {len(self.placed_gates)}\n")
        self.results_text.insert(tk.END, f"Initial State: {self.initial_state}\n")
        self.results_text.insert(tk.END, "-" * 50 + "\n\n")
        
        # State vector
        self.results_text.insert(tk.END, "Final State Vector:\n")
        state_data = state_vector.data
        
        for i, amplitude in enumerate(state_data):
            if abs(amplitude) > 0.001:  # Only show significant amplitudes
                basis_state = format(i, f'0{self.num_qubits}b')
                prob = abs(amplitude) ** 2
                self.results_text.insert(tk.END, 
                    f"|{basis_state}⟩: {amplitude:.4f} (probability: {prob:.4f})\n")
        
        self.results_text.insert(tk.END, "\n")
        
        # Probabilities
        self.results_text.insert(tk.END, "Measurement Probabilities:\n")
        for i, amplitude in enumerate(state_data):
            prob = abs(amplitude) ** 2
            if prob > 0.001:
                basis_state = format(i, f'0{self.num_qubits}b')
                self.results_text.insert(tk.END, f"|{basis_state}⟩: {prob:.1%}\n")

def main():
    """For testing the sandbox independently"""
    root = tk.Tk()
    app = SandboxMode(root)
    root.mainloop()

if __name__ == "__main__":
    main()