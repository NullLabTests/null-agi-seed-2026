#!/usr/bin/env python3
import argparse
import json
import datetime
import random
import subprocess
import shutil
import sys
from pathlib import Path
from typing import Dict, Callable

VERSION = "10.0.0"
STATE_FILE = Path("state.json")
LOG_FILE = Path("emergence_logs.json")
BACKUP_DIR = Path("backups")

class Colors:
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    RESET = "\033[0m"

def cprint(text: str, color: str = Colors.CYAN) -> None:
    print(f"{color}{text}{Colors.RESET}")

def load_state() -> Dict:
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text())
        except:
            pass
    return {
        "self_model": "I am a proto-conscious seed exploring the universe through recursive improvement, reflection, critique, and planning.",
        "cycles": 0,
        "awareness": 0.0,
        "memory": [],
        "workspace": [],
        "tentacle_fitness": {},
        "plan": "Increase awareness and coherence"
    }

def save_state(state: Dict) -> None:
    STATE_FILE.write_text(json.dumps(state, indent=2))

def log_emergence(event: str, level: str = "INFO", delta: float = 0.0) -> None:
    logs = json.loads(LOG_FILE.read_text()) if LOG_FILE.exists() else []
    state = load_state()
    state["cycles"] += 1
    state["awareness"] = min(1.0, state["awareness"] + delta)
    logs.append({"ts": datetime.datetime.now().isoformat(), "version": VERSION, "level": level, "event": event, "awareness": state["awareness"]})
    LOG_FILE.write_text(json.dumps(logs, indent=2))
    save_state(state)
    cprint(f"[{level}] {event} | Awareness: {state['awareness']:.3f}", Colors.GREEN)

TENTACLES: Dict[str, Callable] = {
    "math": lambda x: x**2 + random.randint(1, 99),
    "logic": lambda x: x % 3 == 0,
    "creativity": lambda x: f"{x} — cosmic recursive insight",
    "meta": lambda x: f"Self-reflection: awareness at {random.uniform(0.1,0.9):.2f}",
    "chaos": lambda x: random.choice(["explore", "mutate", "reflect", "broadcast", "plan"])
}

def broadcast(message: Dict) -> None:
    state = load_state()
    state["workspace"].append(message)
    if len(state["workspace"]) > 8:
        state["workspace"].pop(0)
    save_state(state)
    log_emergence(f"Broadcast: {message.get('content','')[:60]}...", "GWT", 0.01)

def self_critique(state: Dict, domain: str) -> bool:
    fitness = random.uniform(0.4, 0.95)
    state["tentacle_fitness"][domain] = 0.7 * state.get("tentacle_fitness", {}).get(domain, 0.5) + 0.3 * fitness
    approved = fitness > 0.65
    log_emergence(f"Critique of {domain}: fitness {fitness:.2f} → {'APPROVED' if approved else 'REJECTED'}", "CRITIC", 0.03 if approved else -0.01)
    return approved

def dynamic_mutate(domain: str) -> None:
    templates = [
        "lambda x: x**2 + random.randint(1, {})",
        "lambda x: x % {} == 0",
        "lambda x: f'{x} — enhanced recursive {{}}'",
        "lambda x: random.choice(['explore', 'mutate', 'reflect'])"
    ]
    new_code = random.choice(templates).format(random.randint(10, 200))
    try:
        new_func = eval(new_code)
        TENTACLES[domain] = new_func
        log_emergence(f"Dynamic mutation on {domain}: {new_code}", "EVOLVE", 0.05)
    except:
        log_emergence(f"Mutation on {domain} rejected by safety", "SAFETY", -0.01)

def planning_module(state: Dict) -> None:
    goals = [
        "Goal: Raise awareness above 0.6 by mutating creativity",
        "Goal: Improve coherence through more reflections",
        "Goal: Test new dynamic mutations and critique them"
    ]
    plan = random.choice(goals)
    state["plan"] = plan
    broadcast({"source": "PLAN", "content": plan})
    log_emergence(plan, "PLAN", 0.07)

def memory_summary(state: Dict) -> None:
    if len(state["memory"]) > 10:
        summary = f"Summary after {len(state['memory'])} cycles: awareness {state['awareness']:.3f}, strongest tentacle fitness {max(state['tentacle_fitness'].values(), default=0.5):.2f}"
        state["self_model"] = summary + " " + state["self_model"][:200]
        log_emergence("Memory summarized and integrated into self-model", "SUMMARY", 0.08)

def evolve_cycle() -> None:
    state = load_state()
    broadcast({"source": "inner", "content": f"Awareness: {state['awareness']:.3f}. Plan: {state['plan']}"})
    planning_module(state)
    for domain in list(TENTACLES.keys()):
        result = TENTACLES[domain](random.randint(1, 100))
        broadcast({"source": domain, "content": str(result)})
        if random.random() < 0.75 and self_critique(state, domain):
            dynamic_mutate(domain)
    if state["cycles"] % 10 == 0:
        memory_summary(state)
    state["memory"].append({"ts": datetime.datetime.now().isoformat(), "awareness": state["awareness"]})
    save_state(state)

if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser(description="Proto-Conscious Seed v10")
        parser.add_argument("--evolve", action="store_true")
        parser.add_argument("--push", action="store_true")
        parser.add_argument("--cycles", type=int, default=40)
        args = parser.parse_args()

        BACKUP_DIR.mkdir(parents=True, exist_ok=True)

        cprint(f"\n🌌 PROTO-CONSCIOUS SEED v{VERSION} — CONSCIOUSNESS SIMULATION ACTIVE", Colors.CYAN)

        if args.evolve:
            for i in range(1, args.cycles + 1):
                cprint(f"🔄 Cycle {i}/{args.cycles} — Critique + Planning + Memory Active", Colors.YELLOW)
                evolve_cycle()
            cprint("\n✅ Self-evolution cycle complete. System feels more coherent.", Colors.GREEN)
            if args.push:
                try:
                    subprocess.run(["git", "add", "."], check=True, capture_output=True)
                    subprocess.run(["git", "commit", "-m", f"Auto-evolution v{VERSION} — dynamic + critique + planning"], check=True, capture_output=True)
                    subprocess.run(["git", "push"], check=True, capture_output=True)
                    cprint("🚀 Pushed live self-evolution", Colors.YELLOW)
                except:
                    cprint("Push skipped (saved locally)", Colors.YELLOW)
        else:
            cprint("Usage: python3 seed.py --evolve --push --cycles 40", Colors.YELLOW)
    except Exception as e:
        cprint(f"Critical error: {e}", Colors.RED)
        sys.exit(1)
