# Security in Computer Networks
## Table of Contents:
## Introduction:
- This chapter will be mainly about secure communication over IP and how to defend it against various types of attacks.
- This chapter will use the famed characters Bob and Alice as two ends of a communication line, and might introduce other characters such as Trudy the intruder. Alice and Bob can be either two routers, a server and a client or two nodes, etc. Alice will be the sender and Bob the receiver, mostly!
- Security can mean a bunch of things, but our focus in this chapter will be about secure communication and security over the network. Topics we will cover include:
	- Communication between Alice and Bob remains secret from busybodies.
	- Bob and Alice are actually communicating with each other, and Trudy is not masquerading as one of them.
	- If communication is tampered with, the tampering is detected.
	- The fundamentals of cryptography, and how cryptography is used to to encrypt communication, authenticate communicators, and maintaining message integrity.
	- How to secure applications, TCP connections, IP and LANs using among cryptography among other things.
	- Organization network security and how it's done through firewalls and intrusion detection systems.

## Network Security:
- **Secure communication** has the following characteristics:
	- **Confidentiality** means only the sender and receiver can understand the meaning of messages they exchange, and no eavesdropper can. This means the messages need to be **encrypted**.
	- **Message integrity** refers to ensuring that a message in transit hasn't been altered either maliciously or accidentally. This is an extension to checksumming, but a more involved one and has to me mainly with security against clever interceptors.
	- **End-point authentication** means the sender and receiver need to first confirm the identities of each other. 
	- **Operational security** is concerned with security in the context of organizations and enterprise networks. Organization networks are prime targets for different types of hacks. To counter such attacks, organizations networks uses *firewalls* and *intrusion detection systems*, which will we see later in this chapter.
- Now that we have an idea about network security, let's have a look at the different ways they can mess with it and exploit it. The following image shows a typical line of communication involving Bob and Alice who exchange data messages and *control messages* (The latter are akin to TCP messages that create or dismantle a connection, but don't carry actual payload). Trudy is an intruder that can do nasty things when the line of communication is not secure.
![Sender, receiver and intruder](img/senderRecIntruder.png)
- Trudy can do the following:
	- **Eavesdropping** which can involve listening to and recording exchanged messages.
	- **Modification, insertion** and **deletion** whole messages or their content.
- Alice and Bob don't necessarily have to be to humans using end systems, but can be devices like routers or switches or anything really!

## Principles of Cryptography:
- Cryptography is a vast field in itself requiring its own book or books. This section will give an overview of important aspects of cryptography and how it's used in networking.
- An important role cryptography plays in secure communication is its role in maintaining confidentiality. Cryptography transforms a message into an unreadable mess that cannot be read by anyone except the receiver of the message. 
- A message in its original form is called **plaintext** or **cleartext**. Alice needs to *encrypt* her message using an **encryption algorithm** before sending it. The encrypted message is called **ciphertext**. 
- Encryption techniques and algorithms are know to everybody, so what is preventing Trudy from breaking Alice's ciphertext if encrypting it is common knowledge? This is the work of so-called keys. Alice, the sender, needs to provide a **key**, ***K<sub>A</sub>***, which is a string of characters and/or numbers as an input to the encryption algorithm. The encryption algorithm takes the cleartext message ***m*** and the key as inputs, and it outputs the ciphertext as an output. We can represent the ciphertext as ***K<sub>A</sub>(m)***, which we obtained by encrypting the message ***m*** using the key ***K<sub>A</sub>***. The Subscript ***A*** refers to Alice. The encryption algorithm is evident from the context. Bob on his part must provide a key ***K<sub>B</sub>*** to the **decryption algorithm**, which takes the ciphertext and the key to produce the original cleartext message. In other words, Bob decrypts the encrypted message ***K<sub>A</sub>(m)*** by computing **K<sub>B</sub>(K<sub>A</sub>(m)) = m**. 
- There are two types of encryption systems based on the keys:
	- **Symmetric key systems**, where Alice and Bob's keys are identical and are also secret.
	- **Public key systems**, where each of the two, Alice and Bob, has two keys, a private key known only to its owner, and a public key known to everybody else.
