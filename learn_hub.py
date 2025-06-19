#!/usr/bin/env python3
"""
Learn Hub for Infinity Qubit
Educational resources and quantum computing concepts hub.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
import webbrowser
import math
import random

class LearnHub:
    def __init__(self, root):
        self.root = root
        self.root.title("Infinity Qubit - Learn Hub")

        # Get screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Window dimensions
        window_width = 1200
        window_height = 800

        # Center the window
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.configure(bg='#0a0a0a')
        self.root.resizable(True, True)

        # Initialize particles for animation
        self.particles = []
        self.animation_running = False

        # Create the main interface
        self.create_learn_hub_ui()

        # Start background animations
        self.start_animations()

        # Make window focused
        self.root.lift()
        self.root.focus_force()

    def create_learn_hub_ui(self):
        """Create the enhanced learn hub interface"""
        # Main container with gradient-like effect
        main_frame = tk.Frame(self.root, bg='#0a0a0a')
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Add subtle top border
        top_border = tk.Frame(main_frame, bg='#00ff88', height=3)
        top_border.pack(fill=tk.X)

        # Content frame
        content_frame = tk.Frame(main_frame, bg='#1a1a1a')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=25, pady=25)

        # Create animated header
        self.create_animated_header(content_frame)

        # Create a container to center the notebook
        notebook_container = tk.Frame(content_frame, bg='#1a1a1a')
        notebook_container.pack(fill=tk.BOTH, expand=True, pady=(20, 0))

        # Create notebook for tabs - centered
        self.notebook = ttk.Notebook(notebook_container)
        self.notebook.pack(expand=True, fill=tk.BOTH)

        # Apply enhanced styling
        self.style_notebook()

        # Create tabs with enhanced design
        self.create_concepts_tab()
        self.create_gates_tab()
        self.create_algorithms_tab()
        self.create_resources_tab()

        # Enhanced footer
        self.create_enhanced_footer(content_frame)

    def create_animated_header(self, parent):
        """Create an animated quantum-themed header"""
        header_frame = tk.Frame(parent, bg='#1a1a1a')
        header_frame.pack(fill=tk.X, pady=(0, 20))

        # Quantum circuit animation canvas
        self.circuit_canvas = tk.Canvas(header_frame, height=120, bg='#1a1a1a',
                                       highlightthickness=0)
        self.circuit_canvas.pack(fill=tk.X, pady=(0, 15))

        # Draw quantum circuit after canvas is created
        self.root.after(100, self.draw_quantum_circuit)

        # Title with shadow effect
        title_frame = tk.Frame(header_frame, bg='#1a1a1a')
        title_frame.pack()

        # Shadow title
        shadow_title = tk.Label(title_frame, text="🚀 Quantum Computing Learn Hub",
                               font=('Arial', 32, 'bold'),
                               fg='#003322', bg='#1a1a1a')
        shadow_title.place(x=3, y=3)

        # Main title with gradient-like effect
        main_title = tk.Label(title_frame, text="🚀 Quantum Computing Learn Hub",
                             font=('Arial', 32, 'bold'),
                             fg='#00ff88', bg='#1a1a1a')
        main_title.pack(pady=(0, 8))

        # Enhanced subtitle with pulsing effect
        self.subtitle_label = tk.Label(header_frame,
                                      text="✨ Explore quantum computing concepts and resources ✨",
                                      font=('Arial', 14, 'italic'),
                                      fg='#4ecdc4', bg='#1a1a1a')
        self.subtitle_label.pack()

        # Learning progress indicator
        self.create_learning_progress(header_frame)

    def draw_quantum_circuit(self):
        """Draw an animated quantum circuit"""
        if not hasattr(self, 'circuit_canvas'):
            return

        self.circuit_canvas.delete("all")

        # Get actual canvas width
        self.circuit_canvas.update_idletasks()
        width = self.circuit_canvas.winfo_width()
        if width <= 1:
            width = 1150  # fallback width

        # Draw quantum wires with glow effect
        wire_colors = ['#ff6b6b', '#4ecdc4', '#f39c12']
        for i in range(3):
            y = 30 + i * 30
            # Draw wire lines with decreasing thickness for glow effect
            for thickness in [6, 4, 2]:
                color = wire_colors[i]
                self.circuit_canvas.create_line(50, y, width-50, y,
                                              fill=color, width=thickness,
                                              tags="circuit")

        # Draw quantum gates with enhanced styling
        gate_info = [
            {'symbol': 'H', 'color': '#ff6b6b', 'x': 150},
            {'symbol': 'X', 'color': '#4ecdc4', 'x': 250},
            {'symbol': 'Z', 'color': '#f39c12', 'x': 350},
            {'symbol': 'CNOT', 'color': '#9b59b6', 'x': 450, 'double': True}
        ]

        for gate in gate_info:
            self.draw_enhanced_gate(gate)

    def draw_enhanced_gate(self, gate_info):
        """Draw enhanced quantum gates with 3D effect"""
        x = gate_info['x']
        color = gate_info['color']
        symbol = gate_info['symbol']

        if gate_info.get('double'):
            # CNOT gate
            y1, y2 = 30, 90
            # Control dot
            self.circuit_canvas.create_oval(x-8, y1-8, x+8, y1+8,
                                          fill=color, outline='white', width=2)
            # Target circle
            self.circuit_canvas.create_oval(x-15, y2-15, x+15, y2+15,
                                          fill='', outline=color, width=3)
            # Plus sign
            self.circuit_canvas.create_line(x-10, y2, x+10, y2, fill=color, width=3)
            self.circuit_canvas.create_line(x, y2-10, x, y2+10, fill=color, width=3)
            # Connection line
            self.circuit_canvas.create_line(x, y1, x, y2, fill=color, width=2)
        else:
            # Single qubit gate
            y = 30 + (0 if symbol == 'H' else 1 if symbol == 'X' else 2) * 30

            # 3D shadow effect
            self.circuit_canvas.create_rectangle(x-17, y-12, x+17, y+12,
                                               fill='#000000', outline='')
            # Main gate
            self.circuit_canvas.create_rectangle(x-15, y-10, x+15, y+10,
                                               fill=color, outline='white', width=2)
            # Gate symbol
            self.circuit_canvas.create_text(x, y, text=symbol,
                                          fill='white', font=('Arial', 12, 'bold'))

    def create_learning_progress(self, parent):
        """Create a visual learning progress indicator"""
        progress_frame = tk.Frame(parent, bg='#1a1a1a')
        progress_frame.pack(fill=tk.X, pady=(15, 0))

        tk.Label(progress_frame, text="📈 Learning Journey",
                font=('Arial', 14, 'bold'),
                fg='#00ff88', bg='#1a1a1a').pack()

        # Progress steps with enhanced visuals
        steps_container = tk.Frame(progress_frame, bg='#1a1a1a')
        steps_container.pack(pady=10)

        steps = [
            ("Basics", True, "#00ff88", "🎯"),
            ("Gates", True, "#4ecdc4", "⚡"),
            ("Algorithms", False, "#666666", "🧠"),
            ("Advanced", False, "#333333", "🚀")
        ]

        for i, (step, completed, color, icon) in enumerate(steps):
            step_frame = tk.Frame(steps_container, bg='#1a1a1a')
            step_frame.pack(side=tk.LEFT, padx=15)

            # Enhanced circle with glow
            canvas = tk.Canvas(step_frame, width=40, height=40,
                              bg='#1a1a1a', highlightthickness=0)
            canvas.pack()

            # Glow effect for completed steps
            if completed:
                canvas.create_oval(2, 2, 38, 38, fill=color, outline=color, width=3)
                canvas.create_oval(8, 8, 32, 32, fill='#1a1a1a', outline='white', width=2)
                canvas.create_text(20, 20, text="✓", fill='white', font=('Arial', 14, 'bold'))
            else:
                canvas.create_oval(8, 8, 32, 32, fill='', outline=color, width=2)

            # Step label with icon
            tk.Label(step_frame, text=f"{icon} {step}", fg=color, bg='#1a1a1a',
                    font=('Arial', 10, 'bold')).pack(pady=(5, 0))

            # Connection line (except for last step)
            if i < len(steps) - 1:
                line_canvas = tk.Canvas(steps_container, width=30, height=5,
                                       bg='#1a1a1a', highlightthickness=0)
                line_canvas.pack(side=tk.LEFT)
                line_canvas.create_line(0, 2, 30, 2, fill='#333333', width=2)

    def style_notebook(self):
        """Apply enhanced styling to the notebook"""
        style = ttk.Style()
        style.theme_use('clam')

        # Enhanced notebook styling - Fixed the focuscolor issue
        style.configure('TNotebook',
                    background='#1a1a1a',
                    borderwidth=0,
                    tabmargins=[2, 5, 2, 0])

        style.configure('TNotebook.Tab',
                    background='#2a2a2a',
                    foreground='#ffffff',
                    padding=[25, 15],
                    borderwidth=0,
                    font=('Arial', 11, 'bold'))

        style.map('TNotebook.Tab',
                background=[('selected', '#00ff88'),
                            ('active', '#4ecdc4')],
                foreground=[('selected', '#000000'),
                            ('active', '#ffffff')])

        style.configure('TFrame', background='#1a1a1a')

        # Center the tabs by configuring tab positioning
        style.configure('TNotebook', tabposition='n')

    def create_concepts_tab(self):
        """Create the enhanced basic concepts tab"""
        concepts_frame = ttk.Frame(self.notebook)
        self.notebook.add(concepts_frame, text="📚 Basic Concepts")

        # Main container with padding
        main_container = tk.Frame(concepts_frame, bg='#1a1a1a')
        main_container.pack(fill=tk.BOTH, expand=True, padx=25, pady=20)

        # Enhanced scrollable text area
        text_frame = tk.Frame(main_container, bg='#2a2a2a', relief=tk.RAISED, bd=2)
        text_frame.pack(fill=tk.BOTH, expand=True)

        concepts_text = scrolledtext.ScrolledText(text_frame,
                                                 wrap=tk.WORD,
                                                 width=80, height=25,
                                                 bg='#2a2a2a', fg='#ffffff',
                                                 font=('Consolas', 11),
                                                 insertbackground='#00ff88',
                                                 selectbackground='#4ecdc4',
                                                 selectforeground='#000000',
                                                 padx=20, pady=15)
        concepts_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Enhanced content with better formatting
        concepts_content = """
