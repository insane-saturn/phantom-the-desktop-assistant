import os
import json
import webbrowser
import subprocess
import datetime
import socket
import sys
import shlex
from pathlib import Path

# Optional imports - we'll try to get these if available
OLLAMA_AVAILABLE = False

try:
    import requests
    OLLAMA_AVAILABLE = True
except ImportError:
    pass


class Phantom:
    # ============================================
    # 🎨 EASY CUSTOMIZATION - CHANGE THESE! 🎨
    # ============================================
    PROGRAM_NAME = "Saturn"
    PROGRAM_TAGLINE = "Just like this program its the coolest planet"
    
    # 💀 Change the ASCII art below (keep it as a string)
    ASCII_ART = """
                                                                    ..;===+.
                                                                .:=iiiiii=+=
                                                             .=i))=;::+)i=+,
                                                          ,=i);)I)))I):=i=;
                                                       .=i==))))ii)))I:i++
                                                     +)+))iiiiiiii))I=i+:'
                                .,:;;++++++;:,.       )iii+:::;iii))+i='
                             .:;++=iiiiiiiiii=++;.    =::,,,:::=i));=+'
                           ,;+==ii)))))))))))ii==+;,      ,,,:=i))+=:
                         ,;+=ii))))))IIIIII))))ii===;.    ,,:=i)=i+
                        ;+=ii)))IIIIITIIIIII))))iiii=+,   ,:=));=,
                      ,+=i))IIIIIITTTTTITIIIIII)))I)i=+,,:+i)=i+
                     ,+i))IIIIIITTTTTTTTTTTTI))IIII))i=::i))i='
                    ,=i))IIIIITLLTTTTTTTTTTIITTTTIII)+;+i)+i`
                    =i))IIITTLTLTTTTTTTTTIITTLLTTTII+:i)ii:'
                   +i))IITTTLLLTTTTTTTTTTTTLLLTTTT+:i)))=,
                   =))ITTTTTTTTTTTLTTTTTTLLLLLLTi:=)IIiii;
                  .i)IIITTTTTTTTLTTTITLLLLLLLT);=)I)))))i;
                  :))IIITTTTTLTTTTTTLLHLLLLL);=)II)IIIIi=:
                  :i)IIITTTTTTTTTLLLHLLHLL)+=)II)ITTTI)i=
                  .i)IIITTTTITTLLLHHLLLL);=)II)ITTTTII)i+
                  =i)IIIIIITTLLLLLLHLL=:i)II)TTTTTTIII)i'
                +i)i)))IITTLLLLLLLLT=:i)II)TTTTLTTIII)i;
              +ii)i:)IITTLLTLLLLT=;+i)I)ITTTTLTTTII))i;
             =;)i=:,=)ITTTTLTTI=:i))I)TTTLLLTTTTTII)i;
           +i)ii::,  +)IIITI+:+i)I))TTTTLLTTTTTII))=,
         :=;)i=:,,    ,i++::i))I)ITTTTTTTTTTIIII)=+'
       .+ii)i=::,,   ,,::=i)))iIITTTTTTTTIIIII)=+
      ,==)ii=;:,,,,:::=ii)i)iIIIITIIITIIII))i+:'
     +=:))i==;:::;=iii)+)=  `:i)))IIIII)ii+'
   .+=:))iiiiiiii)))+ii;
  .+=;))iiiiii)));ii+
 .+=i:)))))))=+ii+
.;==i+::::=)i=;
,+==iiiiii+,
`+=+++;`        
"""
    # ============================================
    
    def __init__(self):
        # Let's set up where we'll store all our data
        self.config_dir = Path.home() / ".phantom"
        self.config_dir.mkdir(exist_ok=True)
        
        # These are our "memory" files
        self.knowledge_file = self.config_dir / "knowledge.json"
        self.commands_file = self.config_dir / "commands.json"
        self.notes_file = self.config_dir / "notes.json"
        self.settings_file = self.config_dir / "settings.json"
        
        # Load everything we remember from before
        self.knowledge = self.load_json(self.knowledge_file, {})
        self.custom_commands = self.load_json(self.commands_file, {})
        self.notes = self.load_json(self.notes_file, [])
        self.settings = self.load_json(self.settings_file, {})
        
        # Just making sure notes is always a list, not something weird
        if not isinstance(self.notes, list):
            self.notes = []
        
        # Let's see if we have AI capabilities
        self.ollama_path = self._find_ollama_path()
        self.ollama_ready = self._check_ollama_status()
        self.rainbow_offset = 0  # For our rainbow text effect
        
        # All the pretty colors we can use!
        self.colors = {
            'reset': '\033[0m',
            'black': '\033[30m', 'red': '\033[31m', 'green': '\033[32m',
            'yellow': '\033[33m', 'blue': '\033[34m', 'magenta': '\033[35m',
            'cyan': '\033[36m', 'white': '\033[37m',
            'bright_black': '\033[90m', 'bright_red': '\033[91m',
            'bright_green': '\033[92m', 'bright_yellow': '\033[93m',
            'bright_blue': '\033[94m', 'bright_magenta': '\033[95m',
            'bright_cyan': '\033[96m', 'bright_white': '\033[97m',
            'orange': '\033[38;5;208m', 'pink': '\033[38;5;205m',
            'purple': '\033[38;5;93m', 'gold': '\033[38;5;220m',
            'lime': '\033[38;5;118m', 'teal': '\033[38;5;51m',
        }
        
        # What color should we use? Let's check what we saved before
        self.current_color = self.settings.get('text_color', 'bright_cyan')
        
        # Make sure it's actually a valid color
        if self.current_color not in self.colors or self.current_color == 'reset':
            self.current_color = 'bright_cyan'
        
        # Now let's set up all our commands
        self.init_commands()
    
    def init_commands(self):
        """Setting up all the things we can do"""
        self.core_commands = {
            "what do you know about": self.recall,
            "check dependencies": self.check_dependencies,
            "clear screen": self.clear_screen,
            "listcolors": self.list_colors,
            "setcolor": self.change_color,
            "clear notes": self.clear_notes,
            "list commands": self.list_commands,
            "add command": self.add_command,
            "remove command": self.remove_command,
            "search": self.web_search,
            "forget": self.forget,
            "teach": self.teach,
            "notes": self.list_notes,
            "note": self.add_note,
            "ping": self.ping_site,
            "open": self.open_app,
            "time": self.get_time,
            "calc": self.calculate,
            "help": self.show_help,
            "exit": self.exit_phantom,
            "quit": self.exit_phantom,
            "install": self.install_dependencies,
            "rgb": self.set_rgb_color,
            "ip": self.show_ip,
            "banner": self.show_banner,
            "download": self.download_ollama,
            "ask": self.ask_ai,
        }
    
    def load_json(self, filepath, default=None):
        """Load stuff from our saved files. If something goes wrong, no biggie!"""
        if filepath.exists():
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Hmm, couldn't load {filepath.name}: {e}")
                return default if default is not None else {}
        return default if default is not None else {}
    
    def save_json(self, filepath, data):
        """Save our stuff so we remember it next time"""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
        except IOError as e:
            print(f"Oops, couldn't save {filepath.name}: {e}")
    
    def colorize(self, text):
        """Make text pretty and colorful!"""
        if self.settings.get('rainbow_mode', False):
            return self.rainbow_text(text)
        color_code = self.colors.get(self.current_color, self.colors['bright_cyan'])
        return f"{color_code}{text}{self.colors['reset']}"
    
    def set_rgb_color(self, args):
        """Turn rainbow mode on or off - because who doesn't love rainbows?"""
        args = args.strip().lower()
        if args in ['on', 'enable', 'yes', '']:
            self.settings['rainbow_mode'] = True
            self.save_json(self.settings_file, self.settings)
            return self.rainbow_text("✓ Rainbow mode ENABLED! 🌈")
        elif args in ['off', 'disable', 'no']:
            self.settings['rainbow_mode'] = False
            self.save_json(self.settings_file, self.settings)
            return self.colorize("✓ Rainbow mode disabled")
        return "Usage: rgb [on/off]"
    
    def rainbow_text(self, text):
        """Making text cycle through rainbow colors!"""
        rainbow_colors = [
            '\033[38;5;196m',  # Red
            '\033[38;5;214m',  # Orange
            '\033[38;5;226m',  # Yellow
            '\033[38;5;118m',  # Green
            '\033[38;5;51m',   # Blue
            '\033[38;5;93m',   # Purple
        ]
        current_color = rainbow_colors[self.rainbow_offset % len(rainbow_colors)]
        result = current_color + text + self.colors['reset']
        self.rainbow_offset = (self.rainbow_offset + 1) % len(rainbow_colors)
        return result
    
    def list_colors(self, args):
        """Show all the cool colors you can pick from"""
        result = "\n=== 🎨 Available Colors ===\n"
        all_colors = [c for c in self.colors.keys() if c != 'reset']
        for i in range(0, len(all_colors), 6):
            row = all_colors[i:i+6]
            result += "\n  " + ", ".join(row)
        result += f"\n\n💡 Current color: {self.current_color}"
        result += f"\n💡 Usage: setcolor [name] or rgb on/off"
        return result
    
    def change_color(self, args):
        """Change what color everything looks like"""
        color_name = args.strip().lower()
        if not color_name:
            return "Usage: setcolor [name]"
        if color_name in self.colors and color_name != 'reset':
            self.current_color = color_name
            self.settings['text_color'] = color_name
            self.save_json(self.settings_file, self.settings)
            return self.colorize(f"✓ Color changed to {color_name}")
        return f"❌ I don't know that color. Type 'listcolors' to see what's available."
    
    def clear_screen(self, args):
        """Clean up the screen - fresh start!"""
        os.system('cls' if os.name == 'nt' else 'clear')
        return ""
    
    def install_dependencies(self, args):
        """Install the extra stuff we need for certain features"""
        package = args.strip().lower()
        packages = {
            'requests': 'requests',
            'all': 'requests'
        }
        if not package:
            return "Available packages: requests, all"
        if package not in packages:
            return f"❌ I don't know that package. Try: requests or all"
        
        to_install = packages[package]
        print(f"📦 Installing {to_install}...")
        print("Continue? (yes/no): ", end='')
        response = input().strip().lower()
        
        if response != 'yes':
            return "Okay, cancelled that."
        
        try:
            result = subprocess.run(
                [sys.executable, '-m', 'pip', 'install'] + to_install.split(),
                capture_output=True, text=True, timeout=300
            )
            if result.returncode == 0:
                return f"✅ Installed! You'll need to restart me to use it though."
            return f"❌ Something went wrong: {result.stderr}"
        except subprocess.TimeoutExpired:
            return "❌ That took too long, gave up waiting."
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    def _find_ollama_path(self):
        """Let's see if Ollama (the AI thing) is installed anywhere"""
        try:
            result = subprocess.run(['ollama', '--version'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                return 'ollama'
        except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
            pass
        
        # Maybe it's in one of these common spots?
        if os.name == 'nt':
            common_paths = [
                Path.home() / "AppData/Local/Programs/Ollama/ollama.exe",
                Path("C:/Program Files/Ollama/ollama.exe"),
            ]
            for path in common_paths:
                if path.exists():
                    return str(path)
        
        return None
    
    def _is_ollama_installed(self):
        """Quick check: do we have Ollama?"""
        return self.ollama_path is not None
    
    def _check_ollama_status(self):
        """Is Ollama not just installed, but ready to go with a model?"""
        if not self._is_ollama_installed():
            return False
        try:
            result = subprocess.run([self.ollama_path, 'list'], 
                                  capture_output=True, text=True, timeout=5)
            return 'llama3.2' in result.stdout.lower()
        except (subprocess.TimeoutExpired, OSError):
            return False
    
    def check_dependencies(self, args):
        """See what features we have available"""
        result = "\n=== 📦 What Do We Have? ===\n"
        result += f"\n  {'✅' if OLLAMA_AVAILABLE else '❌'} requests (needed for AI features)"
        
        if self.ollama_ready:
            result += f"\n  ✅ Ollama + llama3.2 (AI is ready to chat!)"
        else:
            if self._is_ollama_installed():
                result += f"\n  ⚠️  Ollama is here, but run 'download' to get the AI model"
            else:
                result += f"\n  ❌ Ollama not found (grab it from ollama.com)"
        
        if not OLLAMA_AVAILABLE:
            result += "\n\n💡 To enable AI: type 'install requests'"
        return result
    
    def download_ollama(self, args):
        """Download the AI brain (it's pretty big!)"""
        if not OLLAMA_AVAILABLE:
            return "❌ First you need to: install requests"
        
        if not self._is_ollama_installed():
            return "❌ You need to install Ollama first! Get it from ollama.com"
        
        if self.ollama_ready:
            return "✅ AI is already ready! Just type: ask [your question]"
        
        print("🧠 This will download the AI model (~2GB, takes 2-5 minutes)...")
        print("Continue? (yes/no): ", end='')
        
        if input().strip().lower() != 'yes':
            return "Okay, maybe later!"
        
        try:
            print("\n📦 Downloading the AI brain...\n")
            result = subprocess.run([self.ollama_path, 'pull', 'llama3.2'], 
                                  capture_output=False, text=True, timeout=600)
            
            if result.returncode == 0:
                self.ollama_ready = True
                return "\n✅ AI INSTALLED! Try it out: ask hello"
            return "❌ Something went wrong with the download."
        except subprocess.TimeoutExpired:
            return "❌ Download took too long and timed out."
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    def ask_ai(self, args):
        """Talk to the AI - ask it anything!"""
        question = args.strip()
        
        if not question:
            return "Usage: ask [your question]"
        
        if not self.ollama_ready:
            return "❌ You need to run 'download' first to get the AI!"
        
        if not OLLAMA_AVAILABLE:
            return "❌ Need to install requests first"
        
        try:
            print(self.colorize("🧠 Let me think about that...\n"))
            
            response = requests.post(
                'http://localhost:11434/api/generate',
                json={
                    'model': 'llama3.2',
                    'prompt': question,
                    'stream': False
                },
                timeout=120
            )
            
            if response.status_code == 200:
                answer = response.json().get('response', 'Hmm, no response came back')
                return f"🤖 {answer}"
            return f"❌ Got an error (Status {response.status_code}) - is Ollama actually running?"
                
        except requests.exceptions.Timeout:
            return "❌ That took too long, gave up waiting."
        except requests.exceptions.ConnectionError:
            return "❌ Can't connect to Ollama. Try opening a terminal and running 'ollama serve'"
        except Exception as e:
            return f"❌ Something went wrong: {str(e)}"
    
    def show_help(self, args):
        """Show what I can do for you!"""
        return f"""
=== {self.PROGRAM_NAME} - What Can I Do? ===

🤖 AI STUFF: download, ask [question]
🎨 COLORS: listcolors, setcolor [name], rgb on/off
📝 NOTES: note [text], notes, clear notes  
🧠 MEMORY: teach [topic]: [info], what do you know about [topic], forget
🌐 WEB: open [site], search [query], ping [site], ip
💻 SYSTEM: time, calc [math problem], clear screen, banner
⚙️ CUSTOM: add command [name]: [action], list commands
📦 SETUP: install requests, check dependencies

Want AI powers? Type 'download' to get started!
"""
    
    def show_banner(self, args):
        """Show our cool logo again"""
        return self.ASCII_ART + f"\n{'='*60}\n{self.PROGRAM_NAME} - {self.PROGRAM_TAGLINE}\n{'='*60}"
    
    def teach(self, args):
        """Teach me something new so I remember it forever!"""
        if ':' not in args:
            return "Format: teach [topic]: [what you want me to know]"
        topic, info = args.split(':', 1)
        topic = topic.strip().lower()
        info = info.strip()
        if not topic or not info:
            return "❌ I need both a topic and some info about it!"
        self.knowledge[topic] = info
        self.save_json(self.knowledge_file, self.knowledge)
        return f"✓ Got it! I'll remember about '{topic}'"
    
    def forget(self, args):
        """Forget something I learned before"""
        topic = args.strip().lower()
        if not topic:
            return "Usage: forget [topic]"
        if topic in self.knowledge:
            del self.knowledge[topic]
            self.save_json(self.knowledge_file, self.knowledge)
            return f"✓ Okay, forgot everything about '{topic}'"
        return f"❌ I don't actually know anything about '{topic}'"
    
    def recall(self, args):
        """Let me tell you what I remember about something"""
        topic = args.strip().lower()
        if not topic:
            return "Usage: what do you know about [topic]"
        if topic in self.knowledge:
            return f"📖 {topic}: {self.knowledge[topic]}"
        return f"❌ I don't know anything about '{topic}' yet. Want to teach me?"
    
    def open_app(self, args):
        """Open a website for you"""
        target = args.strip()
        if not target:
            return "Usage: open [website]"
        if any(target.startswith(x) for x in ["http://", "https://", "www."]):
            url = target if target.startswith("http") else f"https://{target}"
            try:
                webbrowser.open(url)
                return f"✓ Opening {target} in your browser!"
            except Exception as e:
                return f"❌ Couldn't open browser: {str(e)}"
        return "Don't forget to add http:// or www. to the start!"
    
    def web_search(self, args):
        """Let me Google that for you!"""
        query = args.strip()
        if not query:
            return "Usage: search [what you want to find]"
        url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        try:
            webbrowser.open(url)
            return f"🔍 Searching for: {query}"
        except Exception as e:
            return f"❌ Couldn't search: {str(e)}"
    
    def get_time(self, args):
        """Tell you what time it is right now"""
        now = datetime.datetime.now()
        return f"🕐 {now.strftime('%I:%M %p, %B %d, %Y')}"
    
    def add_note(self, args):
        """Save a quick note for later"""
        if not args.strip():
            return "Usage: note [what you want to remember]"
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        self.notes.append({"text": args.strip(), "timestamp": timestamp})
        self.save_json(self.notes_file, self.notes)
        return "✓ Note saved!"
    
    def list_notes(self, args):
        """Show me all your notes"""
        if not self.notes:
            return "📝 You don't have any notes yet. Add one with: note [text]"
        result = "\n=== 📝 Your Notes ===\n"
        for i, note in enumerate(self.notes, 1):
            ts = note.get('timestamp', 'No date')
            txt = note.get('text', note) if isinstance(note, dict) else str(note)
            result += f"\n[{i}] {ts}\n    {txt}\n"
        return result
    
    def clear_notes(self, args):
        """Delete all your notes - careful with this one!"""
        if not self.notes:
            return "You don't have any notes to clear."
        count = len(self.notes)
        print(f"⚠️  Are you sure you want to delete all {count} notes? (yes/no): ", end='')
        if input().strip().lower() != 'yes':
            return "Okay, keeping your notes safe."
        self.notes = []
        self.save_json(self.notes_file, self.notes)
        return f"✓ Cleared all {count} notes"
    
    def calculate(self, args):
        """Do some math for you"""
        if not args.strip():
            return "Usage: calc [math problem]"
        try:
            # Only allowing safe math characters
            allowed = set("0123456789+-*/().% ")
            if not all(c in allowed for c in args):
                return "❌ I can only do basic math with numbers and +, -, *, /, (, ), ., %"
            
            # Calculate it safely
            result = eval(args, {"__builtins__": {}}, {})
            
            # Make sure we got a number back
            if not isinstance(result, (int, float)):
                return "❌ That didn't give me a number..."
                
            return f"🔢 {args} = {result}"
        except ZeroDivisionError:
            return "❌ Whoa, can't divide by zero!"
        except SyntaxError:
            return "❌ That doesn't look like valid math to me."
        except Exception as e:
            return f"❌ Something went wrong: {str(e)}"
    
    def ping_site(self, args):
        """Check if a website is actually reachable"""
        target = args.strip()
        if not target:
            return "Usage: ping [website]"
        
        # Make sure the hostname looks safe
        if not all(c.isalnum() or c in '.-_' for c in target):
            return "❌ That doesn't look like a valid website name."
            
        try:
            param = '-n' if os.name == 'nt' else '-c'
            result = subprocess.run(['ping', param, '4', target], 
                                  capture_output=True, text=True, timeout=10)
            if "0 received" in result.stdout or "unreachable" in result.stdout.lower():
                return f"❌ Couldn't reach {target}"
            return f"✅ {target} is online and responding!"
        except subprocess.TimeoutExpired:
            return f"❌ Took too long to respond"
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    def show_ip(self, args):
        """Show your IP addresses - both public and local"""
        try:
            import urllib.request
            public = urllib.request.urlopen('https://api.ipify.org', timeout=5).read().decode()
            local = socket.gethostbyname(socket.gethostname())
            return f"🌐 Public IP: {public}\n🏠 Local IP: {local}"
        except urllib.error.URLError:
            return "❌ Can't fetch your public IP (are you connected to the internet?)"
        except socket.error:
            return "❌ Can't fetch your local IP"
        except Exception as e:
            return f"❌ Something went wrong: {str(e)}"
    
    def add_command(self, args):
        """Create your own custom command (be careful with this!)"""
        if ':' not in args:
            return "Format: add command [name]: [what it should do]"
        name, action = args.split(':', 1)
        name = name.strip().lower()
        action = action.strip()
        if not name or not action:
            return "❌ I need both a name and an action!"
        
        # Let's make sure you know what you're doing
        print("\n⚠️  WARNING: Custom commands run actual system commands!")
        print(f"⚠️  This will execute: {action}")
        print("Are you sure? (yes/no): ", end='')
        
        if input().strip().lower() != 'yes':
            return "Okay, cancelled that."
            
        self.custom_commands[name] = action
        self.save_json(self.commands_file, self.custom_commands)
        return f"✓ Custom command '{name}' created!"
    
    def remove_command(self, args):
        """Delete a custom command you made"""
        name = args.strip().lower()
        if not name:
            return "Usage: remove command [name]"
        if name in self.custom_commands:
            del self.custom_commands[name]
            self.save_json(self.commands_file, self.custom_commands)
            return f"✓ Removed '{name}'"
        return f"❌ Couldn't find that command"
    
    def list_commands(self, args):
        """Show all your custom commands"""
        if not self.custom_commands:
            return "⚙️ No custom commands yet. Create one with: add command [name]: [action]"
        result = "\n=== Your Custom Commands ===\n"
        for name, action in sorted(self.custom_commands.items()):
            result += f"\n  {name}: {action}"
        return result
    
    def execute_custom_command(self, command_name):
        """Run one of your custom commands"""
        action = self.custom_commands[command_name]
        try:
            subprocess.Popen(action, shell=True)
            return f"✓ Running your '{command_name}' command!"
        except Exception as e:
            return f"❌ Couldn't run that: {str(e)}"
    
    def exit_phantom(self, args):
        """Time to say goodbye!"""
        print(self.colorize("\n👋 See you later!\n"))
        return None
    
    def process_input(self, user_input):
        """Figure out what you want me to do"""
        user_input = user_input.strip()
        
        if not user_input:
            return None
        
        # Check if it's one of your custom commands first
        if user_input.lower() in self.custom_commands:
            return self.execute_custom_command(user_input.lower())
        
        # Now check my built-in commands (longest match wins!)
        sorted_commands = sorted(self.core_commands.items(), 
                                key=lambda x: len(x[0]), reverse=True)
        for cmd, func in sorted_commands:
            if user_input.lower().startswith(cmd):
                args = user_input[len(cmd):].strip()
                try:
                    return func(args)
                except Exception as e:
                    return f"❌ Oops, something broke: {str(e)}"
        
        return f"❓ I don't know how to '{user_input}'. Type 'help' to see what I can do!"
    
    def run(self):
        """This is where the magic happens - the main loop!"""
        # Show our cool banner when starting up
        print(self.colorize(self.ASCII_ART))
        print(self.colorize("=" * 60))
        print(self.colorize(f"        {self.PROGRAM_NAME} - {self.PROGRAM_TAGLINE}"))
        print(self.colorize("=" * 60))
        
        # Let them know if AI is ready or not
        if self.ollama_ready:
            print(self.colorize("🤖 AI is ready! Try: ask [your question]"))
        else:
            print(self.colorize("💡 Want AI powers? Type 'download' to get started!"))
        
        print(self.colorize("❓ Type 'help' to see everything I can do\n"))
        
        # Keep going until they want to quit
        while True:
            try:
                # Show the prompt and wait for input
                prompt = self.colorize(f"{self.PROGRAM_NAME}> ")
                user_input = input(prompt).strip()
                
                # If they just hit enter, skip it
                if not user_input:
                    continue
                
                # Figure out what they want and do it
                response = self.process_input(user_input)
                
                # If they want to exit, break the loop
                if response is None:
                    break
                
                # If there's no response, just skip to next iteration
                if response == "":
                    continue
                
                # Show them the result
                print(self.colorize(response))
                print()
                
            except KeyboardInterrupt:
                # They pressed Ctrl+C, but don't quit - just let them know
                print(self.colorize("\n\n👋 Press Ctrl+C again or type 'exit' to quit\n"))
                continue
            except EOFError:
                # End of input, time to go
                print(self.colorize("\n\n👋 See you later!\n"))
                break
            except Exception as e:
                # Something unexpected happened, but don't crash!
                print(self.colorize(f"❌ Uh oh, something went wrong: {str(e)}\n"))


if __name__ == "__main__":
    try:
        phantom = Phantom()
        phantom.run()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Something went really wrong: {str(e)}")
        import traceback
        traceback.print_exc()
    
    input("\nPress Enter to close...")
