"""Vision model client for chart image pattern detection."""

from pathlib import Path
from typing import Any


DEFAULT_MODEL_PATH = (
    Path(__file__).resolve().parents[2]
    / "models"
    / "foduucom_stockmarket_pattern_detection_yolov8"
    / "model.pt"
)


class VisionModelClient:
    """YOLO-backed client used to inspect chart images for price-action patterns."""

    def __init__(self, model_name: str | None = None) -> None:
        """
        Create a vision model client.

        Args:
            model_name: Optional path to a YOLO model weights file.
        """
        self.model_path = Path(model_name) if model_name else DEFAULT_MODEL_PATH
        self._model: Any | None = None

    def analyze_image(self, image_path: Path) -> object:
        """
        Analyze a chart image and return raw model output.

        Args:
            image_path: Path to the chart image to inspect.

        Returns:
            Raw provider-specific model output.
        """
        image_payload = self._load_image(image_path)
        return self._run_model(image_payload)

    def _load_image(self, image_path: Path) -> Path:
        """
        Load a chart image into the representation expected by the vision backend.

        Args:
            image_path: Path to a generated candlestick chart image.

        Returns:
            Backend-ready image payload.
        """
        image_path = Path(image_path)
        if not image_path.exists():
            raise FileNotFoundError(f"Chart image does not exist: {image_path}")

        if not image_path.is_file():
            raise ValueError(f"Chart image path is not a file: {image_path}")

        return image_path

    def _run_model(self, image_payload: Path) -> object:
        """
        Run the configured vision model on a prepared image payload.

        Args:
            image_payload: Backend-ready chart image payload.

        Returns:
            Raw provider-specific model output.
        """
        model = self._get_model()
        return model(str(image_payload), verbose=False)

    def _get_model(self) -> object:
        """
        Load and cache the configured YOLO model.

        Returns:
            Loaded Ultralytics YOLO model.
        """
        if self._model is not None:
            return self._model

        if not self.model_path.exists():
            raise FileNotFoundError(
                f"Vision model weights not found: {self.model_path}"
            )

        try:
            from ultralytics import YOLO
        except ImportError as exc:
            raise RuntimeError(
                "ultralytics is required to run the vision model."
            ) from exc

        self._model = YOLO(str(self.model_path))
        return self._model
