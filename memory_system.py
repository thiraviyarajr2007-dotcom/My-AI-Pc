"""
FREE Memory System - SQLite Database
Stores: Commands, preferences, context, learned patterns
100% Free, No cloud, Completely offline
"""

import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional
import os


class MemorySystem:
    """Free local memory system using SQLite."""
    
    def __init__(self, db_path: str = "christa_memory.db"):
        """Initialize memory system."""
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self._init_database()
    
    def _init_database(self):
        """Initialize database and create tables."""
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        
        # Commands history table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS commands (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                command TEXT NOT NULL,
                intent TEXT,
                confidence REAL,
                response TEXT,
                device_id TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                success BOOLEAN
            )
        ''')
        
        # User preferences table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS preferences (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Context table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS context (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                metadata TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Learned patterns table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS patterns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pattern_type TEXT NOT NULL,
                pattern_data TEXT NOT NULL,
                frequency INTEGER DEFAULT 1,
                last_seen DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # App usage table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS app_usage (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                app_name TEXT NOT NULL,
                duration_seconds REAL,
                date DATE DEFAULT CURRENT_DATE,
                UNIQUE(app_name, date)
            )
        ''')
        
        self.conn.commit()
        print("[✓] Memory system initialized")
    
    # ─── Commands History ──────────────────────────────────────
    
    def add_command(
        self,
        command: str,
        intent: str = None,
        confidence: float = None,
        response: str = None,
        device_id: str = None,
        success: bool = True
    ):
        """Store command in history."""
        self.cursor.execute('''
            INSERT INTO commands (command, intent, confidence, response, device_id, success)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (command, intent, confidence, response, device_id, success))
        self.conn.commit()
    
    def get_command_history(self, limit: int = 50, device_id: str = None) -> List[Dict]:
        """Get command history."""
        if device_id:
            self.cursor.execute('''
                SELECT * FROM commands WHERE device_id = ? 
                ORDER BY timestamp DESC LIMIT ?
            ''', (device_id, limit))
        else:
            self.cursor.execute('''
                SELECT * FROM commands ORDER BY timestamp DESC LIMIT ?
            ''', (limit,))
        
        columns = [desc[0] for desc in self.cursor.description]
        return [dict(zip(columns, row)) for row in self.cursor.fetchall()]
    
    def search_commands(self, query: str, limit: int = 10) -> List[Dict]:
        """Search commands by text."""
        self.cursor.execute('''
            SELECT * FROM commands 
            WHERE command LIKE ? OR response LIKE ?
            ORDER BY timestamp DESC LIMIT ?
        ''', (f'%{query}%', f'%{query}%', limit))
        
        columns = [desc[0] for desc in self.cursor.description]
        return [dict(zip(columns, row)) for row in self.cursor.fetchall()]
    
    def get_most_used_commands(self, limit: int = 10) -> List[Dict]:
        """Get most frequently used commands."""
        self.cursor.execute('''
            SELECT command, COUNT(*) as count 
            FROM commands 
            WHERE success = 1
            GROUP BY command 
            ORDER BY count DESC 
            LIMIT ?
        ''', (limit,))
        
        return [{"command": row[0], "count": row[1]} for row in self.cursor.fetchall()]
    
    # ─── User Preferences ──────────────────────────────────────
    
    def set_preference(self, key: str, value: any):
        """Set user preference."""
        value_str = json.dumps(value) if not isinstance(value, str) else value
        self.cursor.execute('''
            INSERT OR REPLACE INTO preferences (key, value, updated_at)
            VALUES (?, ?, CURRENT_TIMESTAMP)
        ''', (key, value_str))
        self.conn.commit()
    
    def get_preference(self, key: str, default: any = None) -> any:
        """Get user preference."""
        self.cursor.execute('SELECT value FROM preferences WHERE key = ?', (key,))
        result = self.cursor.fetchone()
        
        if result:
            try:
                return json.loads(result[0])
            except:
                return result[0]
        return default
    
    def get_all_preferences(self) -> Dict:
        """Get all preferences."""
        self.cursor.execute('SELECT key, value FROM preferences')
        prefs = {}
        for key, value in self.cursor.fetchall():
            try:
                prefs[key] = json.loads(value)
            except:
                prefs[key] = value
        return prefs
    
    # ─── Context Management ────────────────────────────────────
    
    def add_context(self, role: str, content: str, metadata: Dict = None):
        """Add context entry."""
        metadata_str = json.dumps(metadata) if metadata else None
        self.cursor.execute('''
            INSERT INTO context (role, content, metadata)
            VALUES (?, ?, ?)
        ''', (role, content, metadata_str))
        self.conn.commit()
    
    def get_recent_context(self, limit: int = 10) -> List[Dict]:
        """Get recent context."""
        self.cursor.execute('''
            SELECT * FROM context ORDER BY timestamp DESC LIMIT ?
        ''', (limit,))
        
        columns = [desc[0] for desc in self.cursor.description]
        contexts = []
        for row in self.cursor.fetchall():
            ctx = dict(zip(columns, row))
            if ctx['metadata']:
                try:
                    ctx['metadata'] = json.loads(ctx['metadata'])
                except:
                    pass
            contexts.append(ctx)
        return contexts
    
    def clear_old_context(self, days: int = 30):
        """Clear context older than specified days."""
        self.cursor.execute('''
            DELETE FROM context 
            WHERE timestamp < datetime('now', '-' || ? || ' days')
        ''', (days,))
        self.conn.commit()
    
    # ─── Pattern Learning ──────────────────────────────────────
    
    def add_pattern(self, pattern_type: str, pattern_data: Dict):
        """Add or update learned pattern."""
        pattern_str = json.dumps(pattern_data)
        
        # Check if pattern exists
        self.cursor.execute('''
            SELECT id, frequency FROM patterns 
            WHERE pattern_type = ? AND pattern_data = ?
        ''', (pattern_type, pattern_str))
        
        result = self.cursor.fetchone()
        
        if result:
            # Update frequency
            self.cursor.execute('''
                UPDATE patterns 
                SET frequency = frequency + 1, last_seen = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (result[0],))
        else:
            # Insert new pattern
            self.cursor.execute('''
                INSERT INTO patterns (pattern_type, pattern_data)
                VALUES (?, ?)
            ''', (pattern_type, pattern_str))
        
        self.conn.commit()
    
    def get_patterns(self, pattern_type: str = None, min_frequency: int = 1) -> List[Dict]:
        """Get learned patterns."""
        if pattern_type:
            self.cursor.execute('''
                SELECT * FROM patterns 
                WHERE pattern_type = ? AND frequency >= ?
                ORDER BY frequency DESC
            ''', (pattern_type, min_frequency))
        else:
            self.cursor.execute('''
                SELECT * FROM patterns 
                WHERE frequency >= ?
                ORDER BY frequency DESC
            ''', (min_frequency,))
        
        columns = [desc[0] for desc in self.cursor.description]
        patterns = []
        for row in self.cursor.fetchall():
            pattern = dict(zip(columns, row))
            try:
                pattern['pattern_data'] = json.loads(pattern['pattern_data'])
            except:
                pass
            patterns.append(pattern)
        return patterns
    
    # ─── App Usage Tracking ────────────────────────────────────
    
    def add_app_usage(self, app_name: str, duration_seconds: float):
        """Add or update app usage."""
        self.cursor.execute('''
            INSERT INTO app_usage (app_name, duration_seconds)
            VALUES (?, ?)
            ON CONFLICT(app_name, date) 
            DO UPDATE SET duration_seconds = duration_seconds + ?
        ''', (app_name, duration_seconds, duration_seconds))
        self.conn.commit()
    
    def get_app_usage(self, days: int = 7) -> List[Dict]:
        """Get app usage statistics."""
        self.cursor.execute('''
            SELECT app_name, SUM(duration_seconds) as total_seconds
            FROM app_usage
            WHERE date >= date('now', '-' || ? || ' days')
            GROUP BY app_name
            ORDER BY total_seconds DESC
        ''', (days,))
        
        return [
            {
                "app_name": row[0],
                "total_seconds": row[1],
                "total_minutes": round(row[1] / 60, 2),
                "total_hours": round(row[1] / 3600, 2)
            }
            for row in self.cursor.fetchall()
        ]
    
    # ─── Statistics ────────────────────────────────────────────
    
    def get_statistics(self) -> Dict:
        """Get overall statistics."""
        stats = {}
        
        # Total commands
        self.cursor.execute('SELECT COUNT(*) FROM commands')
        stats['total_commands'] = self.cursor.fetchone()[0]
        
        # Successful commands
        self.cursor.execute('SELECT COUNT(*) FROM commands WHERE success = 1')
        stats['successful_commands'] = self.cursor.fetchone()[0]
        
        # Total patterns
        self.cursor.execute('SELECT COUNT(*) FROM patterns')
        stats['learned_patterns'] = self.cursor.fetchone()[0]
        
        # Context entries
        self.cursor.execute('SELECT COUNT(*) FROM context')
        stats['context_entries'] = self.cursor.fetchone()[0]
        
        # Most active device
        self.cursor.execute('''
            SELECT device_id, COUNT(*) as count 
            FROM commands 
            WHERE device_id IS NOT NULL
            GROUP BY device_id 
            ORDER BY count DESC 
            LIMIT 1
        ''')
        result = self.cursor.fetchone()
        if result:
            stats['most_active_device'] = {"device_id": result[0], "commands": result[1]}
        
        return stats
    
    # ─── Cleanup ───────────────────────────────────────────────
    
    def cleanup(self, days: int = 90):
        """Clean up old data."""
        # Delete old commands
        self.cursor.execute('''
            DELETE FROM commands 
            WHERE timestamp < datetime('now', '-' || ? || ' days')
        ''', (days,))
        
        # Delete old context
        self.cursor.execute('''
            DELETE FROM context 
            WHERE timestamp < datetime('now', '-' || ? || ' days')
        ''', (days,))
        
        # Delete old app usage
        self.cursor.execute('''
            DELETE FROM app_usage 
            WHERE date < date('now', '-' || ? || ' days')
        ''', (days,))
        
        self.conn.commit()
        print(f"[✓] Cleaned up data older than {days} days")
    
    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()
            print("[✓] Memory system closed")


