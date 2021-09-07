# Multimedia Networking:

## Table of Contents:

## Introduction:
- We all want to know how to create a video streaming service or a live video chatting application like Whatsapp!! This chapter will cover the networking issues of transmitting sound and video through the network.
- We will start by dividing networked multimedia services into 3 broad categories and look at the special challenges they pose that differ from traditional elastic applications such as email or web browsing:
	- Streaming stored videos.
	- Conversational voice/video over-IP.
	- Streaming live video/audio.
- We will look at content distribution networks (CDNs) and they are the backbone of streaming services.
- We will take a look at popular streaming services such as Netflix and YouTube. and much more. 

## Multimedia Networking Applications:
- A multimedia applications is any that involves audio or video. In this section we will look at the special characteristics of video and audio that make them different from other types of media, and then we will study the different types of networked multimedia applications.

### Properties of Video:
- The following table shows different types of network applications (around 2012), their bit rate and their bandwidth consumption:

| Application types | Bit rate | Bytes transferred in 67 minutes |
| --- | --- | --- |
| Facebook photos | 160 Kbps | 80 MB | 
| Music streaming | 128 Kpbs | 64 MB | 
| Video streaming | 2 MBbps | 2 GB | 

- Compared to other types of network applications, streaming video has a very high bit rate (more than 10 times), and consumes a huge amount of bandwidth.
- Videos are also excellent candidates for compression. A digital video is a series of still images being displayed at a constant rate of say 60 per second. An image itself is an array of pixels and each pixel is encoded into bits that represent *luminance* (What!! :confused:) and color. Videos contain a lot of redundancy that can be exploited by video compression to get the desired bit rate. There two types of redundancy, *spatial redundancy* which are repeated pixels or patterns within a single image, so if the image is all white, then we can simply indicate somehow that without encoding each pixel with repetitive pixel encoding. *Temporal redundancy* refers to changes in pixel from one frame to the next. If the following frame is the same as the current one, then there is no need include the next frame but simply indicate it's the same as the current one. There are many of the shelf software products that do compression to any bit rate. Video compression, more often than not, results in the reduction of video quality.
- A single video can be compressed into different bit rates and offered to be streamed in all these bit rates. The user can choose the appropriate bit rate that best fit their bandwidth, or the streaming provider can change the bit rate dynamically based on the user's Internet speed.

### Properties of Audio:
- Audio has a much lower bit rate than video, but it also has its own special quirks that make it special. Let's first see how audio is converted from its original analog format to a digital format:
	- Audio is *sampled* :confused: at a fixed rate, e.g. 8000 samples per second. The value of each sample is a real number. 
	- The sample values are rounded to "one of a finite number of values", a process called *quantization*. The number of finite values is a power of 2, for examples there can be 256 quantization values.
	- Each quantization value is represented by a fixed number of bits. If there are 256 quantization values, then each sample is represented by one byte. If an a analog audio sound is sampled at 8000 samples per second and each sample is encoded in 8 bits, the resulting digital signal will have a bit rate of 64,000 bps.
- This encoding technique we just described is called *pulse code modulation*. Audio CDs are encoded using 44,100 samples per second using 16 bits for each sample, which results in a bit rate of 705.6 Kbps for mono and 1.411 Mbps for stereo. 
- PCD is rarely used in the Internet, but it's compressed instead. A popular audio compression that somehow still preserve high audio quality is **MPEG layer 3**, more commonly called **MP3**. MP3 encode to different bit rates, with 128 bps being the most popular as it produces very little degradation.
- People can tolerate video glitches, but are somehow very sensitive to audio glitches. Live or sored videos that have many audio glitches are mostly unusable, while video glitches are OK.

### Types of Multimedia Applications:
- 

## Streaming Stored Videos:

## Voice-over-IP:

## Protocols for Real-Time Conversational Applications:

## Network Support for Multimedia:
