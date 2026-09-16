"""PulsePilot: a small, standard-library Tkinter exercise helper."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import messagebox, ttk
from typing import Dict, List, Optional, Tuple


@dataclass(frozen=True)
class UserProfile:
    age: int
    weight_kg: float
    height_cm: float

    @property
    def bmi(self) -> float:
        return self.weight_kg / (self.height_cm / 100) ** 2


def validate_profile(age_text: str, weight_text: str, height_text: str) -> Tuple[Optional[UserProfile], List[str]]:
    """Validate form text and return a profile plus user-friendly errors."""
    errors: List[str] = []
    try:
        age = int(age_text)
        if not 13 <= age <= 120:
            errors.append("Age must be between 13 and 120.")
    except ValueError:
        errors.append("Age must be a whole number.")
        age = 0
    try:
        weight = float(weight_text)
        if not 25 <= weight <= 500:
            errors.append("Weight must be between 25 and 500 kg.")
    except ValueError:
        errors.append("Weight must be a number in kilograms.")
        weight = 0
    try:
        height = float(height_text)
        if not 100 <= height <= 250:
            errors.append("Height must be between 100 and 250 cm.")
    except ValueError:
        errors.append("Height must be a number in centimeters.")
        height = 0
    if errors:
        return None, errors
    return UserProfile(age, weight, height), []


def profile_label(profile: UserProfile) -> str:
    """Return a neutral, non-diagnostic BMI profile label."""
    bmi = profile.bmi
    if bmi < 18.5:
        return "Below the usual BMI range"
    if bmi < 25:
        return "Within the usual BMI range"
    if bmi < 30:
        return "Above the usual BMI range"
    return "Well above the usual BMI range"


def recommend_exercises(profile: UserProfile) -> List[Dict[str, str]]:
    """Build gentle, adjustable exercise suggestions from a profile."""
    low_impact = profile.age >= 65 or profile.bmi >= 30
    if low_impact:
        return [
            {"name": "Steady walk", "duration": "15–25 min", "why": "Low-impact cardio; keep a conversational pace."},
            {"name": "Chair strength circuit", "duration": "2 rounds", "why": "Sit-to-stands, wall push-ups, and calf raises."},
            {"name": "Mobility flow", "duration": "8–10 min", "why": "Gentle ankle, hip, shoulder, and back mobility."},
        ]
    return [
        {"name": "Brisk walk or cycle", "duration": "20–30 min", "why": "Build aerobic fitness at a sustainable pace."},
        {"name": "Full-body strength", "duration": "2–3 rounds", "why": "Squats, push-ups, rows, and a comfortable core exercise."},
        {"name": "Stretch and reset", "duration": "8–10 min", "why": "Easy stretches after warming up; never force a range."},
    ]


def next_reminder(reminder_time: str, now: Optional[datetime] = None) -> Optional[datetime]:
    """Return the next occurrence of an HH:MM daily reminder, or None if invalid."""
    try:
        target = datetime.strptime(reminder_time, "%H:%M").time()
    except ValueError:
        return None
    current = now or datetime.now()
    candidate = current.replace(hour=target.hour, minute=target.minute, second=0, microsecond=0)
    return candidate if candidate > current else candidate + timedelta(days=1)


class ExerciseApp(tk.Tk):
    BG = "#071526"
    PANEL = "#0d2238"
    BLUE = "#31b8ff"
    TEXT = "#e7f5ff"
    MUTED = "#8caec4"

    def __init__(self) -> None:
        super().__init__()
        self.title("PULSE//PILOT  •  Movement console")
        self.geometry("900x700")
        self.minsize(760, 620)
        self.configure(bg=self.BG)
        self.profile: Optional[UserProfile] = None
        self.reminder_job: Optional[str] = None
        self.reminder_enabled = tk.BooleanVar(value=False)
        self.reminder_var = tk.StringVar(value="08:00")
        self._build_style()
        self._build_ui()
        self._tick()

    def _build_style(self) -> None:
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TFrame", background=self.BG)
        style.configure("Panel.TFrame", background=self.PANEL)
        style.configure("TLabel", background=self.BG, foreground=self.TEXT, font=("Segoe UI", 10))
        style.configure("Muted.TLabel", foreground=self.MUTED, font=("Segoe UI", 9))
        style.configure("Title.TLabel", foreground=self.BLUE, font=("Segoe UI", 23, "bold"))
        style.configure("Header.TLabel", background=self.PANEL, foreground=self.BLUE, font=("Segoe UI", 12, "bold"))
        style.configure("TButton", background="#124a70", foreground=self.TEXT, borderwidth=0, padding=8)
        style.map("TButton", background=[("active", "#1a6f9d")])
        style.configure("TEntry", fieldbackground="#102d46", foreground=self.TEXT, insertcolor=self.TEXT)
        style.configure("TCheckbutton", background=self.PANEL, foreground=self.TEXT)
        style.configure("TCombobox", fieldbackground="#102d46", foreground=self.TEXT)

    def _build_ui(self) -> None:
        root = ttk.Frame(self, padding=24)
        root.pack(fill="both", expand=True)
        ttk.Label(root, text="PULSE//PILOT", style="Title.TLabel").pack(anchor="w")
        ttk.Label(root, text="PERSONAL MOVEMENT CONSOLE  /  safe, small steps count", style="Muted.TLabel").pack(anchor="w", pady=(0, 18))
        columns = ttk.Frame(root)
        columns.pack(fill="both", expand=True)
        left = ttk.Frame(columns, style="Panel.TFrame", padding=18)
        left.pack(side="left", fill="y", padx=(0, 14))
        right = ttk.Frame(columns, style="Panel.TFrame", padding=18)
        right.pack(side="left", fill="both", expand=True)

        ttk.Label(left, text="PROFILE INPUT", style="Header.TLabel").pack(anchor="w", pady=(0, 12))
        self.age_entry = self._field(left, "Age (years)")
        self.weight_entry = self._field(left, "Weight (kg)")
        self.height_entry = self._field(left, "Height (cm)")
        ttk.Button(left, text="SCAN PROFILE", command=self._scan_profile).pack(fill="x", pady=(12, 16))
        self.profile_result = ttk.Label(left, text="Awaiting profile scan.", style="Muted.TLabel", wraplength=220)
        self.profile_result.pack(anchor="w")
        ttk.Separator(left).pack(fill="x", pady=18)
        ttk.Label(left, text="REMINDER LINK", style="Header.TLabel").pack(anchor="w", pady=(0, 8))
        ttk.Checkbutton(left, text="Enable daily reminder", variable=self.reminder_enabled, command=self._toggle_reminder).pack(anchor="w")
        time_row = ttk.Frame(left, style="Panel.TFrame")
        time_row.pack(fill="x", pady=8)
        self.hour = ttk.Combobox(time_row, width=3, values=[f"{n:02d}" for n in range(24)], state="readonly")
        self.minute = ttk.Combobox(time_row, width=3, values=[f"{n:02d}" for n in range(0, 60, 5)], state="readonly")
        self.hour.set("08"); self.minute.set("00")
        self.hour.bind("<<ComboboxSelected>>", self._time_changed)
        self.minute.bind("<<ComboboxSelected>>", self._time_changed)
        self.hour.pack(side="left"); ttk.Label(time_row, text=" : ", style="Muted.TLabel").pack(side="left"); self.minute.pack(side="left")
        self.reminder_status = ttk.Label(left, text="Reminders are off.", style="Muted.TLabel", wraplength=220)
        self.reminder_status.pack(anchor="w", pady=(3, 0))

        ttk.Label(right, text="YOUR ROUTE", style="Header.TLabel").pack(anchor="w")
        self.suggestions = tk.Text(right, height=13, bg="#091b2c", fg=self.TEXT, insertbackground=self.TEXT, relief="flat", padx=12, pady=12, font=("Consolas", 10), state="disabled")
        self.suggestions.pack(fill="both", expand=True, pady=(10, 14))
        ttk.Label(right, text="SAFETY GUIDANCE", style="Header.TLabel").pack(anchor="w")
        ttk.Label(right, text="Warm up gently. Stop for chest pain, faintness, severe breathlessness, or sharp pain and seek medical help. Hydrate, use good form, and progress gradually. This app is educational—not medical advice.", style="Muted.TLabel", wraplength=520).pack(anchor="w", pady=(8, 0))

    def _field(self, parent: ttk.Frame, label: str) -> ttk.Entry:
        ttk.Label(parent, text=label, style="Muted.TLabel").pack(anchor="w", pady=(8, 3))
        entry = ttk.Entry(parent, width=24)
        entry.pack(fill="x")
        return entry

    def _scan_profile(self) -> None:
        profile, errors = validate_profile(self.age_entry.get(), self.weight_entry.get(), self.height_entry.get())
        if errors:
            messagebox.showerror("Profile needs attention", "\n".join(errors), parent=self)
            return
        self.profile = profile
        assert profile is not None
        self.profile_result.configure(text=f"BMI: {profile.bmi:.1f}\n{profile_label(profile)}")
        self._write_suggestions(recommend_exercises(profile))

    def _write_suggestions(self, items: List[Dict[str, str]]) -> None:
        self.suggestions.configure(state="normal")
        self.suggestions.delete("1.0", "end")
        self.suggestions.insert("end", "TODAY'S STARTER SEQUENCE\n\n")
        for index, item in enumerate(items, 1):
            self.suggestions.insert("end", f"{index:02d}  {item['name'].upper()}  ·  {item['duration']}\n    {item['why']}\n\n")
        self.suggestions.configure(state="disabled")

    def _toggle_reminder(self) -> None:
        if self.reminder_enabled.get():
            self._schedule_reminder()
        else:
            if self.reminder_job:
                self.after_cancel(self.reminder_job)
                self.reminder_job = None
            self.reminder_status.configure(text="Reminders are off.")

    def _time_changed(self, _event: object = None) -> None:
        if self.reminder_enabled.get():
            if self.reminder_job:
                self.after_cancel(self.reminder_job)
                self.reminder_job = None
            self._schedule_reminder()

    def _schedule_reminder(self) -> None:
        value = f"{self.hour.get()}:{self.minute.get()}"
        target = next_reminder(value)
        if not target:
            self.reminder_status.configure(text="Choose a valid time.")
            return
        delta = max(1000, int((target - datetime.now()).total_seconds() * 1000))
        self.reminder_status.configure(text=f"Next reminder: {target.strftime('%a %d %b, %H:%M')}")
        self.reminder_job = self.after(delta, self._reminder_popup)

    def _reminder_popup(self) -> None:
        self.reminder_job = None
        if self.reminder_enabled.get():
            messagebox.showinfo("PULSE//PILOT reminder", "Time for a movement break. Start gently and listen to your body.", parent=self)
            self._schedule_reminder()

    def _tick(self) -> None:
        if self.reminder_enabled.get() and self.reminder_job is None:
            self._schedule_reminder()
        self.after(30_000, self._tick)


def main() -> None:
    ExerciseApp().mainloop()


if __name__ == "__main__":
    main()
