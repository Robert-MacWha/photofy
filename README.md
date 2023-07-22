# Photofy

Photofy works to combat the issue of false information online, specifically with respect to images. In a time of rising uncertainty as to whether information is real or not, Photofy looks to highlight which images can be trusted and to what degree.

## Description
Photofy will highlight what info is true or false in an easily digestible manner. We realise that individuals may not put significant amounts of thought into determining whether an image is genuine or not. 

Using the blockchain, we are able to store a history of each image, who touched it, and which changes have made. Given this, we can generate a rough trustworthiness score to represent how unmodified an image is, thereby combating visual misinformation. 


## Technical Overview
Photofy consists of an on chain database of images that are related to each other based on the modification history of each image. Each graph is created when the image is first captured, either when it is imported into the system by a trusted user, is captured by a camera that imports a chip, or a generative model that implements our protocol.

Whenever changes are made to an image, using software that implements our protocol, we can track each change made to a source image on-chain. Then, when viewing an image, you can query the image database, find out the changes that have been made, and generate a trust score for each image in real-time. 

The trustworthiness score takes into account many considerations such as who the person making the change is and how significant the change to the image is. For example, a journalist at a reputable media organisation making a change to an image’s colour would not be alarming. However, should a non reputable party make drastic changes to the contents of an image, the user ought to be informed. Photofy facilitates this transfer of information. 

Currently worldcoin identities are used to track individual people, and these individuals have trust scores based on decisions made by a trusted group of moderators. In the future, we would integrate into apps like photoshop, GIMP, and other editing softwares to better track the course of an image of an image from capture to completion. 

## EthGlobal Link
(EthGlobal Paris)[]

## Bounties
- Nouns
- Worldcoin
