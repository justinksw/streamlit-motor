import copy
import pickle
import numpy as np

import torch
from torch import nn

import librosa
import librosa.display
from sklearn.preprocessing import MinMaxScaler


# DEVICE = "mps"
# torch.manual_seed(0)


# class AI_Model:
#     def __init__(self, encoder_pt, deconde_pt, latent_dims=100):

#         self.vae = VAE(latent_dims=latent_dims, device=DEVICE)
#         self.vae.to(DEVICE)

#         self.vae.encoder.load_state_dict(
#             torch.load(
#                 encoder_pt,
#                 map_location=torch.device(DEVICE),
#                 weights_only=True,
#             ),
#         )
#         self.vae.decoder.load_state_dict(
#             torch.load(
#                 deconde_pt,
#                 map_location=torch.device(DEVICE),
#                 weights_only=True,
#             ),
#         )
#         self.vae.eval()

#     @staticmethod
#     def get_feature(data):
#         S = librosa.feature.melspectrogram(
#             y=data,
#             sr=25600,
#             n_fft=2048,  # seg length, default 2048
#             hop_length=200,  # default 512
#             n_mels=128,  # Y-axis, Number of mel-filter band
#             # fmax=1000  # Highest frequency in Hz, default sr // 2
#         )
#         S_db = librosa.power_to_db(S, ref=np.max)[:, :-1]
#         feature = copy.deepcopy(S_db)
#         # feature = copy.deepcopy(S)
#         h, w = feature.shape

#         scaler = MinMaxScaler((-1.0, 1.0))

#         # normalize the 2d array along the axis=0, each column
#         normalized = scaler.fit_transform(feature)
#         normalized_ = normalized.reshape(1, h, w)

#         return normalized_

#     def anomaly_detection(self, data):

#         # == Calculate the anomaly score == #
#         data = torch.from_numpy(data)

#         sample = data.unsqueeze(0).to(torch.float32).to(DEVICE)

#         # sample = tensor
#         # sample.shape = torch.Size([1, 1, 128, 128])

#         with torch.no_grad():
#             mu, log_var, z = self.vae.encoder(sample)

#             data_hat = self.vae.decoder(z)[0]
#             data = data.to(torch.float32).to(DEVICE)

#             score = ((data - data_hat) ** 2).sum().mean()
#             score = score.cpu().detach().numpy()

#         return score


class Encoder(nn.Module):
    def __init__(self, latent_dims, device):
        super(Encoder, self).__init__()
        self.device = device

        def cnn_block(in_chan, out_chan, kernel=3, stride=2, padding=1):
            seq = []
            seq += [
                nn.Conv2d(
                    in_chan,
                    out_chan,
                    kernel_size=kernel,
                    stride=stride,
                    padding=padding,
                    bias=False,
                )
            ]
            seq += [nn.BatchNorm2d(out_chan)]
            seq += [nn.ReLU(inplace=True)]
            return nn.Sequential(*seq)

        self.cnn1 = cnn_block(1, 16)
        self.cnn2 = cnn_block(16, 32)
        self.cnn3 = cnn_block(32, 64)
        self.cnn4 = cnn_block(64, 128)
        self.cnn5 = cnn_block(128, 256, padding=0)

        self.lin = nn.Sequential(
            nn.Flatten(start_dim=1),
            nn.Linear(256 * 3 * 3, 256),
            nn.ReLU(True),
        )

        self.linear1 = nn.Linear(256, latent_dims)
        self.linear2 = nn.Linear(256, latent_dims)

        self.kl = 0

    @staticmethod
    def resample(mu, log_var):
        std = torch.exp(0.5 * log_var)  # e^(1/2 * log(std^2))
        eps = torch.randn_like(std)  # random ~ N(0, 1), size~=std
        z = eps * std + mu
        return z

    def forward(self, x):
        x = x.to(self.device)

        x = self.cnn1(x)
        x = self.cnn2(x)
        x = self.cnn3(x)
        x = self.cnn4(x)
        x = self.cnn5(x)

        x = self.lin(x)

        mu = self.linear1(x)
        log_var = self.linear2(x)

        z = self.resample(mu, log_var)

        self.kl = -0.5 * torch.sum(1 + log_var - mu.pow(2) - log_var.exp())
        return mu, log_var, z


