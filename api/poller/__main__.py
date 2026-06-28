"""Poller CLI: python -m poller --fetch | --compute | --full"""

import argparse
import sys


def main():
    parser = argparse.ArgumentParser(description="SprintSense Poller")
    parser.add_argument("--fetch", action="store_true", help="Phase 1: fetch data from APIs")
    parser.add_argument("--compute", action="store_true", help="Phase 2: compute metrics")
    parser.add_argument("--full", action="store_true", help="Phase 1 + Phase 2")

    args = parser.parse_args()
    if not any([args.fetch, args.compute, args.full]):
        parser.print_help()
        sys.exit(1)

    from api.app import create_app
    app = create_app()

    with app.app_context():
        if args.fetch or args.full:
            from .fetch import run_fetch
            print("=== Phase 1: Fetch ===")
            results = run_fetch()
            total_issues = sum(r["issues"] for r in results.values())
            total_prs = sum(r["prs"] for r in results.values())
            print(f"\nFetch complete: {total_issues} issues, {total_prs} PRs across {len(results)} repos")

        if args.compute or args.full:
            from .compute import resolve_sprints, map_issues_to_sprints, compute_sprint_metrics, compute_engineer_metrics, compute_dora_metrics, detect_alerts, generate_ai_summaries
            print("\n=== Phase 2: Compute ===")
            sprint_map = resolve_sprints()
            print(f"  {len(sprint_map)} sprints resolved")
            mapped = map_issues_to_sprints()
            print(f"  {mapped} issues mapped to sprints")
            metrics = compute_sprint_metrics()
            print(f"  {len(metrics)} sprint metrics computed")
            eng_metrics = compute_engineer_metrics()
            print(f"  {len(eng_metrics)} engineer metrics computed")
            dora = compute_dora_metrics()
            print(f"  {len(dora)} DORA metric sets computed")
            alerts = detect_alerts()
            print(f"  {alerts} alerts detected")
            ai_results = generate_ai_summaries()
            print(f"  {ai_results['generated']} AI summaries generated ({ai_results['skipped']} skipped, {ai_results['errors']} errors)")
            print("\nCompute complete.")


if __name__ == "__main__":
    main()
