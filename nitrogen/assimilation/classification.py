from pathlib import Path
import torch
from torchvision import transforms

# load model
model = torch.hub.load("pytorch/vision:v0.8.1", "resnet18", pretrained=True)
model.eval()

# preprocess image transformation
preprocess = transforms.Compose(
    [
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ]
)

# load labels
with open(Path(__file__).parent / "imagenet_classes.txt") as f:
    categories = [s.strip() for s in f.readlines()]


def predict(input_image):
    input_tensor = preprocess(input_image)
    # create a mini-batch as expected by the model
    input_batch = input_tensor.unsqueeze(0)
    with torch.no_grad():
        output = model(input_batch)
    probabilities = torch.nn.functional.softmax(output[0], dim=0)
    # get the top5 categories
    top5_prob, top5_catid = torch.topk(probabilities, 5)
    # return the top 1 prediction
    return {"prediction": categories[top5_catid[0]], "probability": top5_prob[0].item()}