🔬 QUANTUM COMPUTING FUNDAMENTALS

🌟 What is Quantum Computing?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Quantum computing harnesses the principles of quantum mechanics to process information in
fundamentally different ways than classical computers. Instead of using bits that are either
0 or 1, quantum computers use quantum bits (qubits) that can exist in superposition.

🎯 KEY CONCEPTS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔹 1. QUBIT (Quantum Bit)
   ┌─ The basic unit of quantum information
   ├─ Can be in state |0⟩, |1⟩, or a superposition of both
   └─ Represented as α|0⟩ + β|1⟩ where |α|² + |β|² = 1

🔹 2. SUPERPOSITION
   ┌─ A qubit can exist in multiple states simultaneously
   ├─ Enables quantum computers to process many possibilities at once
   └─ Collapses to a definite state when measured

🔹 3. ENTANGLEMENT
   ┌─ Quantum particles become correlated in impossible ways
   ├─ Measurement of one particle instantly affects its entangled partner
   └─ Key resource for quantum algorithms and communication

🔹 4. INTERFERENCE
   ┌─ Quantum states can interfere constructively or destructively
   ├─ Used in quantum algorithms to amplify correct answers
   └─ Cancels out wrong answers in many quantum computations

🔹 5. MEASUREMENT
   ┌─ The act of observing a quantum system
   ├─ Causes the quantum state to collapse to a classical state
   └─ Probabilistic outcome based on quantum amplitudes

