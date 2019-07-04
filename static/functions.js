class InfoContainer {
    constructor(gameInfo) {
        //Splits up the game into into it's components

        //Separate them by getting the even and odd keys. 
        //Then divide both by half and round down to get it's turn. 
        //For evens just divide by half, for odd subtract one then divide

        this.player1 = {};
        this.player2 = {};

        this.turnNum1 = 0;
        this.turnNum2 = 0;

        for (var num = 0; num < Object.keys(gameInfo).length; num++) {
            
            if (num % 2 === 0) {
                this.player1[num / 2] = gameInfo[num];
            }
            else {
                this.player2[(num - 1) / 2] = gameInfo[num];
            }
        }
    }

    //Returns the info for the player at this specific turn number
    //If max turn is reached, returns none
    princat(player) {
        var info = null;

        if (player === 0) {
            if (this.turnNum1 in this.player1) {
                info = this.player1[this.turnNum1];
            }
        }
        else {
            if (this.turnNum2 in this.player2) {
                info = this.player2[this.turnNum2];
            }
        }
        return info;
    }

    incr(player) {
        if (player === 0) {
            if (this.turnNum1 + 1 in this.player1) {
                this.turnNum1 += 1;
            }
        }
        else {
            if (this.turnNum2 + 1 in this.player2) {
                this.turnNum2 += 1;
            }
        }
    }

    decr(player) {
        if (player === 0) {
            if (this.turnNum1 !== 0) {
                this.turnNum1 -= 1;
            }
        }
        else {
            if (this.turnNum2 !== 0) {
                this.turnNum2 -= 1;
            }
        }
    }
}

var turnNum = -1;

var game;

function initiateSetup(jsonfile) {
    document.getElementById("Board").innerHTML = "";
    game = new InfoContainer(jsonfile);

}

function increment(player) {
    game.incr(player);
    display(player);
}

function decrement(player) {
    game.decr(player);
    display(player);
}

function display(player) {
    var info = game.princat(player);

    var board = document.getElementById("Board");
    board.innerHTML = "";

    var turnNum = document.getElementById("TurnNum");
    turnNum.innerHTML = "Turn number: " + game.turnNum2;

    var turnNum = document.getElementById("ProductionRoll");
    turnNum.innerHTML = "Production Roll: " + game.turnNum2;

    var turnNum = document.getElementById("TurnNum");
    turnNum.innerHTML = "Turn number: " + game.turnNum2;

    for (var i = 0; i < 5; i++) {
        var row = document.createElement("div");
        row.classList.add("row");

        for (var j = 0; j < 17; j++) {


            var slot = document.createElement("div");
            var ty = game.princat(player)["Princ"][i][j];

            if (ty["Type"] === undefined) {
                slot.innerHTML = " ";
            }
            else {
                if ("Amount" in ty) {
                    slot.innerHTML = ty["Number"] + " " + ty["Type"] + " " + ty["Amount"];
                }
                else {
                    slot.innerHTML = ty["Type"];
                }
                
            }
            
            slot.classList.add("slot");
            //console.log(game.princat(player)["Princ"][0])
            row.appendChild(slot);
        }
        board.appendChild(row);
    }
    


}