- We will go into more details on how these two types of keys work.
![Cryptographic components](img/cyptcomponents.png)

### Symmetric Key Cryptography:
#### Caesar Cipher:
- All cryptography involves changing cleartext into a different text using a key. One of the oldest and simplest symmetric key algorithms is the so-called **Caesar cipher**. The Caesar cipher involves shifting each letter in the alphbet by ***k*** positions and allowing for wrap around, meaning the alphabet is a kind of a ring where *z* is followed by *a*. E.g. If we use ***k = 3 *** as our key for Caesar cipher *a* becomes *d*, *b* becomes *e*, *z* becomes *c*, etc. If you know that Caesar cipher is used, it is very easy to break messages encrypted with it because there only 26 letters in the English alphabet.

#### Monoalphabetic Cipher:
- An advanced version of the Caesar cipher is the **monoalphabetic cipher**, which instead of shifting characters by by a uniform ***k*** value, each substitutes another arbitrary letter, but each must have a unique substitute letter, as the following figure shows:
![Monoalphabetic cipher](img/monoalphabetic.png)
- A monoalphabetic cipher is much more robust than a regular Caesar cipher, as brute force breaking it will require 26! or (10<sup>26</sup>) attempts.
- This cipher can however be broken using statistical analysis of letter frequencies. Letters 'e' and 't' occur very frequently. Some other grouping of letters like 'ion', 'ing', and 'the' occur very frequently. If the intruder has some knowledge about the content of the messages such as the names 'Bob' and 'Alice', it would be even easier to break such ciphers. The more the intruder can correctly guess of the these letters and groupings of letters plus the ancillary information about the message contents, the easier it become to brute force the rest. 
- Based on what and how much information the intruder can obtain about a monoalphabetic cipher, she can break the code in one of three ways:
	- *Ciphertext-only attack* happens when the intruder has no external information about the intercepted message except what can be derived from statistical analysis
	- *Known-plaintext attack* happens when the intruder knows some plaintext-ciphertext pairings, like If Trudy knows that 'Alice' and/or 'Bob' for sure occurred in the messages. This can be more severe if Trudy records all the intercepted messages, and then discovers a plaintext version of one of these ciphertexts. This would allow her to know a bunch of letters and then easily break the code.
	- *Chosen-plaintext attack* happens when the intruder decides a plaintext and somehow gets its ciphertext. If Trudy somehow tricks Alice to send "The quick brown fox jumps over the lazy dog" to Bob, then Trudy has managed to completely break the code.

#### Polyalphabetic Encryption:
- Polyalphabetic encryption is also an improvement on monoalphabetic cipher. It uses multiple monoalphabetic ciphers for different letters based on their positions in the text. Take the following figure as an example:
![Polyalphabetic encryption using two Caesar ciphers](img/polyalphabetic.png)
- The figure above has two Caesar ciphers (***k = 5***, and ***k = 19***). We can use the two Caesar ciphers ***C<sub>1</sub>*** and ***C<sub>2</sub>*** in a certain repeating pattern such as ***C<sub>1</sub>, C<sub>2</sub>, C<sub>2</sub>, C<sub>1</sub>, C<sub>2</sub>***. ***C<sub>1</sub>*** uses ***k = 5***, and **C<sub>2</sub>** uses ***k = 19***. What results from this is that the same letter in the ecnrypted messages have different meanings based on its position. *Genius!* This is especially resilient to statistical analysis, it seems. 

#### Block Ciphers:
- Symmetric keys are still used today. Today, two types of symmetric-key based encryption schemes exist, **stream ciphers** which we will see later, and **block ciphers** which we will look at now. Block ciphers are very important in network security. They're used by IPsec, TLS (SSL at the time of the writing of the book) and PGP.
- Block ciphers seem a little similar in principle to monoalphabetic ciphers. In this cipher, a message is processed in blocks of ***k*** bits, and each block is mapped to a different block of ***k*** bits. If we have ***k = 3***, we use a one-to-one mapping that maps 3-bit blocks of plaintext to 3-bit blocks of ciphertext as the following table shows:

