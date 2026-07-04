"""Market structure interpretation and structured report generation skeletons."""

from app.schemas import AnalysisReport, PatternDetection


class AnalysisEngine:
    """Interpret detected technical patterns and assemble a market analysis report."""

    def __init__(self) -> None:
        """Create an analysis engine."""
        pass

    def generate_report(
        self,
        ticker: str,
        detections: list[PatternDetection],
    ) -> AnalysisReport:
        """
        Generate a structured analysis report from detected patterns.

        Args:
            ticker: Ticker analyzed in the chart.
            detections: Technical pattern detections from the vision module.

        Returns:
            Structured market analysis report.
        """
        summary = self._summarize_patterns(detections)
        metadata = self._build_report_metadata(detections)

        return AnalysisReport(
            ticker=ticker,
            summary=summary,
            detections=detections,
            metadata=metadata,
        )

    def _summarize_patterns(self, detections: list[PatternDetection]) -> str:
        """
        Summarize detected patterns in plain analysis language.

        Args:
            detections: Technical pattern detections.

        Returns:
            Concise market structure summary.
        """
        if not detections:
            return "No supported price-action patterns were detected."

        pattern_parts: list[str] = []
        for detection in detections:
            if detection.confidence is None:
                pattern_parts.append(detection.name)
            else:
                pattern_parts.append(f"{detection.name} ({detection.confidence:.2f})")

        return "Detected patterns: " + ", ".join(pattern_parts) + "."

    def _build_report_metadata(self, detections: list[PatternDetection]) -> dict[str, object]:
        """
        Build metadata for the final analysis report.

        Args:
            detections: Technical pattern detections included in the report.

        Returns:
            Structured metadata for the analysis report.
        """
        confidences = [
            detection.confidence
            for detection in detections
            if detection.confidence is not None
        ]

        metadata: dict[str, object] = {
            "detection_count": len(detections),
            "pattern_names": [detection.name for detection in detections],
            "has_confidence": bool(confidences),
        }

        if confidences:
            metadata["average_confidence"] = sum(confidences) / len(confidences)

        return metadata
