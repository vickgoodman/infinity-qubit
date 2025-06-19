#!/usr/bin/env python3
"""
Game Mode Selection Window for Infinity Qubit
Allows users to choose between different game modes.
"""

import sys
import tkinter as tk
import tkinter.messagebox as messagebox

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
        """Create the game mode selection interface"""
        # Main container
        main_frame = tk.Frame(self.root, bg='#1a1a1a')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=30)
        
        # Configure grid weights
        main_frame.grid_rowconfigure(1, weight=1)  # Make buttons area expandable
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Title section
        title_frame = tk.Frame(main_frame, bg='#1a1a1a')
        title_frame.grid(row=0, column=0, sticky='ew', pady=(20, 30))
        
        title_label = tk.Label(title_frame, text="🔬 Infinity Qubit",
                            font=('Arial', 32, 'bold'), 
                            fg='#00ff88', bg='#1a1a1a')
        title_label.pack()
        
        subtitle_label = tk.Label(title_frame, text="Choose Your Quantum Adventure",
                                font=('Arial', 16), 
                                fg='#ffffff', bg='#1a1a1a')
        subtitle_label.pack()
        
        # Game mode buttons container
        buttons_frame = tk.Frame(main_frame, bg='#1a1a1a')
        buttons_frame.grid(row=1, column=0, sticky='nsew', pady=20)
        
        # Create game mode buttons
        self.create_game_mode_buttons(buttons_frame)
        
        # Footer
        footer_frame = tk.Frame(main_frame, bg='#1a1a1a')
        footer_frame.grid(row=2, column=0, sticky='ew', pady=20)
        
        # Exit button
        exit_btn = tk.Button(footer_frame, text="❌ Exit Game",
                            command=self.exit_game,
                            font=('Arial', 12, 'bold'), 
                            bg='#ff6b6b', fg='#ffffff',
                            padx=20, pady=8, 
                            cursor='hand2')
        exit_btn.pack(side=tk.RIGHT)
        
        # Version info
        version_label = tk.Label(footer_frame, text="Version 1.0 | Built with Qiskit",
                                font=('Arial', 10), 
                                fg='#888888', bg='#1a1a1a')
        version_label.pack(side=tk.LEFT)

    def create_game_mode_buttons(self, parent):
        """Create the game mode selection buttons"""
        # Button configurations
        button_configs = [
            {
                'title': '📚 Tutorial Mode',
                'description': 'Interactive tutorial to learn\nquantum computing basics',
                'detail': '',
                'color': '#9b59b6',
                'command': self.start_tutorial_mode
            },
            {
                'title': '🎮 Puzzle Mode',
                'description': 'Learn quantum computing through\ninteractive puzzles and challenges',
                'detail': '',
                'color': '#00ff88',
                'command': self.start_puzzle_mode
            },       
            {
                'title': '🛠️ Sandbox Mode',
                'description': 'Free-form quantum circuit builder\nwith real-time visualization',
                'detail': '',
                'color': '#f39c12',
                'command': self.start_sandbox_mode
            },
            {
                'title': '🚀 Learn Hub',
                'description': 'Explore quantum computing concepts\nand resources in a dedicated hub',
                'detail': '',
                'color': '#e74c3c',
                'command': self.start_learn_hub_mode
                # 'coming_soon': True
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

    def create_mode_button(self, parent, config, row, col):
        """Create a single game mode button"""
        print(f"Creating button for: {config['title']}")
        
        # Create button text
        button_text = f"{config['title']}\n\n{config['description']}\n\n{config['detail']}"
        
        if config.get('coming_soon', False):
            button_text += "\n\n🔜 Coming Soon"
            button_state = tk.DISABLED
            button_command = None
        else:
            button_state = tk.NORMAL
            
            def button_command():
                print(f"Button clicked: {config['title']}")
                self.play_sound()
                config['command']()
        
        # Create the button
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
                action_btn.configure(bg=hover_color)
            
            def on_leave(event):
                action_btn.configure(bg=original_color)
            
            action_btn.bind("<Enter>", on_enter)
            action_btn.bind("<Leave>", on_leave)
        
        print(f"Button created successfully for: {config['title']}")

    def lighten_color(self, color):
        """Lighten a hex color for hover effects"""
        color_map = {
            '#00ff88': '#33ff99',
            '#9b59b6': '#b370d1',
            '#f39c12': '#f5b041',
            '#e74c3c': '#ec7063'
        }
        return color_map.get(color, color)

    def start_tutorial_mode(self):
        """Start the tutorial mode"""
        print("📚 Starting Tutorial Mode...")
        try:
            from tutorial import TutorialWindow
            # Hide the current window
            self.root.withdraw()
            # Create tutorial with callback to return to main menu
            TutorialWindow(self.root, self.return_to_main_menu)
        except ImportError as e:
            print(f"❌ Error importing tutorial: {e}")
            messagebox.showerror("Import Error", f"Could not import tutorial module: {e}")
            self.root.deiconify()  # Show the window again if error
        except Exception as e:
            print(f"❌ Error starting tutorial: {e}")
            messagebox.showerror("Error", f"Failed to start tutorial: {e}")
            self.root.deiconify()  # Show the window again if error

    def return_to_main_menu(self):
        """Return to the main menu from tutorial"""
        self.root.deiconify()  # Show the game mode selection window again
        self.root.lift()  # Bring window to front
        self.root.focus_set()  # Set focus to the window

    def start_puzzle_mode(self):
        """Start the puzzle mode"""
        print("📚 Starting Puzzle Mode...")
        self.root.destroy()
        try:
            from puzzle_mode import PuzzleMode
            puzzle_root = tk.Tk()
            puzzle_app = PuzzleMode(puzzle_root)
            puzzle_root.mainloop()
        except ImportError:
            print("❌ Puzzle mode module not found")
            messagebox.showerror("Error", "Puzzle mode module not available")
        except Exception as e:
            print(f"❌ Error starting puzzle mode: {e}")
            messagebox.showerror("Error", f"Error starting puzzle mode: {str(e)}")
    
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
            messagebox.showerror("Error", "Sandbox module not available")
        except Exception as e:
            print(f"❌ Error starting sandbox: {e}")
            messagebox.showerror("Error", f"Error starting sandbox: {str(e)}")
    
    def start_learn_hub_mode(self):
        """Start the learn hub mode"""
        print("🚀 Starting Learn Hub...")
        self.root.destroy()
        try:
            from learn_hub import LearnHub
            learn_hub_root = tk.Tk()
            learn_hub_app = LearnHub(learn_hub_root)
            learn_hub_root.mainloop()
        except ImportError:
            print("❌ Learn Hub module not found")
            messagebox.showerror("Error", "Learn Hub module not available")
        except Exception as e:
            print(f"❌ Error starting Learn Hub: {e}")
            messagebox.showerror("Error", f"Error starting Learn Hub: {str(e)}")
    
    def exit_game(self):
        """Exit the game"""
        print("👋 Exiting game...")
        self.play_sound()
        self.root.quit()
        self.root.destroy()
        sys.exit(0)
    
    def run(self):
        """Run the game mode selection window"""
        self.root.mainloop()

def main():
    """For testing the game mode selection independently"""
    app = GameModeSelection()
    app.run()

if __name__ == "__main__":
    main()