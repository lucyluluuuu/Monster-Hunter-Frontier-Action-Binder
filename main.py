#!/usr/bin/env python3
"""
MHF Controller Remapping Tool - With English Display Names
Japanese names are preserved in the config file, but displayed in English in the UI
"""

import sys
import os
import re
import shutil
import time

def main():
    import tkinter as tk
    from tkinter import ttk, filedialog, messagebox
    
    # Translation mapping for common action names
    CATEGORY_TRANSLATIONS = {
        "基本アクション": "Basic Actions",
        "Sword & Shield": "Sword & Shield",
        "Dual Blades": "Dual Blades",
        "Gesture": "Gesture",
        "Great Sword": "Great Sword",
        "Long Sword": "Long Sword",
        "Hammer": "Hammer",
        "Hunting Horn": "Hunting Horn",
        "Lance": "Lance",
        "Gunlance": "Gunlance",
        "Bowgun": "Bowgun",
        "Bow": "Bow",
        "Switch Axe F": "Switch Axe F",
        "Magnet Spike 1": "Magnet Spike 1",
        "Magnet Spike 2": "Magnet Spike 2",
        "System": "System",
        "Chat": "Chat",
        "Gallery": "Gallery",
        "Clan Message": "Clan Message",
        "Nyarendo": "Nyarendo",
        "Convenience Functions": "Convenience Functions",
    }
    
    ACTION_TRANSLATIONS = {
        # Basic Actions (Category 0)
        "Move・Forward": "Move Forward",
        "Move・Back": "Move Back",
        "Move・Left": "Move Left",
        "Move・Right": "Move Right",
        "Dash・Forward": "Dash Forward",
        "Dash・Back": "Dash Back",
        "Dash・Left": "Dash Left",
        "Dash・Right": "Dash Right",
        "Walk": "Walk",
        "Dash": "Dash",
        "アナログアクション↑": "Analog Action Up",
        "アナログアクション↓": "Analog Action Down",
        "アナログアクション←": "Analog Action Left",
        "アナログアクション→": "Analog Action Right",
        "方向・前": "Direction Forward",
        "方向・後": "Direction Back",
        "方向・左": "Direction Left",
        "方向・右": "Direction Right",
        "方向・移動": "Direction Move",
        "方向・ダッシュ": "Direction Dash",
        "会話／ボックス": "Talk / Box",
        "会話／ボックス(ロビー)": "Talk / Box (Lobby)",
        "調べる／段差を登る": "Examine / Climb Ledge",
        "しゃがむ／回避行動": "Crouch / Evade",
        "回避行動": "Evade",
        "Reset Camera": "Reset Camera",
        "カメラ/ボウガン照準": "Camera / Bowgun Aim",
        "カメラ/アイテム選択": "Camera / Item Select",
        "Item Bar": "Item Bar",
        "Select Item・Left": "Select Item Left",
        "Select Item・Right": "Select Item Right",
        "Select Ammo・Up": "Select Ammo Up",
        "Select Ammo・Down": "Select Ammo Down",
        "Use Item": "Use Item",
        "アイテムの使用(構え)": "Use Item (Stance)",
        "Signal": "Signal",
        "カメラ操作　上": "Camera Up",
        "カメラ操作　下": "Camera Down",
        "カメラ操作　左": "Camera Left",
        "カメラ操作　右": "Camera Right",
        "Scope Camera A↑": "Scope Camera A Up",
        "Scope Camera A↓": "Scope Camera A Down",
        "Scope Camera A←": "Scope Camera A Left",
        "Scope Camera A→": "Scope Camera A Right",
        "Scope Camera D↑": "Scope Camera D Up",
        "Scope Camera D↓": "Scope Camera D Down",
        "Scope Camera D←": "Scope Camera D Left",
        "Scope Camera D→": "Scope Camera D Right",
        "スコープカメラ減速": "Scope Camera Slow",
        "スコープ倍率　拡大": "Scope Zoom In",
        "スコープ倍率　縮小": "Scope Zoom Out",
        "Kick": "Kick",
        "Add Sword Crystal": "Add Sword Crystal",
        "モンスター注視": "Focus Monster",
        "採集ポイント注視": "Focus Gathering Point",
        "コンボ再生": "Combo Playback",
        "マルチ操作アクティブ": "Multi Operation Active",
        "マルチ操作アタック": "Multi Operation Attack",
        "マルチ操作パッシブ": "Multi Operation Passive",
        "マルチ操作ブース": "Multi Operation Boost",
        
        # Weapon - Sword & Shield (Category 1)
        "斬り下ろし": "Overhead Slash",
        "ジャンプ攻撃": "Jump Attack",
        "Roundslash": "Roundslash",
        "Rising Slash": "Rising Slash",
        "ガード(武器出し)": "Guard (Draw Weapon)",
        "Guard": "Guard",
        "ガード攻撃": "Guard Attack",
        
        # Dual Blades (Category 2)
        "Lunging Strike": "Lunging Strike",
        "Demon Mode": "Demon Mode",
        "鬼人化(武器出し)": "Demonize Draw Weapon",
        "Clash Sharpen": "Clash Sharpen",
        
        # Gesture (Category 3)
        "アナログアクション↑": "Analog Action Up",
        "アナログアクション↓": "Analog Action Down",
        "攻撃01": "Attack 01",
        "攻撃02": "Attack 02",
        "パイル": "Pile",
        "武器出し(短)": "Draw Weapon (Short)",
        "ガード(武器出し)": "Guard (Draw Weapon)",
        "Guard": "Guard",
        "EX Evade": "EX Evade",
        
        # Great Sword (Category 4)
        "ため斬り(ポータブル)": "Charge Slash",
        "ため斬り(武器出し,ポータブル)": "Charge Slash (Draw)",
        "Wide Sweep": "Wide Sweep",
        "Super Armor G": "Super Armor G",
        "Super Guard": "Super Guard",
        
        # Long Sword (Category 5)
        "Step Slash": "Step Slash",
        "Fade Slash": "Fade Slash",
        "Thrust": "Thrust",
        "気刃斬り(武器出し)": "Spirit Blade (Draw)",
        "Spirit Blade": "Spirit Blade",
        "受け流し": "Parry",
        "締め斬り": "Finishing Slash",
        "武器出し受け流し": "Draw Parry",
        
        # Hammer (Category 6)
        "Overhead Smash": "Overhead Smash",
        "Side Smash": "Side Smash",
        "Charge": "Charge",
        "ため(武器出し)": "Charge (Draw)",
        
        # Hunting Horn (Category 7)
        "叩きつけ": "Slam",
        "Hilt Stab": "Hilt Stab",
        "ぶん回し(ポータブル)": "Spin Attack",
        "Perform/Switch Strike": "Perform/Switch Strike",
        "演奏(武器出し)": "Perform (Draw)",
        "Note 1": "Note 1",
        "Note 2・Left": "Note 2 Left",
        "Note 2・Right": "Note 2 Right",
        "Note 3": "Note 3",
        "Sonic Wave": "Sonic Wave",
        
        # Lance (Category 8)
        "Mid Thrust": "Mid Thrust",
        "High Thrust": "High Thrust",
        "Dash Attack": "Dash Attack",
        "上段突き(武器出し)": "High Thrust (Draw)",
        "バフ": "Buff",
        
        # Gunlance (Category 9)
        "Forward Thrust": "Forward Thrust",
        "Shelling": "Shelling",
        "Wyvern's Fire": "Wyvern's Fire",
        "Reload": "Reload",
        "Element Blade": "Element Blade",
        
        # Bowgun (Category 10)
        "Melee Attack": "Melee Attack",
        "Fire": "Fire",
        "スコープ画面 ON/OFF": "Scope ON/OFF",
        "照準モード": "Aim Mode",
        "スコープ/照準": "Scope/Aim",
        "照準リセット": "Reset Aim",
        "FPS移動 前": "FPS Move Forward",
        "FPS移動 後": "FPS Move Back",
        "FPS移動 左": "FPS Move Left",
        "FPS移動 右": "FPS Move Right",
        "FPSカメラ 上": "FPS Camera Up",
        "FPSカメラ 下": "FPS Camera Down",
        "FPSカメラ 左": "FPS Camera Left",
        "FPSカメラ 右": "FPS Camera Right",
        "FPSスコープ 拡大": "FPS Scope Zoom In",
        "FPSスコープ 縮小": "FPS Scope Zoom Out",
        "FPSリロード": "FPS Reload",
        "FPS発射": "FPS Fire",
        
        # Bow (Category 11)
        "Draw Bow": "Draw Bow",
        "Arc Shot Type": "Arc Shot Type",
        "Add Coating": "Add Coating",
        "照準移動↑": "Aim Move Up",
        "照準移動↓": "Aim Move Down",
        "照準移動←": "Aim Move Left",
        "照準移動→": "Aim Move Right",
        "近接攻撃(武器出し)": "Melee (Draw)",
        "照準モード(武器出し)": "Aim Mode (Draw)",
        "Crouch": "Crouch",
        "Melee Attack 2": "Melee Attack 2",
        "近接攻撃(武器出し)2": "Melee (Draw) 2",
        
        # Switch Axe (Category 12)
        "Overhead Slash": "Overhead Slash",
        "Side Slash": "Side Slash",
        "Morph": "Charge",
        "抜刀変形斬り": "Draw Morph Slash",
        "Element Discharge": "Element Discharge/Morph",
        "抜刀特殊アクション2": "Draw Sword Slash",
        "特殊ガード": "Parry",
        "抜刀ガード2": "Draw Parry",
        "抜刀溜め": "Draw Charge",
        
        # Magnet Spike (Category 13 & 14)
        "攻撃R↑|△": "Attack R Up",
        "攻撃R→|○": "Attack R Right",
        "攻撃R↓|△○": "Attack R Down",
        "トリガー(R1)": "Trigger (R1)",
        "ガードカウンター(R←|R2)": "Guard Counter",
        "回避(×)": "Evade",
        "変形(R3|SELECT)": "Transform",
        "トリガー(L2)": "Trigger (L2)",
        "特殊(A)": "Special (A)",
        "特殊(Select)": "Special (Select)",
        
        # System (Category 15)
        "Menu/Back": "Menu/Back",
        "F Key Side Swap": "F Key Side Swap",
        "ACT Mode": "ACT Mode",
        "Map Display Switch": "Map Display Switch",
        "Scene Skip": "Scene Skip",
        "Screenshot": "Screenshot",
        "Confirm": "Confirm",
        "Cancel": "Cancel",
        "Details": "Details",
        "Test": "Test",
        "Organize Button": "Organize Button",
        "Search Button": "Search Button",
        "Item Reset": "Item Reset",
        "Move Cursor Up": "Move Cursor Up",
        "Move Cursor Down": "Move Cursor Down",
        "Move Cursor Left": "Move Cursor Left",
        "Move Cursor Right": "Move Cursor Right",
        "Page Feed A": "Page Feed A",
        "Page Feed B": "Page Feed B",
        "Page Feed C": "Page Feed C",
        "Page Feed D": "Page Feed D",
        "Scroll ↑": "Scroll Up",
        "Scroll ↓": "Scroll Down",
        "Member List Left": "Member List Left",
        "Member List Right": "Member List Right",
        "Member Display": "Member Display",
        "Member Display Toggle": "Member Display Toggle",
        "Hunter Navi": "Hunter Navi",
        "Circular navigation": "Circular Navigation",
        "Move Menu": "Move Menu",
        "Caplink": "Caplink",
        "Cheers": "Cheers",
        "Drink": "Drink",
        "Drunk": "Drunk",
        "Drunk Sleep (Desk)": "Drunk Sleep (Desk)",
        "Drunk Sleep (Chair)": "Drunk Sleep (Chair)",
        "Hymn": "Hymn",
        "D-Pad A・Up": "D-Pad A Up",
        "D-Pad A・Down": "D-Pad A Down",
        "D-Pad A・Left": "D-Pad A Left",
        "D-Pad A・Right": "D-Pad A Right",
        "D-Pad B・Up": "D-Pad B Up",
        "D-Pad B・Down": "D-Pad B Down",
        "D-Pad B・Left": "D-Pad B Left",
        "D-Pad B・Right": "D-Pad B Right",
        "Special Button A": "Special Button A",
        "Special Button B": "Special Button B",
        
        # Chat (Category 16)
        "Chat Mode": "Chat Mode",
        "Cursor ↑": "Cursor Up",
        "Cursor ↓": "Cursor Down",
        "Cursor ←": "Cursor Left",
        "Cursor →": "Cursor Right",
        "送信先変更モード": "Change Recipient Mode",
        "Split Tab": "Split Tab",
        "Tab Switch ↓": "Tab Switch Down",
        "Switch Mode →": "Switch Mode Right",
        "Switch Mode ←": "Switch Mode Left",
        "Palette Switch": "Palette Switch",
        "Edit Shoutouts": "Edit Shoutouts",
        "送受信選択": "Send/Receive Select",
        "Confirm 2": "Confirm 2",
        
        # Gallery (Category 17)
        "ヘルプ表示": "Help Display",
        "操作モード切替": "Operation Mode Switch",
        "３Ｄ操作モード": "3D Operation Mode",
        "家具操作": "Furniture Operation",
        "Menu": "Menu",
        "Acceleration": "Acceleration",
        "Camera ↑": "Camera Up",
        "Camera ↓": "Camera Down",
        "Camera ←": "Camera Left",
        "Camera →": "Camera Right",
        "L Stick ↑": "L Stick Up",
        "L Stick ↓": "L Stick Down",
        "L Stick ←": "L Stick Left",
        "L Stick →": "L Stick Right",
        "R Stick ↑": "R Stick Up",
        "R Stick ↓": "R Stick Down",
        "R Stick ←": "R Stick Left",
        "R Stick →": "R Stick Right",
        
        # Clan Message (Category 18)
        "Switch Board": "Switch Board",
        "Next": "Next",
        "Back": "Back",
        "Edit": "Edit",
        "New Post": "New Post",
        "Personal Mail": "Personal Mail",
        "Personal Chat": "Personal Chat",
        "Delete": "Delete",
        "Fav": "Fav",
        "Help": "Help",
        
        # Nyarendo (Category 19)
        "Pad X": "Pad X",
        "Pad Y": "Pad Y",
        "Pad R1": "Pad R1",
        "Pad A": "Pad A",
        "Pad B": "Pad B",
        "Pad L1": "Pad L1",
        
        # Convenience Functions (Category 20)
        "PCと会話": "Talk to PC",
    }
    
    def translate_action_name(japanese_name):
        """Convert Japanese action name to English for display"""
        if japanese_name in ACTION_TRANSLATIONS:
            return ACTION_TRANSLATIONS[japanese_name]
        return japanese_name
        
    def translate_category_name(japanese_name):
        """Convert Japanese category name to English for display"""
        if japanese_name in CATEGORY_TRANSLATIONS:
            return CATEGORY_TRANSLATIONS[japanese_name]
        return japanese_name    
    
    class MHFControllerRemapper:
        def __init__(self, root):
            self.root = root
            self.root.title("MHF Controller Remapper - English Display")
            self.root.geometry("1200x700")
            
            self.config_path = None
            self.raw_content = None
            self.controller_assignments = {}
            self.categories = {}
            self.actions = {}
            self.current_category_id = None
            self.changed_actions = set()  # Track which actions were modified
            
            self.create_widgets()
            self.check_last_config()
        
        def create_widgets(self):
            # Main container
            main_frame = ttk.Frame(self.root, padding="10")
            main_frame.pack(fill=tk.BOTH, expand=True)
            
            # Top frame - File controls
            top_frame = ttk.LabelFrame(main_frame, text="Configuration", padding="10")
            top_frame.pack(fill=tk.X, pady=(0,10))
            
            self.file_var = tk.StringVar()
            ttk.Entry(top_frame, textvariable=self.file_var, width=80).pack(side=tk.LEFT, padx=(0,5))
            ttk.Button(top_frame, text="Load Config", command=self.select_file).pack(side=tk.LEFT, padx=2)
            ttk.Button(top_frame, text="Reload", command=self.reload_config).pack(side=tk.LEFT, padx=2)
            ttk.Button(top_frame, text="Save Changes", command=self.save_config).pack(side=tk.LEFT, padx=2)
            
            # Middle frame - Category selection and button info
            middle_frame = ttk.Frame(main_frame)
            middle_frame.pack(fill=tk.X, pady=(0,10))
            
            # Category selection
            cat_frame = ttk.LabelFrame(middle_frame, text="Select Category", padding="10")
            cat_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0,5))
            
            self.category_var = tk.StringVar()
            self.category_combo = ttk.Combobox(cat_frame, textvariable=self.category_var, 
                                                state="readonly", width=50)
            self.category_combo.pack(fill=tk.X)
            self.category_combo.bind('<<ComboboxSelected>>', self.on_category_selected)
            
            # Button info display
            info_frame = ttk.LabelFrame(middle_frame, text="Available Buttons (from config)", padding="10")
            info_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5,0))
            
            self.button_info_text = tk.Text(info_frame, height=6, width=40, wrap=tk.WORD)
            self.button_info_text.pack(fill=tk.BOTH, expand=True)
            
            # Main content - Scrollable grid of actions
            actions_frame = ttk.LabelFrame(main_frame, text="Action Bindings (English Display)", padding="10")
            actions_frame.pack(fill=tk.BOTH, expand=True)
            
            # Canvas and scrollbar for scrolling grid
            canvas = tk.Canvas(actions_frame)
            scrollbar = ttk.Scrollbar(actions_frame, orient="vertical", command=canvas.yview)
            self.scrollable_frame = ttk.Frame(canvas)
            
            self.scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
            canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
            # Store dropdown widgets
            self.action_widgets = {}
            
            # Mouse wheel scrolling
            def _on_mousewheel(event):
                canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            canvas.bind_all("<MouseWheel>", _on_mousewheel)
            
            # Status bar
            self.status_var = tk.StringVar()
            self.status_var.set("Ready - Load a keyconfig.cfg file")
            status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
            status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        def parse_config_with_regex(self, content):
            """Parse the config file using regex instead of XML parser"""
            result = {
                'controller': {},
                'categories': {},
                'actions': {}
            }
            
            # Parse controller attributes
            controller_pattern = r'<controller\s+([^>]+)>'
            controller_match = re.search(controller_pattern, content)
            if controller_match:
                attrs_str = controller_match.group(1)
                button_attrs = ['ASSIGN_DLU', 'ASSIGN_DLD', 'ASSIGN_DLL', 'ASSIGN_DLR',
                               'ASSIGN_DRU', 'ASSIGN_DRL', 'ASSIGN_DRR', 'ASSIGN_DRD',
                               'ASSIGN_LC', 'ASSIGN_RC', 'ASSIGN_L1', 'ASSIGN_R1',
                               'ASSIGN_L2', 'ASSIGN_R2', 'ASSIGN_L3', 'ASSIGN_R3']
                
                button_names = {
                    'ASSIGN_DLU': 'DPAD Up', 'ASSIGN_DLD': 'DPAD Down', 
                    'ASSIGN_DLL': 'DPAD Left', 'ASSIGN_DLR': 'DPAD Right',
                    'ASSIGN_DRU': 'Y Button', 'ASSIGN_DRL': 'X Button',
                    'ASSIGN_DRR': 'B Button', 'ASSIGN_DRD': 'A Button',
                    'ASSIGN_LC': 'Select', 'ASSIGN_RC': 'Start',
                    'ASSIGN_L1': 'LB', 'ASSIGN_R1': 'RB',
                    'ASSIGN_L2': 'LT', 'ASSIGN_R2': 'RT',
                    'ASSIGN_L3': 'LS Button', 'ASSIGN_R3': 'RS Button'
                }
                
                for attr in button_attrs:
                    pattern = rf'{attr}="([^"]+)"'
                    match = re.search(pattern, attrs_str)
                    if match:
                        hex_val = match.group(1)
                        if hex_val and hex_val != '0x00000000':
                            result['controller'][button_names.get(attr, attr)] = hex_val
            
            # Parse categories
            category_pattern = r'<category id="(\d+)" name="([^"]+)">(.*?)</category>'
            for cat_match in re.finditer(category_pattern, content, re.DOTALL):
                cat_id = cat_match.group(1)
                cat_name = cat_match.group(2)
                cat_content = cat_match.group(3)
                
                result['categories'][cat_id] = cat_name
                result['actions'][cat_id] = {}
                
                # Parse actions within this category
                action_pattern = r'<action id="(\d+)" name="([^"]+)">(.*?)</action>'
                for act_match in re.finditer(action_pattern, cat_content, re.DOTALL):
                    action_id = act_match.group(1)
                    action_name = act_match.group(2)
                    action_content = act_match.group(3)
                    
                    # Parse keydata
                    key_pattern = r'<keydata key="([^"]+)" subkey="([^"]+)"'
                    key_match = re.search(key_pattern, action_content)
                    
                    if key_match:
                        key_hex = key_match.group(1)
                        subkey_hex = key_match.group(2)
                    else:
                        key_pattern2 = r'<keydata key="([^"]+)"'
                        key_match2 = re.search(key_pattern2, action_content)
                        key_hex = key_match2.group(1) if key_match2 else '0x00000000'
                        subkey_hex = '0x00000000'
                    
                    result['actions'][cat_id][action_id] = {
                        'name': action_name,  # Keep original Japanese for saving
                        'display_name': translate_action_name(action_name),  # English for UI
                        'key': key_hex,
                        'subkey': subkey_hex,
                        'original_key': key_hex,  # Store original for comparison
                        'original_subkey': subkey_hex,
                        'raw_action': action_content
                    }
            
            return result
        
        def hex_add(self, hex1, hex2):
            """Add two hex values and return hex string"""
            val1 = int(hex1, 16) if hex1 != '0x00000000' else 0
            val2 = int(hex2, 16) if hex2 != '0x00000000' else 0
            result = val1 + val2
            return f"0x{result:08X}"
        
        def get_binding_display(self, key_hex, subkey_hex):
            """Get readable display for a binding"""
            if key_hex == '0x00000000' and subkey_hex == '0x00000000':
                return "Not Bound"
            
            key_buttons = self.hex_to_buttons(key_hex)
            
            if subkey_hex and subkey_hex != '0x00000000':
                sub_buttons = self.hex_to_buttons(subkey_hex)
                return f"{'+'.join(key_buttons)} + {'+'.join(sub_buttons)}"
            else:
                return '+'.join(key_buttons) if key_buttons else "Unknown"
        
        def hex_to_buttons(self, hex_value):
            """Convert hex value to list of button names"""
            if hex_value == '0x00000000':
                return []
            
            target = int(hex_value, 16)
            buttons_found = []
            remaining = target
            
            sorted_buttons = sorted(self.controller_assignments.items(), 
                                   key=lambda x: int(x[1], 16), reverse=True)
            
            for button_name, button_hex in sorted_buttons:
                button_val = int(button_hex, 16)
                if button_val > 0 and (remaining & button_val) == button_val:
                    buttons_found.append(button_name)
                    remaining -= button_val
            
            return buttons_found if remaining == 0 else [f"0x{target:08X}"]
        
        def get_hex_options(self):
            """Generate all possible hex options for dropdowns"""
            options = [("None", "0x00000000")]
            
            for button_name, hex_val in sorted(self.controller_assignments.items()):
                options.append((button_name, hex_val))
            
            # Generate combinations
            button_list = list(self.controller_assignments.items())
            for i, (name1, hex1) in enumerate(button_list):
                for name2, hex2 in button_list[i+1:]:
                    combo_name = f"{name1}+{name2}"
                    combo_hex = self.hex_add(hex1, hex2)
                    options.append((combo_name, combo_hex))
            
            # Remove duplicates
            seen = set()
            unique_options = []
            for name, hex_val in options:
                if hex_val not in seen:
                    seen.add(hex_val)
                    unique_options.append((name, hex_val))
            
            return unique_options
        
        def on_category_selected(self, event=None):
            """Populate the action grid with English names"""
            for widget in self.scrollable_frame.winfo_children():
                widget.destroy()
            self.action_widgets.clear()
            
            selected = self.category_var.get()
            if not selected:
                return
            
            match = re.search(r'ID: (\d+) - (.+)', selected)
            if not match:
                return
            
            cat_id = match.group(1)
            self.current_category_id = cat_id
            
            if cat_id not in self.actions:
                return
            
            # Header
            header_frame = ttk.Frame(self.scrollable_frame)
            header_frame.pack(fill=tk.X, pady=(0,5))
            
            ttk.Label(header_frame, text="ID", width=6, anchor=tk.CENTER, 
                     font=('Arial', 9, 'bold')).pack(side=tk.LEFT, padx=2)
            ttk.Label(header_frame, text="Action Name (English)", width=35, anchor=tk.W, 
                     font=('Arial', 9, 'bold')).pack(side=tk.LEFT, padx=2)
            ttk.Label(header_frame, text="Primary Button", width=18, anchor=tk.CENTER, 
                     font=('Arial', 9, 'bold')).pack(side=tk.LEFT, padx=2)
            ttk.Label(header_frame, text="Secondary Button", width=18, anchor=tk.CENTER, 
                     font=('Arial', 9, 'bold')).pack(side=tk.LEFT, padx=2)
            ttk.Label(header_frame, text="Current Binding", width=30, anchor=tk.CENTER, 
                     font=('Arial', 9, 'bold')).pack(side=tk.LEFT, padx=2)
            
            ttk.Separator(self.scrollable_frame, orient='horizontal').pack(fill=tk.X, pady=5)
            
            options = self.get_hex_options()
            option_display = [opt[0] for opt in options]
            
            for action_id, action_data in sorted(self.actions[cat_id].items(), key=lambda x: int(x[0])):
                frame = ttk.Frame(self.scrollable_frame)
                frame.pack(fill=tk.X, pady=2)
                
                ttk.Label(frame, text=action_id, width=6, anchor=tk.CENTER).pack(side=tk.LEFT, padx=2)
                
                # Show English name (or Japanese if no translation)
                display_name = action_data['display_name']
                ttk.Label(frame, text=display_name, width=35, anchor=tk.W).pack(side=tk.LEFT, padx=2)
                
                key_var = tk.StringVar()
                key_combo = ttk.Combobox(frame, textvariable=key_var, values=option_display, 
                                         state="readonly", width=16)
                key_combo.pack(side=tk.LEFT, padx=2)
                
                subkey_var = tk.StringVar()
                subkey_combo = ttk.Combobox(frame, textvariable=subkey_var, values=option_display,
                                           state="readonly", width=16)
                subkey_combo.pack(side=tk.LEFT, padx=2)
                
                current_display = self.get_binding_display(action_data['key'], action_data['subkey'])
                current_label = ttk.Label(frame, text=current_display, width=30, anchor=tk.W, foreground='blue')
                current_label.pack(side=tk.LEFT, padx=2)
                
                # Set current values
                for display, hex_val in options:
                    if hex_val == action_data['key']:
                        key_combo.set(display)
                    if hex_val == action_data['subkey']:
                        subkey_combo.set(display)
                
                self.action_widgets[action_id] = {
                    'key_combo': key_combo,
                    'subkey_combo': subkey_combo,
                    'current_label': current_label,
                    'action_data': action_data
                }
                
                key_combo.bind('<<ComboboxSelected>>', 
                              lambda e, aid=action_id, kc=key_combo, skc=subkey_combo, cl=current_label, ad=action_data: 
                              self.on_binding_changed(aid, kc, skc, cl, ad))
                subkey_combo.bind('<<ComboboxSelected>>', 
                                 lambda e, aid=action_id, kc=key_combo, skc=subkey_combo, cl=current_label, ad=action_data:
                                 self.on_binding_changed(aid, kc, skc, cl, ad))
        
        def on_binding_changed(self, action_id, key_combo, subkey_combo, current_label, action_data):
            """Handle binding changes"""
            key_display = key_combo.get()
            subkey_display = subkey_combo.get()
            
            key_hex = self.get_hex_from_display(key_display)
            subkey_hex = self.get_hex_from_display(subkey_display)
            
            # Check if the value actually changed from original
            if key_hex != action_data['original_key'] or subkey_hex != action_data['original_subkey']:
                action_data['key'] = key_hex
                action_data['subkey'] = subkey_hex
                # Track this action as changed
                self.changed_actions.add(f"{self.current_category_id}_{action_id}")
                
                new_display = self.get_binding_display(key_hex, subkey_hex)
                current_label.config(text=new_display)
                
                self.status_var.set(f"Updated: {action_data['display_name']} → {new_display}")
            else:
                # Reverted back to original
                if f"{self.current_category_id}_{action_id}" in self.changed_actions:
                    self.changed_actions.remove(f"{self.current_category_id}_{action_id}")
                self.status_var.set(f"Reverted: {action_data['display_name']} back to original")
        
        def get_hex_from_display(self, display_text):
            """Get hex value from display text"""
            if display_text == "None":
                return "0x00000000"
            
            if display_text in self.controller_assignments:
                return self.controller_assignments[display_text]
            
            if '+' in display_text:
                parts = display_text.split('+')
                total = "0x00000000"
                for part in parts:
                    part = part.strip()
                    if part in self.controller_assignments:
                        total = self.hex_add(total, self.controller_assignments[part])
                return total
            
            return "0x00000000"
        
        def display_button_info(self):
            """Display available buttons"""
            self.button_info_text.delete(1.0, tk.END)
            
            if not self.controller_assignments:
                self.button_info_text.insert(1.0, "No controller buttons found.")
                return
            
            self.button_info_text.insert(1.0, "Controller Buttons:\n")
            self.button_info_text.insert(1.0, "─" * 40 + "\n")
            
            for button_name, hex_val in sorted(self.controller_assignments.items()):
                self.button_info_text.insert(tk.END, f"{button_name:15} → {hex_val}\n")
        
        def select_file(self):
            file_path = filedialog.askopenfilename(
                title="Select keyconfig.cfg",
                filetypes=[("Config files", "*.cfg"), ("All files", "*.*")]
            )
            if file_path:
                self.config_path = file_path
                self.file_var.set(file_path)
                self.load_config()
                self.save_last_config()
        
        def check_last_config(self):
            """Load the previously used config file path"""
            last_config_file = "keycfgbak.cfg"
            if os.path.exists(last_config_file):
                try:
                    with open(last_config_file, 'r') as f:
                        last_path = f.read().strip()
                        if os.path.exists(last_path):
                            self.config_path = last_path
                            self.file_var.set(last_path)
                            self.load_config()
                except:
                    pass
        
        def save_last_config(self):
            """Save the current config path to keycfgbak.cfg"""
            if self.config_path:
                try:
                    with open("keycfgbak.cfg", 'w') as f:
                        f.write(self.config_path)
                except:
                    pass
        
        def load_config(self):
            if not self.config_path or not os.path.exists(self.config_path):
                self.status_var.set("Error: Config file not found")
                return
            
            try:
                # Read the file as Shift-JIS
                with open(self.config_path, 'rb') as f:
                    raw_bytes = f.read()
                
                try:
                    content = raw_bytes.decode('shift_jis')
                except:
                    content = raw_bytes.decode('shift_jis', errors='ignore')
                
                self.raw_content = content
                self.changed_actions.clear()  # Reset changed actions on load
                
                # Parse using regex
                parsed = self.parse_config_with_regex(content)
                
                self.controller_assignments = parsed['controller']
                self.categories = parsed['categories']
                self.actions = parsed['actions']
                
                self.display_button_info()
                
                # Update category dropdown with translated names
                category_list = [f"ID: {cid} - {translate_category_name(name)}" for cid, name in sorted(self.categories.items(), key=lambda x: int(x[0]))]
                self.category_combo['values'] = category_list
                
                if category_list:
                    self.category_combo.current(0)
                    self.on_category_selected()
                
                self.status_var.set(f"Loaded: {os.path.basename(self.config_path)} - {len(self.categories)} categories")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load config:\n{str(e)}")
                self.status_var.set(f"Error: {str(e)}")
        
        def reload_config(self):
            if self.config_path:
                self.load_config()
                messagebox.showinfo("Reloaded", "Configuration reloaded successfully")
            else:
                messagebox.showwarning("No File", "Please select a config file first")
        
        def save_config(self):
            if not self.config_path or not self.raw_content:
                messagebox.showwarning("No Config", "Please load a config file first")
                return
            
            if not self.changed_actions:
                messagebox.showinfo("No Changes", "No binding changes to save.")
                return
            
            try:
                # Create backup with timestamp
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                backup_path = f"{self.config_path}.backup_{timestamp}"
                shutil.copy2(self.config_path, backup_path)
                
                # Start with original content
                modified_content = self.raw_content
                changes_made = 0
                
                # Only update actions that were actually changed
                for changed_key in self.changed_actions:
                    parts = changed_key.split('_')
                    if len(parts) != 2:
                        continue
                    cat_id, action_id = parts
                    
                    if cat_id not in self.actions:
                        continue
                    if action_id not in self.actions[cat_id]:
                        continue
                    
                    action_data = self.actions[cat_id][action_id]
                    
                    # Use a more precise pattern to find and replace just this action
                    # Match the action tag with its specific name
                    action_name_escaped = re.escape(action_data['name'])
                    
                    # Pattern to find the keydata line within this specific action
                    # Look for the action opening tag, then the keydata line
                    pattern = rf'(<action id="{action_id}" name="{action_name_escaped}">\s*<keydata key=")[^"]+(" subkey=")[^"]+(">)'
                    replacement = rf'\g<1>{action_data["key"]}\g<2>{action_data["subkey"]}\g<3>'
                    
                    new_content = re.sub(pattern, replacement, modified_content, count=1)
                    
                    if new_content != modified_content:
                        changes_made += 1
                        modified_content = new_content
                
                if changes_made == 0:
                    messagebox.showwarning("Save Warning", "Could not find some actions to update. The file structure may have changed.")
                    return
                
                # Save with Shift-JIS encoding (preserving original Japanese text)
                with open(self.config_path, 'wb') as f:
                    f.write(modified_content.encode('shift_jis', errors='ignore'))
                
                # After successful save, update raw_content and clear changed actions
                self.raw_content = modified_content
                
                # Update original values in actions to match saved state
                for changed_key in self.changed_actions:
                    parts = changed_key.split('_')
                    if len(parts) != 2:
                        continue
                    cat_id, action_id = parts
                    if cat_id in self.actions and action_id in self.actions[cat_id]:
                        self.actions[cat_id][action_id]['original_key'] = self.actions[cat_id][action_id]['key']
                        self.actions[cat_id][action_id]['original_subkey'] = self.actions[cat_id][action_id]['subkey']
                
                self.changed_actions.clear()
                
                self.status_var.set(f"Saved! {changes_made} binding(s) updated. Backup: {os.path.basename(backup_path)}")
                messagebox.showinfo("Saved", f"Saved successfully!\n\n{changes_made} binding(s) updated.\nBackup: {backup_path}\n\nRestart the game for changes to take effect.")
                
            except Exception as e:
                messagebox.showerror("Save Error", f"Failed to save:\n{str(e)}")
                self.status_var.set("Error saving config")
    
    root = tk.Tk()
    app = MHFControllerRemapper(root)
    root.mainloop()

if __name__ == "__main__":
    main()