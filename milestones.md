# Milestone 3

## Video 
[Link to video](https://youtu.be/8lus37fdeNo)

## Contribution
### Anthony Yang
* Done: Implemented the node infrastructure under Ethan's instructions.
* TODO: Implementation so that nodes can communicate with each other.
* BLOCK: Same as TODO.
* [Link to commits](https://github.com/ECS153/final-project-group-catch-me-if-you-can/commit/58c61ea18b14b9a10848bde229fbaa23933c39c2)
* [Link to updated node design doc](https://docs.google.com/document/d/1dbC9gJvCgyTVsaopRKNBOPJZnjFKXFHqV19T7Wt-1sw/edit?usp=sharing)
### Scott Lorentzen
* Done: Implemented JavaScript AES/RSA hybrid encryption on client side, and python decryption within the mixnet nodes. Also added python AES/RSA encryption on mixnet nodes to allow for the generation of noise. Wrote some bash automation scripts to make the server/nodes startup much easier.
* TODO: Still need to look into gunicorn as a possible more efficient way to run the servers.
* [Link to pull request](https://github.com/ECS153/final-project-group-catch-me-if-you-can/pull/5)
* [Link to pull request](https://github.com/ECS153/final-project-group-catch-me-if-you-can/pull/8) 
### Ethan Chiang


# Milestone 2

## Video
[Link to video](https://youtu.be/ESGTRwHxJi0)

## Contribution
### Anthony Yang
* Done: Made important decisions on how to implement the node. Started writing API for the node. 
* TODO:
For the upcoming week, I will continue working on the node. At this point, I am stuck on implementing the node in a single thread point of view. (We have to decide how to hide data within the noise.)
* [Link to commits](https://github.com/ECS153/final-project-group-catch-me-if-you-can/commit/9c5b888251488bde4be9a0d1aae47fdd06086ea1)
* [Link to updated node design doc](https://docs.google.com/document/d/1dbC9gJvCgyTVsaopRKNBOPJZnjFKXFHqV19T7Wt-1sw/edit?usp=sharing)

### Scott Lorentzen
* Done: 
Implemented client generated noise. Worked on testing different encryption schemes using JavaScript and Python.
* TODO:
For the next week, I will continue working on encryption. Specifically I will implement the hybrid layered encryption using a mixture of AES and RSA encryption.  
* [Link to pull request](https://github.com/ECS153/final-project-group-catch-me-if-you-can/pull/2)  

### Ethan Chiang
* Done:
Drafted and start implementation of mixnet. Helped with Node design and implementation. Design payload format. 
* TODO:
Continue on working on mixnet, finish send and receive. Work on encryption, and make sure it works with client JS.  
* [Link to pull requests](https://github.com/ECS153/final-project-group-catch-me-if-you-can/pull/4/)
* [Link to communication design doc](https://docs.google.com/document/d/19onjzhucERwFjXTuXm8a50Hb7GHRIj3y9smZuJ6jJjg/edit?usp=sharing)
* [Link to mixnet design doc](https://docs.google.com/document/d/1b_i8GX-ESk5HST2GGUbwnlR8nmCN1DbaHudI-Lw0fNs/edit?usp=sharing)

## Link to meeting notes  
[Meeting Notes](https://docs.google.com/document/d/13nuzrEe7XipyKbtna90X-YhBOP07sIHceZHiEE8fTyI/edit?usp=sharing)

# Milestone 1

## Video
[Link to video](https://www.youtube.com/watch?v=o31LfDrhq-c&feature=youtu.be)
## Contribution

### Anthony Yang
* Done:
This week, I did research on onion routing protocols and brainstormed what I need to implement server nodes. 
* TODO:
For the upcoming week, I would start implementing the node structure. So far I am not stuck on any particular issue. 
[Link to node design doc](https://docs.google.com/document/d/1dbC9gJvCgyTVsaopRKNBOPJZnjFKXFHqV19T7Wt-1sw/edit?usp=sharing)

### Scott Lorentzen
* Done: 
Worked on the follw design doc, which outlines how the CMIYC blog should works. Started a prototypr of a blog website with Flask. 
* TODO:
For the next week, I will work on implementaion and research on what python module can be helpfull.  
[Link to pull request](https://github.com/ECS153/final-project-group-catch-me-if-you-can/pull/1)  
[Link to follow design doc](https://drive.google.com/file/d/1rimZ2-SVYcMUg2qWhu2FLg6AAwGhcq6t/view?usp=sharing)

### Ethan Chiang
* Done:
Worked on overall design of the system. More research on onion routing. Design doc of the communication protocol.
* TODO:
Learn more about Flask or maybe plan B. Look up existing onion routing code for python or JS (plan B). Start implementaion.   
[Link to design doc](https://docs.google.com/document/d/19onjzhucERwFjXTuXm8a50Hb7GHRIj3y9smZuJ6jJjg/edit?usp=sharing)




