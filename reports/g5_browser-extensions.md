---
author: Dorian Erhan, Jort van Driel, Giannos Rekkas, Weicheng Hu
title: "Investigating how ad blocker plug-ins in browsers affect energy consumption"
image: "../img/p1_measuring_software/gX_template/cover.png"
date: 28/02/2025
summary: |-
  This study evaluates the energy consumption of web browsers under different configurations and environments. 
  Specifically, we compare Chrome with two conditions: no extension and uBlock Origin on. uBlock Origin serves the purpose of blocking advertisements during navigation for users.
  The goal is to assess how these extensions impact power usage.
---

# Introduction
<!-- This problem takes another level if we are counting on these measurements to make **groundbreaking research contributions** in this area. Some research projects in the past have underestimated this issue and failed to produce replicable findings. Hence, this article presents a roadmap on how to properly set up a scientific methodology to run energy efficiency experiments. It mostly stems from my previous work on [doing research and publishing](/publications) on Green Software.

This article is divided into two main parts: 1) how to set up energy measurements with minimum bias, and 2) how to analyse and take scientific conclusions from your energy measurements.
Read on so that we can get your paper accepted in the best scientific conference. -->

Since its inception, the web has rapidly evolved from a basic information-sharing platform into a profit-driven medium, where online advertising is one of the primary revenue sources. Ads do exist for a reason. They support a significant portion of online content, as most people won't pay real money for most of what they consume. Whether it's a reputable news establishment or a niche blog, every website needs server space and developer support, which requires some degree of monetary investment. 

However, the rise of online advertising has had a very negative impact on the users. Their overabundance has made the browsing experience cluttered and intrusive. Even worse is the fact that rely on invasive tracking, wihch exploits user data without clear consent, and also facilitate the spread of malicious websites. In response, ad blockers have become a critical tool for users aiming to improve their user experience, privacy, and security while browsing. Even the [FBI recommends ad blockers](https://www.standard.co.uk/news/tech/fbi-recommends-ad-blocker-online-scams-b1048998.html) to avoid falling prey to schemes run by potentially fraudulent websites. 

The debate around ad blockers has recently been intensified with Google Chrome’s announcement to weaken and remove many ad-blocking extensions, [including uBlock Origin](https://www.theverge.com/2024/10/15/24270981/google-chrome-ublock-origin-phaseout-manifest-v3-ad-blocker), one of the most widely used and effective ad blockers. This decision has sparked significant backlash from users who rely on these tools to improve their browsing experience. Beyond the implications for user experience and privacy, this move also raises questions about the broader impact of ad blockers on environmental efficiency and energy consumption.

In this report, we aim to explore the energy consumption of web browsers with and without ad blockers. Our hypothesis is that ad blockers reduce energy consumption by minimizing the number of extra requests and scripts executed during browsing, thereby decreasing the computational workload on devices.

# Methodology

Energy consumption was measured using [EnergiBridge](https://github.com/tdurieux/EnergiBridge).

We ensured that configuration settings were kept consistent across the different devices. Aditionally, when executing the experiments we made sure that the laptop was in "zen mode", which included: 
- No unnecessary applications/services running
- All external hardware disconnected from the device
- Notifications turned off
- Stable internet connection over ethernet cable
- Screen brigtness display at 100% 

(Elaborate on this further)
A single step of the experiment consits of navigating to 10 websites in total. These websites were classified into three different sets, according to their ad density (high, medium and low). A step consisted of opening a new Chrome tab, navigating to the respective website and waiting for 5 seconds, in order to ensure that all relevant resources and requests concluded properly. Each step was repeated 30 times. Since energy consumption is affected by hardware temperature, the first step of the experiment was considered as warp-up and was discarded from the results. 


### Hardware set-up

The experiments were conducted on two different devices, each equipped with distinct operating systems. The specifications for each are specified below:

| Laptop | Acer Nitro V15               |
|--------|------------------------------|
| CPU    | AMD Ryzen 7 7735H            |
| RAM    | 32 GB                        |
| GPU    | NVIDIA GeForce RTX 4060 Max-Q|
| OS     | Fedora Linux 41              |


|     |                              |
|-----|------------------------------|
|     |                              |
|     |                              |
|     |                              | 
|     |                              |

(Justification of why the experiments where ran on different devices?)


(Specify version of chrome and ublock used)

##  Experimental Setup

## Results
The experiments can be found on the [Github repository](https://github.com/JortvD/cs4575-g5). 


# Conclusions and Future Works

<!-- #### 👉 Note 1:
If you are a **software developer** enthusiastic about energy efficiency but you are not particularly interested in scientific experiments, this article is still useful for you. It is not necessary to do "everything by the book" but you may use one or two of these techniques to reduce the likelihood of making wrong decisions regarding the energy efficiency of your software.

--- 

## Unbiased Energy Data ⚖️

There are a few things that need to be considered to minimise the bias of the energy measurements. Below, I pinpoint the most important strategies to minimise the impact of these biases when collecting the data.

### Zen mode 🧘🏾‍♀️

The first thing we need to make sure of is that the only thing running in our system is the software we want to measure. Unfortunately, this is impossible in practice – our system will always have other tasks and things that it will run at the same time. Still, we must at least minimise all these competing tasks:

- all applications should be closed, notifications should be turned off;
- only the required hardware should be connected (avoid USB drives, external disks, external displays, etc.);
- turn off notifications;
- remove any unnecessary services running in the background (e.g., web server, file sharing, etc.);
- if you do not need an internet or intranet connection, switch off your network;
- prefer cable over wireless – the energy consumption from a cable connection is more stable than from a wireless connection.

### Freeze your settings 🥶

It is not possible to shut off the unnecessary things that run in our system. Still, we need to at least make sure that they will behave the same across all sets of experiments. Thus, we must fix and report some configuration settings. One good example is the brightness and resolution of your screen – report the exact value and make sure it stays the same throughout the experiment. Another common mistake is to keep the automatic brightness adjustment on – this is, for example, an awful source of errors when measuring energy efficiency in mobile apps.

---

### 

Nevertheless, using statistical metrics to measure effect size is not enough – there should be a discussion of the **practical effect size**. More important than demonstrating that we came up with a new version that is more energy efficient, you need to demonstrate that the benefits will actually be reflected in the overall energy efficiency of normal usage of the software. For example, imagine that the results show that a given energy improvement was only able to save one joule of energy throughout a whole day of intensive usage of your cloud software. This perspective can hardly be captured by classic effect-size measures. The statistical approach to effect size (e.g., mean difference, Cohen's-*d*, and so on) is agnostic of the context of the problem at hand.
 -->
