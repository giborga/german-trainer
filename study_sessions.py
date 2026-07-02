"""
load study session dates
append today’s date to study session dates if not already last / present
return latest N dates to train recently added words
"""

import json
import os

STUDY_SESSIONS = "study_sessions.json"

def load_sessions() -> list[str]:
    if not os.path.exists(STUDY_SESSIONS):
        return []

    with open(STUDY_SESSIONS, "r", encoding="utf-8") as file:
        return json.load(file)


def save_session(session_date: str) -> None:
    session_dates = load_sessions()

    if session_date not in session_dates:
        session_dates.append(session_date)
        with open(STUDY_SESSIONS, "w", encoding="utf-8") as file:
            json.dump(session_dates, file, ensure_ascii=False, indent=2)


def get_latest_session_dates(limit: int) -> list[str]:
    session_dates = load_sessions()
    print("latest_session_dates: ", session_dates[-limit:])
    return session_dates[-limit:]