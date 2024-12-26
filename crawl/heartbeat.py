import uuid 
from streamlit import session_state, context
import threading
from streamlit.runtime.scriptrunner import add_script_run_ctx
from typing import Dict

class HeartbeatManager:
    def __init__(self, storage_file: str = "user_sessions.json"):
        self.storage_file = Path(storage_file)
        self.lock = threading.Lock()
        self._ensure_storage_file()

    def _ensure_storage_file(self):
        """Create storage file if it doesn't exist"""
        if not self.storage_file.exists():
            with open(self.storage_file, 'w') as f:
                json.dump({}, f)

    def _load_sessions(self) -> Dict:
        """Load session data from file"""
        try:
            with open(self.storage_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}

    def _save_sessions(self, sessions: Dict):
        """Save session data to file"""
        with open(self.storage_file, 'w') as f:
            json.dump(sessions, f, indent=2)

    def update_heartbeat(self, user_id: str):
        """Update user's heartbeat timestamp"""
        current_time = datetime.now().isoformat()
        with self.lock:
            sessions = self._load_sessions()
            
            # Ensure proper data structure
            if user_id not in sessions or not isinstance(sessions[user_id], dict):
                sessions[user_id] = {
                    'heartbeat': current_time,
                    'last_activity': current_time
                }
            else:
                sessions[user_id]['heartbeat'] = current_time
            
            self._save_sessions(sessions)

    def update_activity(self, user_id: str):
        """Update user's last activity timestamp"""
        current_time = datetime.now().isoformat()
        with self.lock:
            sessions = self._load_sessions()
            
            # Ensure proper data structure
            if user_id not in sessions or not isinstance(sessions[user_id], dict):
                sessions[user_id] = {
                    'heartbeat': current_time,
                    'last_activity': current_time
                }
            else:
                sessions[user_id]['last_activity'] = current_time
            
            self._save_sessions(sessions)

    def cleanup_sessions(self, heartbeat_timeout_minutes: int = 1):
        """Remove inactive sessions based on heartbeat"""
        with self.lock:
            sessions = self._load_sessions()
            current_time = datetime.now()
            active_sessions = {}
            
            for user_id, data in sessions.items():
                # Skip invalid entries
                if not isinstance(data, dict) or 'heartbeat' not in data:
                    continue
                
                try:
                    last_heartbeat = datetime.fromisoformat(data['heartbeat'])
                    if current_time - last_heartbeat < timedelta(minutes=heartbeat_timeout_minutes):
                        active_sessions[user_id] = data
                except (ValueError, TypeError):
                    continue
            
            self._save_sessions(active_sessions)
            return active_sessions

    def get_session_info(self, user_id: str) -> Dict:
        """Get session information for a specific user"""
        with self.lock:
            sessions = self._load_sessions()
            user_data = sessions.get(user_id, {})
            if not isinstance(user_data, dict):
                return {}
            return user_data








def periodic_cleanup():
    """Periodically clean up inactive sessions"""
    thread = threading.Timer(60.0, periodic_cleanup)
    add_script_run_ctx(thread)
    thread.daemon = True
    thread.start()
    

    heartbeat_manager.cleanup_sessions()

class SessionState:
    def __init__(self):
        self.user_id = None

def get_user_id():
    """Generate or retrieve user ID from session state"""
    if 'session_state' not in session_state:
        session_state.session_state = SessionState()
        
    if session_state.session_state.user_id is None:
        cookies = context.cookies
        user_id = cookies.get('user_id')
        
        if not user_id:
            user_id = str(uuid.uuid4())
            
        session_state.session_state.user_id = user_id
        
    return session_state.session_state.user_id
