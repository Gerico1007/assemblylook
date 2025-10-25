"""
Analyzer - Session analysis including Assembly mode detection and statistics
♠️🌿🎸🧵
"""

import re
from typing import Dict, List, Any, Optional


class SessionAnalyzer:
    """Analyzes AI sessions for patterns, Assembly mode, and generates summaries."""

    # Assembly mode detection patterns
    ASSEMBLY_PATTERNS = [
        r'♠️.*🌿.*🎸.*🧵',  # Full assembly symbols in order
        r'G\.?MUSIC ASSEMBLY',  # G.MUSIC ASSEMBLY MODE
        r'ASSEMBLY MODE ACTIVE',
        r'Spiral Ensemble',
        r'♠️.*Nyro',
        r'🌿.*Aureon',
        r'🎸.*JamAI',
        r'🧵.*Synth',
    ]

    # Perspective detection
    PERSPECTIVE_PATTERNS = {
        'nyro': r'♠️.*Nyro',
        'aureon': r'🌿.*Aureon',
        'jamai': r'🎸.*JamAI',
        'synth': r'🧵.*Synth',
    }

    def __init__(self):
        self.assembly_regex = re.compile('|'.join(self.ASSEMBLY_PATTERNS), re.IGNORECASE)
        self.perspective_regexes = {
            name: re.compile(pattern, re.IGNORECASE)
            for name, pattern in self.PERSPECTIVE_PATTERNS.items()
        }

    def analyze_session(self, session: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze a single session for Assembly mode, perspectives, and generate summary.

        Returns:
            Dictionary with analysis results:
            {
                'is_assembly_mode': bool,
                'perspectives_present': list of perspective names,
                'assembly_mentions': int,
                'summary': str,
                'first_message': str,
                'last_message': str,
                'stats': {...}
            }
        """
        messages = session.get('messages', [])
        ai_type = session.get('ai_type', '')

        # Extract text content from messages (format varies by AI)
        text_content = self._extract_text_content(messages, ai_type)
        full_text = ' '.join(text_content)

        # Detect Assembly mode
        is_assembly = bool(self.assembly_regex.search(full_text))
        assembly_mentions = len(self.assembly_regex.findall(full_text))

        # Detect perspectives
        perspectives = []
        for name, regex in self.perspective_regexes.items():
            if regex.search(full_text):
                perspectives.append(name)

        # Get first and last messages
        first_msg = self._get_first_user_message(messages, ai_type)
        last_msg = self._get_last_message(messages, ai_type)

        # Generate summary
        summary = self._generate_summary(session, is_assembly, perspectives)

        # Calculate statistics
        stats = self._calculate_stats(messages, ai_type, full_text)

        return {
            'is_assembly_mode': is_assembly,
            'perspectives_present': perspectives,
            'assembly_mentions': assembly_mentions,
            'summary': summary,
            'first_message': first_msg,
            'last_message': last_msg,
            'stats': stats
        }

    def _extract_text_content(self, messages: List[Any], ai_type: str) -> List[str]:
        """Extract text content from messages (handles different formats)."""
        text_content = []

        for msg in messages:
            if isinstance(msg, dict):
                if ai_type == 'claude':
                    # Claude format: check 'type' and 'content'
                    if msg.get('type') == 'text':
                        text_content.append(msg.get('content', ''))
                    elif 'content' in msg and isinstance(msg['content'], str):
                        text_content.append(msg['content'])
                elif ai_type == 'gemini':
                    # Gemini session format
                    if 'content' in msg:
                        text_content.append(str(msg['content']))
                    # Gemini checkpoint format
                    elif 'parts' in msg:
                        for part in msg['parts']:
                            if isinstance(part, dict) and 'text' in part:
                                text_content.append(part['text'])
            elif isinstance(msg, str):
                text_content.append(msg)

        return text_content

    def _get_first_user_message(self, messages: List[Any], ai_type: str) -> str:
        """Extract first user message from session."""
        for msg in messages:
            if not isinstance(msg, dict):
                continue

            if ai_type == 'claude':
                if msg.get('role') == 'user' or msg.get('type') == 'user':
                    content = msg.get('content', '')
                    if isinstance(content, str):
                        return content[:200] + ('...' if len(content) > 200 else '')
            elif ai_type == 'gemini':
                if msg.get('role') == 'user' or msg.get('type') == 'user':
                    content = msg.get('content', '')
                    if isinstance(content, str):
                        return content[:200] + ('...' if len(content) > 200 else '')

        return "No user message found"

    def _get_last_message(self, messages: List[Any], ai_type: str) -> str:
        """Extract last message from session."""
        if not messages:
            return "No messages"

        for msg in reversed(messages):
            if isinstance(msg, dict):
                content = msg.get('content', '')
                if isinstance(content, str) and content.strip():
                    return content[:200] + ('...' if len(content) > 200 else '')

        return "No content"

    def _generate_summary(self, session: Dict[str, Any], is_assembly: bool, perspectives: List[str]) -> str:
        """Generate a human-readable summary of the session."""
        ai_type = session.get('ai_type', 'unknown').capitalize()
        project_name = session.get('project_info', {}).get('name', 'unknown')
        message_count = session.get('message_count', 0)

        summary_parts = [f"{ai_type} session on {project_name}"]

        if is_assembly:
            summary_parts.append(f"♠️🌿🎸🧵 G.MUSIC ASSEMBLY MODE")
            if perspectives:
                perspective_names = ', '.join([p.capitalize() for p in perspectives])
                summary_parts.append(f"Perspectives: {perspective_names}")

        summary_parts.append(f"{message_count} messages")

        return " | ".join(summary_parts)

    def _calculate_stats(self, messages: List[Any], ai_type: str, full_text: str) -> Dict[str, Any]:
        """Calculate session statistics."""
        # Count different message types
        user_messages = 0
        assistant_messages = 0
        tool_calls = 0

        for msg in messages:
            if not isinstance(msg, dict):
                continue

            role = msg.get('role', '')
            msg_type = msg.get('type', '')

            if role == 'user' or msg_type == 'user':
                user_messages += 1
            elif role == 'assistant' or role == 'model' or msg_type == 'model':
                assistant_messages += 1

            # Detect tool calls (Claude format)
            if ai_type == 'claude' and msg.get('type') == 'tool_use':
                tool_calls += 1

            # Gemini function calls
            if ai_type == 'gemini' and isinstance(msg.get('parts'), list):
                for part in msg['parts']:
                    if isinstance(part, dict) and 'functionCall' in part:
                        tool_calls += 1

        # Word count estimate
        word_count = len(full_text.split())

        return {
            'user_messages': user_messages,
            'assistant_messages': assistant_messages,
            'tool_calls': tool_calls,
            'word_count': word_count,
            'avg_message_length': word_count // max(len(messages), 1)
        }

    def enrich_sessions_with_analysis(self, sessions: Dict[str, List[Dict[str, Any]]]) -> Dict[str, List[Dict[str, Any]]]:
        """
        Add analysis data to all sessions.

        Args:
            sessions: Session data from parser

        Returns:
            Sessions enriched with 'analysis' field
        """
        enriched = {'claude': [], 'gemini': []}

        for ai_type in ['claude', 'gemini']:
            for session in sessions.get(ai_type, []):
                analysis = self.analyze_session(session)
                session['analysis'] = analysis
                enriched[ai_type].append(session)

        return enriched

    def get_assembly_sessions(self, sessions: Dict[str, List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
        """
        Filter and return only sessions with Assembly mode active.

        Returns:
            List of Assembly mode sessions
        """
        assembly_sessions = []

        for ai_type in ['claude', 'gemini']:
            for session in sessions.get(ai_type, []):
                if session.get('analysis', {}).get('is_assembly_mode', False):
                    assembly_sessions.append(session)

        # Sort by timestamp
        assembly_sessions.sort(
            key=lambda s: s.get('first_timestamp') or '',
            reverse=True
        )

        return assembly_sessions


if __name__ == "__main__":
    # Quick test
    from assemblylook.core.session_parser import SessionParser
    from assemblylook.core.project_mapper import ProjectMapper

    parser = SessionParser()
    sessions = parser.parse_all_sessions()

    mapper = ProjectMapper()
    enriched = mapper.enrich_sessions(sessions)

    analyzer = SessionAnalyzer()
    analyzed = analyzer.enrich_sessions_with_analysis(enriched)

    print(f"\nTotal sessions: {len(analyzed['claude']) + len(analyzed['gemini'])}")

    # Find Assembly mode sessions
    assembly_sessions = analyzer.get_assembly_sessions(analyzed)
    print(f"\nAssembly Mode sessions: {len(assembly_sessions)}")

    for session in assembly_sessions[:5]:
        analysis = session['analysis']
        print(f"\n  {session['ai_type'].upper()}: {session['project_info']['name']}")
        print(f"  {analysis['summary']}")
        print(f"  Perspectives: {', '.join(analysis['perspectives_present'])}")
        print(f"  Stats: {analysis['stats']}")