| Input | Output |
| --- | --- |
| **`000`** | **`110`** |
| **`001`** | **`111`** |
| **`010`** | **`101`** |
| **`011`** | **`100`** |
| **`100`** | **`011`** |
| **`101`** | **`010`** |
| **`110`** | **`000`** |
| **`111`** | **`001`** |

- These 3 bits can represent ***2<sup>3</sup> = 8*** pieces of informations. There are ***8! = 40,320*** possible mappings with these 3 bits. Each one of the 8 mappings shown in the table above is a key that Alice and Bob can use to encrypt and decrypt the exchanged messages.
- 3-bit block mappings can be easily cracked, but larger blocks such as 46-bit blocks are extremely hard to crack. The problem, though, with large blocks is that they require really huge tables of predetermined mappings which is unfeasible.
- The alternative is to "use functions that simulate randomly permuted tables." The following figure shows how one of such functions work. The function first divides a larger block of 64 bits into 8 smaller bits of 8-bit length each. Each 8-bit block is mapped using an 8-bit to 8-bit table (just as we described earlier, *2<sub>8</sub> = 256* is a manageable table size). These 8 8-bit chunks are then reassembled into a new 64-bit block. (*Not very clear, but it says: "The positions of the 64 bits in the block are then scrambled (permuted) to produce a 64-bit output"* :confused:). This 64-bit output is then fed back to the function and another cycle begins. After *n* cycles, the function outputs the final ciphertext. The repeated rounds affect most if not all the bits of the original 64-bit input. If we apply only one round to the cleartext, that would only affect only 8-bits groupings within the 64-bit block and it would be easy to crack it. The key to this ciphertext is the 8 8-bit mapping tables, and the scramble function is publicly known.
![Block cipher](img/blockCipher.png)
- Popular block ciphers in use today include *data encryption standard (DES)* and *advanced encryption standard (AES)* which are very hard to crack.

#### Cipher-Block Chaining:
- The problem with block ciphers is that they are used to encrypt messages containing repeated patterns such as `HTTP/1.1`. Malicious actors can exploit this knowledge and other pieces of knowledge about the messages and might even be able to crack the whole message. 
- The solution to this problem is to mix in some randomness into the ciphertext to allow identical plaintext blocks to produce different ciphertext blocks. 
- Some random numbers are generated and combined with the ciphertext to scramble identical patterns in the message.
- *I won't into more detail! Cryptography needs its own book, and maybe someday I'll read one! For the moment, we at least have a general idea about how how symmetric-key encryption works and some of the challenges it needs to respond to.*

### Public Key Encryption:
- Before Alice and Bob can exchange secure messages, they need to agree to a common key they use to encrypt and decrypt the messages. In olden days, they'd meet and agree upon a shared key, but this is not the case anymore in our networked world, Alice and Bob might never meet but will still need to exchange messages in a secure manner? If they exchanged the keys, Trudy will easily break their encryption. Can Alice and Bob encrypt and decrypt the messages they exchange without first sharing a common secret key? 
- In 1976, the brainiacs Diffie and Hellman gave use the **Diffie-Hellman key exchange** algorithm which allows Alice and Bob to exchange secure encrypted messages without having shared secret key in advance. This was the basis for modern public key cryptography systems. These systems are the backbone of today's network security and are used not only for encryption, but also for authentication and digital signatures.
- The following figure shows how public key cryptography works:
![Public key cryptography](img/publicKeyEnc.png)
- If Alice wants to send a message to Bob, Bob needs to have two keys:
	- A **public key** known by the whole world.
	- A **private key** know by Bob only.
