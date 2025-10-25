"""
Session Parser - Parse Claude .jsonl and Gemini .json log formats
♠️🌿🎸🧵
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime


class SessionParser:
    """Unified parser for Claude Code and Gemini CLI session logs."""

    def __init__(self):
        self.claude_projects_dir = Path.home() / ".claude" / "projects"
        self.gemini_tmp_dir = Path.home() / ".gemini" / "tmp"

    def parse_claude_sessions(self) -> List[Dict[str, Any]]:
        """
        Parse all Claude Code sessions from .jsonl files.

        Returns:
            List of session dictionaries with metadata and messages
        """
        sessions = []

        if not self.claude_projects_dir.exists():
            return sessions

        for project_dir in self.claude_projects_dir.iterdir():
            if not project_dir.is_dir():
                continue

            # Find all .jsonl files in the project directory
            jsonl_files = list(project_dir.glob("*.jsonl"))

            for jsonl_file in jsonl_files:
                try:
                    session = self._parse_claude_jsonl(jsonl_file, project_dir.name)
                    if session:
                        sessions.append(session)
                except Exception as e:
                    print(f"Error parsing Claude session {jsonl_file}: {e}")

        return sessions

    def _parse_claude_jsonl(self, jsonl_path: Path, project_hash: str) -> Optional[Dict[str, Any]]:
        """Parse a single Claude .jsonl file."""
        messages = []
        session_id = jsonl_path.stem
        first_timestamp = None
        last_timestamp = None

        with open(jsonl_path, 'r', encoding='utf-8') as f:
            for line in f:
                if not line.strip():
                    continue

                try:
                    entry = json.loads(line)
                    timestamp = entry.get('timestamp', '')

                    if timestamp:
                        if not first_timestamp:
                            first_timestamp = timestamp
                        last_timestamp = timestamp

                    messages.append(entry)
                except json.JSONDecodeError:
                    continue

        if not messages:
            return None

        # Extract project path from project_hash (e.g., "-data-data-com-termux-files-home-workspace-assemblylook")
        project_path = self._decode_claude_project_path(project_hash)

        return {
            'ai_type': 'claude',
            'session_id': session_id,
            'project_hash': project_hash,
            'project_path': project_path,
            'messages': messages,
            'message_count': len(messages),
            'first_timestamp': first_timestamp,
            'last_timestamp': last_timestamp,
            'file_path': str(jsonl_path),
            'html_path': str(jsonl_path.with_suffix('.html')) if (jsonl_path.with_suffix('.html')).exists() else None
        }

    def _decode_claude_project_path(self, project_hash: str) -> str:
        """Decode Claude's project hash into a readable path."""
        if project_hash.startswith('-data-data-com-termux-files-home-'):
            # Remove prefix and convert hyphens back to slashes
            path = project_hash.replace('-data-data-com-termux-files-home-', '/data/data/com.termux/files/home/')
            path = path.replace('-', '/')
            return path
        return project_hash

    def parse_gemini_sessions(self) -> List[Dict[str, Any]]:
        """
        Parse all Gemini CLI sessions from .json files.

        Returns:
            List of session dictionaries with metadata and messages
        """
        sessions = []

        if not self.gemini_tmp_dir.exists():
            return sessions

        for project_dir in self.gemini_tmp_dir.iterdir():
            if not project_dir.is_dir():
                continue

            # Find all session JSON files
            session_files = list((project_dir / "chats").glob("session-*.json")) if (project_dir / "chats").exists() else []

            # Also check for checkpoint files
            checkpoint_files = list(project_dir.glob("checkpoint-*.json"))

            # Process session files
            for session_file in session_files:
                try:
                    session = self._parse_gemini_session(session_file, project_dir.name)
                    if session:
                        sessions.append(session)
                except Exception as e:
                    print(f"Error parsing Gemini session {session_file}: {e}")

            # Process checkpoint files
            for checkpoint_file in checkpoint_files:
                try:
                    session = self._parse_gemini_checkpoint(checkpoint_file, project_dir.name)
                    if session:
                        sessions.append(session)
                except Exception as e:
                    print(f"Error parsing Gemini checkpoint {checkpoint_file}: {e}")

        return sessions

    def _parse_gemini_session(self, session_path: Path, project_hash: str) -> Optional[Dict[str, Any]]:
        """Parse a Gemini session JSON file."""
        with open(session_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        messages = data.get('messages', [])
        if not messages:
            return None

        session_id = session_path.stem
        first_timestamp = messages[0].get('timestamp', '') if messages else None
        last_timestamp = messages[-1].get('timestamp', '') if messages else None

        return {
            'ai_type': 'gemini',
            'session_id': session_id,
            'project_hash': project_hash,
            'project_path': self._get_gemini_project_path(project_hash),
            'messages': messages,
            'message_count': len(messages),
            'first_timestamp': first_timestamp,
            'last_timestamp': last_timestamp,
            'file_path': str(session_path),
            'html_path': str(session_path.with_suffix('.html')) if (session_path.with_suffix('.html')).exists() else None
        }

    def _parse_gemini_checkpoint(self, checkpoint_path: Path, project_hash: str) -> Optional[Dict[str, Any]]:
        """Parse a Gemini checkpoint JSON file."""
        with open(checkpoint_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if not data or not isinstance(data, list):
            return None

        session_id = checkpoint_path.stem

        # Checkpoints don't have explicit timestamps in the same format
        # We'll use file modification time as a proxy
        mtime = checkpoint_path.stat().st_mtime
        timestamp = datetime.fromtimestamp(mtime).isoformat()

        return {
            'ai_type': 'gemini',
            'session_id': session_id,
            'project_hash': project_hash,
            'project_path': self._get_gemini_project_path(project_hash),
            'messages': data,
            'message_count': len(data),
            'first_timestamp': timestamp,
            'last_timestamp': timestamp,
            'file_path': str(checkpoint_path),
            'html_path': str(checkpoint_path.with_suffix('.html')) if (checkpoint_path.with_suffix('.html')).exists() else None,
            'is_checkpoint': True
        }

    def _get_gemini_project_path(self, project_hash: str) -> str:
        """
        Try to map Gemini project hash to actual workspace path.
        This is a heuristic - we'll improve it in project_mapper.py
        """
        # For now, just return the hash
        # The project_mapper module will handle the actual mapping
        return f"gemini-project-{project_hash[:8]}"

    def parse_all_sessions(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Parse all sessions from both Claude and Gemini.

        Returns:
            Dictionary with 'claude' and 'gemini' keys containing session lists
        """
        return {
            'claude': self.parse_claude_sessions(),
            'gemini': self.parse_gemini_sessions()
        }


if __name__ == "__main__":
    # Quick test
    parser = SessionParser()
    sessions = parser.parse_all_sessions()
    print(f"Found {len(sessions['claude'])} Claude sessions")
    print(f"Found {len(sessions['gemini'])} Gemini sessions")
