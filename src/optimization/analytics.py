"""
Analytics module for tracking and visualizing agent performance.
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from pathlib import Path
from collections import defaultdict
import statistics


class Analytics:
    """Analytics engine for tracking agent performance."""

    def __init__(self, config: Dict):
        """
        Initialize analytics engine.

        Args:
            config: Analytics configuration
        """
        self.config = config
        self.enabled = config.get("enabled", True)

        # Ensure data directory exists
        self.data_dir = Path("data/analytics")
        self.data_dir.mkdir(parents=True, exist_ok=True)

        self.events_file = self.data_dir / "events.jsonl"
        self.interactions_file = self.data_dir / "interactions.jsonl"
        self.feedback_file = self.data_dir / "feedback.jsonl"

    def log_event(self, event_type: str, data: Dict):
        """
        Log an analytics event.

        Args:
            event_type: Type of event
            data: Event data
        """
        if not self.enabled:
            return

        event = {
            "type": event_type,
            "timestamp": datetime.now().isoformat(),
            "data": data
        }

        with open(self.events_file, 'a') as f:
            f.write(json.dumps(event) + '\n')

    def log_interaction(
        self,
        conversation_id: str,
        intent: str,
        confidence: float,
        response_time: float,
        escalated: bool = False
    ):
        """Log a customer interaction."""
        if not self.enabled:
            return

        interaction = {
            "conversation_id": conversation_id,
            "intent": intent,
            "confidence": confidence,
            "response_time": response_time,
            "escalated": escalated,
            "timestamp": datetime.now().isoformat()
        }

        with open(self.interactions_file, 'a') as f:
            f.write(json.dumps(interaction) + '\n')

    def log_feedback(self, feedback_data: Dict):
        """Log customer feedback."""
        if not self.enabled:
            return

        feedback_data["timestamp"] = datetime.now().isoformat()

        with open(self.feedback_file, 'a') as f:
            f.write(json.dumps(feedback_data) + '\n')

    def get_summary(self, days: int = 7) -> Dict:
        """
        Get analytics summary for the specified period.

        Args:
            days: Number of days to analyze

        Returns:
            Summary dictionary with key metrics
        """
        cutoff = datetime.now() - timedelta(days=days)

        interactions = self._load_recent_data(self.interactions_file, cutoff)
        feedback = self._load_recent_data(self.feedback_file, cutoff)
        events = self._load_recent_data(self.events_file, cutoff)

        # Calculate metrics
        total_interactions = len(interactions)
        escalated_count = sum(1 for i in interactions if i.get("escalated", False))

        confidences = [i["confidence"] for i in interactions if "confidence" in i]
        response_times = [i["response_time"] for i in interactions if "response_time" in i]

        # Feedback metrics
        ratings = [f["rating"] for f in feedback if "rating" in f and f["rating"]]
        resolved = sum(1 for f in feedback if f.get("resolved", False))

        # Intent breakdown
        intent_counts = defaultdict(int)
        for interaction in interactions:
            intent_counts[interaction.get("intent", "unknown")] += 1

        summary = {
            "period_days": days,
            "generated_at": datetime.now().isoformat(),

            "overview": {
                "total_interactions": total_interactions,
                "total_conversations": len(set(i.get("conversation_id") for i in interactions)),
                "total_feedback_responses": len(feedback)
            },

            "performance": {
                "avg_confidence": statistics.mean(confidences) if confidences else 0,
                "avg_response_time_seconds": statistics.mean(response_times) if response_times else 0,
                "escalation_rate": escalated_count / total_interactions if total_interactions > 0 else 0,
                "resolution_rate": resolved / len(feedback) if feedback else 0
            },

            "satisfaction": {
                "avg_rating": statistics.mean(ratings) if ratings else 0,
                "total_ratings": len(ratings),
                "rating_distribution": self._get_rating_distribution(ratings)
            },

            "intents": {
                "breakdown": dict(intent_counts),
                "top_intent": max(intent_counts.items(), key=lambda x: x[1])[0] if intent_counts else "none"
            },

            "trends": self._calculate_trends(interactions, feedback)
        }

        return summary

    def get_intent_analytics(self, intent: str, days: int = 30) -> Dict:
        """Get detailed analytics for a specific intent."""
        cutoff = datetime.now() - timedelta(days=days)
        interactions = self._load_recent_data(self.interactions_file, cutoff)

        intent_interactions = [i for i in interactions if i.get("intent") == intent]

        if not intent_interactions:
            return {
                "intent": intent,
                "status": "no_data",
                "period_days": days
            }

        confidences = [i["confidence"] for i in intent_interactions if "confidence" in i]
        response_times = [i["response_time"] for i in intent_interactions if "response_time" in i]
        escalated = sum(1 for i in intent_interactions if i.get("escalated", False))

        return {
            "intent": intent,
            "period_days": days,
            "total_interactions": len(intent_interactions),
            "avg_confidence": statistics.mean(confidences) if confidences else 0,
            "confidence_std_dev": statistics.stdev(confidences) if len(confidences) > 1 else 0,
            "avg_response_time": statistics.mean(response_times) if response_times else 0,
            "escalation_rate": escalated / len(intent_interactions),
            "daily_volume": self._get_daily_volume(intent_interactions, days)
        }

    def export_data(self, days: int = 30, format: str = "json") -> str:
        """
        Export analytics data.

        Args:
            days: Number of days to export
            format: Export format (json, csv)

        Returns:
            Path to exported file
        """
        cutoff = datetime.now() - timedelta(days=days)

        data = {
            "exported_at": datetime.now().isoformat(),
            "period_days": days,
            "interactions": self._load_recent_data(self.interactions_file, cutoff),
            "feedback": self._load_recent_data(self.feedback_file, cutoff),
            "events": self._load_recent_data(self.events_file, cutoff)
        }

        export_file = self.data_dir / f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{format}"

        if format == "json":
            with open(export_file, 'w') as f:
                json.dump(data, f, indent=2)
        else:
            # CSV export would go here
            pass

        return str(export_file)

    def _load_recent_data(self, file_path: Path, cutoff: datetime) -> List[Dict]:
        """Load data from file since cutoff date."""
        if not file_path.exists():
            return []

        data = []
        with open(file_path, 'r') as f:
            for line in f:
                try:
                    entry = json.loads(line.strip())
                    timestamp = datetime.fromisoformat(entry.get("timestamp", ""))
                    if timestamp >= cutoff:
                        data.append(entry)
                except (json.JSONDecodeError, ValueError):
                    continue

        return data

    def _get_rating_distribution(self, ratings: List[int]) -> Dict:
        """Get distribution of ratings."""
        if not ratings:
            return {}

        distribution = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        for rating in ratings:
            if 1 <= rating <= 5:
                distribution[rating] += 1

        return distribution

    def _calculate_trends(self, interactions: List[Dict], feedback: List[Dict]) -> Dict:
        """Calculate performance trends."""
        if len(interactions) < 2:
            return {"status": "insufficient_data"}

        # Sort by timestamp
        sorted_interactions = sorted(
            interactions,
            key=lambda x: datetime.fromisoformat(x["timestamp"])
        )

        # Split into two halves for comparison
        mid = len(sorted_interactions) // 2
        first_half = sorted_interactions[:mid]
        second_half = sorted_interactions[mid:]

        def calc_metrics(data):
            confidences = [i["confidence"] for i in data if "confidence" in i]
            response_times = [i["response_time"] for i in data if "response_time" in i]
            escalated = sum(1 for i in data if i.get("escalated", False))

            return {
                "avg_confidence": statistics.mean(confidences) if confidences else 0,
                "avg_response_time": statistics.mean(response_times) if response_times else 0,
                "escalation_rate": escalated / len(data) if data else 0
            }

        first_metrics = calc_metrics(first_half)
        second_metrics = calc_metrics(second_half)

        return {
            "confidence_change": second_metrics["avg_confidence"] - first_metrics["avg_confidence"],
            "response_time_change": second_metrics["avg_response_time"] - first_metrics["avg_response_time"],
            "escalation_rate_change": second_metrics["escalation_rate"] - first_metrics["escalation_rate"],
            "overall_trend": "improving" if (
                second_metrics["avg_confidence"] > first_metrics["avg_confidence"] and
                second_metrics["escalation_rate"] < first_metrics["escalation_rate"]
            ) else "declining" if (
                second_metrics["avg_confidence"] < first_metrics["avg_confidence"] or
                second_metrics["escalation_rate"] > first_metrics["escalation_rate"]
            ) else "stable"
        }

    def _get_daily_volume(self, interactions: List[Dict], days: int) -> Dict:
        """Get daily interaction volume."""
        daily_counts = defaultdict(int)

        for interaction in interactions:
            try:
                timestamp = datetime.fromisoformat(interaction["timestamp"])
                date_key = timestamp.strftime("%Y-%m-%d")
                daily_counts[date_key] += 1
            except (KeyError, ValueError):
                continue

        return dict(daily_counts)
