class InfoContainer {
    constructor(gameInfo) {
        //Splits up the game into into it's components

        //Separate them by getting the even and odd keys. 
        //Then divide both by half and round down to get it's turn. 
        //For evens just divide by half, for odd subtract one then divide

        this.player1 = {};
        this.player2 = {};

        for (var num = 0; num < Object.keys(gameInfo).length; num++) {
            
            if (num % 2 === 0) {
                this.player1[num / 2] = gameInfo[num];
            }
            else {
                this.player2[(num - 1) / 2] = gameInfo[num];
            }
        }
    }

    get princat(player, turnNumber) {
        var info;

        if (player == 0) {
            info = this.player1[turnNumber]
        }
        else {
            info = this.player2[turnNumber]
        }


        

    }

}

function createInfo(gameInfo) {
    for (var i = 0; i < 5; i++) {
        //Now we want to return the html block. 
        var node = document.createElement("div");                 // Create a <div> node
        var textnode = document.createTextNode("test");         // Create a text node
        node.appendChild(textnode);                              // Append the text to <li>
        document.getElementById("row" + i).appendChild(node);
    }
    console.log(new InfoContainer(gameInfo));
}