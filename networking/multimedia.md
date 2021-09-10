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
- Live streaming of video is largely similar to streaming audio/video, but with a little time constraint. Since it's live, the video being streamed needs to be available almost immediately, but while conversational VoIP has a timing constraint of a couple 100 milliseconds, a live streamed video can have 10 seconds or more of delay and be still usable.

## Streaming Stored Videos:
- Streaming video applications such YouTube and Netflix involves having Prerecorded videos stored in servers, and users sending requests to the servers to watch these videos. These videos are also interactive in the sense that the user can stop them before they end, watch their entirety or reposition them to different scenes both forward and backward.
- There are three types of video streaming, **UDP streaming**, **HTTP streaming**, and **adaptive HTTP streaming**, with the latter two being the more common ones, and UDP streaming becoming a legacy technology.
- One very important aspect of video streaming is the use of client video buffering which is used to fix fluctuations in delay and changing bandwidth between the server and client. **Buffering** basically means, the client "build[s] up a reserve of video in an application buffer. Once the client has built up a reserve of several seconds of buffered-but-not-yet-played video, the client can then begin video playout." *Client buffering* offers 2 valuable conveniences: 1) It absorbs the varying delay. 2) If the bandwidth occasionally drops below the consumption rate of the video, the use can keep enjoying a smooth playback of the so-far-buffered content. The following graph sheds some light on why buffering is necessary. The rate at which video blocks arrive at the client can make playing it directly a frustrating experience full of glitches. Buffering takes that mess allow it to be played at the rate it was sent from the server, and at the rate it's to be played in the client.
![Client playout delay during video streaming](img/clientPlayoutDelay.png)

### UDP Streaming:
- A central and interesting feature of UDP streaming is that the server transmits video at a rate "that matches the client’s video consumption rate by clocking out the video chunks over UDP at a steady rate". UDP doesn't have congestion control, so the server can push video bits at the consumption rate of the client. UDP streaming also uses a small client buffer that can hold less than a second of video content.
- The server first uses the *real-time transport protocol (RTP)* (which we will see in conversational apps) to encapsulate video chunks in special transport packets used for transporting video and audio. These packets are then passed to UDP.
- The server also keeps a parallel separate control connection with the client. This control connection is used to send command by the client to the server about state changes such as pause, resume and reposition. This parallel connection is similar to the one used in FTP.
- UDP streaming suffers from 3 main drawbacks, however:
	- The supposed constant-rate streaming of UDP can fail to create continuous playback due to the ever unpredictable an fluctuating available bandwidth.
	- UDP streaming requires a media control server such as *real-time streaming protocol (RSTP)* that keeps track of client-to-server interactivity and state changes in the client for each client. As you can easily tell, this introduces such much overhead, cost and complexity.
	- Many firewalls block UDP, thus preventing users from consuming video streamed over UDP.

### HTTP Streaming:
- In HTTP streaming, a video is stored as a regular file in a server and is given a specific URL. The client establishes a TCP connection with the server, and sends an HTTP GET request to that URL. The server responds by sending the video file immediately or until a congestion (if there is one) is relieved. The client starts collecting bytes from the received video in a buffer and after reaching a certain threshold start playing the video. The application grabs frames from the buffer, decompresses them and starts displaying them on screen!
- TCP suffers from higher delay than UDP due to congestion control and retransmission. It was widely believed that video streaming wouldn't work over TCP; they chose UDP, instead, but they learnt with time that buffering and *prefetching*.
- HTTP over TCP doesn't get blocked by firewalls and NATs like UDP. Another massive advantage of streaming over HTTP is that it doesn't require a media control server such as RTSP, thus making it less costly and less complex. This is why popular streaming services such as YouTube use HTTP streaming.

#### Prefetching Video:
- **Prefetching** simply means the application downloads video at a rate higher than the rate it consumes the video. The prefetched bytes are stored in the client buffer. The client builds a reserve of buffered data, so that if the bandwidth drops momentarily below the consumption rate, the reserved bytes can be still played without freezes. Prefetching is easy to implement with TCP since the latter's congestion avoidance techniques always try to use all available bandwidth. 

#### Client Application Buffer and TCP Buffers:
- The following diagram shows how the client and server interact during HTTP streaming:
![HTTP/TCP stored video streaming](img/TCPHTTPStreaming.png)
- On the server side, the white area in the video file represents the part of the video that has already been sent to the server's socket, while the shaded area in blue represents the remaining parts of the video that hasn't been sent yet. Bytes are placed in a TCP send buffer before being sent to the client. The TCP send buffer is all shaded meaning it's full so the application cannot pass anymore of the video bytes to it through the socket. As for the client side, the client application reads bytes from the TCP receive buffer and puts them in application's buffer. Simultaneously, the application can also grab frames from the application buffer to display them on screen.
- If the client application buffer is larger than the video file, then the streaming of the file is effectively equivalent to a regular file download.
- *(I am  assuming here that the video is larger than the buffer).* What happens when the user stops the video while it's being streamed. buffered bits will not be removed from the buffer after they are displayed on screen, but new bits will keep flowing into the buffer from the server. If the buffer size is "finite" (which usually the case, I believe), the buffer becomes full which causes a "back pressure" that goes all the way back to the server. This back pressure happens in a few steps:
	- When the application buffer becomes full, bytes from the TCP receive buffer destined for the application buffer can no longer be sent to it, so these bytes cannot be removed from the TCP buffer. The latter becomes full too.
	- The server's TCP send buffer cannot send bytes to a full TCP receive buffer. So it becomes full too.
	- The server application cannot send bytes into a socket with a full send buffer, so it's effectively blocked from sending anymore bytes until maybe the user resumes the video.
- An application buffer can become full even without the video being paused. In such a case, too, a back pressure will reverberate back to the server blocking it or slowing its send rate. When the buffer is full, the server send rate can not be larger than the consumption rate of the client, because to receive *ƒ* bits, you need to remove *ƒ* bits from the client buffer. 

#### Early Termination and Repositioning the Video: 
- HTTP streaming services use the **HTTP byte-range header** in HTTP GET requests. This header specifies the byte range the user wants from a given video. When you reposition the video (jump forward), a new HTTP request is sent. This HTTP request indicates in its byte-range header the byte in the video from which the video file should start. When the server receives a new HTTP requests, it forgets all what went before and starts sending bytes starting at the byte indicated in the byte-range header. 
- Early termination of a video and repositioning to a future point in the video results in wasting all previously buffered bytes. This can be very costly. This is the reason why buffers are made small. Small buffers limit the amount of prefetched data that can go unused.

### Adaptive Streaming and DASH:
### Content Distribution Networks:
### Examples: Netflix, YouTube and Kankan: 

## Voice-over-IP:

## Protocols for Real-Time Conversational Applications:

## Network Support for Multimedia:
