from torch import nn
from darknet import Darknet
from torchvision import transforms, models


# z = nn.Sequential(
#     nn.Conv2d(3, 16, 5),
#     nn.MaxPool2d(2),
#     nn.Conv2d(16, 400, 5),
#     nn.Conv2d(400, 400, 1),
#     nn.Conv2d(400, 4, 1),
# )
# Original darknet, strange output-pred.shape=6,10647,85, low memory
# model = Darknet("cfg/yolov3.cfg")
# model.load_weights(args.weightsfile)
# Resnet with last layer change
# model = models.resnet18(pretrained=True)
# num_ftrs = model.fc.in_features
# model.fc = nn.Linear(25088, 5)
# pretrained_model = torchvision.models.vgg16(pretrained=True)
# modified_pretrained = nn.Sequential(*list(pretrained_model.features.children())[:-1])


class CustomModel(nn.Module):
    def __init__(self):
        super(CustomModel, self).__init__()

        self.net = nn.Sequential(
            nn.Conv2d(3, 16, 5),
            nn.LeakyReLU(),
            nn.Conv2d(16, 400, 5),
            nn.LeakyReLU(),
            nn.MaxPool2d(7),
            nn.Conv2d(400, 400, 5),
            nn.LeakyReLU(),
            nn.Conv2d(400, 5, 1),
        )

    def forward(self, x):
        return self.net.forward(x)


class MyResnet(nn.Module):
    def __init__(self):
        super(MyResnet, self).__init__()
        pretrained_resnet = models.resnet18(pretrained=True)
        self.modified_resnet = nn.Sequential(*list(pretrained_resnet.children())[:-4])
        for param in self.modified_resnet.parameters(): # Freeze
            param.requires_grad = False

        self.conv_addition = nn.Sequential(
            nn.Conv2d(128, 256, 5),
            nn.LeakyReLU(),
            nn.Conv2d(256, 256, 3),
            nn.LeakyReLU(),
            nn.Conv2d(256, 5, 5)
        )

    def forward(self, x):
        x = self.modified_resnet(x)
        x = self.conv_addition(x)
        return x
