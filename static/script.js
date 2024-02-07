function add_news(data){
  var hold = document.getElementById("news");
  //console.log(data);
  for (var [key, value] of Object.entries(data)) {
    //console.log(key, value);
    var item = addNews(key,value);
    hold.insertBefore(item, hold.childNodes[0]);
    //hold.appendChild(item);
  }
}


function addNews(id,data){
  //unpacking data
  var src = data["image"];
  var title = data["title"];
  var desc = data["description"];

  //creating the objects
  var news = document.createElement("div");
  news.setAttribute("class","card c1");
  news.setAttribute("onclick",`location.href='/article/${id}'`);
  news.setAttribute("style",`background-image: linear-gradient(rgba(0,0,0,0.6),rgba(0,0,0,0.6)),url('${src}')`);

  var det = document.createElement("div");
  det.setAttribute("class","details");

  news.appendChild(det);
  
  var det2 = document.createElement("div");
  det2.setAttribute("class","overlay");
  det.appendChild(det2);

  var det3 = document.createElement("div");
  det3.setAttribute("class","details2");
  det2.appendChild(det3);

  var titl = document.createElement("h4");
  titl.setAttribute("class","mainNewsTitle");
  titl.innerHTML = title;
  det.appendChild(titl);

  titl = document.createElement("h4");
  titl.innerHTML = title;
  det3.appendChild(titl);

  var con = document.createElement("p");
  con.setAttribute("class","readmore");
  con.innerHTML = "Read More";

  det3.appendChild(con);

  return news;
}


function add_clubs(data){
  var hold = document.getElementById("clubs");
  //console.log(data);
  for (var [key, value] of Object.entries(data)) {
    //console.log(key, value);
    var item = addMember(key,value);
    //hold.insertBefore(item, hold.childNodes[0]);
    hold.appendChild(item);
  }
}


function addMember(id,data){
  //unpacking data
  var src = data["image"];
  var title = data["title"];
  var nam = data["name"];
  var desc = data["description"];

  //creating the objects
  var news = document.createElement("div");
  news.setAttribute("class","card c1");
  news.setAttribute("style",`background-image: linear-gradient(rgba(0,0,0,0.4),rgba(0,0,0,0.4)),url('${src}')`);

  var det = document.createElement("div");
  det.setAttribute("class","details");

  news.appendChild(det);

  var det2 = document.createElement("div");
  det2.setAttribute("class","overlay");
  det.appendChild(det2);

  var det3 = document.createElement("div");
  det3.setAttribute("class","details2");
  det2.appendChild(det3);

  //var titl = document.createElement("h4");
  //titl.setAttribute("class","mainNewsTitle");
  //titl.innerHTML = title;
  //det.appendChild(titl);

  titl = document.createElement("h4");
  titl.innerHTML = title;
  det3.appendChild(titl);

  titl = document.createElement("h5");
  titl.innerHTML = nam;
  det3.appendChild(titl);

  var con = document.createElement("p");
  //con.setAttribute("class","readmore");
  con.innerHTML = desc;

  det3.appendChild(con);

  return news;
}

function addMember2(id,data){
  //unpacking data
  var src = data["image"];
  var title = data["title"];
  var nam = data["name"];
  var desc = data["description"];

  //creating the objects
  var news = document.createElement("div");
  news.setAttribute("class","card c1");
  news.setAttribute("style",`background-image: linear-gradient(rgba(0,0,0,0.4),rgba(0,0,0,0.4)),url('${src}')`);

  var det = document.createElement("div");
  det.setAttribute("class","details");

  news.appendChild(det);

  var det2 = document.createElement("div");
  det2.setAttribute("class","details2");
  det.appendChild(det2);

  var titl = document.createElement("h4");
  titl.innerHTML = title;

  var name = document.createElement("h5");
  name.innerHTML = nam;

  det2.appendChild(titl);
  det2.appendChild(name);

  var con = document.createElement("p");
  con.innerHTML = desc;

  det2.appendChild(con);

  return news;
}

function loadarticle(data) {
  var title = document.getElementById("title");
  var cont = document.getElementById("cont");

  var banner = document.getElementById("banner");
  banner.style.backgroundImage = `linear-gradient(rgba(0,0,0,0.75),rgba(0,0,0,0.75)),url('${data["image"]}')`;
  title.innerHTML = data["title"];
  cont.innerHTML = data["description"];
}


function storeItems(items){
  console.log(items.length);
  var holder = document.getElementById("items");
  holder.innerHTML = "";
  for(var i in items){
    var item = document.createElement("div");
    item.setAttribute("class","card c1");
    item.style.backgroundImage = `linear-gradient(rgba(0,0,0,0.4),rgba(0,0,0,0.4)),url('${items[i]["icon"]}')`;

    var det = document.createElement("div");
    det.setAttribute("class","details");
    item.appendChild(det);

    var de = document.createElement("div");
    de.setAttribute("class","details2");
    det.appendChild(de);

    var h4 = document.createElement("h4");
    h4.innerHTML = items[i]["title"];
    de.appendChild(h4);

    var p = document.createElement("p");
    p.innerHTML = items[i]["description"];
    de.appendChild(p);

    holder.appendChild(item);
  }
}

var token;
function setToken(toke){
  token=toke;
}

var mapData;
var userinfo;
function setupMap(data){
  mapData = data;
  var map =document.getElementById("map");
  var children = map.children;
  for (var i = 0; i < children.length; i++) {
    var state = children[i];
    state.setAttribute("onclick",`stateInfo(${state.id})`);
  }
}

function stateInfo(id){
  var stateData = mapData[id];
  //grabbing html elements
  var state = document.getElementById(id);
  var title = document.getElementById("title");
  title.innerHTML = stateData["State"];

  //where the state details will be held
  var det = document.getElementById("statedet");
  //resetting it as on a new click old elements need removing
  det.innerHTML = "";

  //looping over all state info
  for(let key in stateData){
    //checking if key is state
    if(key=="State"){
      continue;
    }
    else{
      var p = document.createElement("p");
      p.innerHTML = `<b>${key}:</b> ${stateData[key]}`;
      det.appendChild(p);
    }
  }
}