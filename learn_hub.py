#!/usr/bin/env python3
"""
Learn Hub for Infinity Qubit
Educational resources and quantum computing concepts hub.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
import webbrowser

class LearnHub:
    def __init__(self, root):
        self.root = root
        self.root.title("Infinity Qubit - Learn Hub")
        
        # Get screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Window dimensions
        window_width = 1000
        window_height = 700
        
        # Center the window
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.configure(bg='#1a1a1a')
        self.root.resizable(True, True)
        
        # Create the main interface
        self.create_learn_hub_ui()
        
        # Make window focused
        self.root.lift()
        self.root.focus_force()
    
    def create_learn_hub_ui(self):
        """Create the learn hub interface"""
        # Main container
        main_frame = tk.Frame(self.root, bg='#1a1a1a')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        header_frame = tk.Frame(main_frame, bg='#1a1a1a')
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Title
        title_label = tk.Label(header_frame, text="🚀 Quantum Computing Learn Hub",
                              font=('Arial', 28, 'bold'), 
                              fg='#00ff88', bg='#1a1a1a')
        title_label.pack(pady=(0, 10))
        
        # Subtitle
        subtitle_label = tk.Label(header_frame, text="Explore quantum computing concepts and resources",
                                 font=('Arial', 14), 
                                 fg='#ffffff', bg='#1a1a1a')
        subtitle_label.pack()
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=(20, 0))
        
        # Configure notebook style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook', background='#1a1a1a')
        style.configure('TNotebook.Tab', background='#2a2a2a', foreground='#ffffff', padding=[20, 10])
        style.configure('TFrame', background='#1a1a1a')
        
        # Create tabs
        self.create_concepts_tab()
        self.create_gates_tab()
        self.create_algorithms_tab()
        self.create_resources_tab()
        
        # Footer
        footer_frame = tk.Frame(main_frame, bg='#1a1a1a')
        footer_frame.pack(fill=tk.X, pady=(20, 0))
        
        # Back to menu button
        back_btn = tk.Button(footer_frame, text="⬅️ Back to Menu",
                            command=self.back_to_menu,
                            font=('Arial', 12, 'bold'),
                            bg='#4ecdc4', fg='#000000',
                            padx=20, pady=10,
                            cursor='hand2')
        back_btn.pack(side=tk.LEFT)
        
        # Close button
        close_btn = tk.Button(footer_frame, text="❌ Close",
                             command=self.close_window,
                             font=('Arial', 12, 'bold'),
                             bg='#ff6b6b', fg='#ffffff',
                             padx=20, pady=10,
                             cursor='hand2')
        close_btn.pack(side=tk.RIGHT)
    
    def create_concepts_tab(self):
        """Create the basic concepts tab"""
        concepts_frame = ttk.Frame(self.notebook)
        self.notebook.add(concepts_frame, text="📚 Basic Concepts")
        
        # Scrollable text area
        concepts_text = scrolledtext.ScrolledText(concepts_frame, 
                                                 wrap=tk.WORD,
                                                 width=80, height=25,
                                                 bg='#2a2a2a', fg='#ffffff',
                                                 font=('Arial', 11),
                                                 insertbackground='#ffffff')
        concepts_text.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Add content
        concepts_content = """
🔬 QUANTUM COMPUTING FUNDAMENTALS

🌟 What is Quantum Computing?
Quantum computing harnesses the principles of quantum mechanics to process information in fundamentally different ways than classical computers. Instead of using bits that are either 0 or 1, quantum computers use quantum bits (qubits) that can exist in superposition.

🎯 Key Concepts:

1. QUBIT (Quantum Bit)
   • The basic unit of quantum information
   • Can be in state |0⟩, |1⟩, or a superposition of both
   • Represented as α|0⟩ + β|1⟩ where |α|² + |β|² = 1

2. SUPERPOSITION
   • A qubit can exist in multiple states simultaneously
   • Enables quantum computers to process many possibilities at once
   • Collapses to a definite state when measured

3. ENTANGLEMENT
   • Quantum particles become correlated in ways that seem impossible classically
   • Measurement of one particle instantly affects its entangled partner
   • Key resource for quantum algorithms and communication

4. INTERFERENCE
   • Quantum states can interfere constructively or destructively
   • Used in quantum algorithms to amplify correct answers
   • Cancels out wrong answers in many quantum computations

5. MEASUREMENT
   • The act of observing a quantum system
   • Causes the quantum state to collapse to a classical state
   • Probabilistic outcome based on quantum amplitudes

🚀 Why Quantum Computing Matters:
• Exponential speedup for certain problems
• Cryptography and security applications
• Drug discovery and molecular simulation
• Optimization problems
• Machine learning and AI
• Financial modeling

🔧 Current Challenges:
• Quantum decoherence (qubits losing their quantum properties)
• Error rates in quantum operations
• Limited number of qubits in current systems
• Need for extremely low temperatures
• Quantum error correction

