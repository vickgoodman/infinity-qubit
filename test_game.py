#!/usr/bin/env python3
"""
Test script to check if all components work
"""

def test_imports():
    try:
        import tkinter as tk
        print("✅ Tkinter: OK")
    except ImportError:
        print("❌ Tkinter: FAILED")
        return False

    try:
        import numpy as np
        print("✅ NumPy: OK")
    except ImportError:
        print("❌ NumPy: FAILED - Run: pip install numpy")
        return False

    try:
        import qiskit
        print("✅ Qiskit: OK")
    except ImportError:
        print("❌ Qiskit: FAILED - Run: pip install qiskit")
        return False

    try:
        from qiskit_aer import Aer
        print("✅ Qiskit Aer: OK")
    except ImportError:
        print("❌ Qiskit Aer: FAILED - Run: pip install qiskit-aer")
        return False

    try:
        import json
        with open('levels.json', 'r') as f:
            levels = json.load(f)
        print(f"✅ Levels JSON: OK ({len(levels)} levels loaded)")
    except FileNotFoundError:
        print("❌ levels.json: NOT FOUND")
        return False
    except json.JSONDecodeError as e:
        print(f"❌ levels.json: INVALID JSON - {e}")
        return False

    try:
        from main import QubitPuzzleGame
        print("✅ Main game class: OK")
    except ImportError as e:
        print(f"❌ Main game class: FAILED - {e}")
        return False

    try:
        from game_tutorial import show_tutorial
        print("✅ Tutorial module: OK")
    except ImportError:
        print("⚠️ Tutorial module: Optional, but recommended")

    return True

if __name__ == "__main__":
    print("🔬 Testing Qubit Puzzle Solver Components...")
    print("-" * 50)

    if test_imports():
        print("-" * 50)
        print("✅ All components working! Run: python run_game.py")
    else:
        print("-" * 50)
        print("❌ Some components failed. Fix the issues above.")
