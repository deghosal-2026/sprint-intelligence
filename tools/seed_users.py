"""Seed test users (alex/sdm, priya/junior) into the database."""

import os
import psycopg2

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://sprintsense:devpassword123@localhost:5432/sprintsense",
)

USERS = [
    {"username": "alex", "display_name": "Alex Chen", "default_persona": "sdm", "team_name": "team1", "is_admin": True},
    {"username": "priya", "display_name": "Priya Sharma", "default_persona": "junior_eng", "team_name": "team1", "is_admin": False},
]


def main():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    for user in USERS:
        cur.execute(
            "INSERT INTO users (username, display_name, default_persona, team_name, is_admin) "
            "VALUES (%(username)s, %(display_name)s, %(default_persona)s, %(team_name)s, %(is_admin)s) "
            "ON CONFLICT (username) DO UPDATE SET display_name = EXCLUDED.display_name",
            user,
        )
        print(f"  User '{user['username']}' ({user['default_persona']}) seeded")
    conn.commit()
    conn.close()
    print("Done. 2 users seeded.")


if __name__ == "__main__":
    main()