class Decoder(nn.Module):
    def __init__(self, latent_dims, device):
        super(Decoder, self).__init__()
        self.device = device

        self.lin = nn.Sequential(
            nn.Linear(latent_dims, 256),
            nn.ReLU(True),
            nn.Linear(256, 256 * 3 * 3),
            nn.ReLU(True),
            nn.Unflatten(dim=1, unflattened_size=(256, 3, 3)),
        )

        def cnnT_block(
            in_chan, out_chan, kernel=3, stride=2, padding=1, output_padding=1
        ):
            seq = []
            seq += [
                nn.ConvTranspose2d(
                    in_chan,
                    out_chan,
                    kernel_size=kernel,
                    stride=stride,
                    padding=padding,
                    output_padding=output_padding,
                    bias=False,
                )
            ]
            seq += [nn.BatchNorm2d(out_chan)]
            seq += [nn.ReLU(inplace=True)]
            return nn.Sequential(*seq)

        self.cnnT1 = cnnT_block(256, 128, padding=0)
        self.cnnT2 = cnnT_block(128, 64)
        self.cnnT3 = cnnT_block(64, 32)
        self.cnnT4 = cnnT_block(32, 16)

        self.cnnT5 = nn.Sequential(
            nn.ConvTranspose2d(16, 1, 3, stride=2, padding=1, output_padding=1),
            nn.Sigmoid(),
        )

    def forward(self, x):
        x = x.to(self.device)

        x = self.lin(x)

        x = self.cnnT1(x)
        x = self.cnnT2(x)
        x = self.cnnT3(x)
        x = self.cnnT4(x)

        x = self.cnnT5(x)
        return x


class VAE(nn.Module):
    def __init__(self, latent_dims, device):
        super(VAE, self).__init__()
        self.device = device
        self.encoder = Encoder(latent_dims, device)
        self.decoder = Decoder(latent_dims, device)

    def forward(self, x):
        x = x.to(self.device)

        _, _, z = self.encoder(x)
        x_ = self.decoder(z)

        return x_


def processing(data):

    data = data[int(50000 * 0.1) : int(50000 * 0.1) + int(50000 * 0.66)]

    S = librosa.feature.melspectrogram(
        y=data,
        sr=50000,
        n_fft=2048,  # seg length, default 2048
        hop_length=256,  # default 512
        n_mels=128,  # Y-axis, Number of mel-filter band
        # fmax=1000  # Highest frequency in Hz, default sr // 2
    )

    feature = librosa.power_to_db(S, ref=np.max)[:, :-1]
    h, w = feature.shape

    # For VAE
    scaler = MinMaxScaler()  # [0, 1]

    normalized = scaler.fit_transform(feature.reshape(-1, 1))
    normalized_ = normalized.reshape(1, h, w)

    return normalized_


def calculate_abnomaly_score(signal):

    data = processing(signal)

    device = torch.device("mps")
    vae = VAE(latent_dims=4, device=device)
    vae.to(device)

    vae.encoder.load_state_dict(
        torch.load(
            "./data/vae/encoder1_data_normal.pt",
            map_location=torch.device("mps"),
            weights_only=False,
        )
    )
    vae.decoder.load_state_dict(
        torch.load(
            "./data/vae/decoder1_data_normal.pt",
            map_location=torch.device("mps"),
            weights_only=False,
        )
    )

    vae.eval()

    # data.shape: torch.Size([1, 128, 128])
    # sample.shape: torch.Size(1, 1, 128, 128)

    data = torch.from_numpy(data)

    sample = data.unsqueeze(0).to(torch.float32).to(device)

    with torch.no_grad():
        mu, log_var, z = vae.encoder(sample)

        data_hat = vae.decoder(z)[0]
        data = data.to(torch.float32).to(device)

        score = ((data - data_hat) ** 2).sum().mean()
        score = score.cpu().detach().numpy()

    return score


def diagnose(signal):

    data = processing(signal)

    device = torch.device("mps")
    vae = VAE(latent_dims=4, device=device)
    vae.to(device)

    vae.encoder.load_state_dict(
        torch.load(
            "./data/vae/encoder1_alldata_trainset.pt",
            map_location=torch.device("mps"),
            weights_only=False,
        )
    )
    vae.decoder.load_state_dict(
        torch.load(
            "./data/vae/decoder1_alldata_trainset.pt",
            map_location=torch.device("mps"),
            weights_only=False,
        )
    )

    vae.eval()

    # data.shape: torch.Size([1, 128, 128])
    # sample.shape: torch.Size(1, 1, 128, 128)

    data = torch.from_numpy(data)

    sample = data.unsqueeze(0).to(torch.float32).to(device)

    with torch.no_grad():
        mu, log_var, z = vae.encoder(sample)
        z = z.cpu().detach().numpy()

    with open("./data/vae/svm.pickle", "rb") as f:
        classifer = pickle.load(f)

    prediction = classifer.predict(z)[0]

    classes = [
        "Normal",
        "Misalignment",
        "Imbalance",
        "Bearing Ball Defect",
        "Bearing Cage Defect",
        "Bearing Outer-race Defect",
    ]

    return classes[prediction]
