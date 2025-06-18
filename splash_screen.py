#!/usr/bin/env python3
"""
Qubit Puzzle Solver - Quantum Computing Educational Game

Run this file to start the game.
"""

import sys
import os
import tkinter as tk
from tkinter import ttk
import threading
import time

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

class SplashScreen:
    def __init__(self):
        self.splash = tk.Tk()
        self.splash.title("Infinity Qubit")
        
        # Add animation control flags
        self.animation_active = True
        self.text_animation_active = True
        
        # Remove window decorations
        self.splash.overrideredirect(True)
        
        # Get screen dimensions
        screen_width = self.splash.winfo_screenwidth()
        screen_height = self.splash.winfo_screenheight()
        
        # Splash screen dimensions
        splash_width = 600
        splash_height = 400
        
        # Center the splash screen
        x = (screen_width - splash_width) // 2
        y = (screen_height - splash_height) // 2
        
        self.splash.geometry(f"{splash_width}x{splash_height}+{x}+{y}")
        self.splash.configure(bg='#1a1a1a')
        
        # Make splash screen stay on top
        self.splash.attributes('-topmost', True)
        
        self.create_splash_content()
        self.animate_loading()
        
        # Start timer to close splash screen
        self.splash.after(4000, self.close_splash)
        
    def create_splash_content(self):
        """Create the content for the splash screen"""
        # Main container
        main_frame = tk.Frame(self.splash, bg='#1a1a1a')
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = tk.Label(main_frame, text="🔬 Infinity Qubit",
                              font=('Arial', 32, 'bold'), 
                              fg='#00ff88', bg='#1a1a1a')
        title_label.pack(pady=(60, 20))
        
        # Subtitle
        subtitle_label = tk.Label(main_frame, text="Quantum Computing Educational Game",
                                 font=('Arial', 16), 
                                 fg='#ffffff', bg='#1a1a1a')
        subtitle_label.pack(pady=(0, 40))
        
        # Quantum circuit animation area
        self.animation_frame = tk.Frame(main_frame, bg='#1a1a1a')
        self.animation_frame.pack(pady=20)
        
        # Create animated quantum gates
        self.create_quantum_animation()
        
        # Loading text
        self.loading_label = tk.Label(main_frame, text="Initializing quantum circuits...",
                                     font=('Arial', 12), 
                                     fg='#4ecdc4', bg='#1a1a1a')
        self.loading_label.pack(pady=(40, 10))
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate', 
                                       length=300, style='Splash.Horizontal.TProgressbar')
        self.progress.pack(pady=10)
        
        # Version info
        version_label = tk.Label(main_frame, text="Version 1.0 | Built with Qiskit",
                                font=('Arial', 10), 
                                fg='#888888', bg='#1a1a1a')
        version_label.pack(side=tk.BOTTOM, pady=(0, 20))
        
        # Configure progress bar style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Splash.Horizontal.TProgressbar',
                       background='#00ff88',
                       troughcolor='#2a2a2a',
                       borderwidth=0,
                       lightcolor='#00ff88',
                       darkcolor='#00ff88')
    
    def create_quantum_animation(self):
        """Create animated quantum circuit elements"""
        # Create a simple quantum circuit visualization
        circuit_canvas = tk.Canvas(self.animation_frame, width=400, height=100,
                                  bg='#1a1a1a', highlightthickness=0)
        circuit_canvas.pack()
        
        # Draw quantum wires
        for i in range(3):
            y = 20 + i * 30
            circuit_canvas.create_line(50, y, 350, y, fill='#ffffff', width=2)
            circuit_canvas.create_text(30, y, text=f'q{i}', fill='#ffffff', font=('Arial', 10))
        
        # Store canvas reference for animation
        self.circuit_canvas = circuit_canvas
        
        # Initial gate positions
        self.gate_positions = [100, 180, 260]
        self.gate_colors = ['#ff6b6b', '#4ecdc4', '#96ceb4']
        self.gate_labels = ['H', 'X', 'Z']
        
        self.draw_animated_gates()
    
    def draw_animated_gates(self):
        """Draw the animated quantum gates"""
        # Check if animation should continue and canvas exists
        if not self.animation_active or not hasattr(self, 'circuit_canvas'):
            return
            
        try:
            # Clear previous gates
            self.circuit_canvas.delete("gate")
            
            # Draw gates at current positions
            for i, (x, color, label) in enumerate(zip(self.gate_positions, self.gate_colors, self.gate_labels)):
                y = 20 + i * 30
                
                # Gate rectangle
                self.circuit_canvas.create_rectangle(x-20, y-15, x+20, y+15,
                                                   fill=color, outline='#ffffff', width=2, tags="gate")
                
                # Gate label
                self.circuit_canvas.create_text(x, y, text=label, fill='#000000',
                                              font=('Arial', 12, 'bold'), tags="gate")
        except tk.TclError:
            # Canvas has been destroyed, stop animation
            self.animation_active = False
    
    def animate_loading(self):
        """Animate the loading elements"""
        # Start progress bar animation
        self.progress.start(10)
        
        # Animate loading text
        self.animate_text()
        
        # Animate quantum gates
        self.animate_gates()
    
    def animate_text(self):
        """Animate the loading text"""
        texts = [
            "Initializing quantum circuits...",
            "Loading quantum gates...",
            "Preparing qubit states...",
            "Calibrating quantum simulator...",
            "Ready to explore quantum computing!"
        ]
        
        def update_text(index=0):
            # Check if animation should continue and widget exists
            if not self.text_animation_active:
                return
                
            try:
                if hasattr(self, 'loading_label') and self.loading_label.winfo_exists():
                    self.loading_label.config(text=texts[index % len(texts)])
                    if index < 20 and self.text_animation_active:  # Animate for ~4 seconds
                        self.splash.after(800, lambda: update_text(index + 1))
            except tk.TclError:
                # Widget has been destroyed, stop animation
                self.text_animation_active = False
        
        update_text()
    
    def animate_gates(self):
        """Animate the quantum gates movement"""
        def move_gates():
            # Check if animation should continue
            if not self.animation_active:
                return
                
            try:
                if hasattr(self, 'circuit_canvas') and self.circuit_canvas.winfo_exists():
                    # Move gates slightly
                    for i in range(len(self.gate_positions)):
                        self.gate_positions[i] += 2
                        if self.gate_positions[i] > 370:
                            self.gate_positions[i] = 80
                    
                    self.draw_animated_gates()
                    
                    # Continue animation if still active
                    if self.animation_active:
                        self.splash.after(100, move_gates)
            except tk.TclError:
                # Widget has been destroyed, stop animation
                self.animation_active = False
        
        move_gates()
    
    def close_splash(self):
        """Close the splash screen and show game mode selection"""
        # Stop all animations before destroying the window
        self.animation_active = False
        self.text_animation_active = False
        
        # Stop progress bar
        try:
            self.progress.stop()
        except:
            pass
        
        # Small delay to ensure all animations stop
        self.splash.after(100, self._destroy_and_continue)
    
    def _destroy_and_continue(self):
        """Destroy splash screen and continue to game mode selection"""
        try:
            self.splash.destroy()
        except:
            pass
        
        # Show game mode selection
        self.show_game_mode_selection()
    
    def show_game_mode_selection(self):
        """Show the game mode selection window"""
        selection_window = GameModeSelection()
        selection_window.run()
    
    def run(self):
        """Run the splash screen"""
        self.splash.mainloop()