📈 The Future:
Quantum computing represents a paradigm shift that could revolutionize how we solve complex problems in science, technology, and beyond.
        """
        
        concepts_text.insert(tk.END, concepts_content)
        concepts_text.config(state=tk.DISABLED)
    
    def create_gates_tab(self):
        """Create the quantum gates tab"""
        gates_frame = ttk.Frame(self.notebook)
        self.notebook.add(gates_frame, text="⚡ Quantum Gates")
        
        # Create a canvas for scrolling
        canvas = tk.Canvas(gates_frame, bg='#1a1a1a')
        scrollbar = ttk.Scrollbar(gates_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#1a1a1a')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Gate definitions
        gates = [
            ("X Gate (NOT)", "Flips |0⟩ ↔ |1⟩", "Pauli-X rotation", "#ff6b6b"),
            ("Y Gate", "Rotates around Y-axis", "Pauli-Y rotation", "#4ecdc4"),
            ("Z Gate", "Phase flip: |1⟩ → -|1⟩", "Pauli-Z rotation", "#96ceb4"),
            ("H Gate (Hadamard)", "Creates superposition", "|0⟩ → (|0⟩+|1⟩)/√2", "#f39c12"),
            ("S Gate", "Phase gate: |1⟩ → i|1⟩", "90° Z rotation", "#9b59b6"),
            ("T Gate", "π/8 gate", "45° Z rotation", "#e74c3c"),
            ("CNOT Gate", "Controlled NOT", "Entangles two qubits", "#00ff88"),
            ("CZ Gate", "Controlled Z", "Conditional phase flip", "#ff9ff3"),
        ]
        
        # Create gate cards
        for i, (name, description, formula, color) in enumerate(gates):
            self.create_gate_card(scrollable_frame, name, description, formula, color, i)
    
    def create_gate_card(self, parent, name, description, formula, color, row):
        """Create a card for each quantum gate"""
        card_frame = tk.Frame(parent, bg='#2a2a2a', relief=tk.RAISED, bd=2)
        card_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Gate name
        name_label = tk.Label(card_frame, text=name,
                             font=('Arial', 16, 'bold'),
                             fg=color, bg='#2a2a2a')
        name_label.pack(anchor=tk.W, padx=15, pady=(10, 5))
        
        # Description
        desc_label = tk.Label(card_frame, text=description,
                             font=('Arial', 12),
                             fg='#ffffff', bg='#2a2a2a')
        desc_label.pack(anchor=tk.W, padx=15, pady=2)
        
        # Formula
        formula_label = tk.Label(card_frame, text=f"Effect: {formula}",
                                font=('Arial', 10, 'italic'),
                                fg='#cccccc', bg='#2a2a2a')
        formula_label.pack(anchor=tk.W, padx=15, pady=(2, 10))
    
    def create_algorithms_tab(self):
        """Create the quantum algorithms tab"""
        algorithms_frame = ttk.Frame(self.notebook)
        self.notebook.add(algorithms_frame, text="🧠 Algorithms")
        
        # Scrollable text area
        algorithms_text = scrolledtext.ScrolledText(algorithms_frame, 
                                                   wrap=tk.WORD,
                                                   width=80, height=25,
                                                   bg='#2a2a2a', fg='#ffffff',
                                                   font=('Arial', 11),
                                                   insertbackground='#ffffff')
        algorithms_text.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Add algorithm content
        algorithms_content = """
🧠 FAMOUS QUANTUM ALGORITHMS

🔍 1. SHOR'S ALGORITHM (1994)
   Purpose: Integer factorization
   Impact: Breaks RSA encryption
   Speedup: Exponential over classical methods
   
   Key Idea:
   • Uses quantum Fourier transform
   • Finds period of modular exponentiation
   • Factors large numbers efficiently
   
   Applications:
   • Cryptography and security
   • Breaking current encryption schemes
   • Motivating post-quantum cryptography

🔍 2. GROVER'S ALGORITHM (1996)
   Purpose: Database search
   Impact: Quadratic speedup for search problems
   Speedup: √N instead of N comparisons
   
   Key Idea:
   • Amplitude amplification
   • Iteratively increases probability of correct answer
   • Uses quantum interference
   
   Applications:
   • Unstructured search
   • Optimization problems
   • Machine learning

🔍 3. DEUTSCH-JOZSA ALGORITHM
   Purpose: Determine if function is constant or balanced
   Impact: First quantum algorithm with exponential speedup
   Speedup: 1 query vs N/2 queries classically
   
   Key Idea:
   • Uses quantum parallelism
   • Evaluates function on all inputs simultaneously
   • Quantum interference reveals global property

🔍 4. SIMON'S ALGORITHM
   Purpose: Find hidden period in function
   Impact: Inspired Shor's algorithm
   Speedup: Exponential over classical methods
   
   Key Idea:
   • Uses quantum superposition
   • Finds XOR pattern in function
   • Linear system solving

🔍 5. VARIATIONAL QUANTUM EIGENSOLVER (VQE)
   Purpose: Find ground state of molecular systems
   Impact: Near-term quantum chemistry applications
   Approach: Hybrid quantum-classical optimization
   
   Key Idea:
   • Parametrized quantum circuits
   • Classical optimization loop
   • Minimizes energy expectation value

