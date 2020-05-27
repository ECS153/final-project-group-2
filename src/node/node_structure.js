class node {
	//constructor method
	constructor(nodeID) {
		this.nodeID = nodeID; //to identify each node
		this.recievedData = [];  //a queue of nodes that
		this.privateKey; //each 
		this.queue = []; //used to store packets ready to forward to next node
	}

	//declaring a queue storing to be forward data

	//receiver
	//receives data from previous node
	//maybe add a event listener that detects if any incomming data
	reciever(){
		return; 
	}

	//parser
	parser(){
		return; 
	}

	//using standard encryption/decryption
	//encryptor
	
	//decryptor

	//sender
	//forwards data to next node
	sender(){
		return; 
	}

	//noise generator
	//start generating noise once node object is declared
	//send out packets with a random interval
	noiseGenerator(){
		return; 
	}

	//filtering out real messages from noise 
	//the filter function should only be called at last node
	//before posts are published to the interface
	filter(){
		return; 
	}

}