class GameModeSelection:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Infinity Qubit - Game Mode Selection")
        
        # Get screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Window dimensions
        window_width = 800
        window_height = 650
        
        # Center the window
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.configure(bg='#1a1a1a')
        self.root.resizable(False, False)
        
        # Store dimensions
        self.window_width = window_width
        self.window_height = window_height
        
        # Initialize sound system
        try:
            import pygame
            pygame.mixer.init()
            self.sound_enabled = True
        except:
            self.sound_enabled = False
        
        self.create_selection_ui()
        
        # Make sure window is focused and on top
        self.root.lift()
        self.root.focus_force()
    
    def play_sound(self, sound_type="click"):
        """Play a simple click sound"""
        if self.sound_enabled:
            try:
                import pygame
                import numpy as np
                
                # Create a simple click sound
                duration = 0.1
                sample_rate = 22050
                frequency = 440
                frames = int(duration * sample_rate)
                arr = np.sin(2 * np.pi * frequency * np.linspace(0, duration, frames))
                arr = (arr * 16383).astype(np.int16)
                sound = pygame.sndarray.make_sound(arr)
                sound.set_volume(0.3)
                sound.play()
            except:
                pass
    
    def create_selection_ui(self):
        """Create the game mode selection interface - SIMPLIFIED"""
        # Main container
        main_frame = tk.Frame(self.root, bg='#1a1a1a')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=30)
        
        # Test button at the top
        test_btn = tk.Button(main_frame, text="🔴 TEST BUTTON - CLICK ME",
                            command=lambda: print("TEST BUTTON WORKS!"),
                            font=('Arial', 14, 'bold'),
                            bg='#ff0000', fg='#ffffff',
                            padx=20, pady=10,
                            cursor='hand2')
        test_btn.pack(pady=10)
        
        # Title
        title_label = tk.Label(main_frame, text="🔬 Infinity Qubit",
                            font=('Arial', 32, 'bold'), 
                            fg='#00ff88', bg='#1a1a1a')
        title_label.pack(pady=(10, 5))
        
        # Subtitle
        subtitle_label = tk.Label(main_frame, text="Choose Your Quantum Adventure",
                                font=('Arial', 16), 
                                fg='#ffffff', bg='#1a1a1a')
        subtitle_label.pack(pady=(0, 20))
        
        # Game mode buttons container - SIMPLIFIED
        buttons_frame = tk.Frame(main_frame, bg='#1a1a1a')
        buttons_frame.pack(expand=True, fill=tk.BOTH, pady=10)
        
        # Create game mode buttons
        self.create_game_mode_buttons(buttons_frame)
        
        # Footer with just the exit button
        footer_frame = tk.Frame(main_frame, bg='#1a1a1a')
        footer_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
        
        # Exit button
        exit_btn = tk.Button(footer_frame, text="❌ Exit Game",
                            command=self.exit_game,
                            font=('Arial', 12, 'bold'), 
                            bg='#ff6b6b', fg='#ffffff',
                            padx=20, pady=8, 
                            cursor='hand2')
        exit_btn.pack(side=tk.RIGHT)
        
        # Simple test to verify button creation
        print("UI created successfully")
    
    def create_game_mode_buttons(self, parent):
        """Create the game mode selection buttons"""
        # Button configurations
        button_configs = [
            {
                'title': '🎮 Puzzle Mode',
                'description': 'Learn quantum computing through\ninteractive puzzles and challenges',
                'detail': 'Progress through levels, solve quantum puzzles,\nand master quantum gates step by step',
                'color': '#00ff88',
                'command': self.start_puzzle_mode
            },
            {
                'title': '📚 Tutorial Mode',
                'description': 'Interactive tutorial to learn\nquantum computing basics',
                'detail': 'Perfect for beginners! Learn quantum concepts\nwith guided explanations and examples',
                'color': '#9b59b6',
                'command': self.start_tutorial_mode
            },
            {
                'title': '🛠️ Sandbox Mode',
                'description': 'Free-form quantum circuit builder\nwith real-time visualization',
                'detail': 'Experiment freely with quantum gates,\nbuild custom circuits, and explore quantum states',
                'color': '#f39c12',
                'command': self.start_sandbox_mode
            },
            {
                'title': '🚀 Challenge Mode',
                'description': 'Advanced quantum challenges\nfor experienced users',
                'detail': 'Test your quantum knowledge with\ncomplex puzzles and time-based challenges',
                'color': '#e74c3c',
                'command': self.start_challenge_mode,
                'coming_soon': True
            }
        ]
        
        # Create buttons in a 2x2 grid
        row = 0
        col = 0
        
        for config in button_configs:
            self.create_mode_button(parent, config, row, col)
            col += 1
            if col > 1:
                col = 0
                row += 1

    # def create_mode_button(self, parent, config, row, col):
    #     """Create a single game mode button"""
    #     # Button frame
    #     button_frame = tk.Frame(parent, bg='#2a2a2a', relief=tk.RAISED, bd=3)
    #     button_frame.grid(row=row, column=col, padx=20, pady=15, sticky='nsew')
        
    #     # Configure grid weights for equal sizing
    #     parent.grid_rowconfigure(row, weight=1)
    #     parent.grid_columnconfigure(col, weight=1)
        
    #     # Button content frame
    #     content_frame = tk.Frame(button_frame, bg='#2a2a2a')
    #     content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
    #     # Title
    #     title_label = tk.Label(content_frame, text=config['title'],
    #                         font=('Arial', 18, 'bold'), 
    #                         fg=config['color'], bg='#2a2a2a')
    #     title_label.pack(pady=(0, 10))
        
    #     # Description
    #     desc_label = tk.Label(content_frame, text=config['description'],
    #                         font=('Arial', 12), 
    #                         fg='#ffffff', bg='#2a2a2a',
    #                         justify=tk.CENTER)
    #     desc_label.pack(pady=(0, 8))
        
    #     # Detail text
    #     detail_label = tk.Label(content_frame, text=config['detail'],
    #                         font=('Arial', 10), 
    #                         fg='#cccccc', bg='#2a2a2a',
    #                         justify=tk.CENTER)
    #     detail_label.pack(pady=(0, 15))
        
    #     # Coming soon badge if applicable
    #     if config.get('coming_soon', False):
    #         coming_soon_label = tk.Label(content_frame, text="🔜 Coming Soon",
    #                                     font=('Arial', 10, 'bold'), 
    #                                     fg='#ff6b6b', bg='#2a2a2a')
    #         coming_soon_label.pack(pady=(0, 10))
        
    #     # Action button - SIMPLIFIED VERSION
    #     button_text = "Select Mode" if not config.get('coming_soon', False) else "Coming Soon"
    #     button_state = tk.NORMAL if not config.get('coming_soon', False) else tk.DISABLED
        
    #     # Create a simple command function with proper closure
    #     def button_command():
    #         print(f"Button clicked: {config['title']}")
    #         self.play_sound()
    #         config['command']()
        
    #     action_btn = tk.Button(content_frame, text=button_text,
    #                         command=button_command if not config.get('coming_soon', False) else None,
    #                         font=('Arial', 12, 'bold'), 
    #                         bg=config['color'], fg='#000000',
    #                         padx=25, pady=10, state=button_state,
    #                         relief=tk.RAISED, bd=2,
    #                         cursor='hand2')
    #     action_btn.pack()
        
    #     # Simple hover effects
    #     if not config.get('coming_soon', False):
    #         original_color = config['color']
    #         hover_color = self.lighten_color(original_color)
            
    #         def on_enter(event):
    #             action_btn.configure(bg=hover_color)
            
    #         def on_leave(event):
    #             action_btn.configure(bg=original_color)
            
    #         action_btn.bind("<Enter>", on_enter)
    #         action_btn.bind("<Leave>", on_leave)
            
    #         # Add a test binding to verify the button receives events
    #         def on_button_press(event):
    #             print(f"Mouse pressed on {config['title']} button")
            
    #         action_btn.bind("<Button-1>", on_button_press)

    # Replace the create_mode_button method with this simplified version:

    def create_mode_button(self, parent, config, row, col):
        """Create a single game mode button - SIMPLIFIED VERSION"""
        print(f"Creating button for: {config['title']}")
        
        # Create a single button that acts as the entire card
        button_text = f"{config['title']}\n\n{config['description']}\n\n{config['detail']}"
        
        if config.get('coming_soon', False):
            button_text += "\n\n🔜 Coming Soon"
            button_state = tk.DISABLED
            button_command = None
        else:
            button_text += "\n\n>>> Click to Select <<<"
            button_state = tk.NORMAL
            
            def button_command():
                print(f"Button clicked: {config['title']}")
                self.play_sound()
                config['command']()
        
        # Create a single button that spans the entire area
        action_btn = tk.Button(parent, 
                            text=button_text,
                            command=button_command,
                            font=('Arial', 11), 
                            bg=config['color'], 
                            fg='#000000',
                            state=button_state,
                            relief=tk.RAISED, 
                            bd=3,
                            cursor='hand2',
                            padx=20, 
                            pady=20,
                            justify=tk.CENTER,
                            wraplength=250)
        
        action_btn.grid(row=row, column=col, padx=20, pady=15, sticky='nsew')
        
        # Configure grid weights
        parent.grid_rowconfigure(row, weight=1)
        parent.grid_columnconfigure(col, weight=1)
        
        # Add hover effects only for enabled buttons
        if not config.get('coming_soon', False):
            original_color = config['color']
            hover_color = self.lighten_color(original_color)
            
            def on_enter(event):
                print(f"Mouse entered: {config['title']}")
                action_btn.configure(bg=hover_color)
            
            def on_leave(event):
                print(f"Mouse left: {config['title']}")
                action_btn.configure(bg=original_color)
            
            def on_click(event):
                print(f"Mouse clicked: {config['title']}")
            
            action_btn.bind("<Enter>", on_enter)
            action_btn.bind("<Leave>", on_leave)
            action_btn.bind("<Button-1>", on_click)
        
        print(f"Button created successfully for: {config['title']}")

    # Add this method to the GameModeSelection class for testing:

    # Add this method to the GameModeSelection class for testing:

    def test_simple_button(self):
        """Create a simple test button to verify click functionality"""
        test_btn = tk.Button(self.root, text="TEST BUTTON - CLICK ME",
                            command=lambda: print("TEST BUTTON CLICKED!"),
                            font=('Arial', 16, 'bold'),
                            bg='#ff0000', fg='#ffffff',
                            padx=20, pady=10,
                            cursor='hand2')
        test_btn.pack(pady=20)
        
        def test_click(event):
            print("TEST BUTTON - Mouse click detected!")
        
        test_btn.bind("<Button-1>", test_click)

    def lighten_color(self, color):
        """Lighten a hex color for hover effects"""
        # Simple color lightening (this is a basic implementation)
        color_map = {
            '#00ff88': '#33ff99',
            '#9b59b6': '#b370d1',
            '#f39c12': '#f5b041',
            '#e74c3c': '#ec7063'
        }
        return color_map.get(color, color)
    
    def start_puzzle_mode(self):
        print("🎮 Puzzle Mode clicked...")
        """Start the puzzle mode (main game)"""
        print("🎮 Starting Puzzle Mode...")
        self.root.destroy()
        try:
            from main import main
            main()
        except ImportError as e:
            print(f"❌ Error importing puzzle mode: {e}")
            import tkinter.messagebox as messagebox
            messagebox.showerror("Import Error", f"Could not import main module: {e}")
        except Exception as e:
            print(f"❌ Error starting puzzle mode: {e}")
            import tkinter.messagebox as messagebox
            messagebox.showerror("Error", f"Failed to start puzzle mode: {e}")
    
    def start_tutorial_mode(self):
        """Start the tutorial mode"""
        print("📚 Starting Tutorial Mode...")
        self.root.destroy()
        try:
            from game_tutorial import show_tutorial
            # Create a temporary root for tutorial
            tutorial_root = tk.Tk()
            tutorial_root.withdraw()  # Hide the root window
            show_tutorial(tutorial_root)
            tutorial_root.mainloop()
        except ImportError:
            print("❌ Tutorial module not found")
            import tkinter.messagebox as messagebox
            messagebox.showerror("Error", "Tutorial module not available")
        except Exception as e:
            print(f"❌ Error starting tutorial: {e}")
            import tkinter.messagebox as messagebox
            messagebox.showerror("Error", f"Error starting tutorial: {str(e)}")
    
    def start_sandbox_mode(self):
        """Start the sandbox mode"""
        print("🛠️ Starting Sandbox Mode...")
        self.root.destroy()
        try:
            from sandbox_mode import SandboxMode
            sandbox_root = tk.Tk()
            sandbox_app = SandboxMode(sandbox_root)
            sandbox_root.mainloop()
        except ImportError:
            print("❌ Sandbox module not found")
            import tkinter.messagebox as messagebox
            messagebox.showerror("Error", "Sandbox module not available")
        except Exception as e:
            print(f"❌ Error starting sandbox: {e}")
            import tkinter.messagebox as messagebox
            messagebox.showerror("Error", f"Error starting sandbox: {str(e)}")
    
    def start_challenge_mode(self):
        """Start the challenge mode (placeholder for future implementation)"""
        print("🚀 Challenge Mode clicked...")
        import tkinter.messagebox as messagebox
        messagebox.showinfo("Coming Soon", 
                           "🚀 Challenge Mode is coming soon!\n\n"
                           "This mode will feature:\n"
                           "• Timed quantum puzzles\n"
                           "• Advanced quantum algorithms\n"
                           "• Leaderboards and scoring\n"
                           "• Multi-qubit complex circuits\n\n"
                           "Stay tuned for updates!")
    
    def show_error(self, message):
        """Show error message and return to selection"""
        import tkinter.messagebox as messagebox
        messagebox.showerror("Error", message)
        # Don't recreate the window, just show the error
    
    def exit_game(self):
        """Exit the game"""
        print("👋 Exiting game...")
        self.play_sound()
        self.root.quit()
        self.root.destroy()
        import sys
        sys.exit(0)
    
    def run(self):
        """Run the game mode selection window"""
        self.root.mainloop()

def show_splash_screen():
    """Show the splash screen before the game mode selection"""
    splash = SplashScreen()
    splash.run()

if __name__ == "__main__":
    try:
        show_splash_screen()
    except KeyboardInterrupt:
        print("\n👋 Thanks for trying Infinity Qubit!")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error running game: {e}")
        sys.exit(1)