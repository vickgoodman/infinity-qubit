# infinity-qubit

# 🔬 Qubit Puzzle Solver

An educational quantum computing puzzle game where players learn quantum gates by solving circuit puzzles.

## 🎮 Game Overview

Transform quantum states by placing gates in the correct sequence! Each level presents a quantum puzzle where you must:

- Start with an input quantum state (like |0⟩)
- Use available quantum gates (H, X, Z, CNOT, etc.)
- Reach the target state (like |+⟩ or Bell states)

## 🚀 Getting Started

### Prerequisites

```bash
pip install qiskit numpy
```

### Running the Game

```bash
python run_game.py
```

## 🎯 How to Play

1. **Select Gates**: Click on available gate buttons to add them to your circuit
2. **Build Circuit**: Gates are placed in sequence from left to right
3. **Run Circuit**: Click "🚀 Run Circuit" to execute your quantum circuit
4. **Check Result**: See if your output matches the target state
5. **Level Up**: Solve puzzles to unlock new levels with more complex challenges

## 🔬 Quantum Gates

- **H (Hadamard)**: Creates superposition
- **X (Pauli-X)**: Bit flip gate
- **Z (Pauli-Z)**: Phase flip gate
- **I (Identity)**: Does nothing (useful for optimization)
- **CNOT**: Two-qubit entangling gate

## 🏆 Scoring

- Base score: 100 points per level
- Efficiency bonus: -5 points per gate used
- Try to solve puzzles with fewer gates for higher scores!

## 📚 Educational Value

This game teaches:

- Quantum state manipulation
- Gate operations and their effects
- Superposition and entanglement concepts
- Quantum circuit design principles

## 🛠️ Technical Details

- Built with Python + Tkinter for the UI
- Uses Qiskit for quantum simulation
- Modular level system with JSON configuration
- Real quantum state calculations

## 🎓 Learning Path

1. **Level 1**: Basic superposition with Hadamard gate
2. **Level 2**: Bit flips with X gate
3. **Level 3**: Phase manipulation with Z gate
4. **Level 4**: Entanglement with CNOT gate
5. **Advanced**: Custom puzzles and multi-qubit challenges

## 🔧 Adding Custom Levels

Edit `levels.json` to add your own puzzles:

```json
{
  "name": "Your Puzzle",
  "description": "Puzzle description",
  "input_state": "|0⟩",
  "target_state": "|1⟩",
  "available_gates": ["H", "X"],
  "qubits": 1,
  "hint": "Your helpful hint"
}
```

## 🎪 Features

- ✅ Interactive quantum circuit builder
- ✅ Real-time state visualization
- ✅ Progressive difficulty levels
- ✅ Hint system for guidance
- ✅ Score tracking and efficiency rewards
- ✅ Educational tooltips and explanations

## 🤝 Contributing

Feel free to contribute additional levels, features, or improvements!

## 📜 License

Educational use - feel free to modify and share!

---

🌟 **Happy Quantum Puzzle Solving!** 🌟
