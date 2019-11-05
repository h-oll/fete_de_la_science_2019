var num=(Math.ceil(Math.random() * 3));
var numsess = (Math.ceil(Math.random() * 1000));


var tab1=document.getElementById('tab1');
var tab2=document.getElementById('tab2');

function check(){
    var checktxt=document.getElementById('select1').value+document.getElementById('select2').value+document.getElementById('select3').value;
    var tabcheck=checktxt.split('');
    var check=parseInt(tabcheck[0])+parseInt(tabcheck[1])+parseInt(tabcheck[2]);
    var testaire="even";
    if(num==1){
        if(check % 2===1){
            document.getElementById('submit1').innerHTML="odd";
            document.getElementById('submit1').style.visibility="visible";
        } else{
            document.getElementById('submit1').innerHTML="even";
            document.getElementById('submit1').style.visibility="visible";
        }

    } else if(num==2){
        if(check % 2===1){
            document.getElementById('submit2').innerHTML="odd";
            document.getElementById('submit2').style.visibility="visible";
        } else{
            document.getElementById('submit2').innerHTML="even";
            document.getElementById('submit2').style.visibility="visible";
        }

    } else if(num==3){
        if(check % 2===1){
            document.getElementById('submit3').innerHTML="odd";
            document.getElementById('submit3').style.visibility="visible";
        } else{
            document.getElementById('submit3').innerHTML="even";
            document.getElementById('submit3').style.visibility="visible";
        }

    }
    if (tab1){
        if(check % 2===1){
            document.getElementById('subbuton').style.visibility="hidden";
        } else{
            document.getElementById('subbuton').style.visibility="visible";
        }
    }
    else if (tab2){
        if(check % 2===0){
                document.getElementById('subbuton').style.visibility="hidden";
        } else{
                document.getElementById('subbuton').style.visibility="visible";
        }
    }
}

if(tab1){
    document.getElementById('inputs').innerHTML="<input type='text' name='numline' value="+num+"><input type='text' name='numsess' value="+numsess+">";
    document.getElementById('numsess').innerHTML=numsess;
}

var tableau='';

function drawTableLine(number){
    for(i=1;i<4;i++){
        if (number==i){
            tableau += "<tr><td><select form='formp1' name='select1' id='select1' onchange='check()'><option selected='selected' value='0'>0</option><option value='1'>1</option></select></td><td><select name='select2' onchange='check()' form='formp1' id='select2'><option selected='selected' value='0'>0</option><option value='1'>1</option></select></td><td><select name='select3' onchange='check()' form='formp1' id='select3'><option selected='selected' value='0'>0</option><option value='1'>1</option></select></td></tr>";
        } else {
            tableau += "<tr><td> X </td><td> X </td><td> X </td></tr>";
        }
    } 
    return tableau;
}

function drawTableColumn(number){
    for(i=1;i<4;i++){
        tableau += "<tr>";
        for(j=1;j<4;j++){
            if(j==number){
                tableau += "<td><select onchange='check()' form='formp1' name='select"+i+"' id='select" + i + "'><option value='0'>0</option><option value='1'>1</option></select></td>";
            } else {
                tableau +="<td> X </td>";
            }
        }
    }
    return tableau;
}


if (tab1){
    var tabligne=drawTableLine(num);
    tab1.innerHTML=tabligne;
}
if (tab2){
    var tabcol=drawTableColumn(num);
    tab2.innerHTML=tabcol;
}


function changelink(){
    var inputsess= document.getElementById('idsess').value;
    document.getElementById("link").href="/player2/en?sessionid="+inputsess;
}

function getUrlVars() {
    var vars = {};
    var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function(m,key,value) {
        vars[key] = value;
    });
    return vars;
}
if(tab2){
    var sessid=getUrlVars()["sessionid"];
    console.log(sessid);
    document.getElementById('inputs').innerHTML="<input type='text' name='numline' value="+num+"><input type='text' name='numsess' value="+sessid+">";
    document.getElementById('numsess').innerHTML=sessid;
}

var items = document.getElementById('items');

if (items){
    var tbody = document.getElementById('tabw');

    var idsess= document.getElementById('idsession').innerHTML;
    var lignetxt= document.getElementById('ligne').innerHTML;
    var lignevaltxt= document.getElementById('ligneval').innerHTML;
    var coltxt= document.getElementById('col').innerHTML;
    var colvaltxt= document.getElementById('colval').innerHTML;
    var ligne = parseInt(lignetxt,10);
    var col = parseInt(coltxt,10);
    var ligneval = lignevaltxt.split('');
    var colval= colvaltxt.split('');

    var tableau=[["X","X","X"],["X","X","X"],["X","X","X"]];
    for(i=0;i<3;i++){
        tableau[ligne-1][i]=ligneval[i];
    }
    for(i=0;i<3;i++){
        tableau[i][col-1]=colval[i];
    }
    var tableauhtml="";
    for(i=0;i<3;i++){
        tableauhtml += "<tr>";
        for(j=0;j<3;j++){
            tableauhtml += "<td>"+tableau[i][j]+"</td>"
        }
        tableauhtml += "</tr>";
    }
    var tbody = document.getElementById('tabw');
    tbody.innerHTML=tableauhtml;

    var results = document.getElementById('results');
    if (results){
        document.getElementById('case').innerHTML="line "+ligne+" and column "+col;
        document.getElementById('casej1').innerHTML=ligneval[ligne-1];
        document.getElementById('casej2').innerHTML=colval[col-1];
        if(ligneval[ligne-1]==colval[col-1]){
            document.getElementById('winlose').innerHTML="won";
        } else{
            document.getElementById('winlose').innerHTML="lost";   
        }
    }
    
}

var test=1;
function opticlass(){
    var tableauopti=[[1,1,0],[1,1,0],[1,1,"X"]];
    var tableauhtmlopti="";
    for(i=0;i<3;i++){
        tableauhtmlopti += "<tr>";
        for(j=0;j<3;j++){
            tableauhtmlopti += "<td>"+tableauopti[i][j]+"</td>"
        }
        tableauhtmlopti += "</tr>";
    }
    var tbody = document.getElementById('tabw');
    if(test==1){
        tbody.innerHTML=tableauhtmlopti;
        test=0;
    } else{
        tbody.innerHTML=tableauhtml ;
        test=1;
    }
}


function showval(){
    document.getElementById('val').style.display="block";
}
function showdetails(){
    document.getElementById('moredetails').style.display="block";
}
