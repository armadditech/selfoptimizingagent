"""
Learning Engine for self-optimization based on interaction analysis.
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from pathlib import Path
from collections import defaultdict
import statistics


class LearningEngine:
    """Engine that learns from interactions and optimizes agent performance."""

    def __init__(self, config: Dict):
        """
        Initialize learning engine.

        Args:
            config: Optimization configuration
        """
        self.config = config
        self.enabled = config.get("enabled", True)
        self.learning_rate = config.get("learning_rate", 0.01)
        self.min_interactions = config.get("min_interactions_for_learning", 50)

        # Ensure data directories exist
        self.data_dir = Path("data/optimizations")
        self.data_dir.mkdir(parents=True, exist_ok=True)

        self.interactions_file = self.data_dir / "interactions.jsonl"
        self.feedback_file = self.data_dir / "feedback.jsonl"
        self.metrics_file = self.data_dir / "metrics.json"
        self.prompts_file = self.data_dir / "prompt_versions.json"

        # Load existing data
        self.interactions = self._load_interactions()
        self.feedback_map = self._load_feedback()
        self.metrics_history = self._load_metrics()
        self.prompt_versions = self._load_prompt_versions()

    def record_interaction(self, interaction_data: Dict):
        """Record an interaction for learning."""
        if not self.enabled:
            return

        # Append to interactions file
        with open(self.interactions_file, 'a') as f:
            f.write(json.dumps(interaction_data) + '\n')

        self.interactions.append(interaction_data)

    def record_feedback(self, conversation_id: str, feedback_data: Dict):
        """Record customer feedback for a conversation."""
        if not self.enabled:
            return

        feedback_entry = {
            "conversation_id": conversation_id,
            "feedback": feedback_data,
            "timestamp": datetime.now().isoformat()
        }

        # Append to feedback file
        with open(self.feedback_file, 'a') as f:
            f.write(json.dumps(feedback_entry) + '\n')

        self.feedback_map[conversation_id] = feedback_data

    def analyze_performance(self) -> Dict:
        """
        Analyze recent performance and identify patterns.

        Returns:
            Dictionary with performance insights
        """
        if len(self.interactions) < self.min_interactions:
            return {
                "total_interactions": len(self.interactions),
                "status": "insufficient_data",
                "message": f"Need at least {self.min_interactions} interactions for analysis"
            }

        # Calculate key metrics
        recent = self._get_recent_interactions(days=7)

        total = len(recent)
        escalated = sum(1 for i in recent if i.get("escalated", False))
        confidences = [i["confidence"] for i in recent if "confidence" in i]
        response_times = [i["response_time"] for i in recent if "response_time" in i]

        # Get feedback metrics
        resolved_count = 0
        ratings = []
        for interaction in recent:
            conv_id = interaction.get("conversation_id")
            if conv_id in self.feedback_map:
                feedback = self.feedback_map[conv_id]
                if feedback.get("resolved"):
                    resolved_count += 1
                if feedback.get("rating"):
                    ratings.append(feedback["rating"])

        insights = {
            "total_interactions": total,
            "escalation_rate": escalated / total if total > 0 else 0,
            "avg_confidence": statistics.mean(confidences) if confidences else 0,
            "avg_response_time": statistics.mean(response_times) if response_times else 0,
            "resolution_rate": resolved_count / total if total > 0 else 0,
            "avg_rating": statistics.mean(ratings) if ratings else 0,
            "period": "7 days"
        }

        # Analyze by intent
        intent_analysis = self._analyze_by_intent(recent)
        insights["by_intent"] = intent_analysis

        # Identify problem areas
        insights["problem_areas"] = self._identify_problem_areas(recent)

        # Save metrics
        self._save_metrics(insights)

        return insights

    def run_ab_tests(self) -> Dict:
        """
        Run A/B tests on different response strategies.

        Returns:
            Dictionary with test results
        """
        if not self.config.get("ab_testing", {}).get("enabled", False):
            return {}

        results = {}

        # Example: Test different response styles
        # In production, this would compare actual variants
        recent = self._get_recent_interactions(days=7)

        if len(recent) < self.config["ab_testing"].get("min_sample_size", 100):
            return {"status": "insufficient_data"}

        # Simulate A/B test results
        # In production, track actual variants
        results["response_style"] = {
            "variant_a": {"conversion": 0.75, "satisfaction": 4.2},
            "variant_b": {"conversion": 0.82, "satisfaction": 4.5},
            "winner": "variant_b",
            "lift": 0.07,
            "confidence": 0.95
        }

        return results

    def optimize_prompts(self) -> Dict:
        """
        Optimize system prompts based on performance data.

        Returns:
            Dictionary with optimization results
        """
        if not self.config.get("auto_update_prompts", False):
            return {}

        insights = self.analyze_performance()

        if insights.get("status") == "insufficient_data":
            return {}

        optimizations = {}

        # Analyze each intent's performance
        for intent, metrics in insights.get("by_intent", {}).items():
            if metrics["escalation_rate"] > 0.2:  # High escalation rate
                # Suggest prompt improvement
                optimizations[intent] = {
                    "issue": "high_escalation_rate",
                    "current_rate": metrics["escalation_rate"],
                    "suggestion": "Add more specific examples and handling strategies",
                    "improvement": 0.15  # Expected improvement
                }

            elif metrics["avg_confidence"] < 0.6:  # Low confidence
                optimizations[intent] = {
                    "issue": "low_confidence",
                    "current_confidence": metrics["avg_confidence"],
                    "suggestion": "Provide more detailed guidelines and examples",
                    "improvement": 0.20
                }

        # Save prompt version
        if optimizations:
            self._save_prompt_version(optimizations)

        return optimizations

    def get_learning_insights(self) -> Dict:
        """Get insights about what the agent has learned."""
        return {
            "total_interactions": len(self.interactions),
            "total_feedback": len(self.feedback_map),
            "prompt_versions": len(self.prompt_versions),
            "learning_enabled": self.enabled,
            "last_analysis": self._get_last_analysis_time()
        }

    def _get_recent_interactions(self, days: int = 7) -> List[Dict]:
        """Get interactions from the last N days."""
        cutoff = datetime.now() - timedelta(days=days)

        recent = []
        for interaction in self.interactions:
            try:
                timestamp = datetime.fromisoformat(interaction["timestamp"])
                if timestamp >= cutoff:
                    recent.append(interaction)
            except (KeyError, ValueError):
                continue

        return recent

    def _analyze_by_intent(self, interactions: List[Dict]) -> Dict:
        """Analyze performance broken down by intent."""
        by_intent = defaultdict(lambda: {
            "count": 0,
            "escalated": 0,
            "confidences": [],
            "response_times": []
        })

        for interaction in interactions:
            intent = interaction.get("intent", "unknown")
            by_intent[intent]["count"] += 1

            if interaction.get("escalated", False):
                by_intent[intent]["escalated"] += 1

            if "confidence" in interaction:
                by_intent[intent]["confidences"].append(interaction["confidence"])

            if "response_time" in interaction:
                by_intent[intent]["response_times"].append(interaction["response_time"])

        # Calculate averages
        results = {}
        for intent, data in by_intent.items():
            results[intent] = {
                "count": data["count"],
                "escalation_rate": data["escalated"] / data["count"] if data["count"] > 0 else 0,
                "avg_confidence": statistics.mean(data["confidences"]) if data["confidences"] else 0,
                "avg_response_time": statistics.mean(data["response_times"]) if data["response_times"] else 0
            }

        return results

    def _identify_problem_areas(self, interactions: List[Dict]) -> List[Dict]:
        """Identify areas needing improvement."""
        problems = []

        by_intent = self._analyze_by_intent(interactions)

        for intent, metrics in by_intent.items():
            if metrics["escalation_rate"] > 0.3:
                problems.append({
                    "area": intent,
                    "issue": "high_escalation_rate",
                    "severity": "high",
                    "metric_value": metrics["escalation_rate"]
                })

            if metrics["avg_confidence"] < 0.5:
                problems.append({
                    "area": intent,
                    "issue": "low_confidence",
                    "severity": "medium",
                    "metric_value": metrics["avg_confidence"]
                })

        return problems

    def _load_interactions(self) -> List[Dict]:
        """Load interaction history."""
        interactions = []
        if self.interactions_file.exists():
            with open(self.interactions_file, 'r') as f:
                for line in f:
                    try:
                        interactions.append(json.loads(line.strip()))
                    except json.JSONDecodeError:
                        continue
        return interactions

    def _load_feedback(self) -> Dict:
        """Load feedback map."""
        feedback_map = {}
        if self.feedback_file.exists():
            with open(self.feedback_file, 'r') as f:
                for line in f:
                    try:
                        entry = json.loads(line.strip())
                        feedback_map[entry["conversation_id"]] = entry["feedback"]
                    except (json.JSONDecodeError, KeyError):
                        continue
        return feedback_map

    def _load_metrics(self) -> List[Dict]:
        """Load metrics history."""
        if self.metrics_file.exists():
            try:
                with open(self.metrics_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return []
        return []

    def _load_prompt_versions(self) -> List[Dict]:
        """Load prompt version history."""
        if self.prompts_file.exists():
            try:
                with open(self.prompts_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return []
        return []

    def _save_metrics(self, metrics: Dict):
        """Save metrics to history."""
        metrics["timestamp"] = datetime.now().isoformat()
        self.metrics_history.append(metrics)

        with open(self.metrics_file, 'w') as f:
            json.dump(self.metrics_history, f, indent=2)

    def _save_prompt_version(self, optimizations: Dict):
        """Save a new prompt version."""
        version = {
            "version": len(self.prompt_versions) + 1,
            "timestamp": datetime.now().isoformat(),
            "optimizations": optimizations
        }

        self.prompt_versions.append(version)

        with open(self.prompts_file, 'w') as f:
            json.dump(self.prompt_versions, f, indent=2)

    def _get_last_analysis_time(self) -> Optional[str]:
        """Get timestamp of last analysis."""
        if self.metrics_history:
            return self.metrics_history[-1].get("timestamp")
        return None