# ─── Standalone Test ───────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 60)
    print("  🧠 FREE Memory System - Test Mode")
    print("=" * 60)
    
    # Initialize
    memory = MemorySystem("test_memory.db")
    
    # Test commands
    print("\n[Test] Adding commands...")
    memory.add_command("open chrome", "open_app", 0.95, "Opening Chrome", "laptop", True)
    memory.add_command("take screenshot", "screenshot", 0.90, "Screenshot taken", "phone", True)
    memory.add_command("find documents", "search", 0.85, "Found 5 files", "laptop", True)
    
    # Test preferences
    print("[Test] Setting preferences...")
    memory.set_preference("voice_rate", 175)
    memory.set_preference("wake_word", "hey christa")
    memory.set_preference("theme", "dark")
    
    # Test context
    print("[Test] Adding context...")
    memory.add_context("user", "What's the weather?", {"intent": "question"})
    memory.add_context("assistant", "I can't check weather yet", {"confidence": 0.8})
    
    # Test patterns
    print("[Test] Learning patterns...")
    memory.add_pattern("morning_routine", {"apps": ["chrome", "spotify", "slack"]})
    memory.add_pattern("work_hours", {"start": 9, "end": 17})
    
    # Test app usage
    print("[Test] Tracking app usage...")
    memory.add_app_usage("VS Code", 3600)  # 1 hour
    memory.add_app_usage("Chrome", 1800)   # 30 minutes
    
    # Get statistics
    print("\n📊 Statistics:")
    stats = memory.get_statistics()
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    # Get command history
    print("\n📜 Command History:")
    history = memory.get_command_history(limit=5)
    for cmd in history:
        print(f"   • {cmd['command']} ({cmd['intent']}) - {cmd['timestamp']}")
    
    # Get preferences
    print("\n⚙️  Preferences:")
    prefs = memory.get_all_preferences()
    for key, value in prefs.items():
        print(f"   {key}: {value}")
    
    # Get patterns
    print("\n🧩 Learned Patterns:")
    patterns = memory.get_patterns()
    for pattern in patterns:
        print(f"   • {pattern['pattern_type']}: {pattern['pattern_data']} (frequency: {pattern['frequency']})")
    
    # Get app usage
    print("\n📱 App Usage (Last 7 days):")
    usage = memory.get_app_usage(days=7)
    for app in usage:
        print(f"   • {app['app_name']}: {app['total_minutes']} minutes")
    
    # Close
    memory.close()
    
    # Clean up test database
    if os.path.exists("test_memory.db"):
        os.remove("test_memory.db")
        print("\n[✓] Test database cleaned up")
    
    print("\n✅ All tests passed!")
    print("=" * 60)
