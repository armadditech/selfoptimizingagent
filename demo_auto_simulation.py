#!/usr/bin/env python3
"""
Live Auto-Simulation Demo Script
Demonstrates the automated customer interaction and self-optimization cycle.
"""

import requests
import time
import json
from datetime import datetime

BASE_URL = "http://localhost:8080"

def print_header(text):
    """Print formatted header."""
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70 + "\n")

def print_section(text):
    """Print section divider."""
    print(f"\n{'─'*70}")
    print(f"  {text}")
    print('─'*70 + "\n")

def start_auto_simulation(interval=5, batch_size=5):
    """Start auto-simulation."""
    print_section("🚀 Starting Auto-Simulation")

    response = requests.post(
        f"{BASE_URL}/api/auto-simulation/start",
        json={"interval": interval, "batch_size": batch_size}
    )

    if response.status_code == 200:
        data = response.json()
        print(f"✅ Auto-simulation started!")
        print(f"   • Interval: {data['interval']} seconds")
        print(f"   • Batch size: {data['batch_size']} interactions")
        print(f"   • Expected rate: ~{batch_size * (60/interval):.0f} interactions/minute")
        return True
    else:
        print(f"❌ Failed to start: {response.text}")
        return False

def get_status():
    """Get current auto-simulation status."""
    response = requests.get(f"{BASE_URL}/api/auto-simulation/status")
    return response.json()

def get_analytics():
    """Get current analytics."""
    response = requests.get(f"{BASE_URL}/api/analytics")
    return response.json()

def get_optimization_history():
    """Get optimization history."""
    response = requests.get(f"{BASE_URL}/api/optimization-history")
    return response.json()

def display_status(status):
    """Display current status."""
    stats = status['stats']

    if status['active']:
        print("📊 Status: 🟢 ACTIVE")
    else:
        print("📊 Status: 🔴 STOPPED")

    print(f"   • Total Interactions: {stats['total_simulated']}")
    print(f"   • Optimizations Run: {stats['total_optimizations']}")

    if stats.get('start_time'):
        start = datetime.fromisoformat(stats['start_time'])
        elapsed = (datetime.now() - start).total_seconds()
        print(f"   • Running Time: {elapsed:.0f}s")

def display_analytics(analytics):
    """Display analytics summary."""
    print("\n📈 Current Metrics:")
    print(f"   • Total Interactions: {analytics['total_interactions']}")
    print(f"   • Satisfaction: {analytics['satisfaction']:.2f}/5.0")
    print(f"   • Resolution Rate: {analytics['resolution_rate']*100:.1f}%")
    print(f"   • Escalation Rate: {analytics['escalation_rate']*100:.1f}%")

    print("\n🎯 Intent Distribution:")
    for intent, count in analytics['by_intent'].items():
        if count > 0:
            pct = (count / analytics['total_interactions']) * 100
            print(f"   • {intent.capitalize()}: {count} ({pct:.1f}%)")

def display_optimization(opt):
    """Display optimization details."""
    print(f"\n⚡ Version {opt['version']} - {opt['timestamp']}")

    if opt.get('issues_found'):
        print("\n   Issues Found:")
        for issue in opt['issues_found']:
            print(f"   • {issue}")

    if opt.get('improvements'):
        print("\n   Improvements Applied:")
        for improvement in opt['improvements']:
            print(f"   • {improvement}")

    print("\n   Performance Change:")
    before = opt['before']
    after = opt['after']

    sat_change = ((after['satisfaction'] - before['satisfaction']) / before['satisfaction']) * 100
    res_change = ((after['resolution'] - before['resolution']) / before['resolution']) * 100

    print(f"   • Satisfaction: {before['satisfaction']:.2f} → {after['satisfaction']:.2f} ({sat_change:+.1f}%)")
    print(f"   • Resolution: {before['resolution']:.1%} → {after['resolution']:.1%} ({res_change:+.1f}%)")

def stop_auto_simulation():
    """Stop auto-simulation."""
    print_section("🛑 Stopping Auto-Simulation")

    response = requests.post(f"{BASE_URL}/api/auto-simulation/stop")

    if response.status_code == 200:
        data = response.json()
        stats = data['stats']
        print(f"✅ Auto-simulation stopped!")
        print(f"\n📊 Final Statistics:")
        print(f"   • Total Interactions: {stats['total_simulated']}")
        print(f"   • Optimizations: {stats['total_optimizations']}")

        if stats.get('start_time'):
            start = datetime.fromisoformat(stats['start_time'])
            end = datetime.fromisoformat(stats['last_activity'])
            duration = (end - start).total_seconds()
            print(f"   • Duration: {duration:.0f}s")
            print(f"   • Average Rate: {stats['total_simulated']/duration:.1f} interactions/second")
        return True
    else:
        print(f"❌ Failed to stop: {response.text}")
        return False

def run_demo(duration=30, update_interval=5):
    """Run a live demonstration."""
    print_header("🤖 Live Auto-Simulation Demo")

    print("This demo will:")
    print("  1. Start auto-simulation")
    print("  2. Monitor progress for 30 seconds")
    print("  3. Display real-time updates")
    print("  4. Show optimization results")
    print("  5. Stop simulation and show summary")

    input("\nPress Enter to start...")

    # Start simulation
    if not start_auto_simulation(interval=3, batch_size=5):
        return

    print(f"\n⏱️  Running for {duration} seconds...")
    print("   (Watch for optimization cycles every 20 interactions)\n")

    # Monitor progress
    last_opt_count = 0
    for i in range(duration // update_interval):
        time.sleep(update_interval)

        # Get current status
        status = get_status()
        analytics = get_analytics()

        print(f"\n⏰ Update #{i+1} ({(i+1)*update_interval}s elapsed)")
        display_status(status)
        display_analytics(analytics)

        # Check for new optimizations
        opt_count = status['stats']['total_optimizations']
        if opt_count > last_opt_count:
            print_section("✨ NEW OPTIMIZATION DETECTED!")
            history = get_optimization_history()
            if history:
                display_optimization(history[-1])
            last_opt_count = opt_count

    # Stop and show final results
    time.sleep(2)
    stop_auto_simulation()

    # Final summary
    print_section("📊 Final Results")

    analytics = get_analytics()
    display_analytics(analytics)

    history = get_optimization_history()
    if history:
        print(f"\n⚡ Optimization History ({len(history)} cycles):")
        for opt in history:
            print(f"\n   Version {opt['version']}:")
            print(f"   • Satisfaction: {opt['before']['satisfaction']:.2f} → {opt['after']['satisfaction']:.2f}")
            print(f"   • Resolution: {opt['before']['resolution']:.1%} → {opt['after']['resolution']:.1%}")

    print_header("✅ Demo Complete!")
    print("The agent successfully:")
    print(f"  • Generated {analytics['total_interactions']} customer interactions")
    print(f"  • Completed {len(history)} optimization cycles")
    print(f"  • Improved performance automatically")
    print("\nThis demonstrates the complete self-optimizing loop!")

if __name__ == "__main__":
    try:
        run_demo(duration=30, update_interval=5)
    except KeyboardInterrupt:
        print("\n\n⚠️  Demo interrupted!")
        stop_auto_simulation()
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to server at http://localhost:8080")
        print("   Make sure the server is running: python app_enhanced.py")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        stop_auto_simulation()
