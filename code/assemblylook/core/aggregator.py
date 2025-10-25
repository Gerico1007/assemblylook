"""
Aggregator - Merge and organize sessions across AI types
♠️🌿🎸🧵
"""

from typing import Dict, List, Any
from datetime import datetime
from collections import defaultdict


class SessionAggregator:
    """Aggregates and organizes sessions across multiple dimensions."""

    def aggregate_by_project(self, sessions: Dict[str, List[Dict[str, Any]]]) -> Dict[str, Dict[str, Any]]:
        """
        Aggregate sessions by project with rich metadata.

        Returns:
            Dictionary mapping project names to aggregated data:
            {
                'project_name': {
                    'sessions': [...],
                    'total_sessions': int,
                    'claude_sessions': int,
                    'gemini_sessions': int,
                    'first_activity': timestamp,
                    'last_activity': timestamp,
                    'total_messages': int,
                    'project_info': {...}
                }
            }
        """
        aggregated = {}
        all_sessions = sessions.get('claude', []) + sessions.get('gemini', [])

        # Group by project name
        by_project = defaultdict(list)
        for session in all_sessions:
            project_info = session.get('project_info', {})
            project_name = project_info.get('name', 'unknown')
            by_project[project_name].append(session)

        # Build aggregated data for each project
        for project_name, project_sessions in by_project.items():
            # Sort sessions by timestamp (most recent first)
            sorted_sessions = sorted(
                project_sessions,
                key=lambda s: s.get('first_timestamp') or '',
                reverse=True
            )

            # Count by AI type
            claude_count = sum(1 for s in project_sessions if s['ai_type'] == 'claude')
            gemini_count = sum(1 for s in project_sessions if s['ai_type'] == 'gemini')

            # Get timestamps
            timestamps = [s.get('first_timestamp') for s in project_sessions if s.get('first_timestamp')]
            first_activity = min(timestamps) if timestamps else None
            last_activity = max(timestamps) if timestamps else None

            # Total messages
            total_messages = sum(s.get('message_count', 0) for s in project_sessions)

            # Get project info from first session
            project_info = sorted_sessions[0].get('project_info', {}) if sorted_sessions else {}

            aggregated[project_name] = {
                'sessions': sorted_sessions,
                'total_sessions': len(project_sessions),
                'claude_sessions': claude_count,
                'gemini_sessions': gemini_count,
                'first_activity': first_activity,
                'last_activity': last_activity,
                'total_messages': total_messages,
                'project_info': project_info
            }

        # Sort projects by last activity
        return dict(sorted(
            aggregated.items(),
            key=lambda item: item[1]['last_activity'] or '',
            reverse=True
        ))

    def aggregate_by_date(self, sessions: Dict[str, List[Dict[str, Any]]]) -> Dict[str, List[Dict[str, Any]]]:
        """
        Aggregate sessions by date.

        Returns:
            Dictionary mapping dates (YYYY-MM-DD) to lists of sessions
        """
        by_date = defaultdict(list)
        all_sessions = sessions.get('claude', []) + sessions.get('gemini', [])

        for session in all_sessions:
            timestamp = session.get('first_timestamp')
            if timestamp:
                try:
                    # Extract date from ISO timestamp
                    date = timestamp.split('T')[0] if 'T' in timestamp else timestamp[:10]
                    by_date[date].append(session)
                except Exception:
                    by_date['unknown'].append(session)
            else:
                by_date['unknown'].append(session)

        # Sort sessions within each date
        for date in by_date:
            by_date[date].sort(
                key=lambda s: s.get('first_timestamp') or '',
                reverse=True
            )

        return dict(sorted(by_date.items(), reverse=True))

    def aggregate_by_ai(self, sessions: Dict[str, List[Dict[str, Any]]]) -> Dict[str, Any]:
        """
        Aggregate sessions by AI type with statistics.

        Returns:
            Dictionary with claude and gemini statistics
        """
        claude_sessions = sessions.get('claude', [])
        gemini_sessions = sessions.get('gemini', [])

        return {
            'claude': {
                'sessions': sorted(
                    claude_sessions,
                    key=lambda s: s.get('first_timestamp') or '',
                    reverse=True
                ),
                'total': len(claude_sessions),
                'total_messages': sum(s.get('message_count', 0) for s in claude_sessions)
            },
            'gemini': {
                'sessions': sorted(
                    gemini_sessions,
                    key=lambda s: s.get('first_timestamp') or '',
                    reverse=True
                ),
                'total': len(gemini_sessions),
                'total_messages': sum(s.get('message_count', 0) for s in gemini_sessions)
            }
        }

    def get_recent_sessions(self, sessions: Dict[str, List[Dict[str, Any]]], limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get the most recent sessions across all AIs.

        Args:
            sessions: Session data
            limit: Maximum number of sessions to return

        Returns:
            List of most recent sessions
        """
        all_sessions = sessions.get('claude', []) + sessions.get('gemini', [])

        sorted_sessions = sorted(
            all_sessions,
            key=lambda s: s.get('first_timestamp') or '',
            reverse=True
        )

        return sorted_sessions[:limit]


if __name__ == "__main__":
    # Quick test
    from assemblylook.core.session_parser import SessionParser
    from assemblylook.core.project_mapper import ProjectMapper

    parser = SessionParser()
    sessions = parser.parse_all_sessions()

    mapper = ProjectMapper()
    enriched = mapper.enrich_sessions(sessions)

    aggregator = SessionAggregator()

    # Test project aggregation
    by_project = aggregator.aggregate_by_project(enriched)
    print(f"\nProjects ({len(by_project)}):")
    for name, data in list(by_project.items())[:5]:
        print(f"  {name}: {data['total_sessions']} sessions, {data['total_messages']} messages")

    # Test date aggregation
    by_date = aggregator.aggregate_by_date(enriched)
    print(f"\nDates ({len(by_date)}):")
    for date, date_sessions in list(by_date.items())[:3]:
        print(f"  {date}: {len(date_sessions)} sessions")

    # Test recent sessions
    recent = aggregator.get_recent_sessions(enriched, limit=5)
    print(f"\nRecent sessions ({len(recent)}):")
    for s in recent:
        print(f"  {s['ai_type']}: {s['project_info']['name']} - {s['first_timestamp']}")
