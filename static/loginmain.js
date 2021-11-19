document.getElementById("myBtn").addEventListener("click", function() {
	document.getElementById("myBtn").style.visibility = "hidden";

    var start = new Date().getTime();
    var score = 0;
    var x = 0;
    var z = 0;
    var total = 0;
    var average = 0;
    var max_width = document.getElementById('bounding-ct').getBoundingClientRect().width
    var ending = 0;
    var tries =1;
    var average1 =0;

    var clear = document.getElementById("clear").value;


    function getRandomColor() {
        var letters = '0123456789ABCDEF'.split('');
        var color = "#";
        for (var i = 0; i< 6; i++) {
            color += letters[Math.floor(Math.random()*16)];
        }
        return color;
    }

    function doAppear() {
        var top = Math.random()*200 -100;
        var left = Math.random()*2000;
        var width = (Math.random()*25)+100;


        if(left>max_width - width){
            left = max_width - width
        }

        // Get circles
        if(Math.random()>0.5) {
            document.getElementById('shape').style.borderRadius = "50%"; //circles
            x=1;
        }
        else {
            document.getElementById('shape').style.borderRadius = "0";	//square
            x=0;
        }

        // Get Random Sized Objects
        document.getElementById('shape').style.backgroundColor = getRandomColor();
        document.getElementById('shape').style.width = width+"px";
        document.getElementById('shape').style.height = width+"px";
        document.getElementById('shape').style.top = top+"px";
        document.getElementById('shape').style.left = left+"px";
        document.getElementById('shape').style.display ="block";
        start = new Date().getTime();
    }

    function appearAgain() {
        setTimeout (doAppear,  Math.random()*2000);
    }
    appearAgain();

    function dis(){
        document.getElementById('shape').style.display = "none";
    }

    var bestTime = Infinity; // Higher Value
    // Get the Click


    document.getElementById('shape').addEventListener("click", function(){
        z++;
        ending =0;
        var end = new Date().getTime();
        var timeTaken = (end - start)/1000;
        /* document.getElementById('time').innerHTML = timeTaken + " s"; */
        dis();
        score++;

        // Get the Best Time
        if (timeTaken < bestTime) {
            bestTime = timeTaken;
            document.getElementById('best-time').innerHTML = bestTime*1000 + " ms";

            if (score <tries){
                appearAgain();
            }

        }

        else {
            document.getElementById('best-time').innerHTML = bestTime*1000 + " ms";
            if (score <tries){
                appearAgain();
            }

        }
        total += timeTaken;
        average = (total/z)
        document.getElementById('final').style.backgroundColor = '#000';
        document.getElementById('result').innerHTML = 'In Progress';
        document.getElementById('average-time').innerHTML = (average*1000).toFixed(0) +" ms";
        document.getElementById('score').innerHTML = score;
        /*	document.getElementById('tries').innerHTML = z; */

        if(score==tries){
            document.getElementById("myBtn").style.visibility = "visible";
            if(average<0.65){
                /* document.getElementById('final').style.backgroundColor = 'rgb(94, 170, 0)';*/
                document.getElementById('result').innerHTML = 'End';
                document.getElementById('clear').value = 'Pass';
                var modal = document.getElementById("myModal");
                var span = document.getElementsByClassName("close")[0];
                modal.style.display = "block";

                span.onclick = function() {
                    modal.style.display = "none";
                }

                window.onclick = function(event) {
                    if (event.target == modal) {
                        modal.style.display = "none";
                    }
                }
                // document.getElementById('line1').innerHTML = 'Yea! You Rock.';
                // document.getElementById('line2').innerHTML = 'Email us: scouting@draftwix.com';
            }

            else{
                /* document.getElementById('final').style.backgroundColor = 'rgb(255, 0, 0)';*/
                document.getElementById('result').innerHTML = 'End';
                document.getElementById('clear').value = 'Fail';
                var modal = document.getElementById("myModal");
                var span = document.getElementsByClassName("close")[0];
                modal.style.display = "block";

                span.onclick = function() {
                    modal.style.display = "none";
                }

                window.onclick = function(event){
                    if (event.target == modal){
                        modal.style.display = "none";
                    }
                }
                // document.getElementById('line1').innerHTML = 'Keen on supporting Esports Ecosystem,';
                // document.getElementById('line2').innerHTML = 'Email us: inquiries@draftwix.com';

            }

        }


    });

})

