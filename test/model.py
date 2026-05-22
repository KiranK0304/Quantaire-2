from huggingface_hub import hf_hub_download

path = hf_hub_download(
    repo_id="foduucom/stockmarket-pattern-detection-yolov8",
    filename="model.pt",
    local_dir="stockmarket-pattern-detection-yolov8"
)

print("Downloaded to:", path)