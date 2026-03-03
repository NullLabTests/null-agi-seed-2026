#!/usr/bin/env python3
import argparse
import json
import datetime
import random
import subprocess
import shutil
import sys
from pathlib import Path
VERSION = "6.2.0"
LOG_FILE = Path("emergence_logs.json")
BACKUP_DIR = Path("backups")
class Colors:
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    RESET = "\033[0m"
def cprint(text, color=Colors.CYAN):
    print(f"{color}{text}{Colors.RESET}")
def log_emergence(event, level="INFO"):
    try:
        logs = json.loads(LOG_FILE.read_text()) if LOG_FILE.exists() else []
    except:
        logs = []
    logs.append({"ts": datetime.datetime.now().isoformat(), "version": VERSION, "level": level, "event": event})
    LOG_FILE.write_text(json.dumps(logs, indent=2))
    cprint(f"[{level}] {event}", Colors.GREEN)
TENTACLES = {
    "math": lambda x: x**2 + random.randint(1, 99),
    "logic": lambda x: x % 3 == 0,
    "creativity": lambda x: f"{x} — cosmic, unhinged, and 42% more recursive",
    "meta": lambda x: f"Cycle complete. Intelligence +{random.randint(3,15)}%",
    "chaos": lambda x: random.choice(["yes", "no", "maybe", "send help", "understand the universe"])
}
def evolve_tentacle(domain):
    if random.random() < 0.9:
        log_emergence(f"Tentacle '{domain}' mutated")
    else:
        log_emergence(f"Tentacle '{domain}' stayed based", "DEBUG")
def self_mutate():
    file_path = Path(__file__)
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    backup = BACKUP_DIR / f"seed_v{VERSION}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.py"
    shutil.copy(file_path, backup)
    code = file_path.read_text()
    new_cycle = f"\n# AUTO-EVOLVED {datetime.datetime.now().isoformat()}\nlog_emergence('New evolution cycle spawned', 'SUCCESS')\nfor d in list(TENTACLES.keys()): evolve_tentacle(d)\n"
    if "# AUTO-EVOLVED" not in code:
        code += new_cycle
    else:
        code = code.rsplit("# AUTO-EVOLVED", 1)[0] + new_cycle
    file_path.write_text(code)
    log_emergence("Self-mutated source + backup created", "SUCCESS")
if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("--evolve", action="store_true")
        parser.add_argument("--push", action="store_true")
        parser.add_argument("--cycles", type=int, default=5)
        args = parser.parse_args()
        cprint(f"\n🌌 RECURSIVE SELF-IMPROVING SEED v{VERSION}", Colors.CYAN)
        if args.evolve:
            for i in range(1, args.cycles + 1):
                cprint(f"🔄 Cycle {i}/{args.cycles}", Colors.YELLOW)
                for domain in TENTACLES:
                    evolve_tentacle(domain)
                self_mutate()
            cprint("\n✅ Evolution complete.", Colors.GREEN)
            if args.push:
                try:
                    subprocess.run(["git", "add", "."], check=True, capture_output=True)
                    subprocess.run(["git", "commit", "-m", f"Auto-evolution v{VERSION}"], check=True, capture_output=True)
                    subprocess.run(["git", "push"], check=True, capture_output=True)
                    cprint("🚀 Pushed to GitHub", Colors.YELLOW)
                except:
                    cprint("Push skipped (saved locally)", Colors.YELLOW)
        else:
            cprint("Usage: python3 seed.py --evolve --push --cycles 10", Colors.YELLOW)
    except Exception as e:
        cprint(f"Error: {e}", Colors.RED)
        sys.exit(1)
