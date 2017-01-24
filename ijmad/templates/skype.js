function renderSkype() {
  Skype.ui({ "name": "call",  "element": "SkypeButtonHidden", "participants": ["{{SKYPE_NAME}}"] });
}

function callSkype() {
  $('p#SkypeButtonHidden_paraElement a').click();
}