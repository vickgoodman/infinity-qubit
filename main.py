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
import pygame  # Add this import for sound

try:
    from game_tutorial import show_tutorial
except ImportError:
    def show_tutorial(parent):
        messagebox.showinfo("Tutorial", "Tutorial module not found")

class QubitPuzzleGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Infinity Qubit")

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

        # Use 90% of screen width and 85% of screen height
        window_width = int(screen_width * 0.75)
        window_height = int(screen_height * 0.6)

        # Calculate center position
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        # Set window geometry with centering
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.configure(bg='#1a1a1a')

        # Store dimensions for adaptive scaling
        self.window_width = window_width
        self.window_height = window_height

        # Game state
        self.current_level = 0
        self.placed_gates = []
        self.score = 0
        self.levels = self.load_levels()

        # Initialize UI
        self.setup_ui()
        self.load_level(self.current_level)

    def load_sounds(self):
        """Load sound effects for the game"""
        self.sounds = {}

        # Define sound files for each gate and action
        sound_files = {
            'H': 'sounds/hadamard.wav',        # Hadamard gate sound
            'X': 'sounds/pauli_x.wav',         # X gate sound
            'Z': 'sounds/pauli_z.wav',         # Z gate sound
            'I': 'sounds/identity.wav',        # Identity gate sound
            'CNOT': 'sounds/cnot.wav',         # CNOT gate sound
            'run_circuit': 'sounds/run_circuit.wav',    # Run circuit sound
            'clear': 'sounds/clear.wav',       # Clear circuit sound
            'hint': 'sounds/hint.wav',         # Hint button sound
            'success': 'sounds/success.wav',   # Puzzle solved sound
            'error': 'sounds/error.wav',       # Error sound
            'level_up': 'sounds/level_up.wav', # Level completion sound
            'button_click': 'sounds/click.wav', # General button click
            'game_complete': 'sounds/victory.wav' # Game completion sound
        }

        # Load each sound file
        for sound_name, file_path in sound_files.items():
            try:
                self.sounds[sound_name] = pygame.mixer.Sound(file_path)
                # Set volume levels (0.0 to 1.0) - Adjusted volumes
                if sound_name in ['H', 'X', 'Z', 'I', 'CNOT']:
                    self.sounds[sound_name].set_volume(0.7)  # Gate sounds
                elif sound_name in ['success', 'level_up']:
                    self.sounds[sound_name].set_volume(0.8)  # Success sounds - reduced from 0.9
                elif sound_name == 'run_circuit':
                    self.sounds[sound_name].set_volume(0.4)  # Run circuit - reduced from 0.6
                elif sound_name == 'game_complete':
                    self.sounds[sound_name].set_volume(0.9)  # Victory sound
                else:
                    self.sounds[sound_name].set_volume(0.6)  # Other sounds
            except pygame.error:
                print(f"Warning: Could not load sound file: {file_path}")
                self.sounds[sound_name] = None

    def play_sound(self, sound_name):
        """Play a sound effect"""
        if self.sound_enabled and sound_name in self.sounds and self.sounds[sound_name]:
            try:
                # print(f"Attempting to play sound: {sound_name}")  # Debug line
                self.sounds[sound_name].play()
                # print(f"Successfully played sound: {sound_name}")  # Debug line
            except pygame.error as e:
                # print(f"Error playing sound {sound_name}: {e}")  # Debug line
                pass  # Ignore sound errors
        # else:
            # print(f"Sound not available or disabled: {sound_name}")  # Debug line

    def create_sound_effects_programmatically(self):
        """Create simple sound effects programmatically if sound files don't exist"""
        if not self.sound_enabled:
            return

        # Create simple beep sounds for different gates
        sample_rate = 22050

        # Different frequencies for different gates
        gate_frequencies = {
            'H': 440,    # A note - Hadamard
            'X': 523,    # C note - X gate
            'Z': 659,    # E note - Z gate
            'I': 349,    # F note - Identity
            'CNOT': [440, 523]  # Fixed: Changed from 523 to [440, 523] for chord
        }

        for gate, freq in gate_frequencies.items():
            if gate not in self.sounds or not self.sounds[gate]:
                try:
                    if isinstance(freq, list):
                        # Create chord for CNOT
                        duration = 0.2
                        frames = int(duration * sample_rate)
                        arr = np.zeros(frames)
                        for f in freq:
                            arr += np.sin(2 * np.pi * f * np.linspace(0, duration, frames))
                        arr = arr / len(freq)  # Normalize
                    else:
                        # Create single tone
                        duration = 0.15
                        frames = int(duration * sample_rate)
                        arr = np.sin(2 * np.pi * freq * np.linspace(0, duration, frames))

                    # Convert to pygame sound
                    arr = (arr * 32767).astype(np.int16)
                    sound = pygame.sndarray.make_sound(arr)
                    # Set appropriate volume for programmatically created sounds
                    if gate == 'CNOT':
                        sound.set_volume(0.4)  # CNOT slightly quieter
                    else:
                        sound.set_volume(0.3)
                    self.sounds[gate] = sound
                    print(f"Created programmatic sound for {gate}")  # Debug line
                except Exception as e:
                    print(f"Failed to create sound for {gate}: {e}")  # Debug line
                    pass  # Ignore if numpy/pygame sound creation fails

    def load_levels(self):
        """Load puzzle levels from JSON file or create defaults"""
        try:
            with open('levels.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            # Create default levels if file doesn't exist
            return self.create_default_levels()
        except json.JSONDecodeError:
            # If file is corrupted, recreate defaults
            return self.create_default_levels()

    def setup_ui(self):
        # Main frame
        main_frame = tk.Frame(self.root, bg='#1a1a1a')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Adaptive font sizes based on screen resolution
        title_font_size = max(16, int(self.window_width / 80))
        header_font_size = max(12, int(self.window_width / 120))
        normal_font_size = max(10, int(self.window_width / 160))

        # Title
        title_label = tk.Label(main_frame, text="🔬 Infinity Qubit",
                            font=('Arial', title_font_size, 'bold'), fg='#00ff88', bg='#1a1a1a')
        title_label.pack(pady=(0, 10))

        # Level and score info - Centered under title
        info_frame = tk.Frame(main_frame, bg='#1a1a1a')
        info_frame.pack(pady=(0, 20))

        self.level_label = tk.Label(info_frame, text="Level: 1",
                                font=('Arial', header_font_size, 'bold'), fg='#ffffff', bg='#1a1a1a')
        self.level_label.pack(side=tk.LEFT, padx=20)

        self.score_label = tk.Label(info_frame, text="Score: 0",
                                font=('Arial', header_font_size, 'bold'), fg='#ffffff', bg='#1a1a1a')
        self.score_label.pack(side=tk.LEFT, padx=20)

        # Add tutorial button - moved to top right corner
        tutorial_btn = tk.Button(main_frame, text="📚 Tutorial",
                                command=lambda: [self.play_sound('button_click'), show_tutorial(self.root)],
                                font=('Arial', normal_font_size), bg='#9b59b6', fg='#ffffff')
        tutorial_btn.place(relx=0.98, rely=0.02, anchor='ne')

        # Circuit area - Made adaptive
        circuit_frame = tk.Frame(main_frame, bg='#2a2a2a', relief=tk.RAISED, bd=3)
        circuit_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))

        # Circuit title
        circuit_title = tk.Label(circuit_frame, text="Quantum Circuit",
                                font=('Arial', header_font_size + 2, 'bold'), fg='#00ff88', bg='#2a2a2a')
        circuit_title.pack(pady=15)

        # Circuit canvas - Adaptive size based on window dimensions
        canvas_width = int(self.window_width * 0.85)
        canvas_height = int(self.window_height * 0.35)

        self.circuit_canvas = tk.Canvas(circuit_frame, width=canvas_width, height=canvas_height,
                                    bg='#1a1a1a', highlightthickness=0)
        self.circuit_canvas.pack(pady=15)

        # Store canvas dimensions for draw_circuit method
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height

        # Gate placement area
        self.gate_frame = tk.Frame(circuit_frame, bg='#2a2a2a')
        self.gate_frame.pack(fill=tk.X, padx=20, pady=15)

        # Available gates - Centered
        gates_label = tk.Label(main_frame, text="Available Gates",
                            font=('Arial', header_font_size, 'bold'), fg='#ffffff', bg='#1a1a1a')
        gates_label.pack(pady=(10, 5))

        self.gates_frame = tk.Frame(main_frame, bg='#1a1a1a')
        self.gates_frame.pack(pady=10)

        # Control buttons - Centered under available gates
        controls_frame = tk.Frame(main_frame, bg='#1a1a1a')
        controls_frame.pack(pady=(15, 10))

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

        # Fixed hint button - play sound immediately when clicked
        self.hint_button = tk.Button(controls_frame, text="💡 Hint",
                                    command=self.show_hint, font=('Arial', button_font_size),
                                    bg='#4ecdc4', fg='#000000', padx=button_padx, pady=button_pady)
        self.hint_button.pack(side=tk.LEFT, padx=10)

        # Status area - Made adaptive
        status_frame = tk.Frame(main_frame, bg='#2a2a2a', relief=tk.RAISED, bd=3)
        status_frame.pack(fill=tk.X, pady=(15, 0))

        # Status title
        status_title = tk.Label(status_frame, text="🔍 Quantum State Information",
                            font=('Arial', header_font_size, 'bold'), fg='#00ff88', bg='#2a2a2a')
        status_title.pack(pady=(10, 5))

        self.status_label = tk.Label(status_frame, text="Ready to solve puzzles!",
                                    font=('Arial', normal_font_size + 2), fg='#ffffff', bg='#2a2a2a')
        self.status_label.pack(pady=5)

        # State display - Adaptive size
        text_height = max(8, int(self.window_height / 100))
        text_width = max(60, int(self.window_width / 20))
        text_font_size = max(8, int(self.window_width / 180))

        self.state_display = tk.Text(status_frame, height=text_height, width=text_width,
                                    font=('Courier', text_font_size), bg='#1a1a1a', fg='#00ff88',
                                    relief=tk.SUNKEN, bd=2)
        self.state_display.pack(pady=15, padx=20)

        # Initialize sound effects after UI is created
        if self.sound_enabled:
            self.create_sound_effects_programmatically()

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
        """Setup available gate buttons - Adaptive sizing"""
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

        # Adaptive gate button sizing
        gate_font_size = max(10, int(self.window_width / 160))
        gate_width = max(4, int(self.window_width / 300))
        gate_height = max(1, int(self.window_height / 600))

        for gate in available_gates:
            color = gate_colors.get(gate, '#ffffff')
            btn = tk.Button(self.gates_frame, text=gate,
                        command=lambda g=gate: self.add_gate(g),
                        font=('Arial', gate_font_size, 'bold'), bg=color, fg='#000000',
                        width=gate_width, height=gate_height)
            btn.pack(side=tk.LEFT, padx=5)

    def add_gate(self, gate):
        """Add a gate to the circuit with sound effect"""
        if len(self.placed_gates) < 10:  # Limit gates
            self.placed_gates.append(gate)
            self.draw_circuit()

            # Play gate-specific sound - Fixed for CNOT
            print(f"Playing sound for gate: {gate}")  # Debug line
            self.play_sound(gate)

    def clear_circuit(self):
        """Clear all placed gates with sound"""
        self.placed_gates = []
        self.draw_circuit()
        self.play_sound('clear')

    def draw_circuit(self):
        """Draw the quantum circuit visualization - Adaptive scaling"""
        self.circuit_canvas.delete("all")

        # Get current level info for proper qubit count
        level = self.levels[self.current_level]
        num_qubits = level['qubits']

        # Adaptive circuit dimensions based on canvas size
        wire_start = int(self.canvas_width * 0.12)
        wire_end = int(self.canvas_width * 0.88)
        circuit_height = self.canvas_height
        qubit_spacing = circuit_height // (num_qubits + 1)

        # Adaptive sizing for elements
        line_width = max(3, int(self.canvas_width / 300))
        font_size = max(12, int(self.canvas_width / 75))

        # Draw input/output dividers and labels - Adaptive
        input_x = wire_start - int(self.canvas_width * 0.05)
        output_x = wire_end + int(self.canvas_width * 0.05)
        margin_y = int(circuit_height * 0.1)

        # Input section
        self.circuit_canvas.create_line(input_x, margin_y, input_x, circuit_height - margin_y,
                                fill='#00ff88', width=line_width)
        self.circuit_canvas.create_text(input_x - int(self.canvas_width * 0.04), circuit_height // 2,
                                text="Input", fill='#00ff88',
                                font=('Arial', font_size, 'bold'), angle=90)

        # Output section
        self.circuit_canvas.create_line(output_x, margin_y, output_x, circuit_height - margin_y,
                                fill='#00ff88', width=line_width)
        self.circuit_canvas.create_text(output_x + int(self.canvas_width * 0.04), circuit_height // 2,
                                text="Output", fill='#00ff88',
                                font=('Arial', font_size, 'bold'), angle=90)

        # Draw quantum wires for each qubit - Adaptive
        for qubit in range(num_qubits):
            y_pos = (qubit + 1) * qubit_spacing + margin_y

            # Wire line
            self.circuit_canvas.create_line(wire_start, y_pos, wire_end, y_pos,
                                    fill='#ffffff', width=line_width)

            # Qubit labels
            self.circuit_canvas.create_text(wire_start - int(self.canvas_width * 0.02), y_pos,
                                    text=f"q{qubit}", fill='#ffffff',
                                    font=('Arial', font_size - 2, 'bold'))

        # Draw gates - Adaptive sizing with proper letter fitting
        gate_width = max(60, int(self.canvas_width / 20))  # Increased from /30 to /20
        gate_height = max(50, int(self.canvas_height / 12))  # Increased from /15 to /12
        gate_spacing = max(120, int(self.canvas_width / 12))  # Increased spacing
        gate_font_size = max(18, int(self.canvas_width / 75))  # Increased font size

        for i, gate in enumerate(self.placed_gates):
            x = wire_start + int(self.canvas_width * 0.08) + i * gate_spacing

            if gate == 'CNOT' and num_qubits > 1:
                # Special handling for CNOT gate - Adaptive
                control_y = qubit_spacing + margin_y
                target_y = 2 * qubit_spacing + margin_y
                dot_radius = max(10, int(self.canvas_width / 150))  # Slightly larger

                # Control qubit (dot)
                self.circuit_canvas.create_oval(x - dot_radius, control_y - dot_radius,
                                        x + dot_radius, control_y + dot_radius,
                                        fill='#ffffff', outline='#ffffff')

                # Connection line
                self.circuit_canvas.create_line(x, control_y, x, target_y,
                                        fill='#ffffff', width=line_width)

                # Target qubit (X symbol) - FIXED: Changed fill='none' to fill=''
                target_radius = max(25, int(self.canvas_width / 60))  # Larger target
                self.circuit_canvas.create_oval(x - target_radius, target_y - target_radius,
                                        x + target_radius, target_y + target_radius,
                                        fill='', outline='#ffffff', width=line_width)  # Fixed: fill='' instead of fill='none'
                cross_size = target_radius * 0.6
                self.circuit_canvas.create_line(x - cross_size, target_y - cross_size,
                                        x + cross_size, target_y + cross_size,
                                        fill='#ffffff', width=line_width)
                self.circuit_canvas.create_line(x - cross_size, target_y + cross_size,
                                        x + cross_size, target_y - cross_size,
                                        fill='#ffffff', width=line_width)
            else:
                # Single qubit gates - Larger boxes to fit letters properly
                y_pos = qubit_spacing + margin_y

                # Gate box - Much larger to accommodate letters
                self.circuit_canvas.create_rectangle(x - gate_width//2, y_pos - gate_height//2,
                                            x + gate_width//2, y_pos + gate_height//2,
                                            fill='#4ecdc4', outline='#ffffff', width=line_width)

                # Gate label - Larger font and better positioning
                self.circuit_canvas.create_text(x, y_pos, text=gate,
                                        fill='#000000', font=('Arial', gate_font_size, 'bold'))

    def run_circuit(self):
        """Execute the quantum circuit and check result with sound"""
        if not self.placed_gates:
            self.status_label.config(text="Add some gates first!")
            self.play_sound('error')
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
                # SUCCESS: Play only success sound, not run_circuit sound
                self.status_label.config(text="🎉 Puzzle solved! Great job!")
                self.play_sound('success')
                # Delay puzzle_solved to let success sound play
                self.root.after(500, self.puzzle_solved)
            else:
                # INCORRECT: Play run_circuit sound first, then error sound
                self.play_sound('run_circuit')
                self.status_label.config(text="Not quite right. Try again!")
                # Delay error sound to avoid overlap
                self.root.after(300, lambda: self.play_sound('error'))

        except Exception as e:
            self.status_label.config(text=f"Error: {str(e)}")
            self.play_sound('error')

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
        """Handle puzzle completion with enhanced sound"""
        # Play level up sound
        self.play_sound('level_up')

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

        # Button frame for better spacing
        button_frame = tk.Frame(congrats_window, bg='#1a1a1a')
        button_frame.pack(pady=(50, 40))

        # Continue button - Made MUCH larger and more prominent
        continue_btn = tk.Button(button_frame, text="🚀 Continue to Next Level",
                                command=lambda: [self.play_sound('button_click'), self.continue_to_next_level(congrats_window)],
                                font=('Arial', 20, 'bold'), bg='#00ff88', fg='#000000',
                                padx=60, pady=25, relief=tk.RAISED, bd=5)
        continue_btn.pack(pady=20)

        # Focus on the button so Enter key works
        continue_btn.focus_set()

        # Bind keys
        congrats_window.bind('<Return>', lambda e: [self.play_sound('button_click'), self.continue_to_next_level(congrats_window)])
        congrats_window.bind('<Escape>', lambda e: [self.play_sound('button_click'), self.continue_to_next_level(congrats_window)])
        congrats_window.bind('<space>', lambda e: [self.play_sound('button_click'), self.continue_to_next_level(congrats_window)])

        # Add a close button as backup - Also larger
        close_btn = tk.Button(button_frame, text="❌ Close",
                            command=lambda: [self.play_sound('button_click'), congrats_window.destroy()],
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
            # Play game complete sound
            self.play_sound('game_complete')

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
                                command=lambda: [self.play_sound('button_click'), self.restart_from_complete(complete_window)],
                                font=('Arial', 14, 'bold'), bg='#00ff88', fg='#000000',
                                padx=40, pady=12, relief=tk.RAISED, bd=3)
            restart_btn.pack(pady=10)

            # Focus and key bindings
            restart_btn.focus_set()
            complete_window.bind('<Return>', lambda e: [self.play_sound('button_click'), self.restart_from_complete(complete_window)])

    def restart_from_complete(self, dialog_window):
        """Close completion dialog and restart game"""
        dialog_window.destroy()
        self.restart_game()

    def restart_game(self):
        """Restart the game from level 1"""
        self.current_level = 0
        self.score = 0
        self.placed_gates = []
        self.load_level(0)

    def show_hint(self):
        """Show hint for current level with sound"""
        # Play hint sound IMMEDIATELY when button is clicked
        self.play_sound('hint')

        hint = self.levels[self.current_level]['hint']
        messagebox.showinfo("Hint", hint)
        # Remove the second play_sound call that was happening after OK

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
