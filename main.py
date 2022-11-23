#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 09:31:36 2022

Main is the interface for which the project CNN Autoencoder will start

Source: https://medium.com/dataseries/convolutional-autoencoder-in-pytorch-on-mnist-dataset-d65145c132ac

@author: Ross Erskine
"""


import matplotlib.pyplot as plt
import random
import torch
import torch.nn as nn
import numpy as np

# import modules
import Parameters as pr
import ImageGenerator as ig
import CNN_Autoencoder as CAE

############################## Constructors ##################################
params = pr.Paramaters() # Construct Paramaters

test_images = ig.get_test_set()
#filename = '../datasets'
traingen, valgen = ig.train_dataLoader()  # Construct ImageGenerator

loss_fn = torch.nn.MSELoss()

model = CAE.Convolutional_Autoencoder()     # Construct model

optimizer = torch.optim.Adam(model.parameters(),
                             lr=1e-3, 
                             weight_decay=1e-5)

########################### GPU check ########################################
# Check if the GPU is available
device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
#print(f'Selected device: {device}')

# Move both the encoder and the decoder to the selected device
#model.to(device)


########################### Train function ########################################
def train_model(model, dataloader, device, loss_fn, optimizer):
    """ Train model using dataloader return the mean training loss """
    
    #model.train()
    train_loss = []
    for (img, _) in traingen:
        # move tensor to device
        #mg = img.to(device)
        
        #Reconstruction error
        recon = model(img)
        loss = loss_fn(recon, img)
        
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    
    print('\t partial train loss (single batch): %f' % (loss.data))
    train_loss.append(loss.detach().cpu().numpy())
    
    return np.mean(train_loss)

##################### Validation function ###########################


    

########################### plot function ########################################
def plot_outputs(model,n=10):
    """Plots after every epoch"""
    plt.figure(figsize=(16,4.5))
    
    for i in range(n):
      ax = plt.subplot(2,n,i+1)
      img = test_images[i][0].unsqueeze(0)#.to(device)
      model.eval()
      with torch.no_grad():
         rec_img  = model.forward(img)
      plt.imshow(img.cpu().squeeze().numpy(), cmap='gist_gray')
      ax.get_xaxis().set_visible(False)
      ax.get_yaxis().set_visible(False)  
      if i == n//2:
        ax.set_title('Original images')
      ax = plt.subplot(2, n, i + 1 + n)
      plt.imshow(rec_img.cpu().squeeze().numpy(), cmap='gist_gray')  
      ax.get_xaxis().set_visible(False)
      ax.get_yaxis().set_visible(False)  
      if i == n//2:
         ax.set_title('Reconstructed images')
    plt.show()

########################### Train and evaluate ########################################
num_epochs = 30
diz_loss = {'train_loss':[]}
for epoch in range(num_epochs):
   train_loss =train_model(model,device, traingen,loss_fn,optimizer)
   
   print('\n EPOCH {}/{} \t train loss {}'.format(epoch + 1, num_epochs,train_loss))
   diz_loss['train_loss'].append(train_loss)
   plot_outputs(model,n=10)