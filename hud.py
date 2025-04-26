import tkinter as tk
from tkinter import ttk
from typing import Dict, Optional
from core.game_state import GameState
from engine.decision_engine import suggest_action

class PokerHUD:
    def __init__(self, my_id: str):
        """Initialize the HUD window."""
        self.my_id = my_id
        self.root = tk.Tk()
        self.root.title("Poker HUD")
        self.root.attributes('-topmost', True)  # Keep window on top
        
        # Configure style
        style = ttk.Style()
        style.configure('Action.TLabel', font=('Arial', 12, 'bold'), padding=5)
        style.configure('Stats.TLabel', font=('Arial', 10), padding=3)
        
        # Create frames
        self.action_frame = ttk.Frame(self.root, padding="5")
        self.action_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.stats_frame = ttk.Frame(self.root, padding="5")
        self.stats_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create labels
        self.action_label = ttk.Label(
            self.action_frame, 
            text="Suggested Action: --", 
            style='Action.TLabel'
        )
        self.action_label.grid(row=0, column=0, sticky=tk.W)
        
        # Stats labels
        self.stats_labels: Dict[str, ttk.Label] = {}
        self.create_stat_label("Pot Size", "0", 0)
        self.create_stat_label("Stack", "0", 1)
        self.create_stat_label("Position", "--", 2)
        self.create_stat_label("Street", "Preflop", 3)
        self.create_stat_label("VPIP", "0%", 4)
        self.create_stat_label("PFR", "0%", 5)
        self.create_stat_label("3Bet", "0%", 6)
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.action_frame.columnconfigure(0, weight=1)
        self.stats_frame.columnconfigure(1, weight=1)
        
    def create_stat_label(self, name: str, initial_value: str, row: int) -> None:
        """Create a new stat label pair."""
        name_label = ttk.Label(
            self.stats_frame, 
            text=f"{name}:", 
            style='Stats.TLabel'
        )
        name_label.grid(row=row, column=0, sticky=tk.W)
        
        value_label = ttk.Label(
            self.stats_frame, 
            text=initial_value, 
            style='Stats.TLabel'
        )
        value_label.grid(row=row, column=1, sticky=tk.W)
        
        self.stats_labels[name] = value_label
        
    def update_action_field(self, action: str) -> None:
        """Update the suggested action display."""
        self.action_label.config(text=f"Suggested Action: {action}")
        
    def update_stats(self, game_state: GameState) -> None:
        """Update all stats based on the current game state."""
        if self.my_id not in game_state.players:
            return
            
        my_player = game_state.players[self.my_id]
        
        # Update basic stats
        self.stats_labels["Pot Size"].config(text=f"${game_state.pot_size:.2f}")
        self.stats_labels["Stack"].config(text=f"${my_player.stack:.2f}")
        self.stats_labels["Position"].config(text=my_player.position or "--")
        self.stats_labels["Street"].config(text=game_state.street.value.capitalize())
        
        # Update poker stats
        total_hands = my_player.hands_played
        if total_hands > 0:
            vpip_pct = (my_player.total_calls + my_player.total_bets) * 100 / total_hands
            pfr_pct = my_player.total_bets * 100 / total_hands
            self.stats_labels["VPIP"].config(text=f"{vpip_pct:.1f}%")
            self.stats_labels["PFR"].config(text=f"{pfr_pct:.1f}%")
            
        # Get and update suggested action
        suggested_action = suggest_action(game_state, self.my_id)
        self.update_action_field(suggested_action)
        
    def run(self) -> None:
        """Start the HUD window."""
        self.root.mainloop()
        
    def update(self, game_state: GameState) -> None:
        """Update all HUD elements."""
        self.update_stats(game_state)
        self.root.update()  # Force window update 