class node {
	//constructor method
	constructor(nodeID) {
		this.nodeID = nodeID; 
		this.recievedData = [];  
		this.privateKey; 
		this.queue = []; 
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
	noiseGenerator(){
		return; 
	}

}
