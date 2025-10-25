"""
Project Mapper - Map session hashes to actual workspace project directories
♠️🌿🎸🧵
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Optional, Any


class ProjectMapper:
    """Maps AI session hashes to actual workspace project directories."""

    def __init__(self, workspace_root: Optional[str] = None):
        """
        Initialize project mapper.

        Args:
            workspace_root: Root directory containing projects (defaults to ~/workspace)
        """
        if workspace_root:
            self.workspace_root = Path(workspace_root)
        else:
            self.workspace_root = Path.home() / "workspace"

        self.src_root = Path.home() / "src"
        self.shortcuts_root = Path.home() / ".shortcuts"

    def map_claude_project(self, project_hash: str) -> Dict[str, Any]:
        """
        Map Claude project hash to actual directory and metadata.

        Args:
            project_hash: Claude's encoded project path (e.g., "-data-data-com-termux-files-home-workspace-assemblylook")

        Returns:
            Dictionary with project info: {
                'path': actual filesystem path,
                'name': project name,
                'category': 'workspace', 'src', 'shortcuts', 'home', or 'other',
                'exists': whether the directory currently exists
            }
        """
        # Decode the hash to actual path
        if project_hash.startswith('-data-data-com-termux-files-home-'):
            decoded_path = project_hash.replace(
                '-data-data-com-termux-files-home-',
                '/data/data/com.termux/files/home/'
            )
            # Replace remaining hyphens with slashes
            decoded_path = decoded_path.replace('-', '/')
        else:
            decoded_path = project_hash

        path = Path(decoded_path)
        exists = path.exists()

        # Determine category and extract project name
        if str(path).startswith(str(self.workspace_root)):
            category = 'workspace'
            relative_path = path.relative_to(self.workspace_root)
            name = str(relative_path).split('/')[0] if '/' in str(relative_path) else str(relative_path)
        elif str(path).startswith(str(self.src_root)):
            category = 'src'
            relative_path = path.relative_to(self.src_root)
            name = str(relative_path).split('/')[0] if '/' in str(relative_path) else str(relative_path)
        elif str(path).startswith(str(self.shortcuts_root)):
            category = 'shortcuts'
            name = '.shortcuts'
        elif str(path) == str(Path.home()):
            category = 'home'
            name = 'home'
        else:
            category = 'other'
            name = path.name or str(path)

        return {
            'path': str(path),
            'name': name,
            'category': category,
            'exists': exists,
            'original_hash': project_hash
        }

    def map_gemini_project(self, project_hash: str, session_messages: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Map Gemini project hash to actual directory using heuristics.

        Since Gemini uses SHA256 hashes, we need to infer the project from message content.

        Args:
            project_hash: Gemini's SHA256 project hash
            session_messages: Messages from the session to analyze for clues

        Returns:
            Dictionary with project info (same format as map_claude_project)
        """
        # Strategy: Look for file paths, commands, or project mentions in messages
        project_path = self._infer_project_from_messages(session_messages)

        if project_path:
            path = Path(project_path)
            exists = path.exists()

            if str(path).startswith(str(self.workspace_root)):
                category = 'workspace'
                relative_path = path.relative_to(self.workspace_root)
                name = str(relative_path).split('/')[0] if '/' in str(relative_path) else str(relative_path)
            elif str(path).startswith(str(self.src_root)):
                category = 'src'
                relative_path = path.relative_to(self.src_root)
                name = str(relative_path).split('/')[0] if '/' in str(relative_path) else str(relative_path)
            else:
                category = 'other'
                name = path.name
        else:
            # Fallback: use hash
            category = 'unknown'
            name = f"gemini-{project_hash[:8]}"
            path = Path.home() / ".gemini" / "tmp" / project_hash
            exists = path.exists()

        return {
            'path': str(path) if project_path else f"unknown-{project_hash[:8]}",
            'name': name,
            'category': category,
            'exists': exists,
            'original_hash': project_hash
        }

    def _infer_project_from_messages(self, messages: List[Dict[str, Any]]) -> Optional[str]:
        """
        Infer project path by analyzing message content.

        Looks for:
        - File paths in commands
        - Working directory mentions
        - Common project path patterns
        """
        path_patterns = [
            r'/data/data/com\.termux/files/home/workspace/([^/\s]+)',
            r'/data/data/com\.termux/files/home/src/([^/\s]+)',
            r'~/workspace/([^/\s]+)',
            r'~/src/([^/\s]+)',
        ]

        for message in messages:
            content = message.get('content', '') if isinstance(message, dict) else str(message)

            # Try to extract paths
            for pattern in path_patterns:
                matches = re.findall(pattern, content)
                if matches:
                    project_name = matches[0]
                    # Construct full path
                    if 'workspace' in pattern:
                        return str(self.workspace_root / project_name)
                    elif 'src' in pattern:
                        return str(self.src_root / project_name)

        return None

    def enrich_sessions(self, sessions: Dict[str, List[Dict[str, Any]]]) -> Dict[str, List[Dict[str, Any]]]:
        """
        Enrich session data with project mapping information.

        Args:
            sessions: Dictionary of sessions from SessionParser

        Returns:
            Enriched sessions with 'project_info' field added
        """
        enriched = {'claude': [], 'gemini': []}

        # Enrich Claude sessions
        for session in sessions['claude']:
            project_info = self.map_claude_project(session['project_hash'])
            session['project_info'] = project_info
            enriched['claude'].append(session)

        # Enrich Gemini sessions
        for session in sessions['gemini']:
            project_info = self.map_gemini_project(
                session['project_hash'],
                session.get('messages', [])
            )
            session['project_info'] = project_info
            enriched['gemini'].append(session)

        return enriched

    def group_by_project(self, sessions: Dict[str, List[Dict[str, Any]]]) -> Dict[str, List[Dict[str, Any]]]:
        """
        Group sessions by project name (merged across both AIs).

        Returns:
            Dictionary mapping project names to lists of sessions
        """
        grouped = {}

        all_sessions = sessions['claude'] + sessions['gemini']

        for session in all_sessions:
            project_info = session.get('project_info', {})
            project_name = project_info.get('name', 'unknown')

            if project_name not in grouped:
                grouped[project_name] = []

            grouped[project_name].append(session)

        # Sort sessions within each project by timestamp
        for project_name in grouped:
            grouped[project_name].sort(
                key=lambda s: s.get('first_timestamp') or '',
                reverse=True  # Most recent first
            )

        return grouped


if __name__ == "__main__":
    # Quick test
    from assemblylook.core.session_parser import SessionParser

    parser = SessionParser()
    sessions = parser.parse_all_sessions()

    mapper = ProjectMapper()
    enriched = mapper.enrich_sessions(sessions)

    grouped = mapper.group_by_project(enriched)

    print(f"\nFound {len(grouped)} unique projects:")
    for project_name, project_sessions in sorted(grouped.items()):
        claude_count = sum(1 for s in project_sessions if s['ai_type'] == 'claude')
        gemini_count = sum(1 for s in project_sessions if s['ai_type'] == 'gemini')
        print(f"  {project_name}: {claude_count} Claude, {gemini_count} Gemini")
