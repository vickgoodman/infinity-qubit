import tkinter as tk
from tkinter import ttk, messagebox
import json
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
import pygame
from PIL import Image, ImageTk

class PuzzleMode:
    def __init__(self, root):
        self.root = root
        self.root.title("🧩 Infinity Qubit - Puzzle Mode")

        # Initialize pygame mixer for sound
        try:
            pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
            self.sound_enabled = True
            self.load_sounds()
        except pygame.error:
            print("Warning: Could not initialize sound system")
            self.sound_enabled = False

        # Get screen dimensions and set adaptive window size
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        window_width = int(screen_width * 0.8)
        window_height = int(screen_height * 0.75)

        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.configure(bg='#1a1a1a')

        self.window_width = window_width
        self.window_height = window_height

        # Game state
        self.current_level = 0
        self.placed_gates = []
        self.score = 0
        self.levels = self.create_puzzle_levels()
        self.max_gates_used = {}  # Track efficiency

        # Initialize UI
        self.setup_ui()
        self.load_level(self.current_level)

    def load_sounds(self):
        """Load sound effects"""
        self.sounds = {}
        sound_files = {
            'H': 'sounds/hadamard.wav',
            'X': 'sounds/pauli_x.wav',
            'Y': 'sounds/click.wav',
            'Z': 'sounds/pauli_z.wav',
            'S': 'sounds/click.wav',
            'T': 'sounds/click.wav',
            'CNOT': 'sounds/cnot.wav',
            'CZ': 'sounds/click.wav',
            'run_circuit': 'sounds/run_circuit.wav',
            'clear': 'sounds/clear.wav',
            'hint': 'sounds/hint.wav',
            'success': 'sounds/success.wav',
            'error': 'sounds/error.wav',
            'level_up': 'sounds/level_up.wav',
            'button_click': 'sounds/click.wav',
            'game_complete': 'sounds/victory.wav'
        }

        for sound_name, file_path in sound_files.items():
            try:
                self.sounds[sound_name] = pygame.mixer.Sound(file_path)
                self.sounds[sound_name].set_volume(0.6)
            except pygame.error:
                self.sounds[sound_name] = None

    def play_sound(self, sound_name):
        """Play a sound effect"""
        if self.sound_enabled and sound_name in self.sounds and self.sounds[sound_name]:
            try:
                self.sounds[sound_name].play()
            except pygame.error:
                pass

    def create_puzzle_levels(self):
        """Create comprehensive puzzle levels with increasing difficulty"""
        levels = [
            # Beginner Level (1-5) - Single Qubit Basics
            {
                "name": "Quantum Flip",
                "description": "Transform |0⟩ into |1⟩",
                "input_state": "|0⟩",
                "target_state": "|1⟩",
                "available_gates": ["H", "X", "Y", "Z"],
                "qubits": 1,
                "hint": "The X gate (Pauli-X) flips |0⟩ to |1⟩",
                "max_gates": 1,
                "difficulty": "Beginner"
            },
            {
                "name": "First Superposition",
                "description": "Create |+⟩ state from |0⟩",
                "input_state": "|0⟩",
                "target_state": "|+⟩",
                "available_gates": ["H", "X", "Y", "Z"],
                "qubits": 1,
                "hint": "The Hadamard gate creates equal superposition",
                "max_gates": 1,
                "difficulty": "Beginner"
            },
            {
                "name": "Phase Flip Challenge",
                "description": "Transform |+⟩ into |-⟩",
                "input_state": "|+⟩",
                "target_state": "|-⟩",
                "available_gates": ["H", "X", "Y", "Z"],
                "qubits": 1,
                "hint": "The Z gate adds a phase flip to |+⟩",
                "max_gates": 1,
                "difficulty": "Beginner"
            },
            {
                "name": "Y-Gate Mystery",
                "description": "Apply Y gate to |0⟩",
                "input_state": "|0⟩",
                "target_state": "|i·1⟩",
                "available_gates": ["H", "X", "Y", "Z"],
                "qubits": 1,
                "hint": "Y gate combines X and Z operations with a phase",
                "max_gates": 1,
                "difficulty": "Beginner"
            },
            {
                "name": "Return to Zero",
                "description": "Bring |1⟩ back to |0⟩",
                "input_state": "|1⟩",
                "target_state": "|0⟩",
                "available_gates": ["H", "X", "Y", "Z"],
                "qubits": 1,
                "hint": "X gate is its own inverse",
                "max_gates": 1,
                "difficulty": "Beginner"
            },
            
            # Intermediate Level (6-15) - Single Qubit Combinations + Phase Gates
            {
                "name": "Double Hadamard",
                "description": "Apply H twice to |0⟩",
                "input_state": "|0⟩",
                "target_state": "|0⟩",
                "available_gates": ["H", "X", "Y", "Z"],
                "qubits": 1,
                "hint": "H·H = I (identity). Two Hadamards cancel out",
                "max_gates": 2,
                "difficulty": "Intermediate"
            },
            {
                "name": "Phase Gate Introduction",
                "description": "Transform |+⟩ using S gate",
                "input_state": "|+⟩",
                "target_state": "|+i⟩",
                "available_gates": ["H", "X", "Y", "Z", "S"],
                "qubits": 1,
                "hint": "S gate adds π/2 phase to |1⟩ component",
                "max_gates": 1,
                "difficulty": "Intermediate"
            },
            {
                "name": "T Gate Challenge",
                "description": "Apply T gate to superposition",
                "input_state": "|+⟩",
                "target_state": "|T+⟩",
                "available_gates": ["H", "X", "Y", "Z", "S", "T"],
                "qubits": 1,
                "hint": "T gate adds π/4 phase to |1⟩ component",
                "max_gates": 1,
                "difficulty": "Intermediate"
            },
            {
                "name": "Complex Sequence",
                "description": "Transform |0⟩ to |-⟩ via |1⟩",
                "input_state": "|0⟩",
                "target_state": "|-⟩",
                "available_gates": ["H", "X", "Y", "Z"],
                "qubits": 1,
                "hint": "Think: |0⟩ → |1⟩ → |-⟩. What gates do this?",
                "max_gates": 2,
                "difficulty": "Intermediate"
            },
            {
                "name": "Phase Correction",
                "description": "Fix the phase of |i·1⟩ to get |1⟩",
                "input_state": "|i·1⟩",
                "target_state": "|1⟩",
                "available_gates": ["H", "X", "Y", "Z", "S"],
                "qubits": 1,
                "hint": "You need to remove the i phase from |1⟩",
                "max_gates": 2,
                "difficulty": "Intermediate"
            },
            
            # Two-Qubit Fundamentals (11-20)
            {
                "name": "First Bell State",
                "description": "Create |Φ+⟩ from |00⟩",
                "input_state": "|00⟩",
                "target_state": "|Φ+⟩",
                "available_gates": ["H", "X", "CNOT"],
                "qubits": 2,
                "hint": "Apply H to first qubit, then CNOT(0,1)",
                "max_gates": 2,
                "difficulty": "Intermediate"
            },
            {
                "name": "Bell State Φ-",
                "description": "Create |Φ-⟩ Bell state",
                "input_state": "|00⟩",
                "target_state": "|Φ-⟩",
                "available_gates": ["H", "X", "Z", "CNOT"],
                "qubits": 2,
                "hint": "Similar to |Φ+⟩ but with a phase flip",
                "max_gates": 3,
                "difficulty": "Intermediate"
            },
            {
                "name": "Bell State Ψ+",
                "description": "Create |Ψ+⟩ Bell state",
                "input_state": "|00⟩",
                "target_state": "|Ψ+⟩",
                "available_gates": ["H", "X", "CNOT"],
                "qubits": 2,
                "hint": "Flip one qubit before creating entanglement",
                "max_gates": 3,
                "difficulty": "Intermediate"
            },
            {
                "name": "Bell State Ψ-",
                "description": "Create |Ψ-⟩ Bell state",
                "input_state": "|00⟩",
                "target_state": "|Ψ-⟩",
                "available_gates": ["H", "X", "Z", "CNOT"],
                "qubits": 2,
                "hint": "Combine X flip and phase operations with entanglement",
                "max_gates": 4,
                "difficulty": "Intermediate"
            },
            {
                "name": "Controlled Operations",
                "description": "Use CNOT to flip second qubit when first is |1⟩",
                "input_state": "|10⟩",
                "target_state": "|11⟩",
                "available_gates": ["H", "X", "CNOT"],
                "qubits": 2,
                "hint": "CNOT flips target when control is |1⟩",
                "max_gates": 1,
                "difficulty": "Intermediate"
            },
            
            # Advanced Single & Two-Qubit (16-25)
            {
                "name": "Superposition Distribution",
                "description": "Create |++⟩ from |00⟩",
                "input_state": "|00⟩",
                "target_state": "|++⟩",
                "available_gates": ["H", "X", "Y", "Z"],
                "qubits": 2,
                "hint": "Apply H to both qubits independently",
                "max_gates": 2,
                "difficulty": "Advanced"
            },
            {
                "name": "Entanglement Destruction",
                "description": "Disentangle |Φ+⟩ back to |00⟩",
                "input_state": "|Φ+⟩",
                "target_state": "|00⟩",
                "available_gates": ["H", "X", "CNOT"],
                "qubits": 2,
                "hint": "Reverse the Bell state creation process",
                "max_gates": 2,
                "difficulty": "Advanced"
            },
            {
                "name": "Quantum Teleportation Setup",
                "description": "Prepare entangled resource |Φ+⟩ on qubits 1,2",
                "input_state": "|000⟩",
                "target_state": "|0Φ+⟩",
                "available_gates": ["H", "X", "CNOT"],
                "qubits": 3,
                "hint": "Leave first qubit alone, entangle qubits 1 and 2",
                "max_gates": 2,
                "difficulty": "Advanced"
            },
            {
                "name": "GHZ State Creation",
                "description": "Create 3-qubit GHZ state",
                "input_state": "|000⟩",
                "target_state": "|GHZ⟩",
                "available_gates": ["H", "X", "CNOT"],
                "qubits": 3,
                "hint": "H on first qubit, then CNOT to others",
                "max_gates": 3,
                "difficulty": "Advanced"
            },
            {
                "name": "Controlled-Z Operation",
                "description": "Apply phase flip between entangled qubits",
                "input_state": "|Φ+⟩",
                "target_state": "|Φ-⟩",
                "available_gates": ["H", "X", "Z", "CZ", "CNOT"],
                "qubits": 2,
                "hint": "CZ gate adds phase when both qubits are |1⟩",
                "max_gates": 1,
                "difficulty": "Advanced"
            },
            
            # Expert Level (21-30) - Complex Multi-Qubit
            {
                "name": "W State Creation",
                "description": "Create 3-qubit W state from |000⟩",
                "input_state": "|000⟩",
                "target_state": "|W⟩",
                "available_gates": ["H", "X", "Y", "CNOT", "Toffoli"],
                "qubits": 3,
                "hint": "W state is symmetric superposition of all single-excitation states",
                "max_gates": 6,
                "difficulty": "Expert"
            },
            {
                "name": "Quantum Error Syndrome",
                "description": "Create error detection pattern",
                "input_state": "|000⟩",
                "target_state": "|err⟩",
                "available_gates": ["H", "X", "CNOT", "Toffoli"],
                "qubits": 3,
                "hint": "Use auxiliary qubits to detect bit flip errors",
                "max_gates": 4,
                "difficulty": "Expert"
            },
            {
                "name": "Quantum Fourier Transform",
                "description": "Apply 2-qubit QFT",
                "input_state": "|00⟩",
                "target_state": "|QFT⟩",
                "available_gates": ["H", "S", "T", "CNOT"],
                "qubits": 2,
                "hint": "H on first qubit, controlled phase operations",
                "max_gates": 3,
                "difficulty": "Expert"
            },
            {
                "name": "Toffoli Gate Demo",
                "description": "Flip third qubit only when first two are |11⟩",
                "input_state": "|110⟩",
                "target_state": "|111⟩",
                "available_gates": ["H", "X", "CNOT", "Toffoli"],
                "qubits": 3,
                "hint": "Toffoli gate performs controlled-controlled-X",
                "max_gates": 1,
                "difficulty": "Expert"
            },
            {
                "name": "Quantum Supremacy Circuit",
                "description": "Create maximally entangled 4-qubit state",
                "input_state": "|0000⟩",
                "target_state": "|MaxEnt⟩",
                "available_gates": ["H", "X", "Y", "Z", "CNOT", "CZ", "Toffoli"],
                "qubits": 4,
                "hint": "Use multiple layers of Hadamard and entangling gates",
                "max_gates": 8,
                "difficulty": "Expert"
            },
            
            # Master Level (26-35) - Ultimate Challenges
            {
                "name": "Quantum Secret Sharing",
                "description": "Encode secret in 3-qubit state",
                "input_state": "|000⟩",
                "target_state": "|Secret⟩",
                "available_gates": ["H", "X", "Y", "Z", "S", "T", "CNOT", "CZ", "Toffoli"],
                "qubits": 3,
                "hint": "Create state where no single qubit reveals the secret",
                "max_gates": 10,
                "difficulty": "Master"
            },
            {
                "name": "Quantum Phase Kickback",
                "description": "Demonstrate phase kickback with ancilla",
                "input_state": "|+0⟩",
                "target_state": "|-0⟩",
                "available_gates": ["H", "X", "Z", "S", "CNOT"],
                "qubits": 2,
                "hint": "Use controlled operation to transfer phase",
                "max_gates": 3,
                "difficulty": "Master"
            },
            {
                "name": "Quantum Interference",
                "description": "Create destructive interference pattern",
                "input_state": "|00⟩",
                "target_state": "|Interference⟩",
                "available_gates": ["H", "X", "Y", "Z", "S", "T", "CNOT"],
                "qubits": 2,
                "hint": "Use multiple paths that interfere destructively",
                "max_gates": 6,
                "difficulty": "Master"
            },
            {
                "name": "Quantum Error Correction",
                "description": "Implement 3-qubit bit flip code",
                "input_state": "|000⟩",
                "target_state": "|ErrorCode⟩",
                "available_gates": ["H", "X", "CNOT", "Toffoli"],
                "qubits": 3,
                "hint": "Encode logical |0⟩ in physical |000⟩",
                "max_gates": 5,
                "difficulty": "Master"
            },
            {
                "name": "Ultimate Challenge",
                "description": "Create the most complex quantum state",
                "input_state": "|0000⟩",
                "target_state": "|Ultimate⟩",
                "available_gates": ["H", "X", "Y", "Z", "S", "T", "CNOT", "CZ", "Toffoli"],
                "qubits": 4,
                "hint": "Use every gate type in a meaningful sequence",
                "max_gates": 15,
                "difficulty": "Master"
            }
        ]
        
        return levels

    def setup_ui(self):
        """Setup the user interface"""
        # Main frame with background
        try:
            bg_image = Image.open("Quantum_Background.jpg")
            bg_photo = ImageTk.PhotoImage(bg_image)
            main_frame = tk.Frame(self.root)
            main_frame.pack(fill='both', expand=True)
            bg_label = tk.Label(main_frame, image=bg_photo)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            main_frame.bg_photo = bg_photo
        except:
            main_frame = tk.Frame(self.root, bg='#1a1a1a')
            main_frame.pack(fill=tk.BOTH, expand=True)

        # Adaptive font sizes
        title_font_size = max(16, int(self.window_width / 80))
        header_font_size = max(12, int(self.window_width / 120))
        normal_font_size = max(10, int(self.window_width / 160))

        # Title and info
        title_label = tk.Label(main_frame, text="🧩 Infinity Qubit - Puzzle Mode",
                            font=('Arial', title_font_size, 'bold'), fg='#ff6b6b', bg='#1a1a1a')
        title_label.pack(pady=(10, 5))

        # Level info with difficulty indicator
        info_frame = tk.Frame(main_frame, bg='#1a1a1a')
        info_frame.pack(pady=(0, 15))

        self.level_label = tk.Label(info_frame, text="Level: 1",
                                font=('Arial', header_font_size, 'bold'), fg='#ffffff', bg='#1a1a1a')
        self.level_label.pack(side=tk.LEFT, padx=20)

        self.difficulty_label = tk.Label(info_frame, text="Difficulty: Beginner",
                                      font=('Arial', header_font_size, 'bold'), fg='#4ecdc4', bg='#1a1a1a')
        self.difficulty_label.pack(side=tk.LEFT, padx=20)

        self.score_label = tk.Label(info_frame, text="Score: 0",
                                font=('Arial', header_font_size, 'bold'), fg='#ffd700', bg='#1a1a1a')
        self.score_label.pack(side=tk.LEFT, padx=20)

        # Circuit area
        circuit_frame = tk.Frame(main_frame, bg='#2a2a2a', relief=tk.RAISED, bd=3)
        circuit_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        circuit_title = tk.Label(circuit_frame, text="🔬 Quantum Circuit",
                                font=('Arial', header_font_size + 2, 'bold'), fg='#ff6b6b', bg='#1a1a1a')
        circuit_title.pack(pady=10)

        # Circuit canvas
        canvas_width = int(self.window_width * 0.85)
        canvas_height = int(self.window_height * 0.3)

        self.circuit_canvas = tk.Canvas(circuit_frame, width=canvas_width, height=canvas_height,
                                    bg='#1a1a1a', highlightthickness=0)
        self.circuit_canvas.pack(pady=10)

        self.canvas_width = canvas_width
        self.canvas_height = canvas_height

        # Available gates
        gates_label = tk.Label(main_frame, text="🎯 Available Quantum Gates",
                            font=('Arial', header_font_size, 'bold'), fg='#ffffff', bg='#1a1a1a')
        gates_label.pack(pady=(10, 5))

        self.gates_frame = tk.Frame(main_frame, bg='#1a1a1a')
        self.gates_frame.pack(pady=5)

        # Control buttons
        controls_frame = tk.Frame(main_frame, bg='#1a1a1a')
        controls_frame.pack(pady=10)

        button_font_size = max(10, int(self.window_width / 140))
        button_padx = max(15, int(self.window_width / 80))
        button_pady = max(5, int(self.window_height / 150))

        self.run_button = tk.Button(controls_frame, text="🚀 Run Circuit",
                                command=self.run_circuit, font=('Arial', button_font_size, 'bold'),
                                bg='#00ff88', fg='#000000', padx=button_padx, pady=button_pady)
        self.run_button.pack(side=tk.LEFT, padx=10)

        self.clear_button = tk.Button(controls_frame, text="🔄 Clear",
                                    command=self.clear_circuit, font=('Arial', button_font_size),
                                    bg='#ff6b6b', fg='#ffffff', padx=button_padx, pady=button_pady)
        self.clear_button.pack(side=tk.LEFT, padx=10)

        self.hint_button = tk.Button(controls_frame, text="💡 Hint",
                                    command=self.show_hint, font=('Arial', button_font_size),
                                    bg='#4ecdc4', fg='#000000', padx=button_padx, pady=button_pady)
        self.hint_button.pack(side=tk.LEFT, padx=10)

        # Add skip button for very difficult levels
        self.skip_button = tk.Button(controls_frame, text="⏭️ Skip Level",
                                   command=self.skip_level, font=('Arial', button_font_size),
                                   bg='#f39c12', fg='#000000', padx=button_padx, pady=button_pady)
        self.skip_button.pack(side=tk.LEFT, padx=10)

        # Status and state display
        status_frame = tk.Frame(main_frame, bg='#2a2a2a', relief=tk.RAISED, bd=3)
        status_frame.pack(fill=tk.X, pady=(10, 0))

        status_title = tk.Label(status_frame, text="📊 Quantum State Analysis",
                            font=('Arial', header_font_size, 'bold'), fg='#ff6b6b', bg='#2a2a2a')
        status_title.pack(pady=(10, 5))

        self.status_label = tk.Label(status_frame, text="Ready for advanced puzzles!",
                                    font=('Arial', normal_font_size + 1), fg='#ffffff', bg='#2a2a2a')
        self.status_label.pack(pady=5)

        text_height = max(6, int(self.window_height / 120))
        text_width = max(60, int(self.window_width / 18))

        self.state_display = tk.Text(status_frame, height=text_height, width=text_width,
                                    font=('Courier', 9), bg='#1a1a1a', fg='#00ff88',
                                    relief=tk.SUNKEN, bd=2)
        self.state_display.pack(pady=10, padx=20)

    def load_level(self, level_index):
        """Load a specific puzzle level"""
        if level_index >= len(self.levels):
            self.game_complete()
            return

        level = self.levels[level_index]
        self.current_level = level_index

        # Update UI
        self.level_label.config(text=f"Level: {level_index + 1}/{len(self.levels)}")
        self.difficulty_label.config(text=f"Difficulty: {level['difficulty']}")
        
        # Color code difficulty
        diff_colors = {
            'Beginner': '#4ecdc4',
            'Intermediate': '#f39c12', 
            'Advanced': '#e74c3c',
            'Expert': '#9b59b6',
            'Master': '#ff6b6b'
        }
        self.difficulty_label.config(fg=diff_colors.get(level['difficulty'], '#ffffff'))
        
        self.status_label.config(text=f"{level['name']}: {level['description']}")

        # Clear previous state
        self.placed_gates = []
        self.clear_circuit()

        # Setup available gates
        self.setup_gates(level['available_gates'])
        self.draw_circuit()
        self.display_states(level)

    def setup_gates(self, available_gates):
        """Setup available gate buttons"""
        for widget in self.gates_frame.winfo_children():
            widget.destroy()

        gate_colors = {
            'H': '#ff6b6b', 'X': '#4ecdc4', 'Y': '#45b7d1', 'Z': '#96ceb4',
            'S': '#feca57', 'T': '#ff9ff3', 'CNOT': '#ffeaa7', 'CZ': '#a29bfe',
            'Toffoli': '#fd79a8'
        }

        gate_font_size = max(10, int(self.window_width / 160))
        
        for gate in available_gates:
            color = gate_colors.get(gate, '#ffffff')
            btn = tk.Button(self.gates_frame, text=gate,
                        command=lambda g=gate: self.add_gate(g),
                        font=('Arial', gate_font_size, 'bold'), bg=color, fg='#000000',
                        width=6, height=1, relief=tk.RAISED, bd=3)
            btn.pack(side=tk.LEFT, padx=5)

    def add_gate(self, gate):
        """Add a gate to the circuit with qubit selection"""
        level = self.levels[self.current_level]
        max_allowed = level.get('max_gates', 20)
        
        if len(self.placed_gates) < max_allowed:
            if gate in ['H', 'X', 'Y', 'Z', 'S', 'T']:
                # For single-qubit gates, show qubit selection dialog
                self.show_qubit_selection_dialog(gate, level['qubits'])
            elif gate in ['CNOT', 'CZ'] and level['qubits'] > 1:
                # For two-qubit gates, show control/target selection
                self.show_two_qubit_selection_dialog(gate, level['qubits'])
            elif gate == 'Toffoli' and level['qubits'] > 2:
                # For Toffoli, show three-qubit selection
                self.show_toffoli_selection_dialog(gate, level['qubits'])
            else:
                self.placed_gates.append({'gate': gate, 'qubits': [0]})
                self.draw_circuit()
                self.play_sound(gate)
        else:
            messagebox.showwarning("Gate Limit", f"Maximum {max_allowed} gates allowed for this puzzle!")
            self.play_sound('error')

    def show_toffoli_selection_dialog(self, gate, num_qubits):
        """Show dialog to select control and target qubits for Toffoli gate"""
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Place {gate} Gate")
        dialog.geometry("450x400")
        dialog.configure(bg='#1a1a1a')
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(dialog, text=f"Select qubits for {gate} gate:",
                font=('Arial', 14, 'bold'), fg='#ffffff', bg='#1a1a1a').pack(pady=20)
        
        control1_var = tk.IntVar(value=0)
        control2_var = tk.IntVar(value=1 if num_qubits > 1 else 0)
        target_var = tk.IntVar(value=2 if num_qubits > 2 else 0)
        
        # Control qubit 1 selection
        tk.Label(dialog, text="Control Qubit 1:", font=('Arial', 12), 
                fg='#4ecdc4', bg='#1a1a1a').pack(pady=(10, 5))
        control1_frame = tk.Frame(dialog, bg='#1a1a1a')
        control1_frame.pack()
        
        for i in range(num_qubits):
            tk.Radiobutton(control1_frame, text=f"q{i}", variable=control1_var, value=i,
                        font=('Arial', 10), fg='#ffffff', bg='#1a1a1a').pack(side=tk.LEFT, padx=5)
        
        # Control qubit 2 selection
        tk.Label(dialog, text="Control Qubit 2:", font=('Arial', 12), 
                fg='#4ecdc4', bg='#1a1a1a').pack(pady=(20, 5))
        control2_frame = tk.Frame(dialog, bg='#1a1a1a')
        control2_frame.pack()
        
        for i in range(num_qubits):
            tk.Radiobutton(control2_frame, text=f"q{i}", variable=control2_var, value=i,
                        font=('Arial', 10), fg='#ffffff', bg='#1a1a1a').pack(side=tk.LEFT, padx=5)
        
        # Target qubit selection
        tk.Label(dialog, text="Target Qubit:", font=('Arial', 12), 
                fg='#ff6b6b', bg='#1a1a1a').pack(pady=(20, 5))
        target_frame = tk.Frame(dialog, bg='#1a1a1a')
        target_frame.pack()
        
        for i in range(num_qubits):
            tk.Radiobutton(target_frame, text=f"q{i}", variable=target_var, value=i,
                        font=('Arial', 10), fg='#ffffff', bg='#1a1a1a').pack(side=tk.LEFT, padx=5)
        
        def confirm_selection():
            control1 = control1_var.get()
            control2 = control2_var.get()
            target = target_var.get()
            
            if len(set([control1, control2, target])) == 3:
                self.placed_gates.append({'gate': gate, 'qubits': [control1, control2, target]})
                self.draw_circuit()
                self.play_sound(gate)
                dialog.destroy()
            else:
                messagebox.showerror("Invalid Selection", "All three qubits must be different!")
        
        tk.Button(dialog, text="Place Gate", command=confirm_selection,
                font=('Arial', 12, 'bold'), bg='#00ff88', fg='#000000',
                padx=20, pady=10).pack(pady=20)

    def show_qubit_selection_dialog(self, gate, num_qubits):
        """Show dialog to select which qubit to place the gate on"""
        if num_qubits == 1:
            # Only one qubit, no selection needed
            self.placed_gates.append({'gate': gate, 'qubits': [0]})
            self.draw_circuit()
            self.play_sound(gate)
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Place {gate} Gate")
        dialog.geometry("300x200")
        dialog.configure(bg='#1a1a1a')
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(dialog, text=f"Select qubit for {gate} gate:",
                font=('Arial', 14, 'bold'), fg='#ffffff', bg='#1a1a1a').pack(pady=20)
        
        selected_qubit = tk.IntVar(value=0)
        
        for i in range(num_qubits):
            tk.Radiobutton(dialog, text=f"Qubit {i}", variable=selected_qubit, value=i,
                        font=('Arial', 12), fg='#ffffff', bg='#1a1a1a',
                        selectcolor='#4ecdc4').pack(pady=5)
        
        def confirm_selection():
            self.placed_gates.append({'gate': gate, 'qubits': [selected_qubit.get()]})
            self.draw_circuit()
            self.play_sound(gate)
            dialog.destroy()
        
        tk.Button(dialog, text="Place Gate", command=confirm_selection,
                font=('Arial', 12, 'bold'), bg='#00ff88', fg='#000000',
                padx=20, pady=10).pack(pady=20)

    def show_two_qubit_selection_dialog(self, gate, num_qubits):
        """Show dialog to select control and target qubits for two-qubit gates"""
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Place {gate} Gate")
        dialog.geometry("400x300")
        dialog.configure(bg='#1a1a1a')
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(dialog, text=f"Select qubits for {gate} gate:",
                font=('Arial', 14, 'bold'), fg='#ffffff', bg='#1a1a1a').pack(pady=20)
        
        control_var = tk.IntVar(value=0)
        target_var = tk.IntVar(value=1 if num_qubits > 1 else 0)
        
        # Control qubit selection
        tk.Label(dialog, text="Control Qubit:", font=('Arial', 12), 
                fg='#4ecdc4', bg='#1a1a1a').pack(pady=(10, 5))
        control_frame = tk.Frame(dialog, bg='#1a1a1a')
        control_frame.pack()
        
        for i in range(num_qubits):
            tk.Radiobutton(control_frame, text=f"q{i}", variable=control_var, value=i,
                        font=('Arial', 10), fg='#ffffff', bg='#1a1a1a').pack(side=tk.LEFT, padx=5)
        
        # Target qubit selection
        tk.Label(dialog, text="Target Qubit:", font=('Arial', 12), 
                fg='#ff6b6b', bg='#1a1a1a').pack(pady=(20, 5))
        target_frame = tk.Frame(dialog, bg='#1a1a1a')
        target_frame.pack()
        
        for i in range(num_qubits):
            tk.Radiobutton(target_frame, text=f"q{i}", variable=target_var, value=i,
                        font=('Arial', 10), fg='#ffffff', bg='#1a1a1a').pack(side=tk.LEFT, padx=5)
        
        def confirm_selection():
            control = control_var.get()
            target = target_var.get()
            if control != target:
                self.placed_gates.append({'gate': gate, 'qubits': [control, target]})
                self.draw_circuit()
                self.play_sound(gate)
                dialog.destroy()
            else:
                messagebox.showerror("Invalid Selection", "Control and target qubits must be different!")
        
        tk.Button(dialog, text="Place Gate", command=confirm_selection,
                font=('Arial', 12, 'bold'), bg='#00ff88', fg='#000000',
                padx=20, pady=10).pack(pady=20)

    def clear_circuit(self):
        """Clear all placed gates"""
        self.placed_gates = []
        self.draw_circuit()
        self.play_sound('clear')

    def draw_circuit(self):
        """Draw the quantum circuit visualization"""
        self.circuit_canvas.delete("all")
        
        level = self.levels[self.current_level]
        num_qubits = level['qubits']
        
        # Adaptive dimensions
        wire_start = int(self.canvas_width * 0.12)
        wire_end = int(self.canvas_width * 0.88)
        circuit_height = self.canvas_height
        qubit_spacing = circuit_height // (num_qubits + 1)
        
        line_width = max(3, int(self.canvas_width / 300))
        font_size = max(12, int(self.canvas_width / 75))
        
        # Draw input/output sections
        input_x = wire_start - int(self.canvas_width * 0.05)
        output_x = wire_end + int(self.canvas_width * 0.05)
        margin_y = int(circuit_height * 0.1)
        
        self.circuit_canvas.create_line(input_x, margin_y, input_x, circuit_height - margin_y,
                                fill='#ff6b6b', width=line_width)
        self.circuit_canvas.create_text(input_x - int(self.canvas_width * 0.04), circuit_height // 2,
                                text="Input", fill='#ff6b6b',
                                font=('Arial', font_size, 'bold'), angle=90)
        
        self.circuit_canvas.create_line(output_x, margin_y, output_x, circuit_height - margin_y,
                                fill='#ff6b6b', width=line_width)
        self.circuit_canvas.create_text(output_x + int(self.canvas_width * 0.04), circuit_height // 2,
                                text="Output", fill='#ff6b6b',
                                font=('Arial', font_size, 'bold'), angle=90)
        
        # Draw quantum wires
        for qubit in range(num_qubits):
            y_pos = (qubit + 1) * qubit_spacing + margin_y
            self.circuit_canvas.create_line(wire_start, y_pos, wire_end, y_pos,
                                    fill='#ffffff', width=line_width)
            self.circuit_canvas.create_text(wire_start - int(self.canvas_width * 0.02), y_pos,
                                    text=f"q{qubit}", fill='#ffffff',
                                    font=('Arial', font_size - 2, 'bold'))
        
        # Draw gates
        gate_width = max(60, int(self.canvas_width / 18))
        gate_height = max(50, int(self.canvas_height / 10))
        gate_spacing = max(100, int(self.canvas_width / 15))
        gate_font_size = max(16, int(self.canvas_width / 80))
        
        for i, gate_info in enumerate(self.placed_gates):
            x = wire_start + int(self.canvas_width * 0.08) + i * gate_spacing
            
            # Handle both old format (string) and new format (dict)
            if isinstance(gate_info, str):
                gate = gate_info
                qubits = [0]  # Default to qubit 0 for backward compatibility
            else:
                gate = gate_info['gate']
                qubits = gate_info['qubits']
            
            if gate in ['CNOT', 'CZ'] and len(qubits) >= 2:
                self.draw_two_qubit_gate(x, qubit_spacing, margin_y, gate, qubits, line_width)
            elif gate == 'Toffoli' and len(qubits) >= 3:
                self.draw_toffoli_gate(x, qubit_spacing, margin_y, qubits, line_width)
            else:
                # Single qubit gates
                self.draw_single_qubit_gate(x, qubit_spacing, margin_y, gate, qubits[0],
                                        gate_width, gate_height, gate_font_size, line_width)

    def draw_single_qubit_gate(self, x, qubit_spacing, margin_y, gate, target_qubit, width, height, font_size, line_width):
        """Draw a single qubit gate"""
        y_pos = (target_qubit + 1) * qubit_spacing + margin_y
        
        gate_colors = {
            'H': '#ff6b6b', 'X': '#4ecdc4', 'Y': '#45b7d1', 'Z': '#96ceb4',
            'S': '#feca57', 'T': '#ff9ff3'
        }
        
        color = gate_colors.get(gate, '#ffffff')
        
        self.circuit_canvas.create_rectangle(x - width//2, y_pos - height//2,
                                    x + width//2, y_pos + height//2,
                                    fill=color, outline='#ffffff', width=line_width)
        
        self.circuit_canvas.create_text(x, y_pos, text=gate,
                                fill='#000000', font=('Arial', font_size, 'bold'))

    def draw_two_qubit_gate(self, x, qubit_spacing, margin_y, gate, qubits, line_width):
        """Draw a two-qubit gate (CNOT or CZ)"""
        control_qubit = qubits[0]
        target_qubit = qubits[1]
        
        control_y = (control_qubit + 1) * qubit_spacing + margin_y
        target_y = (target_qubit + 1) * qubit_spacing + margin_y
        dot_radius = max(10, int(self.canvas_width / 150))
        
        # Control qubit
        self.circuit_canvas.create_oval(x - dot_radius, control_y - dot_radius,
                                x + dot_radius, control_y + dot_radius,
                                fill='#ffffff', outline='#ffffff')
        
        # Connection line
        self.circuit_canvas.create_line(x, control_y, x, target_y,
                                fill='#ffffff', width=line_width)
        
        if gate == 'CNOT':
            # Target qubit (X symbol)
            target_radius = max(25, int(self.canvas_width / 60))
            self.circuit_canvas.create_oval(x - target_radius, target_y - target_radius,
                                    x + target_radius, target_y + target_radius,
                                    fill='', outline='#ffffff', width=line_width)
            cross_size = target_radius * 0.6
            self.circuit_canvas.create_line(x - cross_size, target_y - cross_size,
                                    x + cross_size, target_y + cross_size,
                                    fill='#ffffff', width=line_width)
            self.circuit_canvas.create_line(x - cross_size, target_y + cross_size,
                                    x + cross_size, target_y - cross_size,
                                    fill='#ffffff', width=line_width)
        elif gate == 'CZ':
            # CZ target (Z symbol)
            self.circuit_canvas.create_oval(x - dot_radius, target_y - dot_radius,
                                    x + dot_radius, target_y + dot_radius,
                                    fill='#ffffff', outline='#ffffff')

    def draw_toffoli_gate(self, x, qubit_spacing, margin_y, qubits, line_width):
        """Draw a Toffoli (CCX) gate"""
        control1_qubit = qubits[0]
        control2_qubit = qubits[1]
        target_qubit = qubits[2]
        
        y_positions = [
            (control1_qubit + 1) * qubit_spacing + margin_y,
            (control2_qubit + 1) * qubit_spacing + margin_y,
            (target_qubit + 1) * qubit_spacing + margin_y
        ]
        
        dot_radius = max(8, int(self.canvas_width / 180))
        
        # Draw controls
        for i in range(2):
            self.circuit_canvas.create_oval(x - dot_radius, y_positions[i] - dot_radius,
                                    x + dot_radius, y_positions[i] + dot_radius,
                                    fill='#ffffff', outline='#ffffff')
        
        # Draw connection lines
        min_y = min(y_positions)
        max_y = max(y_positions)
        self.circuit_canvas.create_line(x, min_y, x, max_y,
                                fill='#ffffff', width=line_width)
        
        # Draw target (X symbol)
        target_radius = max(20, int(self.canvas_width / 70))
        target_y = y_positions[2]
        self.circuit_canvas.create_oval(x - target_radius, target_y - target_radius,
                                x + target_radius, target_y + target_radius,
                                fill='', outline='#ffffff', width=line_width)
        cross_size = target_radius * 0.6
        self.circuit_canvas.create_line(x - cross_size, target_y - cross_size,
                                x + cross_size, target_y + cross_size,
                                fill='#ffffff', width=line_width)
        self.circuit_canvas.create_line(x - cross_size, target_y + cross_size,
                                x + cross_size, target_y - cross_size,
                                fill='#ffffff', width=line_width)

    def run_circuit(self):
        """Execute the quantum circuit and check solution"""
        if not self.placed_gates:
            self.status_label.config(text="Add some gates first!")
            self.play_sound('error')
            return

        level = self.levels[self.current_level]

        try:
            # Create and execute quantum circuit
            qc = QuantumCircuit(level['qubits'])
            
            # Set initial state
            self.set_initial_state(qc, level)
            
            # Apply gates
            self.apply_gates(qc, level)
            
            # Get final state
            final_state = Statevector(qc)
            
            # Display current state
            self.display_current_state(final_state.data)
            
            # Check solution
            if self.check_solution(final_state, level):
                self.puzzle_solved()
            else:
                self.play_sound('run_circuit')
                self.status_label.config(text="❌ Not quite right. Keep trying!")
                self.root.after(300, lambda: self.play_sound('error'))
                
        except Exception as e:
            self.status_label.config(text=f"Error: {str(e)}")
            self.play_sound('error')

    def set_initial_state(self, qc, level):
        """Set the initial quantum state"""
        initial = level['input_state']
        
        if initial == "|1⟩":
            qc.x(0)
        elif initial == "|+⟩":
            qc.h(0)
        elif initial == "|-⟩":
            qc.x(0)
            qc.h(0)
        elif initial == "|i·1⟩":
            qc.y(0)
        elif initial == "|10⟩":
            qc.x(0)
        elif initial == "|+0⟩":
            qc.h(0)
        elif initial == "|Φ+⟩":
            qc.h(0)
            qc.cx(0, 1)
        elif initial == "|000⟩":
            pass  # Already |000⟩
        # Add more initial states as needed

    def apply_gates(self, qc, level):
        """Apply the placed gates to the quantum circuit"""
        for gate_info in self.placed_gates:
            if isinstance(gate_info, str):
                # Handle old format for backward compatibility
                gate = gate_info
                qubits = [0]
            else:
                gate = gate_info['gate']
                qubits = gate_info['qubits']
            
            if gate == 'H':
                qc.h(qubits[0])
            elif gate == 'X':
                qc.x(qubits[0])
            elif gate == 'Y':
                qc.y(qubits[0])
            elif gate == 'Z':
                qc.z(qubits[0])
            elif gate == 'S':
                qc.s(qubits[0])
            elif gate == 'T':
                qc.t(qubits[0])
            elif gate == 'CNOT' and len(qubits) >= 2:
                qc.cx(qubits[0], qubits[1])  # control, target
            elif gate == 'CZ' and len(qubits) >= 2:
                qc.cz(qubits[0], qubits[1])
            elif gate == 'Toffoli' and len(qubits) >= 3:
                qc.ccx(qubits[0], qubits[1], qubits[2])  # control1, control2, target

    def check_solution(self, final_state, level):
        """Check if the solution is correct"""
        target_state = self.get_target_state(level)
        fidelity = abs(np.vdot(target_state, final_state.data)) ** 2
        return fidelity > 0.99

    def get_target_state(self, level):
        """Get the target quantum state vector"""
        target = level['target_state']
        
        # Define common quantum states
        states = {
            "|0⟩": np.array([1, 0]),
            "|1⟩": np.array([0, 1]),
            "|+⟩": np.array([1, 1]) / np.sqrt(2),
            "|-⟩": np.array([1, -1]) / np.sqrt(2),
            "|i·1⟩": np.array([0, 1j]),
            "|+i⟩": np.array([1, 1j]) / np.sqrt(2),  # S gate applied to |+⟩
            "|T+⟩": np.array([1, np.exp(1j * np.pi / 4)]) / np.sqrt(2),  # T gate applied to |+⟩
            "|00⟩": np.array([1, 0, 0, 0]),
            "|11⟩": np.array([0, 0, 0, 1]),
            "|++⟩": np.array([1, 1, 1, 1]) / 2,
            "|Φ+⟩": np.array([1, 0, 0, 1]) / np.sqrt(2),
            "|Φ-⟩": np.array([1, 0, 0, -1]) / np.sqrt(2),
            "|Ψ+⟩": np.array([0, 1, 1, 0]) / np.sqrt(2),
            "|Ψ-⟩": np.array([0, 1, -1, 0]) / np.sqrt(2),
            "|GHZ⟩": np.array([1, 0, 0, 0, 0, 0, 0, 1]) / np.sqrt(2),
            "|W⟩": np.array([0, 1, 1, 0, 1, 0, 0, 0]) / np.sqrt(3),
            # Add more complex states for advanced levels
            "|0Φ+⟩": np.array([1, 0, 0, 0, 0, 1, 0, 0]) / np.sqrt(2),  # |0⟩ ⊗ |Φ+⟩
            "|Secret⟩": np.array([1, 1, 1, -1, 1, -1, -1, 1]) / (2 * np.sqrt(2)),  # Example secret sharing state
            "|Interference⟩": np.array([1, 0, 0, -1]) / np.sqrt(2),  # Destructive interference
            "|ErrorCode⟩": np.array([1, 0, 0, 0, 0, 0, 0, 0]),  # 3-qubit error code for |0⟩
            "|MaxEnt⟩": np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]) / 4,  # 4-qubit maximally entangled
            "|Ultimate⟩": np.array([1, 1j, -1, -1j, 1j, -1, -1j, 1, -1, -1j, 1, 1j, -1j, 1, 1j, -1]) / 4,  # Complex ultimate state
            "|QFT⟩": np.array([1, 1, 1, 1]) / 2,  # 2-qubit QFT of |00⟩
            "|err⟩": np.array([1, 1, 1, 0, 1, 0, 0, 0]) / np.sqrt(4)  # Error syndrome state
        }
        
        return states.get(target, np.array([1, 0]))

    def puzzle_solved(self):
        """Handle puzzle completion"""
        self.play_sound('success')
        
        level = self.levels[self.current_level]
        gates_used = len(self.placed_gates)
        max_gates = level.get('max_gates', 20)
        
        # Calculate score based on efficiency
        efficiency_bonus = max(0, (max_gates - gates_used) * 10)
        difficulty_bonus = {'Beginner': 50, 'Intermediate': 100, 'Advanced': 200, 
                          'Expert': 400, 'Master': 800}
        level_score = difficulty_bonus.get(level['difficulty'], 50) + efficiency_bonus
        
        self.score += level_score
        self.score_label.config(text=f"Score: {self.score}")
        
        # Store best efficiency
        self.max_gates_used[self.current_level] = min(
            self.max_gates_used.get(self.current_level, gates_used), gates_used)
        
        # Create congratulations dialog
        self.show_completion_dialog(level_score, gates_used, max_gates)

    def show_completion_dialog(self, level_score, gates_used, max_gates):
        """Show puzzle completion dialog"""
        congrats = tk.Toplevel(self.root)
        congrats.title("🎉 Puzzle Solved!")
        congrats.geometry("700x500")
        congrats.configure(bg='#1a1a1a')
        congrats.transient(self.root)
        congrats.grab_set()
        
        # Center dialog
        congrats.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - 350
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - 250
        congrats.geometry(f"700x500+{x}+{y}")
        
        level = self.levels[self.current_level]
        
        tk.Label(congrats, text="🎉 PUZZLE SOLVED! 🎉",
                font=('Arial', 28, 'bold'), fg='#00ff88', bg='#1a1a1a').pack(pady=(30, 10))
        
        tk.Label(congrats, text=f"Level {self.current_level + 1}: {level['name']}",
                font=('Arial', 18, 'bold'), fg='#ffffff', bg='#1a1a1a').pack(pady=5)
        
        tk.Label(congrats, text=f"Difficulty: {level['difficulty']}",
                font=('Arial', 14), fg='#4ecdc4', bg='#1a1a1a').pack(pady=5)
        
        tk.Label(congrats, text=f"Score: +{level_score}",
                font=('Arial', 20, 'bold'), fg='#ffd700', bg='#1a1a1a').pack(pady=10)
        
        tk.Label(congrats, text=f"Gates Used: {gates_used}/{max_gates}",
                font=('Arial', 16), fg='#ffffff', bg='#1a1a1a').pack(pady=5)
        
        # Efficiency rating
        efficiency = (max_gates - gates_used) / max_gates
        if efficiency >= 0.8:
            rating = "🏆 Excellent!"
            rating_color = '#ffd700'
        elif efficiency >= 0.6:
            rating = "🥈 Great!"
            rating_color = '#c0c0c0'
        elif efficiency >= 0.4:
            rating = "🥉 Good!"
            rating_color = '#cd7f32'
        else:
            rating = "✅ Solved!"
            rating_color = '#00ff88'
            
        tk.Label(congrats, text=f"Efficiency: {rating}",
                font=('Arial', 16, 'bold'), fg=rating_color, bg='#1a1a1a').pack(pady=10)
        
        # Buttons
        button_frame = tk.Frame(congrats, bg='#1a1a1a')
        button_frame.pack(pady=30)
        
        tk.Button(button_frame, text="🚀 Next Level",
                 command=lambda: [self.play_sound('button_click'), self.next_level(congrats)],
                 font=('Arial', 16, 'bold'), bg='#00ff88', fg='#000000',
                 padx=40, pady=15).pack(pady=10)
        
        congrats.focus_set()
        congrats.bind('<Return>', lambda e: self.next_level(congrats))

    def next_level(self, dialog):
        """Advance to next level"""
        dialog.destroy()
        if self.current_level < len(self.levels) - 1:
            self.load_level(self.current_level + 1)
            self.play_sound('level_up')
        else:
            self.game_complete()

    def game_complete(self):
        """Handle game completion"""
        self.play_sound('game_complete')
        
        complete = tk.Toplevel(self.root)
        complete.title("🏆 All Puzzles Complete!")
        complete.geometry("800x600")
        complete.configure(bg='#1a1a1a')
        complete.transient(self.root)
        complete.grab_set()
        
        # Center dialog
        complete.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - 400
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - 300
        complete.geometry(f"800x600+{x}+{y}")
        
        tk.Label(complete, text="🏆 QUANTUM MASTER! 🏆",
                font=('Arial', 32, 'bold'), fg='#ffd700', bg='#1a1a1a').pack(pady=(40, 20))
        
        tk.Label(complete, text="You've solved all puzzle challenges!",
                font=('Arial', 18), fg='#ffffff', bg='#1a1a1a').pack(pady=10)
        
        tk.Label(complete, text=f"Final Score: {self.score}",
                font=('Arial', 24, 'bold'), fg='#00ff88', bg='#1a1a1a').pack(pady=15)
        
        # Statistics
        stats_frame = tk.Frame(complete, bg='#2a2a2a', relief=tk.RAISED, bd=3)
        stats_frame.pack(pady=20, padx=40, fill=tk.X)
        
        tk.Label(stats_frame, text="📊 Your Statistics",
                font=('Arial', 16, 'bold'), fg='#4ecdc4', bg='#2a2a2a').pack(pady=10)
        
        total_gates = sum(self.max_gates_used.values())
        avg_efficiency = np.mean([self.levels[i].get('max_gates', 20) - gates 
                                for i, gates in self.max_gates_used.items()])
        
        tk.Label(stats_frame, text=f"Total Gates Used: {total_gates}",
                font=('Arial', 12), fg='#ffffff', bg='#2a2a2a').pack(pady=2)
        
        tk.Label(stats_frame, text=f"Average Efficiency: {avg_efficiency:.1f}",
                font=('Arial', 12), fg='#ffffff', bg='#2a2a2a').pack(pady=2)
        
        tk.Label(stats_frame, text=f"Levels Completed: {len(self.levels)}",
                font=('Arial', 12), fg='#ffffff', bg='#2a2a2a').pack(pady=(2, 10))
        
        # Buttons
        button_frame = tk.Frame(complete, bg='#1a1a1a')
        button_frame.pack(pady=20)
        
        tk.Button(button_frame, text="🔄 Play Again",
                 command=lambda: [self.play_sound('button_click'), self.restart_game(complete)],
                 font=('Arial', 14, 'bold'), bg='#00ff88', fg='#000000',
                 padx=30, pady=10).pack(side=tk.LEFT, padx=10)
        
        tk.Button(button_frame, text="🏠 Main Menu",
                 command=lambda: [self.play_sound('button_click'), self.return_to_menu(complete)],
                 font=('Arial', 14, 'bold'), bg='#4ecdc4', fg='#000000',
                 padx=30, pady=10).pack(side=tk.LEFT, padx=10)

    def skip_level(self):
        """Skip current level (with score penalty)"""
        result = messagebox.askyesno("Skip Level", 
                                   "Skip this level? You'll lose points but can continue.")
        if result:
            self.score = max(0, self.score - 50)  # Penalty for skipping
            self.score_label.config(text=f"Score: {self.score}")
            self.play_sound('button_click')
            
            if self.current_level < len(self.levels) - 1:
                self.load_level(self.current_level + 1)
            else:
                self.game_complete()

    def show_hint(self):
        """Show hint for current level"""
        self.play_sound('hint')
        hint = self.levels[self.current_level]['hint']
        messagebox.showinfo("💡 Hint", hint)

    def display_states(self, level):
        """Display level information"""
        self.state_display.delete(1.0, tk.END)
        self.state_display.insert(tk.END, f"🎯 Target: {level['target_state']}\n")
        self.state_display.insert(tk.END, f"🔸 Input: {level['input_state']}\n")
        self.state_display.insert(tk.END, f"⚡ Qubits: {level['qubits']}\n")
        self.state_display.insert(tk.END, f"🎲 Max Gates: {level.get('max_gates', 'Unlimited')}\n")
        self.state_display.insert(tk.END, "─" * 50 + "\n")

    def display_current_state(self, state_vector):
        """Display current quantum state"""
        level = self.levels[self.current_level]
        self.state_display.delete(1.0, tk.END)
        
        # Show level info
        self.state_display.insert(tk.END, f"🎯 Target: {level['target_state']}\n")
        self.state_display.insert(tk.END, f"🔸 Input: {level['input_state']}\n")
        self.state_display.insert(tk.END, f"⚡ Qubits: {level['qubits']}\n")
        self.state_display.insert(tk.END, f"🎲 Gates Used: {len(self.placed_gates)}/{level.get('max_gates', '∞')}\n")
        self.state_display.insert(tk.END, "─" * 50 + "\n")
        
        # Show current state
        self.state_display.insert(tk.END, "📊 Current State:\n")
        for i, amplitude in enumerate(state_vector):
            if abs(amplitude) > 0.001:
                binary = f"{i:0{level['qubits']}b}"
                real_part = f"{amplitude.real:.3f}"
                imag_part = f"{amplitude.imag:+.3f}i" if amplitude.imag != 0 else ""
                self.state_display.insert(tk.END, f"|{binary}⟩: {real_part}{imag_part}\n")
        
        self.state_display.see(tk.END)

    def restart_game(self, dialog):
        """Restart the puzzle mode"""
        dialog.destroy()
        self.current_level = 0
        self.score = 0
        self.placed_gates = []
        self.max_gates_used = {}
        self.load_level(0)

    def return_to_menu(self, dialog):
        """Return to main menu"""
        dialog.destroy()
        self.root.destroy()
        # Import and start game mode selection
        try:
            from game_mode_selection import GameModeSelection
            import tkinter as tk
            root = tk.Tk()
            GameModeSelection(root)
            root.mainloop()
        except ImportError:
            print("Could not return to main menu")

if __name__ == "__main__":
    root = tk.Tk()
    app = PuzzleMode(root)
    root.mainloop()