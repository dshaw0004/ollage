from constants import app_dir
import sqlite3

CREATE_SESSIONS_TABLE = '''
CREATE TABLE IF NOT EXISTS sessions(
    id TEXT NOT NULL PRIMARY KEY,
    title TEXT,
    workspace_path TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    first_message TEXT NOT NULL,
    state TEXT NOT NULL DEFAULT 'ACTIVE' CHECK(state IN ('ACTIVE', 'DELETED', 'ARCHIVED'))
);
'''
CREATE_SESSIONS_INDEXES = '''
CREATE INDEX IF NOT EXISTS sessions_workspace_index ON sessions(workspace_path);
'''

CREATE_MESSAGES_TABLE = '''
CREATE TABLE IF NOT EXISTS messages(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT,
    role TEXT NOT NULL CHECK(role IN ('user', 'assistant', 'system', 'tool')),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    count INTEGER,
    session_id TEXT NOT NULL REFERENCES sessions(id),
    tool_call_id TEXT
);
'''
CREATE_MESSAGES_INDEXES = '''
CREATE INDEX IF NOT EXISTS message_session_id_index ON messages(session_id);
'''


class PersistantMemory:
    def __init__(self) -> None:
        self.connection = sqlite3.connect(app_dir + '/master.sqlite3')
        self.cursor = self.connection.cursor()
        self.cursor.execute('PRAGMA journal_mode = WAL;')
        self.cursor.execute(CREATE_SESSIONS_TABLE)
        self.cursor.execute(CREATE_SESSIONS_INDEXES)
        self.cursor.execute(CREATE_MESSAGES_TABLE)
        self.cursor.execute(CREATE_MESSAGES_INDEXES)
        self.connection.commit()

    def __del__(self):
        self.cursor.close()
        self.connection.close()


if '__main__' == __name__:
    PersistantMemory()
