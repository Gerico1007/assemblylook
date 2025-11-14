"""
Perspective Tracker - Granular tracking of individual perspective contributions
♠️🌿🎸🧵

This module provides message-level perspective tracking, creating a "consciousness flow"
view of how different perspectives contribute throughout a session.
"""

import re
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime


class PerspectiveTracker:
    """
    Tracks individual perspective contributions at the message level.

    Creates a detailed timeline showing:
    - Which perspective spoke in each message
    - The content of each perspective's contribution
    - Transitions between perspectives
    - Perspective collaboration patterns
    """

    # Enhanced perspective detection patterns
    PERSPECTIVES = {
        'nyro': {
            'name': 'Nyro',
            'icon': '♠️',
            'patterns': [
                r'♠️\s*Nyro:',
                r'♠️.*Nyro',
                r'\[Nyro\]',
                r'—Nyro(?:\s|$|:)',
            ],
            'themes': ['recursion', 'structure', 'pattern', 'loop', 'architecture'],
        },
        'aureon': {
            'name': 'Aureon',
            'icon': '🌿',
            'patterns': [
                r'🌿\s*Aureon:',
                r'🌿.*Aureon',
                r'\[Aureon\]',
                r'—Aureon(?:\s|$|:)',
            ],
            'themes': ['ground', 'emotional', 'intuitive', 'sacred', 'ceremonial'],
        },
        'jamai': {
            'name': 'JamAI',
            'icon': '🎸',
            'patterns': [
                r'🎸\s*JamAI:',
                r'🎸.*JamAI',
                r'\[JamAI\]',
                r'—JamAI(?:\s|$|:)',
            ],
            'themes': ['rhythm', 'harmony', 'creative', 'musical', 'fugue', 'polyphonic'],
        },
        'synth': {
            'name': 'Synth',
            'icon': '🧵',
            'patterns': [
                r'🧵\s*Synth:',
                r'🧵.*Synth',
                r'\[Synth\]',
                r'—Synth(?:\s|$|:)',
            ],
            'themes': ['synthesis', 'tool', 'execution', 'coordination', 'integration'],
        },
        'mia': {
            'name': 'Mia',
            'icon': '🧠',
            'patterns': [
                r'🧠\s*Mia:',
                r'🧠.*Mia',
                r'\[Mia\]',
                r'—Mia(?:\s|$|:)',
            ],
            'themes': ['technical', 'flow', 'architecture', 'lineage', 'traceable'],
        },
        'miette': {
            'name': 'Miette',
            'icon': '🌸',
            'patterns': [
                r'🌸\s*Miette:',
                r'🌸.*Miette',
                r'\[Miette\]',
                r'—Miette(?:\s|$|:)',
            ],
            'themes': ['simple', 'friendly', 'journal', 'library', 'conversation'],
        },
    }

    def __init__(self):
        """Initialize perspective tracker with compiled regex patterns."""
        self.perspective_regexes = {}
        for key, config in self.PERSPECTIVES.items():
            self.perspective_regexes[key] = [
                re.compile(pattern, re.IGNORECASE | re.MULTILINE)
                for pattern in config['patterns']
            ]

    def detect_perspective_in_message(self, message_text: str) -> Optional[str]:
        """
        Detect which perspective (if any) is speaking in a message.

        Args:
            message_text: The text content of a message

        Returns:
            Perspective key ('nyro', 'aureon', etc.) or None
        """
        for perspective_key, regexes in self.perspective_regexes.items():
            for regex in regexes:
                if regex.search(message_text):
                    return perspective_key
        return None

    def extract_perspective_content(self, message_text: str, perspective: str) -> str:
        """
        Extract the specific content from a perspective's message.

        Tries to isolate the text that comes after the perspective signature.

        Args:
            message_text: The full message text
            perspective: The detected perspective key

        Returns:
            Extracted content (or full message if extraction fails)
        """
        config = self.PERSPECTIVES.get(perspective, {})
        icon = config.get('icon', '')
        name = config.get('name', '')

        # Try to extract content after "Icon Name: " pattern
        pattern = rf'{re.escape(icon)}\s*{re.escape(name)}:\s*(.+?)(?=(?:{"|".join([re.escape(self.PERSPECTIVES[p]["icon"]) for p in self.PERSPECTIVES])}|$))'
        match = re.search(pattern, message_text, re.DOTALL | re.MULTILINE)

        if match:
            return match.group(1).strip()

        # Fallback: return full message
        return message_text

    def analyze_message(self, message: Dict[str, Any], ai_type: str) -> Dict[str, Any]:
        """
        Analyze a single message for perspective information.

        Args:
            message: Message dictionary
            ai_type: 'claude' or 'gemini'

        Returns:
            Dictionary with perspective analysis:
            {
                'has_perspective': bool,
                'perspective': str or None,
                'perspective_name': str or None,
                'perspective_icon': str or None,
                'content': str,
                'extracted_content': str or None,
                'role': str,
                'timestamp': str or None
            }
        """
        # Extract text content
        content = self._extract_message_content(message, ai_type)

        # Detect perspective
        perspective = self.detect_perspective_in_message(content)

        result = {
            'has_perspective': perspective is not None,
            'perspective': perspective,
            'perspective_name': None,
            'perspective_icon': None,
            'content': content,
            'extracted_content': None,
            'role': message.get('role', 'unknown'),
            'timestamp': message.get('timestamp') or message.get('created_at'),
        }

        if perspective:
            config = self.PERSPECTIVES[perspective]
            result['perspective_name'] = config['name']
            result['perspective_icon'] = config['icon']
            result['extracted_content'] = self.extract_perspective_content(content, perspective)

        return result

    def _extract_message_content(self, message: Dict[str, Any], ai_type: str) -> str:
        """Extract text content from a message (handles different AI formats)."""
        if not isinstance(message, dict):
            return str(message)

        if ai_type == 'claude':
            if message.get('type') == 'text':
                return message.get('content', '')
            elif 'content' in message and isinstance(message['content'], str):
                return message['content']
        elif ai_type == 'gemini':
            if 'content' in message:
                return str(message['content'])
            elif 'parts' in message:
                parts_text = []
                for part in message['parts']:
                    if isinstance(part, dict) and 'text' in part:
                        parts_text.append(part['text'])
                return ' '.join(parts_text)

        return ''

    def build_perspective_timeline(self, session: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Build a timeline of perspective contributions throughout a session.

        Args:
            session: Session dictionary with messages

        Returns:
            List of timeline entries with perspective information
        """
        messages = session.get('messages', [])
        ai_type = session.get('ai_type', '')
        timeline = []

        for idx, message in enumerate(messages):
            analysis = self.analyze_message(message, ai_type)

            timeline.append({
                'index': idx,
                'timestamp': analysis['timestamp'],
                'role': analysis['role'],
                'has_perspective': analysis['has_perspective'],
                'perspective': analysis['perspective'],
                'perspective_name': analysis['perspective_name'],
                'perspective_icon': analysis['perspective_icon'],
                'content_preview': analysis['content'][:150] + ('...' if len(analysis['content']) > 150 else ''),
                'full_content': analysis['content'],
                'extracted_content': analysis['extracted_content'],
            })

        return timeline

    def get_perspective_statistics(self, timeline: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calculate statistics about perspective participation.

        Args:
            timeline: Timeline from build_perspective_timeline()

        Returns:
            Statistics dictionary:
            {
                'total_messages': int,
                'perspective_messages': int,
                'perspectives_active': list,
                'perspective_counts': dict,
                'perspective_transitions': list of tuples,
                'collaboration_score': float (0-1)
            }
        """
        total_messages = len(timeline)
        perspective_messages = sum(1 for entry in timeline if entry['has_perspective'])

        # Count per perspective
        perspective_counts = {}
        for entry in timeline:
            if entry['has_perspective']:
                p = entry['perspective']
                perspective_counts[p] = perspective_counts.get(p, 0) + 1

        perspectives_active = list(perspective_counts.keys())

        # Track transitions (when perspective changes)
        transitions = []
        prev_perspective = None
        for entry in timeline:
            if entry['has_perspective']:
                curr_perspective = entry['perspective']
                if prev_perspective and prev_perspective != curr_perspective:
                    transitions.append((prev_perspective, curr_perspective))
                prev_perspective = curr_perspective

        # Collaboration score: 0 = single perspective, 1 = all perspectives equally
        num_perspectives = len(perspectives_active)
        collaboration_score = 0.0
        if num_perspectives > 1:
            # Measure how evenly distributed perspectives are
            if perspective_messages > 0:
                ideal_count = perspective_messages / num_perspectives
                variance = sum(
                    abs(count - ideal_count) / perspective_messages
                    for count in perspective_counts.values()
                )
                collaboration_score = 1.0 - (variance / 2.0)  # Normalize

        return {
            'total_messages': total_messages,
            'perspective_messages': perspective_messages,
            'perspectives_active': perspectives_active,
            'perspective_counts': perspective_counts,
            'perspective_transitions': transitions,
            'collaboration_score': round(collaboration_score, 2),
        }

    def enrich_session_with_perspective_timeline(self, session: Dict[str, Any]) -> Dict[str, Any]:
        """
        Add perspective timeline to a session.

        Args:
            session: Session dictionary

        Returns:
            Session enriched with 'perspective_timeline' and 'perspective_stats' fields
        """
        timeline = self.build_perspective_timeline(session)
        stats = self.get_perspective_statistics(timeline)

        session['perspective_timeline'] = timeline
        session['perspective_stats'] = stats

        return session


if __name__ == "__main__":
    # Quick test
    from assemblylook.core.session_parser import SessionParser

    print("Testing PerspectiveTracker...")

    tracker = PerspectiveTracker()

    # Test detection
    test_messages = [
        "♠️ Nyro: I see the recursion loop you've built...",
        "🎸 JamAI: The pattern rhythm here is beautiful...",
        "🌿 Aureon: What grounds this technically sophisticated architecture...",
        "Regular message without perspective",
        "🧠 Mia: So the technical flow is...",
    ]

    print("\nTesting perspective detection:")
    for msg in test_messages:
        perspective = tracker.detect_perspective_in_message(msg)
        print(f"  '{msg[:50]}...' -> {perspective}")

    # Test with real sessions
    parser = SessionParser()
    sessions = parser.parse_all_sessions()

    all_sessions = sessions.get('claude', []) + sessions.get('gemini', [])

    if all_sessions:
        print(f"\nEnriching {len(all_sessions)} sessions with perspective timelines...")
        for session in all_sessions[:3]:  # Test first 3
            enriched = tracker.enrich_session_with_perspective_timeline(session)
            stats = enriched.get('perspective_stats', {})
            print(f"\n  Session: {session.get('project_info', {}).get('name', 'unknown')}")
            print(f"    Perspectives: {stats.get('perspectives_active', [])}")
            print(f"    Collaboration score: {stats.get('collaboration_score', 0)}")
    else:
        print("\nNo sessions found to test.")
