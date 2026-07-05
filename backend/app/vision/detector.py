"""Technical pattern detection for chart images."""

from pathlib import Path

from app.schemas import PatternDetection
from app.vision.client import VisionModelClient


class PatternDetector:
    """Coordinate chart-image analysis and conversion into structured detections."""

    MIN_CONFIDENCE = 0.25

    def __init__(self, vision_client: VisionModelClient | None = None) -> None:
        """
        Create a pattern detector.

        Args:
            vision_client: Optional vision model client.
        """
        self.vision_client = vision_client or VisionModelClient()

    def detect_patterns(self, image_path: Path) -> list[PatternDetection]:
        """
        Detect technical price action patterns in a chart image.

        Args:
            image_path: Path to a generated candlestick chart.

        Returns:
            Structured pattern detections.
        """
        raw_output = self.vision_client.analyze_image(image_path)
        
        results = list(raw_output)
        if results:
            results[0].save(filename=str(image_path))
            
        detections = self._parse_model_output(results)
        return self._filter_supported_patterns(detections)

    def _parse_model_output(self, raw_output: object) -> list[PatternDetection]:
        """
        Parse raw YOLO model output into project pattern detections.

        Args:
            raw_output: Provider-specific model response from VisionModelClient.

        Returns:
            Structured pattern detections.
        """
        results = list(raw_output)
        if not results:
            return []

        result = results[0]
        names = result.names
        detections: list[PatternDetection] = []

        for box in result.boxes:
            class_id = int(box.cls[0].item())
            class_name = names.get(class_id, str(class_id))
            confidence = float(box.conf[0].item())
            xyxy = [float(value) for value in box.xyxy[0].tolist()]

            detections.append(
                PatternDetection(
                    name=class_name,
                    confidence=confidence,
                    description=f"Detected {class_name} pattern on the chart.",
                    annotations={
                        "class_id": class_id,
                        "box_xyxy": xyxy,
                    },
                )
            )

        return detections

    def _filter_supported_patterns(
        self,
        detections: list[PatternDetection],
    ) -> list[PatternDetection]:
        """
        Filter model detections to the technical patterns supported in Version 1.

        Args:
            detections: Pattern detections returned by the vision client.

        Returns:
            Pattern detections supported by the product scope.
        """
        return [
            detection
            for detection in detections
            if detection.confidence is None or detection.confidence >= self.MIN_CONFIDENCE
        ]
