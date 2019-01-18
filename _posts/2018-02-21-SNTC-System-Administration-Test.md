---
title: SNTC System Administration Test
excerpt: "We have the technology, now we need the enthusiasts."
author_profile: true
author: Sahil Arora
toc: true
toc_label: "On this page"
header:
  overlay_image: "https://media.giphy.com/media/IoP0PvbbSWGAM/giphy.gif"
---

## Introduction

Me and [Shikhar](https://www.facebook.com/shikhar.in) were in our sophomore year when we came across [MetaKGP - The Wikipedia of IIT Kharagpur](https://wiki.metakgp.org/), and we were like **"This is Cool, and we must have such a website for IIT Mandi as well!"**.

![meta-kgp]({{ "/assets/images/meta-kgp.png" | relative_url }} "Meta KGP")

Time flew by, and Programming Club flourished. We both became co-ordinators in our third year for the club and worked hard for people to connect to programming and make cool things. However, this always remained a dream.

With the great help from [Ravi Kumar](https://www.facebook.com/ravisarraf333)(the then general secretary), [Gopal Krishna Agarwal](https://www.facebook.com/gopalkriagg)(the then technical secretary) and Sriram Kailasam sir, we got a new server machine for the institute, just for all the clubs.

Now the problem left for us was how to set up the server so that students who develop stuff can easily share their work with us. Sriram sir was the course instructor for the course System Practicum, and he included a great technology [Docker](https://www.docker.com/), and gave Shikhar a project to setup the server as a part of the course. Shikhar did an amazing job, using Docker, Nginx, etc.

However, there were still a lot of unsolved problems which need to be solved, for instance we wanted to host MediaWiki, Discourse, etc. on the server, and other stuff. And time flew so fast that now we were in our final year and no one else knew how to setup the server! Hence we decided we need to find a team of enthusiastic people who can carry on this task.

## The event

The event was new and simple. We created a set of problems for the students to solve, real life practical problems. We wanted to see how they dedicated they were, how they could find their way through a problem, and how quickly can they learn. We gave them 10 days to solve the problems. You can find the problems here: **<https://github.com/KamandPrompt/sysadmin-test>**

## The problemset and solutions

Here is an overview of the problemset. All the problems were created by me and evaluated by me and Shikhar combined.

### Administration Problem 1

Link to problem: <https://github.com/KamandPrompt/sysadmin-test/blob/master/Problemset/Administration.md>
{: .notice--info}

I encountered this problem when having a discussion with one of my seniors, [Abhishek Pandey](https://www.linkedin.com/in/abhishek-pandey-6b260780/), over the best way to store passwords.

The ideal solution to this problem is to keep the file always encrypted and keep in in sync with some cloud storage, for instance [Dropbox](https://www.dropbox.com). Some of the softwares which already do that are [`CryFS`](https://www.cryfs.org). You could also use a combination of sofwares such as [`encfs`](https://github.com/vgough/encfs) with `dropbox client`. You could also make your own encryption and backup mechanism, such as using GPG for encryption and github for syncronization.

We were looking for a definite and robust way of how to solve it as a user. Some answers stated that we could make a software ourselves, but making our own software is highly cumbersome, hence they lost marks here.

### Administration Problem 2

Link to problem: <https://github.com/KamandPrompt/sysadmin-test/blob/master/Problemset/Administration.md>
{: .notice--info}

This is a pretty straight-forward problem of installation of a software. Those who successfully installed [`streisand`](https://github.com/StreisandEffect/streisand) got 120 marks of 150. The remaining 30 marks were for the documentation and that made the difference in the marks.

### Docker problem

Link to problem: <https://github.com/KamandPrompt/sysadmin-test/blob/master/Problemset/Docker.md>
{: .notice--info}

This is also a pretty straigh-forward problem with the aim to see if students can make an effort to learn a new technology. 100 marks straight for whosoever did it correctly, 35 marks for documentation.

### Networking Problems

Link to problem: <https://github.com/KamandPrompt/sysadmin-test/blob/master/Problemset/Network.md>
{: .notice--info}

All the networking problems were basically to test how well someone can find what he/she is looking for on the internet.

## Submissions

All the submissions for the problems can be found in this `git` repository: **<https://github.com/KamandPrompt/sysadmin-test-submissions/>**.

Overall, we were overwhelmed to see such a great work by the participants. The effort by some of them was truly amazing.

## Results

The problems have been evaluated and you can find the results of the submissions [here](https://docs.google.com/spreadsheets/d/1RQs8HhOSryiueWW_uz1PBUPafeLiTYaVrWN9YYOmaV4/edit?usp=sharing).

The best solutions for each problem have been highlighted so that people can compare their solution to the best solution.

The list of students who have been selected after this is as follows:

1. [Abhigyan Khaund](mailto:b16082@students.iitmandi.ac.in)
2. [Aaditya Arora](mailto:B17071@students.iitmandi.ac.in)
3. [Aditya Singh](mailto:b16085@students.iitmandi.ac.in)
4. [Aman Khandelwal](mailto:amankh1999@gmail.com)
5. [AMRENDRA SINGH](mailto:b16010@students.iitmandi.ac.in)
6. [Dheeraj](mailto:b17041@students.iitmandi.ac.in)
7. [Hitesh Ramchandani](mailto:hitr9831@gmail.com)
8. [Kushagra](mailto:kushagra.s.888@gmail.com)
9. [Sahil Yadav](mailto:sahil_yadav@students.iitmandi.ac.in)
10. [Lakshay arora](mailto:b16060@students.iitmandi.ac.in)
11. [Sai Tarun Reddy Palla](mailto:saitarunreddypalla@gmail.com)
12. [Swapnil Rustagi](mailto:b17104@students.iitmandi.ac.in)
13. [Abhishek](mailto:abhishekbhardwaj540@gmail.com)
14. [Vipul Sharma](mailto:vsvipul555@gmail.com)

Those who have been selected will be contacted personally by email.

For those who were not selected, we thank you for participating and we also look forward to your contribution!