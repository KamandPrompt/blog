---
author: CrackTheCode
title: Crack The Code (CTF) 2019 Editorial
toc: true
toc_label: "On this page"
---

Editorials for Crack the Code 2019. 

Crack The Code 2019 is available at http://ctciitmandi.herokuapp.com for practice. 

There is a common username and password for everyone -
email: guest@students.iitmandi.ac.in<br>
password: guest


### Level 1 - Blank html page
The contents of the page were styled to be hidden with the CSS's
display: none;
property for large display. Either find the key in the source for the page OR open the page on a mobile device OR use developer tools to view it on a small display on any mobile browser. Basically, the key is hidden in base64 encoded text in the source code.


### Level 2 - Samuel Morse.
You've to read the personal page, as the question says - review his personal page!

You'll find an article with heading *amet* which has some proper english describing the 1's and 0's.
It is simple Morse code with "-" (dash) replaced with 1 (trying to represent as binary.) and "." (dot) replaced with a 0.

Translate it with any online translator and get the key.


### Level 3 - Robots
The page and the question have 'robot', 'robots' all over them. This was to make you look for the robots.txt file which every standard site has.
Here that site/page being /fsociety/robots.txt where, as stated in the question, no. of **Allow**ed queries multiplied by no. of **Disallow**ed queries **converted** to hex code (since the robot lord loves square of square of 2 = 16 -> hex code) is the key.

Dab is Illuminati, as stated there itself was just for fun and had nothing to do with the question.

P.S. - I am not a member of Illuminati.

### Level 4 - Stay/Go:

As the name suggests, it is a Stego (Steganography) challenge, use binwalk to inspect the file,

![]({{ "/assets/images/ctf.png" | relative_url }})

As we can see, the image has JPEG file concatenated with a Zip archive.
Simply perform binwalk -e eso.jpg and you ‘ll get a zip file.

Extract the zip, open the QR code, scan it, it leads to a link.

The link has weird + and > symbols, that is the esoteric part. This is written in a language called brainfck, go to ideone.com and paste that code with language set as brainfck, you’ll get the flag : `crackthecode{th3_Sl@p_0f_H1mal@ya}`

### Level 5 - Search Engine:

That questions says a search engine is able to crawl. So you need to see how a search engine crawls. You will find that they crawl using bots. So you need to make the webpage feel like you're a search engine, that you can do by an user-agent. So you had to change your user-agent to bingbot's user agent - which's exact string you can find on the internet easily.



### Level 6 - RSA:

Suppose Ash wants to send a message to Josh without anyone else knowing the contents.
Josh will generate a public key and a private key using RSA. Then he will send his public key to Ash, Ash can encrypt the message using the public key and send it to Josh. 

If m is the message,

	c = Encrypted message  = (m^e) % n
	(n,e) is the PUBLIC key

After receiving, Josh will decrypt the message using his private key, since no other person has access to the private key, only Josh can see the decrypted message

	Decrypted (original) message = (c^d) % n
	d is the PRIVATE key

To find public and private keys:

1. Select two prime numbers p & q
2. Calculate n = p\*q
3. Choose an integer e such that:
	1. `e is not a factor of n`
	2. `1 < e < Φ(n) = (p-1)*(q-1)`,
	Φ(n) is euler’s totient function

* PUBLIC KEY is (n,e)

* PRIVATE KEY is `d = (k*Φ(n) + 1) / e`, k is an integer chosen so as to make the numerator divisible by e.


In our problem, we know the Public key (in the file publickeyz.pem)
Thus, we know n and e. But, to calculate Φ(n) from n is physically impossible because n is very large.

The observation that in this case, e = 3 can be helpful.

As I wrote above, c = m^e % n, if m and e are turn out to be such that me is smaller than n, we may be able to reverse this equation (please verify that it is not possible when me  is larger than n).

That means
	
	m may be equal to c^(1/e) %n
	
In this case, since e is 3, we can perform this attack (aka CUBE ROOT ATTACK)

and we find out that indeed, we get the flag: `crackthecode{Exodia_1$_C0m1n9!}`

PFA the [code for decryption](({{ "/assets/files/CrackTheCode/decrypt.py" | relative_url }})). Study the encrypt.py file first, then come to the decrypt file.

NOTE:

1. Real life RSA cases use padding to make attacks difficult (even if e is small), this was just a toy example to introduce RSA.

2. Some of you might be thinking that how can you take exponents on strings? python’s bytes_to_long function comes to rescue, binary equivalent of ASCII code of each char is concatenated to form the number, google for more.


### Level 7 - Bores code:

Only five functions are relevant in the CPP file : encrypt, \_encrypt, decrypt, \_decrypt, repeat

encrypt:
	Checks if the text is already encrypted or not.

\_encrypt:
	It has three parts:

	Part 1:
		Take every char of the string and work with its ASCII code in binary
		e.g., ‘A’ = 65 = 01000001
		We treat the whole string as a concatenation of binary representations
		e.g., ‘ABC’ = 01000001 01000010 01000011
		And record the positions at which 1 is present in the binary string.
		This record is stored in obj1

	Part 2:
		obj1 is shuffled randomly into obj2
	
	Part 3:
		Entries from obj2 are used to create dashes and dots.

So, the reversing of this will be in opposite order.

To decrypt:

	Part 1:
		Convert from dots and dashes to a numerical array
	
	Part 2:
		sort the array

	Part 3:
		use the array in part one to mark 1’s in a binary string and convert it to characters.
		e.g. [1,2,7,10,15,17,23] ->
		       01000001 01000010 01000011 = ‘ABC’

PFA the code for decryption. Study the encrypt.cpp file first, then come to the [decrypt file]({{ "/assets/files/CrackTheCode/decode_reverse.py" | relative_url }}).