🚀 WHY QUANTUM COMPUTING MATTERS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✨ Exponential speedup for certain problems
✨ Cryptography and security applications
✨ Drug discovery and molecular simulation
✨ Optimization problems
✨ Machine learning and AI
✨ Financial modeling

🔧 CURRENT CHALLENGES:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ Quantum decoherence (qubits losing their quantum properties)
⚠️ Error rates in quantum operations
⚠️ Limited number of qubits in current systems
⚠️ Need for extremely low temperatures
⚠️ Quantum error correction

📈 THE FUTURE:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Quantum computing represents a paradigm shift that could revolutionize how we solve
complex problems in science, technology, and beyond. The future is quantum! 🌟
        """

        concepts_text.insert(tk.END, concepts_content)
        concepts_text.config(state=tk.DISABLED)

    def create_gates_tab(self):
        """Create the enhanced quantum gates tab with all gates in one horizontal line"""
        gates_frame = ttk.Frame(self.notebook)
        self.notebook.add(gates_frame, text="⚡ Quantum Gates")

        # Main container
        main_container = tk.Frame(gates_frame, bg='#1a1a1a')
        main_container.pack(fill=tk.BOTH, expand=True, padx=25, pady=20)

        # Create a canvas for horizontal scrolling with enhanced styling
        canvas_frame = tk.Frame(main_container, bg='#2a2a2a', relief=tk.RAISED, bd=2)
        canvas_frame.pack(fill=tk.BOTH, expand=True)

        # Use horizontal scrollbar instead of vertical
        canvas = tk.Canvas(canvas_frame, bg='#1a1a1a', highlightthickness=0)
        scrollbar = ttk.Scrollbar(canvas_frame, orient="horizontal", command=canvas.xview)
        scrollable_frame = tk.Frame(canvas, bg='#1a1a1a')

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(xscrollcommand=scrollbar.set)  # Changed to xscrollcommand

        canvas.pack(side="top", fill="both", expand=True, padx=5, pady=5)
        scrollbar.pack(side="bottom", fill="x")  # Changed to bottom and fill x

        # Enhanced gate definitions with more details
        gates = [
            ("X Gate (NOT)", "Flips |0⟩ ↔ |1⟩", "Pauli-X rotation", "#ff6b6b", "❌", 2),
            ("Y Gate", "Rotates around Y-axis", "Pauli-Y rotation", "#4ecdc4", "🔄", 3),
            ("Z Gate", "Phase flip: |1⟩ → -|1⟩", "Pauli-Z rotation", "#96ceb4", "⚡", 2),
            ("H Gate (Hadamard)", "Creates superposition", "|0⟩ → (|0⟩+|1⟩)/√2", "#f39c12", "🌟", 4),
            ("S Gate", "Phase gate: |1⟩ → i|1⟩", "90° Z rotation", "#9b59b6", "📐", 3),
            ("T Gate", "π/8 gate", "45° Z rotation", "#e74c3c", "🔺", 3),
            ("CNOT Gate", "Controlled NOT", "Entangles two qubits", "#00ff88", "🔗", 5),
            ("CZ Gate", "Controlled Z", "Conditional phase flip", "#ff9ff3", "⭐", 4),
        ]

        # Create one single row with all gates
        row_frame = tk.Frame(scrollable_frame, bg='#1a1a1a')
        row_frame.pack(fill=tk.BOTH, expand=True, pady=20)

        # Add all gates to the single row
        for name, description, formula, color, icon, difficulty in gates:
            gate_container = tk.Frame(row_frame, bg='#1a1a1a')
            gate_container.pack(side=tk.LEFT, fill=tk.Y, padx=15)  # Changed to side=tk.LEFT and fill=tk.Y

            self.create_enhanced_gate_card_horizontal(gate_container, name, description,
                                                    formula, color, icon, difficulty)

        # Enable mouse wheel scrolling on the canvas
        def on_mousewheel(event):
            canvas.xview_scroll(int(-1*(event.delta/120)), "units")

        canvas.bind("<MouseWheel>", on_mousewheel)
        # For Linux
        canvas.bind("<Button-4>", lambda e: canvas.xview_scroll(-1, "units"))
        canvas.bind("<Button-5>", lambda e: canvas.xview_scroll(1, "units"))

    def create_enhanced_gate_card_horizontal(self, parent, name, description, formula, color, icon, difficulty):
        """Create enhanced cards for quantum gates with horizontal layout and hover effects"""
        card_frame = tk.Frame(parent, bg='#2a2a2a', relief=tk.FLAT, bd=0, width=200, height=250)  # Fixed size
        card_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=8)
        card_frame.pack_propagate(False)  # Maintain fixed size

        # Glow effect frame (initially hidden)
        glow_frame = tk.Frame(card_frame, bg=color, height=3)
        glow_frame.pack(fill=tk.X)
        glow_frame.pack_forget()

        # Main content frame
        content_frame = tk.Frame(card_frame, bg='#2a2a2a')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=12)

        # Header with icon and title
        header_frame = tk.Frame(content_frame, bg='#2a2a2a')
        header_frame.pack(fill=tk.X, pady=(0, 8))

        # Gate icon - centered
        icon_label = tk.Label(header_frame, text=icon,
                            font=('Arial', 24), bg='#2a2a2a')  # Increased icon size
        icon_label.pack()

        # Title - centered
        name_label = tk.Label(header_frame, text=name,
                            font=('Arial', 12, 'bold'),  # Slightly smaller font
                            fg=color, bg='#2a2a2a')
        name_label.pack(pady=(5, 0))

        # Difficulty stars - centered
        stars = "⭐" * difficulty + "☆" * (5 - difficulty)
        difficulty_label = tk.Label(header_frame, text=f"{stars}",
                                font=('Arial', 8),  # Smaller font
                                fg='#f39c12', bg='#2a2a2a')
        difficulty_label.pack()

        # Description - centered
        desc_label = tk.Label(content_frame, text=description,
                            font=('Arial', 9),  # Smaller font
                            fg='#ffffff', bg='#2a2a2a',
                            wraplength=170, justify=tk.CENTER)
        desc_label.pack(pady=(0, 5))

        # Formula - centered
        formula_label = tk.Label(content_frame, text=formula,
                                font=('Arial', 8, 'italic'),  # Smaller font
                                fg='#cccccc', bg='#2a2a2a',
                                wraplength=170, justify=tk.CENTER)
        formula_label.pack()

        # Hover effects
        def on_enter(event):
            card_frame.configure(bg='#3a3a3a')
            content_frame.configure(bg='#3a3a3a')
            header_frame.configure(bg='#3a3a3a')
            for widget in [icon_label, name_label, difficulty_label, desc_label, formula_label]:
                widget.configure(bg='#3a3a3a')
            glow_frame.pack(fill=tk.X, before=content_frame)

        def on_leave(event):
            card_frame.configure(bg='#2a2a2a')
            content_frame.configure(bg='#2a2a2a')
            header_frame.configure(bg='#2a2a2a')
            for widget in [icon_label, name_label, difficulty_label, desc_label, formula_label]:
                widget.configure(bg='#2a2a2a')
            glow_frame.pack_forget()

        card_frame.bind("<Enter>", on_enter)
        card_frame.bind("<Leave>", on_leave)

        # Bind hover to all child widgets
        for widget in [content_frame, header_frame, icon_label, name_label, difficulty_label, desc_label, formula_label]:
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)

    def create_algorithms_tab(self):
        """Create the enhanced algorithms tab"""
        algorithms_frame = ttk.Frame(self.notebook)
        self.notebook.add(algorithms_frame, text="🧠 Algorithms")

        # Main container
        main_container = tk.Frame(algorithms_frame, bg='#1a1a1a')
        main_container.pack(fill=tk.BOTH, expand=True, padx=25, pady=20)

        # Enhanced scrollable text area
        text_frame = tk.Frame(main_container, bg='#2a2a2a', relief=tk.RAISED, bd=2)
        text_frame.pack(fill=tk.BOTH, expand=True)

        algorithms_text = scrolledtext.ScrolledText(text_frame,
                                                   wrap=tk.WORD,
                                                   width=80, height=25,
                                                   bg='#2a2a2a', fg='#ffffff',
                                                   font=('Consolas', 11),
                                                   insertbackground='#00ff88',
                                                   selectbackground='#4ecdc4',
                                                   selectforeground='#000000',
                                                   padx=20, pady=15)
        algorithms_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Enhanced algorithm content
        algorithms_content = """
