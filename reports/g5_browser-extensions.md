---
author: Weicheng Hu, Jort, Dorian, Giannos
title: "Investigating how plug-ins in browsers affect energy consumption"
image: "../img/p1_measuring_software/gX_template/cover.png"
date: 28/02/2025
summary: |-
  This study evaluates the energy consumption of a chosen web browser under different configurations and environments. 
  Specifically, we compare Chrome with three conditions: uBlock Origin on/off. Then we compare the power use across different websites,
  where each website has many/moderate/almost no ads. uBlock Origin is an extension that blocks advertisements during navigation for users.
  The goal is to assess how these extensions impact power usage.
---

## Introduction
Online advertising has become one of the primary revenue streams for many websites. However, ads are not just an avenue for monetization; they also influence the user experience in numerous ways. Some users find ads annoying, or they worry about tracking and privacy, which leads to growing popularity of ad-blocking software. Due to the increasing demands for add-free, concerns about performance impacts, such as increased CPU usage, slower loading times, and higher battery consumption on devices might be a concern in the field of sustainable engineering. 

Although some studies have looked at performance changes associated with ad blocking[1], fewer have examined how the amount of advertisements could affect energy consumption. Moreover, there is no mentions among the studies that they take external factors that might affect the experiments into account. For example, making sure the room temperature is constant, connecting to the same wifi/power supply during the experiment. Meanwhile, we will be using a different energy measurement framework called EnergiBridge[2] to reduce biases.



--- 

## Methodologies
- describe how the script works?

---

## Experiments and results

###  Experimental Setup
- baseline: visiting websites with no extensions
- Device detail(CPU/RAM/Operating System...)
- Number of epoches
- Controlled variables: room temperature, device temperature, no other windows open...(or keep constant during the experiment)
- the metrics we use: Joules, Watts(?), percentage increasing/decreasing in energy consumption against baseline
### Results
- Normally distributed -> use mean and std to generate a plot
- Otherwise: Try remove the anomaly, significance tests if not applicable

## Conclusions and Future Works
- number of ads affect the energy consumption
- The extension increases energy consumption if the website does not have advertisements
- In percentage, extension on is the most effective when there are moderate number of ads
- posible reasons: 


## References
[1] Khan, K. A., Iqbal, M. T., & Jamil, M. (2024). Impact of Ad Blockers on Computer Power Consumption while Web Browsing: A Comparative Analysis. European Journal of Electrical Engineering and Computer Science, 8(5), 18-24.

[2] EnergiBridge (2024). https://github.com/tdurieux/EnergiBridge
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
