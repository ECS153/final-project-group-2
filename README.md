# final-project-group-catch-me-if-you-can
## Author: Ethan Chiang, Scott Lorentzen, Anthony Yang

## Layout

The main files are shown below. There are some extra test files and setup scripts that aren't shown.

```
.
├── src
│   ├── static
│   │   ├── blog.js	// Client Encryption/Sending Messages
│   │   └── main.css	// CSS for Client Web Page
│   ├── templates
│   │   ├── blog.html	// Client Web Page
│   │   └── layout.html	// Client Web Page (Used by blog.html)
│   ├── database.db
│   ├── info.md         // Some information on how to run the mixnet
│   ├── node.py		// Mixnet Node (working_cycle, cyrptography, noise genration) 
│   ├── server.py	// Main Server (DB updates)
│   └── startNodes.sh	// Script to Run Mixnet and Server
├── design_docs.md
├── milestones.md
├── proposal.md
└── README.md

```

## Summary
In this project, we aim to build a platform that allows users to post messages without revealing their identity. To achieve this, we included two key features: 
1. Adding noise to network traffic(adapted from Vuvuzela) 
2. Using onion routing/mixing network(adapted from the Tor Browser). 

These two features assure backtracking to be exponentially difficult. Note: all traffic is secure viz a hybrid crytography scheme (RAS + ASE).  
The end results of this project is a functional and scalable web app model with gerenteed security of the users identity. 

## [Link to slides](https://docs.google.com/presentation/d/1glpboxsZlmwQH7JLTD6uXKMujV2Kes6WO-e2QnHRcnE/edit?usp=sharing)
