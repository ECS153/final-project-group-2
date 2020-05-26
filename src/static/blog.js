
var nodes = [];
const HOST = "10.0.0.3";
const PORT = 10000;
const MAX_NUM_NODES = 10;
const INTERVAL = 200; // This is the time between messages

const SERVER_URL = 'http://' + HOST + ':5000/comment'
const NEXT_URL_PRE = 'http://' + HOST + ':';
const GET_KEYS_POST = '/getkeys';

var MIN_STRING_LENGTH = 5;
var MAX_STRING_LENGTH = 250;
var AES_KEY_SIZE = 16; // 16 bytes for AES256

var intervalTimer;
var requestPending = false;
var commentBuffer = [];
// found at https://gist.github.com/6174/6062387 for basic random string gereration
const chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";

// Retrive all of the public keys
GetPublicKeys();

// send a message at a continous rate
intervalTimer = setInterval(function() {
  // if a message is still in transit, don't send a new message
  if (requestPending) return;

  // if there are any real user posts buffered, send
  // those instead of sending noise
  if (commentBuffer.length != 0) {
    PostComment();
  }
  else { // else send a fake message
    SendNoise();
  }

  requestPending = true;
}, INTERVAL);

// Generates a pseudo-random string of given length
//  NOTE THIS IS NOT CRYPTOGRAPHICALLY SECURE RANDOMNESS
function generateRandomString(length) {
  var random_string = "";
  for (var i = 0; i < length; i++) {
    random_string += chars.charAt(Math.floor(Math.random() * chars.length));
  }
  return random_string
}

// Send a fake message
function SendNoise() {
  var randLength = Math.floor(Math.random() * (MAX_STRING_LENGTH - MIN_STRING_LENGTH) + MIN_STRING_LENGTH);
  var message = generateRandomString(randLength);
  var encryptedMessage = EncryptMessage(message, false);
  SendMessage(encryptedMessage);
}

// When the user tries to post a comment, the comment
// is buffered until the next sending interval
function BufferComment() {
  var message = document.getElementById("CommentTextBox").value;
  if (message.replace(/\s/g, '').length) {
    commentBuffer.push(message);
  }
}

function shuffleNodePath(node_path) {
  if (node_path.length == 0)
    return node_path;

  for (var i = node_path.length - 1; i > 0; i--) {
    var j = Math.floor(Math.random() * (i + 1));
    var temp = node_path[i];
    node_path[i] = node_path[j];
    node_path[j] = temp;
  }
  return node_path;
}


function generateKeyAndIV() {
  // Need a better way of generating a key, possible sending this through the PBKDF2?
  var rKey = generateRandomString(AES_KEY_SIZE);
  var key = CryptoJS.enc.Utf8.parse(rKey);
  var iv = CryptoJS.lib.WordArray.random(AES_KEY_SIZE);

  //var key = CryptoJS.enc.Utf8.parse(rKey);
  //var salt = CryptoJS.lib.WordArray.random(256/8);
  //return CryptoJS.PBKDF2(p, salt, { keySize: 512/32, iterations: 1000 });
  return [key, iv];
}

// Temporary encrypt message. Will perform the actual layered encryption
function EncryptMessage(message, is_real) {

  // this is the base message to be sent
  var jsonMsg = {'next_url': SERVER_URL, 'is_real': is_real, 'content': message};

  // shuffle the nodes
  //  NOTE would it be more random to shufle the original list each time
  //      or is it fine to just reshuffle?
  nodes = shuffleNodePath(nodes);

  // iterate over the path of nodes to generate the layered encryption
  nodes.forEach(function(next_node) {
    // Generate AES Key and IV, and encrypt the actual message
    var key_iv = generateKeyAndIV();
    var encryptedMessage = CryptoJS.AES.encrypt(JSON.stringify(jsonMsg), key_iv[0], { iv: key_iv[1] });
    encryptedMessage = key_iv[1].concat(encryptedMessage.ciphertext).toString(CryptoJS.enc.Base64);

    // Encrypt the AES key using RSA
    var encryptor = new JSEncrypt();
    encryptor.setPublicKey(next_node['key']);
    var encryptedKey = encryptor.encrypt(CryptoJS.enc.Utf8.stringify(key_iv[0]));
    while(encryptedKey.length != 344) {
      encryptedKey = encryptor.encrypt(CryptoJS.enc.Utf8.stringify(key_iv[0]));
    }
    jsonMsg = {'next_url': next_node['url'], 'content': encryptedMessage, 'key': encryptedKey};
  });

  return jsonMsg;
}

// Post the next most recent buffered comment
function PostComment() {
  var message = commentBuffer.shift();
  var encryptedMessage = EncryptMessage(message, true);
  SendMessage(encryptedMessage);
}

// Send the actual JSON message to the mixnet
function SendMessage(message) {
  var request = $.ajax({
    type: 'POST',
    url: message['next_url'],
    data: JSON.stringify(message),
    dataType: 'json',
    contentType: 'application/json'
  });
  request.done(function() {requestPending = false;});
}

// Will need to modify this as we have more mixnet nodes
//  (and in turn more public keys)
function GetPublicKeys() {
  for (var i = 0; i < MAX_NUM_NODES; i++) {
    var next_url = NEXT_URL_PRE + (PORT + i).toString() + GET_KEYS_POST;
    var request = $.ajax({
      type: 'GET',
      url: next_url,
      dataType: 'json',
      contentType: 'application/json'
    });
    request.done(function(response) {
      if (response != null) {
        nodes.push(response);
      }
    });
  }
}
