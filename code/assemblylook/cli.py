#!/usr/bin/env python3
"""
AssemblyLook CLI - Command-line interface for session tracking
♠️🌿🎸🧵
"""

import sys
from assemblylook.core.session_parser import SessionParser
from assemblylook.core.project_mapper import ProjectMapper
from assemblylook.core.aggregator import SessionAggregator
from assemblylook.core.analyzer import SessionAnalyzer
from assemblylook.visualizer.dashboard import DashboardGenerator


def main():
    """Main CLI entry point."""
    print("♠️🌿🎸🧵 AssemblyLook - G.Music Session Tracker")
    print("=" * 60)

    print("\n[1/5] Parsing sessions...")
    parser = SessionParser()
    sessions = parser.parse_all_sessions()
    print(f"  ✓ Found {len(sessions['claude'])} Claude sessions")
    print(f"  ✓ Found {len(sessions['gemini'])} Gemini sessions")

    print("\n[2/5] Mapping projects...")
    mapper = ProjectMapper()
    enriched = mapper.enrich_sessions(sessions)
    grouped = mapper.group_by_project(enriched)
    print(f"  ✓ Mapped to {len(grouped)} unique projects")

    print("\n[3/5] Analyzing sessions...")
    analyzer = SessionAnalyzer()
    analyzed = analyzer.enrich_sessions_with_analysis(enriched)
    assembly_sessions = analyzer.get_assembly_sessions(analyzed)
    print(f"  ✓ Detected {len(assembly_sessions)} Assembly Mode sessions")

    print("\n[4/5] Aggregating data...")
    aggregator = SessionAggregator()
    by_project = aggregator.aggregate_by_project(analyzed)
    by_date = aggregator.aggregate_by_date(analyzed)
    by_ai = aggregator.aggregate_by_ai(analyzed)
    print(f"  ✓ Organized into {len(by_project)} projects across {len(by_date)} dates")

    print("\n[5/5] Generating dashboard...")
    generator = DashboardGenerator()
    output_path = generator.generate_dashboard(
        analyzed, by_project, by_date, by_ai, assembly_sessions
    )
    print(f"  ✓ Dashboard generated: {output_path}")

    print("\n" + "=" * 60)
    print("✅ AssemblyLook generation complete!")
    print(f"📊 Dashboard: {output_path}")
    print("=" * 60)

    return 0


if __name__ == "__main__":
    sys.exit(main())
