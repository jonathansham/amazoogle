function setup() {
  noCanvas()
  let userinput = select('#userinput');
  userinput.input(newText);

  function newText() {
    chrome.tabs.getCurrent(gotTab);

    function gotTab() {
    //send a message to the content script
    let message = userinput.value();
    let msg = {
      txt: "hello"
    }
    chrome.tabs.sendMessage(tab.id, msg);
  }
}
