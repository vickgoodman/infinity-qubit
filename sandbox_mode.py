import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
from qiskit import QuantumCircuit # type: ignore
from qiskit.quantum_info import Statevector # type: ignore
from qiskit.visualization import plot_bloch_multivector, plot_state_qsphere # type: ignore
import pygame # type: ignore
import matplotlib.pyplot as plt # type: ignore
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg # type: ignore

class SandboxMode:
    def __init__(self, root):
        self.root = root
        self.root.title("Quantum Sandbox Mode")

        # Initialize sound system (optional - can reuse from main)
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
            self.sound_enabled = True

            # Load sound files (same as tutorial)
            self.sounds = {}
            try:
                # Gate sounds
                self.sounds['gate_place'] = pygame.mixer.Sound("sounds/click.wav")
                self.sounds['success'] = pygame.mixer.Sound("sounds/run_circuit.wav")
                self.sounds['error'] = pygame.mixer.Sound("sounds/error.wav")
                self.sounds['click'] = pygame.mixer.Sound("sounds/click.wav")
                self.sounds['circuit_run'] = pygame.mixer.Sound("sounds/click.wav")
                self.sounds['clear'] = pygame.mixer.Sound("sounds/clear.wav")

                # Set volumes
                for sound in self.sounds.values():
                    sound.set_volume(0.5)

            except (pygame.error, FileNotFoundError) as e:
                print(f"Could not load sound files: {e}")
                # Fallback to programmatic sounds
                self.sounds = {}

        except:
            self.sound_enabled = False
            self.sounds = {}

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

    def play_sound(self, sound_name, fallback_func=None):
        """Play a sound file or fallback to programmatic sound"""
        if not self.sound_enabled:
            return

        try:
            if sound_name in self.sounds:
                self.sounds[sound_name].play()
            elif fallback_func:
                fallback_func()
        except Exception as e:
            print(f"Sound error: {e}")
            if fallback_func:
                fallback_func()

    def play_gate_sound_fallback(self):
        """Fallback sound for gate placement"""
        try:
            frequency = 440
            duration = 0.15
            sample_rate = 22050
            frames = int(duration * sample_rate)

            t = np.linspace(0, duration, frames)
            wave = np.sin(2 * np.pi * frequency * t)
            envelope = np.exp(-t * 5)
            wave = wave * envelope

            wave = (wave * 16383).astype(np.int16)
            stereo_wave = np.array([wave, wave]).T

            sound = pygame.sndarray.make_sound(stereo_wave)
            sound.set_volume(0.4)
            sound.play()
        except:
            pass

    def play_success_sound_fallback(self):
        """Fallback sound for success"""
        try:
            frequencies = [440, 523, 659, 784]
            duration = 0.15
            sample_rate = 22050
            frames = int(duration * sample_rate)

            total_frames = frames * len(frequencies)
            full_wave = np.zeros(total_frames)

            for i, freq in enumerate(frequencies):
                t = np.linspace(0, duration, frames)
                wave = np.sin(2 * np.pi * freq * t)
                envelope = np.exp(-t * 4)
                wave = wave * envelope

                start_idx = i * frames
                end_idx = start_idx + frames
                full_wave[start_idx:end_idx] = wave

            full_wave = (full_wave * 16383).astype(np.int16)
            stereo_wave = np.array([full_wave, full_wave]).T

            sound = pygame.sndarray.make_sound(stereo_wave)
            sound.set_volume(0.6)
            sound.play()
        except:
            pass

    def play_error_sound_fallback(self):
        """Fallback sound for errors"""
        try:
            frequency = 150
            duration = 0.2
            sample_rate = 22050
            frames = int(duration * sample_rate)

            t = np.linspace(0, duration, frames)
            wave1 = np.sin(2 * np.pi * frequency * t)
            wave2 = np.sin(2 * np.pi * (frequency * 1.1) * t)
            wave = (wave1 + wave2) / 2

            envelope = np.exp(-t * 8)
            wave = wave * envelope

            wave = (wave * 16383).astype(np.int16)
            stereo_wave = np.array([wave, wave]).T

            sound = pygame.sndarray.make_sound(stereo_wave)
            sound.set_volume(0.5)
            sound.play()
        except:
            pass

    def play_clear_sound_fallback(self):
        """Fallback sound for clearing"""
        try:
            start_freq = 800
            duration = 0.3
            sample_rate = 22050
            frames = int(duration * sample_rate)

            t = np.linspace(0, duration, frames)
            freq_sweep = start_freq * np.exp(-t * 5)
            wave = np.sin(2 * np.pi * freq_sweep * t)

            envelope = np.exp(-t * 2)
            wave = wave * envelope

            wave = (wave * 16383).astype(np.int16)
            stereo_wave = np.array([wave, wave]).T

            sound = pygame.sndarray.make_sound(stereo_wave)
            sound.set_volume(0.4)
            sound.play()
        except:
            pass

    def setup_ui(self):
        """Setup the sandbox UI with enhanced styling matching learn hub"""
        # Main container with gradient-like effect
        main_frame = tk.Frame(self.root, bg='#0a0a0a')
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Add subtle top border
        top_border = tk.Frame(main_frame, bg='#00ff88', height=3)
        top_border.pack(fill=tk.X)

        # Content frame
        content_frame = tk.Frame(main_frame, bg='#2a2a2a')
        content_frame.pack(fill=tk.BOTH, expand=True)

        # Create simplified header (no animation)
        self.create_simple_header(content_frame)

        # Main content container
        main_container = tk.Frame(content_frame, bg='#2a2a2a')
        main_container.pack(fill=tk.BOTH, expand=True, padx=25, pady=(0, 25))

        # Control panel
        self.setup_control_panel(main_container)

        # Circuit display area
        self.setup_circuit_area(main_container)

        # Note: setup_action_buttons and setup_results_area are now called from setup_bottom_section

    def create_simple_header(self, parent):
        """Create a simple header without animation to save space"""
        header_frame = tk.Frame(parent, bg='#2a2a2a')
        header_frame.pack(fill=tk.X, padx=25, pady=(15, 10))

        # Add a top navigation bar with title and menu button
        nav_frame = tk.Frame(header_frame, bg='#2a2a2a')
        nav_frame.pack(fill=tk.X)

        # Title on the left
        title_label = tk.Label(nav_frame, text="🛠️ Quantum Circuit Sandbox",
                            font=('Arial', 20, 'bold'),
                            fg='#00ff88', bg='#2a2a2a')
        title_label.pack(side=tk.LEFT)

        # Subtitle below title
        subtitle_label = tk.Label(nav_frame,
                                text="Build and simulate quantum circuits in real-time",
                                font=('Arial', 11, 'italic'),
                                fg='#4ecdc4', bg='#2a2a2a')
        subtitle_label.pack(side=tk.LEFT, padx=(10, 0))

        # Back to Main Menu button - top right
        main_menu_btn = tk.Button(nav_frame, text="🏠 Main Menu",
                                command=self.return_to_main_menu,
                                font=('Arial', 10, 'bold'),
                                bg='#3a3a3a', fg='#4ecdc4',
                                padx=15, pady=8,
                                cursor='hand2',
                                relief=tk.FLAT,
                                borderwidth=1)
        main_menu_btn.pack(side=tk.RIGHT)

        # Add hover effect
        def on_nav_enter(event):
            main_menu_btn.configure(bg='#4ecdc4', fg='#000000')
        def on_nav_leave(event):
            main_menu_btn.configure(bg='#3a3a3a', fg='#4ecdc4')

        main_menu_btn.bind("<Enter>", on_nav_enter)
        main_menu_btn.bind("<Leave>", on_nav_leave)

    def return_to_main_menu(self):
        """Return to the main menu"""
        self.play_sound('click')
        self.root.destroy()

        try:
            # Import and start game mode selection
            from game_mode_selection import GameModeSelection
            selection_window = GameModeSelection()
            selection_window.run()
        except ImportError as e:
            print(f"Error importing game mode selection: {e}")
            # Fallback - try to run main
            try:
                import main
                main.main()
            except ImportError:
                print("Could not return to main menu. Please restart the application.")
        except Exception as e:
            print(f"Error returning to main menu: {e}")

    def setup_control_panel(self, parent):
        """Setup the control panel with enhanced styling"""
        control_frame = tk.Frame(parent, bg='#2a2a2a', relief=tk.RAISED, bd=2)
        control_frame.pack(fill=tk.X, pady=(0, 20))

        # Enhanced title
        control_title = tk.Label(control_frame, text="🎛️ Circuit Configuration",
                                font=('Arial', 16, 'bold'), fg='#00ff88', bg='#2a2a2a')
        control_title.pack(pady=(15, 10))

        # Main controls container
        controls_container = tk.Frame(control_frame, bg='#2a2a2a')
        controls_container.pack(padx=20, pady=(0, 15))

        # Qubit controls - left side
        qubit_frame = tk.Frame(controls_container, bg='#3a3a3a', relief=tk.RAISED, bd=1)
        qubit_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 15), pady=5, ipadx=15, ipady=10)

        tk.Label(qubit_frame, text="⚛️ Number of Qubits",
                font=('Arial', 12, 'bold'), fg='#ffffff', bg='#3a3a3a').pack(pady=(0, 5))

        self.qubit_var = tk.IntVar(value=1)
        qubit_spinbox = tk.Spinbox(qubit_frame, from_=1, to=4, textvariable=self.qubit_var,
                                command=self.on_qubit_change, font=('Arial', 12), width=8,
                                bg='#1a1a1a', fg='#00ff88', insertbackground='#00ff88')
        qubit_spinbox.pack(pady=5)

        # Initial state selection - right side
        state_frame = tk.Frame(controls_container, bg='#3a3a3a', relief=tk.RAISED, bd=1)
        state_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5, ipadx=15, ipady=10)

        tk.Label(state_frame, text="🎯 Initial State",
                font=('Arial', 12, 'bold'), fg='#ffffff', bg='#3a3a3a').pack(pady=(0, 5))

        self.state_var = tk.StringVar(value="|0⟩")
        state_options = ["|0⟩", "|1⟩", "|+⟩", "|-⟩"]

        # Custom styled combobox
        style = ttk.Style()
        style.configure('Custom.TCombobox',
                       fieldbackground='#1a1a1a',
                       background='#3a3a3a',
                       foreground='#00ff88',
                       arrowcolor='#00ff88')

        self.state_combo = ttk.Combobox(state_frame, textvariable=self.state_var,
                                    values=state_options, state="readonly",
                                    font=('Arial', 11), width=8,
                                    style='Custom.TCombobox')
        self.state_combo.pack(pady=5)
        self.state_combo.bind('<<ComboboxSelected>>', self.on_state_change)

    def setup_circuit_area(self, parent):
        """Setup the circuit visualization area with enhanced styling"""
        circuit_frame = tk.Frame(parent, bg='#2a2a2a', relief=tk.RAISED, bd=2)
        circuit_frame.pack(fill=tk.X, pady=(0, 15))

        # Enhanced title with icon
        circuit_title = tk.Label(circuit_frame, text="🔧 Quantum Circuit Designer",
                                font=('Arial', 14, 'bold'), fg='#00ff88', bg='#2a2a2a')
        circuit_title.pack(pady=(10, 8))

        # Circuit canvas with enhanced styling
        canvas_container = tk.Frame(circuit_frame, bg='#1a1a1a', relief=tk.SUNKEN, bd=3)
        canvas_container.pack(padx=20, pady=(0, 10))

        canvas_width = int(self.window_width * 0.85)
        canvas_height = int(self.window_height * 0.25)

        self.circuit_canvas = tk.Canvas(canvas_container, width=canvas_width, height=canvas_height,
                                       bg='#0a0a0a', highlightthickness=0)
        self.circuit_canvas.pack(padx=5, pady=5)

        self.canvas_width = canvas_width
        self.canvas_height = canvas_height

        # Create bottom section with gate palette and controls
        self.setup_bottom_section(parent)

    def setup_bottom_section(self, parent):
        """Setup the bottom section with gate palette on left, controls in middle, and results on right"""
        bottom_frame = tk.Frame(parent, bg='#2a2a2a')
        bottom_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))

        # Left side - Gate Palette (40% width)
        gate_frame = tk.Frame(bottom_frame, bg='#2a2a2a', relief=tk.RAISED, bd=2)
        gate_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

        # Gate palette title
        tk.Label(gate_frame, text="🎨 Gate Palette",
                font=('Arial', 14, 'bold'), fg='#f39c12', bg='#2a2a2a').pack(pady=(10, 10))

        # Create tabbed interface for gates
        gate_notebook = ttk.Notebook(gate_frame)
        gate_notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        # Single-qubit gates tab
        single_frame = ttk.Frame(gate_notebook)
        gate_notebook.add(single_frame, text="Single-Qubit Gates")
        self.setup_single_gate_controls(single_frame)

        # Multi-qubit gates tab
        multi_frame = ttk.Frame(gate_notebook)
        gate_notebook.add(multi_frame, text="Multi-Qubit Gates")
        self.setup_multi_gate_controls(multi_frame)

        # Middle section - Circuit Controls (30% width)
        controls_frame = tk.Frame(bottom_frame, bg='#2a2a2a', relief=tk.RAISED, bd=2)
        controls_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5)

        # Action buttons in middle section
        self.setup_action_buttons(controls_frame)

        # Right side - Quantum State Analysis (30% width)
        results_frame = tk.Frame(bottom_frame, bg='#2a2a2a', relief=tk.RAISED, bd=2)
        results_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))

        # Results area in right section
        self.setup_results_area(results_frame)

    def setup_action_buttons(self, parent):
        """Setup action buttons with enhanced styling in middle section"""
        # Title for action section
        action_title = tk.Label(parent, text="🎮 Circuit Controls",
                               font=('Arial', 14, 'bold'), fg='#00ff88', bg='#2a2a2a')
        action_title.pack(pady=(10, 15))

        # Create buttons container with fixed width and proper height
        action_frame = tk.Frame(parent, bg='#2a2a2a', width=250, height=350)  # Increased height for new button
        action_frame.pack(pady=(0, 15), padx=15)
        action_frame.pack_propagate(False)  # Maintain fixed size

        # Create enhanced buttons with hover effects
        buttons_data = [
            ("🚀 Run Circuit", self.run_circuit, '#00ff88', '#000000'),
            ("🔄 Clear Circuit", self.clear_circuit, '#ff6b6b', '#ffffff'),
            ("↶ Undo Last", self.undo_gate, '#f39c12', '#000000'),
            ("🌐 3D Visualizer", self.open_3d_visualizer, '#9b59b6', '#ffffff')  # New button
        ]

        # Create buttons in a vertical layout for the middle section
        for i, (text, command, bg_color, fg_color) in enumerate(buttons_data):
            # Button container with proper spacing
            btn_container = tk.Frame(action_frame, bg='#3a3a3a', relief=tk.RAISED, bd=2)
            btn_container.pack(fill=tk.X, pady=8, padx=5)  # Reduced padding for 4 buttons

            # Create the actual button
            btn = tk.Button(btn_container, text=text, command=command,
                           font=('Arial', 11, 'bold'), bg=bg_color, fg=fg_color,
                           padx=15, pady=10, cursor='hand2', relief=tk.FLAT, bd=0,  # Reduced pady
                           activebackground='#ffffff', activeforeground='#000000')
            btn.pack(padx=4, pady=4, fill=tk.X)

            # Store button reference for hover effects
            original_bg = bg_color

            def create_hover_functions(button, orig_color):
                def on_enter(event):
                    if orig_color == '#00ff88':
                        button.configure(bg='#ffffff', fg='#000000')
                    elif orig_color == '#ff6b6b':
                        button.configure(bg='#ffffff', fg='#000000')
                    elif orig_color == '#9b59b6':  # New color for 3D visualizer
                        button.configure(bg='#ffffff', fg='#000000')
                    else:
                        button.configure(bg='#ffffff', fg='#000000')

                def on_leave(event):
                    button.configure(bg=orig_color, fg=fg_color)

                return on_enter, on_leave

            on_enter, on_leave = create_hover_functions(btn, original_bg)
            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)

        # Add status info at the bottom of the controls
        status_frame = tk.Frame(action_frame, bg='#3a3a3a', relief=tk.SUNKEN, bd=1)
        status_frame.pack(fill=tk.X, pady=(15, 0), padx=5)  # Reduced top padding

        status_title = tk.Label(status_frame, text="📊 Circuit Status",
                               font=('Arial', 10, 'bold'), fg='#4ecdc4', bg='#3a3a3a')
        status_title.pack(pady=(5, 3))

        # Gates count
        self.gates_count_label = tk.Label(status_frame, text=f"Gates: {len(self.placed_gates)}",
                                         font=('Arial', 9), fg='#ffffff', bg='#3a3a3a')
        self.gates_count_label.pack(pady=2)

        # Qubits info
        self.qubits_info_label = tk.Label(status_frame, text=f"Qubits: {self.num_qubits}",
                                         font=('Arial', 9), fg='#ffffff', bg='#3a3a3a')
        self.qubits_info_label.pack(pady=(0, 5))


    def open_3d_visualizer(self):
        """Open the 3D quantum state visualizer window"""
        try:
            # Check if there are any gates to visualize
            if not self.placed_gates:
                messagebox.showinfo("3D Visualizer", "Add some gates to your circuit first to see the 3D visualization!")
                self.play_sound('error', self.play_error_sound_fallback)
                return

            # Play sound for button click
            self.play_sound('click')

            # Create the quantum circuit
            qc = QuantumCircuit(self.num_qubits)
            self.set_initial_state(qc)

            # Apply gates
            for gate, qubits in self.placed_gates:
                try:
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
                except Exception as gate_error:
                    print(f"Error applying gate {gate}: {str(gate_error)}")

            # Get the final state
            final_state = Statevector(qc)

            # Create and show the 3D visualization window
            self.show_3d_visualization(final_state)

        except ImportError as ie:
            messagebox.showerror("Import Error",
                f"Missing required packages for 3D visualization.\n\n"
                f"Please install: pip install matplotlib\n"
                f"Error: {str(ie)}")
            self.play_sound('error', self.play_error_sound_fallback)
        except Exception as e:
            messagebox.showerror("3D Visualizer Error",
                f"Error creating 3D visualization:\n{str(e)}")
            self.play_sound('error', self.play_error_sound_fallback)

    def show_3d_visualization(self, state_vector):
        """Show the 3D quantum state visualization in a new window"""
        try:
            # Create a new window for the 3D visualization
            viz_window = tk.Toplevel(self.root)
            viz_window.title("🌐 3D Quantum State Visualizer")
            viz_window.configure(bg='#1a1a1a')

            # Set window size and center it
            window_width = 900
            window_height = 700
            screen_width = viz_window.winfo_screenwidth()
            screen_height = viz_window.winfo_screenheight()
            x = (screen_width - window_width) // 2
            y = (screen_height - window_height) // 2
            viz_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

            # Create header
            header_frame = tk.Frame(viz_window, bg='#2a2a2a', relief=tk.RAISED, bd=2)
            header_frame.pack(fill=tk.X, padx=10, pady=(10, 5))

            header_title = tk.Label(header_frame, text="🌐 3D Quantum State Visualization",
                                   font=('Arial', 16, 'bold'), fg='#00ff88', bg='#2a2a2a')
            header_title.pack(pady=10)

            # Create info panel
            info_frame = tk.Frame(viz_window, bg='#2a2a2a', relief=tk.RAISED, bd=1)
            info_frame.pack(fill=tk.X, padx=10, pady=5)

            info_text = tk.Label(info_frame,
                text=f"Circuit: {self.num_qubits} qubits, {len(self.placed_gates)} gates | "
                     f"Gates: {[gate for gate, _ in self.placed_gates]}",
                font=('Arial', 10), fg='#4ecdc4', bg='#2a2a2a')
            info_text.pack(pady=8)

            # Create visualization container
            viz_container = tk.Frame(viz_window, bg='#1a1a1a', relief=tk.SUNKEN, bd=3)
            viz_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

            # Create matplotlib figure with dark theme
            plt.style.use('dark_background')

            # Choose visualization based on number of qubits
            if self.num_qubits == 1:
                # For single qubit, show Bloch sphere
                try:
                    fig = plot_bloch_multivector(state_vector)
                    fig.suptitle('Single Qubit Bloch Sphere Visualization',
                               fontsize=16, color='#00ff88', fontweight='bold')
                except Exception as bloch_error:
                    print(f"Bloch sphere error: {bloch_error}")
                    # Fallback to qsphere if bloch sphere fails
                    fig = plot_state_qsphere(state_vector)
                    fig.suptitle('Single Qubit Q-Sphere Visualization',
                               fontsize=16, color='#00ff88', fontweight='bold')

            else:
                # For multiple qubits, show Q-sphere
                fig = plot_state_qsphere(state_vector)
                fig.suptitle(f'{self.num_qubits}-Qubit Q-Sphere Visualization',
                           fontsize=16, color='#00ff88', fontweight='bold')

            # Customize the plot appearance
            fig.patch.set_facecolor('#1a1a1a')

            # Make sure all axes have dark background
            for ax in fig.get_axes():
                ax.set_facecolor('#1a1a1a')
                # Set text colors to be visible on dark background
                ax.tick_params(colors='white')
                ax.xaxis.label.set_color('white')
                ax.yaxis.label.set_color('white')
                if hasattr(ax, 'zaxis'):
                    ax.zaxis.label.set_color('white')

            # Embed the matplotlib figure in tkinter
            canvas = FigureCanvasTkAgg(fig, viz_container)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

            # Add control buttons at the bottom
            controls_frame = tk.Frame(viz_window, bg='#2a2a2a')
            controls_frame.pack(fill=tk.X, padx=10, pady=5)

            # Save button
            save_btn = tk.Button(controls_frame, text="💾 Save Image",
                               command=lambda: self.save_3d_visualization(fig),
                               font=('Arial', 10, 'bold'), bg='#4ecdc4', fg='#000000',
                               padx=15, pady=8, cursor='hand2', relief=tk.RAISED, bd=2)
            save_btn.pack(side=tk.LEFT, padx=5)

            # Refresh button
            refresh_btn = tk.Button(controls_frame, text="🔄 Refresh",
                                  command=lambda: self.refresh_3d_visualization(viz_window, state_vector),
                                  font=('Arial', 10, 'bold'), bg='#f39c12', fg='#000000',
                                  padx=15, pady=8, cursor='hand2', relief=tk.RAISED, bd=2)
            refresh_btn.pack(side=tk.LEFT, padx=5)

            # Close button
            close_btn = tk.Button(controls_frame, text="❌ Close",
                                command=viz_window.destroy,
                                font=('Arial', 10, 'bold'), bg='#ff6b6b', fg='#ffffff',
                                padx=15, pady=8, cursor='hand2', relief=tk.RAISED, bd=2)
            close_btn.pack(side=tk.RIGHT, padx=5)

            # Add some state information
            state_info_frame = tk.Frame(viz_window, bg='#2a2a2a', relief=tk.RAISED, bd=1)
            state_info_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

            # Calculate and display state information
            state_data = state_vector.data
            entangled = self.is_state_entangled(state_vector) if self.num_qubits > 1 else False

            info_text = f"🔬 State Analysis: "
            if entangled:
                info_text += "Entangled state detected! "
            else:
                info_text += "Separable state. "

            # Count significant amplitudes
            significant_states = sum(1 for amp in state_data if abs(amp) > 0.001)
            info_text += f"Active basis states: {significant_states}/{2**self.num_qubits}"

            state_label = tk.Label(state_info_frame, text=info_text,
                                 font=('Arial', 10), fg='#ffffff', bg='#2a2a2a')
            state_label.pack(pady=8)

            # Play success sound
            self.play_sound('success', self.play_success_sound_fallback)

        except Exception as e:
            messagebox.showerror("Visualization Error",
                f"Error creating 3D visualization:\n{str(e)}")
            self.play_sound('error', self.play_error_sound_fallback)
            print(f"Full visualization error: {e}")
            import traceback
            traceback.print_exc()

    def is_state_entangled(self, state_vector):
        """Simple check for entanglement (for educational purposes)"""
        try:
            if self.num_qubits != 2:
                return False  # Simple check only for 2 qubits

            # For a 2-qubit state to be separable, it should be expressible as |a⟩⊗|b⟩
            # This is a simplified check
            state_data = state_vector.data

            # Check if the state can be written as a product state
            # |00⟩ + |11⟩ (Bell state) would be entangled
            # |00⟩ or |01⟩ or |10⟩ or |11⟩ would be separable

            # Count non-zero amplitudes
            non_zero_count = sum(1 for amp in state_data if abs(amp) > 0.001)

            # If more than one basis state has significant amplitude, might be entangled
            # This is a very simplified check
            return non_zero_count > 1 and not (abs(state_data[0]) > 0.99 or abs(state_data[1]) > 0.99 or
                                             abs(state_data[2]) > 0.99 or abs(state_data[3]) > 0.99)
        except:
            return False

    def save_3d_visualization(self, fig):
        """Save the 3D visualization as an image"""
        try:
            from tkinter import filedialog

            filename = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), ("PDF files", "*.pdf"), ("SVG files", "*.svg")],
                title="Save 3D Visualization"
            )

            if filename:
                fig.savefig(filename, dpi=300, bbox_inches='tight',
                          facecolor='#1a1a1a', edgecolor='none')
                messagebox.showinfo("Success", f"Visualization saved as {filename}")
                self.play_sound('success', self.play_success_sound_fallback)

        except Exception as e:
            messagebox.showerror("Save Error", f"Error saving visualization:\n{str(e)}")
            self.play_sound('error', self.play_error_sound_fallback)

    def refresh_3d_visualization(self, viz_window, state_vector):
        """Refresh the 3D visualization"""
        try:
            # Close current window and reopen with updated state
            viz_window.destroy()
            self.open_3d_visualizer()
        except Exception as e:
            messagebox.showerror("Refresh Error", f"Error refreshing visualization:\n{str(e)}")


    def setup_results_area(self, parent):
        """Setup the results display area on the right side"""
        # Enhanced title
        results_title = tk.Label(parent, text="📊 Quantum State Analysis",
                                font=('Arial', 14, 'bold'), fg='#00ff88', bg='#2a2a2a')
        results_title.pack(pady=(10, 15))

        # Results container with styling
        results_container = tk.Frame(parent, bg='#1a1a1a', relief=tk.SUNKEN, bd=3)
        results_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        # Enhanced results text with scrollbar
        text_frame = tk.Frame(results_container, bg='#1a1a1a')
        text_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.results_text = tk.Text(text_frame, width=40,  # Fixed width for right panel
                                   font=('Consolas', 9), bg='#0a0a0a', fg='#00ff88',
                                   relief=tk.FLAT, bd=0, insertbackground='#00ff88',
                                   selectbackground='#4ecdc4', selectforeground='#000000',
                                   wrap=tk.WORD)

        # Add scrollbar
        scrollbar = tk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.results_text.yview,
                                bg='#3a3a3a', troughcolor='#1a1a1a', activebackground='#4ecdc4')
        self.results_text.configure(yscrollcommand=scrollbar.set)

        self.results_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Initial message
        self.results_text.insert(tk.END, "🌟 Welcome to Quantum Circuit Sandbox!\n\n")
        self.results_text.insert(tk.END, "Build your circuit and click 'Run Circuit' to see the results.\n\n")
        self.results_text.insert(tk.END, "📝 Instructions:\n")
        self.results_text.insert(tk.END, "1. Select gates from the palette\n")
        self.results_text.insert(tk.END, "2. Configure qubits and initial states\n")
        self.results_text.insert(tk.END, "3. Run your circuit to see quantum state analysis\n")
        self.results_text.configure(state=tk.DISABLED)

    def setup_single_gate_controls(self, parent):
        """Setup single-qubit gate controls with centered 2x3 grid layout"""
        # Create a frame that works with ttk parent
        container = tk.Frame(parent)
        container.configure(bg='#2a2a2a')
        container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Target qubit selection at top
        qubit_frame = tk.Frame(container, bg='#3a3a3a', relief=tk.RAISED, bd=1)
        qubit_frame.pack(fill=tk.X, pady=(0, 15), padx=5, ipady=8)

        tk.Label(qubit_frame, text="🎯 Target Qubit:",
                font=('Arial', 11, 'bold'), fg='#ffffff', bg='#3a3a3a').pack(side=tk.LEFT, padx=(10, 5))

        self.target_qubit_var = tk.IntVar(value=0)
        self.target_qubit_combo = ttk.Combobox(qubit_frame, textvariable=self.target_qubit_var,
                                            values=list(range(self.num_qubits)), state="readonly",
                                            font=('Arial', 10), width=5)
        self.target_qubit_combo.pack(side=tk.LEFT, padx=5)

        # Gate buttons section
        gates_title = tk.Label(container, text="Single-Qubit Gates:",
                            font=('Arial', 12, 'bold'), fg='#ffffff', bg='#2a2a2a')
        gates_title.pack(pady=(5, 10))

        # Create centered container for the grid
        grid_container = tk.Frame(container, bg='#2a2a2a')
        grid_container.pack(expand=True)  # This centers the grid

        gate_colors = {
            'H': '#ff6b6b', 'X': '#4ecdc4', 'Y': '#45b7d1',
            'Z': '#96ceb4', 'S': '#feca57', 'T': '#ff9ff3'
        }

        gate_descriptions = {
            'H': 'Hadamard',
            'X': 'Pauli-X',
            'Y': 'Pauli-Y',
            'Z': 'Pauli-Z',
            'S': 'S Gate',
            'T': 'T Gate'
        }

        single_gates = ['H', 'X', 'Y', 'Z', 'S', 'T']

        # Create centered 2x3 grid (2 rows, 3 columns)
        for row in range(2):
            row_frame = tk.Frame(grid_container, bg='#2a2a2a')
            row_frame.pack(pady=5)

            for col in range(3):
                gate_index = row * 3 + col
                if gate_index < len(single_gates):
                    gate = single_gates[gate_index]
                    color = gate_colors.get(gate, '#ffffff')
                    description = gate_descriptions.get(gate, '')

                    # Create button container with fixed size
                    btn_container = tk.Frame(row_frame, bg='#3a3a3a', relief=tk.RAISED, bd=1)
                    btn_container.pack(side=tk.LEFT, padx=8, pady=2)

                    # Create button with fixed dimensions
                    btn = tk.Button(btn_container, text=gate,
                                    command=lambda g=gate: self.add_single_gate(g),
                                    font=('Arial', 12, 'bold'),
                                    bg=color, fg='#000000',
                                    width=8, height=2, cursor='hand2',
                                    relief=tk.FLAT, bd=0)
                    btn.pack(padx=3, pady=3)

                    # Description label
                    desc_label = tk.Label(btn_container, text=description,
                                        font=('Arial', 8), fg='#cccccc', bg='#3a3a3a')
                    desc_label.pack(pady=(0, 3))

    def setup_multi_gate_controls(self, parent):
        """Setup multi-qubit gate controls with enhanced styling"""
        # Create a frame that works with ttk parent
        container = tk.Frame(parent)
        container.configure(bg='#2a2a2a')
        container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Title
        title_label = tk.Label(container, text="Multi-Qubit Gates:",
                              font=('Arial', 12, 'bold'), fg='#ffffff', bg='#2a2a2a')
        title_label.pack(pady=(0, 10))

        # CNOT Gate section with compact layout
        cnot_frame = tk.Frame(container, bg='#3a3a3a', relief=tk.RAISED, bd=2)
        cnot_frame.pack(fill=tk.X, pady=3, ipady=10)

        cnot_title = tk.Label(cnot_frame, text="🔗 CNOT Gate",
                            font=('Arial', 10, 'bold'), fg='#ffeaa7', bg='#3a3a3a')
        cnot_title.pack(pady=(3, 5))

        cnot_controls = tk.Frame(cnot_frame, bg='#3a3a3a')
        cnot_controls.pack()

        # CNOT Controls in compact layout
        tk.Label(cnot_controls, text="Control:", font=('Arial', 9),
                fg='#ffffff', bg='#3a3a3a').pack(side=tk.LEFT, padx=(5, 2))

        self.cnot_control_var = tk.IntVar(value=0)
        self.cnot_control_combo = ttk.Combobox(cnot_controls, textvariable=self.cnot_control_var,
                                            values=list(range(self.num_qubits)), state="readonly",
                                            font=('Arial', 9), width=3)
        self.cnot_control_combo.pack(side=tk.LEFT, padx=2)

        tk.Label(cnot_controls, text="T:", font=('Arial', 9),
                fg='#ffffff', bg='#3a3a3a').pack(side=tk.LEFT, padx=(5, 2))

        self.cnot_target_var = tk.IntVar(value=1 if self.num_qubits > 1 else 0)
        self.cnot_target_combo = ttk.Combobox(cnot_controls, textvariable=self.cnot_target_var,
                                            values=list(range(self.num_qubits)), state="readonly",
                                            font=('Arial', 9), width=3)
        self.cnot_target_combo.pack(side=tk.LEFT, padx=2)

        # CNOT button
        cnot_btn = tk.Button(cnot_controls, text="Add",
                            command=self.add_cnot_gate,
                            font=('Arial', 9, 'bold'), bg='#ffeaa7', fg='#000000',
                            padx=10, pady=3, cursor='hand2', relief=tk.RAISED, bd=1)
        cnot_btn.pack(side=tk.LEFT, padx=8)

        # CZ Gate section with compact layout
        cz_frame = tk.Frame(container, bg='#3a3a3a', relief=tk.RAISED, bd=2)
        cz_frame.pack(fill=tk.X, pady=3, ipady=10)

        cz_title = tk.Label(cz_frame, text="⭐ CZ Gate",
                           font=('Arial', 10, 'bold'), fg='#a29bfe', bg='#3a3a3a')
        cz_title.pack(pady=(3, 5))

        cz_controls = tk.Frame(cz_frame, bg='#3a3a3a')
        cz_controls.pack()

        # CZ Controls in compact layout
        tk.Label(cz_controls, text="Control:", font=('Arial', 9),
                fg='#ffffff', bg='#3a3a3a').pack(side=tk.LEFT, padx=(5, 2))

        self.cz_control_var = tk.IntVar(value=0)
        self.cz_control_combo = ttk.Combobox(cz_controls, textvariable=self.cz_control_var,
                                           values=list(range(self.num_qubits)), state="readonly",
                                           font=('Arial', 9), width=3)
        self.cz_control_combo.pack(side=tk.LEFT, padx=2)

        tk.Label(cz_controls, text="Target:", font=('Arial', 9),
                fg='#ffffff', bg='#3a3a3a').pack(side=tk.LEFT, padx=(5, 2))

        self.cz_target_var = tk.IntVar(value=1 if self.num_qubits > 1 else 0)
        self.cz_target_combo = ttk.Combobox(cz_controls, textvariable=self.cz_target_var,
                                          values=list(range(self.num_qubits)), state="readonly",
                                          font=('Arial', 9), width=3)
        self.cz_target_combo.pack(side=tk.LEFT, padx=2)

        # CZ button
        cz_btn = tk.Button(cz_controls, text="Add",
                          command=self.add_cz_gate,
                          font=('Arial', 9, 'bold'), bg='#a29bfe', fg='#000000',
                          padx=10, pady=3, cursor='hand2', relief=tk.RAISED, bd=1)
        cz_btn.pack(side=tk.LEFT, padx=8)

        # Toffoli Gate section (only show if 3+ qubits) with compact layout
        if self.num_qubits >= 3:
            toffoli_frame = tk.Frame(container, bg='#3a3a3a', relief=tk.RAISED, bd=2)
            toffoli_frame.pack(fill=tk.X, pady=3, ipady=10)

            toffoli_title = tk.Label(toffoli_frame, text="🎯 Toffoli Gate",
                                   font=('Arial', 10, 'bold'), fg='#fd79a8', bg='#3a3a3a')
            toffoli_title.pack(pady=(3, 5))

            toffoli_controls = tk.Frame(toffoli_frame, bg='#3a3a3a')
            toffoli_controls.pack()

            # Toffoli Controls in compact layout
            tk.Label(toffoli_controls, text="C1:", font=('Arial', 9),
                    fg='#ffffff', bg='#3a3a3a').pack(side=tk.LEFT, padx=(3, 1))

            self.toffoli_c1_var = tk.IntVar(value=0)
            self.toffoli_c1_combo = ttk.Combobox(toffoli_controls, textvariable=self.toffoli_c1_var,
                                               values=list(range(self.num_qubits)), state="readonly",
                                               font=('Arial', 8), width=2)
            self.toffoli_c1_combo.pack(side=tk.LEFT, padx=1)

            tk.Label(toffoli_controls, text="C2:", font=('Arial', 9),
                    fg='#ffffff', bg='#3a3a3a').pack(side=tk.LEFT, padx=(3, 1))

            self.toffoli_c2_var = tk.IntVar(value=1)
            self.toffoli_c2_combo = ttk.Combobox(toffoli_controls, textvariable=self.toffoli_c2_var,
                                               values=list(range(self.num_qubits)), state="readonly",
                                               font=('Arial', 8), width=2)
            self.toffoli_c2_combo.pack(side=tk.LEFT, padx=1)

            tk.Label(toffoli_controls, text="Target:", font=('Arial', 9),
                    fg='#ffffff', bg='#3a3a3a').pack(side=tk.LEFT, padx=(3, 1))

            self.toffoli_target_var = tk.IntVar(value=2)
            self.toffoli_target_combo = ttk.Combobox(toffoli_controls, textvariable=self.toffoli_target_var,
                                                   values=list(range(self.num_qubits)), state="readonly",
                                                   font=('Arial', 8), width=2)
            self.toffoli_target_combo.pack(side=tk.LEFT, padx=1)

            # Toffoli button
            toffoli_btn = tk.Button(toffoli_controls, text="Add",
                                  command=self.add_toffoli_gate,
                                  font=('Arial', 9, 'bold'), bg='#fd79a8', fg='#000000',
                                  padx=8, pady=3, cursor='hand2', relief=tk.RAISED, bd=1)
            toffoli_btn.pack(side=tk.LEFT, padx=5)

    def setup_gate_panel(self, parent):
        """Setup the gate selection panel"""
        gate_frame = tk.Frame(parent, bg='#2a2a2a')
        gate_frame.pack(fill=tk.X, padx=20, pady=10)

        tk.Label(gate_frame, text="Available Gates:",
                font=('Arial', 12, 'bold'), fg='#ffffff', bg='#2a2a2a').pack(anchor=tk.W)

        # Gate buttons and qubit selection
        buttons_frame = tk.Frame(gate_frame, bg='#2a2a2a')
        buttons_frame.pack(fill=tk.X, pady=5)

        # Qubit selection for single-qubit gates
        qubit_select_frame = tk.Frame(buttons_frame, bg='#2a2a2a')
        qubit_select_frame.pack(side=tk.LEFT, padx=(0, 20))

        tk.Label(qubit_select_frame, text="Target Qubit:",
                font=('Arial', 10), fg='#ffffff', bg='#2a2a2a').pack()

        self.target_qubit_var = tk.IntVar(value=0)
        self.target_qubit_combo = ttk.Combobox(qubit_select_frame, textvariable=self.target_qubit_var,
                                            values=list(range(self.num_qubits)), state="readonly",
                                            font=('Arial', 10), width=5)
        self.target_qubit_combo.pack()

        # Single-qubit gates
        single_gates_frame = tk.Frame(buttons_frame, bg='#2a2a2a')
        single_gates_frame.pack(side=tk.LEFT, padx=10)

        tk.Label(single_gates_frame, text="Single-Qubit Gates:",
                font=('Arial', 10), fg='#ffffff', bg='#2a2a2a').pack()

        single_gates_buttons = tk.Frame(single_gates_frame, bg='#2a2a2a')
        single_gates_buttons.pack()

        gate_colors = {
            'H': '#ff6b6b', 'X': '#4ecdc4', 'Y': '#45b7d1', 'Z': '#96ceb4',
            'S': '#feca57', 'T': '#ff9ff3'
        }

        single_gates = ['H', 'X', 'Y', 'Z', 'S', 'T']
        for gate in single_gates:
            color = gate_colors.get(gate, '#ffffff')
            btn = tk.Button(single_gates_buttons, text=gate,
                        command=lambda g=gate: self.add_single_gate(g),
                        font=('Arial', 10, 'bold'), bg=color, fg='#000000',
                        width=6, height=1)
            btn.pack(side=tk.LEFT, padx=2, pady=2)

        # Multi-qubit gates section
        multi_gates_frame = tk.Frame(buttons_frame, bg='#2a2a2a')
        multi_gates_frame.pack(side=tk.LEFT, padx=20)

        tk.Label(multi_gates_frame, text="Multi-Qubit Gates:",
                font=('Arial', 10), fg='#ffffff', bg='#2a2a2a').pack()

        # CNOT controls
        cnot_frame = tk.Frame(multi_gates_frame, bg='#2a2a2a')
        cnot_frame.pack(pady=2)

        tk.Label(cnot_frame, text="CNOT - Control:", font=('Arial', 9),
                fg='#ffffff', bg='#2a2a2a').pack(side=tk.LEFT)

        self.cnot_control_var = tk.IntVar(value=0)
        self.cnot_control_combo = ttk.Combobox(cnot_frame, textvariable=self.cnot_control_var,
                                            values=list(range(self.num_qubits)), state="readonly",
                                            font=('Arial', 9), width=3)
        self.cnot_control_combo.pack(side=tk.LEFT, padx=2)

        tk.Label(cnot_frame, text="Target:", font=('Arial', 9),
                fg='#ffffff', bg='#2a2a2a').pack(side=tk.LEFT, padx=(5, 0))

        self.cnot_target_var = tk.IntVar(value=1 if self.num_qubits > 1 else 0)
        self.cnot_target_combo = ttk.Combobox(cnot_frame, textvariable=self.cnot_target_var,
                                            values=list(range(self.num_qubits)), state="readonly",
                                            font=('Arial', 9), width=3)
        self.cnot_target_combo.pack(side=tk.LEFT, padx=2)

        cnot_btn = tk.Button(cnot_frame, text="CNOT",
                            command=self.add_cnot_gate,
                            font=('Arial', 9, 'bold'), bg='#ffeaa7', fg='#000000',
                            width=6, height=1)
        cnot_btn.pack(side=tk.LEFT, padx=5)

        # CZ controls
        cz_frame = tk.Frame(multi_gates_frame, bg='#2a2a2a')
        cz_frame.pack(pady=2)

        tk.Label(cz_frame, text="CZ - Control:", font=('Arial', 9),
                fg='#ffffff', bg='#2a2a2a').pack(side=tk.LEFT)

        self.cz_control_var = tk.IntVar(value=0)
        self.cz_control_combo = ttk.Combobox(cz_frame, textvariable=self.cz_control_var,
                                            values=list(range(self.num_qubits)), state="readonly",
                                            font=('Arial', 9), width=3)
        self.cz_control_combo.pack(side=tk.LEFT, padx=2)

        tk.Label(cz_frame, text="Target:", font=('Arial', 9),
                fg='#ffffff', bg='#2a2a2a').pack(side=tk.LEFT, padx=(5, 0))

        self.cz_target_var = tk.IntVar(value=1 if self.num_qubits > 1 else 0)
        self.cz_target_combo = ttk.Combobox(cz_frame, textvariable=self.cz_target_var,
                                        values=list(range(self.num_qubits)), state="readonly",
                                        font=('Arial', 9), width=3)
        self.cz_target_combo.pack(side=tk.LEFT, padx=2)

        cz_btn = tk.Button(cz_frame, text="CZ",
                        command=self.add_cz_gate,
                        font=('Arial', 9, 'bold'), bg='#a29bfe', fg='#000000',
                        width=6, height=1)
        cz_btn.pack(side=tk.LEFT, padx=5)

        # Toffoli controls (if 3+ qubits)
        if self.num_qubits >= 3:
            toffoli_frame = tk.Frame(multi_gates_frame, bg='#2a2a2a')
            toffoli_frame.pack(pady=2)

            tk.Label(toffoli_frame, text="Toffoli - C1:", font=('Arial', 9),
                    fg='#ffffff', bg='#2a2a2a').pack(side=tk.LEFT)

            self.toffoli_c1_var = tk.IntVar(value=0)
            self.toffoli_c1_combo = ttk.Combobox(toffoli_frame, textvariable=self.toffoli_c1_var,
                                                values=list(range(self.num_qubits)), state="readonly",
                                                font=('Arial', 9), width=3)
            self.toffoli_c1_combo.pack(side=tk.LEFT, padx=2)

            tk.Label(toffoli_frame, text="C2:", font=('Arial', 9),
                    fg='#ffffff', bg='#2a2a2a').pack(side=tk.LEFT, padx=(5, 0))

            self.toffoli_c2_var = tk.IntVar(value=1)
            self.toffoli_c2_combo = ttk.Combobox(toffoli_frame, textvariable=self.toffoli_c2_var,
                                                values=list(range(self.num_qubits)), state="readonly",
                                                font=('Arial', 9), width=3)
            self.toffoli_c2_combo.pack(side=tk.LEFT, padx=2)

            tk.Label(toffoli_frame, text="T:", font=('Arial', 9),
                    fg='#ffffff', bg='#2a2a2a').pack(side=tk.LEFT, padx=(5, 0))

            self.toffoli_target_var = tk.IntVar(value=2)
            self.toffoli_target_combo = ttk.Combobox(toffoli_frame, textvariable=self.toffoli_target_var,
                                                    values=list(range(self.num_qubits)), state="readonly",
                                                    font=('Arial', 9), width=3)
            self.toffoli_target_combo.pack(side=tk.LEFT, padx=2)

            toffoli_btn = tk.Button(toffoli_frame, text="Toffoli",
                                command=self.add_toffoli_gate,
                                font=('Arial', 9, 'bold'), bg='#fd79a8', fg='#000000',
                                width=6, height=1)
            toffoli_btn.pack(side=tk.LEFT, padx=5)

    def add_single_gate(self, gate):
        """Add a single-qubit gate to the selected qubit"""
        target_qubit = self.target_qubit_var.get()

        if target_qubit >= self.num_qubits:
            messagebox.showwarning("Warning", "Invalid target qubit selected")
            self.play_sound('error', self.play_error_sound_fallback)
            return

        self.placed_gates.append((gate, [target_qubit]))
        self.update_circuit_display()
        self.play_sound('gate_place', self.play_gate_sound_fallback)

    def add_cnot_gate(self):
        """Add a CNOT gate"""
        if self.num_qubits < 2:
            messagebox.showwarning("Warning", "CNOT gate requires at least 2 qubits")
            self.play_sound('error', self.play_error_sound_fallback)
            return

        control = self.cnot_control_var.get()
        target = self.cnot_target_var.get()

        if control == target:
            messagebox.showwarning("Warning", "Control and target qubits must be different")
            self.play_sound('error', self.play_error_sound_fallback)
            return

        if control >= self.num_qubits or target >= self.num_qubits:
            messagebox.showwarning("Warning", "Invalid qubit selection")
            self.play_sound('error', self.play_error_sound_fallback)
            return

        self.placed_gates.append(('CNOT', [control, target]))
        self.update_circuit_display()
        self.play_sound('gate_place', self.play_gate_sound_fallback)

    def add_cz_gate(self):
        """Add a CZ gate"""
        if self.num_qubits < 2:
            messagebox.showwarning("Warning", "CZ gate requires at least 2 qubits")
            self.play_sound('error', self.play_error_sound_fallback)
            return

        control = self.cz_control_var.get()
        target = self.cz_target_var.get()

        if control == target:
            messagebox.showwarning("Warning", "Control and target qubits must be different")
            self.play_sound('error', self.play_error_sound_fallback)
            return

        if control >= self.num_qubits or target >= self.num_qubits:
            messagebox.showwarning("Warning", "Invalid qubit selection")
            self.play_sound('error', self.play_error_sound_fallback)
            return

        self.placed_gates.append(('CZ', [control, target]))
        self.update_circuit_display()
        self.play_sound('gate_place', self.play_gate_sound_fallback)

    def add_toffoli_gate(self):
        """Add a Toffoli gate"""
        if self.num_qubits < 3:
            messagebox.showwarning("Warning", "Toffoli gate requires at least 3 qubits")
            self.play_sound('error', self.play_error_sound_fallback)
            return

        c1 = self.toffoli_c1_var.get()
        c2 = self.toffoli_c2_var.get()
        target = self.toffoli_target_var.get()

        if len(set([c1, c2, target])) != 3:
            messagebox.showwarning("Warning", "All three qubits must be different")
            self.play_sound('error', self.play_error_sound_fallback)
            return

        if c1 >= self.num_qubits or c2 >= self.num_qubits or target >= self.num_qubits:
            messagebox.showwarning("Warning", "Invalid qubit selection")
            self.play_sound('error', self.play_error_sound_fallback)
            return

        self.placed_gates.append(('Toffoli', [c1, c2, target]))
        self.update_circuit_display()
        self.play_sound('gate_place', self.play_gate_sound_fallback)

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

        # Clear and update results
        self.results_text.configure(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, "🧹 Circuit cleared. Ready for new gates.\n")
        self.results_text.insert(tk.END, "Add gates using the Gate Palette and click 'Run Circuit' to see results.\n")
        self.results_text.configure(state=tk.DISABLED)

        self.play_sound('clear', self.play_clear_sound_fallback)


    def undo_gate(self):
        """Remove the last placed gate"""
        if self.placed_gates:
            removed_gate = self.placed_gates.pop()
            self.update_circuit_display()

            # Update results
            self.results_text.configure(state=tk.NORMAL)
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, f"↶ Undid last gate: {removed_gate[0]}\n")
            self.results_text.insert(tk.END, f"Gates remaining: {len(self.placed_gates)}\n")
            self.results_text.configure(state=tk.DISABLED)

            self.play_sound('click')
        else:
            # No gates to undo
            self.results_text.configure(state=tk.NORMAL)
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, "❌ No gates to undo.\n")
            self.results_text.configure(state=tk.DISABLED)
            self.play_sound('error', self.play_error_sound_fallback)

    def on_qubit_change(self):
        """Handle change in number of qubits"""
        self.num_qubits = self.qubit_var.get()
        self.placed_gates = []  # Clear gates when changing qubit count

        # Update available initial states based on qubit count
        if self.num_qubits == 1:
            states = ["|0⟩", "|1⟩", "|+⟩", "|-⟩"]
        elif self.num_qubits == 2:
            states = ["|00⟩", "|01⟩", "|10⟩", "|11⟩", "|++⟩"]
        elif self.num_qubits == 3:
            states = ["|000⟩", "|001⟩", "|010⟩", "|011⟩", "|100⟩", "|101⟩", "|110⟩", "|111⟩"]
        elif self.num_qubits == 4:
            states = ["|0000⟩", "|0001⟩", "|0010⟩", "|0011⟩", "|0100⟩", "|0101⟩", "|0110⟩", "|0111⟩",
                "|1000⟩", "|1001⟩", "|1010⟩", "|1011⟩", "|1100⟩", "|1101⟩", "|1110⟩", "|1111⟩"]
        else:
            states = ["|" + "0" * self.num_qubits + "⟩"]

        self.update_state_combobox(states)
        self.state_var.set(states[0])
        self.initial_state = states[0]

        # Update the qubit selection dropdowns
        self.update_qubit_selections()

        self.update_circuit_display()

    def update_qubit_selections(self):
        """Update all qubit selection dropdowns when number of qubits changes"""
        qubit_range = list(range(self.num_qubits))

        # Update target qubit combo
        if hasattr(self, 'target_qubit_combo'):
            self.target_qubit_combo['values'] = qubit_range
            if self.target_qubit_var.get() >= self.num_qubits:
                self.target_qubit_var.set(0)

        # Update CNOT controls directly using stored references
        if hasattr(self, 'cnot_control_combo'):
            self.cnot_control_combo['values'] = qubit_range
            if self.cnot_control_var.get() >= self.num_qubits:
                self.cnot_control_var.set(0)

        if hasattr(self, 'cnot_target_combo'):
            self.cnot_target_combo['values'] = qubit_range
            if self.cnot_target_var.get() >= self.num_qubits:
                self.cnot_target_var.set(1 if self.num_qubits > 1 else 0)

        # Update CZ controls directly using stored references
        if hasattr(self, 'cz_control_combo'):
            self.cz_control_combo['values'] = qubit_range
            if self.cz_control_var.get() >= self.num_qubits:
                self.cz_control_var.set(0)

        if hasattr(self, 'cz_target_combo'):
            self.cz_target_combo['values'] = qubit_range
            if self.cz_target_var.get() >= self.num_qubits:
                self.cz_target_var.set(1 if self.num_qubits > 1 else 0)

        # Update Toffoli controls directly using stored references
        if hasattr(self, 'toffoli_c1_combo'):
            self.toffoli_c1_combo['values'] = qubit_range
            if self.toffoli_c1_var.get() >= self.num_qubits:
                self.toffoli_c1_var.set(0)

        if hasattr(self, 'toffoli_c2_combo'):
            self.toffoli_c2_combo['values'] = qubit_range
            if self.toffoli_c2_var.get() >= self.num_qubits:
                self.toffoli_c2_var.set(1 if self.num_qubits > 1 else 0)

        if hasattr(self, 'toffoli_target_combo'):
            self.toffoli_target_combo['values'] = qubit_range
            if self.toffoli_target_var.get() >= self.num_qubits:
                self.toffoli_target_var.set(2 if self.num_qubits > 2 else 0)

        # Handle Toffoli visibility for 3+ qubits
        self.update_toffoli_visibility()

    def update_toffoli_visibility(self):
        """Show/hide Toffoli controls based on number of qubits"""
        # This is a simplified approach - in a production app you might want
        # to rebuild the entire gate panel, but this preserves the existing widgets
        pass

    def update_state_combobox(self, states):
        """Update the state combobox with new values"""
        # Find and update the combobox
        # This is a bit tricky since we need to access the widget
        # Let's store a reference to the combobox in setup_control_panel
        if hasattr(self, 'state_combo'):
            self.state_combo['values'] = states

    def on_state_change(self, event=None):
        """Handle change in initial state"""
        self.initial_state = self.state_var.get()
        self.update_circuit_display()

    def update_circuit_display(self):
        """Update the circuit visualization with enhanced graphics"""
        self.circuit_canvas.delete("all")

        if self.num_qubits == 0:
            return

        # Enhanced circuit drawing parameters
        wire_start = 60
        wire_end = self.canvas_width - 60
        qubit_spacing = max(40, self.canvas_height // (self.num_qubits + 2))

        # Draw enhanced background grid
        for i in range(0, self.canvas_width, 50):
            self.circuit_canvas.create_line(i, 0, i, self.canvas_height,
                                          fill='#1a1a1a', width=1)

        # Draw enhanced qubit wires with colors
        wire_colors = ['#ff6b6b', '#4ecdc4', '#f39c12', '#a29bfe']

        for qubit in range(self.num_qubits):
            y_pos = (qubit + 1) * qubit_spacing + 20
            color = wire_colors[qubit % len(wire_colors)]

            # Draw wire with gradient effect (multiple lines for thickness)
            for thickness in [6, 4, 2]:
                alpha = 0.3 + (thickness / 6) * 0.7
                self.circuit_canvas.create_line(wire_start, y_pos, wire_end, y_pos,
                                              fill=color, width=thickness)

            # Enhanced qubit label with background
            label_bg = self.circuit_canvas.create_rectangle(wire_start - 35, y_pos - 12,
                                                          wire_start - 5, y_pos + 12,
                                                          fill='#3a3a3a', outline=color, width=2)

            self.circuit_canvas.create_text(wire_start - 20, y_pos,
                                          text=f"q{qubit}", fill='#ffffff',
                                          font=('Arial', 10, 'bold'))

        # Draw enhanced gates
        self.draw_enhanced_gates(wire_start, qubit_spacing)

        # Update status labels if they exist
        if hasattr(self, 'gates_count_label'):
            self.gates_count_label.configure(text=f"Gates: {len(self.placed_gates)}")
        if hasattr(self, 'qubits_info_label'):
            self.qubits_info_label.configure(text=f"Qubits: {self.num_qubits}")

    def draw_enhanced_gates(self, wire_start, qubit_spacing):
        """Draw gates with enhanced 3D styling"""
        gate_x_start = wire_start + 100
        gate_spacing = 100

        gate_colors = {
            'H': '#ff6b6b', 'X': '#4ecdc4', 'Y': '#45b7d1', 'Z': '#96ceb4',
            'S': '#feca57', 'T': '#ff9ff3', 'CNOT': '#ffeaa7', 'CZ': '#a29bfe'
        }

        for i, (gate, qubits) in enumerate(self.placed_gates):
            x = gate_x_start + i * gate_spacing
            color = gate_colors.get(gate, '#ffffff')

            if len(qubits) == 1:
                # Enhanced single qubit gate
                qubit = qubits[0]
                if qubit < self.num_qubits:
                    y_pos = (qubit + 1) * qubit_spacing + 20

                    # 3D shadow effect
                    self.circuit_canvas.create_rectangle(x - 22, y_pos - 17,
                                                        x + 22, y_pos + 17,
                                                        fill='#000000', outline='')

                    # Main gate with gradient effect
                    self.circuit_canvas.create_rectangle(x - 20, y_pos - 15,
                                                        x + 20, y_pos + 15,
                                                        fill=color, outline='#ffffff', width=2)

                    # Inner highlight
                    self.circuit_canvas.create_rectangle(x - 18, y_pos - 13,
                                                        x + 18, y_pos + 13,
                                                        fill='', outline='#ffffff', width=1)

                    # Gate symbol with shadow
                    self.circuit_canvas.create_text(x + 1, y_pos + 1, text=gate,
                                                   fill='#000000', font=('Arial', 11, 'bold'))
                    self.circuit_canvas.create_text(x, y_pos, text=gate,
                                                   fill='#000000', font=('Arial', 12, 'bold'))

            elif len(qubits) == 2 and gate in ['CNOT', 'CZ']:
                # Enhanced two-qubit gate
                control_qubit, target_qubit = qubits
                if control_qubit < self.num_qubits and target_qubit < self.num_qubits:
                    control_y = (control_qubit + 1) * qubit_spacing + 20
                    target_y = (target_qubit + 1) * qubit_spacing + 20

                    # Enhanced control dot with 3D effect
                    self.circuit_canvas.create_oval(x - 10, control_y - 10,
                                                   x + 10, control_y + 10,
                                                   fill='#000000', outline='')
                    self.circuit_canvas.create_oval(x - 8, control_y - 8,
                                                   x + 8, control_y + 8,
                                                   fill='#ffffff', outline='#cccccc', width=2)

                    # Enhanced connection line
                    self.circuit_canvas.create_line(x, control_y, x, target_y,
                                                   fill='#ffffff', width=4)
                    self.circuit_canvas.create_line(x, control_y, x, target_y,
                                                   fill=color, width=2)

                    if gate == 'CNOT':
                        # Enhanced CNOT target
                        self.circuit_canvas.create_oval(x - 17, target_y - 17,
                                                       x + 17, target_y + 17,
                                                       fill='#000000', outline='')
                        self.circuit_canvas.create_oval(x - 15, target_y - 15,
                                                       x + 15, target_y + 15,
                                                       fill='', outline='#ffffff', width=3)

                        # X symbol
                        self.circuit_canvas.create_line(x - 8, target_y - 8,
                                                       x + 8, target_y + 8,
                                                       fill='#ffffff', width=3)
                        self.circuit_canvas.create_line(x - 8, target_y + 8,
                                                       x + 8, target_y - 8,
                                                       fill='#ffffff', width=3)

                    elif gate == 'CZ':
                        # Enhanced CZ target
                        self.circuit_canvas.create_oval(x - 10, target_y - 10,
                                                       x + 10, target_y + 10,
                                                       fill='#000000', outline='')
                        self.circuit_canvas.create_oval(x - 8, target_y - 8,
                                                       x + 8, target_y + 8,
                                                       fill='#ffffff', outline='#cccccc', width=2)

    def run_circuit(self):
        """Execute the quantum circuit and display results"""
        try:
            # Clear previous results first
            self.results_text.configure(state=tk.NORMAL)
            self.results_text.delete(1.0, tk.END)

            # Play sound first for immediate feedback
            self.play_sound('circuit_run', self.play_success_sound_fallback)

            # Check if there are any gates to run
            if not self.placed_gates:
                self.results_text.insert(tk.END, "No gates placed. Add some gates to your circuit first.\n")
                self.results_text.configure(state=tk.DISABLED)
                return

            # Display current circuit info
            self.results_text.insert(tk.END, f"🚀 Running Quantum Circuit...\n")
            self.results_text.insert(tk.END, f"Qubits: {self.num_qubits}\n")
            self.results_text.insert(tk.END, f"Initial State: {self.initial_state}\n")
            self.results_text.insert(tk.END, f"Gates: {[gate for gate, _ in self.placed_gates]}\n")
            self.results_text.insert(tk.END, "-" * 50 + "\n\n")
            self.results_text.update()

            # Create quantum circuit
            qc = QuantumCircuit(self.num_qubits)

            # Set initial state
            self.set_initial_state(qc)

            # Apply gates
            for gate, qubits in self.placed_gates:
                try:
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
                    else:
                        self.results_text.insert(tk.END, f"Warning: Unknown gate {gate} with qubits {qubits}\n")
                except Exception as gate_error:
                    self.results_text.insert(tk.END, f"Error applying gate {gate}: {str(gate_error)}\n")

            # Get final state
            final_state = Statevector(qc)

            # Display results
            self.display_results(final_state)

            # Play success sound after results are displayed
            self.play_sound('success', self.play_success_sound_fallback)

        except ImportError as ie:
            self.results_text.insert(tk.END, f"Import Error: {str(ie)}\n")
            self.results_text.insert(tk.END, "Make sure Qiskit is installed: pip install qiskit\n")
            self.play_sound('error', self.play_error_sound_fallback)
        except Exception as e:
            self.results_text.insert(tk.END, f"Error executing circuit: {str(e)}\n")
            self.results_text.insert(tk.END, f"Error type: {type(e).__name__}\n")
            import traceback
            self.results_text.insert(tk.END, f"Traceback:\n{traceback.format_exc()}\n")
            self.play_sound('error', self.play_error_sound_fallback)
        finally:
            self.results_text.configure(state=tk.DISABLED)

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
        else:
            # Handle arbitrary binary states like |0000⟩, |0001⟩, etc.
            # Extract the binary string from the ket notation
            if state.startswith("|") and state.endswith("⟩"):
                binary_str = state[1:-1]  # Remove |⟩ brackets

                # Apply X gates for each '1' in the binary string
                for i, bit in enumerate(reversed(binary_str)):
                    if bit == '1' and i < self.num_qubits:
                        qc.x(i)

    def display_results(self, state_vector):
        """Display the quantum state results"""
        try:
            # Circuit summary
            self.results_text.insert(tk.END, f"✅ Circuit Executed Successfully!\n\n")

            # State vector
            self.results_text.insert(tk.END, "📊 Final State Vector:\n")
            state_data = state_vector.data

            for i, amplitude in enumerate(state_data):
                if abs(amplitude) > 0.001:  # Only show significant amplitudes
                    basis_state = format(i, f'0{self.num_qubits}b')
                    prob = abs(amplitude) ** 2
                    # Format complex numbers nicely
                    if isinstance(amplitude, complex):
                        real_part = amplitude.real
                        imag_part = amplitude.imag
                        if abs(imag_part) < 0.001:
                            amp_str = f"{real_part:.4f}"
                        else:
                            amp_str = f"{real_part:.4f} + {imag_part:.4f}i"
                    else:
                        amp_str = f"{amplitude:.4f}"

                    self.results_text.insert(tk.END,
                        f"|{basis_state}⟩: {amp_str} (prob: {prob:.1%})\n")

            self.results_text.insert(tk.END, "\n")

            # Measurement probabilities summary
            self.results_text.insert(tk.END, "🎯 Measurement Probabilities:\n")
            total_prob = 0
            for i, amplitude in enumerate(state_data):
                prob = abs(amplitude) ** 2
                if prob > 0.001:
                    basis_state = format(i, f'0{self.num_qubits}b')
                    self.results_text.insert(tk.END, f"|{basis_state}⟩: {prob:.1%}\n")
                    total_prob += prob

            self.results_text.insert(tk.END, f"\nTotal probability: {total_prob:.1%}\n")

        except Exception as e:
            self.results_text.insert(tk.END, f"Error displaying results: {str(e)}\n")

def main():
    """For testing the sandbox independently"""
    root = tk.Tk()
    app = SandboxMode(root)
    root.mainloop()

if __name__ == "__main__":
    main()