- Anybody, including Alice, who wants to send a message to Bob can encrypt the message with the public key. Only Bob can decrypt the message with his private key.
- Let's call Bob's public key ***K<sup>+</sup><sub>B</sub>*** and his private key ***K<sup>-</sup><sub>B</sub>***. To send a message ***m*** to Bob, Alice first obtains his public key and some standard encryption algorithm, and computes ***K<sup>+</sup><sub>B</sub>(m)***. Bob on his part, decrypts the received encrypted message by computing ***K<sup>-</sup><sub>B</sub>(K<sup>+</sup><sub>B</sub>(m))***. There are techniques and algorithms that allow ***K<sup>-</sup><sub>B</sub>(K<sup>+</sup><sub>B</sub>(m)) = m***. This allows the two parties to exchange secure messages without having to first exchange secret keys.
- There are two problems so far with public-key cryptography:
	1. Trudy knows both the public key and the encryption algorithm, so she can mount a chosen-plaintext attack. *I am aware of how this can break a symmetric key, but not really sure, however, how it works on a private key.* Anyways, the authors suggest that selecting keys and encryption/decryption should be done in such a way as to make it impossible or very hard to find the private key or guess the contents of a sent message.
	2. Trudy and anyone really can masquerade as Alice, and gets Bob to say things that are supposed to be secret or do things he is not supposed to do. With symmetric key, knowing the secret itself implicitly identifies the sender, but with public keys that anybody knows, it's easy for intruders to masquerade as Alice. This is actually solved using a digital signatures which bend the sender to the message. We'll see this in a later section

#### RSA:
- Several algorithms have immersed to deal with the two problems mentioned earlier, but **RSA** named after its inventors Ron Rivest, Adi Shamir, and Leonard Adleman, reigns supreme as the most popular public-key encryption algorithm.
- I think the details of RSA are at best confusing to a feeble-minded mortal like me. Let's just say that it's extremely hard to break RSA so far, and there are no easy ways to break it so far!
- The problem with RSA is that it's slower than symmetric keys, so it can be time consuming to encrypt a large amount of data using RSA. The solution to this is to exchange symmetric keys like AES using RSA, and then use AES to exchange data. Such symmetric key is called a **session key**, I think its use is limited to a single session and it changes from session to session.

## Message Integrity and Digital Signatures:
- **Message integrity** means the message:
	1. Came from the actual sender who claims to have sent it.
	2. Hasn't been tampered with in transit.

### Cryptographic Hash Functions:
- A hash functions takes an input ***m*** and outputs a fixed-size string ***H(m)*** known as a hash. A **cryptographic hash functions** must also behave in such a way that it is very hard for two messages produce the same hash. This means the intruder cannot replace a message by a different message that has the same hash. Examples of cryptographic hash functions considered strong include **MD5** and **SHA-1**. I am not sure if these are still considered strong!

### Message Authentication Code:
- Let's have a look a naive flawed scenario where hashes are used to preserve message integrity:
	1. Alice computes the hash ***H(m)*** of message ***m*** using SHA-1.
	2. Alice appends ***H(m)*** to ***m*** thus creating an extended message ***(m, H(m))*** and sends this extended message to Bob.
	3. Bob receives the extended message ***(m, h)***, calculates ***H(m)***, and if ***H(m) = h*** then all is fine.
- There is a problem with this scenario. Trudy can take the message, strip the hash from the extended message, change the message and calculate her own hash and appends it to the message and sends it to Bob. Trudy can also create her own bogus messages and send them to Bob and Bob wouldn't suspect a thing.
- To really preserve message integrity using a hashing function, Alice and Bob need to first have a shared secret key called an **authentication key** which can be used in the following fashion:
	1. Alice concatenates  the authentication key ***s*** to the message ***m*** to get ***m + s***, and calculate the results hash ***H(m + s)***. This hash ***H(m + s)*** is called the **message authentication code**.
	2. Alice appends the MAC to the message to create the extended message ***(m, H(m + s))*** and sends that to Bob.
	3. Bob who knows the authentication key ***s***, receives the extended message ***(m, h)***. He calculates the MAC ***H(m + s)***. If ***H(m + s) = h*** then everything is fine
- One popular standard for MAC is the so-called **HMAC**.
- Message integrity is a separate topic from message confidentiality even though they usually go together. There are information that are public by nature such as routing information exchanged by routers. Routing information need not be secret, but it must be integral and not tampered with.

### Digital Signatures:

## End-Point Authentication:
## Securing E-Mail:
## Securing TCP connection with TLS/SSL:
## Network Layer Security, IPsec and VPNs:
## Securing Wireless LANs:
## Operational Security, Firewalls and Intrusion Detection Systems: