# 42-FaceGenerator

** You need to be a 42 student to use this project, you will need to log with your student account **

## What is this project ?

The goal of this project is to practice machine learning.

I want a neural network to learn what is the typical face of a 42 student, and give him random data to generate fake pictures of students.

We'll use an autoencoder for that.

## What is an autoencoder ?

I wanted to learn using an autoencoder : it' a neural network that takes an input and learn to compress it.
How does it works ?
It's a regular deep learning network, with layers like this :

Input layer : 1028
Hidden 1 : 64
Hidden 2 : 32
Hidden 3 : 64
Output layer : 1028

Of course number of neurons in each layer can change, but it has to have this double funnel shape.

We train the autoencoder to give as the ouput the same input we provided.

To sum up, the network learn to compress data by preserving data despite dimension reduction.

## Dataset

The dataset will be the pictures of the 42 Paris campus.

They have all the same size (175 pixels x 175 pixels), and more important, they have the same framing and the same background.
We want the neural network to focus only on the student faces, not on the environment, so that's perfect.

The script download_faces.py downloads and cleans the dataset. Be patient it's really slow !

## Dev log

### Jan, 6th

Today I finished to collect data. I have now a full dataset of 3620 175x175 pictures of students (120M).

I made cleanup functions to remove pictures of piscine. We only want pictures of students as they all have exactly the same background which will be a huge advantage for our network ! Some pictures was empty, I removed them too. I also removed bot pictures.

I'am now ready to process this data.

I'll reshape them to 64x64, and normalize pixels value between -1 and 1 to speed convergence up.