🧠 FAMOUS QUANTUM ALGORITHMS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔍 1. SHOR'S ALGORITHM (1994) ⭐⭐⭐⭐⭐
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   🎯 Purpose: Integer factorization
   💥 Impact: Breaks RSA encryption
   🚀 Speedup: Exponential over classical methods

   🔑 Key Ideas:
   ┌─ Uses quantum Fourier transform
   ├─ Finds period of modular exponentiation
   └─ Factors large numbers efficiently

   📱 Applications:
   ┌─ Cryptography and security
   ├─ Breaking current encryption schemes
   └─ Motivating post-quantum cryptography

🔍 2. GROVER'S ALGORITHM (1996) ⭐⭐⭐⭐☆
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   🎯 Purpose: Database search
   💥 Impact: Quadratic speedup for search problems
   🚀 Speedup: √N instead of N comparisons

   🔑 Key Ideas:
   ┌─ Amplitude amplification
   ├─ Iteratively increases probability of correct answer
   └─ Uses quantum interference

   📱 Applications:
   ┌─ Unstructured search
   ├─ Optimization problems
   └─ Machine learning

🔍 3. DEUTSCH-JOZSA ALGORITHM ⭐⭐⭐☆☆
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   🎯 Purpose: Determine if function is constant or balanced
   💥 Impact: First quantum algorithm with exponential speedup
   🚀 Speedup: 1 query vs N/2 queries classically

   🔑 Key Ideas:
   ┌─ Uses quantum parallelism
   ├─ Evaluates function on all inputs simultaneously
   └─ Quantum interference reveals global property

🔍 4. VARIATIONAL QUANTUM EIGENSOLVER (VQE) ⭐⭐⭐⭐☆
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   🎯 Purpose: Find ground state of molecular systems
   💥 Impact: Near-term quantum chemistry applications
   🔄 Approach: Hybrid quantum-classical optimization

   🔑 Key Ideas:
   ┌─ Parametrized quantum circuits
   ├─ Classical optimization loop
   └─ Minimizes energy expectation value

🎯 ALGORITHM CATEGORIES:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📈 Algebraic Algorithms:
   • Shor's Algorithm (factoring)
   • Hidden Subgroup Problem
   • Discrete logarithm

🔍 Search Algorithms:
   • Grover's Algorithm
   • Amplitude amplification
   • Quantum walks

🧮 Simulation Algorithms:
   • Quantum chemistry simulation
   • Many-body physics
   • Quantum field theory

🎲 Optimization Algorithms:
   • QAOA
   • VQE
   • Quantum annealing

🔮 FUTURE DIRECTIONS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✨ Fault-tolerant quantum algorithms
✨ Quantum machine learning
✨ Quantum error correction
✨ Distributed quantum computing

The quantum future awaits! 🌟🚀
        """

        algorithms_text.insert(tk.END, algorithms_content)
        algorithms_text.config(state=tk.DISABLED)

    def create_resources_tab(self):
        """Create the enhanced resources tab with horizontal layout"""
        resources_frame = ttk.Frame(self.notebook)
        self.notebook.add(resources_frame, text="🔗 Resources")

        # Main container
        main_container = tk.Frame(resources_frame, bg='#1a1a1a')
        main_container.pack(fill=tk.BOTH, expand=True, padx=25, pady=20)

        # Create scrollable frame with horizontal scrolling
        canvas = tk.Canvas(main_container, bg='#1a1a1a', highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_container, orient="horizontal", command=canvas.xview)
        scrollable_frame = tk.Frame(canvas, bg='#1a1a1a')

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(xscrollcommand=scrollbar.set)

        canvas.pack(side="top", fill="both", expand=True)
        scrollbar.pack(side="bottom", fill="x")

        # Learning Resources section
        self.create_section_header_horizontal(scrollable_frame, "📚 Learning Resources", "#00ff88")

        # Resources in horizontal layout
        resources_row = tk.Frame(scrollable_frame, bg='#1a1a1a')
        resources_row.pack(fill=tk.X, pady=10)

        resources = [
            ("IBM Quantum Experience", "https://quantum-computing.ibm.com/",
            "Hands-on quantum programming", "🔬", 4),
            ("Microsoft Quantum Development Kit", "https://azure.microsoft.com/en-us/products/quantum/",
            "Q# programming language", "💻", 3),
            ("Google Cirq", "https://quantumai.google/cirq",
            "Python framework for quantum circuits", "🐍", 3),
            ("Qiskit Textbook", "https://qiskit.org/textbook/",
            "Comprehensive quantum computing textbook", "📖", 5),
            ("Nielsen & Chuang", "https://www.cambridge.org/core/books/quantum-computation-and-quantum-information/01E10196D0A682A6AEFFEA52D53BE9AE",
            "The quantum computing bible", "📚", 5),
        ]

        for title, url, description, icon, rating in resources:
            resource_container = tk.Frame(resources_row, bg='#1a1a1a')
            resource_container.pack(side=tk.LEFT, fill=tk.Y, padx=10)
            self.create_enhanced_resource_card_horizontal(resource_container, title, url, description, icon, rating)

        # Separator with horizontal layout
        self.create_separator_horizontal(scrollable_frame)

        # Tools section
        self.create_section_header_horizontal(scrollable_frame, "🛠️ Quantum Computing Tools", "#f39c12")

        # Tools in horizontal layout
        tools_row = tk.Frame(scrollable_frame, bg='#1a1a1a')
        tools_row.pack(fill=tk.X, pady=10)

        tools = [
            ("Qiskit", "https://qiskit.org/",
            "Open-source quantum computing framework", "⚛️", 5),
            ("Cirq", "https://quantumai.google/cirq",
            "Google's quantum computing framework", "🔧", 4),
            ("PennyLane", "https://pennylane.ai/",
            "Quantum machine learning library", "🤖", 4),
            ("Quantum Inspire", "https://www.quantum-inspire.com/",
            "QuTech's quantum computing platform", "💡", 3),
        ]

        for title, url, description, icon, rating in tools:
            tool_container = tk.Frame(tools_row, bg='#1a1a1a')
            tool_container.pack(side=tk.LEFT, fill=tk.Y, padx=10)
            self.create_enhanced_resource_card_horizontal(tool_container, title, url, description, icon, rating)

        # Enable mouse wheel scrolling on the canvas
        def on_mousewheel(event):
            canvas.xview_scroll(int(-1*(event.delta/120)), "units")

        canvas.bind("<MouseWheel>", on_mousewheel)
        # For Linux
        canvas.bind("<Button-4>", lambda e: canvas.xview_scroll(-1, "units"))
        canvas.bind("<Button-5>", lambda e: canvas.xview_scroll(1, "units"))

    def create_enhanced_resource_card_horizontal(self, parent, title, url, description, icon, rating):
        """Create enhanced resource cards with horizontal layout and hover effects"""
        card_frame = tk.Frame(parent, bg='#2a2a2a', relief=tk.FLAT, bd=0, width=250, height=300)
        card_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=8)
        card_frame.pack_propagate(False)  # Maintain fixed size

        # Glow frame
        glow_frame = tk.Frame(card_frame, bg='#4ecdc4', height=2)
        glow_frame.pack(fill=tk.X)
        glow_frame.pack_forget()

        # Content frame
        content_frame = tk.Frame(card_frame, bg='#2a2a2a')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        # Header with icon
        header_frame = tk.Frame(content_frame, bg='#2a2a2a')
        header_frame.pack(fill=tk.X, pady=(0, 10))

        # Icon - centered and larger
        icon_label = tk.Label(header_frame, text=icon,
                            font=('Arial', 28), bg='#2a2a2a')
        icon_label.pack()

        # Title - centered with wrapping
        title_label = tk.Label(header_frame, text=title,
                            font=('Arial', 12, 'bold'),
                            fg='#4ecdc4', bg='#2a2a2a',
                            cursor='hand2', wraplength=220, justify=tk.CENTER)
        title_label.pack(pady=(5, 0))
        title_label.bind("<Button-1>", lambda e: self.open_url(url))

        # Rating stars - centered
        stars = "⭐" * rating + "☆" * (5 - rating)
        rating_label = tk.Label(header_frame, text=stars,
                            font=('Arial', 10),
                            fg='#f39c12', bg='#2a2a2a')
        rating_label.pack(pady=(5, 0))

        # Description - centered with wrapping
        desc_label = tk.Label(content_frame, text=description,
                            font=('Arial', 10),
                            fg='#cccccc', bg='#2a2a2a',
                            wraplength=220, justify=tk.CENTER)
        desc_label.pack(pady=(10, 15))

        # Try it button - centered
        try_btn = tk.Button(content_frame, text="Try It →",
                        bg='#00ff88', fg='#000000',
                        font=('Arial', 10, 'bold'),
                        padx=20, pady=8,
                        cursor='hand2',
                        command=lambda: self.open_url(url))
        try_btn.pack()

        # Hover effects
        def on_enter(event):
            card_frame.configure(bg='#3a3a3a')
            content_frame.configure(bg='#3a3a3a')
            header_frame.configure(bg='#3a3a3a')
            for widget in [icon_label, title_label, rating_label, desc_label]:
                widget.configure(bg='#3a3a3a')
            glow_frame.pack(fill=tk.X, before=content_frame)

        def on_leave(event):
            card_frame.configure(bg='#2a2a2a')
            content_frame.configure(bg='#2a2a2a')
            header_frame.configure(bg='#2a2a2a')
            for widget in [icon_label, title_label, rating_label, desc_label]:
                widget.configure(bg='#2a2a2a')
            glow_frame.pack_forget()

        card_frame.bind("<Enter>", on_enter)
        card_frame.bind("<Leave>", on_leave)

        # Bind hover to all child widgets
        for widget in [content_frame, header_frame, icon_label, title_label, rating_label, desc_label]:
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)

    def create_separator_horizontal(self, parent):
        """Create a horizontal separator for horizontal layout"""
        separator_frame = tk.Frame(parent, bg='#1a1a1a')
        separator_frame.pack(fill=tk.X, pady=30)

        # Gradient-like separator
        colors = ['#4ecdc4', '#00ff88', '#4ecdc4']
        for i, color in enumerate(colors):
            line = tk.Frame(separator_frame, bg=color, height=2)
            line.pack(fill=tk.X, pady=1)

    def create_section_header_horizontal(self, parent, title, color):
        """Create an enhanced section header for horizontal layout"""
        header_frame = tk.Frame(parent, bg='#1a1a1a')
        header_frame.pack(fill=tk.X, pady=(20, 15))

        # Title with underline effect
        title_label = tk.Label(header_frame, text=title,
                            font=('Arial', 18, 'bold'),
                            fg=color, bg='#1a1a1a')
        title_label.pack()

        # Underline
        underline = tk.Frame(header_frame, bg=color, height=2)
        underline.pack(fill=tk.X, pady=(5, 0))

    def create_section_header(self, parent, title, color):
        """Create an enhanced section header"""
        header_frame = tk.Frame(parent, bg='#1a1a1a')
        header_frame.pack(fill=tk.X, pady=(20, 15))

        # Title with underline effect
        title_label = tk.Label(header_frame, text=title,
                              font=('Arial', 18, 'bold'),
                              fg=color, bg='#1a1a1a')
        title_label.pack(anchor=tk.W)

        # Underline
        underline = tk.Frame(header_frame, bg=color, height=2)
        underline.pack(fill=tk.X, pady=(5, 0))

    def create_enhanced_resource_card(self, parent, title, url, description, icon, rating):
        """Create enhanced resource cards with ratings and hover effects"""
        card_frame = tk.Frame(parent, bg='#2a2a2a', relief=tk.FLAT, bd=0)
        card_frame.pack(fill=tk.X, pady=8)

        # Glow frame
        glow_frame = tk.Frame(card_frame, bg='#4ecdc4', height=2)
        glow_frame.pack(fill=tk.X)
        glow_frame.pack_forget()

        # Content frame
        content_frame = tk.Frame(card_frame, bg='#2a2a2a')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)

        # Header
        header_frame = tk.Frame(content_frame, bg='#2a2a2a')
        header_frame.pack(fill=tk.X, pady=(0, 8))

        # Icon
        icon_label = tk.Label(header_frame, text=icon,
                             font=('Arial', 20), bg='#2a2a2a')
        icon_label.pack(side=tk.LEFT, padx=(0, 15))

        # Title and rating
        title_frame = tk.Frame(header_frame, bg='#2a2a2a')
        title_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)

        title_label = tk.Label(title_frame, text=title,
                              font=('Arial', 14, 'bold'),
                              fg='#4ecdc4', bg='#2a2a2a',
                              cursor='hand2')
        title_label.pack(anchor=tk.W)
        title_label.bind("<Button-1>", lambda e: self.open_url(url))

        # Rating stars
        stars = "⭐" * rating + "☆" * (5 - rating)
        rating_label = tk.Label(title_frame, text=f"Rating: {stars}",
                               font=('Arial', 10),
                               fg='#f39c12', bg='#2a2a2a')
        rating_label.pack(anchor=tk.W)

        # Try it button
        try_btn = tk.Button(header_frame, text="Try It →",
                           bg='#00ff88', fg='#000000',
                           font=('Arial', 10, 'bold'),
                           padx=15, pady=5,
                           cursor='hand2',
                           command=lambda: self.open_url(url))
        try_btn.pack(side=tk.RIGHT)

        # Description
        desc_label = tk.Label(content_frame, text=description,
                             font=('Arial', 11),
                             fg='#cccccc', bg='#2a2a2a')
        desc_label.pack(anchor=tk.W)

        # Hover effects
        def on_enter(event):
            card_frame.configure(bg='#3a3a3a')
            content_frame.configure(bg='#3a3a3a')
            header_frame.configure(bg='#3a3a3a')
            title_frame.configure(bg='#3a3a3a')
            for widget in [icon_label, title_label, rating_label, desc_label]:
                widget.configure(bg='#3a3a3a')
            glow_frame.pack(fill=tk.X, before=content_frame)

        def on_leave(event):
            card_frame.configure(bg='#2a2a2a')
            content_frame.configure(bg='#2a2a2a')
            header_frame.configure(bg='#2a2a2a')
            title_frame.configure(bg='#2a2a2a')
            for widget in [icon_label, title_label, rating_label, desc_label]:
                widget.configure(bg='#2a2a2a')
            glow_frame.pack_forget()

        card_frame.bind("<Enter>", on_enter)
        card_frame.bind("<Leave>", on_leave)

    def create_separator(self, parent):
        """Create an animated separator"""
        separator_frame = tk.Frame(parent, bg='#1a1a1a')
        separator_frame.pack(fill=tk.X, pady=25)

        # Gradient-like separator
        colors = ['#4ecdc4', '#00ff88', '#4ecdc4']
        for i, color in enumerate(colors):
            line = tk.Frame(separator_frame, bg=color, height=1)
            line.pack(fill=tk.X, pady=1)

    def create_enhanced_footer(self, parent):
        """Create enhanced footer with gradient buttons"""
        footer_frame = tk.Frame(parent, bg='#1a1a1a')
        footer_frame.pack(fill=tk.X, pady=(25, 0))

        # Back button with enhanced styling
        back_btn = tk.Button(footer_frame, text="⬅️ Back to Menu",
                            command=self.back_to_menu,
                            font=('Arial', 12, 'bold'),
                            bg='#4ecdc4', fg='#000000',
                            padx=25, pady=12,
                            cursor='hand2',
                            relief=tk.FLAT,
                            borderwidth=0)
        back_btn.pack(side=tk.LEFT)

        # Add hover effect to back button
        def on_back_enter(event):
            back_btn.configure(bg='#00ff88')
        def on_back_leave(event):
            back_btn.configure(bg='#4ecdc4')

        back_btn.bind("<Enter>", on_back_enter)
        back_btn.bind("<Leave>", on_back_leave)

        # Close button with enhanced styling
        close_btn = tk.Button(footer_frame, text="❌ Close",
                             command=self.close_window,
                             font=('Arial', 12, 'bold'),
                             bg='#ff6b6b', fg='#ffffff',
                             padx=25, pady=12,
                             cursor='hand2',
                             relief=tk.FLAT,
                             borderwidth=0)
        close_btn.pack(side=tk.RIGHT)

        # Add hover effect to close button
        def on_close_enter(event):
            close_btn.configure(bg='#e74c3c')
        def on_close_leave(event):
            close_btn.configure(bg='#ff6b6b')

        close_btn.bind("<Enter>", on_close_enter)
        close_btn.bind("<Leave>", on_close_leave)

    def start_animations(self):
        """Start background animations"""
        self.animation_running = True
        self.root.after(500, self.animate_circuit)  # Start after UI is ready
        self.root.after(1000, self.animate_subtitle)

    def animate_circuit(self):
        """Animate the quantum circuit"""
        if not self.animation_running:
            return

        # Redraw circuit with subtle animation
        self.draw_quantum_circuit()

        # Schedule next animation frame
        self.root.after(3000, self.animate_circuit)

    def animate_subtitle(self):
        """Animate subtitle with pulsing effect"""
        if not self.animation_running or not hasattr(self, 'subtitle_label'):
            return

        try:
            current_color = self.subtitle_label.cget('fg')
            new_color = '#00ff88' if current_color == '#4ecdc4' else '#4ecdc4'
            self.subtitle_label.configure(fg=new_color)
        except:
            pass  # Ignore errors if widget is destroyed

        self.root.after(2000, self.animate_subtitle)

    def open_url(self, url):
        """Open URL in default browser"""
        try:
            webbrowser.open(url)
        except Exception as e:
            print(f"Error opening URL: {e}")

    def back_to_menu(self):
        """Go back to the main menu"""
        self.animation_running = False
        self.root.destroy()
        try:
            from game_mode_selection import GameModeSelection
            selection_window = GameModeSelection()
            selection_window.run()
        except Exception as e:
            print(f"Error returning to menu: {e}")

    def close_window(self):
        """Close the learn hub window"""
        self.animation_running = False
        self.root.destroy()

def main():
    """For testing the learn hub independently"""
    root = tk.Tk()
    app = LearnHub(root)
    root.mainloop()

if __name__ == "__main__":
    main()