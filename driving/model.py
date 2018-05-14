import torch.nn as nn

class CNNDriver(nn.Module):
    def __init__(self):
        super(CNNDriver, self).__init__()

        self.layer1 = nn.Sequential(
            nn.Conv2d(3, 24, kernel_size=5, padding=0, stride=2),
            nn.BatchNorm2d(24),
            nn.ReLU()
        )

        self.layer2 = nn.Sequential(
            nn.Conv2d(24, 36, kernel_size=5, padding=0, stride=2),
            nn.BatchNorm2d(36),
            nn.ReLU()
        )

        self.layer3 = nn.Sequential(
            nn.Conv2d(36, 48, kernel_size=5, padding=0, stride=2),
            nn.BatchNorm2d(48),
            nn.ReLU()
        )

        self.layer4 = nn.Sequential(
            nn.Conv2d(48, 64, kernel_size=3, padding=0, stride=1),
            nn.BatchNorm2d(64),
            nn.ReLU()
        )

        self.layer5 = nn.Sequential(
            nn.Conv2d(64, 64, kernel_size=3, padding=0, stride=1),
            nn.BatchNorm2d(64),
            nn.ReLU()
        )

        self.fc1 = nn.Sequential(
            nn.Linear(1152, 1164),
            nn.ReLU(),
            nn.Dropout(p=0.8)
        )

        self.fc2 = nn.Sequential(
            nn.Linear(1164, 100),
            nn.ReLU(),
            nn.Dropout(p=0.8)
        )

        self.fc3 = nn.Sequential(
            nn.Linear(100, 50),
            nn.ReLU(),
            nn.Dropout(p=0.8)
        )

        self.fc4 = nn.Sequential(
            nn.Linear(50, 10),
            nn.ReLU(),
            nn.Dropout(p=0.8)
        )

        self.fc_out = nn.Sequential(
            nn.Linear(10, 1)#,
            #nn.Tanh()
        )
        #self.fc_out = nn.Linear(10,1)

        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                nn.init.kaiming_normal_(m.weight, mode='fan_out', nonlinearity='relu')
            elif isinstance(m, nn.BatchNorm2d):
                nn.init.normal(m.weight, mean=1, std=0.02)
                nn.init.constant_(m.bias, 0)

    def forward(self, x):
        # The expected image size is 66x200
        layer1 = self.layer1(x)
        layer2 = self.layer2(layer1)
        layer3 = self.layer3(layer2)
        layer4 = self.layer4(layer3)
        layer5 = self.layer5(layer4)

        # Reshape layer5 activation to a vector
        layer5_reshape = layer5.view(layer5.size(0), -1)

        fc1 = self.fc1(layer5_reshape)
        fc2 = self.fc2(fc1)
        fc3 = self.fc3(fc2)
        fc4 = self.fc4(fc3)

        #fc_out = self.forward(fc4)
        fc_out = self.fc_out(fc4)
        return fc_out