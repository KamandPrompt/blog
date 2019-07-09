---
author: Rishi Sharma
title: What the Flag (WTF) 2019 Editorial
toc: true
toc_label: "On this page"
---

Editorials for What the Flag 2019. 

### Level 0 - Direct key
This one was a free point to everyone who participated. But, there was a catch. This level was not displayed when you viewed all the levels. You had to seperately execute this one. I had almost missed it and realized this only after looking at the scoreboard.


### Level 1 - Page Source
The content of the page was Lorem text. But the crack was to look at the page source. The key was directly given there. 

It wasn't visible on the page because the colour was white and rotated by 180 degrees. 


### Level 2 - PNG as SVG
You are given a file ```ctf.svg```. But the file wasn't opening. Opening on a text editor would also display gibberish.

There's a great tool available for Linux and Mac users to tackle this. Go to the terminal and type ```file <filename>```. This gives the details of the filetype.

Using this for the given file, one can easily observe that it is a ```PNG``` file and not an ```SVG``` file. Change the extension of the file and there you have it - your key to Level 2.


### Level 3 - Stylesheet
The clue has the crack. ```This is a **beautiful** page```. This clearly mentions that this level has to do something with the stylesheet.

Looking into the page source, you can find that the stylesheet is ```level2.css```. The easiest way to it is through the Developer Tools. Then if you are a Google Chrome user, go to sources and you will find the stylesheet. There would be a similar option in other web browsers. The key is given inside the stylesheet, just search for ```wtf```.

### Level 4 - XOR:
If you read the clue, everything is mentioned there. The string has been XOR encrypted with a Byte Key, and the resulting hex code is given. But the Byte Key is not given and with a simple calculation, you can conclude that there can be 2<sup>8</sup> Byte Keys. But the only way to solve this is by Brute Forcing.

[CyberChef](https://gchq.github.io/CyberChef/) is a wonderful platform for handling these kinds of Decryptions. There is directly as option for XOR-Brute Force. Paste the input(Remember to remove the 0x at the start!). Create the Recipe. And in the Brute Force result, search for ```wtf```. You will find the key: `wtf{y0u_kN0w_X02}`.

### Level 5 - Binary File:
You get a binary file, that does not execute. Running the ```file``` command on the given file would also show that it is a ELF-64 bit binary file, which is fine.

Open the file in a text editor. Most of it would be gibberish. But wait, there could be something hidden. There are multiple ways to go around this. The easiest being the ```strings``` command in the terminal. Run ```strings blame``` and you'll find all the valid strings in the file. A hex-code catches the eye. Convert the hex-code to text using [CyberChef](https://gchq.github.io/CyberChef/) and you're done. Key: `wtf{Ex0dia_h@1_aa_r4ha}`


### Level 6 - Scavenger Hunt:
Okay, I must confess. This was my favorite one. The hardest too. Mostly because there's no mention what to do. Only #549 and A4 building and a. The clue wasn't of much help. There was no useful QR Code in the A4 building.

Read the Clue again. Confess!! Yes. ```IIT Mandi Confessions #549```. This one was a long planned one. Go to the Shehtoot Tree and scan the QR Code. Now, the only thing one had to do was to follow the sequence given in the Confession. The first number of the tuple is the word number, the second number is the letter number. 


### Level 7 - RSA Challenge:
For this question, I suppose the best editorial is given in [this](https://medium.com/@peterjson/applying-fermats-little-theorem-in-rsa-challenge-864b4c456185) Medium Article. I solved it using this. I don't suppose I can explain any better.


### Level 8 - Cookie Editing:
The clue mentions that the admin access is not granted but you have to log in. Check out the cookies using the Inspect Element of the Browser.
You'll find a cookie named similar to ```logged_in``` which is set to False. You just have to set this to True. Install ```EditThisCookie``` extension on Chrome and you'll easily by able to change it. Reload! and you have the key. 


### Level 9 - Blocked Terminal Commands:
When you SSH into the system, you'll find the key file easily. But when you try to open it, you'll get notified that this is not the key. Try some other commands to open it or some other files, you'll get the same message. This means that someone messed up with Bash commands.

Two ways to solve this:
- Copy all the files to your system and open them easily to find the key.
- Funny thing, you can open ```fish``` terminal from inside ```bash``` on the system itself for which the commands aren't blocked. Easiest way to get the key(I did this).

### Level 10 - Roman to ASCII:
I don't suppose much explanation is needed for this. The ```A```s in the clue are the separators. Convert the Roman to ASCII codes and then to a string. You'll have your key.

### Level 11 - Git History and XOR Filter:
As you unzip the file, you'll find there is only one README file. Enter ```ls -la``` in the terminal. A ```.git``` folder shows up. 

Check out ```git log```.  You'll find 3 commits in the log. Go to the previous commit using ```git reset --hard HEAD~1```. A file name ```gitbit``` shows up. Enter ```file gitbit``` and it you get to see that it a ```PNG``` file. Open it and you'll find it empty. One way to get the key is to fiddle with the colour settings of the image. Another way is to use an application: ```stegsolve```. This allows you to apply predefined filters on the images. Apply XOR filter, squeeze your eyes a little bit and you'll see a pattern in the image ```957```. That is the key for this level. 