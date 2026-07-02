"""Vision model client skeletons for chart image analysis."""

from pathlib import Path

from app.models import PatternDetection


class VisionModelClient:
    """Replaceable interface for a vision-language model used to inspect chart images."""

    def __init__(self, model_name: str | None = None) -> None:
        """
        Create a vision model client.

        Args:
            model_name: Optional model identifier used by the vision backend.
        """
        self.model_name = model_name

    def analyze_image(self, image_path: Path) -> list[PatternDetection]:
        """
        Analyze a chart image and return detected price action patterns.

        Args:
            image_path: Path to the chart image to inspect.

        Returns:
            Detected technical patterns and optional confidence scores.
        """
        # TODO: Receive ChartArtifact.image_path from PatternDetector.detect_patterns().
        # TODO: Call self._load_image(image_path) to prepare the model input.
        # TODO: Call self._run_model(image_payload) to obtain the raw response.
        # TODO: Call self._parse_model_output(raw_output) to structure detections.
        # TODO: Return detections to PatternDetector.detect_patterns().
        pass

    def _load_image(self, image_path: Path) -> object:
        """
        Load a chart image into the representation expected by the vision backend.

        Args:
            image_path: Path to a generated candlestick chart image.

        Returns:
            Backend-ready image payload.
        """
        # TODO: Read the chart image from image_path.
        # TODO: Return the image payload to analyze_image().
        pass

    def _run_model(self, image_payload: object) -> object:
        """
        Run the configured vision model on a prepared image payload.

        Args:
            image_payload: Backend-ready chart image payload.

        Returns:
            Raw provider-specific model output.
        """
        # TODO: Use self.model_name to select or configure the model.
        # TODO: Return raw model output to analyze_image().
        pass

    def _parse_model_output(self, raw_output: object) -> list[PatternDetection]:
        """
        Parse raw model output into project pattern detections.

        Args:
            raw_output: Provider-specific model response.

        Returns:
            Structured pattern detections.
        """
        # TODO: Receive raw output from self._run_model().
        # TODO: Extract pattern names, confidence scores, descriptions, and annotations.
        # TODO: Return PatternDetection objects to analyze_image().
        pass
