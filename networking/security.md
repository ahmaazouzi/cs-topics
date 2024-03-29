# Security in Computer Networks
## Table of Contents:
* [Introduction](#introduction)
* [Network Security](#network-security)
* [Principles of Cryptography](#principles-of-cryptography)
	+ [Symmetric Key Cryptography](#symmetric-key-cryptography)
		+ [Caesar Cipher](#caesar-cipher)
		+ [Monoalphabetic Cipher](#monoalphabetic-cipher)
		+ [Polyalphabetic Encryption](#polyalphabetic-encryption)
		+ [Block Ciphers](#block-ciphers)
		+ [Cipher-Block Chaining](#cipher-block-chaining)
	+ [Public Key Encryption](#public-key-encryption)
		+ [RSA](#rsa)
* [Message Integrity and Digital Signatures](#message-integrity-and-digital-signatures)
	+ [Cryptographic Hash Functions](#cryptographic-hash-functions)
	+ [Message Authentication Code](#message-authentication-code)
	+ [Digital Signatures](#digital-signatures)
		+ [Public Key Certification](#public-key-certification)
* [Securing TCP connection with TLS/SSL](#securing-tcp-connection-with-tls/ssl)
		+ [Handshake](#handshake)
		+ [Key Derivation](#key-derivation)
		+ [Data Transfer](#data-transfer)
		+ [SSL Record](#ssl-record)
		+ [Actual TLS](#actual-tls)
* [Network Layer Security, IPsec and VPNs](#network-layer-security-ipsec-and-vpns)
	+ [IPsec and Virtual Private Networks (VPNs)](#ipsec-and-virtual-private-networks-(vpns))

## Introduction:
- This chapter will be mainly about secure communication over IP and how to defend it against various types of attacks.
- This chapter will use the famed characters Bob and Alice as two ends of a communication line, and might introduce other characters such as Trudy the intruder. Alice and Bob can be either two routers, a server and a client or two nodes, etc. Alice will be the sender and Bob the receiver, mostly!
- Security can mean a bunch of things, but our focus in this chapter will be about secure communication and security over the network. Topics we will cover include:
	- Communication between Alice and Bob remains secret from busybodies.
	- Bob and Alice are actually communicating with each other, and Trudy is not masquerading as one of them.
	- If communication is tampered with, the tampering is detected.
	- The fundamentals of cryptography, and how cryptography is used to to encrypt communication, authenticate communicators, and maintaining message integrity.
	- How to secure applications, TCP connections, and IP using among cryptography among other things.

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
- A **digital signature** is a cryptographic technique for indicating the owner or creator of a document, or for indicating someone's agreement with the content of a document. Digital signatures try to mimic real paper signatures in that they can prove a document was signed by a certain individual and only that individual.
- A digital signature of a document can be very easily done by simply encrypting (or signing) the message with the sender's (or owner's) private key. Anyone possessing the public key can be sure that the owner of the corresponding private key is the owner of the document. The public key can be used to unscramble the original message. Usually messages are encrypted with public keys and decrypted with private keys, but with digital signatures, messages are signed with the private key, and signatures are verified with the public keys. Basically, the public key reverses the work of the private key, the opposite is true. *This is one of those situations where math hold true regardless of the context!!*
- The problem with the approach we've described above is that encryption and decryption are expensive procedures and need to be done only when really necessary. The alternative is to compute the hash of a message (which is probably a much cheaper procedure), and then sign only the resulting fixed-length hash which is usually shorter than the original message. 
- Let's look at a scenario involving signing a document and verifying the signature:
	1. On Bob's side:
		- Bob calculates the hash ***H(m)*** of message ***m***.
		- Bob uses his private key ***K<sup>-</sup><sub>B</sub>*** to sign the document by computing ***K<sup>-</sup><sub>B</sub>(H(m))***.
		- The message along with the digital signature are sent to the Alice.
	2. On Alice's side:
		- Alice uses Bob's public key ***K<sup>+</sup><sub>B</sub>*** and extracts the original hash of Bob's message ***H(m)***.
		- Alice hashes the received message ***m*** to get ***H(m)***.
		- Alice compares the hash she has extracted from the digital signature with the hash she obtained by hashing the message and if the two match, all is OK.

#### Public Key Certification:
- Even with digital signatures, intruders can still cause damage. Trudy can masquerade as Alice and send digitally-signed messages to Bob. Bob will verify the signature and everything will pass, because Bob doesn't know which specific public key really belongs to Alice. We need to verify that such and such public key belongs to so and so.
- **Public key certification** refers to binding a public key to a particular entity and it is done by an **certification authority (CA)**. CAs validate identities and issue certificates. A CA has two roles:
	1. It verifies that an entity is who it says it is. It employs some rigorous procedures to verify identities. CAs are not angels and some might be more trustworthy than others. 
	2. When the CA verifies the identity of an entity, it creates a **certificate** which binds the public key of the entity to its identity. The certificate contains the public key along with information identifying the entity such as a name, an IP address, etc. The certificate is then digitally signed by the CA.
- Now receivers of messages only use CA certificates (which include certified public keys) to verify messages and they were sent from those claiming to have sent them. If Alice receives a message from Trudy claiming it is from Bob, Alice verifies the message using Alice's certificate to check its validity and that it's actually coming from Alice.  

## Securing TCP connection with TLS/SSL:
- **Transport layer security (TLS)**, previously called **secure sockets layer (SSL)**, provides confidentiality, data integrity, and end-point authentication to TCP connections.
- TLS is everywhere around today, and has been around since the days of Netscape. URLs starting with **`https`** rather than **`http`** use TLS.
- I will repeat this: TLS provide confidentiality, data integrity, client authentication, and server authentication.
- TLS is mostly used to secure data used by HTTP, but any application that runs over TCP can make use of TLS because it provides security to TCP rather than HTTP.
![Enhancing TCP with TLS/SSL](img/TLS.png)
- TLS is actually implemented at the application layer, because it is an API that works with sockets just like TCP's APIs. However it is a transport layer protocol. It only handles what goes in the transport layer, which obviously also affects all applications using TCP.
- This subsection will not be about the real TLS/SSL, but something the author calls almost-SSL which will be like a gentle overview of the main functionality of TLS/SSL. We will focus on how and why SSL/TLS works.
- Both almost-SSL and TLS have 3 phases: *handshake*, *key derivation*, and *data transfer*. We will describe these three phases in the context of a communication session between Bob (the client) and Alice (the server). Alice has a private/public key pair and certificate binding her to her public key.

#### Handshake:
- During an almost-SSL handshake, 3 things happen:
	1. Bob establishes a TCP connection with Alice.
	2. Bob verifies that Alice is really Alice.
	3. Bobs sends Alice a master secret key.
- The following figures shows what happens during an almost-SSL handshake:
![An almost-SSL handshake](img/almostSSLHandshake.png)
- After a TCP connection is established Bob sends Alice a "hello" message. Alice responds with a certificate containing her public key. Bob then generates a master secret (MS) key that will be used only in this almost-SSL session. Bob then encrypts this MS key with Alice's certified public key to produce an encrypted master secret (EMS) key, and sends the the EMS to Alice. Alice then decrypts the EMS to get the MS. At this moment both Bob know the MS key for this SSL session.

#### Key Derivation:
- Bob and Alice can now probably use the MS to probably encrypt and data-integrity check all subsequent messages in the almost-SSL session. However it's considered safer for Bob and Alice to each use different keys for encryption and data integrity checking. The MS could be sliced into 4 slices, but real SSL uses more complex schemes to generate the 4 keys for the SSL session. These 4 keys are:
	- ***E<sub>B</sub>*** is used to encrypt data sent from Bob to Alice.
	- ***M<sub>B</sub>*** is the session MAC key for data sent from Bob to Alice.
	- ***E<sub>A</sub>*** is used to encrypt data sent from Alice to Bob.
	- ***M<sub>A</sub>*** is the session MAC key for data sent from Alice to Bob.
- The four keys are all derived from the MS. E keys will be used to encrypt messages to be sent, and MAC keys will be used to check the integrity of received data. MAC keys are the keys used to generate the MAC of each message, not the MACs themselves. Each message has its own MAC.

#### Data Transfer:
- Both Alice and Bob now possess the four session keys, so they can start exchanging secure data over the TCP connection. TCP is a byte-stream protocol so maybe data can be encrypted first and then sent to TCP, but there is an issue of where MACs would be placed!! :confused: *I am not really sure why this is a problem, why wouldn't every segment have its own MAC (data + MAC inside the segment)??!! Maybe, it's the fact something like a large JPEG will be broken into multiple TCP segments, and the same segment might have a fragment of a JPEG, and the start of a text??!!! Who knows!!?*.
- Anyways, networking nerds did what they do best which breaking everything into packets of sorts. SSL divides a data stream into records, appends a MAC to each record for integrity checking and then encrypts the whole record+MAC. The sender uses a hashing algorithm to hash the record along with the MAC key to produce the data's MAC. The record along the MAC are encrypted with the encryption key, and then sent away.
- This is good so far, but Trudy can still do cause some damage. She can intercept Alice and Bob's communication, delete some segments, reverse the order of some or modify some segment sequence numbers. This can be done because TCP is not encrypted. SSL only encrypt SSL payloads which are the SSL records.
- The solution to this problem is the use of a form of sequence number. The sender maintains a sequence number counter which starts at 0 which is incremented for each record it sends. The sequence number is not included in the record. Instead, the MAC of each record is achieved by calculating the hash of data + MAC key + sequence number. The receiver keeps track of the sender's sequence numbers, so when verifying the MAC it includes the correct sequence number. If this doesn't match, it senses foul play.  

#### SSL Record:
- The following figure shows the format of an SSL and almost-SSL record:
![Format of SSL record](img/SSLrecord.png)
- Notice the first three fields of the record are not encrypted.
- Some of these fields are:
	- The **type field** used to indicate whether the record is a handshake message or one used for carrying application data. It's also used for closing a an SSL connection.
	- The **length** field is used for extracting the SSL record out of the TCP byte stream.

#### Actual TLS:
- Almost-SSL largely does what actual TLS does. A few things that actual TLS does include the fact that at the beginning of a handshake, the client sends to the a list of server symmetric key algorithms, public key algorithms, and a MAC algorithms that it supports. The server chooses one and tells the client about it. The client and server also uses nonces ("A nonce is a number that a protocol will use only once in a lifetime. That is, once a protocol uses a nonce, it will never use that number again.") Nonces are used in the MACs in order to prevent replay attacks, where an intruder comes at a later time and resends segments they've captured in the past from a previous session.
- The type field in an SSL record can be used to prevent a so-called **truncation attack**, where Trudy sends a TCP FIN segment which maliciously closes the the connection before the exchange actually ends. If the receiver receives a TCP FIN before an SSL closure record (which needs to be indicated in the type field), it concludes that something fishy is going on!

## Network Layer Security, IPsec and VPNs:
- **IP security (IPsec)** protocol provides security at the network layer. IPsec provides security to datagrams between any 2 network-layer entities be they routers or hosts. Organizations have also figured to exploit IPsec in order to create **virtual private networks (VPNs)** that run over the Internet.
- IPsec provide "blanket coverage" confidentiality. Datagram payload is encrypted, so all UDP, TCP, ICMP is protected against sniffers. As a result all application-level data is also protected. IPsec can potentially even provide data integrity and end-point authentication.

### IPsec and Virtual Private Networks (VPNs):
- Large organizations like companies with multiple branches wish to have their own private networks for security reasons and to hide their internal communication details from prying eyes. They can do this creating their own physical **private networks** with links and routers that are totally separate from the public Internet, but this would be very costly and maybe not really worth it. Instead such organizations create **virtual private networks (VPNs)** that make use of the existing public Internet but still preserve confidentiality. Different branches of the organization are connected to the public Internet, but before their traffic enter the Internet it is encrypted using IPsec. As the following diagram shows, withing a network/branch belonging to the organization, nodes can exchange good old IPv4 datagrams, but any datagrams leaving a branch to another branch needs to be encrypted using IPsec before going to the public Internet.
- An IPsec datagrams is a regular datagram with regular IP headers used for forwarding the datagram to its destination. Its payload includes an IPsec header used for IPsec processing. The payload of the IPsec datagram is encrypted.