🔍 6. QUANTUM APPROXIMATE OPTIMIZATION ALGORITHM (QAOA)
   Purpose: Solve combinatorial optimization problems
   Impact: Near-term quantum advantage for optimization
   Approach: Alternating quantum operators
   
   Key Idea:
   • Problem-specific Hamiltonian
   • Mixing Hamiltonian
   • Variational parameter optimization

🎯 ALGORITHM CATEGORIES:

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

🔮 Future Directions:
• Fault-tolerant quantum algorithms
• Quantum machine learning
• Quantum error correction
• Distributed quantum computing
        """
        
        algorithms_text.insert(tk.END, algorithms_content)
        algorithms_text.config(state=tk.DISABLED)
    
    def create_resources_tab(self):
        """Create the resources and links tab"""
        resources_frame = ttk.Frame(self.notebook)
        self.notebook.add(resources_frame, text="🔗 Resources")
        
        # Main container
        main_container = tk.Frame(resources_frame, bg='#1a1a1a')
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Resources section
        resources_label = tk.Label(main_container, text="📚 Learning Resources",
                                  font=('Arial', 18, 'bold'),
                                  fg='#00ff88', bg='#1a1a1a')
        resources_label.pack(anchor=tk.W, pady=(0, 15))
        
        # Create resource links
        resources = [
            ("IBM Quantum Experience", "https://quantum-computing.ibm.com/", "Hands-on quantum programming"),
            ("Microsoft Quantum Development Kit", "https://azure.microsoft.com/en-us/products/quantum/", "Q# programming language"),
            ("Google Cirq", "https://quantumai.google/cirq", "Python framework for quantum circuits"),
            ("Qiskit Textbook", "https://qiskit.org/textbook/", "Comprehensive quantum computing textbook"),
            ("Quantum Computing: An Applied Approach", "https://www.springer.com/gp/book/9783030239213", "Academic textbook"),
            ("Nielsen & Chuang", "https://www.cambridge.org/core/books/quantum-computation-and-quantum-information/01E10196D0A682A6AEFFEA52D53BE9AE", "The quantum computing bible"),
        ]
        
        for title, url, description in resources:
            self.create_resource_link(main_container, title, url, description)
        
        # Separator
        separator = tk.Frame(main_container, height=2, bg='#4ecdc4')
        separator.pack(fill=tk.X, pady=20)
        
        # Tools section
        tools_label = tk.Label(main_container, text="🛠️ Quantum Computing Tools",
                              font=('Arial', 18, 'bold'),
                              fg='#f39c12', bg='#1a1a1a')
        tools_label.pack(anchor=tk.W, pady=(0, 15))
        
        tools = [
            ("Qiskit", "https://qiskit.org/", "Open-source quantum computing framework"),
            ("Cirq", "https://quantumai.google/cirq", "Google's quantum computing framework"),
            ("PennyLane", "https://pennylane.ai/", "Quantum machine learning library"),
            ("Forest SDK", "https://pyquil-docs.rigetti.com/en/stable/", "Rigetti's quantum programming toolkit"),
            ("Quantum Inspire", "https://www.quantum-inspire.com/", "QuTech's quantum computing platform"),
        ]
        
        for title, url, description in tools:
            self.create_resource_link(main_container, title, url, description)
    
    def create_resource_link(self, parent, title, url, description):
        """Create a clickable resource link"""
        link_frame = tk.Frame(parent, bg='#2a2a2a')
        link_frame.pack(fill=tk.X, pady=5)
        
        # Title (clickable)
        title_label = tk.Label(link_frame, text=f"🔗 {title}",
                              font=('Arial', 12, 'bold'),
                              fg='#4ecdc4', bg='#2a2a2a',
                              cursor='hand2')
        title_label.pack(anchor=tk.W, padx=15, pady=(8, 2))
        title_label.bind("<Button-1>", lambda e: self.open_url(url))
        
        # Description
        desc_label = tk.Label(link_frame, text=description,
                             font=('Arial', 10),
                             fg='#cccccc', bg='#2a2a2a')
        desc_label.pack(anchor=tk.W, padx=15, pady=(0, 8))
        
        # Hover effects
        def on_enter(event):
            title_label.configure(fg='#00ff88')
        
        def on_leave(event):
            title_label.configure(fg='#4ecdc4')
        
        title_label.bind("<Enter>", on_enter)
        title_label.bind("<Leave>", on_leave)
    
    def open_url(self, url):
        """Open URL in default browser"""
        try:
            webbrowser.open(url)
        except Exception as e:
            print(f"Error opening URL: {e}")
    
    def back_to_menu(self):
        """Go back to the main menu"""
        self.root.destroy()
        try:
            from game_mode_selection import GameModeSelection
            selection_window = GameModeSelection()
            selection_window.run()
        except Exception as e:
            print(f"Error returning to menu: {e}")
    
    def close_window(self):
        """Close the learn hub window"""
        self.root.destroy()

def main():
    """For testing the learn hub independently"""
    root = tk.Tk()
    app = LearnHub(root)
    root.mainloop()

if __name__ == "__main__":
    main()