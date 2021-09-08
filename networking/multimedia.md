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
- Networked multimedia applications can be divided into 3 broad categories: **streaming stored audio/video**, **conversational voice/video-over-IP**, and **streaming live audio/video**. Each one of these categories has its own restrictions and challenges.

#### Streaming Stored Audio and Video:
- We will focus on streaming video (which mostly also contain audio). Streaming stored audio is similar to streaming stored video but at a lower bit rate!
- YouTube and Netflix are classic applications for streaming stored video. Prerecorded video content is stored in some server somewhere and users send requests to view such content.
- Streaming stored video has three main characteristics:
	- *Streaming*: The user starts playing the video shortly after video content is received. The user can continue to play the video while later parts of the video are being received. This is as opposed to first downloading the video file and then playing it.
	- *Interactivity*: The user can pause, play, fast forward, etc.
	- *Continuous playout*: This probably refers to freezes experienced when data hasn't been downloaded "no buffering".
- A good streamed video is one with a good average throughput which at least equal to the bit rate of the streamed video. Prefetching and buffering (we will see these later) allow for continuous playout even when throughput fluctuates but with the condition that the average rate (over 5 to 10 seconds stays higher than the video's bitrate).

#### Conversational Voice- and Video-over-IP:
- Conversational voice over the Internet is also called *Internet telephony* as it acts as a transmitter of voice just like a telephone does. It is also commonly called **voice-over-IP (VoIP)**. It often involves video as well and involve more than just two users but many (in so-called teleconferences).
- Conversational VoIP applications needs to pay close attention to two requirements:
	- *Timing considerations*: These applications are *delay sensitive*. A conversation can be become really hard if it experiences delays more than 400 milliseconds as the user cannot know if their interlocutor is still listening or has already started speaking. The user starts speaking only to receive the voice of the interlocutor and then apologizes, etc. 
	- *Loss tolerance*: Conversational applications can tolerate occasional loss of data which appears in the form of video and audio glitches such as those of Skype.
- Conversational VoIP applications are the opposite of elastic applications such as websites and email. The latter can tolerate a lot of delay, but cannot tolerate data loss.

#### Streaming Live Audio and Video:
- This is like broadcasting TV/radio, but over the Internet. It allows for live transmission of audio/video. 
- Live streaming is delivered through application-level multicast (By CDNs) or through "multiple separate unicast streams".
- Live streaming of video is largely similar to streaming audio/video, but with a little time constraint. Since it's live, the video being streamed needs to be available almost immediately, but while conversational VoIP has a timing constraint of a coupe 100 milliseconds, a live streamed video can have 10 seconds or more of delay and be still usable.

## Streaming Stored Videos:

## Voice-over-IP:

## Protocols for Real-Time Conversational Applications:

## Network Support for Multimedia:
