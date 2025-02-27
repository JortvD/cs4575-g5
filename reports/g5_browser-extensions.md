---
author: Jort van Driel, Dorian Erhan, Weicheng Hu, Giannos Rekkas
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

Since its inception, the web has rapidly evolved from a basic information-sharing platform into a profit-driven medium, where online advertising is one of the primary revenue sources. Ads do exist for a reason. They support a significant portion of online content, as most people won't pay real money for most of what they consume. Whether it's a reputable news establishment or a niche blog, every website needs server space and developer support, which requires some degree of financial investment. 

However, the rise of online advertising has had a very negative impact on the users. Their overabundance has made the browsing experience cluttered and intrusive. Even worse is the fact that rely on invasive tracking, which exploits user data without clear consent, and also facilitates the spread of malicious websites. In response, ad blockers have become a critical tool for users aiming to improve their user experience, privacy, and security while browsing. Even the [FBI recommends ad blockers](https://www.standard.co.uk/news/tech/fbi-recommends-ad-blocker-online-scams-b1048998.html) to avoid falling prey to schemes run by potentially fraudulent websites. 

The debate around ad blockers has recently been intensified with Google Chrome’s announcement to weaken and remove many ad-blocking extensions, [including uBlock Origin](https://www.theverge.com/2024/10/15/24270981/google-chrome-ublock-origin-phaseout-manifest-v3-ad-blocker), one of the most widely used and effective ad blockers. This decision has sparked significant backlash from users who rely on these tools to improve their browsing experience. Beyond the implications for user experience and privacy, this move also raises questions about the broader impact of ad blockers on environmental efficiency and energy consumption.

Thus, in this report, we aim to explore the power consumption of web browsers with and without ad blockers. Our hypothesis is that ad blockers reduce power usage by minimizing the number of extra requests and scripts executed during browsing, thereby decreasing the computational workload needed. Some studies have previously examined the power consumption associated with ad blocking[1], and generally found a significant decrease in power consumption when using these extensions, though some exceptions have shown instances of increased consumption. 

# Methodology

This report analyzes the **average power consumption** of web browsers with and without ad blockers. We focus on power consumption as it provides insight into the continuous usage of browsers over time. All measurementes were conducted using [EnergiBridge](https://github.com/tdurieux/EnergiBridge).

For this study, we used Chromium version 135.0.7026.0, as it serves as the foundation for many of the most widely used browsers, including Google Chrome, Microsoft Edge, and Brave, making it a strong representative choice. Testing on Chromium ensures that the results are relevant to a broad range of browsers built on the same engine. The ad blocker tested was uBlock Origin version 1.62.0, one of the most popular extensions, with approximately 39 million users listed in the Chrome Web Store.

### Testing setup
Our study evaluated Chromium's power consumption when browsing websites grouped by advertisement density. We classified websites into three categories — high, medium, and low ad density — with each one containing three different websites.

A **step** is defined as launching Chromium and navigating through all three websites of one category. For each **experimental trial**, we conducted six steps: three (one for each category) with uBlock Origin enabled and three without. To reduce bias, the order of website sets was randomized during each trial. Because hardware temperature can influence power consumption, the very first trial (used as a warm-up) was excluded from the final analysis. In total, we repeated this trial 30 times.

Within each step, the following actions were performed:
1) Launch Chromium through EnergiBridge.
2) Open a new tab with the designated website.
3) Wait 5 seconds to ensure all resources load completely.
4) Close tab.
5) Wait 1 second to allow the tab to close properly.
6) Repeat steps 2–5 for every website in the current set.
7) Close Chromium and wait 5 seconds before continuing to the next step.

After each trial, we reset all caches and user data genereated before continuing to the next one. Note also that we configure the startup of the browser to automatically enable developer mode, a necessary setting for activating uBlock Origin.

Finally, we ensured that configuration settings were kept consistent across the different devices. When executing the experiments we made sure that the laptop was in "zen mode", which included: 
- No unnecessary applications/services running
- All external hardware disconnected from the device
- Notifications turned off
- Stable internet connection over ethernet cable
- Screen brigtness display at 100% 

### Experimental Setup

The experiments were conducted on two different devices, each equipped with distinct operating systems. By testing across multiple configurations, we can identify whether the impact of ad blocking on power usage is consistent or if it varies depending on the system. The specifications for each are specified below:

| Laptop | Acer Nitro V15               |
|--------|------------------------------|
| CPU    | AMD Ryzen 7 7735H            |
| RAM    | 32 GB                        |
| OS     | Fedora Linux 41              |


|     |                              |
|-----|------------------------------|
|     |                              |
|     |                              |
|     |                              | 
|     |                              |


## Results
The replication package for these experiments can be found on the [Github repository](https://github.com/JortvD/cs4575-g5). 


# Conclusions and Future Works

# References
[1] Khan, K. A., Iqbal, M. T., & Jamil, M. (2024). Impact of Ad Blockers on Computer Power Consumption while Web Browsing: A Comparative Analysis. European Journal of Electrical Engineering and Computer Science, 8(5), 18-24.

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
