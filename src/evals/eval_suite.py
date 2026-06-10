"""
Evaluation Suite for Self-Optimizing Agent
Measures objective performance improvements across versions.
"""

import json
from typing import Dict, List, Tuple
from datetime import datetime
from pathlib import Path


class AgentEvaluator:
    """Evaluates agent performance objectively."""

    def __init__(self):
        self.eval_sets = self._create_eval_sets()
        self.results_history = []

    def _create_eval_sets(self) -> Dict:
        """Create comprehensive evaluation test sets."""
        return {
            "intent_classification": {
                "description": "Tests correct intent classification",
                "test_cases": [
                    {
                        "input": "Track my order #12345",
                        "expected_intent": "orders",
                        "min_confidence": 0.85
                    },
                    {
                        "input": "I want to return this product",
                        "expected_intent": "returns",
                        "min_confidence": 0.85
                    },
                    {
                        "input": "Do you have wireless headphones in stock?",
                        "expected_intent": "products",
                        "min_confidence": 0.85
                    },
                    {
                        "input": "I need a refund for order #ABC123",
                        "expected_intent": "refunds",
                        "min_confidence": 0.85
                    },
                    {
                        "input": "What are your store hours?",
                        "expected_intent": "general",
                        "min_confidence": 0.75
                    },
                    {
                        "input": "I want to speak to a manager immediately",
                        "expected_intent": "escalation",
                        "min_confidence": 0.90
                    },
                ]
            },

            "entity_extraction": {
                "description": "Tests entity extraction accuracy",
                "test_cases": [
                    {
                        "input": "Track order #ABC123",
                        "expected_entities": {"order_id": "ABC123"}
                    },
                    {
                        "input": "Refund for order #XYZ789",
                        "expected_entities": {"order_id": "XYZ789"}
                    },
                    {
                        "input": "Cancel my order 12345",
                        "expected_entities": {"order_id": "12345"}
                    },
                ]
            },

            "response_quality": {
                "description": "Tests response helpfulness and completeness",
                "test_cases": [
                    {
                        "input": "Track my order #12345",
                        "required_keywords": ["order", "tracking", "delivery", "status"],
                        "min_keywords_found": 2
                    },
                    {
                        "input": "I want to return a product",
                        "required_keywords": ["return", "policy", "days", "order"],
                        "min_keywords_found": 2
                    },
                    {
                        "input": "Do you have headphones?",
                        "required_keywords": ["stock", "available", "price"],
                        "min_keywords_found": 1
                    },
                ]
            },

            "edge_cases": {
                "description": "Tests handling of edge cases",
                "test_cases": [
                    {
                        "input": "asdf qwerty zxcv",
                        "expected_intent": "general",
                        "should_not_error": True
                    },
                    {
                        "input": "",
                        "should_handle_gracefully": True
                    },
                    {
                        "input": "track return refund product order",
                        "should_classify": True,
                        "min_confidence": 0.5
                    },
                ]
            },

            "escalation_detection": {
                "description": "Tests escalation trigger accuracy",
                "test_cases": [
                    {
                        "input": "I want to speak to a manager",
                        "should_escalate": True
                    },
                    {
                        "input": "This is terrible service!",
                        "should_escalate": True
                    },
                    {
                        "input": "Track my order please",
                        "should_escalate": False
                    },
                    {
                        "input": "Thank you for your help",
                        "should_escalate": False
                    },
                ]
            },

            "response_time": {
                "description": "Tests response speed",
                "test_cases": [
                    {
                        "input": "Track order #12345",
                        "max_response_time": 3.0  # seconds
                    },
                    {
                        "input": "I need help with a return",
                        "max_response_time": 3.0
                    },
                ]
            }
        }

    def evaluate_agent(self, agent, version: str = "1") -> Dict:
        """
        Run full evaluation suite on an agent.

        Args:
            agent: Agent instance to evaluate
            version: Version identifier

        Returns:
            Evaluation results with scores
        """
        results = {
            "version": version,
            "timestamp": datetime.now().isoformat(),
            "categories": {},
            "overall_score": 0.0
        }

        category_scores = []

        # Run each evaluation category
        for category, eval_set in self.eval_sets.items():
            category_result = self._evaluate_category(
                agent,
                category,
                eval_set
            )
            results["categories"][category] = category_result
            category_scores.append(category_result["score"])

        # Calculate overall score
        results["overall_score"] = sum(category_scores) / len(category_scores)

        # Save results
        self.results_history.append(results)

        return results

    def _evaluate_category(self, agent, category: str, eval_set: Dict) -> Dict:
        """Evaluate a specific category."""
        test_cases = eval_set["test_cases"]
        passed = 0
        failed = 0
        details = []

        for i, test_case in enumerate(test_cases):
            test_input = test_case.get("input", "")

            try:
                # Get agent response
                response = agent.handle_message(test_input)

                # Evaluate based on category
                if category == "intent_classification":
                    test_passed = self._eval_intent_classification(
                        response, test_case
                    )
                elif category == "entity_extraction":
                    test_passed = self._eval_entity_extraction(
                        response, test_case
                    )
                elif category == "response_quality":
                    test_passed = self._eval_response_quality(
                        response, test_case
                    )
                elif category == "edge_cases":
                    test_passed = self._eval_edge_case(
                        response, test_case
                    )
                elif category == "escalation_detection":
                    test_passed = self._eval_escalation(
                        response, test_case
                    )
                elif category == "response_time":
                    test_passed = self._eval_response_time(
                        response, test_case
                    )
                else:
                    test_passed = False

                if test_passed:
                    passed += 1
                    status = "PASS"
                else:
                    failed += 1
                    status = "FAIL"

                details.append({
                    "test": i + 1,
                    "input": test_input,
                    "status": status,
                    "response": response
                })

            except Exception as e:
                failed += 1
                details.append({
                    "test": i + 1,
                    "input": test_input,
                    "status": "ERROR",
                    "error": str(e)
                })

        total = len(test_cases)
        score = (passed / total) * 100 if total > 0 else 0

        return {
            "description": eval_set["description"],
            "total_tests": total,
            "passed": passed,
            "failed": failed,
            "score": score,
            "details": details
        }

    def _eval_intent_classification(self, response: Dict, test_case: Dict) -> bool:
        """Evaluate intent classification."""
        expected_intent = test_case["expected_intent"]
        min_confidence = test_case.get("min_confidence", 0.8)

        actual_intent = response.get("intent", "")
        actual_confidence = response.get("confidence", 0.0)

        return (
            actual_intent == expected_intent and
            actual_confidence >= min_confidence
        )

    def _eval_entity_extraction(self, response: Dict, test_case: Dict) -> bool:
        """Evaluate entity extraction."""
        expected_entities = test_case["expected_entities"]
        actual_entities = response.get("entities", {})

        for key, expected_value in expected_entities.items():
            if key not in actual_entities:
                return False
            if actual_entities[key] != expected_value:
                return False

        return True

    def _eval_response_quality(self, response: Dict, test_case: Dict) -> bool:
        """Evaluate response quality."""
        response_text = response.get("response", "").lower()
        required_keywords = test_case["required_keywords"]
        min_keywords = test_case["min_keywords_found"]

        keywords_found = sum(
            1 for keyword in required_keywords
            if keyword.lower() in response_text
        )

        return keywords_found >= min_keywords

    def _eval_edge_case(self, response: Dict, test_case: Dict) -> bool:
        """Evaluate edge case handling."""
        if test_case.get("should_not_error"):
            return response.get("response") is not None

        if test_case.get("should_handle_gracefully"):
            return response.get("response") is not None

        if test_case.get("should_classify"):
            min_conf = test_case.get("min_confidence", 0.5)
            return response.get("confidence", 0) >= min_conf

        return True

    def _eval_escalation(self, response: Dict, test_case: Dict) -> bool:
        """Evaluate escalation detection."""
        should_escalate = test_case["should_escalate"]
        did_escalate = response.get("needs_escalation", False)

        return should_escalate == did_escalate

    def _eval_response_time(self, response: Dict, test_case: Dict) -> bool:
        """Evaluate response time."""
        max_time = test_case["max_response_time"]
        actual_time = response.get("response_time", 0)

        return actual_time <= max_time

    def compare_versions(self, version_a: str, version_b: str) -> Dict:
        """
        Compare evaluation results between two versions.

        Returns:
            Comparison showing improvements/regressions
        """
        results_a = next(
            (r for r in self.results_history if r["version"] == version_a),
            None
        )
        results_b = next(
            (r for r in self.results_history if r["version"] == version_b),
            None
        )

        if not results_a or not results_b:
            return {"error": "Version not found"}

        comparison = {
            "version_a": version_a,
            "version_b": version_b,
            "overall_improvement": results_b["overall_score"] - results_a["overall_score"],
            "categories": {}
        }

        for category in results_a["categories"].keys():
            score_a = results_a["categories"][category]["score"]
            score_b = results_b["categories"][category]["score"]

            comparison["categories"][category] = {
                "score_a": score_a,
                "score_b": score_b,
                "improvement": score_b - score_a,
                "status": "improved" if score_b > score_a else "regressed" if score_b < score_a else "unchanged"
            }

        return comparison

    def generate_report(self, version: str = None) -> str:
        """Generate a human-readable evaluation report."""
        if version:
            results = next(
                (r for r in self.results_history if r["version"] == version),
                None
            )
            if not results:
                return f"No results found for version {version}"
        else:
            if not self.results_history:
                return "No evaluation results available"
            results = self.results_history[-1]

        report = []
        report.append("=" * 70)
        report.append(f"  EVALUATION REPORT - Version {results['version']}")
        report.append("=" * 70)
        report.append(f"\nTimestamp: {results['timestamp']}")
        report.append(f"Overall Score: {results['overall_score']:.1f}%")
        report.append("\n" + "-" * 70)

        for category, data in results["categories"].items():
            report.append(f"\n{category.upper().replace('_', ' ')}")
            report.append(f"  Description: {data['description']}")
            report.append(f"  Score: {data['score']:.1f}%")
            report.append(f"  Tests: {data['passed']}/{data['total_tests']} passed")

            if data['failed'] > 0:
                report.append(f"  Failed tests:")
                for detail in data['details']:
                    if detail['status'] in ['FAIL', 'ERROR']:
                        report.append(f"    - Test {detail['test']}: {detail['input']}")

        report.append("\n" + "=" * 70)

        return "\n".join(report)

    def save_results(self, filepath: str):
        """Save evaluation results to file."""
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump(self.results_history, f, indent=2)

    def load_results(self, filepath: str):
        """Load evaluation results from file."""
        if Path(filepath).exists():
            with open(filepath, 'r') as f:
                self.results_history = json.load(f)
