function storeVal() {
	console.log("3");
  // these lines need to be modified for each website
	var name = document.getElementsByClassName("article-composition pdp-description-list-item");
  var name2 = name.getElementsByClassName("details-list-item")[0];
  console.log(name2)
	console.log(name)
	chrome.storage.local.set({"company": name }, function() {
	          console.log('company is set to ' + name);
	        });



}

console.log("1");
storeVal();
